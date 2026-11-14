# Tuần 2 - Ngày 1: Phân tích chuyên sâu lỗi phân loại của mô hình LLM

## 1. Mục tiêu

Phân tích các trường hợp dự đoán sai của mô hình Qwen2.5:3B khi sử dụng Prompt V2 và Prompt V3, nhằm xác định các nhóm nhãn dễ nhầm lẫn và đề xuất hướng cải thiện mô hình.

## 2. Thiết lập thực nghiệm

- Mô hình: Qwen2.5:3B.
- Công cụ: Ollama.
- Phương pháp: Zero-shot Classification.
- Dữ liệu: 80 ticket trong tập phát triển, mỗi nhãn 10 ticket.
- Số nhóm nhãn: 8.
- File dữ liệu: `results/llm_comparison_v2_v3.csv`.

## 3. Kết quả tổng quan

| Chỉ số | Prompt V2 | Prompt V3 |
|---|---:|---:|
| Accuracy | 42,50% | 42,50% |
| Macro F1 | 0,3908 | 0,3691 |
| HR Support Recall | 10% | 40% |
| Số ticket đúng | 34 | 34 |
| Số ticket sai | 46 | 46 |

Phân tích đối chiếu trên từng ticket cho thấy:

- Cả hai phiên bản dự đoán đúng: 27 ticket.
- Cả hai phiên bản dự đoán sai: 39 ticket.
- V2 sai nhưng V3 đúng: 7 ticket.
- V2 đúng nhưng V3 sai: 7 ticket.

Kết quả cho thấy việc cải thiện Prompt V3 đã thay đổi một số dự đoán nhưng chưa nâng cao Accuracy tổng thể.

## 4. Phân tích những nhóm nhãn dễ nhầm lẫn

### 4.1. Hardware

Trong Prompt V3, có 5 ticket Hardware bị phân loại thành Access và 3 ticket bị phân loại thành Miscellaneous.

Đây là một trong những nhóm có mức độ nhầm lẫn cao nhất.

### 4.2. Administrative rights

Recall của Administrative rights giảm từ 20% ở Prompt V2 xuống 0% ở Prompt V3.

Trong Prompt V3, các trường hợp sai bao gồm 3 ticket được dự đoán thành Storage, 2 ticket thành Access và 2 ticket thành Miscellaneous.

### 4.3. HR Support

Prompt V3 cải thiện Recall của HR Support từ 10% lên 40%.

Tuy nhiên, vẫn có 3 ticket HR Support bị dự đoán thành Access. Ngoài ra, 2 ticket Miscellaneous bị dự đoán thành HR Support.

Điều này cho thấy việc mở rộng định nghĩa HR Support có tác động tích cực đến khả năng nhận diện nhãn này nhưng chưa giải quyết hoàn toàn sự chồng lấn ngữ nghĩa giữa các nhóm.

### 4.4. Storage

Số trường hợp Storage bị dự đoán thành Access giảm từ 5 ở Prompt V2 xuống 3 ở Prompt V3.

Tuy nhiên, Recall tổng thể của Storage vẫn giữ nguyên ở mức 30%.

## 5. Các giả thuyết nguyên nhân

1. Nội dung ticket có thể chứa nhiều thuật ngữ liên quan đến các nhóm nhãn khác nhau.
2. Một số nhãn trong dataset có phạm vi ngữ nghĩa chồng lấn.
3. Prompt chưa mô tả đầy đủ các tình huống đặc thù của Hardware và Administrative rights.
4. Việc mở rộng định nghĩa HR Support có thể ảnh hưởng đến cách mô hình lựa chọn các nhãn khác.
5. Một số ticket có thể thiếu ngữ cảnh hoặc có cách diễn đạt không rõ ràng.

Những nguyên nhân trên là giả thuyết ban đầu, cần được kiểm chứng bằng cách đọc và đối chiếu nội dung các ticket bị phân loại sai.

## 6. Đề xuất hướng nghiên cứu tiếp theo

- Phân tích nội dung 7 ticket được V3 sửa đúng.
- Phân tích 7 ticket V3 làm sai so với V2.
- Nghiên cứu những cặp nhãn nhầm lẫn thường gặp.
- Làm rõ ranh giới giữa Hardware, Access và Administrative rights.
- Nghiên cứu phương án cải thiện prompt mà không làm giảm hiệu quả của các nhãn khác.
- Đánh giá trên dữ liệu phát triển trước khi kiểm thử cuối cùng.

## 7. Hạn chế

Kết quả được tính trên tập phát triển cân bằng gồm 80 ticket, không phản ánh trực tiếp phân bố tự nhiên của dữ liệu thực tế.

Các phân tích lỗi mới dựa trên nhãn thực tế và nhãn dự đoán. Chưa có đủ bằng chứng để xác định nguyên nhân cụ thể của từng trường hợp sai.

## 8. Kết luận

Kết quả phân tích cho thấy Prompt V3 cải thiện khả năng nhận diện HR Support, nhưng hiệu quả phân loại tổng thể chưa tốt hơn Prompt V2.

Các nhóm Hardware và Administrative rights vẫn gặp nhiều khó khăn.

Do đó, cần tiếp tục phân tích nội dung những ticket bị phân loại sai trước khi thiết kế phiên bản Prompt V4.

## 9. Các file liên quan

- `src/experiments/analyze_prompt_errors.py`
- `results/llm_improved_cases.csv`
- `results/llm_regressed_cases.csv`
- `results/llm_both_wrong_cases.csv`
- `results/llm_confusion_pairs.csv`
- `results/llm_error_analysis_week2_day1.md`
## 10. Phân tích chi tiết các trường hợp thay đổi giữa Prompt V2 và V3

### 10.1. Những trường hợp Prompt V3 cải thiện

Phân tích 7 ticket được Prompt V3 sửa đúng cho thấy có 4 ticket thuộc HR Support và 3 ticket thuộc Access.

Đối với HR Support, các trường hợp cải thiện chủ yếu liên quan đến số ngày nghỉ, chấm công, timecard, Oracle và ngày nghỉ lễ. Những nội dung này phù hợp với phạm vi nghiệp vụ đã được bổ sung vào Prompt V3.

Đối với Access, Prompt V3 nhận diện đúng thêm các yêu cầu liên quan đến mật khẩu, quyền truy cập Confluence và thẻ ra vào.

Kết quả cho thấy việc làm rõ định nghĩa các nhãn có thể giúp mô hình phân biệt tốt hơn trong một số tình huống cụ thể.

### 10.2. Những trường hợp Prompt V3 suy giảm

Có 7 ticket được Prompt V2 dự đoán đúng nhưng Prompt V3 dự đoán sai.

Các trường hợp này thuộc những nhóm:

- HR Support: 1 ticket.
- Administrative rights: 2 ticket.
- Hardware: 1 ticket.
- Purchase: 1 ticket.
- Internal Project: 1 ticket.
- Miscellaneous: 1 ticket.

Đáng chú ý, ticket 20684 có nội dung đề cập trực tiếp đến administrator rights nhưng V3 lại dự đoán Access.

Ticket 19161 chứa nhiều thuật ngữ liên quan đến nghỉ phép và phê duyệt nhưng được gán nhãn Miscellaneous. V3 dự đoán HR Support, cho thấy việc mở rộng phạm vi HR có thể gây nhầm lẫn với một số nhãn khác.

Ticket 31742 liên quan đến cảnh báo lỗi thiết bị tape nhưng bị V3 phân loại thành Storage thay vì Hardware.

### 10.3. Nhận xét chung

Phân tích 14 ticket cho thấy Prompt V3 có những cải thiện cục bộ nhưng chưa nâng cao hiệu quả phân loại tổng thể.

Các tình huống sai chủ yếu cần được nghiên cứu thêm ở ranh giới giữa:

- HR Support và Miscellaneous.
- Access và Administrative rights.
- Hardware và Storage.
- Internal Project và Miscellaneous.

Một số trường hợp có thể tồn tại sự chồng lấn ngữ nghĩa hoặc chịu ảnh hưởng của quy ước gán nhãn trong dataset.

Đây là các giả thuyết cần kiểm tra thêm, không phải nguyên nhân đã được chứng minh.

### 10.4. Định hướng tiếp theo

Trong giai đoạn tiếp theo, nhóm sẽ nghiên cứu phương án cải thiện khả năng phân biệt giữa các nhóm nhãn, đặc biệt là Administrative rights và Hardware, đồng thời duy trì những cải thiện đã đạt được ở HR Support và Access.

Việc thiết kế prompt mới sẽ được thực hiện dựa trên kết quả phân tích lỗi, sau đó kiểm chứng bằng dữ liệu đánh giá phù hợp. Các kết quả từ tập phát triển hiện tại không được sử dụng như bằng chứng độc lập về khả năng tổng quát hóa của mô hình.