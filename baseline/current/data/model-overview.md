# Current-state data model overview

Дата обновления: `2026-04-24`

## Domain -> storage map

| Aggregate / concept | Основные persisted сущности | Ключевые замечания | Источники |
|---|---|---|---|
| `Initiative` | `initiative`, связки с `sub_product` | корневой контейнер для `Simulation`, `Pilot`, `Deployment` | `context/source-materials/current-system/diagrams/raw/spec_domain_model.md` |
| `Simulation` | `simulation` | хранит результаты как JSONB; не участвует в approval flow | `context/source-materials/current-system/diagrams/raw/spec_domain_model.md`, `context/source-materials/legacy/changeswork-full/planning/mvp/current/tasks/legacy/mvp_tasks_simulation_lifecycle.md` |
| `Pilot` + `PilotVersion` | `pilot`, `pilot_version` | версии пилота являются approval target | `context/source-materials/current-system/requirements/raw/final-spec/REQ_pilots_backend.md` |
| `Deployment` + `DeploymentVersion` | `deployment`, `deployment_version` | immutable `deployment_type`; для `simulation_based` обязателен `lineage_simulation_id` | `context/source-materials/current-system/requirements/raw/final-spec/REQ_deployments_backend_db_api.md` |
| `Scorecard` + `ScorecardVersion` | `scorecard`, `scorecard_version` | конфигурация и financial effects живут в версии; источники и usage отдельно | `context/source-materials/current-system/requirements/raw/final-spec/REQ_scorecards_backend.md` |
| `ScorecardTemplateVersion` | `scorecard_template`, `scorecard_template_version` | `default_config` содержит структуру полей, default values и criticality thresholds | `context/source-materials/current-system/requirements/raw/final-spec/REQ_scorecards_backend.md` |
| `ScorecardSource` | `scorecard_source` | в MVP поддержан source type `simulation` | `context/source-materials/current-system/requirements/raw/final-spec/REQ_scorecards_backend.md` |
| Usage links | M:N таблицы между `scorecard_version` и `pilot_version` / `deployment_version` | изменение связей перевыпускает доменные версии | `context/source-materials/current-system/requirements/raw/final-spec/REQ_scorecards_backend.md` |
| `ApprovalInstance` + stages | approval-related таблицы | процессный статус живёт отдельно от доменных версий | `context/source-materials/current-system/requirements/raw/final-spec/REQ_approval_core.md` |
| `Package` | package-level grouping + links to `ApprovalInstance` | пакет не имеет собственного status enum | `context/source-materials/current-system/requirements/raw/final-spec/REQ_approval_core.md` |
| Artifacts | artifact / external link storage | URL-only, без file upload | `context/source-materials/current-system/requirements/raw/final-spec/REQ_artifacts_core.md` |
| Access model | user / role / role-space mapping | product-bound roles coexist with global approver/ratifier/admin | `context/source-materials/current-system/requirements/raw/final-spec/REQ_roles_rbac.md` |

## JSON / derived fields

- `Simulation.results` — JSONB с результатами анализа.
- `ScorecardVersion.config` — JSONB-конфигурация скоркарты.
- `ScorecardVersion.financial_effects` — JSONB с расчётными эффектами.
- `ScorecardTemplateVersion.default_config` — JSONB со схемой формы и порогами критичности.
- Derived aggregate statuses (`Initiative`, `Scorecard`) не должны подменять process-status источники вроде `ApprovalInstance`.

## Специальные инварианты хранения

- `Deployment.deployment_type` после первого успешного сохранения становится неизменяемым.
- Для `deployment_type = simulation_based` обязательны `lineage_simulation_id` и `required_scorecard_id`.
- Удаление последней скоркарты из `Pilot` или `Deployment` автоматически требует создания новой default-based скоркарты.
- Симуляция после `completed`/`failed` рассматривается как immutable.
