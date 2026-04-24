# Implementation tasks

Feature: `../../feature.md`  
Slice: `../slice.md`  
Дата обновления: `2026-04-23`

## Правила
- Summary по возможности совпадает с Jira summary.
- Этот файл является source of truth для execution-данных по данному slice.
- Для `scorecards` фактический execution-слой уже переведён на реальные Jira-задачи `RSCON-*`.

## Реестр задач

| Jira | Summary | Kind | Role | Estimate (дн) | Executor | Planned Start | Planned Finish | Actual Start | Actual Finish | Status | Progress % | Related Stories | Details |
|---|---|---|---|---:|---|---|---|---|---|---|---:|---|---|
| RSCON-2339 | RSCON-2339 FE Удаление блока метрик + новая вкладка для скоркарт | real | FE | 1 | TBD_FE | 2026-04-22 | 2026-04-22 |  |  | planned | 0 | STORY-SCORECARDS-002 | `tasks/RSCON-2339.md` |
| RSCON-2340 | RSCON-2340 FE Создание скоркарты (вручную) + наполнение вкладки скоркарт | real | FE | 10 | F2 | 2026-04-08 | 2026-04-21 | 2026-04-08 | 2026-04-21 | done | 100 | STORY-SCORECARDS-002, STORY-SCORECARDS-003 | `tasks/RSCON-2340.md` |
| RSCON-2341 | RSCON-2341 FE Прикрепление существующей скоркарты | real | FE | 4 | TBD_FE | 2026-04-23 | 2026-04-28 |  |  | planned | 0 | STORY-SCORECARDS-003 | `tasks/RSCON-2341.md` |
| RSCON-2342 | RSCON-2342 BE Оценка критичности + шаблоны для скоркарт | real | BE | 4 | B3 | 2026-04-07 | 2026-04-10 | 2026-04-07 | 2026-04-10 | done | 100 | STORY-SCORECARDS-001 | `tasks/RSCON-2342.md` |
| RSCON-2343 | RSCON-2343 BE Сущность скоркарты | real | BE | 5 | B2 | 2026-04-03 | 2026-04-09 | 2026-04-03 | 2026-04-09 | done | 100 | STORY-SCORECARDS-001 | `tasks/RSCON-2343.md` |
| RSCON-2344 | RSCON-2344 BE Привязка скоркарты | real | BE | 1 | B2 | 2026-04-10 | 2026-04-10 | 2026-04-10 | 2026-04-10 | done | 100 | STORY-SCORECARDS-003 | `tasks/RSCON-2344.md` |

## Notes
Импортировано из `mvp_gantt_chart_current_actualized_aggressive.puml`. Отдельная list page скоркарт в текущем MVP исключена, поэтому execution-слой привязан к workspace/detail/form/binding-сценариям.

## Legacy references
- `planning/mvp/current/tasks/legacy/mvp_tasks_scorecard_detail_page.md`
- `planning/mvp/current/tasks/legacy/mvp_tasks_scorecard_form.md`
- `planning/mvp/current/tasks/legacy/mvp_tasks_scorecards_page.md`
