# Tuần 2 - Ngày 2: Thiết kế và đánh giá Prompt V4

## 1. Mục tiêu

Thiết kế Prompt V4 nhằm cải thiện khả năng phân biệt các nhóm nhãn dễ nhầm lẫn trong bài toán phân loại IT Support Ticket bằng mô hình Qwen2.5:3B.

Tập trung vào các cặp nhãn Access/Administrative rights, Hardware/Storage, HR Support/Miscellaneous và Internal Project/Miscellaneous.

## 2. Phương pháp thực nghiệm

- Mô hình: Qwen2.5:3B thông qua Ollama.
- Phương pháp: Zero-shot Classification.
- Phiên bản so sánh: Prompt V2, V3 và V4.
- Tập validation: 160 ticket lấy từ train.csv, cân bằng 20 ticket mỗi nhãn.
- Loại trừ các ticket đã sử dụng trong tập phát triển 80 ticket và các nội dung trùng khớp chính xác với những tập được kiểm tra khi tạo mẫu.
- Các phiên bản được đánh giá trên cùng 160 ticket.
- Chỉ số: Accuracy, Macro F1 và Recall theo nhãn.

## 3. Các thay đổi của Prompt V4

Prompt V4 được xây dựng từ V3, với các điều chỉnh:

- Làm rõ sự khác biệt giữa quyền truy cập thông thường và quyền quản trị hệ thống.
- Phân biệt sự cố thiết bị vật lý với vấn đề dung lượng hoặc lưu trữ dữ liệu.
- Bổ sung ngữ cảnh tiếp nhận và giao hàng vào nhóm Purchase.
- Mở rộng mô tả nhóm Internal Project.
- Hạn chế việc phân loại HR Support chỉ dựa trên từ khóa đơn lẻ.
- Yêu cầu mô hình tập trung vào mục đích chính của ticket.

## 4. Kết quả tổng thể

| Chỉ số | V2 | V3 | V4 |
|---|---:|---:|---:|
| Accuracy | 44,38% | 48,75% | 45,00% |
| Macro F1 | 0,4192 | 0,4616 | 0,4317 |
| HR Support Recall | 20% | 65% | 25% |
| Dự đoán thành công | 159/160 | 160/160 | 158/160 |
| Dự đoán đúng | 71/160 | 78/160 | 72/160 |

Kết quả cho thấy V3 đạt Accuracy và Macro F1 cao nhất trong ba phiên bản.

V4 không cải thiện hiệu quả tổng thể và có mức suy giảm đáng kể ở HR Support.

## 5. So sánh V3 và V4 theo từng ticket

- Số ticket có dự đoán khác nhau: 44.
- V4 sửa đúng so với V3: 8.
- V4 làm sai so với V3: 14.
- Chênh lệch ròng: giảm 6 dự đoán đúng.

Như vậy, những thay đổi trong Prompt V4 có ảnh hưởng đến kết quả dự đoán, nhưng không tạo ra cải thiện tổng thể.

## 6. Recall theo từng nhóm nhãn

| Nhóm nhãn | V2 | V3 | V4 |
|---|---:|---:|---:|
| Access | 70% | 70% | 70% |
| Administrative rights | 0% | 0% | 0% |
| HR Support | 20% | 65% | 25% |
| Hardware | 45% | 55% | 40% |
| Internal Project | 35% | 50% | 60% |
| Miscellaneous | 70% | 50% | 60% |
| Purchase | 90% | 85% | 85% |
| Storage | 25% | 15% | 20% |

V4 cải thiện Recall ở Internal Project, Miscellaneous và Storage so với V3.

Tuy nhiên, Hardware và HR Support bị suy giảm. Administrative rights vẫn không có dự đoán đúng trên tập validation.

## 7. Thảo luận

Kết quả cho thấy việc bổ sung quy tắc phân biệt các nhãn không bảo đảm nâng cao chất lượng phân loại.

Một giả thuyết là các điều chỉnh của V4 làm thay đổi cách mô hình ưu tiên giữa các nhóm nhãn, đặc biệt khi nội dung ticket có nhiều ngữ cảnh chồng lấn.

Tuy nhiên, chưa thể khẳng định nguyên nhân chỉ từ các chỉ số tổng hợp. Cần phân tích thêm những ticket đổi dự đoán và các trường hợp xử lý thất bại.

## 8. Hạn chế

- Tập validation chỉ gồm 160 ticket.
- Mỗi nhãn có 20 ticket nên kết quả theo nhãn vẫn có độ biến động đáng kể.
- Tập validation được lấy từ train.csv; không phù hợp để đánh giá độc lập baseline đã được huấn luyện trên cùng tập train.
- Việc loại bỏ nội dung trùng khớp chính xác chưa bảo đảm loại toàn bộ ticket gần trùng hoặc cùng chuỗi hội thoại.
- V2 có một trường hợp xử lý không thành công và V4 có hai trường hợp; các trường hợp này được tính là dự đoán sai.
- Kết quả chỉ phản ánh những lần chạy hiện tại, chưa đánh giá độ ổn định qua nhiều lần chạy.
### 8.1. Phân tích các trường hợp xử lý thất bại

Trong quá trình đánh giá Prompt V4 trên 160 ticket, mô hình xử lý thành công 158 ticket và ghi nhận 2 trường hợp lỗi:

- Ticket ID 808, thuộc nhóm Hardware.
- Ticket ID 855, thuộc nhóm Administrative rights.

Hai trường hợp này được tính là dự đoán sai khi tính Accuracy và Macro F1, bảo đảm không loại bỏ các mẫu khó hoặc mẫu lỗi khỏi phép đánh giá.

Do chương trình chưa lưu thông báo ngoại lệ cụ thể, chưa thể xác định nguyên nhân là lỗi giao tiếp với Ollama, phản hồi JSON không hợp lệ hay vấn đề khác.

Các kết quả dự đoán gốc được giữ nguyên để bảo đảm tính minh bạch và khả năng tái lập thực nghiệm.

## 9. Kết luận

Prompt V4 chưa đạt mục tiêu cải thiện hiệu quả tổng thể.

Trên tập validation 160 ticket, V3 đạt Accuracy 48,75% và Macro F1 0,4616, cao hơn V2 và V4.

Do đó, nhóm tạm thời lựa chọn Prompt V3 làm phiên bản ưu tiên cho giai đoạn đánh giá tiếp theo.

Nhóm cần tiếp tục nghiên cứu những trường hợp Administrative rights bị phân loại sai và kiểm tra nguyên nhân xử lý thất bại, nhưng không điều chỉnh các dự đoán đã lưu để làm tăng kết quả đánh giá.

## 10. File liên quan

- `src/llm_classifier_v4.py`
- `src/evaluate_dev.py`
- `src/compare_validation.py`
- `results/llm_validation_sample160.csv`
- `results/llm_validation_predictions_v2.csv`
- `results/llm_validation_predictions_v3.csv`
- `results/llm_validation_predictions_v4.csv`
- `results/llm_validation_comparison.csv`
- `results/llm_experiments/analysis/llm_validation_recall_by_label.csv`