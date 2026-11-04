# Đặc tả và quản lý yêu cầu

## 1. Thông tin tài liệu

| Thuộc tính | Giá trị |
|---|---|
| Dự án | DACN — Ứng dụng web quản lý phiên phân tích |
| Phiên bản đặc tả | 0.1 |
| Ngày cập nhật | 2026-11-04 |
| Trạng thái tài liệu | Bản nháp tổng hợp để nhóm rà soát |
| Phạm vi hiện tại | Frontend và backend; tích hợp engine qua adapter sau khi hoàn thành luồng mock |
| Nguồn tổng hợp | Các tài liệu thiết kế FE, BE, API, dữ liệu và kế hoạch trong `docs/` |

Đây là nơi quản lý tập trung những gì sản phẩm cần đáp ứng và cách xác nhận yêu cầu đã đạt. Các tài liệu thiết kế mô tả cách thực hiện. Các lựa chọn công nghệ, bố cục mẫu và tham số vận hành không tự động trở thành yêu cầu nghiệp vụ.

Hiện mới có tài liệu và prototype giao diện; ứng dụng FE/BE theo đặc tả chưa được triển khai. Các yêu cầu bên dưới đều ở trạng thái **Chưa triển khai**. Ảnh chụp và prototype không được dùng làm bằng chứng hoàn thành chức năng có backend.

## 2. Mục tiêu, tác nhân và phạm vi

### 2.1. Mục tiêu

Người dùng có thể đăng nhập, tạo yêu cầu phân tích cho một đối tượng/ngày được hỗ trợ, theo dõi quá trình xử lý, đọc kết quả và mở lại lịch sử. Một phiên tồn tại độc lập với việc trình duyệt còn mở hay không.

Giai đoạn FE/BE phải kiểm thử được toàn bộ luồng bằng engine giả lập. Giai đoạn tích hợp sau đó kết nối TradingAgents qua hợp đồng engine ổn định, giữ nguyên các hành vi đã nghiệm thu của ứng dụng.

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
| FE/BE với mock | Tài khoản, catalog mock, tạo phiên, tiến độ, báo cáo, kết luận, lịch sử, hủy/thử lại, xử lý gián đoạn | Các yêu cầu áp dụng FE/BE đạt bằng dữ liệu giả lập có nhãn |
| Tích hợp live | Adapter TradingAgents, một instrument được nguồn thực hỗ trợ, map kết quả và cô lập phiên | Đạt thêm FR-21 và kiểm tra hồi quy luồng FE/BE |

Ngoài phạm vi hiện tại: tự đăng ký, khôi phục mật khẩu, giao diện quản trị, đặt lệnh thật, quản lý danh mục giao dịch, backtest diện rộng, chọn tùy ý provider/model/prompt, thông báo qua bot, chia sẻ công khai báo cáo, xóa lịch sử qua UI và resume thủ công một phiên terminal.

Chưa cam kết thị trường/vendor cụ thể, độ chính xác đầu tư, lợi nhuận, lưu lượng lớn hoặc thời gian hoạt động 24/7. Những mục này cần yêu cầu và dữ liệu đánh giá riêng nếu được bổ sung.

## 3. Quy ước quản lý

- `FR`: yêu cầu chức năng; `NFR`: yêu cầu phi chức năng; `BR`: quy tắc nghiệp vụ; `TC`: kịch bản nghiệm thu.
- `P0`: bắt buộc trong giai đoạn được ghi; `P1`: có thể thực hiện sau các yêu cầu bắt buộc của giai đoạn đó.
- Cột phụ trách chỉ nhóm công việc FE, BE hoặc vận hành; chưa gán tên thành viên.
- Trạng thái triển khai: **Chưa triển khai → Đang triển khai → Chờ kiểm thử → Đạt**. **Tạm hoãn** cần ghi lý do và mốc xem lại.
- Trạng thái **Đạt** yêu cầu có bằng chứng kiểm thử hoặc biên bản nghiệm thu, không chỉ có code hoặc mockup.
- Mỗi yêu cầu giữ ID ổn định. Khi bỏ yêu cầu, ghi trạng thái và lý do thay vì tái sử dụng ID cho nội dung khác.

## 4. Yêu cầu chức năng

### 4.1. Tài khoản và dữ liệu đầu vào

| ID | Yêu cầu | Ưu tiên / giai đoạn | Phụ trách | Tiêu chí nghiệm thu | Trạng thái |
|---|---|---|---|---|---|
| FR-01 | Cho phép đăng nhập bằng tài khoản đã cấp và khôi phục session hợp lệ khi tải lại trang. | P0 · FE/BE | FE + BE | Thông tin đúng mở lịch sử; sai hiển thị lỗi chung; chưa đăng nhập không đọc được API dữ liệu; tải lại không yêu cầu đăng nhập khi session còn hiệu lực. | Chưa triển khai |
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
| FR-13 | Cho phép đọc các báo cáo đã lưu, kể cả khi phiên chưa hoàn tất. | P0 · FE/BE | FE + BE | Mở từng phần từ danh sách báo cáo; nội dung Markdown đúng phiên; báo cáo đã hoàn thành vẫn đọc được khi failed/cancelled; không hiển thị phần chưa có. | Chưa triển khai |
| FR-14 | Hiển thị kết luận và chất lượng kết luận độc lập với trạng thái thực thi. | P0 · FE/BE | FE + BE | Hiển thị một trong năm rating khi hợp lệ; `needs_review` có cảnh báo và rating null; không đổi thiếu dữ liệu thành Hold; trường không được cung cấp không được tạo thêm; áp dụng BR-05, BR-06. | Chưa triển khai |
| FR-15 | Cung cấp lịch sử cá nhân có tìm kiếm, lọc và phân trang. | P0 · FE/BE | FE + BE | Lọc theo instrument, trạng thái, khoảng ngày tạo; thứ tự mới nhất trước; phân trang cursor; URL giữ điều kiện; có trạng thái rỗng và không tìm thấy phù hợp. | Chưa triển khai |
| FR-16 | Cho phép mở trực tiếp một phiên đã có. | P0 · FE/BE | FE + BE | Sau đăng nhập, mở URL/refresh trang chi tiết đọc đúng snapshot của owner; kết quả đã lưu đọc lại sau restart dịch vụ; URL không tạo run mới. | Chưa triển khai |

### 4.4. Hủy, thử lại và xử lý gián đoạn

| ID | Yêu cầu | Ưu tiên / giai đoạn | Phụ trách | Tiêu chí nghiệm thu | Trạng thái |
|---|---|---|---|---|---|
| FR-17 | Cho phép hủy phiên hợp lệ và theo dõi quá trình dừng. | P0 · FE/BE | FE + BE | Hủy queued chuyển cancelled; hủy running chuyển cancel_requested rồi terminal khi được xác nhận; thao tác lặp không sinh sự kiện trùng; giữ báo cáo đã có; áp dụng BR-07. | Chưa triển khai |
| FR-18 | Cho phép thử lại phiên thất bại hoặc đã hủy bằng một phiên mới. | P0 · FE/BE | FE + BE | Run mới có ID khác và liên kết nguồn; giữ lịch sử cũ; snapshot nguồn được dùng nếu còn khả dụng; source không hợp lệ hoặc cấu hình không còn chạy được nhận `409`; áp dụng BR-08. | Chưa triển khai |
| FR-19 | Xác định và công bố lỗi engine, quá hạn hoặc mất worker. | P0 · FE/BE | BE + FE | Run chuyển failed cùng mã/thông báo công khai; process quá hạn bị dừng; worker mất claim không ghi kết quả muộn; có đường thử lại chủ động; áp dụng BR-11. | Chưa triển khai |

### 4.5. Engine giả lập và tích hợp

| ID | Yêu cầu | Ưu tiên / giai đoạn | Phụ trách | Tiêu chí nghiệm thu | Trạng thái |
|---|---|---|---|---|---|
| FR-20 | Cung cấp mock engine để chạy xuyên suốt ứng dụng và kiểm thử mà không cần provider. | P0 · FE/BE | BE + FE | Chạy được thành công, needs_review, lỗi, chờ lâu, hủy và mất worker bằng fixture/stub; không gọi LLM/vendor thật; chế độ mock được gắn nhãn trên các màn hình; áp dụng BR-09. | Chưa triển khai |
| FR-21 | Tích hợp lõi TradingAgents qua adapter với hợp đồng tiến độ/báo cáo/kết quả đã chốt. | P0 · Tích hợp live | BE + FE | Ít nhất một instrument được nguồn thật hỗ trợ chạy tới kết quả; hai phiên cùng mã/ngày không dùng lẫn state, file hoặc checkpoint; output REVIEW map đúng; CI mặc định vẫn dùng stub; áp dụng BR-10. | Chưa triển khai |

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
| NFR-07 | API tiếp tục phục vụ khi engine chạy lâu; FE chỉ đồng bộ khi cần. | P0 · FE/BE | Mock engine được giữ chờ; đồng thời login/GET/history/create không phải chờ engine kết thúc; tab ẩn và phiên terminal không tiếp tục polling định kỳ; số thời gian chạy thật được đo ở mốc load test. | Chưa triển khai |
| NFR-08 | Giao diện dùng được trên desktop và mobile. | P0 · FE/BE | Kiểm tra luồng chính ở bề rộng 390, 768 và 1440 px; không tràn ngang toàn trang; nội dung bảng dài được xử lý trong vùng riêng; nút/form không bị cắt. | Chưa triển khai |
| NFR-09 | Hỗ trợ sử dụng bằng bàn phím và trạng thái dễ hiểu. | P0 · FE/BE | Form có label; lỗi liên kết trường; focus nhìn thấy; dialog trả focus khi đóng; trạng thái có chữ ngoài màu; luồng login/create/detail dùng được bằng bàn phím. | Chưa triển khai |
| NFR-10 | Dữ liệu ngày giờ và chế độ dữ liệu được biểu diễn nhất quán. | P0 · FE/BE | Timestamp API là UTC ISO 8601; ngày nghiệp vụ theo timezone instrument; UI hiển thị đúng ngữ cảnh; không trộn mock/live; mock có nhãn cả ở lịch sử, chi tiết và báo cáo. | Chưa triển khai |
| NFR-11 | Hợp đồng FE/BE và migration có thể kiểm chứng lặp lại. | P0 · FE/BE | OpenAPI sinh từ schema; FE types/fixture được kiểm tra tương thích; migration chạy từ DB rỗng; có E2E mock và kiểm tra cài đặt lõi; CI mặc định không cần khóa provider thật. | Chưa triển khai |
| NFR-12 | Có thể chạy demo mà chưa cần thuê máy chủ hoặc mua tên miền. | P0 · FE/BE | Có hướng dẫn chạy local FE/API/worker/PostgreSQL với mock engine; demo trọn luồng bằng máy nhóm được chọn; deployment thật và tài nguyên tối thiểu được xác nhận riêng, không giả định gói hosting miễn phí chạy worker liên tục. | Chưa triển khai |

NFR-12 ghi nhận ràng buộc nguồn lực hiện tại. Tên nhà cung cấp hosting, giá dịch vụ và các quyền lợi miễn phí không phải cam kết trong đặc tả này.

## 6. Quy tắc nghiệp vụ

| ID | Quy tắc | Liên quan |
|---|---|---|
| BR-01 | Một phiên thuộc đúng một user, có một instrument ID, ngày dữ liệu, profile/version và ngôn ngữ. Chủ sở hữu được xác định từ session. | FR-07, NFR-01 |
| BR-02 | Input và cấu hình đã resolve được snapshot khi tạo, bất biến trong phiên; secret không được snapshot. Thay catalog/profile về sau không sửa kết quả lịch sử. | FR-05, FR-07, FR-16 |
| BR-03 | Idempotency key có phạm vi user, hiệu lực mặc định 24 giờ. Cùng key và request chuẩn hóa trả resource cũ; request khác bị từ chối. Ý định mới có key mới; retry endpoint cũng có chống trùng. | FR-08, FR-18 |
| BR-04 | Lifecycle gồm queued, running, cancel_requested, succeeded, failed, cancelled. Ba trạng thái cuối là terminal, không chuyển ngược; mở lại trang không khởi chạy phiên mới. | FR-09, FR-10, FR-16 |
| BR-05 | Trạng thái thực thi và chất lượng kết luận là hai thuộc tính riêng. Succeeded cần có decision; valid cần một rating hợp lệ; needs_review dùng rating null. Không có kết quả cuối vì engine hỏng là failed. | FR-14, FR-19 |
| BR-06 | Năm rating là Buy, Overweight, Hold, Underweight, Sell. REVIEW của lõi được chuyển thành needs_review, không phải Hold. FE chỉ trình bày các trường backend thực sự cung cấp. | FR-14, FR-21 |
| BR-07 | Hủy queued có hiệu lực ngay. Hủy running phải chờ xác nhận dừng; request provider đang bay có thể chưa dừng tức thời. Nếu cancel_requested commit trước, không công bố quyết định cuối; nếu succeeded commit trước, hủy nhận 409. | FR-17 |
| BR-08 | Chỉ failed/cancelled được thử lại; tạo run mới liên kết run cũ và dùng snapshot cũ nếu còn hỗ trợ. Không sửa trạng thái hoặc báo cáo lịch sử. Cấu hình cũ không khả dụng trả lỗi để tạo yêu cầu mới. | FR-18 |
| BR-09 | Mock và live là hai chế độ tách biệt. Không ghép instrument mock với profile live hoặc ngược lại. Live chỉ dữ liệu nguồn thật, không bảo đảm dữ liệu tức thời. Kịch bản lỗi giả lập chỉ bật ở môi trường dev/test. | FR-05, FR-20, NFR-10 |
| BR-10 | State, memory, artifact và checkpoint được cô lập theo run. MVP không chia sẻ bộ nhớ liên phiên. Các báo cáo hoàn thành vẫn được lưu và đọc khi run failed/cancelled. | FR-13, FR-21 |
| BR-11 | Worker chỉ được ghi khi còn claim và lease hợp lệ. Lease hết hạn dẫn tới failed/WORKER_LOST qua recovery; quá deadline là failed/RUN_TIMEOUT. Không tự chạy lại cả phiên; người dùng chủ động thử lại. | FR-09, FR-19, NFR-04 |
| BR-12 | Snapshot tiến độ lấy từ server. Event được đánh số tăng theo run; FE đọc tiếp bằng cursor và dedupe. Nội dung chưa có không được tạo thay bằng số liệu hoặc phần trăm giả định. | FR-10, FR-11, FR-14 |

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

Mã màn hình S01–S06 tham chiếu [planning giao diện](planning/frontend-ui.md): đăng nhập, lịch sử, tạo phiên, tiến độ, kết quả và báo cáo. S04/S05/S06 là các cách hiển thị của cùng resource phiên phân tích.

| Yêu cầu | Màn hình / thành phần | API hoặc điểm tích hợp | Kịch bản nghiệm thu |
|---|---|---|---|
| FR-01, FR-02, FR-03 | S01, AppShell; lệnh quản trị | `/auth/login`, `/auth/session`, `/auth/logout`; công cụ cấp user | TC-01, TC-02 |
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

Các đường API rút gọn trong bảng dùng prefix `/api/v1`. Chi tiết request, response, mã lỗi và phân trang nằm tại [api-contract.md](api-contract.md).

## 8. Kịch bản nghiệm thu

Đây là danh mục kiểm thử dự kiến, chưa phải kết quả test đã đạt. Test về transaction/claim dùng PostgreSQL thật; ca nghiệm thu ứng dụng dùng engine mock trừ TC-13.

| ID | Kịch bản và kết quả mong đợi | Yêu cầu chính |
|---|---|---|
| TC-01 | Đăng nhập đúng/sai, refresh, logout, hết hạn và vô hiệu hóa tài khoản; quyền truy cập/cache phản ánh session mới nhất. | FR-01, FR-02, FR-03, NFR-02 |
| TC-02 | A tạo phiên, B thử GET/report/event/cancel/retry bằng ID của A; đều bị từ chối. Sai CSRF, sai origin và vượt rate limit cũng bị chặn. | NFR-01, NFR-02 |
| TC-03 | Tìm instrument trùng mã khác sàn; chọn profile/ngày/ngôn ngữ hợp lệ và không hợp lệ; chỉ tổ hợp hỗ trợ được tạo phiên. | FR-04, FR-05, FR-06 |
| TC-04 | Từ form, tạo phiên mock, xem tiến độ, báo cáo và kết luận; đóng rồi mở URL vẫn đọc đúng phiên; không gọi provider thật. | FR-07, FR-10, FR-13, FR-20, NFR-12 |
| TC-05 | Gửi đồng thời cùng key, khác key ở biên hạn mức, key khác payload và claim bằng hai worker; không tạo trùng hoặc vượt quy tắc quota/claim. | FR-08, FR-09, NFR-04 |
| TC-06 | Nhận event theo nhiều trang cursor, lặp response, đổi tab, terminal và mất mạng; FE dedupe, giữ snapshot, phục hồi và dừng poll đúng lúc. | FR-10, FR-11, FR-12, NFR-07 |
| TC-07 | Đọc báo cáo từng phần khi running/failed/cancelled, chuyển phần giữ ngữ cảnh; nội dung có HTML/script/URL nguy hiểm không được thực thi. | FR-13, NFR-03 |
| TC-08 | Kiểm tra năm rating và REVIEW; hoàn tất xử lý với needs_review không thành Hold; trường thiếu không bị bịa; decision/terminal nhất quán. | FR-14, NFR-04, NFR-10 |
| TC-09 | Lọc lịch sử, đọc tiếp cursor, mở URL trực tiếp và restart dịch vụ giữ DB; queued/history/report đã commit vẫn tồn tại. | FR-15, FR-16, NFR-05 |
| TC-10 | Giữ engine chạy lâu, đọc API khác, dừng worker, chờ hết lease rồi recovery; thử ghi từ claim cũ; deadline dừng process; lỗi công khai có mã tra cứu. | FR-09, FR-19, NFR-04, NFR-06, NFR-07 |
| TC-11 | Hủy queued/running/lặp hủy, hủy tranh chấp hoàn tất, thử lại failed/cancelled, retry cấu hình cũ không còn hỗ trợ; giữ lịch sử và đúng mã lỗi. | FR-17, FR-18, NFR-04 |
| TC-12 | Kiểm tra luồng ở 390/768/1440 px và bàn phím; mock badge, timezone và trạng thái; build/type/contract/migration/E2E trong môi trường sạch. | FR-20, NFR-08, NFR-09, NFR-10, NFR-11, NFR-12 |
| TC-13 | Smoke test chủ động một instrument live; hai run cùng mã/ngày cô lập; stub lỗi/REVIEW map đúng; secret không xuất hiện ở UI/API/log công khai. | FR-21, NFR-03, NFR-10 |

Khi triển khai, ghi đường dẫn test, CI run hoặc biên bản demo vào cột ghi chú/bằng chứng được bổ sung cạnh yêu cầu. Chỉ đổi trạng thái sang Đạt sau khi các ca liên quan đạt trên môi trường đã ghi nhận.

## 9. Thứ tự thực hiện và điều kiện hoàn thành

| Mốc | Nhóm yêu cầu chính | Điều kiện chốt mốc |
|---|---|---|
| 1. Chốt contract/wireframe | Rà soát FR/NFR/BR; schema và fixture | Nhóm xác nhận phạm vi, tiêu chí; design/contract không mâu thuẫn |
| 2. Nền tảng | FR-01–FR-06, NFR-01–NFR-03 | Tài khoản, session, catalog và validation hoạt động |
| 3. Tạo/theo dõi | FR-07–FR-12, FR-20, NFR-04, NFR-07 | Luồng queued → running, progress và chống trùng đạt |
| 4. Kết quả/gián đoạn | FR-13–FR-19, NFR-05–NFR-12 | Toàn bộ yêu cầu FE/BE đạt bằng mock; có demo local |
| 5. Engine live | FR-21 và hồi quy các yêu cầu liên quan | Một luồng live đạt, FE/BE mock vẫn vượt kiểm thử |

Các NFR áp dụng xuyên suốt được kiểm tra từ lúc xây thành phần tương ứng, không dồn toàn bộ tới mốc 4. Lịch, nhân lực và đầu ra chi tiết nằm tại [implementation-plan.md](implementation-plan.md).

## 10. Điểm còn mở và phụ thuộc

| Mã | Điểm cần chốt | Thời điểm cần quyết định |
|---|---|---|
| OPEN-01 | Thành viên phụ trách, thời hạn và quy mô người dùng demo | Trước khi lập sprint |
| OPEN-02 | Máy demo, tài nguyên tối thiểu và phương án public URL nếu cần | Trước nghiệm thu triển khai; không chặn phát triển local |
| OPEN-03 | Ngưỡng response time, tải đồng thời và môi trường đo | Trước nghiệm thu hiệu năng; hiện chưa có SLA |
| OPEN-04 | Provider/instrument/thị trường live, quyền truy cập và ngân sách gọi API | Trước mốc 5 |
| OPEN-05 | Retention báo cáo/artifact, backup/restore và xóa tài khoản | Trước dùng dữ liệu ngoài nhóm hoặc vận hành lâu dài |
| OPEN-06 | Ngưỡng rate limit, kích thước báo cáo và deadline sau đo thực tế | Khi chạy integration/load test |

Mock fixture, database test và tài khoản demo là đầu vào của FE/BE. Provider key và nguồn live là phụ thuộc của mốc tích hợp; việc thiếu chúng không chặn nghiệm thu luồng mock.

## 11. Quy trình cập nhật

1. Ghi yêu cầu hoặc thay đổi tại file này trước: ID, lý do, ưu tiên, giai đoạn và tiêu chí nghiệm thu.
2. Nếu thay phạm vi, chỉ rõ yêu cầu thêm/bỏ và ảnh hưởng tới FE, BE, dữ liệu, engine hoặc vận hành.
3. Cập nhật các liên kết thiết kế/API, mock fixture và test liên quan trong cùng thay đổi.
4. Khi bắt đầu thực hiện, đổi trạng thái và ghi người phụ trách hoặc issue/PR; khi Đạt, thêm bằng chứng.
5. Giữ lịch sử trong Git; cập nhật phiên bản/ngày tài liệu khi baseline thay đổi. Không tự đánh dấu yêu cầu đã được nhóm phê duyệt chỉ vì đã viết tài liệu.

Nếu phát hiện mâu thuẫn giữa đặc tả này và thiết kế/API, ghi nhận và sửa đồng bộ trước khi triển khai phần phụ thuộc; không để FE và BE tự chọn hai hành vi khác nhau.

## 12. Tài liệu liên quan

- [Kiến trúc tổng thể](system-architecture.md): thành phần và luồng dữ liệu.
- [Thiết kế frontend](frontend.md), [planning giao diện](planning/frontend-ui.md): màn hình, tương tác và prototype.
- [Thiết kế backend](backend.md): service, worker, engine adapter và cơ chế phục hồi.
- [Hợp đồng API](api-contract.md): HTTP schema và mã lỗi.
- [Mô hình dữ liệu](data-model.md): lưu trữ, ràng buộc và transaction.
- [Kế hoạch triển khai](implementation-plan.md): thứ tự và đầu ra các mốc.
