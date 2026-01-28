---
name: ruff-enforcer
description: Принудительное использование ruff для всего Python кода.
---

# Ruff Enforcer

Этот skill обеспечивает **принудительное** использование ruff для форматирования и проверки Python кода.

## Обязательный workflow

После **КАЖДОГО** изменения Python файла:

```bash
# ШАГ 1: Форматирование
ruff format <file>

# ШАГ 2: Проверка и авто-исправление
ruff check <file> --fix

# ШАГ 3: Финальная проверка
ruff check <file>
```

## Полезные команды

```bash
# Проверить правило
ruff rule <code>

# Показать все нарушения с объяснением
ruff check --show-fixes

# Игнорировать конкретное правило (только если необходимо)
# noqa: <code>
```

## Конфигурация (pyproject.toml)

```toml
[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]
ignore = []

[tool.ruff.lint.isort]
known-first-party = ["src"]
```

## ЗАПРЕЩЕНО

- Коммитить код без прохождения `ruff check`
- Игнорировать ошибки ruff без явной причины
- Использовать `# noqa` без комментария-обоснования
