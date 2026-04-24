# MVP Planning

Эта папка хранит артефакты планирования MVP в единообразной схеме:

- `versions/` содержит зафиксированные версии планов
- `current/` указывает на актуальную версию (symlink)
- `tasks/` и `gantt/` оставлены как совместимые ссылки на `current/*` (symlink)

## Актуальная версия

- [`planning/mvp/current/`](/home/reutov/Documents/AI/changesWork/planning/mvp/current)

## Версии

- [`planning/mvp/versions/v6.37/`](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.37) текущая (`RSCON-2430` и `RSCON-2340` отмечены завершёнными на `2026/04/20`; добавлен milestone `Конец Q2` на `2026/06/30`; из дополнительных compressed-view поддерживается только aggressive; `current` переключен на эту версию)
- [`planning/mvp/versions/v6.36/`](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.36) предыдущая (добавлен третий, более агрессивный single-page view для actualized gantt: weekly + глобальный `scale 2/3`)
- [`planning/mvp/versions/v6.35/`](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.35) предыдущая (добавлены два альтернативных single-page view для actualized gantt: weekly-view с `printscale weekly` и compact-view с `printscale daily zoom 1`)
- [`planning/mvp/versions/v6.34/`](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.34) предыдущая (в actualized-слой добавлен milestone релиза `RSCON-2438 КОДА 01.024.00` на `2026/05/21`; в этот релиз выносим весь блок скоркарт)
- [`planning/mvp/versions/v6.33/`](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.33) предыдущая (откачены лишние сдвиги из `v6.32`; оставлено только добавление dynamic today-marker в начало actualized PlantUML-диаграммы через `today is colored in LightSalmon`, `%now()` и milestone `Мы сейчас здесь`)
- [`planning/mvp/versions/v6.32/`](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.32) предыдущая (промежуточная версия, заменена `v6.33`)
- [`planning/mvp/versions/v6.31/`](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.31) предыдущая (в actualized tracking слое включено resource-leveling: при старте задач на `B3` нулевые задачи этого же ресурса сдвинуты вправо, чтобы не перегружать ресурс)
- [`planning/mvp/versions/v6.30/`](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.30) предыдущая (блок табличных риск-параметров в actualized tracking слое очищен от legacy/generic задач; оставлены только `RSCON-2430`, `RSCON-2431`, `RSCON-2432`, `RSCON-2429`)
- [`planning/mvp/versions/v6.29/`](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.29) предыдущая (`RSCON-2430` добавлена в actualized tracking слой: `BE2`, `3d`, старт `2026-04-17`, статус ~`10%`)
- [`planning/mvp/versions/v6.28/`](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.28) предыдущая (документация по planning/validation приведена в соответствие: валидатор надо запускать на `mvp_gantt_chart_commander.puml`, а не на frozen `mvp_gantt_chart_current.puml` и не на `current_actualized`)
- [`planning/mvp/versions/v6.27/`](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.27) предыдущая (для `RSCON-2445` уточнена оценка `2d`; backend-последовательность внедрений на `BE3` пересчитана, старт `RSCON-2410` сдвинут на `2026-04-24`)
- [`planning/mvp/versions/v6.26/`](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.26) предыдущая (fact snapshot на `2026-04-17` уточнен по backend-внедрениям: `RSCON-2349`/`RSCON-2410`/`RSCON-2445` назначены на `BE3`, `RSCON-2349` стартовала и оценена в ~15%)
- [`planning/mvp/versions/v6.25/`](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.25) предыдущая (fact snapshot на `2026-04-17` уточнен: `RSCON-2340` оценена в ~85% готовности с прогнозом завершения `2026-04-20`-`2026-04-21`)
- [`planning/mvp/versions/v6.24/`](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.24) предыдущая (fact snapshot на `2026-04-17`; в actualized tracking слое backend-блок скоркарт `RSCON-2342`/`RSCON-2343`/`RSCON-2344` помечен завершенным)
- [`planning/mvp/versions/v6.23/`](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.23) предыдущая (commander baseline + actualized слой со snapshot на `2026-04-10`)
- [`planning/mvp/versions/v6.16/`](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.16) предыдущая (из диаграммы Ганта убраны: `BE_ROLES`, `BE_PKG_PAGE`, `BE_SCD`; последовательность задач сдвинута влево; синхронизированы tasks + gantt)
- [`planning/mvp/versions/v6.15/`](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.15) предыдущая (импорт ProjectLibre `Q2.pod` как источник правды по dev-задачам и оценкам; добавлены AN-задачи 1:1 и QA; Gantt в PlantUML синхронизирован)
- [`planning/mvp/versions/v6.14/`](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.14) предыдущая
- [`planning/mvp/versions/v6.10/`](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.10) предыдущая (убраны "Цепочки" и lineage widget; оставлены created_from sources: автосоздание + preview в формах; Gantt/QA/сводка/порядок задач синхронизированы)
- [`planning/mvp/versions/v6.9/`](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.9) предыдущая (Фаза 1 = весь MVP; QA MVP = 2 недели; Gantt/QA/порядок задач синхронизированы под это)
- [`planning/mvp/versions/v6.8/`](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.8) предыдущая (уточнено: скоркарты не имеют артефактов; добавлены блоки симуляции "Артефакты/Связанные" `FE-SA1`; обновлены формы внедрения по блокам)
- [`planning/mvp/versions/v6.7/`](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.7) предыдущая (из MVP убрана форма пилота; добавлены блоки пилота "Артефакты/Связанные" `AN/BE/FE-PA1` 3+3+3; остальное как v6.6)
- [`planning/mvp/versions/v6.6/`](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.6) предыдущая (добавлена аналитика/UX выбора маршрута согласования в `AN_AP1` (+3 дня); остальное как v6.5)
- [`planning/mvp/versions/v6.5/`](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.5) предыдущая (rescoped: no Initiatives, add Deployments + Chains/Lineage, simulations NOT in approval; уточнены Reject/Recall/Packages)
- [`planning/mvp/versions/v6.4/`](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.4) rescoped (no Initiatives, add Chains/Lineage, simulations NOT in approval)
- [`planning/mvp/versions/v6.3/`](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.3) rescoped (intermediate; included simulations in approval by mistake)
- [`planning/mvp/versions/v6.2/`](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.2) unified snapshot (tasks/gantt aligned + imported docs + prototype link)
- [`planning/mvp/versions/v6.1/`](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.1) aligned to spec v3.1 + gantt v6 (tasks/gantt only)
- [`planning/mvp/versions/v6.0/`](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.0) исходные материалы до выравнивания/перестройки
