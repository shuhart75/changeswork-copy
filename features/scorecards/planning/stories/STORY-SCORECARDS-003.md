# STORY-SCORECARDS-003

Feature: `features/scorecards/feature.md`  
Статус: **импортировано из legacy-плана**  
Дата обновления: `2026-04-23`

## Summary
Создание, редактирование и привязка скоркарты

## Description
Реализовать create/edit flow скоркарты, автоформирование имени, загрузку шаблона, расчёт критичности и сценарии привязки существующей скоркарты к `Pilot` или `Deployment`.

## Ideal scope
Полноценный create/edit workflow скоркарты и lookup/select существующих скоркарт во всех доменных формах, где это допускает предметная область.

## MVP scope
- ручное создание скоркарты;
- редактирование с выпуском новой версии;
- привязка существующей скоркарты;
- предупреждения о выпуске новых версий доменных элементов;
- соблюдение ограничений по mandatory lineage-scorecard.

## Analyst anchor estimate
- 17 человеко-дней

## Team estimate
- 17 человеко-дней

## Agreed estimate
- 17 человеко-дней

## Actualization state
- `materialized`

## Mapping mode
- `inferred`

## Replaced by implementation tasks
- `RSCON-2340`
- `RSCON-2341`
- `RSCON-2344`

## Residual virtual tasks on actual-progress
- none

## Dependencies and assumptions
- зависит от backend foundation и шаблонов;
- часть scope затрагивает формы `Pilot` и `Deployment`, поэтому нужен аккуратный контроль продуктового контекста и правил versioning.

## Notes for quarter planning
Story агрегирует legacy create/edit поток `AN_SCF_BE`, `BE_SCF`, `AN_SCF_FE`, `FE_SCF`; в фактическом backlog часть этой работы разложена на `RSCON-2340`, `RSCON-2341`, `RSCON-2344`.
