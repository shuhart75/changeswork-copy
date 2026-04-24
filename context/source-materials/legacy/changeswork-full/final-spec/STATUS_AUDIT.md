# Аудит статусов системы

**Дата:** 2026-03-21  
**Цель:** зафиксировать актуальную статусную модель и убрать legacy-значения из активных требований.

## Канонические источники

- `final-spec/REQ_approval_core.md`
- `final-spec/REQ_approvals_page_backend.md`
- `final-spec/REQ_packages_page_backend.md`
- `final-spec/REQ_deployments_backend.md`
- `final-spec/REQ_pilots_backend.md`

## Зафиксированная модель

### ApprovalInstance

`ApprovalInstance` является единственным источником текущего состояния процесса согласования/утверждения.

Допустимые статусы:
- `in_approval`
- `approved`
- `awaiting_ratification`
- `in_ratification`
- `ratified`
- `approval_rejected`
- `ratification_rejected`
- `approval_cancelled`
- `ratification_cancelled`

Правила:
- значения задаются в `lowercase_with_underscores`;
- legacy-статусы `PENDING`, `IN_PROGRESS`, `REJECTED`, `CANCELLED` не используются;
- отдельное поле `current_stage` в API не возвращается.

### Этапы внутри `process_snapshot`

Для этапов внутри `approval_instance.process_snapshot` отдельный enum статусов не задаётся.

Состояние этапа для UI определяется по совокупности полей:
- `started_at`;
- `completed_at`;
- `pending_assignees`;
- `decisions`.

Следствия:
- поля `status` у этапа в контракте нет;
- значения вида `pending`, `in_progress`, `approved`, `rejected`, `cancelled` как статус этапа не используются.

### Package

`Package` в MVP является рабочей группировкой нескольких `ApprovalInstance`, а не самостоятельным процессом согласования.

Правила:
- пакет создаётся только из 2 и более элементов в `awaiting_ratification`;
- после создания пакет сразу считается отправленным;
- отдельного статуса пакета нет;
- активный состав пакета определяется по `approval_instance.package_id`;
- отдельные сущности `package_item` и `package_item_decision` в MVP не используются;
- при сокращении активного состава меньше чем до 2 элементов пакет перестаёт существовать как активная группировка, но запись `package` сохраняется для истории.

Минимальный состав таблицы `package`:
- `id`;
- `brief_subject`;
- `brief_body`;
- `created_by`;
- `created_at`.

Поля `status`, `name`, `description`, `ratifier_id` отсутствуют.

### DeploymentVersion

Для версий внедрения используются статусы:
- `draft`
- `requires_approval`
- `in_approval`
- `approved`
- `awaiting_ratification`
- `in_ratification`
- `ratified`
- `approval_rejected`
- `ratification_rejected`
- `approval_cancelled`
- `ratification_cancelled`
- `deployed`
- `rolled_back`
- `archived`

### PilotVersion

Для версий пилота используются статусы:
- `draft`
- `requires_activation`
- `in_approval`
- `approved`
- `awaiting_ratification`
- `in_ratification`
- `ratified`
- `approval_rejected`
- `ratification_rejected`
- `approval_cancelled`
- `ratification_cancelled`
- `active`
- `requires_correction`
- `completed`

## Что считается несоответствием

Несоответствием в активных требованиях считаются:
- любые UPPERCASE-статусы для `ApprovalInstance`;
- отдельный статус этапа внутри `process_snapshot`;
- поле `current_stage` в API страниц `Согласования` и `Пакеты`;
- таблицы или сущности `package_item`, `package_item_decision`;
- собственный статус пакета.

## Итог

В активной спецификации статусная модель согласования унифицирована:
- состояние процесса определяется только `ApprovalInstance.status`;
- состояние этапов выводится без отдельного поля статуса;
- пакет не имеет собственной статусной модели и не требует `package_item`.
