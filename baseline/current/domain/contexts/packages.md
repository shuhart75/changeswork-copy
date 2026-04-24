# Context — Packages

## Purpose
Групповое утверждение нескольких `ApprovalInstance`, уже находящихся в очереди `awaiting_ratification`.

## Main objects
- `Package`

## Key rules
- Package создаётся только вручную и сразу считается отправленным.
- Package не имеет собственного status enum.
- Package не является самостоятельным approval target.
- Активный состав определяется по `approval_instance.package_id`.
- Пакет должен содержать минимум 2 элемента.
- Решения принимаются по связанным `ApprovalInstance`, не по пакету как объекту.
