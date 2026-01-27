# Project Instructions for Claude Code

> **AGENT INSTRUCTION**: Если этот файл содержит незаполненные плейсхолдеры
> (текст в `<!-- -->` комментариях), **заполни их автоматически** на основе
> анализа проекта:
> 1. Просканируй структуру директорий
> 2. Найди package.json, pyproject.toml, requirements.txt, Makefile
> 3. Определи стек, команды тестирования/линтинга
> 4. Заполни все секции конкретными значениями
> 5. Удали этот блок AGENT INSTRUCTION после заполнения

## Quick Facts

| | |
|-|-|
| **Stack** | <!-- ЗАПОЛНИ: язык, фреймворк, база данных --> |
| **Test** | <!-- ЗАПОЛНИ: pytest / npm test / go test --> |
| **Lint** | <!-- ЗАПОЛНИ: ruff check . / eslint / golangci-lint --> |
| **Format** | <!-- ЗАПОЛНИ: ruff format . / prettier / gofmt --> |
| **Build** | <!-- ЗАПОЛНИ: make build / npm run build / go build --> |

## Key Directories

<!-- ЗАПОЛНИ: просканируй проект и опиши реальную структуру -->

```
src/           # Основной код
tests/         # Тесты
docs/          # Документация
```

## Code Style

<!-- ЗАПОЛНИ: определи по существующему коду или конфигам (.editorconfig, pyproject.toml, etc.) -->

- Язык: <!-- Python / TypeScript / Go / ... -->
- Стиль: <!-- Google Style / Airbnb / Standard -->
- Именование: <!-- snake_case / camelCase -->

## Git Conventions

- **Branches**: `{type}/{description}` (например: `feat/add-auth`)
- **Commits**: [Conventional Commits](https://www.conventionalcommits.org/)
  - `feat:` — новая функциональность
  - `fix:` — исправление бага
  - `docs:` — документация
  - `refactor:` — рефакторинг без изменения поведения
  - `test:` — добавление/исправление тестов

## Critical Rules

### Error Handling

- Никогда не глушить ошибки без логирования
- Всегда давать пользователю понятный feedback
- Логировать с достаточным контекстом для отладки

### Testing

- Писать тесты для нового функционала
- Один assert per test (или логически связанная группа)
- Использовать фабрики/фикстуры для тестовых данных

## Skill Activation

| Контекст | Skill |
|----------|-------|
| Перед изменениями кода | `plan-first` |
| После завершения задачи | `verify-and-lock-in` |
| Оценка рисков | `qa-gatekeeper` |
| Сложная задача | `task-decomposition` |
| Python код | `python-style` |

## Common Commands

<!-- ЗАПОЛНИ: найди реальные команды в Makefile, package.json, или документации -->

```bash
# Development
<!-- ЗАПОЛНИ -->

# Testing
<!-- ЗАПОЛНИ -->

# Build
<!-- ЗАПОЛНИ -->
```

## Project-Specific Notes

<!-- ЗАПОЛНИ: добавь важную информацию о проекте -->

- Архитектура: <!-- опиши -->
- Важные зависимости: <!-- перечисли -->
- Известные ограничения: <!-- если есть -->

---

*Этот файл читается Claude Code автоматически. После заполнения удали плейсхолдеры и блок AGENT INSTRUCTION.*
