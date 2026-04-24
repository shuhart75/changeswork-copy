---
name: spec-sync
description: Синхронизация изменений между связанными документами спецификации (domain model, data model, state machine, guide). Обновлено для поддержки билингвального контента (русский/английский).
version: 1.1
---

# Spec Sync - Синхронизация спецификации

Автоматическая синхронизация изменений между связанными документами спецификации.

## Версия 1.1 - Изменения

- ✅ Улучшена поддержка билингвального контента (русский/английский)
- ✅ Исправлены false positives при проверке сущностей
- ✅ Улучшена проверка junction таблиц
- ✅ Фильтрация заголовков секций при проверке состояний

## Назначение

Когда вы изменяете один документ спецификации (например, domain_model.md), изменения должны быть отражены в связанных документах (data_model.puml, state_machine.puml, GUIDE.md). Этот skill автоматизирует процесс синхронизации.

## Использование

### Проверка несоответствий

```bash
# Проверить, есть ли несоответствия между документами
python3 .claude/skills/spec-sync/check_sync.py
```

Результат:
- ✓ Все файлы спецификации найдены
- ✓ Проверка сущностей (Initiative, Simulation, Pilot, Deployment, Scorecard, Package)
- ✓ Проверка junction таблиц (pilot_scorecard, deployment_scorecard, etc.)
- ✓ Проверка критичных состояний

### Что проверяется

1. **Наличие файлов:**
   - spec/domain_model.md
   - spec/data_model.puml
   - spec/state_machine.puml
   - spec/GUIDE.md

2. **Сущности:**
   - Проверка наличия всех основных сущностей во всех документах
   - Поддержка английских и русских названий
   - Учёт вариантов написания (Initiative/Инициатива)

3. **Junction таблицы:**
   - pilot_scorecard
   - deployment_scorecard
   - initiative_subproduct
   - scorecard_subproduct

4. **Критичные состояния:**
   - Черновик, Активна, Завершена, Архивирована
   - Выполняется, Ошибка, Одобрена

## Конфигурация

Файл `.claude/skills/spec-sync/config.json`:

```json
{
  "source_files": [
    "spec/domain_model.md",
    "spec/data_model.puml",
    "spec/state_machine.puml",
    "spec/GUIDE.md"
  ],
  "entity_mapping": {
    "Initiative": ["initiative", "Инициатива"],
    "Simulation": ["simulation", "Симуляция"],
    "Pilot": ["pilot", "Пилот"],
    "Deployment": ["deployment", "Внедрение"],
    "Scorecard": ["scorecard", "Скоркарта"],
    "Package": ["package", "Пакет"]
  }
}
```

## Примеры

### Пример 1: Проверка после изменения domain_model.md

```bash
# Изменили domain_model.md
# Запускаем проверку
python3 .claude/skills/spec-sync/check_sync.py

# Результат:
# ✓ Все файлы спецификации найдены
# ✓ Pilot: найдена во всех файлах
# ✓ Deployment: найдена во всех файлах
# ⚠ Предупреждений: 0
```

### Пример 2: Добавление новой сущности

```bash
# Добавили новую сущность "Report" в domain_model.md
# Запускаем проверку
python3 .claude/skills/spec-sync/check_sync.py

# Результат:
# ⚠ Сущность 'Report' не найдена в: spec/data_model.puml, spec/state_machine.puml
#
# Рекомендация: добавить Report в data_model.puml и state_machine.puml
```

## Интеграция с Claude Code

Skill автоматически доступен через:
```bash
/spec-sync
```

## Changelog

### v1.1 (2026-03-11)
- Улучшена поддержка билингвального контента
- Исправлены false positives
- Улучшена проверка junction таблиц
- Фильтрация заголовков секций

### v1.0 (2026-03-11)
- Первая версия
- Базовая проверка синхронизации
