# Асинхронная отправка сообщения, polling и история (Frontend)

Статус: **draft**
Feature: `simulation-bt-agent`
Slice: `dialog-session`
Область: `MVP`
Дата обновления: `2026-05-06`
Шаблон: `.workflow/templates/requirements/frontend.template.md`

## Связь с feature-level документом

- Главный контрольный документ: `../../requirements.md`
- Этот файл детализирует раздел `Реализация для FRONTEND` для текущего slice.

## Назначение пакета

- Зафиксировать frontend-поведение неблокирующей правой панели агента.
- Описать отправку пользовательского текста через async run вместо долгого браузерного REST.
- Описать polling статуса сессии, terminal states `dialog_status`, блокировку composer и порционную загрузку истории.
- Ограничить пакет общим диалогом, не дублируя правила доступности БТ.

## Источники и трассировка

### Основные источники

- `../slice.md`
- `../../feature.md`
- `../../references.md`
- `../../requirements.md`
- `context/change-requests/simulation-bt-agent/agent_openapi_1.yaml`
- `context/change-requests/simulation-bt-agent/agent_openapi.yaml` как устаревший исходный контракт
- `context/change-requests/simulation-bt-agent/Системные_требования_для_интеграции_АС_КОДА_и_AI_Агента_RAIN.md`
- `/home/reutov/Documents/AI/simulations_AI_agent/prototype/simulation-agent-mock.html`

### Связанные planning stories

- `STORY-SIMULATION-BT-AGENT-002`

### Связанные доменные решения

- `DEC-2026-04-24-SIMULATION-BT-AGENT-001`
- `DEC-2026-04-27-SIMULATION-BT-AGENT-002`
- `DEC-2026-04-29-SIMULATION-BT-AGENT-007`
- `DEC-2026-04-30-SIMULATION-BT-AGENT-009`
- `DEC-2026-05-05-SIMULATION-BT-AGENT-010`

### Связанные артефакты

- Feature requirements: `../../requirements.md`
- Delivery prototype: `../delivery-prototype/prototype.html`
- Domain impact: `../../domain-impact.md`
- Sequence diagram: `context/change-requests/simulation-bt-agent/new_message_indicator_sequence.puml`

## Контекст и бизнес-смысл

### Цель

Сделать окно агента постоянным помощником в интерфейсе симуляций, но не держать браузерный HTTP-запрос открытым до полного ответа RAIN, так как SLA агента может достигать десятков секунд и более.

### Пользователи и роли

- Пользователь интерфейса симуляций взаимодействует с окном агента в рамках своих прав доступа к этим страницам.

### Бизнес-контекст

RAIN по принятому контракту предоставляет async REST API: `POST /chat/runs`, `GET /chat/runs/{run_id}` и постраничную историю. Frontend не вызывает RAIN напрямую: он работает с backend АС КОДА, получает backend-managed `session_id`, подтверждение принятия сообщения и polling-ом читает session-level view без `run_id`.

### Термины и определения

- `run` — одна отправка пользовательского сообщения в RAIN через backend АС КОДА.
- `active run` — run в статусе `queued` или `running`, по которому ещё нет terminal status.
- `terminal status` — `succeeded`, `failed`, `timeout` или `cancelled`.
- `dialog_status` — нормализованное состояние диалога для frontend: `idle`, `queued`, `running`, `succeeded`, `failed`, `timeout`, `cancelled`.
- `can_send_message` — флаг backend АС КОДА, показывающий, можно ли сейчас отправить новое сообщение.
- `polling` — периодический запрос frontend к backend АС КОДА для чтения `dialog_status` и `can_send_message`.
- `cursor` — маркер для порционной загрузки более ранних сообщений истории.
- `history window` — набор страниц истории, загруженных frontend в текущем открытии панели; стартует с последних `20` сообщений и расширяется при догрузке вверх.
- `acknowledged_latest_message_id` — id последнего сообщения, которое пользователь фактически видел внизу истории.
- `current_latest_message_id` — id последнего сообщения, известного frontend после последней загрузки latest page.
- `pending_new_message` — локальный frontend-флаг, что latest page содержит сообщение новее `acknowledged_latest_message_id`, но пользователь ещё не видел актуальный низ истории.
- `is_near_bottom` — локальный frontend-флаг, что viewport находится около нижней границы истории и новое сообщение можно показать без нарушения текущего чтения.
- `composer` — поле ввода, inline actions и кнопка отправки в окне агента.

## Границы MVP

### Входит в MVP

- правая боковая панель агента;
- отправка сообщения через async run;
- polling статуса сессии;
- блокировка composer во время active run;
- отображение Markdown в сообщениях;
- загрузка истории через backend АС КОДА из RAIN;
- порционная загрузка истории сообщений;
- ограничение пользовательского `message` до `3000` символов;
- понятное сообщение об ошибке/timeout с возможностью перезапуска сессии.

### Не входит в MVP

- SSE/WebSocket между frontend и backend;
- прямой вызов RAIN из браузера;
- параллельные runs в рамках одного `session_id`;
- клиентское хранение полной истории как источник правды;
- автоматическая отмена run при закрытии окна.

### Отложено после MVP

- streaming partial responses;
- кнопка остановки активного run с реальной отменой на стороне RAIN;
- виртуализация очень больших сообщений;
- перенос истории между устройствами.

## Пользовательские сценарии

### Сценарий FE-1. Отправка сообщения через async run
1. Пользователь вводит сообщение в composer.
2. Frontend проверяет длину сообщения и готовность агента.
3. Frontend вызывает `POST /dialog/message` и передаёт `session_id` в body.
4. Backend быстро возвращает `202 Accepted` и статус сессии `dialog_status=queued`.
5. Frontend блокирует composer и начинает polling статуса сессии.
6. После terminal status frontend обновляет историю и разблокирует composer, если агент готов.

### Сценарий FE-2. Долгий ответ агента
1. Run остаётся в статусе `running` дольше обычного пользовательского ожидания.
2. Frontend продолжает polling с согласованным интервалом.
3. Пользователь видит состояние ожидания и не может отправить второе сообщение в ту же сессию.
4. Основной интерфейс симуляций остаётся доступным.

### Сценарий FE-3. Timeout или ошибка
1. Backend возвращает run status `failed` или `timeout`.
2. Frontend показывает понятное сообщение об ошибке.
3. Composer разблокируется только если backend сообщает, что сессия может продолжаться; иначе пользователь видит рекомендацию перезапустить сессию.

### Сценарий FE-4. Порционная загрузка истории
1. При открытии окна frontend запрашивает последние сообщения, например `limit=20`.
2. Если есть более ранние сообщения, UI показывает действие `Загрузить ещё` или догружает при прокрутке вверх.
3. Frontend запрашивает следующую страницу истории через `cursor`.

### Сценарий FE-5. Новое сообщение, когда пользователь ушёл далеко вверх
1. Пользователь прокрутил историю вверх так далеко, что latest page и последние сообщения могут быть выгружены из DOM/виртуального списка.
2. Frontend продолжает хранить session-level anchors: `acknowledged_latest_message_id`, `current_latest_message_id`, `is_near_bottom`.
3. Frontend polling-ом получает terminal `dialog_status=succeeded`.
4. Frontend запрашивает latest page: `GET /dialog/messages?session_id=...&limit=20`.
5. Frontend определяет новый `current_latest_message_id` по последнему сообщению latest page и сравнивает его с `acknowledged_latest_message_id`.
6. Если `current_latest_message_id` новее `acknowledged_latest_message_id` и `is_near_bottom=false`, frontend не меняет текущий scroll-position, выставляет `pending_new_message=true` и показывает sticky-индикатор `Новое сообщение`.
7. По клику на индикатор frontend показывает latest page, переводит scroll к последнему сообщению, выставляет `acknowledged_latest_message_id=current_latest_message_id` и убирает индикатор.
8. Если пользователь сам доскроллил до нижней границы истории, frontend выполняет то же подтверждение latest anchor и убирает индикатор.

## UI-состав и навигация

### Экран/состояние 1. Правая боковая панель агента

- Назначение: основная поверхность работы с агентом.
- Откуда открывается: из точки входа на страницах симуляций.
- Куда ведёт: остаётся поверх текущей страницы без смены маршрута.
- Что видно пользователю: status chip агента, история сообщений, индикатор active run, composer.
- Какие действия доступны: писать агенту, копировать текст, загрузить более раннюю историю, перезапустить сессию, продолжать работать в основном интерфейсе.

### Экран/состояние 2. Active run

- Назначение: показать, что сообщение принято и агент готовит ответ.
- Откуда открывается: после успешного `POST /dialog/message`.
- Куда ведёт: к отображению ответа, ошибке или timeout.
- Что видно пользователю: loading state, заблокированный composer, текущий status text.
- Какие действия доступны: работать с основным интерфейсом, копировать уже видимые сообщения, ждать завершения run.

### Экран/состояние 3. Длинная история

- Назначение: не загружать и не рендерить весь диалог сразу.
- Откуда открывается: при наличии более ранних сообщений.
- Куда ведёт: к догрузке предыдущей страницы сообщений.
- Что видно пользователю: последние сообщения и действие догрузки истории.
- Какие действия доступны: загрузить предыдущие сообщения, продолжить диалог после завершения active run.

### Экран/состояние 4. Пользователь не внизу истории

- Назначение: не сбивать пользователя с места чтения при появлении нового ответа агента.
- Откуда открывается: пользователь прокрутил историю вверх дальше порога `near bottom`.
- Куда ведёт: к возврату к последним сообщениям по действию пользователя.
- Что видно пользователю: текущий участок истории, индикатор появления нового сообщения, если frontend после terminal status загрузил latest page и обнаружил новое сообщение относительно `acknowledged_latest_message_id`.
- Какие действия доступны: продолжить читать старые сообщения, нажать индикатор нового сообщения и перейти к последним сообщениям.

## Функциональные требования

### FE-FR-1. Отправка сообщения запускает async run

**Описание:**
Frontend должен отправлять текст пользователя в backend АС КОДА и получать быстрый `202 Accepted` с состоянием сессии, не ожидая полного ответа RAIN.

**Детали:**
- запрос отправки выполняется только если agent status готов, нет active run и prompt проходит ограничения длины;
- frontend отправляет `session_id`, `message` и только согласованные поля текущей симуляции (`simulation_id`, `mode`) при наличии; отдельный `context`/`contextPrompt` не отправляется;
- если `session_id` отсутствует, backend создаёт новую UI-сессию и возвращает новый `session_id`;
- backend возвращает `202 Accepted` с `session_id`, `can_send_message=false` и `dialog_status`;
- после подтверждения frontend переводит composer в blocked state;
- полный ответ агента frontend получает только через polling session status и последующую синхронизацию истории.

**Зависимости:**
- backend async run API;
- status API агента.

### FE-FR-2. Polling session status

**Описание:**
Frontend должен читать состояние диалоговой сессии через polling backend АС КОДА.

**Детали:**
- polling начинается после успешного `POST /dialog/message`, если backend вернул `can_send_message=false` из-за активного run;
- базовый интервал polling задаётся конфигурацией frontend, рекомендуемо `2-5` секунд;
- frontend вызывает `GET /dialog/status?session_id=...`;
- status response содержит `session_id`, `can_send_message`, `dialog_status` и optional `error`; `history_changed` отсутствует в контракте;
- polling завершается, когда `dialog_status` находится в terminal status: `succeeded`, `failed`, `timeout`, `cancelled`;
- при `succeeded` frontend синхронизирует latest page истории;
- при `failed` или `timeout` frontend показывает ошибку и рекомендацию по дальнейшему действию;
- закрытие окна не должно оставлять UI в противоречивом состоянии: при повторном открытии frontend заново читает active run/status из backend.

**Зависимости:**
- `GET /dialog/status?session_id=...`;
- backend session status API;
- RAIN run status через backend АС КОДА.

### FE-FR-3. Composer блокируется при active run и неготовом агенте

**Описание:**
Пользователь не должен отправлять второе сообщение, пока агент обрабатывает предыдущее, а также когда backend сообщает, что RAIN не готов.

**Детали:**
- поле ввода, кнопка отправки и inline actions блокируются при active run;
- поле ввода, кнопка отправки и inline actions блокируются при `agent_status != ready`;
- пользователь видит причину блокировки: `Агент обрабатывает запрос`, `Агент недоступен` или `Агент не готов`;
- основной интерфейс симуляций не блокируется;
- если frontend по ошибке отправил второй запрос, backend должен вернуть конфликт, а frontend показать понятное сообщение.

**Зависимости:**
- status chip из slice `agent-entrypoint`;
- backend active run lock.

### FE-FR-4. Ограничение длины prompt

**Описание:**
Frontend должен предотвращать отправку слишком длинного сообщения до обращения к backend.

**Детали:**
- максимальная длина prompt задаётся конфигурацией, синхронизированной с backend; согласованный MVP value: `3000` символов;
- счётчик длины отображается рядом с composer или в состоянии ошибки;
- при превышении лимита кнопка отправки блокируется;
- шаблон БТ, вставленный inline action, также должен укладываться в лимит или показывать ошибку до отправки.

**Зависимости:**
- backend validation limit;
- шаблон черновика БТ.

### FE-FR-5. История загружается порциями

**Описание:**
Frontend не должен загружать весь длинный диалог сразу и не должен бесконечно держать в DOM все сообщения.

**Детали:**
- при открытии окна загружается последняя страница истории, рекомендуемо `limit=20`;
- если backend вернул `older_cursor` или `has_more_before=true`, UI показывает возможность загрузить более ранние сообщения;
- при догрузке frontend добавляет сообщения в начало истории без сброса текущего scroll-position;
- в рамках одного открытия панели frontend может держать в памяти уже загруженные страницы history window, но не считает их источником правды;
- рекомендуемый верхний предел history window для MVP: `100-200` сообщений или конфигурируемый лимит; при превышении лимита frontend может отбросить самые дальние от текущего viewport страницы и повторно загрузить их по cursor при необходимости;
- если пользователь находится около нижней границы истории, новое сообщение после terminal status добавляется в историю и UI автоматически остаётся внизу;
- если пользователь прокрутил историю вверх и низ не виден, frontend не меняет scroll-position, а показывает sticky-индикатор `Новое сообщение`; по клику на индикатор загружается последняя страница истории `limit=20` и scroll переводится вниз;
- если во время чтения старой истории active run завершился, frontend может сохранить новое сообщение в pending/bottom buffer, но не должен вставлять его так, чтобы сдвинуть текущий viewport;
- после terminal status frontend перечитывает последние `20` сообщений;
- frontend должен корректно отображать ситуацию, когда одно сообщение слишком большое: использовать сворачивание, max-height и внутренний scroll, не ломая панель;
- frontend не должен пытаться рендерить JSON или технические структуры как пользовательский контент.

**Зависимости:**
- `GET /dialog/messages?session_id=...&limit=&before=`;
- backend pagination.

### FE-FR-6. Индикатор нового сообщения работает через frontend anchors

**Описание:**
Frontend должен показывать индикатор `Новое сообщение` без backend-флага `history_changed` и без требования держать последние сообщения загруженными в DOM. Для этого frontend хранит лёгкие session-level anchors отдельно от виртуализированного `history window`.

**Детали:**
- frontend хранит `acknowledged_latest_message_id` — последнее сообщение, которое пользователь фактически видел внизу истории;
- frontend хранит `current_latest_message_id` — последнее известное сообщение после последней загрузки latest page;
- frontend хранит `is_near_bottom` — признак, что viewport находится около нижней границы истории;
- frontend хранит `pending_new_message` и при необходимости `pending_new_count` как локальное UI-состояние;
- виртуализация может выгружать body сообщений и страницы, далёкие от viewport, но не должна выгружать session-level anchors текущей UI-сессии;
- при открытии панели и первой загрузке latest page frontend выставляет `current_latest_message_id` по последнему сообщению страницы; если пользователь видит низ истории, одновременно выставляется `acknowledged_latest_message_id=current_latest_message_id`;
- после terminal `dialog_status=succeeded` frontend всегда запрашивает latest page без `before`;
- если latest page содержит сообщение новее `acknowledged_latest_message_id` и `is_near_bottom=false`, frontend выставляет `pending_new_message=true` и показывает sticky-индикатор `Новое сообщение`;
- если latest page содержит сообщение новее `acknowledged_latest_message_id` и `is_near_bottom=true`, frontend обновляет history window, оставляет scroll внизу, выставляет `acknowledged_latest_message_id=current_latest_message_id` и не показывает индикатор;
- если пользователь нажал индикатор, frontend показывает latest page, скроллит к последнему сообщению, выставляет `acknowledged_latest_message_id=current_latest_message_id`, сбрасывает `pending_new_message=false` и `pending_new_count=0`;
- если пользователь сам доскроллил до нижней границы и последнее известное сообщение оказалось видимым, frontend также выставляет `acknowledged_latest_message_id=current_latest_message_id` и убирает индикатор;
- если latest page не содержит сообщения новее `acknowledged_latest_message_id`, frontend не показывает индикатор;
- если `acknowledged_latest_message_id` отсутствует из-за сброса UI-сессии, frontend должен считать первую загруженную latest page базовой точкой и не показывать индикатор до появления следующего terminal update.

**Зависимости:**
- `GET /dialog/status?session_id=...`;
- `GET /dialog/messages?session_id=...&limit=20`;
- локальное состояние scroll/virtualized list.

### FE-FR-7. Markdown и ссылки отображаются безопасно

**Описание:**
Сообщение агента приходит из истории RAIN через backend АС КОДА, поэтому frontend должен отображать его как пользовательский текст/Markdown без исполнения небезопасного HTML.

**Детали:**
- поддерживаются текст, списки, ссылки и кодовые блоки;
- URL в ответе агента может быть подсвечен как ссылка;
- пользователь может копировать текст и ссылку из сообщения;
- если backend пометил URL как вероятную ссылку на БТ, frontend может показать дополнительное действие копирования ссылки.

**Зависимости:**
- формат сообщений истории RAIN;
- правила безопасности рендера Markdown.

## UI-состояния и отображение данных

| Элемент UI | Источник данных | Пустое состояние | Loading | Error | Примечание |
|---|---|---|---|---|---|
| История сообщений | `GET /dialog/messages?session_id=...` | пустая стартовая история | догрузка страницы | ошибка загрузки истории | загружается страницами, не целиком |
| Composer | локальное состояние + backend status | пустое поле | заблокирован при active run | заблокирован при неготовом агенте | лимит prompt отображается до отправки |
| Индикатор ожидания ответа | `GET /dialog/status?session_id=...` | отсутствует | `queued` / `running` | `failed` / `timeout` | terminal status снимает блокировку composer |
| Индикатор нового сообщения | локальное UI-состояние после terminal status и загрузки latest page | отсутствует | pending update | ошибка синхронизации | показывается, если пользователь не внизу истории |
| Сообщение агента | backend history после run | отсутствует | ожидается | показывается ошибка run | Markdown/linkify без небезопасного HTML |

## Интеграция с Backend API

| Метод и маршрут | Где используется | Что отправляем/читаем | Условия вызова | Примечание |
|---|---|---|---|---|
| `POST /dialog/message` | отправка пользовательского текста | отправляем optional `session_id`, `message`, `simulation_id/mode` при наличии; читаем `session_id`, `can_send_message`, `dialog_status` | после ручной отправки текста | возвращает `202`, не полный ответ агента; отсутствие `session_id` создаёт новую сессию |
| `GET /dialog/status?session_id=...` | polling статуса сессии | читаем `session_id`, `can_send_message`, `dialog_status`, ошибку | пока `dialog_status` активен или нужна синхронизация | отдельный status по `run_id` не нужен |
| `GET /dialog/messages?session_id=...&limit=&before=` | загрузка истории | читаем страницу сообщений, `older_cursor`, `has_more_before` | при открытии окна, после terminal status и догрузке истории | не загружает всю историю сразу |
| `GET /dialog/agent/status` | статус chip и блокировка composer | читаем нормализованный readiness/liveness status | при открытии окна и периодически | frontend не вызывает RAIN health напрямую |

## Валидация на frontend

### Правила

- нельзя отправить сообщение при active run;
- нельзя отправить сообщение при `agent_status != ready`;
- нельзя отправить пустой prompt;
- нельзя отправить prompt длиннее configured limit;
- нельзя считать локальную историю единственным источником правды после terminal status;
- нельзя ожидать, что backend помнит загруженную frontend историю; `history_changed` не используется;
- нельзя автоматически прокручивать пользователя вниз при появлении нового сообщения, если он читает старую историю выше порога `near bottom`;
- при polling timeout/network error frontend должен повторить чтение по согласованной retry policy или показать ошибку синхронизации.

### Сообщения об ошибках

| Ситуация | Код ошибки | Откуда frontend берёт код | Сообщение | Где показываем |
|---|---|---|---|---|
| Агент не готов | `agent_not_ready` | `response.body.error.code` от `POST /dialog/message` или `AgentStatusResponse.status != ready` | `Агент сейчас недоступен. Попробуйте позже.` | composer/status chip |
| Уже есть активный запрос | `run_in_progress` | `response.body.error.code` от `POST /dialog/message` | `Дождитесь ответа агента перед отправкой нового сообщения.` | composer |
| Prompt пустой | `message_empty` | frontend local validation или `response.body.error.code` от `POST /dialog/message` | `Введите сообщение перед отправкой.` | composer |
| Prompt превышает лимит | `message_too_long` | frontend local validation или `response.body.error.code` от `POST /dialog/message` | `Сообщение слишком длинное. Сократите текст перед отправкой.` | composer |
| Не удалось отправить сообщение | `agent_error`, `rain_status_unavailable` или transport error | `response.body.error.code` от `POST /dialog/message`; при network error frontend ставит локальный код transport-сбоя | `Не удалось отправить сообщение агенту.` | внутри окна |
| Run завершился timeout | `generation_timeout` или `agent_timeout` | `DialogSessionView.error.code` из `GET /dialog/status?session_id=...`, нормализованный backend из terminal status/error RAIN | `Агент долго не отвечает. Попробуйте перезапустить сессию или повторить позже.` | внутри окна |
| Run завершился ошибкой | `agent_error` | `DialogSessionView.error.code` из `GET /dialog/status?session_id=...`, нормализованный backend из `RAIN RunStatusResponse.error.code` | `Не удалось получить результат от агента. Попробуйте позже.` | внутри окна |
| Не удалось загрузить историю | `invalid_cursor`, `session_not_found` или transport error | `response.body.error.code` от `GET /dialog/messages`; при network error frontend ставит локальный код transport-сбоя | `Не удалось загрузить историю диалога.` | область истории |

## Нефункциональные требования к UI

- accessibility / keyboard / tab order: окно доступно с клавиатуры, blocked composer сообщает причину недоступности;
- responsive behavior: окно остаётся удобным при параллельной работе со списком, деталью и формой редактирования;
- performance expectations: initial history load ограничен страницей сообщений и не должен рендерить всю историю сразу;
- audit / trace / telemetry if needed: можно логировать отправку сообщения, polling terminal status и ошибки UI.

## Критерии приемки

### FE-AC-1. Async run
- [ ] Отправка сообщения возвращает быстрый `202 Accepted` без ожидания полного ответа RAIN
- [ ] Frontend polling-ом через `GET /dialog/status?session_id=...` получает terminal `dialog_status`
- [ ] Composer заблокирован до terminal status

### FE-AC-2. Статусы и ошибки
- [ ] При `agent_status != ready` composer и actions недоступны
- [ ] При active run повторная отправка недоступна
- [ ] Timeout и ошибка показываются понятным сообщением

### FE-AC-3. История и ограничения
- [ ] При открытии окна загружается только последняя страница истории
- [ ] Более ранняя история догружается через cursor
- [ ] При новом сообщении во время просмотра старой истории scroll-position не сбрасывается, а UI показывает индикатор нового сообщения
- [ ] Индикатор нового сообщения появляется на основе `acknowledged_latest_message_id`, `current_latest_message_id` и latest page, даже если нижние сообщения выгружены из DOM
- [ ] Индикатор нового сообщения исчезает после клика по нему или самостоятельного возврата пользователя к нижней границе истории
- [ ] Prompt длиннее лимита нельзя отправить
- [ ] Большое сообщение агента не ломает вёрстку окна

## Открытые вопросы и допущения

- Лимит пользовательского `message` согласован как `3000` символов и должен быть одинаковым на frontend, backend АС КОДА и RAIN-side валидации.
- Если RAIN позже предоставит streaming/status API, polling нашего backend можно заменить SSE без изменения пользовательского сценария.

## Связанный прототип

- `../delivery-prototype/prototype.html`
- `../delivery-prototype/notes.md`
