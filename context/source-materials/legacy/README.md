# Legacy snapshots

- `changeswork-full/` — полная copied-by-value копия legacy-репозитория `changesWork`, excluding `.git/`, `.claude/worktrees/`, and `__pycache__/`.
- `changeswork-full.manifest.md` — import policy and file counts.
- `changeswork-map.md` — навигационная карта по legacy-структуре и её соответствию новой harness-модели.

## Статус

Полнота snapshot подтверждена сравнением с оригинальным `/home/reutov/Documents/AI/changesWork` по списку файлов с теми же правилами исключений.

## Когда сюда идти

- когда normalized feature/baseline-артефактов не хватает;
- когда нужно восстановить историю решений, ad-hoc правил, старых планов или прототипов;
- когда нужно понять, из какого legacy-файла появилась текущая нормализованная сущность.
