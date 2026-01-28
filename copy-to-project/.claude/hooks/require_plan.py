#!/usr/bin/env python3
"""
require_plan.py — PreToolUse hook

Требует наличия плана перед изменениями кода.
Блокирует Edit/Write если нет PLAN.md или docs/notes/plan-*.md.
"""

from __future__ import annotations

import glob
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

# ---- Конфигурация ----
PLAN_TTL_HOURS = 72
ALLOW_WITHOUT_PLAN_PREFIXES = ("docs/", "tests/")
ALSO_ALLOW_FILES = ("README.md",)
# State хранится в проекте, не в домашней директории
AUDIT_PATH = Path.cwd() / ".claude" / "state" / "hook_audit.log"


# ---- Вспомогательные функции ----
def _audit(msg: str) -> None:
    """Записывает событие в audit log."""
    AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().isoformat(timespec="seconds")
    with AUDIT_PATH.open("a", encoding="utf-8") as f:
        f.write(f"{ts} require_plan: {msg}\n")


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


def _has_recent_plan(now: datetime) -> bool:
    """Проверяет наличие актуального плана."""
    if Path("PLAN.md").exists():
        return True

    plans = sorted(glob.glob("docs/notes/plan-*.md"))
    if not plans:
        return False

    newest = max(plans, key=lambda p: Path(p).stat().st_mtime)
    mtime = datetime.fromtimestamp(Path(newest).stat().st_mtime)
    return (now - mtime) <= timedelta(hours=PLAN_TTL_HOURS)


def _is_doc_or_test_change(file_path: str) -> bool:
    """Проверяет, является ли изменение docs/tests."""
    if not file_path:
        return False
    if file_path in ALSO_ALLOW_FILES:
        return True
    return file_path.startswith(ALLOW_WITHOUT_PLAN_PREFIXES)


def main() -> int:
    """Основная логика хука."""
    now = datetime.now()
    payload = _read_stdin_json()
    file_path = _extract_file_path(payload)

    # Docs/tests разрешены без плана
    if _is_doc_or_test_change(file_path):
        _audit(f"ALLOW docs/tests: {file_path or '(unknown)'}")
        print("OK")
        return 0

    # Проверяем наличие плана
    if _has_recent_plan(now):
        _audit(f"ALLOW (plan found): {file_path or '(unknown)'}")
        print("OK")
        return 0

    # Нет плана — блокируем
    _audit(f"BLOCK (no plan): {file_path or '(unknown)'}")
    print(
        "BLOCKED: No saved plan found.\n\n"
        "ТЫ ОБЯЗАН сохранить план в ФАЙЛ:\n"
        "  - docs/notes/plan-YYYYMMDD-<topic>.md (ПРЕДПОЧТИТЕЛЬНО)\n"
        "  - PLAN.md (для быстрых задач)\n\n"
        "План ОБЯЗАН содержать:\n"
        "  1. Цель (1-2 предложения)\n"
        "  2. Границы (файлы для изменения, файлы не трогать)\n"
        "  3. Риски (2-5 пунктов)\n"
        "  4. Шаги (6-12 шагов)\n"
        "  5. Команда верификации\n\n"
        "НЕ ДЕРЖИ ПЛАН ТОЛЬКО В ПАМЯТИ РАЗГОВОРА!\n"
        "Сохрани план в файл, затем повтори операцию.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
