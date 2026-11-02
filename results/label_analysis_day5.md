# Tuần 1 - Ngày 5: Phân tích phân bố nhãn trong tập dữ liệu huấn luyện

## 1. Mục tiêu

Phân tích phân bố các nhãn trong tập dữ liệu huấn luyện `train.csv`, đặc biệt tập trung vào nhóm HR Support, nhằm tìm hiểu đặc điểm dữ liệu và chuẩn bị cơ sở cải thiện Prompt V3 cho mô hình phân loại yêu cầu hỗ trợ IT bằng LLM.

## 2. Tổng quan dữ liệu

- Tập dữ liệu: `data/train.csv`
- Tổng số yêu cầu (ticket): 38.258
- Số yêu cầu thiếu nội dung: 0
- Số yêu cầu thiếu nhãn: 0
- Tổng số nhóm nhãn: 8

Kết quả cho thấy dữ liệu huấn luyện không có giá trị thiếu ở hai cột chính là `Document` và `Topic_group`.

## 3. Phân bố các nhóm nhãn

| Nhóm nhãn | Số lượng | Tỷ lệ (%) |
|---|---:|---:|
| Hardware | 10.889 | 28,46 |
| HR Support | 8.729 | 22,82 |
| Access | 5.699 | 14,90 |
| Miscellaneous | 5.646 | 14,76 |
| Storage | 2.222 | 5,81 |
| Purchase | 1.970 | 5,15 |
| Internal Project | 1.695 | 4,43 |
| Administrative rights | 1.408 | 3,68 |

### Nhận xét

- Hardware là nhóm có số lượng lớn nhất, chiếm 28,46%.
- HR Support đứng thứ hai với 8.729 yêu cầu, chiếm 22,82%.
- Administrative rights có số lượng thấp nhất, chiếm 3,68%.
- Dữ liệu có sự mất cân bằng giữa các nhóm nhãn.

Đặc biệt, HR Support là một trong những nhóm phổ biến nhất. Do đó, việc mô hình LLM phân loại sai nhóm này cần được nghiên cứu thêm, thay vì mặc định nguyên nhân là thiếu dữ liệu.

## 4. Phân tích nhóm HR Support

### 4.1. Thống kê độ dài yêu cầu

- Tổng số yêu cầu: 8.729
- Độ dài trung bình: 37,76 từ
- Trung vị: 24 từ
- Độ dài ngắn nhất: 3 từ
- Độ dài dài nhất: 817 từ

Kết quả cho thấy độ dài các yêu cầu HR Support khá đa dạng. Nhiều yêu cầu tương đối ngắn, trong khi một số yêu cầu có nội dung rất dài.

### 4.2. Phân tích nội dung mẫu

Sau khi quan sát 20 yêu cầu thuộc nhóm HR Support, có thể nhận thấy các nội dung thường liên quan đến:

- Nghỉ phép và quản lý ngày nghỉ.
- Chấm công và bảng thời gian làm việc.
- Cập nhật thông tin nhân viên.
- Tiếp nhận nhân viên mới.
- Quy trình phê duyệt nhân sự.
- Hệ thống Oracle phục vụ nghiệp vụ nhân sự.
- Các vấn đề truy cập liên quan đến quy trình nhân sự.

### 4.3. Nhận xét

Nhóm HR Support không chỉ bao gồm các yêu cầu nhân sự thông thường mà còn có thể bao gồm vấn đề kỹ thuật phát sinh trong quá trình sử dụng hệ thống phục vụ nghiệp vụ nhân sự.

Điều này có thể khiến mô hình nhầm lẫn giữa HR Support với Access, Miscellaneous hoặc các nhóm khác.

## 5. Những vấn đề cần cải thiện

Trong quá trình thử nghiệm Prompt V2 trên 10 yêu cầu, mô hình đạt độ chính xác 30%.

Đặc biệt, cả 4 yêu cầu thực tế thuộc HR Support trong mẫu thử đều bị phân loại sai.

Một số nguyên nhân có thể bao gồm:

1. Định nghĩa HR Support trong prompt chưa bao quát đầy đủ các nghiệp vụ nhân sự.
2. Mô hình có thể tập trung quá nhiều vào từ khóa kỹ thuật thay vì mục đích chính của yêu cầu.
3. Ranh giới giữa HR Support và Access chưa được mô tả đủ rõ.
4. Nội dung yêu cầu có thể chứa nhiều từ khóa thuộc các nhóm khác nhau.

Đây mới là những giả thuyết ban đầu vì số lượng mẫu thử còn nhỏ.

## 6. Đề xuất cải thiện Prompt V3

Dựa trên kết quả phân tích, đề xuất các hướng cải thiện sau:

1. Mở rộng định nghĩa HR Support, bao gồm nghỉ phép, chấm công, bảng lương, thông tin nhân viên và quy trình tiếp nhận nhân viên mới.
2. Bổ sung hướng dẫn phân biệt HR Support và Access.
3. Yêu cầu mô hình xác định mục đích nghiệp vụ chính của ticket.
4. Tránh phân loại chỉ dựa vào một vài từ khóa riêng lẻ.
5. Tiếp tục thử nghiệm và đánh giá trên tập dữ liệu có nhãn để kiểm tra hiệu quả cải thiện.

## 7. Kết luận

Quá trình phân tích cho thấy HR Support là nhóm nhãn lớn thứ hai trong tập dữ liệu huấn luyện, chiếm 22,82%.

Các mẫu dữ liệu cho thấy phạm vi HR Support khá rộng, bao gồm cả những yêu cầu liên quan đến hệ thống và ứng dụng phục vụ nghiệp vụ nhân sự.

Những kết quả này là cơ sở để xây dựng Prompt V3, hướng đến việc cải thiện khả năng phân biệt HR Support với các nhóm nhãn khác.

Hiệu quả thực tế của Prompt V3 cần được kiểm chứng thông qua các thử nghiệm tiếp theo.

## 8. Các file kết quả

- `src/analyze_labels.py`: Chương trình phân tích dữ liệu.
- `results/label_distribution.csv`: Thống kê phân bố nhãn.
- `results/ticket_length_stats.csv`: Thống kê độ dài ticket.
- `results/hr_support_samples.csv`: Các mẫu yêu cầu HR Support.
- `results/label_analysis_day5.md`: Báo cáo phân tích Ngày 5.
