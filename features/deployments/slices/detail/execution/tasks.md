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
| AN-CHD1 | AN детальная страница Внедрения | virtual | AN | 5 | A3 | 2026-04-21 | 2026-04-25 | 2026-05-08 | 2026-05-08 | done | 100 | STORY-DEPLOYMENTS-005 | Выполнено в рамках других задач. |
| RSCON-2347 | RSCON-2347 FE детальная внедрения | real | FE | 5 | TBD_FE | 2026-04-13 | 2026-04-17 | 2026-04-13 | 2026-05-14 | done | 100 | STORY-DEPLOYMENTS-005 | `tasks/RSCON-2347.md` |
| FE-CHD1 | FE детальная страница Внедрения | virtual | FE | 5 | TBD_FE | 2026-04-28 | 2026-05-05 |  |  | superseded | 0 | STORY-DEPLOYMENTS-005 |  |
| RSCON-2449 | RSCON-2449 BE Связь внедрения и скоркарт | real | BE | 2 | B3 | 2026-05-13 | 2026-05-14 | 2026-05-08 | 2026-05-08 | done | 100 | STORY-DEPLOYMENTS-005 | `tasks/RSCON-2449.md` |

## Notes
Для detail slice в legacy есть отдельные task docs, но в actualized gantt отражена только FE backlog-задача `RSCON-2347`.

`AN-CHD1` отмечена выполненной `2026-05-08` как аналитический объём, закрытый внутри других задач detail scope.

`BE-CHD1`, `RSCON-2450` и `RSCON-2440` убраны из active registry: пользователь подтвердил, что этот объём выполнен в рамках других задач и отдельными execution items больше не отслеживается.

`RSCON-2347` и `RSCON-2449` обновлены по входящему actual-progress snapshot: обе задачи завершены.
