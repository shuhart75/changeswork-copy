# Feature Intake — Промышленная ролевая модель АС КОДА

Статус: **intake**  
Источник: `/home/reutov/Downloads/roll_model_koda.md`  
Предлагаемый slug: `roles-industrialization`  
Квартал: `2026-Q3`  
Дата: `2026-06-01`

## Что это за изменение

- Инициатива переводит текущий MVP/control-layer по RBAC в отдельную промышленную доработку с полным каталогом ролей, матрицей совместимости и маппингом ролей на endpoint-level доступ.
- Это выглядит как новая feature, а не как локальная правка `features/roles`, потому что источник задаёт новую целевую модель ролей, новые pattern-based продуктовые роли и отдельный слой cross-feature enforcement для API и host screens.
- Ожидаемый бизнес-результат: зафиксировать для Q3 целевую ролевую модель АС КОДА без повторного открытия Q2-объёма, который уже описан как imported MVP/control layer.

## Что уже есть в системе

### Покрытие в baseline/current

- `baseline/current/domain/contexts/identity-and-access.md` уже фиксирует существование RBAC и связи `User`/`UserRole`, но не содержит промышленную матрицу ролей из источника.
- `baseline/current/api/endpoints.md` и соседние feature requirements уже опираются на RBAC как на общий слой, но без endpoint-by-endpoint таблицы из нового источника.

### Покрытие в existing features

- `features/roles/` уже существует как Q2 imported control layer для MVP-ролей `prm`, `methodologist`, `approver`, `ratifier`, `admin`.
- `features/pilots/`, `features/simulations/`, `features/artifacts/` и часть соседних фич уже ссылаются на текущий RBAC-контур, но используют более узкие MVP-формулировки.

### Покрытие в legacy planning / source materials

- В `features/roles/` и Q2 planning зафиксирован только imported baseline/control scope, а не новая квартальная дельта.
- Новый источник `/home/reutov/Downloads/roll_model_koda.md` описывает отдельную целевую доработку на следующий квартал: каталог ролей, матрицу совместимости и endpoint mapping.

## Что является новой дельтой

- Глобальные роли `auditor`, `experiment_limited_view`, `experiment_admin`.
- Продуктовые pattern-based роли `experiment_editor_{space.code}`, `metodolog_{space.code}`, `simulation_specialist_{space.code}`.
- Явный справочник продуктов `{space.code}`.
- Матрица совместимости ролей с отдельным правилом для пересечения семейства `experiment_editor_{space.code}`.
- Таблица маппинга ролей на endpoint-операции для `Experiments`, `Spaces`, `Documents`, `Simulations`, `Files`, `NotificationParameters` и смежных read-only справочников.
- Q3-пакет консистентности для переноса новой модели в соседние feature requirements без переписывания Q2 planning scope.

## Предлагаемое размещение в harness

### Вариант решения

- `new feature`

### Почему именно так

- `features/roles/` уже занята Q2 imported feature и служит control layer для текущего квартала.
- Попытка расширить её этим источником смешала бы текущий квартал и Q3-дельту, а пользователь отдельно попросил не пересекать доработку с текущим кварталом.
- Новая feature позволяет держать Q2 как существующее покрытие, а Q3 как отдельную промышленную доработку с собственными planning stories и требованиями.

### Предлагаемый feature slug

- `roles-industrialization`

### Предлагаемые slices

- `role-catalog` — каталог ролей, продуктовых кодов и матрица совместимости.
- `endpoint-access-matrix` — mapping ролей на endpoint-level доступ и backend enforcement rules.
- `cross-feature-enforcement` — правила переноса новой модели в host screens и соседние feature packs.

## Q3 scope draft

### Что входит в Q3

- Нормализация целевой ролевой модели из `/home/reutov/Downloads/roll_model_koda.md` как отдельной feature.
- Planning stories и квартальный Q3-план для новой feature.
- Living requirements в новом лёгком формате по трем смысловым срезам.
- Явная фиксация границы: Q2 `features/roles/` остаётся control layer и не переопределяется этим объёмом.

### Что не входит в Q3

- Перепланирование `planning/2026-Q2` и перенарезка уже импортированного квартала.
- Ретроактивная замена MVP-ролей в `features/roles/` на новую промышленную модель.
- Release-promotion в `baseline/current/`.
- Полная межфичевая синхронизация всех соседних requirements прямо в этом intake-проходе.

### Риски по оценке / планированию

- В источнике у `experiment_limited_view` не расписаны уникальные полномочия, поэтому read-only профиль для этой роли фиксируется как рабочее допущение до уточнения.
- Матрица совместимости требует аккуратной интерпретации: текст про пересечение `experiment_editor_{space.code}` нужно удержать согласованным с таблицей.
- Endpoint mapping затронет соседние feature packs (`pilots`, `simulations`, `artifacts`) и baseline, поэтому часть propagation логично уйдёт в consistency backlog.

## Затронутые артефакты

### Affected baseline artifacts

- `baseline/current/domain/contexts/identity-and-access.md`
- `baseline/current/api/endpoints.md`
- `baseline/current/domain/ubiquitous-language.md`

### Affected existing features

- `features/roles/`
- `features/pilots/`
- `features/simulations/`
- `features/artifacts/`

### Affected prototypes

- `features/pilots/planning/scope-prototype/prototype.html`
- `features/simulations/planning/scope-prototype/prototype.html`

### Affected planning artifacts

- `planning/2026-Q3/gantt/*`

## Пробелы, которые мешают старту

### Baseline gaps

- Промышленная ролевая модель из источника ещё не отражена в `baseline/current`.

### Planning gaps

- В репозитории нет готового квартального контура `planning/2026-Q3`.

### Workflow gaps

- Текущий генератор `actual-progress` не изолирует feature по кварталу, поэтому Q3 execution view нельзя безопасно пересобирать автоматически без отдельной execution-актуализации.

## Решения перед scaffold

- [x] подтверждён feature slug
- [x] подтверждено: это отдельная feature, а не расширение `features/roles/`
- [x] согласованы initial slices
- [x] согласовано, что Q3 scope не пересекается с текущим кварталом
- [x] понятно, что baseline/cross-feature propagation пока уходит в backlog

## Рекомендуемый следующий шаг

- Создать `features/roles-industrialization/` как отдельную Q3 feature с planning stories, Q3 gantt includes и living requirements в новом лёгком формате.
