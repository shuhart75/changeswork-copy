# Domain Impact — pilots-config-type

Дата обновления: `2026-06-08`  
Baseline target: `baseline/current/domain/`  
Decision ID: `DEC-2026-05-13-PILOTS-CONFIG-TYPE`

## Decision registry

| Decision ID | Summary | Status | Consistency level | Source | Supersedes | Reverted by |
|---|---|---|---|---|---|---|
| DEC-2026-05-13-PILOTS-CONFIG-TYPE | Добавить `processType`/`process_type` для пилотов/экспериментов | proposed | cross-feature | `/home/reutov/Downloads/coda_docs` |  |  |

## Changed bounded contexts

- `Pilot Service` / experiment service: добавлено persisted поле типа процесса.

## New or changed aggregates

- `Experiment`: поле `process_type`.

## New or changed entities

- `experiments`: `process_type VARCHAR(32) NOT NULL DEFAULT 'online'`.

## New or changed value objects

- `ProcessType`: `online`, `offline`, `online+offline`.

## New or changed domain events

- Нет новых событий; mutation audit наследуется от существующих действий пилота/эксперимента.

## Business rules and invariants

- `processType` обязателен для новых и существующих записей.
- Default и backfill: `online`.
- Редактирование наследует права и статусные ограничения пилота.
- Внешнюю фильтрацию конфигураций выполняет Config Service только в `/api/v3/config`.
- `/api/v2/config` не расширяется в рамках этой дельты.

## State transitions

- Не меняются.

## API and integration impact

- Обновить request/response schemas внутренних experiment endpoints.
- Подтвердить canonical `coda_api.yaml`: входящий путь заявлен, но файл отсутствует в repo.
- Обновить внешний API `/api/v3/config` после внесения canonical `vneshneye_api_polucheniya_konfiguratsii_eksperimentov.3.1.1.yml`; входящий путь заявлен, но файл отсутствует в repo.

## Affected requirements

| Path | Impact | Sync status |
|---|---|---|
| `features/pilots-config-type/requirements.md` | Feature-level requirements созданы | propagated |
| `features/pilots-config-type/slices/config/slice.md` | Slice card создан | propagated |
| `features/pilots-config-type/slices/config/requirements/frontend.md` | FE pack создан | propagated |
| `features/pilots-config-type/slices/config/requirements/backend.md` | BE pack создан | propagated |
| `features/pilots/requirements.md` | Existing workspace синхронизирован | propagated |
| `features/pilots/slices/workspace/requirements/frontend.md` | Existing FE pack синхронизирован | propagated |
| `features/pilots/slices/workspace/requirements/backend.md` | Existing BE pack синхронизирован | propagated |

## Affected baseline artifacts

| Path | Impact | Sync status |
|---|---|---|
| `baseline/current/domain/` | Добавить `ProcessType` и связь pilot/experiment | open |
| `baseline/current/data/` | Добавить migration/backfill для `experiments.process_type` | open |
| `baseline/current/api/` | Обновить OpenAPI после проверки canonical specs | open |

## Affected prototypes

### Scope prototypes
| Path | Impact | Sync status |
|---|---|---|
| `features/pilots/planning/scope-prototype/prototype.html` | Может не показывать `processType` | defer-ok |

### Delivery prototypes
| Path | Impact | Sync status |
|---|---|---|
| `features/pilots/slices/workspace/delivery-prototype/prototype.html` | Добавить поле `Тип процесса` в prototype mode | defer-ok |
| `features/pilots-config-type/slices/config/delivery-prototype/prototype.html` | Входящий prototype не импортирован в режиме `requirements` | defer-ok |

## Required consistency actions

- [x] local feature requirements updated
- [x] neighboring feature requirements updated or backlog item created
- [x] domain impact reviewed by main agent
- [x] baseline impact updated or backlog item created
- [x] affected prototypes listed
- [ ] release package updated when applicable

## Rollback notes

- До release можно отменить decision и удалить/закрыть related backlog items без изменения baseline.
- После release требуется отдельная rollback/change feature.
