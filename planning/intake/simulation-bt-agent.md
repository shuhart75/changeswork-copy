# Feature Intake — Формирование БТ из симуляции через AI-агента RAIN

Статус: **accepted for scaffold**  
Источник: `/home/reutov/Documents/AI/simulations_AI_agent`  
Предлагаемый slug: `simulation-bt-agent`  
Квартал: `2026-Q2`  
Дата: `2026-04-24`

## Что это за изменение

- Источник описывает сценарий запуска AI-агента RAIN со страницы завершённой симуляции в АС КОДА для формирования бизнес-требования в Confluence и сохранения ссылки на созданный БТ обратно в систему.
- Пользователь отдельно подтвердил, что симуляции и деталка симуляции уже реализованы в системе в полном объёме; значит материалы про `Основную информацию`, вкладки, статус-бар и `GET /api/v1/simulation/{number}` нужно трактовать как описание существующего system coverage, а не как новую feature.
- Истинная новая дельта из источника — AI-agent flow: кнопка запуска, диалог, интеграция с RAIN, публикация БТ и сохранение `btUrl`.
- Ожидаемый бизнес-результат: сократить ручную подготовку БТ после завершённой симуляции и встроить создание документа в рабочий контур ПРМ-аналитика без перехода в другую систему.

## Что уже есть в системе

### Покрытие в baseline/current

- По уточнению пользователя текущая deployed-система уже содержит полный контур симуляций и деталку симуляции; source-файлы с описанием вкладки `Основная информация` относятся к уже существующему поведению.
- `baseline/current/domain/aggregates/simulation.md` уже фиксирует `Simulation` как доменный агрегат с жизненным циклом `draft -> running -> completed/failed`.
- `baseline/current/domain/contexts/research-and-execution.md` уже ставит `Simulation` в один контур с `Pilot` и `Deployment`.
- `baseline/current/domain/business-rules.md` уже содержит инварианты симуляции: запуск только из `draft`, отсутствие редактирования во время выполнения, immutable после завершения.
- `baseline/current/domain/business-rules.md` уже разрешает артефакты для `Simulation`, но не описывает сценарий AI-диалога, `btLink`, UI-кнопку, диалоговые сессии и Confluence-интеграцию.
- `baseline/current/domain/contexts/identity-and-access.md` уже содержит модель ролей, но в baseline нет канонического правила доступа для запуска сценария `Сформировать БТ`.

### Покрытие в existing features

- Отдельной feature `simulations` в harness пока нет.
- `features/deployments/*` и `features/scorecards/*` используют `Simulation` как связанную сущность, но не покрывают диалог с AI-агентом и публикацию БТ.
- `features/roles/*` потенциально затрагивается только в части явной фиксации использования уже существующей роли `experiment_editor_CC`.
- Отсутствие feature `simulations` в harness теперь трактуем не как новую квартальную фичу, а как пробел нормализации baseline/source-of-truth.

### Покрытие в legacy planning / source materials

- В `planning/2026-Q2/imported-source/tasks/mvp_tasks_projectlibre_alignment.md` уже есть simulation-related объем: `FE_SIM_ART`, `FE_TRACE`, `BE_STAT_SIM`, `FE_STAT_SIM`, `BE_SIM_SNAP`, `FE_SIM_SNAP`.
- Эти imported planning artifacts показывают, что simulation scope уже присутствовал в legacy-планировании.
- В самом источнике `/home/reutov/Documents/AI/simulations_AI_agent` есть не только AI-agent интеграция, но и материалы по существующей странице симуляции и её API; для текущего intake эту часть считаем evidence по уже реализованному baseline coverage.

## Что является новой дельтой

- Кнопка `Сформировать БТ` на вкладке `Основная информация` для завершённой симуляции.
- UI-диалог с агентом RAIN с историей сообщений, состояниями ожидания, retry и явным действием `Перезапустить сессию`.
- Формирование `contextPrompt` из данных симуляции, включая `simulationId`, продукт, дату, `businessEffect`, факт наличия ранее созданного БТ и список риск-параметров `AS IS / TO BE`.
- Интеграция с API агента `POST /dialog/init` и `POST /dialog/{sessionId}/continue`.
- Возврат и сохранение `btUrl` в АС КОДА с отображением ссылки в `Итогах симуляции`.
- Аудит, session TTL, последовательная обработка сообщений и защищённое межсервисное взаимодействие.
- Ограничение первой итерации только продуктом `Кредитные карты`.

## Предлагаемое размещение в harness

### Вариант решения

- `new feature`

### Почему именно так

- Split подтверждён: существующая деталка симуляции остаётся в зоне already-implemented system coverage, а новая feature ограничивается AI-agent flow поверх этой деталки.
- Это даёт чёткую planning-границу: не перепланируем уже существующие simulation screens, а проектируем только дельту по `RAIN + Confluence + btUrl`.
- В текущем harness нет existing feature, которую корректно расширить без размытия ответственности; новая функциональность лучше оформляется как отдельная feature на уровне квартального planning.

### Предлагаемый feature slug

- `simulation-bt-agent`

### Предлагаемые slices

- `agent-entrypoint` — условия показа кнопки, сбор `contextPrompt`, проверка существующего БТ.
- `dialog-session` — init/continue, история, retry, restart, anti-double-submit, TTL.
- `bt-publication` — превью БТ, подтверждение, получение `btUrl`, сохранение ссылки и аудит.

## Q2 scope draft

### Что входит в Q2

- Взять в Q2 AI-agent MVP для завершённых симуляций продукта `Кредитные карты`.
- Включить API-интеграцию с агентом, формирование `contextPrompt`, UI-сессию, retry, restart, TTL, сохранение `btUrl`.
- Включить явное правило доступа через уже существующую роль `experiment_editor_CC`, без ввода новых ролей.
- Использовать уже существующую детальную страницу симуляции как host screen для новой кнопки и диалога, без перепроектирования этой страницы.

### Что не входит в Q2

- Реализация или переписывание существующей деталки симуляции, её вкладок, статус-бара и read-only формы просмотра.
- Нормализация всей simulation feature-структуры в harness как отдельной planning-единицы, если пользователь не попросит это отдельно.
- Обобщение сценария на другие продукты за пределами `Кредитные карты`.
- Любая полная переработка simulation domain model сверх уже описанных baseline инвариантов.
- Расширение imported simulation scope из legacy-плана: snapshots, расширенная статусная модель, trace/artifacts actualization.
- Автоматическое обогащение русскими названиями риск-параметров и обратная запись в ФП Риск-параметры.

### Риски по оценке / планированию

- Самый большой риск: canonical baseline в harness пока недоописывает уже существующую детальную страницу симуляции, поэтому легко случайно перепутать existing coverage и новую дельту.
- Не зафиксировано, считать ли хранение истории 30 минут или 1 час: в разных документах есть расхождение.
- Не нормализована граница ответственности между АС КОДА и агентом RAIN по хранению сессии, повторным попыткам и восстановлению истории.
- Нужно аккуратно решить, считаем ли baseline-normalization по уже существующей simulation detail отдельной follow-up работой, чтобы не засорить scope этой feature.

## Затронутые артефакты

### Affected baseline artifacts

- `baseline/current/domain/aggregates/simulation.md`
- `baseline/current/domain/contexts/research-and-execution.md`
- `baseline/current/domain/business-rules.md`
- `baseline/current/domain/contexts/identity-and-access.md`
- `baseline/current/api/README.md`
- `baseline/current/ui/README.md`
- `baseline/current/requirements/README.md`

### Affected existing features

- `features/roles/`

### Affected prototypes

- Явных harness-прототипов, которые обязательно надо менять на этапе intake, пока нет.

### Affected planning artifacts

- `planning/intake/simulation-bt-agent.md`

## Пробелы, которые мешают старту

### Baseline gaps

- В baseline нет канонического описания уже существующего simulation detail page как host screen для AI-agent сценария.
- В baseline нет канонического API-контракта интеграции с AI-агентом.
- Не зафиксировано, является ли `btUrl` специальным полем симуляции, частью результатов симуляции или отдельным доменным объектом/внешней ссылкой.

### Planning gaps

- Нужно отдельно решить, оформляем ли baseline-normalization существующей деталки симуляции как отдельную follow-up работу вне этой feature.
- Нужно подтвердить, где именно хранится truth по полю `Ссылка на БТ`: в summary/results симуляции, в отдельном внешнем artifact-link или в выделенном атрибуте.
- Нужно снять противоречие по времени жизни UI-сессии: `30 минут` в `docs/requirements/*` против `1 час` в системных требованиях из источника.

### Workflow gaps

- Источник лежит вне текущего harness и пока не разложен на `references.md`/feature-local source materials.
- До scaffold не хватает решения, нужно ли отдельно документировать existing simulation detail в baseline/current до старта planning stories по агенту.
- Для следующего шага достаточно одного feature-потока `simulation-bt-agent`; второй scaffold-поток по `simulations` не нужен, если пользователь отдельно его не запрашивает.

## Решения перед scaffold

- [x] подтверждён feature slug
- [x] подтверждено: это отдельная feature или расширение существующей
- [x] согласованы initial slices
- [x] согласовано, что именно входит в Q2
- [ ] понятно, какие baseline gaps закрываем сразу, а какие уводим в backlog

## Рекомендуемый следующий шаг

- Scaffold feature `simulation-bt-agent` выполнен; следующий шаг — использовать planning stories для quarter planning/HLE или переключиться в `requirements` mode для подготовки requirement packs.
