---
name: python-style
description: Python стиль (Google style guide) и обязательное использование ruff. Активируй при работе с Python кодом.
hooks:
  onComplete: |
    ruff format . && ruff check . --fix
permissions:
  - "Bash(ruff*)"
---

## Обязательный workflow

После **КАЖДОГО** изменения Python файла:

```bash
ruff format <file>
ruff check <file> --fix
```

## Стиль (Google Python Style Guide)

### Именование
- `snake_case` — функции, переменные
- `PascalCase` — классы
- `UPPER_CASE` — константы

### Импорты
```python
import os              # 1. Стандартная библиотека
import requests        # 2. Сторонние пакеты
from .module import x  # 3. Локальные модули
```

### Type hints
```python
def process(items: list[str]) -> dict[str, int]:
    """Краткое описание.

    Args:
        items: Описание аргумента.

    Returns:
        Описание возвращаемого значения.
    """
```

## Запрещено

- Коммитить без `ruff check`
- `# noqa` без комментария-обоснования
