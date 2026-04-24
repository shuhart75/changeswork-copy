# Задачи для интеграции ЖЦ Pilot/Deployment с процессом согласования (MVP v6.7)

**Источник правды:** [`spec/domain_model.md`](/home/reutov/Documents/AI/changesWork/spec/domain_model.md)

## Обзор

**Компонент:** Связка `ApprovalInstance` (решения) с жизненными циклами `Pilot` и `Deployment`.  
**Статус:** Новая разработка

### Что реализуется

> Граница ответственности (важно): `BE-INT1` реализует **интеграционные обработчики** (реакцию на события `ApprovalInstance`) и переводит статусы доменных сущностей/версий.  
> Сами state machine, модели версий и action endpoints жизненного цикла (`submit_for_approval`, `complete`, `deploy`, `rollback`) описаны в `BE-PL1` (пилот) и `BE-CL1` (внедрение).

- Pilot (версионирование):
  - `draft -> requires_activation` при отправке **версии** на согласование (submit)
  - при успешном завершении согласования/утверждения: `requires_activation -> active` и публикация версии как текущей (swap current_version у Pilot)
    - предыдущая current-версия переводится в **inactive** (не-active)
  - при отклонении: `* -> approval_rejected|ratification_rejected` (для версии)
- Deployment:
  - `draft -> requires_approval` при отправке на согласование (submit)
  - при успешном завершении согласования/утверждения: `requires_approval -> approved`
  - при отклонении: `* -> approval_rejected|ratification_rejected`
- `auto_ratification`:
  - если `true`: ratification происходит индивидуально (ApprovalInstance приводит к финальному решению)
  - если `false`: после approval-этапов ставим `awaiting_ratification=true` и ждём команды пользователя на запуск ratification (индивидуально или через `Package`)

---

## BE-INT1: Backend интеграции ЖЦ в процесс согласования

**Тип:** Story  
**Приоритет:** Критический  
**Оценка:** 5 дней

### Summary
Реализация обработчиков событий изменения статуса `ApprovalInstance` и корректной синхронизации статусов Pilot/Deployment.

### Description

1. **Единая точка интеграции**
   - В `BE-AP1` (создание/обновление ApprovalInstance) добавить вызовы интеграции, либо оформить через domain-service:
     - `on_approval_instance_completed(instance)`
     - `on_approval_instance_rejected(instance, reason)`
     - `on_approval_instance_cancelled(instance)`

2. **Матрица переходов (минимально для MVP v6.7)**
   - PilotVersion:
     - approved/ratified -> `active` + сделать версию текущей (предыдущая current-версия остаётся активной до этого момента)
     - rejected(at approval) -> `approval_rejected`
     - rejected(at ratification) -> `ratification_rejected`
     - cancelled -> возврат в `pre_submit_status` (для версии)
   - Deployment:
     - approved/ratified -> `approved`
     - rejected(at approval) -> `approval_rejected`
     - rejected(at ratification) -> `ratification_rejected`
     - cancelled -> возврат в `pre_submit_status`

3. **awaiting_ratification**
   - Если для target включена ratification (`ratification_required=true`) и `auto_ratification=false`, и approval-этапы завершены успешно:
     - выставить `awaiting_ratification=true`
     - не переводить target в финальный approved/active до прохождения ratification (индивидуально или через Package)

4. **Синхронизация скоркарт (hook, без глубоких деталей)**
   - Обновление статусов `Scorecard`/`ScorecardVersion` оставляем как часть отдельной реализации, но в BE-INT1 фиксируем места вызовов:
     - при переводе Pilot/Deployment в `requires_*` и при финальном `approved/active/deployed`

### Acceptance Criteria

- [ ] Внедрены обработчики событий `ApprovalInstance` и переходы статусов Pilot/Deployment
- [ ] Работает ветка `auto_ratification=false` (попадание в `awaiting_ratification`)
- [ ] Для rejected корректно выставляются статусы `approval_rejected|ratification_rejected`
- [ ] Для cancelled (recall) target возвращается в `pre_submit_status`
- [ ] Логи/аудит событий интеграции присутствуют

### Dependencies

 - `BE-AP1` ([mvp_tasks_approval_process_backend.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.7/tasks/mvp_tasks_approval_process_backend.md))
 - `BE-PL1` ([mvp_tasks_pilot_lifecycle.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.7/tasks/mvp_tasks_pilot_lifecycle.md))
 - `BE-CL1` ([mvp_tasks_deployment_lifecycle.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.7/tasks/mvp_tasks_deployment_lifecycle.md))
