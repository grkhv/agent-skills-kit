#!/usr/bin/env python3
"""
shell_guard.py — PreToolUse hook

Блокирует опасные shell-команды и доступ к секретам.
Также отмечает команды верификации для enforce_verify hook.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# State хранится в проекте, не в домашней директории
STATE_PATH = Path.cwd() / ".claude" / "state" / "hook_state.json"
AUDIT_PATH = Path.cwd() / ".claude" / "state" / "hook_audit.log"

# Команды верификации
VERIFY_PATTERNS = [
    r"\bmake\s+check\b",
    r"\bjust\s+check\b",
    r"\bpytest\b",
    r"\bpython\s+-m\s+pytest\b",
    r"\bruff\s+check\b",
    r"\bruff\s+format\b",
    r"\bblack\b",
    r"\bmypy\b",
    r"\bpre-commit\s+run\b",
]

# Опасные команды (полный запрет)
DANGEROUS_PATTERNS = [
    r"\brm\s+-rf\s+[/~]",
    r"\brm\s+-r[fF]\s+[/~]",
    r"\bdel\s+/s\b",
    r"\brmdir\s+/s\b",
    r"\bformat\s+([a-z]:)?\b",
    r"\bmkfs(\.|_)?\b",
    r":\(\)\s*\{\s*:\|\:\&\s*\}\s*;\s*:",  # Fork bomb
    r"\bshutdown\b",
    r"\breboot\b",
    r"\bpoweroff\b",
    r"\bsudo\b",
]

# Чувствительные пути (требуют подтверждения)
SENSITIVE_PATH_HINTS = [
    r"\.env\b",
    r"\.ssh\b",
    r"\bid_rsa\b",
    r"\bknown_hosts\b",
]


def _audit(msg: str) -> None:
    """Записывает событие в audit log."""
    AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().isoformat(timespec="seconds")
    with AUDIT_PATH.open("a", encoding="utf-8") as f:
        f.write(f"{ts} shell_guard: {msg}\n")


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
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def _read_stdin_json() -> dict[str, Any]:
    """Читает JSON из stdin."""
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            return {}
        return json.loads(raw)
    except Exception:
        return {}


def _extract_command(payload: dict[str, Any]) -> str:
    """Извлекает команду из payload."""
    tool_input = payload.get("tool_input") or {}
    return str(tool_input.get("command", ""))


def _looks_like_verify(cmd: str) -> bool:
    """Проверяет, является ли команда верификацией."""
    for pat in VERIFY_PATTERNS:
        if re.search(pat, cmd):
            return True
    return False


def _is_dangerous(cmd: str) -> str | None:
    """Возвращает паттерн опасной команды или None."""
    c = cmd.lower()
    for pat in DANGEROUS_PATTERNS:
        if re.search(pat, c):
            return pat
    return None


def _mentions_sensitive_paths(cmd: str) -> str | None:
    """Возвращает паттерн чувствительного пути или None."""
    c = cmd.lower()
    for pat in SENSITIVE_PATH_HINTS:
        if re.search(pat, c):
            return pat
    return None


def main() -> int:
    """Основная логика хука."""
    payload = _read_stdin_json()
    cmd = _extract_command(payload)

    if not cmd.strip():
        _audit("ALLOW (no command)")
        print("OK")
        return 0

    # Проверка на опасные команды
    danger_pat = _is_dangerous(cmd)
    if danger_pat:
        _audit(f"BLOCK dangerous={danger_pat} cmd={cmd!r}")
        print(f"BLOCKED: Unsafe command pattern: {danger_pat}\nCommand: {cmd}", file=sys.stderr)
        return 2

    # Проверка на чувствительные пути
    sensitive_pat = _mentions_sensitive_paths(cmd)
    if sensitive_pat:
        if "I_KNOW_WHAT_IM_DOING" not in cmd:
            _audit(f"BLOCK sensitive={sensitive_pat} cmd={cmd!r}")
            print(
                f"BLOCKED: Command touches sensitive material (env/ssh/secrets).\n"
                f"Matched: {sensitive_pat}\n"
                "If intentional, re-run with suffix: I_KNOW_WHAT_IM_DOING",
                file=sys.stderr,
            )
            return 2

    # Отмечаем верификацию
    if _looks_like_verify(cmd):
        state = _read_state()
        state["last_verify_utc"] = datetime.utcnow().isoformat(timespec="seconds") + "Z"
        _write_state(state)
        _audit(f"MARK verify cmd={cmd!r}")
    else:
        _audit(f"ALLOW cmd={cmd!r}")

    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
