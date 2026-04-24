# Current-state API overview

Дата обновления: `2026-04-24`

## API groups

### Approvals and packages
| Endpoint / group | Назначение | Источники |
|---|---|---|
| `GET /api/v1/approvals/my` | очередь назначений approval/ratification | `context/source-materials/current-system/requirements/raw/final-spec/REQ_approvals_page_backend.md` |
| `GET /api/v1/approvals/{id}` | деталка approval instance | `context/source-materials/current-system/requirements/raw/final-spec/REQ_approvals_page_backend.md` |
| `POST /api/v1/approvals/{id}/action` | индивидуальное решение | `context/source-materials/current-system/requirements/raw/final-spec/REQ_approvals_page_backend.md` |
| `POST /api/v1/approvals/action` | массовое действие | `context/source-materials/current-system/requirements/raw/final-spec/REQ_approvals_page_backend.md` |
| `POST /api/v1/packages` | создание пакета из `awaiting_ratification` | `context/source-materials/current-system/requirements/raw/final-spec/REQ_approval_core.md`, `context/source-materials/current-system/requirements/raw/final-spec/REQ_packages_page_backend.md` |
| `GET /api/v1/packages/queue`, `GET /api/v1/packages/my`, `GET /api/v1/packages/{id}` | очереди и деталка пакетов | `context/source-materials/current-system/requirements/raw/final-spec/REQ_packages_page_backend.md` |
| `POST /api/v1/packages/{id}/action` | ratify / reject пакета | `context/source-materials/current-system/requirements/raw/final-spec/REQ_packages_page_backend.md` |

### Scorecards and templates
| Endpoint / group | Назначение | Источники |
|---|---|---|
| `GET /api/v1/scorecards` | выбор и список скоркарт | `context/source-materials/current-system/requirements/raw/final-spec/REQ_scorecards_backend.md`, `context/source-materials/current-system/requirements/raw/final-spec/REQ_scorecards_backend.openapi.yaml` |
| `POST /api/v1/scorecards` | создание скоркарты и первой версии | `context/source-materials/current-system/requirements/raw/final-spec/REQ_scorecards_backend.md` |
| `GET /api/v1/scorecards/{id}` | деталка скоркарты | `context/source-materials/current-system/requirements/raw/final-spec/REQ_scorecards_backend.md`, `context/source-materials/current-system/requirements/raw/final-spec/REQ_scorecards_backend.openapi.yaml` |
| `PUT /api/v1/scorecards/{id}` | обновление с выпуском новой версии | `context/source-materials/current-system/requirements/raw/final-spec/REQ_scorecards_backend.md`, `context/source-materials/current-system/requirements/raw/final-spec/REQ_scorecards_backend.openapi.yaml` |
| `GET /api/v1/scorecards/{id}/relations` | источники и использование скоркарты | `context/source-materials/current-system/requirements/raw/final-spec/REQ_scorecards_backend.md`, `context/source-materials/current-system/requirements/raw/final-spec/REQ_scorecards_backend.openapi.yaml` |
| `GET /api/v1/scorecard-template-versions` | список template versions | `context/source-materials/current-system/requirements/raw/final-spec/REQ_scorecards_backend.md`, `context/source-materials/current-system/requirements/raw/final-spec/REQ_scorecards_backend.openapi.yaml` |
| `GET /api/v1/scorecard-template-versions/{id}/default-config` | default config для построения формы | `context/source-materials/current-system/requirements/raw/final-spec/REQ_scorecards_backend.md`, `context/source-materials/current-system/requirements/raw/final-spec/REQ_scorecards_backend.openapi.yaml` |

### Deployments
| Endpoint / group | Назначение | Источники |
|---|---|---|
| `GET /api/v1/deployments` | список внедрений | `context/source-materials/current-system/requirements/raw/final-spec/REQ_deployments_backend.md` |
| `GET /api/v1/deployments/{id}` | деталка внедрения | `context/source-materials/current-system/requirements/raw/final-spec/REQ_deployments_backend.md`, `context/source-materials/current-system/requirements/raw/final-spec/REQ_deployments_backend_db_api.md` |
| `POST /api/v1/deployments` | создание draft-shell внедрения | `context/source-materials/current-system/requirements/raw/final-spec/REQ_deployments_backend.md` |
| `PUT /api/v1/deployments/{id}` | финальное сохранение и повторный выпуск draft | `context/source-materials/current-system/requirements/raw/final-spec/REQ_deployments_backend.md`, `context/source-materials/current-system/requirements/raw/final-spec/REQ_deployments_backend_db_api.md` |
| `POST /api/v1/deployments/{id}/action` | lifecycle action endpoint | `context/source-materials/current-system/requirements/raw/final-spec/REQ_deployments_backend_lifecycle.md` |

### Pilots
| Endpoint / group | Назначение | Источники |
|---|---|---|
| `GET /api/v1/pilots`, `GET /api/v1/pilots/{pilot_id}` | список и деталка пилотов | `context/source-materials/current-system/requirements/raw/final-spec/REQ_pilots_frontend.md`, `context/source-materials/current-system/requirements/raw/final-spec/REQ_pilots_backend.md` |
| `POST /api/v1/pilots` | создание пилота | `context/source-materials/current-system/requirements/raw/final-spec/REQ_pilots_frontend.md`, `context/source-materials/current-system/requirements/raw/final-spec/REQ_pilots_backend.md` |
| `DELETE /api/v1/pilots/{pilot_id}` | удаление черновика/разрешённого состояния | `context/source-materials/current-system/requirements/raw/final-spec/REQ_pilots_frontend.md` |
| `POST /api/v1/pilots/{pilot_id}/send-to-approval`, `/activate`, `/complete`, `/require-correction` | lifecycle actions пилота | `context/source-materials/current-system/requirements/raw/final-spec/REQ_pilots_frontend.md` |
| `GET /api/v1/pilots/{pilot_id}/metrics` | метрики пилота | `context/source-materials/current-system/requirements/raw/final-spec/REQ_pilots_frontend.md` |

### Simulations
| Endpoint / group | Назначение | Источники |
|---|---|---|
| `GET /api/simulations/` | legacy list endpoint для списка симуляций | `context/source-materials/legacy/changeswork-full/planning/mvp/current/tasks/legacy/mvp_tasks_simulations_page.md`, `baseline/current/api/simulations.md` |
| `GET /api/simulations/{id}/` | legacy detail endpoint симуляции | `context/source-materials/legacy/changeswork-full/planning/mvp/current/tasks/legacy/mvp_tasks_simulation_detail_page.md`, `baseline/current/api/simulations.md` |
| `GET/POST/DELETE /api/simulations/{id}/artifacts...` | артефакты симуляции | `context/source-materials/legacy/changeswork-full/planning/mvp/current/tasks/legacy/mvp_tasks_simulation_detail_page.md`, `context/source-materials/current-system/requirements/raw/final-spec/REQ_artifacts_core.md`, `baseline/current/api/simulations.md` |
| `GET /api/simulations/{id}/related/` | связанные пилоты и внедрения | `context/source-materials/legacy/changeswork-full/planning/mvp/current/tasks/legacy/mvp_tasks_simulation_detail_page.md`, `baseline/current/api/simulations.md` |
| `POST /api/simulations/{id}/start/`, `/complete/`, `/fail/` | lifecycle actions симуляции | `context/source-materials/legacy/changeswork-full/planning/mvp/current/tasks/legacy/mvp_tasks_simulation_lifecycle.md`, `baseline/current/api/simulations.md` |

### Access / RBAC
| Endpoint / group | Назначение | Источники |
|---|---|---|
| `GET /api/v1/user` | профиль и роли пользователя | `context/source-materials/current-system/requirements/raw/final-spec/REQ_roles_rbac.md` |
| `GET /api/v1/access` | точечная проверка прав | `context/source-materials/current-system/requirements/raw/final-spec/REQ_roles_rbac.md` |

## Нормализационная оговорка

Simulation API в legacy-материалах зафиксирован в более старой форме `/api/simulations/...`, тогда как часть новых материалов использует `/api/v1/...` стиль. До отдельной baseline-normalization задачи считаем это доказательством existing coverage, но не окончательным каноническим URI-стандартом для simulation scope.
