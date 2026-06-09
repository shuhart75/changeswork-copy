# STORY-APPROVALS-001

Feature: `features/approvals/feature.md`  
Статус: **импортировано из legacy-плана**  
Дата обновления: `2026-04-23`

## Summary
Approval core и интеграция с жизненными циклами

## Description
Реализовать backend-основу процесса согласования и утверждения: `ApprovalChain`, этапы, назначения, решения, recall/reject, а также интеграционные обработчики, которые корректно переводят версии Pilot и Deployment по результатам approval/ratification.

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
- `materialized`

## Mapping mode
- `explicit`

## Replaced by implementation tasks
- `RSCON-2629`
- `RSCON-2630`
- `RSCON-2631`
- `RSCON-2633`
- `RSCON-2634`
- `RSCON-2635`
- `RSCON-2649`

## Residual virtual tasks on actual-progress
- none

## Dependencies and assumptions
- требуется доступная ролевая модель approver/ratifier;
- статусы Pilot/Deployment уже определены в доменной модели и lifecycle docs.

## Notes for quarter planning
На actual-progress 2026-06-08 story закрывается реальными задачами SberDocs integration scope; прежние virtual chunks удалены из execution registry.
