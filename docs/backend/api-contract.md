# Hợp đồng API frontend/backend

Đối chiếu hành vi API với các mã yêu cầu FR/NFR/BR tại [requirements.md](../requirements.md). Các thay đổi hành vi phải được cập nhật cùng đặc tả và kịch bản nghiệm thu liên quan.

Hợp đồng dưới đây dành cho MVP1 theo luồng phân tích. API quote/OHLCV/watchlist chỉ là [đề xuất sau MVP1](../planning/post-mvp-market-workspace.md), chưa cần triển khai hoặc sinh vào OpenAPI của MVP1.

## 1. Quy ước chung

- Base path: `/api/v1`.
- JSON UTF-8; tên trường `snake_case`; resource ID là UUID.
- Timestamp theo ISO 8601 UTC, ngày nghiệp vụ theo `YYYY-MM-DD`.
- Mọi endpoint dữ liệu cần session, trừ login và health.
- Session cookie được browser gửi tự động. Mutation đã xác thực gửi thêm `X-CSRF-Token`.
- Server sinh `request_id` và trả trong response header `X-Request-ID` cùng payload lỗi.
- API không nhận `owner_id`, đường dẫn lưu trữ, secret hoặc provider URL từ người dùng.
- Mã hiển thị không phải định danh duy nhất: dùng `instrument_id` khi tạo phân tích.

Tài liệu này là hợp đồng thiết kế. Khi hiện thực hóa, Pydantic schema tạo OpenAPI; frontend sinh TypeScript từ OpenAPI và CI kiểm tra sai lệch. Trong giai đoạn mock, fixture phải tuân thủ các schema dưới đây.

## 2. Danh mục endpoint

| Method | Path | Kết quả chính |
|---|---|---|
| POST | `/auth/login` | `200`, đặt session cookie |
| GET | `/auth/session` | `200`, user và CSRF token; `401` nếu chưa đăng nhập |
| POST | `/auth/logout` | `204`, thu hồi session và xóa cookie |
| GET | `/instruments?q=&cursor=&limit=` | `200`, tìm đối tượng được hỗ trợ |
| GET | `/analysis-profiles` | `200`, profile công khai và capability |
| POST | `/analyses` | `202`, tạo phiên chờ |
| GET | `/analyses?status=&instrument_id=&created_from=&created_to=&cursor=&limit=` | `200`, lịch sử |
| GET | `/analyses/{id}` | `200`, snapshot |
| GET | `/analyses/{id}/events?after=0&limit=100` | `200`, sự kiện sau cursor |
| GET | `/analyses/{id}/reports` | `200`, metadata báo cáo đã có |
| GET | `/analyses/{id}/reports/{report_id}` | `200`, nội dung một báo cáo |
| POST | `/analyses/{id}/cancel` | `200` hoặc `202`, tùy trạng thái |
| POST | `/analyses/{id}/retry` | `202`, phiên mới |
| GET | `/health/live` | `200`, process API đang hoạt động |
| GET | `/health/ready` | `200` hoặc `503`, API và DB sẵn sàng |

Resource thuộc tài khoản khác trả `404`. Report ID luôn được tra cứu bên trong run ID và owner tương ứng.

## 3. Xác thực

`POST /auth/login` nhận `{ "email": "student@example.test", "password": "<mật khẩu người dùng>" }`.

Response `200` và `GET /auth/session` có cùng body:

```json
{
  "user": {
    "id": "00000000-0000-4000-8000-000000000200",
    "email": "student@example.test",
    "display_name": "Sinh viên"
  },
  "csrf_token": "<giá trị do server sinh>",
  "expires_at": "2026-11-04T15:00:00Z"
}
```

Không trả session token trong JSON. Login kiểm tra Origin/Referer cùng origin và rate limit. Sau đăng nhập, các mutation đối chiếu CSRF token với session. Logout yêu cầu CSRF, thu hồi token server-side và xóa cookie bằng cùng Path.

## 4. Catalog phục vụ form

`GET /instruments` trả `{ "items": [...], "next_cursor": null }`. Mỗi item:

```json
{
  "id": "00000000-0000-4000-8000-000000000001",
  "symbol": "DEMO",
  "name": "Đối tượng giả lập",
  "exchange": "DEMO",
  "asset_type": "stock",
  "currency": "USD",
  "timezone": "Asia/Ho_Chi_Minh",
  "supported_profile_ids": ["standard"],
  "earliest_as_of_date": "2026-01-01",
  "latest_as_of_date": "2026-11-04",
  "data_mode": "mock"
}
```

`DEMO` là fixture không đại diện một chứng khoán thật. Catalog live chỉ liệt kê các instrument đã được adapter xác nhận hỗ trợ; giới hạn ngày phụ thuộc nguồn dữ liệu. `live` chỉ nguồn thực, không cam kết dữ liệu tức thời. Backend không chấp nhận kết hợp instrument mock với profile live hoặc ngược lại.

`GET /analysis-profiles` trả:

```json
{
  "items": [
    {
      "id": "standard",
      "name": "Tiêu chuẩn",
      "description": "Phân tích và tổng hợp báo cáo",
      "version": "1",
      "supported_languages": ["vi", "en"],
      "available": true,
      "data_mode": "mock"
    }
  ]
}
```

Provider/model, prompt, timeout và khóa truy cập không nằm trong profile công khai. Backend snapshot phiên bản cấu hình thực thi khi tạo run.

## 5. Tạo phiên

`POST /analyses`, bắt buộc header `Idempotency-Key` có dạng UUID:

```json
{
  "instrument_id": "00000000-0000-4000-8000-000000000001",
  "as_of_date": "2026-11-03",
  "profile_id": "standard",
  "language": "vi"
}
```

Response `202`:

```json
{
  "id": "00000000-0000-4000-8000-000000000100",
  "status": "queued",
  "data_mode": "mock",
  "links": {
    "self": "/api/v1/analyses/00000000-0000-4000-8000-000000000100"
  }
}
```

Header `Location` bằng `links.self`. Frontend mở trang chi tiết và đọc snapshot hiện tại.

- Cùng user, key và request chuẩn hóa trong 24 giờ: trả lại `202`, body và Location đã lưu của lần đầu. `status` trong body replay là trạng thái lúc chấp nhận; trạng thái mới nhất đọc từ GET.
- Cùng key, request khác: `409 IDEMPOTENCY_CONFLICT`.
- Key hết hạn: có thể tạo ý định mới; UI vẫn nên sinh key mới cho mỗi ý định mới.
- Từ chối instrument/profile/ngôn ngữ/ngày không hỗ trợ bằng `422`; không tạo run và không tiêu thụ key.
- Bản đầu không nhận trường ngoài schema; trả validation error khi có extra field.

## 6. Snapshot phiên

`GET /analyses/{id}`:

```json
{
  "id": "00000000-0000-4000-8000-000000000100",
  "status": "running",
  "version": 3,
  "event_cursor": 3,
  "data_mode": "mock",
  "instrument": {
    "id": "00000000-0000-4000-8000-000000000001",
    "symbol": "DEMO",
    "name": "Đối tượng giả lập",
    "exchange": "DEMO",
    "timezone": "Asia/Ho_Chi_Minh"
  },
  "as_of_date": "2026-11-03",
  "profile": { "id": "standard", "name": "Tiêu chuẩn", "version": "1" },
  "language": "vi",
  "created_at": "2026-11-04T07:00:00Z",
  "started_at": "2026-11-04T07:00:01Z",
  "finished_at": null,
  "current_step_key": "analysis",
  "steps": [
    { "key": "prepare", "label": "Chuẩn bị", "order": 1, "status": "completed" },
    { "key": "analysis", "label": "Phân tích", "order": 2, "status": "running" },
    { "key": "synthesis", "label": "Tổng hợp", "order": 3, "status": "pending" },
    { "key": "finalize", "label": "Hoàn tất", "order": 4, "status": "pending" }
  ],
  "reports": [],
  "decision": null,
  "error": null,
  "capabilities": { "can_cancel": true, "can_retry": false },
  "retry_of_run_id": null
}
```

`version` tăng theo thay đổi nghiệp vụ, không tăng mỗi heartbeat. `event_cursor` là seq cuối tại snapshot. Server đọc run, step, report metadata và decision trong một transaction snapshot nhất quán, ví dụ read-only REPEATABLE READ; không ghép các phiên bản khác nhau.

Các enum:

| Trường | Giá trị |
|---|---|
| `status` | `queued`, `running`, `cancel_requested`, `succeeded`, `failed`, `cancelled` |
| `steps[].status` | `pending`, `running`, `completed`, `failed`, `skipped` |
| `data_mode` | `mock`, `live` |
| `decision.quality` | `valid`, `needs_review` |
| `decision.rating` | `Buy`, `Overweight`, `Hold`, `Underweight`, `Sell`, hoặc `null` |

Khi `succeeded`, `decision` là object gồm `quality`, `rating`, `summary_markdown`, `warnings` (mảng `{code, message}`). `valid` yêu cầu rating hợp lệ; `needs_review` dùng `rating = null`. Khi chưa có kết luận, `decision = null`.

Khi `failed`, `error` gồm `{ "code": "WORKER_LOST", "message": "Phiên bị gián đoạn. Bạn có thể thử lại." }`. Các terminal state có `finished_at` và `current_step_key = null`. Report đã có vẫn được trả cho phiên failed/cancelled.

## 7. Sự kiện và báo cáo

`GET /analyses/{id}/events?after=3&limit=100`:

```json
{
  "items": [
    {
      "seq": 4,
      "type": "report.ready",
      "occurred_at": "2026-11-04T07:00:10Z",
      "payload": {
        "report_id": "00000000-0000-4000-8000-000000000300",
        "section_key": "market",
        "title": "Báo cáo kỹ thuật"
      }
    }
  ],
  "next_cursor": 4,
  "has_more": false
}
```

`after` là seq không bao gồm. Sắp xếp tăng dần; `limit` từ 1 đến 100. Nếu không có sự kiện mới, `next_cursor = after`. FE loại trùng theo `(run_id, seq)` và đọc tiếp khi `has_more`.

Các loại sự kiện tối thiểu: `run.queued`, `run.started`, `step.started`, `step.completed`, `step.failed`, `report.ready`, `run.cancel_requested`, `run.cancelled`, `run.succeeded`, `run.failed`. Payload thay đổi theo type và phải có schema riêng khi triển khai.

`GET /analyses/{id}/reports` trả `{ "items": [...] }` với mỗi item gồm `id`, `section_key`, `title`, `updated_at`, `content_format = markdown`, `data_mode`. Snapshot dùng cùng kiểu metadata.

`GET /analyses/{id}/reports/{report_id}` bổ sung `content_markdown`. Phiên còn chạy có thể trả danh sách rỗng. Phần chưa xuất hiện trong danh sách được xem là chưa có báo cáo.

## 8. Hủy và thử lại

| Trạng thái trước khi hủy | Kết quả |
|---|---|
| `queued` | `200`, chuyển `cancelled` |
| `running` | `202`, chuyển `cancel_requested` |
| `cancel_requested` | `202`, giữ nguyên; không ghi sự kiện yêu cầu hủy lặp |
| `cancelled` | `200`, giữ nguyên |
| `succeeded` hoặc `failed` | `409 INVALID_STATE` |

Body hủy là `{ "id": "...", "status": "..." }`. FE refetch snapshot. Hủy có tính idempotent theo trạng thái, không yêu cầu `Idempotency-Key`.

`POST /analyses/{id}/retry` không có body và bắt buộc `Idempotency-Key`. Chỉ cho phép source `failed` hoặc `cancelled`; tạo run mới từ input/config snapshot, trả `202` cùng kiểu response tạo phiên. Nếu engine/profile version cũ không còn chạy được, trả `409 RETRY_UNAVAILABLE`; người dùng tạo phân tích mới với profile hiện tại.

## 9. Lịch sử và phân trang

Danh sách trả `{ "items": [...], "next_cursor": "<opaque>" }`; `next_cursor = null` khi hết. `limit` mặc định 20, tối đa 100. Thứ tự `(created_at DESC, id DESC)`; cursor chỉ vị trí cuối, không phải offset.

Run item là bản gọn: `id`, `instrument` (id/symbol/name/exchange), `as_of_date`, `status`, `data_mode`, `created_at`, `finished_at`, `decision` (quality/rating hoặc null). Không chứa nội dung Markdown đầy đủ.

`created_from`, `created_to` là timestamp UTC, dùng khoảng `[from, to)`. FE chuyển bộ lọc ngày theo timezone đang hiển thị thành khoảng UTC. Filter `status` nhận một enum; `instrument_id` nhận UUID. Khi đổi filter, FE bỏ cursor cũ.

## 10. Lỗi chuẩn

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Vui lòng kiểm tra thông tin phân tích.",
    "fields": { "as_of_date": "Ngày chưa được hỗ trợ." },
    "request_id": "00000000-0000-4000-8000-000000000400"
  }
}
```

| HTTP | Code điển hình | Hành vi frontend |
|---|---|---|
| 401 | `UNAUTHENTICATED` | Xóa session cache, về đăng nhập |
| 403 | `CSRF_FAILED` | Tải lại session/token; không tự gửi lại mutation bằng khóa mới |
| 404 | `NOT_FOUND` | Dừng polling và hiển thị không tìm thấy |
| 409 | `IDEMPOTENCY_CONFLICT`, `INVALID_STATE`, `RETRY_UNAVAILABLE` | Giữ input, giải thích xung đột |
| 422 | `VALIDATION_ERROR`, `UNSUPPORTED_INPUT` | Hiển thị lỗi tại trường |
| 429 | `ACTIVE_RUN_LIMIT`, `RATE_LIMITED` | Giữ form, dùng `Retry-After` nếu có |
| 500/503 | `INTERNAL_ERROR`, `SERVICE_UNAVAILABLE` | Giữ dữ liệu đã tải, cho phép thử lại |

Exception handler chuẩn hóa cả lỗi Pydantic/FastAPI. HTTP error và lỗi thực thi phiên là hai lớp: một request đọc phiên failed vẫn trả `200` với `status = failed`.
