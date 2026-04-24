# FEATURE-SCORECARDS — Скоркарты

Статус: **импортировано из legacy-проекта**  
Квартал: `2026-Q2`  
Дата обновления: `2026-04-23`

## Цель
Собрать в одной feature MVP-контур работы со скоркартами: backend foundation и шаблоны, workspace/detail, создание и редактирование, а также сценарии привязки существующей скоркарты к доменным элементам.

## Контекст
Feature импортирована из `changesWork`. В legacy-задачах фигурировала отдельная страница списка скоркарт, но в текущем MVP она исключена. Актуальный scope фиксируем по текущим frontend/backend requirements и по фактическим backlog items `RSCON-2339..RSCON-2344`.

## Ideal scope
- полноценный scorecards workspace с отдельным list route;
- деталка с источниками, использованием и versioning context;
- формы создания/редактирования с шаблонами и расчётом критичности;
- lookup/select существующих скоркарт в формах `Pilot` и `Deployment`.

## MVP scope
- backend foundation сущности `Scorecard`, шаблоны и критичность;
- workspace скоркарты без отдельной list page;
- деталка скоркарты с источниками и использованием;
- создание и редактирование скоркарты;
- привязка существующей скоркарты к доменному элементу.

## Что исключено из MVP
- отдельная пользовательская страница списка скоркарт с фильтрами, экспортом и toolbar;
- расширенная история версий как отдельный UI-модуль;
- экспорт в Excel и продвинутые list/grid-возможности;
- любые незафиксированные legacy-сценарии за пределами current requirements.

## Входные материалы
- `references.md`
- `planning/MIGRATION_NOTES.md`
- `slices/workspace/requirements/frontend.md`
- `slices/workspace/requirements/backend.md`
- `slices/workspace/delivery-prototype/prototype.html`

## Planning stories
- `planning/stories/STORY-SCORECARDS-001.md`
- `planning/stories/STORY-SCORECARDS-002.md`
- `planning/stories/STORY-SCORECARDS-003.md`

## Риски и зависимости
- feature зависит от `deployments` и `pilots`, потому что создание, редактирование и binding скоркарты меняют версии доменных элементов;
- часть execution backlog сформулирована вокруг workspace/tab, а не напрямую вокруг planning stories, поэтому actualization mapping здесь частично inferred;
- отдельный scorecards list route вне MVP нельзя вернуть в квартал без отдельного planning decision.

## Решение по кварталу
- [x] берём в квартал
- [ ] переносим
- [ ] дробим дополнительно
