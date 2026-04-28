# Consistency Backlog

This backlog tracks known cross-feature, domain-wide, baseline, and prototype consistency work.

## Status values
- `open` — known impact, not yet propagated.
- `in-progress` — propagation is underway.
- `propagated` — required artifacts were updated.
- `deferred` — consciously postponed.
- `cancelled` — source decision was cancelled before release.
- `rolled-back` — propagated change was reversed by later work.
- `rollback-propagation-required` — rollback happened and dependent artifacts still need sync.

## Consistency levels
- `local`
- `cross-feature`
- `domain-wide`

## Items

| ID | Decision ID | Source feature | Level | Status | Affected requirements | Affected baseline | Affected prototypes | Notes |
|---|---|---|---|---|---|---|---|---|
| CONS-YYYY-MM-DD-001 | DEC-YYYY-MM-DD-FEATURE-001 | `features/<feature>/` | cross-feature | open | `features/<other>/...` | `baseline/current/...` | `features/<feature>/.../prototype.html` | <short note> |
| CONS-2026-04-24-001 | DEC-2026-04-24-SIMULATION-BT-AGENT-001 | `features/simulation-bt-agent/` | domain-wide | open | `features/roles/slices/rbac/requirements/frontend.md` | `baseline/current/domain/contexts/research-and-execution.md`, `baseline/current/domain/business-rules.md`, `baseline/current/domain/contexts/identity-and-access.md`, `baseline/current/api/README.md`, `baseline/current/ui/README.md` | `—` | Requirement packs созданы, но baseline/roles propagation по самому сценарию формирования БТ через окно агента ещё не выполнена. |
| CONS-2026-04-27-002 | DEC-2026-04-27-SIMULATION-BT-AGENT-002 | `features/simulation-bt-agent/` | domain-wide | open | `features/roles/slices/rbac/requirements/frontend.md` | `baseline/current/domain/contexts/research-and-execution.md`, `baseline/current/domain/business-rules.md`, `baseline/current/domain/contexts/identity-and-access.md`, `baseline/current/api/README.md`, `baseline/current/ui/README.md` | `—` | После доработки от 2026-04-27 нужно отдельно протянуть в baseline глобальное неблокирующее окно агента, open/restore по `session_id` и BT-specific действие только в eligible simulation context. Planning-артефакты feature всё ещё описывают старую модель `contextPrompt`/`POST /dialog/init` и требуют отдельной planning-синхронизации. |
| CONS-2026-04-27-003 | DEC-2026-04-27-SIMULATION-BT-AGENT-002 | `features/simulation-bt-agent/` | local | propagated | `features/simulation-bt-agent/requirements.md`, `features/simulation-bt-agent/slices/dialog-session/requirements/frontend.md`, `features/simulation-bt-agent/slices/bt-publication/requirements/frontend.md` | `baseline/current/ui/README.md` | `features/simulation-bt-agent/slices/agent-entrypoint/delivery-prototype/prototype.html`, `features/simulation-bt-agent/slices/dialog-session/delivery-prototype/prototype.html`, `features/simulation-bt-agent/slices/bt-publication/delivery-prototype/prototype.html` | Root prototype, living requirements и все три delivery prototype синхронизированы под новый UX панели агента: status chip в шапке, chat area без промежуточных блоков, поле ввода на 5 строк с внутренним скроллом и tooltip у `Сформировать БТ`. Baseline UI описание остаётся отдельной задачей. |
| CONS-2026-04-27-004 | DEC-2026-04-27-SIMULATION-BT-AGENT-003 | `features/simulation-bt-agent/` | domain-wide | deferred | `features/simulation-bt-agent/requirements.md`, `features/simulation-bt-agent/slices/bt-publication/slice.md`, `features/simulation-bt-agent/slices/bt-publication/requirements/frontend.md`, `features/simulation-bt-agent/slices/bt-publication/requirements/backend.md` | `baseline/current/domain/business-rules.md`, `baseline/current/api/README.md`, `baseline/current/ui/README.md` | `—` | В living requirements и прототипах MVP уже переведён на возврат `btUrl` для ручного копирования без автоматического сохранения ссылки в симуляцию. Отдельно остаётся актуализировать только baseline-описания под новый сценарий. |
| CONS-2026-04-28-005 | DEC-2026-04-28-SIMULATION-BT-AGENT-004 | `features/simulation-bt-agent/` | domain-wide | open | `features/simulation-bt-agent/requirements.md`, `features/simulation-bt-agent/slices/agent-entrypoint/slice.md`, `features/simulation-bt-agent/slices/agent-entrypoint/requirements/backend.md`, `features/simulation-bt-agent/slices/bt-publication/slice.md`, `features/simulation-bt-agent/slices/bt-publication/requirements/backend.md` | `baseline/current/api/README.md`, `baseline/current/domain/business-rules.md`, `baseline/current/ui/README.md` | `—` | Living requirements теперь явно фиксируют, что BT-сценарий не получает отдельный preparatory backend-контракт: фронт использует уже реализованный `GET /api/v1/simulation/{number}` как источник доступности и данных страницы. Baseline и соседние narrative-артефакты ещё нужно синхронизировать под это API-решение. |
| CONS-2026-04-28-006 | DEC-2026-04-28-SIMULATION-BT-AGENT-005 | `features/simulation-bt-agent/` | domain-wide | open | `features/simulation-bt-agent/requirements.md`, `features/simulation-bt-agent/slices/agent-entrypoint/requirements/frontend.md`, `features/simulation-bt-agent/slices/agent-entrypoint/requirements/backend.md`, `features/simulation-bt-agent/slices/dialog-session/requirements/frontend.md`, `features/simulation-bt-agent/slices/dialog-session/requirements/backend.md` | `baseline/current/api/README.md`, `baseline/current/domain/business-rules.md`, `baseline/current/ui/README.md` | `—` | В living requirements явно зафиксировано, что `session_id` локально генерируется фронтом как UUID, хранится в пользовательской сессии АС КОДА и приводит к созданию серверной сессии только на первом unseen значении. Baseline API и narrative-артефакты нужно отдельно синхронизировать под это правило. |
