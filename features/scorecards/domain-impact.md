# Domain Impact — scorecards

Дата обновления: `2026-06-08`
Baseline target: `baseline/current/domain/`

## Decision registry

| Decision ID | Summary | Status | Consistency level | Source | Supersedes | Reverted by |
|---|---|---|---|---|---|---|
| DEC-2026-04-23-SCORECARDS-001 | Скоркарта — самостоятельный агрегат со status model `active/archive`, versioning и binding через доменные формы | accepted | domain-wide | `features/scorecards/slices/workspace/requirements/backend.md` |  |  |
| DEC-2026-05-12-SCORECARDS-002 | Сценарии редактирования скоркарт 271-300: лимит 15, запрет удаления последней скоркарты, 409/422 ошибки | accepted | cross-feature | `features/scorecards/slices/workspace/requirements/frontend.md` |  |  |

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
- У версии сущности не более 15 связанных скоркарт.
- У версии сущности должна оставаться минимум одна скоркарта; удаление последней связи запрещено.
- При попытке удалить последнюю скоркарту backend возвращает `422` и сообщение `Нельзя удалить последнюю скоркарту`.
- При попытке привязать больше 15 скоркарт backend возвращает `422` и сообщение `Достигнут лимит (15)`.
- Одна версия скоркарты может быть связана только с одной версией сущности; повторное использование уже связанной версии возвращает `409`.

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
| `features/scorecards/slices/workspace/requirements/frontend.md` | create/edit/detail, binding semantics, сценарии 271-300 | propagated |
| `features/scorecards/slices/workspace/requirements/backend.md` | запрет удаления последней скоркарты, лимит 15, 409 для повторного использования версии | propagated |
| `features/pilots/slices/workspace/requirements/frontend.md` | интеграция с запретом удаления последней скоркарты и disabled lifecycle без скоркарт | open |
| `features/pilots/slices/workspace/requirements/backend.md` | уже содержит запрет удаления последней скоркарты; требуется сверка лимита 15 и 409 reuse | open |
| `features/deployments/slices/workspace/requirements/frontend.md` | интеграция со скоркартами, лимит 15 и обязательная lineage-скоркарта | deferred |

## Affected baseline artifacts

| Path | Impact | Sync status |
|---|---|---|
| `baseline/current/domain/contexts/scorecards.md` | canonical scorecards rules, включая 15/409/422 | open |
| `baseline/current/domain/contexts/scorecard-templates.md` | template semantics | propagated |
| `baseline/current/domain/aggregates/scorecard.md` | aggregate invariants, включая запрет удаления последней скоркарты | open |
| `baseline/current/domain/business-rules.md` | cross-context rules для Pilot/Deployment binding | open |

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
- [x] neighboring feature requirements updated or backlog item created
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
