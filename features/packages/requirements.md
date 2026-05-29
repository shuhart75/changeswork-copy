# Требования по feature — Пакеты

Статус: **исключено из MVP**
Feature: `features/packages/feature.md`
Квартал: `2026-Q2`
Дата обновления: `2026-05-25`
Шаблон: `.workflow/templates/requirements/feature-requirements.template.md`
Decision ID: `DEC-2026-05-25-APPROVALS-SBERDOCS-001`

## Общий контур feature

- Ранее feature описывала страницу `Пакеты` и пакетирование элементов в `awaiting_ratification`.
- По новому решению approval/ratification выполняется в SberDocs, а АС КОДА не реализует собственные package flow, package page и batch decisions.
- Для минимизации разработки feature `packages` не входит в MVP и не должна создавать frontend/backend задачи без отдельного mode switch и пересмотра scope.

## Superseded scope

Отменены для MVP:

- очередь элементов `awaiting_ratification`;
- локальное формирование пакета;
- brief пакета;
- `POST /api/v1/packages`;
- `POST /api/v1/packages/{id}/action`;
- блок `Мои пакеты`;
- read-only деталка пакета;
- пакетные карточки на странице `Согласования`.

## Новый источник процесса

- Маршрут и бриф задаются на host screen согласуемой сущности.
- Документ, маршрут и вложения передаются в SberDocs.
- Статус и история читаются из SberDocs API.
- Если бизнесу позже понадобится групповая отправка нескольких сущностей, это новая feature/intake, а не часть текущего MVP.

## Критерии приемки отмены

1. В требованиях MVP нет page/API для package workflow.
2. Никакие элементы не переводятся в `awaiting_ratification` ради пакетирования в АС КОДА.
3. Старые package prototypes помечены как obsolete в `features/approvals/domain-impact.md` и `features/packages/domain-impact.md`.
4. Planning/estimates требуют отдельной синхронизации вне текущего requirements-mode изменения.
