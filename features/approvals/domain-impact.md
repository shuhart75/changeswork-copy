# Domain Impact — approvals

Дата обновления: `2026-04-23`
Baseline target: `baseline/current/domain/`

## Decision registry

| Decision ID | Summary | Status | Consistency level | Source | Supersedes | Reverted by |
|---|---|---|---|---|---|---|
| DEC-2026-04-23-APPROVALS-001 | Approval route создаётся динамически: 0..* approval stages + 1 ratification stage, recall допустим на любом этапе | accepted | domain-wide | `features/approvals/slices/core-process/requirements/backend.md` |  |  |

## Changed bounded contexts
- `Approval`
- `Identity and Access`

## New or changed aggregates
- `ApprovalInstance` как динамический маршрут approval + ratification

## Business rules and invariants
- 0..* approval stages + 1 ratification stage
- approver и ratifier разделены
- recall допустим на любом этапе
- маршрут создаётся при submit и не предзадан заранее

## State transitions
- target версии проходят `in_approval`, `awaiting_ratification`, `in_ratification`, reject/cancel states

## API and integration impact
- submit/recall/decision flows
- assignments and process snapshot

## Affected requirements

| Path | Impact | Sync status |
|---|---|---|
| `features/approvals/slices/core-process/requirements/backend.md` | approval process semantics | propagated |
| `features/approvals/slices/page/requirements/frontend.md` | approvals page and assignment semantics | propagated |
| `features/packages/slices/page/requirements/backend.md` | package interaction with ratification queue | open |
| `features/deployments/slices/workspace/requirements/backend.md` | deployment submit/recall lifecycle alignment | open |

## Affected baseline artifacts

| Path | Impact | Sync status |
|---|---|---|
| `baseline/current/domain/contexts/approval.md` | canonical approval route | propagated |
| `baseline/current/domain/contexts/identity-and-access.md` | approver/ratifier scope | propagated |
| `baseline/current/domain/business-rules.md` | shared approval rules | propagated |

## Affected prototypes

### Scope prototypes
| Path | Impact | Sync status |
|---|---|---|
| `features/approvals/planning/scope-prototype/prototype.html` | отсутствует в текущем примере | no-update-needed |

### Delivery prototypes
| Path | Impact | Sync status |
|---|---|---|
| `features/approvals/slices/page/delivery-prototype/prototype.html` | route/decision states may need actualization | defer-ok |
| `features/packages/slices/page/delivery-prototype/prototype.html` | interaction with ratification queue may need actualization | defer-ok |

## Required consistency actions
- [x] local feature requirements updated
- [ ] neighboring feature requirements updated or backlog item created
- [x] domain impact reviewed by main agent
- [x] baseline impact updated or backlog item created
- [x] affected prototypes listed
- [ ] release package updated when applicable

## Rollback notes
- До релиза: отменить `DEC-2026-04-23-APPROVALS-001` и закрыть зависимые backlog items как `cancelled`.
- После релиза: откат возможен только новым change/release item с собственной цепочкой promotion.

## Promotion targets
- `baseline/current/domain/contexts/approval.md`
- `baseline/current/domain/contexts/identity-and-access.md`
- `baseline/current/domain/business-rules.md`
