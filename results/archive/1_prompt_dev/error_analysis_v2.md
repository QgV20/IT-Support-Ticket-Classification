# Phân tích lỗi phân loại của mô hình Qwen2.5:3B

## 1. Mục tiêu

Phân tích các trường hợp mô hình LLM dự đoán sai nhãn yêu cầu hỗ trợ CNTT nhằm xác định những khó khăn khi áp dụng phương pháp Zero-shot Classification trên dữ liệu thực tế.

## 2. Thiết lập thực nghiệm

- Mô hình: Qwen2.5:3B
- Công cụ triển khai: Ollama
- Phương pháp: Zero-shot Classification
- Prompt: V2 — Có mô tả 8 nhãn và quy tắc phân loại
- Dữ liệu: 10 ticket đầu tiên từ `data/test_sample.csv`
- File kết quả: `results/llm_predictions_v2_sample10.csv`

## 3. Kết quả

- Tổng số ticket: 10
- Số ticket xử lý thành công: 10
- Số dự đoán khớp nhãn thực tế: 3
- Số dự đoán không khớp: 7
- Accuracy: 30%

## 4. Phân tích lỗi

Các trường hợp phân loại sai tập trung ở một số nhóm yêu cầu có nội dung thiếu rõ ràng hoặc chứa thuật ngữ liên quan đến nhiều nhãn.

Đáng chú ý, cả 4 ticket thuộc nhóm HR Support đều bị dự đoán sang những nhãn khác, bao gồm Storage, Access và Miscellaneous.

Một số ticket chứa những từ khóa như "access request", "Oracle" và "logging", có thể khiến mô hình ưu tiên phân loại theo ý nghĩa thông thường của câu thay vì quy ước gán nhãn trong dataset.

## 5. Giả thuyết nguyên nhân

1. Prompt chưa mô tả đầy đủ ý nghĩa của các nhãn theo quy ước của dataset.
2. Nội dung ticket có nhiều từ viết tắt, thiếu ngữ cảnh hoặc diễn đạt không rõ ràng.
3. Mô hình chưa được huấn luyện chuyên biệt trên dữ liệu IT Support của nhóm.
4. Một số nhãn có thể chồng lấn về ý nghĩa.

Các nguyên nhân trên là giả thuyết cần tiếp tục kiểm chứng.

## 6. Hướng thực nghiệm tiếp theo

- Kiểm tra phân bố và nội dung các nhãn trong tập train.
- Đối chiếu định nghĩa nhãn với dữ liệu thực tế.
- Xây dựng phương án cải thiện prompt dựa trên tập phát triển.
- Đánh giá mô hình trên tập dữ liệu lớn hơn và có phương pháp lấy mẫu phù hợp.
- So sánh LLM với mô hình Machine Learning baseline trên cùng tập kiểm thử.

## 7. Kết luận sơ bộ

Mô hình Qwen2.5:3B đã thực hiện thành công quy trình phân loại tự động bằng Ollama. Tuy nhiên, Accuracy trên 10 ticket đầu tiên chỉ đạt 30%, cho thấy còn sự khác biệt đáng kể giữa nhãn dự đoán và nhãn thực tế.

Do quy mô mẫu nhỏ, kết quả này mang tính thăm dò và chưa đủ để đánh giá hiệu quả tổng quát của mô hình.