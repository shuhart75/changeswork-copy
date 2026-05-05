# STORY-SIMULATIONS-001

Feature: `features/simulations/feature.md`  
Статус: **импортировано из legacy-плана и materialized для artifacts-related slice**  
Дата обновления: `2026-05-04`

## Summary
Артефакты на detail-странице симуляции

## Description
Зафиксировать planning/story опору для simulation slice `artifacts-related`: аналитическая проработка блока артефактов и frontend-реализация на detail-странице симуляции, с актуальной materialization в `RSCON-2439`.

## Ideal scope
Согласованный блок артефактов симуляции как часть detail composition, без разрыва между shared artifacts backend и host-screen frontend.

## MVP scope
- аналитика по FE-блоку артефактов симуляции;
- frontend-блок артефактов на detail-странице;
- фиксация актуального backlog-follow-up `RSCON-2439`.

## Analyst anchor estimate
- AN: 1 человеко-день
- FE: 3 человеко-дня
- BE: 0 человеко-дней
- QA: 0 человеко-дней
- Total: 4 человеко-дня

## Team estimate
- AN: 1 человеко-день
- FE: 3 человеко-дня
- BE: 0 человеко-дней
- QA: 0 человеко-дней
- Total: 4 человеко-дней

## Agreed estimate
- AN: 1 человеко-день
- FE: 3 человеко-дня
- BE: 0 человеко-дней
- QA: 0 человеко-дней
- Total: 4 человеко-дней

## Actualization state
- `materialized`

## Mapping mode
- `explicit`

## Replaced by implementation tasks
- `RSCON-2439`

## Residual virtual tasks on actual-progress
- none

## Dependencies and assumptions
- story остаётся в рамках existing simulation coverage и не превращает всю feature `simulations` в новую квартальную дельту;
- shared backend артефактов живёт в feature `artifacts`, а здесь фиксируется именно host-screen реализация на стороне simulation.

## Notes for quarter planning
Story добавлена постфактум, чтобы execution-задача `RSCON-2439` появилась в общем `actual-progress` и имела baseline-опору.
