# Implementation tasks

Feature: `../../feature.md`
Slice: `../slice.md`
Дата обновления: `2026-06-08`

## Правила
- Summary по возможности совпадает с Jira summary.
- Этот файл является source of truth для execution-данных по фактическому слою конфигурации пилотов в `simulations`.
- Tasks импортированы из входящего actual-progress snapshot; не начатые задачи остаются без actual dates, чтобы генератор сам сдвигал их при пересборке.

## Реестр задач

| Jira | Summary | Kind | Role | Estimate (дн) | Executor | Planned Start | Planned Finish | Actual Start | Actual Finish | Status | Progress % | Related Stories | Details |
|---|---|---|---|---:|---|---|---|---|---|---|---:|---|---|
| AN_SIM_ART | AN Симуляция конфигурации пилотов | virtual | AN | 2 | A2 | 2026-05-04 | 2026-05-05 | 2026-05-04 | 2026-05-05 | done | 100 | STORY-SIMULATIONS-002 |  |
| RSCON-2473 | RSCON-2473 BE Доработки по симуляции (логика + апи) для симуляции конфига пилотов | real | BE | 5 | B2 | 2026-05-12 | 2026-05-18 | 2026-05-12 | 2026-05-18 | done | 100 | STORY-SIMULATIONS-002 |  |
| RSCON-2501 | RSCON-2501 BE Симуляция конфигурации пилотов. RSCON-CONFIG. Выдать АПИ | real | BE | 2 | B2 | 2026-05-13 | 2026-05-14 | 2026-05-13 | 2026-05-14 | done | 100 | STORY-SIMULATIONS-002 |  |
| RSCON-2472 | RSCON-2472 FE Симуляция конфигурации пилотов | real | FE | 6 | F1 | 2026-05-15 | 2026-05-22 | 2026-05-15 | 2026-05-26 | done | 100 | STORY-SIMULATIONS-002 |  |
| RSCON-2474 | RSCON-2474 BE Симуляция конфига пилотов. Интеграция с ФП Симуляция: запуск, деталка | real | BE | 3 | TBD_BE | 2026-05-27 | 2026-05-29 | 2026-05-24 | 2026-05-26 | done | 100 | STORY-SIMULATIONS-002 |  |
| RSCON-2475 | RSCON-2475 BE Симуляция конфигурации пилотов. RSCON-CONFIG | real | BE | 4 | TBD_BE | 2026-06-01 | 2026-06-04 | 2026-05-16 | 2026-05-21 | done | 100 | STORY-SIMULATIONS-002 |  |
| RSCON-2471 | RSCON-2471 FE Уведомления в пилотах о симуляции | real | FE | 2 | TBD_FE | 2026-06-01 | 2026-06-02 | 2026-05-27 | 2026-05-28 | done | 100 | STORY-SIMULATIONS-002 |  |
| RSCON-2488 | RSCON-2488 BE Новый метод апи для симуляции конифугарации пилотов | real | BE | 1 | TBD_BE | 2026-06-02 | 2026-06-02 | 2026-05-13 | 2026-05-13 | done | 100 | STORY-SIMULATIONS-002 |  |
| QA_SIM_CONFIG | QA Симуляция конфигурации пилотов | virtual | QA | 10 | Q1 | 2026-06-05 | 2026-06-19 |  |  | planned | 0 | STORY-SIMULATIONS-002 |  |

## Notes
Импортировано из входящего actual-progress snapshot 2026-06-08 и дополнено фактами завершения от 2026-06-09 по `RSCON-2474`, `RSCON-2475`, `RSCON-2488`, `RSCON-2471`, `RSCON-2472`.
