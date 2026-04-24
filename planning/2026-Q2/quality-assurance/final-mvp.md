# QA Final MVP — итоговое интеграционное тестирование

Дата обновления: `2026-04-24`
Источник: `context/source-materials/legacy/changeswork-full/planning/mvp/current/tasks/legacy/mvp_tasks_qa_final.md`
Оценка legacy: `3 дня`

## Роль этапа

Это финальный e2e-слой перед релизом MVP. Его цель — проверить не отдельные экраны, а рабочую систему целиком.

## Ключевые end-to-end сценарии

### Полный цикл внедрения
- создание `Deployment`;
- создание и выполнение `Simulation`;
- создание `Scorecard` по результатам симуляции;
- создание `Pilot`;
- approval / ratification / activation;
- дальнейшее создание и выпуск `Deployment`;
- проверка связей и уведомлений на всём пути.

### Batch operations
- массовая работа с несколькими элементами;
- формирование `Package`;
- batch approve / ratify;
- проверка групповой обработки и уведомлений.

### Rollback
- выпуск deployment в `deployed`;
- rollback с причиной;
- проверка истории внедрений и уведомлений;
- дальнейший корректирующий цикл.

### Rejection loops
- отклонение на approval и ratification;
- возврат в корректные состояния;
- повторная отправка после исправлений.

## Итоговые deliverables

- финальный QA report;
- consolidated bug list;
- подтверждение прохождения критических e2e-сценариев;
- подтверждение готовности к релизной фиксации.
