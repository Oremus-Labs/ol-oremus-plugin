---
description: Run project tests or lint with guidance
argument-hint: "[command]"
allowed-tools: [Bash, Read, Glob, Grep]
---
If a command is provided, run it. Otherwise, detect common test or lint commands and run the best match.

Preferred order:
1) package.json scripts (test, lint, typecheck)
2) make test / make lint
3) pytest / go test / cargo test

Command: $ARGUMENTS
