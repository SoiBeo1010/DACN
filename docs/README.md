# DACN — Tài liệu dự án

Bộ tài liệu tập trung vào MVP1 quản lý phiên phân tích với lõi TradingAgents và dữ liệu thật: đăng nhập → chọn mã/ngày → tạo phiên → theo dõi tiến độ → đọc báo cáo/kết luận → mở lại lịch sử. Trang chính sau đăng nhập là `/analyses`. MVP1 chỉ được nghiệm thu tại mốc 5 sau khi luồng này chạy được qua adapter với provider thật; mock phục vụ phát triển và kiểm thử.

Bảng điện Việt Nam để theo dõi giá, watchlist, biểu đồ và cập nhật giá định kỳ được triển khai ở giai đoạn tiếp theo **sau MVP1**, không phải điều kiện để nghiệm thu MVP1.

**Trạng thái:** đặc tả và thiết kế để triển khai; đã có prototype giao diện, chưa có ứng dụng web FE/BE hoàn chỉnh. Ngày cập nhật: 2026-11-07.

## Bắt đầu từ đâu?

1. Đọc [yêu cầu](requirements.md) để hiểu phạm vi, ưu tiên và tiêu chí nghiệm thu.
2. Đọc [kiến trúc tổng thể](system-architecture.md) để hiểu các thành phần và luồng dữ liệu.
3. Đi vào nhóm frontend hoặc backend bên dưới; dùng [API contract](backend/api-contract.md) khi phối hợp hai phía.
4. Theo [kế hoạch triển khai](planning/implementation-plan.md) để thực hiện từng mốc.

## Cấu trúc thư mục

```text
docs/
├── README.md                    # Mục lục và hướng dẫn đọc
├── requirements.md              # Quản lý tập trung yêu cầu FR/NFR/BR
├── system-architecture.md       # Kiến trúc dùng chung
├── frontend/
│   ├── design.md                # Cấu trúc FE, màn hình, trạng thái
│   ├── ui-planning.md           # Phác thảo và ảnh màn hình
│   ├── prototype.html           # Bản tương tác mở bằng trình duyệt
│   └── screenshots/             # Ảnh desktop/mobile
├── backend/
│   ├── design.md                # Module, worker, engine adapter
│   ├── api-contract.md          # Hợp đồng FE/BE
│   └── data-model.md            # ERD và ràng buộc dữ liệu
└── planning/
    ├── implementation-plan.md   # Mốc thực hiện và nghiệm thu MVP1
    └── post-mvp-market-workspace.md # Backlog bảng điện sau MVP1
```

## Tài liệu theo nhóm công việc

| Nhóm | Tài liệu | Nội dung |
|---|---|---|
| Dùng chung | [Đặc tả yêu cầu](requirements.md) | Phạm vi, FR/NFR/BR, ưu tiên, trạng thái và kịch bản nghiệm thu |
| Dùng chung | [Kiến trúc hệ thống](system-architecture.md) | Thành phần, quyết định công nghệ và luồng dữ liệu |
| Frontend | [Thiết kế FE](frontend/design.md) | Route, component, quản lý trạng thái và UX |
| Frontend | [Planning giao diện](frontend/ui-planning.md) · [Prototype HTML](frontend/prototype.html) | Sáu màn hình tham khảo, ảnh desktop/mobile và tương tác mẫu |
| Backend | [Thiết kế BE](backend/design.md) | Service, worker, lifecycle, xử lý lỗi và tích hợp engine |
| Backend | [Hợp đồng API](backend/api-contract.md) | Endpoint, schema, mã lỗi, idempotency và phân trang |
| Backend | [Mô hình dữ liệu](backend/data-model.md) | Bảng, quan hệ, index và transaction |
| Triển khai | [Kế hoạch thực hiện](planning/implementation-plan.md) | Thứ tự công việc, đầu ra và tiêu chí hoàn thành |
| Sau MVP1 | [Backlog bảng điện](planning/post-mvp-market-workspace.md) | Bố cục, API và dữ liệu dự kiến của bảng điện/watchlist; chưa bắt buộc |

Prototype hiện tại dùng dữ liệu giả lập để minh họa bố cục luồng phân tích của MVP1 và mở trực tiếp bằng trình duyệt. Khi xem trên GitHub, đọc ảnh trong planning giao diện hoặc tải HTML về để thử. Bằng chứng nghiệm thu MVP1 phải đến từ ứng dụng tích hợp lõi và dữ liệu thật; màn hình bảng điện được xây sau MVP1.

## Cách cập nhật tài liệu

- Thay đổi chức năng, phạm vi hoặc tiêu chí nghiệm thu: cập nhật `requirements.md`, giữ ID yêu cầu ổn định.
- Thay đổi cách thực hiện: cập nhật thiết kế frontend/backend, API hoặc mô hình dữ liệu tương ứng; đối chiếu lại yêu cầu.
- Thay đổi bố cục giao diện: cập nhật planning, prototype và ảnh trong cùng `frontend/`.
- Thay đổi thứ tự hoặc mốc công việc: cập nhật kế hoạch trong `planning/`.
- Ý tưởng sau MVP1: lưu trong backlog, gắn rõ giai đoạn và trạng thái Tạm hoãn tại requirements; không thêm vào luồng bắt buộc của MVP1.
- Thêm, xóa hoặc di chuyển tài liệu: cập nhật mục lục này và liên kết tương đối. Mỗi tài liệu có một vị trí chính.

## Định hướng hiện tại

React/TypeScript cho frontend; FastAPI cho backend; PostgreSQL lưu phiên, báo cáo và hàng đợi; worker riêng chạy phân tích. Trong MVP1, mốc 1–4 xây và kiểm thử FE/BE bằng mock, mốc 5 tích hợp TradingAgents qua adapter và nghiệm thu toàn luồng bằng dữ liệu thật. Sau MVP1 triển khai bảng điện theo dõi giá, gồm quote API, bảng OHLCV, watchlist và collector giá. Dữ liệu phục vụ phân tích trong MVP1 được lấy qua công cụ của lõi, độc lập với dịch vụ bảng điện.

Tham số vận hành ban đầu được ghi tại đặc tả và kiến trúc để kiểm thử, chưa phải SLA. Chi tiết phối hợp bên trong agent, mở rộng vendor, backtest diện rộng và đặt lệnh thuộc các giai đoạn sau.

Mã lõi kế thừa [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents), phân phối theo [Apache License 2.0](../LICENSE).
