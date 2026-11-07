# Kế hoạch triển khai MVP1 và giai đoạn bảng điện

Theo dõi phạm vi, ưu tiên, trạng thái triển khai và tiêu chí nghiệm thu theo mã yêu cầu tại [requirements.md](../requirements.md). Các mốc bên dưới được đối chiếu với ma trận yêu cầu trong tài liệu đó.

## 1. Cách triển khai

MVP1 phải chạy xuyên suốt với lõi TradingAgents và dữ liệu thật: đăng nhập, tạo phiên, worker gọi lõi qua adapter, FE lấy tiến độ, lưu báo cáo/kết luận và mở lại lịch sử. Có thể xây lát cắt bằng mock engine trước để kiểm chứng API, database và UX; mock/stub tiếp tục phục vụ phát triển và CI.

Các mốc dưới đây đi theo đầu ra; bảng đầu việc ở mục 9 cung cấp vai trò phụ trách, dependency và ước lượng công sức ban đầu. Chưa gán ngày bắt đầu/kết thúc vì chưa có thông tin thành viên và thời hạn. Nhóm có thể làm FE bằng mock API song song với BE sau khi chốt contract.

MVP1 gồm toàn bộ mốc 1–5 và chỉ được nghiệm thu tại mốc 5 sau khi tích hợp lõi, chạy dữ liệu thật và đạt TC-01–TC-13. Mốc 4 là đầu ra trung gian để kiểm thử FE/BE bằng mock. Sau nghiệm thu MVP1, triển khai bảng điện theo dõi giá, watchlist, biểu đồ, collector và API giá theo [kế hoạch sau MVP1](post-mvp-market-workspace.md). Các chức năng bảng điện không chặn mốc 1–5; prototype hiện có dùng để tham khảo bố cục.

## 2. Mốc 1 — Chốt hợp đồng và wireframe

Đã có [planning giao diện và các màn hình tham khảo](../frontend/ui-planning.md), kèm [prototype HTML](../frontend/prototype.html) để nhóm xem và chốt bố cục. Schema API và ứng dụng React sẽ được triển khai theo các mốc dưới đây.

| Frontend | Backend | Đầu ra chung |
|---|---|---|
| Wireframe login/list/create/detail; các trạng thái lỗi/rỗng/loading | Pydantic schema công khai, enum, lỗi chuẩn, lifecycle | OpenAPI và fixture khớp nhau |
| Chốt thuật ngữ và component trạng thái mock/live | Chốt fixture catalog và chọn instrument/profile/provider thật theo OPEN-04 | Bộ kịch bản dev/test và đầu vào demo live cho MVP1 |
| Đối chiếu report metadata và decision với màn hình | Khảo sát stream và helper ngày giờ của lõi bằng code/fixture | Bảng ánh xạ input, step, report, rating, timezone để thử bằng stub ở mốc 2 |

Tiêu chí hoàn thành:

- Cả hai phía thống nhất response tạo phiên, snapshot, report, event và lỗi.
- Có fixture cho `queued`, `running`, `cancel_requested`, `succeeded`, `failed`, `cancelled` và kết luận `needs_review`.
- Các ID trong fixture liên kết nhất quán; data mode được gắn nhãn.
- Kiểu TypeScript được sinh từ OpenAPI khi backend schema đã có.
- Chọn ít nhất một instrument được lõi và nguồn thật hỗ trợ; xác định provider dữ liệu/mô hình, người cung cấp quyền truy cập và ngân sách theo OPEN-04 để chuẩn bị tích hợp trong MVP1.
- Có bảng ánh xạ ít nhất `market_report` sang report section `market`, `final_trade_decision` sang decision và `REVIEW` sang `needs_review`; ghi rõ helper đang phụ thuộc ngày máy và thay đổi cần làm ở mốc 5.

## 3. Mốc 2 — Nền tảng ứng dụng

Frontend tạo app shell, router, HTTP client, QueryClient, login và protected route. Backend tạo FastAPI, database session, migration, user/session, seed account/catalog và exception handler. Thực hiện thử nghiệm adapter tối thiểu bằng stub từ bảng ánh xạ mốc 1 trước khi xây worker hoàn chỉnh.

Tiêu chí hoàn thành:

- Đăng nhập/đăng xuất được qua browser cùng origin.
- Tài khoản khác không đọc được dữ liệu của nhau.
- Form tìm instrument và profile hoạt động với catalog mock.
- Build FE và cài đặt BE chạy được từ môi trường sạch.
- Stub phát các chunk theo hình dạng stream của lõi; thử nghiệm đọc được ít nhất một báo cáo và decision hợp lệ/REVIEW, tạo output đúng schema công khai và không phát revision trùng khi nội dung không đổi.
- Fixture input giữ nguyên ngày nghiệp vụ, có timezone instrument và clock UTC thay được trong test. Ghi lại các chỗ lõi cần sửa để API/engine thống nhất khi qua ngày mới; không gọi LLM/vendor và chưa bật adapter live trong ứng dụng.

Output của thử nghiệm là mã thử, fixture và kiểm thử ánh xạ tối thiểu để tái sử dụng ở mốc 5. Nếu phát hiện lệch schema, cập nhật contract/FE fixture ngay tại mốc 2; việc chưa có provider/key không chặn thử nghiệm. Đây chưa phải nghiệm thu FR-21.

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
- Khi cancel_requested commit trước kết quả engine thành công, supervisor xác nhận process đã thoát rồi commit cancelled/steps/finished_at, dọn claim/lease và ghi một run.cancelled; không lưu decision hoặc báo cáo cuối chưa publish. Thứ tự ngược lại trả 409 khi hủy.
- Bấm thử lại liên tiếp, mất response và reload cùng tab giữ key của cùng ý định; replay vẫn mở cùng ID mới dù quota đã đầy. Phiên nguồn giữ nguyên và không tạo nhiều run mới.
- Worker chết làm phiên thất bại sau lease/recovery; thử lại tạo run mới.
- Rating null không bị hiển thị thành Hold.
- Lịch sử vẫn đọc được khi backend restart.
- Tìm mã/tên qua q kết hợp các filter cho cùng kết quả giữa FE/API; ngày đến bao gồm cả ngày đã chọn.
- Mở Tiến trình muộn vẫn đọc đủ event; report thay đổi revision làm mới nội dung đang đọc mà không cần tải lại cả trang.

Đây là mốc kiểm chứng FE/BE bằng mock trước khi tích hợp engine thật trong cùng MVP1; chưa phải mốc nghiệm thu MVP1.

## 6. Mốc 5 — Tích hợp TradingAgents và nghiệm thu MVP1

Backend nối `AnalysisEngine` với mã lõi, cấu hình provider dữ liệu/mô hình thật, bật catalog/profile live đã xác nhận hỗ trợ, cô lập config/storage/checkpoint và map báo cáo/rating. Frontend dùng cùng API để tạo phiên live, xem tiến độ, báo cáo/kết luận và mở lại lịch sử; chỉ điều chỉnh schema khi nhu cầu được thống nhất qua API contract.

Tiêu chí hoàn thành:

- TC-13 đạt: trên máy demo, một instrument/profile được provider thật hỗ trợ chạy từ FE qua API/Worker/adapter đến lõi, hiển thị tiến độ, lưu báo cáo/kết luận và đọc lại từ lịch sử sau reload/restart; API/UI có `data_mode = live`.
- Hai phiên cùng instrument/ngày có artifact, checkpoint và kết quả riêng.
- Backend không dùng singleton graph giữa các phiên.
- Test thông thường và CI mặc định dùng mock/stub; smoke test gọi provider thật là bước chủ động bắt buộc trước nghiệm thu MVP1. Không thay dữ liệu thật bằng fixture hoặc tự chuyển sang mock khi nguồn lỗi.
- Credential và payload nội bộ không xuất hiện trong API/log công khai.
- Engine lỗi, quá hạn và output REVIEW được map đúng hợp đồng.
- API, adapter và helper ngày hiện tại/historical của lõi dùng timezone instrument trong context từng run. Test clock cố định qua nửa đêm/DST và timezone máy khác nhau cho cùng kết quả; CLI không truyền context mới vẫn giữ hành vi cũ.
- Profile live chỉ bật sau khi các công cụ của profile đã được kiểm tra ranh giới ngày nghiệp vụ và chuyển timestamp UTC đúng quy tắc.
- Ghi bằng chứng TC-13 gồm môi trường, provider, instrument/ngày/profile, run_id và báo cáo/kết quả; hướng dẫn local có cách cấu hình provider phía server mà không đưa secret vào tài liệu.
- FR-01–FR-21, NFR-01–NFR-12 và TC-01–TC-13 đều đạt; hồi quy mock/CLI vẫn đạt trước khi chốt MVP1 và chuyển sang giai đoạn bảng điện.

## 7. Ma trận kiểm thử cần xây khi triển khai

| Lớp | Ca kiểm thử có giá trị |
|---|---|
| Frontend component | Form báo lỗi đúng trường, label trạng thái/quality, report Markdown an toàn |
| Frontend với mock API | Polling dừng terminal, mất session, mạng gián đoạn; double click retry/mất response/reload dùng cùng key và mở đúng run mới |
| Backend domain | Chuyển trạng thái hợp lệ; kết quả thành công đến sau cancel_requested phải xác nhận dừng rồi cancelled, không có decision; retry source terminal |
| Backend tích hợp PostgreSQL | Idempotency create/retry đồng thời, replay retry trước quota/capability, quota đồng thời, claim nhiều worker, ghi sau mất lease bị chặn; barrier cho cả hai thứ tự commit hủy/hoàn tất |
| Backend quyền truy cập | Đọc run/report/event của người khác, CSRF và session hết hạn |
| E2E | CI chạy mock; nghiệm thu MVP1 bắt buộc thêm TC-13 với lõi/provider thật: login → tạo → tiến độ → báo cáo/kết luận → mở lại lịch sử |
| Phục hồi | Tắt worker giữa phiên, restart backend, timeout process con, retry mới |
| Adapter | Thử nghiệm stream/report/rating bằng stub từ mốc 2; mốc 5 thêm cô lập cùng ticker/ngày, lỗi engine và clock cố định qua ranh giới ngày/DST/timezone máy |

Các test về claim, khóa và transaction dùng PostgreSQL thật trong môi trường test, vì SQLite không có cùng hành vi SKIP LOCKED. Không gọi LLM thật trong CI mặc định.

CI dùng mock không thay thế bằng chứng nghiệm thu dữ liệu thật của TC-13. Thiếu provider/key có thể tiếp tục kiểm thử mốc 1–4, nhưng chưa thể nghiệm thu MVP1.

## 8. Môi trường và CI dự kiến

Compose cho ứng dụng web sẽ có reverse proxy phục vụ FE static, API, worker và PostgreSQL. Dùng volume cho database và artifact; `.env` server được loại khỏi Git. Compose hiện có phục vụ CLI, cần được bổ sung hoặc tách thành cấu hình web khi triển khai.

| Pipeline | Kiểm tra |
|---|---|
| Frontend | Typecheck, lint, component/API mock test, production build |
| Backend | Ruff, unit/integration test, migration từ DB rỗng |
| Contract | Xuất OpenAPI, sinh FE types, phát hiện thay đổi chưa commit |
| E2E | Chạy toàn luồng bằng mock engine |
| Nghiệm thu live MVP1 | Chạy chủ động TC-13 với lõi và provider thật trên môi trường demo; lưu bằng chứng riêng trước khi chốt mốc 5 |
| Đóng gói lõi | Giữ kiểm tra cài đặt package và import hiện tại |

Trong runtime, migration chạy một lần ở bước release; API/worker không tự cạnh tranh chạy migration khi startup. API readiness chỉ thành công khi schema phù hợp.

## 9. Đầu việc, phụ trách và dependency

Đơn vị ước lượng là **ngày công của một người**, gồm triển khai và kiểm thử liên quan; đây là khoảng dự kiến để lập sprint, chưa phải lịch cam kết. FE/BE là vai trò chịu trách nhiệm đầu ra; tên thành viên, reviewer và ngày giao phải được nhóm gán trước khi kéo việc vào sprint. Dependency là điều kiện hoàn tất/tích hợp; FE có thể làm sớm bằng fixture đã chốt.

| ID | Mốc | Đầu việc / đầu ra | Phụ trách | Ngày công dự kiến | Dependency |
|---|---|---|---|---|---|
| M1-01 | 1 | Schema/OpenAPI, enum, lỗi, lifecycle và fixture contract | BE | 1–2 | Không |
| M1-02 | 1 | Wireframe, trạng thái màn hình, FE fixture/types | FE | 1–2 | M1-01 |
| M1-03 | 1 | Bảng ánh xạ stream/report/decision và khảo sát timezone lõi | BE, FE đối chiếu | 0.5–1 | M1-01 |
| M1-04 | 1 | Chọn instrument/profile/provider thật; xác nhận quyền truy cập và ngân sách theo OPEN-04 | BE + vận hành | 0.5–1 | M1-03 |
| M2-01 | 2 | FastAPI, DB/migration, auth/CSRF, lệnh user và catalog | BE | 2–3 | M1-01 |
| M2-02 | 2 | App shell/router, session, login và form catalog | FE | 2–3 | M1-02, M2-01 |
| M2-03 | 2 | Thử nghiệm adapter bằng stub và kiểm thử ánh xạ schema | BE, FE kiểm tra fixture | 1–2 | M1-03 |
| M3-01 | 3 | Tạo phiên/idempotency/quota, claim/heartbeat và mock engine | BE | 3–4 | M2-01, M2-03 |
| M3-02 | 3 | Form tạo, polling snapshot và timeline | FE | 3–4 | M2-02, M3-01 |
| M4-01 | 4 | Report/decision/history, executor hủy/deadline/recovery và retry | BE | 3–5 | M3-01 |
| M4-02 | 4 | Reader/result/history và UX hủy/thử lại cùng key | FE | 3–4 | M3-02, M4-01 |
| M4-03 | 4 | Compose web/local, CI, E2E mock và kiểm chứng TC-01–TC-12 | FE + BE | 2–3 | M4-01, M4-02 |
| M5-01 | 5 | Adapter production, catalog/profile live, cấu hình provider thật, cô lập storage và sửa clock/timezone lõi | BE | 3–5 | M1-04, M2-03, M4-03, OPEN-04 |
| M5-02 | 5 | Demo live TC-13, hồi quy mock/CLI, hướng dẫn local live và bằng chứng nghiệm thu MVP1 | BE, FE xác nhận UI | 1–2 | M5-01, M4-03 |

Người nhận việc cập nhật issue/PR, tên phụ trách, reviewer, ước lượng sau khảo sát và bằng chứng test cạnh ID tương ứng. Nếu thử nghiệm M2-03 phát hiện phải đổi contract, hoàn tất cập nhật trước M3-01/M3-02. M4-03 là đầu ra kiểm thử trung gian; phải hoàn thành cả M4-03 và M5-02 mới đủ điều kiện nghiệm thu MVP1. Phần bảng điện bắt đầu triển khai sau đó.

### Các quyết định nhóm còn cần cung cấp

- Người phụ trách FE/BE, thời hạn và quy mô demo.
- Bộ UI component, nhận diện trực quan và mức hỗ trợ mobile.
- Provider/market đầu tiên có dữ liệu thực tế đáp ứng, cùng quyền truy cập cần thiết.
- Thời gian lưu dữ liệu, môi trường deploy và ngân sách chạy engine.

Tên thành viên và lịch giao được chốt trước khi lập sprint theo OPEN-01; các thông tin còn lại được chốt ở mốc tương ứng trong requirements. Có thể chuẩn bị schema, fixture hoặc phát triển local bằng mock trước; quyền truy cập provider dữ liệu/mô hình thật phải sẵn sàng cho mốc 5 và nghiệm thu MVP1.

## 10. Sau MVP1 — bảng điện Việt Nam

Triển khai phần này sau khi nghiệm thu MVP1 tại mốc 5: FR-22–FR-26, NFR-13 và TC-14–TC-16. Bắt đầu với bảng điện VN để theo dõi giá cập nhật định kỳ có thể trễ, sau đó bổ sung watchlist, biểu đồ ngày và phân tích từ mã. Luồng phân tích tái sử dụng adapter/lõi đã chạy dữ liệu thật trong MVP1. Thiết kế, API và dữ liệu dự kiến nằm trong [kế hoạch bảng điện](post-mvp-market-workspace.md).

Các yêu cầu này được đánh dấu P1 / Sau MVP1 / Tạm hoãn ở requirements vì chờ hoàn thành MVP1. Chưa chọn nguồn bảng giá VN vẫn có thể nghiệm thu MVP1 nếu luồng phân tích đã có nguồn dữ liệu và mô hình thật; nguồn bảng điện, phạm vi mã và độ trễ được xác nhận riêng ở giai đoạn này.
