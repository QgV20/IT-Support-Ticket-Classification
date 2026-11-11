# Tuần 3 — Ngày 3: So sánh Confusion Matrix của Baseline và LLM

## 1. Mục tiêu

Phân tích chất lượng phân loại của hai mô hình theo từng nhãn trên cùng tập kiểm thử gồm 400 IT Support Ticket.

Hai phương pháp được so sánh:

- Baseline: TF-IDF + Logistic Regression.
- LLM: Qwen2.5:3B Zero-shot, Prompt V3.

Nghiên cứu sử dụng Confusion Matrix để xác định các nhóm nhãn hoạt động tốt, những nhãn thường bị phân loại sai và các cặp nhãn dễ nhầm lẫn.

## 2. Dữ liệu và phương pháp

Tập kiểm thử: `data/test_sample.csv`, gồm 400 ticket thuộc tám nhóm nhãn.

Các kết quả sử dụng:

- `results/confusion_sample.png`: Confusion Matrix Baseline trên 400 ticket.
- `results/llm_confusion_final_v3_400.png`: Confusion Matrix LLM trên 400 ticket.
- `results/baseline_report.txt`: Classification Report Baseline.
- `results/llm_final_predictions_v3_400.csv`: Dự đoán của LLM.

Confusion Matrix của LLM có thêm một cột `__ERROR__` để ghi nhận trường hợp dự đoán không hợp lệ. Nhãn lỗi được tính là dự đoán sai.

## 3. Kết quả tổng thể

| Chỉ số | Baseline | LLM V3 |
|---|---:|---:|
| Accuracy | 85,75% | 41,00% |
| Macro F1 | 0,8611 | 0,3729 |
| Số dự đoán đúng | 343/400 | 164/400 |

Baseline vượt trội về cả Accuracy và Macro F1 trong điều kiện thực nghiệm hiện tại.

## 4. So sánh Recall theo từng nhãn

| Nhãn | Baseline | LLM V3 |
|---|---:|---:|
| Access | 79,7% | 50,8% |
| Administrative rights | 100,0% | 0,0% |
| HR Support | 83,5% | 56,0% |
| Hardware | 85,1% | 31,6% |
| Internal Project | 94,4% | 44,4% |
| Miscellaneous | 88,1% | 33,9% |
| Purchase | 81,0% | 71,4% |
| Storage | 95,7% | 17,4% |

Baseline có Recall cao hơn LLM ở cả tám nhóm nhãn.

Khoảng cách lớn nhất xuất hiện ở Administrative rights, Storage, Miscellaneous và Hardware.

## 5. Phân tích Confusion Matrix của Baseline

Baseline phân loại đúng 343/400 ticket.

Các nhóm có Recall cao gồm:

- Administrative rights: 15/15 ticket.
- Storage: 22/23 ticket.
- Internal Project: 17/18 ticket.
- Miscellaneous: 52/59 ticket.

Một số nhầm lẫn đáng chú ý:

- HR Support → Hardware: 7 ticket.
- Hardware → HR Support: 5 ticket.
- Hardware → Miscellaneous: 5 ticket.
- Access → Hardware: 4 ticket.

Baseline vẫn mắc lỗi, nhưng phần lớn dự đoán tập trung trên đường chéo chính của Confusion Matrix.

## 6. Phân tích Confusion Matrix của LLM V3

LLM phân loại đúng 164/400 ticket.

Các nhóm có Recall tương đối cao:

- Purchase: 15/21 ticket.
- HR Support: 51/91 ticket.
- Access: 30/59 ticket.

Các nhóm có Recall thấp:

- Administrative rights: 0/15 ticket.
- Storage: 4/23 ticket.
- Hardware: 36/114 ticket.
- Miscellaneous: 20/59 ticket.

Một trường hợp thuộc HR Support không được gán nhãn hợp lệ do mô hình trả về Security, nên được ghi vào cột `__ERROR__`.

## 7. Những cặp nhãn LLM thường nhầm lẫn

| Nhãn thực tế | Dự đoán sai | Số ticket |
|---|---|---:|
| Hardware | Miscellaneous | 46 |
| Access | Miscellaneous | 23 |
| HR Support | Access | 18 |
| Miscellaneous | HR Support | 18 |
| Hardware | Access | 17 |
| HR Support | Miscellaneous | 14 |
| Storage | Access | 11 |
| Internal Project | Miscellaneous | 8 |
| Administrative rights | Access | 6 |
| Miscellaneous | Access | 6 |

Các kết quả cho thấy LLM có xu hướng nhầm nhiều ticket thuộc các nhãn chuyên biệt sang Miscellaneous và Access.

Đặc biệt, 46/114 ticket Hardware bị dự đoán thành Miscellaneous.

## 8. Thảo luận

Kết quả cho thấy phương pháp TF-IDF + Logistic Regression được huấn luyện có giám sát nhận diện tám nhóm nhãn tốt hơn mô hình Qwen2.5:3B sử dụng Zero-shot Prompt V3.

Một giải thích có thể là Baseline đã học được các đặc điểm từ dữ liệu có nhãn, trong khi LLM phải dựa vào mô tả nhãn và nội dung ticket trong prompt.

Những nhãn phản ánh quy ước nghiệp vụ đặc thù như Administrative rights có thể khó nhận diện bằng Zero-shot nếu định nghĩa chung không phù hợp hoàn toàn với cách gán nhãn của dataset.

Tuy nhiên, đây là giả thuyết giải thích kết quả, không phải bằng chứng nhân quả về cơ chế dự đoán của mô hình.

## 9. Hạn chế

- Chỉ đánh giá một mô hình LLM Zero-shot với Prompt V3.
- Tập test400 có phân bố nhãn không cân bằng.
- Một số nhãn có ít mẫu, ví dụ Administrative rights chỉ có 15 ticket.
- Một phần dữ liệu test từng được quan sát trong giai đoạn phát triển prompt.
- Confusion Matrix chỉ cho biết phân bố lỗi, không tự giải thích nguyên nhân ngữ nghĩa.
- Chưa kiểm định kết quả trên nhiều lần chạy LLM.

## 10. Kết luận

Confusion Matrix cho thấy Baseline đạt hiệu quả tốt hơn LLM V3 ở cả tám nhóm nhãn trên tập test400.

Những nhầm lẫn đáng chú ý nhất của LLM gồm Hardware → Miscellaneous, Access → Miscellaneous, HR Support → Access và Storage → Access.

LLM đặc biệt gặp khó khăn với Administrative rights, Hardware và Storage.

Kết quả bổ sung bằng chứng cho kết luận rằng TF-IDF + Logistic Regression phù hợp hơn với bài toán phân loại ticket có nhãn trong thiết lập thực nghiệm hiện tại.

Các kết quả cũng giúp xác định những nhóm nhãn cần tập trung nếu nghiên cứu được mở rộng sang Few-shot, Fine-tuning hoặc các phương pháp kết hợp.

## 11. File liên quan

- `src/train_baseline.py`
- `src/analyze_final_confusion.py`
- `results/confusion_sample.png`
- `results/confusion_full.png`
- `results/llm_confusion_final_v3_400.png`
- `results/baseline_report.txt`
- `results/llm_final_predictions_v3_400.csv`