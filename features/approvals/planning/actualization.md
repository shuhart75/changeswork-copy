# Actualization map

Feature: `features/approvals/feature.md`  
Quarter: `2026-Q2`  
Baseline: `commander-plan`

## Правила
- Реальные задачи `RSCON-2629..2637`, `RSCON-2649` и QA-задачи закрывают весь scope согласований.
- Старые virtual chunks и прежний набор `RSCON-2518..2521` удалены из активных task registry, чтобы не дублировать actual-progress layer.

## Mapping

| Story ID | Summary | Baseline Start | Baseline Duration (дн) | Actualization State | Mapping Mode | Replaced By | Residual Virtual Tasks | Depends On |
|---|---|---|---:|---|---|---|---|---|
| STORY-APPROVALS-001 | Approval core и интеграция с ЖЦ | 2026-04-01 | 24 | materialized | explicit | RSCON-2629, RSCON-2630, RSCON-2631, RSCON-2633, RSCON-2634, RSCON-2635, RSCON-2649 |  |  |
| STORY-APPROVALS-002 | Страница "Согласования" | 2026-04-06 | 29 | materialized | explicit | RSCON-2636, QA-APPROVALS-CARD, RSCON-2637, QA-APPROVALS-EMAIL-PREVIEW |  | STORY-APPROVALS-001 |
