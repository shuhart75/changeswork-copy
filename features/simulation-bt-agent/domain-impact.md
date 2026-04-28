# Domain Impact — simulation-bt-agent

Дата обновления: `2026-04-28`
Baseline target: `baseline/current/domain/`

## Decision registry

| Decision ID | Summary | Status | Consistency level | Source | Supersedes | Reverted by |
|---|---|---|---|---|---|---|
| DEC-2026-04-24-SIMULATION-BT-AGENT-001 | Завершённая `Simulation` получает сценарий формирования БТ через окно агента | accepted | domain-wide | `features/simulation-bt-agent/feature.md` |  |  |
| DEC-2026-04-27-SIMULATION-BT-AGENT-002 | Окно агента становится глобальным для интерфейса симуляций, восстанавливается по `session_id`, не блокирует основной интерфейс, а при отправке текста дополнительно передаются ФИО пользователя из СУДИР и момент старта диалога; действие по БТ доступно только в подходящем контексте симуляции | accepted | domain-wide | `features/simulation-bt-agent/slices/*/requirements/*.md` |  |  |
| DEC-2026-04-27-SIMULATION-BT-AGENT-003 | В MVP `btUrl` не сохраняется автоматически в данных симуляции: пользователь получает ссылку в окне агента, вручную копирует её и при желании сам сохраняет в соответствующем разделе симуляции | accepted | domain-wide | `features/simulation-bt-agent/requirements.md` |  |  |
| DEC-2026-04-28-SIMULATION-BT-AGENT-004 | Для BT-сценария не вводится отдельный backend-контракт подготовки черновика: фронт использует уже реализованный `GET /api/v1/simulation/{number}` как источник признаков доступности и данных страницы | accepted | domain-wide | `context/change-requests/simulation-bt-agent/simulations_api.md` |  |  |
| DEC-2026-04-28-SIMULATION-BT-AGENT-005 | `session_id` локально генерируется фронтом как UUID при первом открытии окна, хранится в пользовательской сессии АС КОДА, а backend создаёт серверную сессию при первом unseen значении и восстанавливает её при повторных вызовах | accepted | domain-wide | `features/simulation-bt-agent/slices/agent-entrypoint/requirements/frontend.md` |  |  |

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
- `Research and Execution`
- `Identity and Access`

## New or changed aggregates
- `Simulation` получает новый пользовательский сценарий публикации БТ поверх существующей деталки

## New or changed entities
- кандидат на нормализацию: пользовательская сессия диалога формирования БТ

## New or changed value objects
- `сессия окна агента`
- `признаки доступности`
- `черновик запроса`
- `dialog_started_at`
- `результат публикации БТ с btUrl для ручного копирования`

## New or changed domain events
- запуск сессии формирования БТ
- восстановление окна агента по `session_id`
- ручная вставка черновика запроса
- публикация БТ и возврат `btUrl` в окно агента
- ручное копирование ссылки на БТ пользователем

## Business rules and invariants
- окно агента доступно с любой страницы интерфейса симуляций;
- окно агента не блокирует основной интерфейс;
- история и контекст диалога принадлежат агенту и восстанавливаются по `session_id`;
- `session_id` генерируется на фронте локально в формате UUID при первом открытии окна, остаётся неизменным в рамках активной пользовательской сессии и сбрасывается вместе с ней или при перезапуске;
- при отправке текста в агент АС КОДА передаёт ФИО пользователя из СУДИР и дату-время первого открытия окна;
- действие по БТ доступно только для конкретной завершённой симуляции с доступной опцией вывода в ПРОМ;
- в Q2 поддерживается только продукт `Кредитные карты`;
- черновик запроса вставляется в поле ввода, но не отправляется автоматически;
- для доступности BT-сценария и черновика запроса используется уже реализованный `GET /api/v1/simulation/{number}`, без отдельного BT-specific preparatory API;
- публикация БТ требует явного подтверждения пользователя;
- после успешной публикации `btUrl` возвращается в окно агента и доступен для ручного копирования;
- автоматическое сохранение ссылки на БТ в данных симуляции в MVP не выполняется;
- при наличии существующего БТ пользователь может создать новый документ повторно.

## State transitions
- новых доменных статусов `Simulation` не добавляется;
- возможен новый прикладной сценарий поверх `completed` и подходящего контекста симуляции: черновик запроса -> ручная отправка -> превью БТ -> публикация или отмена.

## API and integration impact
- новый интеграционный контракт с AI-агентом: `POST /dialog/session` для открытия и восстановления и отдельный вызов отправки сообщения после открытия окна;
- `POST /dialog/session` принимает только client-generated UUID `session_id`; при первом unseen значении создаётся серверная сессия, при повторном вызове выполняется восстановление;
- existing simulation detail API `GET /api/v1/simulation/{number}` переиспользуется как источник данных страницы для BT-сценария без отдельного backend-метода подготовки черновика;
- возврат `btUrl` без автоматического сохранения ссылки в данных симуляции;
- аудит и защищённый транспорт для межсервисного обмена.

## Affected requirements

| Path | Impact | Sync status |
|---|---|---|
| `features/simulation-bt-agent/requirements.md` | корневой source-of-truth зафиксирован под existing detail API без отдельного BT-specific preparatory backend-контракта | propagated |
| `features/simulation-bt-agent/slices/agent-entrypoint/requirements/frontend.md` | глобальное открытие окна агента, локальная генерация UUID `session_id` и клиентское хранение активного идентификатора | propagated |
| `features/simulation-bt-agent/slices/agent-entrypoint/requirements/backend.md` | единый REST открытия и восстановления, UUID-валидация `session_id` и фиксация existing detail API как источника BT-контекста страницы | propagated |
| `features/simulation-bt-agent/slices/dialog-session/requirements/frontend.md` | неблокирующее окно, локальная генерация и переиспользование `session_id`, история на стороне агента | propagated |
| `features/simulation-bt-agent/slices/dialog-session/requirements/backend.md` | восстановление по client-generated UUID `session_id`, создание серверной сессии при unseen значении и отдельная отправка сообщения | propagated |
| `features/simulation-bt-agent/slices/bt-publication/requirements/frontend.md` | кнопка `Сформировать БТ`, черновик запроса, ручное редактирование, показ `btUrl` и ручное копирование без автообновления симуляции | propagated |
| `features/simulation-bt-agent/slices/bt-publication/requirements/backend.md` | existing detail API как источник признаков доступности и данных для черновика, публикация БТ и возврат `btUrl` без автосохранения | propagated |
| `features/roles/slices/rbac/requirements/frontend.md` | при необходимости формализовать права на глобальное окно агента и действие по БТ | open |

## Affected baseline artifacts

| Path | Impact | Sync status |
|---|---|---|
| `baseline/current/domain/contexts/research-and-execution.md` | отразить глобальное окно агента в интерфейсе симуляций и сценарий БТ | open |
| `baseline/current/domain/business-rules.md` | новые правила глобального окна, черновика запроса, ручного копирования `btUrl` и отсутствия автосохранения в MVP | open |
| `baseline/current/domain/contexts/identity-and-access.md` | канонизировать права на окно агента и действие по БТ | open |
| `baseline/current/api/README.md` | описать REST открытия и восстановления сессии, client-generated UUID `session_id`, переиспользование existing detail API для BT-сценария и возврат `btUrl` без автосохранения | open |
| `baseline/current/ui/README.md` | зафиксировать неблокирующее окно агента, условное действие по БТ и ручное копирование `btUrl` | open |

## Affected prototypes

### Scope prototypes
| Path | Impact | Sync status |
|---|---|---|
| `features/simulation-bt-agent/prototype.html` | общий feature prototype синхронизирован под сценарий ручного копирования `btUrl` без автосохранения в симуляцию | no-update-needed |
| `features/simulation-bt-agent/prototype-notes.md` | notes синхронизированы с решением об отсутствии автосохранения `btUrl` в MVP | no-update-needed |
| `features/simulation-bt-agent/planning/scope-prototype/prototype.html` | legacy scope prototype не используется как канонический артефакт для текущей feature | no-update-needed |

### Delivery prototypes
| Path | Impact | Sync status |
|---|---|---|
| `features/simulation-bt-agent/slices/agent-entrypoint/delivery-prototype/prototype.html` | handoff-артефакт обновлён под утверждённый root prototype: единая кнопка `AI-агент RAIN`, open/restore только по `session_id`, контексты list/detail/results/edit | no-update-needed |
| `features/simulation-bt-agent/slices/dialog-session/delivery-prototype/prototype.html` | handoff-артефакт обновлён под утверждённый root prototype: status chip, чистая chat area и поле ввода на 5 строк | no-update-needed |
| `features/simulation-bt-agent/slices/bt-publication/delivery-prototype/prototype.html` | handoff-артефакт синхронизирован под ручное копирование `btUrl` без автоматического обновления данных симуляции | no-update-needed |

## Prototype sync status values
- `must-update-now` — prototype is an active handoff/scope artifact and must be updated.
- `defer-ok` — known drift is acceptable until user asks to actualize prototypes.
- `no-update-needed` — decision does not affect the prototype.
- `obsolete` — prototype should no longer be treated as current.

## Required consistency actions
- [x] local feature requirements updated
- [ ] neighboring feature requirements updated or backlog item created
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
- `baseline/current/domain/aggregates/simulation.md`
- `baseline/current/domain/contexts/research-and-execution.md`
- `baseline/current/domain/business-rules.md`
- `baseline/current/domain/contexts/identity-and-access.md`
- `baseline/current/api/`
- `baseline/current/ui/`
