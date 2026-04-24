# Симуляции — Детальная страница (Frontend)

Статус: **legacy imported existing coverage**
Область: baseline
Дата обновления: `2026-04-24`
Источники:
- `context/source-materials/legacy/changeswork-full/planning/mvp/current/tasks/legacy/mvp_tasks_simulation_detail_page.md`
- `context/source-materials/current-system/requirements/raw/final-spec/REQ_artifacts_core.md`

## Что считается существующим поведением
- отображение `display_id`, названия, статуса, продукта, дат и автора;
- read-only просмотр основных полей симуляции;
- блок `Артефакты` со списком URL-ссылок;
- блок `Связанные сущности` с пилотами и внедрениями через скоркарты;
- переход к связанным сущностям из деталки.

## Host-screen note
- Именно эта existing detail page используется как host screen для будущей дельты `simulation-bt-agent`.
- Кнопка `Сформировать БТ` не входит в текущий baseline этого slice.
