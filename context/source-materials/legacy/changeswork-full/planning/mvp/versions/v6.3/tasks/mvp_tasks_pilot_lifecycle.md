# Задачи для жизненного цикла Пилота (Pilot Lifecycle)

## Обзор

**Компонент:** Жизненный цикл Пилота (Pilot Lifecycle)
**Статус:** Новая разработка

### Что реализуется:

**Состояния Пилота:**
- draft - черновик
- requires_activation - требует активации (отправлен на согласование)
- active - активен (согласован и запущен)
- requires_correction - требует корректировки (отклонен)
- completed - завершен

**Переходы:**
- draft → requires_activation (отправка на согласование)
- requires_activation → active (согласование успешно)
- requires_activation → requires_correction (отклонение)
- requires_correction → requires_activation (повторная отправка после исправлений)
- active → completed (завершение пилота)

**Бизнес-правила:**
- Пилот должен быть связан минимум с 1 скоркартой
- Только ПРМ (свой продукт) или Админ могут управлять переходами
- При отклонении сохраняется причина (rejection_reason)

---

## BE-PL1: Backend для жизненного цикла Пилота

**Тип:** Story
**Приоритет:** Критический
**Оценка:** 3 дня

### Summary
Реализация жизненного цикла Пилота с переходами между состояниями

### Description

Реализовать жизненный цикл Пилота:

1. **Модель данных Pilot (обновление):**

   ```python
   class Pilot(models.Model):
       """Пилот"""
       id = models.UUIDField(primary_key=True, default=uuid.uuid4)
       display_id = models.CharField(max_length=50, unique=True)
       name = models.CharField(max_length=255)

       # Связи
       deployment = models.ForeignKey(Deployment, on_delete=models.CASCADE)
       scorecards = models.ManyToManyField(Scorecard, related_name='pilots')

       # Статус
       status = models.CharField(
           max_length=50,
           choices=[
               ('draft', 'Черновик'),
               ('requires_activation', 'Требует активации'),
               ('active', 'Активен'),
               ('requires_correction', 'Требует корректировки'),
               ('completed', 'Завершен')
           ],
           default='draft'
       )

       # Даты
       created_at = models.DateTimeField(auto_now_add=True)
       activated_at = models.DateTimeField(null=True, blank=True)
       completed_at = models.DateTimeField(null=True, blank=True)

       # Отклонение
       rejection_reason = models.TextField(null=True, blank=True)

       # Автор
       created_by = models.ForeignKey(User, on_delete=models.PROTECT)

       class Meta:
           db_table = 'pilot'
   ```

2. **API Endpoint: POST /api/pilots/{id}/submit_for_approval/**

   **Параметры запроса:**
   ```json
   {
     "approval_stages": [
       { "approvers": ["user-uuid-1", "user-uuid-2"] }
     ],
     "ratifier_id": "user-uuid-3",
     "auto_ratification": false
   }
   ```

   **Бизнес-логика:**
   - Валидация: статус = 'draft' или 'requires_correction'
   - Валидация: минимум 1 скоркарта связана
   - Валидация: пользователь имеет право (ПРМ своего продукта, Админ)
   - Вызов `BE-AP1` (создание `ApprovalInstance(target_type='pilot')`)
   - Перевод статуса: `draft -> requires_activation` (или остаётся `requires_correction` при переотправке)

3. **API Endpoint: POST /api/pilots/{id}/complete/**

   **Бизнес-логика:**
   - Валидация: статус = 'active'
   - Валидация: пользователь имеет право (ПРМ своего продукта, Админ)
   - Обновление статуса → 'completed'
   - Установка completed_at = now()

4. **Интеграция с процессом согласования:**

   **При успешном согласовании (через BE-INT1):**
   - Обновление статуса → 'active'
   - Установка activated_at = now()
   - Очистка rejection_reason

   **При отклонении (через BE-INT1):**
   - Обновление статуса → 'requires_correction'
   - Сохранение rejection_reason
   - Отправка уведомления автору

5. **Бизнес-правила:**

   **БП-1: Переход draft → requires_activation**
   - Пилот должен быть связан минимум с 1 скоркартой
   - Только ПРМ (свой продукт) или Админ

   **БП-2: Переход requires_activation → active**
   - Автоматически после успешного согласования
   - Установка activated_at

   **БП-3: Переход requires_activation → requires_correction**
   - Автоматически при отклонении
   - Сохранение rejection_reason

   **БП-4: Переход requires_correction → requires_activation**
   - Повторная отправка на согласование
   - Только ПРМ (свой продукт) или Админ

   **БП-5: Переход active → completed**
   - Завершение пилота
   - Только ПРМ (свой продукт) или Админ
   - Установка completed_at

6. **Права доступа:**
   - Отправить на согласование может: ПРМ (свой продукт), Админ
   - Завершить может: ПРМ (свой продукт), Админ

### Acceptance Criteria

- [ ] Модель Pilot обновлена (статусы, даты)
- [ ] Миграции применены
- [ ] POST /api/pilots/{id}/submit_for_approval/ реализован
- [ ] POST /api/pilots/{id}/complete/ реализован
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
