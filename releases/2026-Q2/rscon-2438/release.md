# Release — RSCON-2438

Квартал: `2026-Q2`
Дата обновления: `2026-05-04`
Статус: `draft`

## Scope
Релиз собирает подтверждённый execution scope по табличным риск-параметрам, блоку артефактов симуляции и скоркартам. Состав зафиксирован по user update и текущим execution facts.

## Included features
- `features/tabular-risk-parameters/`
- `features/simulations/`:
  slice `artifacts-related`, задача `RSCON-2439`
- `features/scorecards/`:
  workspace-slice, задачи `RSCON-2339`, `RSCON-2340`, `RSCON-2341`, `RSCON-2342`, `RSCON-2343`, `RSCON-2344`

## Included execution tasks
- Все execution-задачи feature `tabular-risk-parameters`: `RSCON-2429`, `RSCON-2430`, `RSCON-2431`, `RSCON-2432`, `RSCON-2452`
- `RSCON-2439` — артефакты на detail-странице симуляции
- `RSCON-2339`, `RSCON-2340`, `RSCON-2341`, `RSCON-2342`, `RSCON-2343`, `RSCON-2344` — контур скоркарт

## Release milestone
- Плановая отметка релиза: `2026-05-21`

## Final requirements sources
- `features/tabular-risk-parameters/slices/core/requirements/`
- `features/simulations/slices/artifacts-related/requirements/`
- `features/scorecards/slices/workspace/requirements/`
- `features/tabular-risk-parameters/domain-impact.md`
- `features/simulations/domain-impact.md`
- `features/scorecards/domain-impact.md`
- `planning/2026-Q2/gantt/actual-progress.puml`

## Domain promotion summary
В релиз необходимо собрать финальные изменения по табличным риск-параметрам, simulation artifacts и scorecards, затем промоутить их в `baseline/current/`.

## Promoted baseline version
Пока не зафиксировано.
