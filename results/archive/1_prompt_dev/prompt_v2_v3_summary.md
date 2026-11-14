# So sánh hiệu quả Prompt V2 và Prompt V3

## 1. Mục tiêu thực nghiệm

Đánh giá tác động của việc cải thiện prompt đối với khả năng phân loại tự động yêu cầu hỗ trợ CNTT bằng mô hình Qwen2.5:3B thông qua Ollama.

Thực nghiệm tập trung vào việc so sánh hiệu quả tổng thể và khả năng nhận diện nhóm HR Support giữa Prompt V2 và Prompt V3.

## 2. Thiết lập thực nghiệm

- Mô hình: Qwen2.5:3B
- Công cụ triển khai: Ollama
- Phương pháp: Zero-shot Classification
- Số nhóm nhãn: 8
- Dữ liệu: 80 ticket lấy từ `train.csv`
- Phương pháp lấy mẫu: 10 ticket cho mỗi nhóm nhãn, sử dụng random_state=42
- Temperature: 0
- Hai phiên bản được chạy trên cùng 80 ticket.

Tập dữ liệu trên được sử dụng cho mục đích phát triển và so sánh prompt, không phải tập kiểm thử độc lập cuối cùng.

## 3. Kết quả so sánh tổng thể

| Chỉ số | Prompt V2 | Prompt V3 |
|---|---:|---:|
| Accuracy | 42,50% | 42,50% |
| Macro F1 | 0,3908 | 0,3691 |
| HR Support Recall | 10% | 40% |
| Số dự đoán đúng | 34/80 | 34/80 |
| Số ticket xử lý thành công | 80/80 | 80/80 |

Kết quả cho thấy hai phiên bản đạt cùng Accuracy, nhưng Macro F1 của V3 thấp hơn V2.

Trong khi đó, HR Support Recall của V3 tăng 30 điểm phần trăm so với V2.

## 4. Phân tích sự thay đổi kết quả dự đoán

- Cả hai phiên bản dự đoán đúng: 27 ticket.
- Cả hai phiên bản dự đoán sai: 39 ticket.
- V2 dự đoán sai nhưng V3 dự đoán đúng: 7 ticket.
- V2 dự đoán đúng nhưng V3 dự đoán sai: 7 ticket.

Như vậy, Prompt V3 đã thay đổi kết quả phân loại của một số ticket nhưng không làm tăng tổng số dự đoán đúng.

## 5. Đánh giá theo từng nhóm nhãn

| Nhóm nhãn | Recall V2 | Recall V3 |
|---|---:|---:|
| Access | 30% | 60% |
| Administrative rights | 20% | 0% |
| HR Support | 10% | 40% |
| Hardware | 10% | 0% |
| Internal Project | 70% | 60% |
| Miscellaneous | 70% | 60% |
| Purchase | 100% | 90% |
| Storage | 30% | 30% |

### Nhận xét

Prompt V3 cải thiện rõ rệt Recall của HR Support và Access trên mẫu thử.

Tuy nhiên, Recall của Hardware và Administrative rights giảm xuống 0%. Một số nhóm khác cũng giảm nhẹ.

Điều này cho thấy việc mở rộng định nghĩa HR Support chưa bảo đảm cải thiện đồng đều hiệu quả phân loại của tám nhóm.

## 6. Hạn chế của thực nghiệm

- Tập phát triển chỉ gồm 80 ticket, mỗi nhãn 10 ticket.
- Tập mẫu cân bằng không phản ánh phân bố nhãn tự nhiên trong dữ liệu thực tế.
- Việc lựa chọn và thiết kế Prompt V3 đã sử dụng thông tin phân tích từ tập train.
- Các nhãn trong dataset có thể chứa trường hợp chồng lấn hoặc khó phân biệt về ngữ nghĩa.
- Chưa đánh giá hiệu quả tổng quát trên một tập kiểm thử độc lập hoàn toàn.

Vì vậy, các kết quả cần được xem là kết quả thực nghiệm thăm dò.

## 7. Kết luận

Prompt V3 đạt mục tiêu cải thiện khả năng nhận diện HR Support, với Recall tăng từ 10% lên 40%.

Tuy nhiên, Accuracy của V3 không thay đổi so với V2 và Macro F1 giảm từ 0,3908 xuống 0,3691.

Do đó, chưa có đủ cơ sở để kết luận V3 tốt hơn V2 về hiệu quả tổng thể.

Trong giai đoạn tiếp theo, nhóm cần phân tích các trường hợp phân loại sai, cân nhắc cải thiện cách định nghĩa nhãn và đánh giá lại trên dữ liệu độc lập trước khi lựa chọn phương án cuối cùng.

## 8. Các file liên quan

- `results/llm_dev_sample80.csv`
- `results/llm_dev_predictions_v2.csv`
- `results/llm_dev_predictions_v3.csv`
- `results/llm_comparison_v2_v3.csv`
- `results/llm_experiments/analysis/llm_recall_by_label.csv`
- `src/evaluate_dev.py`
- `src/experiments/compare_prompts.py`