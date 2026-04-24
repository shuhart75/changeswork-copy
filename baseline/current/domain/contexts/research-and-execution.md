# Context — Research and Execution

## Purpose
Модель фаз изменения стратегии: исследование, пилот, продуктовое внедрение.

## Main objects
- `Simulation`
- `Pilot` + `PilotVersion`
- `Deployment` + `DeploymentVersion`

## Key rules
- `Simulation` неизменяема после завершения.
- `Pilot` и `Deployment` — логические сущности с versioning; согласование идёт на уровне версий.
- `PilotVersion` должен быть связан минимум с одной `ScorecardVersion`.
- `DeploymentVersion` должен быть связан минимум с одной `ScorecardVersion`.
- У `Deployment` есть immutable `deployment_type`; для `simulation_based` обязательны `lineage_simulation_id` и `required_scorecard_id`.
