# Симуляции — Артефакты и связанные сущности (Backend)

Статус: **legacy imported existing coverage**
Область: baseline
Дата обновления: `2026-04-24`
Источники:
- `context/source-materials/legacy/changeswork-full/planning/mvp/current/tasks/legacy/mvp_tasks_simulation_artifacts_related.md`
- `context/source-materials/current-system/requirements/raw/final-spec/REQ_artifacts_core.md`

## Подтверждённый API-контур
- `GET /api/simulations/{id}/artifacts/`
- `POST /api/simulations/{id}/artifacts/`
- `DELETE /api/simulations/{id}/artifacts/{artifact_id}/`
- `GET /api/simulations/{id}/related/`

## Бизнес-правила
- артефакты хранятся как внешние URL;
- related entities возвращаются как read-only связи с пилотами и внедрениями через скоркарты;
- simulation scope не получает собственный approval-related процесс ради этих блоков.
