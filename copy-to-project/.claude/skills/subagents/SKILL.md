---
name: subagents
description: Субагенты для параллельных задач, тестирования и исследования. Только Claude Code.
---

Claude Code поддерживает субагентов через `Task`. Используй для параллельных операций.

## Типы субагентов

| subagent_type | Назначение |
|---------------|------------|
| `Bash` | Выполнение команд |
| `Explore` | Исследование кодовой базы (Glob, Grep, Read) |
| `Plan` | Планирование (без Edit/Write) |
| `general-purpose` | Многошаговые задачи (все инструменты) |

## Обязательно после изменений

```
Task(subagent_type: "Bash", prompt: "ruff check . && pytest tests/ -v")
```

Или параллельно:
```
Task(subagent_type: "Bash", prompt: "ruff check .")
Task(subagent_type: "Bash", prompt: "pytest tests/")
Task(subagent_type: "Bash", prompt: "mypy src/")
```

## Паттерны

**Explore → Plan → Execute**:
```
Task(Explore, "Find all usages of auth module")
→ анализ → правки
```

**Parallel Validation**:
```
// В одном сообщении — выполнятся параллельно
Task(Bash, "pytest")
Task(Bash, "mypy .")
Task(Bash, "ruff check .")
```

## Правила

- `Explore` для поиска, `Bash` для команд
- Независимые задачи запускай параллельно
- `run_in_background: true` для долгих операций
- Субагенты не видят контекст — давай полный промпт
