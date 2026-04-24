# STORY-SCORECARDS-002

Feature: `features/scorecards/feature.md`  
Статус: **импортировано из legacy-плана**  
Дата обновления: `2026-04-23`

## Summary
Workspace скоркарты: вкладка, деталка, источники и использование

## Description
Собрать пользовательский workspace скоркарты без отдельной list page: вкладку со скоркартами в доменном контексте, деталку скоркарты и блоки `Источники формирования` / `Используется в`.

## Ideal scope
Полноценный scorecards workspace с отдельным роутом списка, деталкой, источниками, использованием и переходами в связанные сущности.

## MVP scope
- вкладка/entry point для скоркарт в доменном workspace;
- деталка скоркарты;
- блоки источников и использования;
- переходы к связанным сущностям.

## Analyst anchor estimate
- 12 человеко-дней

## Team estimate
- 12 человеко-дней

## Agreed estimate
- 12 человеко-дней

## Actualization state
- `materialized`

## Mapping mode
- `inferred`

## Replaced by implementation tasks
- `RSCON-2339`
- `RSCON-2340`

## Residual virtual tasks on actual-progress
- none

## Dependencies and assumptions
- зависит от готового backend foundation по скоркартам;
- отдельная page/list скоркарт не входит в MVP и не должна возвращаться в scope этой story.

## Notes for quarter planning
Story объединяет legacy detail-поток и фактический workspace backlog, потому что текущие Jira-задачи описывают работу через вкладку скоркарт, а не через отдельную страницу списка.
