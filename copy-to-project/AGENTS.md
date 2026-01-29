# AGENTS.md

Instructions for AI coding agents (Codex, Windsurf, Antigravity).

## Обязательные правила

### 1. Артефакты в файлы

| Артефакт | Папка | Формат |
|----------|-------|--------|
| План | `docs/notes/` | `plan-YYYYMMDD-<topic>.md` |
| Исследование | `docs/notes/` | `research-YYYYMMDD-<topic>.md` |
| Lock-in | `docs/notes/` | `lock-in-YYYYMMDD-HHmm-<topic>.md` |

**НЕ держи планы и результаты только в памяти разговора!**

### 2. Python: ruff

После каждого изменения: `ruff format <file> && ruff check <file> --fix`

### 3. Тесты

После изменений кода: `pytest tests/ -v` или `make check`

### 4. Definition of Done

1. План (если требовался) существует и соответствует diff
2. Тесты есть для нового поведения
3. Верификация пройдена (`ruff` + `pytest`)
4. Lock-in summary создан

---

## Planning

Перед нетривиальными изменениями (>2 файлов, логика) создай `docs/notes/plan-YYYYMMDD-<topic>.md`:
- Цель, Границы, Риски (2-5), Шаги (6-12), Верификация

## Verification

После правок создай `docs/notes/lock-in-YYYYMMDD-HHmm-<topic>.md`:
- Что изменилось (3-8 пунктов)
- Как проверено (команды + результат)
- Остаточные риски

## Safety

**Никогда**: `rm -rf /`, `sudo`, чтение `.env` / SSH keys без подтверждения
**Всегда**: сначала read-only, короткие обратимые операции

## Code Style (Python)

- `snake_case` — функции/переменные, `PascalCase` — классы
- Type hints для public API
- Формат: `ruff format`

## Quality Gates

- **Low**: косметика, локальные изменения
- **Medium**: логика в одном модуле
- **High**: критические пути, платежи, безопасность

## Skills

Директории: `.agent/skills/`, `.codex/skills/`, `.windsurf/skills/`

| Skill | Описание |
|-------|----------|
| `artifacts` | Сохранение планов и результатов |
| `python-style` | Стиль кода и ruff |
| `verify-and-lock-in` | Фиксация результатов |
| `qa-gatekeeper` | Контроль качества |
| `test-runner` | Запуск тестов |
| `safe-shell` | Безопасные shell-команды |
| `change-budget` | Ограничение масштаба изменений |
| `task-decomposition` | Декомпозиция сложных задач |
| `refactoring-specialist` | Безопасный рефакторинг |
| `doc-steward` | Создание проектной документации |
| `project-architect-bootstrap` | Каркас для новых проектов |
