# References

## Legacy sources used for import
- `context/source-materials/current-system/requirements/raw/final-spec/REQ_deployments_frontend.md`
- `context/source-materials/current-system/requirements/raw/final-spec/REQ_deployments_backend.md`
- `context/source-materials/current-system/prototypes/raw/deployments.html`
- `context/source-materials/current-system/requirements/raw/final-spec/REQ_deployments_list_frontend.md`
- `context/source-materials/current-system/requirements/raw/final-spec/REQ_deployments_form_frontend.md`
- `context/source-materials/current-system/requirements/raw/final-spec/REQ_deployments_detail_frontend.md`
- `context/source-materials/current-system/requirements/raw/final-spec/REQ_deployments_backend_db_api.md`
- `context/source-materials/current-system/requirements/raw/final-spec/REQ_deployments_backend_lifecycle.md`

## Additional source folders
- `context/source-materials/current-system/requirements/raw/`
- `context/source-materials/current-system/prototypes/raw/`
- `context/source-materials/current-system/diagrams/raw/`

## Current implementation evidence
- `/home/reutov/Downloads/Telegram Desktop/rscon-api.yaml` — OpenAPI tag `Deployments`, источник текущих маршрутов и DTO.
- `/home/reutov/Downloads/Telegram Desktop/111.xlsx` — модель данных, таблица `deployments`.
- `/home/reutov/Downloads/Telegram Desktop/2026-05-13-deployment-state-machine-summary.md` — реализованная state machine, сверенная с текущими требованиями.
- `features/approvals/requirements.md` — SberDocs integration как источник согласования, статусов и истории для состояния `ON_APPROVAL`.

## Reviewed incoming package

Папка `/home/reutov/Downloads/coda_docs` содержит path-coded документы `features_deployments_*`, полученные 2026-06-08. Они просмотрены как входная порция, но не скопированы поверх текущих requirements, потому что часть пакета датирована 2026-05-21 и противоречит уже принятому состоянию:

- `coda-docs_features_deployments_requirements.md` — содержит старые `draft-shell`, 9-state lifecycle, локальные `approve`/`reject`, поэтому не является текущим source of truth.
- `coda-docs_features_deployments_domain-impact.md` — содержит старые решения `DEC-2026-05-12/21-DEPLOYMENTS-*`, superseded текущими `DEC-2026-05-22-DEPLOYMENTS-*` и `DEC-2026-06-08-DEPLOYMENTS-SBERDOCS-006`.
- `coda-docs_features_deployments_planning_*`, `coda-docs_features_deployments_slices_db-api_execution_*`, `coda_docs_features_deployments_planning_scope_prototype_prototype.html` — относятся к planning, execution-update или prototype режимам и не применялись в активном requirements mode.
