# Задачи для жизненного цикла Внедрения (Deployment Lifecycle)

## Обзор

**Компонент:** Жизненный цикл Deployment (State Machine)
**Статус:** Новая разработка

### Что реализуется:

**Диаграмма состояний Deployment:**
```
draft → requires_approval → approved → deployed
                                         ↓
                                    rolled_back
```

**Переходы:**
- draft → requires_approval: отправка на согласование
- requires_approval → approved: успешное согласование и утверждение
- requires_approval → draft: отклонение, возврат на доработку
- approved → deployed: внедрение в продакшн
- deployed → rolled_back: откат изменения

**Бизнес-правила:**
- Deployment должно быть связано минимум с одной Скоркартой
- Только одно активное внедрение на Deployment (rollback_at = null)
- При deployed статус Initiative автоматически становится deployed
- При rollback создается новая запись с rollback_at
- Критичность рассчитывается автоматически: MAX(criticality) всех скоркарт

---

## BE-CL1: Backend для жизненного цикла Изменения

**Тип:** Story
**Приоритет:** Критический
**Оценка:** 5 дней

### Summary
Реализация state machine для жизненного цикла Change с валидацией переходов и автоматическим расчетом критичности

### Description

Реализовать Backend логику для управления жизненным циклом Change:

1. **State Machine для Change:**

   **Состояния:**
   - draft - черновик
   - requires_approval - отправлено на согласование
   - approved - согласовано и утверждено
   - deployed - внедрено в продакшн
   - rolled_back - откачено

   **Переходы:**
   ```python
   TRANSITIONS = {
       'draft': ['requires_approval'],
       'requires_approval': ['approved', 'draft'],
       'approved': ['deployed'],
       'deployed': ['rolled_back'],
       'rolled_back': []  # финальное состояние
   }
   ```

2. **API Endpoints:**

   **POST /api/changes/{id}/submit_for_approval/**
   - Переход: draft → requires_approval
   - Валидация: минимум 1 скоркарта связана
   - Создание записи в approval_workflow
   - Возврат: 200 OK или 400 Bad Request

   **POST /api/changes/{id}/approve/**
   - Переход: requires_approval → approved
   - Валидация: все этапы согласования пройдены
   - Обновление approval_workflow
   - Возврат: 200 OK или 400 Bad Request

   **POST /api/changes/{id}/reject/**
   - Переход: requires_approval → draft
   - Параметры: reason (обязательный)
   - Обновление approval_workflow
   - Возврат: 200 OK или 400 Bad Request

   **POST /api/changes/{id}/deploy/**
   - Переход: approved → deployed
   - Установка deployed_at = now()
   - Автоматическое обновление статуса Deployment → deployed
   - Возврат: 200 OK или 400 Bad Request

   **POST /api/changes/{id}/rollback/**
   - Переход: deployed → rolled_back
   - Параметры: reason (обязательный)
   - Установка rollback_at = now()
   - Создание новой записи Deployment (копия с новым ID)
   - Возврат: 200 OK или 400 Bad Request

3. **Бизнес-правила:**

   **БП-1: Валидация перехода draft → requires_approval**
   - Change должно быть связано минимум с 1 скоркартой
   - Все обязательные поля заполнены
   - HTTP 400 если валидация не прошла

   **БП-2: Автоматический расчет критичности**
   - При создании/обновлении Change
   - Критичность = MAX(criticality) всех связанных скоркарт
   - Если нет скоркарт → criticality = 'low'

   **БП-3: Обновление статуса Initiative**
   - При переходе Deployment в deployed → Initiative.status = deployed
   - Проверка: хотя бы одно Deployment в deployed

   **БП-4: Rollback**
   - Только для deployed Deployment
   - Установка rollback_at = now()
   - Создание новой записи Deployment (копия) со статусом draft
   - Связь с той же Initiative

   **БП-5: Только одно активное внедрение**
   - rollback_at = null означает активное внедрение
   - При rollback старая запись получает rollback_at, новая создается с rollback_at = null

4. **Валидация переходов:**
   ```python
   def validate_transition(change, new_status):
       """Валидация перехода состояния"""
       allowed = TRANSITIONS.get(change.status, [])
       if new_status not in allowed:
           raise ValidationError(
               f"Переход {change.status} → {new_status} недопустим"
           )

       # Дополнительные проверки
       if new_status == 'requires_approval':
           if not change.scorecards.exists():
               raise ValidationError(
                   "Change должно быть связано минимум с 1 скоркартой"
               )
   ```

5. **Автоматический расчет критичности:**
   ```python
   def calculate_criticality(change):
       """Рассчитать критичность как MAX критичности всех скоркарт"""
       scorecards = change.scorecards.all()
       if not scorecards:
           return 'low'

       criticality_order = {'low': 1, 'medium': 2, 'high': 3, 'critical': 4}
       max_criticality = max(
           criticality_order.get(sc.criticality, 1)
           for sc in scorecards
       )

       for level, value in criticality_order.items():
           if value == max_criticality:
               return level

       return 'low'
   ```

6. **Обновление статуса Initiative:**
   ```python
   def update_initiative_status(initiative):
       """Автоматическое обновление статуса Initiative"""
       deployments = initiative.deployments.all()

       # Если хотя бы одно Deployment в deployed → Initiative.status = deployed
       if any(d.status == 'deployed' for d in deployments):
           initiative.status = 'deployed'
           initiative.save()
   ```

7. **Rollback логика:**
   ```python
   def rollback_deployment(deployment, reason):
       """Откат внедрения"""
       if deployment.status != 'deployed':
           raise ValidationError("Можно откатить только deployed Deployment")

       # Установка rollback_at для текущей записи
       deployment.rollback_at = timezone.now()
       deployment.status = 'rolled_back'
       deployment.save()

       # Создание новой записи (копия)
       new_deployment = Deployment.objects.create(
           initiative=deployment.initiative,
           name=deployment.name,
           description=deployment.description,
           status='draft',
           rollback_reason=reason,
           rollback_at=None
       )

       # Копирование связей со скоркартами
       new_deployment.scorecards.set(deployment.scorecards.all())

       return new_deployment
   ```

### Acceptance Criteria

- [ ] State machine для Deployment реализована
- [ ] Все переходы состояний работают корректно
- [ ] POST /api/changes/{id}/submit_for_approval/ endpoint реализован
- [ ] POST /api/changes/{id}/approve/ endpoint реализован
- [ ] POST /api/changes/{id}/reject/ endpoint реализован
- [ ] POST /api/changes/{id}/deploy/ endpoint реализован
- [ ] POST /api/changes/{id}/rollback/ endpoint реализован
- [ ] Валидация переходов работает (HTTP 400 при недопустимом переходе)
- [ ] Валидация минимум 1 скоркарты при submit_for_approval работает
- [ ] Автоматический расчет критичности работает
- [ ] Обновление статуса Initiative при deployed Deployment работает
- [ ] Rollback создает новую запись Deployment корректно
- [ ] Только одно активное внедрение (rollback_at = null) обеспечивается
- [ ] Unit тесты покрывают все сценарии (coverage > 80%)
- [ ] Integration тесты для всех переходов
- [ ] API документация обновлена

### Dependencies
Нет

### Technical Notes

**Пример использования State Machine:**
```python
from django.db import transaction

@transaction.atomic
def submit_change_for_approval(change_id, user):
    change = Change.objects.get(id=change_id)

    # Валидация перехода
    validate_transition(change, 'requires_approval')

    # Обновление статуса
    change.status = 'requires_approval'
    change.save()

    # Создание записи в approval_workflow
    ApprovalWorkflow.objects.create(
        entity_type='change',
        entity_id=change.id,
        status='pending',
        submitted_by=user
    )

    return change
```

---

## Итоговая зависимость задач

```
BE-CL1 (5 дней)
```

**Общая длительность (критический путь):** 5 дней

---

## ✅ Ключевые особенности

1. **State Machine** - строгая валидация переходов состояний
2. **Автоматический расчет критичности** - MAX критичности всех скоркарт
3. **Обновление статуса Initiative** - автоматическое при deployed Deployment
4. **Rollback** - создание новой записи Deployment при откате
5. **Только одно активное внедрение** - rollback_at = null
6. **Валидация минимум 1 скоркарты** - при отправке на согласование
7. **Integration с approval_workflow** - создание записи при submit_for_approval

---
