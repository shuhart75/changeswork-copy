# Cross-cutting stream — Trace / related entities

Дата обновления: `2026-04-24`
Источники:
- `context/source-materials/legacy/changeswork-full/planning/mvp/current/tasks/legacy/mvp_tasks_chains_page.md`
- `planning/2026-Q2/imported-source/tasks/mvp_tasks_projectlibre_alignment.md`
- `planning/2026-Q2/imported-source/tasks/mvp_tasks_execution_order.md`
- `planning/2026-Q2/imported-source/tasks/mvp_tasks_list_no_analytics.md`
- `baseline/current/domain/contexts/lineage.md`

## Почему это отдельный stream

В legacy-gantt trace шёл как собственная дорожка:
- `AN_TRACE_BE`
- `BE_TRACE`
- `AN_TRACE_FE`
- `FE_TRACE`
- `QA_TRACE`

При этом trace не равен отдельной странице продукта. Это сквозной блок `Связанные сущности`, который должен был появляться на нескольких host screens.

## Legacy scope

### BE trace
- хранение и получение связей между `Pilot`, `Simulation`, `Deployment`;
- вычисление связей через `Scorecard` и/или `created_from`;
- API для read-only блока `Связанные сущности`.

### FE trace
- виджет / блок связанных сущностей на страницах пилота, симуляции и внедрения;
- переходы к связанным элементам;
- empty/loading/error states.

### QA trace
- отдельная проверка корректности связанных сущностей и переходов.

## Важное ограничение legacy

Документ `mvp_tasks_chains_page.md` явно фиксировал границу:
- полноценную страницу `Цепочки` не делаем;
- lineage widget как отдельную сущность тоже не делаем;
- допустим ограниченный preview источников и read-only trace блоки в формах / detail pages.

## Где этот stream разложен сейчас
- `baseline/current/domain/contexts/lineage.md`
- `baseline/current/ui/navigation.md`
- `features/simulations/slices/artifacts-related/`
- `features/pilots/`
- `features/deployments/`
- `planning/2026-Q2/quality-assurance/phase-4.md`
- `planning/2026-Q2/quality-assurance/final-mvp.md`

## Практический вывод

Trace уже частично растворён в feature-level требованиях, но в квартальном плане он был самостоятельным сквозным потоком. Этот файл нужен, чтобы сохранить именно эту управленческую картину и не потерять её между `features/*` и raw gantt.
