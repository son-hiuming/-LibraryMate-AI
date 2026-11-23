# Evidence capture and README screenshots

This guide describes how to collect verifiable project evidence for the assignment. It does not claim that screenshots are already included.

## 1. Prepare the environment

From the repository root, run:

```powershell
python -m scripts.init_db
python -m scripts.build_rag_index
python -m scripts.run_offline_evals
python -m pytest -q
streamlit run app.py
```

Use the **same version** of the code as the version shown in the screenshots. Ensure that `.env` is not committed. For a live Gemini demo, check your quota first and label the mode clearly.

## 2. Capture four images

Save PNGs under `docs/images/` using these names:

1. `chat-book-search.png` — a real search result showing book availability and shelf.
2. `rag-policy.png` — a policy question/answer showing P03 and its evidence source; note whether the mode is GEMINI or DEMO.
3. `observability-timeline.png` — the actual event timeline for one Run ID, showing `input_rail`, `agent`, `tool_call`, `output_rail`, `completed`.
4. `offline-evals.png` — the terminal report or Evaluation UI showing `passed=30`, `failed=0`, `error=0`, `skipped=0`.

Avoid including credentials, account-specific paths, or private questions in images. If a screenshot contains information you cannot safely crop, redact it locally before sharing.

## 3. Embed in README only after the files exist

```markdown
![Book search demo](docs/images/chat-book-search.png)
![Policy RAG demo](docs/images/rag-policy.png)
![Observability trace](docs/images/observability-timeline.png)
![Offline evaluation results](docs/images/offline-evals.png)
```

For GitHub upload, create a branch and add the actual PNG files first. Then update README with those Markdown image references and open a pull request to `main`.

## 4. Evidence interpretation

- **30/30** is the observed *offline* evaluation result, not a 100% live answer accuracy claim.
- The example trace supplied by the project team recorded **2 Gemini calls**, **1 policy tool call**, **44.294 seconds** total and **36.757 seconds** in the RAG tool. It is a single run, not a population average.
- The demo mode uses rules, whereas Gemini mode uses real LLM tool calling.
- The project uses fictional books and library policies.

## 5. Final submission links

- GitHub: https://github.com/son-hiuming/-LibraryMate-AI
- Slides: add a stable URL after uploading
- Intro/demo video: add a stable URL after uploading
- Report: `reports/offline_evals.json` is generated locally; publish only if reviewed for sensitive information
