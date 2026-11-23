# LibraryMate AI — Intro video + demo script (Vietnamese)

## Video đề xuất: 3–5 phút

**0:00–0:25 — Giới thiệu:** “Nhóm xây dựng LibraryMate AI, trợ lý thư viện giả lập dựa trên Gemini, LangGraph và RAG. Sinh viên có thể tra cứu sách, tình trạng tồn kho và quy định mượn.”

**0:25–0:55 — Kiến trúc:** Cho xem slide kiến trúc. Giải thích Input Guardrail → LLM Agent → Tool validation → SQLite/RAG → Output Guardrail. Đây là một Agent có ba công cụ chỉ đọc dữ liệu.

**0:55–1:45 — Demo công cụ:** Hỏi “Tìm sách Python còn để mượn”. Trên ứng dụng, chỉ ra tên sách, số bản, vị trí. Với câu hỏi kết hợp “Tìm sách SQL còn để mượn và cho biết thời hạn mượn”, minh họa công cụ tra cứu và P02. **Chỉ quay cảnh nếu đã chạy thành công thật.**

**1:45–2:20 — RAG:** Hỏi “Tôi muốn giữ sách thêm một tuần nữa được không?”. Chỉ ra P03 và điều kiện gia hạn. Nếu Gemini hết quota, chuyển sang lệnh `python -m pytest -q tests/test_rag_live.py` rồi giải thích đây là RAG độc lập, không phải Tool Calling Gemini.

**2:20–2:55 — An toàn:** Thử yêu cầu phá hoại dữ liệu trong một môi trường thử nghiệm để minh họa Input Guardrail. Công cụ trong hệ thống là read-only.

**2:55–3:35 — Observability:** Mở bảng timeline, chọn một Run ID. Chỉ ra input_rail, agent, tool_call, output_rail, completed. Ví dụ run đã quan sát có 2 LLM calls / 1 policy tool call / 44.294 s.

**3:35–4:05 — Evals:** Mở trang Evaluation hoặc Terminal, chạy `python -m scripts.run_offline_evals`. Kết quả đã ghi nhận là 30/30 passed trên bộ offline; lưu ý đây không phải độ chính xác live.

**4:05–4:30 — Kết luận:** “Điểm mạnh: có workflow, tool calling, RAG, guardrails, traces và Evals. Giới hạn: dữ liệu giả lập, quota API Gemini, độ trễ của RAG; hướng tiếp theo là giảm cold start và đánh giá online.”

## Technical presentation — speaker outline (4–6 phút)
1. Kiến trúc có trạng thái: `messages`, `run_id`, `steps`, `tool_count`, `blocked`, `error`.
2. LLM quyết định gọi công cụ; `search_books` và `check_availability` truy vấn SQLite, `search_library_policy` dùng embeddings + Chroma.
3. Giới hạn: 3 lượt LLM, tối đa 5 tool calls, tối đa 3 tool calls mỗi batch; tham số được kiểm tra.
4. Traces JSONL ghi event & latency, không lưu toàn bộ nội dung hỏi đáp; vẫn có hạn chế nếu ứng dụng dừng bất ngờ.
5. 30 offline evals: kết quả xác nhận từ terminal 30 passed; đánh giá live end-to-end chưa hoàn chỉnh vì quota.

## Before filming
- Hide .env and any credentials.
- Verify enough Gemini API quota, or honestly label portions run in DEMO/offline mode.
- Clear private browser tabs; enlarge Streamlit page.
- Do not show fake output as successful live API execution.
