# Задачи для процесса согласования/утверждения (Approval Process Backend, spec-aligned)

**Источник правды:** [`spec/domain_model.md`](/home/reutov/Documents/AI/changesWork/spec/domain_model.md)

## Обзор

**Компонент:** Динамический многоэтапный процесс согласования (Approval) и утверждения (Ratification)  
**Статус:** Новая разработка (в рамках v6.1)

### Что реализуется

**Объекты согласования (target):**
- `Pilot` (когда status = `requires_activation` или `requires_correction`)
- `Deployment` (когда status = `requires_approval`)
- `Package` (группа `Pilot`/`Deployment` для совместного утверждения, без draft-статуса)

**Ключевые принципы (как в spec):**
- Маршрут не предзадан: этапы создаются при отправке на согласование
- Этапы Approval: 0..* (последовательно между этапами, параллельно внутри этапа)
- Этап Ratification: 0..1 (ровно 1 ratifier)
- `auto_ratification`: если `true`, после Approval переходим в индивидуальную Ratification; если `false`, элемент попадает в `awaiting_ratification` и ждёт формирования `Package`
- Нельзя выбрать самого себя
- Для Approval-этапов можно выбирать только пользователей с ролью `approver`
- Для Ratification-этапа можно выбирать только пользователя с ролью `ratifier`

---

## BE-AP1: Backend для процесса согласования/утверждения

**Тип:** Story  
**Приоритет:** Критический  
**Оценка:** 8 дней

### Summary
Реализация `ApprovalInstance` + этапов/назначений/решений и API для отправки/принятия решений по Pilot/Deployment/Package.

### Scope (минимально необходимое для MVP v6.1)

1. **Модель данных (Django/DRF, названия как в spec):**
   - `ApprovalInstance`:
     - `target_type` (`pilot`/`deployment`/`package`)
     - `target_id` (UUID)
     - `status` (`pending`/`in_progress`/`approved`/`rejected`/`cancelled`)
     - `auto_ratification` (bool)
     - `current_stage_order` (int)
     - `submitted_by`, `submitted_at`, `completed_at`
   - `ApprovalStage`:
     - `approval_instance_id`
     - `stage_type` (`approval`/`ratification`)
     - `stage_order` (1..N)
     - `status` (`pending`/`in_progress`/`approved`/`rejected`)
   - `ApprovalAssignment`:
     - `approval_stage_id`
     - `user_id`
   - `ApprovalDecision`:
     - `approval_stage_id`
     - `user_id`
     - `decision` (`approved`/`rejected`)
     - `comment` (обязателен при `rejected`)
     - `decided_at`

2. **API: отправка на согласование**
   - `POST /api/pilots/{id}/submit_for_approval/`
   - `POST /api/deployments/{id}/submit_for_approval/`
   - Тело запроса (единый формат):
     - `approval_stages`: массив этапов Approval (0..*)
     - `ratifier_id`: UUID (опционально)
     - `auto_ratification`: bool (имеет смысл только если задан `ratifier_id`)
   - Валидации:
     - target в допустимом статусе (Pilot: `draft` или `requires_correction`?; Deployment: `draft`)
     - все `approver_id` имеют роль `approver`, `ratifier_id` имеет роль `ratifier`
     - пользователь не выбран в маршруте как approver/ratifier
     - хотя бы один этап в сумме (Approval или Ratification)
   - Побочные эффекты:
     - создаём `ApprovalInstance` + `ApprovalStage` + `ApprovalAssignment`
     - переводим Pilot: `draft -> requires_activation` (или сохраняем `requires_correction`, если переотправка)
     - переводим Deployment: `draft -> requires_approval`
     - инициируем уведомления (см. `BE-NOT1`)

3. **API: принятие решений**
   - `POST /api/approval-instances/{id}/approve/`
   - `POST /api/approval-instances/{id}/reject/`
   - `POST /api/approval-instances/{id}/ratify/` (для ratification)
   - Валидации:
     - текущий пользователь назначен на текущий `ApprovalStage`
     - при `reject` комментарий обязателен
   - Логика:
     - решение пишем в `ApprovalDecision`
     - если в этапе есть reject: этап/инстанс -> `rejected`, возвращаем target в рабочий статус (Pilot -> `requires_correction`, Deployment -> `draft`)
     - если все approve в этапе: двигаем `current_stage_order`, либо завершаем ApprovalInstance
     - при завершении Approval:
       - если `ratifier_id` задан и `auto_ratification=true`: создаём ratification-этап (или отдельный ApprovalInstance для ratification, если так проще) и уведомляем ratifier
       - если `ratifier_id` задан и `auto_ratification=false`: ставим target в `awaiting_ratification=true` (флаг/поле) и отображаем на странице Package
       - если ratifier не задан: считаем согласование завершённым (`approved`)

4. **API: чтение**
   - `GET /api/approval-instances/{id}/` (деталка: stages, assignments, decisions)
   - `GET /api/approval-instances/my/?stage_type=approval|ratification` (для страницы "Согласования": только назначения текущего пользователя)

### Acceptance Criteria

- [ ] Реализованы модели `ApprovalInstance`, `ApprovalStage`, `ApprovalAssignment`, `ApprovalDecision`
- [ ] `POST /api/pilots/{id}/submit_for_approval/` реализован и валидирует роли/самого себя
- [ ] `POST /api/deployments/{id}/submit_for_approval/` реализован и валидирует роли/самого себя
- [ ] Решения по этапам работают (approve/reject/ratify) и корректно двигают процесс
- [ ] `auto_ratification` поддержан (индивидуальная ratification или `awaiting_ratification`)
- [ ] Права доступа на чтение "мои согласования" работают (только назначения)
- [ ] Интеграция уведомлений вызвана (фактическая отправка в `BE-NOT1`)
- [ ] Логи/аудит: события и решения сохраняются

### Dependencies

- `BE-CL1` ([mvp_tasks_deployment_lifecycle.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.1/tasks/mvp_tasks_deployment_lifecycle.md)) для статусов Deployment
- `BE-PL1` ([mvp_tasks_pilot_lifecycle.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.1/tasks/mvp_tasks_pilot_lifecycle.md)) для статусов Pilot
- `BE-NOT1` ([mvp_tasks_notifications.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.1/tasks/mvp_tasks_notifications.md)) для email/уведомлений

