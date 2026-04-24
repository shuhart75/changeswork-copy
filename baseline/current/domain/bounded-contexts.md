# Bounded Contexts

Дата обновления: `2026-04-23`
Source: `context/source-materials/current-system/diagrams/raw/spec_domain_model.md`

| Context | Purpose | Main objects | Canonical file |
|---|---|---|---|
| Identity and Access | пользователи, роли, scope доступа и назначения | `User`, `UserRole` | `contexts/identity-and-access.md` |
| Product Catalog | каталог продуктов и подпродуктов | `Product`, `SubProduct` | `contexts/product-catalog.md` |
| Scorecard Templates | versioned шаблоны скоркарт | `ScorecardTemplate`, `ScorecardTemplateVersion` | `contexts/scorecard-templates.md` |
| Scorecards | фактические скоркарты и их источники/использование | `Scorecard`, `ScorecardVersion`, `ScorecardSource` | `contexts/scorecards.md` |
| Initiatives | верхнеуровневая группировка изменений | `Initiative` | `contexts/initiatives.md` |
| Research and Execution | фазы жизненного цикла изменения | `Simulation`, `Pilot`, `Deployment` | `contexts/research-and-execution.md` |
| Lineage | ограниченная MVP-трассировка происхождения | `Deployment.lineage_simulation_id` | `contexts/lineage.md` |
| Packages | групповое ratification через пакет | `Package` | `contexts/packages.md` |
| Approval | динамический маршрут approval + ratification | `ApprovalInstance`, stages, assignments | `contexts/approval.md` |

## Boundary notes
- `Scorecards` не являются самостоятельным approval target; они участвуют в доменных версиях `PilotVersion` и `DeploymentVersion`.
- `Packages` не имеют собственного lifecycle enum и не являются target процесса согласования.
- `Lineage` в baseline ограничен `simulation_based` внедрениями и не разворачивается в полную graph-модель.
