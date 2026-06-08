# Implementation tasks

Feature: `../../feature.md`  
Slice: `../slice.md`  
Дата обновления: `2026-06-08`

## Правила
- Summary по возможности совпадает с Jira summary.
- Этот файл является source of truth для execution-данных по данному slice.
- Фактические даты и исполнитель обновляются по мере работы.

## Реестр задач

| Jira | Summary | Kind | Role | Estimate (дн) | Executor | Planned Start | Planned Finish | Actual Start | Actual Finish | Status | Progress % | Related Stories | Details |
|---|---|---|---|---:|---|---|---|---|---|---|---:|---|---|
| AN_AP_CORE | AN процесс согласования/утверждения (BE core) | virtual | AN | 2 | A1 | 2026-04-01 | 2026-04-02 |  |  | superseded | 0 | STORY-APPROVALS-001 |  |
| BE_AP_CORE | BE процесс согласования и утверждения - БД+логика | virtual | BE | 10 | B1 | 2026-04-06 | 2026-04-17 |  |  | superseded | 0 | STORY-APPROVALS-001 |  |
| AN_PILOT_LC_AP | AN ЖЦ пилота: согласование/утверждение (BE) | virtual | AN | 1 | A2 | 2026-04-05 | 2026-04-05 |  |  | superseded | 0 | STORY-APPROVALS-001 |  |
| BE_PILOT_LC_AP | BE ЖЦ пилота - согласование/утверждение | virtual | BE | 5 | B2 | 2026-05-20 | 2026-05-26 |  |  | superseded | 0 | STORY-APPROVALS-001 |  |
| RSCON-2518 | RSCON-2518 BE БД + API + Логика цепочки согласований | real | BE | 5 | TBD_BE | 2026-05-20 | 2026-05-26 |  |  | planned | 0 | STORY-APPROVALS-001 |  |
| RSCON-2519 | RSCON-2519 BE Получение списка пользователей для цепочки согласования | real | BE | 2 | TBD_BE | 2026-05-20 | 2026-05-21 |  |  | planned | 0 | STORY-APPROVALS-001 |  |
| RSCON-2520 | RSCON-2520 BE История изменений для цепочки согласования | real | BE | 4 | TBD_BE | 2026-05-20 | 2026-05-25 |  |  | planned | 0 | STORY-APPROVALS-001 |  |

## Notes
Импортировано из legacy gantt baseline; по входящему actual-progress snapshot 2026-06-08 virtual chunks superseded, active layer переведён на `RSCON-2518..2520`.
