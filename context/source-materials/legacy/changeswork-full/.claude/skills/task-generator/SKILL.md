---
name: task-generator
description: Генерация задач разработки из спецификации с оценкой времени
version: 1.0
---

# Task Generator - Генерация задач разработки

Инструмент для автоматической генерации задач разработки на основе спецификации с оценкой времени.

## Возможности

1. **Генерация backend задач** - модели, сериализаторы, viewsets, права доступа, state machines, тесты
2. **Генерация frontend задач** - списки, детальные просмотры, формы
3. **Генерация инфраструктурных задач** - настройка Django, React, PostgreSQL, CI/CD, Docker
4. **Оценка времени** - автоматический расчёт времени разработки
5. **Экспорт в JSON/Markdown** - сохранение задач в удобном формате

## Использование

### Быстрая оценка времени

```bash
python3 scripts/task_generator.py estimate
```

Результат:
```
=== Оценка времени разработки ===

Всего задач: 48
  - Инфраструктура: 6
  - Backend: 36
  - Frontend: 18

infrastructure: 23 часов
backend: 84 часов
frontend: 84 часов

Итого: 191 часов
       4.8 недель
       2.4 спринтов
```

### Генерация задач в JSON

```bash
python3 scripts/task_generator.py generate json
```

Что происходит:
1. Генерируются задачи для всех сущностей (Initiative, Simulation, Pilot, Deployment, Scorecard, Package)
2. Рассчитываются оценки времени
3. Создаётся файл `planning/generated_tasks.json`

Формат JSON:
```json
{
  "generated_at": "2026-03-11T12:00:00",
  "tasks": [
    {
      "id": "backend-initiative-model",
      "title": "Создать Django модель Initiative",
      "description": "Реализовать модель Initiative согласно data_model.puml",
      "type": "backend",
      "entity": "Initiative",
      "estimate_hours": 2,
      "dependencies": []
    }
  ],
  "estimates": {
    "by_type": {
      "infrastructure": 23,
      "backend": 84,
      "frontend": 84
    },
    "total_hours": 191,
    "total_weeks": 4.8,
    "total_sprints": 2.4
  }
}
```

### Генерация задач в Markdown

```bash
python3 scripts/task_generator.py generate markdown
```

Создаёт файл `planning/generated_tasks.md` с читаемым форматом:

```markdown
# Задачи разработки

## Инфраструктура

### Настроить Django проект
**ID:** `infra-setup-django`
**Описание:** Создать Django проект с базовой конфигурацией
**Оценка:** 4 часов

## Backend

### Initiative
- **Создать Django модель Initiative** (2ч)
  - Реализовать модель Initiative согласно data_model.puml
- **Создать сериализатор для Initiative** (1ч)
  - Реализовать DRF сериализатор для Initiative
...
```

## Структура задач

### Backend задачи (для каждой сущности)

1. **Модель** (2ч) - Django модель согласно data_model.puml
2. **Сериализатор** (1ч) - DRF сериализатор
3. **ViewSet** (2ч) - CRUD операции
4. **Права доступа** (2ч) - Ролевая модель
5. **State machine** (3ч) - Переходы состояний (если применимо)
6. **Тесты** (4ч) - Unit и integration тесты

**Итого на сущность:** 14-17 часов

### Frontend задачи (для каждой сущности)

1. **Список** (4ч) - Таблица с фильтрацией и сортировкой
2. **Детальный просмотр** (4ч) - Страница с полной информацией
3. **Форма** (6ч) - Создание и редактирование

**Итого на сущность:** 14 часов

### Инфраструктурные задачи

1. **Django проект** (4ч) - Базовая настройка
2. **Django REST Framework** (3ч) - DRF, аутентификация, CORS
3. **PostgreSQL** (2ч) - Настройка БД
4. **React проект** (4ч) - React + TypeScript + Material-UI
5. **CI/CD** (6ч) - GitHub Actions
6. **Docker** (4ч) - Dockerfile и docker-compose

**Итого:** 23 часа

## Оценки времени

### По умолчанию

```python
estimates = {
    "model": 2,           # Django модель
    "serializer": 1,      # DRF сериализатор
    "viewset": 2,         # DRF viewset
    "permissions": 2,     # Права доступа
    "tests": 4,           # Тесты
    "frontend_list": 4,   # Список (таблица)
    "frontend_detail": 4, # Детальный просмотр
    "frontend_form": 6,   # Форма создания/редактирования
    "state_machine": 3,   # State machine логика
}
```

### Общая оценка

Для 6 сущностей (Initiative, Simulation, Pilot, Deployment, Scorecard, Package):

- **Backend:** 84 часа (14ч × 6 сущностей)
- **Frontend:** 84 часа (14ч × 6 сущностей)
- **Инфраструктура:** 23 часа
- **Итого:** 191 час ≈ 5 недель ≈ 2.5 спринта

## Примеры использования

### Пример 1: Планирование спринта

```bash
# Генерируем задачи
python3 scripts/task_generator.py generate json

# Импортируем в Jira/Linear/GitHub Projects
# Используем planning/generated_tasks.json
```

### Пример 2: Оценка проекта

```bash
# Быстрая оценка для презентации
python3 scripts/task_generator.py estimate

# Результат: 191 час ≈ 5 недель
```

### Пример 3: Документация для команды

```bash
# Генерируем читаемый Markdown
python3 scripts/task_generator.py generate markdown

# Отправляем planning/generated_tasks.md команде
```

## Зависимости задач

Задачи имеют зависимости для правильной последовательности:

```
Backend:
  model → serializer → viewset → permissions
  model → state_machine
  viewset + permissions → tests

Frontend:
  list → detail → form

Infrastructure:
  django → drf
  django → postgres
  django + postgres → docker
  django + react → ci/cd
```

## Интеграция с другими skills

### С version-manager

```bash
# Создаём версию перед началом разработки
python3 scripts/version_manager.py create v3.2 "Начало разработки MVP"

# Генерируем задачи
python3 scripts/task_generator.py generate json

# Коммитим
git add planning/generated_tasks.json
git commit -m "Сгенерированы задачи разработки для v3.2"
```

### С spec-sync

```bash
# Проверяем синхронизацию спецификации
python3 .claude/skills/spec-sync/check_sync.py

# Если всё ОК - генерируем задачи
python3 scripts/task_generator.py generate markdown
```

### С diagram-updater

```bash
# Проверяем диаграммы
python3 scripts/diagram_updater.py check-all

# Генерируем задачи
python3 scripts/task_generator.py estimate
```

## Кастомизация оценок

Если нужно изменить оценки времени, отредактируйте `scripts/task_generator.py`:

```python
self.estimates = {
    "model": 3,           # Было 2, стало 3
    "serializer": 1,
    "viewset": 3,         # Было 2, стало 3
    # ...
}
```

Затем перегенерируйте задачи:

```bash
python3 scripts/task_generator.py generate json
```

## Добавление новых сущностей

Если добавили новую сущность в спецификацию:

1. Обновите список в `task_generator.py`:
```python
self.entities = [
    "Initiative", "Simulation", "Pilot", "Deployment",
    "Scorecard", "Package", "NewEntity"  # Добавили
]
```

2. Перегенерируйте задачи:
```bash
python3 scripts/task_generator.py generate json
```

## Формат вывода

### JSON структура

```json
{
  "generated_at": "ISO timestamp",
  "tasks": [
    {
      "id": "unique-task-id",
      "title": "Task title",
      "description": "Task description",
      "type": "backend|frontend|infrastructure",
      "entity": "EntityName or null",
      "estimate_hours": 4,
      "dependencies": ["task-id-1", "task-id-2"]
    }
  ],
  "estimates": {
    "by_type": {
      "backend": 84,
      "frontend": 84,
      "infrastructure": 23
    },
    "total_hours": 191,
    "total_weeks": 4.8,
    "total_sprints": 2.4
  }
}
```

### Markdown структура

```markdown
# Задачи разработки

## Инфраструктура
### Task title
**ID:** `task-id`
**Описание:** Description
**Оценка:** X часов
**Зависимости:** dep1, dep2

## Backend
### EntityName
- **Task title** (Xч)
  - Description

## Frontend
### EntityName
- **Task title** (Xч)
  - Description

## Оценка времени
- **backend:** X часов
- **frontend:** X часов
- **infrastructure:** X часов

**Итого:** X часов (Y недель, Z спринтов)
```

## Best Practices

1. **Генерируйте задачи после стабилизации спецификации**
   ```bash
   python3 scripts/task_generator.py generate json
   ```

2. **Используйте estimate для быстрой оценки**
   ```bash
   python3 scripts/task_generator.py estimate
   ```

3. **Обновляйте оценки на основе реального опыта**
   - После первого спринта скорректируйте estimates в коде
   - Перегенерируйте задачи

4. **Версионируйте сгенерированные задачи**
   ```bash
   git add planning/generated_tasks.json
   git commit -m "Обновлены задачи разработки"
   ```

5. **Используйте JSON для импорта в task trackers**
   - Jira: импорт через API
   - Linear: импорт через CSV (конвертируйте JSON)
   - GitHub Projects: импорт через API

## Ограничения

1. **Оценки приблизительные** - реальное время может отличаться
2. **Не учитывает сложность бизнес-логики** - только базовый CRUD
3. **Не включает задачи интеграции** - только отдельные компоненты
4. **Не учитывает code review и QA** - только разработка

## Troubleshooting

**Проблема:** Оценки слишком оптимистичные

**Решение:** Увеличьте estimates в коде на 20-30%

**Проблема:** Нужны дополнительные типы задач

**Решение:** Добавьте новые задачи в методы generate_*_tasks()

**Проблема:** Нужна другая структура зависимостей

**Решение:** Измените dependencies в генерируемых задачах

## Changelog

### v1.0 (2026-03-11)
- Первая версия
- Генерация backend, frontend, infrastructure задач
- Оценка времени разработки
- Экспорт в JSON и Markdown
- Поддержка зависимостей задач
