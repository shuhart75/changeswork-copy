# Задачи для жизненного цикла Пилота (Pilot Lifecycle)

## Обзор

**Компонент:** Жизненный цикл Пилота (Pilot Lifecycle)
**Статус:** Новая разработка

### Что реализуется:

**Состояния версии Пилота (PilotVersion):**
- draft - черновик версии
- requires_activation - версия отправлена на согласование/утверждение
- active - текущая активная версия (используется в системе)
- inactive - неактивная версия (замещена более новой, хранится для истории)
- approval_rejected - версия отклонена на согласовании (можно редактировать и переотправить)
- ratification_rejected - версия отклонена на утверждении (можно редактировать и переотправить)
- completed - версия завершена (ручное завершение пилота)
- archived - версия в архиве (история)

**Правило версионирования (MVP):**
- Изменения пилота делаются через **новую версию**.
- Пока новая версия не согласована/утверждена и не опубликована, **предыдущая active-версия остаётся активной**.

**Переходы (для версии):**
- draft → requires_activation (отправка версии на согласование)
- requires_activation → active (версия согласована/утверждена и опубликована как текущая)
- active → inactive (замещение новой версией, старая версия остаётся в истории)
- requires_activation → approval_rejected|ratification_rejected (отклонение версии)
- approval_rejected|ratification_rejected → requires_activation (повторная отправка версии после исправлений)
- active → completed (завершение пилота)
- completed → archived (архивирование)

**Бизнес-правила:**
- Пилот должен быть связан минимум с 1 скоркартой
- Только ПРМ (свой продукт) или Админ могут управлять переходами
- При отклонении сохраняется причина (rejection_reason)
- Статус `requires_correction` в MVP не используем: изменения в пилоте вносятся вручную, затем пилот отправляется на новый круг согласования/утверждения.

---

## BE-PL1: Backend для жизненного цикла Пилота

**Тип:** Story
**Приоритет:** Критический
**Оценка:** 3 дня

### Summary
Реализация жизненного цикла Пилота с переходами между состояниями

### Description

Реализовать жизненный цикл Пилота:

1. **Модель данных Pilot + PilotVersion (обновление):**

   ```python
   class Pilot(models.Model):
       """Пилот"""
       id = models.UUIDField(primary_key=True, default=uuid.uuid4)
       display_id = models.CharField(max_length=50, unique=True)
       name = models.CharField(max_length=255)

       # Связи
       deployment = models.ForeignKey(Deployment, on_delete=models.CASCADE)
       scorecards = models.ManyToManyField(Scorecard, related_name='pilots')

       # Текущая версия (версионирование)
       current_version = models.ForeignKey(
           'PilotVersion',
           on_delete=models.SET_NULL,
           null=True,
           blank=True,
           related_name='+',
       )

       # Автор
       created_by = models.ForeignKey(User, on_delete=models.PROTECT)

       created_at = models.DateTimeField(auto_now_add=True)

       class Meta:
           db_table = 'pilot'

   class PilotVersion(models.Model):
       """Версия пилота (все статусы согласования живут здесь)"""
       id = models.UUIDField(primary_key=True, default=uuid.uuid4)
       pilot = models.ForeignKey(Pilot, on_delete=models.CASCADE, related_name='versions')

       version_number = models.IntegerField()
       status = models.CharField(
           max_length=50,
           choices=[
               ('draft', 'Черновик'),
               ('requires_activation', 'Требует активации'),
               ('active', 'Активная (current)'),
               ('inactive', 'Неактивная (замещена)'),
               ('approval_rejected', 'Отклонена на согласовании'),
               ('ratification_rejected', 'Отклонена на утверждении'),
               ('completed', 'Завершена'),
               ('archived', 'Архив'),
           ],
           default='draft',
       )

       activated_at = models.DateTimeField(null=True, blank=True)
       completed_at = models.DateTimeField(null=True, blank=True)
       rejection_reason = models.TextField(null=True, blank=True)

       created_by = models.ForeignKey(User, on_delete=models.PROTECT)
       created_at = models.DateTimeField(auto_now_add=True)

       class Meta:
           db_table = 'pilot_version'
   ```

2. **API Endpoint: POST /api/pilot-versions/{id}/submit_for_approval/**

   **Параметры запроса:**
   Пример 1 (есть ratification, auto_ratification=true: ratifier выбирается при submit):

   ```json
   {
     "approval_stages": [
       { "approvers": ["user-uuid-1", "user-uuid-2"] }
     ],
     "ratification_required": true,
     "ratifier_id": "user-uuid-3",
     "auto_ratification": true
   }
   ```

   Пример 2 (есть ratification, auto_ratification=false: ratifier выбирается при запуске ratification из очереди `awaiting_ratification`):

   ```json
   {
     "approval_stages": [
       { "approvers": ["user-uuid-1", "user-uuid-2"] }
     ],
     "ratification_required": true,
     "auto_ratification": false
   }
   ```

   **Бизнес-логика:**
   - Валидация: версия в статусе 'draft' или 'approval_rejected' или 'ratification_rejected'
   - Валидация: минимум 1 скоркарта связана
   - Валидация: пользователь имеет право (ПРМ своего продукта, Админ)
   - Вызов `BE-AP1` (создание `ApprovalInstance(target_type='pilot_version')`)
   - Перевод статуса: `draft|approval_rejected|ratification_rejected -> requires_activation`

3. **API Endpoint: POST /api/pilot-versions/{id}/complete/**

   **Бизнес-логика:**
   - Валидация: статус = 'active' (current версия)
   - Валидация: пользователь имеет право (ПРМ своего продукта, Админ)
   - Обновление статуса → 'completed'
   - Установка completed_at = now()

4. **Интеграция с процессом согласования (версионирование):**

   **При успешном согласовании (через BE-INT1):**
   - Новая версия становится `active` и публикуется как current_version у Pilot
   - Предыдущая current-версия переводится в `inactive`
   - Установка activated_at для новой версии
   - Очистка rejection_reason для новой версии

   **При отклонении (через BE-INT1):**
   - Версия получает статус `approval_rejected` или `ratification_rejected`
   - Сохранение rejection_reason
   - Отправка уведомления автору

5. **Бизнес-правила:**

   **БП-1: Переход draft → requires_activation**
   - Пилот должен быть связан минимум с 1 скоркартой
   - Только ПРМ (свой продукт) или Админ

   **БП-2: Переход requires_activation → active**
   - Автоматически после успешного согласования
   - Установка activated_at

   **БП-3: Переход requires_activation → approval_rejected|ratification_rejected**
   - Автоматически при отклонении на этапе Approval/Ratification
   - Сохранение rejection_reason

   **БП-4: Переход approval_rejected|ratification_rejected → requires_activation**
   - Повторная отправка на согласование после правок
   - Только ПРМ (свой продукт) или Админ

   **БП-5: Переход active → completed**
   - Завершение пилота (успешное окончание)
   - Только ПРМ (свой продукт) или Админ
   - Установка completed_at

   **БП-6: Архивирование**
   - completed → archived (ручное действие пользователя)

6. **Права доступа:**
   - Отправить на согласование версию может: ПРМ (свой продукт), Админ
   - Завершить может: ПРМ (свой продукт), Админ

### Acceptance Criteria

- [ ] Модель Pilot + PilotVersion обновлены (версионирование, статусы, даты)
- [ ] Миграции применены
- [ ] POST /api/pilot-versions/{id}/submit_for_approval/ реализован
- [ ] POST /api/pilot-versions/{id}/complete/ реализован
- [ ] Интеграция с процессом согласования работает
- [ ] Автоматическое обновление статусов работает
- [ ] Сохранение rejection_reason работает
- [ ] Права доступа реализованы
- [ ] Unit тесты покрывают все сценарии (coverage > 80%)
- [ ] Integration тесты для всех переходов
- [ ] API документация обновлена

### Dependencies
- BE-AP1 (требуется процесс согласования)
- BE-INT1 (требуется интеграция ЖЦ)

---

## Итоговая зависимость задач

```
BE-AP1 (8 дней)
  ↓
BE-INT1 (3 дня)
  ↓
BE-PL1 (3 дня)
```

**Общая длительность (критический путь):** 14 дней

---

## ✅ Ключевые особенности

1. **Жизненный цикл Пилота** - 5 состояний
2. **Интеграция с процессом согласования** - автоматические переходы
3. **Сохранение причины отклонения** - rejection_reason
4. **Валидация минимум 1 скоркарты** - перед отправкой на согласование
5. **Права доступа** - ПРМ (свой продукт), Админ
6. **Даты переходов** - activated_at, completed_at

---
