# FEATURE-ARTIFACTS — Артефакты

Статус: **импортировано из legacy-проекта**  
Квартал: `2026-Q2`  
Дата обновления: `2026-04-27`

## Цель
Собрать в одной feature shared-контур артефактов как внешних ссылок для ключевых доменных сущностей MVP.

## Контекст
Feature импортирована из `changesWork` и current-system requirements. Артефакты используются как повторно применяемый механизм для `Pilot`, `Simulation` и `Deployment`, поэтому их удобно держать отдельной feature, а не размазывать по всем host screens.

## Ideal scope
- единый reusable artifacts module для всех целевых сущностей;
- согласованный CRUD, права доступа и сортировка;
- единообразное UI-отображение на host screens;
- базовый audit trail и traceability.

## MVP scope
- артефакты как внешние URL;
- привязка к `Pilot`, `Simulation`, `Deployment`;
- наследование прав от родительской сущности;
- единый BE/FE контракт и shared block behavior.

## Что исключено из MVP
- загрузка и хранение файлов;
- версионирование артефактов;
- preview/metadata extraction;
- отдельный workflow согласования артефактов.

## Входные материалы
- `references.md`
- `requirements.md`
- `slices/core/requirements/frontend.md`
- `slices/core/requirements/backend.md`

## Planning stories
- отдельные planning stories в standalone-проекте пока не нормализованы; feature зафиксирована как imported shared scope.

## Риски и зависимости
- feature зависит от прав на родительские сущности;
- изменение shared artifacts behavior потенциально затрагивает `pilots`, `simulations`, `deployments`.

## Решение по кварталу
- [x] imported shared scope зафиксирован
- [ ] берём как новую квартальную дельту
- [ ] дробим дополнительно
