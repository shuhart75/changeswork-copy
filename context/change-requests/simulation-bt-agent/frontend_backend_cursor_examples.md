# Примеры обмена FE -> BE для `simulation-bt-agent` с использованием `cursor`

Дата: `2026-05-06`

## Назначение

Показать, как frontend АС КОДА работает с backend АС КОДА при:

- первичной загрузке последних сообщений;
- прокрутке истории вверх;
- завершении active run;
- появлении нового ответа, пока пользователь читает старую историю.

## Ключевая идея

- `history_changed` не используется во frontend/backend API.
- Backend не хранит scroll-position, загруженные страницы frontend или "последнее увиденное" сообщение.
- `older_cursor` возвращает backend в ответе на `GET /dialog/messages`.
- Для загрузки более ранней истории frontend передаёт `before=<older_cursor>`.
- После terminal `dialog_status=succeeded` frontend запрашивает latest page без `before`.
- Если пользователь не внизу истории, frontend сам показывает индикатор `Новое сообщение` после получения latest page.
- Коды ошибок frontend берёт из `response.body.error.code` для HTTP error response или из `DialogSessionView.error.code` для terminal `failed`/`timeout`.

## Пример 0. Открытие панели и получение `session_id`

```http
POST /dialog/session HTTP/1.1
Content-Type: application/json
```

```json
{}
```

```json
{
  "session_id": "sess-7f7d2d4e-5b6f-4a38-9e13-7c1b8a7d0011",
  "can_send_message": true,
  "dialog_status": "idle"
}
```

## Пример 1. Первичная загрузка последних 20 сообщений

```http
GET /dialog/messages?session_id=sess-7f7d2d4e-5b6f-4a38-9e13-7c1b8a7d0011&limit=20 HTTP/1.1
```

```json
{
  "items": [
    { "message_id": "msg-181", "role": "user", "content": "Сообщение 181", "created_at": "2026-05-04T10:00:01+03:00" },
    { "message_id": "msg-182", "role": "assistant", "content": "Ответ 182", "created_at": "2026-05-04T10:00:05+03:00" },
    { "message_id": "msg-199", "role": "user", "content": "Сообщение 199", "created_at": "2026-05-04T10:09:01+03:00" },
    { "message_id": "msg-200", "role": "assistant", "content": "Ответ 200", "created_at": "2026-05-04T10:09:07+03:00" }
  ],
  "older_cursor": "cur_older_180_7YpQaL",
  "has_more_before": true
}
```

Frontend сохраняет `older_cursor` как opaque token.

## Пример 2. Пользователь прокручивает историю вверх

```http
GET /dialog/messages?session_id=sess-7f7d2d4e-5b6f-4a38-9e13-7c1b8a7d0011&limit=20&before=cur_older_180_7YpQaL HTTP/1.1
```

```json
{
  "items": [
    { "message_id": "msg-161", "role": "user", "content": "Сообщение 161", "created_at": "2026-05-04T09:50:01+03:00" },
    { "message_id": "msg-162", "role": "assistant", "content": "Ответ 162", "created_at": "2026-05-04T09:50:06+03:00" },
    { "message_id": "msg-179", "role": "user", "content": "Сообщение 179", "created_at": "2026-05-04T09:59:01+03:00" },
    { "message_id": "msg-180", "role": "assistant", "content": "Ответ 180", "created_at": "2026-05-04T09:59:06+03:00" }
  ],
  "older_cursor": "cur_older_160_aB91Zm",
  "has_more_before": true
}
```

Frontend добавляет страницу в начало `history window` и сохраняет текущий `scroll-position`.

## Пример 3. Active run завершился, пользователь читает старую историю

Frontend узнаёт terminal status через polling:

```http
GET /dialog/status?session_id=sess-7f7d2d4e-5b6f-4a38-9e13-7c1b8a7d0011 HTTP/1.1
```

```json
{
  "session_id": "sess-7f7d2d4e-5b6f-4a38-9e13-7c1b8a7d0011",
  "can_send_message": true,
  "dialog_status": "succeeded",
  "error": null
}
```

После этого frontend запрашивает latest page:

```http
GET /dialog/messages?session_id=sess-7f7d2d4e-5b6f-4a38-9e13-7c1b8a7d0011&limit=20 HTTP/1.1
```

```json
{
  "items": [
    { "message_id": "msg-182", "role": "assistant", "content": "Ответ 182", "created_at": "2026-05-04T10:00:05+03:00" },
    { "message_id": "msg-199", "role": "user", "content": "Сообщение 199", "created_at": "2026-05-04T10:09:01+03:00" },
    { "message_id": "msg-200", "role": "assistant", "content": "Ответ 200", "created_at": "2026-05-04T10:09:07+03:00" },
    { "message_id": "msg-201", "role": "assistant", "content": "Новый ответ агента 201", "created_at": "2026-05-04T10:10:15+03:00" }
  ],
  "older_cursor": "cur_older_181_Bh2kLm",
  "has_more_before": true
}
```

Если пользователь не внизу истории, frontend:

- не меняет текущий `scroll-position`;
- показывает sticky-индикатор `Новое сообщение`;
- по клику на индикатор прокручивает историю к latest page.

## Практическое правило для frontend

1. При открытии панели загружать latest page.
2. При прокрутке вверх догружать историю через `before=older_cursor`.
3. При polling читать только `dialog_status` и `can_send_message`.
4. После terminal `succeeded` загружать latest page без `before`.
5. Индикатор нового сообщения вычислять локально, исходя из позиции scroll и полученной latest page.

## Примеры ошибок для frontend

### Ошибка HTTP response

```http
POST /dialog/message HTTP/1.1
Content-Type: application/json
```

```json
{
  "session_id": "sess-7f7d2d4e-5b6f-4a38-9e13-7c1b8a7d0011",
  "message": ""
}
```

```http
HTTP/1.1 400 Bad Request
Content-Type: application/json
```

```json
{
  "error": {
    "code": "message_empty",
    "message": "Введите сообщение перед отправкой.",
    "retryable": false
  }
}
```

Frontend берёт код из `response.body.error.code`.

### Terminal ошибка run

```http
GET /dialog/status?session_id=sess-7f7d2d4e-5b6f-4a38-9e13-7c1b8a7d0011 HTTP/1.1
```

```json
{
  "session_id": "sess-7f7d2d4e-5b6f-4a38-9e13-7c1b8a7d0011",
  "can_send_message": true,
  "dialog_status": "timeout",
  "error": {
    "code": "generation_timeout",
    "message": "Ответ не был сформирован за отведённое время",
    "retryable": true
  }
}
```

Frontend берёт код из `DialogSessionView.error.code`; backend нормализует его из terminal status/error RAIN.
