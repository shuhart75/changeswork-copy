# Simulation API baseline

Дата обновления: `2026-04-24`

## Статус

Simulation API считаем существующим baseline coverage, но зафиксированным в legacy-источниках не полностью в том же стандарте URI, что и более новые `v1`-контракты. До отдельной canonical normalization задачи эти endpoint'ы считаются подтверждённым existing behavior, а не новой квартальной доработкой.

## Endpoint groups

### List
Источник: `context/source-materials/legacy/changeswork-full/planning/mvp/current/tasks/legacy/mvp_tasks_simulations_page.md`

`GET /api/simulations/`

Назначение:
- получить список симуляций с фильтрацией, поиском, сортировкой и пагинацией.

Ключевые query-параметры из legacy-описания:
- `product_id`
- `status`
- `search`
- `page`
- `page_size`
- `ordering`

Возвращаемые поля списка:
- `id`
- `display_id`
- `name`
- `mode`
- `status`
- `stage`
- `stage_updated_at`
- `created_at`
- `created_by`

### Detail
Источник: `context/source-materials/legacy/changeswork-full/planning/mvp/current/tasks/legacy/mvp_tasks_simulation_detail_page.md`

`GET /api/simulations/{id}/`

Возвращает current-state деталку симуляции, включая:
- идентификаторы;
- название;
- статус;
- продукт;
- даты `created_at`, `started_at`, `completed_at`;
- автора;
- агрегированные счётчики `artifacts_count`, `related_pilots_count`, `related_changes_count`.

### Artifacts and related entities
Источник: `context/source-materials/legacy/changeswork-full/planning/mvp/current/tasks/legacy/mvp_tasks_simulation_detail_page.md`

Подтверждённое existing coverage:
- `GET /api/simulations/{id}/artifacts/`
- `POST /api/simulations/{id}/artifacts/`
- `DELETE /api/simulations/{id}/artifacts/{artifact_id}/`
- `GET /api/simulations/{id}/related/`

Смысл:
- хранение и выдача URL-артефактов симуляции;
- выдача связанных пилотов и внедрений через lineage/scorecard usage.

### Lifecycle actions
Источник: `context/source-materials/legacy/changeswork-full/planning/mvp/current/tasks/legacy/mvp_tasks_simulation_lifecycle.md`

Подтверждённое existing coverage:
- `POST /api/simulations/{id}/start/`
- `POST /api/simulations/{id}/complete/`
- `POST /api/simulations/{id}/fail/`

Смысл:
- переход `draft -> running`;
- переход `running -> completed`;
- переход `running -> failed`.

## Business rules fixed by API layer

- Симуляция не участвует в approval / ratification.
- Управление lifecycle доступно только ПРМ своего продукта или админу.
- При завершении сохраняется `result`.
- При ошибке сохраняется `error_message`.
- После `completed` / `failed` simulation scope считается immutable в baseline-логике.

## Нормализационная оговорка

Эти endpoint'ы задокументированы преимущественно в legacy task docs, а не в финальном unified OpenAPI. Поэтому:
- считаем их частью существующей системы;
- не создаём из этого новую feature;
- отдельно помним, что URI и field naming ещё могут потребовать future baseline normalization.
