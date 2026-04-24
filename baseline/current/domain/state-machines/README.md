# State Machines

Canonical source: `context/source-materials/current-system/diagrams/raw/spec_domain_model.md`
Supporting diagrams: `context/source-materials/current-system/diagrams/raw/spec_state_machine.puml`

## Initiative
- `draft -> active -> deployed -> archived`
- `archived` допустим только при отсутствии deployed внедрений и активных вложенных сущностей.

## Simulation
- `draft -> running -> completed|failed`

## PilotVersion
- `draft -> requires_activation -> in_approval|awaiting_ratification|in_ratification`
- terminal/secondary states: `approved`, `ratified`, `active`, `completed`, `inactive`, `archived`, `approval_rejected`, `ratification_rejected`, `approval_cancelled`, `ratification_cancelled`

## DeploymentVersion
- `draft -> in_approval|awaiting_ratification|in_ratification`
- post-ratification: `ratified -> deployed -> rolled_back -> archived`
- rejection/cancel states: `approval_rejected`, `ratification_rejected`, `approval_cancelled`, `ratification_cancelled`

## Scorecard
- `active -> archive`
- переход в `archive` происходит при потере последней связи использования.

## Package
- отдельного lifecycle enum нет;
- активность определяется числом связанных `ApprovalInstance` в группе.
