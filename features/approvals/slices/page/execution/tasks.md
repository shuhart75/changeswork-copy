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
| RSCON-2636 | RSCON-2636 FE Карточка новой сущности, новая вкладка и экшены | real | FE | 10 | F2 | 2026-06-11 | 2026-06-25 | 2026-06-09 |  | in_progress | 0 | STORY-APPROVALS-002 |  |
| QA-APPROVALS-CARD | QA Карточка новой сущности, новая вкладка и экшены | real | QA | 4 | TBD_QA | 2026-06-26 | 2026-07-01 |  |  | planned | 0 | STORY-APPROVALS-002 | QA-задача без Jira-id во входящем списке; должна стартовать сразу после завершения `RSCON-2636`. |
| RSCON-2637 | RSCON-2637 FE Превью Email | real | FE | 5 | TBD_FE | 2026-06-26 | 2026-07-02 |  |  | planned | 0 | STORY-APPROVALS-002 |  |
| QA-APPROVALS-EMAIL-PREVIEW | QA Превью Email | real | QA | 2 | TBD_QA | 2026-07-03 | 2026-07-06 |  |  | planned | 0 | STORY-APPROVALS-002 | QA-задача без Jira-id во входящем списке; должна стартовать сразу после завершения `RSCON-2637`. |

## Notes
По входящему actual-progress snapshot 2026-06-08 прежние virtual chunks и старый `RSCON-2521` исключены из active registry. Scope закрывается реальными FE/QA задачами `RSCON-2636`, `RSCON-2637`, `QA-APPROVALS-CARD`, `QA-APPROVALS-EMAIL-PREVIEW`.

`RSCON-2636` переведена в `in_progress` с фактическим стартом `2026-06-09`, исполнитель `F2`.
