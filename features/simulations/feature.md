# FEATURE-SIMULATIONS — Симуляции

Статус: **импортировано как existing baseline coverage**  
Квартал: `2026-Q2`  
Дата обновления: `2026-04-24`

## Цель
Собрать в отдельной feature уже существующий контур симуляций, чтобы simulation scope был виден не только в `baseline/current/`, но и в `features/` как нормализованный legacy-workspace с понятными slices и ссылками на источники.

## Контекст
В legacy `changesWork` симуляции были описаны отдельными task docs и использовались как уже существующий функционал, который в рамках MVP v6.5+ не переписывали. Эта feature не вводит новую квартальную дельту, а фиксирует existing coverage в структуре harness.

## Ideal scope
- полный нормализованный workspace симуляций со списком, формой, деталкой, lifecycle и связанными сущностями;
- единая карта UI/API/data для simulation scope;
- явная связь с `scorecards`, `pilots`, `deployments`, `artifacts` и `simulation-bt-agent` как будущей дельтой.

## MVP scope
- нормализовать existing coverage по simulation scope в виде отдельной feature;
- разложить legacy-материалы по slices `list`, `detail`, `form`, `lifecycle`, `artifacts-related`;
- сохранить traceability на исходные legacy task docs и baseline summaries.

## Что исключено из MVP
- новая разработка simulation scope;
- перепроектирование текущего UI/API симуляций;
- искусственное натягивание simulation scope на квартальный planning как новой дельты;
- AI-agent сценарий формирования БТ, который живёт отдельно в `features/simulation-bt-agent/`.

## Входные материалы
- `references.md`
- `planning/MIGRATION_NOTES.md`
- `slices/*/requirements/*.md`
- `baseline/current/ui/simulations.md`
- `baseline/current/api/simulations.md`

## Planning stories
- Для этой feature в текущем виде planning stories не поднимались: это normalization of existing coverage, а не новая квартальная дельта.

## Риски и зависимости
- legacy simulation docs частично используют старый URI-стиль `/api/simulations/...`, который не до конца выровнен с `v1`-контрактами;
- simulation scope связан со `scorecards`, а через них — с `pilots` и `deployments`, поэтому при изменениях легко появляются cross-feature эффекты;
- future feature `simulation-bt-agent` зависит от simulation detail page как host screen, но не должна размывать текущий existing scope.

## Решение по кварталу
- [x] existing coverage зафиксирован
- [ ] берём как новую квартальную дельту
- [ ] переносим
