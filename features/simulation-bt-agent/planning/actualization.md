# Actualization map

Feature: `features/simulation-bt-agent/feature.md`  
Quarter: `2026-Q2`  
Baseline: `commander-plan`

## Правила
- Для `simulation-bt-agent` planning layer уже разложен на три semantic stories, а execution пришёл двумя крупными backlog-задачами плюс feature-level QA.
- Используем `materialized` + `inferred`, потому что реальные Jira-задачи не совпадают 1:1 с planning stories и покрывают сразу несколько slices.

## Mapping

| Story ID | Summary | Baseline Start | Baseline Duration (дн) | Actualization State | Mapping Mode | Replaced By | Residual Virtual Tasks | Depends On |
|---|---|---|---:|---|---|---|---|---|
| STORY-SIMULATION-BT-AGENT-001 | Точка входа и контекст запуска БТ | 2026-04-28 | 7 | materialized | inferred | RSCON-2480, RSCON-2479 |  |  |
| STORY-SIMULATION-BT-AGENT-002 | Сессия диалога и оркестрация AI-агента | 2026-04-28 | 10 | materialized | inferred | RSCON-2480, RSCON-2479 |  | STORY-SIMULATION-BT-AGENT-001 |
| STORY-SIMULATION-BT-AGENT-003 | Публикация БТ, сохранение ссылки и аудит | 2026-05-14 | 8 | materialized | inferred | RSCON-2480, RSCON-2479, QA_SIM_BT_AGENT |  | STORY-SIMULATION-BT-AGENT-002 |
