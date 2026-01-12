#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"ERROR: Failed to parse JSON: {path} ({exc})\n")
        raise SystemExit(1)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Set Claude Code default model in ~/.claude/settings.json"
    )
    parser.add_argument(
        "model",
        help="Model in provider,model format (e.g. local,qwen3-coder-30b-q4k-xl)",
    )
    args = parser.parse_args()

    if "," not in args.model:
        sys.stderr.write("ERROR: model must be in provider,model format\n")
        return 2

    settings_path = Path.home() / ".claude" / "settings.json"
    settings_path.parent.mkdir(parents=True, exist_ok=True)
    settings = load_json(settings_path)
    settings["model"] = args.model
    settings_path.write_text(json.dumps(settings, indent=2) + "\n")

    print(f"Updated {settings_path} model to: {args.model}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
