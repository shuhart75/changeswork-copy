# Список внедрений (Бэкенд)

Статус: **актуализировано после реализации**
Фича: `deployments`
Срез: `list`
Область: `MVP`
Дата обновления: `2026-05-22`
Шаблон: `.workflow/templates/requirements/backend.template.md`

## Цель среза

Отдать фронту реестр внедрений с фильтрами, сортировкой, пагинацией и актуальными статусами.

## Контракт API

```yaml
paths:
  /api/v1/deployments:
    parameters:
      - name: spaceCode
        in: query
        required: true
        schema: { type: string }
    post:
      tags: [Deployments]
      summary: Список внедрений
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: '#/components/schemas/GetDeploymentRegistry' }
      responses:
        '200':
          description: OK
```

## Запрос и ответ

```json
{
  "pagination": { "page": 0, "size": 20 },
  "sort": { "field": "createdDateTime", "direction": "DESC" },
  "filter": {}
}
```

Бэкенд возвращает `DeploymentRegistry.records[]` с полями `DeploymentRecord`: `id`, `number`, `name`, `deploymentType`, `status`, `criticality`, `authorEmployee`, `initialCreateDateTime`, `createdDateTime`, `deployedAt`.

## Правила

- `spaceCode` обязателен.
- В список попадает последняя актуальная версия (`isLast=true`) каждого внедрения.
- `ARCHIVED` по умолчанию можно скрывать только если это явно согласовано фильтром; иначе статус должен быть доступен для отображения.
- Бэкенд не возвращает статусы вне перечисления `DeploymentStatus`.
- Критичность рассчитывается бэкендом и приходит как `HIGH`/`LOW`.

## Ошибки

| Код | Когда |
|---|---|
| `400` | некорректное тело запроса, сортировка, фильтр или пагинация |
| `500` | внутренняя ошибка |

## Чеклист для тестирования среза

- [ ] Без `spaceCode` запрос отклоняется.
- [ ] Ответ содержит только актуальные версии внедрений.
- [ ] Фильтр/сортировка/пагинация работают вместе.
- [ ] В ответе нет `draft`, `ratified`, `cancelled`.
- [ ] Для `NEW`, `ON_APPROVAL`, `REJECTED`, `DEPLOYED`, `ARCHIVED` возвращается корректная строка перечисления.
