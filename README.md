# Research Summary — Generative AI for IT Support Ticket Classification

## 1. Thông tin bài báo nghiên cứu

**Tên bài báo:** Generative AI Implementation in Enterprises: Lessons From a Case Study of Enhanced IT Service Management

**Tác giả:** Ashish Jagdish Sharma, Bhawana Rathore, Baidyanath Biswas, Xiao Xiao và Rohit Gupta.

**Năm công bố:** 2026

**Tạp chí:** Information Systems Journal

**DOI:** https://doi.org/10.1111/isj.70029

**Bối cảnh nghiên cứu:** Ứng dụng Generative AI (GenAI) trong hoạt động quản lý dịch vụ công nghệ thông tin (IT Service Management — ITSM) tại doanh nghiệp Apollo Tyres Limited.

## 2. Tổng quan nội dung nghiên cứu

Bài báo nghiên cứu quá trình triển khai Generative AI trong môi trường doanh nghiệp nhằm cải thiện các hoạt động quản lý dịch vụ CNTT.

Nghiên cứu phân tích cách doanh nghiệp ứng dụng GenAI, những năng lực công nghệ và tổ chức được hình thành, cũng như các bài học từ quá trình triển khai.

Các hướng ứng dụng chính bao gồm:

1. **Quản lý tương tác người dùng:** ứng dụng GenAI để cải thiện quá trình tiếp nhận và phản hồi yêu cầu hỗ trợ.
2. **Quản lý sự cố CNTT:** hỗ trợ phân tích, phân loại, ưu tiên và xử lý các sự cố IT.
3. **Quản lý tài sản CNTT:** hỗ trợ quản lý và phân tích thông tin về tài sản công nghệ.
4. **Phân tích dữ liệu vận hành:** khai thác dữ liệu ITSM để hỗ trợ hoạt động quản lý và ra quyết định.

Trong đó, nhóm lựa chọn tập trung nghiên cứu ứng dụng AI trong phân loại phiếu yêu cầu hỗ trợ CNTT.

## 3. Cơ sở lựa chọn hướng thực nghiệm

Trong hoạt động IT Service Management, người dùng thường gửi các phiếu yêu cầu (ticket) để báo cáo sự cố hoặc yêu cầu hỗ trợ kỹ thuật.

Các ticket có thể chứa mô tả bằng ngôn ngữ tự nhiên với nội dung, độ dài và cách diễn đạt khác nhau.

Việc phân loại ticket thủ công có thể tiêu tốn thời gian và phụ thuộc vào kinh nghiệm của nhân viên hỗ trợ.

Trong phần nghiên cứu về quản lý sự cố, bài báo đề cập đến khả năng ứng dụng GenAI để phân tích nội dung mô tả, hỗ trợ phân loại và điều phối yêu cầu.

Từ cơ sở đó, nhóm lựa chọn thực nghiệm bài toán **IT Support Ticket Category Classification**.

Mục tiêu là đánh giá khả năng phân loại yêu cầu IT của mô hình ngôn ngữ lớn (Large Language Model — LLM), đồng thời so sánh với phương pháp Machine Learning truyền thống.

Thực nghiệm này chỉ tập trung vào một chức năng liên quan đến bài báo, không nhằm tái tạo toàn bộ giải pháp ITSM được triển khai tại Apollo Tyres Limited.

## 4. Mục tiêu và câu hỏi nghiên cứu

### 4.1. Mục tiêu

- Xây dựng mô hình phân loại phiếu yêu cầu IT dựa trên nội dung văn bản.
- Thử nghiệm phương pháp Machine Learning truyền thống và phương pháp GenAI.
- Đánh giá hiệu quả dự đoán của các phương pháp trên cùng tập dữ liệu kiểm thử.
- Phân tích ưu điểm, hạn chế và khả năng ứng dụng của GenAI trong phân loại ticket.

### 4.2. Câu hỏi nghiên cứu

**RQ1:** Mô hình LLM có thể phân loại các phiếu yêu cầu hỗ trợ CNTT dựa trên mô tả văn bản với hiệu quả như thế nào?

**RQ2:** Hiệu quả phân loại của LLM khác biệt ra sao so với phương pháp TF-IDF kết hợp Logistic Regression?

**RQ3:** Những loại yêu cầu nào thường bị phân loại sai và những yếu tố nào có thể ảnh hưởng đến kết quả dự đoán?

## 5. Dataset sử dụng trong thực nghiệm

### 5.1. Nguồn dữ liệu

Nhóm sử dụng dataset các phiếu yêu cầu hỗ trợ CNTT được lưu trữ trong thư mục `data/` của GitHub repository.

Các file hiện có:

- `all_tickets_processed_improved_...`: file dữ liệu gốc hoặc dữ liệu đã xử lý, cần xác nhận tên đầy đủ và vai trò.
- `train.csv`: tập dữ liệu huấn luyện.
- `test.csv`: tập dữ liệu kiểm thử.
- `test_sample.csv`: tập mẫu kiểm thử.

Việc phân chia dữ liệu do Thành viên 1 phụ trách và cần được kiểm tra để đảm bảo không có rò rỉ dữ liệu giữa các tập.

### 5.2. Cấu trúc dữ liệu

Dựa trên file `test_sample.csv` đã được kiểm tra:

| Thuộc tính | Mô tả | Vai trò |
|---|---|---|
| Document | Nội dung văn bản mô tả yêu cầu hỗ trợ IT | Biến đầu vào |
| Topic_group | Nhãn thể hiện loại yêu cầu | Biến mục tiêu |

Thông tin thống kê của `test_sample.csv`:

- Tổng số bản ghi: 400.
- Số cột: 2.
- Số lớp phân loại: 8.
- Số giá trị thiếu: 0.

### 5.3. Phân bố các loại yêu cầu

| Loại yêu cầu | Số lượng mẫu |
|---|---:|
| Hardware | 114 |
| HR Support | 91 |
| Access | 59 |
| Miscellaneous | 59 |
| Storage | 23 |
| Purchase | 21 |
| Internal Project | 18 |
| Administrative rights | 15 |
| **Tổng cộng** | **400** |

Dữ liệu có sự chênh lệch về số lượng mẫu giữa các lớp. Do đó, việc đánh giá không nên chỉ dựa vào Accuracy mà cần sử dụng thêm Macro F1-score.

Các thống kê trên chỉ phản ánh file `test_sample.csv`, không đại diện cho toàn bộ dataset.

## 6. Phương pháp thực nghiệm đề xuất

Nhóm dự kiến triển khai hai phương pháp.

### 6.1. Phương pháp 1 — Machine Learning Baseline

**Phụ trách:** Thành viên 1.

Sử dụng TF-IDF để biểu diễn nội dung văn bản dưới dạng vector đặc trưng.

Sau đó, mô hình Logistic Regression được huấn luyện để dự đoán nhãn `Topic_group`.

Quy trình:

1. Đọc dữ liệu huấn luyện.
2. Tiền xử lý văn bản.
3. Trích xuất đặc trưng TF-IDF.
4. Huấn luyện Logistic Regression.
5. Dự đoán trên tập kiểm thử.
6. Đánh giá kết quả.

### 6.2. Phương pháp 2 — Generative AI / LLM

**Phụ trách:** Thành viên 2.

Sử dụng mô hình ngôn ngữ lớn thông qua Ollama để thực hiện phân loại văn bản theo phương pháp Zero-shot Classification.

Mô hình nhận hai thành phần đầu vào:

- Nội dung mô tả ticket từ cột `Document`.
- Danh sách tám nhãn phân loại hợp lệ từ cột `Topic_group`.

Mô hình được yêu cầu chọn đúng một nhãn và trả về kết quả có cấu trúc.

Ví dụ minh họa:

**Input:** "Please create a new user account for an employee."

**Predicted category:** Access

Nhãn trên chỉ mang tính minh họa, không phải kết quả thực nghiệm đã được kiểm chứng.

Phương pháp zero-shot không yêu cầu huấn luyện lại trọng số LLM trên dataset của nhóm.

### 6.3. Thiết kế so sánh

Để đảm bảo tính công bằng:

- Hai phương pháp sử dụng cùng tập kiểm thử.
- Sử dụng cùng danh sách nhãn hợp lệ.
- Không sử dụng nhãn thật của ticket kiểm thử làm thông tin đầu vào cho mô hình.
- Ghi lại cấu hình mô hình, prompt và các tham số suy luận.
- Đánh giá bằng cùng các chỉ số.
- Phân tích riêng các dự đoán không hợp lệ hoặc bị lỗi.

Việc điều chỉnh prompt và lựa chọn cấu hình cần được thực hiện trước khi đánh giá cuối cùng, sử dụng dữ liệu phát triển riêng nếu cần.

## 7. Chỉ số đánh giá

Nhóm dự kiến sử dụng các chỉ số:

**Accuracy:** tỷ lệ dự đoán chính xác trên tổng số ticket được đánh giá.

**Precision:** đo mức độ chính xác của các dự đoán thuộc từng lớp.

**Recall:** đo khả năng phát hiện các mẫu thực tế thuộc từng lớp.

**Macro F1-score:** trung bình F1-score của các lớp, giúp đánh giá hiệu quả khi dữ liệu có sự mất cân bằng.

**Confusion Matrix:** thể hiện sự nhầm lẫn giữa các loại yêu cầu.

**Inference Time:** thời gian cần thiết để mô hình đưa ra dự đoán.

Các chỉ số này sẽ được tính từ kết quả thực nghiệm thực tế, không sử dụng số liệu giả định.

## 8. Mối liên hệ với bài báo gốc

Bài báo gốc nghiên cứu ứng dụng Generative AI trong môi trường IT Service Management, bao gồm việc hỗ trợ phân loại và xử lý sự cố IT.

Thực nghiệm của nhóm tập trung vào chức năng phân loại ticket dựa trên mô tả văn bản.

Điểm tương đồng là cả hai đều quan tâm đến khả năng ứng dụng AI để hỗ trợ quá trình tiếp nhận và quản lý yêu cầu CNTT.

Tuy nhiên, hai nghiên cứu khác nhau về phạm vi:

- Bài báo gốc nghiên cứu quá trình triển khai GenAI trong môi trường doanh nghiệp thực tế.
- Thực nghiệm của nhóm đánh giá các phương pháp phân loại trên một dataset có sẵn.
- Nhóm không triển khai hệ thống ITSM hoàn chỉnh.
- Nhóm không đo lường hiệu quả vận hành thực tế như thời gian giải quyết sự cố hay mức độ hài lòng của người dùng.

Do đó, thực nghiệm được xem là một nghiên cứu ứng dụng kỹ thuật có liên quan đến bài báo, không phải sự tái tạo đầy đủ nghiên cứu gốc.

## 9. Giới hạn nghiên cứu

- Thực nghiệm chưa được triển khai trong hệ thống ITSM thực tế.
- Chất lượng mô hình phụ thuộc vào dữ liệu và nhãn được cung cấp.
- Các lớp có ít mẫu có thể gây khó khăn trong đánh giá.
- Hiệu quả LLM có thể thay đổi theo mô hình, prompt và cấu hình suy luận.
- Thời gian suy luận phụ thuộc vào phần cứng và môi trường chạy.
- Kết quả trên dataset không đủ để kết luận rằng thời gian xử lý sự cố trong doanh nghiệp sẽ giảm.

## 10. Kết quả kỳ vọng

Sau khi hoàn thành, nhóm dự kiến có:

1. Mô hình Machine Learning baseline.
2. Module phân loại ticket bằng LLM.
3. Kết quả dự đoán của hai phương pháp.
4. Bảng so sánh các chỉ số đánh giá.
5. Phân tích những trường hợp dự đoán sai.
6. Báo cáo thực nghiệm và thảo luận về khả năng ứng dụng GenAI trong ITSM.

Các nội dung trên là kết quả kỳ vọng, chưa phải kết quả đã đạt được.

## 11. Tài liệu tham khảo

Sharma, A. J., Rathore, B., Biswas, B., Xiao, X., & Gupta, R. (2026). *Generative AI Implementation in Enterprises: Lessons From a Case Study of Enhanced IT Service Management*. Information Systems Journal. https://doi.org/10.1111/isj.70029
