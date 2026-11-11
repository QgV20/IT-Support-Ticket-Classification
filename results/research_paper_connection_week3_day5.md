# Tuần 3 — Ngày 5: Liên hệ thực nghiệm phân loại IT Support Ticket với nghiên cứu ứng dụng Generative AI trong ITSM

## 1. Mục tiêu

Báo cáo phân tích mối liên hệ giữa bài báo *Generative AI Implementation in Enterprises: Lessons From a Case Study of Enhanced IT Service Management* của Sharma và cộng sự (2026) với thực nghiệm phân loại IT Support Ticket của nhóm.

Mục tiêu gồm:

- Xác định cơ sở khoa học cho việc lựa chọn bài toán phân loại ticket.
- So sánh phạm vi và phương pháp nghiên cứu.
- Thảo luận các kết quả thực nghiệm trong bối cảnh ứng dụng GenAI vào ITSM.
- Trả lời các câu hỏi nghiên cứu RQ1, RQ2 và RQ3.
- Đề xuất những bài học về công nghệ, dữ liệu và quản lý hệ thống thông tin.

## 2. Tổng quan bài báo gốc

### 2.1. Thông tin nghiên cứu

- Tên bài báo: Generative AI Implementation in Enterprises: Lessons From a Case Study of Enhanced IT Service Management.
- Tác giả: Ashish Jagdish Sharma, Bhawana Rathore, Baidyanath Biswas, Xiao Xiao và Rohit Gupta.
- Năm: 2026.
- Tạp chí: Information Systems Journal.
- DOI: https://doi.org/10.1111/isj.70029.

### 2.2. Bối cảnh

Bài báo nghiên cứu việc triển khai Generative AI tại Apollo Tyres Limited trong hoạt động quản lý dịch vụ CNTT.

Nghiên cứu không chỉ xem xét năng lực của mô hình AI mà còn phân tích cách doanh nghiệp tổ chức, tích hợp và vận hành công nghệ trong môi trường thực tế.

### 2.3. Bốn năng lực GenAI trong ITSM

Nghiên cứu trình bày bốn nhóm năng lực chính:

1. Cải thiện quản lý tương tác với người dùng, bao gồm xử lý các rào cản ngôn ngữ.
2. Hỗ trợ quản lý sự cố và yêu cầu thay đổi, bao gồm phân loại và xử lý yêu cầu.
3. Hỗ trợ quản lý tài sản CNTT bằng các khả năng phân tích và dự báo.
4. Phân tích dữ liệu vận hành để hỗ trợ tri thức và ra quyết định.

Trong đó, nhóm lựa chọn nghiên cứu chức năng phân loại yêu cầu hỗ trợ CNTT dựa trên nội dung văn bản.

## 3. Mối liên hệ với bài toán của nhóm

### 3.1. Cơ sở lựa chọn bài toán

Trong hệ thống ITSM, người dùng tạo các ticket để báo cáo sự cố hoặc yêu cầu hỗ trợ.

Việc phân loại ticket giúp xác định loại yêu cầu, từ đó hỗ trợ quá trình tiếp nhận và chuyển tiếp đến bộ phận phù hợp.

Bài báo gốc đề cập đến việc sử dụng GenAI để hỗ trợ quản lý sự cố, trong đó có phân loại yêu cầu dựa trên nội dung văn bản.

Từ hướng ứng dụng này, nhóm lựa chọn bài toán IT Support Ticket Classification.

### 3.2. Phạm vi thực nghiệm

Nhóm xây dựng và so sánh hai phương pháp:

- TF-IDF + Logistic Regression: phương pháp học máy có giám sát.
- Qwen2.5:3B Zero-shot: phương pháp sử dụng mô hình ngôn ngữ thông qua Ollama và Prompt Engineering.

Tập dữ liệu gồm tám nhãn:

- Hardware.
- HR Support.
- Access.
- Miscellaneous.
- Storage.
- Purchase.
- Internal Project.
- Administrative rights.

Nghiên cứu của nhóm chỉ đánh giá khả năng dự đoán nhãn ticket, không xây dựng một hệ thống ITSM hoàn chỉnh.

## 4. Khác biệt về phương pháp nghiên cứu

| Tiêu chí | Bài báo gốc | Thực nghiệm của nhóm |
|---|---|---|
| Phương pháp | Nghiên cứu trường hợp doanh nghiệp | Thực nghiệm phân loại văn bản |
| Môi trường | Hệ thống ITSM thực tế | Dữ liệu có sẵn và môi trường Python |
| Đối tượng đánh giá | Năng lực ứng dụng GenAI trong tổ chức | Chất lượng dự đoán nhãn ticket |
| Công nghệ | GenAI tích hợp với quy trình và công cụ doanh nghiệp | TF-IDF + Logistic Regression, Qwen2.5:3B |
| Chỉ số | Hiệu quả vận hành và triển khai | Accuracy, Macro F1, Recall, thời gian dự đoán |
| Phạm vi kết luận | Bối cảnh triển khai tại Apollo Tyres | Bài toán tám nhãn trên dataset của nhóm |

Bài báo gốc nghiên cứu GenAI như một thành phần trong hệ thống thông tin của doanh nghiệp, còn nhóm chủ yếu đánh giá một chức năng kỹ thuật có liên quan.

Vì vậy, kết quả của nhóm không được diễn giải thành kết luận về hiệu quả tổng thể của GenAI trong ITSM.

## 5. Kết quả thực nghiệm của nhóm

### 5.1. Kết quả phân loại

Trên cùng tập test_sample.csv gồm 400 ticket:

| Chỉ số | Baseline | LLM V3 |
|---|---:|---:|
| Accuracy | 85,75% | 41,00% |
| Macro F1 | 0,8611 | 0,3729 |
| Số dự đoán đúng | 343 | 164 |

Baseline đạt kết quả cao hơn trên cả Accuracy và Macro F1.

LLM Zero-shot chưa đạt hiệu quả tương đương phương pháp được huấn luyện bằng dữ liệu có nhãn.

### 5.2. Kết quả phân tích từng ticket

| Trường hợp | Số ticket |
|---|---:|
| Cả hai đúng | 152 |
| Chỉ Baseline đúng | 191 |
| Chỉ LLM đúng | 12 |
| Cả hai sai | 45 |

Kết quả cho thấy hai phương pháp không mắc lỗi hoàn toàn giống nhau.

Trong đó, LLM nhận diện đúng 12 trường hợp mà Baseline dự đoán sai.

Tuy nhiên, số trường hợp chỉ Baseline đúng lớn hơn đáng kể, nên kết quả không chứng minh rằng LLM có thể thay thế Baseline.

### 5.3. Các nhãn gây khó khăn cho LLM

Những kết quả nổi bật:

- Administrative rights: Recall 0%.
- Storage: Recall khoảng 17,4%.
- Hardware: Recall khoảng 31,6%.
- Miscellaneous: Recall khoảng 33,9%.

Một số cặp nhầm lẫn đáng chú ý:

- Hardware → Miscellaneous: 46 ticket.
- Access → Miscellaneous: 23 ticket.
- HR Support → Access: 18 ticket.
- Miscellaneous → HR Support: 18 ticket.
- Storage → Access: 11 ticket.

Điều này cho thấy các nhãn có nội dung chồng lấn hoặc mang quy ước đặc thù có thể gây khó khăn cho mô hình Zero-shot.

### 5.4. Thời gian dự đoán

- Baseline: 0,052 ms/ticket theo báo cáo gốc.
- LLM: khoảng 202,1 ms/ticket.
- LLM xử lý hợp lệ: 399/400 ticket.

Hai phép đo thời gian có phương pháp và điều kiện thực thi khác nhau, nên chỉ được sử dụng như bằng chứng mô tả, không phải benchmark phần cứng được kiểm soát.

## 6. Trả lời các câu hỏi nghiên cứu

### RQ1: Mô hình LLM có thể phân loại các phiếu yêu cầu hỗ trợ CNTT dựa trên mô tả văn bản với hiệu quả như thế nào?

Qwen2.5:3B Zero-shot Prompt V3 đạt Accuracy 41,00% và Macro F1 0,3729 trên tập test400.

Mô hình nhận diện tương đối tốt nhóm Purchase nhưng gặp khó khăn với Administrative rights, Hardware và Storage.

Điều này cho thấy LLM có khả năng thực hiện phân loại Zero-shot, nhưng chất lượng chưa đủ cao để được xem là phương án phân loại tự động đáng tin cậy trong thiết lập hiện tại.

### RQ2: Hiệu quả phân loại của LLM khác biệt ra sao so với TF-IDF kết hợp Logistic Regression?

Baseline đạt Accuracy 85,75% và Macro F1 0,8611, cao hơn LLM lần lượt 44,75 điểm phần trăm Accuracy và 0,4882 Macro F1.

Baseline cũng đạt Recall cao hơn ở cả tám nhóm nhãn.

Trong điều kiện thực nghiệm của nhóm, phương pháp học máy có giám sát hiệu quả hơn phương pháp LLM Zero-shot.

Kết quả này không chứng minh rằng mọi mô hình LLM đều kém hơn các phương pháp học máy truyền thống.

### RQ3: Những loại yêu cầu nào thường bị phân loại sai và những yếu tố nào có thể ảnh hưởng đến kết quả dự đoán?

LLM thường nhầm Hardware thành Miscellaneous, Storage thành Access và một số nghiệp vụ HR Support thành Access hoặc Miscellaneous.

Các yếu tố có thể liên quan gồm:

- Nội dung ticket mơ hồ hoặc thiếu thông tin.
- Các nhóm nhãn có phạm vi nghiệp vụ chồng lấn.
- Quy ước gán nhãn đặc thù của dataset.
- Sự khác biệt giữa kiến thức tổng quát của LLM và cách phân loại trong dữ liệu.
- Khả năng Prompt Engineering ảnh hưởng đến mức ưu tiên của các nhãn.

Đây là các hướng giải thích được gợi ý từ phân tích lỗi, chưa phải kết luận nhân quả đã được kiểm chứng độc lập.

## 7. Thảo luận dưới góc nhìn Cơ sở hệ thống thông tin

### 7.1. Công nghệ phải phù hợp với bài toán

Kết quả cho thấy lựa chọn công nghệ cần dựa trên mục tiêu của hệ thống thông tin.

Với bài toán phân loại tám nhóm ticket có dữ liệu huấn luyện, Baseline mang lại hiệu quả tốt hơn trong điều kiện được đánh giá.

Việc sử dụng công nghệ mới không mặc nhiên tạo ra hiệu quả cao hơn một giải pháp đơn giản và phù hợp với dữ liệu.

### 7.2. Dữ liệu và quy ước nghiệp vụ có vai trò quan trọng

Các nhóm như Administrative rights có thể chứa những yêu cầu không dễ nhận biết chỉ từ nghĩa thông thường của tên nhãn.

Điều này nhấn mạnh vai trò của dữ liệu có nhãn, định nghĩa nghiệp vụ và sự phối hợp giữa người hiểu quy trình với người phát triển công nghệ.

### 7.3. GenAI cần được đánh giá như một thành phần hệ thống

Bài báo gốc mô tả GenAI được tích hợp với quy trình ITSM, cơ chế hỗ trợ quyết định, nguồn tri thức và hoạt động vận hành doanh nghiệp.

Đối với nhóm, hiệu quả của mô hình phân loại chỉ là một khía cạnh.

Nếu triển khai thực tế, còn cần xem xét độ tin cậy, xử lý lỗi, khả năng kiểm toán, quyền riêng tư và cơ chế chuyển những trường hợp không chắc chắn cho nhân viên hỗ trợ.

### 7.4. Triển khai có kiểm soát

Kết quả hiện tại không ủng hộ việc thay thế hoàn toàn Baseline bằng LLM Zero-shot.

Một hướng nghiên cứu tiếp theo có thể là triển khai thử nghiệm hệ thống hỗ trợ, trong đó phương pháp phân loại chính được lựa chọn dựa trên dữ liệu và hiệu quả đã xác minh.

Các phương pháp kết hợp, Few-shot hoặc RAG có thể được nghiên cứu thêm, nhưng không được coi là giải pháp đã chứng minh hiệu quả khi chưa có thực nghiệm riêng.

## 8. Bài học rút ra từ nghiên cứu gốc

Nghiên cứu của Sharma và cộng sự trình bày bảy bài học triển khai GenAI, gồm:

1. Lựa chọn trường hợp sử dụng cụ thể theo nghiệp vụ.
2. Chú trọng khác biệt ngôn ngữ và văn hóa.
3. Phát triển năng lực GenAI của nhân sự.
4. Thiết lập cơ chế phản hồi và cải tiến.
5. Đồng thiết kế quy trình với nhiều nhóm chuyên môn.
6. Triển khai theo từng giai đoạn có kiểm soát.
7. Bảo đảm nhân sự chuyên môn và năng lực tổ chức để mở rộng hệ thống.

Đối chiếu với thực nghiệm của nhóm, các bài học liên quan trực tiếp nhất là lựa chọn use case phù hợp, hiểu quy ước nghiệp vụ, thực hiện phản hồi từ phân tích lỗi và đánh giá có kiểm soát trước khi triển khai rộng.

Nhóm chưa đánh giá các vấn đề như đa ngôn ngữ, đào tạo nhân sự hay quản trị vận hành tại doanh nghiệp.

## 9. Giới hạn khi liên hệ hai nghiên cứu

- Bài báo nghiên cứu một triển khai GenAI thực tế tại doanh nghiệp.
- Nhóm thực nghiệm trên dataset có sẵn, không triển khai trong IT Service Desk đang hoạt động.
- Bài báo đánh giá những khía cạnh vận hành rộng hơn chất lượng phân loại.
- Nhóm không đo thời gian giải quyết sự cố thực tế, mức độ hài lòng người dùng hoặc chi phí vận hành.
- Nhóm sử dụng Qwen2.5:3B Zero-shot; đây không phải công nghệ hay kiến trúc đầy đủ được triển khai trong nghiên cứu gốc.
- Không thể so sánh trực tiếp Accuracy của nhóm với mức cải thiện thời gian giải quyết sự cố trong bài báo.

## 10. Kết luận

Bài báo gốc cung cấp cơ sở khoa học cho việc nghiên cứu ứng dụng GenAI vào hoạt động ITSM, trong đó phân loại ticket là một chức năng có liên quan.

Thực nghiệm của nhóm cho thấy Qwen2.5:3B Zero-shot có thể dự đoán nhãn ticket nhưng đạt hiệu quả thấp hơn đáng kể so với TF-IDF + Logistic Regression trên dataset được sử dụng.

Kết quả không phủ nhận tiềm năng ứng dụng GenAI trong ITSM. Thay vào đó, nó cho thấy tính hiệu quả của một công nghệ cần được đánh giá trong bối cảnh bài toán, dữ liệu và kiến trúc hệ thống cụ thể.

Bài học quan trọng là triển khai AI vào hệ thống thông tin cần xuất phát từ nhu cầu nghiệp vụ, dữ liệu đáng tin cậy, phép đánh giá phù hợp và quá trình triển khai có kiểm soát.

## 11. Tài liệu tham khảo

Sharma, A. J., Rathore, B., Biswas, B., Xiao, X., & Gupta, R. (2026). Generative AI Implementation in Enterprises: Lessons From a Case Study of Enhanced IT Service Management. *Information Systems Journal, 36*(5), 661–690. https://doi.org/10.1111/isj.70029

## 12. File thực nghiệm liên quan

- `README.md`
- `results/llm_two_week_summary.md`
- `results/baseline_llm_comparison_week3_day1.md`
- `results/baseline_llm_shared_errors_week3_day2.md`
- `results/baseline_llm_confusion_week3_day3.md`
- `results/baseline_llm_efficiency_week3_day4.md`
- `results/baseline_report.txt`