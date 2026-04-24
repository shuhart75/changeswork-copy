# Context — Lineage

Дата обновления: `2026-04-24`

## Purpose
Минимально необходимая MVP-трассировка происхождения для `simulation_based` внедрений и связанных с ними scorecard-driven связей.

## Main objects
- `Deployment.lineage_simulation_id`
- обязательная lineage-скоркарта у `Deployment`
- best-effort source preview в формах `Pilot` / `Deployment`

## Key rules
- Lineage не является CRUD-сущностью.
- В MVP lineage существует только для `Deployment` типа `simulation_based`.
- Для одного внедрения допустима только одна lineage-симуляция.
- Эта симуляция должна совпадать с источником обязательной lineage-скоркарты.
- Полная рекурсивная цепочка `Simulation -> Pilot -> Deployment` остаётся целевой архитектурой следующих итераций.

## Explicit boundary from legacy planning
- Страница `Цепочки` как отдельный экран не входит в MVP.
- Отдельный lineage widget тоже не считается обязательным поставляемым экраном.
- Вместо этого допустим ограниченный preview источников в формах `Pilot` и `Deployment` на основе выбранных scorecards.
- Preview не должен блокировать сохранение и может работать как best-effort API.
