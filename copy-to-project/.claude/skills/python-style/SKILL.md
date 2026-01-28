---
name: python-style
description: Соблюдение Python стиля (Google style guide) и ОБЯЗАТЕЛЬНОЕ использование ruff.
hooks:
  onComplete: |
    ruff format . && ruff check .
permissions:
  - "Bash(ruff*)"
---

# Python Style

При написании Python кода следуй Google Python Style Guide.

## ОБЯЗАТЕЛЬНЫЙ workflow

После **КАЖДОГО** изменения Python файла:

```bash
# ШАГ 1: Форматирование
ruff format <file>

# ШАГ 2: Проверка и авто-исправление
ruff check <file> --fix

# ШАГ 3: Финальная проверка
ruff check <file>
```

## Инструменты

```bash
# Форматирование
ruff format <file>

# Линтинг
ruff check <file>

# Типы
mypy <file>
```

## Основные правила

### Именование

- `snake_case` для функций и переменных
- `PascalCase` для классов
- `UPPER_CASE` для констант
- `_private` для приватных членов

### Документация

```python
def function(arg: str) -> int:
    """Краткое описание.

    Args:
        arg: Описание аргумента.

    Returns:
        Описание возвращаемого значения.

    Raises:
        ValueError: Когда возникает.
    """
```

### Импорты

```python
# Стандартная библиотека
import os
import sys

# Сторонние пакеты
import requests

# Локальные модули
from .module import function
```

### Type hints

```python
from typing import Optional, List, Dict

def process(items: List[str]) -> Dict[str, int]:
    ...
```

## Ограничения

- Максимальная длина строки: 88 символов (ruff default)
- Всегда использовать type hints для public API

## ЗАПРЕЩЕНО

- Коммитить код без прохождения `ruff check`
- Игнорировать ошибки ruff без явной причины
- Использовать `# noqa` без комментария-обоснования
