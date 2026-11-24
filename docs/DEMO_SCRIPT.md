# LibraryMate AI — Kịch bản video demo (4–5 phút)

> Bản demo của **thư viện giả lập**. Dữ liệu sách, tình trạng tồn kho và chính sách P01–P07 không phải dữ liệu thật. Khi quay phải phân biệt **DEMO** (bộ điều phối theo quy tắc) với **GEMINI** (LLM Tool Calling thật). Không nói rằng ảnh DEMO chứng minh Tool Calling Gemini.

## Chuẩn bị

1. Tại thư mục gốc của dự án, kích hoạt Python 3.11 và cài `requirements.txt`.
2. Chạy `python -m scripts.init_db`, `python -m scripts.build_rag_index`, `python -m scripts.run_offline_evals`.
3. Khởi chạy `python -m streamlit run app.py`, mở `http://localhost:8501`.
4. Để video ổn định, chọn `LIBRARYMATE_MODE=demo` trong `.env` (giữ kín file này); khởi động lại Streamlit khi chuyển mode.
5. Mở sẵn Chat, Observability và Evaluation. Không quay API key, file `.env`, thông tin cá nhân hoặc tab không liên quan.

## Phân cảnh với thao tác và lời thoại gợi ý

| Thời gian | Hình/Thao tác | Lời thoại gợi ý |
|---|---|---|
| **00:00–00:25** | Mở slide tiêu đề, sau đó giao diện Streamlit. | "Xin chào, đây là LibraryMate AI — sản phẩm MVP trợ lý thư viện giả lập của nhóm. Ứng dụng hỗ trợ tra cứu sách, số bản còn và quy định mượn trả." |
| **00:25–00:55** | Chỉ vào sơ đồ LangGraph trên slide. | "Hệ thống dùng Streamlit làm giao diện, LangGraph điều phối xử lý, SQLite lưu danh mục 150 sách và ChromaDB truy xuất ngữ nghĩa 7 mục quy định. Input, tool và output guardrails kiểm tra các bước xử lý." |
| **00:55–01:35** | Tại Chat nhập **Tìm sách Python**. Chỉ vào tên sách, số bản còn, kệ. | "Đây là chế độ DEMO: ứng dụng truy vấn dữ liệu mẫu để trả về danh sách Python cùng tình trạng tồn kho. Không có thao tác mượn sách thật." |
| **01:35–02:15** | Nhập **Tôi muốn gia hạn thời gian mượn sách**. Chỉ vào mục **P03**. | "Với câu hỏi về gia hạn, công cụ RAG tìm bằng chứng trong văn bản quy định. Mục P03 nêu có thể gia hạn một lần thêm 7 ngày nếu chưa có người khác yêu cầu và phải gửi trước hạn." |
| **02:15–02:50** | Mở Observability, kéo xuống chi tiết Run ID; nếu có, chọn timeline của một lần truy xuất. | "Mỗi lượt xử lý có Run ID, thống kê các lần gọi công cụ và thời gian chạy. Logs được thiết kế không lưu nguyên văn câu hỏi, câu trả lời và API key." |
| **02:50–03:20** | Mở Evaluation. Chỉ **Passed 30, Failed 0, Errors 0, Skipped 0**. | "Bộ đánh giá offline đã ghi nhận 30 trên 30 ca đạt. Đây là kết quả kiểm thử SQLite, RAG và guardrails, không phải độ chính xác của Gemini ngoài thực tế." |
| **03:20–03:45** | Slide Guardrails, có thể nhập thử câu lệnh phá dữ liệu trong DEMO thử nghiệm. | "Ba công cụ đều chỉ đọc. Hệ thống giới hạn tối đa 3 lượt LLM, 5 tool calls và 3 tool calls trong một lượt; các tham số công cụ được kiểm tra." |
| **03:45–04:15** | Mở GitHub README, ảnh và các file chính. | "Mã nguồn được công bố trên GitHub với tài liệu cài đặt, kiểm thử và ảnh minh chứng. Các cải tiến gần đây bao gồm cache Chroma client và giảm công cụ gọi trùng." |
| **04:15–04:40** | Slide kết luận. | "LibraryMate AI minh họa quy trình Agentic AI có công cụ, RAG, guardrails, observability và evaluation. Giới hạn hiện tại là dữ liệu mô phỏng, quota Gemini và độ trễ khởi tạo RAG. Xin cảm ơn." |

## Phương án dành cho Gemini thật

- Chỉ sử dụng nếu `LIBRARYMATE_MODE=gemini`, có khóa hợp lệ và còn quota.
- Ghi chú trên video **GEMINI — real LLM tool calling**; để rõ sự khác biệt so với DEMO.
- Thử câu hỏi kết hợp: **Tìm sách SQL và cho biết thời hạn mượn**. Kiểm tra tool traces và kết quả trước khi quay.
- Nếu Google trả về lỗi 429/rate limit, **không** thay bằng ảnh DEMO và gọi đó là Gemini thật. Chuyển sang DEMO đã được ghi nhãn, hoặc trình bày bằng log/test có sẵn với chú thích rõ.

## Câu hỏi phản biện ngắn

**Tại sao cần LangGraph?** — Để điều phối có trạng thái giữa input guardrail, agent, validated tools, output guardrail và ghi trace.

**Semantic RAG khác tìm từ khóa thế nào?** — Câu hỏi và đoạn quy định được mã hóa thành embedding; Chroma dùng độ tương đồng để truy xuất các đoạn có mã nguồn P01–P07.

**30/30 có nghĩa Gemini chính xác 100%?** — Không. Đây là bộ offline evals riêng; cần đánh giá live end-to-end để kết luận về chất lượng câu trả lời của Gemini.

**Có cập nhật được kho sách thật không?** — Chưa. Công cụ chỉ đọc SQLite giả lập; hệ thống không có chức năng cho mượn hay đặt sách thật.

**Có dùng API key trong video không?** — Không trình chiếu hay commit API key; giữ trong `.env` trên máy và đưa `.env` vào `.gitignore`.
