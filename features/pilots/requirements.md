# Требования по feature — Пилоты

Статус: **draft**
Feature: `features/pilots/feature.md`
Квартал: `2026-Q2`
Дата обновления: `2026-04-27`
Шаблон: `.workflow/templates/requirements/feature-requirements.template.md`

## Оглавление

Используются заголовки до уровня `####`.

## Общий контур feature

- Назначение feature: собрать контрольный слой по workspace пилотов.
- Что уже есть в baseline/current: детальные frontend/backend requirements пилотов.
- Какая дельта добавляется этой feature: единый feature-level документ контроля требований.
- Какие slice входят в контрольный документ: `workspace`.

## Порядок slice для контроля

1. `01 workspace — Workspace пилотов`

---

## STORY-PILOTS-001 — Workspace пилотов

Slice card: `slices/workspace/slice.md`
Детализация FE: `slices/workspace/requirements/frontend.md`
Детализация BE: `slices/workspace/requirements/backend.md`
Прототип: `slices/workspace/delivery-prototype/prototype.html`
Planning story: `не нормализована отдельно; imported workspace scope`

**Бизнес-требования**

- Цель: зафиксировать единый контур работы с пилотами: list/detail/form/lifecycle в рамках одного workspace.
- Бизнес-правила: пилоты связаны с deployment и scorecards; lifecycle и approval constraints обязательны.
- Ограничения: root document не заменяет детальные packs.

**Пользовательские требования к АС КОДА**

- Пользователь должен иметь единый рабочий контур для пилотов и связанных действий.

**Критерии приемки**

1. Workspace покрывает базовые сценарии пилотов без противоречий.
2. Связь с deployment и scorecards отражена корректно.
3. Lifecycle и approval rules не расходятся с backend behavior.

**USE CASES**

- **осн. сценарий 1** пользователь создаёт или открывает пилот.
- **альт. сценарий 1.1** пользователь меняет состав связанных scorecards.
- **альт. сценарий 1.2** действие блокируется статусом или ролью.
- **осн. сценарий 2** пользователь доводит пилот до следующего lifecycle-состояния.

### Функциональные требования

#### Реализация для FRONTEND

**Описание UI**

| Экран | Результат |
| --- | --- |
| Workspace пилотов | Поддерживает основные пользовательские сценарии пилотов |

Требования на фронт:

- реализовать единый workspace пилотов по детальным требованиям.

Связанный детальный FE pack: `slices/workspace/requirements/frontend.md`

#### Реализация BACKEND

Требования на бэк:

- обеспечить contracts для списка, формы, detail и lifecycle пилотов.

Связанный детальный BE pack: `slices/workspace/requirements/backend.md`

| | |
| --- | --- |
| **Сервис** | `pilots workspace` |
| ИФТ URL | `уточняется` |
| База данных | `см. detail pack` |
| Методы | `см. slices/workspace/requirements/backend.md` |

**Изменения в ролевой модели**

- На уровне control document новых ролей не зафиксировано.

**Отправка в Аудит**

- В аудит попадают lifecycle и mutation actions, если это закреплено в detail packs.

**BUGS (Если есть)**

- Пока не зафиксированы.

### Доп. пояснения

- Для pilots пока достаточно одного root section, потому что детальные packs уже собирают весь контур в workspace.
