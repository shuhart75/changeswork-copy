# FEATURE-APPROVALS — Согласования

Статус: **импортировано из legacy-проекта**  
Квартал: `2026-Q2`  
Дата обновления: `2026-04-23`

## Цель
Собрать в одной feature процесс согласования и утверждения, а также UI страницы "Согласования" для назначенных участников процесса.

## Контекст
Feature импортирована из `changesWork`. В legacy-материалах логика процесса и UI страницы были описаны отдельными task-документами и requirement packs.

## Ideal scope
- единый backend-процесс approval/ratification;
- интеграция с жизненными циклами Pilot и Deployment;
- страница "Согласования" с отдельными и пакетными сценариями;
- история решений и комментариев по item и package.

## MVP scope
- core backend процесса approval/ratification;
- интеграция с жизненными циклами Pilot/Deployment;
- approvals page для individual и package ratification сценариев.

## Что исключено из MVP
- развитие поиска и сортировки сверх описанного в requirement docs;
- расширенные пользовательские фильтры и доп. пользовательские представления.

## Входные материалы
- `references.md`
- `planning/MIGRATION_NOTES.md`
- `slices/core-process/requirements/backend.md`
- `slices/page/requirements/frontend.md`
- `slices/page/requirements/backend.md`

## Planning stories
- `planning/stories/STORY-APPROVALS-001.md`
- `planning/stories/STORY-APPROVALS-002.md`

## Риски и зависимости
- feature зависит от согласованной ролевой модели и жизненных циклов Pilot/Deployment;
- package-сценарии частично пересекаются с feature `packages` и требуют аккуратной границы ответственности.

## Решение по кварталу
- [x] берём в квартал
- [ ] переносим
- [ ] дробим дополнительно
