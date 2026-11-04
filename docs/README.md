# DACN — Thiết kế frontend và backend

Bộ thiết kế này xác định cách xây một ứng dụng web để tạo, theo dõi và xem lại các phiên phân tích. Thiết kế được xây từ yêu cầu sản phẩm và khảo sát mã nguồn, độc lập với các tài liệu dự án trước đây.

**Trạng thái:** đề xuất kiến trúc để triển khai; frontend, HTTP API, cơ sở dữ liệu ứng dụng và worker trong tài liệu chưa được hiện thực hóa. Ngày lập: 2026-11-04.

## Mục tiêu của giai đoạn hiện tại

Hoàn thành một luồng có thể kiểm thử: đăng nhập → chọn đối tượng phân tích → tạo phiên → xem tiến độ → đọc báo cáo và kết luận → mở lại lịch sử.

Frontend và backend được phát triển với engine giả lập trước. Một adapter riêng sẽ kết nối lõi TradingAgents sau khi luồng ứng dụng hoạt động. Nguồn dữ liệu và thị trường được lựa chọn qua khả năng hỗ trợ thực tế của engine; tài liệu không mặc định một thị trường hay vendor cụ thể.

| Tài liệu | Nội dung | Người sử dụng chính |
|---|---|---|
| [Đặc tả yêu cầu](requirements.md) | Yêu cầu FR/NFR, quy tắc nghiệp vụ, ưu tiên, trạng thái và tiêu chí nghiệm thu | Cả nhóm |
| [Kiến trúc hệ thống](system-architecture.md) | Phạm vi, quyết định công nghệ, thành phần, luồng dữ liệu | Cả nhóm |
| [Thiết kế frontend](frontend.md) | Màn hình, điều hướng, component, quản lý trạng thái, UX | Frontend |
| [Planning giao diện frontend](planning/frontend-ui.md) | Sáu màn hình tham khảo, ảnh desktop/mobile và prototype HTML | Cả nhóm |
| [Thiết kế backend](backend.md) | Module, worker, vòng đời phiên, tích hợp engine, xử lý lỗi | Backend |
| [Hợp đồng API](api-contract.md) | Endpoint, request/response, lỗi, phân trang, idempotency | Frontend và backend |
| [Mô hình dữ liệu](data-model.md) | ERD, bảng, ràng buộc và transaction | Backend |
| [Kế hoạch triển khai](implementation-plan.md) | Thứ tự công việc, đầu ra, tiêu chí nghiệm thu | Cả nhóm |

## Những lựa chọn đã chốt cho bản đầu

- Frontend: React, TypeScript, Vite, React Router, TanStack Query.
- Backend: FastAPI, Pydantic, SQLAlchemy, Alembic.
- PostgreSQL lưu dữ liệu nghiệp vụ và các phiên chờ xử lý.
- Một worker riêng lấy việc từ PostgreSQL, chạy tối đa một phiên tại một thời điểm trong mỗi worker process.
- Frontend lấy tiến độ bằng polling khi phiên còn hoạt động; chu kỳ mặc định 2 giây.
- Browser và API được phục vụ cùng origin; xác thực bằng session cookie.
- Dữ liệu giả lập luôn được gắn nhãn `mock`; engine thật luôn được gắn nhãn `live`.

Các tham số vận hành là giá trị khởi đầu để kiểm thử, có thể điều chỉnh sau khi đo tải. Phiên bản thư viện sẽ được khóa khi khởi tạo ứng dụng, thay vì dùng phiên bản trôi nổi trong môi trường triển khai.

## Ranh giới của bản thiết kế

Giai đoạn này đặc tả giao diện và dịch vụ ứng dụng. Luồng nội bộ giữa các agent thuộc phạm vi của engine; frontend nhận các bước chạy và báo cáo qua API ổn định. Việc thêm vendor, chỉnh chiến lược agent, backtest diện rộng và tích hợp đặt lệnh thuộc các giai đoạn sau.

Mã lõi hiện có kế thừa [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents), được phân phối theo [Apache License 2.0](../LICENSE).
