# Context — Scorecard Templates

## Purpose
Поддержка versioned-шаблонов, из которых создаются скоркарты и вычисляется критичность.

## Main objects
- `ScorecardTemplate`
- `ScorecardTemplateVersion`

## Key rules
- Каждая версия шаблона привязана к продукту и имеет период действия.
- `default_config` хранит:
  - структуру полей;
  - значения по умолчанию;
  - `criticality_thresholds`.
- В MVP у каждого продукта есть своя версия шаблона, даже если содержимое фактически совпадает.
