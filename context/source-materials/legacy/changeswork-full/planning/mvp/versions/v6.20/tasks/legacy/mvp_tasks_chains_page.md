# Задачи: Источники lineage (created_from) и preview источников в формах

**Источник правды:** [`spec/domain_model.md`](/home/reutov/Documents/AI/changesWork/spec/domain_model.md) (контекст Lineage, см. раздел 7)

## Обзор

**Смысл:** в рамках MVP мы поддерживаем только концепт "создано из" (sources) для `Pilot`/`Deployment` на основе выбранных скоркарт, и показываем preview источников в формах.  
**Важно:** Страницы **"Цепочки"** и lineage widget **не делаем** (ни в MVP, ни вообще).

## AN-CD1: Аналитика источников created_from ("создано из")

**Тип:** Task  
**Оценка:** 5 дней (как в Gantt v6 для AN_CD1)

### Summary
Зафиксировать правила определения "источников" (created_from) и требования к автосозданию `PilotSource` / `DeploymentSource`, а также UX-preview источников в формах при выборе скоркарт.

### Что уточнить (MVP)

- Когда создаём/обновляем источники:
  - минимум: на create (как в `BE-CD1`)
  - опционально: на update новой версии (PilotVersion/DeploymentVersion) при изменении набора скоркарт
- Как выбираем источники по скоркартам:
  - симуляции как источники скоркарт (read-only, симуляции не дорабатываем)
  - пилоты как источники скоркарт (если скоркарта была создана/использована ими, как в spec)
- Как действуем при множественных источниках одной скоркарты.
- Что показываем в preview в формах Pilot/Deployment:
  - список источников (SIM/PLT) агрегировано по выбранным скоркартам
  - отображение "через скоркарты: SC-xxx, SC-yyy"
- Нужен ли отдельный API для preview источников (рекомендуется да, т.к. lineage widget/page отсутствуют).

### Deliverables

- Правила определения источников (MVP) в виде краткого spec-блока
- API контракт для preview источников (если нужен) и описание UX на формах

## BE-CD1: Источники lineage: автосоздание + preview для форм

**Тип:** Task  
**Оценка:** 2 дня (как в Gantt v6 для BE_CD1)

### Scope

1. **Автосоздание источников (`created_from`) на create**
- При создании `Pilot` и `Deployment` на основе выбранных `Scorecard`:
  - backend определяет, какие `Simulation`/`Pilot` являются источниками выбранных скоркарт (как в spec)
  - записывает `PilotSource` / `DeploymentSource` автоматически

2. **Preview источников по выбранным скоркартам (для форм)**
- Реализовать best-effort API, который по списку `scorecard_ids[]` вернет агрегированный список источников:
  - `simulations[]`: id/display_id/name (минимум)
  - `pilots[]`: id/display_id/name (минимум)
  - для каждого источника: список `via_scorecards[]` (display_id) для отображения "через скоркарты: ..."
- Предпочтительный endpoint:
  - `GET /api/sources/preview/?scorecard_ids=...` (или `POST /api/sources/preview/`), без привязки к странице "Цепочки"

### Acceptance Criteria

 - [ ] `PilotSource` / `DeploymentSource` создаются автоматически на create (минимум).
 - [ ] Preview endpoint возвращает источники по выбранным скоркартам и не блокирует сохранение форм (best-effort).

## FE-CD1: Preview источников (created_from) в формах (UX)

**Тип:** Task  
**Оценка:** 3 дня (как в Gantt v6 для FE_CD1)

### Scope

- В формах `Pilot` и `Deployment` (создание/редактирование):
  - пользователь выбирает `Scorecard` (как и раньше)
  - UI показывает "источники" выбранных скоркарт (preview created_from), если возможно

### Acceptance Criteria

- [ ] Preview источников не блокирует сохранение (может быть best-effort).
