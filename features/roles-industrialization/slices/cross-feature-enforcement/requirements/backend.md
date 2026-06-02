# Перенос в host screens и соседние фичи (Бэкенд)

Статус: **draft**
Фича: `roles-industrialization`
Срез: `cross-feature-enforcement`
Область: `MVP`
Дата обновления: `2026-06-01`
Формат: **новый лёгкий**
Шаблон: `.workflow/templates/requirements/backend.readable.template.md`

## Цель среза

Зафиксировать backend propagation rules: какие соседние доменные контуры должны принимать новую role matrix и как это отражается в deferred consistency.

## Источники

- Главный документ: `../../requirements.md`
- Карточка среза: `../slice.md`
- OpenAPI: соседние host-feature endpoints
- Модель данных: role assignments + endpoint access rules
- Доменные решения: `../../domain-impact.md`

## Контракт API

| Метод | Маршрут | Операция | Запрос | Ответ |
|---|---|---|---|---|
| `GET` | `/api/v1/experiments` | чтение списка пилотов/экспериментов | user context + filters | read-only или scoped data |
| `GET` | `/api/v1/simulations` | чтение симуляций | user context + filters | read-only или scoped data |
| `POST` | `/api/v1/documents` | создание документа | parent entity context | created / access denied |
| `POST` | `/api/v1/files` | загрузка файла | parent entity context | uploaded / access denied |

### OpenAPI-фрагмент

```yaml
openapi: 3.0.3
paths:
  /api/v1/experiments:
    get:
      summary: Получить эксперименты с role-aware фильтрацией
  /api/v1/simulations:
    get:
      summary: Получить симуляции с role-aware фильтрацией
  /api/v1/documents:
    post:
      summary: Создать документ с parent-based RBAC
components:
  schemas:
    RoleAwareScope:
      type: object
      properties:
        roleCode:
          type: string
        spaceCode:
          type: string
          nullable: true
```

## Модель данных

| Сущность / таблица | Поле | Тип | Обяз. | По умолчанию | Комментарий |
|---|---|---|---:|---|---|
| `user_role_assignment` | `role_code` | string | да |  | новая промышленная роль |
| `user_role_assignment` | `space_code` | string | нет |  | обязателен для product-scoped ролей |
| `endpoint_role_access` | `operation_code` | string | да |  | используется соседними контурами |
| `artifact_parent_scope` | `parent_entity_type` | string | да |  | права на документы/файлы наследуются от родителя |

## Бизнес-правила и инварианты

| Правило | Поведение бэкенда |
|---|---|
| Соседние API не используют старую MVP-матрицу как единственный источник | backend должен опираться на новую role matrix после propagation |
| Product-scoped чтение и мутации не расширяются на чужой продукт | фильтрация и authorization используют `space.code` |
| Документы и файлы наследуют parent RBAC | backend не выдаёт отдельные обходные права на artifacts |
| До baseline promotion propagation может быть deferred | impact обязан быть записан в `domain-impact.md` и backlog |

## Примеры

### Успешный запрос

```http
GET /api/v1/simulations?spaceCode=CC HTTP/1.1
```

```json
{
  "items": [
    {
      "number": "SIM-001",
      "spaceCode": "CC"
    }
  ]
}
```

## Ошибки

| HTTP | Условие | Что проверяет тестировщик |
|---|---|---|
| `400` | запрос противоречит ожидаемому role-aware context | API не принимает сломанный role/product context |
| `403` | роль не имеет доступа к соседнему контексту | propagation реально усиливает BE checks |
| `404` | родительская сущность недоступна или не найдена | artifacts не обходят RBAC через parent absence |
| `409` | конфликт между product scope и requested action | backend различает deny и state conflict |
| `500` | внутренняя ошибка propagation layer | ошибка не становится allow |

## Чеклист для тестирования среза

- [ ] Все маршруты доступны и соответствуют OpenAPI.
- [ ] Обязательные поля валидируются на бэкенде.
- [ ] Недоступные действия возвращают ожидаемую ошибку.
- [ ] Права ролей проверяются на бэкенде, а не только на фронте.
- [ ] Данные сохраняются в актуальной модели данных.
- [ ] Старые статусы, поля и маршруты не принимаются, если срез заменяет прежнюю логику.

## Открытые вопросы и допущения

- Полная синхронизация соседних feature packs откладывается отдельным requirements/release проходом, но список target-артефактов уже зафиксирован.
