# FEATURE-PACKAGES — Пакеты

Статус: **импортировано из legacy-проекта**  
Квартал: `2026-Q2`  
Дата обновления: `2026-04-23`

## Цель
Собрать в одной feature MVP-сценарий пакетирования элементов в `awaiting_ratification`: очередь, локальный выбор элементов, бриф пакета, список отправленных пакетов и просмотр деталки пакета.

## Контекст
Feature импортирована из `changesWork`. В legacy-материалах исходный scope страницы был шире, чем текущий MVP: там были отдельные вкладки для in-progress, rejected и history, а также дополнительные batch-сценарии. В новой структуре зафиксирован именно актуальный MVP из текущих requirement packs.

## Ideal scope
- единая страница `Пакеты` как workspace для пакетирования и аудита;
- полная цепочка queue -> brief -> package -> read-only detail;
- согласованность со страницей `Согласования` и approval core;
- расширенные bucket/view-сценарии для in-progress, rejected и history.

## MVP scope
- маршрут `/packages`;
- очередь элементов в `awaiting_ratification`;
- локальное формирование пакета без backend draft;
- brief пакета и отправка через `POST /api/v1/packages`;
- блок `Мои пакеты` и read-only деталка пакета.

## Что исключено из MVP
- backend draft пакетов;
- редактирование уже созданного пакета;
- выбор `ratifier` на странице `Пакеты`;
- поиск, сортировка, расширенные фильтры и отдельная history page;
- recall и package actions вне уже зафиксированных approval flows.

## Входные материалы
- `references.md`
- `planning/MIGRATION_NOTES.md`
- `slices/page/requirements/frontend.md`
- `slices/page/requirements/backend.md`
- `slices/page/delivery-prototype/prototype.html`

## Planning stories
- `planning/stories/STORY-PACKAGES-001.md`

## Риски и зависимости
- feature зависит от `approvals` и от готового approval core, потому что очередь и пакетный контекст строятся вокруг `ApprovalInstance`;
- в `changesWork` исходный scope был шире текущего MVP, поэтому при обсуждении с заказчиками важно не возвращать legacy-вкладки обратно без отдельного решения по кварталу;
- execution-слой пока живёт virtual-задачами, без прямых Jira-ключей.

## Решение по кварталу
- [x] берём в квартал
- [ ] переносим
- [ ] дробим дополнительно
