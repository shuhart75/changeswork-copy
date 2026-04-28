# STORY-SIMULATION-BT-AGENT-001

Feature: `features/simulation-bt-agent/feature.md`  
Статус: **новая planning story**  
Дата обновления: `2026-04-24`

## Summary
Точка входа и контекст запуска БТ

## Description
Добавить в существующую детальную страницу завершённой симуляции точку входа в AI-agent сценарий: условный показ кнопки `Сформировать БТ`, проверку наличия уже созданного БТ, сбор `contextPrompt` из данных симуляции и передачу в диалоговый flow корректного начального контекста.

## Ideal scope
Гибкий entrypoint для нескольких продуктов и типов симуляций с полностью нормализованным mapping между данными simulation detail и полями, которые требуются агенту для формирования БТ.

## MVP scope
- отображение кнопки только для завершённой симуляции;
- использование существующей роли `experiment_editor_CC`;
- проверка наличия существующего БТ в деталке/итогах симуляции;
- сбор `simulationId`, `product`, `date`, `businessEffect`, `bt`, `riskParam`;
- подготовка host-экранной интеграции без переписывания существующей деталки.

## Analyst anchor estimate
- AN: 1 человеко-дней
- FE: 4 человеко-дней
- BE: 2 человеко-дней
- QA: 0 человеко-дней
- Total: 7 человеко-дней

## Team estimate
- AN: 1 человеко-дней
- FE: 4 человеко-дней
- BE: 2 человеко-дней
- QA: 0 человеко-дней
- Total: 7 человеко-дней

## Agreed estimate
- AN: 1 человеко-дней
- FE: 4 человеко-дней
- BE: 2 человеко-дней
- QA: 0 человеко-дней
- Total: 7 человеко-дней

## Actualization state
- `virtual`

## Mapping mode
- `explicit`

## Replaced by implementation tasks
- none yet

## Residual virtual tasks on actual-progress
- none

## Dependencies and assumptions
- существующая деталка симуляции и данные для `contextPrompt` уже доступны в deployed-системе;
- требуется подтвердить, где именно живёт source of truth для поля `Ссылка на БТ`;
- статусная логика показа кнопки не должна менять уже реализованный simulation UI.

## Notes for quarter planning
Опирается на `/home/reutov/Documents/AI/simulations_AI_agent/docs/requirements/requirements-v1.md` и `/home/reutov/Documents/AI/simulations_AI_agent/materials/source/Системные требования для интеграции АС КОДА и AI-Агента RAIN.md`.
