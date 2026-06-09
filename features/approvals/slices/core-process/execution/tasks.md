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
| RSCON-2649 | RSCON-2649 BE API для согласований | real | BE | 3 | B3 | 2026-06-03 | 2026-06-05 | 2026-06-03 | 2026-06-05 | done | 100 | STORY-APPROVALS-001 | Факт закрытия зафиксирован 2026-06-08; точные даты не были переданы, задача разложена как 3 рабочих дня до старта RSCON-2630. |
| RSCON-2629 | RSCON-2629 BE Получение справочника согласующих и утверждающих | real | BE | 3 | TBD_BE | 2026-06-08 | 2026-06-10 |  |  | planned | 0 | STORY-APPROVALS-001 |  |
| RSCON-2630 | RSCON-2630 BE БД для согласования | real | BE | 3 | B3 | 2026-06-08 | 2026-06-10 | 2026-06-08 |  | in_progress | 20 | STORY-APPROVALS-001 | Started today. |
| RSCON-2631 | RSCON-2631 BE Сохранение документа | real | BE | 2 | TBD_BE | 2026-06-08 | 2026-06-09 |  |  | planned | 0 | STORY-APPROVALS-001 |  |
| RSCON-2633 | RSCON-2633 BE Отправка документа в SberDocs | real | BE | 3 | TBD_BE | 2026-06-08 | 2026-06-10 |  |  | planned | 0 | STORY-APPROVALS-001 |  |
| RSCON-2634 | RSCON-2634 BE Polling из SberDocs и комбинация статусов | real | BE | 3 | TBD_BE | 2026-06-08 | 2026-06-10 |  |  | planned | 0 | STORY-APPROVALS-001 |  |
| RSCON-2635 | RSCON-2635 BE HTML preview и отправка письма | real | BE | 3 | TBD_BE | 2026-06-08 | 2026-06-10 |  |  | planned | 0 | STORY-APPROVALS-001 |  |

## Notes
По входящему actual-progress snapshot 2026-06-08 прежние virtual chunks и старый набор `RSCON-2518..2520` исключены из active registry. Scope закрывается реальными задачами `RSCON-2629..2635` и `RSCON-2649`.
