# Требования по feature — Формирование БТ из симуляции через AI-агента RAIN

Статус: **draft**
Feature: `features/simulation-bt-agent/feature.md`
Квартал: `2026-Q2`
Дата обновления: `2026-05-07`
Шаблон: `.workflow/templates/requirements/feature-requirements.template.md`

## Оглавление

Используются заголовки до уровня `####`.

## Общий контур feature

- Назначение feature: встроить в интерфейс симуляций окно агента для консультационного диалога и формирования БТ по данным завершённой симуляции.
- Что уже есть в baseline/current: список симуляций, деталка симуляции, вкладки деталки, форма редактирования, данные симуляции и существующая ролевая модель.
- Какая дельта добавляется этой feature: глобальная точка входа в окно агента, правая неблокирующая панель диалога, UI-сессия АС КОДА с backend-managed `session_id`, проксирование принятого async REST API RAIN через backend АС КОДА, polling статуса сессии и текущего run, health-статус агента по `/health/liveness` и `/health/readiness`, действие подготовки БТ, публикация БТ через агента, показ ссылки из ответа агента для ручного копирования, аудит сценария и контроль ограничений длины prompt/истории.
- Какие slice входят в контрольный документ: `agent-entrypoint`, `dialog-session`, `bt-publication`.
- Какой общий feature prototype используется как визуальная база: `features/simulation-bt-agent/prototype.html`.

## Источники и приоритет

1. Принятый целевой контракт RAIN, согласованный с RAIN: `context/change-requests/simulation-bt-agent/agent_openapi_1.yaml`.
2. Предыдущие проектные предложения и исходные материалы: `context/change-requests/simulation-bt-agent/rain_api_proposal.md`, `context/change-requests/simulation-bt-agent/agent_openapi.yaml`.
3. Системные требования и SLA: `context/change-requests/simulation-bt-agent/Системные_требования_для_интеграции_АС_КОДА_и_AI_Агента_RAIN.md`.
4. Existing simulation API: `context/change-requests/simulation-bt-agent/simulations_api.md`.
5. Ранее подготовленные feature/slice artifacts.

Если системные требования, `rain_api_proposal.md` или исходный `agent_openapi.yaml` противоречат принятому `agent_openapi_1.yaml`, для целевой API-интеграции используется `agent_openapi_1.yaml`. Системные требования остаются источником бизнес-сценариев, SLA, ограничений HTTPS/mTLS/OTT и требований к UI-сессии.

## Интеграционное решение MVP

- Frontend АС КОДА не вызывает RAIN напрямую и не получает OTT.
- Backend АС КОДА является `agent integration boundary`: авторизует пользователя, управляет UI-сессией АС КОДА, проксирует RAIN server-to-server по HTTPS/mTLS/OTT и скрывает внутренний контракт агента от браузера.
- Под RAIN в этих требованиях для server-to-server интеграции понимается REST-фасад RAIN. АС КОДА интегрируется с фасадом, а не с внутренним агентом напрямую.
- Ошибки интеграции делятся на ошибки фасада и ошибки агента. Ошибки фасада приходят как обычные HTTP/API errors до принятия run, например validation/authorization/conflict/temporary unavailable; ошибки агента приходят через status фасада как terminal `dialog_status=failed` или `dialog_status=timeout`.
- Если фасад вернул `202 Accepted` на создание run, повторять `POST /chat/runs` нельзя: run уже принят, и АС КОДА дальше только poll-ит фасад по статусу. Retry имеет смысл только для retryable ошибок фасада/transport до принятия run; validation `400` и terminal статусы агента не являются основанием для retry.
- RAIN по принятому целевому контракту предоставляет `GET /health/liveness`, `GET /health/readiness`, `POST /chat/runs`, `GET /chat/runs/{run_id}`, `GET /chat/runs/{run_id}/result`, `GET /chat/sessions/{session_id}/messages` и `GET /chat/messages/{message_id}`.
- Terminal status run принадлежит RAIN. Backend АС КОДА не переводит RAIN run в terminal status, а читает статус RAIN, нормализует его для frontend и может краткоживуще кэшировать состояние для UI.
- Frontend не работает с конкретным `run_id` и не получает объект текущего run в обычном UI-контракте. Backend АС КОДА отдаёт session-level view по `GET /dialog/status?session_id=...`, потому что в одной `session_id` допускается только один active run.
- `session_id` создаётся и валидируется backend АС КОДА. Frontend хранит полученный opaque `session_id` только для продолжения сессии; если frontend вызывает dialog API без `session_id`, backend создаёт новую UI-сессию и тем самым сбрасывает предыдущий диалоговый контекст для текущего окна.
- История диалога и агентский контекст принадлежат RAIN; backend АС КОДА проксирует/нормализует историю и может хранить локальную копию для UI/аудита по правилам синхронизации, но не является владельцем агентского контекста.
- АС КОДА не отправляет в RAIN отдельное поле `context`/`contextPrompt`: для консультации передаётся только `message`, а для БТ-сценария дополнительно передаются согласованные поля `simulation_id`, `risk_params`, `start_datetime` и `fio`.
- Максимальная длина пользовательского `message` для отправки в RAIN в MVP: `3000` символов; лимит валидируется на frontend и backend до server-to-server вызова.
- `history_changed` не используется во frontend/backend API: backend не хранит состояние видимой frontend history window, а frontend после terminal status сам запрашивает latest page истории и решает, обновлять низ чата или показать индикатор нового сообщения.
- `btUrl` как отдельное поле RAIN не используется в текущих требованиях; целевой контракт RAIN возвращает структурированные `artifacts[]` для результата run, включая возможную ссылку на БТ.

## Модель ошибок для frontend

- Все ошибки frontend-facing `/dialog/*` API должны возвращать машинный код в `error.code` и безопасный для пользователя текст в `error.message`.
- Если ошибка возвращается HTTP error response, frontend берёт код из `response.body.error.code`.
- Если ошибка связана с terminal status сессии, frontend берёт код из `DialogSessionView.error.code` в ответе `GET /dialog/status?session_id=...`.
- Если ошибка выявлена до обращения к backend, frontend использует локальный код валидации из FE-правил и не имитирует backend/Rain-код.
- Если источник ошибки RAIN-фасад, backend АС КОДА берёт код из HTTP/API error фасада и маппит его в безопасный `DialogError.code`.
- Если источник ошибки агент, backend АС КОДА берёт terminal `RunStatusResponse.status/error.code` из polling фасада, маппит его в безопасный `DialogError.code` и не раскрывает stack trace, OTT, внутренний URL или сырой технический текст RAIN.
- `failed` и `timeout` агента не возвращаются как HTTP error response `POST /dialog/message`; они доступны frontend только через `DialogSessionView.error` после polling `GET /dialog/status?session_id=...`.
- Для пользователя показывается сообщение из таблиц frontend-требований; `error.code` используется для выбора сценария UI, telemetry и диагностики.

| Сценарий | Код для frontend | Откуда frontend берёт код | Пользовательское сообщение |
|---|---|---|---|
| Невалидный `session_id` | `invalid_session_id_format` | `response.body.error.code` от `POST /dialog/session` или `GET /dialog/status` | `Не удалось восстановить текущую сессию агента.` |
| Нет доступа к разделу/сессии/симуляции | `access_denied`, `simulation_access_denied` | `response.body.error.code` от соответствующего `/dialog/*` endpoint | `Недостаточно прав для действия с агентом.` |
| Сессия не найдена или не принадлежит пользователю | `session_not_found` | `response.body.error.code` от `/dialog/*` endpoint | `Не удалось восстановить текущую сессию агента.` |
| Агент не готов принимать сообщения | `agent_not_ready` | `response.body.error.code` от `POST /dialog/message` или `AgentStatusResponse.status != ready` | `Агент сейчас не готов принимать сообщения.` |
| Уже есть active run | `run_in_progress` | `response.body.error.code` от `POST /dialog/message` | `Дождитесь ответа агента перед отправкой нового сообщения.` |
| Пустое сообщение | `message_empty` | frontend local validation или `response.body.error.code` от `POST /dialog/message` | `Введите сообщение перед отправкой.` |
| Сообщение длиннее `3000` символов | `message_too_long` | frontend local validation или `response.body.error.code` от `POST /dialog/message` | `Сообщение слишком длинное. Сократите текст перед отправкой.` |
| Не удалось прочитать статус через RAIN-фасад | `rain_status_unavailable` | `response.body.error.code` от `GET /dialog/status` | `Не удалось обновить статус агента. Попробуйте ещё раз.` |
| Агент завершил run ошибкой | `agent_error` | `DialogSessionView.error.code`, нормализованный из terminal status/error фасада | `Не удалось получить результат от агента. Попробуйте позже.` |
| Агент завершил run timeout | `generation_timeout` или `agent_timeout` | `DialogSessionView.error.code`, нормализованный из terminal status/error фасада | `Агент долго не отвечает. Перезапустите сессию агента.` |
| BT-сценарий недоступен для симуляции | `bt_context_not_available` | frontend context validation или `response.body.error.code` от `POST /dialog/message` | `Сформировать БТ можно только для завершённой симуляции, доступной к выводу в ПРОМ.` |
| Нет риск-параметров для BT run | `bt_risk_params_missing` | `response.body.error.code` от `POST /dialog/message` | `Не удалось подготовить данные симуляции для БТ.` |

## Полный OpenAPI-контракт RAIN

Ниже приведена полная утверждённая версия server-to-server контракта RAIN из `context/change-requests/simulation-bt-agent/agent_openapi_1.yaml`. Этот блок включён в общие требования, чтобы FE/BE/QA видели целевой внешний контракт без перехода в отдельный файл. Каноническим файлом для машинной проверки остаётся `agent_openapi_1.yaml`; при изменении согласованного контракта RAIN нужно синхронно обновить и файл, и этот раздел.

Важно для frontend/backend boundary: браузер не вызывает эти методы напрямую, не получает `run_id`, OTT/mTLS details и внутренние URL RAIN. Backend АС КОДА вызывает RAIN server-to-server и нормализует ответы в frontend-facing `/dialog/*` API.

```yaml
openapi: 3.0.3
info:
  title: Rain API
  description: |
    API обработки сообщений.
    - Идемпотентное создание run с ключом `Idempotency-Key`.
    - Статусы run: `queued`, `running`, `succeeded`, `failed`, `timeout`, `cancelled`.
    - Cursor-пагинация истории сообщений.
  version: 1.0.0
servers:
  - url: /chat
    description: Chat base path

tags:
  - name: Runs
    description: Асинхронные операции обработки сообщений
  - name: Messages
    description: История сообщений

paths:
  /runs:
    post:
      tags:
        - Runs
      summary: Создать асинхронную операцию обработки сообщения
      operationId: createRun
      parameters:
        - name: Idempotency-Key
          in: header
          required: true
          schema:
            $ref: '#/components/schemas/IdempotencyKey'
          description: Уникальный ключ идемпотентности (UUID)
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateRunRequest'
      responses:
        '202':
          description: Запрос принят, run создан
          headers:
            Location:
              description: URL созданного run
              schema:
                type: string
                format: uri-reference
                example: /chat/runs/run-123
            Retry-After:
              description: Рекомендуемое время до повторного опроса статуса (секунды)
              schema:
                type: integer
                example: 5
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/RunStatusResponse'
              example:
                run_id: "run-123"
                session_id: "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
                idempotency_key: "3bdb8f6e-c9e1-46d0-b469-327d4b6fd0f8"
                status: "queued"
                retry_after_seconds: 5
        '200':
          description: Запрос идемпотентен, run уже существует (тот же ключ и тело)
          headers:
            Retry-After:
              description: Рекомендуемое время до повторного опроса статуса (опционально)
              schema:
                type: integer
              example: 5
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/RunStatusResponse'
              example:
                run_id: "run-123"
                session_id: "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
                idempotency_key: "3bdb8f6e-c9e1-46d0-b469-327d4b6fd0f8"
                status: "running"
                retry_after_seconds: 5
        '409':
          $ref: '#/components/responses/IdempotencyConflict'
        '400':
          $ref: '#/components/responses/BadRequest'

  /runs/{run_id}:
    get:
      tags:
        - Runs
      summary: Получить состояние run
      operationId: getRunStatus
      parameters:
        - name: run_id
          in: path
          required: true
          schema:
            type: string
          example: run-123
      responses:
        '200':
          description: Состояние run
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/RunStatusResponse'
              examples:
                running:
                  value:
                    run_id: "run-123"
                    session_id: "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
                    idempotency_key: "3bdb8f6e-c9e1-46d0-b469-327d4b6fd0f8"
                    status: "running"
                    created_at: "2026-04-29T12:30:00.123+03:00"
                    updated_at: "2026-04-29T12:30:20.000+03:00"
                    retry_after_seconds: 5
                succeeded:
                  value:
                    run_id: "run-123"
                    session_id: "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
                    idempotency_key: "3bdb8f6e-c9e1-46d0-b469-327d4b6fd0f8"
                    status: "succeeded"
                    created_at: "2026-04-29T12:30:00.123+03:00"
                    updated_at: "2026-04-29T12:31:40.000+03:00"
                    result_url: "/chat/runs/run-123/result"
                    message_id: "msg-789"
                failed:
                  value:
                    run_id: "run-123"
                    session_id: "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
                    idempotency_key: "3bdb8f6e-c9e1-46d0-b469-327d4b6fd0f8"
                    status: "failed"
                    created_at: "2026-04-29T12:30:00.123+03:00"
                    updated_at: "2026-04-29T12:31:00.000+03:00"
                    error:
                      code: "agent_error"
                      message: "Не удалось сформировать ответ"
                timeout:
                  value:
                    run_id: "run-123"
                    session_id: "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
                    idempotency_key: "3bdb8f6e-c9e1-46d0-b469-327d4b6fd0f8"
                    status: "timeout"
                    created_at: "2026-04-29T12:30:00.123+03:00"
                    updated_at: "2026-04-29T12:35:00.000+03:00"
                    error:
                      code: "generation_timeout"
                      message: "Ответ не был сформирован за отведённое время"
                cancelled:
                  value:
                    run_id: "run-123"
                    session_id: "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
                    idempotency_key: "3bdb8f6e-c9e1-46d0-b469-327d4b6fd0f8"
                    status: "cancelled"
                    created_at: "2026-04-29T12:30:00.123+03:00"
                    updated_at: "2026-04-29T12:32:00.000+03:00"
        '404':
          $ref: '#/components/responses/NotFound'

  /runs/{run_id}/result:
    get:
      tags:
        - Runs
      summary: Получить результат завершённого run
      operationId: getRunResult
      parameters:
        - name: run_id
          in: path
          required: true
          schema:
            type: string
          example: run-123
      responses:
        '200':
          description: Результат завершённого run
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/RunResultResponse'
              example:
                run_id: "run-123"
                session_id: "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
                idempotency_key: "3bdb8f6e-c9e1-46d0-b469-327d4b6fd0f8"
                message:
                  message_id: "msg-789"
                  role: "assistant"
                  content: "Страница БТ создана: https://confluence.example.local/pages/viewpage.action?pageId=12345"
                  created_at: "2026-04-29T12:31:40.000+03:00"
                artifacts:
                  - type: "bt_page"
                    url: "https://confluence.example.local/pages/viewpage.action?pageId=12345"
                    title: "БТ SIM-CC-148"
        '404':
          $ref: '#/components/responses/NotFound'
        '409':
          description: Run ещё не завершён
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
              example:
                error:
                  code: "run_not_completed"
                  message: "Результат недоступен, пока run не завершён"

  /sessions/{session_id}/messages:
    get:
      tags:
        - Messages
      summary: Получить страницу истории сообщений сессии
      operationId: getSessionMessages
      parameters:
        - name: session_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
          example: a1b2c3d4-e5f6-7890-abcd-ef1234567890
        - name: limit
          in: query
          schema:
            type: integer
            minimum: 1
            maximum: 50
            default: 20
          description: Размер страницы
        - name: before
          in: query
          schema:
            type: string
          description: Cursor для загрузки более ранних сообщений
        - name: after
          in: query
          schema:
            type: string
          description: Cursor для загрузки новых сообщений
        - name: order
          in: query
          schema:
            type: string
            enum: [asc, desc]
            default: desc
          description: Порядок сообщений в выдаче
      responses:
        '200':
          description: Страница сообщений
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SessionMessagesResponse'
              example:
                session_id: "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
                items:
                  - message_id: "msg-101"
                    role: "user"
                    content: "Сформируй БТ по симуляции SIM-CC-148."
                    created_at: "2026-04-29T12:30:03.000+03:00"
                    run_id: "run-123"
                  - message_id: "msg-102"
                    role: "assistant"
                    content: "Уточните бизнес-эффект для БТ."
                    created_at: "2026-04-29T12:30:40.000+03:00"
                    run_id: "run-123"
                older_cursor: "cursor-older-001"
                sync_cursor: "cursor-after-102"
                message_count: 2
                last_message_id: "msg-102"
                last_message_seq: 102
                history_version: "hv-20260429-000102"
                has_more_before: true
                has_more_after: false
        '400':
          description: Невалидный cursor
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
              example:
                error:
                  code: "invalid_cursor"
                  message: "Cursor недействителен или истёк"
        '404':
          $ref: '#/components/responses/NotFound'

  /messages/{message_id}:
    get:
      tags:
        - Messages
      summary: Получить одно сообщение целиком
      operationId: getMessageById
      parameters:
        - name: message_id
          in: path
          required: true
          schema:
            type: string
          example: msg-200
      responses:
        '200':
          description: Сообщение
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/MessageObject'
              example:
                message_id: "msg-200"
                role: "assistant"
                content: "полный текст длинного ответа..."
                created_at: "2026-04-29T12:35:00.000+03:00"
                run_id: "run-123"
        '404':
          $ref: '#/components/responses/NotFound'

components:
  schemas:
    IdempotencyKey:
      type: string
      format: uuid
      example: 3bdb8f6e-c9e1-46d0-b469-327d4b6fd0f8

    CreateRunRequest:
      type: object
      required:
        - session_id
        - message
      properties:
        session_id:
          type: string
          format: uuid
          description: Идентификатор сессии
          example: a1b2c3d4-e5f6-7890-abcd-ef1234567890
        message:
          type: string
          maxLength: 3000
          description: Текст сообщения пользователя, максимум 3000 символов
          example: "Сформируй БТ по симуляции SIM-CC-148."
        mode:
          type: string
          description: Режим обработки (например, bt_creation)
          example: "bt_creation"
        simulation_id:
          type: string
          description: Идентификатор симуляции
          example: "SIM-CC-148"
        risk_params:
          type: object
          description: Параметры риска
          properties:
            as_is:
              $ref: '#/components/schemas/RiskParams'
            to_be:
              $ref: '#/components/schemas/RiskParams'
        start_datetime:
          type: string
          format: date-time
          description: Опциональная временная метка начала
          example: "2026-04-29T12:30:00.123+03:00"
        fio:
          type: string
          description: ФИО инициатора
          example: "Иванов Иван Иванович"

    RiskParams:
      type: object
      description: Пара "показатель-значение" (значения как строки для точности decimal)
      properties:
        PD_LIMIT:
          anyOf:
            - type: number
            - type: string
          example: "0.38"                
        UTIL_SEGMENT_CAP:
          anyOf:
            - type: number
            - type: string
          example: "98000"

    RunStatusResponse:
      type: object
      required:
        - run_id
        - session_id
        - idempotency_key
        - status
      properties:
        run_id:
          type: string
          example: "run-123"
        session_id:
          type: string
          format: uuid
          example: "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
        idempotency_key:
          $ref: '#/components/schemas/IdempotencyKey'
        status:
          type: string
          enum: [queued, running, succeeded, failed, timeout, cancelled]
          example: "running"
        created_at:
          type: string
          format: date-time
          description: Время создания run
        updated_at:
          type: string
          format: date-time
          description: Время последнего обновления статуса
        retry_after_seconds:
          type: integer
          description: Рекомендуемое время до повторного опроса (для активных статусов)
          example: 5
        result_url:
          type: string
          format: uri-reference
          description: URL результата (только для статуса succeeded)
          example: "/chat/runs/run-123/result"
        message_id:
          type: string
          description: Идентификатор сообщения агента (при succeeded)
          example: "msg-789"
        error:
          $ref: '#/components/schemas/ErrorInfo'

    ErrorInfo:
      type: object
      properties:
        code:
          type: string
        message:
          type: string

    RunResultResponse:
      type: object
      required:
        - run_id
        - session_id
        - idempotency_key
        - message
      properties:
        run_id:
          type: string
          example: "run-123"
        session_id:
          type: string
          format: uuid
          example: "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
        idempotency_key:
          $ref: '#/components/schemas/IdempotencyKey'
        message:
          $ref: '#/components/schemas/MessageObject'
        artifacts:
          type: array
          items:
            $ref: '#/components/schemas/Artifact'

    Artifact:
      type: object
      required:
        - type
        - url
      properties:
        type:
          type: string
          example: "bt_page"
        url:
          type: string
          format: uri
          example: "https://confluence.example.local/pages/viewpage.action?pageId=12345"
        title:
          type: string
          example: "БТ SIM-CC-148"

    MessageObject:
      type: object
      required:
        - message_id
        - role
        - content
        - created_at
      properties:
        message_id:
          type: string
          example: "msg-789"
        role:
          type: string
          enum: [user, assistant]
          example: "assistant"
        content:
          type: string
          example: "Страница БТ создана: https://..."
        created_at:
          type: string
          format: date-time
          example: "2026-04-29T12:31:40.000+03:00"
        run_id:
          type: string
          description: Идентификатор run, породившего сообщение (для ассистента)
          example: "run-123"

    SessionMessagesResponse:
      type: object
      required:
        - session_id
        - items
        - older_cursor
        - sync_cursor
        - message_count
        - last_message_id
        - last_message_seq
        - history_version
        - has_more_before
        - has_more_after
      properties:
        session_id:
          type: string
          format: uuid
        items:
          type: array
          items:
            allOf:
              - $ref: '#/components/schemas/MessageObject'
              - type: object
                properties:
                  run_id:
                    type: string
                required: [run_id]
        older_cursor:
          type: string
          nullable: true
          description: Cursor для более старых сообщений (null если нет)
        sync_cursor:
          type: string
          description: Cursor для инкрементальной синхронизации
        message_count:
          type: integer
          description: Количество сообщений в текущей странице
        last_message_id:
          type: string
        last_message_seq:
          type: integer
          description: Порядковый номер последнего сообщения в истории
        history_version:
          type: string
          description: Версия истории (для контроля согласованности)
        has_more_before:
          type: boolean
          description: Есть ли более ранние сообщения
        has_more_after:
          type: boolean
          description: Есть ли более новые сообщения (относительно after)

    ErrorResponse:
      type: object
      required:
        - error
      properties:
        error:
          $ref: '#/components/schemas/ErrorInfo'

  responses:
    BadRequest:
      description: Некорректный запрос
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ErrorResponse'
    NotFound:
      description: Ресурс не найден
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ErrorResponse'
          example:
            error:
              code: "not_found"
              message: "Запрашиваемый ресурс не существует"
    IdempotencyConflict:
      description: Конфликт идемпотентности – тот же ключ, другое тело
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ErrorResponse'
          example:
            error:
              code: "idempotency_conflict"
              message: "Idempotency-Key уже использован для другого запроса"
              retryable: false
```

## Порядок slice для контроля

1. `01 agent-entrypoint — Точка входа, UI-сессия и статус агента`
2. `02 dialog-session — Асинхронная отправка сообщения, polling и история`
3. `03 bt-publication — Действия по БТ, контекст симуляции и публикация`

---

## STORY-SIMULATION-BT-AGENT-001 — Точка входа, UI-сессия и статус агента

Slice card: `slices/agent-entrypoint/slice.md`
Детализация FE: `slices/agent-entrypoint/requirements/frontend.md`
Детализация BE: `slices/agent-entrypoint/requirements/backend.md`
Общий prototype: `prototype.html`
Slice prototype: `slices/agent-entrypoint/delivery-prototype/prototype.html`
Planning story: `planning/stories/STORY-SIMULATION-BT-AGENT-001.md`

**Бизнес-требования**

- Цель: дать пользователю единую точку входа в окно агента на страницах симуляций и явно показать готовность агента к работе.
- Бизнес-правила: окно агента доступно со списка, деталки, вкладок деталки и формы редактирования; `session_id` создаёт backend АС КОДА при первом открытии или сбросе сессии, а frontend только хранит и передаёт его как opaque token; статус агента определяется readiness/liveness агента через backend АС КОДА; действие по БТ доступно только для конкретной успешно завершённой симуляции с опцией вывода в ПРОМ.
- Ограничения: открытие окна не должно блокировать основной интерфейс; RAIN не имеет отдельного API открытия или восстановления диалога; frontend не вызывает RAIN напрямую и не работает с OTT.

**Пользовательские требования к АС КОДА**

- Пользователь может открыть окно агента с любой страницы раздела симуляций.
- Пользователь остаётся на текущей странице, а окно открывается без смены маршрута.
- Пользователь видит в шапке окна status chip агента.
- Если агент не готов, пользователь видит понятный статус, а ввод/отправка сообщения блокируются до восстановления готовности.
- На странице подходящей симуляции пользователь видит inline-действие `Сформировать БТ для текущей симуляции`.

**Критерии приемки**

1. Окно агента открывается со списка симуляций, с деталки, с вкладок деталки и с формы редактирования.
2. При первом открытии окна frontend вызывает backend без `session_id`, backend создаёт UI-сессию и возвращает `session_id`; RAIN при этом не вызывается.
3. Status chip использует readiness/liveness агента, полученные через backend АС КОДА.
4. При `readiness=not ready` или потере связи с агентом поле ввода, отправка и agent actions недоступны.

**USE CASES**

- **осн. сценарий 1** пользователь открывает окно агента со списка симуляций.
- **альт. сценарий 1.1** пользователь открывает окно агента с деталки симуляции или с её вкладки.
- **альт. сценарий 1.2** readiness агента недоступен, и окно открывается в состоянии `Агент недоступен`.
- **осн. сценарий 2** frontend периодически обновляет статус агента через backend.

### Функциональные требования

#### Реализация для FRONTEND

**Описание UI**

| Экран | Результат |
| --- | --- |
| Список симуляций | Доступна точка входа в окно агента |
| Деталка симуляции, вкладки деталки, форма редактирования | Доступна точка входа в окно агента без смены маршрута |
| Окно агента | В шапке отображается status chip агента, ниже история, composer и контекстные agent actions |

Требования на фронт:

- добавить единую точку входа в окно агента на ключевых страницах раздела симуляций;
- открыть окно как неблокирующую панель без сброса состояния страницы;
- при первом открытии окна вызвать backend без `session_id`, получить `session_id` и дальше передавать его параметром для продолжения той же UI-сессии;
- при намеренном сбросе сессии вызвать dialog API без `session_id`, чтобы backend создал новую UI-сессию и вернул новый `session_id`;
- при открытии окна не отправлять `context`, `contextPrompt`, историю, риск-параметры или ФИО в RAIN;
- показывать status chip агента по данным backend status API;
- блокировать поле ввода, отправку и agent actions, если агент не готов или есть активный run.

Связанный детальный FE pack: `slices/agent-entrypoint/requirements/frontend.md`

#### Реализация BACKEND

Требования на бэк:

- предоставить frontend endpoint для открытия/восстановления UI-сессии АС КОДА без вызова RAIN;
- создавать, хранить и восстанавливать UI-сессию по backend-managed `session_id` в рамках пользовательской СУДИР-сессии;
- предоставить frontend endpoint статуса агента, агрегирующий `GET RAIN /health/liveness` и `GET RAIN /health/readiness`;
- использовать короткие таймауты и кэш статуса агента, чтобы status chip не создавал лишнюю нагрузку;
- не отдавать в браузер OTT, mTLS details и внутренний endpoint RAIN.

Связанный детальный BE pack: `slices/agent-entrypoint/requirements/backend.md`

| | |
| --- | --- |
| **Сервис** | `АС КОДА agent integration boundary` |
| ИФТ URL | `POST /dialog/session`, `GET /dialog/agent/status`; server-to-server: `GET /health/liveness`, `GET /health/readiness` |
| База данных | `agent_ui_session`, `agent_dialog_message` или эквивалентное хранилище UI-сессии |
| Методы | `slices/agent-entrypoint/requirements/backend.md` |

**Изменения в ролевой модели**

- Новая отдельная роль в рамках MVP не вводится.
- Доступ к окну агента наследуется от доступа к разделу симуляций.
- Действие по БТ дополнительно зависит от контекста завершённой симуляции.

**Отправка в Аудит**

- Технически логируются открытие окна, проверка статуса агента и ошибки восстановления UI-сессии.
- Бизнес-аудит публикации БТ фиксируется в slice `bt-publication`.

**BUGS (Если есть)**

- Пока не зафиксированы.

### Доп. пояснения

- Этот раздел задаёт вход в feature и должен оставаться первым в контрольной последовательности.
- Health endpoints RAIN используются только backend АС КОДА; frontend получает нормализованный статус.

---

## STORY-SIMULATION-BT-AGENT-002 — Асинхронная отправка сообщения, polling и история

Slice card: `slices/dialog-session/slice.md`
Детализация FE: `slices/dialog-session/requirements/frontend.md`
Детализация BE: `slices/dialog-session/requirements/backend.md`
Общий prototype: `prototype.html`
Slice prototype: `slices/dialog-session/delivery-prototype/prototype.html`
Planning story: `planning/stories/STORY-SIMULATION-BT-AGENT-002.md`

**Бизнес-требования**

- Цель: обеспечить устойчивый диалог с агентом внутри АС КОДА без долгого блокирующего браузерного REST-запроса.
- Бизнес-правила: frontend отправляет сообщение в backend АС КОДА и получает быстрый `202 Accepted` с состоянием сессии; backend вызывает REST-фасад RAIN `POST /chat/runs` и сохраняет внутренний `agent_dialog_run_ref` для связи `session_id` с `run_id` RAIN; после `202 Accepted` retry создания run не выполняется, frontend/backend только poll-ят фасад по статусу; frontend polling-ом читает статус диалоговой сессии по `session_id`; новая отправка по той же сессии запрещена, пока у RAIN есть активный run; история диалога читается страницами через backend АС КОДА из RAIN.
- Ограничения: frontend не вызывает RAIN напрямую; RAIN владеет run status и историей; для одного `session_id` в MVP допускается только один активный run; frontend не должен загружать всю длинную историю сразу.

**Пользовательские требования к АС КОДА**

- Диалог открывается в неблокирующей правой панели.
- Пользователь может продолжать работу со страницей симуляции вне панели агента.
- На время активного run поле ввода и отправка заблокированы, а пользователь видит состояние ожидания.
- После ответа агента сообщение появляется в истории.
- Если история длинная, пользователь видит последние сообщения и может догрузить более ранние.
- После ошибки агента пользователь видит понятное сообщение. После timeout агента пользователь видит рекомендацию перезапустить сессию, то есть начать заново с новым `session_id`.

**Критерии приемки**

1. Отправка сообщения возвращает быстрый `202 Accepted` без ожидания полного ответа RAIN.
2. Frontend polling-ом по `session_id` получает `dialog_status`: `queued`/`running`, затем terminal status: `succeeded`, `failed` или `timeout`.
3. Пока run активен, повторная отправка по тому же `session_id` недоступна на frontend и отклоняется backend.
4. История сообщений грузится порциями, а не целиком.
5. Ограничения длины prompt и отображаемой истории применяются и на frontend, и на backend.

**USE CASES**

- **осн. сценарий 1** пользователь отправляет сообщение и получает ответ после polling.
- **альт. сценарий 1.1** RAIN отвечает дольше обычного SLA, UI остаётся в состоянии ожидания.
- **альт. сценарий 1.2** run завершается `failed` или `timeout`, полученными через status фасада; UI не повторяет run автоматически, при timeout предлагает перезапуск с новым `session_id`.
- **осн. сценарий 2** пользователь догружает более ранние сообщения истории.

**Sequence diagram**

```plantuml
@startuml
title simulation-bt-agent: session-level polling and paginated history

actor User as U
participant "АС КОДА Frontend" as FE
participant "АС КОДА Backend" as BE
participant "RAIN" as RAIN

== Открытие панели ==
U -> FE: Открыть окно агента
FE -> BE: POST /dialog/session\nsession_id отсутствует
BE --> FE: session_id,\ncan_send_message,\ndialog_status
FE -> BE: GET /dialog/messages?session_id=...&limit=20
BE --> FE: items[], older_cursor,\nhas_more_before
FE -> BE: GET /dialog/status?session_id=...
BE --> FE: session_id,\ncan_send_message,\ndialog_status

== Отправка сообщения ==
U -> FE: Отправить prompt
FE -> BE: POST /dialog/message\nsession_id, message
BE -> BE: Проверить/создать session_id,\nreadiness, лимиты и отсутствие active run
BE -> RAIN: POST /chat/runs\nsession_id, message,\noptional simulation_id/risk_params,\nstart_datetime, fio
RAIN --> BE: 202 Accepted\nrun_id, status=queued
BE -> BE: Сохранить внутренний\nagent_dialog_run_ref
BE --> FE: 202 Accepted\nsession_id,\ncan_send_message=false,\ndialog_status=queued
FE --> U: Заблокировать composer\nпоказать ожидание

== Polling статуса сессии ==
loop пока dialog_status queued/running
  FE -> BE: GET /dialog/status?session_id=...
  BE -> RAIN: GET /chat/runs/{run_id}
  RAIN --> BE: run status
  BE --> FE: session_id,\ncan_send_message,\ndialog_status
end

FE -> BE: GET /dialog/messages?session_id=...&limit=20
BE -> RAIN: GET /chat/sessions/{session_id}/messages?limit=20
RAIN --> BE: latest items[], cursors
BE --> FE: latest items[], older_cursor,\nhas_more_before
alt Пользователь находится внизу истории
  FE --> U: Показать ответ и оставить scroll внизу
else Пользователь читает старые сообщения выше
  FE --> U: Не менять scroll-position\nпоказать индикатор "Новое сообщение"
  U -> FE: Клик по индикатору
  FE --> U: Перейти к последним сообщениям
end

== Догрузка старой истории ==
U -> FE: Скролл вверх / Загрузить ещё
FE -> BE: GET /dialog/messages?session_id=...&limit=20&before=older_cursor
BE -> RAIN: GET /chat/sessions/{session_id}/messages?limit=20&before=older_cursor
RAIN --> BE: previous items[], older_cursor,\nhas_more_before
BE --> FE: previous items[], older_cursor,\nhas_more_before
FE --> U: Добавить сообщения выше\nбез сброса scroll-position
@enduml
```

### Функциональные требования

#### Реализация для FRONTEND

**Описание UI**

| Экран | Результат |
| --- | --- |
| Правая панель агента | В шапке отображается status chip; ниже история, загрузка run, поле ввода, inline actions и кнопка отправки |
| Длинная история | Сначала загружаются последние сообщения; более ранние догружаются по действию пользователя или прокрутке вверх |

Требования на фронт:

- отправлять сообщение через backend АС КОДА и получать быстрый `202 Accepted` с состоянием сессии;
- запускать polling статуса сессии через `GET /dialog/status?session_id=...` и завершать ожидание только по terminal `dialog_status`;
- блокировать composer на время активного run и когда readiness агента не готов;
- показывать loading, timeout и error states без блокировки основного интерфейса;
- отображать Markdown в сообщениях агента;
- ограничивать длину вводимого prompt и показывать счётчик/ошибку при превышении;
- загружать историю сообщений страницами, например последние `20` сообщений при открытии и более ранние через cursor;
- если пользователь прокрутил историю вверх и последние сообщения не видны, при появлении нового сообщения не сбрасывать scroll-position, а показать индикатор `Новое сообщение`/счётчик и загрузить последние сообщения по действию пользователя;
- не хранить клиентскую историю как единственный источник правды после отправки: после terminal status синхронизироваться с backend history.

Связанный детальный FE pack: `slices/dialog-session/requirements/frontend.md`

#### Реализация BACKEND

Требования на бэк:

- принять пользовательское сообщение и создать run в RAIN через `POST /chat/runs`;
- маппить данные АС КОДА в поля RAIN: `session_id`, `message`, `risk_params`, `simulation_id`, `start_datetime`, `fio`;
- хранить внутренний `agent_dialog_run_ref` между UI-сессией АС КОДА и `run_id` RAIN и проксировать статус RAIN;
- предоставить polling endpoint статуса сессии с `session_id` в параметрах запроса, возвращающий `session_id`, `dialog_status`, `can_send_message` и ошибку без раскрытия `run_id`;
- не возвращать `history_changed` и не хранить состояние frontend history window на backend;
- проксировать/нормализовать историю RAIN и отдавать её frontend порциями через cursor/limit;
- применять server-side ограничение длины пользовательского `message` до `3000` символов и лимиты страниц истории;
- выполнять retry только для retryable ошибок фасада/transport до принятия run; после `202 Accepted` не повторять `POST /chat/runs`, а только poll-ить фасад;
- не выполнять автоматический retry для terminal `failed`/`timeout` агента; при agent timeout пользователь должен перезапустить сессию с новым `session_id`.

Связанный детальный BE pack: `slices/dialog-session/requirements/backend.md`

| | |
| --- | --- |
| **Сервис** | `АС КОДА agent integration boundary` |
| ИФТ URL | `POST /dialog/message`, `GET /dialog/status?session_id=...`, `GET /dialog/messages?session_id=...`; server-to-server: `POST /chat/runs`, `GET /chat/runs/{run_id}`, `GET /chat/sessions/{session_id}/messages` |
| База данных | `agent_dialog_run`, `agent_dialog_message`, `agent_ui_session` или эквивалент |
| Методы | `slices/dialog-session/requirements/backend.md` |

**Изменения в ролевой модели**

- Ролевая модель не расширяется.
- Доступ к диалогу наследуется от точки входа feature.

**Отправка в Аудит**

- Технически логируются отправка сообщения, создание run, terminal status, timeout и ошибки агента.
- Бизнес-аудит публикации БТ фиксируется отдельно в slice `bt-publication`.

**BUGS (Если есть)**

- Пока не зафиксированы.

### Доп. пояснения

- Этот раздел должен оставаться вторым в порядке контроля, потому что зависит от согласованной точки входа.
- Для UI не используется долгий браузерный REST до полного ответа агента.

---

## STORY-SIMULATION-BT-AGENT-003 — Действия по БТ, контекст симуляции и публикация

Slice card: `slices/bt-publication/slice.md`
Детализация FE: `slices/bt-publication/requirements/frontend.md`
Детализация BE: `slices/bt-publication/requirements/backend.md`
Общий prototype: `prototype.html`
Slice prototype: `slices/bt-publication/delivery-prototype/prototype.html`
Planning story: `planning/stories/STORY-SIMULATION-BT-AGENT-003.md`

**Бизнес-требования**

- Цель: дать пользователю управляемый сценарий формирования БТ через окно агента и показать ссылку на созданный БТ для ручного копирования.
- Бизнес-правила: action `Сформировать БТ для текущей симуляции` доступен только для конкретной успешно завершённой симуляции с опцией вывода в ПРОМ; клик по action только вставляет черновик запроса; пользователь может редактировать текст или не отправлять его; публикация БТ выполняется только после явного подтверждения внутри диалога с агентом; после успешной публикации агент возвращает ответ, в котором должна быть ссылка на БТ; автоматическое сохранение ссылки на БТ в данных симуляции в MVP не выполняется.
- Ограничения: черновик запроса формируется на стороне АС КОДА по данным existing simulation detail API; RAIN `POST /chat/runs` принимает optional `risk_params` и `simulation_id`; результат создания БТ должен читаться через `GET /chat/runs/{run_id}/result` и структурированные `artifacts[]`.

**Пользовательские требования к АС КОДА**

- В подходящем контексте пользователь видит inline action `Сформировать БТ для текущей симуляции`.
- По клику пользователь получает черновик запроса в поле ввода и может его свободно менять.
- После успешной публикации пользователь видит ответ агента; если RAIN вернул `artifacts[]` с `bt_page.url`, ссылка отображается и доступна для копирования.
- При желании пользователь сам сохраняет скопированную ссылку в соответствующем разделе симуляции вне автоматического сценария MVP.

**Критерии приемки**

1. Action по БТ доступен только в подходящем контексте симуляции и только когда агент готов.
2. По клику action вставляет черновик запроса, который не отправляется автоматически.
3. При отправке БТ-контекста backend передаёт RAIN `simulation_id` и `risk_params`, если данные доступны и валидны.
4. После успешной публикации ответ агента отображается в окне; URL на БТ можно открыть и скопировать, если он присутствует в `artifacts[]` результата RAIN run.
5. В рамках MVP данные симуляции не обновляются автоматически ссылкой на БТ после публикации.

**USE CASES**

- **осн. сценарий 1** пользователь открывает окно из подходящей симуляции и вставляет черновик запроса.
- **альт. сценарий 1.1** окно открыто из неподходящей страницы, и action по БТ недоступен.
- **альт. сценарий 1.2** пользователь редактирует черновик запроса или отказывается от отправки.
- **осн. сценарий 2** после успешной публикации пользователь получает ответ агента со ссылкой на созданный БТ.

### Функциональные требования

#### Реализация для FRONTEND

**Описание UI**

| Экран | Результат |
| --- | --- |
| Окно агента | Над composer divider отображается inline action `Сформировать БТ для текущей симуляции`; под полем ввода остаётся основная отправка |
| Страница симуляции | Автоматическое обновление ссылки на БТ после публикации в MVP не выполняется |

Требования на фронт:

- показать inline action БТ только в подходящем контексте и при готовом агенте;
- по клику вставлять в поле ввода черновик запроса по шаблону, используя данные уже реализованного `GET /api/v1/simulation/{number}`;
- не отправлять черновик автоматически;
- при отправке связать run с текущей симуляцией, чтобы backend мог передать RAIN `simulation_id` и `risk_params`;
- после успеха отобразить ответ агента и структурированную ссылку из `artifacts[]`, если RAIN её вернул, без автоматического обновления данных симуляции.

Связанный детальный FE pack: `slices/bt-publication/requirements/frontend.md`

#### Реализация BACKEND

Требования на бэк:

- переиспользовать existing simulation detail API как источник признаков доступности действия по БТ и данных риск-параметров;
- перед вызовом RAIN проверять, что пользователь имеет доступ к указанной симуляции и что она подходит для BT-сценария, если run связан с БТ;
- создать RAIN run через `POST /chat/runs` с `message`, `fio`, backend `start_datetime`, `session_id`, а также optional `simulation_id` и `risk_params`;
- после terminal status получить результат RAIN run через `GET /chat/runs/{run_id}/result`;
- использовать структурированные `artifacts[]`, включая `bt_page.url`, если они присутствуют в результате;
- аудировать успешный и неуспешный сценарий публикации по признакам ответа и terminal status.

Связанный детальный BE pack: `slices/bt-publication/requirements/backend.md`

| | |
| --- | --- |
| **Сервис** | `АС КОДА agent integration boundary + RAIN /chat/runs` |
| ИФТ URL | `GET /api/v1/simulation/{number}`, `POST /dialog/message`, server-to-server `POST /chat/runs`, `GET /chat/runs/{run_id}/result` |
| База данных | `новое автоматическое хранение btUrl в Simulation в рамках MVP не требуется` |
| Методы | `slices/bt-publication/requirements/backend.md` |

**Изменения в ролевой модели**

- Дополнительные роли не вводятся.
- Проверка прав наследуется от точки входа и страниц симуляций.

**Отправка в Аудит**

- Обязателен аудит успешной и неуспешной публикации БТ, если из ответа/сценария можно определить факт публикации.
- Отдельное событие автоматического обновления ссылки у симуляции в MVP не формируется, потому что такого обновления нет.

**BUGS (Если есть)**

- Пока не зафиксированы.

### Доп. пояснения

- Этот раздел завершает контрольную последовательность feature и должен идти после диалогового slice.
- Ссылка на БТ должна обрабатываться из `artifacts[]` результата RAIN run; отдельное поле `btUrl` в frontend API АС КОДА не требуется.
