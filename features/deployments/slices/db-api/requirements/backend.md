# БД/API контракт внедрения (Бэкенд)

Статус: **актуализировано после реализации**
Фича: `deployments`
Срез: `db-api`
Область: `MVP`
Дата обновления: `2026-06-08`
Шаблон: `.workflow/templates/requirements/backend.template.md`

## Цель среза

Дать разработчикам и тестировщикам короткий, проверяемый контракт по API и модели данных внедрений.

## Источники

- API: `/home/reutov/Downloads/rscon-api.yaml`, тег `Deployments`.
- Модель данных: `/home/reutov/Downloads/111.xlsx`, таблица `deployments`.

## Маршруты

| Метод | Маршрут | Операция | Запрос | Ответ |
|---|---|---|---|---|
| `POST` | `/api/v1/deployments?spaceCode=...` | `getDeployments` | `GetDeploymentRegistry` | `DeploymentRegistry` |
| `POST` | `/api/v1/deployment` | `createDeployment` | `CreateDeployment` | `DeploymentOperationResult` |
| `GET` | `/api/v1/deployment/{number}` | `getDeploymentByNumber` | — | `Deployment` |
| `PUT` | `/api/v1/deployment/{number}?id=...` | `updateDeployment` | `UpdateDeployment` | `DeploymentOperationResult` |
| `DELETE` | `/api/v1/deployment/{number}` | `deleteDeployment` | — | `DeploymentOperationResult` |
| `GET` | `/api/v1/deployment/id/{id}` | `getDeploymentById` | — | `Deployment` |
| `PUT` | `/api/v1/deployment/{number}/action?id=...&action=...` | `doDeploymentAction` | параметры запроса | `DeploymentOperationResult` |

## Сводка DTO

### Перечисления

```yaml
DeploymentMode: [GENERAL, SIMULATION_BASED]
DeploymentStatus: [NEW, ON_APPROVAL, REJECTED, DEPLOYED, ARCHIVED]
DeploymentCriticality: [HIGH, LOW]
DeploymentAction: [submitForApproval, edit, deploy, toArchive]
```

### `CreateDeployment`

```yaml
required: [spaceCode, name]
properties:
  spaceCode: string
  name: string # maxLength 1000
  goal: string
  changeDescription: string
  applicationPerimeter: string
  deploymentType: DeploymentMode
  lineageSimulationId: uuid
```

### `UpdateDeployment`

```yaml
properties:
  name: string # maxLength 255
  goal: string
  changeDescription: string
  applicationPerimeter: string
```

### `Deployment`

```yaml
properties:
  id: uuid
  number: string
  spaceCode: string
  name: string
  goal: string
  changeDescription: string
  applicationPerimeter: string
  deploymentType: DeploymentMode
  lineageSimulation: SimulationReference
  status: DeploymentStatus
  criticality: DeploymentCriticality
  availableActions: DeploymentAvailableAction[]
  version: integer
  isLast: boolean
  initialCreateDateTime: date-time
  createdDateTime: date-time
  updateDateTime: date-time
  authorEmployee: string
  employeeNumber: string
```

## Модель данных и инварианты

### Единственная таблица

В текущей модели данных для внедрений есть только одна таблица: `deployments`. Отдельной таблицы версий нет; версии представлены строками `deployments` с общим `number`, увеличивающимся `version` и флагом `is_last`.

| # | Колонка | Тип | Обяз. | По умолчанию | Комментарий |
|---:|---|---|---:|---|---|
| 1 | `id` | `uuid` | да | — | UUID внедрения |
| 2 | `number` | `varchar(255)` | да | — | Номер внедрения |
| 3 | `space_code` | `varchar(10)` | да | — | Код пространства |
| 4 | `deployment_type` | `varchar(50)` | да | — | Тип внедрения |
| 5 | `lineage_simulation_id` | `uuid` | нет | — | ID симуляции для `SIMULATION_BASED` |
| 6 | `name` | `varchar(255)` | да | — | Название |
| 7 | `goal` | `varchar(2000)` | нет | — | Цель |
| 8 | `change_description` | `varchar(2000)` | нет | — | Описание изменений |
| 9 | `application_perimeter` | `varchar(2000)` | нет | — | Периметр применения |
| 10 | `status` | `varchar(50)` | да | — | Статус |
| 11 | `version` | `int4` | да | — | Версия |
| 12 | `is_last` | `bool` | да | — | Признак последней актуальной версии |
| 13 | `employee_number` | `varchar(255)` | нет | — | Табельный номер редактора |
| 14 | `author_employee_number` | `varchar(255)` | да | — | Табельный номер создавшего внедрение |
| 15 | `create_datetime` | `timestamp` | да | — | Дата создания |
| 16 | `initial_create_datetime` | `timestamp` | да | — | Дата заведения первой версии |
| 17 | `update_datetime` | `timestamp` | нет | — | Дата обновления |
| 18 | `criticality` | `varchar(50)` | да | `'LOW'::character varying` | Критичность внедрения |


### Инварианты

| Инвариант | Правило |
|---|---|
| Последняя версия | для актуальной строки `is_last=true`; старые строки того же `number` получают `is_last=false` |
| Создание | первая строка имеет `version=1`, `status=NEW`, `is_last=true` |
| Редактирование `NEW` | создаётся новая строка в `deployments`, `version` увеличивается, новый `status=NEW` |
| Редактирование `ON_APPROVAL` | создаётся новая строка в `deployments`, `version` увеличивается, новый `status=NEW` |
| Согласование | решения и комментарии выполняются в SberDocs через `features/approvals`, а не локальными действиями `approve`/`reject` Deployments |
| `deployment_type` | обязательно в БД; значение из `DeploymentMode` |
| `criticality` | обязательно в БД, по умолчанию `LOW`; вручную в запросах создания/обновления не передаётся |
| Связь со скоркартами | живёт в контуре скоркарт, привязка через `entityType=deployment`, `entityId` |
| Связь с артефактами | живёт в общем контуре артефактов, доступна после создания deployment; это единственный контур редактирования для методолога |

## Примеры

### Создание

```http
POST /api/v1/deployment HTTP/1.1
Content-Type: application/json
```

```json
{
  "spaceCode": "CC",
  "name": "Внедрение стратегии Премиум",
  "goal": "Перевести изменение в продуктив",
  "changeDescription": "Обновлены пороги отсечения и веса факторов",
  "applicationPerimeter": "Новые заявки Премиум",
  "deploymentType": "GENERAL"
}
```

### Действие

```http
PUT /api/v1/deployment/DEP-001/action?id=550e8400-e29b-41d4-a716-446655440000&action=submitForApproval HTTP/1.1
```

## Ошибки

| HTTP | Проверка |
|---|---|
| `400` | проверка схемы, неизвестное перечисление или действие |
| `403` | нет прав |
| `404` | строка/версия внедрения или симуляция не найдена |
| `409` | недопустимый переход, неизменяемое поле, нарушение правила второй руки, конфликт связи с симуляцией |
| `500` | внутренняя ошибка |

## Чеклист для тестирования среза

- [ ] Все маршруты из таблицы API доступны и соответствуют методам OpenAPI.
- [ ] `GET /api/v1/deployments` из старых требований заменён на `POST /api/v1/deployments`.
- [ ] `POST /api/v1/deployments` из старых требований заменён на `POST /api/v1/deployment` для создания.
- [ ] Маршрут действия использует `PUT`, `/deployment/{number}/action` в единственном числе и параметры запроса `id` и `action`.
- [ ] `CreateDeployment` не требует скоркарт/артефактов.
- [ ] `UpdateDeployment` не содержит скоркарт/артефактов.
- [ ] В БД для внедрений используется только таблица `deployments`, без отдельной таблицы версий.
- [ ] В перечислениях API нет `draft`, `approved`, `ratified`, `cancelled`, `recall`, `start_ratification`, локальных `approve`/`reject`.
- [ ] Для методолога API внедрений не разрешает создание, обновление и действия ЖЦ, кроме связанных операций артефактов в общем контуре.
