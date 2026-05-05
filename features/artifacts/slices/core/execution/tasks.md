# Implementation tasks

Feature: `../../feature.md`  
Slice: `../slice.md`  
Дата обновления: `2026-05-04`

## Правила
- Summary по возможности совпадает с Jira summary.
- Этот файл является source of truth для execution-данных по данному slice.
- Для `artifacts` execution-слой смешанный: legacy shared scope сохранён virtual-задачами, а новые подтверждённые backlog-задачи добавляются как `real`.

## Реестр задач

| Jira | Summary | Kind | Role | Estimate (дн) | Executor | Planned Start | Planned Finish | Actual Start | Actual Finish | Status | Progress % | Related Stories | Details |
|---|---|---|---|---:|---|---|---|---|---|---|---:|---|---|
| AN_ART_BE | AN артефакты (BE): модель/контракты/права | virtual | AN | 1 | A2 | 2026-03-31 | 2026-03-31 | 2026-03-31 | 2026-03-31 | done | 100 | STORY-ARTIFACTS-001 |  |
| BE_ART | BE артефакты (ссылки на документы) - БД + API | virtual | BE | 3 | B2 | 2026-04-01 | 2026-04-03 | 2026-04-01 | 2026-04-03 | done | 100 | STORY-ARTIFACTS-001 |  |
| RSCON-2468 | RSCON-2468 BE Дать доступ к разделу Документы для пользователей | real | BE | 2 | BE3 | 2026-04-28 | 2026-04-29 | 2026-04-28 | 2026-04-29 | done | 100 | STORY-ARTIFACTS-001 | `tasks/RSCON-2468.md` |

## Notes
- Импортировано из `planning/2026-Q2/imported-source/gantt/mvp_gantt_chart_current_actualized_aggressive.puml`.
- При появлении реальных Jira-задач этот реестр нужно materialize-ить без потери связи со story `STORY-ARTIFACTS-001`.

## Legacy references
- `planning/2026-Q2/imported-source/tasks/mvp_tasks_artifacts_core.md`
