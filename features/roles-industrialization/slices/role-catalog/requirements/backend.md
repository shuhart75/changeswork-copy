# Каталог ролей и совместимость (Бэкенд)

Статус: **draft**
Фича: `roles-industrialization`
Срез: `role-catalog`
Область: `MVP`
Дата обновления: `2026-06-01`
Формат: **новый лёгкий**
Шаблон: `.workflow/templates/requirements/backend.readable.template.md`

## Цель среза

Зафиксировать backend-каталог ролей, product scope и compatibility rules как основу для endpoint authorization.

## Источники

- Главный документ: `../../requirements.md`
- Карточка среза: `../slice.md`
- OpenAPI: `GET /api/v1/user`, `GET /api/v1/access`
- Модель данных: role catalog, role-space mapping, incompatible roles
- Доменные решения: `../../domain-impact.md`

## Контракт API

| Метод | Маршрут | Операция | Запрос | Ответ |
|---|---|---|---|---|
| `GET` | `/api/v1/user` | получить профиль пользователя | `employeeNumber` или текущий контекст пользователя | роли пользователя и связанные продуктовые коды |
| `GET` | `/api/v1/access` | проверить наличие доступа | `accessType`, опционально `spaceCode` | `allow/deny` для requested role context |

### OpenAPI-фрагмент

```yaml
openapi: 3.0.3
paths:
  /api/v1/user:
    get:
      summary: Получить роли пользователя
  /api/v1/access:
    get:
      summary: Проверить доступ по роли и продукту
components:
  schemas:
    RoleAssignment:
      type: object
      properties:
        roleCode:
          type: string
        scopeType:
          type: string
          enum: [global, product]
        spaceCode:
          type: string
          nullable: true
```

## Модель данных

| Сущность / таблица | Поле | Тип | Обяз. | По умолчанию | Комментарий |
|---|---|---|---:|---|---|
| `role_catalog` | `role_code` | string | да |  | код роли или role pattern |
| `role_catalog` | `scope_type` | enum | да |  | `global` или `product` |
| `role_space_mapping` | `space_code` | string | нет |  | обязателен для product-scoped roles |
| `role_catalog` | `role_family` | enum | да |  | `auditor`, `limited_view`, `admin`, `editor`, `metodolog`, `simulation_specialist` |
| `incompatible_roles` | `left_role_code` | string | да |  | одна сторона пары несовместимости |
| `incompatible_roles` | `right_role_code` | string | да |  | вторая сторона пары несовместимости |

## Бизнес-правила и инварианты

| Правило | Поведение бэкенда |
|---|---|
| Global role не требует `space.code` | backend не ожидает product mapping для `auditor`, `experiment_limited_view`, `experiment_admin` |
| Product role требует `space.code` | без продуктового кода роль не даёт product-scoped доступ |
| `experiment_editor_{space.code}` может пересекаться с таким же семейством по другим продуктам | backend допускает агрегирование нескольких editor assignments |
| Остальные роли не должны молча совмещаться вне compatibility rules | backend должен валидировать назначения по compatibility matrix |
| `simulation_specialist_{space.code}` ограничен simulation-контуром | backend разрешает роли simulation CRUD, lifecycle actions и документы симуляции только в пределах её `space.code` |
| `simulation_specialist_{space.code}` не расширяется до соседних доменов | backend возвращает `403` на pilot/space/deployment/admin operations, даже если у пользователя нет других ролей |

## Примеры

### Успешный запрос

```http
GET /api/v1/user?employeeNumber=12345 HTTP/1.1
```

```json
{
  "roles": [
    {
      "roleCode": "experiment_editor_CC",
      "scopeType": "product",
      "spaceCode": "CC"
    },
    {
      "roleCode": "simulation_specialist_CC",
      "scopeType": "product",
      "spaceCode": "CC"
    }
  ]
}
```

### Семантика новой роли

- `simulation_specialist_{space.code}` добавляется в role catalog как отдельное product-scoped семейство.
- Для этой роли backend должен уметь различать как минимум:
  - simulation read: list/detail/report-related reads;
  - simulation write: create/update/delete;
  - simulation lifecycle: start/cancel or equivalent `DoSimulationAction`;
  - simulation documents: просмотр и редактирование документов симуляции.
- Доступ к каждой из этих групп разрешён только если `space.code` симуляции совпадает с product scope роли.

## Ошибки

| HTTP | Условие | Что проверяет тестировщик |
|---|---|---|
| `400` | некорректный `spaceCode` или `accessType` | неизвестный код роли/продукта не трактуется как валидный доступ |
| `403` | пользователь не имеет requested role context | backend не отдаёт повышенный доступ без role match |
| `404` | пользователь не найден | отсутствие пользователя не маппится в пустой успешный профиль |
| `409` | обнаружено запрещённое совмещение ролей | compatibility matrix реально применяется |
| `500` | внутренняя ошибка каталога ролей | ошибка не превращается в allow-by-default |

## Чеклист для тестирования среза

- [ ] Все маршруты доступны и соответствуют OpenAPI.
- [ ] Обязательные поля валидируются на бэкенде.
- [ ] Недоступные действия возвращают ожидаемую ошибку.
- [ ] Права ролей проверяются на бэкенде, а не только на фронте.
- [ ] Данные сохраняются в актуальной модели данных.
- [ ] Старые статусы, поля и маршруты не принимаются, если срез заменяет прежнюю логику.

## Открытые вопросы и допущения

- Точный формат хранения compatibility matrix в persistent model будет уточняться на реализации; в living requirements сейчас важны сами инварианты, а не конкретная схема миграции.
