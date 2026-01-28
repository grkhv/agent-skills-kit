#!/usr/bin/env python3
"""
enforce_subagent_tests.py — Stop hook

Блокирует завершение если были изменения кода, но тесты не запускались.
Работает совместно с shell_guard.py который отмечает запуск тестов.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

# State хранится в проекте, не в домашней директории
STATE_PATH = Path.cwd() / ".claude" / "state" / "hook_state.json"
AUDIT_PATH = Path.cwd() / ".claude" / "state" / "hook_audit.log"

# Если тесты запускались менее N минут назад — считаем OK
TEST_FRESHNESS_MINUTES = 30


def _audit(msg: str) -> None:
    """Записывает событие в audit log."""
    AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().isoformat(timespec="seconds")
    with AUDIT_PATH.open("a", encoding="utf-8") as f:
        f.write(f"{ts} enforce_subagent_tests: {msg}\n")


def _read_state() -> dict[str, Any]:
    """Читает состояние из файла."""
    if not STATE_PATH.exists():
        return {}
    try:
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _has_dirty_files(state: dict[str, Any]) -> bool:
    """Проверяет, были ли изменения кода (отмечаются mark_dirty.py)."""
    dirty = state.get("dirty_files", [])
    return len(dirty) > 0


def _has_recent_test(state: dict[str, Any], now: datetime) -> bool:
    """Проверяет, запускались ли тесты недавно."""
    last_test = state.get("last_test_utc")
    if not last_test:
        return False

    try:
        test_time = datetime.fromisoformat(last_test.replace("Z", "+00:00"))
        # Убираем timezone для сравнения
        test_time = test_time.replace(tzinfo=None)
        return (now - test_time) <= timedelta(minutes=TEST_FRESHNESS_MINUTES)
    except Exception:
        return False


def main() -> int:
    """Основная логика хука."""
    now = datetime.utcnow()
    state = _read_state()

    # Если нет изменений — пропускаем
    if not _has_dirty_files(state):
        _audit("ALLOW (no dirty files)")
        print("OK")
        return 0

    # Если тесты запускались недавно — пропускаем
    if _has_recent_test(state, now):
        _audit("ALLOW (recent test found)")
        print("OK")
        return 0

    # Есть изменения, но тесты не запускались
    _audit("BLOCK (no recent test after code changes)")
    print(
        "WARNING: Код был изменён, но тесты НЕ запускались!\n\n"
        "Запусти тесты перед завершением:\n"
        "  pytest tests/ -v\n"
        "  # или\n"
        "  make check\n\n"
        "Или используй субагента:\n"
        '  Task(subagent_type: "Bash", prompt: "pytest tests/ -v")\n',
        file=sys.stderr,
    )
    # Возвращаем 0 чтобы не блокировать полностью, но предупреждаем
    # Если хотим жёстко блокировать — изменить на return 2
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
