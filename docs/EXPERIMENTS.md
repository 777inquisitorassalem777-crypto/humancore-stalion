# First experiment plan

Do not claim improvements before running measured comparisons.

## Conditions
A. Recency-only memory ranking.
B. Lexical similarity ranking.
C. Memory Gravity (current heuristic).

## Tasks
- Exact recall after 1/10/50 intervening events.
- Related-event retrieval under paraphrase.
- Identity anchor preservation after adaptive-value updates.
- Plan-step completeness and risk mention.
- Contradiction identification in paired observations.

## Metrics
- Recall@k, MRR, event retention by distance, core-value drift, plan checklist pass rate, latency.
- For comparisons: paired bootstrap confidence intervals and a preregistered primary metric.
- Use held-out task templates to reduce leakage. Report failures as well as wins.
