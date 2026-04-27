# Implementation tasks

Feature: `../../feature.md`  
Slice: `../slice.md`  
Дата обновления: `2026-04-27`

## Правила
- Summary по возможности совпадает с Jira summary.
- Этот файл является source of truth для execution-данных по данному slice.
- Для `pilots` здесь собраны только те execution items, которые явно выделены в actualized legacy gantt; полный imported workspace scope пока не разложен на более мелкие stories.

## Реестр задач

| Jira | Summary | Kind | Role | Estimate (дн) | Executor | Planned Start | Planned Finish | Actual Start | Actual Finish | Status | Progress % | Related Stories | Details |
|---|---|---|---|---:|---|---|---|---|---|---|---:|---|---|
| AN_FE_PILOT_ART | AN блок артефактов (FE): пилоты | virtual | AN | 1 | A2 | 2026-04-01 | 2026-04-01 | 2026-04-01 | 2026-04-01 | done | 100 | STORY-PILOTS-001 |  |
| FE_PILOT_ART | FE пилоты - блок артефакты + UI под ЖЦ | virtual | FE | 4 | F1 | 2026-04-06 | 2026-04-09 | 2026-04-06 | 2026-04-09 | done | 100 | STORY-PILOTS-001 |  |
| AN_PILOT_LC_AP | AN ЖЦ пилота: согласование/утверждение (BE) | virtual | AN | 1 | A3 | 2026-04-01 | 2026-04-01 | 2026-04-01 | 2026-04-01 | done | 100 | STORY-PILOTS-001 |  |
| BE_PILOT_LC_AP | BE ЖЦ пилота - согласование/утверждение | virtual | BE | 5 | B2 | 2026-05-19 | 2026-05-23 |  |  | planned | 0 | STORY-PILOTS-001 |  |

## Notes
- Реестр отражает только pilot-centric execution из legacy actualized gantt. Задачи по scorecards, trace и notifications, влияющие на пилоты косвенно, остаются в своих feature/cross-cutting пакетах.

## Legacy references
- `planning/mvp/current/tasks/legacy/mvp_tasks_pilots_page.md`
- `planning/mvp/current/tasks/legacy/mvp_tasks_pilot_form.md`
- `planning/mvp/current/tasks/legacy/mvp_tasks_pilot_detail_page.md`
- `planning/2026-Q2/imported-source/gantt/mvp_gantt_chart_current_actualized_aggressive.puml`
