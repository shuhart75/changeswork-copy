# Simulation UI baseline

Дата обновления: `2026-04-24`

## Статус

Simulation UI считается частью уже существующего deployed baseline. В текущем квартале мы не перепроектируем эту область целиком; новая feature `simulation-bt-agent` добавляет дельту поверх существующей simulation detail page.

## Основные страницы

### Simulations list
Источник: `context/source-materials/legacy/changeswork-full/planning/mvp/current/tasks/legacy/mvp_tasks_simulations_page.md`

Что считаем existing coverage:
- отдельная страница списка симуляций из бокового меню;
- табличное представление с колонками: `ID`, `Название`, `Режим симуляции`, `Статус`, `Этап`, `Дата обновления этапа`, `Автор`, `Дата создания`;
- фильтрация по продукту и статусу;
- поиск по названию;
- сортировка по столбцам;
- пагинация;
- переход из строки списка в деталку.

Ролевая модель на уровне UI:
- ПРМ видит симуляции по всем продуктам, но изменение ограничено своим продуктом;
- методолог видит все симуляции;
- админ видит все симуляции.

### Simulation detail
Источники:
- `context/source-materials/legacy/changeswork-full/planning/mvp/current/tasks/legacy/mvp_tasks_simulation_detail_page.md`
- `context/source-materials/current-system/requirements/raw/final-spec/REQ_artifacts_core.md`

Что считаем existing coverage:
- блок `Основная информация` с `display_id`, названием, статусом, продуктом, датами и автором;
- read-only просмотр полей симуляции;
- блок артефактов как список внешних URL;
- блок связанных сущностей: пилоты и внедрения, связанные через скоркарты;
- переход к связанным сущностям из деталки;
- отображение статуса `draft/running/completed/failed`.

## Lifecycle-related UI behavior

- Симуляция не участвует в approval / ratification flow.
- Статусы симуляции отображают независимый execution lifecycle.
- После завершения или ошибки симуляция считается immutable для baseline-логики.

## Что не входит в baseline

- Кнопка `Сформировать БТ`;
- AI-диалог с RAIN;
- публикация БТ и отображение `btUrl`;
- любые новые session/retry/restart-паттерны, связанные с AI-agent flow.

Эти элементы относятся уже к `features/simulation-bt-agent/`.
