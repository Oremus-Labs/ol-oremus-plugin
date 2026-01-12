#!/usr/bin/env python3
import json
import sys
from pathlib import Path


def load_json(path: Path):
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"ERROR: Failed to parse JSON: {path} ({exc})\n")
        return None


def main() -> int:
    home = Path.home()
    cfg_path = home / ".claude-code-router" / "config.json"
    settings_path = home / ".claude" / "settings.json"

    cfg = load_json(cfg_path)
    if not cfg:
        sys.stderr.write(f"ERROR: Missing or invalid config: {cfg_path}\n")
        return 1

    providers = cfg.get("Providers") or []
    router = cfg.get("Router") or {}
    settings = load_json(settings_path) or {}

    print("Models by provider:")
    for provider in providers:
        name = provider.get("name") or "unknown"
        models = provider.get("models") or []
        print(f"- {name}")
        for model in models:
            print(f"  - {model}")
        if models:
            print("  full names:")
            for model in models:
                print(f"  - {name},{model}")

    router_default = router.get("default")
    if router_default:
        print(f"\nRouter default: {router_default}")

    settings_model = settings.get("model")
    if settings_model:
        print(f"Claude Code default: {settings_model}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
