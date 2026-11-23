# LangGraph workflow (design)

```mermaid
flowchart TD
  START --> A[Input guardrail]
  A -->|Blocked| B[Safe refusal]
  A -->|Pass| C[LLM agent]
  C -->|Tool calls| D[Validate tool names and arguments]
  D -->|Valid| E[Execute approved read-only tools]
  D -->|Invalid| F[Return controlled tool error]
  E --> C
  F --> C
  C -->|Final answer| G[Output guardrail]
  G --> H[Response with evidence and uncertainties]
  B --> END
  H --> END
```

State: `messages`, `run_id`, `iteration_count`, `source_refs`, `guardrail_flags`, `errors`.

Stop conditions: final LLM message without tool calls; max iterations reached; policy rejection; unrecoverable error.

Observability: a structured event for each node and tool invocation, durations and status.
