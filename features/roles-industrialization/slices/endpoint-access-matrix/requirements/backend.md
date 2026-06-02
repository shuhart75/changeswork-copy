# Матрица доступа к endpoint (Бэкенд)

Статус: **draft**
Фича: `roles-industrialization`
Срез: `endpoint-access-matrix`
Область: `MVP`
Дата обновления: `2026-06-01`
Формат: **новый лёгкий**
Шаблон: `.workflow/templates/requirements/backend.readable.template.md`

## Цель среза

Зафиксировать backend source-of-truth для endpoint-level authorization по новой промышленной ролевой модели.

## Источники

- Главный документ: `../../requirements.md`
- Карточка среза: `../slice.md`
- OpenAPI: domain endpoints experiments/spaces/simulations/documents/files
- Модель данных: `endpoint_role_access`
- Доменные решения: `../../domain-impact.md`

## Контракт API

| Метод | Маршрут | Операция | Запрос | Ответ |
|---|---|---|---|---|
| `POST` | `/api/v1/experiment` | createExperiment | payload эксперимента + user context | created / access denied |
| `PUT` | `/api/v1/space/{code}` | updateSpace | payload пространства + product context | updated / access denied |
| `POST` | `/api/v1/simulation` | createSimulation | payload симуляции + product context | created / access denied |
| `PUT` | `/api/v1/simulation/{id}` | updateSimulation | payload симуляции + product context | updated / access denied |
| `DELETE` | `/api/v1/simulation/{id}` | deleteSimulation | simulation id + product context | deleted / access denied |
| `PUT` | `/api/v1/simulation/{id}/action` | doSimulationAction | action + product context | transitioned / access denied |
| `GET` | `/api/v1/simulation/{id}` | getSimulationById | simulation id + user context | detail / access denied |
| `GET` | `/api/v1/simulations` | getSimulations | filters + user context | list / access denied |
| `GET` | `/api/v1/simulation-filters` | getSimulationFilters | user context | filters / access denied |
| `GET` | `/api/v1/risk-parameters` | getRiskParameters | user context + product context | parameters / access denied |
| `PUT` | `/api/v1/risk-parameters` | updateRiskParameters | payload + product context | updated / access denied |
| `POST` | `/api/v1/simulation-documents` | createSimulationDocument | document payload + parent simulation context | created / access denied |
| `POST` | `/api/v1/file` | uploadFile | file + parent entity context | uploaded / access denied |

### OpenAPI-фрагмент

```yaml
openapi: 3.0.3
paths:
  /api/v1/experiment:
    post:
      summary: Create experiment
  /api/v1/space/{code}:
    put:
      summary: Update space
  /api/v1/simulation:
    post:
      summary: Create simulation
  /api/v1/simulation/{id}:
    put:
      summary: Update simulation
    delete:
      summary: Delete simulation
  /api/v1/simulation/{id}/action:
    put:
      summary: Apply simulation action
components:
  schemas:
    EndpointAccessRule:
      type: object
      properties:
        operation:
          type: string
        roleCode:
          type: string
        accessMode:
          type: string
          enum: [allow, allow_in_space, deny]
```

## Модель данных

| Сущность / таблица | Поле | Тип | Обяз. | По умолчанию | Комментарий |
|---|---|---|---:|---|---|
| `endpoint_role_access` | `operation_code` | string | да |  | канонический код операции |
| `endpoint_role_access` | `role_code` | string | да |  | конкретная роль или role pattern |
| `endpoint_role_access` | `access_mode` | enum | да | `deny` | `allow`, `allow_in_space`, `deny` |
| `endpoint_role_access` | `space_bound` | boolean | да | `false` | требует ли операция совпадения `space.code` |
| `endpoint_role_access` | `domain_scope` | enum | да |  | `simulation`, `pilot`, `space`, `deployment`, `shared_dictionary`, `document` |

## Бизнес-правила и инварианты

| Правило | Поведение бэкенда |
|---|---|
| Read-only роли не мутируют данные | create/edit/delete/action endpoints возвращают `403` |
| `experiment_admin` имеет полный доступ | backend не ограничивает роль продуктом |
| Product-scoped роль проходит только при совпадении `space.code` | backend валидирует product context до доменной мутации |
| Одна и та же operation должна иметь единое правило | FE и BE не расходятся по одному endpoint |
| Файлы и документы наследуют доступ от родительской сущности | доступ к file/doc endpoint проверяется через parent context |
| `simulation_specialist_{space.code}` разрешён только в simulation domain | backend даёт роли `allow_in_space` на simulation reads/writes/actions и `deny` на pilot/space/deployment mutations |
| Документы симуляции доступны через parent simulation scope | backend валидирует право на родительскую симуляцию до create/update/delete документа |
| Simulation dictionaries доступны по product scope | filters/risk parameters открываются роли только для её product context |

## Примеры

### Успешный запрос

```http
POST /api/v1/simulation HTTP/1.1
Content-Type: application/json
```

```json
{
  "spaceCode": "CC",
  "number": "SIM-001"
}
```

### Матрица для `simulation_specialist_{space.code}`

| Группа операций | Ожидаемый access mode |
|---|---|
| `getSimulations`, `getSimulationById`, `getSimulationByNumber`, `SimulationGetReport`, `getPilotsForSimulation` | `allow_in_space` |
| `createSimulation`, `updateSimulation`, `deleteSimulation`, `DoSimulationAction`, `SimulationApplyChanges` | `allow_in_space` |
| `getSimulationFilters`, `getRiskParameters`, `updateRiskParameters` | `allow_in_space` |
| документы симуляции (`getDocuments`, `createDocuments`, file operations с parent simulation) | `allow_in_space` |
| `createExperiment`, `editExperiment`, `createSpace`, `updateSpace`, deployment mutations | `deny` |

## Ошибки

| HTTP | Условие | Что проверяет тестировщик |
|---|---|---|
| `400` | operation не получила нужный product context | без `space.code` product-scoped мутация не проходит |
| `403` | роль не разрешена для операции | read-only и чужие product roles не обходят правило |
| `404` | сущность или product context не найдены | backend не переводит это в allow |
| `409` | compatibility/state conflict | несовместимые или конфликтующие access conditions отражаются явно |
| `500` | внутренняя ошибка authorization layer | ошибка не расширяет доступ |

## Чеклист для тестирования среза

- [ ] Все маршруты доступны и соответствуют OpenAPI.
- [ ] Обязательные поля валидируются на бэкенде.
- [ ] Недоступные действия возвращают ожидаемую ошибку.
- [ ] Права ролей проверяются на бэкенде, а не только на фронте.
- [ ] Данные сохраняются в актуальной модели данных.
- [ ] Старые статусы, поля и маршруты не принимаются, если срез заменяет прежнюю логику.

## Открытые вопросы и допущения

- Полный машиночитаемый список operation codes будет удобнее выделить отдельным контрактным артефактом ближе к реализации, но в living requirements уже зафиксированы группы endpoint и semantics доступа.
- В этом пакете используется каноническое имя роли из источника: `simulation_specialist_{space.code}`. Если в коде или Jira появится вариант `simulations_specialist`, его нужно трактовать как неканоничный алиас и не закреплять в source-of-truth.
