# Domain Impact — scorecards

Дата обновления: `2026-04-23`
Baseline target: `baseline/current/domain/`

## Decision registry

| Decision ID | Summary | Status | Consistency level | Source | Supersedes | Reverted by |
|---|---|---|---|---|---|---|
| DEC-2026-04-23-SCORECARDS-001 | Скоркарта — самостоятельный агрегат со status model `active/archive`, versioning и binding через доменные формы | accepted | domain-wide | `features/scorecards/slices/workspace/requirements/backend.md` |  |  |

## Changed bounded contexts
- `Scorecard Templates`
- `Scorecards`
- `Research and Execution`

## New or changed aggregates
- `Scorecard` как самостоятельный агрегат со status model `active/archive`
- `Pilot` и `Deployment` как потребители `ScorecardVersion`

## New or changed entities
- `ScorecardVersion`
- `ScorecardSource`

## Business rules and invariants
- Скоркарта создаётся только из контекста `Pilot` или `Deployment`.
- Критичность считается на фронте по threshold'ам шаблона и сохраняется в `ScorecardVersion`.
- Любое изменение скоркарты создаёт новую версию и перевыпускает все связанные доменные версии.
- Binding скоркарты меняется только из доменной формы `Pilot`/`Deployment`.

## State transitions
- `Scorecard`: `active -> archive`

## API and integration impact
- lookup/select шаблонов и default config
- create/update/detail scorecard contracts
- связи с `PilotVersion` и `DeploymentVersion`

## Affected requirements

| Path | Impact | Sync status |
|---|---|---|
| `features/scorecards/slices/workspace/requirements/backend.md` | Основной scorecard domain contract | propagated |
| `features/scorecards/slices/workspace/requirements/frontend.md` | create/edit/detail and binding semantics | propagated |
| `features/deployments/slices/workspace/requirements/frontend.md` | интеграция со скоркартами и обязательная lineage-скоркарта | deferred |

## Affected baseline artifacts

| Path | Impact | Sync status |
|---|---|---|
| `baseline/current/domain/contexts/scorecards.md` | canonical scorecards rules | propagated |
| `baseline/current/domain/contexts/scorecard-templates.md` | template semantics | propagated |
| `baseline/current/domain/aggregates/scorecard.md` | aggregate invariants | propagated |
| `baseline/current/domain/business-rules.md` | cross-context rules | propagated |

## Affected prototypes

### Scope prototypes
| Path | Impact | Sync status |
|---|---|---|
| `features/scorecards/planning/scope-prototype/prototype.html` | Может отставать от финальной create/edit semantics | defer-ok |

### Delivery prototypes
| Path | Impact | Sync status |
|---|---|---|
| `features/scorecards/slices/workspace/delivery-prototype/prototype.html` | create/edit/binding flows may need actualization | defer-ok |
| `features/deployments/slices/workspace/delivery-prototype/prototype.html` | scorecard attachment and lineage interactions | defer-ok |

## Required consistency actions
- [x] local feature requirements updated
- [ ] neighboring feature requirements updated or backlog item created
- [x] domain impact reviewed by main agent
- [x] baseline impact updated or backlog item created
- [x] affected prototypes listed
- [ ] release package updated when applicable

## Rollback notes
- До релиза: отменить `DEC-2026-04-23-SCORECARDS-001`, пометить backlog item как `cancelled`, baseline не трогать если промоушена ещё не было.
- После релиза: rollback оформляется отдельной change/release единицей с новым `Decision ID`.

## Promotion targets
- `baseline/current/domain/contexts/scorecards.md`
- `baseline/current/domain/contexts/scorecard-templates.md`
- `baseline/current/domain/aggregates/scorecard.md`
- `baseline/current/domain/business-rules.md`
