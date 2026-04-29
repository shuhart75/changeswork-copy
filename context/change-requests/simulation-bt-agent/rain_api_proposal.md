# Предложения по REST API AI-агента RAIN для интеграции с АС КОДА

Дата: `2026-04-29`

## Цель документа

Предложить альтернативный REST-контракт RAIN, который:

- не требует держать долгий браузерный или межсервисный HTTP-запрос до полного ответа агента;
- позволяет АС КОДА показывать понятные статусы ожидания;
- безопасно обрабатывает долгие SLA агента;
- не требует передавать всю историю диалога в каждом сообщении;
- даёт структурированный результат создания БТ, включая ссылку на страницу;
- поддерживает идемпотентность для операций с побочными эффектами.

## Текущий контракт и проблема

Текущий `agent_openapi.yaml` содержит:

- `GET /health/liveness`;
- `GET /health/readiness`;
- `POST /chat`.

`POST /chat` является синхронным:

```text
АС КОДА -> RAIN: POST /chat
RAIN -> АС КОДА: 200 { response }
```

Проблемы для АС КОДА:

- по SLA диалоговое взаимодействие может занимать около `91.6 + 69.2` секунд;
- создание БТ от подтверждения до ссылки пока не имеет подтверждённого SLA;
- при долгом синхронном вызове сложно отличить “агент работает” от “запрос завис”;
- при timeout непонятно, был ли создан БТ;
- ответ содержит только строковое поле `response`, отдельного `btUrl` нет;
- если агент не хранит состояние диалога, возникает риск передавать всю историю в каждом сообщении, что плохо масштабируется.

## Рекомендуемый вариант: async REST API на стороне RAIN

Вместо синхронного `/chat` предлагается ввести модель `run`.

```text
POST /chat/runs
GET  /chat/runs/{run_id}
GET  /chat/runs/{run_id}/result
GET  /chat/sessions/{session_id}/messages
```

Ключевая идея:

- АС КОДА отправляет новое сообщение и получает `run_id`;
- RAIN обрабатывает сообщение асинхронно;
- АС КОДА polling-ом читает статус `run`;
- результат забирается отдельно;
- история диалога читается страницами, а не передаётся целиком в каждом сообщении.

## Health endpoints

Текущие health endpoints стоит сохранить.

### `GET /health/liveness`

Назначение: проверить, что сервис RAIN жив как процесс.

Пример ответа:

```json
{
  "status": "alive"
}
```

### `GET /health/readiness`

Назначение: проверить, что RAIN готов принимать новые сообщения/runs.

Пример успешного ответа:

```json
{
  "status": "ready"
}
```

Пример неготовности:

```json
{
  "status": "not_ready",
  "reason": "model_initializing"
}
```

АС КОДА использует readiness для status chip и блокировки отправки сообщений.

## Сессия диалога

### Вариант A, предпочтительный: RAIN хранит состояние и историю диалога

RAIN принимает `session_id` от АС КОДА и хранит по нему:

- историю сообщений;
- внутренний контекст агента;
- активные или завершённые runs;
- артефакты, созданные в ходе диалога.

АС КОДА не отправляет всю историю в каждом сообщении. Она отправляет только:

- `session_id`;
- новое сообщение пользователя;
- текущий бизнес-контекст, если он нужен для данного сообщения.

### `PUT /chat/sessions/{session_id}`

Идемпотентно создать или восстановить сессию.

```http
PUT /chat/sessions/a1b2c3d4-e5f6-7890-abcd-ef1234567890
Content-Type: application/json
```

```json
{
  "start_datetime": "2026-04-29T12:30:00.123+03:00",
  "fio": "Иванов Иван Иванович",
  "source_system": "AS_KODA",
  "product": "credit_cards"
}
```

Ответ:

```json
{
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "status": "active",
  "created": false
}
```

Если команда RAIN не хочет отдельный endpoint сессии, допустимо создавать сессию лениво при первом `POST /chat/runs`.

## Создание run

### `POST /chat/runs`

Создать асинхронную операцию обработки одного сообщения.

Обязательные требования:

- поддержать `Idempotency-Key`;
- возвращать `202 Accepted`;
- возвращать `Location` на созданный run;
- не создавать второй run при повторе того же `Idempotency-Key`.

```http
POST /chat/runs
Content-Type: application/json
Idempotency-Key: 3bdb8f6e-c9e1-46d0-b469-327d4b6fd0f8
```

```json
{
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "message": "Сформируй БТ по симуляции SIM-CC-148.",
  "mode": "bt_creation",
  "simulation_id": "SIM-CC-148",
  "risk_params": {
    "as_is": {
      "PD_LIMIT": "0.38",
      "UTIL_SEGMENT_CAP": "98000"
    },
    "to_be": {
      "PD_LIMIT": "0.42",
      "UTIL_SEGMENT_CAP": "125000"
    }
  },
  "start_datetime": "2026-04-29T12:30:00.123+03:00",
  "fio": "Иванов Иван Иванович"
}
```

Ответ:

```http
202 Accepted
Location: /chat/runs/run-123
Retry-After: 5
```

```json
{
  "run_id": "run-123",
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "status": "queued",
  "retry_after_seconds": 5
}
```

## Статусы run

### `GET /chat/runs/{run_id}`

Получить состояние run.

```http
GET /chat/runs/run-123
```

Пока выполняется:

```json
{
  "run_id": "run-123",
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "status": "running",
  "created_at": "2026-04-29T12:30:00.123+03:00",
  "updated_at": "2026-04-29T12:30:20.000+03:00",
  "retry_after_seconds": 5
}
```

Успех:

```json
{
  "run_id": "run-123",
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "status": "succeeded",
  "result_url": "/chat/runs/run-123/result",
  "message_id": "msg-789"
}
```

Ошибка:

```json
{
  "run_id": "run-123",
  "status": "failed",
  "error": {
    "code": "agent_error",
    "message": "Не удалось сформировать ответ"
  }
}
```

Timeout:

```json
{
  "run_id": "run-123",
  "status": "timeout",
  "error": {
    "code": "generation_timeout",
    "message": "Ответ не был сформирован за отведённое время"
  }
}
```

Минимальный набор статусов:

- `queued`;
- `running`;
- `succeeded`;
- `failed`;
- `timeout`;
- `cancelled`.

Желательный расширенный набор:

- `waiting_user_input` — агент ожидает уточнение пользователя;
- `waiting_confirmation` — агент ожидает подтверждение создания БТ.

## Результат run

### `GET /chat/runs/{run_id}/result`

Получить результат завершённого run.

```http
GET /chat/runs/run-123/result
```

Ответ:

```json
{
  "run_id": "run-123",
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "message": {
    "message_id": "msg-789",
    "role": "assistant",
    "content": "Страница БТ создана: https://confluence.example.local/pages/viewpage.action?pageId=12345",
    "created_at": "2026-04-29T12:31:40.000+03:00"
  },
  "artifacts": [
    {
      "type": "bt_page",
      "url": "https://confluence.example.local/pages/viewpage.action?pageId=12345",
      "title": "БТ SIM-CC-148"
    }
  ]
}
```

Для АС КОДА критично, чтобы ссылка на БТ была структурированной:

```json
{
  "type": "bt_page",
  "url": "https://...",
  "title": "..."
}
```

Текстовое поле `response` можно оставить для отображения пользователю, но не использовать как единственный источник ссылки.

## История сообщений

### Почему не передавать всю историю в каждом сообщении

Передача всей истории в каждом `POST /chat` плоха по нескольким причинам:

- растёт размер каждого запроса;
- ухудшается latency;
- повышается риск превышения лимитов gateway/model context;
- сложнее защищать персональные данные и аудит;
- при длинном диалоге frontend и backend начинают таскать лишние данные;
- появляется риск рассинхронизации клиентской копии истории и состояния агента.

Поэтому история должна храниться у владельца диалога и читаться страницами.

### Предпочтительная модель истории

RAIN хранит историю по `session_id`, а АС КОДА при необходимости получает её порциями.

```text
GET /chat/sessions/{session_id}/messages?limit=20
GET /chat/sessions/{session_id}/messages?limit=20&before=cursor-abc
```

### `GET /chat/sessions/{session_id}/messages`

Получить страницу истории сообщений.

Параметры:

- `limit` — размер страницы, default `20`, max `50`;
- `before` — cursor для загрузки более ранних сообщений;
- `after` — cursor для загрузки новых сообщений, если нужен incremental sync.

```http
GET /chat/sessions/a1b2c3d4-e5f6-7890-abcd-ef1234567890/messages?limit=20
```

Ответ:

```json
{
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "items": [
    {
      "message_id": "msg-101",
      "role": "user",
      "content": "Сформируй БТ по симуляции SIM-CC-148.",
      "created_at": "2026-04-29T12:30:03.000+03:00"
    },
    {
      "message_id": "msg-102",
      "role": "assistant",
      "content": "Уточните бизнес-эффект для БТ.",
      "created_at": "2026-04-29T12:30:40.000+03:00"
    }
  ],
  "next_cursor": "cursor-older-001",
  "has_more": true
}
```

Для больших сообщений желательно поддержать:

```json
{
  "message_id": "msg-200",
  "role": "assistant",
  "content": "первые N символов...",
  "truncated": true,
  "full_content_url": "/chat/messages/msg-200"
}
```

### `GET /chat/messages/{message_id}`

Получить одно большое сообщение целиком.

```http
GET /chat/messages/msg-200
```

Ответ:

```json
{
  "message_id": "msg-200",
  "role": "assistant",
  "content": "полный текст длинного ответа...",
  "created_at": "2026-04-29T12:35:00.000+03:00"
}
```

## Если RAIN не может хранить историю

Если RAIN принципиально не хранит историю, нужен один из двух fallback-вариантов.

### Fallback B1: историю хранит АС КОДА, RAIN возвращает opaque state token

RAIN не хранит всю историю, но возвращает непрозрачный токен состояния:

```json
{
  "response": "Ответ агента...",
  "conversation_state_token": "opaque-token"
}
```

Следующий запрос содержит:

```json
{
  "session_id": "...",
  "message": "Новое сообщение",
  "conversation_state_token": "opaque-token"
}
```

Плюсы:

- не нужно отправлять всю историю;
- RAIN может восстановить внутренний контекст по compact state.

Минусы:

- токен может быть большим;
- нужно управлять TTL и совместимостью токена;
- история для UI всё равно хранится в АС КОДА.

### Fallback B2: историю хранит только АС КОДА, RAIN получает только новое сообщение и текущий бизнес-контекст

В этом варианте RAIN должен уметь отвечать без полной истории, используя:

- новое сообщение пользователя;
- `session_id`;
- текущий бизнес-контекст;
- `risk_params`;
- `simulation_id`;
- `fio`;
- `start_datetime`.

Минус: агент может терять диалоговый контекст, если он не хранится ни у RAIN, ни в state token.

Этот вариант хуже для настоящего диалога и подходит только для простых одношаговых запросов.

## Идемпотентность

Для создания БТ идемпотентность обязательна.

АС КОДА должна передавать:

```http
Idempotency-Key: <uuid>
```

Правило RAIN:

- повтор `POST /chat/runs` с тем же `Idempotency-Key` возвращает тот же `run_id`;
- повтор не создаёт вторую страницу БТ;
- ключ должен храниться достаточно долго, чтобы пережить сетевые повторы и timeout.

Без идемпотентности автоматический retry создания БТ опасен.

## Cancel endpoint

Желательно, но можно отложить после MVP.

```http
POST /chat/runs/{run_id}/cancel
```

Ответ:

```json
{
  "run_id": "run-123",
  "status": "cancelled"
}
```

Если RAIN не может гарантированно отменить уже начатую публикацию БТ, endpoint должен явно отвечать:

```json
{
  "run_id": "run-123",
  "status": "cancel_requested",
  "guaranteed": false
}
```

## Ошибки

Рекомендуемый формат ошибки:

```json
{
  "error": {
    "code": "agent_not_ready",
    "message": "Агент временно не готов принимать запросы",
    "retryable": true
  }
}
```

Рекомендуемые коды:

- `invalid_request`;
- `session_not_found`;
- `run_not_found`;
- `agent_not_ready`;
- `generation_timeout`;
- `agent_error`;
- `bt_creation_failed`;
- `idempotency_conflict`;
- `rate_limited`.

## Минимальный набор изменений для MVP

Если RAIN не готов быстро внедрить полный контракт, минимально нужно:

1. `POST /chat/runs` вместо синхронного `POST /chat`.
2. `GET /chat/runs/{run_id}` для статуса.
3. `GET /chat/runs/{run_id}/result` для результата.
4. `Idempotency-Key` для создания БТ.
5. Структурированный `artifacts[]` с `bt_page.url`.
6. Один способ не передавать всю историю:
   - либо RAIN хранит историю и отдаёт `GET /chat/sessions/{session_id}/messages`;
   - либо RAIN возвращает `conversation_state_token`, а UI-историю хранит АС КОДА.

## Рекомендуемая целевая схема

```text
АС КОДА Frontend
  -> АС КОДА Backend
    -> RAIN /health/liveness
    -> RAIN /health/readiness
    -> RAIN /chat/runs
    -> RAIN /chat/runs/{run_id}
    -> RAIN /chat/runs/{run_id}/result
    -> RAIN /chat/sessions/{session_id}/messages
```

Frontend не вызывает RAIN напрямую и не получает OTT. Межсервисная аутентификация `АС КОДА Backend -> RAIN` остаётся через HTTPS/mTLS/OTT.

## Открытые вопросы к команде RAIN

1. Может ли RAIN хранить историю по `session_id` хотя бы в пределах TTL UI-сессии?
2. Если RAIN не хранит историю, может ли он возвращать `conversation_state_token`?
3. Может ли RAIN поддержать `Idempotency-Key` для сценария создания БТ?
4. Может ли RAIN возвращать структурированный `artifacts[]` с `bt_page.url`?
5. Какой hard timeout RAIN рекомендует для обычного диалога и для создания БТ?
6. Какой TTL у run/result/history?
7. Можно ли отменять run, и что означает отмена, если Confluence page уже создаётся?
