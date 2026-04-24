# Отчет по выравниванию планирования MVP (v6.1)

**Дата:** 2026-03-11  
**Основа спецификации:** [`spec/domain_model.md`](/home/reutov/Documents/AI/changesWork/spec/domain_model.md)  
**Основа плана/оценок:** [`planning/mvp/gantt/mvp_gantt_chart_v6.puml`](/home/reutov/Documents/AI/changesWork/planning/mvp/gantt/mvp_gantt_chart_v6.puml)

> Примечание: это исторический отчет про выравнивание v6.1.  
> Для текущего скоупа MVP v6.3 (без Initiative, с Chains/Lineage и approval для Simulation) см. `reports/RESCOPE_REPORT.md`.

## Что сделано

1. Создана новая версия материалов планирования: [`planning/mvp/versions/v6.1/`](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.1)
2. Сформирована "терминологически выровненная" диаграмма Ганта:
   - [`planning/mvp/versions/v6.1/gantt/mvp_gantt_chart_v6.1_aligned.puml`](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.1/gantt/mvp_gantt_chart_v6.1_aligned.puml)
   - Изменения только в названиях задач (коды/длительности/зависимости сохранены как в v6)
3. Скопированы и выровнены task-документы в:
   - [`planning/mvp/versions/v6.1/tasks/`](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.1/tasks)
   - Оценки в markdown синхронизированы с длительностями из Gantt v6 для тех задач, которые есть в диаграмме.
4. Уточнена ключевая часть MVP (согласования/пакеты/скоркарты) в соответствии с `spec/domain_model.md`:
   - Approval: обновлено на модель `ApprovalInstance/Stage/Assignment/Decision`
   - Packages: убраны ссылки на "цепочки", статус Package перенесен на items (как в spec)
   - Scorecards: добавлено версионирование через `ScorecardVersion` и привязка к версии шаблона
5. Обновлены утилиты проверки Gantt:
   - [`scripts/check_overlaps_v6.py`](/home/reutov/Documents/AI/changesWork/scripts/check_overlaps_v6.py) теперь принимает путь к файлу и учитывает ресурсы вида `{F2:50%}`
   - [`scripts/verify_dependencies_v6.py`](/home/reutov/Documents/AI/changesWork/scripts/verify_dependencies_v6.py) теперь принимает путь к файлу и корректно читает множественные зависимости

## Важные выравнивания терминов

- `Initiative` (Инициатива) теперь явно отделена от `Deployment` (Внедрение).
- В task-доках выполнено переименование файлов:
  - `mvp_tasks_deployments_*` -> `mvp_tasks_initiatives_*` (там, где речь про Initiative)
  - `mvp_tasks_changes_*` -> `mvp_tasks_deployments_*` (там, где речь про Deployment)

Сводка и карта соответствия "Gantt -> task docs":  
[`planning/mvp/versions/v6.1/tasks/mvp_tasks_summary.md`](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.1/tasks/mvp_tasks_summary.md)

## Проверки

- На [`planning/mvp/versions/v6.1/gantt/mvp_gantt_chart_v6.1_aligned.puml`](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.1/gantt/mvp_gantt_chart_v6.1_aligned.puml) проверка перекрытий показала `0` overlaps по ресурсам (с учетом `{F2:50%}` как отдельного ресурса в проверке).

## Известные допущения и риски

1. В Gantt v6 отсутствуют отдельные backend-задачи для деталок Simulation/Pilot (`BE-SD1`, `BE-PD1`), при этом FE-деталки (`FE_SD1`, `FE_PD1`) запланированы.
   - В v6.1 это оформлено как допущение: backend-деталки уже есть (или входят в `BE_S1/BE_P1`).
2. Внутри спецификации встречаются противоречия (пример: каскадность архивирования Initiative, наличие/отсутствие статусов у Package в разных артефактах spec).
   - В v6.1 мы следовали `spec/domain_model.md` как источнику правды, но эти места лучше зафиксировать как вопросы для подтверждения с владельцем домена.

## Результат

Готов "чистый" набор артефактов планирования v6.1, который:
- использует `spec/domain_model.md` как терминологическую и смысловую основу
- использует `Gantt v6` как основу оценок и последовательности работ
- убирает наиболее критичные расхождения (Initiative vs Deployment, approval model, package semantics, scorecard versioning)
