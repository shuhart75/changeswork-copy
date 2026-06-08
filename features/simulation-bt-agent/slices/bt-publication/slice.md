# Slice — Действия по БТ, контекст симуляции и публикация

Статус: **draft**  
Feature: `features/simulation-bt-agent/feature.md`  
Порядок в feature requirements: `03`  
Дата обновления: `2026-06-08`

## Назначение
Описать часть сценария БТ внутри окна агента: условия доступности inline action `Сформировать БТ для текущей симуляции`, шаблон черновика запроса по ФИО пользователя и изменённым "Нижним границам" скалярных риск-параметров, запрет BT-сценария при табличных риск-параметрах, изменении только "Верхней границы" или только "Действует с" (дата), ручное редактирование текста перед отправкой, передачу `simulation_id` и `risk_params` в REST-фасад RAIN `POST /chat/runs`, запрет retry после `202 Accepted` и при terminal `failed`/`timeout` агента, а также показ `message.content` и структурированного `bt_page` artifact из результата run для ручного копирования без автосохранения в симуляцию.

## Связанные planning stories
- `STORY-SIMULATION-BT-AGENT-003`

## Источники
- `../../references.md`
- `context/change-requests/simulation-bt-agent/agent_openapi_1.yaml`
- `context/change-requests/simulation-bt-agent/Системные_требования_для_интеграции_АС_КОДА_и_AI_Агента_RAIN.md`
- `context/change-requests/simulation-bt-agent/simulations_api.md`
- `/home/reutov/Documents/AI/simulations_AI_agent/docs/requirements/requirements-v1.md`
- `/home/reutov/Documents/AI/simulations_AI_agent/docs/requirements/system-requirements-v1.md`
- `/home/reutov/Documents/AI/simulations_AI_agent/materials/source/API_Examples.md`
- `/home/reutov/Documents/AI/simulations_AI_agent/prototype/simulation-agent-mock.html`

## Пакеты требований
- `../../requirements.md`
- `requirements/frontend.md`
- `requirements/backend.md`

## Связанные прототипы
- `delivery-prototype/prototype.html`

## Связанные execution-артефакты
- `execution/tasks.md` — пока отсутствует
