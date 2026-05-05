# STORY-ARTIFACTS-001

Feature: `features/artifacts/feature.md`  
Статус: **импортировано из legacy-плана и partially materialized**  
Дата обновления: `2026-05-04`

## Summary
Shared backend-контур артефактов и доступ к разделу Документы

## Description
Собрать shared backend-контур артефактов как внешних ссылок: аналитическую постановку, БД и API, а также follow-up по открытию доступа к разделу `Документы` для пользователей.

## Ideal scope
Единый reusable backend-модуль артефактов с согласованными правами, валидацией и доступностью на host screens.

## MVP scope
- модель/контракты/права для shared-контура артефактов;
- БД и API для артефактов как ссылок;
- follow-up по доступу к разделу `Документы`.

## Analyst anchor estimate
- AN: 2 человеко-дня
- FE: 0 человеко-дней
- BE: 3 человеко-дня
- QA: 0 человеко-дней
- Total: 5 человеко-дней

## Team estimate
- AN: 2 человеко-дня
- FE: 0 человеко-дней
- BE: 3 человеко-дня
- QA: 0 человеко-дней
- Total: 5 человеко-дней

## Agreed estimate
- AN: 2 человеко-дня
- FE: 0 человеко-дней
- BE: 3 человеко-дня
- QA: 0 человеко-дней
- Total: 5 человеко-дней

## Actualization state
- `mixed`

## Mapping mode
- `explicit`

## Replaced by implementation tasks
- `RSCON-2468`

## Residual virtual tasks on actual-progress
- `AN_ART_BE`
- `BE_ART`

## Dependencies and assumptions
- shared backend-контур дальше используется `pilots`, `simulations`, `deployments`;
- `RSCON-2468` трактуем как продолжение той же story, а не как отдельную feature.

## Notes for quarter planning
Story нормализована только сейчас: раньше feature жила как imported shared scope без отдельной planning-story, хотя execution-слой уже был частично заполнен.
