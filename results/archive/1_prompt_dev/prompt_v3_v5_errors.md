# Tuần 2 - Ngày 6: Phân tích chi tiết sự thay đổi giữa Prompt V3 và V5

## 1. Mục tiêu

Phân tích những thay đổi trong kết quả phân loại giữa Prompt V3 và Prompt V5 nhằm xác định các nhóm nhãn được cải thiện, những nhóm suy giảm và các nguyên nhân tiềm năng.

Đặc biệt, nghiên cứu tập trung giải thích vì sao Prompt V5 cải thiện Administrative rights Recall nhưng làm giảm Accuracy tổng thể.

## 2. Thiết lập thực nghiệm

- Mô hình: Qwen2.5:3B.
- Công cụ: Ollama.
- Phương pháp: Zero-shot Classification.
- Tập dữ liệu: validation160 gồm 160 ticket, cân bằng 20 ticket mỗi nhãn.
- Phiên bản so sánh: Prompt V3 và Prompt V5.
- Phương pháp: Ghép dự đoán theo ticket_id, đối chiếu đúng/sai và đọc nội dung các ticket thay đổi kết quả.

Kết quả được phân tích từ các file dự đoán đã lưu, không chạy lại mô hình.

## 3. Kết quả tổng thể

| Chỉ số | V3 | V5 |
|---|---:|---:|
| Accuracy | 48,75% | 40,00% |
| Macro F1 | 0,4616 | 0,4180 |
| Administrative rights Recall | 0% | 25% |
| HR Support Recall | 65% | 40% |
| Dự đoán đúng | 78/160 | 64/160 |
| Xử lý thành công | 160/160 | 160/160 |

Prompt V5 cải thiện Administrative rights Recall nhưng giảm Accuracy và Macro F1 so với V3.

## 4. Phân tích sự thay đổi theo từng ticket

| Trường hợp | Số ticket |
|---|---:|
| V3 và V5 dự đoán khác nhau | 68 |
| Cả hai đúng | 51 |
| Cả hai sai | 69 |
| V3 sai, V5 đúng | 13 |
| V3 đúng, V5 sai | 27 |

Số dự đoán đúng thay đổi ròng là 13 - 27 = -14 ticket.

Trong số 68 ticket đổi nhãn, có 28 ticket vẫn bị phân loại sai ở cả hai phiên bản.

## 5. Phân tích những ticket V5 sửa đúng

Trong 13 ticket được V5 sửa đúng:

- Administrative rights: 5 ticket.
- Miscellaneous: 8 ticket.

### 5.1. Administrative rights

Các ticket 2321, 12349, 27731, 31966 và 37998 được V5 phân loại đúng thành Administrative rights.

Những trường hợp này chủ yếu liên quan đến cài đặt Windows, nâng cấp hệ điều hành, cập nhật phần mềm hoặc tác vụ nâng cấp hệ thống.

Kết quả phù hợp với định hướng thiết kế V5 dựa trên nghiên cứu quy ước nhãn trong dữ liệu train.

### 5.2. Miscellaneous

Tám ticket Miscellaneous được V5 sửa đúng trước đó bị V3 phân loại thành Access, HR Support hoặc Internal Project.

Một số trường hợp liên quan đến báo cáo chi phí, phê duyệt hợp đồng, thông báo phê duyệt và các yêu cầu hành chính.

Kết quả cho thấy V5 nhận diện đúng thêm một số trường hợp thuộc Miscellaneous.

## 6. Phân tích những ticket V5 làm sai

Có 27 ticket V3 dự đoán đúng nhưng V5 dự đoán sai.

Đáng chú ý, cả 27 ticket đều được V5 chuyển thành Miscellaneous.

Phân bố theo nhãn thực tế:

| Nhãn | Số ticket suy giảm |
|---|---:|
| Access | 7 |
| Internal Project | 7 |
| HR Support | 5 |
| Purchase | 5 |
| Hardware | 2 |
| Storage | 1 |
| Tổng | 27 |

### 6.1. Access

Các ticket như 10049 và 28548 liên quan đến truy cập Confluence hoặc đổi mật khẩu nhưng bị V5 phân loại thành Miscellaneous.

### 6.2. Internal Project

Các ticket như 9893 và 37749 đề cập tạo hoặc đóng project code trên hệ thống PAS.

V5 không duy trì được khả năng nhận diện nhóm Internal Project ở một số trường hợp V3 đã phân loại đúng.

### 6.3. HR Support

Các ticket 1201 và 2646 liên quan đến contractor và quy trình nhân viên mới.

V5 chuyển những trường hợp này thành Miscellaneous, góp phần làm giảm HR Support Recall.

### 6.4. Purchase

Các ticket 22505 và 24812 liên quan đến purchase order, requisition và phân bổ sản phẩm đã mua nhưng bị V5 phân loại thành Miscellaneous.

### 6.5. Hardware và Storage

Một số ticket liên quan sự cố mạng hoặc shared mailbox cũng bị chuyển thành Miscellaneous.

## 7. So sánh Recall theo từng nhãn

| Nhãn | Recall V3 | Recall V5 | Thay đổi |
|---|---:|---:|---:|
| Access | 70% | 35% | -35 điểm % |
| Administrative rights | 0% | 25% | +25 điểm % |
| HR Support | 65% | 40% | -25 điểm % |
| Hardware | 55% | 45% | -10 điểm % |
| Internal Project | 50% | 15% | -35 điểm % |
| Miscellaneous | 50% | 90% | +40 điểm % |
| Purchase | 85% | 60% | -25 điểm % |
| Storage | 15% | 10% | -5 điểm % |

Prompt V5 cải thiện hai nhãn Administrative rights và Miscellaneous, nhưng làm giảm Recall của sáu nhãn còn lại.

## 8. Thảo luận

Phân tích chi tiết cho thấy V5 có xu hướng chuyển nhiều dự đoán sang Miscellaneous.

Xu hướng này giúp mô hình phân loại đúng thêm một số ticket Miscellaneous, nhưng đồng thời làm sai nhiều ticket vốn thuộc Access, HR Support, Internal Project và Purchase.

Các quy tắc bổ sung trong V5 có thể đã ảnh hưởng đến cách mô hình lựa chọn nhãn trên toàn bộ tập dữ liệu.

Tuy nhiên, đây chỉ là giả thuyết về cơ chế hoạt động. Cần thực hiện thêm các thử nghiệm có kiểm soát hoặc phân tích từng thành phần prompt để xác định nguyên nhân cụ thể.

## 9. Hạn chế

- Tập validation chỉ gồm 160 ticket.
- Mỗi nhãn có 20 ticket.
- Tập validation đã được sử dụng trong quá trình phát triển các prompt trước đó.
- Một số nội dung ticket được rút gọn khi hiển thị trong Terminal.
- Chưa đánh giá riêng tác động của từng quy tắc mới bằng thử nghiệm loại bỏ thành phần.
- Chưa kiểm tra độ ổn định của kết quả qua nhiều lần chạy.
- Kết quả chưa thể hiện hiệu quả tổng quát hóa trên tập test độc lập.

## 10. Kết luận

Prompt V5 cải thiện khả năng nhận diện Administrative rights, đạt Recall 25% so với 0% của V3.

Tuy nhiên, Prompt V5 làm giảm Accuracy từ 48,75% xuống 40,00% và Macro F1 từ 0,4616 xuống 0,4180.

Phân tích từng ticket cho thấy V5 sửa đúng 13 ticket nhưng làm sai 27 ticket. Tất cả 27 trường hợp suy giảm đều được chuyển sang Miscellaneous.

Vì vậy, Prompt V3 tiếp tục là phiên bản ưu tiên theo Accuracy và Macro F1 trên tập phát triển hiện tại.

Prompt V5 được giữ lại để ghi nhận kết quả nghiên cứu cải thiện Administrative rights và sự đánh đổi giữa các nhóm nhãn.

## 11. Các file liên quan

- `src/llm_classifier.py`
- `src/experiments/llm_classifier_v5.py`
- `src/compare_v3_v5.py`
- `results/llm_validation_predictions_v3.csv`
- `results/llm_validation_predictions_v5.csv`
- `results/llm_v3_v5_comparison.csv`
- `results/llm_v5_improved_cases.csv`
- `results/llm_v5_regressed_cases.csv`
- `results/llm_experiments/analysis/llm_v3_v5_label_summary.csv`