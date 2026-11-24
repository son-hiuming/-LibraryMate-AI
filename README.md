# 📚 LibraryMate AI — Agentic Library Assistant

**Working academic MVP** | Python · Streamlit · LangGraph · Gemini · SQLite · Semantic RAG (ChromaDB)

> **Disclaimer:** This is a university-course prototype. All 150 catalog entries and seven borrowing-policy sections are **fictional**; the app does not connect to any real library or perform real loans.

## Project at a glance

| Item | Implementation |
| --- | --- |
| Interface | Streamlit chat + Observability and Evaluation pages |
| AI orchestration | LangGraph with Gemini tool calling (or clearly labeled rule-based DEMO mode) |
| Knowledge sources | Synthetic SQLite book catalog + bilingual fictional library policies |
| Retrieval | Sentence Transformers + local ChromaDB |
| Safety | Input/tool/output checks, read-only tools, LLM/tool-call budgets |
| Evidence | 30/30 offline evaluations reported by project team; selected trace recorded below |
| Repository | https://github.com/son-hiuming/-LibraryMate-AI |

> **Evidence boundary:** A passing offline evaluation does not demonstrate live Gemini reliability. Live API calls remain subject to model availability and project rate limits.

## What it does

- Search the catalog of 150 example books; check copy availability and shelf location.
- Retrieve fictional library regulations from bilingual policy chunks with **Sentence Transformers** and **ChromaDB**; cite section IDs P01–P07.
- Route questions with **Gemini tool calling through LangGraph**; supports questions that involve multiple tools.
- Apply **input, tool, and output guardrails** plus per-question budgets (3 LLM calls / 5 tool calls / max 3 per tool batch).
- Record structured JSONL events and inspect them in Streamlit **Observability**.
- Execute 30 deterministic **offline evals** without using Gemini API and view reports in **Evaluation**.

## Architecture

```mermaid
flowchart TD
  U[Student] --> UI[Streamlit chat]
  UI --> I[Input guardrail]
  I -->|accepted| A[LangGraph Gemini agent]
  I -->|blocked| E[Safe response]
  A -->|tool calls| V[Tool validation and budget]
  V --> B[search_books - SQLite]
  V --> C[check_availability - SQLite]
  V --> R[search_library_policy - Chroma RAG]
  B --> A
  C --> A
  R --> A
  A -->|final message| O[Output guardrail]
  O --> UI
  A -.-> L[JSONL trace events]
  V -.-> L
  L --> D[Observability dashboard]
  T[Offline evaluation suite] --> B
  T --> C
  T --> R
```

The 3 tools are **read-only**. `LIBRARYMATE_MODE=demo` is rule-based simulation, whereas `gemini` uses a real LLM; do not equate them when presenting results.

## Quick start — Windows PowerShell / Python 3.11

```powershell
py -3.11 -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env`: to use real LLM tool calling, set `LIBRARYMATE_MODE=gemini`, enter your own `GOOGLE_API_KEY` locally, and choose a Gemini model **available to your project**. To test without API calls, leave `LIBRARYMATE_MODE=demo`. **Never commit or upload `.env`.**

```powershell
python -m scripts.init_db
python -m scripts.build_rag_index
python -m scripts.run_offline_evals
python -m pytest -q
python -m streamlit run app.py
```

Open the local URL Streamlit prints (usually `http://localhost:8501`). RAG index creation can download multilingual embedding weights once; internet is required for that first download. The default `demo` mode runs without a Gemini API key.


## Demo Screenshots (captured from local app)

### 1. Book Search (DEMO Mode)
![Book Search](docs/images/chat-book-search.png)

### 2. Semantic RAG (DEMO Mode)
![Policy Retrieval](docs/images/rag-policy.png)

### 3. Observability Dashboard
![Observability Dashboard](docs/images/observability-timeline.png)

### 4. Offline Evaluation Results
![Offline Evaluation](docs/images/offline-evals.png)

> Note: Book Search and RAG screenshots were captured in DEMO mode. The 30/30 pass rate applies to offline evaluations, not live Gemini accuracy.

## Rebuild after changing data

- `data/books.csv` changed: `python -m scripts.init_db`
- `data/library_policy.md` or embedding model changed: `python -m scripts.build_rag_index --force`

## Evidence and current status (local observations)

- **Offline Evals:** the project team ran `python -m scripts.run_offline_evals` and reported **30 passed, 0 failed, 0 errors, 0 skipped**. These tests cover catalog search, stock, RAG and input guardrails. They are *not* 100% real-world answer accuracy.
- **Observability:** a later screenshot provided by the project team shows 15 runs, 15 successes, 0 errors, and a reported mean successful-run latency of 18,646 ms *for that local log set*. A separate earlier trace completed in **44.294s**, with **2 Gemini calls**, **1 `search_library_policy` call**, and **36.757s** in the RAG tool; neither figure is a benchmark of current code.
- **Known constraints:** Google API rate limits can prevent a live Gemini demo; Chroma/model initial load can make early requests slow. The current code caches the embedding model and Chroma client per process and includes `python -m scripts.benchmark_rag` to measure warm vs cold retrieval locally. **No post-optimization speedup is claimed here without benchmark results.**

## Technical decisions and limitations

- **Single-agent design:** One LangGraph agent and three read-only tools keep the course MVP testable and auditable.
- **Two data access patterns:** SQLite supports structured catalog/availability lookups; ChromaDB supports semantic policy retrieval.
- **Offline vs live evaluation:** Offline tests validate deterministic behavior without API quota. They do not measure live answer correctness or tool-selection reliability.
- **Rate limits:** Gemini 3 Flash quota has affected live runs. A rate-limit response is an API constraint rather than evidence of a failed Chroma retrieval.
- **RAG cold start:** The observed example spent 36.757 s in `search_library_policy`; this is an **example trace**, not an average benchmark. Caching the embedding model and Chroma client is implemented; actual speedup must be measured with `python -m scripts.benchmark_rag`.
- **Privacy:** JSONL logs omit question and answer bodies by default; a sudden process stop may leave an incomplete trace.

## Test commands

```powershell
python -m pytest -q
python -m pytest -q tests/test_rag_live.py
python -m scripts.run_offline_evals
```

Offline report: `reports/offline_evals.json` (generated locally and ignored by Git). Logs: `logs/events.jsonl` (also ignored). To inspect run timeline use Streamlit sidebar → **Observability**.

## Repository map

```text
app.py                       Streamlit chat
pages/1_Observability.py    Logs/dashboard
pages/2_Evaluation.py       Offline evaluation viewer
src/agent/graph.py          LangGraph state, nodes, routes, Gemini/demo mode
src/tools/library_tools.py Read-only book and policy tools
src/rag/engine.py           Local embeddings and Chroma retrieval
src/guardrails/rules.py     Guardrail validation
src/monitoring/             Structured run logs and analytics
scripts/                    SQLite, RAG indexing, offline evaluations
data/                       Synthetic catalog and policies
evals/                      Evaluation cases
tests/                      Automated tests
docs/                       Architecture, demo script, hand-in notes
```

## Project submission

- **Repository:** [son-hiuming/-LibraryMate-AI](https://github.com/son-hiuming/-LibraryMate-AI)
- **Demo filming script:** [docs/DEMO_SCRIPT.md](docs/DEMO_SCRIPT.md)
- **Submission checklist:** [docs/SUBMISSION_CHECKLIST.md](docs/SUBMISSION_CHECKLIST.md)
- **Screenshot evidence:** [docs/EVIDENCE_GUIDE.md](docs/EVIDENCE_GUIDE.md) and the four images above
- **Slides / final video:** Add verified upload links here after they are published. Files are not automatically included by creating this README.
- **Automated tests:** [GitHub Actions](.github/workflows/tests.yml) runs a Python 3.11 pytest suite on pushes and pull requests. Check the Actions tab for the actual outcome; this sentence is not a claim of a passing CI run.

Do not commit `.env`, API keys, local logs, the generated Chroma index, or private data.

## Limitations & safety

This is an educational demonstration, not a production service. Catalog and policy statements must be sourced from the fictional dataset. Guardrails are baseline rules, not a complete security guarantee; logs omit raw questions and responses by design. The offline evaluation set does not assess live LLM tool-selection accuracy or adversarial robustness across all prompts. The GitHub Actions workflow does not call Gemini or replace local semantic-RAG benchmark measurements.
