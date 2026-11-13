# Tuần 3 — Ngày 4: So sánh thời gian suy luận và hiệu quả triển khai Baseline và LLM

## 1. Mục tiêu

Đánh giá sự khác biệt về thời gian xử lý và chất lượng phân loại giữa hai phương pháp:

- TF-IDF + Logistic Regression (Baseline).
- Qwen2.5:3B Zero-shot Prompt V3 (LLM).

Thực nghiệm sử dụng kết quả dự đoán đã lưu trên cùng tập `test_sample.csv` gồm 400 ticket.

Mục tiêu là phân tích sự đánh đổi giữa độ chính xác, tốc độ và khả năng ứng dụng vào bài toán phân loại IT Support Ticket.

## 2. Dữ liệu và phương pháp đo

### 2.1. Baseline

Thời gian dự đoán được lấy từ `results/baseline_report.txt`.

Chương trình `train_baseline.py` đo thời gian thực hiện `model.predict()` trên tập 400 ticket và chia cho tổng số dòng.

Thời gian này không bao gồm huấn luyện mô hình, đọc dữ liệu hoặc tải mô hình từ file.

### 2.2. LLM

Thời gian suy luận được lấy từ cột `processing_time_seconds` trong `results/llm_final_predictions_v3_400.csv`.

Tập kết quả gồm:

- 400 ticket được xử lý.
- 399 ticket có dự đoán hợp lệ.
- 1 ticket trả về nhãn không hợp lệ và được ghi nhận là lỗi.

Thời gian của cả 400 ticket, bao gồm ticket lỗi, được giữ lại trong phân tích.

Các chỉ số được tính gồm Mean, Median, P95, Min, Max và tổng thời gian.

## 3. Kết quả thời gian của LLM

| Chỉ số | Kết quả |
|---|---:|
| Tổng ticket | 400 |
| Tổng thời gian | 80,854 giây |
| Thời gian trung bình | 0,2021 giây/ticket |
| Trung vị | 0,1785 giây/ticket |
| P95 | 0,2453 giây/ticket |
| Nhỏ nhất | 0,137 giây |
| Lớn nhất | 6,627 giây |
| Ticket đầu tiên | 6,627 giây |
| Trung bình bỏ ticket đầu | 0,1860 giây/ticket |

Kết quả cho thấy ticket đầu tiên có thời gian xử lý cao hơn rõ rệt so với phần lớn ticket còn lại.

Hiện tượng này có thể liên quan đến chi phí khởi tạo hoặc nạp mô hình, nhưng thực nghiệm chưa đo riêng từng thành phần.

Sau khi loại ticket đầu khỏi phép tính trung bình bổ sung, thời gian trung bình còn khoảng 186,0 ms/ticket.

## 4. So sánh thời gian xử lý

| Chỉ số | Baseline | LLM V3 |
|---|---:|---:|
| Thời gian trung bình | 0,052 ms/ticket | 202,1 ms/ticket |
| Tổng thời gian trên 400 ticket | Khoảng 0,0208 giây | 80,854 giây |
| Thời gian trung bình sau khi bỏ lần gọi đầu của LLM | Không đo | 186,0 ms/ticket |

Tổng thời gian Baseline được ước tính từ thời gian trung bình đã làm tròn trong báo cáo.

Tỷ số giữa thời gian trung bình LLM và Baseline:

202,1 / 0,052 ≈ 3.887 lần.

Nếu sử dụng thời gian LLM trung bình sau khi loại lần gọi đầu:

186,0 / 0,052 ≈ 3.577 lần.

Các tỷ số này mang tính mô tả dựa trên những phép đo hiện có, không phải kết quả benchmark trên môi trường phần cứng và quy trình đo được kiểm soát hoàn toàn giống nhau.

## 5. So sánh tốc độ và chất lượng phân loại

| Chỉ số | Baseline | LLM V3 |
|---|---:|---:|
| Accuracy | 85,75% | 41,00% |
| Macro F1 | 0,8611 | 0,3729 |
| Dự đoán đúng | 343/400 | 164/400 |
| Dự đoán hợp lệ | 400/400 | 399/400 |
| Thời gian trung bình/ticket | 0,052 ms | 202,1 ms |

Baseline đạt Accuracy cao hơn 44,75 điểm phần trăm và Macro F1 cao hơn 0,4882.

Đồng thời, thời gian dự đoán được báo cáo của Baseline thấp hơn nhiều so với LLM.

## 6. Phân tích khả năng ứng dụng

### 6.1. Baseline

TF-IDF + Logistic Regression có những ưu điểm được hỗ trợ bởi kết quả thực nghiệm:

- Accuracy và Macro F1 cao trên tập kiểm thử.
- Dự đoán nhanh trong phép đo hiện có.
- Nhận diện tốt cả tám nhóm nhãn so với LLM V3.
- Có thể sử dụng mô hình đã huấn luyện để phân loại dữ liệu mới có cùng cấu trúc.

Hạn chế là mô hình cần dữ liệu có nhãn để huấn luyện và có thể phải cập nhật khi nội dung hoặc quy ước phân loại thay đổi.

### 6.2. LLM Zero-shot

Qwen2.5:3B Zero-shot không cần huấn luyện lại trọng số trên dữ liệu ticket của nhóm.

Mô hình có thể được hướng dẫn bằng prompt và mô tả các nhãn.

Tuy nhiên, trong thiết lập thực nghiệm hiện tại:

- Accuracy và Macro F1 thấp hơn Baseline.
- Thời gian suy luận quan sát được lớn hơn.
- Một dự đoán trả về nhãn ngoài danh sách hợp lệ.
- Một số nhóm nhãn, đặc biệt Administrative rights, có Recall rất thấp.

LLM vẫn phân loại đúng 12 ticket mà Baseline dự đoán sai, cho thấy hai phương pháp không có tập lỗi hoàn toàn giống nhau.

Kết quả này chưa chứng minh rằng kết hợp hai mô hình sẽ cải thiện chất lượng phân loại.

## 7. Hạn chế của phép so sánh thời gian

- Hai phép đo sử dụng những phương thức ghi nhận thời gian khác nhau.
- Chưa xác minh việc chạy trên cùng phần cứng, cùng tải hệ thống và cùng điều kiện thực thi.
- Thời gian Baseline không bao gồm chi phí huấn luyện và nạp mô hình.
- Thời gian LLM bao gồm lần gọi đầu có độ trễ cao.
- Chưa đo riêng thời gian tải mô hình Ollama.
- Chưa đo mức sử dụng RAM, CPU, GPU hoặc điện năng.
- Chưa thực hiện nhiều lần benchmark độc lập để xác định độ biến thiên.

Vì vậy, kết quả chỉ phản ánh thời gian xử lý trong các lần chạy đã ghi nhận.

## 8. Kết luận

Trong phạm vi phân loại tám nhóm IT Support Ticket trên tập test400, phương pháp TF-IDF + Logistic Regression có hiệu quả tổng thể vượt trội so với Qwen2.5:3B Zero-shot Prompt V3.

Baseline đạt Accuracy 85,75% và Macro F1 0,8611, trong khi LLM đạt Accuracy 41,00% và Macro F1 0,3729.

Thời gian dự đoán trung bình đã báo cáo của Baseline là 0,052 ms/ticket, còn LLM có thời gian xử lý trung bình khoảng 202,1 ms/ticket.

Các kết quả ủng hộ việc ưu tiên Baseline cho chức năng phân loại ticket tự động trong phạm vi dữ liệu và điều kiện thực nghiệm của nhóm.

Việc sử dụng LLM cho các chức năng hỗ trợ khác hoặc thiết kế mô hình kết hợp cần được nghiên cứu và đánh giá riêng.

## 9. File liên quan

- `src/train_baseline.py`
- `src/run_llm_batch.py`
- `results/baseline_report.txt`
- `results/llm_final_predictions_v3_400.csv`
- `results/baseline_llm_comparison_400.csv`
- `results/baseline_llm_efficiency_week3_day4.md`