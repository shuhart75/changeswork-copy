# Business Rules

Дата обновления: `2026-04-23`
Canonical source: `context/source-materials/current-system/diagrams/raw/spec_domain_model.md`

## BR-1 Initiative lifecycle
- Статус инициативы вычисляется автоматически из вложенных сущностей.
- Архивирование не каскадирует архивирование вложенных сущностей.
- Архивирование запрещено при наличии deployed внедрения или неархивированных вложенных сущностей.

## BR-2 Simulation execution
- Симуляция стартует только из `draft`.
- Выполняющаяся симуляция не редактируется.
- Завершённая симуляция immutable.

## BR-3 Scorecard management
- Скоркарта создаётся только из контекста `Pilot` или `Deployment`.
- Критичность считает фронт по шаблону и передаёт в `ScorecardVersion`.
- Новая версия скоркарты перевыпускает все связанные доменные версии.
- Изменение binding-связей выполняется только из `Pilot`/`Deployment` контекста.
- Скоркарта не имеет собственного approval flow.

## BR-4 Pilot approval
- `PilotVersion` отправляется в процесс из `requires_activation`.
- После approval путь зависит от `auto_ratification`.
- Из `awaiting_ratification` изменение версии снимает её из очереди и требует повторного submit.

## BR-5 Deployment approval
- `DeploymentVersion` можно отправлять повторно из `draft`, reject и cancel статусов.
- После `ratified` версия может быть переведена в `deployed`.
- Только одна продуктивная версия deployment может быть активной одновременно.

## BR-6 Lineage restriction
- Lineage в MVP реализован только для `simulation_based` deployment.
- Допускается ровно одна lineage-симуляция.
- Lineage-симуляция обязана совпадать с источником обязательной lineage-скоркарты.

## BR-7 Dynamic approval route
- Approval stages: 0..*; ratification stage: ровно 1.
- Нельзя выбрать самого себя.
- Один человек не может быть в нескольких этапах одного маршрута.
- Recall допустим как на approval, так и на ratification.

## BR-8 Package handling
- Package создаётся вручную из `awaiting_ratification` и сразу считается отправленным.
- Package не имеет собственного status enum и не является target согласования.
- Решения принимаются по каждому `ApprovalInstance`, даже если ratifier действует по всей группе.

## BR-9 Access scope
- ПРМ и методолог работают в продуктовом scope, кроме исключения `methodologist` на странице `Пакеты`.
- `Approver` и `Ratifier` не редактируют доменные сущности, а только принимают решения в своих назначениях.

## BR-10 Artifacts
- Артефакты — внешние URL, не загружаемые файлы.
- Артефакты допускаются для `Initiative`, `Simulation`, `Pilot`, `Deployment`.
- Скоркарта не моделируется как артефакт.
