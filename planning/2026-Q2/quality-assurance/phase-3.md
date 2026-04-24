# QA Phase 3 — backend процессы

Дата обновления: `2026-04-24`
Источник: `context/source-materials/legacy/changeswork-full/planning/mvp/current/tasks/legacy/mvp_tasks_qa_phase3.md`
Оценка legacy: `3 дня`

## Фокус фазы

Интеграционное тестирование сложной backend-логики:
- lifecycle `Simulation`;
- lifecycle `Change`;
- lifecycle `Pilot`;
- approval / ratification процесс;
- интеграция lifecycle с approval flow;
- notifications.

## Основные сценарии

### Simulation lifecycle
- `draft -> running -> completed/failed`;
- запрет недопустимых переходов;
- независимость от approval flow.

### Change lifecycle
- обязательность минимум одной scorecard;
- автоматический расчёт критичности как `MAX`;
- переходы до `deployed` и `rolled_back`;
- запрет второго активного deployment одновременно.

### Pilot lifecycle
- путь `draft -> requires_activation -> active -> completed`;
- повторный submit после изменений;
- валидации и права доступа.

### Approval process
- двухэтапный процесс `Approval -> Ratification`;
- назначение approver / ratifier;
- approve / reject / batch operations;
- возвраты в корректные статусы.

### Notifications
- email-уведомления на ключевых переходах;
- корректность шаблонов;
- сохранение истории уведомлений.

## Deliverables

- отчёт о тестировании;
- список найденных багов;
- примеры email-уведомлений;
- фактические диаграммы переходов состояний.
