# CLAUDE.md

> **AGENT**: Если видишь `<!-- ЗАПОЛНИ -->` — заполни автоматически на основе анализа проекта (pyproject.toml, Makefile, структура директорий). Удали этот блок после заполнения.

## Обязательные правила

1. **Артефакты в файлы** — планы, исследования, lock-in сохраняй в `docs/notes/`
2. **Python: ruff** — после каждого изменения: `ruff format <file> && ruff check <file> --fix`
3. **Тесты** — после изменений кода: `pytest tests/ -v` или `make check`
4. **Definition of Done** — план соответствует diff, тесты есть, верификация пройдена

Детали: см. [.claude/rules/](.claude/rules/)

---

## Quick Facts

| | |
|-|-|
| **Stack** | <!-- ЗАПОЛНИ --> |
| **Test** | <!-- ЗАПОЛНИ: pytest / npm test --> |
| **Lint** | <!-- ЗАПОЛНИ: ruff check . / eslint --> |
| **Build** | <!-- ЗАПОЛНИ: make build / npm run build --> |

## Структура

```
<!-- ЗАПОЛНИ: просканируй проект -->
src/           # Основной код
tests/         # Тесты
docs/          # Документация
```

## Стиль кода

<!-- ЗАПОЛНИ: определи по конфигам -->
- Язык: <!-- Python / TypeScript / Go -->
- Стиль: <!-- Google Style / Airbnb -->
- Именование: <!-- snake_case / camelCase -->

## Git

- Branches: `{type}/{description}` (feat/add-auth)
- Commits: [Conventional Commits](https://www.conventionalcommits.org/) — feat, fix, docs, refactor, test

## Команды

```bash
# <!-- ЗАПОЛНИ из Makefile / package.json -->
make check     # lint + test
make test      # только тесты
```

## Специфика проекта

<!-- ЗАПОЛНИ: архитектура, важные зависимости, ограничения -->

---

## Skills

| Skill | Когда |
|-------|-------|
| `artifacts` | Сохранение планов и результатов |
| `python-style` | Python код |
| `verify-and-lock-in` | После завершения задачи |
| `qa-gatekeeper` | Оценка рисков |
| `test-runner` | Запуск тестов |
| `safe-shell` | Shell-команды |
| `subagents` | Параллельные задачи |
| `change-budget` | Ограничение масштаба |
| `task-decomposition` | Сложные задачи (3+ файлов) |
| `refactoring-specialist` | Крупный рефакторинг |
| `doc-steward` | Проектная документация |
| `project-architect-bootstrap` | Новые проекты |
| `bug-hunter` | Поиск и исправление багов из GitHub Issues |

*Детали: [.claude/skills/](.claude/skills/)*
