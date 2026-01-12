---
description: Draft commit message and perform safe commit steps
argument-hint: "[message]"
allowed-tools: [Bash, Read, Glob, Grep]
---
Prepare a commit for the current changes.

Steps:
- Review git status and diff.
- Draft a concise message that matches repo conventions.
- If a message was provided, use it; otherwise propose one.
- Only commit when user explicitly confirms.

Message: $ARGUMENTS
