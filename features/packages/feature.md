# FEATURE-PACKAGES — Пакеты

Статус: **исключено из MVP**  
Квартал: `2026-Q2`  
Дата обновления: `2026-06-09`

## Цель

Зафиксировать, что локальный package flow больше не входит в MVP после решения `DEC-2026-05-25-APPROVALS-SBERDOCS-001` о переносе согласований/утверждений в SberDocs.

## Контекст

Feature была импортирована из `changesWork` как страница для пакетирования элементов в `awaiting_ratification`. Новая реализация не использует локальные `ApprovalInstance` и package queue: АС КОДА отправляет документ/маршрут в SberDocs и читает статус/историю оттуда.

## Ideal scope

- Не актуален для текущего MVP.
- Если позднее потребуется групповая отправка нескольких сущностей в SberDocs, нужен отдельный intake и новый scope.

## MVP scope

- package page не реализуется;
- package API не реализуется;
- package brief не реализуется;
- package prototypes считаются obsolete.

## Что исключено из MVP

- маршрут `/packages`;
- очередь элементов `awaiting_ratification`;
- локальное формирование пакета;
- `POST /api/v1/packages` и package actions;
- блок `Мои пакеты` и read-only деталка пакета;
- package cards на странице `Согласования`.

## Входные материалы

- `references.md`
- `requirements.md`
- `slices/page/requirements/frontend.md`
- `slices/page/requirements/backend.md`

## Planning stories

- `planning/stories/STORY-PACKAGES-001.md` — отменена для `2026-Q2` и оставлена только как legacy trace.

## Риски и зависимости

- baseline и прототипы требуют отдельной синхронизации;
- возврат package flow возможен только отдельным решением после оценки SberDocs coverage.

## Решение по кварталу

- [ ] берём в квартал
- [x] переносим / исключаем из MVP
- [ ] дробим дополнительно
