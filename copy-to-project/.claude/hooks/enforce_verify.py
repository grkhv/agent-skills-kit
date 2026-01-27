#!/usr/bin/env python3
"""
enforce_verify.py — Stop hook

Требует верификацию перед остановкой если были изменения.
Проверяет что last_verify_utc >= last_edit_utc.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# State хранится в проекте, не в домашней директории
STATE_PATH = Path.cwd() / ".claude" / "state" / "hook_state.json"
AUDIT_PATH = Path.cwd() / ".claude" / "state" / "hook_audit.log"


def _audit(msg: str) -> None:
    """Записывает событие в audit log."""
    AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().isoformat(timespec="seconds")
    with AUDIT_PATH.open("a", encoding="utf-8") as f:
        f.write(f"{ts} enforce_verify: {msg}\n")


def _read_state() -> dict[str, Any]:
    """Читает состояние из файла."""
    if not STATE_PATH.exists():
        return {}
    try:
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _parse_utc(ts: str | None) -> datetime | None:
    """Парсит UTC timestamp."""
    if not ts:
        return None
    try:
        if ts.endswith("Z"):
            return datetime.fromisoformat(ts[:-1]).replace(tzinfo=timezone.utc)
        return datetime.fromisoformat(ts)
    except Exception:
        return None


def main() -> int:
    """Основная логика хука."""
    state = _read_state()
    dirty = bool(state.get("dirty"))

    if not dirty:
        _audit("ALLOW (not dirty)")
        return 0

    last_edit = _parse_utc(state.get("last_edit_utc"))
    last_verify = _parse_utc(state.get("last_verify_utc"))

    verified_after_edit = False
    if last_edit and last_verify:
        verified_after_edit = last_verify >= last_edit

    if not verified_after_edit:
        touched = state.get("touched_files") or []
        touched_preview = "\n".join(f"- {p}" for p in touched[-10:]) if touched else "(unknown files)"

        _audit("BLOCK (dirty without verify)")
        print(
            "BLOCKED: Changes detected but verification not run after last edit.\n\n"
            "Do this before stopping:\n"
            "  1) Run verification (preferred): make check\n"
            "     If no Makefile: pytest + ruff + mypy (as applicable)\n"
            "  2) Provide lock-in summary in chat:\n"
            "     - What changed\n"
            "     - How verified (commands + result)\n"
            "     - Tests/ADR added (paths)\n\n"
            f"Touched files (recent):\n{touched_preview}",
            file=sys.stderr,
        )
        return 2

    # Верификация была — очищаем dirty
    state["dirty"] = False
    state["touched_files"] = []
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    _audit("ALLOW (verified) and cleared dirty")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
