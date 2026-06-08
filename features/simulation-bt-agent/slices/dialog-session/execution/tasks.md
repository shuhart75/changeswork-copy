# Implementation tasks

Feature: `../../feature.md`  
Slice: `../slice.md`  
Дата обновления: `2026-06-08`

## Правила
- Summary по возможности совпадает с Jira summary.
- Этот файл является source of truth для execution-данных по feature-level backlog `simulation-bt-agent`, пока реальные задачи заведены крупнее semantic slices.
- Mapping к planning stories остаётся `inferred`, потому что текущие FE/BE задачи покрывают сразу entrypoint, dialog-session и BT-publication.

## Реестр задач

| Jira | Summary | Kind | Role | Estimate (дн) | Executor | Planned Start | Planned Finish | Actual Start | Actual Finish | Status | Progress % | Related Stories | Details |
|---|---|---|---|---:|---|---|---|---|---|---|---:|---|---|
| RSCON-2479 | RSCON-2479 BE агент AI - БТ по симуляции | real | BE | 4 | BE1 | 2026-05-04 | 2026-05-07 | 2026-05-04 |  | in_progress | 0 | STORY-SIMULATION-BT-AGENT-001, STORY-SIMULATION-BT-AGENT-002, STORY-SIMULATION-BT-AGENT-003 | `tasks/RSCON-2479.md` |
| RSCON-2480 | RSCON-2480 FE агент AI - БТ по симуляции | real | FE | 10 | FE1 | 2026-04-28 | 2026-05-13 | 2026-04-28 | 2026-05-15 | done | 100 | STORY-SIMULATION-BT-AGENT-001, STORY-SIMULATION-BT-AGENT-002, STORY-SIMULATION-BT-AGENT-003 | `tasks/RSCON-2480.md` |
| QA_SIM_BT_AGENT | QA агент AI - БТ по симуляции | virtual | QA | 5 | Q1 | 2026-05-14 | 2026-05-20 |  |  | planned | 0 | STORY-SIMULATION-BT-AGENT-003 | `tasks/QA_SIM_BT_AGENT.md` |

## Notes
- `RSCON-2479` передана исполнителю `BE1`; фактический старт зафиксирован датой `2026-05-04`, прогресс пока остаётся `0%`.
- QA-задача пока остаётся виртуальной и начинается после планового завершения frontend-потока.
- `RSCON-2480` обновлена по входящему actual-progress snapshot: завершена `2026-05-15`.
