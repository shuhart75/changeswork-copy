# Implementation tasks

Feature: `../../feature.md`  
Slice: `../slice.md`  
Дата обновления: `2026-04-27`

## Правила
- Summary по возможности совпадает с Jira summary.
- Этот файл является source of truth для execution-данных по данному slice.
- Для `artifacts` реальные Jira-ключи в импортированном snapshot не нормализованы, поэтому execution-слой пока отражён virtual tasks из actualized legacy gantt.

## Реестр задач

| Jira | Summary | Kind | Role | Estimate (дн) | Executor | Planned Start | Planned Finish | Actual Start | Actual Finish | Status | Progress % | Related Stories | Details |
|---|---|---|---|---:|---|---|---|---|---|---|---:|---|---|
| AN_ART_BE | AN артефакты (BE): модель/контракты/права | virtual | AN | 1 | A2 | 2026-03-31 | 2026-03-31 | 2026-03-31 | 2026-03-31 | done | 100 | STORY-ARTIFACTS-001 |  |
| BE_ART | BE артефакты (ссылки на документы) - БД + API | virtual | BE | 3 | B2 | 2026-04-01 | 2026-04-03 | 2026-04-01 | 2026-04-03 | done | 100 | STORY-ARTIFACTS-001 |  |

## Notes
- Импортировано из `planning/2026-Q2/imported-source/gantt/mvp_gantt_chart_current_actualized_aggressive.puml`.
- При появлении реальных Jira-задач этот реестр нужно materialize-ить без потери связи со story `STORY-ARTIFACTS-001`.

## Legacy references
- `planning/2026-Q2/imported-source/tasks/mvp_tasks_artifacts_core.md`
