# Actualization map

Feature: `features/simulations/feature.md`
Quarter: `2026-Q2`
Baseline: `commander-plan`

## Правила
- Основная часть `simulations` по-прежнему отражает imported existing coverage.
- Для slice `artifacts-related` добавляем точечную story map, чтобы `RSCON-2439` и `RSCON-2490` были видны в общем `actual-progress`.
- Для конфигурации пилотов добавляем фактический execution layer из входящего actual-progress snapshot без расширения requirements-слоя в режиме `execution-update`.

## Mapping

| Story ID | Summary | Baseline Start | Baseline Duration (дн) | Actualization State | Mapping Mode | Replaced By | Residual Virtual Tasks | Depends On |
|---|---|---|---:|---|---|---|---|---|
| STORY-SIMULATIONS-001 | Артефакты на detail-странице симуляции | 2026-03-19 | 6 | materialized | explicit | RSCON-2439, RSCON-2490 |  |  |
| STORY-SIMULATIONS-002 | Конфигурация пилотов | 2026-05-12 | 28 | mixed | inferred | RSCON-2473, RSCON-2501 | RSCON-2472, RSCON-2474, RSCON-2475, RSCON-2471, RSCON-2488, QA_SIM_CONFIG |  |
