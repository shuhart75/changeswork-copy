# Migration Notes

Legacy simulation scope imported into the harness as an existing-coverage feature.

## Что нормализовано
- список симуляций;
- детальная страница симуляции;
- форма создания/редактирования;
- независимый lifecycle симуляции;
- блоки `Артефакты` и `Связанные сущности`.

## Что важно
- Это не новая planning feature на квартал.
- Основная цель — сделать simulation scope видимым и в `features/`, а не только в `baseline/current/` и raw snapshot.
- Новая дельта поверх этого scope живёт отдельно в `features/simulation-bt-agent/`.
