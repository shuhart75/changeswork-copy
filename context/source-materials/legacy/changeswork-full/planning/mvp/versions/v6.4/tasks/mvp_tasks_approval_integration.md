# Задачи для интеграции ЖЦ Pilot/Deployment с процессом согласования (MVP v6.4)

**Источник правды:** [`spec/domain_model.md`](/home/reutov/Documents/AI/changesWork/spec/domain_model.md)

## Обзор

**Компонент:** Связка `ApprovalInstance` (решения) с жизненными циклами `Pilot` и `Deployment`.  
**Статус:** Новая разработка

### Что реализуется

- Pilot:
  - `draft -> requires_activation` при отправке на согласование (submit)
  - при успешном завершении согласования/утверждения: `requires_activation|requires_correction -> active` (и фиксация метаданных активации)
  - при отклонении: `* -> requires_correction`
- Deployment:
  - `draft -> requires_approval` при отправке на согласование (submit)
  - при успешном завершении согласования/утверждения: `requires_approval -> approved`
  - при отклонении: `* -> draft`
- `auto_ratification`:
  - если `true`: ratification происходит индивидуально (ApprovalInstance приводит к финальному решению)
  - если `false`: после approval-этапов ставим `awaiting_ratification=true` и переносим утверждение в `Package`

---

## BE-INT1: Backend интеграции ЖЦ в процесс согласования

**Тип:** Story  
**Приоритет:** Критический  
**Оценка:** 3 дня

### Summary
Реализация обработчиков событий изменения статуса `ApprovalInstance` и корректной синхронизации статусов Pilot/Deployment.

### Description

1. **Единая точка интеграции**
   - В `BE-AP1` (создание/обновление ApprovalInstance) добавить вызовы интеграции, либо оформить через domain-service:
     - `on_approval_instance_completed(instance)`
     - `on_approval_instance_rejected(instance, reason)`
     - `on_approval_instance_cancelled(instance)`

2. **Матрица переходов (минимально для MVP v6.4)**
   - Pilot:
     - approved/ratified -> `active`
     - rejected -> `requires_correction`
     - cancelled -> возврат в предыдущий рабочий статус (обычно `draft` или `requires_correction`)
   - Deployment:
     - approved/ratified -> `approved`
     - rejected -> `draft`
     - cancelled -> `draft`

3. **awaiting_ratification**
   - Если у target задан ratifier и `auto_ratification=false`, и approval-этапы завершены успешно:
     - выставить `awaiting_ratification=true`
     - не переводить target в финальный approved/active до прохождения ratification (через Package)

4. **Синхронизация скоркарт (hook, без глубоких деталей)**
   - Обновление статусов `Scorecard`/`ScorecardVersion` оставляем как часть отдельной реализации, но в BE-INT1 фиксируем места вызовов:
     - при переводе Pilot/Deployment в `requires_*` и при финальном `approved/active/deployed`

### Acceptance Criteria

- [ ] Внедрены обработчики событий `ApprovalInstance` и переходы статусов Pilot/Deployment
- [ ] Работает ветка `auto_ratification=false` (попадание в `awaiting_ratification`)
- [ ] Для rejected/cancelled корректно выставляются статусы target-сущностей
- [ ] Логи/аудит событий интеграции присутствуют

### Dependencies

 - `BE-AP1` ([mvp_tasks_approval_process_backend.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.4/tasks/mvp_tasks_approval_process_backend.md))
 - `BE-PL1` ([mvp_tasks_pilot_lifecycle.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.3/tasks/mvp_tasks_pilot_lifecycle.md))
 - `BE-CL1` ([mvp_tasks_deployment_lifecycle.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.3/tasks/mvp_tasks_deployment_lifecycle.md))
