# Current-state UI navigation

Дата обновления: `2026-04-24`

## Навигационная карта

| Area | Screen / route | Что считается baseline | Источники |
|---|---|---|---|
| Approvals | `/approvals`, `/approvals?approval_instance_id={id}`, `/approvals?package_id={id}` | единая страница назначения согласующих и ratifier workflow с деталкой approval/package | `context/source-materials/current-system/requirements/raw/final-spec/REQ_approvals_page_frontend.md` |
| Packages | `/packages` | очередь пакетов, создание пакета, деталка пакета | `context/source-materials/current-system/requirements/raw/final-spec/REQ_packages_page_frontend.md` |
| Scorecards | `/scorecards/:id`, `/scorecards/new`, `/scorecards/:id/edit` | деталка, создание из `Pilot`/`Deployment`, редактирование | `context/source-materials/current-system/requirements/raw/final-spec/REQ_scorecards_frontend.md` |
| Deployments | `/deployments`, `/deployments/:id` | список внедрений, детальная форма, редактирование через ту же host page | `context/source-materials/current-system/requirements/raw/final-spec/REQ_deployments_frontend.md`, `context/source-materials/current-system/requirements/raw/final-spec/REQ_deployments_list_frontend.md`, `context/source-materials/current-system/requirements/raw/final-spec/REQ_deployments_detail_frontend.md` |
| Pilots | business page `Pilots` (exact route not re-normalized yet) | список, деталка, создание, lifecycle actions | `context/source-materials/current-system/requirements/raw/final-spec/REQ_pilots_frontend.md` |
| Simulations | business pages `Simulations list` and `Simulation detail` (exact route not re-normalized yet) | список симуляций, детальная страница, status/read-only host screen, артефакты и связанные сущности | `context/source-materials/legacy/changeswork-full/planning/mvp/current/tasks/legacy/mvp_tasks_simulations_page.md`, `context/source-materials/legacy/changeswork-full/planning/mvp/current/tasks/legacy/mvp_tasks_simulation_detail_page.md`, `baseline/current/ui/simulations.md` |

## Sidebar baseline

Legacy navigation-menu scope подтверждает, что текущий baseline исходит из левого sidebar как главной точки входа.

### Разделы меню
- `Deployments`
- `Simulations`
- `Pilots`
- `Changes`
- `Packages` — если пакетный контур включён в поставку
- `Approvals` — для approval / ratification workflow

### Поведение
- активный пункт визуально выделяется;
- меню умеет сворачиваться до иконок;
- в свёрнутом состоянии названия раскрываются через tooltip;
- состояние сворачивания может храниться локально в браузере;
- на tablet/mobile меню переходит в overlay / drawer-паттерн.

### Ролевой срез
- `PRM`, `Methodologist`, `Admin` видят основной рабочий набор разделов;
- `Approver` может быть ограничен страницей `Approvals`;
- продуктовые ограничения применяются поверх общей видимости пункта меню.

### Что не нормализовано до конца
- точные route names для части legacy screens ещё не выровнены в единый current-state каталог;
- counters в меню и profile dropdown зафиксированы как UX-детали legacy-плана, но не как самостоятельные baseline contracts.

## Host-screen notes

### Simulation detail
- Simulation detail page считается existing baseline coverage.
- Именно эта страница выступает host screen для новой feature `simulation-bt-agent`.
- В baseline сюда уже входят: `Основная информация`, статус, продукт, даты, автор, артефакты и связанные сущности.
- Новая кнопка `Сформировать БТ` и AI-диалог в baseline пока не входят.

### Deployment detail
- Одна host page совмещает просмотр и редактирование в зависимости от статуса и прав.
- Важные baseline-секции: общая информация, связанные скоркарты, связанные сущности, артефакты, lifecycle actions.

### Cross-page behavior
- Русскоязычные status labels не должны расходиться с backend status/source-of-truth.
- Product-scope visibility определяется RBAC и не дублируется локальными UI-правилами.
