# STORY-SIMULATION-BT-AGENT-002

Feature: `features/simulation-bt-agent/feature.md`  
Статус: **новая planning story**  
Дата обновления: `2026-04-24`

## Summary
Сессия диалога и оркестрация AI-агента

## Description
Реализовать прикладной контур диалога с AI-агентом RAIN: `POST /dialog/init`, `POST /dialog/{sessionId}/continue`, хранение и восстановление истории, блокировку параллельных сообщений, retry, restart и корректную обработку ошибок/таймаутов на стороне АС КОДА и интеграционного слоя.

## Ideal scope
Надёжный reusable dialog framework для AI-сценариев внутри АС КОДА с единым session lifecycle, строгой последовательностью сообщений, наблюдаемостью и согласованными SLA.

## MVP scope
- генерация `sessionId` и init диалога;
- продолжение диалога через `continue`;
- история сообщений и ограниченное восстановление сессии;
- retry до 3 попыток, таймаут, hard-block и `Перезапустить сессию`;
- anti-double-submit и строго последовательная обработка сообщений;
- фиксация Q2-ограничения на один продукт и один UI-flow.

## Analyst anchor estimate
- AN: 1 человеко-дней
- FE: 4 человеко-дней
- BE: 5 человеко-дней
- QA: 0 человеко-дней
- Total: 10 человеко-дней

## Team estimate
- AN: 1 человеко-дней
- FE: 4 человеко-дней
- BE: 5 человеко-дней
- QA: 0 человеко-дней
- Total: 10 человеко-дней

## Agreed estimate
- AN: 1 человеко-дней
- FE: 4 человеко-дней
- BE: 5 человеко-дней
- QA: 0 человеко-дней
- Total: 10 человеко-дней

## Actualization state
- `virtual`

## Mapping mode
- `explicit`

## Replaced by implementation tasks
- none yet

## Residual virtual tasks on actual-progress
- none

## Dependencies and assumptions
- зависит от story `STORY-SIMULATION-BT-AGENT-001`, потому что ей нужен подготовленный `contextPrompt`;
- в источниках есть конфликт по TTL сессии (`30 минут` vs `1 час`), который нужно снять до requirements;
- API агента и фактическая state machine должны быть приведены к одному контракту.

## Notes for quarter planning
Опирается на `/home/reutov/Documents/AI/simulations_AI_agent/docs/requirements/system-requirements-v1.md`, `/home/reutov/Documents/AI/simulations_AI_agent/materials/source/openapi.yaml` и интерактивный mock `prototype/simulation-agent-mock.html`.
