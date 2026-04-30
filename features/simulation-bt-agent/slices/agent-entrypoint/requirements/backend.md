# Точка входа, UI-сессия и статус агента (Backend)

Статус: **draft**
Feature: `simulation-bt-agent`
Slice: `agent-entrypoint`
Область: `MVP`
Дата обновления: `2026-04-30`
Шаблон: `.workflow/templates/requirements/backend.template.md`

## Связь с feature-level документом

- Главный контрольный документ: `../../requirements.md`
- Этот файл детализирует раздел `Реализация BACKEND` для текущего slice.

## Назначение пакета

- Зафиксировать backend-контракт открытия UI-сессии окна агента в АС КОДА.
- Описать нормализованный статус агента на основе RAIN `/health/liveness` и `/health/readiness`.
- Убрать предположение о вызове RAIN при открытии окна: по принятому RAIN API UI-сессию создаёт backend АС КОДА, а RAIN session создаётся лениво при первом `POST /chat/runs`.
- Сохранить existing simulation detail API как источник признаков доступности БТ.

## Источники и трассировка

### Основные источники

- `../slice.md`
- `../../feature.md`
- `../../references.md`
- `../../requirements.md`
- `baseline/current/domain/aggregates/simulation.md`
- `baseline/current/domain/contexts/research-and-execution.md`
- `context/change-requests/simulation-bt-agent/agent_openapi.yaml`
- `context/change-requests/simulation-bt-agent/Системные_требования_для_интеграции_АС_КОДА_и_AI_Агента_RAIN.md`
- `context/change-requests/simulation-bt-agent/simulations_api.md`

### Связанные planning stories

- `STORY-SIMULATION-BT-AGENT-001`

### Связанные доменные решения

- `DEC-2026-04-24-SIMULATION-BT-AGENT-001`
- `DEC-2026-04-27-SIMULATION-BT-AGENT-002`
- `DEC-2026-04-29-SIMULATION-BT-AGENT-007`
- `DEC-2026-04-30-SIMULATION-BT-AGENT-009`

### Связанные артефакты

- Feature requirements: `../../requirements.md`
- Требования фронтенда: `frontend.md`
- Domain impact: `../../domain-impact.md`
- Implementation tasks: `../execution/tasks.md`

## Контекст и бизнес-смысл

### Цель

Сделать открытие окна агента быстрым и независимым от долгого ответа RAIN, а status chip питать короткими health-проверками через backend АС КОДА.

### Источник правды

Источником правды для UI-сессии является АС КОДА. Источником правды для технической готовности RAIN являются `GET /health/liveness` и `GET /health/readiness`, но frontend получает только нормализованный статус backend АС КОДА. История и агентский контекст после первого run принадлежат RAIN и читаются через backend АС КОДА.

### Затронутые bounded contexts / aggregates

- `Research and Execution`
- `Simulation`
- `Identity and Access`
- прикладное состояние `agent_ui_session`

### Термины и определения

- `UI-сессия` — состояние окна агента в АС КОДА.
- `liveness` — признак, что сервис RAIN жив как процесс.
- `readiness` — признак, что RAIN готов принимать `/chat`.
- `agent status` — нормализованный статус для UI: `ready`, `not_ready`, `unavailable`, `unknown`.
- `status cache` — короткий backend cache результата health-проверок, чтобы не перегружать RAIN частыми проверками chip.

## Бизнес-правила и системные ограничения

### BR-1. Открытие окна не вызывает RAIN `/chat`
- при открытии окна backend АС КОДА создаёт или восстанавливает UI-сессию;
- backend не вызывает RAIN `/chat`, пока пользователь не отправил сообщение;
- RAIN не считается источником истории при открытии окна.

### BR-2. `session_id` и `start_datetime` создаёт backend АС КОДА
- frontend не генерирует `session_id` и не фиксирует `start_datetime`;
- если frontend вызывает `POST /dialog/session` без `session_id`, backend создаёт новую UI-сессию, фиксирует `start_datetime` и возвращает `session_id`;
- если frontend передаёт `session_id`, backend продолжает существующую UI-сессию текущего пользователя;
- отсутствие `session_id` в dialog API трактуется как сброс текущего окна и создание новой UI-сессии.

### BR-3. Status chip строится по readiness/liveness
- `readiness=200` означает, что агент готов принимать `/chat`;
- `readiness=503` при живом liveness означает, что агент недоступен для отправки сообщений;
- сбой liveness/readiness означает `unavailable` или `unknown`;
- composer/actions должны блокироваться при любом статусе, кроме `ready`.

### BR-4. Frontend не получает OTT и внутренний URL RAIN
- mTLS/OTT используется только server-to-server;
- frontend работает только с backend АС КОДА;
- тестовый режим без OTT на ИФТ допустим только как явно зарегистрированный технический долг.

### BR-5. Доступность БТ вычисляется по existing simulation detail API
- для определения подходящего контекста используется уже реализованная деталка симуляции;
- отдельный endpoint открытия окна не должен готовить БТ-контекст;
- подробности передачи `risk_params` в RAIN описаны в slice `bt-publication`.

## Границы MVP

### Входит в MVP

- `POST /dialog/session` для создания/восстановления UI-сессии АС КОДА;
- `GET /dialog/agent/status` для нормализованного статуса агента;
- backend вызовы RAIN `/health/liveness` и `/health/readiness`;
- status cache;
- валидация `session_id`;
- связь UI-сессии с пользователем.

### Не входит в MVP

- вызов RAIN при открытии окна;
- прямое восстановление истории из RAIN при открытии окна без явного запроса истории;
- прямой frontend call в RAIN;
- выдача OTT в frontend;
- отдельный preparatory API для БТ при открытии окна.

### Отложено после MVP

- подробная диагностика readiness для support UI;
- circuit breaker с отдельной страницей мониторинга;
- перенос UI-сессии между устройствами.

## Пользовательские и системные сценарии

### Сценарий BE-1. Открытие UI-сессии
1. Frontend вызывает `POST /dialog/session`.
2. Backend проверяет пользователя.
3. Если `session_id` передан, backend восстанавливает UI-сессию текущего пользователя.
4. Если `session_id` отсутствует, backend создаёт новую UI-сессию и новый `session_id`.
5. Backend возвращает базовое состояние UI-сессии без вызова RAIN `/chat`.

### Сценарий BE-2. Проверка статуса агента
1. Frontend вызывает `GET /dialog/agent/status`.
2. Backend использует свежий cache или делает короткие server-to-server проверки RAIN health.
3. Backend возвращает нормализованный status.

### Сценарий BE-3. RAIN не готов
1. RAIN `/health/readiness` возвращает `503` или health check не отвечает.
2. Backend возвращает `not_ready`, `unavailable` или `unknown`.
3. Frontend блокирует composer/actions.

## Функциональные требования

### BE-FR-1. UI-сессия создаётся и восстанавливается в АС КОДА

**Описание:**
Backend должен иметь endpoint открытия/восстановления UI-сессии окна агента без обращения к RAIN `/chat`.

**Правила и ограничения:**
- request может содержать optional `session_id`;
- если `session_id` передан, он должен быть UUID и принадлежать текущему пользователю;
- если `session_id` не передан, backend создаёт новый UUID и фиксирует `start_datetime`;
- UI-сессия связывается с текущим пользователем СУДИР;
- повторный вызов с тем же `session_id` восстанавливает UI-сессию и active run status, если он есть;
- дополнительные данные вроде `contextPrompt`, истории и риск-параметров в этом вызове не нужны.

**Зависимости:**
- frontend UI session;
- хранилище UI-сессий АС КОДА.

### BE-FR-2. Backend отдаёт нормализованный статус агента

**Описание:**
Backend должен предоставить frontend status endpoint, который скрывает детали RAIN health endpoints.

**Правила и ограничения:**
- backend вызывает или кэширует `GET RAIN /health/liveness`;
- backend вызывает или кэширует `GET RAIN /health/readiness`;
- короткий таймаут health-check рекомендуемо `1-2` секунды;
- status cache TTL рекомендуемо `5-15` секунд;
- ответ frontend содержит нормализованный `status`, время проверки и безопасную причину;
- `ready` возможен только при успешном readiness;
- `not_ready`, `unavailable`, `unknown` должны приводить к блокировке отправки сообщений.

**Зависимости:**
- RAIN health endpoints;
- инфраструктура mTLS/OTT.

### BE-FR-3. Existing detail API остаётся источником контекста страницы

**Описание:**
Backend открытия окна не должен вводить отдельный preparatory endpoint для БТ.

**Правила и ограничения:**
- для страниц симуляций используется уже реализованный `GET /api/v1/simulation/{number}`;
- отсутствие конкретной симуляции означает, что action по БТ недоступен;
- детальная проверка возможности БТ выполняется в slice `bt-publication`;
- opening/status endpoints не должны мутировать данные симуляции.

**Зависимости:**
- existing simulation API;
- slice `bt-publication`.

## Модель данных

### Основные сущности и поля

| Сущность / таблица | Поле | Тип | Обязательность | Описание |
|---|---|---|---|---|
| `agent_ui_session` | `session_id` | UUID/string | обязательно | backend-generated идентификатор UI-сессии |
| `agent_ui_session` | `user_id` | string/UUID | обязательно | пользователь СУДИР |
| `agent_ui_session` | `start_datetime` | timestamp with timezone | обязательно | момент первого открытия окна |
| `agent_ui_session` | `created_at` / `updated_at` | timestamp | обязательно | технические даты |
| `agent_status_cache` | `status` | enum | обязательно | `ready`, `not_ready`, `unavailable`, `unknown` |
| `agent_status_cache` | `liveness_status` | string/null | опционально | результат `/health/liveness` |
| `agent_status_cache` | `readiness_status` | string/null | опционально | результат `/health/readiness` |
| `agent_status_cache` | `checked_at` | timestamp | обязательно | время последней проверки |

### Инварианты и ограничения

- `session_id` генерируется backend и не должен быть доступен другому пользователю;
- открытие UI-сессии не создаёт run и не вызывает RAIN `/chat`;
- `ready` не выставляется без успешного readiness;
- status cache не должен скрывать длительную недоступность агента сверх TTL.

### Индексы / уникальности / FK

- уникальный индекс по `session_id` в рамках пользователя или пользовательской СУДИР-сессии;
- индекс по `user_id`, `updated_at` для обслуживания активных UI-сессий.

## API-контракт

### Эндпоинты

| Метод и маршрут | Назначение | Кто вызывает | Примечание |
|---|---|---|---|
| `POST /dialog/session` | открыть, восстановить или сбросить UI-сессию | frontend agent window | отсутствие `session_id` создаёт новую сессию; не вызывает RAIN `/chat` |
| `GET /dialog/agent/status` | получить нормализованный статус агента | frontend status chip | backend использует RAIN liveness/readiness |
| `GET RAIN /health/liveness` | проверить, что сервис жив | backend АС КОДА | server-to-server |
| `GET RAIN /health/readiness` | проверить готовность к `/chat` | backend АС КОДА | server-to-server |

### OpenAPI fragment

```yaml
openapi: 3.0.3
info:
  title: Agent Entrypoint and Status API
  version: 1.0.0
paths:
  /dialog/session:
    post:
      summary: Открыть или восстановить UI-сессию окна агента
      requestBody:
        required: false
        content:
          application/json:
            schema:
              type: object
              properties:
                session_id:
                  type: string
                  format: uuid
                  nullable: true
      responses:
        "200":
          description: UI-сессия открыта или восстановлена
          content:
            application/json:
              schema:
                type: object
                required: [session_id, can_send_message, dialog_status, history_changed]
                properties:
                  session_id:
                    type: string
                    format: uuid
                  can_send_message:
                    type: boolean
                  dialog_status:
                    type: string
                    enum: [idle, queued, running, succeeded, failed, timeout, cancelled]
                  history_changed:
                    type: boolean
  /dialog/agent/status:
    get:
      summary: Получить нормализованный статус RAIN
      responses:
        "200":
          description: Статус агента
          content:
            application/json:
              schema:
                type: object
                required: [status, checked_at]
                properties:
                  status:
                    type: string
                    enum: [ready, not_ready, unavailable, unknown]
                  liveness:
                    type: string
                    nullable: true
                  readiness:
                    type: string
                    nullable: true
                  checked_at:
                    type: string
                    format: date-time
                  reason:
                    type: string
                    nullable: true
components: {}
```

### Примеры запросов и ответов

#### Пример 1. Открытие UI-сессии

```http
POST /dialog/session HTTP/1.1
Content-Type: application/json
```

```json
{}
```

```json
{
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "can_send_message": true,
  "dialog_status": "idle",
  "history_changed": false
}
```

#### Пример 1.1. Продолжение UI-сессии

```http
POST /dialog/session HTTP/1.1
Content-Type: application/json
```

```json
{
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

```json
{
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "can_send_message": false,
  "dialog_status": "running",
  "history_changed": false
}
```

#### Пример 2. Статус агента

```http
GET /dialog/agent/status HTTP/1.1
```

```json
{
  "status": "ready",
  "liveness": "alive",
  "readiness": "ready",
  "checked_at": "2026-04-29T12:30:04.000+03:00",
  "reason": null
}
```

## Интеграции, вычисления и фоновые процессы

- Внешние системы: RAIN health endpoints;
- Асинхронные процессы: обновление status cache может выполняться по запросу или фоновой проверкой;
- Вычисление статусов / derived fields: `status=ready` только при успешном readiness;
- Идемпотентность / ретраи: повторное открытие UI-сессии с тем же `session_id` безопасно; вызов без `session_id` намеренно создаёт новую UI-сессию.

## Ошибки и валидация

### Валидационные правила

- если `session_id` передан, он должен быть UUID;
- пользователь должен иметь доступ к разделу симуляций;
- status endpoint не должен раскрывать внутренние URL, OTT или stack trace.

### Ошибки API

| Код/сценарий | Условие | Ответ |
|---|---|---|
| `400 invalid_session_id_format` | `session_id` не UUID | ошибка валидации |
| `403 access_denied` | нет доступа к разделу симуляций | отказ доступа |
| `503 agent_status_unavailable` | backend не смог проверить health RAIN | нормализованный `status=unknown/unavailable` |

## Миграция и обратная совместимость

- Нужны ли миграции данных: да, если UI-сессии/история хранятся в новом backend-хранилище.
- Нужен ли backfill: нет.
- Есть ли риски для текущего baseline: да, прежняя модель восстановления истории на стороне агента заменяется UI-сессией АС КОДА.
- Что должно попасть в release finalization: статусная модель агента, UI-сессия, health-check contract.

## Observability и аудит

- Логи: открытие UI-сессии, status checks, health-check latency, status transitions;
- Метрики: readiness success rate, liveness success rate, status cache hit rate, latency health endpoints;
- Audit trail: открытие окна не считается бизнес-публикацией БТ; бизнес-аудит в `bt-publication`.

## Критерии приемки

### BE-AC-1. UI-сессия
- [ ] `POST /dialog/session` создаёт или восстанавливает UI-сессию АС КОДА
- [ ] `POST /dialog/session` не вызывает RAIN `/chat`
- [ ] При отсутствии `session_id` backend создаёт новую UI-сессию и возвращает новый `session_id`
- [ ] Переданный `session_id` валидируется как UUID и принадлежит текущему пользователю
- [ ] UI-сессия связана с пользователем

### BE-AC-2. Статус агента
- [ ] Backend вызывает или кэширует RAIN `/health/liveness`
- [ ] Backend вызывает или кэширует RAIN `/health/readiness`
- [ ] Frontend получает только нормализованный статус
- [ ] При неготовом RAIN frontend может заблокировать composer/actions

## Открытые вопросы и допущения

- Требуется подтвердить инфраструктурные значения timeout и TTL для health status cache.
- Требуется зафиксировать, будет ли ИФТ временно работать без OTT и каким backlog/technical debt это оформляется.
