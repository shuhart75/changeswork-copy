# Требования по feature — Типизация конфигов пилотов

Статус: **draft**  
Feature: `features/pilots-config-type/feature.md`  
Квартал: `2026-Q2`  
Дата обновления: `2026-06-08`  
Шаблон: `.workflow/templates/requirements/feature-requirements.template.md`

## Оглавление

Используются заголовки до уровня `####`.

## Общий контур feature

- Назначение feature: добавить поле `processType` для выбора контура пилота/эксперимента.
- Что уже есть в baseline/current: существующая модель пилотов/экспериментов без явного типа процесса.
- Какая дельта добавляется этой feature: обязательное поле `processType`, хранение в `experiments.process_type`, возврат в API и отображение в UI.
- Какие slice входят в контрольный документ: `config`.
- Какой общий feature prototype используется как визуальная база: `features/pilots/slices/workspace/delivery-prototype/prototype.html` требует последующей актуализации в prototype mode.

**Терминология:** внешнее пользовательское представление — "пилоты"; внутренняя модель и API текущей системы используют "experiments". Для этой дельты источник данных — таблица `experiments`.

## Порядок slice для контроля

1. `01 config — Конфигурация процесса`

---

## STORY-PILOTS-CONFIG-001 — Конфигурация процесса

Slice card: `slices/config/slice.md`  
Детализация FE: `slices/config/requirements/frontend.md`  
Детализация BE: `slices/config/requirements/backend.md`  
Общий prototype: `features/pilots/slices/workspace/delivery-prototype/prototype.html`  
Slice prototype: `slices/config/delivery-prototype/prototype.html` во входящей папке не импортирован в режиме `requirements`  
Planning story: `planning/stories/STORY-PILOTS-CONFIG-001.md` во входящей папке не импортирован в режиме `requirements`

**Бизнес-требования**

- Цель: пользователь задаёт контур пилота/эксперимента, чтобы downstream-потребители могли выбирать применимые конфигурации для online/offline сценариев.
- Бизнес-правила: допустимые значения `online`, `offline`, `online+offline`; значение по умолчанию — `online`; существующие записи мигрируются в `online`.
- Ограничения: изменение не вводит новые роли и не меняет жизненный цикл пилота.

**Пользовательские требования к АС КОДА**

- Пользователь должен иметь возможность выбрать тип процесса при создании пилота.
- Пользователь должен видеть тип процесса на детальной странице пилота.
- Пользователь должен иметь возможность изменить тип процесса в тех же статусах, где разрешено редактирование пилота.
- Потребитель API должен получать `processType` в ответах experiment/pilot API.

**Критерии приемки**

1. UI содержит обязательный select `Тип процесса` со значениями `Онлайн`, `Офлайн`, `Онлайн+Офлайн`.
2. При создании без явного выбора применяется `online`.
3. Backend хранит значение в `experiments.process_type` и не допускает NULL/недопустимые значения.
4. Списковые, детальные и исторические experiment endpoints возвращают `processType`.
5. Существующие записи после миграции имеют `process_type = 'online'`.
6. Config Service фильтрует внешние конфигурации по `processType` только в `/api/v3/config`; `/api/v2/config` не расширяется в рамках этой дельты.

**USE CASES**

- **осн. сценарий 1** пользователь создаёт пилот и оставляет тип процесса `Онлайн` по умолчанию.
- **осн. сценарий 2** пользователь выбирает `Офлайн` или `Онлайн+Офлайн` в форме создания/редактирования.
- **осн. сценарий 3** пользователь открывает деталку пилота и видит читаемое значение типа процесса.
- **альт. сценарий 3.1** backend возвращает неизвестное значение — UI показывает ошибку данных и не даёт сохранить форму без корректировки.
- **осн. сценарий 4** потребитель API читает `processType` из ответа и применяет собственную договорённую логику.

### Функциональные требования

#### Реализация для FRONTEND

**Описание UI**

| Экран | Результат |
| --- | --- |
| Форма создания/редактирования пилота | Обязательное поле `Тип процесса` |
| Детальная страница пилота | Read-only отображение типа процесса |
| Список пилотов | Отображение типа процесса допустимо как колонка/чип, если это не перегружает текущий workspace |

Требования на фронт:

- добавить reusable select `PilotProcessTypeSelect` или эквивалентный компонент в форму пилота;
- использовать значения `online`, `offline`, `online+offline` на wire-level;
- показывать пользователю подписи `Онлайн`, `Офлайн`, `Онлайн+Офлайн`;
- при создании устанавливать `online` до отправки формы;
- валидировать значение на клиенте перед отправкой;
- блокировать редактирование типа процесса в тех же случаях, что и остальные редактируемые поля пилота.

Связанный детальный FE pack: `slices/config/requirements/frontend.md`

#### Реализация BACKEND

Требования на бэк:

- добавить поле `process_type` в таблицу `experiments`;
- задать `NOT NULL DEFAULT 'online'`;
- выполнить backfill существующих записей значением `online`;
- добавить проверку enum: `online`, `offline`, `online+offline`;
- обновить схемы `CreateExperiment`, `UpdateExperiment`, `Experiment`, `ExperimentRecord`, `ExtendedExperimentRecordWithSamplesDto`, `ExperimentWithSampleHistory`;
- обновить endpoints:
  - `POST /api/v1/experiment`;
  - `PUT /api/v1/experiment/{id}`;
  - `POST /api/v1/experiments`;
  - `POST /api/v1/experimentsExtended`;
  - `POST /api/v1/experimentsWithSampleHistory`;
  - `GET /api/v1/experiment/{number}`.

Связанный детальный BE pack: `slices/config/requirements/backend.md`

| | |
| --- | --- |
| **Сервис** | `experiment service` / `Pilot Service` |
| ИФТ URL | `уточняется` |
| База данных | `experiments.process_type` |
| Методы | `POST /api/v1/experiment`, `PUT /api/v1/experiment/{id}`, list/detail experiment endpoints |

**Фильтрация внешних конфигураций**

Уточнение от 2026-06-08: фильтрацию выполняет Config Service, причём только в `/api/v3/config`.

- `/api/v3/config` принимает optional `processType` и возвращает конфигурации по правилам:
  - `online` → `online` + `online+offline`;
  - `offline` → `offline` + `online+offline`;
  - `online+offline` → все конфигурации;
  - параметр не указан → только `online`.
- `/api/v2/config` не получает фильтрацию `processType` и не меняет контракт в рамках этой дельты.
- Splitter не выполняет самостоятельную фильтрацию по `process_type` для сценария `/api/v3/config`; он получает уже отфильтрованный результат.

**Изменения в ролевой модели**

- Новых ролей нет.
- Права редактирования типа процесса наследуют существующие права редактирования пилота.

**Отправка в Аудит**

- Создание/изменение `processType` аудируется как часть существующих mutation actions пилота/эксперимента.
- Отдельное audit-событие не требуется, если текущий audit trail уже сохраняет changed fields.

**BUGS (Если есть)**

- Входящие материалы по владельцу фильтрации были противоречивы; уточнение от 2026-06-08 принято как источник правды для living requirements.

### Доп. пояснения

- `online+offline` хранится как строковое enum-значение; при генерации OpenAPI нужно проверить escaping/валидацию плюса.
- Это изменение обратно совместимо для старых клиентов за счёт default/backfill `online`, но клиенты, читающие полную модель, должны быть готовы к новому полю в ответе.
