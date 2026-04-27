# Заметки к scope prototype

## Цель
Показать end-to-end контур согласования и утверждения так, чтобы команда могла отдельно оценить backend core и пользовательскую страницу `Согласования`.

## Какой идеальный сценарий показываем
- пользователь отправляет версию `Pilot` или `Deployment` в approval flow;
- approver видит назначение, открывает карточку элемента и принимает решение;
- ratifier работает как с individual item, так и с package-элементами;
- система сохраняет комментарии, историю решений и корректно меняет lifecycle доменной сущности.

## Какой MVP cut показываем отдельно
- вкладки `Approval` и `Ratification`;
- individual и package карточки без лишней автоматики;
- batch approve/reject/ratify в пределах уже описанного MVP;
- просмотр комментариев и краткого контекста элемента;
- без расширенной аналитики и без отдельного package-workspace вне `approvals`.

## Какие planning stories обсуждаем через этот прототип
- `STORY-APPROVALS-001`
- `STORY-APPROVALS-002`

## Mock data
- 2 версии `Deployment` в статусе `awaiting_approval`;
- 1 версия `Pilot` в статусе `awaiting_ratification`;
- 1 package из 3 элементов с mixed-результатами по individual решениям;
- комментарии approver/ratifier и история переходов по этапам.

## Открытые вопросы
- где проходит граница между feature `approvals` и feature `packages` для package-specific UI;
- нужен ли в MVP отдельный drill-down в доменную деталку из каждой карточки;
- какой объём audit/history обязателен прямо на странице, а какой остаётся в detail views.
