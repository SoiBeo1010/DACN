# Rà soát tính thống nhất của tài liệu

Ngày rà soát: 2026-11-04. Baseline yêu cầu sau rà soát: **0.4**.

## 1. Phạm vi và kết luận

Đã đối chiếu 10 tài liệu Markdown nguồn, prototype HTML và 8 ảnh trong `docs/`: yêu cầu, kiến trúc, FE, BE, API, dữ liệu, planning giao diện, kế hoạch và backlog sau MVP1.

Phạm vi MVP1 được giữ nhất quán: đăng nhập → `/analyses` → tạo phiên → theo dõi → đọc báo cáo/kết luận → lịch sử. Bảng điện/watchlist/biểu đồ chỉ thuộc backlog P1 / Sau MVP1 / Tạm hoãn. MVP1 FE/BE nghiệm thu bằng mock tại mốc 4; tích hợp TradingAgents live ở mốc 5 theo cùng luồng, không đòi hỏi bảng điện.

Các lệch chi tiết phát hiện trong lần rà soát này đã được sửa đồng bộ. Các yêu cầu vẫn ở trạng thái chưa triển khai/tạm hoãn; việc rà soát tài liệu không đổi chúng thành đã nghiệm thu ứng dụng.

## 2. Điểm đã phát hiện và sửa

| Điểm | Trước rà soát | Sau rà soát |
|---|---|---|
| Tìm kiếm lịch sử | FE/prototype có ô mã/tên nhưng API list chưa nhận q | API nhận q tìm trên instrument snapshot; FE, FR-15 và TC-09 dùng cùng quy tắc |
| Khoảng ngày và cursor | Cách bao gồm ngày đến, kết hợp filter và bỏ cursor chưa được diễn đạt đủ rõ | AND giữa filter; UI đổi ngày đến thành mốc đầu ngày kế tiếp rồi chuyển UTC; đổi filter bắt đầu lại cursor |
| Timeline mở muộn | FE có thể dùng nhầm event_cursor của snapshot, bỏ qua lịch sử chưa đọc | last_read_event_seq riêng; mở lần đầu after=0, đọc tiếp bằng next_cursor và lấy đủ sự kiện terminal |
| Nội dung báo cáo được cập nhật | DB giữ nội dung mới nhất nhưng cache FE chỉ dựa report ID | Giữ ID ổn định, tăng revision; API/DB/BE/FE và FR-13, TC-07 thống nhất cách invalidate cache |
| Ví dụ API | Snapshot đang ở bước phân tích nhưng version/cursor còn mơ hồ | Đồng bộ ví dụ version/event_cursor và event tiếp theo; bổ sung revision trong report.ready |
| Catalog và quyền session | Search/phân trang catalog và phản ứng với user bị vô hiệu hóa chưa đủ rõ giữa các file | Quy định q/cursor/limit catalog; kiểm tra user.is_active cho cả session đang tồn tại |
| Điều kiện rating hợp lệ | Mô tả SQL CHECK chưa nhấn mạnh trường hợp rating null | Nhánh valid phải kiểm tra rating IS NOT NULL và thuộc năm mức |
| Mốc tích hợp engine | Sơ đồ có cả mock/live dễ bị hiểu là cần provider cho MVP1 | Gắn nhãn MVP1 cho mock; TradingAgents/provider được ghi rõ mốc 5 |
| Prototype hủy phiên | Hủy phiên chờ PA-101 có thể nhảy sang PA-104; lịch sử chưa phản ánh thao tác | Giữ đúng ID/ngày, cập nhật trạng thái trong bộ nhớ; queued hủy vẫn có 0 báo cáo; running giữ báo cáo từng phần |
| Prototype trạng thái/form | Đang yêu cầu hủy chưa được tính/lọc đầy đủ; ngôn ngữ chọn chưa được giữ trong thông tin phiên mới | Tính cancel_requested là hoạt động, bổ sung filter, giữ ngày/ngôn ngữ của yêu cầu mới |
| Thuật ngữ backlog | Cờ candle được gọi completed nhưng schema dùng is_complete | Dùng cùng tên is_complete trong phần mở rộng |

## 3. Kiểm tra đối chiếu

| Nội dung | Kết quả |
|---|---|
| Route trang chính | FE, requirements, README và prototype cùng dùng lịch sử phiên cho MVP1 |
| Trạng thái run | queued/running/cancel_requested/succeeded/failed/cancelled thống nhất; terminal không chuyển ngược |
| Chất lượng kết luận | succeeded có thể needs_review; rating null không thành Hold |
| Hủy/thử lại | Hủy theo trạng thái; retry tạo ID mới từ failed/cancelled; không tự chạy lại cả phiên |
| Tham số baseline | Poll chi tiết 2 giây, lịch sử 5 giây, heartbeat 10 giây, lease 60 giây, deadline 15 phút, 2 phiên hoạt động/user |
| Session/idempotency | Session 8 giờ, key 24 giờ; owner từ session, chống trùng trước kiểm tra quota |
| Các mã yêu cầu | FR-01–FR-26, NFR-01–NFR-13, BR-01–BR-15, TC-01–TC-16 giữ ID và liên kết hợp lệ |
| Scope sau MVP1 | FR-22–FR-26/NFR-13 được tạm hoãn; API, migration và collector tương ứng không nằm trong thiết kế triển khai bắt buộc |
| Ví dụ và liên kết | Kiểm tra JSON, link nội bộ/ảnh, code fence và đường README của package |

## 4. Kiểm tra prototype

Đã chạy JavaScript syntax check và browser smoke test trên Chrome:

- Hủy phiên đang chờ giữ đúng ID; không sinh báo cáo; mở lại từ lịch sử và thử lại đúng phiên nguồn.
- Hủy phiên đang chạy giữ báo cáo từng phần; trạng thái cancel_requested có trong bộ lọc lịch sử.
- Tạo phiên giữ ngày/ngôn ngữ đã chọn và ID mới khi hủy.
- Tìm mã kết hợp trạng thái và khoảng ngày cho kết quả đúng.
- 33 tổ hợp màn hình/trạng thái ở bề rộng 390, 768, 1440 px không có JavaScript error hoặc tràn ngang toàn trang.
- Chụp lại 8 ảnh để khớp với prototype hiện tại.

Prototype là fixture trình bày cục bộ, chưa mô phỏng backend/session/quota/lease hoặc polling thật. Các ca TC của ứng dụng vẫn cần được triển khai và chạy theo kế hoạch.

## 5. Điểm còn mở

Các mục OPEN-01–OPEN-06 trong [requirements](../requirements.md) vẫn cần được chốt khi tới mốc tương ứng: nhân lực/thời hạn, môi trường demo, ngưỡng đo tải, nguồn live, retention/backup và các hạn mức vận hành. Đây là quyết định chưa hoàn tất, không phải mâu thuẫn giữa các tài liệu hoặc dependency bảng điện của MVP1.

Các thay đổi tiếp theo cần cập nhật cùng [requirements](../requirements.md), [API](../backend/api-contract.md), [dữ liệu](../backend/data-model.md), [FE](../frontend/design.md), [BE](../backend/design.md) và [kế hoạch](implementation-plan.md) nếu có ảnh hưởng tới những phần này.
