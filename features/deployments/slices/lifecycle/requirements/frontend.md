# Жизненный цикл внедрения (Frontend)

Статус: **draft**  
Feature: `deployments`  
Slice: `lifecycle`  
Область: `MVP`  
Дата обновления: `2026-04-27`  
Шаблон: `.workflow/templates/requirements/frontend.template.md`

## Связь с feature-level документом

- Главный контрольный документ: `../../requirements.md`
- Этот файл детализирует раздел `Реализация для FRONTEND` для текущего slice.

## Назначение пакета

- Зафиксировать UI-правила отображения status и lifecycle actions для deployment.
- Синхронизировать UI с backend process and lifecycle model.

## Источники и трассировка

### Основные источники

- `../slice.md`
- `../../requirements.md`
- `../../feature.md`
- `../../references.md`
- `requirements/backend.md`

### Связанные planning stories

- `STORY-DEPLOYMENTS-005`

## Контекст и бизнес-смысл

### Цель

Пользователь должен видеть текущее lifecycle-состояние внедрения и вызывать только допустимые действия.

### Пользователи и роли

- автор внедрения;
- участники approval flow;
- `admin`.

## Границы MVP

### Входит в MVP

- отображение status;
- lifecycle buttons;
- блокировка недопустимых действий;
- UX вокруг submit/recall/deploy/archive/rollback там, где это допускается.

### Не входит в MVP

- локальная frontend state machine, отличная от backend.

## Пользовательские сценарии

### Сценарий FE-1. Просмотр lifecycle state
1. Пользователь открывает deployment host screen.
2. UI показывает текущий status.
3. UI вычисляет доступные actions по backend state и ролям.

### Сценарий FE-2. Запуск lifecycle action
1. Пользователь выбирает допустимое действие.
2. UI отправляет запрос в backend.
3. После ответа status и actions обновляются.

## UI-состав и навигация

### Экран/состояние 1. Lifecycle action area

- Назначение: показать status и actions.
- Откуда открывается: из detail/form host screens.
- Куда ведёт: к lifecycle endpoints и смежным dialogs.
- Что видно пользователю: status badge, actions, reasons/errors.
- Какие действия доступны: зависят от status и роли.

## Функциональные требования

### FE-FR-1. Display by source-of-truth

**Описание:**
UI показывает lifecycle state по backend данным без локального переопределения.

### FE-FR-2. Action gating

**Описание:**
Недопустимые действия скрываются или disabled.

## Интеграция с Backend API

| Метод и маршрут | Где используется | Что отправляем/читаем | Условия вызова | Примечание |
|---|---|---|---|---|
| lifecycle endpoints из backend pack | detail/form host screens | action payload и status | только в допустимом status | source-of-truth на backend |

## Валидация на frontend

### Правила

- нельзя вызвать lifecycle action повторно во время pending state;
- rollback требует причину, если это закреплено backend contract.

### Сообщения об ошибках

| Ситуация | Сообщение | Где показываем |
|---|---|---|
| недопустимое действие | `Действие недоступно в текущем статусе` | action area |
| ошибка backend | `Не удалось изменить статус внедрения` | toast / inline |

## Критерии приемки

### FE-AC-1. Correct action set
- [ ] На экране доступны только допустимые lifecycle actions

### FE-AC-2. Status sync
- [ ] UI не расходится с backend status model
