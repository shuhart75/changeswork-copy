# Задачи для процесса согласования/утверждения (Approval Process Backend)

## Обзор

**Компонент:** Универсальный процесс согласования/утверждения
**Статус:** Новая разработка

### Что реализуется:

**Двухэтапный процесс:**
1. **Согласование (Approval)** - первый этап, согласующие риск-менеджеры
2. **Утверждение (Ratification)** - второй этап, руководство

**Сущности, участвующие в процессе:**
- Pilot (когда status = 'requires_activation' или 'requires_correction')
- Change (когда status = 'requires_approval')
- Package (группа Цепочек с одинаковым маршрутом)

**Маршрут согласования:**
- Определяется при отправке на согласование
- Состоит из этапов (stages): Approval → Ratification
- Каждый этап имеет список согласующих (approvers)
- Согласующие назначаются пользователем при отправке

**Статусы согласования:**
- pending - ожидает согласования
- in_progress - в процессе согласования
- approved - согласовано (этап пройден)
- rejected - отклонено
- completed - завершено (все этапы пройдены)

---

## BE-AP1: Backend для процесса согласования/утверждения

**Тип:** Story
**Приоритет:** Критический
**Оценка:** 8 дней

### Summary
Реализация универсального двухэтапного процесса согласования/утверждения для Pilot, Change и Package

### Description

Реализовать Backend для универсального процесса согласования/утверждения:

1. **Модель данных ApprovalWorkflow:**

   ```python
   class ApprovalWorkflow(models.Model):
       """Процесс согласования"""
       id = models.UUIDField(primary_key=True, default=uuid.uuid4)

       # Полиморфная связь с сущностью
       entity_type = models.CharField(max_length=50)  # 'pilot', 'change', 'package'
       entity_id = models.UUIDField()

       # Статус процесса
       status = models.CharField(
           max_length=50,
           choices=[
               ('pending', 'Ожидает'),
               ('in_progress', 'В процессе'),
               ('approved', 'Согласовано'),
               ('rejected', 'Отклонено'),
               ('completed', 'Завершено')
           ],
           default='pending'
       )

       # Метаданные
       submitted_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='submitted_approvals')
       submitted_at = models.DateTimeField(auto_now_add=True)
       completed_at = models.DateTimeField(null=True, blank=True)

       # Текущий этап
       current_stage = models.IntegerField(default=0)  # 0 = Approval, 1 = Ratification

       class Meta:
           db_table = 'approval_workflow'
           indexes = [
               models.Index(fields=['entity_type', 'entity_id']),
               models.Index(fields=['status']),
           ]
   ```

2. **Модель данных ApprovalStage:**

   ```python
   class ApprovalStage(models.Model):
       """Этап согласования"""
       id = models.UUIDField(primary_key=True, default=uuid.uuid4)
       workflow = models.ForeignKey(ApprovalWorkflow, on_delete=models.CASCADE, related_name='stages')

       # Порядок этапа
       order = models.IntegerField()  # 0 = Approval, 1 = Ratification

       # Название этапа
       name = models.CharField(max_length=100)  # 'Согласование', 'Утверждение'

       # Статус этапа
       status = models.CharField(
           max_length=50,
           choices=[
               ('pending', 'Ожидает'),
               ('in_progress', 'В процессе'),
               ('approved', 'Согласовано'),
               ('rejected', 'Отклонено')
           ],
           default='pending'
       )

       # Метаданные
       started_at = models.DateTimeField(null=True, blank=True)
       completed_at = models.DateTimeField(null=True, blank=True)

       class Meta:
           db_table = 'approval_stage'
           ordering = ['order']
   ```

3. **Модель данных ApprovalDecision:**

   ```python
   class ApprovalDecision(models.Model):
       """Решение согласующего"""
       id = models.UUIDField(primary_key=True, default=uuid.uuid4)
       stage = models.ForeignKey(ApprovalStage, on_delete=models.CASCADE, related_name='decisions')

       # Согласующий
       approver = models.ForeignKey(User, on_delete=models.PROTECT, related_name='approval_decisions')

       # Решение
       decision = models.CharField(
           max_length=50,
           choices=[
               ('pending', 'Ожидает'),
               ('approved', 'Согласовано'),
               ('rejected', 'Отклонено')
           ],
           default='pending'
       )

       # Комментарий
       comment = models.TextField(blank=True)

       # Метаданные
       decided_at = models.DateTimeField(null=True, blank=True)

       class Meta:
           db_table = 'approval_decision'
           unique_together = [['stage', 'approver']]
   ```

4. **API Endpoints:**

   **POST /api/pilots/{id}/submit_for_approval/**
   - Отправка Pilot на согласование
   - Параметры: approval_route (список согласующих для каждого этапа)
   - Создание ApprovalWorkflow, ApprovalStage, ApprovalDecision
   - Обновление статуса Pilot → requires_activation
   - Отправка уведомлений согласующим первого этапа
   - Возврат: 200 OK или 400 Bad Request

   **POST /api/changes/{id}/submit_for_approval/**
   - Отправка Change на согласование
   - Параметры: approval_route
   - Создание ApprovalWorkflow, ApprovalStage, ApprovalDecision
   - Обновление статуса Change → requires_approval
   - Отправка уведомлений согласующим первого этапа
   - Возврат: 200 OK или 400 Bad Request

   **POST /api/packages/{id}/submit_for_approval/**
   - Отправка Package на согласование
   - Параметры: approval_route
   - Валидация: все Цепочки в Package должны иметь одинаковые маршруты
   - Создание ApprovalWorkflow, ApprovalStage, ApprovalDecision
   - Отправка уведомлений согласующим первого этапа
   - Возврат: 200 OK или 400 Bad Request

   **POST /api/approval-workflows/{id}/approve/**
   - Согласование текущего этапа
   - Параметры: comment (optional)
   - Обновление ApprovalDecision для текущего пользователя
   - Проверка: все ли согласующие этапа приняли решение
   - Если все согласовали → переход к следующему этапу или завершение
   - Отправка уведомлений
   - Возврат: 200 OK или 400 Bad Request

   **POST /api/approval-workflows/{id}/reject/**
   - Отклонение согласования
   - Параметры: comment (обязательный)
   - Обновление ApprovalDecision для текущего пользователя
   - Обновление статуса ApprovalWorkflow → rejected
   - Возврат сущности в предыдущий статус (draft для Change, requires_correction для Pilot)
   - Отправка уведомлений
   - Возврат: 200 OK или 400 Bad Request

   **GET /api/approval-workflows/?entity_type=&entity_id=**
   - Получение процесса согласования для сущности
   - Фильтрация по entity_type, entity_id
   - Возврат: ApprovalWorkflow с вложенными stages и decisions

   **GET /api/approval-workflows/my/**
   - Получение списка согласований, где текущий пользователь назначен согласующим
   - Фильтрация по статусу (pending, in_progress)
   - Пагинация
   - Возврат: список ApprovalWorkflow

5. **Бизнес-логика:**

   **БП-1: Создание процесса согласования**
   ```python
   def create_approval_workflow(entity_type, entity_id, approval_route, submitted_by):
       """Создание процесса согласования"""
       workflow = ApprovalWorkflow.objects.create(
           entity_type=entity_type,
           entity_id=entity_id,
           status='in_progress',
           submitted_by=submitted_by,
           current_stage=0
       )

       # Создание этапов
       for order, stage_data in enumerate(approval_route):
           stage = ApprovalStage.objects.create(
               workflow=workflow,
               order=order,
               name=stage_data['name'],
               status='in_progress' if order == 0 else 'pending'
           )

           # Создание решений для согласующих
           for approver_id in stage_data['approvers']:
               ApprovalDecision.objects.create(
                   stage=stage,
                   approver_id=approver_id,
                   decision='pending'
               )

       return workflow
   ```

   **БП-2: Согласование этапа**
   ```python
   def approve_stage(workflow_id, user, comment=''):
       """Согласование текущего этапа"""
       workflow = ApprovalWorkflow.objects.get(id=workflow_id)
       current_stage = workflow.stages.get(order=workflow.current_stage)

       # Обновление решения пользователя
       decision = ApprovalDecision.objects.get(
           stage=current_stage,
           approver=user
       )
       decision.decision = 'approved'
       decision.comment = comment
       decision.decided_at = timezone.now()
       decision.save()

       # Проверка: все ли согласовали
       all_approved = all(
           d.decision == 'approved'
           for d in current_stage.decisions.all()
       )

       if all_approved:
           # Завершение текущего этапа
           current_stage.status = 'approved'
           current_stage.completed_at = timezone.now()
           current_stage.save()

           # Переход к следующему этапу или завершение
           next_stage = workflow.stages.filter(order=workflow.current_stage + 1).first()
           if next_stage:
               workflow.current_stage += 1
               next_stage.status = 'in_progress'
               next_stage.started_at = timezone.now()
               next_stage.save()
               workflow.save()
               # Отправка уведомлений согласующим следующего этапа
           else:
               # Все этапы пройдены
               workflow.status = 'completed'
               workflow.completed_at = timezone.now()
               workflow.save()
               # Обновление статуса сущности (approved для Change, active для Pilot)
   ```

   **БП-3: Отклонение согласования**
   ```python
   def reject_approval(workflow_id, user, comment):
       """Отклонение согласования"""
       workflow = ApprovalWorkflow.objects.get(id=workflow_id)
       current_stage = workflow.stages.get(order=workflow.current_stage)

       # Обновление решения пользователя
       decision = ApprovalDecision.objects.get(
           stage=current_stage,
           approver=user
       )
       decision.decision = 'rejected'
       decision.comment = comment
       decision.decided_at = timezone.now()
       decision.save()

       # Обновление статусов
       current_stage.status = 'rejected'
       current_stage.completed_at = timezone.now()
       current_stage.save()

       workflow.status = 'rejected'
       workflow.completed_at = timezone.now()
       workflow.save()

       # Возврат сущности в предыдущий статус
       # Change → draft, Pilot → requires_correction
   ```

6. **Права доступа:**
   - Отправить на согласование может: ПРМ (свой продукт), Методолог, Админ
   - Согласовать/отклонить может: только назначенный согласующий
   - Просмотреть процесс может: автор, согласующие, Админ

7. **Уведомления:**
   - При отправке на согласование → уведомления согласующим первого этапа
   - При согласовании этапа → уведомление автору + согласующим следующего этапа
   - При отклонении → уведомление автору
   - При завершении → уведомление автору

### Acceptance Criteria

- [ ] Модели ApprovalWorkflow, ApprovalStage, ApprovalDecision созданы
- [ ] Миграции применены
- [ ] POST /api/pilots/{id}/submit_for_approval/ endpoint реализован
- [ ] POST /api/changes/{id}/submit_for_approval/ endpoint реализован
- [ ] POST /api/packages/{id}/submit_for_approval/ endpoint реализован
- [ ] POST /api/approval-workflows/{id}/approve/ endpoint реализован
- [ ] POST /api/approval-workflows/{id}/reject/ endpoint реализован
- [ ] GET /api/approval-workflows/ endpoint реализован
- [ ] GET /api/approval-workflows/my/ endpoint реализован
- [ ] Создание процесса согласования работает
- [ ] Согласование этапа работает
- [ ] Переход к следующему этапу работает
- [ ] Завершение процесса работает
- [ ] Отклонение согласования работает
- [ ] Возврат сущности в предыдущий статус работает
- [ ] Права доступа реализованы
- [ ] Уведомления отправляются корректно
- [ ] Unit тесты покрывают все сценарии (coverage > 80%)
- [ ] Integration тесты для всех переходов
- [ ] API документация обновлена

### Dependencies
- BE-CL1 (требуется ЖЦ Change)

### Technical Notes

**Пример approval_route:**
```json
[
  {
    "name": "Согласование",
    "approvers": ["user-uuid-1", "user-uuid-2", "user-uuid-3"]
  },
  {
    "name": "Утверждение",
    "approvers": ["user-uuid-4", "user-uuid-5"]
  }
]
```

---

## Итоговая зависимость задач

```
BE-CL1 (5 дней)
  ↓
BE-AP1 (8 дней)
```

**Общая длительность (критический путь):** 13 дней

---

## ✅ Ключевые особенности

1. **Универсальный процесс** - работает для Pilot, Change, Package
2. **Двухэтапное согласование** - Approval → Ratification
3. **Полиморфная связь** - entity_type + entity_id
4. **Маршрут согласования** - определяется при отправке
5. **Множественные согласующие** - на каждом этапе
6. **Автоматический переход** - к следующему этапу после согласования всех
7. **Уведомления** - на каждом этапе процесса
8. **Права доступа** - только назначенные согласующие могут принимать решения

---
