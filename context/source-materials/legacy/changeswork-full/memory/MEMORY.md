# Project memory (Claude Code)

## Requirements formatting conventions (portable)

### File naming (in this repo)
- Handoff requirements live in `final-spec/` and use `REQ_<topic>.md` (e.g. `REQ_artifacts_core.md`, `REQ_roles_rbac.md`, `REQ_approval_core.md`).

### Integration with existing systems
- **rscon-sudir integration (roles/RBAC):**
  - **MVP подход: только чтение, без управления ролями**
  - Existing API: `GET /api/v1/user`, `GET /api/v1/access`
  - Existing enum `accessType`: ADMIN, EDITOR, METODOLOG, VIEWER, AUDITOR
  - MVP roles mapping:
    - `prm` → EDITOR (product-scoped via `permittedSpaces`)
    - `methodologist` → METODOLOG (global)
    - `approver` → APPROVER (NEW, global)
    - `ratifier` → RATIFIER (NEW, global)
    - `admin` → ADMIN (global)
  - Minimal changes (делает backend-команда rscon-sudir):
    - Добавить 2 новых значения в enum accessType: APPROVER, RATIFIER
    - Создать роли через внутренние инструменты/миграции
    - Назначить роли пользователям через внутренние инструменты
  - Наша команда: только читаем через GET /api/v1/user и проверяем через GET /api/v1/access
  - См. `final-spec/REQ_roles_rbac.md` раздел 4 для деталей интеграции

Эти правила — **мета-требования к оформлению требований**. Держать их переносимыми между проектами.

### Data model (БД/сущности)

- Описание таблиц в модели данных **всегда** делать Markdown-таблицей с колонками:
  - **Поле | Тип | Обязательность | Описание**
- Если у поля есть дефолт/ограничение — отражать это в колонке «Описание» (или отдельным подпунктом сразу под таблицей).
- Недостаточно просто перечислить сущности или связи: для **каждой необходимой к реализации таблицы** нужно явно давать такую таблицу полей.

### OpenAPI / API contract

- Если в требованиях описываются backend endpoints — **обязательно** добавлять OpenAPI‑фрагмент.
- Формат: **OpenAPI 3.x**, YAML.
- Язык:
  - `summary`/`description` писать **на русском**.
  - Имена схем/полей/enum — в формате проекта (обычно латиница, camelCase в JSON).
- Контракт должен быть согласован с моделью данных и DTO в тексте требований:
  - одинаковые названия полей
  - одинаковые required/optional
  - одинаковые enum значения
  - одинаковые ограничения (maxLength и т.п.)
- Помимо OpenAPI-фрагмента, для каждого endpoint **обязательно** добавлять:
  - пример запроса;
  - пример успешного ответа;
  - при необходимости пример типовой ошибки.
- Ошибки/коды:
  - всегда явно перечислять ожидаемые HTTP-коды ответов (`200/201/204/403/404/422` и т.п.)
  - если в проекте есть стандарт ошибок (Problem Details / ErrorEnvelope) — ссылаться на него или включать schema

### Maintenance

- Дополнять эти правила по мере работы.
- Если пользователь уточняет правило оформления — фиксировать здесь, чтобы не повторять в дальнейшем.

## Planning / Gantt agent rules (reference-only)

> Эти правила уже являются source-of-truth в `CLAUDE.md` и `PLANNING_LAWS.md`.
> Здесь храним только краткую памятку/указатели, чтобы быстрее ориентироваться.

- Законы планирования (non-negotiable): см. `PLANNING_LAWS.md` и `CLAUDE.md`.
- Нельзя допускать >100% загрузки ресурсов.
- Оценки в базовом плане «священны»: производительность моделируется только через `{X:NN%}` / `efficiency`.
- Если снимаем non‑MVP gate — обязателен явный resource-leveling/seq constraints.
- При изменениях в gantt обязательно прогонять валидатор:
  - `python3 scripts/validate_gantt_laws.py planning/mvp/current/gantt/mvp_gantt_chart_current.puml`
- Замороженные версии `planning/mvp/versions/v6.*` не править; делать новую версию.

### TaskJuggler tracking

- Прогресс вести только в `planning/mvp/current/taskjuggler/status/actual.tji` (минимально: `% complete`).
- Baseline PlantUML (`mvp_gantt_chart_current.puml`) не менять для факта; факт вести отдельным файлом (например `mvp_gantt_chart_actual.puml`).

### Repo workflow (high-level)

- Работать в feature ветках `work/<area>-<short>`.
- Коммиты: `<area>: <what> (refs: spec vX.Y, mvp v6.Z)`.

### Why keep this here?

- Это не дублирование source-of-truth, а «индекс/памятка» для ускорения работы и переносимости практик.

## User preferences

- Требования (handoff) писать на русском.
- При необходимости терминов — можно добавлять англ. термин в скобках для однозначности.
- Модель данных в требованиях: **только таблицей** (см. выше).
- По API: всегда добавлять OpenAPI контракт **и** примеры запросов/ответов.

## Open questions / to clarify later

- Единый формат ошибок API (ProblemDetails vs custom envelope) — уточнить при необходимости.
- Тип идентификаторов в API (uuid vs numeric) — уточнять при необходимости, не гадать.

---

Update log:
- 2026-03-15: зафиксированы правила оформления data model и OpenAPI; добавлена памятка по planning/gantt.

---

Note: Keep this file under ~200 lines; it is always loaded into context.
