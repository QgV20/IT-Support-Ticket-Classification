# Tuần 3 — Ngày 2: Phân tích các ticket Baseline và LLM cùng dự đoán sai

## 1. Mục tiêu

Phân tích những ticket mà cả TF-IDF + Logistic Regression (Baseline) và Qwen2.5:3B Zero-shot Prompt V3 (LLM) đều dự đoán sai trên cùng tập test400.

Mục tiêu là xác định các nhóm nhãn khó, những kiểu nhầm lẫn phổ biến và các yếu tố có thể ảnh hưởng đến hiệu quả phân loại.

## 2. Dữ liệu và phương pháp

- Tập dữ liệu: `data/test_sample.csv`, gồm 400 ticket.
- Kết quả so sánh: `results/baseline_llm_comparison_400.csv`.
- Tiêu chí lựa chọn: `comparison_case == "both_wrong"`.
- Phương pháp: Thống kê theo nhãn thực tế, so sánh nhãn dự đoán và phân tích nội dung một số trường hợp tiêu biểu.

Không chạy lại mô hình hoặc điều chỉnh tham số trong giai đoạn phân tích.

## 3. Kết quả tổng quan

Trong 400 ticket, có 45 trường hợp cả Baseline và LLM cùng phân loại sai, tương đương 11,25% tập test.

Trong 45 trường hợp này:

- 18 ticket: hai mô hình chọn cùng một nhãn sai.
- 27 ticket: hai mô hình chọn hai nhãn sai khác nhau.

| Nhãn thực tế | Số ticket cả hai sai |
|---|---:|
| Hardware | 16 |
| HR Support | 12 |
| Access | 6 |
| Miscellaneous | 6 |
| Purchase | 3 |
| Storage | 1 |
| Internal Project | 1 |
| Administrative rights | 0 |
| **Tổng cộng** | **45** |

Hardware và HR Support chiếm 28/45 trường hợp cùng sai, tương đương khoảng 62,22%.

Đây là số lượng lỗi tuyệt đối trong nhóm cùng sai; chưa phải tỷ lệ lỗi trên tổng số mẫu của từng nhãn.

## 4. Những kiểu nhầm lẫn nổi bật

### 4.1. Baseline

Trong 45 trường hợp cùng sai, những cặp nhầm lẫn xuất hiện nhiều gồm:

- HR Support → Hardware: 7 ticket.
- Hardware → Miscellaneous: 5 ticket.
- Hardware → Access: 4 ticket.
- Hardware → HR Support: 4 ticket.

### 4.2. LLM

Những cặp nhầm lẫn xuất hiện nhiều gồm:

- Hardware → Miscellaneous: 9 ticket.
- HR Support → Miscellaneous: 6 ticket.
- Miscellaneous → Internal Project: 4 ticket.
- Access → Miscellaneous: 4 ticket.
- Hardware → Access: 4 ticket.

Các thống kê này chỉ áp dụng cho nhóm 45 ticket cả hai cùng sai, không đại diện cho toàn bộ lỗi của từng mô hình.

## 5. Phân tích sáu trường hợp tiêu biểu

| Row ID | Nhãn thực tế | Baseline | LLM |
|---|---|---|---|
| 19 | HR Support | Administrative rights | Hardware |
| 77 | Hardware | Miscellaneous | Miscellaneous |
| 89 | Access | HR Support | HR Support |
| 113 | Miscellaneous | Internal Project | Internal Project |
| 222 | Purchase | Miscellaneous | Hardware |
| 315 | Storage | Administrative rights | Access |

### Ticket 19 — Windows installation failure

Ticket mô tả lỗi cài đặt Windows, nhưng nhãn thực tế là HR Support.

Cả hai mô hình lựa chọn nhãn liên quan đến hoạt động kỹ thuật thay vì HR Support. Đây có thể là trường hợp nhãn phản ánh quy trình nghiệp vụ không thể suy ra trực tiếp từ mô tả ngắn.

### Ticket 77 — Server patching reports

Ticket yêu cầu báo cáo tình trạng cập nhật bản vá. Cả hai mô hình dự đoán Miscellaneous thay vì Hardware.

Trường hợp này gợi ý sự khó khăn trong việc xác định ranh giới giữa tác vụ quản trị hệ thống và nhóm Hardware theo quy ước dataset.

### Ticket 89 — Credentials expired

Ticket đề cập thông tin xác thực hết hạn trong bối cảnh thực tập.

Cả hai mô hình dự đoán HR Support, trong khi nhãn thực tế là Access. Đây là một ví dụ về sự chồng lấn giữa ngữ cảnh nhân sự và yêu cầu xác thực tài khoản.

### Ticket 113 — Project manager / project code

Ticket chứa các từ ngữ liên quan đến dự án. Hai mô hình đều chọn Internal Project nhưng nhãn thực tế là Miscellaneous.

Các từ khóa liên quan đến dự án có thể không đủ để suy ra đúng nhãn nghiệp vụ.

### Ticket 222 — Computer out of order

Ticket mô tả máy tính gặp sự cố. Baseline chọn Miscellaneous và LLM chọn Hardware, trong khi nhãn thực tế là Purchase.

Nội dung nhìn thấy chưa nêu rõ mục đích mua sắm, do đó chưa thể giải thích chắc chắn vì sao nhãn chuẩn là Purchase.

### Ticket 315 — Not enough rights on portal

Ticket phản ánh việc không đủ quyền trên cổng thông tin. Baseline chọn Administrative rights, LLM chọn Access, nhưng nhãn thực tế là Storage.

Đây là trường hợp cần chú ý khi đánh giá mức độ phù hợp giữa ngữ nghĩa văn bản và quy ước nhãn trong dữ liệu.

## 6. Thảo luận

Phân tích cho thấy ba vấn đề đáng chú ý:

Thứ nhất, nhiều ticket thuộc nhóm cùng sai có ngữ cảnh chồng lấn giữa các nhãn.

Thứ hai, một số mô tả có vẻ phù hợp với nhãn khác hơn nhãn thực tế theo cách hiểu thông thường. Điều này có thể liên quan đến quy ước gán nhãn đặc thù, thông tin ngữ cảnh bị thiếu hoặc sự phức tạp của ticket.

Thứ ba, LLM có xu hướng nhầm một số ticket Hardware và HR Support thành Miscellaneous. Baseline cũng có những nhầm lẫn riêng, đặc biệt giữa HR Support và Hardware trong nhóm lỗi được xem xét.

Các giải thích trên là giả thuyết dựa trên quan sát, không phải kết luận rằng nhãn gốc bị sai.

## 7. Hạn chế

- Mới phân tích định tính sáu trường hợp tiêu biểu trong tổng số 45 ticket.
- Một số ticket có thể thiếu ngữ cảnh nghiệp vụ quan trọng.
- Các kết quả dựa trên tập test 400 ticket.
- Chưa kiểm tra độc lập chất lượng nhãn của dataset.
- Chưa xác định nguyên nhân nhân quả của các lỗi dự đoán.

## 8. Kết luận

Có 45/400 ticket mà cả Baseline và LLM đều dự đoán sai.

Trong đó, 18 ticket được hai mô hình gán cùng một nhãn sai và 27 ticket được gán hai nhãn sai khác nhau.

Hardware và HR Support là hai nhóm có số lượng trường hợp cùng sai cao nhất.

Phân tích các ví dụ cho thấy việc phân loại ticket có thể gặp khó khăn do ngữ cảnh nghiệp vụ, mô tả mơ hồ, sự chồng lấn giữa các nhãn và quy ước phân loại đặc thù của dataset.

Những phát hiện này cung cấp cơ sở cho việc đánh giá confusion matrix của LLM và so sánh lỗi theo từng nhãn trong bước nghiên cứu tiếp theo.