# MVP Planning v6.31 Commander Baseline (source: ProjectLibre Q2.pod)

**Base spec:** `spec/domain_model.md`  
**Base schedule:** Commander baseline (см. `gantt/`, файл `mvp_gantt_chart_current.puml` указывает на `mvp_gantt_chart_commander_frozen.puml`)

**Plan priority:** leadership baseline derived from `all_tasks_fast`, with official 2026 non-working days, named vacations, and commander coefficient `1.3`.

**Previous baseline:** approved MVP-priority plan is kept in `planning/mvp/versions/v6.22/`.

## Entry points

- Prototype (MVP): `prototype.html` (symlink to `prototypes/current.html`)
- Gantt (frozen baseline view): `gantt/mvp_gantt_chart_current.puml`
- Gantt source (editable, dependency-based): `gantt/mvp_gantt_chart_commander.puml`
- Gantt tracking / fact-forecast view: `gantt/mvp_gantt_chart_current_actualized.puml`
- Tasks index: `tasks/mvp_tasks_summary.md`
- TaskJuggler baseline: `taskjuggler/mvp_current.tjp`
- MVP scope / plan / stories / timeline: `docs/`

## Notes (MVP v6.15 scope)

- **Инициативы (Initiative)** исключены из MVP (CRUD/страницы/ЖЦ не делаем).
- Симуляции НЕ участвуют в согласовании/утверждении (существующий ЖЦ не меняем).
- Блоки **"Артефакты" (URL)** и **"Связанные сущности"** добавляем на страницы и формы: Simulation, Pilot, Deployment.
- Страницы **"Цепочки"** и lineage widget **не делаем** (ни в MVP, ни вообще). В MVP остаются только источники `created_from`: автосоздание на create + preview в формах.
- **Список скоркарт** (страница/роут/пункт меню) исключен из MVP; в MVP остаются **деталка** и **создание/редактирование** скоркарты.
- Уточнены правила ratification (поэлементные статусы в пакете), статусы при reject (`approval_rejected` / `ratification_rejected`) и обязательный recall.

### Важно про план задач

В v6.15 декомпозиция и оценки dev-задач синхронизированы с ProjectLibre файлом:

- `planning/mvp/imports/projectlibre/Q2.pod`

Рекомендуемая точка входа:

- `tasks/mvp_tasks_summary.md`
- `tasks/mvp_tasks_execution_order.md`
- `tasks/mvp_tasks_projectlibre_alignment.md`


## Actualization notes (2026-04-17)

- В actualized tracking слое завершен backend-блок скоркарт: `RSCON-2342`, `RSCON-2343`, `RSCON-2344`.
- `RSCON-2340` оценена в ~85% готовности; прогноз завершения - в понедельник-вторник, `2026-04-20`-`2026-04-21`.
- В backend-блоке внедрений задачи `RSCON-2349`, `RSCON-2410`, `RSCON-2445` назначены на `BE3`; `RSCON-2349` стартовала и оценена в ~15% готовности.
- `RSCON-2445` уточнена до оценки `2d`; backend-последовательность внедрений на `BE3` пересчитана с учетом этой длительности.
- Блок табличных риск-параметров в actualized tracking слое очищен от legacy/generic задач; оставлены только реальные backlog-задачи `RSCON-2430`, `RSCON-2431`, `RSCON-2432`, `RSCON-2429`.
- `RSCON-2430` (BE Табличные риск-параметры: API, БД, логика) назначена на `BE2`, оценка `3d`, старт `2026-04-17`, статус ~`10%`.
- `RSCON-2431` и `RSCON-2432` добавлены как backend backlog stream табличных РП; исполнитель пока не указан, поэтому оставлены на `TBD_BE`.
- `RSCON-2429` (FE Переделка формы для изменения риск-параметров) добавлена в tracking слой на `FE1`, оценка `10d`, пока `0%`.
- Для actualized tracking включено resource-leveling по факту: при старте `RSCON-2349` на `B3` нулевые задачи этого же ресурса (`BE_NOT`, `BE_STAT_SIM`) сдвинуты вправо, чтобы у ресурса не было параллельных 0%-задач.

## Validation notes

- Для проверки capacity / overlap текущим валидатором используйте `gantt/mvp_gantt_chart_commander.puml`.
- `gantt/mvp_gantt_chart_current.puml` — frozen/rendered baseline view; это не тот файл, который надо редактировать или валидировать как source of dependencies.
- `gantt/mvp_gantt_chart_current_actualized.puml` — fact/forecast view с явными датами старта; текущий валидатор этот формат не поддерживает.
- Известное ограничение текущего валидатора: vacation-блоки `VAC_*` с явными `starts YYYY/MM/DD` в `gantt/mvp_gantt_chart_commander.puml` могут давать ложные overlap-срабатывания.
