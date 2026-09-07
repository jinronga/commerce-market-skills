#!/usr/bin/env python3
"""Check local prerequisites without reading or printing credential values."""

from __future__ import annotations

import json
import platform
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "resources" / "config.json"


def configured() -> bool:
    if not CONFIG.exists():
        return False
    try:
        data = json.loads(CONFIG.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return False
    placeholders = {"", "your_app_key_here", "your_app_secret_here"}
    return str(data.get("app_key", "")).strip() not in placeholders and str(data.get("app_secret", "")).strip() not in placeholders


def state(name: str, ok: bool, remedy: str = "") -> bool:
    print(f"{'OK' if ok else 'MISSING'}  {name}{'' if ok else ': ' + remedy}")
    return ok


def main() -> int:
    checks = [
        state("Python 3.10+", sys.version_info >= (3, 10), "install Python 3.10 or newer"),
        state("Miaoshou config", configured(), "copy resources/config.json.example to resources/config.json and fill your own credentials"),
    ]
    is_macos = platform.system() == "Darwin"
    checks.append(state("macOS Chrome upload support", is_macos and Path("/Applications/Google Chrome.app").exists(), "direct Chrome upload is bundled for macOS with Google Chrome"))
    checks.append(state("osascript", bool(shutil.which("osascript")) if is_macos else False, "required by the macOS Chrome upload adapter"))
    print("\nSecurity: credentials and browser login are user-specific and are never copied into this skill.")
    return 0 if all(checks[:2]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
