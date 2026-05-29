# Domain Impact — packages

Дата обновления: `2026-05-25`
Baseline target: `baseline/current/domain/`

## Decision registry

| Decision ID | Summary | Status | Consistency level | Source | Supersedes | Reverted by |
|---|---|---|---|---|---|---|
| DEC-2026-04-23-PACKAGES-001 | `Package` — это группировка `ApprovalInstance` без собственного lifecycle enum; для `methodologist` допустим mixed-product package | superseded | cross-feature | `features/packages/slices/page/requirements/backend.md` |  |  |
| DEC-2026-05-25-APPROVALS-SBERDOCS-001 | Package flow исключён из MVP, потому что approval/ratification выполняется в SberDocs | accepted | domain-wide | `features/approvals/requirements.md` | DEC-2026-04-23-PACKAGES-001 |  |

## Changed bounded contexts

- `Packages` исключается из MVP scope.
- `Approval` больше не отдаёт элементы в `awaiting_ratification` для локального пакетирования.

## New or changed aggregates

- `Package` не создаётся как MVP aggregate.
- История группового согласования, если она нужна, должна приходить из SberDocs документа/маршрута или быть оформлена отдельной будущей feature.

## Business rules and invariants

- АС КОДА не группирует несколько `ApprovalInstance` в пакет.
- АС КОДА не хранит package brief как отдельный источник истины.
- АС КОДА не выполняет package `ratify/reject`.

## State transitions

- Старый переход `awaiting_ratification -> in_ratification` через package больше не применяется.
- Host entity использует mapped SberDocs status из approvals integration.

## API and integration impact

- `POST /api/v1/packages`, `GET /api/v1/packages`, `GET /api/v1/packages/{id}`, `POST /api/v1/packages/{id}/action` исключены из MVP.

## Affected requirements

| Path | Impact | Sync status |
|---|---|---|
| `features/packages/requirements.md` | package feature cancelled | propagated |
| `features/packages/slices/page/slice.md` | package page cancelled | propagated |
| `features/packages/slices/page/requirements/frontend.md` | FE scope cancelled | propagated |
| `features/packages/slices/page/requirements/backend.md` | BE/API scope cancelled | propagated |
| `features/approvals/requirements.md` | approvals source decision | propagated |

## Affected baseline artifacts

| Path | Impact | Sync status |
|---|---|---|
| `baseline/current/domain/contexts/approval.md` | remove package/rating queue semantics | open |
| `baseline/current/api/README.md` | remove package endpoints from target MVP | open |
| `baseline/current/ui/README.md` | remove package page from MVP navigation | open |

## Affected prototypes

| Path | Impact | Sync status |
|---|---|---|
| `features/packages/planning/scope-prototype/prototype.html` | obsolete for MVP | obsolete |
| `features/packages/slices/page/delivery-prototype/prototype.html` | obsolete for MVP | obsolete |
| `features/approvals/slices/page/delivery-prototype/prototype.html` | package cards obsolete with approvals page | obsolete |

## Required consistency actions

- [x] local package requirements updated
- [x] approvals domain impact updated
- [ ] baseline impact updated or backlog item created
- [ ] planning stories/estimates updated in planning mode
- [ ] prototypes updated/retired in prototype modes

## Rollback notes

- До релиза: можно вернуть package flow отдельным решением, если SberDocs integration не покрывает нужный групповой сценарий.
- После релиза: требуется новая feature/intake для групповой отправки в SberDocs или локальных пакетов.
