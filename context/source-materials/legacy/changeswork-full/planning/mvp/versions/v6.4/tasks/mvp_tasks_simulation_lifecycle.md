# Задачи для жизненного цикла Симуляции (Simulation Lifecycle)

## Обзор

**Компонент:** Жизненный цикл Симуляции (Simulation Lifecycle)
**Статус:** Адаптация существующего функционала

### Что реализуется:

**Состояния Симуляции:**
- draft - черновик
- running - выполняется
- completed - завершена успешно
- failed - завершена с ошибкой

**Переходы:**
- draft → running (запуск симуляции)
- running → completed (успешное завершение)
- running → failed (завершение с ошибкой)

**Бизнес-правила:**
- Только ПРМ (свой продукт) или Админ могут управлять переходами
- Симуляция НЕ участвует в процессе согласования (независимый ЖЦ)
- При завершении сохраняется результат или ошибка

---

## BE-SL1: Backend для жизненного цикла Симуляции

**Тип:** Story
**Приоритет:** Средний
**Оценка:** 2 дня

### Summary
Адаптация жизненного цикла Симуляции с переходами между состояниями

### Description

Адаптировать жизненный цикл Симуляции:

1. **Модель данных Simulation (обновление):**

   ```python
   class Simulation(models.Model):
       """Симуляция"""
       id = models.UUIDField(primary_key=True, default=uuid.uuid4)
       display_id = models.CharField(max_length=50, unique=True)
       name = models.CharField(max_length=255)

       # Связи
       deployment = models.ForeignKey(Deployment, on_delete=models.CASCADE)

       # Статус
       status = models.CharField(
           max_length=50,
           choices=[
               ('draft', 'Черновик'),
               ('running', 'Выполняется'),
               ('completed', 'Завершена'),
               ('failed', 'Ошибка')
           ],
           default='draft'
       )

       # Даты
       created_at = models.DateTimeField(auto_now_add=True)
       started_at = models.DateTimeField(null=True, blank=True)
       completed_at = models.DateTimeField(null=True, blank=True)

       # Результат/ошибка
       result = models.JSONField(null=True, blank=True)
       error_message = models.TextField(null=True, blank=True)

       # Автор
       created_by = models.ForeignKey(User, on_delete=models.PROTECT)

       class Meta:
           db_table = 'simulation'
   ```

2. **API Endpoint: POST /api/simulations/{id}/start/**

   **Бизнес-логика:**
   - Валидация: статус = 'draft'
   - Валидация: пользователь имеет право (ПРМ своего продукта, Админ)
   - Обновление статуса → 'running'
   - Установка started_at = now()
   - Запуск фоновой задачи выполнения симуляции

3. **API Endpoint: POST /api/simulations/{id}/complete/**

   **Параметры запроса:**
   ```json
   {
     "result": {
       "metrics": {...},
       "summary": "..."
     }
   }
   ```

   **Бизнес-логика:**
   - Валидация: статус = 'running'
   - Валидация: пользователь имеет право (ПРМ своего продукта, Админ)
   - Обновление статуса → 'completed'
   - Установка completed_at = now()
   - Сохранение result

4. **API Endpoint: POST /api/simulations/{id}/fail/**

   **Параметры запроса:**
   ```json
   {
     "error_message": "Ошибка при выполнении симуляции: ..."
   }
   ```

   **Бизнес-логика:**
   - Валидация: статус = 'running'
   - Валидация: пользователь имеет право (ПРМ своего продукта, Админ)
   - Обновление статуса → 'failed'
   - Установка completed_at = now()
   - Сохранение error_message

5. **Бизнес-правила:**

   **БП-1: Переход draft → running**
   - Запуск симуляции
   - Только ПРМ (свой продукт) или Админ
   - Установка started_at

   **БП-2: Переход running → completed**
   - Успешное завершение
   - Только ПРМ (свой продукт) или Админ
   - Сохранение result
   - Установка completed_at

   **БП-3: Переход running → failed**
   - Завершение с ошибкой
   - Только ПРМ (свой продукт) или Админ
   - Сохранение error_message
   - Установка completed_at

   **БП-4: Симуляция НЕ участвует в процессе согласования**
   - Независимый жизненный цикл
   - Нет интеграции с Approval/Ratification

6. **Права доступа:**
   - Запустить может: ПРМ (свой продукт), Админ
   - Завершить может: ПРМ (свой продукт), Админ
   - Отметить как failed может: ПРМ (свой продукт), Админ

### Acceptance Criteria

- [ ] Модель Simulation обновлена (статусы, даты, result, error_message)
- [ ] Миграции применены
- [ ] POST /api/simulations/{id}/start/ реализован
- [ ] POST /api/simulations/{id}/complete/ реализован
- [ ] POST /api/simulations/{id}/fail/ реализован
- [ ] Валидация переходов работает
- [ ] Сохранение result/error_message работает
- [ ] Права доступа реализованы
- [ ] Unit тесты покрывают все сценарии (coverage > 80%)
- [ ] Integration тесты для всех переходов
- [ ] API документация обновлена

### Dependencies
Нет (независимый жизненный цикл)

---

## Итоговая зависимость задач

**Общая длительность:** 2 дня

**Независимая задача** - не зависит от процесса согласования

---

## ✅ Ключевые особенности

1. **Адаптация существующего функционала** - минимальные изменения
2. **Жизненный цикл Симуляции** - 4 состояния
3. **Независимый ЖЦ** - НЕ участвует в процессе согласования
4. **Сохранение результата** - result (JSON) при успехе
5. **Сохранение ошибки** - error_message при failed
6. **Права доступа** - ПРМ (свой продукт), Админ
7. **Даты переходов** - started_at, completed_at

---
