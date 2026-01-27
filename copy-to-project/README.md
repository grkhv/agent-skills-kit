# Agent Skills Kit — Quick Start

Готовые skills и hooks для AI coding агентов.

## Поддерживаемые агенты

| Агент | Skills | Hooks | Что копировать |
|-------|:------:|:-----:|----------------|
| Claude Code | ✅ | ✅ | `.claude/` |
| Codex | ✅ | ❌ | `.codex/` |
| Windsurf | ✅ | ❌ | `.windsurf/` + `AGENTS.md` |
| Antigravity | ✅ | ❌ | `.agent/` |

## Быстрый старт

### Claude Code (полная поддержка)

```bash
# Копируем skills + hooks + state
cp -r .claude/ /path/to/your-project/

# Копируем templates и docs
cp -r templates/ docs/ /path/to/your-project/
```

### Codex

```bash
cp -r .codex/ /path/to/your-project/
cp -r templates/ docs/ /path/to/your-project/
```

### Windsurf

```bash
cp -r .windsurf/ /path/to/your-project/
cp AGENTS.md /path/to/your-project/
cp -r templates/ docs/ /path/to/your-project/
```

### Antigravity

```bash
cp -r .agent/ /path/to/your-project/
cp -r templates/ docs/ /path/to/your-project/
```

## Что внутри

### Skills

**Claude Code (11 skills):**

| Skill | Описание |
|-------|----------|
| `plan-first` | Требует план перед изменениями кода |
| `verify-and-lock-in` | Верификация и lock-in summary после изменений |
| `qa-gatekeeper` | Оценка рисков и планирование тестов |
| `safe-shell` | Блокировка опасных shell-команд |
| `python-style` | Google Python Style Guide |
| `task-decomposition` | Декомпозиция сложных задач на шаги с feedback loop |
| `change-budget` | Ограничение масштаба: ≤8 файлов, одна ось изменений |
| `doc-steward` | Интервью и документация проекта |
| `project-architect-bootstrap` | Каркас для новых Python-проектов |
| `refactoring-specialist` | Безопасный рефакторинг и применение паттернов |
| `subagents` | Использование субагентов для параллельных задач (только Claude Code) |

**Другие агенты (10 skills):** все кроме `subagents`

### Hooks (только Claude Code)

| Hook | Событие | Назначение |
|------|---------|------------|
| `require_plan.py` | PreToolUse | Блокирует Edit/Write без плана |
| `shell_guard.py` | PreToolUse | Блокирует опасные Bash команды |
| `mark_dirty.py` | PostToolUse | Отслеживает изменённые файлы |
| `auto_format.py` | PostToolUse | Авто-форматирует файлы (py, json, md, sql, yaml, js/ts) |
| `enforce_verify.py` | Stop | Требует верификацию перед остановкой |

### Templates

| Файл | Назначение |
|------|------------|
| `PLAN.md` | Шаблон плана задачи |
| `TODO.md` | Отслеживание задач проекта |
| `CHANGELOG.md` | История изменений |

### Docs

```
docs/
├── notes/          # Планы и lock-in summaries
│   └── .gitkeep
└── ADR/
    └── template.md # Шаблон Architecture Decision Record
```

## Структура файлов

```
your-project/
├── .claude/                 # Claude Code
│   ├── skills/              # 11 skills
│   ├── hooks/               # 5 hooks
│   ├── state/               # Локальный state (hook_state.json)
│   └── settings.local.json
├── .codex/skills/           # Codex (только skills)
├── .windsurf/skills/        # Windsurf (только skills)
├── .agent/skills/           # Antigravity (только skills)
├── docs/
│   ├── notes/               # Планы и lock-in summaries
│   └── ADR/                 # Architecture Decision Records
├── templates/               # Скелеты файлов
├── AGENTS.md                # Windsurf guidelines
└── ...
```

## Важно: переключение между IDE

State хуков сохраняется в `.claude/state/` **проекта**, не в домашней директории.
Это позволяет переключаться между IDE и сохранять контекст работы.

Lock-in summaries записываются в `docs/notes/lock-in-*.md` — доступны всем агентам.

## Настройка

### Отключить конкретный hook

Отредактируйте `.claude/settings.local.json` и удалите ненужный hook.

### Добавить свой skill

Создайте `.claude/skills/my-skill/SKILL.md`:

```yaml
---
name: my-skill
description: Когда активировать этот skill
---

# Инструкции

Ваши инструкции здесь...
```

## Стандарт

Skills соответствуют [agentskills.io](https://agentskills.io) — открытому стандарту для AI-агентов.

## Ссылки

- [agentskills.io](https://agentskills.io) — открытый стандарт
- [Claude Code Docs](https://code.claude.com/docs) — документация Claude Code
- [ADR Standard](https://github.com/joelparkerhenderson/architecture-decision-record) — стандарт ADR
