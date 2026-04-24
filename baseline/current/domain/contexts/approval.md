# Context — Approval

## Purpose
Динамический процесс согласования и утверждения версий пилотов и внедрений.

## Main objects
- `ApprovalInstance`
- approval stages
- ratification stage
- assignments and process snapshot

## Key rules
- Маршрут согласования не предзадан и собирается при submit.
- Approval-этапов может быть 0..*.
- Ratification-этап ровно один и обязателен.
- Approvers работают параллельно внутри этапа; этапы идут последовательно.
- `auto_ratification=true` отправляет версию напрямую в индивидуальный ratification после approval.
- `auto_ratification=false` переводит версию в `awaiting_ratification`, откуда можно стартовать индивидуальный ratification или собрать package.
- Recall допустим и на approval, и на ratification.
