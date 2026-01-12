---
description: Show how to inject secrets with 1Password CLI for MCP
argument-hint: ""
---
Use 1Password CLI to inject secrets at runtime (no secrets committed):

1) Create an env file locally (gitignored):
   GITHUB_PAT=op://<vault>/<item>/<field>

2) Run Claude Code (or your MCP host) with op:
   op run --env-file=.env -- claude

3) The MCP config reads Authorization from ${GITHUB_PAT}.
   - op injects the real token value into GITHUB_PAT at runtime.
