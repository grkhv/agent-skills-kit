---
name: python-style
description: Соблюдение Python стиля (Google style guide) и автоматическое форматирование.
---

# Python Style

При написании Python кода следуй Google Python Style Guide.

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
