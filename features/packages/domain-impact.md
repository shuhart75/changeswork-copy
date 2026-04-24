# Domain Impact — packages

Дата обновления: `2026-04-23`
Baseline target: `baseline/current/domain/`

## Decision registry

| Decision ID | Summary | Status | Consistency level | Source | Supersedes | Reverted by |
|---|---|---|---|---|---|---|
| DEC-2026-04-23-PACKAGES-001 | `Package` — это группировка `ApprovalInstance` без собственного lifecycle enum; для `methodologist` допустим mixed-product package | accepted | cross-feature | `features/packages/slices/page/requirements/backend.md` |  |  |

## Changed bounded contexts
- `Packages`
- `Approval`
- `Identity and Access`

## New or changed aggregates
- `Package` как операционная группировка `ApprovalInstance`

## Business rules and invariants
- пакет создаётся только из `awaiting_ratification`
- minimum size = 2
- package не имеет собственного lifecycle enum
- package не является самостоятельным approval target
- для `methodologist` допустим mixed-product package

## State transitions
- отдельный lifecycle отсутствует; активность определяется связанными `ApprovalInstance`

## API and integration impact
- queue/create/detail package contracts
- совместная работа с approvals page

## Affected requirements

| Path | Impact | Sync status |
|---|---|---|
| `features/packages/slices/page/requirements/backend.md` | package semantics and queue/create/detail contracts | propagated |
| `features/packages/slices/page/requirements/frontend.md` | package UX and queue flow | propagated |
| `features/approvals/slices/page/requirements/frontend.md` | согласованность page semantics и package actions | open |
| `features/approvals/slices/page/requirements/backend.md` | согласованность package context in approvals | open |

## Affected baseline artifacts

| Path | Impact | Sync status |
|---|---|---|
| `baseline/current/domain/contexts/packages.md` | canonical package semantics | propagated |
| `baseline/current/domain/contexts/approval.md` | package and ratification interplay | open |
| `baseline/current/domain/contexts/identity-and-access.md` | mixed-product package exception for methodologist | propagated |
| `baseline/current/domain/aggregates/package.md` | package invariants | propagated |

## Affected prototypes

### Scope prototypes
| Path | Impact | Sync status |
|---|---|---|
| `features/packages/planning/scope-prototype/prototype.html` | history/in-progress legacy tabs may be outdated relative to MVP semantics | defer-ok |

### Delivery prototypes
| Path | Impact | Sync status |
|---|---|---|
| `features/packages/slices/page/delivery-prototype/prototype.html` | package queue/cards/detail composition may need actualization | defer-ok |
| `features/approvals/slices/page/delivery-prototype/prototype.html` | package handling on approvals page may need actualization | defer-ok |

## Required consistency actions
- [x] local feature requirements updated
- [ ] neighboring feature requirements updated or backlog item created
- [x] domain impact reviewed by main agent
- [x] baseline impact updated or backlog item created
- [x] affected prototypes listed
- [ ] release package updated when applicable

## Rollback notes
- До релиза: пометить `DEC-2026-04-23-PACKAGES-001` как `reverted-before-release` и отменить открытые consistency items.
- После релиза: rollback оформляется новым релизным изменением; история package semantics не переписывается задним числом.

## Promotion targets
- `baseline/current/domain/contexts/packages.md`
- `baseline/current/domain/contexts/approval.md`
- `baseline/current/domain/contexts/identity-and-access.md`
- `baseline/current/domain/aggregates/package.md`
