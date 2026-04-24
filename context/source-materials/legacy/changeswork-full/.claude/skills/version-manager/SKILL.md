---
name: version-manager
description: Управление версиями спецификации - создание, сравнение, восстановление версий
version: 1.0
---

# Version Manager - Управление версиями спецификации

Инструмент для управления версиями файлов спецификации.

## Возможности

1. **Создание версий** - сохранение текущего состояния спецификации
2. **Список версий** - просмотр всех сохранённых версий
3. **Сравнение версий** - сравнение двух версий
4. **Восстановление версий** - откат к предыдущей версии

## Использование

### Создание новой версии

```bash
# Создать версию с именем
python3 scripts/version_manager.py create v3.2

# Создать версию с описанием
python3 scripts/version_manager.py create v3.2 "Добавлена поддержка rollback"
```

Что происходит:
- Создаётся папка `spec/versions/v3.2/`
- Копируются текущие файлы из `spec/`:
  - domain_model.md
  - data_model.puml
  - state_machine.puml
  - GUIDE.md
- Создаётся файл метаданных `version.json`

### Просмотр всех версий

```bash
python3 scripts/version_manager.py list
```

Результат:
```
=== Доступные версии ===

📦 v3.0
   Создана: 2026-03-01 10:00
   Файлов: 4

📦 v3.1
   Создана: 2026-03-10 15:30
   Описание: Переименование Change → Deployment
   Файлов: 4

📦 v3.2
   Создана: 2026-03-11 12:00
   Описание: Добавлена поддержка rollback
   Файлов: 4
```

### Сравнение версий

```bash
python3 scripts/version_manager.py compare v3.0 v3.1
```

Результат:
```
=== Сравнение версий v3.0 и v3.1 ===

✓ domain_model.md: без изменений (80504 байт)
📝 data_model.puml: изменён (+1234 байт)
📝 state_machine.puml: изменён (+567 байт)

Для детального сравнения используйте:
  diff spec/versions/v3.0/domain_model.md spec/versions/v3.1/domain_model.md
```

### Восстановление версии

```bash
python3 scripts/version_manager.py restore v3.1
```

Что происходит:
1. Создаётся автоматическая резервная копия текущей версии
2. Файлы из `spec/versions/v3.1/` копируются в `spec/`
3. Текущая версия заменяется на v3.1

**ВАЖНО:** Перед восстановлением автоматически создаётся резервная копия!

## Примеры использования

### Пример 1: Создание версии перед большими изменениями

```bash
# Перед началом работы создаём версию
python3 scripts/version_manager.py create v3.1 "Стабильная версия перед рефакторингом"

# Вносим изменения в spec/domain_model.md
# ...

# Если что-то пошло не так, откатываемся
python3 scripts/version_manager.py restore v3.1
```

### Пример 2: Сравнение изменений

```bash
# Создали версию v3.2
python3 scripts/version_manager.py create v3.2

# Внесли изменения
# ...

# Создали версию v3.3
python3 scripts/version_manager.py create v3.3

# Сравниваем что изменилось
python3 scripts/version_manager.py compare v3.2 v3.3

# Детальное сравнение конкретного файла
diff spec/versions/v3.2/domain_model.md spec/versions/v3.3/domain_model.md
```

### Пример 3: Просмотр истории версий

```bash
# Посмотреть все версии
python3 scripts/version_manager.py list

# Результат показывает когда и что было создано
```

## Структура версий

```
spec/
├── domain_model.md          # Текущая версия
├── data_model.puml
├── state_machine.puml
├── GUIDE.md
└── versions/
    ├── v3.0/
    │   ├── domain_model.md
    │   ├── data_model.puml
    │   ├── state_machine.puml
    │   ├── GUIDE.md
    │   └── version.json     # Метаданные
    ├── v3.1/
    │   └── ...
    └── v3.2/
        └── ...
```

## Метаданные версии (version.json)

```json
{
  "version": "v3.2",
  "created_at": "2026-03-11T12:00:00",
  "description": "Добавлена поддержка rollback",
  "files": [
    "domain_model.md",
    "data_model.puml",
    "state_machine.puml",
    "GUIDE.md"
  ]
}
```

## Интеграция с git

Version Manager дополняет git, но не заменяет его:

**Git:** Версионирование всего проекта, коммиты, ветки
**Version Manager:** Быстрые снапшоты спецификации, удобное сравнение

Рекомендуется использовать оба:
```bash
# Создать версию
python3 scripts/version_manager.py create v3.2

# Закоммитить в git
git add spec/versions/v3.2/
git commit -m "Создана версия v3.2 спецификации"
```

## Best Practices

1. **Создавайте версии перед большими изменениями**
   ```bash
   python3 scripts/version_manager.py create v3.1 "Перед рефакторингом"
   ```

2. **Используйте осмысленные имена версий**
   - ✅ v3.2, v3.2.1, v4.0
   - ❌ test, tmp, new

3. **Добавляйте описания**
   ```bash
   python3 scripts/version_manager.py create v3.2 "Добавлен rollback для Deployment"
   ```

4. **Регулярно проверяйте список версий**
   ```bash
   python3 scripts/version_manager.py list
   ```

5. **Используйте compare перед restore**
   ```bash
   python3 scripts/version_manager.py compare current v3.1
   python3 scripts/version_manager.py restore v3.1
   ```

## Troubleshooting

**Проблема:** Версия не создаётся

**Решение:** Проверьте что файлы существуют в `spec/`

**Проблема:** Restore не работает

**Решение:** Проверьте что версия существует в `spec/versions/`

**Проблема:** Compare показывает неточные результаты

**Решение:** Используйте `diff` для детального сравнения

## Changelog

### v1.0 (2026-03-11)
- Первая версия
- Создание, список, сравнение, восстановление версий
- Автоматические резервные копии при restore
- Метаданные версий
