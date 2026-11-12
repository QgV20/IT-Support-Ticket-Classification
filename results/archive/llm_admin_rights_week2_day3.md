# Tuần 2 - Ngày 3: Phân tích chuyên sâu lỗi Administrative rights

## 1. Mục tiêu

Phân tích nguyên nhân mô hình Qwen2.5:3B không nhận diện đúng nhóm Administrative rights khi sử dụng Prompt V2, V3 và V4.

Nghiên cứu tập trung vào sự khác biệt giữa nhãn thực tế của dataset và nhãn được dự đoán dựa trên nội dung ticket.

## 2. Thiết lập phân tích

- Mô hình: Qwen2.5:3B.
- Công cụ: Ollama.
- Phương pháp: Zero-shot Classification.
- Dữ liệu: 20 ticket Administrative rights thuộc tập validation160.
- Phiên bản phân tích: Prompt V2, V3 và V4.
- Phương pháp: Thống kê dự đoán, đối chiếu nội dung ticket và phân tích định tính.

## 3. Kết quả phân bố dự đoán

| Nhãn dự đoán | V2 | V3 | V4 |
|---|---:|---:|---:|
| Hardware | 3 | 10 | 3 |
| Access | 4 | 4 | 4 |
| Miscellaneous | 6 | 3 | 7 |
| Storage | 3 | 3 | 3 |
| Purchase | 4 | 0 | 2 |
| Lỗi xử lý | 0 | 0 | 1 |
| Administrative rights | 0 | 0 | 0 |

Cả ba phiên bản đều có Recall bằng 0% đối với Administrative rights trên tập validation160.

Prompt V3 phân loại 10/20 ticket Administrative rights thành Hardware, trong khi V4 phân loại 7/20 thành Miscellaneous.

V3 và V4 có 8 dự đoán khác nhau trong nhóm này, nhưng không phiên bản nào dự đoán đúng nhãn gốc.

## 4. Phân tích nội dung ticket

### 4.1. Các yêu cầu liên quan Windows và nâng cấp phần mềm

Các ticket như 2321, 27731, 34365 và 37998 đề cập cài đặt hoặc nâng cấp Windows.

Những thao tác này có thể liên quan đến đặc quyền quản trị, tuy nhiên nội dung được quan sát không luôn nêu rõ yêu cầu cấp quyền.

Do đó, mô hình có thể ưu tiên Hardware hoặc những nhóm hỗ trợ kỹ thuật khác.

### 4.2. Các yêu cầu Outlook và tài khoản

Ticket 24596 đề cập vấn đề mật khẩu Outlook và được cả V3 lẫn V4 dự đoán thành Access.

Xét theo nội dung hiển thị, Access là một cách diễn giải có cơ sở. Tuy nhiên, nhãn gốc của dataset là Administrative rights.

Trường hợp này cho thấy chỉ dựa vào văn bản ticket có thể chưa đủ để tái hiện quy ước gán nhãn.

### 4.3. Các yêu cầu thiết bị và lưu trữ

Ticket 16208 đề cập tình trạng thiếu dung lượng khi nâng cấp Windows. Cả V3 và V4 dự đoán Storage.

Ticket 26038 mô tả ổ đĩa không hiển thị và cũng được dự đoán thành Storage.

Ticket 38239 yêu cầu thiết lập máy in Xerox và được dự đoán thành Hardware.

Những trường hợp này cho thấy mô hình đang phân loại theo chủ đề kỹ thuật thể hiện trực tiếp trong văn bản thay vì nhãn Administrative rights của dataset.

### 4.4. Các yêu cầu thao tác hệ thống

Ticket 12567 liên quan đến việc khởi động lại server hoặc ứng dụng.

Đây là thao tác có thể cần đặc quyền quản trị, nhưng yêu cầu không trực tiếp nêu vấn đề cấp quyền.

Điều đó có thể khiến mô hình khó phân biệt giữa một tác vụ quản trị và một sự cố thiết bị hoặc ứng dụng.

## 5. Giả thuyết nguyên nhân

Từ các kết quả trên, nhóm đưa ra ba giả thuyết:

1. Nhãn Administrative rights có thể phản ánh quy trình xử lý hoặc nhóm phụ trách ticket, thay vì chỉ phản ánh những từ ngữ xuất hiện trong nội dung.
2. Một số ticket thiếu thông tin trực tiếp về quyền quản trị, khiến việc suy luận nhãn không rõ ràng.
3. Định nghĩa nhãn trong Prompt V2/V3/V4 có thể chưa phù hợp với cách sử dụng nhãn trong dataset.

Các giả thuyết này chưa được xác nhận vì nhóm chưa có tài liệu chính thức mô tả quy tắc gán nhãn cho toàn bộ dataset.

## 6. Đề xuất hướng cải thiện

- Kiểm tra thêm những ticket Administrative rights trong tập train chưa được sử dụng để đánh giá prompt.
- Xác định các dấu hiệu nghiệp vụ thường xuất hiện trong nhóm này.
- Đối chiếu các ví dụ có nội dung tương tự nhưng được gán nhãn khác nhau.
- Xem xét bổ sung ngữ cảnh về tác vụ quản trị hệ thống nếu có bằng chứng từ dữ liệu.
- Không tự ý sửa nhãn thực tế để phù hợp với dự đoán của mô hình.
- Chỉ đánh giá hiệu quả của prompt mới trên dữ liệu chưa dùng để thiết kế prompt.

## 7. Hạn chế

- Chỉ phân tích 20 ticket Administrative rights.
- Một số nội dung đã được rút gọn khi hiển thị trong Terminal.
- Chưa có thông tin về bộ phận tiếp nhận hoặc quy trình gán nhãn ban đầu.
- Phân tích định tính chưa đủ để xác nhận nhãn dữ liệu bị sai.
- Prompt V4 có một trường hợp lỗi xử lý trong nhóm này, cần phân biệt với lỗi chọn nhãn.

## 8. Kết luận

Kết quả phân tích cho thấy Administrative rights là nhóm nhãn khó phân loại đối với mô hình Qwen2.5:3B trong thực nghiệm hiện tại.

Nhiều ticket thuộc nhóm này mô tả những yêu cầu liên quan đến Windows, Outlook, thiết bị hoặc lưu trữ mà không nêu rõ đặc quyền quản trị.

Điều này gợi ý khả năng tồn tại khoảng cách giữa nội dung văn bản và quy ước gán nhãn của dataset.

Vì vậy, bước nghiên cứu tiếp theo nên tập trung tìm hiểu quy ước nhãn từ dữ liệu train trước khi tiếp tục thiết kế Prompt V5.

## 9. Các file liên quan

- `src/analyze_admin_rights.py`
- `results/llm_admin_rights_analysis.csv`
- `results/llm_experiments/analysis/llm_admin_rights_summary.csv`
- `results/llm_validation_predictions_v2.csv`
- `results/llm_validation_predictions_v3.csv`
- `results/llm_validation_predictions_v4.csv`