# Заметки к scope prototype

## Цель
Показать целостный контур внедрений: от backend foundation и списка до формы, detail view и lifecycle, чтобы HLE можно было обсуждать по отдельным planning stories.

## Какой идеальный сценарий показываем
- пользователь открывает список внедрений, фильтрует и переходит в деталку;
- в detail видит основную информацию, связанные scorecards, артефакты и историю;
- создаёт новое внедрение или новую версию существующего;
- переводит версию по жизненному циклу вплоть до `deployed` и rollback-сценариев.

## Какой MVP cut показываем отдельно
- list page со статусами, критичностью и переходом в detail;
- create/edit form с выбором скоркарт и базовыми полями;
- detail page с history/artifacts/related blocks;
- lifecycle `draft -> approval -> approved -> deployed` и базовые reject/recall/rollback сценарии.

## Какие planning stories обсуждаем через этот прототип
- `STORY-DEPLOYMENTS-001`
- `STORY-DEPLOYMENTS-002`
- `STORY-DEPLOYMENTS-003`
- `STORY-DEPLOYMENTS-004`
- `STORY-DEPLOYMENTS-005`

## Mock data
- 4 внедрения со статусами `draft`, `awaiting_approval`, `approved`, `deployed`;
- 2 scorecards разной критичности для выбора в форме;
- история версий одного внедрения с предыдущим rollout;
- связанные артефакты и краткий trace-контекст.

## Открытые вопросы
- какой объём related entities обязателен прямо в detail MVP;
- нужно ли отдельно показывать release milestones/test stand dependencies внутри detail;
- где проходит граница между lifecycle detail и approval-specific комментариями.
