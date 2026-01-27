# Agent Skills Kit

Skills и hooks для AI-агентов: **Claude Code**, **Codex**, **Windsurf**, **Antigravity**.

## Quick Start

```bash
# Claude Code (полная поддержка)
cp -r copy-to-project/.claude/ your-project/
cp copy-to-project/CLAUDE.md copy-to-project/CODEMAP.md your-project/
cp copy-to-project/.gitignore your-project/  # или merge с существующим
cp -r copy-to-project/templates/ copy-to-project/docs/ your-project/

# Codex
cp -r copy-to-project/.codex/ your-project/
cp copy-to-project/CODEMAP.md your-project/

# Windsurf
cp -r copy-to-project/.windsurf/ your-project/
cp copy-to-project/AGENTS.md copy-to-project/CODEMAP.md your-project/

# Antigravity
cp -r copy-to-project/.agent/ your-project/
cp copy-to-project/CODEMAP.md your-project/

# Готово! Заполните CLAUDE.md и CODEMAP.md
```

## Что внутри

```
copy-to-project/
├── .claude/                 # Claude Code (skills + hooks)
│   ├── skills/              # 10 skills
│   ├── hooks/               # 5 hooks
│   ├── state/               # Локальный state проекта
│   └── settings.local.json
├── .codex/skills/           # Codex (только skills)
├── .windsurf/skills/        # Windsurf (только skills)
├── .agent/skills/           # Antigravity (только skills)
├── docs/
│   ├── notes/               # Планы и lock-in summaries
│   └── ADR/                 # Architecture Decision Records
├── templates/               # Скелеты файлов (PLAN, TODO, CHANGELOG)
├── CLAUDE.md                # Инструкции для Claude Code (шаблон)
├── CODEMAP.md               # Описание структуры проекта (шаблон)
├── AGENTS.md                # Windsurf guidelines
├── .gitignore               # Игнорировать state файлы
└── README.md
```

## Поддержка агентов

| Агент | Skills | Hooks | Что копировать |
|-------|:------:|:-----:|----------------|
| Claude Code | ✅ | ✅ | `.claude/` + `CLAUDE.md` + `CODEMAP.md` + `.gitignore` + `templates/` + `docs/` |
| Codex | ✅ | ❌ | `.codex/` + `CODEMAP.md` + `templates/` + `docs/` |
| Windsurf | ✅ | ❌ | `.windsurf/` + `AGENTS.md` + `CODEMAP.md` + `templates/` + `docs/` |
| Antigravity | ✅ | ❌ | `.agent/` + `CODEMAP.md` + `templates/` + `docs/` |

## Skills

| Skill | Описание | Агенты |
|-------|----------|--------|
| `plan-first` | Требует план перед изменениями кода | Все |
| `verify-and-lock-in` | Верификация и lock-in summary в файл | Все |
| `qa-gatekeeper` | Оценка рисков и планирование тестов | Все |
| `safe-shell` | Блокировка опасных shell-команд | Все |
| `python-style` | Google Python Style Guide | Все |
| `task-decomposition` | Декомпозиция сложных задач на шаги | Все |
| `change-budget` | Ограничение масштаба: ≤8 файлов, одна ось изменений | Все |
| `doc-steward` | Интервью и документация проекта | Все |
| `project-architect-bootstrap` | Каркас для новых Python-проектов | Все |
| `subagents` | Использование субагентов для параллельных задач | Claude Code |

## Hooks (Claude Code)

| Hook | Событие | Назначение |
|------|---------|------------|
| `require_plan.py` | PreToolUse | Блокирует Edit/Write без плана |
| `shell_guard.py` | PreToolUse | Блокирует опасные Bash команды |
| `mark_dirty.py` | PostToolUse | Отслеживает изменённые файлы |
| `auto_format.py` | PostToolUse | Авто-форматирует файлы (py, json, md, sql, yaml, js/ts) |
| `enforce_verify.py` | Stop | Требует верификацию перед остановкой |

## Ключевые особенности

- **State в проекте**: Хуки хранят состояние в `.claude/state/`, не в домашней директории
- **Lock-in в файл**: Результаты работы сохраняются в `docs/notes/lock-in-*.md`
- **Переключение между IDE**: Контекст сохраняется при смене агента
- **Шаблоны файлов**: Готовые `PLAN.md`, `TODO.md`, `CHANGELOG.md`
- **Авто-форматирование**: Python (ruff), JSON (built-in), MD/YAML/JS/TS (prettier), SQL (sqlfluff)
- **Декомпозиция задач**: Skill для разбиения сложных задач на шаги с feedback loop

## Стандарт

Skills соответствуют [agentskills.io](https://agentskills.io) — открытому стандарту для AI-агентов.

## Лицензия

MIT
