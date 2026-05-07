# Slice — Асинхронная отправка сообщения, polling и история

Статус: **draft**  
Feature: `features/simulation-bt-agent/feature.md`  
Порядок в feature requirements: `02`  
Дата обновления: `2026-05-07`

## Назначение
Описать жизненный цикл неблокирующей правой панели агента после открытия UI-сессии: отправку пользовательских сообщений через REST-фасад RAIN и async run, polling статуса сессии по `session_id`, разделение ошибок фасада и terminal `failed`/`timeout` агента, чтение RAIN-owned истории через backend АС КОДА, порционную загрузку длинной истории, отказ от `history_changed` в FE-BE API, лимит пользовательского `message=3000` символов и работу поверх интерфейса симуляций без блокировки экрана.

## Связанные planning stories
- `STORY-SIMULATION-BT-AGENT-002`

## Источники
- `../../references.md`
- `context/change-requests/simulation-bt-agent/agent_openapi_1.yaml`
- `context/change-requests/simulation-bt-agent/Системные_требования_для_интеграции_АС_КОДА_и_AI_Агента_RAIN.md`
- `/home/reutov/Documents/AI/simulations_AI_agent/docs/requirements/requirements-v1.md`
- `/home/reutov/Documents/AI/simulations_AI_agent/docs/requirements/system-requirements-v1.md`
- `/home/reutov/Documents/AI/simulations_AI_agent/materials/source/openapi.yaml`
- `/home/reutov/Documents/AI/simulations_AI_agent/prototype/simulation-agent-mock.html`

## Пакеты требований
- `../../requirements.md`
- `requirements/frontend.md`
- `requirements/backend.md`

## Связанные прототипы
- `delivery-prototype/prototype.html`

## Связанные execution-артефакты
- `execution/tasks.md` — пока отсутствует
