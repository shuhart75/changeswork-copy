# Требования по feature — Скоркарты

Статус: **draft**
Feature: `features/scorecards/feature.md`
Квартал: `2026-Q2`
Дата обновления: `2026-04-27`
Шаблон: `.workflow/templates/requirements/feature-requirements.template.md`

## Оглавление

Используются заголовки до уровня `####`.

## Общий контур feature

- Назначение feature: описать MVP-контур скоркарт как workspace без отдельной list page, с create/edit/detail и binding к доменным элементам.
- Что уже есть в baseline/current: workspace frontend/backend packs и прототип.
- Какая дельта добавляется этой feature: единый root-документ контроля вместо разрозненного чтения детальных packs.
- Какие slice входят в контрольный документ: `workspace`.

## Порядок slice для контроля

1. `01 workspace — Workspace скоркарты`

---

## STORY-SCORECARDS-001..003 — Workspace скоркарты

Slice card: `slices/workspace/slice.md`
Детализация FE: `slices/workspace/requirements/frontend.md`
Детализация BE: `slices/workspace/requirements/backend.md`
Прототип: `slices/workspace/delivery-prototype/prototype.html`
Planning story: `planning/stories/STORY-SCORECARDS-001.md`, `planning/stories/STORY-SCORECARDS-002.md`, `planning/stories/STORY-SCORECARDS-003.md`

**Бизнес-требования**

- Цель: обеспечить работу со скоркартами как с доменным инструментом для `Pilot` и `Deployment`.
- Бизнес-правила: отдельная list page вне текущего MVP исключена; критичность вычисляется по правилам; изменения binding влияют на связанные доменные элементы.
- Ограничения: Excel/export и расширенный list UX вне scope.

**Пользовательские требования к АС КОДА**

- Пользователь может создавать, просматривать, редактировать и привязывать существующие скоркарты.
- Пользователь видит источники, использование и ключевые атрибуты скоркарты.

**Критерии приемки**

1. Create/edit/detail flow работает без отдельной list page.
2. Binding существующей скоркарты к доменному элементу поддерживается по правилам MVP.
3. Критичность и шаблоны скоркарты обрабатываются согласованно.

**USE CASES**

- **осн. сценарий 1** пользователь создаёт новую скоркарту из контекста доменного элемента.
- **альт. сценарий 1.1** пользователь редактирует существующую скоркарту.
- **альт. сценарий 1.2** пользователь привязывает существующую скоркарту вместо создания новой.
- **осн. сценарий 2** пользователь открывает деталку скоркарты и видит источники и использование.

### Функциональные требования

#### Реализация для FRONTEND

**Описание UI**

| Экран | Результат |
| --- | --- |
| Workspace / detail / form flow | Поддерживает просмотр, создание, редактирование и binding |

Требования на фронт:

- реализовать workspace-модель без отдельного list route;
- поддержать create/edit/detail и binding flows.

Связанный детальный FE pack: `slices/workspace/requirements/frontend.md`

#### Реализация BACKEND

Требования на бэк:

- реализовать сущность скоркарты, шаблоны, версии и контракты binding;
- согласовать изменения скоркарты с `Pilot` и `Deployment`.

Связанный детальный BE pack: `slices/workspace/requirements/backend.md`

| | |
| --- | --- |
| **Сервис** | `scorecards workspace` |
| ИФТ URL | `уточняется` |
| База данных | `см. detail pack` |
| Методы | `см. slices/workspace/requirements/backend.md` |

**Изменения в ролевой модели**

- Отдельных изменений ролевой модели на уровне control document не зафиксировано.

**Отправка в Аудит**

- В аудит попадают создание, изменение и операции binding, если это закреплено в detail packs.

**BUGS (Если есть)**

- Пока не зафиксированы.

### Доп. пояснения

- Это единый slice, но внутри него сохранён полный контролируемый контур workspace/detail/form/binding.
