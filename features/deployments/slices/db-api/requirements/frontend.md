# БД/API контракт внедрения (Фронтенд)

Статус: **актуализировано после реализации**
Фича: `deployments`
Срез: `db-api`
Область: `MVP`
Дата обновления: `2026-06-08`
Шаблон: `.workflow/templates/requirements/frontend.template.md`

## Цель среза

Зафиксировать, как фронт вызывает актуальный API Deployments без старых маршрутов во множественном числе и старых имён в snake_case.

## Краткая памятка API для FE

| UI-сценарий | Метод | Маршрут |
|---|---|---|
| загрузить список | `POST` | `/api/v1/deployments?spaceCode={spaceCode}` |
| создать | `POST` | `/api/v1/deployment` |
| открыть карточку | `GET` | `/api/v1/deployment/{number}` |
| открыть конкретную версию | `GET` | `/api/v1/deployment/id/{id}` |
| сохранить поля | `PUT` | `/api/v1/deployment/{number}?id={id}` |
| выполнить действие | `PUT` | `/api/v1/deployment/{number}/action?id={id}&action={action}` |

## Соответствие DTO -> VM

```typescript
type DeploymentStatus = 'NEW' | 'ON_APPROVAL' | 'REJECTED' | 'DEPLOYED' | 'ARCHIVED';
type DeploymentMode = 'GENERAL' | 'SIMULATION_BASED';
type DeploymentCriticality = 'HIGH' | 'LOW';
type DeploymentAction = 'submitForApproval' | 'edit' | 'deploy' | 'toArchive';

interface DeploymentVm {
  id: string;
  number: string;
  name?: string;
  status: DeploymentStatus;
  deploymentType?: DeploymentMode;
  criticality?: DeploymentCriticality;
  availableActions?: DeploymentAction[];
  version?: number;
  isLast?: boolean;
}
```

## Важные несовместимости со старым текстом

- Не использовать `GET /api/v1/deployments` для списка: в текущем OpenAPI список — `POST /api/v1/deployments`.
- Не использовать `POST /api/v1/deployments` для создания: создание выполняется через `POST /api/v1/deployment`.
- Не использовать `POST /api/v1/deployments/{id}/action`: действие — `PUT /api/v1/deployment/{number}/action?id=...&action=...`.
- Не отправлять `scorecard_version_ids` и `artifacts` в запросы создания/обновления внедрения.
- Не ждать локальный `approvalInstance.status` как источник истины для статуса внедрения: в текущем DTO Deployments есть `status`, а детали согласования читаются из `features/approvals` / SberDocs.
- Не показывать `approve`/`reject` как локальные действия внедрения: решения согласования выполняются в SberDocs.

## Чеклист для тестирования среза

- [ ] Все методы сервисного слоя FE используют маршруты из таблицы.
- [ ] Имена действий в camelCase: `submitForApproval`, `toArchive`.
- [ ] UI не отправляет snake_case `submit_for_approval`/`to_archive`.
- [ ] Перечисление TypeScript не содержит старые статусы/действия, включая локальные `approve`/`reject` для Deployments.
- [ ] Ошибка API не преобразуется в успешное локальное состояние.
