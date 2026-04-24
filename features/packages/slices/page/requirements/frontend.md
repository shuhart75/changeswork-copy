# Страница "Пакеты" (Frontend)

Статус: **для передачи команде**  
Область: MVP  
Дата обновления: 2026-03-21

## Оглавление
1. [Бизнес-требования](#бизнес-требования)
2. [Границы MVP](#границы-mvp)
3. [Пользовательские требования к АС КОДА](#пользовательские-требования-к-ас-кода)
4. [Критерии приемки](#критерии-приемки)
5. [Функциональные требования](#функциональные-требования)
6. [Описание UI-модели данных](#описание-ui-модели-данных)
7. [Интеграция с Backend API](#интеграция-с-backend-api)
8. [Примеры запросов и ответов](#примеры-запросов-и-ответов)
9. [Валидация](#валидация)
10. [Обработка ошибок](#обработка-ошибок)
11. [Интеграция и консистентность](#интеграция-и-консистентность)

## Бизнес-требования

### Цель

Реализовать Frontend для страницы `Пакеты`, чтобы пользователь мог:
- видеть очередь элементов, ожидающих ручного запуска утверждения;
- локально выбрать несколько элементов и отправить их как пакет;
- просматривать свои отправленные пакеты;
- открывать пакет и видеть его состав;
- работать консистентно со страницей `Согласования`.

### Контекст

Под доменным элементом в рамках страницы `Пакеты` понимается версия согласуемой предметной сущности:
- `PilotVersion`;
- `DeploymentVersion`.

Ключевые правила MVP:
- фронт не вычисляет очередь по статусам доменных сущностей;
- фронт не вычисляет пакетную группировку по сырым данным;
- фронт не хранит backend-черновик пакета;
- пакет создаётся единственным запросом `POST /api/v1/packages`;
- после создания пакет доступен только для просмотра;
- на странице `Пакеты` не выбирается отдельный `ratifier`;
- для страницы используется `criticality`, а не `priority`.

Допустимые значения `criticality`:
- `high`;
- `low`;
- `null`.

## Границы MVP

### Входит в MVP

- Маршрут `/packages`.
- Блок `Очередь ожидания утверждения`.
- Локальный выбор элементов для отправки пакета.
- Форма брифа пакета.
- Отправка пакета.
- Блок `Мои пакеты`.
- Деталка пакета в режиме просмотра.

### Не входит в MVP

- backend-черновики пакетов;
- редактирование уже созданного пакета;
- удаление пакета;
- выбор `ratifier` на этой странице;
- поиск;
- сортировка;
- ручные фильтры;
- drag-and-drop.

## Пользовательские требования к АС КОДА

### ПТ-1. Структура страницы

**Описание:** Страница должна содержать две рабочие области.

**Детали:**
- `Очередь ожидания утверждения` — элементы с `ApprovalInstance.status = awaiting_ratification`.
- `Мои пакеты` — список уже созданных пакетов текущего пользователя.
- Страница доступна ролям `prm`, `methodologist`, `admin`.

### ПТ-2. Очередь ожидания утверждения

**Описание:** Пользователь должен видеть только элементы, доступные ему для пакетирования.

**Детали:**
- показываются только элементы со статусом `awaiting_ratification`;
- элементы, уже входящие в активный пакет, не показываются;
- для `prm` backend уже возвращает только элементы его продукта;
- для `methodologist` backend может вернуть элементы разных продуктов;
- для элемента показываются:
  - тип;
  - название;
  - краткое описание;
  - продукт;
  - критичность;
  - дата создания;
  - чекбокс выбора.

### ПТ-3. Локальное формирование пакета

**Описание:** Пользователь должен иметь возможность выбрать несколько элементов и отправить пакет без промежуточного сохранения на backend.

**Детали:**
- пользователь выбирает элементы очереди чекбоксами;
- кнопка отправки пакета становится доступной, когда выбрано не меньше 2 элементов;
- перед отправкой пользователь заполняет бриф пакета;
- отдельный сохранённый backend-черновик не создаётся.

### ПТ-4. Бриф пакета

**Описание:** Пользователь должен задать данные брифа пакета перед отправкой.

**Детали:**
- форма брифа содержит:
  - тему;
  - текст брифа.
- после успешной отправки бриф отображается в шапке деталки пакета;
- во вложенных элементах пакета блок брифа не дублируется.

### ПТ-5. Отправка пакета

**Описание:** Пользователь должен иметь возможность отправить выбранные элементы как пакет.

**Детали:**
- отправка выполняется вызовом `POST /api/v1/packages`;
- после успешной отправки:
  - элементы исчезают из очереди;
  - новый пакет появляется в списке `Мои пакеты`;
  - пакет открывается только в режиме просмотра;
  - фронт получает компактный ответ о созданном пакете и при необходимости догружает полную деталку через `GET /api/v1/packages/{id}`.

### ПТ-6. Список `Мои пакеты`

**Описание:** Пользователь должен видеть список уже созданных пакетов.

**Детали:**
- список содержит только отправленные пакеты текущего пользователя;
- карточка пакета должна показывать:
  - ярлык пакета, построенный на фронте как `PKG-{packageId}`;
  - тему брифа;
  - количество элементов;
  - продукты;
  - критичность;
  - дату отправки.

### ПТ-7. Деталка пакета

**Описание:** Пользователь должен иметь возможность открыть пакет и посмотреть его состав.

**Детали:**
- в шапке показываются:
  - ярлык пакета;
  - бриф пакета;
  - количество элементов;
  - продукты;
  - критичность;
  - дата отправки.
- для каждого входящего элемента показываются:
  - тип;
  - название;
  - описание;
  - текст, поясняющий, для чего именно запрошено согласование или утверждение;
  - ссылка на связанный доменный элемент;
  - продукт;
  - критичность;
  - текущий статус `ApprovalInstance`;
  - связанные скоркарты;
  - история процесса.

### ПТ-8. Критичность и статусы

**Описание:** UI должен использовать только актуальные значения.

**Детали:**
- для `criticality` допустимы:
  - `high`;
  - `low`;
  - отсутствие значения.
- для этапов фронт не типизирует отдельный enum статусов.
- текущее состояние элемента фронт определяет только по `approvalStatus`.
- поле `current_stage` фронт не ожидает.

## Критерии приемки

### КП-1. Очередь

- [ ] В очереди показываются только элементы с `awaiting_ratification`
- [ ] Элементы из активных пакетов в очереди не показываются
- [ ] Для `prm` не отображаются элементы чужих продуктов
- [ ] Для `methodologist` допустимы элементы разных продуктов

### КП-2. Формирование и отправка пакета

- [ ] Пакет отправляется минимум из 2 элементов
- [ ] Frontend не требует backend-черновик пакета
- [ ] Перед отправкой пользователь заполняет бриф пакета
- [ ] После отправки элементы исчезают из очереди
- [ ] После отправки пакет появляется в `Моих пакетах`
- [ ] Frontend не ожидает в ответе `POST /api/v1/packages` поля `products`, `criticality` и `target.url`

### КП-3. Модель пакета

- [ ] Frontend не использует поля старой модели пакета: `status`, `name`, `description`, `ratifier`
- [ ] Frontend не ожидает поля старой модели элементов пакета: `package_item_id`, `item_status`
- [ ] Ярлык пакета строится на фронте из `packageId`

### КП-4. Деталка

- [ ] Бриф пакета показывается в шапке деталки ровно один раз
- [ ] Деталка пакета показывает полные текущие скоркарты с данными, достаточными для отображения финансовых эффектов и бинарных переключателей
- [ ] Деталка пакета показывает историю процесса по каждому элементу

### КП-5. Консистентность

- [ ] Фронт не трактует пакет как отдельный `ApprovalInstance`
- [ ] Фронт не ожидает поле `current_stage`
- [ ] Контракт деталки пакета согласован со страницей `Согласования`

## Функциональные требования

### ФТ-1. Роут

В MVP должен поддерживаться маршрут:
- `/packages`

### ФТ-2. Загрузка данных страницы

Для страницы используются endpoint'ы:
- `GET /api/v1/packages/queue`;
- `GET /api/v1/packages/my`;
- `POST /api/v1/packages`;
- `GET /api/v1/packages/{id}`.

Правила:
- очередь и список пакетов загружаются независимо;
- `POST /api/v1/packages` возвращает компактный объект созданного пакета;
- при открытии деталки фронт загружает `GET /api/v1/packages/{id}`;
- страница `Пакеты` не вызывает `POST /api/v1/packages/{id}/action`.

### ФТ-3. Компонент очереди

Компонент `PackagesQueue` должен рендерить `PackageQueueItemVm`.

#### Поля карточки элемента очереди

- тип элемента;
- название;
- краткое описание;
- продукт;
- критичность;
- дата создания;
- чекбокс выбора.

### ФТ-4. Локальная форма отправки пакета

Компонент формы отправки пакета должен:
- показывать количество выбранных элементов;
- позволять редактировать тему брифа;
- позволять редактировать текст брифа;
- отправлять `POST /api/v1/packages`.

После успешной отправки:
- фронт должен уметь обработать компактный ответ `PackageCreateResultVm`;
- если UI нужно показать продукты, критичность пакета или ссылки на связанные доменные элементы, фронт должен догрузить `PackageDetailVm` через `GET /api/v1/packages/{id}`.

### ФТ-5. Компонент списка пакетов

Компонент `PackagesList` должен рендерить `PackageSummaryVm`.

#### Поля карточки пакета

- ярлык `PKG-{packageId}`;
- тема брифа;
- количество элементов;
- список продуктов;
- критичность;
- дата отправки.

### ФТ-6. Компонент деталки пакета

Компонент `PackageDetailDialog` должен включать:
- шапку пакета;
- бриф пакета;
- список элементов пакета.

Для каждого входящего элемента показываются:
- тип и идентификатор доменного элемента;
- название и описание;
- текст, поясняющий, для чего именно запрошено согласование или утверждение;
- ссылка на связанный доменный элемент;
- продукт;
- критичность;
- текущий статус `ApprovalInstance`;
- связанные скоркарты;
- маршрут и история процесса.

### ФТ-7. Поведение после действий

- после успешной отправки пакета фронт обновляет очередь и список пакетов;
- при успешной отправке фронт может сразу открыть деталку созданного пакета;
- при ошибке отправки фронт сохраняет локально выбранные элементы и введённый бриф, пока пользователь не изменит состояние вручную.

### ФТ-8. Цветовая схема и иконки

#### Критичность

- `high` — предупреждающий акцент;
- `low` — нейтральный цвет;
- `null` — без цветного бэйджа.

#### Статусы этапов

- UI не использует отдельный enum статусов этапов.
- Визуальное состояние этапа определяется по `startedAt`, `completedAt`, `pendingAssignees` и `decisions`.

## Описание UI-модели данных

### Модель `PackageQueueItemVm`

| Поле | Тип | Обязательность | Описание |
|---|---|---|---|
| `approvalInstanceId` | `string` | Да | Идентификатор `ApprovalInstance` |
| `approvalStatus` | `'awaiting_ratification'` | Да | Статус процесса для очереди |
| `targetType` | `'PILOT_VERSION' \| 'DEPLOYMENT_VERSION'` | Да | Тип доменной версии |
| `targetId` | `string` | Да | Идентификатор доменной версии |
| `targetName` | `string` | Да | Название элемента |
| `targetSummary` | `string \| null` | Нет | Краткое описание |
| `product` | `ProductRefVm` | Да | Продукт элемента |
| `criticality` | `'high' \| 'low' \| null` | Нет | Критичность элемента |
| `createdAt` | `string` | Да | Дата создания |

### Модель `PackageSummaryVm`

| Поле | Тип | Обязательность | Описание |
|---|---|---|---|
| `packageId` | `string` | Да | Идентификатор пакета |
| `brief` | `BriefVm` | Да | Бриф пакета |
| `itemsCount` | `number` | Да | Количество элементов |
| `products` | `ProductRefVm[]` | Да | Продукты, представленные в пакете |
| `criticality` | `'high' \| 'low' \| null` | Нет | Критичность пакета |
| `submittedAt` | `string` | Да | Дата отправки пакета |

### Модель `PackageCreateResultVm`

| Поле | Тип | Обязательность | Описание |
|---|---|---|---|
| `packageId` | `string` | Да | Идентификатор созданного пакета |
| `brief` | `BriefVm` | Да | Бриф пакета |
| `itemsCount` | `number` | Да | Количество элементов |
| `submittedAt` | `string` | Да | Дата отправки пакета |
| `items` | `PackageCreateItemVm[]` | Да | Элементы, вошедшие в пакет |

### Модель `PackageDetailVm`

| Поле | Тип | Обязательность | Описание |
|---|---|---|---|
| `packageId` | `string` | Да | Идентификатор пакета |
| `brief` | `BriefVm` | Да | Бриф пакета |
| `itemsCount` | `number` | Да | Количество элементов |
| `products` | `ProductRefVm[]` | Да | Продукты пакета |
| `criticality` | `'high' \| 'low' \| null` | Нет | Критичность пакета |
| `submittedAt` | `string` | Да | Дата отправки пакета |
| `items` | `PackageItemVm[]` | Да | Элементы пакета |

### Модель `PackageCreateItemVm`

| Поле | Тип | Обязательность | Описание |
|---|---|---|---|
| `approvalInstanceId` | `string` | Да | Идентификатор `ApprovalInstance` |
| `approvalStatus` | `string` | Да | Статус `ApprovalInstance` |
| `targetType` | `'PILOT_VERSION' \| 'DEPLOYMENT_VERSION'` | Да | Тип доменной версии |
| `targetId` | `string` | Да | Идентификатор доменной версии |
| `submittedAt` | `string` | Да | Дата отправки элемента в утверждение |
| `target` | `ApprovalTargetSummaryVm` | Да | Контекст связанного доменного элемента без UI-ссылки |
| `scorecards` | `ApprovalScorecardVm[]` | Да | Полные текущие скоркарты |
| `history` | `ApprovalHistoryVm` | Да | История процесса |

### Модель `PackageItemVm`

| Поле | Тип | Обязательность | Описание |
|---|---|---|---|
| `approvalInstanceId` | `string` | Да | Идентификатор `ApprovalInstance` |
| `approvalStatus` | `string` | Да | Статус `ApprovalInstance` |
| `targetType` | `'PILOT_VERSION' \| 'DEPLOYMENT_VERSION'` | Да | Тип доменной версии |
| `targetId` | `string` | Да | Идентификатор доменной версии |
| `submittedAt` | `string` | Да | Дата отправки элемента в утверждение |
| `target` | `ApprovalTargetVm` | Да | Полный контекст связанного доменного элемента |
| `scorecards` | `ApprovalScorecardVm[]` | Да | Полные текущие скоркарты |
| `history` | `ApprovalHistoryVm` | Да | История процесса |

### Вспомогательные модели

| Поле | Тип | Обязательность | Описание |
|---|---|---|---|
| `ProductRefVm.productId` | `string` | Да | Идентификатор продукта |
| `ProductRefVm.productName` | `string` | Да | Название продукта |
| `BriefVm.subject` | `string` | Нет | Тема брифа |
| `BriefVm.body` | `string \| null` | Нет | Текст брифа |
| `ApprovalTargetSummaryVm.name` | `string` | Да | Название доменного элемента |
| `ApprovalTargetSummaryVm.description` | `string \| null` | Нет | Описание доменного элемента |
| `ApprovalTargetSummaryVm.approvalPurpose` | `string` | Да | Текст, поясняющий, для чего именно запрошено согласование или утверждение |
| `ApprovalTargetVm.url` | `string` | Да | UI-ссылка на связанный доменный элемент |
| `ApprovalScorecardVm.url` | `string \| null` | Нет | UI-ссылка на скоркарту; обязательна для не ручной скоркарты |

### Фронтовые типы

```typescript
type PackageCriticality = 'high' | 'low' | null;

interface ProductRefVm {
  productId: string;
  productName: string;
}

interface BriefVm {
  subject?: string;
  body?: string | null;
}

interface PackageQueueItemVm {
  approvalInstanceId: string;
  approvalStatus: 'awaiting_ratification';
  targetType: 'PILOT_VERSION' | 'DEPLOYMENT_VERSION';
  targetId: string;
  targetName: string;
  targetSummary: string | null;
  product: ProductRefVm;
  criticality: PackageCriticality;
  createdAt: string;
}

interface PackageSummaryVm {
  packageId: string;
  brief: BriefVm;
  itemsCount: number;
  products: ProductRefVm[];
  criticality: PackageCriticality;
  submittedAt: string;
}

interface PackageCreateResultVm {
  packageId: string;
  brief: BriefVm;
  itemsCount: number;
  submittedAt: string;
  items: PackageCreateItemVm[];
}

interface PackageCreateItemVm {
  approvalInstanceId: string;
  approvalStatus: string;
  targetType: 'PILOT_VERSION' | 'DEPLOYMENT_VERSION';
  targetId: string;
  submittedAt: string;
  target: ApprovalTargetSummaryVm;
  scorecards: ApprovalScorecardVm[];
  history: ApprovalHistoryVm;
}

interface PackageDetailVm extends PackageSummaryVm {
  items: PackageItemVm[];
}

interface PackageItemVm {
  approvalInstanceId: string;
  approvalStatus: string;
  targetType: 'PILOT_VERSION' | 'DEPLOYMENT_VERSION';
  targetId: string;
  submittedAt: string;
  target: ApprovalTargetVm;
  scorecards: ApprovalScorecardVm[];
  history: ApprovalHistoryVm;
}

interface ApprovalTargetSummaryVm {
  name: string;
  description: string | null;
  approvalPurpose: string;
  version: string | null;
  product: ProductRefVm;
  criticality: PackageCriticality;
  createdAt: string | null;
  attributes: Array<{
    key: string;
    label: string;
    value: string | null;
  }>;
}

interface ApprovalTargetVm extends ApprovalTargetSummaryVm {
  url: string;
}

interface ApprovalScorecardVm {
  scorecardId: string;
  displayId: string;
  name: string;
  description: string | null;
  version: number;
  status: string;
  criticality: PackageCriticality;
  isManual: boolean;
  url: string | null;
  createdAt: string;
  updatedAt: string | null;
  scorecardJson: Record<string, unknown>;
}

interface ApprovalHistoryVm {
  approvalStages: ApprovalHistoryStageVm[];
  ratificationStage: ApprovalHistoryStageVm | null;
  statusTransitions: Array<{
    fromStatus: string | null;
    toStatus: string;
    timestamp: string;
    userId: string | null;
  }>;
}

interface ApprovalHistoryStageVm {
  stageOrder: number | null;
  stageName: string;
  startedAt: string | null;
  completedAt: string | null;
  assignees: Array<{ userId: string; userName: string }>;
  pendingAssignees: Array<{ userId: string; userName: string }>;
  decisions: Array<{
    userId: string;
    userName: string;
    decision: string;
    comment: string | null;
    decidedAt: string;
  }>;
}
```

## Интеграция с Backend API

### Используемые endpoint'ы

- `GET /api/v1/packages/queue`
- `GET /api/v1/packages/my`
- `POST /api/v1/packages`
- `GET /api/v1/packages/{id}`

### OpenAPI-фрагмент для фронта

```yaml
openapi: 3.0.3
info:
  title: Packages Page Frontend Integration
  version: 1.0.0
paths:
  /api/v1/packages/queue:
    get:
      summary: Получить очередь ожидания утверждения
  /api/v1/packages/my:
    get:
      summary: Получить пакеты текущего пользователя
  /api/v1/packages:
    post:
      summary: Создать и отправить пакет
      requestBody:
        required: true
        content:
          application/json:
            schema:
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
                  type: object
                  properties:
                    subject:
                      type: string
                    body:
                      type: string
                      nullable: true
  /api/v1/packages/{id}:
    get:
      summary: Получить деталку пакета
```

## Примеры запросов и ответов

### Пример 1. Загрузка очереди

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
    }
  ],
  "total": 1
}
```

### Пример 2. Отправка пакета

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
                }
              ]
            }
          ],
          "ratification_stage": null,
          "status_transitions": [
            {
              "from_status": "awaiting_ratification",
              "to_status": "in_ratification",
              "timestamp": "2026-03-19T09:10:00Z",
              "user_id": "1c2d5d8e-65b0-4f9d-9e87-f3327a8c3333"
            }
          ]
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
        "scorecards": [
          {
            "scorecard_id": "b1d5b936-55ba-43d6-90e0-4f6d77ceaa44",
            "display_id": "SC-710",
            "name": "CL Revamp manual review",
            "description": "Ручная экспертная скоркарта для внедрения",
            "version": 1,
            "status": "draft",
            "criticality": "low",
            "is_manual": true,
            "url": null,
            "created_at": "2026-03-15T10:00:00Z",
            "updated_at": null,
            "scorecard_json": {
              "financial_effects": {
                "ar": "+0.9M",
                "volume": "+5%",
                "npv": "+1.8M",
                "rc": "+0.1%"
              },
              "switches": {
                "manual_override": true
              }
            }
          }
        ],
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

### Пример 3. Деталка пакета

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
                }
              ]
            }
          ],
          "ratification_stage": null,
          "status_transitions": [
            {
              "from_status": "awaiting_ratification",
              "to_status": "in_ratification",
              "timestamp": "2026-03-19T09:10:00Z",
              "user_id": "1c2d5d8e-65b0-4f9d-9e87-f3327a8c3333"
            }
          ]
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
        "scorecards": [
          {
            "scorecard_id": "b1d5b936-55ba-43d6-90e0-4f6d77ceaa44",
            "display_id": "SC-710",
            "name": "CL Revamp manual review",
            "description": "Ручная экспертная скоркарта для внедрения",
            "version": 1,
            "status": "draft",
            "criticality": "low",
            "is_manual": true,
            "url": null,
            "created_at": "2026-03-15T10:00:00Z",
            "updated_at": null,
            "scorecard_json": {
              "financial_effects": {
                "ar": "+0.9M",
                "volume": "+5%",
                "npv": "+1.8M",
                "rc": "+0.1%"
              },
              "switches": {
                "manual_override": true
              }
            }
          }
        ],
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

## Валидация

- отправка пакета доступна только при выборе 2 и более элементов;
- форма не должна отправлять пустой `brief`, в котором пусты и `subject`, и `body`;
- фронт не должен пытаться вызвать действия редактирования пакета;
- фронт не должен ожидать в ответе `POST /api/v1/packages` поля:
  - `products`;
  - `criticality`;
  - `target.url`;
- фронт не должен ожидать дублирования транспортных полей скоркарты внутри `scorecardJson`:
  - `isManual`;
  - `url`;
  - `createdAt`;
  - `updatedAt`;
- фронт не должен ожидать в ответах поля старой модели:
  - `status`;
  - `name`;
  - `description`;
  - `ratifier`;
  - `available_actions`;
  - `package_item_id`;
  - `item_status`.

## Обработка ошибок

- `400` — показать ошибку структуры запроса;
- `403` — показать сообщение о недостаточных правах;
- `404` — показать, что пакет или элемент не найден;
- `409` — показать, что состав или статусы элементов успели измениться;
- `422` — показать бизнес-ошибку валидации и сохранить локально выбранные элементы и введённый бриф.

## Интеграция и консистентность

### С backend страницы `Пакеты`

- контракт фронта должен соответствовать `final-spec/REQ_packages_page_backend.md`;
- фронт использует только `criticality = high | low | null`;
- фронт не работает с несуществующим `current_stage`.
- ответ `POST /api/v1/packages` фронт трактует как компактный ответ создания, а не как полную деталку пакета.

### Со страницей `Согласования`

- деталка пакета должна быть совместима с `GET /api/v1/packages/{id}`, который используется и на странице `Согласования`;
- пакет не считается отдельным процессом, а является группировкой `ApprovalInstance`;
- пакетные действия `ratify` и `reject` выполняются не на странице `Пакеты`, а на странице `Согласования`.
