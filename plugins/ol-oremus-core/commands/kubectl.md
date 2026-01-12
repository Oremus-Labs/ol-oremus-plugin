---
description: Safe kubectl wrapper for read-only and guarded mutations
argument-hint: "<kubectl args>"
allowed-tools: [Bash]
---
Use kubectl with safety checks.

Rules:
- Default to read-only commands (get, describe, logs).
- For mutating commands (apply, delete, patch, scale, rollout restart), ask for explicit confirmation and echo the exact command before running.
- Never use eval. Pass arguments directly.

Args: $ARGUMENTS
