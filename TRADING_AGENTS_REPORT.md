# Báo Cáo Phân Tích Kiến Trúc & Luồng Hoạt Động Hệ Thống TradingAgents

## 1. Tổng Quan về Concept (Executive Summary)

**TradingAgents** là một hệ thống Multi-Agent AI được phát triển nhằm tự động hóa quy trình phân tích đầu tư và ra quyết định giao dịch tài chính (Cổ phiếu, Crypto) chuyên nghiệp tương tự mô hình vận hành của một quỹ đầu tư (Hedge Fund).

Thay vì phụ thuộc vào một mô hình ngôn ngữ đơn lẻ dễ bị định kiến hoặc sót thông tin, **TradingAgents** chia nhỏ quy trình thành các vai trò chuyên biệt, ứng dụng mô hình thảo luận nhiều chiều (Multi-Agent Debate) và tranh luận đối kháng (Bull vs Bear, Risk Debate), đồng thời kết hợp cơ chế **tự phản tư và học từ quá khứ (Reflection & Memory Log)**.

### Các điểm đặc trưng cốt lõi:
1. **Kiến trúc Multi-Agent phân cấp (Hierarchical Multi-Agent Graph):** Xây dựng trên [LangGraph](file:///d:/Huy%20Tuan%20Giang/BK/HK%20261/TradingAgents/tradingagents/graph/setup.py), đảm bảo luồng dữ liệu chặt chẽ và nhất quán.
2. **Chiến lược Dual-Tier LLM:** Phân chia công việc giữa **Quick-Thinking LLM** (xử lý thu thập tin tức, dữ liệu kỹ thuật, thảo luận nhanh) và **Deep-Thinking LLM** (suy luận sâu ở vai trò Quản lý Nghiên cứu & Quản lý Danh mục).
3. **Cơ chế Phản tư Phân kỳ (Deferred Reflection & Memory System):** Lưu lại các quyết định giao dịch, tự động đánh giá lợi nhuận thực tế (Alpha Return) sau thời gian nắm giữ, rút ra bài học kinh nghiệm để tiêm vào ngữ cảnh (context) của các lượt phân tích tiếp theo.
4. **Bảo vệ tính toàn vẹn dữ liệu (Point-in-Time Enforcement & Deterministic Identity):** Ngăn chặn rò rỉ dữ liệu tương lai trong backtest và chống hiện tượng ảo giác (hallucination) về tên/ngành nghề công ty bằng cách khóa identity thực tế từ `yfinance`.

---

## 2. Luồng Hoạt Động Tổng Thể (System Workflow Diagram)

Luồng xử lý của hệ thống trải qua 5 giai đoạn chính được biểu diễn qua sơ đồ Mermaid dưới đây:

```mermaid
flowchart TD
    Start([Khởi động: Ticker & Trade Date]) --> Init[Khóa Identity Công Ty & Tiêm Memory Log Quá Khứ]
    
    subgraph Phase1["Giai Đoạn 1: Đội Nguồn Phân Tích (Analyst Team)"]
        Market[Market Analyst\n(Chỉ báo kỹ thuật, OHLCV)]
        Sentiment[Sentiment Analyst\n(Mạng xã hội, Tâm lý)]
        News[News Analyst\n(Tin tức vĩ mô, Thị trường)]
        Fund[Fundamentals Analyst\n(Báo cáo tài chính, P/E, Ratios)]
        
        Market --> Sentiment --> News --> Fund
    end

    Init --> Phase1

    subgraph Phase2["Giai Đoạn 2: Tranh Luận Luận Điểm Đầu Tư (Research Debate)"]
        Bull[Bull Researcher\n(Bảo vệ góc nhìn Tăng)]
        Bear[Bear Researcher\n(Bảo vệ góc nhìn Giảm)]
        RManager[Research Manager - Deep LLM\n(Tổng hợp & Đưa ra Kế hoạch Đầu tư)]
        
        Bull <-->|Max Debate Rounds| Bear
        Bull --> RManager
        Bear --> RManager
    end

    Fund --> Bull

    subgraph Phase3["Giai Đoạn 3: Thiết Lập Kế Hoạch Giao Dịch"]
        Trader[Trader Agent\n(Chuyển luận điểm thành Kế hoạch Giao dịch cụ thể)]
    end

    RManager --> Trader

    subgraph Phase4["Giai Đoạn 4: Tranh Luận Quản Trị Rủi Ro (Risk Management Debate)"]
        Aggressive[Aggressive Analyst\n(Ưu tiên Lợi nhuận/Tăng trưởng)]
        Conservative[Conservative Analyst\n(Bảo vệ Vốn/Bảo thủ)]
        Neutral[Neutral Analyst\n(Cân bằng Risk/Reward)]
        
        Aggressive --> Conservative --> Neutral -->|Max Risk Rounds| Aggressive
    end

    Trader --> Aggressive

    subgraph Phase5["Giai Đoạn 5: Ra Quyết Định Cuối Cùng & Lưu Ký"]
        PM[Portfolio Manager - Deep LLM\n(Tổng hợp Risk + Plan + Memory Context + Portfolio Context)]
        Decision[Quyết định Giao dịch Cuối cùng\nBuy / Overweight / Hold / Underweight / Sell]
        LogDisk[Ghi JSON State & Trading Memory Log]
        
        Neutral --> PM
        PM --> Decision
        Decision --> LogDisk
    end

    subgraph Phase6["Giai Đoạn Phản Tư Sau Nắm Giữ (Deferred Reflection / Settlement)"]
        Settle[Tính Alpha Return sau N ngày]
        Reflect[Reflector Agent đánh giá bài học]
        LogUpdate[Cập nhật Memory Log cho các lượt phân tích tương lai]
        
        Settle --> Reflect --> LogUpdate
    end
```

---

## 3. Chi Tiết Các Vai Trò Agent Trong Hệ Thống

Các Agent được định nghĩa chi tiết tại thư mục [tradingagents/agents](file:///d:/Huy%20Tuan%20Giang/BK/HK%20261/TradingAgents/tradingagents/agents):

### 3.1. Nhóm Chuyên Viên Phân Tích (Analyst Team)
| Agent | File Mã Nguồn | Chức Năng & Công Cụ (Tools) |
| :--- | :--- | :--- |
| **Market Analyst** | [market_analyst.py](file:///d:/Huy%20Tuan%20Giang/BK/HK%20261/TradingAgents/tradingagents/agents/analysts/market_analyst.py) | Phân tích xu hướng giá, hỗ trợ/kháng cự, chỉ báo kỹ thuật (RSI, MACD, Moving Averages, Bollinger Bands). Gọi các tool: `get_stock_data`, `get_indicators`, `get_verified_market_snapshot`. |
| **Sentiment Analyst** | [sentiment_analyst.py](file:///d:/Huy%20Tuan%20Giang/BK/HK%20261/TradingAgents/tradingagents/agents/analysts/sentiment_analyst.py) | Phân tích tâm lý đám đông, xu hướng thảo luận trên mạng xã hội và cộng đồng nhà đầu tư. Gọi tool `get_sentiment`. |
| **News Analyst** | [news_analyst.py](file:///d:/Huy%20Tuan%20Giang/BK/HK%20261/TradingAgents/tradingagents/agents/analysts/news_analyst.py) | Theo dõi sự kiện kinh tế vĩ mô, tin tức doanh nghiệp, ngành hàng. Gọi tool `get_news`. |
| **Fundamentals Analyst** | [fundamentals_analyst.py](file:///d:/Huy%20Tuan%20Giang/BK/HK%20261/TradingAgents/tradingagents/agents/analysts/fundamentals_analyst.py) | Đánh giá sức khỏe tài chính: Bảng cân đối kế toán, P/E, P/B, dòng tiền, nợ nần, tăng trưởng doanh thu/lợi nhuận. Gọi tool `get_fundamentals`. |

*Đặc điểm thiết kế:* Mỗi Analyst chạy theo quy trình Tool-calling loop. Sau khi hoàn thành báo cáo chuyên sâu, node xóa toàn bộ tin nhắn scratchpad tạm thời (`create_msg_delete`) để tránh làm dầy context window cho các Agent phía sau.

### 3.2. Nhóm Nghiên Cứu Luận Điểm (Research Team)
- **Bull Researcher** ([bull_researcher.py](file:///d:/Huy%20Tuan%20Giang/BK/HK%20261/TradingAgents/tradingagents/agents/researchers/bull_researcher.py)): Tổng hợp dữ liệu từ 4 báo cáo analyst để đưa ra luận điểm tăng giá (Bullish Thesis) mạnh mẽ nhất, tìm kiếm động lực tăng trưởng và cơ hội.
- **Bear Researcher** ([bear_researcher.py](file:///d:/Huy%20Tuan%20Giang/BK/HK%20261/TradingAgents/tradingagents/agents/researchers/bear_researcher.py)): Đóng vai trò đối kháng, chỉ ra rủi ro tiềm ẩn, định giá đắt đỏ, áp lực cạnh tranh hoặc yếu tố vĩ mô bất lợi (Bearish Thesis).
- **Research Manager** ([research_manager.py](file:///d:/Huy%20Tuan%20Giang/BK/HK%20261/TradingAgents/tradingagents/agents/managers/research_manager.py)): Sử dụng **Deep-Thinking LLM**. Đóng vai trò trọng tài cân bằng hai luận điểm Bull/Bear, giải quyết mâu thuẫn dữ liệu và đưa ra **Kế hoạch Đầu tư (`investment_plan`)**.

### 3.3. Nhóm Thiết Lập Chiến Lược (Trader)
- **Trader** ([trader.py](file:///d:/Huy%20Tuan%20Giang/BK/HK%20261/TradingAgents/tradingagents/agents/trader/trader.py)): Tiếp nhận kế hoạch đầu tư từ Research Manager và cụ thể hóa thành **Kế hoạch Giao dịch (`trader_investment_plan`)** bao gồm mức giá vào lệnh (entry), mục tiêu chốt lời (target exit), cắt lỗ (stop-loss) và khung thời gian dự kiến.

### 3.4. Nhóm Quản Trị Rủi Ro (Risk Management Team)
- **Aggressive Analyst** ([aggressive_debator.py](file:///d:/Huy%20Tuan%20Giang/BK/HK%20261/TradingAgents/tradingagents/agents/risk_mgmt/aggressive_debator.py)): Đề xuất quy mô vị thế lớn, tối ưu hóa lợi nhuận khi có tín hiệu mạnh.
- **Conservative Analyst** ([conservative_debator.py](file:///d:/Huy%20Tuan%20Giang/BK/HK%20261/TradingAgents/tradingagents/agents/risk_mgmt/conservative_debator.py)): Đặt sự an toàn của vốn lên hàng đầu, đề xuất siết chặt stop-loss và hạ tỷ trọng nếu rủi ro cao.
- **Neutral Analyst** ([neutral_debator.py](file:///d:/Huy%20Tuan%20Giang/BK/HK%20261/TradingAgents/tradingagents/agents/risk_mgmt/neutral_debator.py)): Đóng vai trò trung dung, dung hòa góc nhìn lợi nhuận và rủi ro.

### 3.5. Giám Đốc Phụ Trách Danh Mục (Portfolio Manager - CIO)
- **Portfolio Manager** ([portfolio_manager.py](file:///d:/Huy%20Tuan%20Giang/BK/HK%20261/TradingAgents/tradingagents/agents/managers/portfolio_manager.py)): Sử dụng **Deep-Thinking LLM**. Đưa ra quyết định giao dịch cuối cùng (`final_trade_decision`).
  - Phân tích đồng thời: Kế hoạch của Trader + Kết quả thảo luận Risk Debate + Ngữ cảnh danh mục hiện tại (`portfolio_context`) + Bài học từ quá khứ (`past_context`).
  - Phát ra tín hiệu giao dịch tiêu chuẩn 5 mức: **`Buy` / `Overweight` / `Hold` / `Underweight` / `Sell`** (xác định qua [rating.py](file:///d:/Huy%20Tuan%20Giang/BK/HK%20261/TradingAgents/tradingagents/agents/rating.py)).

---

## 4. Các Cơ Chế Kỹ Thuật Độc Đáo Trong Mã Nguồn

### 4.1. Hệ Thống Bộ Nhớ & Phản Tư (Memory Log & Deferred Reflection)
Được triển khai trong [decision_log.py](file:///d:/Huy%20Tuan%20Giang/BK/HK%20261/TradingAgents/tradingagents/decision_log.py) và [reflection.py](file:///d:/Huy%20Tuan%20Giang/BK/HK%20261/TradingAgents/tradingagents/graph/reflection.py):
1. **Lưu vết (Phase A):** Sau khi hoàn tất một lượt phân tích, quyết định được ghi vào file log dạng markdown dưới dạng trạng thái `pending`.
2. **Tất toán & Đánh giá (Phase B / Settlement):** Khi khoảng thời gian nắm giữ (ví dụ 5 ngày) trôi qua, hệ thống gọi `settle_pending` ([settlement.py](file:///d:/Huy%20Tuan%20Giang/BK/HK%20261/TradingAgents/tradingagents/graph/settlement.py)) để lấy giá thực tế, tính toán tỷ lệ sinh lời thực tế (Raw Return) và tỷ lệ vượt trội so với chỉ số tham chiếu như SPY (Alpha Return).
3. **Phản tư bằng LLM:** `Reflector` tạo ra một đoạn nhận xét 2-4 câu giải thích lý do thắng/thua và rút ra bài học kinh nghiệm.
4. **Tiêm ngữ cảnh (Context Injection):** Ở các lần phân tích sau, hàm `get_past_context` sẽ tự động trích xuất các bài học cũ của chính mã đó (same-ticker) và bài học từ các mã khác (cross-ticker) đưa vào prompt cho `Portfolio Manager`, giúp hệ thống tự tiến hóa và không lặp lại sai lầm.

```
[2026-09-01 | NVDA | Buy | pending]
  └── (Sau 5 ngày nắm giữ) ──> Alpha: +4.2%
  └── Reflector tạo bài học ──> Đưa vào past_context cho lượt phân tích kế tiếp
```

### 4.2. Khóa Identity Doanh Nghiệp (Deterministic Instrument Identity Anchor)
Định nghĩa tại [context.py](file:///d:/Huy%20Tuan%20Giang/BK/HK%20261/TradingAgents/tradingagents/agents/context.py):
- LLM khi nhìn vào biểu đồ giá độc lập đôi khi suy đoán sai tên công ty hoặc ngành nghề (ví dụ nhầm lẫn giữa mã cổ phiếu công nghệ và mã năng lượng do mẫu hình giá).
- `TradingAgents` giải quyết bằng cách dùng `resolve_instrument_identity()` tra cứu chính xác tên công ty, ngành hàng, sàn giao dịch từ `yfinance` ngay khi bắt đầu lượt chạy và tiêm cố định vào `instrument_context` của toàn bộ các Agent.

### 4.3. Kiểm Soát Thời Gian Nghiêm Ngặt (Point-in-Time Data Enforcement)
Định nghĩa tại [tools.py](file:///d:/Huy%20Tuan%20Giang/BK/HK%20261/TradingAgents/tradingagents/agents/tools.py):
- Mọi Tool lấy dữ liệu (`get_stock_data`, `get_indicators`, `get_fundamentals`, `get_news`) đều nhận tham số `trade_date` được tiêm từ trạng thái đồ thị (`InjectedState`).
- Các hàm cắt dữ liệu `as_of` và `as_of_window` đảm bảo Agent không bao giờ truy cập được dữ liệu phía sau ngày `trade_date`, giúp việc thử nghiệm lịch sử (Backtesting) đạt độ chính xác 100%.

### 4.4. Đồ Thị Trạng Thái & Khả Năng Phôi Phục (LangGraph Checkpoint Resiliency)
Định nghĩa tại [trading_graph.py](file:///d:/Huy%20Tuan%20Giang/BK/HK%20261/TradingAgents/tradingagents/graph/trading_graph.py) và [checkpointer.py](file:///d:/Huy%20Tuan%20Giang/BK/HK%20261/TradingAgents/tradingagents/graph/checkpointer.py):
- Tích hợp `SqliteSaver` lưu lại checkpoint sau mỗi bước chạy của Agent.
- Nếu tiến trình bị đứt quãng (do mất mạng hoặc lỗi API), hệ thống có thể khôi phục chính xác từ node bị ngắt mà không phải chạy lại từ đầu.

---

## 5. Cấu Trúc Trạng Thái Hệ Thống (AgentState Schema)

Trạng thái di chuyển xuyên suốt đồ thị được định nghĩa trong [state.py](file:///d:/Huy%20Tuan%20Giang/BK/HK%20261/TradingAgents/tradingagents/agents/state.py):

```python
class AgentState(MessagesState):
    company_of_interest: str    # Mã chứng khoán phân tích (VD: NVDA)
    asset_type: str             # Phân loại tài sản (stock / crypto)
    instrument_context: str     # Thông tin xác thực doanh nghiệp từ yfinance
    trade_date: str             # Ngày thực hiện phân tích (YYYY-MM-DD)
    
    # Báo cáo từ nhóm Analyst
    market_report: str
    sentiment_report: str
    news_report: str
    fundamentals_report: str
    
    # Luận điểm tranh luận Bull vs Bear
    investment_debate_state: InvestDebateState
    investment_plan: str        # Kế hoạch do Research Manager phê duyệt
    
    trader_investment_plan: str # Kế hoạch thực thi của Trader
    
    # Tranh luận rủi ro & Quyết định cuối
    risk_debate_state: RiskDebateState
    final_trade_decision: str   # Quyết định chi tiết của Portfolio Manager
    past_context: str           # Bài học lịch sử được tiêm từ Memory Log
    portfolio_context: str      # Thông tin số dư cash/vị thế hiện tại
```

---

## 6. Tổng Kết Danh Mục Tệp Tin Chính Trong Mã Nguồn

| Thư mục / Tệp tin | Vai trò chính |
| :--- | :--- |
| [main.py](file:///d:/Huy%20Tuan%20Giang/BK/HK%20261/TradingAgents/main.py) | File khởi chạy nhanh mẫu cho 1 mã cổ phiếu. |
| [tradingagents/graph/trading_graph.py](file:///d:/Huy%20Tuan%20Giang/BK/HK%20261/TradingAgents/tradingagents/graph/trading_graph.py) | Lớp điều phối chính (`TradingAgentsGraph`), kết nối đồ thị, checkpoint, ghi log và điều hướng chạy. |
| [tradingagents/graph/setup.py](file:///d:/Huy%20Tuan%20Giang/BK/HK%20261/TradingAgents/tradingagents/graph/setup.py) | Khai báo các node, edge và biên dịch đồ thị LangGraph (`StateGraph`). |
| [tradingagents/graph/conditional_logic.py](file:///d:/Huy%20Tuan%20Giang/BK/HK%20261/TradingAgents/tradingagents/graph/conditional_logic.py) | Logic rẽ nhánh vòng lặp tranh luận (Bull/Bear và Risk Debate). |
| [tradingagents/decision_log.py](file:///d:/Huy%20Tuan%20Giang/BK/HK%20261/TradingAgents/tradingagents/decision_log.py) | Quản lý bộ nhớ ghi chép quyết định & bài học lịch sử (Memory Log). |
| [tradingagents/backtest.py](file:///d:/Huy%20Tuan%20Giang/BK/HK%20261/TradingAgents/tradingagents/backtest.py) | Đánh giá chất lượng quyết định trên lưới dữ liệu nhiều mã và nhiều mốc thời gian. |
| [tradingagents/reporting.py](file:///d:/Huy%20Tuan%20Giang/BK/HK%20261/TradingAgents/tradingagents/reporting.py) | Xuất báo cáo cây thư mục dạng Markdown chi tiết cho người dùng. |

---

## 7. Kết Luận

**TradingAgents** thể hiện một kiến trúc Multi-Agent mạnh mẽ, hiện đại và chuẩn mực trong lĩnh vực Tài chính AI. Nhờ việc phân tách vai trò rõ ràng, áp dụng cơ chế đối kháng đa góc nhìn, phân lớp LLM thông minh và lưu giữ bộ nhớ bài học qua thời gian, hệ thống vượt trội so với các cách tiếp cận prompt đơn lẻ truyền thống, mang lại quyết định giao dịch có căn cứ, quản trị rủi ro chặt chẽ và khả năng giải thích cao (explainability).
