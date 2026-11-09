# Tuần 2 - Ngày 4: Nghiên cứu quy ước gán nhãn Administrative rights

## 1. Mục tiêu

Khảo sát các ticket thuộc nhóm Administrative rights trong dữ liệu train nhằm tìm hiểu đặc điểm nội dung và các dấu hiệu có thể hỗ trợ phân loại.

Kết quả được sử dụng để định hướng thiết kế prompt trong giai đoạn tiếp theo.

## 2. Dữ liệu và phương pháp

- Nguồn dữ liệu: `data/train.csv`.
- Số ticket train ban đầu: 38.258.
- Số ticket còn lại sau khi loại các mẫu đã sử dụng và nội dung trùng khớp: 37.998.
- Số ticket Administrative rights được khảo sát: 1.378.
- Phương pháp: Tìm kiếm từ khóa bằng biểu thức chính quy, thống kê tỷ lệ theo nhãn và đọc mẫu định tính.

Chương trình loại trừ các ticket thuộc tập phát triển 80 mẫu, tập validation 160 mẫu và các nội dung trùng khớp với những tập được kiểm tra.

Một ticket có thể khớp nhiều chủ đề.

## 3. Thống kê Administrative rights

| Chủ đề | Số ticket | Tỷ lệ |
|---|---:|---:|
| Software / installation / application | 409 | 29,68% |
| Outlook / email | 389 | 28,23% |
| Windows upgrade | 321 | 23,29% |
| Server / restart | 158 | 11,47% |
| Printer / device | 136 | 9,87% |
| Storage / drive | 134 | 9,72% |
| Password / login | 90 | 6,53% |
| Administrator / privilege | 37 | 2,69% |

Đây là thống kê từ khóa, không phải kết quả phân loại chủ đề bằng mô hình.

## 4. So sánh Windows upgrade giữa các nhãn

| Nhãn | Số ticket khớp | Tỷ lệ |
|---|---:|---:|
| Administrative rights | 321 | 23,29% |
| Hardware | 94 | 0,87% |
| Access | 6 | 0,11% |
| Miscellaneous | 9 | 0,16% |

Chủ đề Windows upgrade có tỷ lệ xuất hiện cao hơn rõ rệt trong Administrative rights so với các nhãn Hardware và Access.

Điều này cho thấy Windows upgrade là một dấu hiệu đáng nghiên cứu khi phân biệt các nhóm nhãn trong dataset hiện tại.

## 5. Phân tích mẫu ticket Windows upgrade

Năm ticket được xem xét gồm:

- Ticket 20760: Lỗi task sequence khi nâng cấp Windows.
- Ticket 16704: Lỗi không thể thực hiện thay đổi trong quá trình nâng cấp.
- Ticket 23546: Lỗi cài đặt bản nâng cấp Windows.
- Ticket 731: Nâng cấp Windows thất bại, có thông tin liên quan phân vùng.
- Ticket 12286: Nâng cấp Windows thất bại và yêu cầu hỗ trợ.

Cả năm ticket đều liên quan trực tiếp đến quá trình nâng cấp hệ điều hành.

Tuy nhiên, phần nội dung quan sát được không cho thấy tất cả các ticket đều yêu cầu cấp quyền administrator.

## 6. Phân tích các ticket chứa từ khóa quản trị

Năm mẫu được xem xét gồm các ticket 25001, 20760, 7502, 31572 và 37729.

Một số trường hợp có từ administrator trong thông báo lỗi nâng cấp Windows. Ticket 7502 có từ admin trong tên thư mục Outlook.

Những ví dụ này cho thấy sự hiện diện của từ admin hoặc administrator không đủ để xác định bản chất yêu cầu là cấp quyền quản trị.

Một số nội dung bị cắt ngắn khi xuất ra Terminal, vì vậy chưa thể phân tích đầy đủ ngữ cảnh của tất cả các mẫu.

## 7. Nhận xét về quy ước nhãn

Từ kết quả khảo sát có thể hình thành giả thuyết rằng nhóm Administrative rights trong dataset bao gồm một số tác vụ triển khai hoặc bảo trì hệ thống, đặc biệt là nâng cấp Windows.

Điều này có thể khác với cách Prompt V2, V3 và V4 mô tả nhãn Administrative rights chủ yếu theo quyền quản trị và đặc quyền truy cập.

Tuy nhiên, chưa có tài liệu gán nhãn chính thức để xác nhận giả thuyết trên.

## 8. Hạn chế

- Biểu thức software_install bao gồm cả từ software và application nên có phạm vi khá rộng.
- Từ admin và administrator có thể xuất hiện trong ngữ cảnh không phải yêu cầu cấp quyền.
- Việc khớp từ khóa không xác định được mục đích chính của ticket.
- Các mẫu đọc thủ công có kích thước nhỏ và có thể trùng nhau giữa những chủ đề.
- Chưa loại được tất cả các trường hợp gần trùng hoặc cùng chuỗi hội thoại.
- Kết quả khảo sát train chưa đủ để khẳng định quy ước gán nhãn chính thức.

## 9. Kết luận

Kết quả cho thấy Windows upgrade là một chủ đề xuất hiện tương đối đặc trưng trong các ticket Administrative rights của dataset.

Trong khi đó, từ khóa admin hoặc administrator không nhất thiết thể hiện yêu cầu cấp quyền quản trị.

Các phát hiện trên cung cấp cơ sở để nghiên cứu cách mở rộng định nghĩa Administrative rights theo ngữ cảnh tác vụ hệ thống, thay vì chỉ dựa vào từ khóa đặc quyền.

Tuy nhiên, việc điều chỉnh prompt cần xem xét thêm các trường hợp đối chiếu ở những nhãn khác để hạn chế làm giảm Accuracy và Macro F1.

## 10. File liên quan

- `src/explore_admin_labels.py`
- `results/admin_topic_distribution.csv`
- `results/admin_train_topic_samples.csv`
- `results/admin_label_study_week2_day4.md`