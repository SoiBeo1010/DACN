# Đặc tả và quản lý yêu cầu

## 1. Thông tin tài liệu

| Thuộc tính | Giá trị |
|---|---|
| Dự án | DACN — Ứng dụng web quản lý phiên phân tích |
| Phiên bản đặc tả | 0.6 |
| Ngày cập nhật | 2026-11-07 |
| Trạng thái tài liệu | Bản nháp tổng hợp để nhóm rà soát |
| Phạm vi hiện tại | MVP1 gồm frontend, backend và tích hợp lõi TradingAgents qua adapter để phân tích bằng dữ liệu thật; sau MVP1 triển khai bảng điện theo dõi giá |
| Nguồn tổng hợp | Các tài liệu thiết kế FE, BE, API, dữ liệu và kế hoạch trong `docs/` |

Đây là nơi quản lý tập trung những gì sản phẩm cần đáp ứng và cách xác nhận yêu cầu đã đạt. Các tài liệu thiết kế mô tả cách thực hiện. Các lựa chọn công nghệ, bố cục mẫu và tham số vận hành không tự động trở thành yêu cầu nghiệp vụ.

Hiện mới có tài liệu và prototype giao diện; ứng dụng FE/BE theo đặc tả chưa được triển khai. Yêu cầu của luồng phân tích ở trạng thái **Chưa triển khai**; phần bảng điện sau MVP1 được đánh dấu **Tạm hoãn**. Ảnh chụp và prototype không được dùng làm bằng chứng hoàn thành chức năng có backend.

## 2. Mục tiêu, tác nhân và phạm vi

### 2.1. Mục tiêu

**MVP1 giữ luồng ban đầu:** đăng nhập → danh sách phiên → chọn mã/ngày/profile → tạo phiên → theo dõi tiến độ → đọc báo cáo/kết luận → mở lại lịch sử. Trang chính sau đăng nhập là `/analyses`.

MVP1 phải kết nối lõi TradingAgents qua adapter, lấy dữ liệu từ nguồn thật và trả báo cáo/kết luận thực tế cho ít nhất một instrument được hỗ trợ. Hoàn thành luồng giả lập chưa đủ để nghiệm thu MVP1.

Phiên phân tích tồn tại độc lập với browser. MVP1 không yêu cầu bảng điện, watchlist, biểu đồ giá, collector giá định kỳ hoặc panel phân tích trên bảng điện.

Trong quá trình xây MVP1, FE/BE vẫn phải kiểm thử được toàn bộ luồng bằng engine giả lập. Mock/stub phục vụ phát triển và CI; trước khi nghiệm thu MVP1 phải hoàn thành tích hợp TradingAgents, kiểm thử dữ liệu thật và hồi quy luồng ứng dụng. Giai đoạn tiếp theo triển khai bảng điện để theo dõi giá.

### 2.2. Tác nhân

| Tác nhân | Nhu cầu / trách nhiệm |
|---|---|
| Người dùng đã được cấp tài khoản | Tạo và quản lý các phiên thuộc tài khoản của mình |
| Người vận hành trong nhóm | Tạo/vô hiệu hóa tài khoản, cấu hình catalog/profile, chạy dịch vụ và xem log bằng công cụ nội bộ |
| Engine phân tích | Nhận input hợp lệ, cung cấp tiến độ, báo cáo và kết quả qua adapter |

Người vận hành chưa có màn hình quản trị hoặc API đọc phiên của mọi người dùng. Engine là thành phần tích hợp, không đăng nhập bằng tài khoản người dùng để gọi API công khai.

### 2.3. Phạm vi theo giai đoạn

| Giai đoạn | Bao gồm | Điều kiện nghiệm thu |
|---|---|---|
| MVP1 — xây dựng và kiểm thử FE/BE, mốc 1–4 | Tài khoản, catalog, tạo phiên, tiến độ, báo cáo, kết luận, lịch sử, hủy/thử lại, xử lý gián đoạn; mock để phát triển/CI | Các kiểm thử ứng dụng bằng mock đạt tại mốc 4; đây là đầu ra trung gian của MVP1 |
| MVP1 — tích hợp lõi và nghiệm thu, mốc 5 | Adapter TradingAgents, catalog/profile live cho mã được nguồn hỗ trợ, dữ liệu thật, map kết quả và cô lập phiên | FR-01–FR-21, NFR-01–NFR-12 và TC-01–TC-13 đạt; bắt buộc có luồng từ FE đến báo cáo/kết luận thật và đọc lại lịch sử |
| Sau MVP1 — bảng điện theo dõi giá | Giá VN định kỳ có thể trễ, watchlist, biểu đồ ngày và phân tích từ mã | Triển khai sau nghiệm thu MVP1 tại mốc 5; FR-22–FR-26 không chặn MVP1 |

Ngoài phạm vi hiện tại: tự đăng ký, khôi phục mật khẩu, giao diện quản trị, đặt lệnh thật, quản lý danh mục giao dịch, backtest diện rộng, chọn tùy ý provider/model/prompt, thông báo qua bot, chia sẻ công khai báo cáo, xóa lịch sử qua UI và resume thủ công một phiên terminal.

Giai đoạn sau MVP1 triển khai bảng điện chứng khoán Việt Nam, cập nhật định kỳ và có thể trễ. Vendor, độ bao phủ mã và độ trễ thực tế chưa chốt; không bắt buộc tích hợp nguồn bảng giá VN để hoàn thành MVP1, nhưng nguồn dữ liệu thật phục vụ phân tích của TradingAgents là bắt buộc. Giá realtime, nến intraday, sổ lệnh nhiều mức, độ chính xác đầu tư, lợi nhuận, tải lớn và hoạt động 24/7 chưa được cam kết.

## 3. Quy ước quản lý

- `FR`: yêu cầu chức năng; `NFR`: yêu cầu phi chức năng; `BR`: quy tắc nghiệp vụ; `TC`: kịch bản nghiệm thu.
- `P0`: bắt buộc trong giai đoạn được ghi; `P1`: có thể thực hiện sau các yêu cầu bắt buộc của giai đoạn đó.
- FR-01–FR-21, NFR-01–NFR-12 và TC-01–TC-13 áp dụng cho MVP1, gồm cả tích hợp lõi với dữ liệu thật tại mốc 5. FR-22–FR-26, NFR-13, BR-13–BR-15 và TC-14–TC-16 chỉ áp dụng sau MVP1.
- NFR-10 được kiểm tra với API/UI/mock ở các mốc đầu; phần đối chiếu timezone và sửa helper của lõi live phải đạt cùng FR-21 tại mốc 5 trước nghiệm thu MVP1.
- Cột phụ trách chỉ nhóm công việc FE, BE hoặc vận hành; chưa gán tên thành viên.
- Trạng thái triển khai: **Chưa triển khai → Đang triển khai → Chờ kiểm thử → Đạt**. **Tạm hoãn** cần ghi lý do và mốc xem lại.
- Trạng thái **Đạt** yêu cầu có bằng chứng kiểm thử hoặc biên bản nghiệm thu, không chỉ có code hoặc mockup.
- Mỗi yêu cầu giữ ID ổn định. Khi bỏ yêu cầu, ghi trạng thái và lý do thay vì tái sử dụng ID cho nội dung khác.

## 4. Yêu cầu chức năng

### 4.1. Tài khoản và dữ liệu đầu vào

| ID | Yêu cầu | Ưu tiên / giai đoạn | Phụ trách | Tiêu chí nghiệm thu | Trạng thái |
|---|---|---|---|---|---|
| FR-01 | Cho phép đăng nhập bằng tài khoản đã cấp và khôi phục session hợp lệ khi tải lại trang. | P0 · FE/BE | FE + BE | Thông tin đúng mở lịch sử `/analyses` hoặc trang đích hợp lệ đã yêu cầu; sai hiển thị lỗi chung; chưa đăng nhập không đọc được API dữ liệu; tải lại không yêu cầu đăng nhập khi session còn hiệu lực. | Chưa triển khai |
| FR-02 | Cho phép đăng xuất và xử lý session hết hạn. | P0 · FE/BE | FE + BE | Logout thu hồi session; request sau đó bị từ chối; FE dừng polling, xóa cache tài khoản và về đăng nhập khi session kết thúc. | Chưa triển khai |
| FR-03 | Cung cấp công cụ nội bộ để cấp và vô hiệu hóa tài khoản ban đầu. | P0 · FE/BE | BE + vận hành | Tạo tài khoản bằng lệnh nội bộ; user bị vô hiệu hóa không đăng nhập hoặc tiếp tục dùng session cũ; không cần trang tự đăng ký. | Chưa triển khai |
| FR-04 | Cho phép tìm và chọn đối tượng phân tích được hỗ trợ. | P0 · FE/BE | FE + BE | Tìm theo mã/tên; hiển thị tên, sàn, loại tài sản và giới hạn ngày; hai mã giống nhau ở các sàn vẫn phân biệt được qua instrument ID. | Chưa triển khai |
| FR-05 | Cung cấp profile và ngôn ngữ báo cáo phù hợp với đối tượng. | P0 · FE/BE | FE + BE | Form chỉ cho chọn các giá trị hỗ trợ; API kiểm tra lại tổ hợp instrument/profile/ngôn ngữ và chế độ dữ liệu; cấu hình provider bí mật không xuất hiện trên form/API công khai. | Chưa triển khai |
| FR-06 | Kiểm tra input và trả lỗi có thể sửa được trước khi tạo phiên. | P0 · FE/BE | FE + BE | Ngày ngoài phạm vi, ID không hỗ trợ hoặc extra field nhận lỗi chuẩn; chưa tạo run; FE giữ form, đặt lỗi đúng trường và focus trường lỗi đầu tiên. | Chưa triển khai |

### 4.2. Tạo và theo dõi phiên

| ID | Yêu cầu | Ưu tiên / giai đoạn | Phụ trách | Tiêu chí nghiệm thu | Trạng thái |
|---|---|---|---|---|---|
| FR-07 | Tiếp nhận phiên phân tích và trả mã phiên sau khi lưu yêu cầu. | P0 · FE/BE | FE + BE | API trả `202` cùng ID/Location sau commit; phiên ở `queued`; FE mở chi tiết; request không chờ engine hoàn thành; áp dụng BR-01, BR-02. | Chưa triển khai |
| FR-08 | Chống tạo trùng khi gửi lại cùng ý định. | P0 · FE/BE | FE + BE | Gửi đồng thời cùng user/key/input chỉ tạo một run; response mất có thể gửi lại cùng key; key còn hiệu lực nhưng input khác nhận `409`; áp dụng BR-03. | Chưa triển khai |
| FR-09 | Thực thi phiên trong worker, độc lập với browser và request API. | P0 · FE/BE | BE | Đóng trang không dừng phiên; hai worker claim đồng thời không thực thi cùng run; queued chưa claim còn tồn tại sau khi restart; áp dụng BR-04, BR-11. | Chưa triển khai |
| FR-10 | Hiển thị snapshot tiến độ của phiên và trạng thái từng giai đoạn. | P0 · FE/BE | FE + BE | Hiển thị trạng thái, bước hiện tại, thời gian và báo cáo đã có từ API; tải lại không khởi chạy thêm phiên; terminal dừng polling; áp dụng BR-04, BR-12. | Chưa triển khai |
| FR-11 | Cung cấp lịch sử sự kiện theo từng phiên. | P0 · FE/BE | FE + BE | Sự kiện có thứ tự tăng; FE đọc tiếp từ cursor và loại trùng; người dùng thấy bắt đầu, hoàn thành bước, báo cáo sẵn sàng và trạng thái kết thúc; không lộ payload nội bộ. | Chưa triển khai |
| FR-12 | Giữ snapshot gần nhất và phục hồi giao diện khi kết nối gián đoạn. | P0 · FE/BE | FE | Mất mạng không xóa báo cáo đang đọc; hiển thị mất kết nối; khi phục hồi lấy trạng thái mới; `401/404` được xử lý theo API contract và không polling vô hạn. | Chưa triển khai |

### 4.3. Báo cáo, kết luận và lịch sử

| ID | Yêu cầu | Ưu tiên / giai đoạn | Phụ trách | Tiêu chí nghiệm thu | Trạng thái |
|---|---|---|---|---|---|
| FR-13 | Cho phép đọc các báo cáo đã lưu, kể cả khi phiên chưa hoàn tất. | P0 · FE/BE | FE + BE | Mở từng phần đúng phiên; nội dung cache được làm mới khi revision tăng; báo cáo hoàn thành vẫn đọc được khi failed/cancelled; không hiển thị phần chưa có. | Chưa triển khai |
| FR-14 | Hiển thị kết luận và chất lượng kết luận độc lập với trạng thái thực thi. | P0 · FE/BE | FE + BE | Hiển thị một trong năm rating khi hợp lệ; `needs_review` có cảnh báo và rating null; không đổi thiếu dữ liệu thành Hold; trường không được cung cấp không được tạo thêm; áp dụng BR-05, BR-06. | Chưa triển khai |
| FR-15 | Cung cấp lịch sử cá nhân có tìm kiếm, lọc và phân trang. | P0 · FE/BE | FE + BE | Tìm q theo mã/tên trong snapshot; kết hợp instrument, trạng thái và khoảng ngày tạo bằng AND; mới nhất trước; cursor và URL giữ đúng bộ lọc; có trạng thái rỗng/không tìm thấy. | Chưa triển khai |
| FR-16 | Cho phép mở trực tiếp một phiên đã có. | P0 · FE/BE | FE + BE | Sau đăng nhập, mở URL/refresh trang chi tiết đọc đúng snapshot của owner; kết quả đã lưu đọc lại sau restart dịch vụ; URL không tạo run mới. | Chưa triển khai |

### 4.4. Hủy, thử lại và xử lý gián đoạn

| ID | Yêu cầu | Ưu tiên / giai đoạn | Phụ trách | Tiêu chí nghiệm thu | Trạng thái |
|---|---|---|---|---|---|
| FR-17 | Cho phép hủy phiên hợp lệ và theo dõi quá trình dừng. | P0 · FE/BE | FE + BE | Hủy queued chuyển cancelled; hủy running chuyển cancel_requested rồi terminal khi được xác nhận; nếu kết quả thành công đến sau hủy, xác nhận process đã thoát rồi commit cancelled, không có decision; thao tác lặp không sinh sự kiện trùng; giữ báo cáo đã có; áp dụng BR-07. | Chưa triển khai |
| FR-18 | Cho phép thử lại phiên thất bại hoặc đã hủy bằng một phiên mới. | P0 · FE/BE | FE + BE | Run mới có ID khác và liên kết nguồn; double click, mất response hoặc reload cùng tab giữ key đang chờ và chỉ tạo một run mới; `202` mở đúng ID mới; giữ lịch sử cũ; snapshot nguồn được dùng nếu còn khả dụng; source không hợp lệ hoặc cấu hình không còn chạy được nhận `409`; áp dụng BR-03, BR-08. | Chưa triển khai |
| FR-19 | Xác định và công bố lỗi engine, quá hạn hoặc mất worker. | P0 · FE/BE | BE + FE | Run chuyển failed cùng mã/thông báo công khai; process quá hạn bị dừng; worker mất claim không ghi kết quả muộn; có đường thử lại chủ động; áp dụng BR-11. | Chưa triển khai |

### 4.5. Engine giả lập và tích hợp

| ID | Yêu cầu | Ưu tiên / giai đoạn | Phụ trách | Tiêu chí nghiệm thu | Trạng thái |
|---|---|---|---|---|---|
| FR-20 | Cung cấp mock engine để chạy xuyên suốt ứng dụng và kiểm thử mà không cần provider. | P0 · FE/BE | BE + FE | Chạy được thành công, needs_review, lỗi, chờ lâu, hủy và mất worker bằng fixture/stub; không gọi LLM/vendor thật; chế độ mock được gắn nhãn trên các màn hình; áp dụng BR-09. | Chưa triển khai |
| FR-21 | Tích hợp lõi TradingAgents qua adapter với hợp đồng tiến độ/báo cáo/kết quả đã chốt ngay trong MVP1. | P0 · MVP1 | BE + FE | Từ FE, ít nhất một instrument/profile live gọi lõi với provider dữ liệu và mô hình thật, hiển thị tiến độ, lưu báo cáo/kết luận và đọc lại từ lịch sử; data_mode = live, không thay kết quả bằng fixture; hai phiên cùng mã/ngày không dùng lẫn state, file hoặc checkpoint; output REVIEW map đúng; TC-13 bắt buộc trước nghiệm thu MVP1, CI mặc định vẫn dùng stub; áp dụng BR-09, BR-10. | Chưa triển khai |

### 4.6. Bảng điện và theo dõi giá — sau MVP1

Nhóm yêu cầu dưới đây được lưu để triển khai sau MVP1. Giữ ID để truy vết, không đưa vào đường đi bắt buộc hoặc tiêu chí nghiệm thu của MVP1. Bản thiết kế dự kiến nằm tại [backlog bảng điện](planning/post-mvp-market-workspace.md).

| ID | Yêu cầu | Ưu tiên / giai đoạn | Phụ trách | Tiêu chí nghiệm thu | Trạng thái |
|---|---|---|---|---|---|
| FR-22 | Bảng điện VN là trang chính sau đăng nhập khi triển khai mở rộng. | P1 · Sau MVP1 | FE + BE | Hiển thị mã/tên/sàn, giá gần nhất, thay đổi và tổng khối lượng khi có; tìm/lọc trong catalog hỗ trợ; mỗi dòng có xem chi tiết và phân tích. | Tạm hoãn |
| FR-23 | Lưu watchlist cá nhân để theo dõi nhanh các mã. | P1 · Sau MVP1 | FE + BE | Thêm/bỏ mã, không trùng, còn sau reload/restart DB; người khác không thay đổi watchlist; không coi watchlist là danh mục sở hữu. | Tạm hoãn |
| FR-24 | Cập nhật giá định kỳ và hiển thị độ mới dữ liệu. | P1 · Sau MVP1 | FE + BE | Hiển thị thời điểm giá và lần fetch; lỗi nguồn giữ giá cũ có nhãn; thiếu giá hiển thị —; tách mock/live, delayed/unknown và thị trường đóng cửa; áp dụng BR-13. | Tạm hoãn |
| FR-25 | Cho phép xem chi tiết mã và biểu đồ OHLCV ngày. | P1 · Sau MVP1 | FE + BE | Chọn mã từ bảng điện mở đúng instrument ID; biểu đồ có đơn vị, thời gian và khoảng ngày hỗ trợ; không có dữ liệu có trạng thái riêng; không hứa nến intraday. | Tạm hoãn |
| FR-26 | Khởi tạo phân tích ngay từ bảng điện/chi tiết mã. | P1 · Sau MVP1 | FE + BE | Form điền sẵn mã, user xác nhận ngày/profile; dùng cùng API/idempotency; theo dõi ở panel hoặc trang đầy đủ, bảng điện vẫn cập nhật; giá đổi không tự gọi LLM; áp dụng BR-14, BR-15. | Tạm hoãn |

## 5. Yêu cầu phi chức năng

Các tiêu chí dưới đây là điều kiện kiểm chứng hành vi. Chưa đặt SLA công khai, số người dùng đồng thời hay ngưỡng response time khi chưa có môi trường đo tải được thống nhất.

| ID | Yêu cầu | Ưu tiên / giai đoạn | Tiêu chí nghiệm thu | Trạng thái |
|---|---|---|---|---|
| NFR-01 | Bảo vệ dữ liệu theo chủ sở hữu. | P0 · FE/BE | User B không đọc/hủy/thử lại run, report hoặc event của A dù biết ID; API trả `404` cho resource của người khác; owner lấy từ session, không tin input browser. | Chưa triển khai |
| NFR-02 | Bảo vệ tài khoản và session. | P0 · FE/BE | Password chỉ lưu hash phù hợp; session được thu hồi server-side; cookie production có HttpOnly/Secure/SameSite; mutation sai CSRF và login sai origin bị chặn; có rate limit cấu hình được. | Chưa triển khai |
| NFR-03 | Giữ secret và nội dung không tin cậy trong ranh giới phù hợp. | P0 · FE/BE | Không có API key, token, password, prompt hoặc stack trace trong bundle/API/log công khai; Markdown có HTML/script và URL nguy hiểm không thực thi trong trình duyệt. | Chưa triển khai |
| NFR-04 | Giữ dữ liệu nhất quán khi có request hoặc worker đồng thời. | P0 · FE/BE | Integration test PostgreSQL chứng minh idempotency/quota/claim đúng khi chạy đồng thời; snapshot không trộn phiên bản; decision và terminal state commit cùng nhau; kết quả từ claim cũ bị từ chối. | Chưa triển khai |
| NFR-05 | Dữ liệu đã xác nhận phải tồn tại qua restart thông thường. | P0 · FE/BE | Restart API/worker trong khi giữ DB/volume không làm mất queued, báo cáo hoặc lịch sử đã commit; không dùng file local tạm làm nguồn duy nhất cho dữ liệu UI. | Chưa triển khai |
| NFR-06 | Thực thi tác vụ có giới hạn và quan sát được. | P0 · FE/BE | Engine có deadline, số lần retry hữu hạn, hạn mức run hoạt động; worker phát heartbeat; lỗi/terminal có request_id hoặc run_id để tra log; health phân biệt liveness/readiness. | Chưa triển khai |
| NFR-07 | API tiếp tục phục vụ khi engine chạy lâu; FE chỉ đồng bộ khi cần. | P0 · FE/BE | Mock engine được giữ chờ; đồng thời login/GET/history/create không phải chờ engine kết thúc; tab ẩn và phiên terminal không tiếp tục polling định kỳ; thời gian thực tế được đo ở mốc load test. | Chưa triển khai |
| NFR-08 | Giao diện dùng được trên desktop và mobile. | P0 · FE/BE | Kiểm tra luồng chính ở bề rộng 390, 768 và 1440 px; không tràn ngang toàn trang; nội dung bảng dài được xử lý trong vùng riêng; nút/form không bị cắt. | Chưa triển khai |
| NFR-09 | Hỗ trợ sử dụng bằng bàn phím và trạng thái dễ hiểu. | P0 · FE/BE | Form có label; lỗi liên kết trường; focus nhìn thấy; dialog trả focus khi đóng; trạng thái có chữ ngoài màu; luồng login/create/detail dùng được bằng bàn phím. | Chưa triển khai |
| NFR-10 | Dữ liệu ngày giờ và chế độ dữ liệu được biểu diễn nhất quán. | P0 · FE/BE | Timestamp API là UTC ISO 8601; ngày nghiệp vụ, giới hạn catalog và validation theo timezone instrument, không phụ thuộc timezone máy; UI hiển thị đúng ngữ cảnh; không trộn mock/live; mock có nhãn cả ở lịch sử, chi tiết và báo cáo. API/engine được đối chiếu clock qua nửa đêm/DST ở mốc 5 trong MVP1. | Chưa triển khai |
| NFR-11 | Hợp đồng FE/BE và migration có thể kiểm chứng lặp lại. | P0 · FE/BE | OpenAPI sinh từ schema; FE types/fixture được kiểm tra tương thích; migration chạy từ DB rỗng; có E2E mock và kiểm tra cài đặt lõi; CI mặc định không cần khóa provider thật. | Chưa triển khai |
| NFR-12 | Có thể chạy demo mà chưa cần thuê máy chủ hoặc mua tên miền. | P0 · FE/BE | Có hướng dẫn chạy local FE/API/worker/PostgreSQL với TradingAgents adapter và cấu hình provider phía server; demo trọn luồng với dữ liệu thật trên máy nhóm được chọn trước nghiệm thu MVP1; kèm chế độ mock để phát triển/CI; deployment thật và tài nguyên tối thiểu được xác nhận riêng, không giả định gói hosting miễn phí chạy worker liên tục. | Chưa triển khai |
| NFR-13 | Theo dõi giá dùng tài nguyên có giới hạn và độc lập với phân tích AI. | P1 · Sau MVP1 | Giá được fetch theo lô/cache dùng chung; thêm user không tạo một collector riêng; tab ẩn dừng polling giá; engine chạy lâu không chặn quote API; chu kỳ nguồn và backoff cấu hình được. | Tạm hoãn |

NFR-12 ghi nhận ràng buộc nguồn lực hiện tại. Tên nhà cung cấp hosting, giá dịch vụ và các quyền lợi miễn phí không phải cam kết trong đặc tả này. NFR-13 chỉ áp dụng khi triển khai bảng điện sau MVP1.

## 6. Quy tắc nghiệp vụ

| ID | Quy tắc | Liên quan |
|---|---|---|
| BR-01 | Một phiên thuộc đúng một user, có một instrument ID, ngày dữ liệu, profile/version và ngôn ngữ. Chủ sở hữu được xác định từ session. | FR-07, NFR-01 |
| BR-02 | Input và cấu hình đã resolve được snapshot khi tạo, bất biến trong phiên; secret không được snapshot. Thay catalog/profile về sau không sửa kết quả lịch sử. | FR-05, FR-07, FR-16 |
| BR-03 | Idempotency key có phạm vi user, hiệu lực mặc định 24 giờ. Cùng key và request chuẩn hóa trả resource cũ trước kiểm tra capability/quota hiện tại; request khác bị từ chối. Ý định mới có key mới; retry endpoint cũng có chống trùng. FE giữ key của ý định retry chưa rõ kết quả khi gửi lại/reload cùng tab; hết 24 giờ không tự tạo key để gửi tiếp. | FR-08, FR-18 |
| BR-04 | Lifecycle gồm queued, running, cancel_requested, succeeded, failed, cancelled. Ba trạng thái cuối là terminal, không chuyển ngược; mở lại trang không khởi chạy phiên mới. | FR-09, FR-10, FR-16 |
| BR-05 | Trạng thái thực thi và chất lượng kết luận là hai thuộc tính riêng. Succeeded cần có decision; valid cần một rating hợp lệ; needs_review dùng rating null. Không có kết quả cuối vì engine hỏng là failed. | FR-14, FR-19 |
| BR-06 | Năm rating là Buy, Overweight, Hold, Underweight, Sell. REVIEW của lõi được chuyển thành needs_review, không phải Hold. FE chỉ trình bày các trường backend thực sự cung cấp. | FR-14, FR-21 |
| BR-07 | Hủy queued có hiệu lực ngay. Hủy running phải chờ xác nhận dừng; request provider đang bay có thể chưa dừng tức thời. Nếu cancel_requested commit trước, kể cả engine trả kết quả thành công sau đó, supervisor xác nhận process đã thoát rồi commit cancelled/steps/finished_at, dọn claim/lease và ghi một run.cancelled khi còn claim/lease hợp lệ; không công bố decision hoặc báo cáo cuối chưa publish. Nếu succeeded commit trước, hủy nhận 409. | FR-17 |
| BR-08 | Chỉ failed/cancelled được thử lại; tạo run mới liên kết run cũ và dùng snapshot cũ nếu còn hỗ trợ. Không sửa trạng thái hoặc báo cáo lịch sử. Cấu hình cũ không khả dụng trả lỗi để tạo yêu cầu mới. | FR-18 |
| BR-09 | Mock và live là hai chế độ tách biệt. Không ghép instrument mock với profile live hoặc ngược lại. Live chỉ dữ liệu nguồn thật, không bảo đảm dữ liệu tức thời; lỗi nguồn live không tự chuyển sang mock. Kịch bản lỗi giả lập chỉ bật ở môi trường dev/test. | FR-05, FR-20, FR-21, NFR-10 |
| BR-10 | State, memory, artifact và checkpoint được cô lập theo run. MVP không chia sẻ bộ nhớ liên phiên. Các báo cáo hoàn thành vẫn được lưu và đọc khi run failed/cancelled. | FR-13, FR-21 |
| BR-11 | Worker chỉ được ghi khi còn claim và lease hợp lệ. Lease hết hạn dẫn tới failed/WORKER_LOST qua recovery; quá deadline là failed/RUN_TIMEOUT. Không tự chạy lại cả phiên; người dùng chủ động thử lại. | FR-09, FR-19, NFR-04 |
| BR-12 | Snapshot tiến độ lấy từ server. Event tăng theo run; FE đọc từ after=0 lần đầu, sau đó từ next_cursor đã tải và dedupe, không nhảy theo event_cursor của snapshot. Báo cáo thay đổi tăng revision để FE làm mới cache. Không tạo số liệu hoặc phần trăm giả định. | FR-10, FR-11, FR-13, FR-14 |
| BR-13 | **Sau MVP1:** quoted_at là thời điểm dữ liệu giá từ nguồn; fetched_at là lúc server lấy. Fetch lại giá cũ không làm nó thành mới. Thiếu giá dùng null; độ trễ không biết được ghi rõ. | FR-24 |
| BR-14 | **Sau MVP1:** giá bảng điện và dữ liệu phân tích là hai ngữ cảnh. Giá mới không sửa phiên cũ. Chỉ ghi snapshot giá khi tương thích ngày phân tích; không nhận giá tương lai cho phân tích lịch sử. | FR-14, FR-26 |
| BR-15 | **Sau MVP1:** đọc giá/biểu đồ không gọi LLM; user xác nhận tạo phiên, backend resolve giá. Watchlist chỉ lưu mã yêu thích; không cấp quyền đọc kết quả của user khác. | FR-23, FR-26, NFR-01, NFR-13 |

### 6.1. Tham số khởi đầu có thể cấu hình

| Tham số | Giá trị đề xuất hiện tại | Cách áp dụng |
|---|---|---|
| Phiên hoạt động mỗi user | 2 | Tính queued/running/cancel_requested; vượt giới hạn trả 429 |
| Poll chi tiết / lịch sử đang hoạt động | 2 giây / 5 giây | Chỉ khi tab hiển thị và còn phiên hoạt động |
| Worker concurrency | 1 run/process | Tăng số worker sau kiểm tra tài nguyên |
| Heartbeat / lease | 10 giây / 60 giây | Đo lease theo đồng hồ DB; chỉ gia hạn khi còn claim |
| Deadline một phiên | 15 phút | Rà soát lại khi chạy engine live |
| Hạn session tuyệt đối | 8 giờ | Logout/vô hiệu hóa user có thể kết thúc sớm |
| Hạn idempotency key | 24 giờ | Key hết hạn được xử lý trong transaction |
| Phân trang danh sách | Mặc định 20, tối đa 100 | Cursor theo created_at và ID |

Đây là baseline để triển khai và thử nghiệm, không phải SLA hay ngân sách đã đo. Khi thay đổi tham số cần đồng bộ cấu hình, API contract và kịch bản liên quan.

## 7. Liên kết yêu cầu với màn hình, API và kiểm thử

Mã màn hình S01–S06 tham chiếu [planning giao diện](frontend/ui-planning.md): đăng nhập, lịch sử, tạo phiên, tiến độ, kết quả và báo cáo. S04/S05/S06 là các cách hiển thị của cùng resource phiên phân tích.

S07 (bảng điện) và S08 (chi tiết cổ phiếu) chỉ thuộc [phần mở rộng sau MVP1](planning/post-mvp-market-workspace.md). Prototype hiện tại minh họa đúng luồng phân tích của MVP1; chưa cần hai màn hình này để nghiệm thu.

| Yêu cầu | Màn hình / thành phần | API hoặc điểm tích hợp | Kịch bản nghiệm thu |
|---|---|---|---|
| FR-01, FR-02, FR-03 | S01 → S02, AppShell; lệnh quản trị | `/auth/login`, `/auth/session`, `/auth/logout`; công cụ cấp user | TC-01, TC-02 |
| FR-04, FR-05, FR-06 | S03 | `/instruments`, `/analysis-profiles`, validation `/analyses` | TC-03 |
| FR-07, FR-08 | S03 → S04 | `POST /analyses`, transaction idempotency | TC-04, TC-05 |
| FR-09 | Worker, S04 | Claim/lease/executor, không có endpoint worker công khai | TC-05, TC-10 |
| FR-10, FR-11, FR-12 | S04, tab Tiến trình | `GET /analyses/{id}`, `/events` | TC-06, TC-10 |
| FR-13, FR-14 | S04, S05, S06 | `GET /analyses/{id}`, `/reports`, `/reports/{report_id}` | TC-07, TC-08 |
| FR-15, FR-16 | S02, S04/S05 | `GET /analyses`, `GET /analyses/{id}` | TC-09 |
| FR-17, FR-18 | S04, dialog hủy, nút thử lại | `POST /analyses/{id}/cancel`, `/retry` | TC-11 |
| FR-19 | S04 lỗi; worker/recovery | Snapshot error, heartbeat, deadline | TC-10 |
| FR-20 | S01–S06, Mock engine | Hợp đồng engine và fixture dev/test | TC-04 đến TC-12 |
| FR-21 | Adapter engine, S04–S06 | TradingAgents → AnalysisEngine | TC-13 |
| FR-22, FR-24 | Sau MVP1: S07, S08 | API dự kiến `/market/quotes`, `/instruments/{id}` | TC-14 · Sau MVP1 |
| FR-23 | Sau MVP1: S07 watchlist | API dự kiến `/watchlist`, `/watchlist/items/{instrument_id}` | TC-15 · Sau MVP1 |
| FR-25, FR-26 | Sau MVP1: S07/S08 → panel phân tích | API dự kiến `/instruments/{id}/ohlcv`, `POST /analyses` | TC-16 · Sau MVP1 |

Các đường API rút gọn trong bảng dùng prefix `/api/v1`. Chi tiết request, response, mã lỗi và phân trang nằm tại [hợp đồng API](backend/api-contract.md).

## 8. Kịch bản nghiệm thu

Đây là danh mục kiểm thử dự kiến, chưa phải kết quả test đã đạt. TC-01–TC-13 đều bắt buộc cho MVP1; TC-13 xác nhận tích hợp lõi và dữ liệu thật tại mốc 5. TC-14–TC-16 chỉ áp dụng sau MVP1. Test transaction/claim dùng PostgreSQL thật; kiểm thử ứng dụng tự động dùng mock, còn phần chạy live của TC-13 gọi provider thật và lưu bằng chứng nghiệm thu riêng.

| ID | Kịch bản và kết quả mong đợi | Yêu cầu chính |
|---|---|---|
| TC-01 | Đăng nhập đúng/sai, refresh, logout, hết hạn và vô hiệu hóa tài khoản; quyền truy cập/cache phản ánh session mới nhất. | FR-01, FR-02, FR-03, NFR-02 |
| TC-02 | A tạo phiên, B thử GET/report/event/cancel/retry bằng ID của A; đều bị từ chối. Sai CSRF, sai origin và vượt rate limit cũng bị chặn. | NFR-01, NFR-02 |
| TC-03 | Tìm instrument trùng mã khác sàn; chọn profile/ngày/ngôn ngữ hợp lệ và không hợp lệ; chỉ tổ hợp hỗ trợ được tạo phiên. | FR-04, FR-05, FR-06 |
| TC-04 | Từ form, tạo phiên mock, xem tiến độ, báo cáo và kết luận; đóng rồi mở URL vẫn đọc đúng phiên; không gọi provider thật. | FR-07, FR-10, FR-13, FR-20 |
| TC-05 | Gửi đồng thời cùng key, khác key ở biên hạn mức, key khác payload và claim bằng hai worker; không tạo trùng hoặc vượt quy tắc quota/claim. | FR-08, FR-09, NFR-04 |
| TC-06 | Mở Tiến trình muộn, đọc nhiều trang/lặp event, đổi tab, terminal và mất mạng; FE không bỏ sót sự kiện cuối, dedupe, giữ snapshot và dừng poll đúng lúc. | FR-10, FR-11, FR-12, NFR-07 |
| TC-07 | Đọc báo cáo khi running/failed/cancelled; giữ ngữ cảnh và tải lại khi revision tăng; response revision cũ không ghi đè mới; HTML/script/URL nguy hiểm không thực thi. | FR-13, NFR-03 |
| TC-08 | Kiểm tra năm rating và REVIEW; hoàn tất xử lý với needs_review không thành Hold; trường thiếu không bị bịa; decision/terminal nhất quán. | FR-14, NFR-04, NFR-10 |
| TC-09 | Tìm q kết hợp filter/đọc cursor, kiểm tra ngày đến được bao gồm theo timezone, đổi filter bỏ cursor cũ; mở URL và restart giữ DB vẫn đọc được queued/history/report. | FR-15, FR-16, NFR-05 |
| TC-10 | Giữ engine chạy lâu, đọc API khác, dừng worker, chờ hết lease rồi recovery; thử ghi từ claim cũ; deadline dừng process; lỗi công khai có mã tra cứu. | FR-09, FR-19, NFR-04, NFR-06, NFR-07 |
| TC-11 | Hủy queued/running/lặp hủy; dùng barrier ép cả hai thứ tự commit hủy/hoàn tất. Hủy thắng phải cancelled sau khi process thoát, không decision/run.succeeded, giữ report đã commit và dọn claim/lease. Thử lại failed/cancelled với double click, mất response/reload, request đồng thời cùng key, replay khi quota đã đầy/cấu hình vừa bị tắt; chỉ một run mới, mở đúng ID. Ý định mới gặp cấu hình cũ không hỗ trợ nhận 409. | FR-17, FR-18, NFR-04 |
| TC-12 | Kiểm tra luồng ở 390/768/1440 px và bàn phím; mock/live badge, timezone và trạng thái; build/type/contract/migration/E2E trong môi trường sạch. | FR-20, NFR-08, NFR-09, NFR-10, NFR-11 |
| TC-13 | **Bắt buộc trong MVP1:** trên môi trường demo, đăng nhập, chọn instrument/profile live, tạo phiên từ FE, Worker gọi lõi TradingAgents với nguồn dữ liệu và mô hình thật, xem tiến độ/báo cáo/kết luận rồi mở lại từ lịch sử sau reload/restart; API/UI giữ data_mode = live. Ghi môi trường, provider, instrument/ngày/profile, run_id và bằng chứng kết quả; không dùng fixture thay dữ liệu thật. Hai run cùng mã/ngày cô lập; stub lỗi/REVIEW map đúng; secret không xuất hiện ở UI/API/log công khai. Clock cố định quanh nửa đêm/DST với Asia/Ho_Chi_Minh và America/New_York trên máy khác timezone cho API/engine cùng giới hạn ngày và phân loại historical/live; không đổi ngày snapshot, CLI cũ không bị đổi hành vi. | FR-07, FR-10, FR-13, FR-14, FR-16, FR-21, NFR-03, NFR-10, NFR-12 |
| TC-14 | **Sau MVP1:** bảng điện poll theo lô, xử lý giá cũ/thiếu/lỗi/đóng cửa; chia sẻ cache, không chặn bởi engine. | FR-22, FR-24, NFR-13 |
| TC-15 | **Sau MVP1:** thêm/bỏ mã, reload, đổi tài khoản; watchlist không trùng hoặc lẫn owner. | FR-23, NFR-01 |
| TC-16 | **Sau MVP1:** phân tích từ mã, biểu đồ/ngày đúng; giá cập nhật không sửa kết luận cũ hoặc tự gọi mô hình. | FR-25, FR-26, BR-14, BR-15 |

Khi triển khai, ghi đường dẫn test, CI run hoặc biên bản demo vào cột ghi chú/bằng chứng được bổ sung cạnh yêu cầu. Chỉ đổi trạng thái sang Đạt sau khi các ca liên quan đạt trên môi trường đã ghi nhận.

## 9. Thứ tự thực hiện và điều kiện hoàn thành

| Mốc | Nhóm yêu cầu chính | Điều kiện chốt mốc |
|---|---|---|
| 1. Chốt contract/wireframe | Rà soát FR/NFR/BR; schema và fixture | Nhóm xác nhận phạm vi, tiêu chí; design/contract không mâu thuẫn; có bảng ánh xạ stream/report/decision và khảo sát timezone lõi |
| 2. Nền tảng | FR-01–FR-06, NFR-01–NFR-03; kiểm chứng contract engine | Tài khoản, session, catalog và validation hoạt động; thử nghiệm adapter bằng stub đọc một báo cáo/decision đúng schema, không gọi provider; chưa nghiệm thu FR-21 |
| 3. Tạo/theo dõi | FR-07–FR-12, FR-20, NFR-04, NFR-07 | Luồng queued → running, progress và chống trùng đạt |
| 4. Kết quả/gián đoạn | FR-13–FR-19, kiểm thử mock của NFR-05–NFR-12 | TC-01–TC-12 đạt và có demo local bằng mock; đầu ra trung gian, chưa nghiệm thu MVP1 |
| 5. Engine live và nghiệm thu MVP1 | FR-21, NFR-10, NFR-12 và hồi quy các yêu cầu liên quan | TC-13 đạt với dữ liệu thật; FR-01–FR-21, NFR-01–NFR-12 và TC-01–TC-13 đạt; ghi bằng chứng demo live và hồi quy mock/CLI |
| Sau MVP1: bảng điện | FR-22–FR-26, NFR-13, TC-14–TC-16 | Lập lịch riêng sau MVP1; không chặn các mốc 1–5 của luồng phân tích |

Các NFR áp dụng xuyên suốt được kiểm tra từ lúc xây thành phần tương ứng; phần tích hợp live hoàn tất tại mốc 5. MVP1 chỉ được nghiệm thu sau mốc 5. Lịch, nhân lực và đầu ra chi tiết nằm tại [kế hoạch triển khai](planning/implementation-plan.md).

## 10. Điểm còn mở và phụ thuộc

| Mã | Điểm cần chốt | Thời điểm cần quyết định |
|---|---|---|
| OPEN-01 | Gán tên thành viên/reviewer và ngày giao vào bảng đầu việc có vai trò, dependency, ước lượng tại implementation-plan; chốt thời hạn và quy mô người dùng demo | Trước khi lập sprint |
| OPEN-02 | Máy demo, tài nguyên tối thiểu và phương án public URL nếu cần | Trước nghiệm thu triển khai; không chặn phát triển local |
| OPEN-03 | Ngưỡng response time, tải đồng thời và môi trường đo | Trước nghiệm thu hiệu năng; hiện chưa có SLA |
| OPEN-04 | Provider/instrument live cho luồng phân tích; quyền truy cập và ngân sách LLM/data | Chọn ở mốc 1, có quyền truy cập trước mốc 5; là phụ thuộc bắt buộc để nghiệm thu MVP1. Nguồn bảng giá VN chốt riêng khi triển khai sau MVP1 |
| OPEN-05 | Retention báo cáo/artifact, backup/restore và xóa tài khoản | Trước dùng dữ liệu ngoài nhóm hoặc vận hành lâu dài |
| OPEN-06 | Ngưỡng rate limit, kích thước báo cáo và deadline sau đo thực tế | Khi chạy integration/load test |

Mock fixture, database test và tài khoản demo là đầu vào của FE/BE. Provider key và nguồn live là phụ thuộc bắt buộc của MVP1: thiếu chúng vẫn có thể phát triển và kiểm thử bằng mock ở mốc 1–4, nhưng chưa thể hoàn thành TC-13 hoặc nghiệm thu MVP1. Chưa có nguồn bảng giá VN không chặn MVP1 nếu instrument được chọn đã có dữ liệu thật cho phân tích.

## 11. Quy trình cập nhật

1. Ghi yêu cầu hoặc thay đổi tại file này trước: ID, lý do, ưu tiên, giai đoạn và tiêu chí nghiệm thu.
2. Nếu thay phạm vi, chỉ rõ yêu cầu thêm/bỏ và ảnh hưởng tới FE, BE, dữ liệu, engine hoặc vận hành.
3. Cập nhật các liên kết thiết kế/API, mock fixture và test liên quan trong cùng thay đổi.
4. Khi bắt đầu thực hiện, đổi trạng thái và ghi người phụ trách hoặc issue/PR; khi Đạt, thêm bằng chứng.
5. Giữ lịch sử trong Git; cập nhật phiên bản/ngày tài liệu khi baseline thay đổi. Không tự đánh dấu yêu cầu đã được nhóm phê duyệt chỉ vì đã viết tài liệu.

Nếu phát hiện mâu thuẫn giữa đặc tả này và thiết kế/API, ghi nhận và sửa đồng bộ trước khi triển khai phần phụ thuộc; không để FE và BE tự chọn hai hành vi khác nhau.

## 12. Tài liệu liên quan

- [Kiến trúc tổng thể](system-architecture.md): thành phần và luồng dữ liệu.
- [Thiết kế frontend](frontend/design.md), [planning giao diện](frontend/ui-planning.md): màn hình, tương tác và prototype.
- [Backlog bảng điện sau MVP1](planning/post-mvp-market-workspace.md): hướng mở rộng, chưa thuộc đường đi bắt buộc hiện tại.
- [Thiết kế backend](backend/design.md): service, worker, engine adapter và cơ chế phục hồi.
- [Hợp đồng API](backend/api-contract.md): HTTP schema và mã lỗi.
- [Mô hình dữ liệu](backend/data-model.md): lưu trữ, ràng buộc và transaction.
- [Kế hoạch triển khai](planning/implementation-plan.md): thứ tự và đầu ra các mốc.
