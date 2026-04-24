# Задачи для жизненного цикла Внедрения (Deployment Lifecycle)

## Обзор

**Компонент:** Жизненный цикл версии Deployment (DeploymentVersion State Machine)
**Статус:** Новая разработка

### Что реализуется:

> Правило версионирования (MVP): изменения внедрения делаются через **новую версию**. Предыдущая deployed-версия остаётся deployed до развертывания новой версии.

**Диаграмма состояний DeploymentVersion:**
```
draft → requires_approval → approved → deployed → rolled_back
           ↓                 ↑
      approval_rejected      |
           ↓                 |
    (edit + resubmit)        |
           ↓                 |
    requires_approval        |
           ↓                 |
     ratification_rejected --+
```

**Переходы:**
- draft → requires_approval: отправка на согласование
- requires_approval → approved: успешное согласование и (если включено) утверждение
- requires_approval → approval_rejected: отклонение на этапе согласования (Approval)
- requires_approval → ratification_rejected: отклонение на этапе утверждения (Ratification)
- approval_rejected → requires_approval: повторная отправка на согласование (после правок)
- ratification_rejected → requires_approval: повторная отправка на согласование (после правок)
- approved → deployed: внедрение в продакшн
- deployed → rolled_back: откат изменения

**Бизнес-правила:**
- DeploymentVersion должно быть связано минимум с одной Скоркартой
- Только одно активное развертывание для Deployment (rollback_at = null) среди версий
- При rollback создается новая запись с rollback_at
- Критичность рассчитывается автоматически: MAX(criticality) всех скоркарт

---

## BE-CL1: Backend для жизненного цикла Внедрения

**Тип:** Story
**Приоритет:** Критический
**Оценка:** 5 дней

### Summary
Реализация state machine для жизненного цикла Deployment с валидацией переходов и автоматическим расчетом критичности

### Description

Реализовать Backend логику для управления жизненным циклом Deployment:

1. **State Machine для Deployment:**

**Состояния:**
- draft - черновик
- requires_approval - отправлено на согласование
- approved - процесс согласования завершён успешно (и, если был Ratification, он также завершён успешно)
- approval_rejected - отклонено на согласовании (можно редактировать и переотправить)
- ratification_rejected - отклонено на утверждении (можно редактировать и переотправить)
- deployed - внедрено в продакшн
- rolled_back - откачено

   **Переходы:**
   ```python
   TRANSITIONS = {
       'draft': ['requires_approval'],
       'requires_approval': ['approved', 'approval_rejected', 'ratification_rejected'],
       'approval_rejected': ['requires_approval'],
       'ratification_rejected': ['requires_approval'],
       'approved': ['deployed'],
       'deployed': ['rolled_back'],
       'rolled_back': []  # финальное состояние
   }
   ```

2. **API Endpoints:**

**POST /api/deployment-versions/{id}/submit_for_approval/**
- Переход: draft → requires_approval
   - Валидация: минимум 1 скоркарта связана
   - Создание `ApprovalInstance(target_type='deployment_version')` (см. `BE-AP1`)
   - Возврат: 200 OK или 400 Bad Request
- Примечание: approve/reject выполняются через endpoints `ApprovalInstance` (см. `BE-AP1`), а смена статуса Deployment синхронизируется в `BE-INT1`.
  - Важное правило MVP: reject не возвращает Deployment в `draft`. После reject Deployment попадает в `approval_rejected` или `ratification_rejected` (в зависимости от этапа), где доступно редактирование и повторная отправка.

   **POST /api/deployments/{id}/deploy/**
   - Переход: approved → deployed
   - Установка deployed_at = now()
   - Автоматическое обновление статуса Deployment → deployed
   - Возврат: 200 OK или 400 Bad Request

   **POST /api/deployments/{id}/rollback/**
   - Переход: deployed → rolled_back
   - Параметры: reason (обязательный)
   - Установка rollback_at = now()
   - Создание новой записи Deployment (копия с новым ID)
   - Возврат: 200 OK или 400 Bad Request

3. **Бизнес-правила:**

   **БП-1: Валидация перехода draft → requires_approval**
   - Deployment должно быть связано минимум с 1 скоркартой
   - Все обязательные поля заполнены
   - HTTP 400 если валидация не прошла

   **БП-2: Автоматический расчет критичности**
   - При создании/обновлении Deployment
   - Критичность = MAX(criticality) всех связанных скоркарт
   - Если нет скоркарт → criticality = 'low'

   **БП-3: Rollback**
   - Только для deployed Deployment
   - Установка rollback_at = now()
   - Создание новой записи Deployment (копия) со статусом draft
   - Сохранение ссылки на "предыдущее развертывание" (если модель это поддерживает)

   **БП-5: Только одно активное внедрение**
   - rollback_at = null означает активное внедрение
   - При rollback старая запись получает rollback_at, новая создается с rollback_at = null

   **БП-6: Recall (отзыв) из согласования/утверждения**
   - Recall обязателен в MVP (см. `BE-AP1`)
   - Отзыв переводит `ApprovalInstance.status='cancelled'` и возвращает Deployment в `pre_submit_status` (как правило, `draft`)
   - История решений и комментариев сохраняется

4. **Валидация переходов:**
   ```python
   def validate_transition(deployment, new_status):
       """Валидация перехода состояния"""
       allowed = TRANSITIONS.get(deployment.status, [])
       if new_status not in allowed:
           raise ValidationError(
               f"Переход {deployment.status} → {new_status} недопустим"
           )

       # Дополнительные проверки
       if new_status == 'requires_approval':
           if not deployment.scorecards.exists():
               raise ValidationError(
                   "Deployment должно быть связано минимум с 1 скоркартой"
               )
   ```

5. **Автоматический расчет критичности:**
   ```python
   def calculate_criticality(deployment):
       """Рассчитать критичность как MAX критичности всех скоркарт"""
       scorecards = deployment.scorecards.all()
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

6. **Rollback логика:**
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
- [ ] POST /api/deployment-versions/{id}/submit_for_approval/ endpoint реализован
- [ ] POST /api/deployments/{id}/deploy/ endpoint реализован
- [ ] POST /api/deployments/{id}/rollback/ endpoint реализован
- [ ] Валидация переходов работает (HTTP 400 при недопустимом переходе)
- [ ] Валидация минимум 1 скоркарты при submit_for_approval работает
- [ ] Автоматический расчет критичности работает
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
def submit_deployment_for_approval(deployment_id, user):
    deployment = Deployment.objects.get(id=deployment_id)

    # Валидация перехода
    validate_transition(deployment, 'requires_approval')

    # Обновление статуса
    deployment.status = 'requires_approval'
    deployment.save()

    # Создание ApprovalInstance (см. BE-AP1)
    create_approval_instance(
        target_type='deployment',
        target_id=deployment.id,
        submitted_by=user,
        approval_stages=[...],
        ratifier_id=None,
        auto_ratification=False,
    )

    return deployment
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
3. **Rollback** - создание новой записи Deployment при откате
4. **Только одно активное внедрение** - rollback_at = null
5. **Валидация минимум 1 скоркарты** - при отправке на согласование
6. **Integration с ApprovalInstance** - создание процесса согласования при submit_for_approval

---
