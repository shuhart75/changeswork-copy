# Interactive Status Snapshot 2026-04-17

Captured from the user in chat. If no executor is listed, the task is currently not assigned.

## Confirmed Status

| Task | Status | Executor | Notes |
| --- | --- | --- | --- |
| AN новые роли: роли/права/матрица | 100% | AN2 | |
| AN артефакты (BE): модель/контракты/права | 100% | AN2 | |
| BE артефакты (ссылки на документы) - БД + API | 100% | BE2 | |
| AN блок артефактов (FE): пилоты | 100% | AN2 | user corrected the earlier answer |
| FE пилоты - блок артефакты + UI под ЖЦ | 100% | FE1 | |
| AN блок артефактов (FE): симуляции | 100% | AN2 | |
| FE симуляции - блок артефакты | 100% | FE1 | |
| AN внедрения (BE): модель/контракты/права | 100% | AN1 | |
| BE внедрения - БД+API | 15% | BE3 | started on 2026-04-17; aligned to backlog task `RSCON-2349` |
| AN ЖЦ внедрений (BE) | 100% | AN1 | |
| BE ЖЦ внедрений | 0% | BE3 | assigned; queued after current deployment backend stream |
| AN список внедрений (FE) | 100% | AN1 | |
| FE список внедрений | 0% |  | |
| AN форма внедрения (создание/редактирование) (FE) | 100% | AN1 | |
| FE форма внедрения (создание/редактирование) | 0% |  | |
| AN скоркарты (BE): модель/шаблоны/валидаторы | 100% | AN1 | |
| BE скоркарты (включая шаблоны) - БД + API | 100% |  | backend-блок скоркарт закрыт; подтверждено пользователем 2026-04-17 |
| AN детальная скоркарты (BE) | 100% | AN1 | |
| AN детальная скоркарты (FE) | 100% | AN1 | |
| FE детальная скоркарты | 30% | FE2 | |
| AN форма скоркарты (BE) | 100% | AN1 | |
| BE форма создания/редактирования скоркарты | 100% | BE2 | backend-блок скоркарт закрыт; подтверждено пользователем 2026-04-17 |
| AN форма скоркарты (FE) | 100% | AN3 | |
| FE форма создания/редактирования скоркарты | 85% | FE2 | estimate aligned to real backlog task `RSCON-2340`; expected finish 2026-04-20 or 2026-04-21 |
| AN процесс согласования/утверждения (BE core) | 80% | AN3 | |
| BE процесс согласования и утверждения - БД+логика | 0% |  | |
| AN ЖЦ пилота: согласование/утверждение (BE) | 100% | AN3 | |
| BE ЖЦ пилота - согласование/утверждение | 0% |  | |
| AN страница "Согласования" (BE): контракты/фильтры/действия | 0% |  | |
| BE страница "Согласования" - API, логика | 0% |  | |
| AN страница "Согласования" (FE): UX/компоненты/edge-cases | 0% |  | |
| FE страница "Согласования" | 0% |  | |
| AN страница "Пакеты" (BE): контракты/массовые действия | 80% | AN3 | |
| AN страница "Пакеты" (FE): UX/компоненты/edge-cases | 80% | AN3 | |
| FE страница "Пакеты" | 0% |  | |
| AN уведомления: шаблоны/триггеры/получатели | 0% |  | |
| BE уведомления | 0% |  | |
| AN Trace (BE): модель связей/запросы/производительность | 100% | AN1 | |
| BE Trace - БД + логика + API | 0% |  | |
| AN Trace (FE): виджет блока связей | 100% | AN1 | |
| FE Trace - пилоты/симуляции/внедрения: блок связи | 0% |  | |
| QA подготовка (тест-план, тестовые данные, стенд) | 0% |  | |
| QA Артефакты | 0% |  | |
| QA Скоркарты (деталка+форма) | 0% |  | |
| QA Trace (блок связей) | 0% |  | |
| QA Согласования + Пакеты | 0% |  | |
| QA Регрессия + E2E smoke | 0% |  | |
| BE чата AI - интеграция | 0% |  | |
| FE UI для чата с AI агентом | 0% |  | |
| RSCON-2430 BE Табличные риск-параметры: API, БД, логика | 10% | BE2 | started on 2026-04-17; estimate 3d |
| RSCON-2431 BE Интеграция с РП: реализовать получение, обработку табличных РП | 0% |  | queued; estimate 3d |
| RSCON-2432 BE Интеграция с ФП Симуляция: доработать передачу табличных РП при запуске симуляции | 0% |  | queued; estimate 3d |
| RSCON-2429 FE Переделка формы для изменения риск-параметров | 0% | FE1 | queued; estimate 10d |
| BE статусной модели симуляции | 0% |  | |
| FE статусной модели симуляции | 0% |  | |
| BE симуляции снепшотов | 0% |  | |
| FE симуляции снепшотов | 0% |  | |
| QA AI чат | 0% |  | all QA tasks are 0% |
| QA Статусная модель симуляции | 0% |  | all QA tasks are 0% |
| QA Симуляция снепшотов | 0% |  | all QA tasks are 0% |
| QA All: smoke/regression | 0% |  | all QA tasks are 0% |

## Additional actualized notes

- Табличные риск-параметры в actualized tracking слое теперь представлены только реальными backlog-задачами `RSCON-2430`, `RSCON-2431`, `RSCON-2432`, `RSCON-2429`; legacy/generic задачи удалены.
- `RSCON-2430` assigned to `BE2`, estimate `3d`, started on `2026-04-17`, current status ~`10%`.
- `RSCON-2431` and `RSCON-2432` added as backend backlog tasks for tabular risk parameters; executor not specified yet.
- `RSCON-2429` assigned to `FE1`, estimate `10d`, currently `0%`.
- `RSCON-2445` (BE Базовая функциональность для внедрений) added to the actualized deployments backlog, assigned to `BE3`, currently `0%`, estimate `2d`.
- Because `RSCON-2445` is `2d`, `RSCON-2410` is forecast to start on `2026-04-24`.
- Resource leveling rule applied for `B3`: zero-progress tasks `BE_NOT` and `BE_STAT_SIM` were pushed right after the active deployments stream so the resource is not double-booked.
- Added a dynamic PlantUML today marker to the actualized gantt: current day is colored with `today is colored in LightSalmon`, plus milestone `[Мы сейчас здесь]` on `%now()`.
- Added milestone `Релиз RSCON-2438 КОДА 01.024.00` on `2026-05-21`; this release is used as the rollout point for the whole scorecards scope.
- Real backlog task `RSCON-2340` (manual scorecard creation + scorecards tab fill) is assessed at ~85% complete as of `2026-04-17`.
- Forecast finish date for `RSCON-2340`: Monday `2026-04-20` or Tuesday `2026-04-21`.
