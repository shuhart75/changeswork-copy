# Оценки planning stories

Feature: `features/simulations/feature.md`  
Квартал: `2026-Q2`

Эта feature по-прежнему отражает mostly existing baseline coverage, но для `artifacts-related` slice и конфигурации пилотов добавлена planning-story опора, чтобы связать execution-факт с baseline.

Формат ролевых оценок: `AN / FE / BE / QA`.

| Story ID | Summary | Analyst anchor, дн | Team estimate, дн | Agreed estimate, дн | Agreed total, дн | Notes |
|---|---|---|---|---|---:|---|
| STORY-SIMULATIONS-001 | Артефакты на detail-странице симуляции | `1 / 3 / 0 / 0` | `1 / 3 / 0 / 0` | `1 / 3 / 0 / 0` | 4 | Legacy `AN_FE_SIM_ART` + `FE_SIM_ART`; actualized через `RSCON-2439` |
| STORY-SIMULATIONS-002 | Конфигурация пилотов | `1 / 4 / 12 / 10` | `1 / 4 / 12 / 10` | `1 / 4 / 12 / 10` | 27 | Execution layer импортирован из входящего actual-progress snapshot; оценки отражают текущие task estimates без изменения commander baseline |
