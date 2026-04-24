# FEATURE-DEPLOYMENTS — Внедрения

Статус: **импортировано из legacy-проекта**  
Квартал: `2026-Q2`  
Дата обновления: `2026-04-23`

## Цель
Собрать в одной feature MVP-контур для сущности "Внедрение": список, форму, деталку, жизненный цикл, связанные артефакты и связанный trace через скоркарты.

## Контекст
Feature импортирована из `changesWork`. В legacy-структуре требования и прототипы были распределены по общим frontend/backend документам, отдельным task docs и фактическому backlog в actualized gantt.

## Ideal scope
- полный workspace сущности Deployment;
- отдельные list/form/detail сценарии;
- ЖЦ и approval-интеграция;
- trace и артефакты на детальной и в форме.

## MVP scope
- список внедрений;
- создание/редактирование внедрения;
- детальная страница;
- backend API и lifecycle;
- привязка к approval flow и related entities.

## Что исключено из MVP
- расширения beyond MVP, не зафиксированные в current requirement docs;
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
- в legacy-факте часть работ уже была переформулирована в реальные backlog items `RSCON-*`, поэтому planning stories и execution tasks не совпадают 1:1.

## Решение по кварталу
- [x] берём в квартал
- [ ] переносим
- [ ] дробим дополнительно
