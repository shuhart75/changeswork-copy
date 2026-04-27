# Domain Impact — simulation-bt-agent

Дата обновления: `2026-04-27`
Baseline target: `baseline/current/domain/`

## Decision registry

| Decision ID | Summary | Status | Consistency level | Source | Supersedes | Reverted by |
|---|---|---|---|---|---|---|
| DEC-2026-04-24-SIMULATION-BT-AGENT-001 | Завершённая `Simulation` получает сценарий формирования БТ с сохранением внешней ссылки на результат | accepted | domain-wide | `features/simulation-bt-agent/feature.md` |  |  |
| DEC-2026-04-27-SIMULATION-BT-AGENT-002 | Окно агента становится глобальным для интерфейса симуляций, восстанавливается по `session_id`, не блокирует основной интерфейс, а при отправке текста дополнительно передаются ФИО пользователя из СУДИР и момент старта диалога; действие по БТ доступно только в подходящем контексте симуляции | accepted | domain-wide | `features/simulation-bt-agent/slices/*/requirements/*.md` |  |  |

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
- кандидат на нормализацию: ссылка на созданный БТ как отдельный атрибут результата симуляции или как внешняя reference-сущность
- кандидат на нормализацию: пользовательская сессия диалога формирования БТ

## New or changed value objects
- `сессия окна агента`
- `признаки доступности`
- `черновик запроса`
- `dialog_started_at`

## New or changed domain events
- запуск сессии формирования БТ
- восстановление окна агента по `session_id`
- ручная вставка черновика запроса
- публикация БТ и сохранение `btUrl`

## Business rules and invariants
- окно агента доступно с любой страницы интерфейса симуляций;
- окно агента не блокирует основной интерфейс;
- история и контекст диалога принадлежат агенту и восстанавливаются по `session_id`;
- при отправке текста в агент АС КОДА передаёт ФИО пользователя из СУДИР и дату-время первого открытия окна;
- действие по БТ доступно только для конкретной завершённой симуляции с доступной опцией вывода в ПРОМ;
- в Q2 поддерживается только продукт `Кредитные карты`;
- черновик запроса вставляется в поле ввода, но не отправляется автоматически;
- публикация БТ требует явного подтверждения пользователя;
- при наличии существующего БТ пользователь может создать новый документ повторно.

## State transitions
- новых доменных статусов `Simulation` не добавляется;
- возможен новый прикладной сценарий поверх `completed` и подходящего контекста симуляции: черновик запроса -> ручная отправка -> превью БТ -> публикация или отмена.

## API and integration impact
- новый интеграционный контракт с AI-агентом: `POST /dialog/session` для открытия и восстановления и отдельный вызов отправки сообщения после открытия окна;
- возврат `btUrl` и сохранение ссылки в АС КОДА;
- аудит и защищённый транспорт для межсервисного обмена.

## Affected requirements

| Path | Impact | Sync status |
|---|---|---|
| `features/simulation-bt-agent/slices/agent-entrypoint/requirements/frontend.md` | глобальное открытие окна агента и открытие или восстановление по `session_id` | propagated |
| `features/simulation-bt-agent/slices/agent-entrypoint/requirements/backend.md` | единый REST открытия и восстановления и признаки доступности текущей страницы | propagated |
| `features/simulation-bt-agent/slices/dialog-session/requirements/frontend.md` | неблокирующее окно, история на стороне агента, локальная блокировка только внутри окна | propagated |
| `features/simulation-bt-agent/slices/dialog-session/requirements/backend.md` | восстановление по `session_id`, контекст на стороне агента, отдельная отправка сообщения | propagated |
| `features/simulation-bt-agent/slices/bt-publication/requirements/frontend.md` | кнопка `Сформировать БТ`, черновик запроса, ручное редактирование и отправка | propagated |
| `features/simulation-bt-agent/slices/bt-publication/requirements/backend.md` | признаки доступности, данные для черновика запроса, публикация БТ и `btUrl` | propagated |
| `features/roles/slices/rbac/requirements/frontend.md` | при необходимости формализовать права на глобальное окно агента и действие по БТ | open |

## Affected baseline artifacts

| Path | Impact | Sync status |
|---|---|---|
| `baseline/current/domain/aggregates/simulation.md` | уточнить, как в модели отражается `btLink` и контекст доступности действия по БТ | open |
| `baseline/current/domain/contexts/research-and-execution.md` | отразить глобальное окно агента в интерфейсе симуляций и сценарий БТ | open |
| `baseline/current/domain/business-rules.md` | новые правила глобального окна, черновика запроса и публикации БТ | open |
| `baseline/current/domain/contexts/identity-and-access.md` | канонизировать права на окно агента и действие по БТ | open |
| `baseline/current/api/README.md` | описать REST открытия и восстановления сессии и вызов отправки сообщения | open |
| `baseline/current/ui/README.md` | зафиксировать неблокирующее окно агента и условное действие по БТ | open |

## Affected prototypes

### Scope prototypes
| Path | Impact | Sync status |
|---|---|---|
| `features/simulation-bt-agent/prototype.html` | общий feature prototype обновлён: панель агента переведена в формат `status chip -> chat -> input + actions`, уточнены tooltip-правила и компактное поле ввода | must-update-now |
| `features/simulation-bt-agent/prototype-notes.md` | зафиксирована визуальная база и статус root prototype | must-update-now |
| `features/simulation-bt-agent/planning/scope-prototype/prototype.html` | legacy scope prototype не используется как канонический артефакт для текущей feature | no-update-needed |

### Delivery prototypes
| Path | Impact | Sync status |
|---|---|---|
| `features/simulation-bt-agent/slices/agent-entrypoint/delivery-prototype/prototype.html` | handoff-артефакт не синхронизирован с новым root prototype и единым названием кнопки агента | defer-ok |
| `features/simulation-bt-agent/slices/dialog-session/delivery-prototype/prototype.html` | handoff-артефакт не синхронизирован с новым root prototype: status chip, чистая chat area и поле ввода на 5 строк пока не протянуты | defer-ok |
| `features/simulation-bt-agent/slices/bt-publication/delivery-prototype/prototype.html` | handoff-артефакт не синхронизирован с новым root prototype: tooltip у `Сформировать БТ` и новое расположение кнопок пока не протянуты | defer-ok |

## Prototype sync status values
- `must-update-now` — prototype is an active handoff/scope artifact and must be updated.
- `defer-ok` — known drift is acceptable until user asks to actualize prototypes.
- `no-update-needed` — decision does not affect the prototype.
- `obsolete` — prototype should no longer be treated as current.

## Required consistency actions
- [x] local feature requirements updated
- [ ] neighboring feature requirements updated or backlog item created
- [x] domain impact reviewed by main agent
- [ ] baseline impact updated or backlog item created
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
