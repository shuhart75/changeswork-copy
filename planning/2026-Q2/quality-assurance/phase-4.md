# QA Phase 4 — detail pages и формы Change/Scorecard

Дата обновления: `2026-04-24`
Источник: `context/source-materials/legacy/changeswork-full/planning/mvp/current/tasks/legacy/mvp_tasks_qa_phase4.md`
Оценка legacy: `2 дня`

## Фокус фазы

Проверка detail/form UX для сложных рабочих экранов:
- detail `Change`;
- detail `Scorecard`;
- form `Change`;
- form `Scorecard`.

## Что проверялось

### Change detail
- основная информация, статусы, даты, автор;
- связанные scorecards;
- артефакты;
- связанные сущности;
- история внедрений и rollback timeline;
- lifecycle actions и rollback dialog.

### Scorecard detail
- основная информация и конфигурация;
- источники и использование;
- артефакты;
- JSON viewer / конфигурационные блоки.

### Change form
- обязательные поля;
- выбор scorecards;
- расчёт критичности в реальном времени;
- валидация и редирект после создания.

### Scorecard form
- выбор шаблона;
- JSON editor и валидация JSON;
- загрузка конфигурации из шаблона;
- создание и обработка ошибок.

## Acceptance frame

Legacy считал обязательным, чтобы:
- detail screens отображали все связные блоки корректно;
- timeline и related entities не расходились с данными;
- формы валидировали бизнес-правила и JSON;
- навигация между сущностями работала;
- права доступа и error handling были перепроверены.
