# Context — Lineage

## Purpose
Минимально необходимая MVP-трассировка происхождения для `simulation_based` внедрений.

## Main objects
- `Deployment.lineage_simulation_id`

## Key rules
- Lineage не является CRUD-сущностью.
- В MVP lineage существует только для `Deployment` типа `simulation_based`.
- Для одного внедрения допустима только одна lineage-симуляция.
- Эта симуляция должна совпадать с источником обязательной lineage-скоркарты.
- Полная рекурсивная цепочка `Simulation -> Pilot -> Deployment` остаётся целевой архитектурой следующих итераций.
