# Создание и редактирование внедрения (Бэкенд)

Статус: **актуализировано после реализации**
Фича: `deployments`
Срез: `form-editing`
Область: `MVP`
Дата обновления: `2026-05-22`
Шаблон: `.workflow/templates/requirements/backend.template.md`

## Цель среза

Зафиксировать контракт создания/обновления: бэкенд создаёт внедрение сразу как `NEW`, без черновика-оболочки и без вложенного сохранения скоркарт/артефактов.

## Фрагмент OpenAPI

```yaml
paths:
  /api/v1/deployment:
    post:
      tags: [Deployments]
      summary: Создание внедрения
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: '#/components/schemas/CreateDeployment' }
      responses:
        '201': { description: Created }
  /api/v1/deployment/{number}:
    put:
      parameters:
        - name: id
          in: query
          required: true
          schema: { type: string }
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: '#/components/schemas/UpdateDeployment' }
```

## `CreateDeployment`

| Поле | Обязательность | Правило |
|---|---|---|
| `spaceCode` | да | код пространства |
| `name` | да | до 1000 символов по OpenAPI |
| `goal` | нет | цель |
| `changeDescription` | нет | описание изменений |
| `applicationPerimeter` | нет | периметр |
| `deploymentType` | нет/по UI | `GENERAL` или `SIMULATION_BASED` |
| `lineageSimulationId` | для `SIMULATION_BASED` | UUID симуляции |

## `UpdateDeployment`

| Поле | Правило |
|---|---|
| `name` | можно изменить, до 255 символов по OpenAPI |
| `goal` | можно изменить |
| `changeDescription` | можно изменить |
| `applicationPerimeter` | можно изменить |

`UpdateDeployment` не принимает вложенные скоркарты/артефакты и не должен менять `deploymentType`/`lineageSimulationId`.

## Правила бэкенда

- После создания: `status=NEW`, `version=1`, `isLast=true`.
- Не создаём технический `draft-shell` и не запускаем таймер автоудаления.
- Скоркарты и артефакты привязываются отдельными API после появления `deployment.id`.
- Редактирование в `NEW` создаёт новую строку в `deployments` со статусом `NEW`.
- Редактирование в `ON_APPROVAL` создаёт новую строку в `deployments` со статусом `NEW`, если бэкенд разрешил `edit`; согласование считается снятым/сброшенным.
- `DEPLOYED`, `REJECTED`, `ARCHIVED` не редактируются через обновление формы.
- Методолог не имеет права создавать/обновлять поля внедрения, скоркарты и ЖЦ в контуре внедрений; для него разрешено только редактирование артефактов через общий контур артефактов.

## Пример создания

```json
{
  "spaceCode": "CC",
  "name": "Внедрение стратегии Премиум",
  "goal": "Перевести изменение в продуктив",
  "changeDescription": "Изменены веса факторов",
  "applicationPerimeter": "Новые заявки Премиум",
  "deploymentType": "GENERAL"
}
```

## Ошибки

| Код | Условие |
|---|---|
| `400` | пустой `spaceCode`/`name`, неверное тело запроса |
| `404` | строка/версия внедрения не найдена при обновлении |
| `409` | обновление в недопустимом статусе, изменение неизменяемых полей |
| `500` | внутренняя ошибка |

## Чеклист для тестирования среза

- [ ] Создание без скоркарт/артефактов успешно при валидных `spaceCode` и `name`.
- [ ] Создание возвращает `NEW`, а не `draft`.
- [ ] Обновление меняет только разрешённые поля.
- [ ] Обновление не принимает `scorecard_version_ids`, `artifacts`, `criticality` как поля `UpdateDeployment`.
- [ ] Изменение `deploymentType` после фиксации отклоняется.
- [ ] Обновление конечного статуса отклоняется.
- [ ] Обновление из `ON_APPROVAL` возвращает внедрение в `NEW`.
