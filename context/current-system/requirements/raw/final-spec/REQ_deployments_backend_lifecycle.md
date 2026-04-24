# Внедрения (Backend) — Жизненный цикл

Статус: **выделено из общего документа для отдельной задачи**  
Область: MVP  
Дата выделения: 2026-04-07  
Источник: [REQ_deployments_backend.md](/home/reutov/Documents/AI/changesWork/final-spec/REQ_deployments_backend.md)

## Бизнес-правила ЖЦ

#### БП-5. Жизненный цикл внедрения

- Жизненный цикл внедрения в MVP:
  - `draft`;
  - после отправки на согласование/утверждение UI и API используют статус прикреплённого `approvalInstance`;
  - `deployed`;
  - `archived`.
- `draft`:
  - допускает редактирование;
  - допускает архивирование;
  - допускает отправку на согласование/утверждение;
- после отправки на согласование:
  - backend создаёт или привязывает `ApprovalInstance`;
  - текущий процессный статус определяется только состоянием `ApprovalInstance`;
- если `approvalInstance.status = in_approval` или `in_ratification`, доступно только действие `recall`;
- для внедрения `recall` из `in_approval` и `in_ratification` возвращает состояние в `draft`;
- если `approvalInstance.status = approved`, доступны:
  - `start_ratification`;
  - `archive`;
  - `edit`;
- если пользователь редактирует внедрение из `approved`, backend должен сбросить approval-state и перевести внедрение в `draft`;
- если `approvalInstance.status = ratified`, доступны:
  - `deploy`;
  - `archive`;
  - `edit`;
- если пользователь редактирует внедрение из `ratified`, backend должен сбросить approval-state и перевести внедрение в `draft`;
- если `approvalInstance.status` относится к группам `rejected` или `cancelled`, доступны:
  - `archive`;
  - `edit`;
  - повторная отправка на согласование/утверждение;
- при редактировании после `rejected` или `cancelled` внедрение возвращается в `draft`;
- `deployed` является конечным статусом;
- `archived` является конечным статусом.

#### БП-6. Синхронизация со связанным ApprovalInstance

- После отправки внедрения backend обязан сохранять ссылку на связанный `ApprovalInstance`.
- Для незавершённого процесса backend обязан возвращать:
  - ссылку на `approvalInstance`;
  - текущий `approvalInstance.status`.
- Backend не должен придумывать отдельный промежуточный статус внедрения, дублирующий `approvalInstance.status`.
- Backend может хранить внутренние технические статусы процесса, но они не должны подменять `approvalInstance.status` во внешнем API для фронта.
- Успешное завершение процесса согласования/утверждения определяется статусом `ApprovalInstance`, согласованным с `Approval core`.

#### БП-7. Доступные действия

- В MVP поддерживаются действия:
  - `submit_for_approval`;
  - `start_ratification`;
  - `recall`;
  - `deploy`;
  - `archive`.
- `submit_for_approval` доступно только из `draft`.
- `start_ratification` доступно только из `approved`.
- `recall` доступно только из `in_approval` и `in_ratification`.
- `archive` доступно из `draft`, `approved`, `ratified`, `rejected`, `cancelled`.
- `deploy` доступно только из `ratified`.

#### БП-8. Ограничения редактирования

- Редактирование внедрения допустимо в статусах:
  - `draft`;
  - `approved`;
  - `ratified`;
  - `rejected`;
  - `cancelled`.
- При редактировании из состояний `approved`, `ratified`, `rejected`, `cancelled` approval-state должен быть сброшен, а внедрение переведено в `draft`.
- После отправки на согласование редактирование запрещено для `in_approval` и `in_ratification`.
- Для `deployed` и `archived` редактирование запрещено.

#### БП-9. Архивация

- Архивация является soft-delete сценарием.
- При архивации внедрение получает статус `archived`.
- Архивное внедрение по умолчанию не должно попадать в активный список, если не включён соответствующий фильтр.

#### БП-10. Права доступа

- Просмотр доступен ролям, имеющим доступ к доменной модели.
- `prm` и `methodologist` видят внедрения всех продуктов.
- Создание, обновление и lifecycle-действия доступны:
  - `prm` своего продукта;
  - `admin`.
- `methodologist` не создаёт, не редактирует и не переводит внедрение по жизненному циклу, но может просматривать внедрения всех продуктов.
- `approver` и `ratifier` работают с процессом через страницу согласований, а не через CRUD внедрения.

## Границы MVP (ЖЦ)

- Отправка на согласование/утверждение.
- Отправка на утверждение после `approved`.
- Отзыв из `in_approval` и `in_ratification`.
- Архивация внедрения из `draft`.
- Перевод в `deployed` после успешного approval flow.

## Пользовательские сценарии ЖЦ

### Сценарий 3. Отправка на согласование/утверждение

1. Пользователь вызывает `submit_for_approval` для внедрения в `draft`.
2. Backend создаёт или привязывает `ApprovalInstance`.
3. После этого текущее процессное состояние внедрения определяется по `approvalInstance.status`.
4. Backend возвращает обновлённую карточку внедрения с актуальным `approvalInstance.status`.

### Сценарий 4. Отзыв из процесса

1. Внедрение находится в `in_approval` или `in_ratification`.
2. Пользователь вызывает `recall`.
3. Backend останавливает текущий процесс согласования для внедрения.
4. Внедрение возвращается в `draft`.

### Сценарий 5. Запуск утверждения

1. Внедрение находится в `approved`.
2. Пользователь вызывает `start_ratification`.
3. Backend переводит связанный процесс в ratification-стадию.
4. Текущее состояние внедрения далее определяется по `approvalInstance.status`.

### Сценарий 6. Внедрение

1. Связанный `ApprovalInstance` завершён успешно.
2. Пользователь вызывает `deploy`.
3. Backend переводит внедрение в `deployed`.
4. Backend фиксирует `deployed_at`.

### Сценарий 7. Архивация

1. Пользователь вызывает `archive` для внедрения в допустимом статусе.
2. Backend переводит внедрение в `archived`.
3. Архивное внедрение не возвращается в активной выборке по умолчанию.

## Критерии приемки ЖЦ

### Критерий 2. Жизненный цикл

- [ ] Из `draft` доступны `submit_for_approval` и `archive`
- [ ] После `submit_for_approval` backend возвращает привязанный `approvalInstance`
- [ ] Во время процесса статус внедрения для UI определяется по `approvalInstance.status`
- [ ] Из `in_approval` и `in_ratification` доступен только `recall`
- [ ] `recall` из `in_approval` и `in_ratification` возвращает внедрение в `draft`
- [ ] Из `approved` доступны `start_ratification`, `archive` и `edit`
- [ ] Из `ratified` доступны `deploy`, `archive` и `edit`
- [ ] Из `rejected` и `cancelled` доступны `archive`, `edit` и повторная отправка
- [ ] `deployed` является конечным статусом
- [ ] `archived` является конечным статусом
- [ ] Внешний API не подменяет промежуточный процессный статус внедрения отдельным полем вместо `approvalInstance.status`

### Критерий 3. Ограничения

- [ ] `PUT /api/v1/deployments/{id}` запрещён в `in_approval` и `in_ratification`
- [ ] При `PUT /api/v1/deployments/{id}` из `approved`, `ratified`, `rejected`, `cancelled` внедрение переводится в `draft`
- [ ] `archive` запрещён в `in_approval`, `in_ratification`, `deployed`, `archived`
- [ ] `deploy` вне `ratified` запрещён
- [ ] Попытка изменить `deployment_type` после его фиксации завершается ошибкой
- [ ] Для `simulation_based` попытка удалить обязательную lineage-скоркарту завершается ошибкой

## API-контракт, влияющий на ЖЦ

Правило отображаемого статуса:
- если `deployment.status = draft`, UI показывает статус `Черновик`;
- если `deployment.status = deployed`, UI показывает статус `Внедрено`;
- если `deployment.status = archived`, UI показывает статус `Архив`;
- в остальных промежуточных случаях UI должен использовать `approval_instance.status`, но отображать его русским человекочитаемым лейблом, согласованным с процессом согласования.

Правило возврата доступных действий:
- backend должен возвращать список `available_actions`, рассчитанный по текущему состоянию внедрения;
- если связанный `approvalInstance` перешёл в конечный статус `ratified`, backend должен включать действие `deploy` в `available_actions`;
- если `deploy` присутствует в `available_actions`, это означает, что backend разрешает перевод внедрения в `deployed`;
- если `deploy` отсутствует в `available_actions`, frontend не должен предлагать пользователю кнопку `Внедрить`.

Правила обновления (из ФТ-5):
- обновление разрешено для `draft`, `approved`, `ratified`, `rejected`, `cancelled`;
- при обновлении из `approved`, `ratified`, `rejected`, `cancelled` backend переводит внедрение в `draft`;

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

## Ошибки и валидация (ЖЦ)

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
