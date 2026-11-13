# Tổng kết hai tuần thực nghiệm phân loại IT Support Ticket bằng LLM

## 1. Mục tiêu

Nghiên cứu khả năng phân loại IT Support Ticket bằng mô hình ngôn ngữ Qwen2.5:3B thông qua Ollama, sử dụng phương pháp Zero-shot Classification.

Thực nghiệm tập trung vào thiết kế prompt, cải thiện khả năng nhận diện tám nhóm ticket, phân tích lỗi và so sánh với phương pháp Machine Learning truyền thống TF-IDF + Logistic Regression.

## 2. Thiết lập thực nghiệm

- Mô hình LLM: Qwen2.5:3B.
- Công cụ triển khai: Ollama và Python.
- Phương pháp LLM: Zero-shot Classification.
- Số nhóm nhãn: 8.
- Tập phát triển ban đầu: 80 ticket, cân bằng 10 ticket mỗi nhãn.
- Tập validation bổ sung: 160 ticket, cân bằng 20 ticket mỗi nhãn.
- Tập test cuối cùng: 400 ticket.
- Chỉ số đánh giá: Accuracy, Macro F1, Precision và Recall theo nhãn.
- Baseline: TF-IDF kết hợp Logistic Regression, do Thành viên 1 thực hiện.

Các tập phát triển được lấy từ train.csv và chỉ dùng để nghiên cứu prompt. Tập test được dùng cho đánh giá cuối cùng.

## 3. Quá trình phát triển prompt

### Prompt V1

Xây dựng bộ phân loại Zero-shot ban đầu, xác định danh sách tám nhãn và yêu cầu mô hình trả về kết quả theo định dạng JSON.

### Prompt V2

Bổ sung định nghĩa các nhóm nhãn và những quy tắc phân biệt cơ bản nhằm giảm nhầm lẫn giữa các loại ticket.

### Prompt V3

Mở rộng mô tả HR Support để nhận diện các nghiệp vụ như timecard, annual leave, payroll, onboarding và lỗi ứng dụng liên quan đến quy trình nhân sự.

### Prompt V4

Bổ sung các quy tắc phân biệt Access/Administrative rights, Hardware/Storage và một số nhóm nhãn dễ nhầm lẫn khác.

Kết quả thực nghiệm cho thấy V4 chưa cải thiện hiệu quả tổng thể.

### Prompt V5

Nghiên cứu đặc điểm của Administrative rights trong dữ liệu train, đặc biệt các yêu cầu Windows upgrade và triển khai hệ điều hành.

Prompt V5 mở rộng định nghĩa Administrative rights và bổ sung quy tắc phân biệt với Hardware.

V5 cải thiện Recall của Administrative rights nhưng làm giảm Accuracy và Macro F1 tổng thể.

## 4. Kết quả trên tập validation160

| Chỉ số | V2 | V3 | V4 | V5 |
|---|---:|---:|---:|---:|
| Accuracy | 44,38% | 48,75% | 45,00% | 40,00% |
| Macro F1 | 0,4192 | 0,4616 | 0,4317 | 0,4180 |
| HR Support Recall | 20% | 65% | 25% | 40% |
| Administrative rights Recall | 0% | 0% | 0% | 25% |

Theo tiêu chí ưu tiên Accuracy và Macro F1, Prompt V3 được lựa chọn cho bước đánh giá cuối cùng.

## 5. Phân tích lỗi giữa Prompt V3 và V5

Trên 160 ticket:

- Hai phiên bản cho 68 dự đoán khác nhau.
- Cả hai cùng đúng: 51 ticket.
- Cả hai cùng sai: 69 ticket.
- V5 sửa đúng so với V3: 13 ticket.
- V5 làm sai so với V3: 27 ticket.

Năm trong số 13 ticket V5 sửa đúng thuộc nhóm Administrative rights, chủ yếu liên quan đến cài đặt hoặc nâng cấp hệ thống.

Đáng chú ý, cả 27 ticket bị V5 làm sai đều được chuyển thành Miscellaneous.

Điều này gợi ý Prompt V5 có xu hướng lựa chọn Miscellaneous rộng hơn so với V3.

## 6. Đánh giá Prompt V3 trên tập test cuối cùng

Tập test gồm 400 ticket thuộc tám nhãn.

Kết quả:

- Accuracy: 41,00% (164/400 ticket).
- Macro F1: 0,3729.
- Dự đoán thành công: 399/400 ticket.
- Có một trường hợp lỗi do mô hình trả về nhãn Security ngoài danh sách tám nhãn hợp lệ.

Ticket lỗi được giữ trong tập đánh giá và tính là dự đoán sai.

### Kết quả theo từng nhãn

| Nhãn | Precision | Recall | F1-score |
|---|---:|---:|---:|
| Access | 0,34 | 0,51 | 0,41 |
| Administrative rights | 0,00 | 0,00 | 0,00 |
| HR Support | 0,62 | 0,56 | 0,59 |
| Hardware | 0,73 | 0,32 | 0,44 |
| Internal Project | 0,40 | 0,44 | 0,42 |
| Miscellaneous | 0,17 | 0,34 | 0,22 |
| Purchase | 0,62 | 0,71 | 0,67 |
| Storage | 0,36 | 0,17 | 0,24 |

Purchase là nhãn có F1-score cao nhất của LLM trên tập test.

Administrative rights tiếp tục là nhãn có hiệu quả thấp nhất với Recall bằng 0%.

## 7. Phân tích bổ sung trên 390 ticket

Nhóm loại 10 ticket đầu của test_sample.csv từng được xem trong quá trình phát triển prompt, chỉ ở bước tính chỉ số bổ sung.

Kết quả trên 390 ticket còn lại:

- Accuracy: 40,51%.
- Macro F1: 0,3691.
- Có một trường hợp lỗi xử lý.

Kết quả gần với phép đánh giá trên 400 ticket, nhưng không chứng minh toàn bộ 390 ticket hoàn toàn độc lập ở cấp chuỗi hội thoại.

## 8. So sánh với baseline

Baseline của Thành viên 1 sử dụng TF-IDF kết hợp Logistic Regression.

Hai phương pháp được báo cáo trên cùng tập test_sample.csv gồm 400 ticket.

| Chỉ số | Baseline | LLM Prompt V3 |
|---|---:|---:|
| Accuracy | 85,75% | 41,00% |
| Macro F1 | 0,8611 | 0,3729 |
| Số dự đoán đúng | 343/400 | 164/400 |

Baseline cao hơn LLM:

- 44,75 điểm phần trăm Accuracy.
- 0,4882 Macro F1.
- 179 dự đoán đúng.

Baseline cũng có Recall cao hơn LLM ở cả tám nhóm nhãn.

## 9. Thảo luận

Kết quả cho thấy mô hình TF-IDF + Logistic Regression được huấn luyện có giám sát hoạt động tốt hơn đáng kể so với Qwen2.5:3B Zero-shot trong thiết lập thực nghiệm này.

Một số khả năng cần xem xét gồm:

- Baseline được huấn luyện trực tiếp trên dữ liệu có nhãn của bài toán.
- LLM sử dụng kiến thức tổng quát và mô tả nhãn trong prompt, không được fine-tune trên tập train.
- Một số nhãn, đặc biệt Administrative rights, có thể phản ánh quy ước xử lý ticket đặc thù của dataset.
- Việc mở rộng prompt không bảo đảm cải thiện đồng thời tất cả các nhãn.

Các khả năng trên là hướng giải thích và cần được kiểm chứng thêm, không phải kết luận nhân quả từ những phép thử hiện có.

## 10. Hạn chế thực nghiệm

- Mô hình LLM chỉ sử dụng Qwen2.5:3B.
- Thực nghiệm tập trung vào Zero-shot, chưa đánh giá Few-shot hoặc Fine-tuning.
- Các chỉ số validation dựa trên tập phát triển được lấy từ train.csv.
- Một phần dữ liệu test đã được quan sát khi thiết kế các prompt trước đó.
- Kiểm tra nội dung trùng khớp chính xác không phát hiện hết các trường hợp gần trùng hoặc cùng chuỗi hội thoại.
- Chưa đánh giá độ ổn định qua nhiều lần chạy trên cùng tập dữ liệu.
- Chưa thực hiện so sánh thống kê ghép cặp dự đoán từng ticket giữa baseline và LLM.
- Các chỉ số thời gian xử lý của hai phương pháp cần được diễn giải thận trọng do điều kiện thực thi và cách đo có thể khác nhau.

## 11. Kết luận

Trong các phiên bản prompt được thử nghiệm, Prompt V3 đạt Accuracy và Macro F1 cao nhất trên tập validation160, nên được lựa chọn cho đánh giá cuối cùng.

Trên test_sample.csv gồm 400 ticket, Qwen2.5:3B Zero-shot Prompt V3 đạt Accuracy 41,00% và Macro F1 0,3729.

Baseline TF-IDF + Logistic Regression đạt Accuracy 85,75% và Macro F1 0,8611 trên cùng tập test.

Kết quả cho thấy phương pháp baseline vượt trội trong bài toán và điều kiện thực nghiệm hiện tại.

Nghiên cứu đồng thời chỉ ra những hạn chế của việc phân loại ticket theo prompt, đặc biệt với các nhãn có quy ước đặc thù và nội dung chồng lấn.

## 12. File kết quả chính

- `src/llm_classifier.py`
- `src/llm_classifier_v5.py`
- `src/run_llm_batch.py`
- `src/check_final_test.py`
- `results/llm_final_predictions_v3_400.csv`
- `results/baseline_report.txt`
- `results/final_test_integrity_check.csv`
- `results/llm_validation_predictions_v3.csv`
- `results/llm_validation_predictions_v5.csv`
- `results/llm_two_week_summary.md`