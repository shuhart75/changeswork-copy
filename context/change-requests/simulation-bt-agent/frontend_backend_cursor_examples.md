# Примеры обмена FE -> BE для `simulation-bt-agent` с использованием `cursor`

Дата: `2026-05-04`

## Назначение

Показать на конкретных HTTP-примерах, как frontend АС КОДА работает с backend АС КОДА при:

- первичной загрузке последних сообщений;
- прокрутке истории вверх;
- возврате вниз внутри уже загруженного окна;
- появлении нового сообщения, пока пользователь читает старую историю;
- возврате к самому последнему сообщению.

## Ключевая идея `cursor`

- `older_cursor` возвращает backend в ответе на `GET /dialog/messages`.
- `sync_cursor` возвращает backend в ответе на `GET /dialog/messages` и отражает актуальный хвост истории.
- frontend не интерпретирует `cursor`, а хранит его как opaque token.
- для загрузки более ранней истории frontend передаёт `before=<older_cursor>`.
- для вычисления `history_changed` frontend передаёт `known_sync_cursor=<sync_cursor>` в `GET /dialog/status`; backend не хранит, какую историю уже видел frontend.
- для возврата к последним сообщениям frontend не использует старый `cursor`, а делает новый запрос без `before`:
  `GET /dialog/messages?session_id=...&limit=20`

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
    { "message_id": "msg-181", "role": "user",  "content": "Сообщение 181", "created_at": "2026-05-04T10:00:01+03:00" },
    { "message_id": "msg-182", "role": "assistant", "content": "Ответ 182", "created_at": "2026-05-04T10:00:05+03:00" },
    { "message_id": "msg-183", "role": "user",  "content": "Сообщение 183", "created_at": "2026-05-04T10:01:01+03:00" },
    { "message_id": "msg-184", "role": "assistant", "content": "Ответ 184", "created_at": "2026-05-04T10:01:08+03:00" },
    { "message_id": "msg-185", "role": "user",  "content": "Сообщение 185", "created_at": "2026-05-04T10:02:01+03:00" },
    { "message_id": "msg-186", "role": "assistant", "content": "Ответ 186", "created_at": "2026-05-04T10:02:09+03:00" },
    { "message_id": "msg-187", "role": "user",  "content": "Сообщение 187", "created_at": "2026-05-04T10:03:01+03:00" },
    { "message_id": "msg-188", "role": "assistant", "content": "Ответ 188", "created_at": "2026-05-04T10:03:07+03:00" },
    { "message_id": "msg-189", "role": "user",  "content": "Сообщение 189", "created_at": "2026-05-04T10:04:01+03:00" },
    { "message_id": "msg-190", "role": "assistant", "content": "Ответ 190", "created_at": "2026-05-04T10:04:06+03:00" },
    { "message_id": "msg-191", "role": "user",  "content": "Сообщение 191", "created_at": "2026-05-04T10:05:01+03:00" },
    { "message_id": "msg-192", "role": "assistant", "content": "Ответ 192", "created_at": "2026-05-04T10:05:06+03:00" },
    { "message_id": "msg-193", "role": "user",  "content": "Сообщение 193", "created_at": "2026-05-04T10:06:01+03:00" },
    { "message_id": "msg-194", "role": "assistant", "content": "Ответ 194", "created_at": "2026-05-04T10:06:08+03:00" },
    { "message_id": "msg-195", "role": "user",  "content": "Сообщение 195", "created_at": "2026-05-04T10:07:01+03:00" },
    { "message_id": "msg-196", "role": "assistant", "content": "Ответ 196", "created_at": "2026-05-04T10:07:06+03:00" },
    { "message_id": "msg-197", "role": "user",  "content": "Сообщение 197", "created_at": "2026-05-04T10:08:01+03:00" },
    { "message_id": "msg-198", "role": "assistant", "content": "Ответ 198", "created_at": "2026-05-04T10:08:06+03:00" },
    { "message_id": "msg-199", "role": "user",  "content": "Сообщение 199", "created_at": "2026-05-04T10:09:01+03:00" },
    { "message_id": "msg-200", "role": "assistant", "content": "Ответ 200", "created_at": "2026-05-04T10:09:07+03:00" }
  ],
  "older_cursor": "cur_older_180_7YpQaL",
  "sync_cursor": "cur_sync_200_Gh8nPx",
  "last_message_id": "msg-200",
  "last_message_seq": 200,
  "history_version": "hv-20260504-000200",
  "has_more_before": true
}
```

Frontend сохраняет:

- `session_id = sess-7f7d2d4e-5b6f-4a38-9e13-7c1b8a7d0011`
- `older_cursor = cur_older_180_7YpQaL`
- `sync_cursor = cur_sync_200_Gh8nPx`

## Пример 2. Пользователь прокручивает историю вверх

```http
GET /dialog/messages?session_id=sess-7f7d2d4e-5b6f-4a38-9e13-7c1b8a7d0011&limit=20&before=cur_older_180_7YpQaL HTTP/1.1
```

```json
{
  "items": [
    { "message_id": "msg-161", "role": "user",  "content": "Сообщение 161", "created_at": "2026-05-04T09:50:01+03:00" },
    { "message_id": "msg-162", "role": "assistant", "content": "Ответ 162", "created_at": "2026-05-04T09:50:06+03:00" },
    { "message_id": "msg-163", "role": "user",  "content": "Сообщение 163", "created_at": "2026-05-04T09:51:01+03:00" },
    { "message_id": "msg-164", "role": "assistant", "content": "Ответ 164", "created_at": "2026-05-04T09:51:06+03:00" },
    { "message_id": "msg-165", "role": "user",  "content": "Сообщение 165", "created_at": "2026-05-04T09:52:01+03:00" },
    { "message_id": "msg-166", "role": "assistant", "content": "Ответ 166", "created_at": "2026-05-04T09:52:06+03:00" },
    { "message_id": "msg-167", "role": "user",  "content": "Сообщение 167", "created_at": "2026-05-04T09:53:01+03:00" },
    { "message_id": "msg-168", "role": "assistant", "content": "Ответ 168", "created_at": "2026-05-04T09:53:07+03:00" },
    { "message_id": "msg-169", "role": "user",  "content": "Сообщение 169", "created_at": "2026-05-04T09:54:01+03:00" },
    { "message_id": "msg-170", "role": "assistant", "content": "Ответ 170", "created_at": "2026-05-04T09:54:06+03:00" },
    { "message_id": "msg-171", "role": "user",  "content": "Сообщение 171", "created_at": "2026-05-04T09:55:01+03:00" },
    { "message_id": "msg-172", "role": "assistant", "content": "Ответ 172", "created_at": "2026-05-04T09:55:06+03:00" },
    { "message_id": "msg-173", "role": "user",  "content": "Сообщение 173", "created_at": "2026-05-04T09:56:01+03:00" },
    { "message_id": "msg-174", "role": "assistant", "content": "Ответ 174", "created_at": "2026-05-04T09:56:06+03:00" },
    { "message_id": "msg-175", "role": "user",  "content": "Сообщение 175", "created_at": "2026-05-04T09:57:01+03:00" },
    { "message_id": "msg-176", "role": "assistant", "content": "Ответ 176", "created_at": "2026-05-04T09:57:06+03:00" },
    { "message_id": "msg-177", "role": "user",  "content": "Сообщение 177", "created_at": "2026-05-04T09:58:01+03:00" },
    { "message_id": "msg-178", "role": "assistant", "content": "Ответ 178", "created_at": "2026-05-04T09:58:06+03:00" },
    { "message_id": "msg-179", "role": "user",  "content": "Сообщение 179", "created_at": "2026-05-04T09:59:01+03:00" },
    { "message_id": "msg-180", "role": "assistant", "content": "Ответ 180", "created_at": "2026-05-04T09:59:06+03:00" }
  ],
  "older_cursor": "cur_older_160_aB91Zm",
  "sync_cursor": "cur_sync_200_Gh8nPx",
  "last_message_id": "msg-200",
  "last_message_seq": 200,
  "history_version": "hv-20260504-000200",
  "has_more_before": true
}
```

Frontend:

- добавляет новую страницу в начало `history window`;
- сохраняет текущий `scroll-position`;
- обновляет `older_cursor`.

## Пример 3. Пользователь уходит ещё дальше в прошлое

```http
GET /dialog/messages?session_id=sess-7f7d2d4e-5b6f-4a38-9e13-7c1b8a7d0011&limit=20&before=cur_older_160_aB91Zm HTTP/1.1
```

```json
{
  "items": [
    { "message_id": "msg-141", "role": "user",  "content": "Сообщение 141", "created_at": "2026-05-04T09:40:01+03:00" },
    { "message_id": "msg-142", "role": "assistant", "content": "Ответ 142", "created_at": "2026-05-04T09:40:06+03:00" },
    { "message_id": "msg-143", "role": "user",  "content": "Сообщение 143", "created_at": "2026-05-04T09:41:01+03:00" },
    { "message_id": "msg-144", "role": "assistant", "content": "Ответ 144", "created_at": "2026-05-04T09:41:06+03:00" },
    { "message_id": "msg-145", "role": "user",  "content": "Сообщение 145", "created_at": "2026-05-04T09:42:01+03:00" },
    { "message_id": "msg-146", "role": "assistant", "content": "Ответ 146", "created_at": "2026-05-04T09:42:06+03:00" },
    { "message_id": "msg-147", "role": "user",  "content": "Сообщение 147", "created_at": "2026-05-04T09:43:01+03:00" },
    { "message_id": "msg-148", "role": "assistant", "content": "Ответ 148", "created_at": "2026-05-04T09:43:06+03:00" },
    { "message_id": "msg-149", "role": "user",  "content": "Сообщение 149", "created_at": "2026-05-04T09:44:01+03:00" },
    { "message_id": "msg-150", "role": "assistant", "content": "Ответ 150", "created_at": "2026-05-04T09:44:06+03:00" },
    { "message_id": "msg-151", "role": "user",  "content": "Сообщение 151", "created_at": "2026-05-04T09:45:01+03:00" },
    { "message_id": "msg-152", "role": "assistant", "content": "Ответ 152", "created_at": "2026-05-04T09:45:06+03:00" },
    { "message_id": "msg-153", "role": "user",  "content": "Сообщение 153", "created_at": "2026-05-04T09:46:01+03:00" },
    { "message_id": "msg-154", "role": "assistant", "content": "Ответ 154", "created_at": "2026-05-04T09:46:06+03:00" },
    { "message_id": "msg-155", "role": "user",  "content": "Сообщение 155", "created_at": "2026-05-04T09:47:01+03:00" },
    { "message_id": "msg-156", "role": "assistant", "content": "Ответ 156", "created_at": "2026-05-04T09:47:06+03:00" },
    { "message_id": "msg-157", "role": "user",  "content": "Сообщение 157", "created_at": "2026-05-04T09:48:01+03:00" },
    { "message_id": "msg-158", "role": "assistant", "content": "Ответ 158", "created_at": "2026-05-04T09:48:06+03:00" },
    { "message_id": "msg-159", "role": "user",  "content": "Сообщение 159", "created_at": "2026-05-04T09:49:01+03:00" },
    { "message_id": "msg-160", "role": "assistant", "content": "Ответ 160", "created_at": "2026-05-04T09:49:06+03:00" }
  ],
  "older_cursor": "cur_older_140_Xk72pQ",
  "sync_cursor": "cur_sync_200_Gh8nPx",
  "last_message_id": "msg-200",
  "last_message_seq": 200,
  "history_version": "hv-20260504-000200",
  "has_more_before": true
}
```

## Пример 4. Пользователь скроллит вниз внутри уже загруженного окна

Дополнительных HTTP-вызовов не требуется.

Frontend двигается вниз локально в пределах уже загруженного `history window`, например по диапазону сообщений `141..200`.

## Пример 5. Появилось новое сообщение, пока пользователь читает старую историю

Frontend узнаёт об этом через polling status endpoint:

```http
GET /dialog/status?session_id=sess-7f7d2d4e-5b6f-4a38-9e13-7c1b8a7d0011&known_sync_cursor=cur_sync_200_Gh8nPx HTTP/1.1
```

```json
{
  "session_id": "sess-7f7d2d4e-5b6f-4a38-9e13-7c1b8a7d0011",
  "can_send_message": true,
  "dialog_status": "succeeded",
  "history_changed": true,
  "error": null
}
```

Что делает frontend:

- не меняет текущий `scroll-position`;
- не прыгает вниз автоматически;
- показывает sticky-индикатор `Новое сообщение`.

## Пример 6. Пользователь возвращается к самому последнему сообщению

Для этого frontend не использует старый `older_cursor`, а повторно запрашивает latest page:

```http
GET /dialog/messages?session_id=sess-7f7d2d4e-5b6f-4a38-9e13-7c1b8a7d0011&limit=20 HTTP/1.1
```

```json
{
  "items": [
    { "message_id": "msg-182", "role": "assistant", "content": "Ответ 182", "created_at": "2026-05-04T10:00:05+03:00" },
    { "message_id": "msg-183", "role": "user",  "content": "Сообщение 183", "created_at": "2026-05-04T10:01:01+03:00" },
    { "message_id": "msg-184", "role": "assistant", "content": "Ответ 184", "created_at": "2026-05-04T10:01:08+03:00" },
    { "message_id": "msg-185", "role": "user",  "content": "Сообщение 185", "created_at": "2026-05-04T10:02:01+03:00" },
    { "message_id": "msg-186", "role": "assistant", "content": "Ответ 186", "created_at": "2026-05-04T10:02:09+03:00" },
    { "message_id": "msg-187", "role": "user",  "content": "Сообщение 187", "created_at": "2026-05-04T10:03:01+03:00" },
    { "message_id": "msg-188", "role": "assistant", "content": "Ответ 188", "created_at": "2026-05-04T10:03:07+03:00" },
    { "message_id": "msg-189", "role": "user",  "content": "Сообщение 189", "created_at": "2026-05-04T10:04:01+03:00" },
    { "message_id": "msg-190", "role": "assistant", "content": "Ответ 190", "created_at": "2026-05-04T10:04:06+03:00" },
    { "message_id": "msg-191", "role": "user",  "content": "Сообщение 191", "created_at": "2026-05-04T10:05:01+03:00" },
    { "message_id": "msg-192", "role": "assistant", "content": "Ответ 192", "created_at": "2026-05-04T10:05:06+03:00" },
    { "message_id": "msg-193", "role": "user",  "content": "Сообщение 193", "created_at": "2026-05-04T10:06:01+03:00" },
    { "message_id": "msg-194", "role": "assistant", "content": "Ответ 194", "created_at": "2026-05-04T10:06:08+03:00" },
    { "message_id": "msg-195", "role": "user",  "content": "Сообщение 195", "created_at": "2026-05-04T10:07:01+03:00" },
    { "message_id": "msg-196", "role": "assistant", "content": "Ответ 196", "created_at": "2026-05-04T10:07:06+03:00" },
    { "message_id": "msg-197", "role": "user",  "content": "Сообщение 197", "created_at": "2026-05-04T10:08:01+03:00" },
    { "message_id": "msg-198", "role": "assistant", "content": "Ответ 198", "created_at": "2026-05-04T10:08:06+03:00" },
    { "message_id": "msg-199", "role": "user",  "content": "Сообщение 199", "created_at": "2026-05-04T10:09:01+03:00" },
    { "message_id": "msg-200", "role": "assistant", "content": "Ответ 200", "created_at": "2026-05-04T10:09:07+03:00" },
    { "message_id": "msg-201", "role": "assistant", "content": "Новый ответ агента 201", "created_at": "2026-05-04T10:10:15+03:00" }
  ],
  "older_cursor": "cur_older_181_Bh2kLm",
  "sync_cursor": "cur_sync_201_Wk4rTs",
  "last_message_id": "msg-201",
  "last_message_seq": 201,
  "history_version": "hv-20260504-000201",
  "has_more_before": true
}
```

Что делает frontend:

- заменяет текущее окно истории на latest page;
- сохраняет новый `sync_cursor = cur_sync_201_Wk4rTs`;
- скрывает индикатор `Новое сообщение`;
- прокручивает список вниз к `msg-201`.

## Итого

### Когда нужен `cursor`

Только для движения в прошлое:

```http
GET /dialog/messages?session_id=...&limit=20&before=<older_cursor>
```

### Когда `cursor` не нужен

Когда нужно получить актуальный хвост диалога:

```http
GET /dialog/messages?session_id=...&limit=20
```

## Практическое правило для frontend

1. При открытии панели загружать latest page.
2. При прокрутке вверх догружать историю через `before=older_cursor`.
3. При движении вниз внутри уже загруженного окна не делать HTTP-вызовов.
4. При polling передавать `known_sync_cursor`; если backend вернул `history_changed=true` и пользователь не внизу, показывать индикатор нового сообщения.
5. При нажатии на индикатор заново загружать latest page без `before`.
