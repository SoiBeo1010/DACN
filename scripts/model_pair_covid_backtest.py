"""Compare model pairs on a dated market-event backtest window.

The script runs the same backtest grid once per model pair, records elapsed time
and callback-reported token usage, then writes a combined JSON and CSV summary.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cli.stats_handler import StatsCallbackHandler
from tradingagents.backtest import BacktestResult, iter_grid, summarize
from tradingagents.agents.analysts import news_analyst
from tradingagents.dataflows.symbols import safe_ticker_component
from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.graph import analyst_execution
from tradingagents.graph.trading_graph import TradingAgentsGraph


MODEL_PAIRS = [
    ("q6l_d6s", "gpt-6-luna", "gpt-6-sol"),
    ("q6l_d6l", "gpt-6-luna", "gpt-6-luna"),
]

DEFAULT_TICKERS = ["SPY", "QQQ", "NVDA"]
DEFAULT_ANALYSTS = ["news"]


def _parse_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def _summary_to_dict(summary) -> dict:
    return {
        "resolved": summary.resolved,
        "pending": summary.pending,
        "unscored": summary.unscored,
        "holding": summary.holding,
        "by_rating": {
            rating: asdict(score)
            for rating, score in summary.by_rating.items()
        },
        "rendered": summary.render(),
    }


def _is_model_unavailable(exc: Exception) -> bool:
    text = str(exc)
    return "model_price_error" in text or "has not been priced" in text


def _is_retryable_timeout(exc: Exception) -> bool:
    text = str(exc)
    return (
        "Error code: 524" in text
        or "'status': 524" in text
        or '"status": 524' in text
        or "origin_response_timeout" in text
    )


def _limit_news_tools() -> None:
    """Keep the pilot benchmark on archived news tools, not live macro extras."""
    news_only_tools = (
        news_analyst.get_news,
        news_analyst.get_global_news,
    )
    news_analyst.TOOLS = news_only_tools
    old_spec = analyst_execution.ANALYST_NODE_SPECS["news"]
    analyst_execution.ANALYST_NODE_SPECS["news"] = analyst_execution.AnalystNodeSpec(
        key=old_spec.key,
        agent_node=old_spec.agent_node,
        clear_node=old_spec.clear_node,
        report_key=old_spec.report_key,
        tools=news_only_tools,
    )


def _run_pair(
    *,
    label: str,
    quick_model: str,
    deep_model: str,
    dates: list[str],
    tickers: list[str],
    analysts: list[str],
    run_prefix: str,
    temperature: float | None,
    asset_type: str,
    retries: int,
    retry_wait_seconds: float,
    save_reports: bool,
) -> dict:
    run_id = safe_ticker_component(f"{run_prefix}_{label}")
    config = deepcopy(DEFAULT_CONFIG)
    config["llm_provider"] = "openai"
    config["quick_think_llm"] = quick_model
    config["deep_think_llm"] = deep_model
    if temperature is not None:
        config["temperature"] = temperature

    run_dir = Path(config["results_dir"]) / "backtest" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    run_config = {
        **config,
        "results_dir": str(run_dir),
        "memory_log_path": str(run_dir / "trading_memory.md"),
    }

    stats = StatsCallbackHandler()
    graph = TradingAgentsGraph(analysts, config=run_config, callbacks=[stats])
    result = BacktestResult(run_id=run_id, log_path=Path(run_config["memory_log_path"]))
    done = {(entry["ticker"], entry["date"]) for entry in graph.memory_log.load_entries()}

    pair_status = "completed"
    pair_error = ""
    started = time.perf_counter()
    for ticker in tickers:
        if pair_status != "completed":
            break
        for date in dates:
            if (ticker, date) in done:
                result.skipped += 1
                continue
            print(f"[{label}] {ticker} {date}")
            for attempt in range(retries + 1):
                try:
                    final_state, _ = graph.propagate(ticker, date, asset_type=asset_type)
                    if save_reports:
                        graph.save_reports(
                            final_state,
                            ticker,
                            save_path=(
                                run_dir
                                / "reports"
                                / safe_ticker_component(ticker)
                                / date
                            ),
                        )
                    result.cells_run += 1
                    break
                except Exception as exc:
                    if _is_model_unavailable(exc):
                        pair_status = "model_unavailable"
                        pair_error = str(exc)
                        result.failures.append((ticker, date, pair_error))
                        print(f"[{label}] model unavailable; skipping pair: {exc}")
                        break
                    if _is_retryable_timeout(exc) and attempt < retries:
                        print(
                            f"[{label}] timeout; retrying {ticker} {date} "
                            f"in {retry_wait_seconds:.0f}s ({attempt + 1}/{retries})"
                        )
                        time.sleep(retry_wait_seconds)
                        continue
                    result.failures.append((ticker, date, str(exc)))
                    print(f"[{label}] failed {ticker} {date}: {exc}")
                    break
            if pair_status != "completed":
                break

    if pair_status == "completed":
        for ticker in tickers:
            try:
                graph.settle_pending(ticker)
            except Exception as exc:
                result.settlement_failures.append((ticker, str(exc)))
                print(f"[{label}] settlement failed {ticker}: {exc}")

    elapsed_seconds = time.perf_counter() - started
    stats_snapshot = stats.get_stats()
    stats_snapshot["tokens_total"] = (
        stats_snapshot["tokens_in"] + stats_snapshot["tokens_out"]
    )

    summary = summarize(result) if result.log_path.exists() else None
    payload = {
        "label": label,
        "quick_model": quick_model,
        "deep_model": deep_model,
        "run_id": run_id,
        "run_dir": str(run_dir),
        "log_path": str(result.log_path),
        "tickers": tickers,
        "dates": dates,
        "analysts": analysts,
        "asset_type": asset_type,
        "reports_dir": str(run_dir / "reports") if save_reports else "",
        "status": pair_status,
        "error": pair_error,
        "cells_run": result.cells_run,
        "skipped": result.skipped,
        "failures": result.failures,
        "settlement_failures": result.settlement_failures,
        "elapsed_seconds": round(elapsed_seconds, 3),
        "stats": stats_snapshot,
        "summary": _summary_to_dict(summary) if summary else None,
    }

    (run_dir / "model_pair_metrics.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return payload


def _write_combined_outputs(rows: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "model_pair_summary.json").write_text(
        json.dumps(rows, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    csv_path = output_dir / "model_pair_summary.csv"
    fields = [
        "label",
        "quick_model",
        "deep_model",
        "run_id",
        "cells_run",
        "skipped",
        "failure_count",
        "settlement_failure_count",
        "status",
        "error",
        "elapsed_seconds",
        "llm_calls",
        "tool_calls",
        "tokens_in",
        "tokens_out",
        "tokens_total",
        "resolved",
        "pending",
        "unscored",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            stats = row["stats"]
            summary = row.get("summary") or {}
            writer.writerow({
                "label": row["label"],
                "quick_model": row["quick_model"],
                "deep_model": row["deep_model"],
                "run_id": row["run_id"],
                "cells_run": row["cells_run"],
                "skipped": row["skipped"],
                "failure_count": len(row["failures"]),
                "settlement_failure_count": len(row["settlement_failures"]),
                "status": row.get("status", ""),
                "error": row.get("error", ""),
                "elapsed_seconds": row["elapsed_seconds"],
                "llm_calls": stats["llm_calls"],
                "tool_calls": stats["tool_calls"],
                "tokens_in": stats["tokens_in"],
                "tokens_out": stats["tokens_out"],
                "tokens_total": stats["tokens_total"],
                "resolved": summary.get("resolved"),
                "pending": summary.get("pending"),
                "unscored": summary.get("unscored"),
            })


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run dated event-window backtests for selected OpenAI model pairs."
    )
    parser.add_argument("--start", default="2020-02-19")
    parser.add_argument("--end", default="2020-04-30")
    parser.add_argument("--every", type=int, default=5)
    parser.add_argument("--tickers", default=",".join(DEFAULT_TICKERS))
    parser.add_argument("--analysts", default=",".join(DEFAULT_ANALYSTS))
    parser.add_argument("--run-prefix", default="covid")
    parser.add_argument("--asset-type", default="stock")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--retries", type=int, default=1)
    parser.add_argument("--retry-wait-seconds", type=float, default=130.0)
    parser.add_argument(
        "--save-reports",
        action="store_true",
        help="Write per-cell Markdown report trees under each model-pair run directory.",
    )
    parser.add_argument(
        "--full-news-tools",
        action="store_true",
        help="Allow News Analyst to call macro and prediction-market tools.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the grid and model pairs without calling providers.",
    )
    args = parser.parse_args()

    dates = iter_grid(args.start, args.end, args.every)
    tickers = _parse_csv(args.tickers)
    analysts = _parse_csv(args.analysts)
    if not tickers:
        raise SystemExit("No tickers supplied.")
    if not analysts:
        raise SystemExit("No analysts supplied.")
    if "news" in analysts and not args.full_news_tools:
        _limit_news_tools()

    output_dir = Path(DEFAULT_CONFIG["results_dir"]) / "backtest" / f"{args.run_prefix}_model_pairs"
    print(f"Dates: {len(dates)} | Tickers: {len(tickers)} | Cells per pair: {len(dates) * len(tickers)}")
    print(f"Analysts: {', '.join(analysts)}")
    if "news" in analysts and not args.full_news_tools:
        print("News tools: get_news, get_global_news (macro/prediction tools disabled)")
    print(f"Output: {output_dir}")
    for label, quick_model, deep_model in MODEL_PAIRS:
        print(f"- {label}: quick={quick_model}, deep={deep_model}")

    if args.dry_run:
        return 0

    rows = []
    overall_start = time.perf_counter()
    try:
        for label, quick_model, deep_model in MODEL_PAIRS:
            rows.append(_run_pair(
                label=label,
                quick_model=quick_model,
                deep_model=deep_model,
                dates=dates,
                tickers=tickers,
                analysts=analysts,
                run_prefix=args.run_prefix,
                temperature=args.temperature,
                asset_type=args.asset_type,
                retries=args.retries,
                retry_wait_seconds=args.retry_wait_seconds,
                save_reports=args.save_reports,
            ))
            _write_combined_outputs(rows, output_dir)
    finally:
        if rows:
            _write_combined_outputs(rows, output_dir)

    print(f"Finished in {time.perf_counter() - overall_start:.1f}s")
    print(f"Wrote {output_dir / 'model_pair_summary.json'}")
    print(f"Wrote {output_dir / 'model_pair_summary.csv'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
