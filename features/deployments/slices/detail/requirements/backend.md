# Детальная карточка внедрения (Бэкенд)

Статус: **актуализировано после реализации**
Фича: `deployments`
Срез: `detail`
Область: `MVP`
Дата обновления: `2026-06-08`
Шаблон: `.workflow/templates/requirements/backend.template.md`

## Цель среза

Отдать проекцию детальной карточки внедрения для фронта: актуальную версию, статус, доступные действия, связь со SberDocs-согласованием и блоки только для чтения.

## Контракт API

```yaml
paths:
  /api/v1/deployment/{number}:
    get:
      tags: [Deployments]
      summary: Получение последней версии внедрения по номеру
      responses:
        '200': { description: OK }
  /api/v1/deployment/id/{id}:
    get:
      tags: [Deployments]
      summary: Получение конкретной версии внедрения по ID
      responses:
        '200': { description: OK }
```

## Проекция `Deployment`

Минимально нужны поля из OpenAPI schema `Deployment`:

| Поле | Для чего нужно FE |
|---|---|
| `id`, `number` | идентификация строки `deployments` и бизнес-номера внедрения |
| `name`, `goal`, `changeDescription`, `applicationPerimeter` | основные поля |
| `spaceCode` | контекст продукта/пространства |
| `deploymentType`, `lineageSimulation` | тип и блок исходной симуляции |
| `status` | чип статуса и действия |
| `criticality` | чип критичности |
| `availableActions` | кнопки действий; не включает локальные `approve`/`reject` для SberDocs-сценария |
| `approvalLink` / `sberdocsSystemNumber` или связанный approval snapshot | ссылка/номер SberDocs для `ON_APPROVAL`, если эти данные отдаются через контур `features/approvals` |
| `version`, `isLast` | версия строки в единственной таблице `deployments` |
| `initialCreateDateTime`, `createdDateTime`, `updateDateTime`, `authorEmployee`, `employeeNumber` | аудит/метаданные |

## Правила сборки блоков

- Скоркарты: возвращаются/читаются из API скоркарт по `entityType=deployment`, `entityId=deployment.id`.
- Артефакты: возвращаются общим контуром артефактов по сущности deployment.
- Связанные сущности: вычисление только для чтения на основании скоркарт и исходной симуляции; ручных связей в API детальной карточки не требуем.
- `availableActions` рассчитываются бэкендом по статусу, роли и ЖЦ. Для методолога действия внедрений не возвращаются; он может только редактировать артефакты через права общего контура артефактов.
- В `ON_APPROVAL` детали согласования, комментарии и решения остаются в SberDocs/`features/approvals`; карточка внедрения показывает только read-only status/link/snapshot.

## Ошибки

| Код | Условие |
|---|---|
| `400` | некорректный `number`/`id` |
| `404` | строка/версия внедрения не найдена |
| `500` | внутренняя ошибка |

## Чеклист для тестирования среза

- [ ] `GET /api/v1/deployment/{number}` возвращает последнюю версию.
- [ ] `GET /api/v1/deployment/id/{id}` возвращает конкретную версию.
- [ ] `availableActions` меняются при смене статуса.
- [ ] Для `ON_APPROVAL` backend не возвращает локальные действия `approve`/`reject`.
- [ ] `DeploymentStatus` не содержит старые значения `draft`, `approved`, `ratified`, `cancelled`.
- [ ] Для `SIMULATION_BASED` поле `lineageSimulation` заполнено, если задан `lineageSimulationId`.
- [ ] Для отсутствующих связанных блоков API/UI дают пустой список, а не ошибку.
