# Задачи: Артефакты (документы) как ссылки на внешние ресурсы

**Источник правды:** [`spec/domain_model.md`](/home/reutov/Documents/AI/changesWork/spec/domain_model.md) → БП-11 "Управление артефактами"

## Обзор

**Компонент:** Артефакты (Artifacts)  
**Статус:** Новая разработка (MVP v6.8)

### MVP-правило (как в spec)

- Артефакты это **ссылки на внешние документы (URL)**, а не загрузка файлов.
- Артефакты могут быть привязаны к сущностям: `Simulation`, `Pilot`, `Deployment`, `Initiative` (но Initiative не в MVP).
- К `Scorecard`/`ScorecardVersion` артефакты **никогда не прикрепляем** (скоркарта не является контейнером `Artifact`).
- Типы: `business_case`, `rov`, `other`.
- Права управления наследуются от родительской сущности и ролей (ПРМ своего продукта; методолог глобально; админ глобально).

> Примечание: UI в прототипе соответствует этому правилу (имя + тип + URL).

---

## BE-ART1: Backend артефактов (URL)

**Тип:** Story  
**Приоритет:** Критический  
**Оценка:** 3 дня (как в Gantt v6)

### Summary
Реализовать единый backend-механизм хранения и управления артефактами как URL-ссылками и подключить его к детальным страницам сущностей.

### Модель данных (минимально)

```python
class Artifact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    entity_type = models.CharField(max_length=50)  # 'pilot'|'deployment'|'simulation'|'initiative'
    entity_id = models.UUIDField()

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=[('business_case','...'),('rov','...'),('other','...')])
    url = models.URLField(max_length=2048)

    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['entity_type', 'entity_id']),
        ]
```

### API (предпочтительный, единообразный)

1. **List**

`GET /api/artifacts/?entity_type={type}&entity_id={uuid}`

Response:
```json
{
  "results": [
    {
      "id": "uuid",
      "entity_type": "deployment",
      "entity_id": "uuid",
      "name": "Бизнес-кейс Q1",
      "type": "business_case",
      "url": "https://...",
      "created_by": { "id": "uuid", "full_name": "..." },
      "created_at": "2026-03-01T10:00:00Z"
    }
  ]
}
```

2. **Create**

`POST /api/artifacts/`

Request:
```json
{
  "entity_type": "deployment",
  "entity_id": "uuid",
  "name": "ROV модель",
  "type": "rov",
  "url": "https://..."
}
```

3. **Delete**

`DELETE /api/artifacts/{id}/`

### Поддержка nested-эндпоинтов (для совместимости с задачами страниц)

Если UI/страницы используют nested URL, допускается проксирование на тот же механизм:
- `GET/POST /api/deployments/{id}/artifacts/` → `entity_type='deployment'`
- `GET/POST /api/pilots/{id}/artifacts/` → `entity_type='pilot'`
- `GET/POST /api/simulations/{id}/artifacts/` → `entity_type='simulation'`
- `DELETE /api/<entity>/{id}/artifacts/{artifact_id}/` → delete

### Бизнес-правила и права доступа

- Валидация URL: формат URL (как в spec).
- Права:
  - ПРМ может создавать/удалять артефакты только для сущностей своего продукта.
  - Методолог может управлять артефактами для любых сущностей.
  - Админ может всё.
- Approver/Ratifier не получают отдельного права на артефакты; их видимость определяется правом просмотра родительской сущности.

### Acceptance Criteria

- [ ] Модель `Artifact` добавлена (миграции) и индексируется по `(entity_type, entity_id)`
- [ ] Реализованы `GET /api/artifacts/`, `POST /api/artifacts/`, `DELETE /api/artifacts/{id}/`
- [ ] (Если нужно для страниц) реализованы nested-эндпоинты для deployments/pilots/simulations
- [ ] Валидация URL работает (400 на невалидный url)
- [ ] Права доступа реализованы по правилам spec
- [ ] Unit тесты: права + базовый CRUD (минимум list/create/delete)
