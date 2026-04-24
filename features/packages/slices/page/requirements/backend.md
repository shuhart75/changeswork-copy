# Страница "Пакеты" (Backend API)

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

Реализовать Backend API для страницы `Пакеты`, которая позволяет пользователю:
- видеть очередь элементов, ожидающих ручного запуска утверждения;
- локально выбрать несколько элементов и отправить их в пакет;
- просматривать свои отправленные пакеты;
- открывать деталку пакета;
- работать консистентно с `approval_core` и страницей `Согласования`.

### Источник правды

Основными источниками правил для этой спецификации являются:
- `final-spec/REQ_approval_core.md`;
- `final-spec/REQ_approvals_page_backend.md`;
- `final-spec/spec_domain_model.md`;
- `final-spec/REQ_roles_rbac.md`.

### Определения

#### Доменный элемент

- Под доменным элементом в рамках страницы `Пакеты` понимается версия согласуемой предметной сущности:
  - `PilotVersion`;
  - `DeploymentVersion`.
- Доменные версии используются только как контекст отображения.

#### ApprovalInstance

- `ApprovalInstance` — это экземпляр процесса согласования и утверждения, связанный с одной конкретной версией доменного элемента.
- Именно `ApprovalInstance`, а не доменная версия, является источником статуса процесса.
- В очередь пакетирования попадают только `ApprovalInstance.status = awaiting_ratification`.

#### Package

- `Package` — это операционная группировка нескольких `ApprovalInstance` для общего запуска этапа утверждения и последующего пакетного решения.
- `Package` не является target процесса и не имеет собственного маршрута согласования или утверждения.
- В MVP `Package` создаётся только в момент отправки группировки.
- Локальный черновик пакета на фронте не является backend-сущностью и не хранится в базе.

### Бизнес-правила

#### БП-1. Источник истины страницы

- Страница `Пакеты` строится вокруг `ApprovalInstance`.
- Страница не вычисляет очередь по статусам доменных сущностей напрямую.
- Для текущего состояния элемента в API используется только `approval_status`.
- Поле `current_stage` в API страницы `Пакеты` не возвращается.

#### БП-2. Что такое пакет в MVP

- Пакет создаётся только из 2 и более `ApprovalInstance`, находящихся в `awaiting_ratification`.
- После создания пакет сразу считается отправленным.
- Сохраняемые backend-черновики пакетов в MVP отсутствуют.
- У пакета нет собственных полей:
  - `status`;
  - `name`;
  - `description`;
  - `ratifier_id`.
- Если UI нужен человекочитаемый ярлык пакета, он строится из идентификатора пакета на стороне фронта, например `PKG-{package_id}`.

#### БП-3. Текущий и исторический состав пакета

- Текущий активный состав пакета определяется по `approval_instance.package_id`.
- Отдельная таблица `package_item` в MVP не используется.
- Отдельное хранение исторического состава пакета в собственной таблице в MVP не задаётся.
- Пакетный контекст для истории отображения хранится в истории соответствующих `ApprovalInstance`.

#### БП-4. Создание и отправка пакета

- В запросе на создание пакета backend получает:
  - список `approval_instance_ids`;
  - бриф пакета `brief`.
- Все выбранные элементы должны быть доступны текущему пользователю по RBAC.
- Все выбранные элементы должны находиться в `awaiting_ratification` на момент запроса.
- Если хотя бы один элемент уже вошёл в другой активный пакет или вышел из `awaiting_ratification`, создание отклоняется целиком.
- После успешного создания:
  - создаётся запись `package`;
  - в ней сохраняются поля брифа пакета;
  - все выбранные `ApprovalInstance` переводятся в `in_ratification`;
  - всем выбранным `ApprovalInstance` присваивается `package_id`.

#### БП-5. Бриф пакета

- Бриф пакета хранится в таблице `package`.
- В API пакета backend возвращает один блок `brief`:
  - `subject`;
  - `body`.
- Деталка пакета возвращает бриф пакета один раз в шапке.
- Во вложенных элементах деталки пакета блок брифа не дублируется.

#### БП-6. Права доступа и продуктовый контекст

- `prm` работает только с элементами своего продукта.
- `methodologist` видит элементы любых продуктов и может формировать смешанный пакет.
- `admin` работает со всеми элементами.
- Для `prm` backend автоматически ограничивает очередь и доступные элементы своим продуктом.
- Для `methodologist` ручной фильтр по продукту в MVP не требуется.

#### БП-7. Критичность

- Для страницы `Пакеты` используется поле `criticality`, а не `priority`.
- Допустимые значения:
  - `high`;
  - `low`;
  - `null`.
- Критичность пакета вычисляется как максимум по входящим элементам:
  - если хотя бы один элемент имеет `high`, пакет имеет `high`;
  - иначе, если хотя бы один элемент имеет `low`, пакет имеет `low`;
  - иначе возвращается `null`.

#### БП-8. Жизненный цикл пакета после создания

- На странице `Пакеты` пакет после создания доступен только для просмотра.
- Пакетные решения `ratify` и `reject` выполняются на странице `Согласования`.
- Если внутри пакета по отдельным элементам приняты индивидуальные решения и активных элементов остаётся меньше 2:
  - пакет перестаёт отображаться как карточка пакета на странице `Согласования`;
  - запись `package` сохраняется;
  - пакетный контекст остаётся доступен в истории соответствующих `ApprovalInstance`.

#### БП-9. Что не входит в MVP

Не входят в MVP:
- backend-черновики пакетов;
- редактирование состава уже созданного пакета;
- отдельный выбор `ratifier` на странице `Пакеты`;
- поиск;
- сортировка;
- развитые фильтры;
- шаблоны пакетов;
- автоматическое формирование пакетов.

## Границы MVP

### Входит в MVP

- API очереди элементов `awaiting_ratification`;
- создание и немедленная отправка пакета;
- список отправленных пакетов текущего пользователя;
- детальная карточка пакета;
- общий endpoint `POST /api/v1/packages/{id}/action` для пакетных решений на странице `Согласования`.

### Не входит в MVP

- backend-сохранение черновиков;
- любые действия редактирования уже созданного пакета;
- ручной фильтр по продукту;
- отдельная страница истории пакетов;
- legacy-значения критичности `critical` и `medium`.

## Пользовательские сценарии

### Сценарий 1. Просмотр очереди

1. Пользователь открывает страницу `Пакеты`.
2. Backend возвращает элементы с `ApprovalInstance.status = awaiting_ratification`.
3. Элементы, уже входящие в активный пакет, в очередь не попадают.

### Сценарий 2. Создание пакета

1. Пользователь выбирает 2 и более элемента.
2. Заполняет бриф пакета.
3. Отправляет `POST /api/v1/packages`.
4. Backend создаёт пакет и переводит выбранные элементы в `in_ratification`.
5. Элементы исчезают из очереди и появляются в списке `Мои пакеты`.

### Сценарий 3. Просмотр списка пакетов

1. Пользователь открывает блок `Мои пакеты`.
2. Backend возвращает только уже созданные пакеты текущего пользователя.

### Сценарий 4. Просмотр деталки пакета

1. Пользователь открывает пакет.
2. Backend возвращает шапку пакета, бриф и список входящих элементов.
3. Для каждого элемента возвращается полный контекст, достаточный для страницы `Пакеты` и страницы `Согласования`.

## Критерии приемки

### Критерий 1. Очередь

- [ ] В очередь попадают только элементы с `ApprovalInstance.status = awaiting_ratification`
- [ ] Элементы из активных пакетов в очередь не попадают
- [ ] Для `prm` очередь ограничена элементами его продукта
- [ ] Для `methodologist` допустимы элементы разных продуктов

### Критерий 2. Создание пакета

- [ ] Пакет создаётся минимум из 2 элементов
- [ ] Backend не сохраняет черновики пакетов
- [ ] После создания пакет сразу считается отправленным
- [ ] Для каждого выбранного элемента заполняется `approval_instance.package_id`

### Критерий 3. Модель пакета

- [ ] Таблица `package` не содержит `status`
- [ ] Таблица `package` не содержит `name`
- [ ] Таблица `package` не содержит `description`
- [ ] Таблица `package` не содержит `ratifier_id`
- [ ] Отдельная таблица `package_item` отсутствует
- [ ] Текущий состав пакета определяется по `approval_instance.package_id`

### Критерий 4. Бриф и деталка

- [ ] Бриф пакета хранится в `package`
- [ ] В деталке пакета бриф показывается один раз в шапке
- [ ] Во вложенных элементах деталки пакетный бриф не дублируется
- [ ] Деталка пакета возвращает полные текущие скоркарты, включая JSON снимок скоркарты

### Критерий 5. Консистентность

- [ ] Пакет не трактуется как отдельный `ApprovalInstance`
- [ ] Пакетные решения выполняются через `POST /api/v1/packages/{id}/action`
- [ ] В API страницы `Пакеты` не возвращается `current_stage`

## Функциональные требования

### ФТ-1. Получение очереди

**Endpoint:** `GET /api/v1/packages/queue`

Правила:
- возвращает только элементы с `ApprovalInstance.status = awaiting_ratification`;
- не принимает ручных фильтров в MVP;
- применяет RBAC автоматически.

### ФТ-2. Получение списка моих пакетов

**Endpoint:** `GET /api/v1/packages/my`

Правила:
- возвращает пакеты текущего пользователя;
- возвращает только уже созданные пакеты;
- не возвращает локальные фронтовые черновики.

### ФТ-3. Создание и отправка пакета

**Endpoint:** `POST /api/v1/packages`

Запрос должен содержать:
- `approval_instance_ids` — массив из 2 и более идентификаторов;
- `brief` — бриф пакета.

### ФТ-4. Получение деталки пакета

**Endpoint:** `GET /api/v1/packages/{id}`

Ответ должен включать:
- идентификатор пакета;
- бриф пакета;
- количество элементов;
- список продуктов;
- критичность;
- дату отправки пакета;
- список элементов пакета.

### ФТ-5. Пакетные действия

**Endpoint:** `POST /api/v1/packages/{id}/action`

Поддерживаемые действия:
- `ratify`;
- `reject`.

Примечание:
- этот endpoint используется страницей `Согласования`;
- страница `Пакеты` в MVP не использует действий редактирования пакета.

### ФТ-6. Контракт элемента очереди

`PackageQueueItem` должен содержать:
- `approval_instance_id`;
- `approval_status`;
- `target_type`;
- `target_id`;
- `target_name`;
- `target_summary`;
- `product`;
- `criticality`;
- `created_at`.

### ФТ-7. Контракт карточки пакета

`PackageSummary` должен содержать:
- `package_id`;
- `brief`;
- `items_count`;
- `products`;
- `criticality`;
- `submitted_at`.

### ФТ-8. Контракт ответа на создание пакета

`POST /api/v1/packages` должен возвращать компактный объект созданного пакета:
- `package_id`;
- `brief`;
- `items_count`;
- `submitted_at`;
- массив `items`.

Каждый элемент `items` в ответе на создание должен содержать:
- `approval_instance_id`;
- `approval_status`;
- `target_type`;
- `target_id`;
- `submitted_at`;
- `target`;
- `scorecards`;
- `history`.

Примечание:
- в ответе на создание пакета не возвращаются поля `products` и `criticality`;
- внутри `target` в ответе на создание не возвращается `url`, так как ссылка нужна только на деталке пакета;
- внутри `target` backend возвращает `approval_purpose` — текст, поясняющий, для чего именно запрошено согласование или утверждение по данному элементу;
- комментарии согласовавших и утверждающих возвращаются в `history.approval_stages[].decisions[].comment` и `history.ratification_stage.decisions[].comment`.

### ФТ-9. Контракт деталки пакета

`PackageDetail` должен содержать:
- поля `PackageSummary`;
- массив `items`.

Каждый элемент `items` должен содержать:
- `approval_instance_id`;
- `approval_status`;
- `target_type`;
- `target_id`;
- `submitted_at`;
- `target`;
- `scorecards`;
- `history`.

Примечание:
- контракт деталки пакета должен быть достаточен и для страницы `Пакеты`, и для деталки пакета на странице `Согласования`;
- на деталке пакета внутри `target` возвращается `url` для перехода к связанному доменному элементу;
- внутри `target` backend возвращает `approval_purpose` — текст, поясняющий, для чего именно запрошено согласование или утверждение по данному элементу;
- для связанных скоркарт backend возвращает полные текущие снимки, включая JSON скоркарты целиком;
- транспортные метаполя скоркарты не дублируются внутри `scorecard_json`: `is_manual`, `url`, `created_at`, `updated_at` возвращаются только на верхнем уровне объекта скоркарты;
- если `is_manual = false`, backend должен вернуть `url` скоркарты.

## Описание модели данных

### Таблица `approval_instance` (используемые поля)

| Поле | Тип | Обязательность | Описание |
|---|---|---|---|
| `id` | UUID | Да | Идентификатор процесса согласования/утверждения |
| `target_type` | ENUM | Да | Тип доменной версии: `PILOT_VERSION` или `DEPLOYMENT_VERSION` |
| `target_id` | UUID | Да | Идентификатор доменной версии |
| `status` | ENUM | Да | Текущий статус `ApprovalInstance` |
| `package_id` | UUID, FK | Нет | Идентификатор активного пакета, если элемент сейчас включён в пакет |
| `brief_subject` | VARCHAR(255) | Нет | Тема брифа `ApprovalInstance` |
| `brief_body` | TEXT | Нет | Тело брифа `ApprovalInstance` |
| `process_snapshot` | JSONB | Да | История этапов, решений и переходов статусов |
| `created_at` | TIMESTAMP WITH TIME ZONE | Да | Дата создания процесса |

### Таблица `package`

| Поле | Тип | Обязательность | Описание |
|---|---|---|---|
| `id` | UUID | Да | Идентификатор пакета |
| `brief_subject` | VARCHAR(255) | Нет | Тема брифа пакета |
| `brief_body` | TEXT | Нет | Тело брифа пакета |
| `created_by` | UUID | Да | Пользователь, создавший пакет |
| `created_at` | TIMESTAMP WITH TIME ZONE | Да | Момент создания пакета; в API используется как дата отправки пакета |

Примечание:
- поля `status`, `name`, `description`, `ratifier_id` в таблице `package` отсутствуют.
- отдельная таблица `package_item` не используется;
- отдельная таблица истории пакетных решений в MVP не задаётся.

## Спецификация API (OpenAPI)

```yaml
openapi: 3.0.3
info:
  title: Packages Page Backend API
  version: 1.0.0
paths:
  /api/v1/packages/queue:
    get:
      summary: Получить очередь ожидания утверждения
      responses:
        '200':
          description: Очередь элементов
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PackageQueueResponse'
  /api/v1/packages/my:
    get:
      summary: Получить список пакетов текущего пользователя
      responses:
        '200':
          description: Список пакетов
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PackageListResponse'
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
  /api/v1/packages/{id}:
    get:
      summary: Получить деталку пакета
      parameters:
        - in: path
          name: id
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Детальная карточка пакета
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PackageDetailResponse'
  /api/v1/packages/{id}/action:
    post:
      summary: Выполнить пакетное решение
      parameters:
        - in: path
          name: id
          required: true
          schema:
            type: string
            format: uuid
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PackageActionRequest'
      responses:
        '200':
          description: Действие выполнено
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PackageActionResponse'
components:
  schemas:
    PackageQueueResponse:
      type: object
      required: [items, total]
      properties:
        items:
          type: array
          items:
            $ref: '#/components/schemas/PackageQueueItem'
        total:
          type: integer
    PackageListResponse:
      type: object
      required: [items, total]
      properties:
        items:
          type: array
          items:
            $ref: '#/components/schemas/PackageSummary'
        total:
          type: integer
    PackageDetailResponse:
      type: object
      required: [package]
      properties:
        package:
          $ref: '#/components/schemas/PackageDetail'
    PackageCreateResponse:
      type: object
      required: [package]
      properties:
        package:
          $ref: '#/components/schemas/PackageCreateResult'
    PackageQueueItem:
      type: object
      required:
        - approval_instance_id
        - approval_status
        - target_type
        - target_id
        - target_name
        - product
        - created_at
      properties:
        approval_instance_id:
          type: string
          format: uuid
        approval_status:
          type: string
          enum: [awaiting_ratification]
        target_type:
          type: string
          enum: [PILOT_VERSION, DEPLOYMENT_VERSION]
        target_id:
          type: string
          format: uuid
        target_name:
          type: string
        target_summary:
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
    PackageSummary:
      type: object
      required:
        - package_id
        - brief
        - items_count
        - products
        - submitted_at
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
    PackageDetail:
      allOf:
        - $ref: '#/components/schemas/PackageSummary'
        - type: object
          required: [items]
          properties:
            items:
              type: array
              items:
                $ref: '#/components/schemas/PackageDetailItem'
    PackageCreateResult:
      type: object
      required:
        - package_id
        - brief
        - items_count
        - submitted_at
        - items
      properties:
        package_id:
          type: string
          format: uuid
        brief:
          $ref: '#/components/schemas/BriefInfo'
        items_count:
          type: integer
        submitted_at:
          type: string
          format: date-time
        items:
          type: array
          items:
            $ref: '#/components/schemas/PackageCreateItem'
    PackageDetailItem:
      type: object
      required:
        - approval_instance_id
        - approval_status
        - target_type
        - target_id
        - submitted_at
        - target
        - scorecards
        - history
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
    PackageCreateItem:
      type: object
      required:
        - approval_instance_id
        - approval_status
        - target_type
        - target_id
        - submitted_at
        - target
        - scorecards
        - history
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
          $ref: '#/components/schemas/ApprovalTargetSummary'
        scorecards:
          type: array
          items:
            $ref: '#/components/schemas/ApprovalScorecard'
        history:
          $ref: '#/components/schemas/ApprovalHistory'
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
      required: [affected_approval_instance_ids]
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
    ProductRef:
      type: object
      required: [product_id, product_name]
      properties:
        product_id:
          type: string
          format: uuid
        product_name:
          type: string
    BriefInfo:
      type: object
      properties:
        subject:
          type: string
        body:
          type: string
          nullable: true
    ApprovalTargetSummary:
      type: object
      required: [name, approval_purpose, product, attributes]
      properties:
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
    ApprovalTarget:
      type: object
      required: [url, name, approval_purpose, product, attributes]
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
      required: [scorecard_id, display_id, name, version, status, is_manual, created_at, scorecard_json]
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
    ApprovalHistory:
      type: object
      required: [approval_stages, status_transitions]
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
      required: [stage_name, assignees, pending_assignees, decisions]
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
    UserRef:
      type: object
      required: [user_id, user_name]
      properties:
        user_id:
          type: string
          format: uuid
        user_name:
          type: string
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
          nullable: true
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
```

## Примеры запросов и ответов

### Пример 1. Получение очереди ожидания утверждения

Запрос:

```http
GET /api/v1/packages/queue
```

Ответ:

```json
{
  "items": [
    {
      "approval_instance_id": "9ce60ec3-91ef-4f6c-a9df-a96398f26f4a",
      "approval_status": "awaiting_ratification",
      "target_type": "PILOT_VERSION",
      "target_id": "5f0a6327-e5f8-4c7c-bbf6-aec9b3793914",
      "target_name": "Пилот модели LTV для POS",
      "target_summary": "Сегмент mass, волна 2",
      "product": {
        "product_id": "f8e4d590-9d58-48ae-a136-8b654cd20ed5",
        "product_name": "POS Loans"
      },
      "criticality": "high",
      "created_at": "2026-03-19T08:30:00Z"
    },
    {
      "approval_instance_id": "4149c318-f587-4ef9-9c62-0f689f5556cb",
      "approval_status": "awaiting_ratification",
      "target_type": "DEPLOYMENT_VERSION",
      "target_id": "5f8f9b6b-3c53-458c-b5e9-e0d93ff83991",
      "target_name": "Внедрение CL Revamp",
      "target_summary": "Запуск версии 3.4",
      "product": {
        "product_id": "b77d6d8b-8e88-437f-bd9d-d2957d779f0f",
        "product_name": "Consumer Loans"
      },
      "criticality": "low",
      "created_at": "2026-03-19T08:45:00Z"
    }
  ],
  "total": 2
}
```

### Пример 2. Создание и отправка пакета

Запрос:

```http
POST /api/v1/packages
Content-Type: application/json

{
  "approval_instance_ids": [
    "9ce60ec3-91ef-4f6c-a9df-a96398f26f4a",
    "4149c318-f587-4ef9-9c62-0f689f5556cb"
  ],
  "brief": {
    "subject": "Пакет мартовских изменений на утверждение",
    "body": "Просим рассмотреть и утвердить пакет изменений по POS Loans и Consumer Loans."
  }
}
```

Ответ:

```json
{
  "package": {
    "package_id": "cb70039a-a20f-4cfb-b2a4-1a9ef0fd5fa9",
    "brief": {
      "subject": "Пакет мартовских изменений на утверждение",
      "body": "Просим рассмотреть и утвердить пакет изменений по POS Loans и Consumer Loans."
    },
    "items_count": 2,
    "submitted_at": "2026-03-19T09:10:00Z",
    "items": [
      {
        "approval_instance_id": "9ce60ec3-91ef-4f6c-a9df-a96398f26f4a",
        "approval_status": "in_ratification",
        "target_type": "PILOT_VERSION",
        "target_id": "5f0a6327-e5f8-4c7c-bbf6-aec9b3793914",
        "submitted_at": "2026-03-19T09:10:00Z",
        "target": {
          "name": "Пилот модели LTV для POS",
          "description": "Сегмент mass, волна 2",
          "approval_purpose": "Согласование активации с отложенной датой",
          "version": "7",
          "product": {
            "product_id": "f8e4d590-9d58-48ae-a136-8b654cd20ed5",
            "product_name": "POS Loans"
          },
          "criticality": "high",
          "created_at": "2026-03-10T08:00:00Z",
          "attributes": []
        },
        "scorecards": [
          {
            "scorecard_id": "0f5ef419-df87-44bb-9609-c9ae07fd98a1",
            "display_id": "SC-501",
            "name": "POS LTV март",
            "description": "Текущая скоркарта пилота",
            "version": 4,
            "status": "in_ratification",
            "criticality": "high",
            "is_manual": false,
            "url": "/scorecards/0f5ef419-df87-44bb-9609-c9ae07fd98a1",
            "created_at": "2026-03-12T08:00:00Z",
            "updated_at": "2026-03-19T09:05:00Z",
            "scorecard_json": {
              "financial_effects": {
                "ar": "+1.4M",
                "volume": "+7%",
                "npv": "+3.1M",
                "rc": "-0.2%"
              },
              "switches": {
                "all_subproducts": true,
                "only_new_clients": false
              }
            }
          }
        ],
        "history": {
          "approval_stages": [
            {
              "stage_order": 1,
              "stage_name": "Риск-менеджмент",
              "started_at": "2026-03-18T10:00:00Z",
              "completed_at": "2026-03-18T10:45:00Z",
              "assignees": [
                {
                  "user_id": "7ef8a8df-44ba-43ff-9ec6-9a71f6601111",
                  "user_name": "Иван Петров"
                },
                {
                  "user_id": "c6bcf3d1-29d4-43a7-a22b-72b2774c2222",
                  "user_name": "Мария Смирнова"
                }
              ],
              "pending_assignees": [],
              "decisions": [
                {
                  "user_id": "7ef8a8df-44ba-43ff-9ec6-9a71f6601111",
                  "user_name": "Иван Петров",
                  "decision": "approve",
                  "comment": "Риски проверены, замечаний нет.",
                  "decided_at": "2026-03-18T10:21:00Z"
                },
                {
                  "user_id": "c6bcf3d1-29d4-43a7-a22b-72b2774c2222",
                  "user_name": "Мария Смирнова",
                  "decision": "approve",
                  "comment": "Согласовано при сохранении текущих порогов cut-off.",
                  "decided_at": "2026-03-18T10:45:00Z"
                }
              ]
            },
            {
              "stage_order": 2,
              "stage_name": "Методология",
              "started_at": "2026-03-18T10:50:00Z",
              "completed_at": "2026-03-18T11:10:00Z",
              "assignees": [
                {
                  "user_id": "bb9324bf-4f41-47fa-8d95-20a5146b3333",
                  "user_name": "Елена Кузнецова"
                }
              ],
              "pending_assignees": [],
              "decisions": [
                {
                  "user_id": "bb9324bf-4f41-47fa-8d95-20a5146b3333",
                  "user_name": "Елена Кузнецова",
                  "decision": "approve",
                  "comment": "Финансовые эффекты подтверждены.",
                  "decided_at": "2026-03-18T11:10:00Z"
                }
              ]
            }
          ],
          "ratification_stage": {
            "stage_order": null,
            "stage_name": "Утверждение",
            "started_at": "2026-03-19T09:10:00Z",
            "completed_at": null,
            "assignees": [
              {
                "user_id": "5bc0c0d2-5de8-4c06-9822-f3acbeef4444",
                "user_name": "Алексей Орлов"
              }
            ],
            "pending_assignees": [
              {
                "user_id": "5bc0c0d2-5de8-4c06-9822-f3acbeef4444",
                "user_name": "Алексей Орлов"
              }
            ],
            "decisions": []
          },
          "status_transitions": [
            {
              "from_status": "in_approval",
              "to_status": "approved",
              "timestamp": "2026-03-18T11:10:00Z",
              "user_id": "bb9324bf-4f41-47fa-8d95-20a5146b3333"
            },
            {
              "from_status": "approved",
              "to_status": "awaiting_ratification",
              "timestamp": "2026-03-18T11:10:01Z",
              "user_id": null
            },
            {
              "from_status": "awaiting_ratification",
              "to_status": "in_ratification",
              "timestamp": "2026-03-19T09:10:00Z",
              "user_id": "1f9e2f20-2cf7-4bd0-b5d0-11eb6a0cc300"
            }
          ],
          "package_context": null
        }
      },
      {
        "approval_instance_id": "4149c318-f587-4ef9-9c62-0f689f5556cb",
        "approval_status": "in_ratification",
        "target_type": "DEPLOYMENT_VERSION",
        "target_id": "5f8f9b6b-3c53-458c-b5e9-e0d93ff83991",
        "submitted_at": "2026-03-19T09:10:00Z",
        "target": {
          "name": "Внедрение CL Revamp",
          "description": "Запуск версии 3.4",
          "approval_purpose": "Утверждение внедрения версии 3.4 в продуктив",
          "version": "3.4",
          "product": {
            "product_id": "b77d6d8b-8e88-437f-bd9d-d2957d779f0f",
            "product_name": "Consumer Loans"
          },
          "criticality": "low",
          "created_at": "2026-03-11T09:15:00Z",
          "attributes": []
        },
        "scorecards": [],
        "history": {
          "approval_stages": [
            {
              "stage_order": 1,
              "stage_name": "Риск-менеджмент",
              "started_at": "2026-03-18T12:00:00Z",
              "completed_at": "2026-03-18T12:25:00Z",
              "assignees": [
                {
                  "user_id": "1e1d4a38-b53f-4b89-b44b-883706c25555",
                  "user_name": "Ольга Федорова"
                }
              ],
              "pending_assignees": [],
              "decisions": [
                {
                  "user_id": "1e1d4a38-b53f-4b89-b44b-883706c25555",
                  "user_name": "Ольга Федорова",
                  "decision": "approve",
                  "comment": "Согласовано, rollout допустим.",
                  "decided_at": "2026-03-18T12:25:00Z"
                }
              ]
            }
          ],
          "ratification_stage": {
            "stage_order": null,
            "stage_name": "Утверждение",
            "started_at": "2026-03-19T09:10:00Z",
            "completed_at": null,
            "assignees": [
              {
                "user_id": "5bc0c0d2-5de8-4c06-9822-f3acbeef4444",
                "user_name": "Алексей Орлов"
              }
            ],
            "pending_assignees": [
              {
                "user_id": "5bc0c0d2-5de8-4c06-9822-f3acbeef4444",
                "user_name": "Алексей Орлов"
              }
            ],
            "decisions": []
          },
          "status_transitions": [
            {
              "from_status": "in_approval",
              "to_status": "approved",
              "timestamp": "2026-03-18T12:25:00Z",
              "user_id": "1e1d4a38-b53f-4b89-b44b-883706c25555"
            },
            {
              "from_status": "approved",
              "to_status": "awaiting_ratification",
              "timestamp": "2026-03-18T12:25:01Z",
              "user_id": null
            },
            {
              "from_status": "awaiting_ratification",
              "to_status": "in_ratification",
              "timestamp": "2026-03-19T09:10:00Z",
              "user_id": "1f9e2f20-2cf7-4bd0-b5d0-11eb6a0cc300"
            }
          ],
          "package_context": null
        }
      }
    ]
  }
}
```

### Пример 3. Получение деталки пакета

Запрос:

```http
GET /api/v1/packages/cb70039a-a20f-4cfb-b2a4-1a9ef0fd5fa9
```

Ответ:

```json
{
  "package": {
    "package_id": "cb70039a-a20f-4cfb-b2a4-1a9ef0fd5fa9",
    "brief": {
      "subject": "Пакет мартовских изменений на утверждение",
      "body": "Просим рассмотреть и утвердить пакет изменений по POS Loans и Consumer Loans."
    },
    "items_count": 2,
    "products": [
      {
        "product_id": "f8e4d590-9d58-48ae-a136-8b654cd20ed5",
        "product_name": "POS Loans"
      },
      {
        "product_id": "b77d6d8b-8e88-437f-bd9d-d2957d779f0f",
        "product_name": "Consumer Loans"
      }
    ],
    "criticality": "high",
    "submitted_at": "2026-03-19T09:10:00Z",
    "items": [
      {
        "approval_instance_id": "9ce60ec3-91ef-4f6c-a9df-a96398f26f4a",
        "approval_status": "in_ratification",
        "target_type": "PILOT_VERSION",
        "target_id": "5f0a6327-e5f8-4c7c-bbf6-aec9b3793914",
        "submitted_at": "2026-03-19T09:10:00Z",
        "target": {
          "url": "/pilots/5f0a6327-e5f8-4c7c-bbf6-aec9b3793914",
          "name": "Пилот модели LTV для POS",
          "description": "Сегмент mass, волна 2",
          "approval_purpose": "Согласование активации с отложенной датой",
          "version": "7",
          "product": {
            "product_id": "f8e4d590-9d58-48ae-a136-8b654cd20ed5",
            "product_name": "POS Loans"
          },
          "criticality": "high",
          "created_at": "2026-03-10T08:00:00Z",
          "attributes": []
        },
        "scorecards": [
          {
            "scorecard_id": "0f5ef419-df87-44bb-9609-c9ae07fd98a1",
            "display_id": "SC-501",
            "name": "POS LTV март",
            "description": "Текущая скоркарта пилота",
            "version": 4,
            "status": "in_ratification",
            "criticality": "high",
            "is_manual": false,
            "url": "/scorecards/0f5ef419-df87-44bb-9609-c9ae07fd98a1",
            "created_at": "2026-03-12T08:00:00Z",
            "updated_at": "2026-03-19T09:05:00Z",
            "scorecard_json": {
              "financial_effects": {
                "ar": "+1.4M",
                "volume": "+7%",
                "npv": "+3.1M",
                "rc": "-0.2%"
              },
              "switches": {
                "all_subproducts": true
              }
            }
          }
        ],
        "history": {
          "approval_stages": [
            {
              "stage_order": 1,
              "stage_name": "Риск-менеджмент",
              "started_at": "2026-03-18T10:00:00Z",
              "completed_at": "2026-03-18T10:45:00Z",
              "assignees": [
                {
                  "user_id": "7ef8a8df-44ba-43ff-9ec6-9a71f6601111",
                  "user_name": "Иван Петров"
                },
                {
                  "user_id": "c6bcf3d1-29d4-43a7-a22b-72b2774c2222",
                  "user_name": "Мария Смирнова"
                }
              ],
              "pending_assignees": [],
              "decisions": [
                {
                  "user_id": "7ef8a8df-44ba-43ff-9ec6-9a71f6601111",
                  "user_name": "Иван Петров",
                  "decision": "approve",
                  "comment": "Риски проверены, замечаний нет.",
                  "decided_at": "2026-03-18T10:21:00Z"
                },
                {
                  "user_id": "c6bcf3d1-29d4-43a7-a22b-72b2774c2222",
                  "user_name": "Мария Смирнова",
                  "decision": "approve",
                  "comment": "Согласовано при сохранении текущих порогов cut-off.",
                  "decided_at": "2026-03-18T10:45:00Z"
                }
              ]
            },
            {
              "stage_order": 2,
              "stage_name": "Методология",
              "started_at": "2026-03-18T10:50:00Z",
              "completed_at": "2026-03-18T11:10:00Z",
              "assignees": [
                {
                  "user_id": "bb9324bf-4f41-47fa-8d95-20a5146b3333",
                  "user_name": "Елена Кузнецова"
                }
              ],
              "pending_assignees": [],
              "decisions": [
                {
                  "user_id": "bb9324bf-4f41-47fa-8d95-20a5146b3333",
                  "user_name": "Елена Кузнецова",
                  "decision": "approve",
                  "comment": "Финансовые эффекты подтверждены.",
                  "decided_at": "2026-03-18T11:10:00Z"
                }
              ]
            }
          ],
          "ratification_stage": {
            "stage_order": null,
            "stage_name": "Утверждение",
            "started_at": "2026-03-19T09:10:00Z",
            "completed_at": null,
            "assignees": [
              {
                "user_id": "5bc0c0d2-5de8-4c06-9822-f3acbeef4444",
                "user_name": "Алексей Орлов"
              }
            ],
            "pending_assignees": [
              {
                "user_id": "5bc0c0d2-5de8-4c06-9822-f3acbeef4444",
                "user_name": "Алексей Орлов"
              }
            ],
            "decisions": []
          },
          "status_transitions": [
            {
              "from_status": "in_approval",
              "to_status": "approved",
              "timestamp": "2026-03-18T11:10:00Z",
              "user_id": "bb9324bf-4f41-47fa-8d95-20a5146b3333"
            },
            {
              "from_status": "approved",
              "to_status": "awaiting_ratification",
              "timestamp": "2026-03-18T11:10:01Z",
              "user_id": null
            },
            {
              "from_status": "awaiting_ratification",
              "to_status": "in_ratification",
              "timestamp": "2026-03-19T09:10:00Z",
              "user_id": "1f9e2f20-2cf7-4bd0-b5d0-11eb6a0cc300"
            }
          ],
          "package_context": null
        }
      },
      {
        "approval_instance_id": "4149c318-f587-4ef9-9c62-0f689f5556cb",
        "approval_status": "in_ratification",
        "target_type": "DEPLOYMENT_VERSION",
        "target_id": "5f8f9b6b-3c53-458c-b5e9-e0d93ff83991",
        "submitted_at": "2026-03-19T09:10:00Z",
        "target": {
          "url": "/deployments/5f8f9b6b-3c53-458c-b5e9-e0d93ff83991",
          "name": "Внедрение CL Revamp",
          "description": "Запуск версии 3.4",
          "approval_purpose": "Утверждение внедрения версии 3.4 в продуктив",
          "version": "3.4",
          "product": {
            "product_id": "b77d6d8b-8e88-437f-bd9d-d2957d779f0f",
            "product_name": "Consumer Loans"
          },
          "criticality": "low",
          "created_at": "2026-03-11T09:15:00Z",
          "attributes": []
        },
        "scorecards": [],
        "history": {
          "approval_stages": [
            {
              "stage_order": 1,
              "stage_name": "Риск-менеджмент",
              "started_at": "2026-03-18T12:00:00Z",
              "completed_at": "2026-03-18T12:25:00Z",
              "assignees": [
                {
                  "user_id": "1e1d4a38-b53f-4b89-b44b-883706c25555",
                  "user_name": "Ольга Федорова"
                }
              ],
              "pending_assignees": [],
              "decisions": [
                {
                  "user_id": "1e1d4a38-b53f-4b89-b44b-883706c25555",
                  "user_name": "Ольга Федорова",
                  "decision": "approve",
                  "comment": "Согласовано, rollout допустим.",
                  "decided_at": "2026-03-18T12:25:00Z"
                }
              ]
            }
          ],
          "ratification_stage": {
            "stage_order": null,
            "stage_name": "Утверждение",
            "started_at": "2026-03-19T09:10:00Z",
            "completed_at": null,
            "assignees": [
              {
                "user_id": "5bc0c0d2-5de8-4c06-9822-f3acbeef4444",
                "user_name": "Алексей Орлов"
              }
            ],
            "pending_assignees": [
              {
                "user_id": "5bc0c0d2-5de8-4c06-9822-f3acbeef4444",
                "user_name": "Алексей Орлов"
              }
            ],
            "decisions": []
          },
          "status_transitions": [
            {
              "from_status": "in_approval",
              "to_status": "approved",
              "timestamp": "2026-03-18T12:25:00Z",
              "user_id": "1e1d4a38-b53f-4b89-b44b-883706c25555"
            },
            {
              "from_status": "approved",
              "to_status": "awaiting_ratification",
              "timestamp": "2026-03-18T12:25:01Z",
              "user_id": null
            },
            {
              "from_status": "awaiting_ratification",
              "to_status": "in_ratification",
              "timestamp": "2026-03-19T09:10:00Z",
              "user_id": "1f9e2f20-2cf7-4bd0-b5d0-11eb6a0cc300"
            }
          ],
          "package_context": null
        }
      }
    ]
  }
}
```

### Пример 4. Пакетное решение

Запрос:

```http
POST /api/v1/packages/cb70039a-a20f-4cfb-b2a4-1a9ef0fd5fa9/action
Content-Type: application/json

{
  "action": "ratify",
  "comment": "Утверждено пакетом"
}
```

Ответ:

```json
{
  "affected_approval_instance_ids": [
    "9ce60ec3-91ef-4f6c-a9df-a96398f26f4a",
    "4149c318-f587-4ef9-9c62-0f689f5556cb"
  ],
  "notification": "Пакет утверждён",
  "resulting_statuses": [
    {
      "approval_instance_id": "9ce60ec3-91ef-4f6c-a9df-a96398f26f4a",
      "status": "ratified"
    },
    {
      "approval_instance_id": "4149c318-f587-4ef9-9c62-0f689f5556cb",
      "status": "ratified"
    }
  ]
}
```

## Ошибки и валидация

### Валидации создания пакета

- `approval_instance_ids` должен содержать минимум 2 уникальных значения.
- Все элементы должны быть доступны пользователю по RBAC.
- Все элементы должны находиться в `awaiting_ratification`.
- Ни один элемент не должен входить в другой активный пакет.
- `brief` обязателен.
- Внутри `brief` хотя бы одно из полей `subject` или `body` должно быть непустым.

### Валидации пакетного действия

- Допустимы только `ratify` и `reject`.
- Пакетное действие разрешено только для активной группировки с 2 и более элементами в `in_ratification`.
- Текущий пользователь должен иметь право выполнить ratification-действие по всем активным элементам пакета.
- Если состав пакета изменился конкурентно и активных элементов стало меньше 2, backend должен вернуть конфликт состояния.

### Ошибки API

- `400 Bad Request` — неверная структура запроса.
- `403 Forbidden` — пользователь не имеет доступа к элементу или пакету.
- `404 Not Found` — пакет или элемент не найден.
- `409 Conflict` — состояние объекта изменилось конкурентно:
  - элемент уже ушёл из `awaiting_ratification`;
  - элемент уже попал в другой активный пакет;
  - активная пакетная группировка уже распалась.
- `422 Unprocessable Entity` — нарушено бизнес-правило:
  - передано меньше 2 элементов;
  - передан пустой бриф.

## Интеграция и консистентность

### С `approval_core`

- Очередь страницы `Пакеты` строится только по `ApprovalInstance.status = awaiting_ratification`.
- После создания пакета связанные `ApprovalInstance` переходят в `in_ratification`.
- Пакет не является отдельным target процесса.

### Со страницей `Согласования`

- Карточка пакета на вкладке `На утверждении` строится по `package` и связанным `ApprovalInstance`.
- Если в активной группировке остаётся меньше 2 элементов со статусом `in_ratification`, пакет перестаёт возвращаться как карточка пакета на странице `Согласования`.
- Финальные пакетные решения выполняются через `POST /api/v1/packages/{id}/action`.
- Контракт `GET /api/v1/packages/{id}` должен быть одинаковым для страницы `Пакеты` и страницы `Согласования`.

### С RBAC

- Для `prm` backend автоматически ограничивает очередь и доступные для пакетирования элементы своим продуктом.
- Для `methodologist` backend допускает смешанный пакет из элементов разных продуктов.

### По критичности

- На странице `Пакеты`, на странице `Согласования` и в доменной модели используется единое поле `criticality`.
- Для этих требований допустимы только:
  - `high`;
  - `low`;
  - `null`.
