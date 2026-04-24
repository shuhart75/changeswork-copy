#!/usr/bin/env bash
set -euo pipefail

# TaskJuggler wrapper for this repo.
# - Can be executed from anywhere inside the project.
# - Renders reports into /tmp/tj-out (default) or a custom directory.
# - Opens the output folder (and the main HTML report) after rendering.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../../.." && pwd)"
TJP_FILE="${ROOT_DIR}/planning/mvp/current/taskjuggler/mvp_current.tjp"
STATUS_FILE="${ROOT_DIR}/planning/mvp/current/taskjuggler/status/actual.tji"

OUT_DIR="${1:-/tmp/tj-out}"

mkdir -p "${OUT_DIR}"

# Render HTML + CSV
# Note: TaskJuggler requires OUT_DIR to exist.
tj3 "${TJP_FILE}" --output-dir "${OUT_DIR}"

# Print a short hint where to track progress
cat <<EOF

OK: reports rendered to:
  ${OUT_DIR}

Tracking file (edit % complete here):
  ${STATUS_FILE}

Main report:
  ${OUT_DIR}/Overview.html
EOF

# Open output folder + main report.
# Linux: prefer xdg-open.
# If xdg-open isn't available, just print the paths.
if command -v xdg-open >/dev/null 2>&1; then
  # Open folder in file manager
  xdg-open "${OUT_DIR}" >/dev/null 2>&1 || true
  # Open main HTML report in default browser
  if [[ -f "${OUT_DIR}/Overview.html" ]]; then
    xdg-open "${OUT_DIR}/Overview.html" >/dev/null 2>&1 || true
  fi
else
  echo
  echo "Note: xdg-open not found; open the folder manually."
fi
