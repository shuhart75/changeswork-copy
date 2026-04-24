# Внедрения (Backend) — БД и API

Статус: **выделено из общего документа для отдельной задачи**  
Область: MVP  
Дата выделения: 2026-04-07  
Источник: [REQ_deployments_backend.md](/home/reutov/Documents/AI/changesWork/final-spec/REQ_deployments_backend.md)

## Доменные определения и бизнес-правила для БД/API

### Определения

- `Внедрение (Deployment)`:
  агрегат верхнего уровня, который объединяет все версии одного внедрения, хранит ссылки на актуальную и продуктивную версии, а также фиксирует неизменяемый тип внедрения.
- `Версия внедрения (DeploymentVersion)`:
  неизменяемый снимок редактируемых полей внедрения на конкретный момент времени. Именно версия внедрения участвует в процессе согласования и утверждения.
- `Черновик-оболочка внедрения`:
  минимально созданные записи `Deployment` и `DeploymentVersion v1` в статусе `draft`, которые нужны, чтобы форма могла дальше создать скоркарты и артефакты в контексте уже существующего внедрения.
- `Текущая проекция внедрения`:
  API-представление внедрения для frontend, собранное из агрегата `Deployment`, актуальной `DeploymentVersion` и связанных сущностей.
- `Тип внедрения (deployment_type)`:
  неизменяемая агрегатная характеристика внедрения. В MVP допустимы значения `general` (`Общий`) и `simulation_based` (`Внедрение по результатам симуляции`).
- `Lineage симуляции`:
  ограниченная для MVP ссылка внедрения типа `simulation_based` на одну `Simulation`, результаты которой внедряются.
- `Обязательная lineage-скоркарта`:
  скоркарта, созданная по результатам `lineage_simulation_id` и зафиксированная как обязательная связь для внедрения типа `simulation_based`. Такая скоркарта не может быть удалена из состава внедрения.

### Бизнес-правила

#### БП-1. Модель внедрения

- `Deployment` является самостоятельной доменной сущностью.
- Backend для внедрений должен использовать полноценную версионную модель:
  - агрегат `Deployment`;
  - версионную сущность `DeploymentVersion`.
- `Deployment` хранит только агрегатные поля и ссылки на актуальные версии.
- Все изменяемые бизнес-поля и поля процесса должны жить на уровне `DeploymentVersion`.
- Поля версии не должны дублироваться в таблице `deployment`.
- API внедрений может отдавать плоскую текущую проекцию внедрения для удобства frontend, но источником данных для этой проекции остаётся актуальная `DeploymentVersion`.
- Для сценария создания нового внедрения backend должен поддерживать создание черновика-оболочки:
  - сначала создаётся `Deployment` + `DeploymentVersion v1` в `draft`;
  - после этого новая запись `deployment.id` используется как родительский контекст для API скоркарт и артефактов;
  - финальная сборка состава скоркарт и артефактов выполняется через последующий `PUT /api/v1/deployments/{id}`.
- В таблице `Deployment` должны храниться агрегатные неизменяемые поля:
  - `deployment_type`;
  - `lineage_simulation_id`;
  - `required_scorecard_id`.
- `deployment_type` после первого успешного сохранения внедрения не может быть изменён ни в одном статусе, включая `draft`.
- Если пользователь ошибся с типом, он должен удалить `draft` и создать новое внедрение заново.

#### БП-1.1. Редактируемые поля версии внедрения

- У версии внедрения обязательно есть поле `name`.
- Вместо единого поля `description` версия внедрения должна хранить три независимых опциональных поля:
  - `goal` (`Цель`);
  - `change_description` (`Описание изменений`);
  - `application_perimeter` (`Периметр применения`).
- Все три поля редактируются независимо друг от друга и могут одновременно быть `null`.

#### БП-1.2. Типизация внедрения

- В MVP поддерживаются только типы внедрения:
  - `general`;
  - `simulation_based`.
- Тип внедрения выбирается пользователем в потоке создания скоркарты из контекста внедрения и фиксируется при первом успешном сохранении внедрения.
- Backend обязан отклонять попытку изменить уже зафиксированный `deployment_type` даже для внедрения в `draft`.
- Для `general`:
  - `lineage_simulation_id` должен отсутствовать;
  - `required_scorecard_id` должен отсутствовать.
- Для `simulation_based`:
  - `lineage_simulation_id` обязателен;
  - среди связанных `scorecard_version_ids` должна быть хотя бы одна версия скоркарты, у которой в `scorecard_source` есть ссылка на ту же `Simulation`;
  - при первом успешном сохранении backend должен зафиксировать соответствующую скоркарту как `required_scorecard_id`;
  - при последующих обновлениях внедрения backend обязан проверять, что среди связанных версий по-прежнему присутствует версия этой же скоркарты;
  - попытка удалить обязательную lineage-скоркарту из состава внедрения должна завершаться ошибкой валидации.

#### БП-2. Контекст продукта

- Внедрение принадлежит одному продукту.
- Все связанные версии скоркарт должны принадлежать тому же продукту.
- Видимость внедрений для `prm` и `methodologist` не ограничивается их продуктом: они могут просматривать внедрения всех продуктов.
- Ограничение по продукту применяется только к CRUD-операциям и lifecycle-действиям:
  - `prm` может изменять только внедрения своего продукта;
  - `methodologist` не выполняет CRUD и lifecycle-действия;
  - `admin` может изменять внедрения всех продуктов.

#### БП-3. Критичность

- Критичность не вводится вручную.
- Backend рассчитывает критичность по связанным скоркартам.
- Правило расчёта:
  - `high`, если хотя бы одна связанная скоркарта имеет `criticality = high`;
  - иначе `low`.

#### БП-4. Блок `Связанные сущности`

- Блок `Связанные сущности` возвращается как read-only.
- Блок вычисляется backend только через связи текущего внедрения со скоркартами.
- Допустимые типы связанных сущностей в MVP:
  - `pilot`;
  - `simulation`.
- В MVP не поддерживаются отдельные ручные связи `Deployment -> Pilot/Simulation` вне скоркарт.
- Backend должен возвращать все доменные элементы, связанные с текущим внедрением через его скоркарты.
- Если внедрение использует существующую скоркарту, блок `Связанные сущности` должен включать все доменные элементы, уже связанные с этой скоркартой.
- Если у скоркарты нет связанных доменных элементов, она не даёт записей в блок `Связанные сущности`.
- Для `simulation_based` backend обязан включать `lineage_simulation` в список `related_simulations`, так как обязательная lineage-скоркарта связана с этой симуляцией.
- Для такой записи в `related_simulations` backend обязан возвращать признак `is_lineage = true`.

#### БП-4.1. Ограниченный Lineage для внедрений

- В текущем MVP `Lineage` вводится только для внедрений типа `simulation_based`.
- `Lineage` для внедрения не заменяет блок `Связанные сущности` и не вычисляется рекурсивно.
- Backend должен возвращать отдельное поле `lineage_simulation`, если у внедрения задан `lineage_simulation_id`.
- Для внедрений типа `general` поле `lineage_simulation` должно быть `null`.

## Функциональные требования

### ФТ-1. Endpoint'ы

В MVP используются endpoint'ы:
- `GET /api/v1/deployments`
- `GET /api/v1/deployments/{id}`
- `POST /api/v1/deployments`
- `PUT /api/v1/deployments/{id}`
- `POST /api/v1/deployments/{id}/action`
- `GET /api/v1/scorecards`
- `POST /api/v1/scorecards`
- `PUT /api/v1/scorecards/{id}`
- `GET /api/v1/scorecard-template-versions`
- `GET /api/v1/scorecard-template-versions/{id}/default-config`
- `GET /api/DEPLOYMENT/{entityId}/artifacts`
- `POST /api/DEPLOYMENT/{entityId}/artifacts`
- `PATCH /api/artifacts/{artifactId}`
- `DELETE /api/artifacts/{artifactId}`

### ФТ-2. Список внедрений

`GET /api/v1/deployments` должен поддерживать:
- фильтр по продукту;
- опциональное включение архивных записей.

Для каждой записи списка backend должен возвращать:
- `id`;
- `display_id`;
- `name`;
- `deployment_type`;
- `status`;
- `approval_instance_status`, если применимо;
- `criticality`;
- `created_by`;
- `created_at`;
- `deployed_at`.

Опционально для строки списка backend может возвращать:
- `available_actions`.

### ФТ-3. Детальная карточка

`GET /api/v1/deployments/{id}` должен возвращать:
- основные поля внедрения;
- `deployment_type`;
- `lineage_simulation`, если применимо;
- связанные скоркарты;
- связанные `Simulation`;
- связанные `Pilot`;
- артефакты;
- `approval_instance`:
  - `id`;
  - `status`;
- `available_actions`;
- вычисленный UI-статус или достаточные для него поля.

Правило отображаемого статуса:
- если `deployment.status = draft`, UI показывает статус `Черновик`;
- если `deployment.status = deployed`, UI показывает статус `Внедрено`;
- если `deployment.status = archived`, UI показывает статус `Архив`;
- в остальных промежуточных случаях UI должен использовать `approval_instance.status`, но отображать его русским человекочитаемым лейблом, согласованным с процессом согласования.

Правило возврата type/lineage:
- backend всегда возвращает `deployment_type`;
- если `deployment_type = simulation_based`, backend возвращает:
  - `lineage_simulation` как отдельный объект ссылки с полями:
    - `id`;
    - `display_id`;
    - `name`;
    - `status`;
    - `url`;
  - для обязательной lineage-скоркарты признак `is_required = true` в составе элемента `scorecards`;
- если `deployment_type = general`, backend возвращает `lineage_simulation = null`, а у всех скоркарт `is_required = false`.

Правило формирования блока `Связанные сущности`:
- backend возвращает объединение всех `Pilot` и `Simulation`, связанных с текущим внедрением через его скоркарты;
- каждый элемент в `related_simulations` и `related_pilots` должен содержать:
  - `entity_type`;
  - `id`;
  - `display_id`;
  - `name`;
  - `status`;
  - `url`;
- дубликаты по типу сущности и идентификатору должны устраняться;
- текущее внедрение должно исключаться из результата, даже если оно попадает в выборку через usage-связи тех же скоркарт;
- прямые ручные связи внедрения с `Pilot` или `Simulation` в MVP не поддерживаются.
- если `deployment_type = simulation_based`, симуляция из `lineage_simulation` должна присутствовать в `related_simulations`;
- для этой записи backend должен возвращать `is_lineage = true`;
- для остальных записей `related_simulations` backend должен возвращать `is_lineage = false` или не возвращать признак вообще.

Правило возврата доступных действий:
- backend должен возвращать список `available_actions`, рассчитанный по текущему состоянию внедрения;
- если связанный `approvalInstance` перешёл в конечный статус `ratified`, backend должен включать действие `deploy` в `available_actions`;
- если `deploy` присутствует в `available_actions`, это означает, что backend разрешает перевод внедрения в `deployed`;
- если `deploy` отсутствует в `available_actions`, frontend не должен предлагать пользователю кнопку `Внедрить`.

### ФТ-4. Создание внедрения

`POST /api/v1/deployments` принимает:
- `product_id` или иной согласованный продуктовый контекст;
- опционально начальные поля версии:
  - `name`;
  - `goal`;
  - `change_description`;
  - `application_perimeter`;
- опционально `scorecard_version_ids` или согласованный список связанных версий скоркарт;

Правила:
- `POST /api/v1/deployments` должен поддерживать сценарий первоначального создания черновика-оболочки;
- в сценарии создания черновика-оболочки список `scorecard_version_ids` может быть пустым;
- после `POST /api/v1/deployments` frontend получает `deployment.id`, который затем используется:
  - в `POST /api/v1/scorecards` как `parent_context.entity_id` при `parent_context.entity_type = deployment`;
  - в `POST /api/DEPLOYMENT/{entityId}/artifacts` как родительский `entityId`;
- на этапе финального сохранения через `PUT /api/v1/deployments/{id}` должна быть указана минимум одна версия скоркарты;
- все связанные версии скоркарт должны принадлежать тому же продукту;
- при первом успешном `PUT /api/v1/deployments/{id}` должны быть переданы:
  - `deployment_type`;
  - для `simulation_based` также `lineage_simulation_id`;
- `criticality` в запросе не принимается как пользовательское поле;
- статус нового внедрения всегда `draft`.
- после `POST /api/v1/deployments` backend должен считать новое внедрение техническим `draft-shell` до первого успешного `PUT /api/v1/deployments/{id}`;
- если в течение 2 минут после `POST /api/v1/deployments` не выполнен успешный `PUT /api/v1/deployments/{id}` с минимум одной связанной скоркартой, backend должен автоматически удалить такой `draft-shell`;
- при автоудалении `draft-shell` backend должен удалить само внедрение, его версию и артефакты, созданные для этого `deployment.id`;
- выбранные пользователем уже существующие скоркарты при автоудалении `draft-shell` не удаляются.

#### Интеграционный сценарий формы создания

Для новой формы внедрения backend должен поддерживать следующую последовательность вызовов:
1. `POST /api/v1/deployments`
2. При выборе существующих скоркарт:
   - `GET /api/v1/scorecards?product_id=...`
3. При ручном создании новой скоркарты:
   - `POST /api/v1/scorecards`
4. При создании скоркарты по симуляции:
   - `POST /api/v1/scorecards` с `source_refs`
5. При создании артефактов:
   - `POST /api/DEPLOYMENT/{entityId}/artifacts`
6. При необходимости чтения уже созданных артефактов:
   - `GET /api/DEPLOYMENT/{entityId}/artifacts`
7. Финальная сборка внедрения:
   - `PUT /api/v1/deployments/{id}`

Правила последовательности вызовов:
- API скоркарт и API артефактов являются источником правды для своих сущностей;
- `POST /api/v1/deployments` не должен пытаться дублировать nested-контракт скоркарт и артефактов;
- итоговый `PUT /api/v1/deployments/{id}` принимает уже готовые идентификаторы связанных `scorecard_version_ids`;
- если внедрение сохраняется как `simulation_based`, хотя бы одна из переданных скоркарт должна иметь `source_refs` на `lineage_simulation_id`;
- backend должен зафиксировать такую скоркарту как `required_scorecard_id` и не позволять исключить её из следующих версий внедрения.
- успешным завершением сценария создания считается только успешный `PUT /api/v1/deployments/{id}`;
- если второй этап не завершён в течение 2 минут, backend удаляет незавершённый `draft-shell`.

### ФТ-5. Обновление внедрения

`PUT /api/v1/deployments/{id}` принимает тот же набор редактируемых полей, что и create.

Правила:
- обновление разрешено для `draft`, `approved`, `ratified`, `rejected`, `cancelled`;
- при обновлении из `approved`, `ratified`, `rejected`, `cancelled` backend переводит внедрение в `draft`;
- `PUT /api/v1/deployments/{id}` должен принимать финальный список `scorecard_version_ids` как целевое состояние связей версии внедрения;
- `PUT /api/v1/deployments/{id}` не должен принимать изменение ранее зафиксированного `deployment_type`;
- если `deployment_type = simulation_based`, `PUT /api/v1/deployments/{id}` не должен принимать изменение `lineage_simulation_id`;
- если `deployment_type = simulation_based`, список `scorecard_version_ids` обязан содержать актуальную версию скоркарты, у которой `scorecard_id = required_scorecard_id`;
- backend пересчитывает:
  - `criticality`;
  - `related_simulations`;
  - `related_pilots`.
- при пересчёте `related_simulations` backend также должен корректно пересчитывать признак `is_lineage`.

#### Интеграционный сценарий формы редактирования

Для формы редактирования backend должен поддерживать следующую последовательность вызовов:
1. `GET /api/v1/deployments/{id}`
2. Для просмотра и синхронизации артефактов:
   - `GET /api/DEPLOYMENT/{entityId}/artifacts`
3. При создании новой скоркарты из формы внедрения:
   - `POST /api/v1/scorecards`
4. При редактировании существующей скоркарты:
   - `PUT /api/v1/scorecards/{id}`
5. При выборе существующей скоркарты:
   - `GET /api/v1/scorecards?product_id=...`
6. При создании артефакта:
   - `POST /api/DEPLOYMENT/{entityId}/artifacts`
7. При изменении артефакта:
   - `PATCH /api/artifacts/{artifactId}`
8. При удалении артефакта:
   - `DELETE /api/artifacts/{artifactId}`
9. При финальном сохранении формы:
   - `PUT /api/v1/deployments/{id}`

Правила последовательности вызовов:
- если скоркарта была перевыпущена через `PUT /api/v1/scorecards/{id}`, frontend обязан использовать идентификатор новой текущей версии скоркарты при следующем `PUT /api/v1/deployments/{id}`;
- если набор артефактов изменился, это не должно менять `deployment_version`, пока не выполнен итоговый `PUT /api/v1/deployments/{id}` для синхронизации карточки;
- backend деталки должен быть устойчив к промежуточному состоянию, когда черновик-оболочка уже создана, но состав скоркарт и артефактов ещё не завершён.

### ФТ-6. Lifecycle action endpoint

`POST /api/v1/deployments/{id}/action` поддерживает действия:
- `submit_for_approval`;
 - `start_ratification`;
 - `recall`;
- `deploy`;
- `archive`.

Формат запроса:

```json
{
  "action": "submit_for_approval",
  "payload": {}
}
```

Правила:
- для `submit_for_approval` backend создаёт/привязывает `ApprovalInstance`;
- для `start_ratification` backend переводит процесс из `approved` в этап утверждения;
- для `recall` backend останавливает активный процесс согласования и возвращает внедрение в `draft`;
- для `deploy` backend проверяет успешное завершение `ApprovalInstance`;
- для `archive` backend проверяет, что текущий статус допускает архивацию.
- после любого lifecycle-действия backend должен возвращать обновлённую карточку внедрения вместе с пересчитанным `available_actions`.

## Описание модели данных

```typescript
type DeploymentAggregateStatus = 'active' | 'archived';

type DeploymentVersionStatus = 'draft' | 'deployed' | 'archived' | 'approval_flow';

type DeploymentType = 'general' | 'simulation_based';

interface Deployment {
  id: string;
  displayId: string;
  productId: string;
  deploymentType: DeploymentType | null;
  lineageSimulationId: string | null;
  requiredScorecardId: string | null;
  latestVersionId: string;
  productionVersionId: string | null;
  aggregateStatus: DeploymentAggregateStatus;
  createdBy: string;
  createdAt: string;
  updatedAt: string;
}

interface DeploymentVersion {
  id: string;
  deploymentId: string;
  version: number;
  name: string;
  goal: string | null;
  changeDescription: string | null;
  applicationPerimeter: string | null;
  status: DeploymentVersionStatus;
  criticality: 'high' | 'low';
  approvalInstanceId: string | null;
  deployedAt: string | null;
  createdBy: string;
  createdAt: string;
}
```

Примечание:
- `approval_flow` является внутренним техническим состоянием backend;
- для UI в этом состоянии источником правды является `approvalInstance.status`.

### Таблица `deployment`

Назначение:
- Хранит агрегат внедрения как корневую доменную сущность.
- Нужна для хранения агрегатных ссылок на актуальную и продуктивную версии.

| Поле | Тип | Обязательность | Описание |
|---|---|---:|---|
| `id` | UUID | да | PK внедрения |
| `product_id` | UUID | да | FK на `product.id`; определяет продукт внедрения |
| `deployment_type` | VARCHAR(32) | нет | Неизменяемый тип внедрения: `general` или `simulation_based`; заполняется при первом успешном сохранении |
| `lineage_simulation_id` | UUID | нет | FK на `simulation.id`; обязателен только для `simulation_based` |
| `required_scorecard_id` | UUID | нет | FK на `scorecard.id`; обязательная lineage-скоркарта для `simulation_based` |
| `latest_version_id` | UUID | да | FK на `deployment_version.id`; актуальная версия внедрения |
| `production_version_id` | UUID | нет | FK на `deployment_version.id`; версия внедрения, находящаяся в проде |
| `aggregate_status` | VARCHAR(32) | да | Агрегатный статус: `active` или `archived` |
| `created_at` | TIMESTAMP WITH TIME ZONE | да | Дата и время создания внедрения |
| `created_by` | UUID | да | Пользователь, создавший внедрение |
| `updated_at` | TIMESTAMP WITH TIME ZONE | да | Дата и время последнего изменения |
| `updated_by` | UUID | да | Пользователь, внёсший последнее изменение |

Примечания:
- `display_id` должен отдаваться в API как человекочитаемый идентификатор внедрения, но не обязан быть отдельной колонкой таблицы.
- В таблице `deployment` не должны храниться поля версии:
  - `name`;
  - `goal`;
  - `change_description`;
  - `application_perimeter`;
  - `status`;
  - `criticality`;
  - `approval_instance_id`;
  - `deployed_at`.
- Эти поля должны храниться только в `deployment_version`.

### Таблица `deployment_version`

Назначение:
- Хранит версионное содержимое внедрения.
- Нужна для фиксации бизнес-полей, process-полей и истории изменений без перезаписи предыдущих версий.

| Поле | Тип | Обязательность | Описание |
|---|---|---:|---|
| `id` | UUID | да | PK версии внедрения |
| `deployment_id` | UUID | да | FK на `deployment.id` |
| `version` | INTEGER | да | Порядковый номер версии, начиная с `1` |
| `name` | VARCHAR(255) | да | Название внедрения в данной версии |
| `goal` | TEXT | нет | Цель внедрения в данной версии |
| `change_description` | TEXT | нет | Описание изменений в данной версии |
| `application_perimeter` | TEXT | нет | Периметр применения в данной версии |
| `status` | VARCHAR(32) | да | Текущее состояние версии: `draft`, `approval_flow`, `deployed`, `archived` |
| `criticality` | VARCHAR(16) | да | Критичность версии: `low` или `high` |
| `approval_instance_id` | UUID | нет | Ссылка на `approval_instance.id`, если для версии запущен approval flow |
| `deployed_at` | TIMESTAMP WITH TIME ZONE | нет | Дата и время перевода версии в `deployed` |
| `created_at` | TIMESTAMP WITH TIME ZONE | да | Дата и время создания версии |
| `created_by` | UUID | да | Пользователь, создавший версию |

Примечания:
- Для одной записи `deployment` комбинация `(deployment_id, version)` должна быть уникальной.
- Таблица `deployment_version` является целевой сущностью для `ApprovalInstance`, что согласовано с [REQ_approval_core.md](/home/reutov/Documents/AI/changesWork/final-spec/REQ_approval_core.md).
- Для UI промежуточные статусы не должны браться из `deployment_version.status`, если для версии есть `approval_instance`; в этом случае источником правды является `approval_instance.status`.
- Валидация неизменяемости `deployment_type`, `lineage_simulation_id` и `required_scorecard_id` должна выполняться на уровне агрегата `deployment`.

### Связи версии внедрения со скоркартами

Назначение:
- Связи версии внедрения со скоркартами должны использовать уже существующую таблицу `scorecard_version_deployment_version`.

Примечания:
- Источником правды по этой таблице является [REQ_scorecards_backend.md](/home/reutov/Documents/AI/changesWork/final-spec/REQ_scorecards_backend.md).
- В частности, используется таблица `scorecard_version_deployment_version` с полями:
  - `scorecard_version_id`;
  - `deployment_version_id`;
  - `linked_at`;
  - `linked_by`.
- Отдельная таблица `deployment_scorecard` в контексте внедрений не создаётся.
- Для каждой `deployment_version` должна существовать минимум одна связанная запись в `scorecard_version_deployment_version`.

### Связи внедрения с артефактами

Назначение:
- Артефакты внедрения должны использовать единый системный механизм артефактов.

Примечания:
- Источником правды является [REQ_artifacts_core.md](/home/reutov/Documents/AI/changesWork/final-spec/REQ_artifacts_core.md).
- Используется общая таблица `artifacts`.
- Для внедрения должны использоваться значения:
  - `entity_type = DEPLOYMENT`;
  - `entity_id = deployment.id`.
- Артефакты прикрепляются к агрегату `deployment`, а не к отдельной записи `deployment_version`.
- Отдельная таблица `deployment_artifact` в контексте внедрений не создаётся.

### Связи версии внедрения с ApprovalInstance

Назначение:
- Внедрение использует общий approval-механизм без собственной локальной таблицы процесса.

Примечания:
- Источником правды является [REQ_approval_core.md](/home/reutov/Documents/AI/changesWork/final-spec/REQ_approval_core.md).
- Каноническая связь процесса с версией внедрения задаётся полями:
  - `approval_instance.target_type = DEPLOYMENT_VERSION`;
  - `approval_instance.target_id = deployment_version.id`.
- Поле `deployment_version.approval_instance_id` может храниться как сервисная ссылка для ускорения чтения, но не должно подменять каноническую связь через `approval_instance.target_id`.

## Спецификация API

### `GET /api/v1/deployments`

Пример ответа:

```json
{
  "items": [
    {
      "id": "dep-1",
      "display_id": "CHG-1",
      "name": "Внедрение новой скоркарты Premium",
      "deployment_type": "simulation_based",
      "status": "draft",
      "approval_instance_status": null,
      "available_actions": [
        "edit",
        "submit_for_approval",
        "archive"
      ],
      "criticality": "high",
      "created_by": "Иванов И.И.",
      "created_at": "2026-02-01T10:00:00Z",
      "deployed_at": null
    }
  ],
  "total": 1
}
```

### `GET /api/v1/deployments/{id}`

Пример ответа:

```json
{
  "id": "dep-1",
  "display_id": "CHG-1",
  "name": "Внедрение новой скоркарты Premium",
  "deployment_type": "simulation_based",
  "goal": "Перевести в production результат симуляции Premium Q1",
  "change_description": "Обновление cut-off и весов признаков для premium-сегмента.",
  "application_perimeter": "Новые заявки по кредитным картам Premium.",
  "product_id": "credit_cards",
  "product_name": "Кредитные карты",
  "status": "approval_flow",
  "approval_instance": {
    "id": "apr-100",
    "status": "ratified"
  },
  "available_actions": [
    "edit",
    "deploy",
    "archive"
  ],
  "criticality": "high",
  "created_by": "Иванов И.И.",
  "created_at": "2026-02-01T10:00:00Z",
  "deployed_at": null,
  "lineage_simulation": {
    "id": "sim-1",
    "display_id": "SIM-1",
    "name": "Симуляция изменения весов факторов",
    "status": "completed",
    "url": "/simulations/sim-1"
  },
  "scorecards": [
    {
      "id": "sc-1",
      "name": "Скоркарта Premium v2.3",
      "criticality": "high",
      "is_required": true
    }
  ],
  "related_simulations": [
    {
      "entity_type": "simulation",
      "id": "sim-1",
      "display_id": "SIM-1",
      "name": "Симуляция изменения весов факторов",
      "status": "completed",
      "url": "/simulations/sim-1",
      "is_lineage": true
    }
  ],
  "related_pilots": [
    {
      "entity_type": "pilot",
      "id": "plt-1",
      "display_id": "PLT-1",
      "name": "Пилот Premium Q1 2026",
      "status": "completed",
      "url": "/pilots/plt-1"
    }
  ],
  "artifacts": [
    {
      "id": "art-1",
      "title": "Бизнес-кейс внедрения",
      "type": "business_case",
      "url": "https://docs.bank.ru/bc-change-001"
    }
  ]
}
```


## Ошибки и валидация

### Валидация

- `name` обязателен;
- `goal`, `change_description`, `application_perimeter` опциональны и передаются независимо;
- `deployment_type` обязателен при первом успешном итоговом сохранении внедрения;
- для итогового сохранения внедрения должна быть указана минимум одна версия скоркарты;
- для первоначального `POST /api/v1/deployments` в сценарии draft-shell допустим пустой список `scorecard_version_ids`;
- `artifact.url` обязателен, если артефакт передаётся;
- `artifact.title` обязателен, если артефакт передаётся;
- нельзя привязать версии скоркарт другого продукта.
- если `deployment_type = general`, `lineage_simulation_id` передавать нельзя;
- если `deployment_type = simulation_based`, `lineage_simulation_id` обязателен;
- если `deployment_type = simulation_based`, среди `scorecard_version_ids` должна быть актуальная версия обязательной lineage-скоркарты, у которой `scorecard_id = required_scorecard_id` и источник из той же `Simulation`;
- нельзя изменить `deployment_type` и `lineage_simulation_id` после их фиксации;
- нельзя удалить обязательную lineage-скоркарту из состава внедрения.

### Ошибки

- `400 Bad Request`:
  - некорректное тело запроса;
  - отсутствуют обязательные поля;
- `403 Forbidden`:
  - недостаточно прав;
- `404 Not Found`:
  - внедрение не найдено;
- `409 Conflict`:
  - попытка редактировать внедрение в недопустимом статусе;
  - попытка архивировать внедрение в недопустимом статусе;
  - попытка `deploy` вне `ratified`;
  - попытка изменить `deployment_type` или `lineage_simulation_id`;
  - попытка удалить обязательную lineage-скоркарту.

## Интеграция и синхронизация

- Контракт `approval_instance.status` должен быть синхронизирован с `REQ_approval_core.md`.
- Фронт не должен зависеть от внутренних backend-статусов процесса, кроме `draft`, `deployed`, `archived`.
- Если backend хранит дополнительные внутренние состояния, в API внедрений он обязан возвращать `approval_instance.status` как источник правды для промежуточного этапа.
