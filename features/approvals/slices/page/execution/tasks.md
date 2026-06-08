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
| AN_AP_PAGE_BE | AN страница "Согласования" (BE): контракты/фильтры/действия | virtual | AN | 1 | A1 | 2026-04-06 | 2026-04-06 |  |  | superseded | 0 | STORY-APPROVALS-002 |  |
| BE_AP_PAGE | BE страница "Согласования" - API, логика | virtual | BE | 10 | B1 | 2026-05-07 | 2026-05-20 |  |  | superseded | 0 | STORY-APPROVALS-002 |  |
| AN_AP_PAGE_FE | AN страница "Согласования" (FE): UX/компоненты/edge-cases | virtual | AN | 1 | A2 | 2026-04-07 | 2026-04-07 |  |  | superseded | 0 | STORY-APPROVALS-002 |  |
| FE_AP_PAGE | FE страница "Согласования" | virtual | FE | 10 | F1 | 2026-04-14 | 2026-04-27 |  |  | superseded | 0 | STORY-APPROVALS-002 |  |
| RSCON-2521 | RSCON-2521 FE Цепочка согласования | real | FE | 8 | TBD_FE | 2026-05-25 | 2026-06-04 |  |  | planned | 0 | STORY-APPROVALS-002 |  |

## Notes
Импортировано из legacy baseline и approvals page task docs. По входящему actual-progress snapshot 2026-06-08 virtual chunks superseded, active layer переведён на `RSCON-2521`.
