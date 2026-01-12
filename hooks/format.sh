#!/usr/bin/env bash
set -euo pipefail

file_path="${1:-}"
if [ -z "$file_path" ]; then
  exit 0
fi

# Run prettier if available for JS/TS files.
if [[ "$file_path" =~ \.(js|jsx|ts|tsx)$ ]]; then
  if command -v prettier >/dev/null 2>&1; then
    prettier --write "$file_path" >/dev/null 2>&1 || true
  fi
fi
