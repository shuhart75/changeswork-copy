# Симуляции — Артефакты и связанные сущности (Frontend)

Статус: **legacy imported existing coverage**
Область: baseline
Дата обновления: `2026-04-24`
Источники:
- `context/source-materials/legacy/changeswork-full/planning/mvp/current/tasks/legacy/mvp_tasks_simulation_artifacts_related.md`
- `context/source-materials/current-system/requirements/raw/final-spec/REQ_artifacts_core.md`

## Что считается существующим поведением
- на simulation detail отображаются блоки `Артефакты` и `Связанные сущности`;
- в edit form артефакты доступны для list/add/delete с учётом прав;
- в create form блоки присутствуют, но disabled / empty до создания сущности;
- связанные сущности отображаются как read-only список пилотов и внедрений.

## UI-state rules
- артефакты представлены URL-ссылками, а не загруженными файлами;
- связанные сущности показывают cross-feature связь через скоркарты;
- отсутствие backend endpoint для related view трактуется как backend-gap, а не как UI-изобретение нового контракта.
