# Aggregate — Simulation

## Purpose
Анализ исторических данных и генерация результатов для гипотез и частичного предзаполнения скоркарт.

## Invariants
- принадлежит одной `Initiative`;
- период данных валиден (`from < to`);
- не изменяется после завершения;
- может быть источником `ScorecardSource`.

## Status model
- `draft`
- `running`
- `completed`
- `failed`
