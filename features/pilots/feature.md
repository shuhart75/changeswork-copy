# FEATURE-PILOTS — Пилоты

Статус: **импортировано из legacy-проекта**  
Квартал: `2026-Q2`  
Дата обновления: `2026-06-08`

## Цель
Собрать в одной feature MVP-контур работы с пилотами: workspace, создание, просмотр, жизненный цикл и связи со скоркартами и внедрениями.

## Контекст
Feature импортирована из `changesWork` и current-system requirements. В существующих материалах пилоты описаны как единый рабочий контур без детального дробления на много user-facing slices, поэтому в новой структуре пока сохранён workspace-centric формат.

Порция документов от 2026-06-08 добавила связанную requirements-дельту `pilots-config-type`: пользовательский `processType` для пилотов хранится во внутренней модели `experiments.process_type`. Planning/execution/prototype материалы этой порции не импортированы в текущем режиме `requirements`.

## Ideal scope
- list/detail/form/lifecycle контур пилотов;
- тип процесса `processType` для online/offline/online+offline контура;
- связь с deployment и scorecards;
- approval/activation сценарии;
- trace, artifacts и бизнес-метрики без расхождений между экранами и API.

## MVP scope
- единый workspace пилотов;
- создание и редактирование пилота;
- выбор и отображение типа процесса через связанный пакет `features/pilots-config-type/`;
- просмотр деталки;
- lifecycle actions;
- работа со связанными scorecards и базовыми notifications/alerts в зафиксированном объёме.

## Что исключено из MVP
- дополнительные пользовательские представления вне зафиксированного workspace scope;
- произвольное расширение analytics/monitoring beyond existing requirement docs.

## Входные материалы
- `references.md`
- `requirements.md`
- `slices/workspace/requirements/frontend.md`
- `slices/workspace/requirements/backend.md`

## Planning stories
- `planning/stories/STORY-PILOTS-001.md`

## Риски и зависимости
- feature зависит от `deployments`, `scorecards`, `approvals` и shared `artifacts`;
- текущий импорт собран вокруг workspace pack, поэтому при будущей декомпозиции нужно аккуратно не потерять lifecycle и binding semantics.

## Решение по кварталу
- [x] imported existing scope зафиксирован
- [ ] берём как новую квартальную дельту
- [ ] дробим дополнительно
