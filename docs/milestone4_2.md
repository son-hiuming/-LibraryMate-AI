# Milestone 4.2 — Observability & Evals

## Mục đích
- Dashboard đọc JSONL (`logs/events.jsonl`), thống kê runs thành công/lỗi, latency, event tool call và lỗi Gemini.
- Bộ 30 ca đánh giá offline: 10 catalog, 5 stock, 10 semantic RAG, 5 input guardrails.
- Không gọi Gemini trong dashboard, pytest hoặc `scripts.run_offline_evals`.

## Chạy
```powershell
python -m scripts.init_db
python -m scripts.build_rag_index
python -m scripts.run_offline_evals
python -m pytest -q
streamlit run app.py
```

Streamlit sidebar → **Observability** và **Evaluation**. Đặt `LIBRARYMATE_MODE=demo` khi muốn demo mà không dùng Gemini API.

## Diễn giải
- `pass_rate` = pass / (passed+failed+error); `skipped` không vào mẫu số, cần báo cáo riêng.
- Semantic RAG eval đo **expected section in top-3 passages**, không đo độ chính xác câu trả lời AI.
- Agent step count quan sát qua event `agent` chỉ tính lần gọi đã hoàn tất; API 429 có thể khiến số lần gọi thực tế cao hơn số quan sát.
- Dashboard giữ chi tiết `run_id`, status, loại lỗi, tên tool, latency; không ghi prompt hoặc API key.
- Các giá trị này là số liệu của bản demo giả lập, không phản ánh độ chính xác trong môi trường thực tế.

## Hạn chế
- Không có phân tích độ chính xác Gemini/tool-selection E2E vì quota hiện đang giới hạn.
- Traces chỉ mức ứng dụng (JSONL), không phải distributed tracing với parent-span IDs.
- Chưa có xác thực người dùng cho dashboard; chỉ dùng cục bộ, không triển khai công khai.
