# Cross-cutting streams — 2026-Q2

Дата обновления: `2026-04-24`
Статус: **нормализовано из legacy planning**

## Зачем этот слой нужен

Некоторые куски legacy-плана не являются отдельными бизнес-фичами, но при этом занимали самостоятельные дорожки в gantt и влияли сразу на несколько feature lanes.

В `changesWork` это были прежде всего:
- `notifications`;
- `trace` / блок `Связанные сущности`.

Если оставить их только в raw gantt и task docs, теряется управленческий смысл: почему это были отдельные задачи, какие у них были deliverables и где их следы в feature-level материалах.

## Что внутри

| Stream | Legacy tasks | Где проявляется в новой структуре |
|---|---|---|
| `notifications.md` | `AN_NOT`, `BE_NOT`, `mvp_tasks_notifications.md` | approval/package/pilot/deployment сценарии, QA phase 3, final MVP QA |
| `trace.md` | `AN_TRACE_BE`, `BE_TRACE`, `AN_TRACE_FE`, `FE_TRACE`, `QA_TRACE`, `mvp_tasks_chains_page.md` | related-entities blocks в `features/simulations/`, `features/pilots/`, `features/deployments/`, lineage boundary в `baseline/current/domain/contexts/lineage.md` |

## Практическое правило

- Если речь о delivered/user-facing требованиях конкретной области — идём в `features/`.
- Если нужно понять, почему отдельный сквозной поток вообще был в квартальном плане — идём сюда.
- Для исторической детализации и точных исходных формулировок используем `planning/2026-Q2/imported-source/` и raw legacy snapshot.
