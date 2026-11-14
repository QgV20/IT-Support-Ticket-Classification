# Tuần 2 - Ngày 5: Thiết kế và đánh giá Prompt V5

## 1. Mục tiêu

Thiết kế Prompt V5 nhằm cải thiện khả năng nhận diện nhóm Administrative rights trong bài toán phân loại IT Support Ticket bằng mô hình Qwen2.5:3B.

Prompt V5 được phát triển từ Prompt V3, dựa trên kết quả phân tích dữ liệu train và nghiên cứu các trường hợp nhầm lẫn giữa Administrative rights và Hardware.

## 2. Cơ sở thiết kế

Kết quả khảo sát dữ liệu train ở Ngày 4 cho thấy:

- Có 1.378 ticket Administrative rights được sử dụng để phân tích.
- Có 321 ticket, tương ứng 23,29%, khớp dấu hiệu Windows upgrade.
- Trong nhóm Hardware, tỷ lệ khớp dấu hiệu này là 0,87%.
- Các từ khóa admin hoặc administrator không phải lúc nào cũng thể hiện yêu cầu cấp quyền quản trị.

Phân tích các ví dụ cho thấy nhóm Administrative rights trong dataset có thể bao gồm những tác vụ nâng cấp, triển khai hoặc bảo trì hệ điều hành.

Từ đó, nhóm xây dựng Prompt V5 bằng cách mở rộng định nghĩa Administrative rights và bổ sung quy tắc phân biệt có điều kiện.

## 3. Thiết lập thực nghiệm

- Mô hình: Qwen2.5:3B.
- Công cụ: Ollama.
- Phương pháp: Zero-shot Classification.
- Phiên bản so sánh: Prompt V3 và Prompt V5.
- Tập dữ liệu: validation160, gồm 160 ticket, cân bằng 20 ticket mỗi nhóm nhãn.
- Chỉ số: Accuracy, Macro F1, HR Support Recall và Administrative rights Recall.
- Hai phiên bản được đánh giá trên cùng tập dữ liệu.

Tập validation160 đã được sử dụng trong quá trình phát triển các phiên bản prompt trước. Vì vậy, kết quả này chỉ phục vụ phân tích phát triển và không được coi là đánh giá độc lập cuối cùng.

## 4. Những thay đổi trong Prompt V5

Prompt V5 kế thừa các định nghĩa và quy tắc cơ bản từ Prompt V3, đồng thời bổ sung:

- Những tác vụ liên quan triển khai và bảo trì hệ điều hành vào phạm vi xem xét của Administrative rights.
- Các trường hợp Windows upgrade, Windows Update deployment, Software Center và task sequence failure.
- Quy tắc phân biệt sự cố thiết bị vật lý với yêu cầu nâng cấp hoặc triển khai hệ điều hành.
- Quy tắc tránh phân loại chỉ dựa trên từ administrator trong thông báo lỗi.
- Quy tắc giữ nguyên cách xử lý những nghiệp vụ HR như timecard, payroll, leave và onboarding.

Mục tiêu của các điều chỉnh là làm rõ cách phân biệt Administrative rights với những nhãn khác mà không dùng quy tắc từ khóa tuyệt đối.

## 5. Kết quả đánh giá tổng thể

| Chỉ số | Prompt V3 | Prompt V5 |
|---|---:|---:|
| Accuracy | 48,75% | 40,00% |
| Macro F1 | 0,4616 | 0,4180 |
| HR Support Recall | 65% | 40% |
| Administrative rights Recall | 0% | 25% |
| Số dự đoán đúng | 78/160 | 64/160 |
| Số ticket xử lý thành công | 160/160 | 160/160 |

Kết quả cho thấy Prompt V5 cải thiện khả năng nhận diện Administrative rights nhưng làm giảm Accuracy, Macro F1 và HR Support Recall so với V3.

## 6. Phân tích Administrative rights

Trong 20 ticket Administrative rights thuộc tập validation160, Prompt V5 cho kết quả:

| Nhãn dự đoán | Số ticket |
|---|---:|
| Administrative rights | 5 |
| Miscellaneous | 7 |
| Storage | 5 |
| Hardware | 3 |
| **Tổng** | **20** |

Prompt V5 dự đoán đúng 5/20 ticket, đạt Recall 25%.

Trong khi đó, Prompt V3 không dự đoán đúng ticket Administrative rights nào trong cùng tập dữ liệu.

Điều này cung cấp bằng chứng bước đầu rằng việc bổ sung ngữ cảnh nâng cấp Windows và tác vụ hệ thống có thể hỗ trợ nhận diện nhóm Administrative rights.

Tuy nhiên, 15/20 ticket vẫn bị phân loại sai, chủ yếu thành Miscellaneous, Storage hoặc Hardware.

## 7. Phân tích sự đánh đổi

So với Prompt V3:

- Accuracy của V5 giảm 8,75 điểm phần trăm.
- Macro F1 giảm 0,0436.
- HR Support Recall giảm 25 điểm phần trăm.
- Administrative rights Recall tăng 25 điểm phần trăm.
- Tổng số dự đoán đúng giảm 14 ticket.

Việc mở rộng phạm vi Administrative rights chưa bảo đảm cải thiện hiệu quả tổng thể.

Một giả thuyết là các quy tắc bổ sung đã ảnh hưởng đến cách mô hình lựa chọn giữa những nhóm nhãn có nội dung chồng lấn. Tuy nhiên, cần phân tích những ticket thay đổi dự đoán để xác định nguyên nhân cụ thể.

## 8. Hạn chế

- Tập validation chỉ có 160 ticket, mỗi nhãn 20 ticket.
- Tập validation được lấy từ train.csv và đã được xem xét trong quá trình phát triển prompt.
- Kết quả chưa phản ánh khả năng tổng quát hóa trên tập test độc lập.
- Những phân tích theo từ khóa từ dữ liệu train chưa chứng minh được quy ước gán nhãn chính thức.
- Thực nghiệm mới dựa trên một lần chạy mỗi phiên bản trong điều kiện hiện tại.
- Chưa có phân tích chi tiết những ticket V5 sửa đúng hoặc làm sai so với V3.

## 9. Kết luận

Prompt V5 đạt mục tiêu cải thiện một phần khả năng nhận diện Administrative rights, nâng Recall của nhóm này từ 0% lên 25% trên tập validation160.

Tuy nhiên, hiệu quả phân loại tổng thể của V5 thấp hơn V3.

Do đó, Prompt V3 tiếp tục là phiên bản ưu tiên nếu mục tiêu lựa chọn là Accuracy và Macro F1 trên tập phát triển hiện tại.

Prompt V5 được giữ lại như một kết quả thực nghiệm nhằm nghiên cứu tác động của việc mở rộng quy tắc gán nhãn Administrative rights.

Trong giai đoạn tiếp theo, nhóm cần kiểm tra những dự đoán thay đổi giữa V3 và V5, đồng thời chuẩn bị đánh giá cuối cùng trên dữ liệu kiểm thử tách biệt.

## 10. Các file liên quan

- `src/experiments/compare_windows_labels.py`
- `src/experiments/llm_classifier_v5.py`
- `src/experiments/evaluate_dev.py`
- `results/llm_validation_predictions_v3.csv`
- `results/llm_validation_predictions_v5.csv`
- `results/prompt_v5.md`