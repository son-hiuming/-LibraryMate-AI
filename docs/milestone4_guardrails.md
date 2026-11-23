# Milestone 4.1 — Guardrails & quota-safe Agent

Đây là bản nâng cấp **từ Milestone 3 RAG**, giữ nguyên 150 đầu sách và tài liệu P01–P07.

## Các thay đổi

- Gemini: `max_retries=0`, `timeout=30`. Không tự lặp lại khi gặp 429.
- Ngân sách mỗi yêu cầu: tối đa **3 lượt LLM**, **5 lời gọi công cụ**, tối đa **3 công cụ trong một lượt**. Nếu vượt, hệ thống dừng **không gọi LLM tiếp**, không giả vờ đã có câu trả lời xác minh.
- Tool rail: allowlist, kiểm tra kiểu và biên giá trị tham số trước khi thực thi công cụ.
- Quan sát: `agent`, `tool_call`, `llm_error`, `budget_reached`, `completed` và các số đếm (không ghi API key hay nguyên văn câu hỏi).
- Lỗi quota: hiển thị thông báo ngắn gọn để kiểm tra hạn mức.

## Cài đặt / cập nhật

1. **Sao lưu thư mục đang chạy**. Giải nén ZIP này sang thư mục riêng.
2. Sao chép `.env` của thư mục cũ vào thư mục mới. Không gửi và không commit `.env`.
3. Trong PowerShell (đứng ở thư mục có `app.py`):

```powershell
py -3.11 -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m scripts.init_db
python -m scripts.build_rag_index
python -m pytest -q
streamlit run app.py
```

Nếu có sẵn `data/chroma_db` từ bản cũ có thể sao chép sang bản mới thay vì build lại, miễn là model và `library_policy.md` không thay đổi.

## Những điều vẫn cần xác thực

- Các unit tests chạy offline không chứng minh Gemini có đủ quota.
- Chưa có cơ chế phân quyền theo người dùng, không sử dụng với dữ liệu thư viện thật.
- Công cụ RAG phải trả `passages` có Pxx. Việc gọi tool thành công không đồng nghĩa RAG có bằng chứng.
- Guardrails dựa trên quy tắc là lớp phòng vệ cơ bản; chưa phải phòng chống prompt injection toàn diện.

## Thử nghiệm

- `python -m pytest -q tests/test_milestone4.py`
- Hỏi riêng câu về gia hạn, sau đó câu hỏi SQL + thời hạn.
- Xem `logs/events.jsonl`, đối chiếu Run ID và `tool_call` events.
