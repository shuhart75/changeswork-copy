# Domain Impact — simulation-bt-agent

Дата обновления: `2026-04-24`
Baseline target: `baseline/current/domain/`

## Decision registry

| Decision ID | Summary | Status | Consistency level | Source | Supersedes | Reverted by |
|---|---|---|---|---|---|---|
| DEC-2026-04-24-SIMULATION-BT-AGENT-001 | Завершённая `Simulation` получает AI-agent сценарий формирования БТ с сохранением внешней ссылки на результат | proposed | domain-wide | `features/simulation-bt-agent/feature.md` |  |  |

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
- кандидат на нормализацию: UI-сессия диалога формирования БТ

## New or changed value objects
- `contextPrompt`
- `riskParam AS IS / TO BE`

## New or changed domain events
- запуск сессии формирования БТ
- перезапуск сессии формирования БТ
- публикация БТ и сохранение `btUrl`

## Business rules and invariants
- сценарий доступен только для завершённой симуляции;
- в Q2 поддерживается только продукт `Кредитные карты`;
- публикация БТ требует явного подтверждения пользователя;
- при наличии существующего БТ пользователь может создать новый документ повторно;
- в MVP для одной сессии допускается только один активный `continue` запрос одновременно.

## State transitions
- новых доменных статусов `Simulation` не добавляется;
- возможен новый прикладной subflow поверх `completed` симуляции: запуск диалога -> превью БТ -> публикация/отмена.

## API and integration impact
- новый интеграционный контракт с AI-агентом: `POST /dialog/init`, `POST /dialog/{sessionId}/continue`;
- возврат `btUrl` и сохранение ссылки в АС КОДА;
- аудит и защищённый транспорт для межсервисного обмена.

## Affected requirements

| Path | Impact | Sync status |
|---|---|---|
| `features/simulation-bt-agent/slices/agent-entrypoint/requirements/frontend.md` | условия показа кнопки, сбор `contextPrompt`, проверка уже созданного БТ | open |
| `features/simulation-bt-agent/slices/dialog-session/requirements/frontend.md` | диалог, retry, restart, anti-double-submit, восстановление истории | open |
| `features/simulation-bt-agent/slices/dialog-session/requirements/backend.md` | init/continue, state machine, хранение сессии, очередность сообщений | open |
| `features/simulation-bt-agent/slices/bt-publication/requirements/backend.md` | публикация БТ, `btUrl`, аудит, security constraints | open |
| `features/roles/slices/rbac/requirements/frontend.md` | если потребуется явное отражение доступа для `experiment_editor_CC` | open |

## Affected baseline artifacts

| Path | Impact | Sync status |
|---|---|---|
| `baseline/current/domain/aggregates/simulation.md` | уточнить, как в модели отражается ссылка на созданный БТ и прикладной publish-flow | open |
| `baseline/current/domain/contexts/research-and-execution.md` | отразить сценарий AI-публикации БТ из завершённой симуляции | open |
| `baseline/current/domain/business-rules.md` | новые правила доступа и публикации БТ из симуляции | open |
| `baseline/current/domain/contexts/identity-and-access.md` | канонизировать использование роли `experiment_editor_CC` в этом сценарии | open |
| `baseline/current/api/README.md` | описать новый интеграционный контракт с агентом | open |
| `baseline/current/ui/README.md` | зафиксировать страницу-хост и UX диалога | open |

## Affected prototypes

### Scope prototypes
| Path | Impact | Sync status |
|---|---|---|
| `features/simulation-bt-agent/planning/scope-prototype/prototype.html` | может понадобиться позднее для customer alignment, но сейчас не обязателен | no-update-needed |

### Delivery prototypes
| Path | Impact | Sync status |
|---|---|---|
| `features/simulation-bt-agent/slices/dialog-session/delivery-prototype/prototype.html` | пока отсутствует; создать при переходе в delivery-prototype mode | no-update-needed |

## Prototype sync status values
- `must-update-now` — prototype is an active handoff/scope artifact and must be updated.
- `defer-ok` — known drift is acceptable until user asks to actualize prototypes.
- `no-update-needed` — decision does not affect the prototype.
- `obsolete` — prototype should no longer be treated as current.

## Required consistency actions
- [ ] local feature requirements updated
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
