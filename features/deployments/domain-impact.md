# Domain Impact — deployments

Дата обновления: `2026-04-23`
Baseline target: `baseline/current/domain/`

## Decision registry

| Decision ID | Summary | Status | Consistency level | Source | Supersedes | Reverted by |
|---|---|---|---|---|---|---|
| DEC-2026-04-23-DEPLOYMENTS-001 | `simulation_based` deployment требует `lineage_simulation_id` и обязательную lineage-скоркарту | accepted | domain-wide | `features/deployments/slices/workspace/requirements/backend.md` |  |  |

## Changed bounded contexts
- `Research and Execution`
- `Lineage`
- `Approval`

## New or changed aggregates
- `Deployment` с versioning на уровне `DeploymentVersion`

## New or changed entities
- `DeploymentVersion`

## Business rules and invariants
- immutable `deployment_type`
- для `simulation_based` обязательны `lineage_simulation_id` и `required_scorecard_id`
- только одна активная продуктивная версия deployment
- критичность версии = максимум по связанным скоркартам

## State transitions
- `DeploymentVersion`: от `draft` до `deployed/rolled_back/archived` через approval + ratification

## API and integration impact
- submit/recall/deploy/rollback flows
- связи со скоркартами и lineage

## Affected requirements

| Path | Impact | Sync status |
|---|---|---|
| `features/deployments/slices/workspace/requirements/backend.md` | Основной контракт deployment version и lineage | propagated |
| `features/scorecards/slices/workspace/requirements/backend.md` | Правило `required_scorecard_id` и ограничения на удаление связи | open |
| `features/deployments/slices/workspace/requirements/frontend.md` | UI-представление lineage и deployment type | open |

## Affected baseline artifacts

| Path | Impact | Sync status |
|---|---|---|
| `baseline/current/domain/contexts/research-and-execution.md` | canonical rule for `Deployment` aggregate | propagated |
| `baseline/current/domain/contexts/lineage.md` | MVP lineage semantics | propagated |
| `baseline/current/domain/aggregates/deployment.md` | aggregate invariants and versioning | propagated |
| `baseline/current/domain/state-machines/README.md` | lifecycle summary | propagated |

## Affected prototypes

### Scope prototypes
| Path | Impact | Sync status |
|---|---|---|
| `features/deployments/planning/scope-prototype/prototype.html` | Может потребоваться явный simulation-based сценарий и пояснение по lineage | defer-ok |

### Delivery prototypes
| Path | Impact | Sync status |
|---|---|---|
| `features/deployments/slices/detail/delivery-prototype/prototype.html` | lineage field and required scorecard visualization | defer-ok |
| `features/deployments/slices/workspace/delivery-prototype/prototype.html` | entry points to simulation-based flow | defer-ok |

## Required consistency actions
- [x] local feature requirements updated
- [ ] neighboring feature requirements updated or backlog item created
- [x] domain impact reviewed by main agent
- [x] baseline impact updated or backlog item created
- [x] affected prototypes listed
- [ ] release package updated when applicable

## Rollback notes
- До релиза: пометить `DEC-2026-04-23-DEPLOYMENTS-001` как `reverted-before-release` и закрыть соответствующий backlog item.
- После релиза: rollback делать отдельной change/release единицей с ссылкой на этот `Decision ID`.

## Promotion targets
- `baseline/current/domain/contexts/research-and-execution.md`
- `baseline/current/domain/contexts/lineage.md`
- `baseline/current/domain/aggregates/deployment.md`
- `baseline/current/domain/state-machines/README.md`
