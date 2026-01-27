#!/usr/bin/env python3
"""
auto_format.py — PostToolUse hook

Автоматически форматирует файлы после изменений.
Поддерживает: Python, JSON, Markdown, SQL, YAML, JS/TS.
"""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# State хранится в проекте, не в домашней директории
AUDIT_PATH = Path.cwd() / ".claude" / "state" / "hook_audit.log"

# Директории для пропуска
SKIP_PATTERNS = [
    "venv/",
    ".venv/",
    "__pycache__/",
    ".pytest_cache/",
    "node_modules/",
    ".git/",
    "dist/",
    "build/",
    ".mypy_cache/",
]

# Форматтеры по расширению файла
# Формат: extension -> (command_parts, tool_name, install_hint)
FORMATTERS: dict[str, tuple[list[str], str, str]] = {
    # Python
    ".py": (["ruff", "format", "{file}"], "ruff", "pip install ruff"),
    # JSON - используем Python json.tool для универсальности
    ".json": (["python", "-m", "json.tool", "{file}"], "json.tool", "built-in"),
    # Markdown - prettier если есть
    ".md": (["prettier", "--write", "{file}"], "prettier", "npm install -g prettier"),
    # YAML
    ".yaml": (["prettier", "--write", "{file}"], "prettier", "npm install -g prettier"),
    ".yml": (["prettier", "--write", "{file}"], "prettier", "npm install -g prettier"),
    # SQL - sqlfluff
    ".sql": (["sqlfluff", "fix", "--force", "{file}"], "sqlfluff", "pip install sqlfluff"),
    # JavaScript/TypeScript - prettier
    ".js": (["prettier", "--write", "{file}"], "prettier", "npm install -g prettier"),
    ".ts": (["prettier", "--write", "{file}"], "prettier", "npm install -g prettier"),
    ".jsx": (["prettier", "--write", "{file}"], "prettier", "npm install -g prettier"),
    ".tsx": (["prettier", "--write", "{file}"], "prettier", "npm install -g prettier"),
}

# Кэш доступных инструментов
_tool_cache: dict[str, bool] = {}


def _audit(msg: str) -> None:
    """Записывает событие в audit log."""
    AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().isoformat(timespec="seconds")
    with AUDIT_PATH.open("a", encoding="utf-8") as f:
        f.write(f"{ts} auto_format: {msg}\n")


def _read_stdin_json() -> dict[str, Any]:
    """Читает JSON из stdin."""
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            return {}
        return json.loads(raw)
    except Exception as e:
        _audit(f"ERROR reading stdin: {e}")
        return {}


def _extract_file_path(payload: dict[str, Any]) -> str:
    """Извлекает путь к файлу из payload."""
    tool_input = payload.get("tool_input") or {}
    return str(tool_input.get("file_path") or tool_input.get("filePath") or "")


def _is_tool_available(tool_name: str) -> bool:
    """Проверяет доступность инструмента."""
    if tool_name in _tool_cache:
        return _tool_cache[tool_name]

    # json.tool всегда доступен
    if tool_name == "json.tool":
        _tool_cache[tool_name] = True
        return True

    try:
        subprocess.run(
            [tool_name, "--version"],
            capture_output=True,
            timeout=5,
        )
        _tool_cache[tool_name] = True
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        _tool_cache[tool_name] = False
        return False


def _should_format(file_path: str) -> tuple[bool, str]:
    """
    Проверяет, нужно ли форматировать файл.
    Возвращает (should_format, extension).
    """
    if not file_path:
        return False, ""

    path = Path(file_path)

    # Проверяем существование
    if not path.exists():
        return False, ""

    # Получаем расширение
    ext = path.suffix.lower()
    if ext not in FORMATTERS:
        return False, ext

    # Пропускаем определённые директории
    normalized = file_path.replace("\\", "/")
    for pattern in SKIP_PATTERNS:
        if pattern in normalized:
            return False, ext

    return True, ext


def _format_json_inplace(file_path: str) -> tuple[bool, str]:
    """Форматирует JSON файл in-place (json.tool пишет в stdout)."""
    try:
        path = Path(file_path)
        content = path.read_text(encoding="utf-8")
        formatted = json.dumps(json.loads(content), indent=2, ensure_ascii=False)
        path.write_text(formatted + "\n", encoding="utf-8")
        return True, f"Formatted JSON: {file_path}"
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"
    except Exception as e:
        return False, f"JSON format error: {e}"


def _format_file(file_path: str, ext: str) -> tuple[bool, str]:
    """Форматирует файл соответствующим инструментом."""
    if ext not in FORMATTERS:
        return False, f"No formatter for {ext}"

    cmd_template, tool_name, install_hint = FORMATTERS[ext]

    # Проверяем доступность инструмента
    if not _is_tool_available(tool_name):
        return False, f"{tool_name} not found - install: {install_hint}"

    # Особый случай для JSON - используем встроенный форматтер
    if ext == ".json":
        return _format_json_inplace(file_path)

    # Формируем команду
    cmd = [part.replace("{file}", file_path) for part in cmd_template]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0:
            return True, f"Formatted ({tool_name}): {file_path}"
        else:
            error_msg = result.stderr or result.stdout or "Unknown error"
            # Некоторые инструменты возвращают non-zero даже при успехе
            # Проверяем stderr на реальные ошибки
            if "error" in error_msg.lower() or "failed" in error_msg.lower():
                return False, f"Format failed: {error_msg[:200]}"
            return True, f"Formatted ({tool_name}): {file_path}"

    except FileNotFoundError:
        _tool_cache[tool_name] = False
        return False, f"{tool_name} not found - install: {install_hint}"
    except subprocess.TimeoutExpired:
        return False, f"Format timeout: {file_path}"
    except Exception as e:
        return False, f"Format error: {e}"


def main() -> int:
    """Основная логика хука."""
    payload = _read_stdin_json()
    file_path = _extract_file_path(payload)

    should_format, ext = _should_format(file_path)

    if not should_format:
        if ext:
            _audit(f"SKIP ({ext}): {file_path}")
        else:
            _audit(f"SKIP: {file_path or '(unknown)'}")
        print("OK")
        return 0

    success, message = _format_file(file_path, ext)

    if success:
        _audit(f"FORMATTED: {file_path}")
        print(message)
    else:
        _audit(f"FAILED: {message}")
        # Не выводим ошибку в stderr для отсутствующих инструментов
        # чтобы не пугать пользователя
        if "not found" in message:
            print(f"SKIP (tool unavailable): {file_path}")
        else:
            print(message, file=sys.stderr)

    # Всегда возвращаем 0 — не блокируем при ошибке форматирования
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
