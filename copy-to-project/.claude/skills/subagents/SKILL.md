---
name: subagents
description: Используй субагентов для параллельных задач, тестирования и исследования. Только для Claude Code.
---

Claude Code поддерживает субагентов через инструмент `Task`. Используй их для параллельных операций.

## Доступные типы субагентов

| subagent_type | Назначение | Инструменты |
|---------------|------------|-------------|
| `Bash` | Выполнение команд | Bash |
| `general-purpose` | Многошаговые задачи | Все |
| `Explore` | Исследование кодовой базы | Glob, Grep, Read |
| `Plan` | Планирование реализации | Все кроме Edit/Write |

## Когда использовать субагентов

### 1. Параллельный запуск тестов

Если нужно проверить несколько вещей одновременно:

```
Task(
  subagent_type: "Bash",
  description: "Run unit tests",
  prompt: "Run pytest tests/unit/ and report results"
)

Task(
  subagent_type: "Bash",
  description: "Run integration tests",
  prompt: "Run pytest tests/integration/ and report results"
)
```

### 2. Исследование перед изменениями

Перед правками — исследуй кодовую базу:

```
Task(
  subagent_type: "Explore",
  description: "Find auth usage",
  prompt: "Find all files that import or use the auth module. List file paths and usage patterns."
)
```

### 3. Параллельная валидация

После изменений — проверь разные аспекты параллельно:

```
// Запускаем в одном сообщении для параллельного выполнения
Task(subagent_type: "Bash", prompt: "Run type checker: mypy src/")
Task(subagent_type: "Bash", prompt: "Run linter: ruff check src/")
Task(subagent_type: "Bash", prompt: "Run tests: pytest")
```

### 4. Фоновое выполнение

Для длинных операций — запуск в фоне:

```
Task(
  subagent_type: "Bash",
  description: "Build project",
  prompt: "Run full build: npm run build",
  run_in_background: true
)
```

Результат можно проверить позже через `TaskOutput`.

## Паттерны использования

### Паттерн: Test → Fix → Test

```
1. Task(Bash): Run tests → получаем список failing tests
2. Fix failing tests
3. Task(Bash): Run tests again → проверяем что исправлено
```

### Паттерн: Explore → Plan → Execute

```
1. Task(Explore): Исследуй где используется X
2. Task(Plan): Спланируй изменения на основе найденного
3. Выполни изменения
```

### Паттерн: Parallel Validation

После изменений запускай все проверки параллельно:

```
// Один вызов с несколькими Task — выполнятся параллельно
Task(Bash, "pytest")
Task(Bash, "mypy .")
Task(Bash, "ruff check .")
```

## Правила

1. **Используй правильный тип** — Explore для поиска, Bash для команд
2. **Параллель где можно** — независимые задачи запускай вместе
3. **Фон для долгих задач** — build, heavy tests → `run_in_background: true`
4. **Описание кратко** — 3-5 слов в `description`
5. **Промпт конкретно** — что делать и что вернуть

## Пример: CI-подобная проверка

После изменений выполни полную проверку:

```
// Все три запускаются параллельно
Task(
  subagent_type: "Bash",
  description: "Type check",
  prompt: "Run mypy on all Python files in src/. Report any type errors."
)

Task(
  subagent_type: "Bash",
  description: "Lint check",
  prompt: "Run ruff check on src/. Report any lint errors."
)

Task(
  subagent_type: "Bash",
  description: "Run tests",
  prompt: "Run pytest with coverage. Report failed tests and coverage %."
)
```

## Ограничения

- Субагенты **не видят контекст разговора** — давай полный промпт
- Результат возвращается **одним сообщением** — не интерактивно
- **Только Claude Code** — другие агенты не поддерживают Task tool
