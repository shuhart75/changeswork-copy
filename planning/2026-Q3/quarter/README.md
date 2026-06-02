# 2026-Q3

## Notes

Этот квартал создан как новый planning-контур внутри harness, а не как импорт legacy-плана.
На текущем шаге в квартал заведена отдельная feature `roles-industrialization`, которая описывает промышленную доработку ролевой модели поверх уже существующего Q2 control-layer.

## Scope Decisions

- `features/roles/` и `planning/2026-Q2` остаются без перепланирования и продолжают описывать imported MVP/control scope.
- Новая промышленная ролевая модель вынесена в отдельную feature `features/roles-industrialization/`.
- Quarter-plan и commander-plan в `2026-Q3` используются как план новой дельты, а не как rewrite текущего квартала.

## Comparison Notes

- При сравнении кварталов проверяем, что Q2 фиксирует существующее MVP-покрытие, а Q3 добавляет новую промышленную матрицу ролей, endpoint mapping и cross-feature propagation.
- Если позже потребуется execution-tracking по Q3, его надо заводить отдельно в `execution-update`, не смешивая с Q2 actual-progress.
