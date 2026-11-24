# LibraryMate AI — Checklist trước khi nộp

**Tình trạng:** Dự án minh họa học thuật; không kết nối thư viện thực tế. Đánh dấu chỉ sau khi tự kiểm tra trên **commit cuối cùng** của nhánh `main`.

## A. Mã nguồn và bảo mật

- [ ] Nhánh `main` có mã nguồn mới nhất; `git status` sạch.
- [ ] `.env`, API keys, log cá nhân và Chroma index không được commit.
- [ ] `README.md` có kiến trúc Mermaid, hướng dẫn chạy và ghi rõ chế độ DEMO/GEMINI.
- [ ] Các đường dẫn tới ảnh trong `docs/images/` hiển thị trên GitHub.
- [ ] Ba công cụ `search_books`, `check_availability`, `search_library_policy` hoạt động và chỉ đọc.
- [ ] Guardrails chặn yêu cầu không phù hợp và giới hạn tham số.

## B. Kiểm thử tái hiện được

Chạy từ thư mục gốc, Python 3.11 đã kích hoạt:

```powershell
python -m scripts.init_db
python -m scripts.build_rag_index
python -m pytest -q
python -m scripts.run_offline_evals
python -m scripts.benchmark_rag
```

- [ ] Pytest thành công trên phiên bản `main` cuối cùng.
- [ ] Offline Evals: 30 passed, 0 failed, 0 errors, 0 skipped (ghi lại kết quả thực tế).
- [ ] RAG retrieval cho câu hỏi gia hạn có mã mục **P03**.
- [ ] Chạy benchmark; không tuyên bố tăng tốc khi chưa có số liệu so sánh trước/sau.
- [ ] GitHub Actions hiện dấu check xanh ở commit cần nộp (nếu workflow được bật và chạy thành công).
- [ ] Test Gemini riêng khi còn quota; nếu không, ghi đúng giới hạn đã gặp.

## C. Minh chứng và video

- [ ] 4 ảnh Book Search, Policy RAG, Observability, Offline Evals có trên GitHub.
- [ ] Ảnh chat từ DEMO được ghi nhãn DEMO, không giới thiệu như Tool Calling live.
- [ ] Video MP4 4–5 phút, âm thanh rõ, chữ đủ lớn.
- [ ] Trong video, trình diễn luồng RAG và trích dẫn P03.
- [ ] Có phần Observability, Evaluation, giới hạn và kết luận.
- [ ] Đã xem lại toàn bộ video để loại bỏ API key và thông tin cá nhân.

## D. Tài liệu và nộp bài

- [ ] Slide thuyết trình đã kiểm tra chính tả và nội dung phù hợp code cuối cùng.
- [ ] Kịch bản video theo `docs/DEMO_SCRIPT.md`.
- [ ] Link video hoạt động ở chế độ người xem/giảng viên có thể mở.
- [ ] README chứa link slide và video sau khi upload.
- [ ] Chốt version/tag `v1.0.0` **chỉ khi** các bước trên đạt.

## Giới hạn cần trình bày trung thực

1. 150 sách và bảy mục chính sách là dữ liệu mô phỏng.
2. 30/30 offline evals không khẳng định 100% chính xác với Gemini thật.
3. Các guardrails là baseline; không bảo đảm chống mọi prompt injection.
4. Cache Chroma client và embedding model đã triển khai nhưng chưa mặc định bảo đảm một ngưỡng hiệu năng.
5. Gemini có thể bị rate limit và không thể mặc định demo live mọi lúc.
