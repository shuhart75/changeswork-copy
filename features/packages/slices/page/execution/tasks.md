# Implementation tasks

Feature: `../../feature.md`  
Slice: `../slice.md`  
Дата обновления: `2026-04-23`

## Правила
- Summary по возможности совпадает с Jira summary.
- Этот файл является source of truth для execution-данных по данному slice.
- Пока реальные Jira-задачи для `packages` не зафиксированы, используем virtual execution items из legacy actualized gantt.

## Реестр задач

| Jira | Summary | Kind | Role | Estimate (дн) | Executor | Planned Start | Planned Finish | Actual Start | Actual Finish | Status | Progress % | Related Stories | Details |
|---|---|---|---|---:|---|---|---|---|---|---|---:|---|---|
| AN_PKG_BE | AN страница Пакеты (BE): контракты и массовые действия | virtual | AN | 1 | A3 | 2026-04-09 | 2026-04-09 | 2026-04-09 |  | in_progress | 80 | STORY-PACKAGES-001 |  |
| AN_PKG_FE | AN страница Пакеты (FE): UX, компоненты и edge cases | virtual | AN | 1 | A3 | 2026-04-10 | 2026-04-10 | 2026-04-10 |  | in_progress | 80 | STORY-PACKAGES-001 |  |
| FE_PKG_PAGE | FE страница Пакеты | virtual | FE | 10 | F2 | 2026-04-22 | 2026-05-06 |  |  | planned | 0 | STORY-PACKAGES-001 |  |

## Notes
Импортировано из `mvp_gantt_chart_current_actualized_aggressive.puml`. Реальных Jira-ключей по `packages` в snapshot пока нет, поэтому на actual-progress отображаются virtual execution items.

## Legacy references
- `planning/mvp/current/tasks/legacy/mvp_tasks_packages_page.md`
