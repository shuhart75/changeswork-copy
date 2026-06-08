# Domain Impact — pilots

Дата обновления: `2026-06-08`
Baseline target: `baseline/current/domain/`

## Decision registry

| Decision ID | Summary | Status | Consistency level | Source | Supersedes | Reverted by |
|---|---|---|---|---|---|---|
| DEC-2026-05-13-PILOTS-CONFIG-TYPE | Добавить `processType`/`process_type` для пилотов/экспериментов | proposed | cross-feature | `/home/reutov/Downloads/coda_docs` |  |  |

## Status values
- `proposed` — решение сформулировано, но ещё не принято.
- `accepted` — решение принято и должно распространяться по артефактам.
- `deferred` — решение отложено.
- `reverted-before-release` — решение отменено до релиза.
- `released` — решение попало в release package.
- `rolled-back-after-release` — решение отменяется отдельным rollback/change после релиза.

## Consistency levels
- `local` — влияет только на текущую feature/slice.
- `cross-feature` — влияет на соседние feature requirements.
- `domain-wide` — влияет на baseline/current/domain, shared API, lifecycle, roles or business rules.

## Changed bounded contexts

- `Pilot Service` / experiment service: добавлено persisted поле типа процесса.

## New or changed aggregates

- `Experiment`: новое поле `process_type`.
- `Pilot` workspace: отображает и редактирует `processType` как пользовательское представление поля эксперимента.

## New or changed entities

- `experiments`: добавлено `process_type`.

## New or changed value objects

- `ProcessType`: enum `online`, `offline`, `online+offline`.

## New or changed domain events

## Business rules and invariants

- Значение `processType` обязательно для пилота/эксперимента.
- Default при создании: `online`.
- Backfill существующих записей: `online`.
- Допустимые значения: `online`, `offline`, `online+offline`.
- Права редактирования наследуются от существующих правил редактирования пилота.
- Внешнюю фильтрацию конфигураций выполняет Config Service только в `/api/v3/config`.
- `/api/v2/config` не расширяется в рамках этой дельты.

## State transitions

- Не меняются.

## API and integration impact

- Внутренние experiment endpoints должны принимать/возвращать `processType`:
  - `POST /api/v1/experiment`
  - `PUT /api/v1/experiment/{id}`
  - `POST /api/v1/experiments`
  - `POST /api/v1/experimentsExtended`
  - `POST /api/v1/experimentsWithSampleHistory`
  - `GET /api/v1/experiment/{number}`
- Canonical `context/source-materials/current-system/requirements/raw/docs/coda_api.yaml` заявлен во входящих материалах, но отсутствует в текущем repo.
- Внешний `/api/v3/config` должен принимать optional `processType` и возвращать отфильтрованные конфигурации.
- Внешний `/api/v2/config` не меняется в рамках этой дельты.

## Affected requirements

| Path | Impact | Sync status |
|---|---|---|
| `features/pilots/requirements.md` | Root workspace синхронизирован с дельтой `processType` | propagated |
| `features/pilots/slices/workspace/slice.md` | Добавлены ссылки на related config requirements | propagated |
| `features/pilots/slices/workspace/requirements/frontend.md` | Добавлены UI/type/API требования по `processType` | propagated |
| `features/pilots/slices/workspace/requirements/backend.md` | Добавлены model/API/open-question требования по `processType` | propagated |
| `features/pilots-config-type/requirements.md` | Создан отдельный requirements-пакет из входящей папки | propagated |
| `features/pilots-config-type/slices/config/requirements/frontend.md` | Создан детальный FE pack | propagated |
| `features/pilots-config-type/slices/config/requirements/backend.md` | Создан детальный BE pack | propagated |

## Affected baseline artifacts

| Path | Impact | Sync status |
|---|---|---|
| `baseline/current/domain/` | Добавить `ProcessType` и связь pilot/experiment | open |
| `baseline/current/data/` | Добавить migration/backfill для `experiments.process_type` | open |
| `baseline/current/api/` | Обновить experiment OpenAPI и внешний `/api/v3/config`; `/api/v2/config` не менять | open |

## Affected prototypes

### Scope prototypes
| Path | Impact | Sync status |
|---|---|---|
| `features/pilots/planning/scope-prototype/prototype.html` | Может не показывать `processType` в форме/деталке | defer-ok |

### Delivery prototypes
| Path | Impact | Sync status |
|---|---|---|
| `features/pilots/slices/workspace/delivery-prototype/prototype.html` | Нужно добавить поле `Тип процесса` после переключения в prototype mode | defer-ok |
| `features/pilots-config-type/slices/config/delivery-prototype/prototype.html` | Входящий prototype не импортирован в режиме `requirements` | defer-ok |

## Prototype sync status values
- `must-update-now` — prototype is an active handoff/scope artifact and must be updated.
- `defer-ok` — known drift is acceptable until user asks to actualize prototypes.
- `no-update-needed` — decision does not affect the prototype.
- `obsolete` — prototype should no longer be treated as current.

## Required consistency actions
- [x] local feature requirements updated
- [x] neighboring feature requirements updated or backlog item created
- [x] domain impact reviewed by main agent
- [x] baseline impact updated or backlog item created
- [x] affected prototypes listed
- [ ] release package updated when applicable

## Rollback notes

### Before release
- Mark decision as `reverted-before-release`.
- Cancel related consistency backlog items.
- Revert already-propagated living requirements if needed.
- Do not touch baseline if the decision was not promoted.

### After release
- Create a new rollback/change feature or release item.
- Reference the original `Decision ID` in `Supersedes` or `Reverted by`.
- Promote the rollback as a normal baseline-changing release.

## Promotion targets
- `baseline/current/domain/`
- `baseline/current/api/`
- `baseline/current/requirements/`
