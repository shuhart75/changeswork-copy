# STORY-APPROVALS-002

Feature: `features/approvals/feature.md`  
Статус: **импортировано из legacy-плана**  
Дата обновления: `2026-04-23`

## Summary
Страница "Согласования"

## Description
Сделать пользовательскую страницу для назначений на approval и ratification: вкладки, карточки individual/package, batch-операции, комментарии, историю решений и открытие подробного контекста элемента.

## Ideal scope
Единая approvals page со всеми основными сценариями ratification, package-логикой и удобным просмотром истории/комментариев по item.

## MVP scope
- вкладки Approval и Ratification;
- отдельные карточки и пакетные карточки;
- batch approve/reject/ratify в пределах допущений MVP;
- комментарии и деталка элемента/пакета.

## Analyst anchor estimate
- AN: 2 человеко-дней
- FE: 10 человеко-дней
- BE: 10 человеко-дней
- QA: 0 человеко-дней
- Total: 22 человеко-дней

## Team estimate
- AN: 2 человеко-дней
- FE: 10 человеко-дней
- BE: 10 человеко-дней
- QA: 0 человеко-дней
- Total: 22 человеко-дней

## Agreed estimate
- AN: 2 человеко-дней
- FE: 10 человеко-дней
- BE: 10 человеко-дней
- QA: 0 человеко-дней
- Total: 22 человеко-дней

## Actualization state
- `materialized`

## Mapping mode
- `explicit`

## Replaced by implementation tasks
- `RSCON-2636`
- `QA-APPROVALS-CARD`
- `RSCON-2637`
- `QA-APPROVALS-EMAIL-PREVIEW`

## Residual virtual tasks on actual-progress
- none

## Dependencies and assumptions
- зависит от готового approval core;
- package flow исключён из MVP текущего квартала и не является зависимостью этой story.
- actual-progress FE/QA слой стартует после backend scope `STORY-APPROVALS-001`.

## Notes for quarter planning
На actual-progress 2026-06-08 story закрывается реальными FE/QA задачами по карточке новой сущности, экшенам и Email preview; прежние virtual chunks удалены из execution registry.
