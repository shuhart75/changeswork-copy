# ADR — Legacy normalization boundary

Дата: `2026-04-24`
Статус: `accepted`

## Контекст

Проект `changeswork-copy` одновременно хранит:
- канонический current baseline;
- рабочие feature-level дельты;
- полный исторический snapshot legacy `changesWork`.

Без явной границы между этими слоями легко перепутать:
- что уже deployed;
- что является только legacy evidence;
- что является новой квартальной доработкой.

## Решение

- `baseline/current/` считаем единственным каноническим описанием deployed-системы.
- `features/` используем только для change delta и living requirements по новым доработкам.
- `context/source-materials/current-system/` используем как curated raw evidence для baseline normalization.
- `context/source-materials/legacy/changeswork-full/` используем как полный исторический архив, но не как прямой source of truth.
- Отсутствие отдельной feature в harness не трактуем как отсутствие существующего system coverage. Это особенно важно для `Simulation` scope.

## Следствия

- Для existing simulation pages baseline нормализуется через `baseline/current/*`, а не через создание retro-feature `simulations`, если пользователь отдельно этого не попросит.
- Новая feature `simulation-bt-agent` считается дельтой поверх уже существующей simulation detail page.
- При последующих миграциях сначала ищем canonical baseline или feature artifact, и только потом уходим в raw snapshot.
