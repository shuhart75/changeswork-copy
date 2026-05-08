# Implementation tasks

Feature: `../../feature.md`
Slice: `../slice.md`
Дата обновления: `2026-05-08`

## Правила
- Summary по возможности совпадает с Jira summary.
- Этот файл является source of truth для execution-данных по данному slice.
- Исторический imported coverage по simulation artifacts сохраняется, но новые подтверждённые backlog-задачи фиксируем прямо здесь.

## Реестр задач

| Jira | Summary | Kind | Role | Estimate (дн) | Executor | Planned Start | Planned Finish | Actual Start | Actual Finish | Status | Progress % | Related Stories | Details |
|---|---|---|---|---:|---|---|---|---|---|---|---:|---|---|
| RSCON-2439 | RSCON-2439 FE Раздел Документы СИМУЛЯЦИЯ: добавить артефакты | real | FE | 3 | FE1 | 2026-04-25 | 2026-04-29 | 2026-04-25 | 2026-04-29 | done | 100 | STORY-SIMULATIONS-001 | `tasks/RSCON-2439.md` |
| RSCON-2490 | RSCON-2490 BE Интеграция с ФП Симуляция: создание доков с jiraId при обновлении деталки | real | BE | 1 | B2 | 2026-05-08 | 2026-05-08 | 2026-05-08 | 2026-05-08 | done | 100 | STORY-SIMULATIONS-001 | `tasks/RSCON-2490.md` |

## Notes
- Slice остаётся частью imported existing simulation coverage, но execution-факт по доработке блока документов теперь зафиксирован отдельно.
- `RSCON-2490` добавлена по пользовательскому факту от `2026-05-08`: завершена сегодня, executor `B2`, прогресс `100%`.
- Исторические task docs смотри в `../../references.md` и raw legacy snapshot.
