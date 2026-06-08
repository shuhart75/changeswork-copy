# Конфигурация процесса (Backend)

Статус: **draft**  
Feature: `pilots-config-type`  
Slice: `config`  
Область: `MVP`  
Дата обновления: `2026-06-08`  
Шаблон: `.workflow/templates/requirements/backend.template.md`

## Связь с feature-level документом

- Главный контрольный документ: `../../requirements.md`
- Этот файл детализирует раздел `Реализация BACKEND` для текущего slice.

## Назначение пакета

Backend должен хранить, валидировать и возвращать тип процесса пилота/эксперимента без изменения жизненного цикла пилотов.

## Источники и трассировка

### Основные источники

- `../slice.md`
- `../../feature.md`
- `../../references.md`
- `/home/reutov/Downloads/coda_docs/coda-docs_features_pilots-config-type_requirements.md`
- `/home/reutov/Downloads/coda_docs/coda-docs_features_pilots-config-type_domain-impact.md`

### Связанные planning stories

- `STORY-PILOTS-CONFIG-001` — не импортирован в режиме `requirements`.

### Связанные доменные решения

- `DEC-2026-05-13-PILOTS-CONFIG-TYPE`

### Связанные артефакты

- Feature requirements: `../../requirements.md`
- Frontend requirements: `frontend.md`
- Domain impact: `../../domain-impact.md`
- Existing pilots BE pack: `features/pilots/slices/workspace/requirements/backend.md`

## Контекст и бизнес-смысл

### Цель

Сделать тип процесса частью persisted model, чтобы downstream API мог однозначно передавать контур пилота.

### Источник правды

Внутренняя таблица `experiments`, поле `process_type`.

### Затронутые bounded contexts / aggregates

- `Pilot Service` / experiment service.
- `Experiment` aggregate.

### Термины и определения

- `processType` — API field.
- `process_type` — database column.

## Бизнес-правила и системные ограничения

### BR-1. Допустимые значения
- `process_type` принимает только `online`, `offline`, `online+offline`.

### BR-2. Default и миграция
- Новые записи по умолчанию получают `online`, если клиент не прислал значение.
- Существующие записи backfill-ятся в `online`.

### BR-3. Редактирование
- `processType` меняется только в тех же сценариях, где разрешено редактирование пилота/эксперимента.

## Границы MVP

### Входит в MVP

- DB column, enum validation, default, backfill;
- request/response schema update;
- возврат `processType` в списках и деталке.

### Не входит в MVP

- отдельный справочник типов процесса;
- новая lifecycle-логика;
- изменение `/api/v2/config`.

### Отложено после MVP

- baseline promotion и OpenAPI source-file update, если canonical yaml будет добавлен в repo.

## Пользовательские и системные сценарии

### Сценарий BE-1. Создание эксперимента
1. Backend получает `processType` или не получает поле.
2. Если поле отсутствует, применяет `online`.
3. Валидирует enum.
4. Сохраняет значение в `experiments.process_type`.

### Сценарий BE-2. Получение списка/деталки
1. Backend читает `experiments.process_type`.
2. Возвращает `processType` в response DTO.
3. Для legacy данных после миграции пустых значений нет.

## Функциональные требования

### BE-FR-1. Хранение process_type

**Описание:** В таблице `experiments` должно появиться поле `process_type`.

**Правила и ограничения:**
- тип `VARCHAR(32)`;
- `NOT NULL`;
- default `online`;
- CHECK/enum по допустимым значениям.

**Зависимости:**
- миграция данных и rollback script.

### BE-FR-2. API-схемы

**Описание:** Внутренние experiment endpoints должны принимать/возвращать `processType`.

**Правила и ограничения:**
- `CreateExperiment` и `UpdateExperiment` принимают optional `processType`;
- response-схемы возвращают non-null `processType`;
- неизвестные значения возвращают validation error.

**Зависимости:**
- canonical OpenAPI `coda_api.yaml` заявлен входящими материалами, но в repo не найден.

## Модель данных

### Основные сущности и поля

| Сущность / таблица | Поле | Тип | Обязательность | Описание |
|---|---|---|---|---|
| `experiments` | `process_type` | `VARCHAR(32)` | да, default `online` | Тип процесса: `online`, `offline`, `online+offline` |

### Инварианты и ограничения

- `process_type IS NOT NULL`.
- `process_type IN ('online', 'offline', 'online+offline')`.

### Индексы / уникальности / FK

- Индекс по `process_type` нужен только если реализация `/api/v3/config` будет фильтровать большие объёмы без иного селективного условия.

## API-контракт

### Эндпоинты

| Метод и маршрут | Назначение | Кто вызывает | Примечание |
|---|---|---|---|
| `POST /api/v1/experiment` | создать эксперимент/пилот | Frontend/API client | request `processType` optional |
| `PUT /api/v1/experiment/{id}` | обновить эксперимент/пилот | Frontend/API client | request `processType` optional |
| `POST /api/v1/experiments` | список экспериментов | Frontend/API client | response records include `processType` |
| `POST /api/v1/experimentsExtended` | расширенный список | Frontend/API client | response records include `processType` |
| `POST /api/v1/experimentsWithSampleHistory` | список с историей выборок | Frontend/API client | response records include `processType` |
| `GET /api/v1/experiment/{number}` | атрибуты эксперимента | Frontend/API client | response includes `processType` |
| `/api/v3/config` | получить внешнюю конфигурацию экспериментов | Splitter/config consumer | Config Service фильтрует по optional `processType` |

### OpenAPI fragment

```yaml
openapi: 3.0.3
info:
  title: AS KODA Experiment API processType delta
  version: 1.0.0
components:
  schemas:
    ProcessType:
      type: string
      enum: [online, offline, online+offline]
      default: online
    CreateExperiment:
      type: object
      properties:
        processType:
          $ref: '#/components/schemas/ProcessType'
    UpdateExperiment:
      type: object
      properties:
        processType:
          $ref: '#/components/schemas/ProcessType'
    Experiment:
      type: object
      required: [processType]
      properties:
        processType:
          $ref: '#/components/schemas/ProcessType'
```

### Примеры запросов и ответов

#### Пример 1. Создание с explicit processType

```http
POST /api/v1/experiment HTTP/1.1
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "name": "Пилот offline-сценария",
  "processType": "offline"
}
```

```json
{
  "number": "EXP-001",
  "name": "Пилот offline-сценария",
  "processType": "offline"
}
```

#### Пример 2. Создание без processType

```json
{
  "name": "Пилот online по умолчанию"
}
```

```json
{
  "number": "EXP-002",
  "name": "Пилот online по умолчанию",
  "processType": "online"
}
```

## Интеграции, вычисления и фоновые процессы

- Внешние системы: splitter/config consumers вызывают `/api/v3/config`; Config Service возвращает уже отфильтрованный результат.
- Асинхронные процессы: одноразовый backfill/migration.
- Вычисление статусов / derived fields: не меняется.
- Идемпотентность / ретраи: миграция должна быть повторяемой или защищённой idempotent checks.

## Ошибки и валидация

### Валидационные правила

- если `processType` отсутствует при создании, применяется `online`;
- если `processType` передан и не входит в enum, запрос отклоняется;
- NULL после миграции невозможен.

### Ошибки API

| Код/сценарий | Условие | Ответ |
|---|---|---|
| `422` | неизвестный `processType` | validation error с перечнем допустимых значений |
| `422` | попытка изменить `processType`, когда пилот не редактируем | существующая ошибка редактирования по статусу |

## Миграция и обратная совместимость

- Нужны миграции данных: да, добавить column и backfill.
- Нужен backfill: да, все существующие `experiments` получают `online`.
- Есть риски для текущего baseline: возможна несовместимость generated clients, если они не допускают новые поля.
- Что должно попасть в release finalization: migration script, OpenAPI update, release notes для потребителей.

## Observability и аудит

- Логи: ошибки валидации неизвестных значений.
- Метрики: количество записей по `process_type` полезно для эксплуатации, но не обязательно для MVP.
- Audit trail: mutation audit должен фиксировать изменение поля.

## Критерии приемки

### BE-AC-1. Модель данных
- [ ] `experiments.process_type` создано как non-null поле с default `online`.
- [ ] Backfill существующих записей выполнен.
- [ ] Невалидное значение отклоняется.

### BE-AC-2. API
- [ ] Create/update принимает `processType`.
- [ ] List/detail/history endpoints возвращают `processType`.
- [ ] OpenAPI-схемы обновлены для request/response DTO.

## Открытые вопросы и допущения

- Нужно подтвердить canonical OpenAPI-файл: входящий путь `context/source-materials/current-system/requirements/raw/docs/coda_api.yaml` в текущем repo отсутствует.
- Нужно внести/проверить canonical внешний OpenAPI для `/api/v3/config`; входящий путь `context/source-materials/current-system/requirements/raw/docs/vneshneye_api_polucheniya_konfiguratsii_eksperimentov.3.1.1.yml` в текущем repo отсутствует.
