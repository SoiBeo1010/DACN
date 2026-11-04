# Thiết kế frontend

Yêu cầu chức năng và phi chức năng được quản lý tại [requirements.md](../requirements.md); các mã FR/NFR/BR dùng để đối chiếu khi triển khai và nghiệm thu.

Xem [planning giao diện](ui-planning.md) để tham khảo ảnh các màn hình và [prototype tương tác](prototype.html). Các bản phác thảo giúp chốt bố cục trước khi triển khai React.

**MVP1:** đăng nhập → `/analyses` → tạo phiên → theo dõi → báo cáo/lịch sử. Bảng điện, watchlist và trang chi tiết giá được giữ tại [backlog sau MVP1](../planning/post-mvp-market-workspace.md), chưa thêm vào route hoặc module bắt buộc của FE.

## 1. Vai trò và cấu trúc

Frontend giúp người dùng quản lý một phiên phân tích từ lúc nhập yêu cầu đến lúc xem lại kết quả. Các thuật ngữ trên giao diện ưu tiên nghiệp vụ: đối tượng phân tích, ngày dữ liệu, tiến độ, báo cáo và kết luận.

Stack đề xuất: React, TypeScript, Vite, React Router, TanStack Query; dùng CSS variables và một bộ component thống nhất. Thư viện biểu đồ chỉ bổ sung khi API dữ liệu biểu đồ được chốt.

```text
frontend/
  src/
    app/                 # Router, providers, app shell
    pages/               # Login, analysis list, create, detail
    features/
      auth/              # Session, login, logout
      instruments/       # Search và chọn đối tượng
      analyses/          # Form, mutations, polling, bộ lọc
      reports/           # Đọc báo cáo và hiển thị kết luận
    shared/
      api/               # HTTP client, lỗi chuẩn, kiểu sinh từ OpenAPI
      ui/                # Button, field, badge, dialog, empty state
      lib/               # Date/time, formatter
      config/            # Public runtime config
    mocks/               # Mock Service Worker và fixture theo API contract
```

Quy tắc phụ thuộc: `app/pages → features → shared`. Feature không import ngược từ page. Dữ liệu API không được sao chép thành nhiều global store.

## 2. Các route

| Route | Màn hình | Quyền |
|---|---|---|
| `/login` | Đăng nhập | Công khai |
| `/analyses` | Lịch sử và trạng thái các phiên | Có session |
| `/analyses/new` | Tạo phiên | Có session |
| `/analyses/:id` | Tiến độ và kết quả của một phiên | Chủ phiên |
| `/` | Chuyển tới `/analyses` hoặc `/login` | Theo session |

Đây là SPA: reverse proxy trả app shell khi người dùng mở trực tiếp `/analyses/:id`. Route API giữ nguyên mã lỗi JSON, không bị SPA fallback ghi đè.

## 3. Màn hình đăng nhập

- Hai trường email và mật khẩu; nút hiện/ẩn mật khẩu và nút đăng nhập.
- Khi gửi: khóa submit lặp, giữ email và không lưu mật khẩu.
- Khi sai: hiển thị thông báo chung, không tiết lộ email có tồn tại.
- Khi thành công: cập nhật session cache và về trang được bảo vệ đã yêu cầu, nếu đó là đường dẫn nội bộ hợp lệ.
- Nếu không có trang đích trước đó, mở `/analyses`.
- Session hết hạn: dừng polling, xóa dữ liệu cache của tài khoản và chuyển về đăng nhập.

Ứng dụng gọi `GET /auth/session` lúc khởi động. Cache của người dùng trước phải được xóa khi đăng xuất hoặc đổi tài khoản.

## 4. Màn hình danh sách phiên

```text
+---------------------------------------------------------------+
| DACN                  Lịch sử              Tài khoản / Đăng xuất|
| Phiên phân tích                              [Tạo phân tích]  |
| [Tìm mã...] [Trạng thái v] [Từ ngày] [Đến ngày] [Áp dụng]       |
|---------------------------------------------------------------|
| Đối tượng | Ngày dữ liệu | Trạng thái | Tạo lúc | Kết luận      |
| DEMO      | 03/11/2026   | Đang chạy | ...     | Đang phân tích |
| DEMO      | 02/11/2026   | Hoàn thành| ...     | Cần xem xét    |
|---------------------------------------------------------------|
|                        [Xem thêm]                             |
+---------------------------------------------------------------+
```

- Bộ lọc lưu trong URL để refresh và chia sẻ đường dẫn vẫn giữ điều kiện.
- Ô tìm mã/tên gửi q tới GET /analyses; backend tìm trên snapshot của phiên. Các bộ lọc kết hợp bằng AND. Đổi tìm kiếm hoặc bộ lọc thì bỏ cursor cũ; ngày “đến” bao gồm cả ngày đã chọn theo timezone hiển thị.
- Danh sách phân trang bằng cursor; mặc định mới nhất trước.
- Không có dữ liệu: giải thích ngắn và hiển thị nút tạo phiên.
- Không có kết quả lọc: giữ bộ lọc, cho phép xóa lọc.
- Lỗi tải: giữ dữ liệu đã có và cung cấp nút tải lại.
- Khi có phiên hoạt động và tab đang hiển thị: refetch mỗi 5 giây.

## 5. Màn hình tạo phiên

| Trường | Nguồn dữ liệu | Kiểm tra |
|---|---|---|
| Đối tượng phân tích | `/instruments?q=...` | Bắt buộc chọn một bản ghi được hỗ trợ |
| Ngày dữ liệu | Người dùng; giới hạn từ instrument/profile | Định dạng ngày, không vượt ngày hiện tại theo timezone nghiệp vụ |
| Cấu hình phân tích | `/analysis-profiles` | Chọn profile còn khả dụng |
| Ngôn ngữ báo cáo | Danh sách của profile | Chỉ gửi giá trị được hỗ trợ |

Hiển thị mã, tên và sàn cạnh nhau để tránh chọn nhầm các mã trùng tên. Search debounce 300 ms và hủy request search cũ khi truy vấn đổi.

Profile được đặt tên theo nhu cầu, ví dụ “Tiêu chuẩn”; backend quyết định cấu hình thực thi. Giao diện người dùng không có ô nhập API key, base URL, đường dẫn file hoặc prompt hệ thống.

Trước khi submit, trình duyệt tạo một `Idempotency-Key` và giữ nguyên khóa cho các lần gửi lại của cùng yêu cầu. Nếu mạng đứt sau khi gửi, giữ form và cho phép kiểm tra/gửi lại bằng khóa cũ. Khi người dùng sửa input để tạo một ý định mới, sinh khóa mới.

Sau `202`, chuyển ngay tới `/analyses/{id}`. Khi nhận lỗi validation, đặt lỗi sát trường tương ứng và focus trường lỗi đầu tiên. Khi server báo đạt giới hạn phiên hoạt động, giữ form và liên kết về lịch sử.

## 6. Màn hình chi tiết phiên

```text
+----------------------------------------------------------------+
| < Lịch sử        DEMO · ngày dữ liệu 03/11/2026    [Yêu cầu hủy] |
| [DỮ LIỆU GIẢ LẬP]  Đang chạy · Bước: Phân tích tin tức           |
| Bắt đầu ...       Thời gian đã chạy ...                          |
|----------------------------------------------------------------|
| [Tổng quan] [Báo cáo] [Tiến trình]                               |
|                                                                |
| Kết luận / trạng thái chờ                                      |
| Các bước: [x] Chuẩn bị [x] Phân tích [>] Tổng hợp [ ] Hoàn tất    |
| Báo cáo đã sẵn sàng: [Kỹ thuật] [Tin tức]                        |
+----------------------------------------------------------------+
```

### Tổng quan

Hiển thị snapshot của input, trạng thái, bước hiện tại, thời gian và kết luận khi có. Nhãn `mock/live` luôn nhìn thấy. Khi kết luận cần xem xét, dùng thông báo riêng cùng nguyên nhân; không gán nó thành `Hold`.

| Giá trị từ API | Nhãn gợi ý |
|---|---|
| `Buy` | Mua |
| `Overweight` | Tăng tỷ trọng |
| `Hold` | Giữ |
| `Underweight` | Giảm tỷ trọng |
| `Sell` | Bán |
| `quality = needs_review`, `rating = null` | Cần xem xét |

Nhãn trạng thái thực thi và nhãn kết luận là hai component riêng.

### Báo cáo

Danh sách các phần đã có; chỉ fetch nội dung đầy đủ khi mở phần. Render Markdown bằng cấu hình tắt raw HTML, loại bỏ URL nguy hiểm và mở liên kết ngoài với thuộc tính an toàn. Nội dung từ mô hình được xem là dữ liệu không tin cậy.

Metadata báo cáo có revision. Khi snapshot mới cho thấy revision tăng, invalidate query nội dung đang cache theo report ID; nếu đang đọc phần đó thì tải lại. Không coi report ID ổn định là nội dung bất biến.

Nếu phiên thất bại hoặc bị hủy, các báo cáo đã hoàn thành vẫn đọc được. Hiển thị rõ kết quả chưa hoàn tất. Không hiển thị ô giá mục tiêu hoặc tỷ lệ tin cậy nếu API chưa có dữ liệu tương ứng.

### Tiến trình

Hiển thị các bước và sự kiện nghiệp vụ: bắt đầu, hoàn thành bước, có báo cáo, yêu cầu hủy, hoàn tất hoặc thất bại. Không hiển thị prompt, khóa truy cập, raw stack trace hay toàn bộ tool payload.

Backend cung cấp tên bước, thứ tự và trạng thái; frontend không tự suy luận thứ tự agent từ tên file hoặc tên node của LangGraph. Với bước còn lặp, dùng tiến độ theo giai đoạn và thời gian đã chạy, tránh hiển thị phần trăm chính xác giả tạo.

## 7. Quản lý trạng thái và đồng bộ

| Loại dữ liệu | Nơi quản lý |
|---|---|
| Session, instrument, profile, danh sách phiên, snapshot, báo cáo | TanStack Query |
| Bộ lọc danh sách và tab đang chọn | URL search params |
| Form chưa gửi, dialog, phần đang mở | React local state |
| HTTP schema | TypeScript sinh từ OpenAPI của backend |

Query key phải bao gồm resource ID và tham số lọc, ví dụ `['analysis', id]`, `['analyses', filters]`, `['report', runId, reportId]`. Xóa query cache lúc session kết thúc.

### Quy tắc polling

1. Fetch snapshot khi vào trang chi tiết.
2. Poll mỗi 2 giây nếu `status` thuộc `queued`, `running`, `cancel_requested` và tab đang hiển thị.
3. Dừng polling khi terminal; refetch ngay khi tab được mở lại hoặc mạng phục hồi.
4. Khi version tăng, cập nhật snapshot và đối chiếu report revision để làm mới nội dung đã cache.
5. Giữ last_read_event_seq riêng với event_cursor của snapshot. Mở Tiến trình lần đầu đọc after=0; sau đó dùng next_cursor cuối đã tải, dedupe theo (run_id, seq) và đọc tiếp tới khi has_more=false. Khi phiên vừa terminal vẫn đọc hết các sự kiện còn thiếu trước khi dừng; không nhảy thẳng tới event_cursor mới của server.
6. `404` dừng tải và hiển thị trang không tìm thấy; `401` kết thúc session phía UI.

GET có thể retry tối đa hai lần với backoff khi lỗi mạng/5xx. Mutation tạo phiên không được retry tự động bằng một khóa mới. Sau hủy hoặc thử lại, invalidate snapshot và lịch sử liên quan.

HTTP client dùng `credentials: include`, gửi `X-CSRF-Token` cho mutation đã xác thực, chuẩn hóa lỗi và giữ `request_id` để hỗ trợ điều tra. Mỗi query có thể hủy request khi không còn cần.

## 8. Responsive và khả năng truy cập

- Desktop: sidebar điều hướng, header theo ngữ cảnh, vùng nội dung rộng; timeline và báo cáo đặt cạnh nhau khi đủ chỗ.
- Mobile: một cột; bảng lịch sử chuyển thành card, hành động hủy nằm trong vùng dễ nhìn.
- Form có label, lỗi gắn với trường; dialog quản lý focus và hoạt động bằng bàn phím.
- Trạng thái có chữ và biểu tượng bên cạnh màu; thông báo tiến độ dùng live region ở mức vừa phải.
- Khi dữ liệu đang tải, dùng skeleton; khi polling lỗi, giữ snapshot trước cùng nhãn “Đang mất kết nối”.

## 9. Tiêu chí nghiệm thu frontend

- Có thể hoàn thành luồng chính với mock API mà không cần LLM hay tài khoản vendor.
- Reload và mở trực tiếp trang chi tiết không tạo thêm phiên.
- Nhấn submit nhiều lần hoặc gửi lại sau lỗi mạng chỉ tạo một phiên cho một ý định.
- Hoàn tất, thất bại, cần xem xét và bị hủy đều có giao diện riêng.
- Đăng xuất xóa dữ liệu tài khoản trước khỏi cache.
- Polling dừng đúng lúc; lỗi mạng không làm mất báo cáo đã tải.
- Timeline không bỏ sót sự kiện khi mở muộn; phần báo cáo đang đọc được cập nhật khi revision tăng.
- Nhãn giả lập xuất hiện trên danh sách, chi tiết và báo cáo của phiên mock.
