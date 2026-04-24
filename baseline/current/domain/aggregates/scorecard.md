# Aggregate — Scorecard

## Purpose
Самостоятельный агрегат конфигурации и финансовых эффектов, используемый доменными версиями `Pilot` и `Deployment`.

## Contains
- `ScorecardVersion` (1..*)
- `ScorecardSource` (0..*)
- usage links to `PilotVersion` / `DeploymentVersion`

## Invariants
- создаётся из `ScorecardTemplateVersion`;
- каждая новая редакция создаёт новую `ScorecardVersion`;
- если `is_manual = false`, должен быть хотя бы один источник `simulation`;
- статус определяется только связями использования, а не approval-процессом;
- изменение самой скоркарты перевыпускает все связанные доменные версии;
- изменение binding-связей допустимо только из контекста доменной сущности.

## Status model
- `active`
- `archive`
