#!/usr/bin/env python3
"""
mark_dirty.py — PostToolUse hook

Отмечает файлы как изменённые после Edit/Write.
Состояние сохраняется в .claude/state/ проекта.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
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
        f.write(f"{ts} mark_dirty: {msg}\n")


def _read_state() -> dict[str, Any]:
    """Читает состояние из файла."""
    if not STATE_PATH.exists():
        return {}
    try:
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _write_state(state: dict[str, Any]) -> None:
    """Записывает состояние в файл."""
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(
        json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def _read_stdin_json() -> dict[str, Any]:
    """Читает JSON из stdin."""
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            return {}
        return json.loads(raw)
    except Exception:
        return {}


def _extract_file_path(payload: dict[str, Any]) -> str:
    """Извлекает путь к файлу из payload."""
    tool_input = payload.get("tool_input") or {}
    fp = tool_input.get("file_path") or tool_input.get("filePath") or ""
    return str(fp).replace("\\", "/")


def main() -> int:
    """Основная логика хука."""
    payload = _read_stdin_json()
    fp = _extract_file_path(payload)

    # Пропускаем файлы конфигурации Claude
    if fp and ".claude/" in fp:
        _audit(f"SKIP (Claude config): {fp}")
        print("OK")
        return 0

    state = _read_state()
    state["dirty"] = True
    state["last_edit_utc"] = datetime.utcnow().isoformat(timespec="seconds") + "Z"

    if fp:
        touched = state.get("touched_files") or []
        if fp not in touched:
            touched.append(fp)
        state["touched_files"] = touched[-50:]  # Ограничение

    _write_state(state)
    _audit(f"DIRTY set; file={fp or '(unknown)'}")
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
