# Final Domain Delta — RSCON-2438

Дата обновления: `2026-04-23`
Target baseline: `baseline/current/domain/`

## Changed bounded contexts
- `Scorecards`
- `Research and Execution`
- `Packages`
- `Approval`

## Added or changed aggregates
- Уточнение `Scorecard` как самостоятельного агрегата со status model `active/archive`.
- Уточнение `Deployment` для `simulation_based` lineage.
- Уточнение `Package` как группировки `ApprovalInstance`, а не самостоятельного approval target.

## Changed invariants and business rules
- `Scorecard` не имеет собственного approval flow.
- `Package` не имеет собственного lifecycle enum.
- `methodologist` имеет доменное исключение для mixed-product package.

## Files promoted to baseline
- `baseline/current/domain/*`
