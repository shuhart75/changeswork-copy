# Domain Baseline

Этот каталог — каноническая DDD-модель текущей deployed-системы.

## Source of truth
- основной источник: `context/source-materials/current-system/diagrams/raw/spec_domain_model.md`
- дополнительный legacy-контекст: `context/source-materials/current-system/requirements/raw/spec/domain_model.md`

## Structure
- `ubiquitous-language.md` — единый язык
- `bounded-contexts.md` — карта bounded contexts
- `contexts/` — разложение по bounded contexts
- `aggregates/` — агрегаты, инварианты, связи и версия сущностей
- `business-rules.md` — cross-context бизнес-правила
- `state-machines/` — жизненные циклы canonical baseline
