# LibraryMate AI — Submission checklist

## 1. GitHub link
- [ ] Run tests on the final unmodified version.
- [ ] Review `.gitignore`; never commit `.env`, `.venv`, `logs`, `reports`, `data/*.db`, `data/chroma_db`.
- [ ] Create new GitHub repository `LibraryMate-AI` under a team/member account (do not claim it exists before creation).
- [ ] Add source, README, tests, fictional data, docs and requirements.
- [ ] Link repository in slide and final submission.

## 2. Working MVP
- [ ] Show Streamlit chat, 150 fictional books and a search query.
- [ ] Show policy retrieval with citation P03; if Gemini quota unavailable, show offline RAG results separately and explain that DEMO mode is rule-based.
- [ ] Demonstrate guardrail block and tool validation.
- [ ] Capture full run timeline on Observability.
- [ ] Run offline evals and capture 30/30 result and JSON report.

## 3. Presentation and video
- [ ] Insert team names, course and repo link into slide deck.
- [ ] Present problem → architecture → workflow → guards → tracing → evals → limitations.
- [ ] Record short introduction and screen-capture of real demo (not a fabricated demo).
- [ ] Be explicit about quota issues and synthetic dataset.

## 4. Evidence claims
- Offline suite: 30 passed / 0 failed / 0 errors / 0 skipped, according to 23 Nov 2026 user run.
- Example 23 Nov trace: 2 LLM calls, 1 RAG tool call, 44.294 s total, 36.757 s RAG step.
- Local dashboard: 8 observed runs, all successful in that log; NOT a global success-rate claim.
- Actual GitHub URL and demo video URL must be supplied by the team.
