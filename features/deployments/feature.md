# FEATURE-DEPLOYMENTS — Внедрения

Статус: **актуализировано после реализации и SberDocs-boundary**  
Квартал: `2026-Q2`  
Дата обновления: `2026-06-08`

## Цель
Собрать в одной feature MVP-контур для сущности "Внедрение": список, форму, детальную карточку, реализованный жизненный цикл, связанные артефакты и trace через скоркарты.

## Контекст
Feature импортирована из `changesWork`. В legacy-структуре требования и прототипы были распределены по общим frontend/backend документам, отдельным task docs и фактическому backlog в actualized gantt.

После сверки с реализацией и SberDocs-решением feature опирается на:
- единственную таблицу `deployments`, где версии представлены строками с `number`, `version`, `is_last`;
- текущий OpenAPI tag `Deployments`, где список и CRUD используют маршруты `/deployment` / `/deployments`;
- SberDocs integration из `features/approvals` как источник согласования и статуса `ON_APPROVAL`.

## Ideal scope
- полный workspace сущности Deployment;
- отдельные list/form/detail сценарии;
- ЖЦ и read-only связь с SberDocs-согласованием;
- trace и артефакты на детальной и в форме.

## MVP scope
- список внедрений;
- создание/редактирование внедрения;
- детальная страница;
- backend API и lifecycle;
- привязка к SberDocs approval flow и related entities.

## Что исключено из MVP
- расширения beyond MVP, не зафиксированные в current requirement docs;
- локальные действия согласования `approve`/`reject` внутри Deployments;
- `draft-shell`, отдельная таблица `DeploymentVersion` и 9-state lifecycle из старых документов;
- дополнительная аналитика и UI вне текущих legacy-артефактов.

## Входные материалы
- `references.md`
- `planning/MIGRATION_NOTES.md`
- `slices/*/requirements/*.md`
- `slices/*/delivery-prototype/prototype.html`

## Planning stories
- `planning/stories/STORY-DEPLOYMENTS-001.md`
- `planning/stories/STORY-DEPLOYMENTS-002.md`
- `planning/stories/STORY-DEPLOYMENTS-003.md`
- `planning/stories/STORY-DEPLOYMENTS-004.md`
- `planning/stories/STORY-DEPLOYMENTS-005.md`

## Риски и зависимости
- feature зависит от scorecards, artifacts, trace и approval flows;
- `ON_APPROVAL` должен оставаться согласованным с `features/approvals` / SberDocs, а не превращаться в отдельный локальный workflow;
- в legacy-факте часть работ уже была переформулирована в реальные backlog items `RSCON-*`, поэтому planning stories и execution tasks не совпадают 1:1.

## Решение по кварталу
- [x] берём в квартал
- [ ] переносим
- [ ] дробим дополнительно
