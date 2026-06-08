# References — Типизация конфигов пилотов

Feature: `features/pilots-config-type/feature.md`  
Дата обновления: `2026-06-08`

## Источники требований

### Входящая папка
- `/home/reutov/Downloads/coda_docs/coda-docs_features_pilots-config-type_requirements.md`
- `/home/reutov/Downloads/coda_docs/coda_docs_features_pilots_config_type_slices_config_requirements.md`
- `/home/reutov/Downloads/coda_docs/coda-docs_features_pilots-config-type_slices_config_slice.md`
- `/home/reutov/Downloads/coda_docs/coda-docs_features_pilots-config-type_domain-impact.md`
- `/home/reutov/Downloads/coda_docs/coda-docs_features_pilots-config-type_references.md`
- `/home/reutov/Downloads/coda_docs/coda-docs_features_pilots_requirements.md`
- `/home/reutov/Downloads/coda_docs/coda-docs_features_pilots_domain-impact.md`

### Связанные repo-артефакты
- `features/pilots/requirements.md`
- `features/pilots/slices/workspace/requirements/frontend.md`
- `features/pilots/slices/workspace/requirements/backend.md`
- `features/pilots/domain-impact.md`

## Контрактные источники
- `context/source-materials/current-system/requirements/raw/docs/coda_api.yaml` — заявлен входящими материалами как OpenAPI внутреннего API; в текущем repo файл не найден и требует отдельного внесения/проверки.
- `context/source-materials/current-system/requirements/raw/docs/vneshneye_api_polucheniya_konfiguratsii_eksperimentov.3.1.1.yml` — заявлен входящими материалами как внешний API конфигураций; в текущем repo файл не найден и требует отдельного внесения/проверки.

## Классификация входящих файлов
- Requirements/domain-impact/reference файлы актуализированы в текущем режиме.
- Planning, execution и delivery-prototype файлы из входящей папки не импортированы, потому что текущий active mode — `requirements`.

## Примечания
- Внутренняя модель использует `experiments` и поле `process_type`.
- Пользовательское представление на фронте остаётся "Пилоты".
