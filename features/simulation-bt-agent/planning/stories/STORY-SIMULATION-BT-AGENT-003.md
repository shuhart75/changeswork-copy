# STORY-SIMULATION-BT-AGENT-003

Feature: `features/simulation-bt-agent/feature.md`  
Статус: **новая planning story**  
Дата обновления: `2026-04-24`

## Summary
Публикация БТ, сохранение ссылки и аудит

## Description
Собрать финальную часть сценария: превью БТ перед публикацией, явное подтверждение пользователя, получение `btUrl` от агента, сохранение ссылки в АС КОДА, аудит ключевых событий и учёт межсервисных ограничений безопасности для Q2.

## Ideal scope
Полный publish-flow с согласованной моделью итогового документа, надёжным сохранением результата, прозрачным audit trail и production-ready security contract без окруженческих допущений.

## MVP scope
- превью структуры БТ перед созданием страницы;
- обязательное подтверждение пользователя `Да/Нет`;
- получение и сохранение `btUrl`;
- отображение ссылки в `Итогах симуляции`;
- аудит запуска, перезапуска, успеха и финальной ошибки;
- учёт HTTPS/mTLS/OTT ограничений и Q2-допущений для ИФТ.

## Analyst anchor estimate
- 8 человеко-дней

## Team estimate
- 8 человеко-дней

## Agreed estimate
- 8 человеко-дней

## Actualization state
- `virtual`

## Mapping mode
- `explicit`

## Replaced by implementation tasks
- none yet

## Residual virtual tasks on actual-progress
- none

## Dependencies and assumptions
- зависит от story `STORY-SIMULATION-BT-AGENT-002`, потому что publish-flow завершает диалоговую сессию;
- требуется подтвердить storage semantics для `btUrl` и канонический способ отображения ссылки в АС КОДА;
- security и audit constraints не должны потеряться при переходе от planning к requirements.

## Notes for quarter planning
Опирается на `/home/reutov/Documents/AI/simulations_AI_agent/docs/requirements/requirements-v1.md`, `/home/reutov/Documents/AI/simulations_AI_agent/docs/requirements/system-requirements-v1.md` и `/home/reutov/Documents/AI/simulations_AI_agent/materials/source/API_Examples.md`.
