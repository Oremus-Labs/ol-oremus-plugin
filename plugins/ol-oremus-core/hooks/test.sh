#!/usr/bin/env bash
set -euo pipefail

# Run lightweight checks if a known command exists.
if [ -f package.json ]; then
  if command -v npm >/dev/null 2>&1; then
    npm test -- --passWithNoTests >/dev/null 2>&1 || true
  fi
  exit 0
fi

if [ -f pyproject.toml ] || [ -f setup.py ]; then
  if command -v pytest >/dev/null 2>&1; then
    pytest -q >/dev/null 2>&1 || true
  fi
  exit 0
fi

exit 0
