# Системные требования — Процесс согласования/утверждения (Approval/Ratification core)

Статус: **для передачи команде**  
Область: MVP  
Дата обновления: 2026-03-21

## Оглавление
1. [Бизнес-требования](#бизнес-требования)
2. [Границы MVP](#границы-mvp)
3. [Пользовательские сценарии](#пользовательские-сценарии)
4. [Критерии приемки](#критерии-приемки)
5. [Функциональные требования](#функциональные-требования)
6. [Описание модели данных](#описание-модели-данных)
7. [Спецификация API (OpenAPI)](#спецификация-api-openapi)
8. [Примеры запросов и ответов](#примеры-запросов-и-ответов)
9. [Ошибки и валидация](#ошибки-и-валидация)
10. [Интеграция и консистентность](#интеграция-и-консистентность)

## Бизнес-требования

### Цель

Система должна реализовать единый процесс согласования и утверждения для версий `Pilot` и `Deployment` через `ApprovalInstance`, чтобы:
- поддерживать `Approval` как опциональную часть маршрута;
- поддерживать обязательный этап `Ratification`;
- поддерживать автоматический и ручной запуск `Ratification`;
- поддерживать пакетное утверждение;
- хранить историю этапов, назначений, решений и переходов статусов;
- давать единый источник истины для страниц `Согласования` и `Пакеты`.

### Источник правды

Основными источниками правил для этой спецификации являются:
- `final-spec/spec_domain_model.md`;
- `final-spec/REQ_roles_rbac.md`;
- `final-spec/REQ_packages_page_backend.md`;
- `final-spec/REQ_approvals_page_backend.md`.

### Бизнес-правила

#### БП-1. Центральная сущность процесса

- Под доменным элементом в рамках процесса согласования понимается версия согласуемой предметной сущности:
  - `PilotVersion`;
  - `DeploymentVersion`.
- Центральной сущностью процесса является `ApprovalInstance`.
- `ApprovalInstance` всегда связан с конкретным доменным элементом:
  - `PILOT_VERSION`;
  - `DEPLOYMENT_VERSION`.
- `Package` не является target `ApprovalInstance`.
- Пакет существует только как рабочая группировка нескольких `ApprovalInstance`.
- `ApprovalInstance` хранит собственный бриф согласования:
  - `brief_subject`;
  - `brief_body`.

#### БП-2. Разделение доменного ЖЦ и approval flow

- Статусы согласования и утверждения принадлежат `ApprovalInstance`.
- Статусы доменного элемента принадлежат его собственной версии (`PilotVersion`, `DeploymentVersion`).
- Доменная версия синхронизирует свой статус с `ApprovalInstance`, но не дублирует свою собственную историю процесса.
- Страница `Согласования` и связанные API читают процесс только из `ApprovalInstance`.

#### БП-3. Обязательность Ratification

- `Ratification` в MVP обязательно для любого элемента.
- `Approval` опционален и может содержать `0..*` последовательных этапов.
- Минимально допустимый маршрут:
  - `0` этапов `Approval`;
  - `1` этап `Ratification`.

#### БП-4. Роли участников

- На этапы `Approval` можно назначать только пользователей с ролью `approver`.
- На этап `Ratification` можно назначать только пользователей с ролью `ratifier`.
- Нельзя выбрать самого себя.
- Проверка ролей выполняется через `rscon-sudir`.

#### БП-5. Бизнес-статусы ApprovalInstance

Система должна использовать бизнес-ориентированные статусы `ApprovalInstance`:
- `in_approval`
- `approved`
- `awaiting_ratification`
- `in_ratification`
- `ratified`
- `approval_rejected`
- `ratification_rejected`
- `approval_cancelled`
- `ratification_cancelled`

#### БП-6. Старт ApprovalInstance

- Если в маршруте есть хотя бы один Approval-этап, при submit создаётся `ApprovalInstance` в статусе `in_approval`.
- Если Approval-этапов нет и `auto_ratification = true`, при submit создаётся `ApprovalInstance` в статусе `in_ratification`.
- Если Approval-этапов нет и `auto_ratification = false`, при submit создаётся `ApprovalInstance` в статусе `awaiting_ratification`.

#### БП-7. Переходы ApprovalInstance

- Если есть `Approval` и `auto_ratification = true`:
  - `in_approval -> approved -> in_ratification -> ratified`
- Если есть `Approval` и `auto_ratification = false`:
  - `in_approval -> approved -> awaiting_ratification -> in_ratification -> ratified`
- Если `Approval` нет и `auto_ratification = true`:
  - `in_ratification -> ratified`
- Если `Approval` нет и `auto_ratification = false`:
  - `awaiting_ratification -> in_ratification -> ratified`

#### БП-8. Reject

- Reject на этапе `Approval` переводит `ApprovalInstance` в `approval_rejected`.
- Reject на этапе `Ratification` переводит `ApprovalInstance` в `ratification_rejected`.
- Комментарий при reject в MVP не обязателен.

#### БП-9. Recall

- Recall обязателен для MVP.
- Recall на этапе `Approval` переводит `ApprovalInstance` в `approval_cancelled`.
- Recall на этапе `Ratification` переводит `ApprovalInstance` в `ratification_cancelled`.
- История процесса сохраняется.
- При повторной отправке после правок создаётся новый `ApprovalInstance` для новой версии доменного элемента.

#### БП-10. Approved и awaiting_ratification

- `approved` означает: все Approval-этапы успешно завершены, Ratification ещё не завершён.
- `awaiting_ratification` означает: Approval завершён или отсутствовал, но Ratification ждёт ручного запуска.
- В пакетизацию попадают только `ApprovalInstance` со статусом `awaiting_ratification`.

#### БП-11. Package

- `Package` является операционной группировкой элементов для batch-утверждения.
- Пакет может быть сформирован только из `ApprovalInstance.status = awaiting_ratification`.
- Один `ApprovalInstance` может входить только в один активный пакет.
- В MVP пакет создаётся только в момент отправки и отдельного сохранённого черновика не имеет.
- После создания пакета связанные `ApprovalInstance` получают `in_ratification`.
- Текущий состав активного пакета определяется по `approval_instance.package_id`.
- Поля `status`, `name`, `description`, `ratifier_id` в таблице `package` отсутствуют.
- Пакет существует, пока в нём 2 и более элемента.

#### БП-12. Индивидуальные и пакетные решения

- Ratifier может принять решение по пакету целиком.
- Ratifier может принять решение по отдельному элементу внутри пакета.
- При индивидуальном решении по элементу внутри пакета:
  - элемент исключается из пакета;
  - если в пакете остаётся больше 1 элемента, пакет продолжает существовать;
  - если остаётся 1 элемент, пакет прекращает существование.

#### БП-13. Массовые действия

- Для страницы `Согласования` допускаются массовые действия по списку `ApprovalInstance`.
- Массовые действия поддерживают:
  - `approve`
  - `reject`
  - `ratify`
- Массовый `recall` в MVP не поддерживается.
- Массовое действие по элементам из пакета обрабатывается как серия индивидуальных действий.

#### БП-14. История процесса

- История процесса должна храниться на уровне `ApprovalInstance`.
- В историю входят:
  - этапы;
  - участники;
  - решения;
  - комментарии;
  - временные метки;
  - переходы статусов;
  - пакетный контекст, если решение принято в составе пакета.

#### БП-15. Представление этапов для UI и истории

- В истории этапов не используется отдельное поле `status`.
- Состояние этапа для UI определяется по совокупности полей:
  - `started_at`;
  - `completed_at`;
  - `pending_assignees`;
  - `decisions`.
- Отдельный enum статусов этапов в `process_snapshot`, API-контрактах и фронтовых типах не задаётся.

## Границы MVP

### Входит в MVP

- Создание `ApprovalInstance`.
- Индивидуальные действия:
  - `approve`
  - `reject`
  - `ratify`
  - `recall`
  - `start_ratification`
- Массовые действия по `ApprovalInstance`.
- Пакетное ratification.
- API-представления для страниц `Согласования` и `Пакеты`.
- Хранение истории в `process_snapshot`.

### Не входит в MVP

- Автоматическая маршрутизация по продукту, критичности и иным атрибутам.
- SLA, эскалации, напоминания.
- Делегирование полномочий.
- ЭП/КЭП.
- Отдельный развитый раздел истории пакета.
- Массовый `recall`.

## Пользовательские сценарии

### Сценарий 1. Отправка версии в процесс

1. Пользователь отправляет `PilotVersion` или `DeploymentVersion` в процесс.
2. Система валидирует маршрут и участников.
3. Система создаёт `ApprovalInstance`.
4. Система устанавливает стартовый статус:
   - `in_approval`, если есть Approval;
   - `in_ratification`, если Approval нет и Ratification auto;
   - `awaiting_ratification`, если Approval нет и Ratification manual.

### Сценарий 2. Approval

1. Approver получает назначение на текущий Approval-этап.
2. Принимает `approve` или `reject`.
3. Система обновляет историю этапа.
4. При необходимости переводит процесс на следующий статус.

### Сценарий 3. Индивидуальный запуск Ratification

1. `ApprovalInstance` находится в `awaiting_ratification`.
2. Пользователь запускает `start_ratification`.
3. Система назначает ratifier и переводит процесс в `in_ratification`.

### Сценарий 4. Пакетное утверждение

1. Пользователь формирует пакет из элементов в `awaiting_ratification`.
2. Отправляет пакет на утверждение.
3. Система переводит входящие `ApprovalInstance` в `in_ratification`.
4. Ratifier принимает решение:
   - по пакету целиком;
   - или по отдельным элементам.

### Сценарий 5. Recall

1. Пользователь отзывает активный процесс.
2. Система фиксирует `approval_cancelled` или `ratification_cancelled`.
3. История процесса сохраняется.

## Критерии приемки

### Критерий 1. Статусы ApprovalInstance

- [ ] Используются только статусы из БП-5
- [ ] Нет legacy-статусов вне этого набора

### Критерий 2. Старт процесса

- [ ] Если есть Approval, процесс стартует в `in_approval`
- [ ] Если Approval нет и `auto_ratification = true`, процесс стартует в `in_ratification`
- [ ] Если Approval нет и `auto_ratification = false`, процесс стартует в `awaiting_ratification`

### Критерий 3. Действия

- [ ] Индивидуальные действия `approve`, `reject`, `ratify`, `recall`, `start_ratification` работают корректно
- [ ] Массовые действия поддерживают только `approve`, `reject`, `ratify`
- [ ] Для `POST /api/v1/packages` создаётся и сразу отправляется пакет
- [ ] Для `POST /api/v1/packages/{id}/action` используются только `ratify` и `reject`

### Критерий 4. Package

- [ ] В пакет можно включать только `ApprovalInstance` в `awaiting_ratification`
- [ ] После отправки пакета его элементы переходят в `in_ratification`
- [ ] Пакет не имеет собственного `ApprovalInstance`

### Критерий 5. История

- [ ] История восстанавливается из `process_snapshot`
- [ ] Для пакетного решения сохраняется `packageId` и признак пакетного решения
- [ ] В истории этапов не используется отдельное поле `status`
- [ ] Состояние этапа определяется по `started_at`, `completed_at`, `pending_assignees` и `decisions`

## Функциональные требования

### ФТ-1. Создание ApprovalInstance

Система должна предоставлять API для создания `ApprovalInstance` при submit доменного элемента в процесс.

### ФТ-2. Действия по ApprovalInstance

Система должна предоставлять единый endpoint:
- `POST /api/v1/approvals/{id}/action`

Поддерживаемые значения `action`:
- `approve`
- `reject`
- `ratify`
- `recall`
- `start_ratification`

### ФТ-3. Массовые действия по ApprovalInstance

Система должна предоставлять единый endpoint:
- `POST /api/v1/approvals/action`

Поддерживаемые значения `action`:
- `approve`
- `reject`
- `ratify`

### ФТ-4. Создание пакета

Система должна предоставлять endpoint:
- `POST /api/v1/packages`

Запрос должен содержать:
- `approval_instance_ids`;
- `brief`.

После успешного создания пакета связанные `ApprovalInstance` переводятся в `in_ratification`.

### ФТ-5. Пакетные действия

Система должна предоставлять единый endpoint:
- `POST /api/v1/packages/{id}/action`

Поддерживаемые значения `action`:
- `ratify`
- `reject`

### ФТ-6. API-представления для UI

Система должна предоставлять ориентированные на UI API-представления для:
- страницы `Согласования`;
- страницы `Пакеты`.

### ФТ-7. История процесса

Система должна хранить в `process_snapshot`:
- этапы;
- участников этапов;
- признаки начала и завершения этапов;
- решения участников;
- комментарии;
- временные метки;
- переходы статусов `ApprovalInstance`;
- пакетный контекст.

Отдельные таблицы `approval_stage`, `approval_assignment` и `approval_decision` в MVP не используются.
Маршрут, участники, решения и история процесса хранятся в `approval_instance.process_snapshot`.
Для построения API-представлений страницы `Согласования` backend использует `approval_instance.status` как единственный источник текущего состояния процесса; отдельное поле `current_stage` в контракте не требуется.

## Описание модели данных

### Таблица `approval_instance`

| Поле | Тип | Обязательность | Описание |
|---|---|---|---|
| `id` | UUID | Да | Идентификатор экземпляра процесса |
| `target_type` | ENUM(`PILOT_VERSION`, `DEPLOYMENT_VERSION`) | Да | Тип доменной версии |
| `target_id` | UUID | Да | Идентификатор версии доменного элемента |
| `status` | ENUM | Да | Текущий статус `ApprovalInstance` |
| `auto_ratification` | BOOLEAN | Да | Признак автоматического запуска Ratification после Approval |
| `package_id` | UUID, FK | Нет | Идентификатор пакета, если элемент включён в пакет |
| `brief_subject` | VARCHAR(255) | Нет | Тема брифа, отправленного вместе с `ApprovalInstance` |
| `brief_body` | TEXT | Нет | Тело брифа, отправленного вместе с `ApprovalInstance` |
| `process_snapshot` | JSONB | Да | Снапшот истории процесса |
| `created_at` | TIMESTAMP WITH TIME ZONE | Да | Дата создания |
| `created_by` | UUID, FK | Да | Пользователь-создатель |
| `updated_at` | TIMESTAMP WITH TIME ZONE | Да | Дата последнего изменения |
| `updated_by` | UUID, FK | Да | Пользователь, выполнивший последнее изменение |

Описание таблицы `package` вынесено в [REQ_packages_page_backend.md](/home/reutov/Documents/AI/changesWork/final-spec/REQ_packages_page_backend.md), так как именно этот документ является источником правды по backend-модели пакетов.

## Спецификация API (OpenAPI)

```yaml
openapi: 3.0.3
info:
  title: Approval Core API
  version: 1.0.0
paths:
  /api/v1/approval-instances:
    post:
      summary: Создать ApprovalInstance
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateApprovalInstanceRequest'
      responses:
        '201':
          description: ApprovalInstance создан
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ApprovalInstanceDto'
  /api/v1/approval-instances/{id}:
    get:
      summary: Получить ApprovalInstance
      parameters:
        - in: path
          name: id
          required: true
          schema: { type: string, format: uuid }
      responses:
        '200':
          description: ApprovalInstance
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ApprovalInstanceDto'
  /api/v1/approvals/{id}/action:
    post:
      summary: Выполнить действие над ApprovalInstance
      parameters:
        - in: path
          name: id
          required: true
          schema: { type: string, format: uuid }
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ApprovalActionRequest'
      responses:
        '200':
          description: Действие выполнено
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ApprovalInstanceDto'
  /api/v1/approvals/action:
    post:
      summary: Массовое действие по нескольким ApprovalInstance
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/BulkApprovalActionRequest'
      responses:
        '200':
          description: Массовое действие выполнено
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BulkApprovalActionResponse'
  /api/v1/packages:
    post:
      summary: Создать и отправить пакет
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PackageCreateRequest'
      responses:
        '201':
          description: Пакет создан
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PackageCreateResponse'
  /api/v1/packages/{id}/action:
    post:
      summary: Выполнить пакетное действие
      parameters:
        - in: path
          name: id
          required: true
          schema: { type: string, format: uuid }
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PackageActionRequest'
      responses:
        '200':
          description: Пакетное действие выполнено
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PackageActionResponse'
components:
  schemas:
    CreateApprovalInstanceRequest:
      type: object
      required: [target_type, target_id, approval_stages, ratification, brief]
      properties:
        target_type:
          type: string
          enum: [PILOT_VERSION, DEPLOYMENT_VERSION]
        target_id:
          type: string
          format: uuid
        brief:
          $ref: '#/components/schemas/BriefInfo'
        approval_stages:
          type: array
          items:
            $ref: '#/components/schemas/ApprovalStageInput'
        ratification:
          $ref: '#/components/schemas/RatificationInput'
    ApprovalStageInput:
      type: object
      required: [stage_order, stage_name, assignee_ids]
      properties:
        stage_order:
          type: integer
        stage_name:
          type: string
        assignee_ids:
          type: array
          minItems: 1
          items:
            type: string
            format: uuid
    RatificationInput:
      type: object
      required: [mode]
      properties:
        mode:
          type: string
          enum: [auto, manual]
        ratifier_id:
          type: string
          format: uuid
          nullable: true
    ApprovalActionRequest:
      type: object
      required: [action]
      properties:
        action:
          type: string
          enum: [approve, reject, ratify, recall, start_ratification]
        comment:
          type: string
          nullable: true
        ratifier_id:
          type: string
          format: uuid
          nullable: true
    BulkApprovalActionRequest:
      type: object
      required: [approval_instance_ids, action]
      properties:
        approval_instance_ids:
          type: array
          minItems: 1
          items:
            type: string
            format: uuid
        action:
          type: string
          enum: [approve, reject, ratify]
        comment:
          type: string
          nullable: true
    BulkApprovalActionResponse:
      type: object
      properties:
        success_count:
          type: integer
        failed_count:
          type: integer
        results:
          type: array
          items:
            type: object
            properties:
              approval_instance_id:
                type: string
                format: uuid
              success:
                type: boolean
              error:
                type: string
                nullable: true
    PackageCreateRequest:
      type: object
      required: [approval_instance_ids, brief]
      properties:
        approval_instance_ids:
          type: array
          minItems: 2
          items:
            type: string
            format: uuid
        brief:
          $ref: '#/components/schemas/BriefInfo'
    PackageCreateResponse:
      type: object
      required: [package]
      properties:
        package:
          type: object
          additionalProperties: true
          description: Компактный объект созданного пакета. Содержит `package_id`, `brief`, `items_count`, `submitted_at` и `items`. Не является полной деталкой пакета: поля `products` и `criticality` не возвращаются, а в `items[].target` не возвращается `url`. Детальная структура задаётся `REQ_packages_page_backend.md`.
    PackageActionRequest:
      type: object
      required: [action]
      properties:
        action:
          type: string
          enum: [ratify, reject]
        comment:
          type: string
          nullable: true
    PackageActionResponse:
      type: object
      properties:
        affected_approval_instance_ids:
          type: array
          items:
            type: string
            format: uuid
        notification:
          type: string
          nullable: true
        resulting_statuses:
          type: array
          nullable: true
          items:
            type: object
            properties:
              approval_instance_id:
                type: string
                format: uuid
              status:
                type: string
    ApprovalInstanceDto:
      type: object
      properties:
        id:
          type: string
          format: uuid
        target_type:
          type: string
        target_id:
          type: string
          format: uuid
        status:
          type: string
          enum: [in_approval, approved, awaiting_ratification, in_ratification, ratified, approval_rejected, ratification_rejected, approval_cancelled, ratification_cancelled]
        auto_ratification:
          type: boolean
        package_id:
          type: string
          format: uuid
          nullable: true
        brief:
          nullable: true
          allOf:
            - $ref: '#/components/schemas/BriefInfo'
        process_snapshot:
          type: object
    BriefInfo:
      type: object
      properties:
        subject:
          type: string
        body:
          type: string
```

## Примеры запросов и ответов

### Пример 1. Создание ApprovalInstance

Запрос:

```http
POST /api/v1/approval-instances
Content-Type: application/json
```

```json
{
  "target_type": "DEPLOYMENT_VERSION",
  "target_id": "9a3d9ae3-c5ff-4f26-a350-000000000101",
  "brief": {
    "subject": "Согласование внедрения premium cutoff",
    "body": "Просим согласовать запуск новой отсечки для premium-сегмента."
  },
  "approval_stages": [
    {
      "stage_order": 1,
      "stage_name": "Согласование риск-менеджером",
      "assignee_ids": ["user-approver-1", "user-approver-2"]
    }
  ],
  "ratification": {
    "mode": "manual"
  }
}
```

Ответ:

```json
{
  "id": "appr-inst-001",
  "target_type": "DEPLOYMENT_VERSION",
  "target_id": "9a3d9ae3-c5ff-4f26-a350-000000000101",
  "status": "in_approval",
  "auto_ratification": false,
  "package_id": null,
  "brief": {
    "subject": "Согласование внедрения premium cutoff",
    "body": "Просим согласовать запуск новой отсечки для premium-сегмента."
  },
  "process_snapshot": {
    "approval_stages": [
      {
        "stage_order": 1,
        "stage_name": "Согласование риск-менеджером",
        "started_at": "2026-03-19T10:00:00Z",
        "completed_at": null,
        "assignees": [
          {
            "user_id": "user-approver-1",
            "user_name": "Иванов Иван",
            "role": "approver"
          },
          {
            "user_id": "user-approver-2",
            "user_name": "Петров Петр",
            "role": "approver"
          }
        ],
        "decisions": []
      }
    ],
    "ratification_stage": {
      "stage_name": "Утверждение",
      "started_at": null,
      "completed_at": null,
      "assignees": [],
      "decisions": []
    },
    "status_transitions": [
      {
        "from_status": null,
        "to_status": "in_approval",
        "timestamp": "2026-03-19T10:00:00Z",
        "user_id": "user-prm-1"
      }
    ],
    "package_context": null
  }
}
```

### Пример 2. Индивидуальный запуск Ratification

Запрос:

```http
POST /api/v1/approvals/appr-inst-001/action
Content-Type: application/json
```

```json
{
  "action": "start_ratification",
  "ratifier_id": "user-ratifier-1"
}
```

Ответ:

```json
{
  "id": "appr-inst-001",
  "target_type": "DEPLOYMENT_VERSION",
  "target_id": "9a3d9ae3-c5ff-4f26-a350-000000000101",
  "status": "in_ratification",
  "auto_ratification": false,
  "package_id": null,
  "brief": {
    "subject": "Согласование внедрения premium cutoff",
    "body": "Просим согласовать запуск новой отсечки для premium-сегмента."
  },
  "process_snapshot": {
    "approval_stages": [],
    "ratification_stage": {
      "stage_name": "Утверждение",
      "started_at": "2026-03-19T12:00:00Z",
      "completed_at": null,
      "assignees": [
        {
          "user_id": "user-ratifier-1",
          "user_name": "Сидоров Сидор",
          "role": "ratifier"
        }
      ],
      "decisions": []
    },
    "status_transitions": [
      {
        "from_status": "awaiting_ratification",
        "to_status": "in_ratification",
        "timestamp": "2026-03-19T12:00:00Z",
        "user_id": "user-prm-1"
      }
    ],
    "package_context": null
  }
}
```

### Пример 3. Approve

Запрос:

```http
POST /api/v1/approvals/appr-inst-001/action
Content-Type: application/json
```

```json
{
  "action": "approve",
  "comment": "Согласовано"
}
```

### Пример 4. Создание пакета

Запрос:

```http
POST /api/v1/packages
Content-Type: application/json
```

```json
{
  "approval_instance_ids": [
    "appr-inst-101",
    "appr-inst-102"
  ],
  "brief": {
    "subject": "Пакет квартальных изменений",
    "body": "Просим перевести выбранные элементы на этап утверждения единым пакетом."
  }
}
```

Ответ:

```json
{
  "package": {
    "package_id": "pkg-001",
    "brief": {
      "subject": "Пакет квартальных изменений",
      "body": "Просим перевести выбранные элементы на этап утверждения единым пакетом."
    },
    "items_count": 2,
    "submitted_at": "2026-03-19T09:10:00Z",
    "items": [
      {
        "approval_instance_id": "appr-inst-101",
        "approval_status": "in_ratification",
        "target_type": "PILOT_VERSION",
        "target_id": "pilot-version-101",
        "submitted_at": "2026-03-19T09:10:00Z",
        "target": {
          "name": "Пилот модели LTV для POS",
          "description": "Сегмент mass, волна 2",
          "approval_purpose": "Согласование активации с отложенной датой",
          "version": "7",
          "product": {
            "product_id": "prod-001",
            "product_name": "POS Loans"
          },
          "criticality": "high",
          "created_at": "2026-03-10T08:00:00Z",
          "attributes": []
        },
        "scorecards": [],
        "history": {
          "approval_stages": [],
          "ratification_stage": null,
          "status_transitions": []
        }
      },
      {
        "approval_instance_id": "appr-inst-102",
        "approval_status": "in_ratification",
        "target_type": "DEPLOYMENT_VERSION",
        "target_id": "deployment-version-102",
        "submitted_at": "2026-03-19T09:10:00Z",
        "target": {
          "name": "Внедрение CL Revamp",
          "description": "Запуск версии 3.4",
          "approval_purpose": "Утверждение внедрения версии 3.4 в продуктив",
          "version": "3.4",
          "product": {
            "product_id": "prod-002",
            "product_name": "Consumer Loans"
          },
          "criticality": "low",
          "created_at": "2026-03-11T09:15:00Z",
          "attributes": []
        },
        "scorecards": [],
        "history": {
          "approval_stages": [],
          "ratification_stage": null,
          "status_transitions": []
        }
      }
    ]
  }
}
```

### Пример 5. Reject по пакету

Запрос:

```http
POST /api/v1/packages/pkg-001/action
Content-Type: application/json
```

```json
{
  "action": "reject",
  "comment": "Требуется доработка перед утверждением."
}
```

Ответ:

```json
{
  "affected_approval_instance_ids": [
    "appr-inst-101",
    "appr-inst-102",
    "appr-inst-103"
  ],
  "notification": "Пакет отклонён",
  "resulting_statuses": [
    {
      "approval_instance_id": "appr-inst-101",
      "status": "ratification_rejected"
    },
    {
      "approval_instance_id": "appr-inst-102",
      "status": "ratification_rejected"
    },
    {
      "approval_instance_id": "appr-inst-103",
      "status": "ratification_rejected"
    }
  ]
}
```

## Ошибки и валидация

### Базовые коды ошибок

- `400 Bad Request` — некорректная структура запроса.
- `403 Forbidden` — недостаточно прав.
- `404 Not Found` — процесс, этап, пакет или target не найдены.
- `409 Conflict` — конфликт бизнес-состояния.
- `422 Unprocessable Entity` — нарушение бизнес-валидации.

### Обязательные бизнес-валидации

- Нельзя создать `ApprovalInstance` без Ratification.
- Нельзя создать `ApprovalInstance` без полей брифа.
- При `ratification.mode = auto` обязателен `ratifier_id`.
- При `start_ratification` обязателен `ratifier_id`.
- Для `POST /api/v1/packages` обязателен `brief`.
- Для `POST /api/v1/packages` допустимы только элементы в `awaiting_ratification`.
- Нельзя выбрать самого себя approver'ом или ratifier'ом.
- На Approval-этапы можно назначать только `approver`.
- На Ratification можно назначать только `ratifier`.
- `approve` допустим только на активном Approval-этапе.
- `ratify` допустим только на активном Ratification-этапе.
- `start_ratification` допустим только для `awaiting_ratification`.
- В пакет можно включать только `ApprovalInstance` в `awaiting_ratification`.
- Массовый `recall` в MVP запрещён.

## Интеграция и консистентность

### С доменными сущностями

- `PilotVersion` и `DeploymentVersion` не должны изобретать собственный параллельный набор approval-статусов.
- Их статусы процесса должны синхронизироваться со статусами `ApprovalInstance`.

### Со страницей `Согласования`

- Страница `Согласования` строится по `ApprovalInstance`, а не по статусам доменных сущностей.
- В истории этапов не используется отдельный статус этапа.

### Со страницей `Пакеты`

- Страница `Пакеты` работает только с `ApprovalInstance.status = awaiting_ratification`.
- После отправки пакета элементы уходят из очереди `Пакеты` и попадают на вкладку `На утверждении` страницы `Согласования`.
- `POST /api/v1/packages` возвращает компактный ответ создания, а не полную деталку пакета.
- Детальный контракт `POST /api/v1/packages/{id}/action` задаётся в `REQ_packages_page_backend.md`; поля пакетного запроса и валидации должны быть консистентны с ним.
