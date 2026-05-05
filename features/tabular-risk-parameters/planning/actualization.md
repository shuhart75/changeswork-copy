# Actualization map

Feature: `features/tabular-risk-parameters/feature.md`  
Quarter: `2026-Q2`  
Baseline: `commander-plan`

## Правила
- Для `tabular-risk-parameters` actual-progress строится из planning stories и уже materialized backlog-задач `RSCON-*`.
- Baseline start/duration выровнены по legacy commander baseline, а фактическая materialization идёт по актуальному execution-слою.

## Mapping

| Story ID | Summary | Baseline Start | Baseline Duration (дн) | Actualization State | Mapping Mode | Replaced By | Residual Virtual Tasks | Depends On |
|---|---|---|---:|---|---|---|---|---|
| STORY-TABULAR-RISK-PARAMETERS-001 | Backend табличных риск-параметров и интеграция с источниками/запуском симуляции | 2026-04-16 | 16 | materialized | explicit | RSCON-2430, RSCON-2432, RSCON-2452 |  |  |
| STORY-TABULAR-RISK-PARAMETERS-002 | Frontend форма изменения табличных риск-параметров | 2026-05-22 | 13 | materialized | explicit | RSCON-2429, QA_TABULAR_RISK_PARAMETERS |  | STORY-TABULAR-RISK-PARAMETERS-001 |
