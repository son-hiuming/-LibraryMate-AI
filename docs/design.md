# Milestone 1 — Software requirements and design

## 1. Product goal
Build a working AI agent for a fictional campus library. Students ask questions in Vietnamese and receive grounded answers about catalog records, availability, and policies.

## 2. Actors
- Student / library user (primary)
- Developer / evaluator (reviews logs, evaluation reports)

## 3. Core use cases
### UC01 Search books
Input: topic, title, author, description or study goal.
Flow: validate input → agent calls `search_books` → returns matching books → summarise with book IDs.
Failure: no match → state no matching books, suggest alternative search terms.

### UC02 Check availability
Input: book name or book ID.
Flow: validate input → `check_availability` → report count from DB.
Failure: ambiguous title → request disambiguation; unknown book → no claim of availability.

### UC03 Answer policy questions
Input: borrowing, renewal, return, overdue, hours or other policy query.
Flow: validate input → `search_library_policy` → retrieval → grounded answer citing source section.
Failure: no reliable evidence → explicitly say policy not found in available documents.

### UC04 Combined question
Input: e.g. 'Gợi ý sách Python còn để mượn và hạn mượn bao lâu?'
Flow: search_books → check_availability for candidates → search_library_policy → synthesis.

## 4. Functional requirements
FR01: Vietnamese input/output. FR02: structured book search.
FR03: read-only inventory lookup. FR04: RAG-based policy Q&A.
FR05: LLM-driven tool routing. FR06: tool schema validation.
FR07: answer uncertainty and citation handling.
FR08: trace per run; FR09: repeatable eval suite.

## 5. Nonfunctional requirements
NFR01: No mutating database commands exposed to agent.
NFR02: Max 5 tool iterations per run, with graceful fallback.
NFR03: no secrets in source control and redact sensitive logging fields.
NFR04: deterministic retrieval tests and recorded tool-call traces.
NFR05: separate UI, agent, data, guardrail, monitoring and evaluation modules.

## 6. Component plan
Model: chat LLM with tool-calling support (provider config to be validated before implementation).
Graph: START → input_guardrail → agent → (tool_guardrail → tool_exec → agent)* → output_guardrail → END.
Tools: search_books(query,limit), check_availability(book_id), search_library_policy(query,k).
Storage: SQLite `books`, Chroma vectors with metadata source/section/chunk.
Safety: input length and domain checks, allowed tool map/typed args/read-only DB, grounded policy answers and no false availability claims.
Monitoring: run_id, node events, tool name/status, duration, retrieval source IDs, guardrail triggers, errors; exclude API keys/private content.
Evaluation: tool routing, policy source support, inventory correctness, guardrail handling, exception handling, latency.

## 7. Database schema
```sql
CREATE TABLE books (
    book_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT NOT NULL,
    total_copies INTEGER NOT NULL CHECK(total_copies>=0),
    available_copies INTEGER NOT NULL CHECK(available_copies>=0 AND available_copies<=total_copies),
    shelf_location TEXT NOT NULL
);
```

## 8. Out of scope
Real library integration; account/login; borrow/reserve/return transactions; payments; user profiling; unrestricted web access; complex multi-agent architecture.

## 9. Milestone acceptance checklist
- [x] Define problem, scope, actors, use cases and schema
- [x] Provide initial synthetic dataset and policy document
- [x] Specify graph and test plan
- [ ] Implement and execute graph in Milestone 2
- [ ] Run automated tests and record measured results later
