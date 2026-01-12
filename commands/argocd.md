---
description: Safe argocd CLI wrapper with guarded mutations
argument-hint: "<argocd args>"
allowed-tools: [Bash]
---
Use argocd CLI with safety checks.

Rules:
- Default to read-only commands (app list, app get, app diff).
- For mutating commands (app sync, app delete), ask for explicit confirmation and echo the exact command before running.
- Never use eval. Pass arguments directly.

Args: $ARGUMENTS
