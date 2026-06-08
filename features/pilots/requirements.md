# Требования по feature — Пилоты

Статус: **draft**
Feature: `features/pilots/feature.md`
Квартал: `2026-Q2`
Дата обновления: `2026-06-08`
Шаблон: `.workflow/templates/requirements/feature-requirements.template.md`

## Оглавление

Используются заголовки до уровня `####`.

## Общий контур feature

- Назначение feature: собрать контрольный слой по workspace пилотов.
- Что уже есть в baseline/current: детальные frontend/backend requirements пилотов.
- Какая дельта добавляется этой feature: единый feature-level документ контроля требований; отдельная дельта `processType` вынесена в `features/pilots-config-type/` и синхронизирована здесь как связанное изменение workspace.
- Какие slice входят в контрольный документ: `workspace`; связанный requirements-пакет `pilots-config-type/config`.

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
- Бизнес-правила: пилоты связаны с deployment и scorecards; lifecycle и approval constraints обязательны; пилот/эксперимент имеет обязательный тип процесса `processType` со значениями `online`, `offline`, `online+offline`.
- Ограничения: root document не заменяет детальные packs; детальная дельта `processType` ведётся в `features/pilots-config-type/requirements.md`.

**Пользовательские требования к АС КОДА**

- Пользователь должен иметь единый рабочий контур для пилотов и связанных действий.
- Пользователь должен видеть и задавать тип процесса пилота при создании/редактировании в допустимых статусах.

**Критерии приемки**

1. Workspace покрывает базовые сценарии пилотов без противоречий.
2. Связь с deployment и scorecards отражена корректно.
3. Lifecycle и approval rules не расходятся с backend behavior.
4. Поле `processType` хранится и возвращается backend API пилотов/экспериментов, а UI отображает его в форме и деталке.

**USE CASES**

- **осн. сценарий 1** пользователь создаёт или открывает пилот.
- **альт. сценарий 1.1** пользователь меняет состав связанных scorecards.
- **альт. сценарий 1.2** пользователь выбирает или меняет `processType`.
- **альт. сценарий 1.3** действие блокируется статусом или ролью.
- **осн. сценарий 2** пользователь доводит пилот до следующего lifecycle-состояния.

### Функциональные требования

#### Реализация для FRONTEND

**Описание UI**

| Экран | Результат |
| --- | --- |
| Workspace пилотов | Поддерживает основные пользовательские сценарии пилотов |

Требования на фронт:

- реализовать единый workspace пилотов по детальным требованиям.
- добавить в форму создания/редактирования обязательный select `Тип процесса` со значениями `Онлайн`, `Офлайн`, `Онлайн+Офлайн`; значение по умолчанию при создании — `Онлайн`.
- отображать тип процесса в деталке пилота в читаемом виде.

Связанный детальный FE pack: `slices/workspace/requirements/frontend.md`

#### Реализация BACKEND

Требования на бэк:

- обеспечить contracts для списка, формы, detail и lifecycle пилотов.
- хранить `processType` во внутренней модели экспериментов как `experiments.process_type`, `VARCHAR`, `NOT NULL`, default `online`.
- возвращать `processType` в списках, деталке и OpenAPI-схемах внутренних experiment endpoints, перечисленных в `features/pilots-config-type/requirements.md`.

Связанный детальный BE pack: `slices/workspace/requirements/backend.md`

| | |
| --- | --- |
| **Сервис** | `pilots workspace` |
| ИФТ URL | `уточняется` |
| База данных | `см. detail pack`; `experiments.process_type` |
| Методы | `см. slices/workspace/requirements/backend.md`; `features/pilots-config-type/requirements.md` |

**Изменения в ролевой модели**

- На уровне control document новых ролей не зафиксировано.

**Отправка в Аудит**

- В аудит попадают lifecycle и mutation actions, если это закреплено в detail packs.

**BUGS (Если есть)**

- Пока не зафиксированы.

### Доп. пояснения

- Для pilots пока достаточно одного root section, потому что детальные packs уже собирают весь контур в workspace.
- Внутренняя модель входящей дельты использует термин `experiments`, а пользовательский UI — `Пилоты`; это терминологическое соответствие зафиксировано в `features/pilots-config-type/requirements.md`.
