# Current-state requirements overview

Дата обновления: `2026-04-24`

## Что считаем текущим baseline

Система уже покрывает базовый домен управления инициативами и стратегическими изменениями:
- инициативы;
- симуляции;
- пилоты;
- внедрения;
- скоркарты и шаблоны скоркарт;
- approval / ratification;
- пакеты на этапе ratification;
- артефакты как внешние URL;
- RBAC и продуктовые scope-ограничения.

## Coverage matrix

| Область | Статус в baseline | Основные источники | Где нормализовано |
|---|---|---|---|
| Initiatives + core domain backbone | existing | `context/source-materials/current-system/diagrams/raw/spec_domain_model.md`, `context/source-materials/current-system/requirements/raw/docs/faq_stakeholders.md` | `baseline/current/domain/` |
| Simulations | existing | `context/source-materials/legacy/changeswork-full/planning/mvp/current/tasks/legacy/mvp_tasks_simulations_page.md`, `context/source-materials/legacy/changeswork-full/planning/mvp/current/tasks/legacy/mvp_tasks_simulation_detail_page.md`, `context/source-materials/current-system/diagrams/raw/spec_state_machine.puml` | `baseline/current/domain/aggregates/simulation.md`, `baseline/current/ui/simulations.md`, `baseline/current/api/simulations.md` |
| Pilots | existing | `context/source-materials/current-system/requirements/raw/final-spec/REQ_pilots_frontend.md`, `context/source-materials/current-system/requirements/raw/final-spec/REQ_pilots_backend.md` | `baseline/current/domain/aggregates/pilot.md`, `baseline/current/ui/navigation.md`, `baseline/current/api/endpoints.md` |
| Deployments | existing | `context/source-materials/current-system/requirements/raw/final-spec/REQ_deployments_frontend.md`, `context/source-materials/current-system/requirements/raw/final-spec/REQ_deployments_backend.md`, `context/source-materials/current-system/requirements/raw/final-spec/REQ_deployments_backend_db_api.md` | `features/deployments/`, `baseline/current/ui/navigation.md`, `baseline/current/api/endpoints.md`, `baseline/current/data/model-overview.md` |
| Scorecards | existing | `context/source-materials/current-system/requirements/raw/final-spec/REQ_scorecards_frontend.md`, `context/source-materials/current-system/requirements/raw/final-spec/REQ_scorecards_backend.md`, `context/source-materials/current-system/requirements/raw/final-spec/REQ_scorecards_backend.openapi.yaml` | `features/scorecards/`, `baseline/current/api/endpoints.md`, `baseline/current/data/model-overview.md` |
| Approvals + packages | existing | `context/source-materials/current-system/requirements/raw/final-spec/REQ_approval_core.md`, `context/source-materials/current-system/requirements/raw/final-spec/REQ_approvals_page_frontend.md`, `context/source-materials/current-system/requirements/raw/final-spec/REQ_packages_page_frontend.md` | `features/approvals/`, `features/packages/`, `baseline/current/api/endpoints.md`, `baseline/current/ui/navigation.md` |
| Artifacts | existing | `context/source-materials/current-system/requirements/raw/final-spec/REQ_artifacts_core.md` | `features/artifacts/`, `baseline/current/domain/business-rules.md` |
| RBAC | existing | `context/source-materials/current-system/requirements/raw/final-spec/REQ_roles_rbac.md` | `features/roles/`, `baseline/current/domain/contexts/identity-and-access.md` |

## Важная граница

- `features/simulation-bt-agent/` не относится к current baseline; это новая квартальная дельта поверх уже существующей simulation detail page.
- Отсутствие отдельной feature `simulations` в harness не означает отсутствия simulation coverage в deployed-системе.
