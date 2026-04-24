# Страница "Согласования" (Frontend)

Статус: **для передачи команде**  
Область: MVP  
Дата обновления: 2026-03-21

## Оглавление
1. [Бизнес-требования](#бизнес-требования)
2. [Границы MVP](#границы-mvp)
3. [Пользовательские требования к АС КОДА](#пользовательские-требования-к-ас-кода)
4. [Критерии приемки](#критерии-приемки)
5. [Функциональные требования](#функциональные-требования)
6. [Интеграция с Backend API](#интеграция-с-backend-api)
7. [Примеры запросов и ответов](#примеры-запросов-и-ответов)
8. [Валидация](#валидация)
9. [Обработка ошибок](#обработка-ошибок)

## Бизнес-требования

### Цель

Реализовать Frontend для страницы `Согласования`, чтобы пользователь мог:
- видеть свои активные назначения на согласование и утверждение;
- принимать решения по отдельным элементам;
- выполнять массовые действия;
- работать с карточками пакетов на вкладке утверждения;
- открывать подробный контекст элемента и историю процесса;
- принимать решения по пакету целиком.

### Контекст

Под доменным элементом в рамках страницы `Согласования` понимается версия согласуемой предметной сущности:
- `PilotVersion`;
- `DeploymentVersion`.

Поле `target` в API страницы `Согласования` — это представление этого доменного элемента для UI.

`ApprovalInstance` в рамках страницы `Согласования` — это экземпляр процесса согласования/утверждения, связанный с одной конкретной версией доменного элемента (`PilotVersion` или `DeploymentVersion`).

`ApprovalInstance` хранит:
- маршрут согласования и утверждения;
- назначенных участников;
- историю решений и комментариев;
- переходы статусов процесса;
- ссылку на доменный элемент, по которому открыт процесс.

Страница `Согласования` строится на API-представлении, которое backend собирает из `ApprovalInstance` и `Package`.

Ключевое правило MVP:
- фронт не должен сам группировать сырые `ApprovalInstance` в пакеты;
- backend сразу отдаёт готовые карточки вкладки `На утверждении`:
  - одиночные;
  - пакетные.

Ещё одно ключевое правило:
- текущий этап процесса не передаётся отдельным полем `current_stage`;
- текущее состояние элемента на странице определяется по `approval_status`;
- подробный маршрут, решения и ожидающие участники показываются в деталке элемента или пакета.
- UI показывает только один блок брифа:
  - если `ApprovalInstance` входит в активный пакет, показывается бриф пакета;
  - если активного пакета нет или пакет рассыпался, показывается бриф самого `ApprovalInstance`;
- на approvals page в MVP используется `criticality`, а не `priority`;
- допустимые значения `criticality`:
  - `high`
  - `low`
  - `null`
- значения `critical`, `medium` на этой странице не используются.

## Границы MVP

### Входит в MVP

- Вкладка `На согласовании`.
- Вкладка `На утверждении`.
- Карточки одиночных элементов.
- Карточки пакетов.
- Детальная карточка элемента.
- Детальная карточка пакета.
- Индивидуальные действия.
- Массовые действия.
- Пакетные действия.

### Не входит в MVP

- Поиск.
- Сортировка.
- Развитые пользовательские фильтры.
- Ручное формирование пакета на этой странице.
- Локальная агрегация пакетов на фронте.

## Пользовательские требования к АС КОДА

### ПТ-1. Структура страницы

**Описание:** Страница должна содержать две вкладки.

**Детали:**
- `На согласовании` — для элементов в `in_approval`.
- `На утверждении` — для элементов и пакетов, относящихся к `in_ratification`.
- Пользователь с ролью только `approver` видит только вкладку `На согласовании`.
- Пользователь с ролью только `ratifier` видит только вкладку `На утверждении`.
- Пользователь с обеими ролями видит обе вкладки.

### ПТ-2. Вкладка "На согласовании"

**Описание:** Пользователь должен видеть свои текущие назначения на Approval.

**Детали:**
- Отображаются только карточки типа `single`.
- Для карточки показываются:
  - тип элемента;
  - название;
  - краткое описание доменного элемента;
  - ссылка на связанный доменный элемент;
  - продукт;
  - критичность;
  - дата отправки на согласование;
  - превью связанных скоркарт.

### ПТ-3. Вкладка "На утверждении"

**Описание:** Пользователь должен видеть свои текущие назначения на Ratification.

**Детали:**
- Отображаются:
  - карточки одиночных элементов;
  - карточки пакетов.
- На этой вкладке пакет не имеет отдельного собственного статуса карточки.
- Если карточка пакета показана пользователю, это означает, что входящие элементы уже находятся в `in_ratification`.

### ПТ-4. Детальный просмотр элемента

**Описание:** Пользователь должен иметь возможность открыть подробную карточку элемента.

**Детали:**
- Показываются:
  - один блок данных из брифа на согласование, выбранный по правилу источника брифа;
  - название и описание связанного доменного элемента;
  - ссылка на связанный доменный элемент с открытием в новом окне;
  - критичность, продукт и дата отправки на согласование;
  - все связанные скоркарты;
  - маршрут согласования/утверждения и история решений по нему.
- Правило выбора брифа:
  - если `ApprovalInstance` входит в активный пакет, UI показывает бриф пакета;
  - если активного пакета нет или пакет рассыпался, UI показывает бриф `ApprovalInstance`.
- История не должна опираться на отдельный статус этапа.
- Состояние этапа UI определяет по `startedAt`, `completedAt`, `pendingAssignees` и `decisions`.
- В маршруте должны быть видны:
  - все этапы согласования и утверждения;
  - кто уже принял решение;
  - комментарии к решениям;
  - дата и время каждого решения;
  - кто ещё не принял решение.

### ПТ-5. Детальный просмотр пакета

**Описание:** Пользователь должен иметь возможность открыть подробную карточку пакета.

**Детали:**
- Показывается шапка пакета, включая бриф пакета.
- Показывается список входящих элементов.
- Каждый входящий элемент отображается как вложенная деталка с теми же данными, что и одиночный элемент, кроме блока брифа:
  - бриф пакета показывается один раз в шапке пакета;
  - внутри входящих элементов отдельный блок брифа не дублируется.
- Так как пакет может включать разные продукты, UI должен корректно отображать несколько продуктов.
- Для каждого входящего элемента должна быть доступна ссылка на связанный доменный элемент с открытием в новом окне.

### ПТ-5.1. Открытие деталки по ссылке

**Описание:** Пользователь должен иметь возможность открыть превью/деталку `ApprovalInstance` или пакета по прямой ссылке.

**Детали:**
- По ссылке должен открываться экран `Согласования` сразу с открытой деталкой нужного элемента или пакета.
- Deep link должен поддерживаться и для `ApprovalInstance`, и для `Package`.
- Для открытия по ссылке пользователь не должен сначала вручную искать карточку в списке.
- Если деталка открыта по ссылке, UI должен восстановить это состояние после перезагрузки страницы.

### ПТ-6. Принятие решений

**Описание:** Пользователь должен иметь возможность принять доступное решение.

**Детали:**
- Для одиночного элемента на Approval:
  - `approve`
  - `reject`
  - `recall`, если действие доступно
- Для одиночного элемента на Ratification:
  - `ratify`
  - `reject`
  - `recall`, если действие доступно
- Для пакета:
  - `ratify`
  - `reject`
- Массовые действия:
  - на вкладке Approval: `approve`, `reject`
  - на вкладке Ratification: `ratify`, `reject`
- Массовый `recall` в MVP отсутствует.

### ПТ-7. Комментарии

**Описание:** Пользователь должен иметь возможность оставить комментарий к действию.

**Детали:**
- Комментарий при `reject` опционален.
- Комментарий при `approve` и `ratify` опционален.
- Комментарий при `recall` опционален.
- Фронт не должен требовать обязательный комментарий, если backend этого не требует.

### ПТ-8. Цветовая индикация

**Описание:** UI должен использовать только актуальные значения статусов и критичности.

**Детали:**
- Для `criticality`:
  - `high`
  - `low`
  - отсутствие значения
- Для этапов фронт не типизирует отдельный enum статусов.
- Для доменных статусов связанных сущностей фронт не должен использовать отдельный локальный enum страницы `Согласования`; он показывает значение, пришедшее от backend.

## Критерии приемки

### КП-1. Вкладки

- [ ] `На согласовании` показывает только элементы в `in_approval`
- [ ] `На утверждении` показывает только карточки, относящиеся к `in_ratification`
- [ ] Вкладка `На утверждении` не опирается на отдельный собственный статус пакета

### КП-2. Карточки

- [ ] На вкладке Approval показываются только карточки `single`
- [ ] На вкладке Ratification показываются карточки `single` и `package`
- [ ] Карточка пакета умеет отображать несколько продуктов
- [ ] Карточки не используют поле `current_stage`

### КП-3. Критичность

- [ ] Используются только `high`, `low` или `null`
- [ ] Значения `critical`, `medium` отсутствуют во фронтовых типах, фильтрах, бэйджах и цветовых схемах

### КП-4. История

- [ ] В истории этапов нет отдельного поля `status`
- [ ] Состояние этапа определяется по `startedAt`, `completedAt`, `pendingAssignees` и `decisions`
- [ ] Деталка `ApprovalInstance` показывает ровно один блок брифа
- [ ] Если `ApprovalInstance` входит в активный пакет, деталка показывает бриф пакета
- [ ] Если активного пакета нет или пакет рассыпался, деталка показывает бриф `ApprovalInstance`
- [ ] Деталка `ApprovalInstance` показывает название и описание связанного доменного элемента
- [ ] Деталка `ApprovalInstance` показывает критичность, продукт и дату отправки на согласование
- [ ] Деталка `ApprovalInstance` показывает полные текущие скоркарты, достаточные для отображения бинарных переключателей и финансовых эффектов
- [ ] Деталка `ApprovalInstance` показывает маршрут согласования/утверждения с решениями, комментариями, датами решений и оставшимися участниками
- [ ] Из деталки `ApprovalInstance` можно открыть связанный доменный элемент в новом окне

### КП-5. Действия

- [ ] Массовый `recall` отсутствует
- [ ] Пакетный `recall` отсутствует
- [ ] Комментарий при reject не обязателен

### КП-6. Открытие по ссылке

- [ ] Ссылка на `ApprovalInstance` открывает страницу `Согласования` сразу с деталкой нужного элемента
- [ ] Ссылка на пакет открывает страницу `Согласования` сразу с деталкой нужного пакета
- [ ] Состояние открытой по ссылке деталки сохраняется при перезагрузке страницы

## Функциональные требования

### ФТ-1. Роут и точки входа

В MVP должен поддерживаться маршрут:
- `/approvals`
- `/approvals?approval_instance_id={id}`
- `/approvals?package_id={id}`

Детальные карточки открываются:
- внутри страницы в модальном окне или drawer;
- без обязательной навигации на отдельную страницу.

Правила deeplink:
- query-параметр `approval_instance_id` открывает `ApprovalDetailDialog` сразу после загрузки страницы;
- query-параметр `package_id` открывает `PackageDetailDialog` сразу после загрузки страницы;
- пользователь может открыть только одну деталку по deeplink одновременно;
- если переданы оба параметра, приоритет не допускается: фронт должен считать URL некорректным и открыть страницу без деталки с безопасным fallback;
- закрытие деталки должно очищать соответствующий query-параметр из URL без полной перезагрузки страницы.

### ФТ-2. Загрузка вкладок

Для обеих вкладок используется один endpoint:
- `GET /api/v1/approvals/my`

Правила вызова:
- для вкладки `На согласовании` фронт передаёт `stage_type=approval`;
- для вкладки `На утверждении` фронт передаёт `stage_type=ratification`.

### ФТ-3. Компонент списка Approval

Компонент `ApprovalTab` должен рендерить карточки `ApprovalSingleCard`.

#### Поля карточки

- тип элемента;
- название;
- краткое описание доменного элемента;
- ссылка на связанный доменный элемент;
- продукт;
- критичность;
- дата отправки на согласование;
- превью связанных скоркарт;
- чекбокс выбора, если действие доступно.

### ФТ-4. Компонент списка Ratification

Компонент `RatificationTab` должен рендерить:
- `ApprovalSingleCard`;
- `ApprovalPackageCard`.

#### Поля карточки пакета

- бриф пакета;
- количество элементов;
- список продуктов или агрегированное представление нескольких продуктов;
- критичность;
- дата отправки на утверждение;
- preview входящих элементов.

Примечание:
- для каждого элемента в `itemsPreview` фронт получает `targetApprovalPurpose` — текст, поясняющий, для чего именно запрошено согласование или утверждение по элементу;
- `target_url` должен быть относительной UI-ссылкой на детальную карточку связанного доменного элемента.
- Если `ApprovalInstance` связан с конкретной версией доменного элемента, `target_url` должен открывать именно эту версию.

### ФТ-5. Компонент деталки элемента

Компонент `ApprovalDetailDialog` должен включать:
- вкладку `Общая информация`;
- вкладку `История процесса`;
- вкладку `Связанные скоркарты`.

#### Общая информация

- один блок данных из брифа на согласование;
- название;
- описание;
- текст, поясняющий, для чего именно запрошено согласование или утверждение;
- ссылка на связанный доменный элемент с открытием в новом окне;
- версия;
- продукт;
- критичность;
- дата отправки на согласование;
- дополнительные атрибуты;
- дата создания;

Правило выбора брифа:
- если `ApprovalInstance` входит в активный пакет, фронт показывает бриф пакета;
- если активного пакета нет или пакет рассыпался, фронт показывает бриф `ApprovalInstance`.

#### История процесса

Для каждого этапа показываются:
- название этапа;
- признаки выполнения этапа;
- назначенные пользователи;
- пользователи, уже принявшие решение;
- пользователи, от которых решение ещё ожидается;
- решения;
- комментарии;
- даты и время.

Дополнительно:
- маршрут должен включать как approval stages, так и ratification stage, если он существует;
- для каждого решения показываются пользователь, тип решения, комментарий и `decided_at`;
- если по этапу ещё нет решения, UI должен явно показывать, что этап или конкретный участник ещё ожидается.

#### Связанные скоркарты

Для каждой связанной скоркарты показываются:
- `display_id`;
- название;
- номер версии;
- статус;
- критичность;
- признак ручного заполнения;
- ссылка на скоркарту, если она не ручная;
- дата создания;
- финансовые эффекты;
- остальные параметры из полного JSON текущей скоркарты, включая положения бинарных переключателей.

Примечание:
- если `isManual = false`, фронт должен ожидать `url` скоркарты;
- `scorecardJson` не должен дублировать транспортные метаполя `isManual`, `url`, `createdAt`, `updatedAt`.

### ФТ-6. Компонент деталки пакета

Компонент `PackageDetailDialog` должен включать:
- шапку пакета;
- бриф пакета;
- список входящих элементов;
- действия по пакету.

Для каждого входящего элемента показываются:
- идентификатор и тип доменного элемента;
- название;
- описание;
- текст, поясняющий, для чего именно запрошено согласование или утверждение;
- ссылка на связанный доменный элемент с открытием в новом окне;
- продукт;
- критичность;
- связанные скоркарты;
- маршрут и история процесса.

Блок брифа в деталке пакета показывается один раз в шапке пакета и не дублируется внутри входящих элементов.

### ФТ-7. Действия

#### Индивидуальные действия

Выполняются через:
- `POST /api/v1/approvals/{id}/action`

Поддерживаемые действия:
- `approve`
- `reject`
- `ratify`
- `recall`

#### Массовые действия

Выполняются через:
- `POST /api/v1/approvals/action`

Поддерживаемые действия:
- `approve`
- `reject`
- `ratify`

#### Пакетные действия

Выполняются через:
- `POST /api/v1/packages/{id}/action`

Поддерживаемые действия:
- `ratify`
- `reject`

### ФТ-8. Типы данных на фронте

```typescript
type ApprovalCriticality = 'high' | 'low' | null;

type ApprovalCard =
  | ApprovalSingleCard
  | ApprovalPackageCard;

interface ApprovalSingleCard {
  cardType: 'single';
  approvalInstanceId: string;
  approvalStatus: string;
  targetType: 'PILOT_VERSION' | 'DEPLOYMENT_VERSION';
  targetId: string;
  targetName: string;
  targetDescription: string | null;
  targetApprovalPurpose: string;
  targetUrl: string;
  product: ProductRef;
  criticality: ApprovalCriticality;
  submittedAt: string;
  scorecardsCount: number;
  scorecardsPreview: ApprovalScorecardPreview[];
}

interface ApprovalPackageCard {
  cardType: 'package';
  packageId: string;
  brief: ApprovalBrief;
  itemsCount: number;
  products: ProductRef[];
  criticality: ApprovalCriticality;
  submittedAt: string;
  itemsPreview: PackagePreviewItem[];
}

interface ProductRef {
  productId: string;
  productName: string;
}

interface PackagePreviewItem {
  approvalInstanceId: string;
  approvalStatus: string;
  targetType: 'PILOT_VERSION' | 'DEPLOYMENT_VERSION';
  targetName: string;
  targetDescription: string | null;
  targetApprovalPurpose: string;
  targetUrl: string;
  product: ProductRef;
  criticality: ApprovalCriticality;
}

interface ApprovalDetail {
  approvalInstanceId: string;
  approvalStatus: string;
  targetType: 'PILOT_VERSION' | 'DEPLOYMENT_VERSION';
  targetId: string;
  briefSource: 'approval_instance' | 'package' | null;
  brief: ApprovalBrief | null;
  submittedAt: string;
  target: ApprovalTarget;
  scorecards: ApprovalScorecard[];
  history: ApprovalDetailHistory;
}

interface ApprovalBrief {
  subject: string;
  body: string;
}

interface ApprovalTarget {
  url: string;
  name: string;
  description: string | null;
  approvalPurpose: string;
  version: string | null;
  product: ProductRef;
  criticality: ApprovalCriticality;
  createdAt: string | null;
  attributes: Array<{
    key: string;
    label: string;
    value: string;
  }>;
}

interface ApprovalScorecardPreview {
  scorecardId: string;
  displayId: string;
  name: string;
  criticality: ApprovalCriticality;
}

interface ApprovalScorecard {
  scorecardId: string;
  displayId: string;
  name: string;
  description: string | null;
  version: number;
  status: string;
  criticality: ApprovalCriticality;
  isManual: boolean;
  url: string | null;
  createdAt: string;
  updatedAt: string | null;
  scorecardJson: Record<string, unknown>;
}

interface ApprovalDetailHistory {
  approvalStages: ApprovalHistoryStage[];
  ratificationStage: ApprovalHistoryStage | null;
  statusTransitions: Array<{
    fromStatus: string | null;
    toStatus: string;
    timestamp: string;
    userId: string | null;
  }>;
}

interface ApprovalHistoryStage {
  stageOrder: number | null;
  stageName: string;
  startedAt: string | null;
  completedAt: string | null;
  assignees: Array<{
    userId: string;
    userName: string;
  }>;
  pendingAssignees: Array<{
    userId: string;
    userName: string;
  }>;
  decisions: Array<{
    userId: string;
    userName: string;
    decision: 'approve' | 'reject' | 'ratify' | 'recall';
    comment: string | null;
    decidedAt: string;
  }>;
}

interface PackageDetail {
  packageId: string;
  brief: ApprovalBrief;
  products: ProductRef[];
  criticality: ApprovalCriticality;
  submittedAt: string;
  items: PackageApprovalItemDetail[];
}

interface PackageApprovalItemDetail {
  approvalInstanceId: string;
  approvalStatus: string;
  targetType: 'PILOT_VERSION' | 'DEPLOYMENT_VERSION';
  targetId: string;
  submittedAt: string;
  target: ApprovalTarget;
  scorecards: ApprovalScorecard[];
  history: ApprovalDetailHistory;
}
```

### ФТ-9. Цветовая схема и иконки

#### Критичность

- `high` — акцентный предупреждающий цвет.
- `low` — нейтральный цвет.
- `null` — критичность не показывается как цветной бэйдж.

#### Статусы этапов

- UI не использует отдельный enum статусов этапов.
- Визуальное состояние этапа определяется по `startedAt`, `completedAt`, `pendingAssignees` и `decisions`.

#### Типы карточек

- `PILOT_VERSION` — иконка пилота.
- `DEPLOYMENT_VERSION` — иконка внедрения.
- `package` — иконка пакета.

Примечание:
- фронт не должен иметь отдельной цветовой схемы для несуществующих значений `critical`, `medium` и для отдельного legacy-enum статусов этапов.

## Интеграция с Backend API

### Используемые endpoint'ы

- `GET /api/v1/approvals/my`
- `GET /api/v1/approvals/{id}`
- `GET /api/v1/packages/{id}`
- `POST /api/v1/approvals/{id}/action`
- `POST /api/v1/approvals/action`
- `POST /api/v1/packages/{id}/action`

### OpenAPI-фрагмент для фронта

```yaml
openapi: 3.0.3
info:
  title: Approvals Page Frontend Integration
  version: 1.0.0
paths:
  /api/v1/approvals/my:
    get:
      summary: Получить карточки вкладки Согласования
    parameters:
      - in: query
        name: stage_type
        required: true
        schema:
          type: string
          enum: [approval, ratification]
  /api/v1/approvals/{id}:
    get:
      summary: Получить деталку элемента
  /api/v1/packages/{id}:
    get:
      summary: Получить деталку пакета
  /api/v1/approvals/{id}/action:
    post:
      summary: Выполнить индивидуальное действие
  /api/v1/approvals/action:
    post:
      summary: Выполнить массовое действие
  /api/v1/packages/{id}/action:
    post:
      summary: Выполнить пакетное действие
```

## Примеры запросов и ответов

### Пример 1. Загрузка вкладки Approval

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

### Пример 2. Загрузка вкладки Ratification

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
        }
      ]
    }
  ],
  "total": 1
}
```

### Пример 3. Индивидуальное действие

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

### Пример 4. Массовое действие

Запрос:

```http
POST /api/v1/approvals/action
Content-Type: application/json
```

```json
{
  "approval_instance_ids": ["appr-inst-001", "appr-inst-002"],
  "action": "reject",
  "comment": "Требуется доработка."
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

## Валидация

### Проверки на фронте

- Для `GET /api/v1/approvals/my` обязателен `stage_type`.
- Для индивидуальных и массовых действий фронт должен предлагать только те action, которые разрешены для текущей вкладки.
- Комментарий на фронте не должен быть обязательным ни для `reject`, ни для `approve`, ни для `ratify`, ни для `recall`.
- Фронт не должен ожидать поле `current_stage`; текущее состояние элемента он определяет по `approval_status`.
- Для перехода на связанный доменный элемент фронт использует `target_url` и открывает его в новом окне.
- Если `isManual = false`, фронт должен ожидать `url` скоркарты и использовать его для перехода к связанной скоркарте.
- Для деталки `ApprovalInstance` фронт использует только один блок брифа:
  - пакетный, если есть активный пакет;
  - иначе бриф самого `ApprovalInstance`.
- Фронт не должен принимать и типизировать legacy-критичности и отдельные legacy-статусы этапов.

## Обработка ошибок

### Ошибки загрузки

- Ошибка загрузки одной вкладки не должна ломать вторую вкладку.
- Ошибка загрузки деталки пакета не должна ломать список карточек.

### Ошибки действий

- При `409` UI должен перезагрузить карточку или вкладку и показать, что состояние элемента изменилось.
- При частичном успехе массового действия UI должен показать результат по каждому элементу.

### Ошибки консистентности

- Если backend вернул неизвестное значение `criticality` или статуса этапа, UI должен показать безопасное fallback-отображение и зафиксировать клиентскую ошибку.
