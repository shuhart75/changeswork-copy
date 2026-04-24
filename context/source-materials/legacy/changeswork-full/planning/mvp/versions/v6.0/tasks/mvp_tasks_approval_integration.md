# Задачи для интеграции ЖЦ в процесс согласования

## Обзор

**Компонент:** Интеграция жизненных циклов Pilot, Change, Simulation в процесс согласования
**Статус:** Новая разработка

### Что реализуется:

**Интеграция ЖЦ с процессом согласования:**
- Pilot: requires_activation → процесс согласования → active
- Pilot: requires_correction → процесс согласования → active
- Change: requires_approval → процесс согласования → approved
- Simulation: НЕ участвует в процессе согласования (только draft → running → completed/failed)

**Автоматические действия:**
- При успешном согласовании Pilot → статус меняется на active
- При успешном согласовании Change → статус меняется на approved
- При отклонении Pilot → статус меняется на requires_correction
- При отклонении Change → статус меняется на draft

---

## BE-INT1: Backend для интеграции ЖЦ в процесс согласования

**Тип:** Story
**Приоритет:** Критический
**Оценка:** 3 дня

### Summary
Интеграция жизненных циклов Pilot и Change с процессом согласования/утверждения

### Description

Реализовать интеграцию ЖЦ Pilot и Change с процессом согласования:

1. **Интеграция Pilot с процессом согласования:**

   **Переходы с согласованием:**
   - requires_activation → [процесс согласования] → active
   - requires_correction → [процесс согласования] → active

   **Логика:**
   ```python
   def submit_pilot_for_approval(pilot_id, approval_route, user):
       """Отправка Pilot на согласование"""
       pilot = Pilot.objects.get(id=pilot_id)

       # Валидация статуса
       if pilot.status not in ['requires_activation', 'requires_correction']:
           raise ValidationError(
               "Pilot должен быть в статусе requires_activation или requires_correction"
           )

       # Создание процесса согласования
       workflow = create_approval_workflow(
           entity_type='pilot',
           entity_id=pilot.id,
           approval_route=approval_route,
           submitted_by=user
       )

       return workflow

   def complete_pilot_approval(pilot_id):
       """Завершение согласования Pilot"""
       pilot = Pilot.objects.get(id=pilot_id)

       # Обновление статуса
       pilot.status = 'active'
       pilot.activated_at = timezone.now()
       pilot.save()

       # Отправка уведомлений
       send_notification(
           user=pilot.created_by,
           message=f"Пилот {pilot.display_id} успешно согласован и активирован"
       )

   def reject_pilot_approval(pilot_id, reason):
       """Отклонение согласования Pilot"""
       pilot = Pilot.objects.get(id=pilot_id)

       # Обновление статуса
       pilot.status = 'requires_correction'
       pilot.rejection_reason = reason
       pilot.save()

       # Отправка уведомлений
       send_notification(
           user=pilot.created_by,
           message=f"Пилот {pilot.display_id} отклонен. Причина: {reason}"
       )
   ```

2. **Интеграция Change с процессом согласования:**

   **Переходы с согласованием:**
   - requires_approval → [процесс согласования] → approved

   **Логика:**
   ```python
   def submit_change_for_approval(change_id, approval_route, user):
       """Отправка Change на согласование"""
       change = Change.objects.get(id=change_id)

       # Валидация статуса
       if change.status != 'requires_approval':
           raise ValidationError(
               "Change должно быть в статусе requires_approval"
           )

       # Валидация минимум 1 скоркарты
       if not change.scorecards.exists():
           raise ValidationError(
               "Change должно быть связано минимум с 1 скоркартой"
           )

       # Создание процесса согласования
       workflow = create_approval_workflow(
           entity_type='change',
           entity_id=change.id,
           approval_route=approval_route,
           submitted_by=user
       )

       return workflow

   def complete_change_approval(change_id):
       """Завершение согласования Change"""
       change = Change.objects.get(id=change_id)

       # Обновление статуса
       change.status = 'approved'
       change.approved_at = timezone.now()
       change.save()

       # Отправка уведомлений
       send_notification(
           user=change.created_by,
           message=f"Изменение {change.display_id} успешно согласовано и утверждено"
       )

   def reject_change_approval(change_id, reason):
       """Отклонение согласования Change"""
       change = Change.objects.get(id=change_id)

       # Обновление статуса
       change.status = 'draft'
       change.rejection_reason = reason
       change.save()

       # Отправка уведомлений
       send_notification(
           user=change.created_by,
           message=f"Изменение {change.display_id} отклонено. Причина: {reason}"
       )
   ```

3. **Обработка событий процесса согласования:**

   **Signals для автоматической обработки:**
   ```python
   from django.db.models.signals import post_save
   from django.dispatch import receiver

   @receiver(post_save, sender=ApprovalWorkflow)
   def handle_approval_workflow_completion(sender, instance, **kwargs):
       """Обработка завершения процесса согласования"""
       if instance.status == 'completed':
           # Определение типа сущности
           if instance.entity_type == 'pilot':
               complete_pilot_approval(instance.entity_id)
           elif instance.entity_type == 'change':
               complete_change_approval(instance.entity_id)
           elif instance.entity_type == 'package':
               complete_package_approval(instance.entity_id)

       elif instance.status == 'rejected':
           # Получение причины отклонения
           rejection_reason = get_rejection_reason(instance)

           # Определение типа сущности
           if instance.entity_type == 'pilot':
               reject_pilot_approval(instance.entity_id, rejection_reason)
           elif instance.entity_type == 'change':
               reject_change_approval(instance.entity_id, rejection_reason)
           elif instance.entity_type == 'package':
               reject_package_approval(instance.entity_id, rejection_reason)

   def get_rejection_reason(workflow):
       """Получение причины отклонения из решений"""
       for stage in workflow.stages.all():
           for decision in stage.decisions.all():
               if decision.decision == 'rejected':
                   return decision.comment
       return "Не указана"
   ```

4. **API Endpoints (обновление):**

   **POST /api/pilots/{id}/submit_for_approval/**
   - Обновление: интеграция с ЖЦ Pilot
   - Валидация статуса: requires_activation или requires_correction
   - Создание ApprovalWorkflow
   - Возврат: 200 OK или 400 Bad Request

   **POST /api/changes/{id}/submit_for_approval/**
   - Обновление: интеграция с ЖЦ Change
   - Валидация статуса: requires_approval
   - Валидация минимум 1 скоркарты
   - Создание ApprovalWorkflow
   - Возврат: 200 OK или 400 Bad Request

5. **Бизнес-правила:**

   **БП-1: Pilot может быть отправлен на согласование только в статусах:**
   - requires_activation (первая отправка)
   - requires_correction (повторная отправка после отклонения)

   **БП-2: Change может быть отправлено на согласование только в статусе:**
   - requires_approval

   **БП-3: При успешном согласовании:**
   - Pilot → active (установка activated_at)
   - Change → approved (установка approved_at)

   **БП-4: При отклонении:**
   - Pilot → requires_correction (сохранение rejection_reason)
   - Change → draft (сохранение rejection_reason)

   **БП-5: Simulation НЕ участвует в процессе согласования:**
   - Simulation имеет свой независимый ЖЦ: draft → running → completed/failed

6. **Уведомления:**
   - При отправке на согласование → уведомления согласующим
   - При успешном согласовании → уведомление автору
   - При отклонении → уведомление автору с причиной

### Acceptance Criteria

- [ ] Интеграция Pilot с процессом согласования реализована
- [ ] Интеграция Change с процессом согласования реализована
- [ ] POST /api/pilots/{id}/submit_for_approval/ обновлен
- [ ] POST /api/changes/{id}/submit_for_approval/ обновлен
- [ ] Валидация статусов работает
- [ ] Автоматическое обновление статусов при завершении согласования работает
- [ ] Автоматическое обновление статусов при отклонении работает
- [ ] Signals для обработки событий реализованы
- [ ] Уведомления отправляются корректно
- [ ] Unit тесты покрывают все сценарии (coverage > 80%)
- [ ] Integration тесты для всех переходов
- [ ] API документация обновлена

### Dependencies
- BE-CL1 (требуется ЖЦ Change)
- BE-AP1 (требуется процесс согласования)

### Technical Notes

**Пример полного flow для Pilot:**
```python
# 1. Создание Pilot
pilot = Pilot.objects.create(
    deployment=deployment,
    name="Пилот оптимизации лимитов",
    status='draft'
)

# 2. Переход в requires_activation
pilot.status = 'requires_activation'
pilot.save()

# 3. Отправка на согласование
workflow = submit_pilot_for_approval(
    pilot_id=pilot.id,
    approval_route=[
        {
            "name": "Согласование",
            "approvers": ["user-1", "user-2"]
        },
        {
            "name": "Утверждение",
            "approvers": ["user-3"]
        }
    ],
    user=current_user
)

# 4. Согласование (автоматически через signals)
# После завершения всех этапов:
# - workflow.status = 'completed'
# - pilot.status = 'active'
# - pilot.activated_at = now()
```

**Пример полного flow для Change:**
```python
# 1. Создание Change
change = Change.objects.create(
    deployment=deployment,
    name="Внедрение новой скоркарты",
    status='draft'
)

# 2. Связь со скоркартами
change.scorecards.add(scorecard1, scorecard2)

# 3. Переход в requires_approval
change.status = 'requires_approval'
change.save()

# 4. Отправка на согласование
workflow = submit_change_for_approval(
    change_id=change.id,
    approval_route=[...],
    user=current_user
)

# 5. Согласование (автоматически через signals)
# После завершения всех этапов:
# - workflow.status = 'completed'
# - change.status = 'approved'
# - change.approved_at = now()
```

---

## Итоговая зависимость задач

```
BE-CL1 (5 дней)
  ↓
BE-AP1 (8 дней)
  ↓
BE-INT1 (3 дня)
```

**Общая длительность (критический путь):** 16 дней

---

## ✅ Ключевые особенности

1. **Интеграция ЖЦ с процессом согласования** - автоматическое обновление статусов
2. **Signals для обработки событий** - автоматическая реакция на завершение/отклонение
3. **Валидация статусов** - только определенные статусы могут быть отправлены на согласование
4. **Автоматические уведомления** - на каждом этапе процесса
5. **Сохранение причины отклонения** - rejection_reason в сущности
6. **Simulation не участвует** - независимый ЖЦ без согласования

---
