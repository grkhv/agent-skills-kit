---
paths:
  - "**/*.py"
---

# Python: стиль и ruff

## Обязательный workflow

После **КАЖДОГО** изменения Python файла:

```bash
ruff format <file>
ruff check <file> --fix
```

## Стиль (Google Python Style Guide)

- `snake_case` — функции, переменные
- `PascalCase` — классы
- `UPPER_CASE` — константы
- Type hints для public API

## Импорты

```python
# 1. Стандартная библиотека
import os

# 2. Сторонние пакеты
import requests

# 3. Локальные модули
from .module import function
```

## Запрещено

- Коммитить без `ruff check`
- `# noqa` без комментария-обоснования
