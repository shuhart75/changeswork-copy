# Core approval/ratification процесс (Frontend)

Статус: **draft**  
Feature: `approvals`  
Slice: `core-process`  
Область: `MVP`  
Дата обновления: `2026-04-27`  
Шаблон: `.workflow/templates/requirements/frontend.template.md`

## Связь с feature-level документом

- Главный контрольный документ: `../../requirements.md`
- Этот файл детализирует раздел `Реализация для FRONTEND` для текущего slice.

## Назначение пакета

- Зафиксировать, как frontend отображает approval/ratification states и процессные действия на host screens.
- Согласовать пользовательские статусы с `ApprovalInstance`.
- Не допустить локальной переинтерпретации backend status model.

## Источники и трассировка

### Основные источники

- `../slice.md`
- `../../requirements.md`
- `../../feature.md`
- `../../references.md`
- `requirements/backend.md`

### Связанные planning stories

- `STORY-APPROVALS-001`

### Связанные артефакты

- Feature requirements: `../../requirements.md`
- Domain impact: `../../domain-impact.md`

## Контекст и бизнес-смысл

### Цель

Показать пользователю текущий этап согласования, доступные решения и последствия этих решений на host screens `Pilot` и `Deployment`.

### Пользователи и роли

- автор доменной версии;
- `approver`;
- `ratifier`;
- `admin`.

### Бизнес-контекст

Frontend не владеет процессной логикой. Он читает состояние из `ApprovalInstance` и отображает его единообразно.

## Границы MVP

### Входит в MVP

- отображение approval/ratification statuses;
- кнопки process actions в допустимых состояниях;
- показ комментариев и причин отклонения;
- read-only history fragments там, где они есть на host screens.

### Не входит в MVP

- отдельный visual workflow designer;
- локальные frontend-статусы сверх backend source-of-truth.

## Пользовательские сценарии

### Сценарий FE-1. Просмотр состояния процесса
1. Пользователь открывает host screen.
2. UI читает `ApprovalInstance.status`.
3. UI показывает русскоязычный label и доступные действия.

### Сценарий FE-2. Принятие решения
1. Назначенный пользователь выбирает action.
2. UI запрашивает комментарий, если это требуется сценарием.
3. После ответа backend экран обновляет процессный статус.

## UI-состав и навигация

### Экран/состояние 1. Host screen action area

- Назначение: показать process state и actions.
- Откуда открывается: из `Pilot` / `Deployment`.
- Куда ведёт: к выполнению process action или к page-level approval workspace.
- Что видно пользователю: status badge, actions, comments, errors.
- Какие действия доступны: submit, approve, reject, recall, start ratification.

## Функциональные требования

### FE-FR-1. Единое отображение process status

**Описание:**
Frontend отображает process status только по данным `ApprovalInstance`.

**Детали:**
- не вычисляет промежуточные состояния локально;
- одинаково трактует statuses на всех host screens;
- показывает reject/cancel states раздельно.

### FE-FR-2. Ограничение действий по роли и статусу

**Описание:**
UI показывает только допустимые действия.

**Детали:**
- `approver` видит approval actions;
- `ratifier` видит ratification actions;
- автор видит submit/recall там, где это допустимо.

## Интеграция с Backend API

| Метод и маршрут | Где используется | Что отправляем/читаем | Условия вызова | Примечание |
|---|---|---|---|---|
| process endpoints из backend pack | host screens | решения, комментарии, текущий status | по допустимому lifecycle | source-of-truth на backend |

## Валидация на frontend

### Правила

- action недоступен, если не подходит роль;
- повторный submit во время pending request блокируется.

### Сообщения об ошибках

| Ситуация | Сообщение | Где показываем |
|---|---|---|
| action недопустим | `Действие недоступно в текущем статусе` | рядом с action area |
| backend reject | `Не удалось выполнить действие согласования` | toast / inline |

## Нефункциональные требования к UI

- единые русскоязычные статусы на всех экранах;
- no local state drift относительно backend process state.

## Критерии приемки

### FE-AC-1. Status source-of-truth
- [ ] Host screens отображают process status только по backend state

### FE-AC-2. Actions by role
- [ ] Пользователь видит и может вызвать только допустимые process actions

## Открытые вопросы и допущения

- page-level approval workspace описан отдельно в `slices/page/`.
