# Асинхронная отправка сообщения, polling и история (Backend)

Статус: **draft**
Feature: `simulation-bt-agent`
Slice: `dialog-session`
Область: `MVP`
Дата обновления: `2026-04-29`
Шаблон: `.workflow/templates/requirements/backend.template.md`

## Связь с feature-level документом

- Главный контрольный документ: `../../requirements.md`
- Этот файл детализирует раздел `Реализация BACKEND` для текущего slice.

## Назначение пакета

- Зафиксировать backend async facade над синхронным RAIN `POST /chat`.
- Описать хранение UI-сессии, истории сообщений и статусов run на стороне АС КОДА.
- Описать polling endpoint для frontend.
- Зафиксировать ограничения длины, таймауты, terminal statuses и запрет параллельных runs.

## Источники и трассировка

### Основные источники

- `../slice.md`
- `../../feature.md`
- `../../references.md`
- `../../requirements.md`
- `context/change-requests/simulation-bt-agent/agent_openapi.yaml`
- `context/change-requests/simulation-bt-agent/Системные_требования_для_интеграции_АС_КОДА_и_AI_Агента_RAIN.md`
- `context/change-requests/simulation-bt-agent/simulations_api.md`

### Связанные planning stories

- `STORY-SIMULATION-BT-AGENT-002`

### Связанные доменные решения

- `DEC-2026-04-24-SIMULATION-BT-AGENT-001`
- `DEC-2026-04-27-SIMULATION-BT-AGENT-002`
- `DEC-2026-04-29-SIMULATION-BT-AGENT-007`

### Связанные артефакты

- Feature requirements: `../../requirements.md`
- Frontend requirements: `frontend.md`
- Domain impact: `../../domain-impact.md`
- Implementation tasks: `../execution/tasks.md`

## Контекст и бизнес-смысл

### Цель

Скрыть от frontend долгий синхронный вызов RAIN `/chat`, сохранив для пользователя управляемый диалог и не блокируя браузерный request до полного ответа агента.

### Источник правды

Источником правды для UI-истории, активного run и terminal status является backend АС КОДА. RAIN является источником текста ответа `response`, но по текущему контракту не предоставляет историю, статус run или streaming.

### Затронутые bounded contexts / aggregates

- прикладное состояние UI-сессии агента вне базовой модели `Simulation`
- `Research and Execution`
- `Identity and Access`

### Термины и определения

- `agent_ui_session` — UI-сессия окна агента в АС КОДА, связанная с `session_id` и пользовательской СУДИР-сессией.
- `agent_dialog_run` — асинхронная операция отправки одного сообщения в RAIN.
- `agent_dialog_message` — сохранённое сообщение пользователя или агента для порционной истории.
- `RAIN /chat` — синхронный server-to-server метод агента из `agent_openapi.yaml`.
- `terminal status` — конечное состояние run: `succeeded`, `failed`, `timeout`, `cancelled`.

## Бизнес-правила и системные ограничения

### BR-1. RAIN вызывается только backend АС КОДА
- frontend не вызывает RAIN напрямую;
- OTT, mTLS и внутренние endpoints RAIN не передаются в браузер;
- backend АС КОДА маппит данные frontend/АС КОДА в контракт RAIN `/chat`.

### BR-2. Долгий вызов RAIN оборачивается в async run
- `POST /dialog/{session_id}/message` не ждёт полного ответа RAIN;
- backend создаёт `run_id` и возвращает `202 Accepted`;
- фоновый worker или async task вызывает RAIN `POST /chat`;
- frontend читает статус через polling.

### BR-3. В рамках одного `session_id` допускается один active run
- если для `session_id` уже есть run в статусе `queued` или `running`, новый `POST /message` отклоняется;
- это защищает от смешивания контекста и повторной публикации БТ;
- повторная отправка после terminal status считается новым пользовательским действием.

### BR-4. История хранится в АС КОДА и отдаётся страницами
- backend сохраняет user message до вызова RAIN и agent response после успеха;
- frontend не должен загружать всю историю сразу;
- backend обязан поддержать cursor/limit для истории;
- если история длинная, backend отдаёт последние сообщения и признак наличия более ранних.

### BR-5. Ограничения длины обязательны на backend
- backend валидирует длину `message` независимо от frontend;
- backend ограничивает размер сохраняемого `response` или переводит run в ошибку, если ответ превышает допустимый предел;
- числовые лимиты должны быть конфигурируемыми.

### BR-6. SLA RAIN учитывается через timeout policy
- SLA системных требований: стандартный запрос около `24.9 + 13.9` секунд, диалоговое взаимодействие около `91.6 + 69.2` секунд;
- backend не должен держать браузерный запрос открытым на это время;
- server-to-server вызов RAIN может быть долгим, но должен иметь hard timeout;
- создание БТ от подтверждения до ссылки не имеет подтверждённого SLA, поэтому timeout и retry policy должны быть явно согласованы.

## Границы MVP

### Входит в MVP

- `POST /dialog/{session_id}/message` с быстрым ответом `202 { run_id }`;
- фоновый вызов RAIN `POST /chat`;
- `GET /dialog/{session_id}/runs/{run_id}` для polling;
- `GET /dialog/{session_id}/messages` с cursor/limit;
- сохранение истории в АС КОДА;
- active run lock;
- server-side validation prompt length;
- обработка `succeeded`, `failed`, `timeout`, `cancelled`;
- логирование и метрики run.

### Не входит в MVP

- frontend SSE/WebSocket;
- streaming partial responses;
- polling самого RAIN, потому что в контракте нет run/status endpoint;
- параллельные runs в одной сессии;
- автоматический retry создания БТ без идемпотентности;
- хранение истории в RAIN как источник правды.

### Отложено после MVP

- переход на SSE при появлении streaming/status API у RAIN;
- отмена run с propagation cancel в RAIN;
- идемпотентный ключ публикации БТ;
- архивирование длинной истории.

## Пользовательские и системные сценарии

### Сценарий BE-1. Создание async run
1. Frontend вызывает `POST /dialog/{session_id}/message`.
2. Backend проверяет пользователя, `session_id`, readiness агента, лимит длины и отсутствие active run.
3. Backend сохраняет user message, создаёт `agent_dialog_run` в статусе `queued` или `running`.
4. Backend возвращает `202 Accepted` с `run_id`.
5. Backend в фоне вызывает RAIN `POST /chat`.

### Сценарий BE-2. Завершение run успехом
1. RAIN возвращает `200 { response }`.
2. Backend валидирует размер `response`, сохраняет agent message.
3. Run переводится в `succeeded`.
4. Polling endpoint возвращает terminal status и ссылку на сохранённое сообщение/результат.

### Сценарий BE-3. Timeout или ошибка RAIN
1. RAIN возвращает ошибку или не отвечает до hard timeout.
2. Backend переводит run в `failed` или `timeout`.
3. Backend сохраняет техническую ошибку и возвращает frontend нормализованный код.
4. Active run lock снимается по terminal status.

### Сценарий BE-4. Порционная история
1. Frontend запрашивает историю с `limit`.
2. Backend возвращает последние сообщения и `next_cursor`, если есть более ранние.
3. При запросе с `before` backend возвращает предыдущую страницу.

## Функциональные требования

### BE-FR-1. Отправка сообщения создаёт async run

**Описание:**
Backend должен принимать пользовательское сообщение и возвращать `run_id` без ожидания полного ответа RAIN.

**Правила и ограничения:**
- `session_id` обязателен и должен принадлежать текущей пользовательской СУДИР-сессии;
- `message` обязателен и не может быть пустым;
- `start_datetime` обязателен, формат ISO 8601 с миллисекундами;
- `fio` берётся из профиля СУДИР на backend или принимается от frontend только если это уже канонический frontend context; итоговое значение должно соответствовать профилю пользователя;
- при active run возвращается `409 run_in_progress`;
- при неготовом агенте возвращается `503 agent_not_ready`;
- успешный ответ `POST /message` имеет статус `202`, а не `200` с полным ответом агента.

**Зависимости:**
- UI session store;
- status API агента;
- worker/async execution infrastructure.

### BE-FR-2. Backend вызывает RAIN `POST /chat`

**Описание:**
Backend должен вызывать RAIN строго по предоставленному OpenAPI-контракту.

**Правила и ограничения:**
- server-to-server request содержит `session_id`, `message`, `start_datetime`, `fio`;
- `risk_params` и `simulation_id` передаются, когда сообщение связано с конкретной симуляцией и данные доступны;
- `risk_params.as_is` и `risk_params.to_be` собираются из доверенного existing simulation detail API или валидируются backend перед отправкой;
- backend использует HTTPS/mTLS/OTT для вызова RAIN, когда окружение это поддерживает;
- тестовый режим без OTT на ИФТ допускается только как явно зафиксированный технический долг, если OTT не готов во 2Q.

**Зависимости:**
- `context/change-requests/simulation-bt-agent/agent_openapi.yaml`;
- existing simulation detail API;
- инфраструктура mTLS/OTT.

### BE-FR-3. Polling endpoint возвращает состояние run

**Описание:**
Backend должен предоставить endpoint для чтения состояния run.

**Правила и ограничения:**
- endpoint возвращает `run_id`, `session_id`, `status`, `created_at`, `updated_at`;
- для terminal status возвращается нормализованный результат: `message_id` и/или `response` preview;
- для `failed`/`timeout` возвращается безопасный для UI код и сообщение;
- endpoint не раскрывает OTT, внутренние URL RAIN, stack trace или полный технический лог;
- чтение чужого run запрещено.

**Зависимости:**
- `agent_dialog_run` storage.

### BE-FR-4. История сообщений отдаётся через pagination

**Описание:**
Backend должен отдавать историю диалога страницами.

**Правила и ограничения:**
- поддерживаются параметры `limit` и `before`;
- default `limit` рекомендуемо `20`, max `50`;
- порядок ответа должен быть стабильным и позволять frontend восстановить хронологию;
- backend возвращает `next_cursor` или `has_more`;
- большие сообщения могут отдавать `truncated=true` и `full_message_available=true`, если UI не должен сразу грузить полный текст;
- backend не отдаёт всю историю без лимита.

**Зависимости:**
- `agent_dialog_message` storage;
- индексы по `session_id`, `created_at` или sequence.

### BE-FR-5. Лимиты длины и размера

**Описание:**
Backend должен централизованно ограничивать размер входного prompt, ответа RAIN и страницы истории.

**Правила и ограничения:**
- `message_max_chars` конфигурируемый, рекомендуемый MVP default `8000`;
- `agent_response_max_chars` конфигурируемый, рекомендуемый MVP default `50000`;
- `history_page_max_messages` конфигурируемый, рекомендуемый max `50`;
- при превышении `message_max_chars` возвращается `400 message_too_long`;
- если `response` RAIN превышает лимит, backend сохраняет ошибку или усечённое сообщение только по явно согласованному правилу; silent truncation запрещён;
- лимиты должны быть возвращаемы frontend через config/status endpoint или синхронизированы в deployment config.

**Зависимости:**
- frontend validation;
- storage capacity.

### BE-FR-6. Timeout и retry policy

**Описание:**
Backend должен иметь явную политику timeout для долгого вызова RAIN.

**Правила и ограничения:**
- server-to-server `POST /chat` имеет hard timeout, рекомендуемый MVP default `180` секунд для диалогового взаимодействия;
- для сценария создания БТ hard timeout может быть больше только после согласования SLA с RAIN, так как в системных требованиях нет значения от подтверждения до ссылки;
- при timeout run получает terminal status `timeout`;
- автоматический retry `POST /chat` запрещён для сообщений, которые могли привести к созданию БТ, пока RAIN не предоставит идемпотентный ключ или безопасный status endpoint;
- для технических ошибок до передачи запроса в RAIN допускается retry по инфраструктурной политике, но он должен быть прозрачно логирован.

**Зависимости:**
- SLA RAIN;
- бизнес-правила публикации БТ.

## Модель данных

### Основные сущности и поля

| Сущность / таблица | Поле | Тип | Обязательность | Описание |
|---|---|---|---|---|
| `agent_ui_session` | `session_id` | UUID/string | обязательно | идентификатор UI-сессии окна агента |
| `agent_ui_session` | `user_id` | string/UUID | обязательно | пользователь СУДИР |
| `agent_ui_session` | `start_datetime` | timestamp with timezone | обязательно | дата и время первого открытия окна |
| `agent_ui_session` | `status` | string | обязательно | `active`, `restarted`, `closed` |
| `agent_dialog_run` | `run_id` | UUID/string | обязательно | идентификатор async run |
| `agent_dialog_run` | `session_id` | UUID/string | обязательно | ссылка на UI-сессию |
| `agent_dialog_run` | `status` | enum | обязательно | `queued`, `running`, `succeeded`, `failed`, `timeout`, `cancelled` |
| `agent_dialog_run` | `rain_http_status` | integer/null | опционально | статус ответа RAIN |
| `agent_dialog_run` | `error_code` | string/null | опционально | нормализованный код ошибки |
| `agent_dialog_run` | `created_at` / `updated_at` | timestamp | обязательно | контроль polling и timeout |
| `agent_dialog_message` | `message_id` | UUID/string | обязательно | идентификатор сообщения |
| `agent_dialog_message` | `session_id` | UUID/string | обязательно | ссылка на UI-сессию |
| `agent_dialog_message` | `run_id` | UUID/string/null | опционально | run, породивший сообщение |
| `agent_dialog_message` | `role` | enum | обязательно | `user`, `agent`, `system` |
| `agent_dialog_message` | `content` | text | обязательно | текст сообщения |
| `agent_dialog_message` | `content_length` | integer | обязательно | длина сообщения для лимитов |
| `agent_dialog_message` | `created_at` | timestamp | обязательно | порядок истории |

### Инварианты и ограничения

- у одного `session_id` не может быть более одного active run;
- `session_id` принадлежит пользовательской СУДИР-сессии и не должен быть доступен другому пользователю;
- user message сохраняется до запуска RAIN;
- agent message сохраняется только после успешного ответа RAIN;
- история отдаётся только с `limit`;
- silent truncation ответа агента запрещён без явного признака `truncated`.

### Индексы / уникальности / FK

- уникальный индекс по `run_id`;
- индекс active run по `session_id`, `status`;
- индекс истории по `session_id`, `created_at` или sequence;
- уникальность `session_id` в рамках пользователя или пользовательской СУДИР-сессии.

## API-контракт

### Эндпоинты

| Метод и маршрут | Назначение | Кто вызывает | Примечание |
|---|---|---|---|
| `POST /dialog/{session_id}/message` | создать async run отправки сообщения | frontend agent window | возвращает `202 { run_id }` |
| `GET /dialog/{session_id}/runs/{run_id}` | получить статус run | frontend polling | terminal statuses: `succeeded`, `failed`, `timeout`, `cancelled` |
| `GET /dialog/{session_id}/messages` | получить страницу истории | frontend agent window | параметры `limit`, `before` |
| `POST RAIN /chat` | отправить сообщение агенту | backend АС КОДА | server-to-server по `agent_openapi.yaml` |

### OpenAPI fragment

```yaml
openapi: 3.0.3
info:
  title: Agent Dialog Async Facade API
  version: 1.0.0
paths:
  /dialog/{session_id}/message:
    post:
      summary: Создать async run отправки сообщения агенту
      parameters:
        - in: path
          name: session_id
          required: true
          schema:
            type: string
            format: uuid
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [message]
              properties:
                message:
                  type: string
                  maxLength: 8000
                simulation_id:
                  type: string
                  nullable: true
                mode:
                  type: string
                  enum: [consultation, bt_creation]
                  nullable: true
      responses:
        "202":
          description: Run создан
          content:
            application/json:
              schema:
                type: object
                required: [run_id, status]
                properties:
                  run_id:
                    type: string
                    format: uuid
                  status:
                    type: string
                    example: queued
        "400":
          description: Ошибка валидации
        "409":
          description: По session_id уже есть активный run
        "503":
          description: Агент не готов
  /dialog/{session_id}/runs/{run_id}:
    get:
      summary: Получить статус async run
      parameters:
        - in: path
          name: session_id
          required: true
          schema:
            type: string
            format: uuid
        - in: path
          name: run_id
          required: true
          schema:
            type: string
            format: uuid
      responses:
        "200":
          description: Состояние run
          content:
            application/json:
              schema:
                type: object
                required: [run_id, status]
                properties:
                  run_id:
                    type: string
                  status:
                    type: string
                    enum: [queued, running, succeeded, failed, timeout, cancelled]
                  message_id:
                    type: string
                    nullable: true
                  error_code:
                    type: string
                    nullable: true
                  error_message:
                    type: string
                    nullable: true
  /dialog/{session_id}/messages:
    get:
      summary: Получить страницу истории диалога
      parameters:
        - in: path
          name: session_id
          required: true
          schema:
            type: string
            format: uuid
        - in: query
          name: limit
          schema:
            type: integer
            default: 20
            maximum: 50
        - in: query
          name: before
          schema:
            type: string
      responses:
        "200":
          description: Страница сообщений
components: {}
```

### Примеры запросов и ответов

#### Пример 1. Создание run

```http
POST /dialog/a1b2c3d4-e5f6-7890-abcd-ef1234567890/message HTTP/1.1
Content-Type: application/json
```

```json
{
  "message": "Сформируй БТ по этой симуляции.",
  "simulation_id": "SIM-CC-148",
  "mode": "bt_creation"
}
```

```json
{
  "run_id": "7e1d4c3c-7ac0-41dd-a69d-7320f7f29a51",
  "status": "queued"
}
```

#### Пример 2. Server-to-server вызов RAIN

```http
POST /chat HTTP/1.1
Content-Type: application/json
```

```json
{
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "message": "Сформируй БТ по этой симуляции.",
  "risk_params": {
    "as_is": {
      "PD_LIMIT": "0.38"
    },
    "to_be": {
      "PD_LIMIT": "0.42"
    }
  },
  "simulation_id": "SIM-CC-148",
  "start_datetime": "2026-04-29T12:30:00.123+03:00",
  "fio": "Иванов Иван Иванович"
}
```

```json
{
  "response": "Страница БТ создана: https://confluence.example.local/pages/viewpage.action?pageId=12345"
}
```

#### Пример 3. Polling terminal status

```http
GET /dialog/a1b2c3d4-e5f6-7890-abcd-ef1234567890/runs/7e1d4c3c-7ac0-41dd-a69d-7320f7f29a51 HTTP/1.1
```

```json
{
  "run_id": "7e1d4c3c-7ac0-41dd-a69d-7320f7f29a51",
  "status": "succeeded",
  "message_id": "msg-1002451"
}
```

#### Пример 4. Страница истории

```http
GET /dialog/a1b2c3d4-e5f6-7890-abcd-ef1234567890/messages?limit=20 HTTP/1.1
```

```json
{
  "items": [
    {
      "message_id": "msg-1002450",
      "role": "user",
      "content": "Сформируй БТ по этой симуляции.",
      "created_at": "2026-04-29T12:30:03.000+03:00"
    },
    {
      "message_id": "msg-1002451",
      "role": "agent",
      "content": "Страница БТ создана: https://confluence.example.local/pages/viewpage.action?pageId=12345",
      "created_at": "2026-04-29T12:31:40.000+03:00"
    }
  ],
  "next_cursor": null,
  "has_more": false
}
```

## Интеграции, вычисления и фоновые процессы

- Внешние системы: AI-агент RAIN, existing simulation detail API;
- Асинхронные процессы: worker/background task вызова RAIN `/chat`;
- Вычисление статусов / derived fields: `run.status`, `has_active_run`, `has_more`;
- Идемпотентность / ретраи: автоматический retry `POST /chat` для БТ запрещён без идемпотентности RAIN.

## Ошибки и валидация

### Валидационные правила

- `session_id` обязателен и валиден;
- `message` обязателен, непустой и не длиннее `message_max_chars`;
- `start_datetime` хранится в UI-сессии и передаётся в RAIN в формате ISO 8601;
- `fio` берётся из СУДИР-профиля пользователя;
- нельзя создать второй active run по тому же `session_id`;
- polling чужого `run_id` запрещён;
- история без `limit` использует безопасный default.

### Ошибки API

| Код/сценарий | Условие | Ответ |
|---|---|---|
| `400 message_empty` | пустой текст | ошибка валидации |
| `400 message_too_long` | prompt превышает лимит | ошибка валидации с текущим лимитом |
| `404 session_not_found` | `session_id` не найден или не принадлежит пользователю | ошибка отсутствующей сессии |
| `404 run_not_found` | `run_id` не найден в сессии | ошибка отсутствующего run |
| `409 run_in_progress` | уже есть active run | конфликт |
| `503 agent_not_ready` | RAIN readiness не готов | временная недоступность |
| `504 agent_timeout` | RAIN не ответил в hard timeout | terminal status `timeout` |
| `502 agent_error` | RAIN вернул ошибку или некорректный ответ | terminal status `failed` |

## Миграция и обратная совместимость

- Нужны ли миграции данных: да, если история и run status хранятся в постоянном backend-хранилище АС КОДА.
- Нужен ли backfill: нет.
- Есть ли риски для текущего baseline: да, прежняя модель прямого синхронного ответа заменяется async facade над RAIN `/chat`.
- Что должно попасть в release finalization: async contract, лимиты, timeout policy, health/status behavior и правила хранения истории.

## Observability и аудит

- Логи: создание run, вызов RAIN, terminal status, timeout, error_code, `session_id`, `run_id`;
- Метрики: run duration, success/failure/timeout rate, readiness state, средний размер prompt/response, количество сообщений в истории;
- Audit trail: обычные сообщения технически логируются, бизнес-аудит публикации БТ фиксируется в slice `bt-publication`.

## Критерии приемки

### BE-AC-1. Async facade
- [ ] `POST /message` возвращает `202 { run_id }` без ожидания полного ответа RAIN
- [ ] Backend вызывает RAIN `/chat` в фоне
- [ ] Polling endpoint возвращает terminal status
- [ ] Active run lock не позволяет создать второй run в той же сессии

### BE-AC-2. История и лимиты
- [ ] User message и agent response сохраняются в истории АС КОДА
- [ ] История отдаётся только страницами с `limit`
- [ ] Backend отклоняет prompt длиннее configured limit
- [ ] Backend не отдаёт всю историю без pagination

### BE-AC-3. Timeout и ошибки
- [ ] При timeout RAIN run получает terminal status `timeout`
- [ ] Ошибки RAIN нормализуются для UI
- [ ] Автоматический retry не выполняется для БТ без идемпотентности

## Открытые вопросы и допущения

- Значения `message_max_chars`, `agent_response_max_chars` и hard timeout должны быть подтверждены с командами RAIN и эксплуатации.
- Требуется отдельно решить, нужен ли RAIN структурированный `btUrl` в ответе вместо извлечения URL из строки `response`.
