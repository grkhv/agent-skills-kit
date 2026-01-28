---
name: test-runner
description: Обязательный запуск тестов после изменений кода.
---

# Test Runner

## ОБЯЗАТЕЛЬНОЕ правило

После **ЛЮБОГО** изменения кода (не docs) ты **ОБЯЗАН** запустить тесты:

```bash
python -m pytest tests/ -v --tb=short
```

Или используй субагента:
```
Task(subagent_type: "Bash", prompt: "ruff check . && pytest tests/ -v")
```

## Полезные команды

```bash
# Быстрая проверка
pytest tests/ -v --tb=short

# С coverage
pytest tests/ --cov=src --cov-report=term

# Конкретный тест
pytest tests/test_module.py::test_function -v

# Только failed
pytest tests/ --lf

# Параллельно (если установлен pytest-xdist)
pytest tests/ -n auto
```

## Workflow после изменений

1. Сделал изменения в коде
2. Запустил ruff (обязательно)
3. Запустил тесты (обязательно)
4. Если тесты падают → исправь → повтори

```bash
# Минимальный обязательный pipeline
ruff check . && pytest tests/ -v
```

## Интеграция с CI

Перед коммитом убедись что локально проходит:

```bash
make check
# или
ruff format . && ruff check . && pytest tests/ -v && mypy src/
```

## Использование субагентов

После изменений запускай параллельную валидацию:

```
// Все три запускаются параллельно
Task(subagent_type: "Bash", prompt: "Run mypy on src/")
Task(subagent_type: "Bash", prompt: "Run ruff check on src/")
Task(subagent_type: "Bash", prompt: "Run pytest with coverage")
```

## ЗАПРЕЩЕНО

- Коммитить код без запуска тестов
- Игнорировать падающие тесты
- Удалять тесты чтобы они не падали (без явной причины)
