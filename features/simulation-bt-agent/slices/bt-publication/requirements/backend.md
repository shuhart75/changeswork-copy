# Действия по БТ, контекст симуляции и публикация (Backend)

Статус: **draft**
Feature: `simulation-bt-agent`
Slice: `bt-publication`
Область: `MVP`
Дата обновления: `2026-04-29`
Шаблон: `.workflow/templates/requirements/backend.template.md`

## Связь с feature-level документом

- Главный контрольный документ: `../../requirements.md`
- Этот файл детализирует раздел `Реализация BACKEND` для текущего slice.

## Назначение пакета

- Зафиксировать server-side правила передачи контекста симуляции в RAIN `/chat`.
- Сохранить использование existing simulation detail API как источника признаков доступности и риск-параметров.
- Описать публикацию БТ через текстовый ответ RAIN `response`, без гарантированного отдельного поля `btUrl`.
- Зафиксировать отсутствие автоматической записи ссылки на БТ в данные симуляции.

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

- `STORY-SIMULATION-BT-AGENT-003`

### Связанные доменные решения

- `DEC-2026-04-24-SIMULATION-BT-AGENT-001`
- `DEC-2026-04-27-SIMULATION-BT-AGENT-003`
- `DEC-2026-04-28-SIMULATION-BT-AGENT-004`
- `DEC-2026-04-29-SIMULATION-BT-AGENT-007`

### Связанные артефакты

- Feature requirements: `../../requirements.md`
- Требования фронтенда: `frontend.md`
- Domain impact: `../../domain-impact.md`
- Implementation tasks: `../execution/tasks.md`

## Контекст и бизнес-смысл

### Цель

Передать RAIN достаточно контекста завершённой симуляции для формирования БТ, но сохранить контроль АС КОДА над доступностью действия, историей, асинхронным ожиданием и отображением результата.

### Источник правды

Источником правды для доступности действия по БТ и риск-параметров является existing simulation detail API. Источником текста результата является RAIN `ChatResponse.response`. Структурированного источника `btUrl` в текущем контракте RAIN нет.

### Затронутые bounded contexts / aggregates

- `Simulation`
- `Research and Execution`
- `Identity and Access`
- прикладная интеграция `agent_dialog_run`

### Термины и определения

- `BT run` — async run, связанный с режимом `bt_creation`.
- `risk_params` — структура RAIN `/chat` с `as_is` и `to_be`.
- `BT URL candidate` — URL, найденный в строковом ответе RAIN.

## Бизнес-правила и системные ограничения

### BR-1. BT-сценарий доступен только для подходящей симуляции
- страница должна быть привязана к конкретной симуляции;
- симуляция должна быть успешно завершённой;
- для симуляции должна быть доступна опция вывода в ПРОМ или эквивалентный признак;
- список симуляций и другие экраны без такого контекста не становятся подходящими сами по себе.

### BR-2. Backend не доверяет критичному BT-контексту из браузера без проверки
- frontend может передать `simulation_id` и режим `bt_creation`;
- backend проверяет права пользователя на симуляцию;
- backend проверяет подходящий статус симуляции;
- `risk_params` для RAIN собираются backend из existing simulation detail API или валидируются по нему перед отправкой.

### BR-3. Черновик запроса не создаёт побочных эффектов
- клик inline action на frontend не вызывает RAIN и не создаёт страницу в Confluence;
- только ручная отправка сообщения создаёт async run;
- RAIN может создать БТ только в ходе диалога и после явного подтверждения пользователя, если это предусмотрено агентским сценарием.

### BR-4. Ответ RAIN текстовый
- RAIN возвращает только `response`;
- backend сохраняет `response` как сообщение агента;
- backend может извлечь URL-кандидаты для удобства UI, но не должен гарантировать `btUrl`, пока контракт RAIN его не содержит;
- отсутствие URL в `response` не должно приводить к фиктивной ссылке.

### BR-5. Автосохранение ссылки в Simulation не выполняется
- backend не обновляет поле `btLink` или аналог в данных симуляции;
- пользователь вручную копирует ссылку из окна агента;
- отдельного события автоматического обновления симуляции нет.

## Границы MVP

### Входит в MVP

- проверка доступности BT-сценария по existing simulation detail API;
- сбор `risk_params.as_is` и `risk_params.to_be` для RAIN `/chat`;
- передача `simulation_id` в RAIN `/chat`;
- сохранение текстового ответа RAIN в истории;
- извлечение URL-кандидата из `response`, если это безопасно и однозначно;
- аудит успешного/неуспешного BT run по доступным признакам;
- отсутствие автосохранения ссылки в симуляцию.

### Не входит в MVP

- отдельный preparatory backend endpoint для черновика;
- автоматическая запись `btUrl` в Simulation;
- гарантия структурированного `btUrl`;
- автоматический retry публикации БТ при timeout;
- проверка уникальности названия БТ на стороне АС КОДА.

### Отложено после MVP

- расширение контракта RAIN `ChatResponse.btUrl`;
- идемпотентный ключ публикации;
- статусный endpoint RAIN для проверки результата после timeout;
- автоматическое сохранение выбранной ссылки в симуляцию.

## Пользовательские и системные сценарии

### Сценарий BE-1. Проверка подходящей симуляции
1. Frontend отправляет сообщение с `mode=bt_creation` и `simulation_id`.
2. Backend проверяет доступ пользователя к симуляции.
3. Backend читает existing simulation detail API.
4. Backend проверяет статус и доступность вывода в ПРОМ.
5. Если проверка не пройдена, run не создаётся или переводится в ошибку валидации.

### Сценарий BE-2. Вызов RAIN с BT-контекстом
1. Backend создаёт async run.
2. Backend собирает `risk_params.as_is` и `risk_params.to_be`.
3. Backend вызывает RAIN `POST /chat` с `session_id`, `message`, `simulation_id`, `risk_params`, `start_datetime`, `fio`.
4. RAIN возвращает `response`.
5. Backend сохраняет ответ как сообщение агента.

### Сценарий BE-3. Ответ содержит ссылку
1. Backend получает `response` от RAIN.
2. Backend сохраняет полный текст ответа в истории.
3. Backend может извлечь URL-кандидаты и пометить их для UI.
4. Backend не обновляет данные симуляции.

### Сценарий BE-4. Timeout после возможной публикации
1. RAIN не ответил до hard timeout.
2. Backend переводит run в `timeout`.
3. Backend не выполняет автоматический retry, потому что неизвестно, была ли создана страница БТ.
4. Пользователь получает ошибку и может вручную продолжить/проверить результат.

## Функциональные требования

### BE-FR-1. Backend проверяет право и состояние симуляции

**Описание:**
Для BT run backend должен проверить, что указанная симуляция действительно подходит для формирования БТ.

**Правила и ограничения:**
- `simulation_id` обязателен для `mode=bt_creation`;
- пользователь должен иметь доступ к симуляции;
- симуляция должна быть завершена;
- должен быть доступен признак вывода в ПРОМ или эквивалентный бизнес-признак;
- при неподходящей симуляции возвращается ошибка валидации без вызова RAIN.

**Зависимости:**
- existing simulation detail API;
- модель доступа пользователя.

### BE-FR-2. Backend формирует `risk_params` для RAIN

**Описание:**
Backend должен передать RAIN риск-параметры в формате, совместимом с `agent_openapi.yaml`.

**Правила и ограничения:**
- `risk_params.as_is` содержит текущие значения риск-параметров;
- `risk_params.to_be` содержит новые значения риск-параметров;
- значения приводятся к string, если контракт RAIN требует `additionalProperties: string`;
- если риск-параметры отсутствуют, backend должен либо вызвать RAIN без `risk_params` для консультационного режима, либо отклонить BT run как неполный контекст;
- frontend не является единственным источником правды для `risk_params`.

**Зависимости:**
- mapping полей existing simulation detail API;
- RAIN `ChatRequest.risk_params`.

### BE-FR-3. Backend вызывает RAIN `/chat` с BT-контекстом

**Описание:**
BT run использует общий async facade, но server-to-server payload должен содержать дополнительные поля симуляции.

**Правила и ограничения:**
- обязательные поля RAIN: `session_id`, `message`, `start_datetime`, `fio`;
- дополнительные поля для BT: `simulation_id`, `risk_params`;
- `start_datetime` берётся из UI-сессии;
- `fio` берётся из СУДИР-профиля пользователя;
- backend не передаёт клиентскую историю целиком в RAIN, если этого нет в контракте;
- backend сохраняет request/response metadata без утечки персональных данных сверх требований аудита.

**Зависимости:**
- `dialog-session` async run;
- RAIN `/chat`.

### BE-FR-4. Backend сохраняет `response` и извлекает URL-кандидаты

**Описание:**
Ответ RAIN должен быть сохранён как текстовое сообщение агента; URL на БТ может быть извлечён для UI, но не считается контрактным полем.

**Правила и ограничения:**
- backend сохраняет исходный `response`;
- backend может извлечь URL по безопасному URL parser;
- если найден один Confluence URL, backend может вернуть его как `url_candidates[0]` в сообщении;
- если URL нет или их несколько, UI показывает только текст и не делает предположений;
- backend не должен менять содержание ответа агента.

**Зависимости:**
- формат `ChatResponse.response`;
- правила безопасного linkify.

### BE-FR-5. Retry публикации ограничен

**Описание:**
Поскольку создание БТ может иметь побочный эффект, backend не должен автоматически повторять запросы, результат которых неизвестен.

**Правила и ограничения:**
- автоматический retry запрещён после отправки BT run в RAIN, если нет подтверждённой идемпотентности;
- retry `3` из системных требований может применяться только к безопасным техническим операциям до фактической передачи в RAIN или к health-check, если это согласовано;
- при timeout пользователю показывается неопределённый результат, а не автоматический повтор создания БТ;
- для полноценного retry нужен идемпотентный ключ публикации или status endpoint RAIN.

**Зависимости:**
- SLA RAIN;
- будущий контракт идемпотентности.

## Модель данных

### Основные сущности и поля

| Сущность / таблица | Поле | Тип | Обязательность | Описание |
|---|---|---|---|---|
| `Simulation` view | `status` | enum/string | условно обязательно | признак завершённой симуляции |
| `Simulation` detail response | `availableActions` / эквивалент | array | условно обязательно | признак доступности вывода в ПРОМ |
| `Simulation` detail response | `riskParameters` / `riskParamsChange` | object/array | условно обязательно | источник `risk_params` |
| `agent_dialog_run` | `mode` | enum/string | опционально | `consultation` или `bt_creation` |
| `agent_dialog_run` | `simulation_id` | string/null | условно обязательно | симуляция для BT run |
| `agent_dialog_run` | `url_candidates` | JSON/null | опционально | URL, извлечённые из `response` |
| `agent_dialog_message` | `content` | text | обязательно | исходный `response` RAIN |

### Инварианты и ограничения

- BT run не стартует без проверки симуляции;
- `risk_params` не берутся на доверие только из браузера;
- автоматическая запись `btUrl` в `Simulation` не выполняется;
- отсутствующий URL в `response` не заменяется фиктивным значением.

### Индексы / уникальности / FK

- индекс run по `simulation_id`, если нужен аудит или поиск BT-сценариев;
- внешняя связь с Simulation может быть логической, если bounded contexts разделены.

## API-контракт

### Эндпоинты

| Метод и маршрут | Назначение | Кто вызывает | Примечание |
|---|---|---|---|
| `GET /api/v1/simulation/{number}` / existing detail API | вернуть признаки доступности и данные риск-параметров | backend/frontend АС КОДА | источник BT-контекста |
| `POST /dialog/{session_id}/message` | создать async run, включая BT mode | frontend agent window | возвращает `run_id` |
| `POST RAIN /chat` | отправить сообщение агенту | backend АС КОДА | контракт из `agent_openapi.yaml` |

### OpenAPI fragment

```yaml
openapi: 3.0.3
info:
  title: BT Publication via RAIN Chat
  version: 1.0.0
paths:
  /dialog/{session_id}/message:
    post:
      summary: Создать async run для сообщения или БТ-сценария
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
                mode:
                  type: string
                  enum: [consultation, bt_creation]
                simulation_id:
                  type: string
                  nullable: true
      responses:
        "202":
          description: Run создан
        "400":
          description: Некорректный контекст БТ
        "409":
          description: Уже есть active run
        "503":
          description: Агент не готов
components: {}
```

### Примеры запросов и ответов

#### Пример 1. Server-to-server вызов RAIN для БТ

```http
POST /chat HTTP/1.1
Content-Type: application/json
```

```json
{
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "message": "Сформируй БТ по симуляции SIM-CC-148...",
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

#### Пример 2. Ошибка неподходящей симуляции

```json
{
  "error_code": "bt_context_not_available",
  "message": "БТ можно сформировать только для завершённой симуляции, доступной к выводу в ПРОМ."
}
```

## Интеграции, вычисления и фоновые процессы

- Внешние системы: RAIN, Confluence через RAIN, existing simulation detail API;
- Асинхронные процессы: BT run выполняется через общий background call RAIN `/chat`;
- Вычисление статусов / derived fields: доступность BT-сценария, `url_candidates`;
- Идемпотентность / ретраи: автоматический retry после передачи BT run в RAIN запрещён без идемпотентности.

## Ошибки и валидация

### Валидационные правила

- `simulation_id` обязателен для `mode=bt_creation`;
- пользователь должен иметь доступ к симуляции;
- симуляция должна быть завершена и доступна к выводу в ПРОМ;
- риск-параметры должны быть доступны или BT run отклоняется как неполный контекст;
- `response` RAIN не должен интерпретироваться как JSON, если контракт возвращает строку.

### Ошибки API

| Код/сценарий | Условие | Ответ |
|---|---|---|
| `400 bt_context_not_available` | симуляция неподходящая | ошибка бизнес-валидации |
| `400 bt_risk_params_missing` | нет риск-параметров для BT run | ошибка неполного контекста |
| `403 simulation_access_denied` | пользователь не имеет доступа к симуляции | отказ доступа |
| `404 simulation_not_found` | симуляция не найдена | ошибка отсутствующей симуляции |
| `504 agent_timeout` | RAIN не ответил до timeout | terminal status `timeout` |
| `502 agent_error` | ошибка RAIN | terminal status `failed` |

## Миграция и обратная совместимость

- Нужны ли миграции данных: нет для `Simulation`, да для хранения run/history, если ещё не создано.
- Нужен ли backfill: нет.
- Есть ли риски для текущего baseline: да, `btUrl` больше нельзя считать структурированным полем ответа агента.
- Что должно попасть в release finalization: mapping `risk_params`, правило отсутствия автосохранения, ограничение retry, необходимость структурированного `btUrl` как открытый вопрос.

## Observability и аудит

- Логи: BT run, `simulation_id`, terminal status, URL candidates count, ошибки валидации;
- Метрики: длительность BT run, success/failure/timeout rate, количество ответов с URL;
- Audit trail: успешная и неуспешная публикация БТ по доступным признакам; автоматического события сохранения ссылки в симуляцию нет.

## Критерии приемки

### BE-AC-1. Контекст БТ
- [ ] Backend проверяет доступ пользователя к симуляции
- [ ] Backend проверяет, что симуляция подходит для БТ
- [ ] Backend собирает `risk_params` из доверенного источника
- [ ] Backend передаёт RAIN `simulation_id` и `risk_params` для BT run

### BE-AC-2. Ответ и ссылка
- [ ] Backend сохраняет исходный `response` RAIN
- [ ] Backend не обещает отдельный `btUrl`, если его нет в контракте RAIN
- [ ] URL-кандидаты извлекаются только из реального текста ответа
- [ ] Backend не обновляет `Simulation.btLink` автоматически

### BE-AC-3. Timeout и retry
- [ ] Timeout BT run не приводит к скрытому автоматическому повтору
- [ ] Ошибка/timeout возвращаются frontend как terminal status
- [ ] Для безопасного retry зафиксирован открытый вопрос идемпотентности RAIN

## Открытые вопросы и допущения

- Нужно запросить у RAIN структурированный `btUrl` или `artifacts` в `ChatResponse`.
- Нужно подтвердить, что `risk_params.additionalProperties` действительно должны быть строками, и согласовать mapping числовых/булевых значений.
- Нужно согласовать idempotency key для сценария создания БТ, иначе автоматический retry остаётся запрещённым.
