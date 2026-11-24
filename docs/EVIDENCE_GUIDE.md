# Evidence capture and README screenshots

Four screenshots are already committed under `docs/images/` and embedded in the repository README. This guide documents their provenance and how to replace or recapture them responsibly.

## 1. Prepare the environment

From the repository root, run:

```powershell
python -m scripts.init_db
python -m scripts.build_rag_index
python -m scripts.run_offline_evals
python -m pytest -q
streamlit run app.py
```


## 2. Capture four images

Save PNGs under `docs/images/` using these names:

1. `chat-book-search.png` — a real search result showing book availability and shelf.
2. `rag-policy.png` — a policy question/answer showing P03 and its evidence source; note whether the mode is GEMINI or DEMO.
3. `observability-timeline.png` — the current uploaded image shows the **Observability dashboard summary** (run count, success count, tools). To prove a specific run's node sequence, add a separate screenshot of the Run ID timeline below the fold.
4. `offline-evals.png` — the terminal report or Evaluation UI showing `passed=30`, `failed=0`, `error=0`, `skipped=0`.


## 3. README image references (already present)

```markdown
![Book search demo](docs/images/chat-book-search.png)
![Policy RAG demo](docs/images/rag-policy.png)
![Observability trace](docs/images/observability-timeline.png)
![Offline evaluation results](docs/images/offline-evals.png)
```


## 4. Evidence interpretation

- **30/30** is the observed *offline* evaluation result, not a 100% live answer accuracy claim.
- The example trace supplied by the project team recorded **2 Gemini calls**, **1 policy tool call**, **44.294 seconds** total and **36.757 seconds** in the RAG tool. It is a single run, not a population average.
- The demo mode uses rules, whereas Gemini mode uses real LLM tool calling.
- The project uses fictional books and library policies.

## 5. Final submission links

- GitHub: https://github.com/son-hiuming/-LibraryMate-AI
- Slides: add a stable URL after uploading and verifying
- Intro/demo video: add a stable URL after uploading and verifying
- Report: `reports/offline_evals.json` is generated locally; publish only if reviewed for sensitive information
