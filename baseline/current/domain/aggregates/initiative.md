# Aggregate — Initiative

## Purpose
Корневой агрегат, группирующий workstream стратегического изменения.

## Contains
- `Simulation` (0..*)
- `Pilot` (0..*)
- `Deployment` (0..*)
- артефакты (0..*)

## Invariants
- принадлежит одному `Product`;
- имя уникально в рамках продукта;
- может быть связано с несколькими `SubProduct`, а при их отсутствии покрывает весь продукт;
- `archived` запрещён при наличии `deployed` внедрений или неархивированных вложенных сущностей.

## Status model
- `draft`
- `active`
- `deployed`
- `archived`
