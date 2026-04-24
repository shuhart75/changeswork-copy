# Aggregate — Package

## Purpose
Операционная группировка нескольких `ApprovalInstance` для совместного ratification.

## Contains
- 2..* связанных `ApprovalInstance`
- brief пакета

## Invariants
- создаётся только из `awaiting_ratification`;
- minimum size = 2;
- не имеет собственного `ApprovalInstance`;
- не имеет собственных полей `status`, `name`, `description`, `ratifier_id`;
- может объединять элементы разных initiatives и, для `methodologist`, разных продуктов;
- перестаёт существовать как активная группировка, когда активных элементов становится меньше 2.
