# STORY-APPROVALS-001

Feature: `features/approvals/feature.md`  
Статус: **импортировано из legacy-плана**  
Дата обновления: `2026-04-23`

## Summary
Approval core и интеграция с жизненными циклами

## Description
Реализовать backend-основу процесса согласования и утверждения: `ApprovalInstance`, этапы, назначения, решения, recall/reject, а также интеграционные обработчики, которые корректно переводят версии Pilot и Deployment по результатам approval/ratification.

## Ideal scope
Полный MVP-поток approval/ratification с per-item решениями, package-сценариями и сохранением истории решений для дальнейшего UI-отображения.

## MVP scope
- core backend approval/ratification;
- recall/reject/resubmit;
- интеграция с ЖЦ Pilot/Deployment;
- поддержка `auto_ratification` и `awaiting_ratification`.

## Analyst anchor estimate
- AN: 3 человеко-дней
- FE: 0 человеко-дней
- BE: 15 человеко-дней
- QA: 0 человеко-дней
- Total: 18 человеко-дней

## Team estimate
- AN: 3 человеко-дней
- FE: 0 человеко-дней
- BE: 15 человеко-дней
- QA: 0 человеко-дней
- Total: 18 человеко-дней

## Agreed estimate
- AN: 3 человеко-дней
- FE: 0 человеко-дней
- BE: 15 человеко-дней
- QA: 0 человеко-дней
- Total: 18 человеко-дней

## Actualization state
- `virtual`

## Mapping mode
- `explicit`

## Replaced by implementation tasks
- none yet

## Residual virtual tasks on actual-progress
- none

## Dependencies and assumptions
- требуется доступная ролевая модель approver/ratifier;
- статусы Pilot/Deployment уже определены в доменной модели и lifecycle docs.

## Notes for quarter planning
Импортировано из legacy-комбинации `AN_AP_CORE`, `BE_AP_CORE`, `AN_PILOT_LC_AP`, `BE_PILOT_LC_AP`.
