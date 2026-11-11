# Tuần 3 — Ngày 1: Phân tích so sánh Baseline và LLM theo từng ticket

## 1. Mục tiêu

So sánh kết quả dự đoán của hai phương pháp phân loại IT Support Ticket trên cùng tập kiểm thử gồm 400 ticket.

Hai phương pháp gồm:

- Baseline: TF-IDF + Logistic Regression.
- LLM: Qwen2.5:3B, Zero-shot Prompt V3.

Ngoài các chỉ số tổng thể, nghiên cứu tập trung phân tích những ticket mà hai mô hình đưa ra kết quả đúng/sai khác nhau, từ đó xác định những trường hợp LLM có thể bổ sung giá trị.

## 2. Dữ liệu và phương pháp

Tập dữ liệu sử dụng là `data/test_sample.csv`, gồm 400 ticket thuộc tám nhóm nhãn.

Dự đoán Baseline được xuất từ mô hình đã huấn luyện `baseline_tfidf_lr.joblib`. Kết quả đã được đối chiếu với chương trình tái tạo trước đó và trùng khớp 400/400 dự đoán.

Dự đoán LLM được lấy từ `llm_final_predictions_v3_400.csv`, không chạy lại Ollama.

Hai file dự đoán được đối chiếu theo thứ tự dòng, nội dung Document và nhãn Topic_group trước khi phân tích.

Một trường hợp LLM trả về nhãn không hợp lệ được tính là dự đoán sai.

## 3. Kết quả đánh giá tổng thể

| Chỉ số | Baseline | LLM Prompt V3 |
|---|---:|---:|
| Accuracy | 85,75% | 41,00% |
| Macro F1 | 0,8611 | 0,3729 |
| Dự đoán đúng | 343/400 | 164/400 |

Baseline đạt hiệu quả tổng thể cao hơn đáng kể so với LLM Zero-shot trong thiết lập thực nghiệm hiện tại.

## 4. So sánh đúng/sai theo từng ticket

| Trường hợp | Số ticket | Tỷ lệ |
|---|---:|---:|
| Cả hai dự đoán đúng | 152 | 38,00% |
| Chỉ Baseline đúng | 191 | 47,75% |
| Chỉ LLM đúng | 12 | 3,00% |
| Cả hai dự đoán sai | 45 | 11,25% |
| **Tổng** | **400** | **100%** |

Kiểm tra:

- Baseline đúng: 152 + 191 = 343 ticket.
- LLM đúng: 152 + 12 = 164 ticket.
- Chênh lệch số dự đoán đúng: 191 - 12 = 179 ticket.

Các số liệu nhất quán với Accuracy đã báo cáo.

## 5. Phân tích 12 ticket chỉ LLM đúng

Phân bố theo nhãn thực tế:

| Nhãn | Số ticket |
|---|---:|
| Access | 6 |
| HR Support | 3 |
| Hardware | 1 |
| Purchase | 1 |
| Miscellaneous | 1 |
| **Tổng** | **12** |

### 5.1. Nhóm Access

Các ticket 30, 34, 271, 320, 328 và 388 thuộc nhóm Access.

Trong đó, một số trường hợp có nội dung liên quan đến repository access, tài khoản, secure token, thay đổi mật khẩu và yêu cầu xác thực.

Baseline đã nhầm các trường hợp này sang Hardware, Miscellaneous, Internal Project hoặc Administrative rights.

LLM phân loại đúng cả sáu trường hợp theo nhãn thực tế.

Tuy nhiên, một số ticket như 271 và 320 có mô tả được hiển thị chưa đầy đủ, nên cần thận trọng khi giải thích nguyên nhân nhầm lẫn.

### 5.2. Nhóm HR Support

Ba ticket 73, 224 và 240 được LLM phân loại đúng thành HR Support.

Nội dung nhìn thấy liên quan đến lịch vắng mặt, timecard code và hồ sơ nghỉ phép.

Những chủ đề này phù hợp với phần mô tả nghiệp vụ nhân sự trong Prompt V3.

Kết quả gợi ý việc bổ sung ngữ cảnh nghiệp vụ trong prompt có thể hữu ích, nhưng chưa đủ để xác định tác động nhân quả của từng quy tắc.

### 5.3. Các nhóm còn lại

- Ticket 219: Hardware, có đề cập RAM và nhân viên mới.
- Ticket 279: Purchase, liên quan yêu cầu mua thiết bị.
- Ticket 380: Miscellaneous, liên quan vấn đề cài đặt Project Plan.

Trong ba trường hợp này, LLM dự đoán đúng nhãn thực tế, còn Baseline dự đoán sai.

## 6. Thảo luận về khả năng bổ sung của LLM

Trong 400 ticket, có 12 trường hợp LLM đúng nhưng Baseline sai, chiếm 3% tổng tập test và khoảng 21,1% trong 57 trường hợp Baseline dự đoán sai.

Điều này chứng minh rằng tập hợp các ticket được hai mô hình phân loại đúng không hoàn toàn giống nhau.

Tuy nhiên, Baseline phân loại đúng 191 ticket mà LLM dự đoán sai.

Do đó, kết quả chỉ cho thấy khả năng bổ sung trên một số trường hợp, chưa chứng minh được một hệ thống kết hợp Baseline và LLM sẽ cải thiện Accuracy thực tế.

Muốn đánh giá mô hình kết hợp, cần thiết kế quy tắc lựa chọn dự đoán mà không sử dụng nhãn thật của ticket kiểm thử.

## 7. Hạn chế

- Tập kiểm thử chỉ gồm 400 ticket.
- LLM sử dụng một mô hình và một phiên bản prompt đã lựa chọn.
- Một số ticket test từng được quan sát trong giai đoạn phát triển prompt.
- Phân tích nội dung 12 ticket mới dựa trên văn bản được rút gọn khi hiển thị trong Terminal.
- Chưa phân tích định tính đầy đủ 45 ticket cả hai mô hình cùng sai.
- Chưa thực hiện kiểm định thống kê cho sự khác biệt giữa hai mô hình.
- Chưa xây dựng hoặc đánh giá một phương pháp kết hợp thực tế.

## 8. Kết luận

Baseline TF-IDF + Logistic Regression vượt trội về Accuracy và Macro F1 so với Qwen2.5:3B Zero-shot Prompt V3 trên cùng 400 ticket.

Phân tích theo từng ticket cho thấy:

- 152 ticket cả hai mô hình cùng đúng.
- 191 ticket chỉ Baseline đúng.
- 12 ticket chỉ LLM đúng.
- 45 ticket cả hai cùng sai.

Mặc dù LLM có hiệu quả tổng thể thấp hơn, 12 trường hợp chỉ LLM đúng cho thấy sự khác biệt trong hành vi phân loại giữa hai phương pháp.

Kết quả này là cơ sở cho các phân tích lỗi tiếp theo, nhưng chưa đủ để khẳng định lợi ích của việc kết hợp hai mô hình.

## 9. Các file liên quan

- `src/train_baseline.py`
- `src/export_baseline_predictions.py`
- `src/compare_baseline_llm.py`
- `results/baseline_report.txt`
- `results/baseline_predictions_400.csv`
- `results/llm_final_predictions_v3_400.csv`
- `results/baseline_llm_comparison_400.csv`