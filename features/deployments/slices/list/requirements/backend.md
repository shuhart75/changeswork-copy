# Список внедрений (Backend)

Статус: **draft**  
Feature: `deployments`  
Slice: `list`  
Область: `MVP`  
Дата обновления: `2026-04-27`  
Шаблон: `.workflow/templates/requirements/backend.template.md`

## Связь с feature-level документом

- Главный контрольный документ: `../../requirements.md`
- Этот файл детализирует раздел `Реализация BACKEND` для текущего slice.

## Назначение пакета

- Описать list API и правила выборки внедрений для пользовательского списка.
- Согласовать поля списка со status model и product filtering.

## Источники и трассировка

### Основные источники

- `../slice.md`
- `../../requirements.md`
- `../../feature.md`
- `../../references.md`
- `../requirements/frontend.md`

### Связанные planning stories

- `STORY-DEPLOYMENTS-002`

## Контекст и бизнес-смысл

### Цель

Backend должен возвращать список внедрений в виде, достаточном для list screen: status, criticality, author, creation/deployment dates и базовые identifying fields.

### Источник правды

- deployment aggregate;
- approval state для process-driven statuses.

## Бизнес-правила и системные ограничения

### BR-1. Источник process status
- после отправки из `draft` list status определяется по `ApprovalInstance.status`;
- конечные состояния `deployed` и `archived` отображаются отдельно.

### BR-2. Product filtering
- список должен поддерживать фильтрацию по продукту;
- product visibility подчиняется RBAC rules.

## Границы MVP

### Входит в MVP

- list endpoint;
- product filter;
- stable set of list fields;
- сортировка и пагинация там, где они уже зафиксированы в фронтовом пакете.

### Не входит в MVP

- произвольная analytics-агрегация;
- расширенные пользовательские представления вне detail packs.

## Пользовательские и системные сценарии

### Сценарий BE-1. Получение списка
1. Клиент запрашивает deployments list.
2. Backend собирает данные deployment и process status.
3. Backend возвращает список с полями, достаточными для таблицы.

### Сценарий BE-2. Применение фильтра
1. Клиент передаёт product filter и другие допустимые параметры.
2. Backend ограничивает выборку.
3. Возвращается отфильтрованный набор.

## Функциональные требования

### BE-FR-1. List response contract

**Описание:**
List response содержит идентификатор, название, тип, статус, критичность, автора и даты.

**Правила и ограничения:**
- не допускается локальное frontend-вычисление процессного статуса;
- поля должны быть стабильны для list screen.

### BE-FR-2. Filtering and visibility

**Описание:**
List endpoint учитывает RBAC и product scope.

## Модель данных

### Основные сущности и поля

| Сущность / таблица | Поле | Тип | Обязательность | Описание |
|---|---|---|---|---|
| `deployment` | `id`, `name`, `product_id`, `created_at`, `deployed_at` | domain | да | базовые list fields |
| `approval_instance` | `status` | process | нет | источник process status после submit |

## API-контракт

### Эндпоинты

| Метод и маршрут | Назначение | Кто вызывает | Примечание |
|---|---|---|---|
| `GET /api/v1/deployments` | список внедрений | frontend list screen | поддерживает фильтрацию |

## Ошибки и валидация

### Валидационные правила

- неподдерживаемые filter params отклоняются;
- недопустимый доступ ограничивает набор данных или возвращает ошибку доступа.

### Ошибки API

| Код/сценарий | Условие | Ответ |
|---|---|---|
| `400` | невалидный фильтр | сообщение о невалидных параметрах |
| `403` | нет доступа к scope | ошибка доступа |

## Критерии приемки

### BE-AC-1. Stable list contract
- [ ] List endpoint возвращает поля, достаточные для таблицы внедрений

### BE-AC-2. Status and filter logic
- [ ] Process status и product filtering рассчитываются на backend
