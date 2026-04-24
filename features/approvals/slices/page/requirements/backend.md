# Страница "Согласования" (Backend API)

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

Реализовать Backend API для страницы `Согласования`, которая позволяет пользователю:
- видеть свои активные назначения на согласование и утверждение;
- принимать решения по отдельным `ApprovalInstance`;
- выполнять массовые действия по нескольким `ApprovalInstance`;
- работать с карточками пакетов на вкладке утверждения;
- открывать подробный контекст элемента и историю процесса;
- принимать решения по пакету целиком.

### Источник правды

Основными источниками правил для этой спецификации являются:
- `final-spec/REQ_approval_core.md`;
- `final-spec/REQ_packages_page_backend.md`;
- `final-spec/spec_domain_model.md`.

### Бизнес-правила

#### Определение `ApprovalInstance`

- Под доменным элементом в рамках approvals API понимается версия согласуемой предметной сущности:
  - `PilotVersion`;
  - `DeploymentVersion`.
- Поле `target` в ответах approvals API — это представление этого доменного элемента для UI.
- `ApprovalInstance` — это экземпляр процесса согласования и утверждения, связанный с одной конкретной версией доменного элемента.
- В MVP `ApprovalInstance` может ссылаться только на:
  - `PilotVersion`;
  - `DeploymentVersion`.
- `ApprovalInstance` хранит маршрут, участников, решения, комментарии, переходы статусов и ссылку на согласуемый доменный элемент.

#### БП-1. Источник истины страницы

- Страница `Согласования` строится по `ApprovalInstance`.
- Доменные версии `PilotVersion` и `DeploymentVersion` используются только как контекст отображения.
- Страница не определяет действия по статусу доменного элемента.
- История процесса читается только из `ApprovalInstance`.

#### БП-2. Вкладка "На согласовании"

- На вкладке `На согласовании` показываются только `ApprovalInstance.status = in_approval`.
- Пользователь видит элемент на этой вкладке, только если он назначен на текущий Approval-этап.
- На этой вкладке отображаются только одиночные карточки элементов.

#### БП-3. Вкладка "На утверждении"

- На вкладке `На утверждении` показываются только `ApprovalInstance.status = in_ratification`.
- Пользователь видит элемент на этой вкладке, только если он назначен на текущий Ratification-этап.
- На этой вкладке backend должен отдавать готовое представление данных для UI в виде карточек двух типов:
  - одиночная карточка;
  - карточка пакета.
- Пакет на этой вкладке не имеет отдельного собственного статуса карточки.
- Если пакет отображается на этой вкладке, это означает:
  - пакет уже отправлен;
  - его элементы уже находятся в `in_ratification`.

#### БП-4. Карточка пакета

- Карточка пакета является UI-группировкой нескольких `ApprovalInstance`, связанных с одним `Package`.
- Пакет отображается на вкладке `На утверждении`, только если:
  - существует запись `package`;
  - у пакета 2 и более активных элементов;
  - все отображаемые элементы находятся в `in_ratification`.
- Поскольку пакет может включать элементы разных продуктов, карточка пакета не должна предполагать единственный продукт.

#### БП-5. Критичность для approvals page

- Для approvals page в MVP используется поле `criticality`, а не `priority`.
- Допустимые значения `criticality` на странице:
  - `high`
  - `low`
  - `null`, если доменный элемент не возвращает критичность
- Значения `critical`, `medium` для страницы `Согласования` в MVP не используются.
- Критичность пакета вычисляется как максимум по входящим карточкам:
  - если хотя бы один элемент `high`, пакет `high`;
  - иначе `low`;
  - если ни у одного элемента нет значения, возвращается `null`.

#### БП-6. Действия

- Индивидуальные действия выполняются по `approvalInstanceId`.
- Массовые действия выполняются по списку `approvalInstanceId`.
- Пакетные действия выполняются по `packageId`.
- Для страницы `Согласования` допустимы:
  - индивидуально: `approve`, `reject`, `ratify`, `recall`;
  - массово: `approve`, `reject`, `ratify`;
  - по пакету: `ratify`, `reject`.
- Массовый `recall` и `recall` по пакету в MVP не поддерживаются.

#### БП-7. Индивидуальные решения внутри пакета

- Если решение принято по одному элементу внутри пакета:
  - элемент исключается из пакета;
  - если в пакете остаётся больше 1 элемента, пакет продолжает существовать;
  - если остаётся 1 элемент, пакет прекращает существование, а последний элемент должен отображаться как одиночная карточка на вкладке `На утверждении`.

#### БП-8. История

- История процесса отображается на уровне `ApprovalInstance`.
- Если решение принято в составе пакета, в истории соответствующего `ApprovalInstance` фиксируется пакетный контекст.
- Пакет не является самостоятельным носителем истории маршрута согласования/утверждения.
- Текущее состояние элемента на странице определяется по `approval_status`; отдельное поле `current_stage` в API не используется.
- В истории этапов не используется отдельное поле `status`.
- Состояние этапа для UI определяется по `started_at`, `completed_at`, `pending_assignees` и `decisions`.

#### БП-8.1. Источник брифа в деталке элемента

- В деталке `ApprovalInstance` backend должен возвращать только один разрешённый для показа бриф.
- Если у `ApprovalInstance` есть активный пакет, backend возвращает бриф пакета.
- Если активного пакета нет или пакет рассыпался, backend возвращает бриф самого `ApprovalInstance`.
- В ответе деталки backend возвращает:
  - `brief_source` — источник выбранного брифа;
  - `brief` — сам бриф.
- Поля брифа пакета и `ApprovalInstance` одновременно в одной деталке не возвращаются.

#### БП-9. Ограничения MVP

Не входят в MVP:
- поиск;
- сортировка;
- развитые пользовательские фильтры;
- отдельный раздел истории пакетов;
- ручная настройка цветовых схем на бэке;
- локальное вычисление фронтом состава карточки пакета по сырым `ApprovalInstance`.

## Границы MVP

### Входит в MVP

- API-представление вкладки `На согласовании`.
- API-представление вкладки `На утверждении`.
- Детальная карточка `ApprovalInstance`.
- Детальная карточка пакета.
- Индивидуальные, массовые и пакетные действия.
- Возврат достаточного контекста доменного элемента и связанных скоркарт.

### Не входит в MVP

- Поиск и фильтрация.
- Расширенный аудит пакета как отдельной сущности.
- Возврат невалидных legacy-значений статусов и критичностей.

## Пользовательские сценарии

### Сценарий 1. Просмотр вкладки "На согласовании"

1. Пользователь открывает страницу `Согласования`.
2. Выбирает вкладку `На согласовании`.
3. Backend возвращает только карточки элементов с `ApprovalInstance.status = in_approval`, назначенных пользователю.

### Сценарий 2. Просмотр вкладки "На утверждении"

1. Пользователь открывает вкладку `На утверждении`.
2. Backend возвращает карточки:
   - одиночных элементов;
   - пакетов.
3. Все отображаемые элементы находятся в `in_ratification`.

### Сценарий 3. Открытие деталки элемента

1. Пользователь открывает карточку элемента.
2. Backend возвращает развернутый контекст доменной версии, связанные скоркарты и историю процесса.

### Сценарий 4. Открытие деталки пакета

1. Пользователь открывает карточку пакета.
2. Backend возвращает шапку пакета и список входящих элементов.
3. Для каждого элемента возвращается та же детализация, что и для одиночной карточки.

### Сценарий 5. Индивидуальное действие

1. Пользователь выполняет `approve`, `reject`, `ratify` или `recall`.
2. Backend обновляет `ApprovalInstance`.
3. Если элемент был частью пакета, пакет при необходимости пересчитывается.

### Сценарий 6. Массовое действие

1. Пользователь выбирает несколько карточек на одной вкладке.
2. Выполняет одно действие над всеми выбранными `ApprovalInstance`.
3. Backend возвращает результат по каждому элементу.

### Сценарий 7. Пакетное действие

1. Ratifier выполняет `ratify` или `reject` по карточке пакета.
2. Backend применяет одинаковое решение ко всем входящим элементам.
3. В истории каждого элемента фиксируется пакетный контекст.

## Критерии приемки

### Критерий 1. Вкладка "На согласовании"

- [ ] Возвращает только `ApprovalInstance.status = in_approval`
- [ ] Возвращает только карточки, назначенные текущему пользователю
- [ ] Не возвращает карточки пакетов

### Критерий 2. Вкладка "На утверждении"

- [ ] Возвращает только элементы из `in_ratification`
- [ ] Возвращает готовые карточки двух типов: `single` и `package`
- [ ] Не использует отдельный собственный статус пакета как бизнес-статус карточки утверждения
- [ ] Не возвращает поле `current_stage`

### Критерий 3. Критичность

- [ ] На approvals page используются только значения `high`, `low` или `null`
- [ ] Значения `critical`, `medium` не используются
- [ ] Критичность пакета рассчитывается консистентно с критичностями его элементов

### Критерий 4. История

- [ ] В истории этапов не используется отдельное поле `status`
- [ ] Состояние этапа определяется по `started_at`, `completed_at`, `pending_assignees` и `decisions`
- [ ] Для пакетных решений история содержит `packageId` и признак пакетного решения
- [ ] Деталка `ApprovalInstance` содержит `brief_source`, `brief`, `submitted_at` и ссылку на связанный доменный элемент
- [ ] Если у элемента есть активный пакет, `brief_source = package`
- [ ] Если активного пакета нет или пакет рассыпался, `brief_source = approval_instance`
- [ ] Деталка `ApprovalInstance` возвращает полные текущие скоркарты, включая JSON снимок для отображения бинарных переключателей и финансовых эффектов
- [ ] Карточки и деталки содержат достаточно данных для открытия связанного доменного элемента в новом окне

### Критерий 5. Действия

- [ ] Индивидуальные действия работают по `approvalInstanceId`
- [ ] Массовые действия поддерживают только `approve`, `reject`, `ratify`
- [ ] Пакетные действия поддерживают только `ratify`, `reject`
- [ ] Массовый `recall` отсутствует

## Функциональные требования

### ФТ-1. Представление данных вкладки

**Endpoint:** `GET /api/v1/approvals/my`

Обязательный query-параметр:
- `stage_type = approval | ratification`

Правила:
- для `stage_type = approval` backend возвращает только карточки типа `single`;
- для `stage_type = ratification` backend возвращает карточки типа `single` и `package`.

### ФТ-2. Контракт карточки одиночного элемента

`ApprovalSingleCard` должен содержать:
- `card_type = single`
- `approval_instance_id`
- `approval_status`
- `target_type`
- `target_id`
- `target_name`
- `target_description`
- `target_approval_purpose`
- `target_url`
- `product`
- `criticality`
- `submitted_at`
- `scorecards_count`
- `scorecards_preview`

### ФТ-3. Контракт карточки пакета

`ApprovalPackageCard` должен содержать:
- `card_type = package`
- `package_id`
- `brief`
- `items_count`
- `products`
- `criticality`
- `submitted_at`
- `items_preview`

Примечание:
- `products` должен быть массивом, потому что пакет может включать элементы разных продуктов.
- Каждый элемент в `items_preview` должен содержать данные, достаточные для показа превью и перехода на связанный доменный элемент в новом окне.
- Каждый элемент в `items_preview` должен содержать `target_approval_purpose` — текст, поясняющий, для чего именно запрошено согласование или утверждение по данному элементу.
- `target_url` должен быть относительной UI-ссылкой на детальную карточку связанного доменного элемента.
- Если `ApprovalInstance` связан с конкретной версией доменного элемента, `target_url` должен открывать именно эту версию.

### ФТ-4. Детальная карточка ApprovalInstance

**Endpoint:** `GET /api/v1/approvals/{id}`

Ответ должен включать:
- идентификатор процесса;
- текущий approval-статус;
- разрешённый для показа бриф и источник этого брифа;
- дату отправки на согласование или утверждение;
- развернутый target-context;
- список полных текущих скоркарт;
- историю этапов и переходов статусов;
- пакетный контекст, если есть.

Правило выбора брифа:
- если у `ApprovalInstance` есть активный пакет, backend возвращает `brief_source = package` и поля брифа пакета;
- если активного пакета нет или пакет рассыпался, backend возвращает `brief_source = approval_instance` и поля брифа `ApprovalInstance`.

Дополнительно:
- в `target` backend должен возвращать `approval_purpose` — текст, поясняющий, для чего именно запрошено согласование или утверждение по элементу;
- если `scorecards[].is_manual = false`, backend должен вернуть `scorecards[].url`;
- транспортные метаполя скоркарты не дублируются внутри `scorecard_json`: `is_manual`, `url`, `created_at`, `updated_at` возвращаются только на верхнем уровне объекта скоркарты.

### ФТ-5. Детальная карточка пакета

**Endpoint:** `GET /api/v1/packages/{id}`

Ответ должен включать:
- шапку пакета;
- бриф пакета;
- дату отправки пакета на утверждение;
- список входящих элементов;
- по каждому элементу:
  - target-context;
  - полные текущие scorecards;
  - history.

В деталке пакета бриф пакета возвращается один раз в шапке пакета и не дублируется внутри каждого входящего элемента.

Дополнительно:
- контракт `GET /api/v1/packages/{id}` должен быть консистентен с `REQ_packages_page_backend.md`;
- внутри `target` backend должен возвращать `approval_purpose`;
- если `scorecards[].is_manual = false`, backend должен вернуть `scorecards[].url`;
- транспортные метаполя скоркарты не дублируются внутри `scorecard_json`.

### ФТ-6. Индивидуальные действия

**Endpoint:** `POST /api/v1/approvals/{id}/action`

Поддерживаемые `action`:
- `approve`
- `reject`
- `ratify`
- `recall`

### ФТ-7. Массовые действия

**Endpoint:** `POST /api/v1/approvals/action`

Поддерживаемые `action`:
- `approve`
- `reject`
- `ratify`

### ФТ-8. Пакетные действия

**Endpoint:** `POST /api/v1/packages/{id}/action`

Поддерживаемые `action`:
- `ratify`
- `reject`

## Описание модели данных

### Таблица `approval_instance`

| Поле | Тип | Обязательность | Описание |
|---|---|---|---|
| `id` | UUID | Да | Идентификатор процесса |
| `target_type` | ENUM | Да | Тип доменной версии |
| `target_id` | UUID | Да | Идентификатор доменной версии |
| `status` | ENUM | Да | Текущий approval-статус |
| `package_id` | UUID, FK | Нет | Активный пакет, если элемент включён в пакет |
| `brief_subject` | VARCHAR(255) | Нет | Тема брифа, отправленного вместе с `ApprovalInstance` |
| `brief_body` | TEXT | Нет | Тело брифа, отправленного вместе с `ApprovalInstance` |
| `process_snapshot` | JSONB | Да | История процесса и маршрут для построения API-представлений страницы |
| `created_at` | TIMESTAMP WITH TIME ZONE | Да | Дата создания |
| `created_by` | UUID | Да | Создатель |

### Таблица `package`

| Поле | Тип | Обязательность | Описание |
|---|---|---|---|
| `id` | UUID | Да | Идентификатор пакета |
| `brief_subject` | VARCHAR(255) | Нет | Тема брифа пакета |
| `brief_body` | TEXT | Нет | Тело брифа пакета |
| `created_at` | TIMESTAMP WITH TIME ZONE | Да | Дата создания |
| `created_by` | UUID | Да | Создатель |

Примечание:
- поля `status`, `name`, `description`, `ratifier_id` в таблице `package` отсутствуют;
- текущая активная принадлежность элемента пакету определяется по `approval_instance.package_id`;
- отдельная таблица истории пакетных решений в MVP не задаётся.

## Спецификация API (OpenAPI)

```yaml
openapi: 3.0.3
info:
  title: Approvals Page Backend API
  version: 1.0.0
paths:
  /api/v1/approvals/my:
    get:
      summary: Получить карточки для страницы Согласования
      parameters:
        - in: query
          name: stage_type
          required: true
          schema:
            type: string
            enum: [approval, ratification]
      responses:
        '200':
          description: Карточки для вкладки
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ApprovalsInboxResponse'
  /api/v1/approvals/{id}:
    get:
      summary: Получить деталку ApprovalInstance
      parameters:
        - in: path
          name: id
          required: true
          schema: { type: string, format: uuid }
      responses:
        '200':
          description: Детальная карточка элемента
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ApprovalDetailResponse'
  /api/v1/packages/{id}:
    get:
      summary: Получить деталку пакета
      parameters:
        - in: path
          name: id
          required: true
          schema: { type: string, format: uuid }
      responses:
        '200':
          description: Детальная карточка пакета
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PackageDetailResponse'
  /api/v1/approvals/{id}/action:
    post:
      summary: Индивидуальное действие по ApprovalInstance
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
                $ref: '#/components/schemas/ApprovalActionResponse'
  /api/v1/approvals/action:
    post:
      summary: Массовое действие по ApprovalInstance
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
  /api/v1/packages/{id}/action:
    post:
      summary: Пакетное действие
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
    ApprovalsInboxResponse:
      type: object
      properties:
        items:
          type: array
          items:
            oneOf:
              - $ref: '#/components/schemas/ApprovalSingleCard'
              - $ref: '#/components/schemas/ApprovalPackageCard'
        total:
          type: integer
    ApprovalSingleCard:
      type: object
      properties:
        card_type:
          type: string
          enum: [single]
        approval_instance_id:
          type: string
          format: uuid
        approval_status:
          type: string
        target_type:
          type: string
          enum: [PILOT_VERSION, DEPLOYMENT_VERSION]
        target_id:
          type: string
          format: uuid
        target_name:
          type: string
        target_description:
          type: string
          nullable: true
        target_approval_purpose:
          type: string
          description: Текст, поясняющий, для чего именно запрошено согласование или утверждение по данному элементу.
        target_url:
          type: string
        product:
          $ref: '#/components/schemas/ProductRef'
        criticality:
          type: string
          enum: [high, low]
          nullable: true
        submitted_at:
          type: string
          format: date-time
        scorecards_count:
          type: integer
        scorecards_preview:
          type: array
          items:
            $ref: '#/components/schemas/ScorecardPreviewRef'
    ApprovalPackageCard:
      type: object
      properties:
        card_type:
          type: string
          enum: [package]
        package_id:
          type: string
          format: uuid
        brief:
          $ref: '#/components/schemas/BriefInfo'
        items_count:
          type: integer
        products:
          type: array
          items:
            $ref: '#/components/schemas/ProductRef'
        criticality:
          type: string
          enum: [high, low]
          nullable: true
        submitted_at:
          type: string
          format: date-time
        items_preview:
          type: array
          items:
            $ref: '#/components/schemas/PackagePreviewItem'
    PackagePreviewItem:
      type: object
      properties:
        approval_instance_id:
          type: string
          format: uuid
        approval_status:
          type: string
        target_type:
          type: string
        target_name:
          type: string
        target_description:
          type: string
          nullable: true
        target_approval_purpose:
          type: string
          description: Текст, поясняющий, для чего именно запрошено согласование или утверждение по данному элементу.
        target_url:
          type: string
        product:
          $ref: '#/components/schemas/ProductRef'
        criticality:
          type: string
          enum: [high, low]
          nullable: true
    ProductRef:
      type: object
      properties:
        product_id:
          type: string
          format: uuid
        product_name:
          type: string
    ScorecardPreviewRef:
      type: object
      properties:
        scorecard_id:
          type: string
          format: uuid
        display_id:
          type: string
        name:
          type: string
        criticality:
          type: string
          enum: [high, low]
          nullable: true
    UserRef:
      type: object
      properties:
        user_id:
          type: string
          format: uuid
        user_name:
          type: string
    ApprovalDetailResponse:
      type: object
      properties:
        approval_instance_id:
          type: string
          format: uuid
        approval_status:
          type: string
        target_type:
          type: string
        target_id:
          type: string
          format: uuid
        submitted_at:
          type: string
          format: date-time
        brief_source:
          type: string
          enum: [approval_instance, package]
          nullable: true
        brief:
          nullable: true
          allOf:
            - $ref: '#/components/schemas/BriefInfo'
        target:
          $ref: '#/components/schemas/ApprovalTarget'
        scorecards:
          type: array
          items:
            $ref: '#/components/schemas/ApprovalScorecard'
        history:
          $ref: '#/components/schemas/ApprovalHistory'
    ApprovalTarget:
      type: object
      properties:
        url:
          type: string
        name:
          type: string
        description:
          type: string
          nullable: true
        approval_purpose:
          type: string
          description: Текст, поясняющий, для чего именно запрошено согласование или утверждение по данному элементу.
        version:
          type: string
          nullable: true
        product:
          $ref: '#/components/schemas/ProductRef'
        criticality:
          type: string
          enum: [high, low]
          nullable: true
        created_at:
          type: string
          format: date-time
          nullable: true
        attributes:
          type: array
          items:
            $ref: '#/components/schemas/AttributeRef'
    BriefInfo:
      type: object
      properties:
        subject:
          type: string
        body:
          type: string
    AttributeRef:
      type: object
      properties:
        key:
          type: string
        label:
          type: string
        value:
          type: string
          nullable: true
    ApprovalScorecard:
      type: object
      properties:
        scorecard_id:
          type: string
          format: uuid
        display_id:
          type: string
        name:
          type: string
        description:
          type: string
          nullable: true
        version:
          type: integer
        status:
          type: string
        criticality:
          type: string
          enum: [high, low]
          nullable: true
        is_manual:
          type: boolean
        url:
          type: string
          nullable: true
          description: Возвращается для связанных скоркарт с is_manual=false; для ручной скоркарты может быть null.
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time
          nullable: true
        scorecard_json:
          type: object
          additionalProperties: true
          description: Полный JSONB текущей скоркарты, достаточный для отображения бинарных переключателей, финансовых эффектов и других параметров деталки. Транспортные метаполя is_manual, url, created_at, updated_at не дублируются внутри scorecard_json.
    ApprovalHistory:
      type: object
      properties:
        approval_stages:
          type: array
          items:
            $ref: '#/components/schemas/HistoryStage'
        ratification_stage:
          nullable: true
          allOf:
            - $ref: '#/components/schemas/HistoryStage'
        status_transitions:
          type: array
          items:
            $ref: '#/components/schemas/StatusTransition'
        package_context:
          nullable: true
          allOf:
            - $ref: '#/components/schemas/PackageContext'
    HistoryStage:
      type: object
      properties:
        stage_order:
          type: integer
          nullable: true
        stage_name:
          type: string
        started_at:
          type: string
          format: date-time
          nullable: true
        completed_at:
          type: string
          format: date-time
          nullable: true
        assignees:
          type: array
          items:
            $ref: '#/components/schemas/UserRef'
        pending_assignees:
          type: array
          items:
            $ref: '#/components/schemas/UserRef'
        decisions:
          type: array
          items:
            $ref: '#/components/schemas/DecisionRef'
    DecisionRef:
      type: object
      properties:
        user_id:
          type: string
          format: uuid
        user_name:
          type: string
        decision:
          type: string
        comment:
          type: string
          nullable: true
        decided_at:
          type: string
          format: date-time
    StatusTransition:
      type: object
      properties:
        from_status:
          type: string
          nullable: true
        to_status:
          type: string
        timestamp:
          type: string
          format: date-time
        user_id:
          type: string
          format: uuid
    PackageContext:
      type: object
      properties:
        package_id:
          type: string
          format: uuid
        is_batch_decision:
          type: boolean
        batch_comment:
          type: string
          nullable: true
    PackageDetailResponse:
      type: object
      required: [package]
      properties:
        package:
          $ref: '#/components/schemas/PackageDetail'
    PackageDetail:
      type: object
      properties:
        package_id:
          type: string
          format: uuid
        brief:
          $ref: '#/components/schemas/BriefInfo'
        items_count:
          type: integer
        products:
          type: array
          items:
            $ref: '#/components/schemas/ProductRef'
        criticality:
          type: string
          enum: [high, low]
          nullable: true
        submitted_at:
          type: string
          format: date-time
        items:
          type: array
          items:
            $ref: '#/components/schemas/PackageItemDetail'
    PackageItemDetail:
      type: object
      properties:
        approval_instance_id:
          type: string
          format: uuid
        approval_status:
          type: string
        target_type:
          type: string
          enum: [PILOT_VERSION, DEPLOYMENT_VERSION]
        target_id:
          type: string
          format: uuid
        submitted_at:
          type: string
          format: date-time
        target:
          $ref: '#/components/schemas/ApprovalTarget'
        scorecards:
          type: array
          items:
            $ref: '#/components/schemas/ApprovalScorecard'
        history:
          $ref: '#/components/schemas/ApprovalHistory'
    ApprovalActionRequest:
      type: object
      required: [action]
      properties:
        action:
          type: string
          enum: [approve, reject, ratify, recall]
        comment:
          type: string
          nullable: true
    ApprovalActionResponse:
      type: object
      properties:
        approval_instance_id:
          type: string
          format: uuid
        status:
          type: string
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
        package:
          $ref: '#/components/schemas/PackageDetail'
          nullable: true
        affected_approval_instance_ids:
          type: array
          items:
            type: string
            format: uuid
        notification:
          type: string
          nullable: true
```

## Примеры запросов и ответов

### Пример 1. Вкладка "На согласовании"

Запрос:

```http
GET /api/v1/approvals/my?stage_type=approval
```

Ответ:

```json
{
  "items": [
    {
      "card_type": "single",
      "approval_instance_id": "appr-inst-001",
      "approval_status": "in_approval",
      "target_type": "PILOT_VERSION",
      "target_id": "pilot-version-001",
      "target_name": "Пилот новой риск-модели",
      "target_description": "Пилот для сегмента premium",
      "target_approval_purpose": "Согласование активации пилота для premium-сегмента",
      "target_url": "/pilots/pilot-version-001",
      "product": {
        "product_id": "prod-001",
        "product_name": "Premium Cards"
      },
      "criticality": "high",
      "submitted_at": "2026-03-19T10:00:00Z",
      "scorecards_count": 2,
      "scorecards_preview": [
        {
          "scorecard_id": "sc-001",
          "display_id": "SC-001",
          "name": "Premium underwriting",
          "criticality": "high"
        }
      ]
    }
  ],
  "total": 1
}
```

### Пример 2. Вкладка "На утверждении"

Запрос:

```http
GET /api/v1/approvals/my?stage_type=ratification
```

Ответ:

```json
{
  "items": [
    {
      "card_type": "package",
      "package_id": "pkg-001",
      "brief": {
        "subject": "Пакет мартовских релизов",
        "body": "Пакет элементов на общее утверждение"
      },
      "items_count": 2,
      "products": [
        {
          "product_id": "prod-001",
          "product_name": "Premium Cards"
        },
        {
          "product_id": "prod-002",
          "product_name": "Mortgage"
        }
      ],
      "criticality": "high",
      "submitted_at": "2026-03-19T12:00:00Z",
      "items_preview": [
        {
          "approval_instance_id": "appr-inst-101",
          "approval_status": "in_ratification",
          "target_type": "DEPLOYMENT_VERSION",
          "target_name": "Внедрение premium cutoff",
          "target_description": "Основное внедрение для premium-сегмента",
          "target_approval_purpose": "Согласование активации с отложенной датой",
          "target_url": "/deployments/dep-version-101",
          "product": {
            "product_id": "prod-001",
            "product_name": "Premium Cards"
          },
          "criticality": "high"
        },
        {
          "approval_instance_id": "appr-inst-102",
          "approval_status": "in_ratification",
          "target_type": "DEPLOYMENT_VERSION",
          "target_name": "Внедрение mortgage scoring",
          "target_description": "Ипотечное внедрение весеннего релиза",
          "target_approval_purpose": "Утверждение внедрения версии 3.4 в продуктив",
          "target_url": "/deployments/dep-version-102",
          "product": {
            "product_id": "prod-002",
            "product_name": "Mortgage"
          },
          "criticality": "low"
        }
      ]
    },
    {
      "card_type": "single",
      "approval_instance_id": "appr-inst-201",
      "approval_status": "in_ratification",
      "target_type": "DEPLOYMENT_VERSION",
      "target_id": "dep-version-201",
      "target_name": "Внедрение retail scoring",
      "target_description": "Одиночное утверждение вне пакета",
      "target_approval_purpose": "Утверждение внепакетного внедрения в продуктив",
      "target_url": "/deployments/dep-version-201",
      "product": {
        "product_id": "prod-003",
        "product_name": "Retail Loans"
      },
      "criticality": "low",
      "submitted_at": "2026-03-19T12:10:00Z",
      "scorecards_count": 1,
      "scorecards_preview": [
        {
          "scorecard_id": "sc-010",
          "display_id": "SC-010",
          "name": "Retail scoring baseline",
          "criticality": "low"
        }
      ]
    }
  ],
  "total": 2
}
```

### Пример 3. Деталка элемента

Запрос:

```http
GET /api/v1/approvals/appr-inst-001
```

Ответ:

```json
{
  "approval_instance_id": "appr-inst-001",
  "approval_status": "in_ratification",
  "target_type": "DEPLOYMENT_VERSION",
  "target_id": "dep-version-001",
  "submitted_at": "2026-03-19T10:00:00Z",
  "brief_source": "package",
  "brief": {
    "subject": "Согласование изменений риск-стратегии",
    "body": "Направляем на согласование изменение риск-стратегии premium-сегмента."
  },
  "target": {
    "url": "/deployments/dep-version-001",
    "name": "Внедрение premium cutoff",
    "description": "Публикация новой отсечки в production-контур.",
    "approval_purpose": "Согласование активации с отложенной датой",
    "version": "2",
    "product": {
      "product_id": "prod-001",
      "product_name": "Premium Cards"
    },
    "criticality": "high",
    "created_at": "2026-03-15T08:30:00Z",
    "attributes": [
      {
        "key": "author",
        "label": "Автор",
        "value": "Иван Петров"
      }
    ]
  },
  "scorecards": [
    {
      "scorecard_id": "sc-001",
      "display_id": "SC-001",
      "name": "Premium underwriting",
      "description": "Основная скоркарта premium-сегмента",
      "version": 3,
      "status": "ratified",
      "criticality": "high",
      "is_manual": false,
      "url": "/scorecards/sc-001",
      "created_at": "2026-03-10T09:00:00Z",
      "updated_at": "2026-03-18T14:30:00Z",
      "scorecard_json": {
        "financial_effects": {
          "ar": "+2.5M",
          "volume": "+18%",
          "npv": "+5.8M",
          "rc": "-0.4%"
        },
        "switches": {
          "all_subproducts": true,
          "manual_override": false
        }
      }
    },
    {
      "scorecard_id": "sc-004",
      "display_id": "SC-004",
      "name": "Premium early warning",
      "description": "Дополнительная скоркарта раннего предупреждения",
      "version": 2,
      "status": "draft",
      "criticality": "low",
      "is_manual": true,
      "url": null,
      "created_at": "2026-03-11T11:00:00Z",
      "updated_at": null,
      "scorecard_json": {
        "financial_effects": {
          "ar": "+0.8M",
          "volume": "+4%",
          "npv": "+1.5M",
          "rc": "+0.1%"
        },
        "switches": {
          "all_subproducts": false,
          "manual_override": true
        }
      }
    }
  ],
  "history": {
    "approval_stages": [
      {
        "stage_order": 1,
        "stage_name": "Согласование риск-менеджером",
        "started_at": "2026-03-19T10:00:00Z",
        "completed_at": "2026-03-19T11:00:00Z",
        "assignees": [
          {
            "user_id": "user-approver-1",
            "user_name": "Иванов Иван"
          }
        ],
        "pending_assignees": [],
        "decisions": [
          {
            "user_id": "user-approver-1",
            "user_name": "Иванов Иван",
            "decision": "approve",
            "comment": "Согласовано",
            "decided_at": "2026-03-19T11:00:00Z"
          }
        ]
      }
    ],
    "ratification_stage": {
      "stage_order": null,
      "stage_name": "Утверждение",
      "started_at": "2026-03-19T12:00:00Z",
      "completed_at": null,
      "assignees": [
        {
          "user_id": "user-ratifier-1",
          "user_name": "Сидоров Сидор"
        }
      ],
      "pending_assignees": [
        {
          "user_id": "user-ratifier-1",
          "user_name": "Сидоров Сидор"
        }
      ],
      "decisions": []
    },
    "status_transitions": [
      {
        "from_status": null,
        "to_status": "in_approval",
        "timestamp": "2026-03-19T10:00:00Z",
        "user_id": "user-prm-1"
      },
      {
        "from_status": "in_approval",
        "to_status": "approved",
        "timestamp": "2026-03-19T11:00:00Z",
        "user_id": "user-approver-1"
      },
      {
        "from_status": "approved",
        "to_status": "in_ratification",
        "timestamp": "2026-03-19T12:00:00Z",
        "user_id": "user-prm-1"
      }
    ],
    "package_context": null
  }
}
```

### Пример 4. Индивидуальное действие

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

### Пример 5. Пакетное действие

Запрос:

```http
POST /api/v1/packages/pkg-001/action
Content-Type: application/json
```

```json
{
  "action": "ratify",
  "comment": "Утверждено в составе пакета"
}
```

## Ошибки и валидация

### Базовые коды ошибок

- `400 Bad Request` — некорректная структура запроса.
- `403 Forbidden` — у пользователя нет прав на действие.
- `404 Not Found` — элемент или пакет не найдены.
- `409 Conflict` — конфликт бизнес-состояния.
- `422 Unprocessable Entity` — нарушение бизнес-валидации.

### Обязательные валидации

- `GET /api/v1/approvals/my` требует `stage_type`.
- Для `stage_type = approval` нельзя возвращать `package`-карточки.
- Для `stage_type = ratification` нельзя возвращать элементы вне `in_ratification`.
- Карточки и деталки элементов должны возвращать `target_url`, если связанный доменный элемент доступен для открытия по UI.
- Для карточек страницы `Согласования` backend не должен возвращать поле `current_stage`.
- Для деталки `ApprovalInstance` backend должен возвращать только один бриф:
  - пакетный, если у элемента есть активный пакет;
  - иначе бриф самого `ApprovalInstance`.
- Для деталки `ApprovalInstance` и деталки пакета backend должен возвращать полные текущие скоркарты с `scorecard_json`.
- Для связанных скоркарт при `is_manual = false` backend должен возвращать `url`.
- Транспортные метаполя скоркарты `is_manual`, `url`, `created_at`, `updated_at` не должны дублироваться внутри `scorecard_json`.
- Индивидуальное `approve` допустимо только на активном Approval-этапе.
- Индивидуальное `ratify` допустимо только на активном Ratification-этапе.
- `recall` допустим только для активного процесса.
- Массовое действие должно проверять доступ к каждому `ApprovalInstance` отдельно.
- Пакетное действие допустимо только для активной группировки с 2 и более элементами в `in_ratification`.

## Интеграция и консистентность

### С approval_core

- Набор статусов `ApprovalInstance` должен полностью соответствовать `REQ_approval_core.md`.
- Представление этапов в истории без отдельного поля `status` должно полностью соответствовать `REQ_approval_core.md`.

### С packages

- Страница `Согласования` не должна трактовать пакет как approval-target.
- Карточка пакета на вкладке `На утверждении` строится по данным `package` и связанных `ApprovalInstance` в `in_ratification`.
- Контракт `GET /api/v1/packages/{id}` должен быть консистентен с `REQ_packages_page_backend.md`, включая поля брифа пакета и детальные данные входящих элементов.

### Со scorecards и доменными страницами

- В карточках и деталках approvals page используется поле `criticality`, согласованное с текущими требованиями по scorecards и deployment.
- В MVP это `high | low | null`; legacy `priority` и значения `critical | medium` не используются.
- В примерах скоркарт должны использоваться актуальные статусы, например `draft`, `ratified`, `archived`, а не legacy `active`.
