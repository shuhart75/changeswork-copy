# Задачи для процесса согласования/утверждения (Approval Process Backend, spec-aligned)

**Источник правды:** [`spec/domain_model.md`](/home/reutov/Documents/AI/changesWork/spec/domain_model.md)

## Обзор

**Компонент:** Динамический многоэтапный процесс согласования (Approval) и утверждения (Ratification)  
**Статус:** Новая разработка (в рамках v6.5)

### Что реализуется

**Объекты согласования (target):**
- `PilotVersion` (когда status = `requires_activation`)
- `DeploymentVersion` (когда status = `requires_approval`)
- `Package` (группа `PilotVersion`/`DeploymentVersion` для совместного утверждения, без draft-статуса)

**Ключевые принципы (как в spec):**
- Маршрут не предзадан: этапы создаются при отправке на согласование
- **Нет автоматической маршрутизации** по продукту/критичности в MVP: пользователь явно выбирает approvers по этапам и (опционально) ratifier.
- Этапы Approval: 0..* (последовательно между этапами, параллельно внутри этапа)
- Этап Ratification: 0..1 (ровно 1 ratifier)
- `auto_ratification`: если `true`, после Approval переходим в индивидуальную Ratification; если `false`, элемент попадает в очередь `awaiting_ratification`, после чего по команде пользователя может быть отправлен на Ratification индивидуально или через `Package`
- **Уточнение MVP v6.5:** если `auto_ratification=false`, элемент попадает в очередь `awaiting_ratification` и дальше по команде пользователя может быть отправлен на Ratification:
  - **индивидуально** (создать Ratification-этап для одной сущности),
  - **или через Package** (группой, с возможностью "одной кнопки" и поэлементных решений).
- Нельзя выбрать самого себя
- Для Approval-этапов можно выбирать только пользователей с ролью `approver`
- Для Ratification-этапа можно выбирать только пользователя с ролью `ratifier`

---

## AN-AP1: Аналитика процесса согласования/утверждения

**Тип:** Story  
**Приоритет:** Критический  
**Оценка:** 5 дней

### Summary
Зафиксировать MVP-правила процесса согласования (Approval) и утверждения (Ratification) и подготовить единый контракт (статусы, очереди, recall/reject, Package, права, API).

### Deliverables (что должно появиться по итогам)

1. **Набор правил и матрица переходов (MVP):**
   - Target-и согласования: `PilotVersion`, `DeploymentVersion`, `Package` (симуляции не участвуют)
   - `auto_ratification=true`: индивидуальная ratification сразу после approval
   - `auto_ratification=false`: попадание в очередь `awaiting_ratification` с возможностью запуска ratification:
     - индивидуально или
     - через `Package`
   - `Package`: обертка удобства для ratifier (одно письмо/одна кнопка), при этом статусы ratification хранятся по item
     - решение возможно "по всем item сразу" и "по item отдельно"
   - `reject` не возвращает в `draft`: `approval_rejected` / `ratification_rejected` (редактирование + повторная отправка + архивирование)
   - `recall` обязателен и работает и на approval, и на ratification (возврат в `pre_submit_status`)
   - `recall` поддерживается:
     - для PilotVersion/DeploymentVersion индивидуально
     - для Package целиком
     - для отдельных items внутри Package (item возвращается в `awaiting_ratification`, Package продолжает по оставшимся)

2. **API-спецификация MVP (черновик контракта):**
   - submit_for_approval (PilotVersion/DeploymentVersion)
   - approve/reject/ratify + batch (если нужно)
   - recall
   - запуск ratification из `awaiting_ratification`:
     - индивидуально
     - через Package

3. **Права доступа и видимость:**
   - кто может отправлять, отзывать, редактировать после reject
   - кто видит что на странице "Согласования" / "Пакеты"

### Acceptance Criteria

- [ ] Все правила из `spec/domain_model.md` и MVP-уточнений сведены в единый документ без противоречий
- [ ] Закрыты спорные места (минимальный список): выбор ratifier при `auto_ratification=false`, формат статусов/флагов `awaiting_ratification`, семантика batch-решений по Package
- [ ] API контракт согласован (на уровне полей/эндпоинтов/кодов ошибок)

---

## BE-AP1: Backend для процесса согласования/утверждения

**Тип:** Story  
**Приоритет:** Критический  
**Оценка:** 8 дней

### Summary
Реализация `ApprovalInstance` + этапов/назначений/решений и API для отправки/принятия решений по PilotVersion/DeploymentVersion/Package.

### Scope (минимально необходимое для MVP v6.5)

1. **Модель данных (Django/DRF, названия как в spec):**
   - `ApprovalInstance`:
     - `target_type` (`pilot_version`/`deployment_version`/`package`)
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
     - `comment` (опционально)
     - `decided_at`
   - `PackageItemDecision` (история решений ratifier по каждому item в составе Package):
     - `package_id`, `package_item_id`
     - `item_type` (`pilot_version`/`deployment_version`), `item_id`
     - `decision` (`ratified`/`ratification_rejected`/`recalled`/`released`)
     - `comment` (сохраняется **по каждому item отдельно**; при batch-утверждении всего Package префикс: `одобрено в составе пакета с комментарием: ...`)
     - `decided_by`, `decided_at`

2. **API: отправка на согласование**
   - `POST /api/pilot-versions/{id}/submit_for_approval/`
   - `POST /api/deployment-versions/{id}/submit_for_approval/`
   - Тело запроса (единый формат):
     - `approval_stages`: массив этапов Approval (0..*)
     - `ratification_required`: bool (нужен ли этап Ratification; **по умолчанию false**)
     - `ratifier_id`: UUID (опционально; обязателен если `ratification_required=true` и `auto_ratification=true`)
     - `auto_ratification`: bool (имеет смысл только если `ratification_required=true`)
   - Валидации:
    - target в допустимом статусе (PilotVersion: `requires_activation`; DeploymentVersion: `requires_approval`)
     - все `approver_id` имеют роль `approver`; если передан `ratifier_id`, то он имеет роль `ratifier`
     - пользователь не выбран в маршруте как approver/ratifier
     - хотя бы один этап в сумме (Approval или Ratification)
   - Побочные эффекты:
     - создаём `ApprovalInstance` + `ApprovalStage` + `ApprovalAssignment`
    - переводим PilotVersion: `draft -> requires_activation` (при отправке версии)
     - переводим DeploymentVersion: `draft -> requires_approval` (при отправке версии)
     - инициируем уведомления (см. `BE-NOT1`)

3. **API: принятие решений**
   - `POST /api/approval-instances/{id}/approve/`
   - `POST /api/approval-instances/{id}/reject/`
   - `POST /api/approval-instances/{id}/ratify/` (для ratification)
   - Валидации:
     - текущий пользователь назначен на текущий `ApprovalStage`
     - комментарий опционален для всех действий
   - Логика:
     - решение пишем в `ApprovalDecision`
      - если в этапе есть reject: этап/инстанс -> `rejected`, возвращаем target в рабочий статус:
       - PilotVersion/DeploymentVersion -> `approval_rejected` или `ratification_rejected` (в зависимости от этапа)
     - если все approve в этапе: двигаем `current_stage_order`, либо завершаем ApprovalInstance
     - при завершении Approval:
       - если `ratification_required=true` и `auto_ratification=true`: создаём ratification-этап (или отдельный ApprovalInstance для ratification, если так проще) и уведомляем ratifier
       - если `ratification_required=true` и `auto_ratification=false`: ставим target в `awaiting_ratification=true` (флаг/поле) и отображаем в очереди ожидания утверждения (можно утвердить индивидуально или через Package; ratifier выбирается при запуске ratification)
       - если `ratification_required=false`: считаем согласование завершённым (`approved`)

   **Ratification по Package (поэлементно и batch):**
   - При ratification target_type='package' решение сохраняется не только в `ApprovalDecision` (факт решения ratifier), но и **по каждому item**:
     - обновление `package_item.status` (ratified/ratification_rejected/recalled)
     - создание `PackageItemDecision` для каждого затронутого item с комментарием
   - Batch "утвердить весь пакет":
     - создаём `PackageItemDecision` на каждый item (кроме уже recalled)
     - comment для item сохраняем с префиксом `одобрено в составе пакета с комментарием: ...`
   - Поэлементные решения:
     - comment сохраняется как введён пользователем (без принудительного префикса)
   - Batch по выбранным items пакета:
     - по выбранным items применяем решение (ratified/ratification_rejected) и создаём PackageItemDecision
     - по НЕвыбранным items создаём PackageItemDecision(decision='released') и:
       - снимаем item из пакета (PackageItem.status='released')
       - создаём индивидуальный ratification-only ApprovalInstance для item с тем же ratifier (чтобы item появился в списке на утверждение как standalone)

4. **API: чтение**
   - `GET /api/approval-instances/{id}/` (деталка: stages, assignments, decisions)
   - `GET /api/approval-instances/my/?stage_type=approval|ratification` (для страницы "Согласования": только назначения текущего пользователя)
   - Для target_type='package' деталка должна включать состав пакета и историю `PackageItemDecision` по items (для отображения комментариев).

### Acceptance Criteria

- [ ] Реализованы модели `ApprovalInstance`, `ApprovalStage`, `ApprovalAssignment`, `ApprovalDecision`
- [ ] `POST /api/pilot-versions/{id}/submit_for_approval/` реализован и валидирует роли/самого себя
- [ ] `POST /api/deployment-versions/{id}/submit_for_approval/` реализован и валидирует роли/самого себя
- [ ] Решения по этапам работают (approve/reject/ratify) и корректно двигают процесс
- [ ] Для ratification в составе Package комментарий сохраняется **по каждому item отдельно** (через `PackageItemDecision`) и доступен:
  - в деталке Package/ApprovalInstance,
  - в истории каждого item (PilotVersion/DeploymentVersion)
- [ ] `auto_ratification` поддержан (индивидуальная ratification или `awaiting_ratification`)
- [ ] Reject переводит target в `approval_rejected` / `ratification_rejected` (не в draft)
- [ ] Recall (cancelled) реализован и возвращает target в `pre_submit_status`
- [ ] Права доступа на чтение "мои согласования" работают (только назначения)
- [ ] Интеграция уведомлений вызвана (фактическая отправка в `BE-NOT1`)
- [ ] Логи/аудит: события и решения сохраняются

### Dependencies

- `BE-CL1` ([mvp_tasks_deployment_lifecycle.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.5/tasks/mvp_tasks_deployment_lifecycle.md)) для статусов Deployment
- `BE-PL1` ([mvp_tasks_pilot_lifecycle.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.5/tasks/mvp_tasks_pilot_lifecycle.md)) для статусов Pilot
- `BE-NOT1` ([mvp_tasks_notifications.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.5/tasks/mvp_tasks_notifications.md)) для email/уведомлений
5. **API: recall (обязательно для MVP)**
   - `POST /api/approval-instances/{id}/recall/`
   - Валидации:
     - право: автор процесса или админ
     - статус instance: pending/in_progress
   - Побочный эффект:
     - `ApprovalInstance.status = cancelled`
     - target возвращается в `pre_submit_status` (сохранить в instance при submit)
