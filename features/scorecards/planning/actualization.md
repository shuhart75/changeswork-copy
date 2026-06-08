# Actualization map

Feature: `features/scorecards/feature.md`  
Quarter: `2026-Q2`  
Baseline: `commander-plan`

## Правила
- Для `scorecards` actual-progress показываем planning stories из commander baseline и реальные Jira-задачи `RSCON-2339..RSCON-2344`, `RSCON-2491`, `RSCON-2492`; superseded-задачи не включаются в active layer.
- Mapping оставлен `inferred`, потому что фактический backlog описывает workspace/tab и binding-сценарии, а planning layer был собран по semantic slices.

## Mapping

| Story ID | Summary | Baseline Start | Baseline Duration (дн) | Actualization State | Mapping Mode | Replaced By | Residual Virtual Tasks | Depends On |
|---|---|---|---:|---|---|---|---|---|
| STORY-SCORECARDS-001 | Backend foundation, шаблоны и критичность скоркарт | 2026-04-15 | 13 | materialized | inferred | RSCON-2342, RSCON-2343, RSCON-2492 |  |  |
| STORY-SCORECARDS-002 | Workspace скоркарты: вкладка, деталка, источники и использование | 2026-04-21 | 16 | materialized | inferred | RSCON-2339, RSCON-2340, RSCON-2491 |  |  |
| STORY-SCORECARDS-003 | Создание, редактирование и привязка скоркарты | 2026-04-24 | 23 | materialized | inferred | RSCON-2340, RSCON-2344, RSCON-2491, RSCON-2492 |  |  |
