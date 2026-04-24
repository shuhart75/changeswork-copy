---
name: diagram-updater
description: Проверка синхронизации PlantUML диаграмм с domain model и генерация PNG
version: 1.0
---

# Diagram Updater - Управление PlantUML диаграммами

Инструмент для проверки синхронизации PlantUML диаграмм с domain model и генерации PNG изображений.

## Возможности

1. **Проверка data_model.puml** - проверка наличия всех сущностей из domain_model.md
2. **Проверка state_machine.puml** - проверка наличия state machines для всех сущностей
3. **Проверка всех диаграмм** - комплексная проверка синхронизации
4. **Генерация PNG** - автоматическая генерация PNG из PlantUML файлов

## Использование

### Проверка data_model.puml

```bash
python3 scripts/diagram_updater.py check-data
```

Результат:
```
=== Извлечение сущностей из domain_model.md ===

✓ Найдено сущностей: 6
  - Initiative
  - Simulation
  - Pilot
  - Deployment
  - Scorecard
  - Package

=== Проверка синхронизации data_model.puml ===

✓ Initiative: найдена в data_model.puml
✓ Simulation: найдена в data_model.puml
✓ Pilot: найдена в data_model.puml
✓ Deployment: найдена в data_model.puml
✓ Scorecard: найдена в data_model.puml
✓ Package: найдена в data_model.puml

✓ Найдено: 6/6
```

### Проверка state_machine.puml

```bash
python3 scripts/diagram_updater.py check-state
```

Результат:
```
=== Извлечение сущностей из domain_model.md ===

✓ Найдено сущностей: 6

=== Проверка синхронизации state_machine.puml ===

✓ Initiative: найдена в state_machine.puml
✓ Simulation: найдена в state_machine.puml
✓ Pilot: найдена в state_machine.puml
✓ Deployment: найдена в state_machine.puml
✓ Scorecard: найдена в state_machine.puml
✓ Package: найдена в state_machine.puml

✓ Найдено: 6/6
```

### Проверка всех диаграмм

```bash
python3 scripts/diagram_updater.py check-all
```

Выполняет обе проверки и выводит итоговый результат.

### Генерация PNG из PlantUML

```bash
python3 scripts/diagram_updater.py generate-png
```

Что происходит:
1. Создаётся директория `spec/diagrams/` (если не существует)
2. Генерируются PNG файлы из PlantUML:
   - `data_model.png`
   - `state_machine.png`
3. PNG файлы сохраняются в `spec/diagrams/`

**Требования:**
- Установленный PlantUML: `sudo apt install plantuml`
- Или скачать с https://plantuml.com/download

## Примеры использования

### Пример 1: Проверка после изменения domain_model.md

```bash
# Изменили domain_model.md (добавили новую сущность)
# Проверяем синхронизацию

python3 scripts/diagram_updater.py check-all

# Результат покажет, какие сущности отсутствуют в диаграммах
# Обновляем data_model.puml и state_machine.puml вручную
# Проверяем снова

python3 scripts/diagram_updater.py check-all
```

### Пример 2: Генерация PNG для документации

```bash
# Обновили PlantUML диаграммы
# Генерируем PNG для вставки в документацию

python3 scripts/diagram_updater.py generate-png

# PNG файлы появятся в spec/diagrams/
# Можно использовать в README.md или других документах
```

### Пример 3: Проверка перед коммитом

```bash
# Перед коммитом проверяем синхронизацию

python3 scripts/diagram_updater.py check-all

# Если всё ОК - коммитим
# Если есть несоответствия - исправляем
```

## Как работает проверка

### Извлечение сущностей

Скрипт ищет в `domain_model.md` секции вида:
```markdown
### Entity: EntityName
### Сущность: EntityName
```

И извлекает имена сущностей (Initiative, Simulation, Pilot, и т.д.).

### Проверка data_model.puml

Для каждой сущности проверяет наличие в PlantUML:
```plantuml
entity EntityName {
  ...
}
```

или

```plantuml
class EntityName {
  ...
}
```

### Проверка state_machine.puml

Для каждой сущности проверяет наличие упоминания в файле (state machine, комментарии, заголовки).

## Интеграция с другими skills

### С spec-sync

```bash
# Сначала проверяем общую синхронизацию
python3 .claude/skills/spec-sync/check_sync.py

# Затем проверяем диаграммы
python3 scripts/diagram_updater.py check-all
```

### С version-manager

```bash
# Создаём версию перед изменениями
python3 scripts/version_manager.py create v3.2 "Перед добавлением новой сущности"

# Вносим изменения в domain_model.md и диаграммы
# ...

# Проверяем синхронизацию
python3 scripts/diagram_updater.py check-all

# Если всё ОК - создаём новую версию
python3 scripts/version_manager.py create v3.3 "Добавлена новая сущность"
```

## Структура файлов

```
spec/
├── domain_model.md          # Источник истины
├── data_model.puml          # ER диаграмма (проверяется)
├── state_machine.puml       # State machines (проверяется)
└── diagrams/                # Сгенерированные PNG
    ├── data_model.png
    └── state_machine.png
```

## Ограничения

1. **Автоматическое обновление не поддерживается** - скрипт только проверяет синхронизацию, но не обновляет PlantUML файлы автоматически
2. **Генерация PNG требует PlantUML** - без установленного PlantUML команда `generate-png` не работает
3. **Простая проверка** - скрипт проверяет только наличие сущностей, но не проверяет корректность атрибутов и связей

## Best Practices

1. **Проверяйте синхронизацию после каждого изменения domain_model.md**
   ```bash
   python3 scripts/diagram_updater.py check-all
   ```

2. **Генерируйте PNG для документации**
   ```bash
   python3 scripts/diagram_updater.py generate-png
   ```

3. **Используйте вместе с version-manager**
   - Создавайте версию перед изменениями
   - Проверяйте синхронизацию после изменений
   - Создавайте новую версию после проверки

4. **Интегрируйте в pre-commit hook**
   ```bash
   #!/bin/bash
   # .git/hooks/pre-commit
   python3 scripts/diagram_updater.py check-all
   if [ $? -ne 0 ]; then
     echo "Диаграммы не синхронизированы с domain_model.md"
     exit 1
   fi
   ```

## Troubleshooting

**Проблема:** Сущность не найдена в data_model.puml

**Решение:** Добавьте сущность в PlantUML файл:
```plantuml
entity EntityName {
  * id : uuid <<PK>>
  ...
}
```

**Проблема:** PlantUML не установлен

**Решение:** Установите PlantUML:
```bash
sudo apt install plantuml
```

**Проблема:** Генерация PNG зависает

**Решение:** Проверьте синтаксис PlantUML файлов, возможно есть ошибки

## Changelog

### v1.0 (2026-03-11)
- Первая версия
- Проверка синхронизации data_model.puml
- Проверка синхронизации state_machine.puml
- Генерация PNG из PlantUML
