# Domain Impact — simulation-bt-agent

Дата обновления: `2026-04-30`
Baseline target: `baseline/current/domain/`

## Decision registry

| Decision ID | Summary | Status | Consistency level | Source | Supersedes | Reverted by |
|---|---|---|---|---|---|---|
| DEC-2026-04-24-SIMULATION-BT-AGENT-001 | Завершённая `Simulation` получает сценарий формирования БТ через окно агента | accepted | domain-wide | `features/simulation-bt-agent/feature.md` |  |  |
| DEC-2026-04-27-SIMULATION-BT-AGENT-002 | Окно агента становится глобальным для интерфейса симуляций, не блокирует основной интерфейс, а действие по БТ доступно только в подходящем контексте симуляции | accepted | domain-wide | `features/simulation-bt-agent/slices/*/requirements/*.md` |  |  |
| DEC-2026-04-27-SIMULATION-BT-AGENT-003 | В MVP ссылка на БТ не сохраняется автоматически в данных симуляции: пользователь получает её в окне агента, вручную копирует и при желании сам сохраняет в соответствующем разделе симуляции | accepted | domain-wide | `features/simulation-bt-agent/requirements.md` |  |  |
| DEC-2026-04-28-SIMULATION-BT-AGENT-004 | Для BT-сценария не вводится отдельный backend-контракт подготовки черновика: АС КОДА использует уже реализованный `GET /api/v1/simulation/{number}` как источник признаков доступности и данных страницы | accepted | domain-wide | `context/change-requests/simulation-bt-agent/simulations_api.md` |  |  |
| DEC-2026-04-28-SIMULATION-BT-AGENT-005 | `session_id` локально генерируется фронтом как UUID при первом открытии окна и хранится в пользовательской сессии АС КОДА | reverted-before-release | domain-wide | `features/simulation-bt-agent/slices/agent-entrypoint/requirements/frontend.md` |  | DEC-2026-04-30-SIMULATION-BT-AGENT-009 |
| DEC-2026-04-29-SIMULATION-BT-AGENT-007 | Принятый контракт RAIN фиксируется по `rain_api_proposal.md`: RAIN предоставляет `liveness`, `readiness`, async runs и постраничную историю; АС КОДА владеет UI-сессией и frontend boundary, но не terminal status и не агентской историей | accepted | domain-wide | `context/change-requests/simulation-bt-agent/rain_api_proposal.md` | DEC-2026-04-28-SIMULATION-BT-AGENT-005 |  |
| DEC-2026-04-30-SIMULATION-BT-AGENT-008 | Frontend API АС КОДА читает статус диалога по `session_id`, а не по конкретному `run_id`; история отображается как windowed pagination с индикатором новых сообщений, если пользователь прокрутил чат вверх | accepted | domain-wide | `features/simulation-bt-agent/requirements.md`, `features/simulation-bt-agent/slices/dialog-session/requirements/*.md` | DEC-2026-04-29-SIMULATION-BT-AGENT-007 |  |
| DEC-2026-04-30-SIMULATION-BT-AGENT-009 | `session_id` создаёт backend АС КОДА; frontend передаёт его параметром запроса для продолжения сессии, а отсутствие `session_id` означает создание новой/сброс текущей UI-сессии; status response сокращён до `session_id`, `can_send_message`, `dialog_status`, `history_changed`, `error` | accepted | domain-wide | `features/simulation-bt-agent/requirements.md`, `features/simulation-bt-agent/slices/*/requirements/*.md` | DEC-2026-04-28-SIMULATION-BT-AGENT-005, DEC-2026-04-30-SIMULATION-BT-AGENT-008 |  |

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
- `Simulation` получает пользовательский сценарий публикации БТ поверх существующей деталки.
- Прикладная интеграция агента получает backend-managed UI-сессию и async boundary на стороне АС КОДА; история сообщений и агентский контекст остаются у RAIN.

## New or changed entities
- `agent_ui_session`
- `agent_dialog_run`
- `agent_dialog_message`
- `agent_status_cache`

## New or changed value objects
- `session_id`
- `start_datetime`
- `agent_status`
- `run_id`
- `terminal status`
- `risk_params`
- `BT URL candidate`
- `history cursor`
- `history window`

## New or changed domain events
- открытие UI-сессии агента;
- проверка готовности RAIN;
- запуск async run;
- завершение run успехом, ошибкой или timeout;
- ручная вставка черновика запроса;
- публикация БТ через агентский ответ;
- ручное копирование ссылки на БТ пользователем.

## Business rules and invariants
- окно агента доступно с любой страницы интерфейса симуляций;
- окно агента не блокирует основной интерфейс;
- frontend не вызывает RAIN напрямую и не получает OTT;
- RAIN вызывается backend АС КОДА server-to-server по HTTPS/mTLS/OTT;
- открытие окна не создаёт RAIN run;
- UI-сессия и frontend boundary принадлежат АС КОДА; run status, история сообщений и агентский контекст принадлежат RAIN;
- `session_id` генерируется backend АС КОДА при первом открытии окна или сбросе сессии; frontend хранит его как opaque token и передаёт параметром запроса для продолжения сессии;
- отсутствие `session_id` в dialog API означает создание новой UI-сессии и сброс текущего диалогового контекста окна;
- `start_datetime` фиксируется backend при создании UI-сессии и передаётся в RAIN `POST /chat/runs`;
- status chip агента строится на нормализованном результате `RAIN /health/liveness` и `RAIN /health/readiness`;
- composer и agent actions блокируются, если RAIN не готов или есть active run;
- пользовательское сообщение запускает RAIN async run через backend АС КОДА, frontend читает статус сессии через polling по `session_id`;
- для одного `session_id` допускается только один active run;
- длинная история загружается страницами через cursor/limit;
- frontend стартует с последних `20` сообщений и может держать в памяти только window загруженных страниц, а не всю историю без ограничения;
- если пользователь прокрутил историю вверх, новые сообщения не сбрасывают scroll-position; UI показывает индикатор новых сообщений и загружает последние сообщения по действию пользователя;
- prompt и отображаемые сообщения истории имеют backend/frontend лимиты длины;
- действие по БТ доступно только для конкретной завершённой симуляции с доступной опцией вывода в ПРОМ;
- в Q2 поддерживается продукт `Кредитные карты`;
- черновик запроса вставляется в поле ввода, но не отправляется автоматически;
- для доступности BT-сценария и риск-параметров используется уже реализованный `GET /api/v1/simulation/{number}`;
- backend проверяет доступность симуляции и собирает/валидирует `risk_params` перед вызовом RAIN;
- terminal status run, история и агентский контекст принадлежат RAIN;
- после успешной публикации URL на БТ отображается из структурированных `artifacts[]` результата RAIN run, если он присутствует;
- автоматическое сохранение ссылки на БТ в данных симуляции в MVP не выполняется;
- автоматический retry BT run после передачи в RAIN запрещён без идемпотентности.

## State transitions
- новых доменных статусов `Simulation` не добавляется;
- возможен прикладной сценарий поверх `completed` и подходящего контекста симуляции: черновик запроса -> ручная отправка -> async run -> ответ агента -> ручное копирование URL или ошибка/timeout.

## API and integration impact
- frontend API АС КОДА: `POST /dialog/session` создаёт/восстанавливает UI-сессию без вызова RAIN;
- frontend API АС КОДА: `GET /dialog/agent/status` отдаёт нормализованный readiness/liveness status;
- frontend API АС КОДА: `POST /dialog/message` создаёт async run и возвращает `202` со статусом сессии;
- frontend API АС КОДА: `GET /dialog/status?session_id=...` отдаёт `session_id`, `can_send_message`, `dialog_status`, `history_changed` и ошибку;
- frontend API АС КОДА: `GET /dialog/messages?session_id=...&limit=&before=` отдаёт историю страницами и cursor для windowed UI;
- server-to-server RAIN: `GET /health/liveness`, `GET /health/readiness`, `POST /chat/runs`, `GET /chat/runs/{run_id}`, `GET /chat/runs/{run_id}/result`, `GET /chat/sessions/{session_id}/messages`;
- existing simulation detail API `GET /api/v1/simulation/{number}` переиспользуется как источник данных страницы для BT-сценария;
- `btUrl` как отдельное поле frontend API АС КОДА не требуется; ссылка на БТ берётся из `artifacts[]` результата RAIN run;
- аудит и защищённый транспорт для межсервисного обмена остаются обязательными.

## Affected requirements

| Path | Impact | Sync status |
|---|---|---|
| `features/simulation-bt-agent/requirements.md` | root source-of-truth перестроен под фактический контракт RAIN, async facade, session-level polling, health status и лимиты истории | propagated |
| `features/simulation-bt-agent/slices/agent-entrypoint/slice.md` | обновлена цель slice под UI-сессию и status health | propagated |
| `features/simulation-bt-agent/slices/agent-entrypoint/requirements/frontend.md` | открытие окна, backend-managed `session_id`, status chip и blocked composer описаны без прямого вызова RAIN | propagated |
| `features/simulation-bt-agent/slices/agent-entrypoint/requirements/backend.md` | описаны `POST /dialog/session`, создание/продолжение/сброс UI-сессии, `GET /dialog/agent/status`, liveness/readiness и status cache | propagated |
| `features/simulation-bt-agent/slices/dialog-session/slice.md` | обновлена цель slice под async run, polling, историю АС КОДА и лимиты длины | propagated |
| `features/simulation-bt-agent/slices/dialog-session/requirements/frontend.md` | описаны async run, polling с `session_id` в параметрах запроса, compact status response, terminal statuses, blocked composer, history window и индикатор новых сообщений | propagated |
| `features/simulation-bt-agent/slices/dialog-session/requirements/backend.md` | описаны backend async facade без path `session_id`, session status endpoint, run storage, history pagination, лимиты и timeout/retry policy | propagated |
| `features/simulation-bt-agent/slices/bt-publication/slice.md` | обновить цель slice под `risk_params`, `simulation_id` и `artifacts[]` результата RAIN run | open |
| `features/simulation-bt-agent/slices/bt-publication/requirements/frontend.md` | обновить inline action БТ, async run и отображение URL из `artifacts[]` вместо извлечения из `response` | open |
| `features/simulation-bt-agent/slices/bt-publication/requirements/backend.md` | проверка симуляции, сбор `risk_params`, вызов RAIN `POST /chat/runs`, чтение result/artifacts и retry policy | open |
| `features/roles/slices/rbac/requirements/frontend.md` | при необходимости формализовать права на глобальное окно агента и действие по БТ | open |

## Affected baseline artifacts

| Path | Impact | Sync status |
|---|---|---|
| `baseline/current/domain/contexts/research-and-execution.md` | отразить окно агента, async run и сценарий БТ | open |
| `baseline/current/domain/business-rules.md` | новые правила UI-сессии, readiness block, run lock, prompt/history limits, ручного копирования URL и отсутствия автосохранения | open |
| `baseline/current/domain/contexts/identity-and-access.md` | канонизировать права на окно агента, действие по БТ и server-to-server OTT/mTLS | open |
| `baseline/current/api/README.md` | описать frontend API АС КОДА без `session_id` в path, compact session-level status, server-to-server RAIN async runs/history и health endpoints | open |
| `baseline/current/ui/README.md` | зафиксировать status chip, blocked composer, async run/session polling, paginated history, new-message indicator и inline action БТ | open |

## Affected prototypes

### Scope prototypes
| Path | Impact | Sync status |
|---|---|---|
| `features/simulation-bt-agent/prototype.html` | требует синхронизации под async run/session polling, health status readiness block, paginated history, new-message indicator и `artifacts[]` результата RAIN run | defer-ok |
| `features/simulation-bt-agent/prototype-notes.md` | требует обновления заметок после новой интеграционной модели | defer-ok |
| `features/simulation-bt-agent/planning/scope-prototype/prototype.html` | legacy scope prototype не используется как канонический артефакт для текущей feature | obsolete |

### Delivery prototypes
| Path | Impact | Sync status |
|---|---|---|
| `features/simulation-bt-agent/slices/agent-entrypoint/delivery-prototype/prototype.html` | требует синхронизации под health/readiness status и отсутствие вызова RAIN при открытии | defer-ok |
| `features/simulation-bt-agent/slices/dialog-session/delivery-prototype/prototype.html` | требует синхронизации под async run, session polling, terminal statuses, paginated history и new-message indicator | defer-ok |
| `features/simulation-bt-agent/slices/bt-publication/delivery-prototype/prototype.html` | требует синхронизации под inline action, `risk_params/simulation_id` и URL из `artifacts[]` | defer-ok |

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
