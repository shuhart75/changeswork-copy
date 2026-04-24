# STORY-DEPLOYMENTS-002

Feature: `features/deployments/feature.md`  
Статус: **импортировано из legacy-плана**  
Дата обновления: `2026-04-23`

## Summary
Жизненный цикл внедрений

## Description
Описать и реализовать lifecycle `DeploymentVersion`: переходы между draft, approval, approved, deployed и rollback/reject сценариями, включая интеграцию с approval flow.

## Ideal scope
Цельный и непротиворечивый lifecycle внедрения с поддержкой resubmit, deploy и rollback.

## MVP scope
- основные статусы и переходы;
- submit/deploy/rollback;
- reject и recall сценарии в связке с approval.

## Analyst anchor estimate
- 6 человеко-дней

## Team estimate
- 6 человеко-дней

## Agreed estimate
- 6 человеко-дней

## Actualization state
- `materialized`

## Mapping mode
- `explicit`

## Replaced by implementation tasks
- `RSCON-2410`

## Residual virtual tasks on actual-progress
- none

## Dependencies and assumptions
- зависит от backend foundation и approval flow.

## Notes for quarter planning
Импортировано из `AN_DEP_LC` и `BE_DEP_LC`.
