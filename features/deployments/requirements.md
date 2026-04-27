# Требования по feature — Внедрения

Статус: **draft**
Feature: `features/deployments/feature.md`
Квартал: `2026-Q2`
Дата обновления: `2026-04-27`
Шаблон: `.workflow/templates/requirements/feature-requirements.template.md`

## Оглавление

Используются заголовки до уровня `####`.

## Общий контур feature

- Назначение feature: собрать в одном контрольном документе список, workspace, форму, деталку, lifecycle и API-контур внедрений.
- Что уже есть в baseline/current: детальные FE/BE packs по каждому deployment slice и прототипы.
- Какая дельта добавляется этой feature: единая точка контроля требований по порядку slice-ов.
- Какие slice входят в контрольный документ: `workspace`, `list`, `form-editing`, `detail`, `lifecycle`, `db-api`.

## Порядок slice для контроля

1. `01 workspace — Общий deployment workspace`
2. `02 list — Список внедрений`
3. `03 form-editing — Создание и редактирование внедрения`
4. `04 detail — Детальная страница внедрения`
5. `05 lifecycle — Жизненный цикл внедрения`
6. `06 db-api — DB/API контракт внедрения`

---

## STORY-DEPLOYMENTS-001 — Общий deployment workspace

Slice card: `slices/workspace/slice.md`
Детализация FE: `slices/workspace/requirements/frontend.md`
Детализация BE: `slices/workspace/requirements/backend.md`
Прототип: `slices/workspace/delivery-prototype/prototype.html`
Planning story: `planning/stories/STORY-DEPLOYMENTS-001.md`

**Бизнес-требования**

- Цель: задать общий контур работы пользователя с внедрениями как доменной сущностью.
- Бизнес-правила: workspace объединяет основные состояния и навигацию, но не подменяет собой отдельные form/detail/lifecycle slices.
- Ограничения: control document не дублирует полный детальный текст FE/BE packs.

**Пользовательские требования к АС КОДА**

- Пользователь должен понимать, где находится список, где форма, где деталка и какие действия доступны по внедрению.

**Критерии приемки**

1. Общий контур пользовательской работы с внедрениями зафиксирован.
2. Переходы между list/form/detail не противоречат друг другу.
3. Workspace не расходится с lifecycle и approval constraints.

**USE CASES**

- **осн. сценарий 1** пользователь заходит в контур внедрений и выбирает нужный сценарий.
- **альт. сценарий 1.1** часть действий скрыта из-за статуса или роли.
- **альт. сценарий 1.2** пользователь переходит между list/detail/form без потери контекста.
- **осн. сценарий 2** workspace остаётся согласованным со связанными scorecards и trace.

### Функциональные требования

#### Реализация для FRONTEND

**Описание UI**

| Экран | Результат |
| --- | --- |
| Deployment workspace | Определяет общую навигацию и состав ключевых экранов |

Требования на фронт:

- поддержать общую композицию deployment-контуров и навигации между ними.

Связанный детальный FE pack: `slices/workspace/requirements/frontend.md`

#### Реализация BACKEND

Требования на бэк:

- обеспечить общий payload и статусы, на которых строятся workspace и переходы.

Связанный детальный BE pack: `slices/workspace/requirements/backend.md`

| | |
| --- | --- |
| **Сервис** | `deployments workspace` |
| ИФТ URL | `уточняется` |
| База данных | `см. detail packs` |
| Методы | `см. slices/workspace/requirements/backend.md` |

**Изменения в ролевой модели**

- На уровне control document новых ролей не зафиксировано.

**Отправка в Аудит**

- Аудит определяется детальными сценариями изменения и lifecycle.

**BUGS (Если есть)**

- Пока не зафиксированы.

### Доп. пояснения

- Workspace идёт первым, потому что задаёт общий путь чтения остальных slice-ов.

---

## STORY-DEPLOYMENTS-002 — Список внедрений

Slice card: `slices/list/slice.md`
Детализация FE: `slices/list/requirements/frontend.md`
Детализация BE: `slices/list/requirements/backend.md`
Прототип: `slices/list/delivery-prototype/prototype.html`
Planning story: `planning/stories/STORY-DEPLOYMENTS-002.md`

**Бизнес-требования**

- Цель: предоставить пользователю список внедрений с навигацией к нужной записи.
- Бизнес-правила: список поддерживает фильтры, статусы и продуктовый контекст.
- Ограничения: дополнительные list-возможности за пределами детальных packs не добавляются.

**Пользовательские требования к АС КОДА**

- Пользователь может найти нужное внедрение и перейти к нему.

**Критерии приемки**

1. Список отображает релевантные поля и статусы.
2. Фильтры и поиск работают по согласованным правилам.
3. Переход к detail screen работает корректно.

**USE CASES**

- **осн. сценарий 1** пользователь ищет внедрение в списке.
- **альт. сценарий 1.1** пользователь фильтрует по продукту или статусу.
- **альт. сценарий 1.2** список пуст по выбранным условиям.
- **осн. сценарий 2** пользователь открывает деталку найденного внедрения.

### Функциональные требования

#### Реализация для FRONTEND

**Описание UI**

| Экран | Результат |
| --- | --- |
| Список внедрений | Показывает grid, фильтры и переход к detail |

Требования на фронт:

- реализовать grid/list view с фильтрами и статусами.

Связанный детальный FE pack: `slices/list/requirements/frontend.md`

#### Реализация BACKEND

Требования на бэк:

- отдать list data, фильтрацию, сортировку и поиск для deployment scope.

Связанный детальный BE pack: `slices/list/requirements/backend.md`

| | |
| --- | --- |
| **Сервис** | `deployments list` |
| ИФТ URL | `уточняется` |
| База данных | `см. detail pack` |
| Методы | `см. slices/list/requirements/backend.md` |

**Изменения в ролевой модели**

- Изменения ролевой модели на уровне control document не зафиксированы.

**Отправка в Аудит**

- На уровне списка специальных новых audit требований не добавляется.

**BUGS (Если есть)**

- Пока не зафиксированы.

### Доп. пояснения

- После списка логично читать форму и деталку.

---

## STORY-DEPLOYMENTS-003 — Создание и редактирование внедрения

Slice card: `slices/form-editing/slice.md`
Детализация FE: `slices/form-editing/requirements/frontend.md`
Детализация BE: `slices/form-editing/requirements/backend.md`
Прототип: `slices/form-editing/delivery-prototype/prototype.html`
Planning story: `planning/stories/STORY-DEPLOYMENTS-003.md`

**Бизнес-требования**

- Цель: зафиксировать create/edit flow внедрения.
- Бизнес-правила: доступность полей зависит от статуса и типа внедрения; lineage и scorecards должны подчиняться доменным ограничениям.
- Ограничения: artefacts и approval flows контролируются соседними slices.

**Пользовательские требования к АС КОДА**

- Пользователь может создать или отредактировать внедрение в разрешённых состояниях.

**Критерии приемки**

1. Форма учитывает обязательные поля и доменные ограничения.
2. Изменение недопустимых полей по статусу блокируется.
3. Scorecards, lineage и связанные данные синхронизированы с правилами backend.

**USE CASES**

- **осн. сценарий 1** пользователь создаёт внедрение.
- **альт. сценарий 1.1** пользователь редактирует draft.
- **альт. сценарий 1.2** система блокирует недопустимое изменение lifecycle-зависимых полей.
- **осн. сценарий 2** после сохранения пользователь продолжает работу с detail screen.

### Функциональные требования

#### Реализация для FRONTEND

**Описание UI**

| Экран | Результат |
| --- | --- |
| Форма внедрения | Показывает поля, валидацию, scorecards и lineage-контекст |

Требования на фронт:

- собрать форму create/edit с валидацией и статусными ограничениями.

Связанный детальный FE pack: `slices/form-editing/requirements/frontend.md`

#### Реализация BACKEND

Требования на бэк:

- принять create/update payload и enforce доменные ограничения.

Связанный детальный BE pack: `slices/form-editing/requirements/backend.md`

| | |
| --- | --- |
| **Сервис** | `deployments form editing` |
| ИФТ URL | `уточняется` |
| База данных | `см. detail packs` |
| Методы | `см. slices/form-editing/requirements/backend.md` |

**Изменения в ролевой модели**

- Изменений ролевой модели на уровне control document не зафиксировано.

**Отправка в Аудит**

- В аудит попадают create/edit действия, если это закреплено в detail packs.

**BUGS (Если есть)**

- Пока не зафиксированы.

### Доп. пояснения

- Этот slice контролируется до detail и lifecycle, потому что он задаёт изменение данных.

---

## STORY-DEPLOYMENTS-004 — Детальная страница внедрения

Slice card: `slices/detail/slice.md`
Детализация FE: `slices/detail/requirements/frontend.md`
Детализация BE: `slices/detail/requirements/backend.md`
Прототип: `slices/detail/delivery-prototype/prototype.html`
Planning story: `planning/stories/STORY-DEPLOYMENTS-004.md`

**Бизнес-требования**

- Цель: показать текущее состояние внедрения и связанных данных.
- Бизнес-правила: detail screen собирает основные данные, scorecards, related entities и artifacts в согласованном read/edit контексте.
- Ограничения: детальная страница не подменяет форму и lifecycle API.

**Пользовательские требования к АС КОДА**

- Пользователь открывает detail screen и видит полную картину по внедрению.

**Критерии приемки**

1. Детальная страница показывает все baseline-блоки внедрения.
2. Переходы к связанным сущностям и связанным scorecards работают корректно.
3. Read/edit режимы не расходятся со status rules.

**USE CASES**

- **осн. сценарий 1** пользователь открывает detail screen.
- **альт. сценарий 1.1** часть блоков скрыта или read-only по статусу.
- **альт. сценарий 1.2** пользователь открывает связанную сущность.
- **осн. сценарий 2** пользователь переключается к редактированию в допустимом состоянии.

### Функциональные требования

#### Реализация для FRONTEND

**Описание UI**

| Экран | Результат |
| --- | --- |
| Детальная страница внедрения | Показывает информацию, связанные блоки и actions |

Требования на фронт:

- собрать detail composition и read/edit представление.

Связанный детальный FE pack: `slices/detail/requirements/frontend.md`

#### Реализация BACKEND

Требования на бэк:

- отдать detail payload и связанные данные для page composition.

Связанный детальный BE pack: `slices/detail/requirements/backend.md`

| | |
| --- | --- |
| **Сервис** | `deployment detail` |
| ИФТ URL | `уточняется` |
| База данных | `см. detail packs` |
| Методы | `см. slices/detail/requirements/backend.md` |

**Изменения в ролевой модели**

- Изменений ролевой модели на уровне control document не зафиксировано.

**Отправка в Аудит**

- Аудит определяется детальными пользовательскими действиями и lifecycle changes.

**BUGS (Если есть)**

- Пока не зафиксированы.

### Доп. пояснения

- Detail screen контролируется отдельно от формы, хотя они тесно связаны.

---

## STORY-DEPLOYMENTS-005 — Жизненный цикл внедрения

Slice card: `slices/lifecycle/slice.md`
Детализация FE: `slices/lifecycle/requirements/frontend.md`
Детализация BE: `slices/lifecycle/requirements/backend.md`
Прототип: `slices/lifecycle/delivery-prototype/prototype.html`
Planning story: `planning/stories/STORY-DEPLOYMENTS-005.md`

**Бизнес-требования**

- Цель: зафиксировать lifecycle rules для deployment.
- Бизнес-правила: переходы зависят от approval/ratification и product constraints; одновременно активна только одна продуктивная версия.
- Ограничения: lifecycle не дублирует page composition и DB schema.

**Пользовательские требования к АС КОДА**

- Пользователь видит доступные lifecycle actions и понимает последствия переходов.

**Критерии приемки**

1. Разрешённые переходы соответствуют бизнес-правилам.
2. Статусы и доступность действий синхронизированы между frontend и backend.
3. Ограничения по активной productive version enforced.

**USE CASES**

- **осн. сценарий 1** пользователь переводит внедрение по допустимому lifecycle-сценарию.
- **альт. сценарий 1.1** система отклоняет недопустимый переход.
- **альт. сценарий 1.2** переход блокируется из-за правил approval/ratification.
- **осн. сценарий 2** пользователь выполняет rollback или release-related action в допустимом состоянии.

### Функциональные требования

#### Реализация для FRONTEND

**Описание UI**

| Экран | Результат |
| --- | --- |
| Lifecycle actions на host screens | Показывают статусы и доступные переходы |

Требования на фронт:

- отображать lifecycle actions и ограничения по статусу.

Связанный детальный FE pack: `slices/lifecycle/requirements/frontend.md`

#### Реализация BACKEND

Требования на бэк:

- реализовать state transitions, guards и version constraints.

Связанный детальный BE pack: `slices/lifecycle/requirements/backend.md`

| | |
| --- | --- |
| **Сервис** | `deployment lifecycle` |
| ИФТ URL | `уточняется` |
| База данных | `см. slices/lifecycle/requirements/backend.md` |
| Методы | `см. detail pack` |

**Изменения в ролевой модели**

- Изменений ролевой модели на уровне control document не зафиксировано.

**Отправка в Аудит**

- В аудит попадают lifecycle transitions и rollback/release decisions, если это закреплено в detail packs.

**BUGS (Если есть)**

- Пока не зафиксированы.

### Доп. пояснения

- Lifecycle читаетcя после detail и формы, потому что зависит от их данных и контекста.

---

## DEPLOYMENTS-DB-API — DB/API контракт внедрения

Slice card: `slices/db-api/slice.md`
Детализация FE: `slices/db-api/requirements/frontend.md`
Детализация BE: `slices/db-api/requirements/backend.md`
Прототип: `slices/db-api/delivery-prototype/prototype.html`
Planning story: `planning/stories/STORY-DEPLOYMENTS-005.md`

**Бизнес-требования**

- Цель: зафиксировать низкоуровневый контракт хранения и API для внедрений.
- Бизнес-правила: DB/API слой не должен расходиться с lifecycle, lineage и scorecards rules.
- Ограничения: это инфраструктурный slice для контроля требований, а не отдельный пользовательский сценарий.

**Пользовательские требования к АС КОДА**

- Пользовательский эффект косвенный: корректная работа списков, форм, detail и lifecycle.

**Критерии приемки**

1. API и модель данных покрывают пользовательские сценарии deployment scope.
2. Поля, ограничения и маршруты согласованы с верхнеуровневыми slices.
3. Контракт совместим с существующим baseline и соседними features.

**USE CASES**

- **осн. сценарий 1** frontend вызывает deployment API для чтения и изменения данных.
- **альт. сценарий 1.1** backend отклоняет невалидное изменение.
- **альт. сценарий 1.2** несогласованный payload не проходит валидацию.
- **осн. сценарий 2** data model поддерживает lifecycle и lineage constraints.

### Функциональные требования

#### Реализация для FRONTEND

**Описание UI**

| Экран | Результат |
| --- | --- |
| Не отдельный экран | Slice обслуживает верхние UI-сценарии косвенно |

Требования на фронт:

- использовать согласованный API-контракт без локальных расхождений.

Связанный детальный FE pack: `slices/db-api/requirements/frontend.md`

#### Реализация BACKEND

Требования на бэк:

- описать и реализовать DB/API слой для deployment scope.

Связанный детальный BE pack: `slices/db-api/requirements/backend.md`

| | |
| --- | --- |
| **Сервис** | `deployment db-api` |
| ИФТ URL | `уточняется` |
| База данных | `см. slices/db-api/requirements/backend.md` |
| Методы | `см. detail pack` |

**Изменения в ролевой модели**

- Изменений ролевой модели на уровне control document не зафиксировано.

**Отправка в Аудит**

- Audit requirements определяются соседними пользовательскими slices.

**BUGS (Если есть)**

- Пока не зафиксированы.

### Доп. пояснения

- Этот slice завершает контроль, потому что служит технической опорой для остальных разделов.
