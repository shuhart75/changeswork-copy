# Aggregate — Deployment

## Purpose
Продуктовое внедрение стратегии с версионированием через `DeploymentVersion`.

## Versioning
- `Deployment` — логическая сущность.
- Изменения выполняются через новую `DeploymentVersion`.
- Агрегат хранит `latest_version` и `production_version`.

## Invariants
- принадлежит одной `Initiative`;
- каждая версия связана минимум с одной `ScorecardVersion`;
- immutable `deployment_type` = `general` или `simulation_based`;
- для `simulation_based` обязательны `lineage_simulation_id` и `required_scorecard_id`;
- у агрегата может быть только одна активная продуктивная версия.

## Version fields
- `name`
- `goal`
- `change_description`
- `application_perimeter`

## Status model for `DeploymentVersion`
- `draft`
- `in_approval`
- `approved`
- `awaiting_ratification`
- `in_ratification`
- `ratified`
- `approval_rejected`
- `ratification_rejected`
- `approval_cancelled`
- `ratification_cancelled`
- `deployed`
- `rolled_back`
- `archived`
