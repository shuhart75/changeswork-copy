#!/bin/bash
# Simple conflict checker for v6

GANTT_FILE="planning/mvp/current/gantt/mvp_gantt_chart_current.puml"

if [[ ! -f "$GANTT_FILE" ]]; then
  echo "Gantt file not found: $GANTT_FILE" >&2
  exit 2
fi

echo "=== Checking A1 sequence ==="
grep "on {A1}" "$GANTT_FILE" | grep -E "^\[" | head -10

echo ""
echo "=== Checking A2 sequence ==="
grep "on {A2}" "$GANTT_FILE" | grep -E "^\[" | head -10

echo ""
echo "=== Checking B1 sequence ==="
grep "on {B1}" "$GANTT_FILE" | grep -E "^\[" | head -10

echo ""
echo "=== Checking F2 sequence ==="
grep "on {F2}" "$GANTT_FILE" | grep -E "^\[" | head -10
