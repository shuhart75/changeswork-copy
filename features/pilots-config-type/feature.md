# FEATURE-PILOTS-CONFIG-TYPE — Типизация конфигов пилотов

Статус: **draft**  
Квартал: `2026-Q2`  
Дата обновления: `2026-06-08`

## Цель
Добавить к пилоту/эксперименту тип процесса `processType`, чтобы пользователь мог явно задать контур `online`, `offline` или `online+offline`, а API возвращало это значение потребителям конфигураций.

## Контекст
Входящий пакет из `/home/reutov/Downloads/coda_docs` описывает отдельную дельту `pilots-config-type`. В пользовательском интерфейсе сущность называется "пилот", но внутренняя модель и OpenAPI текущей системы используют термин "эксперимент" и таблицу `experiments`.

## MVP scope
- обязательное поле `processType` в форме создания/редактирования пилота;
- отображение типа процесса в деталке пилота;
- хранение значения в `experiments.process_type`;
- возврат значения во внутренних experiment endpoints;
- backfill существующих записей значением `online`.

## Что исключено из MVP
- изменение жизненного цикла пилота;
- новая ролевая модель;
- импорт planning, execution и prototype артефактов из входящей папки без переключения режима.

## Входные материалы
- `/home/reutov/Downloads/coda_docs/coda-docs_features_pilots-config-type_requirements.md`
- `/home/reutov/Downloads/coda_docs/coda_docs_features_pilots_config_type_slices_config_requirements.md`
- `/home/reutov/Downloads/coda_docs/coda-docs_features_pilots-config-type_domain-impact.md`
- `/home/reutov/Downloads/coda_docs/coda-docs_features_pilots_requirements.md`
- `/home/reutov/Downloads/coda_docs/coda-docs_features_pilots_domain-impact.md`

## Planning stories
- `planning/stories/STORY-PILOTS-CONFIG-001.md` во входящем пакете не импортирован в repo: текущий режим `requirements`.

## Риски и зависимости
- Уточнение от 2026-06-08 снимает противоречие входящих документов: фильтрует Config Service, только в `/api/v3/config`; `/api/v2/config` не расширяется.
- Требуется синхронизация с внешним API `/api/v3/config` и baseline в отдельных режимах.
