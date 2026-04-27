# FEATURE-PILOTS — Пилоты

Статус: **импортировано из legacy-проекта**  
Квартал: `2026-Q2`  
Дата обновления: `2026-04-27`

## Цель
Собрать в одной feature MVP-контур работы с пилотами: workspace, создание, просмотр, жизненный цикл и связи со скоркартами и внедрениями.

## Контекст
Feature импортирована из `changesWork` и current-system requirements. В существующих материалах пилоты описаны как единый рабочий контур без детального дробления на много user-facing slices, поэтому в новой структуре пока сохранён workspace-centric формат.

## Ideal scope
- list/detail/form/lifecycle контур пилотов;
- связь с deployment и scorecards;
- approval/activation сценарии;
- trace, artifacts и бизнес-метрики без расхождений между экранами и API.

## MVP scope
- единый workspace пилотов;
- создание и редактирование пилота;
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
- отдельные planning stories в standalone-проекте пока не нормализованы; imported pilot scope зафиксирован как единый workspace.

## Риски и зависимости
- feature зависит от `deployments`, `scorecards`, `approvals` и shared `artifacts`;
- текущий импорт собран вокруг workspace pack, поэтому при будущей декомпозиции нужно аккуратно не потерять lifecycle и binding semantics.

## Решение по кварталу
- [x] imported existing scope зафиксирован
- [ ] берём как новую квартальную дельту
- [ ] дробим дополнительно
