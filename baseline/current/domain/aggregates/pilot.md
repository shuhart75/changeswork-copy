# Aggregate — Pilot

## Purpose
Контролируемый реальный эксперимент с версионированием через `PilotVersion`.

## Versioning
- `Pilot` — логическая сущность.
- Изменения выполняются через новую `PilotVersion`.
- В каждый момент времени есть только одна current version.

## Invariants
- принадлежит одной `Initiative`;
- каждая версия связана минимум с одной `ScorecardVersion`;
- `pilot_group_size + control_group_size > 0`;
- активную или согласуемую версию нельзя удалять.

## Status model for `PilotVersion`
- `draft`
- `requires_activation`
- `in_approval`
- `approved`
- `awaiting_ratification`
- `in_ratification`
- `ratified`
- `active`
- `completed`
- `approval_rejected`
- `ratification_rejected`
- `approval_cancelled`
- `ratification_cancelled`
- `inactive`
- `archived`
