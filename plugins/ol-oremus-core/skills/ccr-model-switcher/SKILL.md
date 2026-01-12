---
name: ccr-model-switcher
description: List Claude Code Router (CCR) models and guide switching the active model for Claude Code sessions. Use when the user asks “what models can I use”, “what models are available”, “list models”, “show models”, “available models”, “model list”, “model options/choices”, “which model should I use”, switch/change models, set a default model, or troubleshoot model selection with claude-code-router.
---

# CCR Model Switcher

## Overview

List models configured in claude-code-router and switch the active model for Claude Code sessions. Use the scripts in scripts/ to list models and set the default model for future sessions; use /model for the current session.

## Quick start

1. List models: `python3 /home/sbuglione/.claude/skills/ccr-model-switcher/scripts/list_models.py`
2. Switch current session: ask the user to run `/model provider,model`
3. Set default for future sessions: `python3 scripts/set_default_model.py provider,model`

## Tasks

### List available models

- Run `python3 /home/sbuglione/.claude/skills/ccr-model-switcher/scripts/list_models.py`.
- Report provider names, model IDs, and the copy-paste `provider,model` strings.
- Include the current Router default and `~/.claude/settings.json` model if present.

### Switch model for the current session

- Tell the user to run `/model provider,model`.
- Remind that the built-in model picker only shows Anthropic models; custom models must be typed.
- Do not edit config files unless asked; this applies only to the active session.

### Set default model for new sessions

- Ask for the target `provider,model`.
- Run `python3 scripts/set_default_model.py provider,model`.
- Tell the user to restart Claude Code or open a new session to apply the change.

### Optional verification

- If model requests fail, check router status with `ccr status`.
- If models are missing, confirm `~/.claude-code-router/config.json` has the provider and models.

## Resources

### scripts/

- `list_models.py` - Print providers/models and default model values.
- `set_default_model.py` - Update `~/.claude/settings.json` model.
