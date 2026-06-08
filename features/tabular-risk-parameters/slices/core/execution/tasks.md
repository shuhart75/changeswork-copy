# Implementation tasks

Feature: `../../feature.md`  
Slice: `../slice.md`  
Дата обновления: `2026-06-08`

## Правила
- Summary по возможности совпадает с Jira summary.
- Этот файл является source of truth для execution-данных по данному slice.
- Legacy generic блок `BE_RISK_TABLE` / `FE_RISK_TABLE` materialized в реальные backlog-задачи `RSCON-*`.

## Реестр задач

| Jira | Summary | Kind | Role | Estimate (дн) | Executor | Planned Start | Planned Finish | Actual Start | Actual Finish | Status | Progress % | Related Stories | Details |
|---|---|---|---|---:|---|---|---|---|---|---|---:|---|---|
| RSCON-2430 | RSCON-2430 BE Табличные риск-параметры: API, БД, логика | real | BE | 3 | BE2 | 2026-04-17 | 2026-04-20 | 2026-04-17 | 2026-04-20 | done | 100 | STORY-TABULAR-RISK-PARAMETERS-001 | `tasks/RSCON-2430.md` |
| RSCON-2432 | RSCON-2432 BE Интеграция с ФП Симуляция: доработать передачу табличных РП при запуске симуляции | real | BE | 3 | B2 | 2026-04-27 | 2026-04-29 | 2026-05-06 | 2026-05-07 | done | 100 | STORY-TABULAR-RISK-PARAMETERS-001 | `tasks/RSCON-2432.md` |
| RSCON-2452 | RSCON-2452 BE Табличные риск-параметры - шедулер очистки файлов | real | BE | 3 | FE2 | 2026-04-29 | 2026-05-04 | 2026-04-29 | 2026-05-04 | done | 100 | STORY-TABULAR-RISK-PARAMETERS-001 | `tasks/RSCON-2452.md` |
| RSCON-2429 | RSCON-2429 FE Переделка формы для изменения риск-параметров | real | FE | 10 | FE1 | 2026-04-20 | 2026-05-04 | 2026-04-20 | 2026-04-27 | done | 100 | STORY-TABULAR-RISK-PARAMETERS-002 | `tasks/RSCON-2429.md` |
| QA_TABULAR_RISK_PARAMETERS | QA Табличные риск-параметры | virtual | QA | 4 | Q1 | 2026-05-04 | 2026-05-07 | 2026-05-04 | 2026-05-08 | done | 100 | STORY-TABULAR-RISK-PARAMETERS-002 | `tasks/QA_TABULAR_RISK_PARAMETERS.md` |

## Notes
Импортировано из `mvp_gantt_chart_current_actualized_aggressive.puml` и user updates по `RSCON-2452`.
`RSCON-2431` удалена из execution-слоя по пользовательскому уточнению: эта работа была фактически выполнена в рамках `RSCON-2430`.
`RSCON-2429` закрыта фактом `2026-04-27`; виртуальный QA-хвост `QA_TABULAR_RISK_PARAMETERS` стартует `2026-05-04`, потому что QA-задачи в этом контуре должны начинаться после завершения FE-потока.
Новый backlog `RSCON-2452` продолжает тот же backend-stream табличных РП и не выносится в отдельную feature.
`RSCON-2432` обновлена по пользовательскому факту от `2026-05-08`: завершена `2026-05-07` со 100% прогресса; исполнитель нормализован как `B2` по ранее зафиксированному назначению на `BE2`.
`QA_TABULAR_RISK_PARAMETERS` обновлена по входящему actual-progress snapshot: завершена `2026-05-08`.

## Legacy references
- `planning/2026-Q2/imported-source/tasks/mvp_tasks_list_no_analytics.md`
- `planning/2026-Q2/imported-source/gantt/mvp_gantt_chart_current_actualized_aggressive.puml`
- `context/source-materials/legacy/changeswork-full/planning/mvp/versions/v6.37/taskjuggler/status/interactive_status_2026-04-20.md`
