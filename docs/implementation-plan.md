# Kế hoạch hiện thực hóa frontend/backend

Theo dõi phạm vi, ưu tiên, trạng thái triển khai và tiêu chí nghiệm thu theo mã yêu cầu tại [requirements.md](requirements.md). Các mốc bên dưới được đối chiếu với ma trận yêu cầu trong tài liệu đó.

## 1. Cách triển khai

Làm một lát cắt xuyên suốt bằng mock engine trước: đăng nhập, tạo phiên, worker chạy, FE lấy tiến độ, lưu kết quả và mở lại lịch sử. Cách này kiểm chứng API, database và UX độc lập với độ ổn định hoặc chi phí của provider.

Các mốc dưới đây đi theo đầu ra, chưa gán số tuần vì chưa có thông tin nhân lực và thời hạn. Nhóm có thể chia người làm FE và BE đồng thời sau khi chốt contract.

## 2. Mốc 1 — Chốt hợp đồng và wireframe

Đã có [planning giao diện và các màn hình tham khảo](planning/frontend-ui.md), kèm [prototype HTML](planning/frontend-preview.html) để nhóm xem và chốt bố cục. Schema API và ứng dụng React sẽ được triển khai theo các mốc dưới đây.

| Frontend | Backend | Đầu ra chung |
|---|---|---|
| Wireframe login/list/create/detail; các trạng thái lỗi/rỗng/loading | Pydantic schema công khai, enum, lỗi chuẩn, lifecycle | OpenAPI và fixture khớp nhau |
| Chốt thuật ngữ và component trạng thái | Chốt instrument/profile catalog mock | Một bộ kịch bản có thể demo |

Tiêu chí hoàn thành:

- Cả hai phía thống nhất response tạo phiên, snapshot, report, event và lỗi.
- Có fixture cho `queued`, `running`, `cancel_requested`, `succeeded`, `failed`, `cancelled` và kết luận `needs_review`.
- Các ID trong fixture liên kết nhất quán; data mode được gắn nhãn.
- Kiểu TypeScript được sinh từ OpenAPI khi backend schema đã có.

## 3. Mốc 2 — Nền tảng ứng dụng

Frontend tạo app shell, router, HTTP client, QueryClient, login và protected route. Backend tạo FastAPI, database session, migration, user/session, seed account/catalog và exception handler.

Tiêu chí hoàn thành:

- Đăng nhập/đăng xuất được qua browser cùng origin.
- Tài khoản khác không đọc được dữ liệu của nhau.
- Form tìm instrument và profile hoạt động với catalog mock.
- Build FE và cài đặt BE chạy được từ môi trường sạch.

## 4. Mốc 3 — Luồng tạo và theo dõi phiên

Frontend triển khai form, idempotency key, trang chi tiết, polling và timeline. Backend triển khai tạo phiên trong transaction, worker claim, heartbeat, progress event và mock engine chạy theo thời gian.

Tiêu chí hoàn thành:

- Nhấn gửi nhiều lần hoặc gửi lại sau mất response vẫn chỉ có một run.
- Trình duyệt đóng rồi mở lại vẫn thấy phiên đang chạy.
- Hai worker thử claim cùng lúc không thực thi cùng một run.
- API vẫn trả lời khi engine đang chạy lâu.
- Trang chi tiết hiển thị tiến độ lấy từ backend, không chạy timer để tự đoán kết quả.

## 5. Mốc 4 — Kết quả, lịch sử và gián đoạn

Frontend triển khai reader Markdown, quality/rating, lịch sử có filter và các thao tác hủy/thử lại. Backend triển khai persist result, report query, cursor pagination, cancel và recovery.

Tiêu chí hoàn thành:

- Báo cáo hoàn thành từng phần đọc được khi phiên vẫn chạy.
- Có thể phân biệt hoàn tất hợp lệ, cần xem xét, thất bại và hủy.
- Hủy queued có hiệu lực ngay; hủy running hiển thị chờ xác nhận dừng.
- Worker chết làm phiên thất bại sau lease/recovery; thử lại tạo run mới.
- Rating null không bị hiển thị thành Hold.
- Lịch sử vẫn đọc được khi backend restart.

Đây là mốc nghiệm thu FE/BE chính trước khi tích hợp engine thật.

## 6. Mốc 5 — Adapter TradingAgents

Backend nối `AnalysisEngine` với mã lõi, cô lập config/storage/checkpoint, map báo cáo và rating. Frontend chỉ điều chỉnh khi xuất hiện một nhu cầu sản phẩm mới được thống nhất qua API contract.

Tiêu chí hoàn thành:

- Một instrument được provider hỗ trợ chạy được từ FE đến kết quả live.
- Hai phiên cùng instrument/ngày có artifact, checkpoint và kết quả riêng.
- Backend không dùng singleton graph giữa các phiên.
- Test thông thường dùng mock/stub; việc gọi provider thật thuộc smoke test chủ động.
- Credential và payload nội bộ không xuất hiện trong API/log công khai.
- Engine lỗi, quá hạn và output REVIEW được map đúng hợp đồng.

## 7. Ma trận kiểm thử cần xây khi triển khai

| Lớp | Ca kiểm thử có giá trị |
|---|---|
| Frontend component | Form báo lỗi đúng trường, label trạng thái/quality, report Markdown an toàn |
| Frontend với mock API | Polling dừng terminal, mất session, mạng gián đoạn, gửi lại cùng key |
| Backend domain | Chuyển trạng thái hợp lệ, hủy/hoàn tất tranh chấp, retry source terminal |
| Backend tích hợp PostgreSQL | Idempotency đồng thời, quota đồng thời, claim nhiều worker, ghi sau mất lease bị chặn |
| Backend quyền truy cập | Đọc run/report/event của người khác, CSRF và session hết hạn |
| E2E | Login → tạo → tiến độ → kết quả → mở lại lịch sử |
| Phục hồi | Tắt worker giữa phiên, restart backend, timeout process con, retry mới |
| Adapter | Cô lập cùng ticker/ngày, mapping report/rating và lỗi engine |

Các test về claim, khóa và transaction dùng PostgreSQL thật trong môi trường test, vì SQLite không có cùng hành vi SKIP LOCKED. Không gọi LLM thật trong CI mặc định.

## 8. Môi trường và CI dự kiến

Compose cho ứng dụng web sẽ có reverse proxy phục vụ FE static, API, worker và PostgreSQL. Dùng volume cho database và artifact; `.env` server được loại khỏi Git. Compose hiện có phục vụ CLI, cần được bổ sung hoặc tách thành cấu hình web khi triển khai.

| Pipeline | Kiểm tra |
|---|---|
| Frontend | Typecheck, lint, component/API mock test, production build |
| Backend | Ruff, unit/integration test, migration từ DB rỗng |
| Contract | Xuất OpenAPI, sinh FE types, phát hiện thay đổi chưa commit |
| E2E | Chạy toàn luồng bằng mock engine |
| Đóng gói lõi | Giữ kiểm tra cài đặt package và import hiện tại |

Trong runtime, migration chạy một lần ở bước release; API/worker không tự cạnh tranh chạy migration khi startup. API readiness chỉ thành công khi schema phù hợp.

## 9. Những điểm cần chốt khi bước sang implementation

- Người phụ trách FE/BE, thời hạn và quy mô demo.
- Bộ UI component, nhận diện trực quan và mức hỗ trợ mobile.
- Provider/market đầu tiên có dữ liệu thực tế đáp ứng, cùng quyền truy cập cần thiết.
- Thời gian lưu dữ liệu, môi trường deploy và ngân sách chạy engine.

Các quyết định này không chặn việc triển khai FE/BE với mock engine. Phạm vi ban đầu và contract được mô tả đủ để bắt đầu mốc 1.
