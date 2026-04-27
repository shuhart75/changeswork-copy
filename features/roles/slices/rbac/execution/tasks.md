# Implementation tasks

Feature: `../../feature.md`  
Slice: `../slice.md`  
Дата обновления: `2026-04-27`

## Правила
- Summary по возможности совпадает с Jira summary.
- Этот файл является source of truth для execution-данных по данному slice.
- Для RBAC в imported snapshot отдельно зафиксирован analyst task, а фактический FE/BE enforcement размазан по доменным features и должен проверяться через consistency sweep.

## Реестр задач

| Jira | Summary | Kind | Role | Estimate (дн) | Executor | Planned Start | Planned Finish | Actual Start | Actual Finish | Status | Progress % | Related Stories | Details |
|---|---|---|---|---:|---|---|---|---|---|---|---:|---|---|
| AN_ROLES | AN новые роли: роли/права/матрица | virtual | AN | 1 | A1 | 2026-03-30 | 2026-03-30 | 2026-03-30 | 2026-03-30 | done | 100 | STORY-ROLES-001 |  |

## Notes
- FE/BE-задачи, которые реально применяют RBAC, живут в `approvals`, `packages`, `pilots`, `deployments`, `scorecards` и должны ссылаться на `features/roles/requirements.md` как на контрольный слой.

## Legacy references
- `planning/2026-Q2/imported-source/tasks/mvp_tasks_projectlibre_alignment.md`
- `planning/2026-Q2/imported-source/gantt/mvp_gantt_chart_current_actualized_aggressive.puml`
