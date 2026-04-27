# Ролевая модель и ограничения доступа (Frontend)

Статус: **draft**  
Feature: `roles`  
Slice: `rbac`  
Область: `MVP`  
Дата обновления: `2026-04-27`  
Шаблон: `.workflow/templates/requirements/frontend.template.md`

## Связь с feature-level документом

- Главный контрольный документ: `../../requirements.md`
- Этот файл детализирует раздел `Реализация для FRONTEND` для текущего slice.

## Назначение пакета

- Описать, как frontend применяет RBAC на уровне экранов, действий и section visibility.
- Не допустить расхождения между FE visibility и backend enforcement.

## Источники и трассировка

### Основные источники

- `../slice.md`
- `../../requirements.md`
- `../../feature.md`
- `../../references.md`
- `requirements/backend.md`

### Связанные planning stories

- imported RBAC scope, без отдельной planning story

## Контекст и бизнес-смысл

### Цель

Frontend должен показывать пользователю только разрешённые разделы, действия и данные в пределах его ролей и product scope.

### Пользователи и роли

- `prm`
- `methodologist`
- `approver`
- `ratifier`
- `admin`

## Границы MVP

### Входит в MVP

- visibility разделов;
- visibility и disabled state действий;
- product-scoped ограничения для UI.

### Не входит в MVP

- UI для администрирования ролей;
- отдельный policy editor.

## Пользовательские сценарии

### Сценарий FE-1. Видимость разделов
1. Пользователь открывает приложение.
2. UI получает его роли и scope.
3. UI показывает только разрешённые разделы и actions.

### Сценарий FE-2. Ограничение действий
1. Пользователь открывает сущность.
2. UI проверяет role/scope.
3. Недопустимые действия скрываются или disabled.

## UI-состав и навигация

### Экран/состояние 1. Navigation and action gating

- Назначение: ограничить разделы и действия по RBAC.
- Откуда открывается: по всей системе.
- Куда ведёт: только в разрешённые разделы.
- Что видно пользователю: доступные меню, кнопки и blocks.
- Какие действия доступны: зависят от role/scope.

## Функциональные требования

### FE-FR-1. Section visibility by role

**Описание:**
UI скрывает недоступные sections и routes.

### FE-FR-2. Action gating by scope

**Описание:**
UI не показывает mutation actions пользователю вне допустимого product scope.

## Интеграция с Backend API

| Метод и маршрут | Где используется | Что отправляем/читаем | Условия вызова | Примечание |
|---|---|---|---|---|
| user/access endpoints | app bootstrap | роли и scope пользователя | при старте и refresh | backend остаётся окончательным арбитром |

## Валидация на frontend

### Правила

- отсутствие роли не должно приводить к показу action;
- отсутствие scope не должно давать mutation actions для product-scoped ролей.

### Сообщения об ошибках

| Ситуация | Сообщение | Где показываем |
|---|---|---|
| действие недоступно | `Недостаточно прав для выполнения действия` | toast / inline |

## Критерии приемки

### FE-AC-1. Role-based visibility
- [ ] Недоступные разделы и actions не показываются пользователю

### FE-AC-2. Product scope
- [ ] Product-scoped ограничения одинаково применяются на host screens
