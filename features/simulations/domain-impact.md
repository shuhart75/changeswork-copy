# Domain Impact — Simulations

Decision ID: `SIM-BASELINE-LEGACY-NORMALIZATION-2026-04-24`
Статус: `accepted`
Impact: `cross-feature`

## Что фиксируем
- `Simulation` — существующий агрегат baseline, а не новая feature-добавка.
- Simulation scope влияет на `Scorecard`, `Pilot`, `Deployment`, `Artifacts` и `RBAC`.
- Detail page симуляции является host screen для будущих дельт, в частности для `simulation-bt-agent`.

## Affected baseline artifacts
- `baseline/current/domain/aggregates/simulation.md`
- `baseline/current/ui/simulations.md`
- `baseline/current/api/simulations.md`
- `baseline/current/data/model-overview.md`

## Affected features
- `features/scorecards/`
- `features/pilots/`
- `features/deployments/`
- `features/artifacts/`
- `features/simulation-bt-agent/`

## Prototype impact
- Existing simulation prototypes are tracked in raw legacy materials only.
- No mandatory prototype refresh is required as part of this normalization pass.

## Consistency notes
- Не трактовать отсутствие отдельной planning-story структуры как отсутствие уже deployed simulation behavior.
- Любая новая simulation-доработка должна явно ссылаться на этот baseline container.
