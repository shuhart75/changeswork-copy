# Actualization map

Feature: `features/approvals/feature.md`  
Quarter: `2026-Q2`  
Baseline: `commander-plan`

## Правила
- Реальные Jira-задачи `RSCON-2518..2521` заменяют прежние virtual chunks в actual-progress layer.
- Старые virtual items сохраняются в task registry как superseded, чтобы не терять traceability.

## Mapping

| Story ID | Summary | Baseline Start | Baseline Duration (дн) | Actualization State | Mapping Mode | Replaced By | Residual Virtual Tasks | Depends On |
|---|---|---|---:|---|---|---|---|---|
| STORY-APPROVALS-001 | Approval core и интеграция с ЖЦ | 2026-04-01 | 24 | materialized | inferred | RSCON-2518, RSCON-2519, RSCON-2520 |  |  |
| STORY-APPROVALS-002 | Страница "Согласования" | 2026-04-06 | 29 | materialized | inferred | RSCON-2521 |  |  |
