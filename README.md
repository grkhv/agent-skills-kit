<div align="center">

# 🛠️ Agent Skills Kit

**Готовые skills и hooks для AI coding агентов**

[![Skills](https://img.shields.io/badge/skills-12-blue?style=flat-square)](copy-to-project/.claude/skills/)
[![Hooks](https://img.shields.io/badge/hooks-6-green?style=flat-square)](copy-to-project/.claude/hooks/)
[![Rules](https://img.shields.io/badge/rules-2-teal?style=flat-square)](copy-to-project/.claude/rules/)
[![Агенты](https://img.shields.io/badge/агенты-4-orange?style=flat-square)](#-поддерживаемые-агенты)
[![Стандарт](https://img.shields.io/badge/стандарт-agentskills.io-purple?style=flat-square)](https://agentskills.io)
[![Лицензия](https://img.shields.io/badge/лицензия-MIT-lightgrey?style=flat-square)](LICENSE)

**Claude Code** · **Codex** · **Windsurf** · **Antigravity**

</div>

---

## 🚀 Быстрый старт

Скопируйте из `copy-to-project/` в корень вашего проекта:

| Агент | Что копировать |
|:------|:---------------|
| **Claude Code** | `.claude/`, `CLAUDE.md`, `CODEMAP.md`, `templates/`, `docs/` |
| **Codex** | `.codex/`, `AGENTS.md`, `CODEMAP.md`, `templates/`, `docs/` |
| **Windsurf** | `.windsurf/`, `AGENTS.md`, `CODEMAP.md`, `templates/`, `docs/` |
| **Antigravity** | `.agent/`, `CODEMAP.md`, `templates/`, `docs/` |

---

## 🤖 Поддерживаемые агенты

| Агент | Skills | Rules | Hooks | Что копировать |
|:------|:------:|:-----:|:-----:|:---------------|
| **Claude Code** | ✅ 12 | ✅ 2 | ✅ 6 | `.claude/` + `CLAUDE.md` + `CODEMAP.md` |
| **Codex** | ✅ 11 | ❌ | ❌ | `.codex/` + `AGENTS.md` + `CODEMAP.md` |
| **Windsurf** | ✅ 11 | ❌ | ❌ | `.windsurf/` + `AGENTS.md` + `CODEMAP.md` |
| **Antigravity** | ✅ 11 | ❌ | ❌ | `.agent/` + `CODEMAP.md` |

---

## 📚 Skills

### Планирование и верификация

| Skill | Описание |
|:------|:---------|
| [**artifacts**](copy-to-project/.claude/skills/artifacts/) | Сохранение планов, исследований и lock-in в файлы |
| [**verify-and-lock-in**](copy-to-project/.claude/skills/verify-and-lock-in/) | Верификация и lock-in summary после изменений |
| [**task-decomposition**](copy-to-project/.claude/skills/task-decomposition/) | Декомпозиция сложных задач на шаги с feedback loop |

### Качество и безопасность

| Skill | Описание |
|:------|:---------|
| [**qa-gatekeeper**](copy-to-project/.claude/skills/qa-gatekeeper/) | Оценка рисков и планирование тестов |
| [**safe-shell**](copy-to-project/.claude/skills/safe-shell/) | Блокировка опасных shell-команд |
| [**change-budget**](copy-to-project/.claude/skills/change-budget/) | Ограничение масштаба: ≤8 файлов, одна ось изменений |
| [**refactoring-specialist**](copy-to-project/.claude/skills/refactoring-specialist/) | Безопасный рефакторинг и применение паттернов |

### Стиль кода и тестирование

| Skill | Описание |
|:------|:---------|
| [**python-style**](copy-to-project/.claude/skills/python-style/) | Google Python Style Guide + обязательный ruff |
| [**test-runner**](copy-to-project/.claude/skills/test-runner/) | Обязательный запуск тестов после изменений кода |
| [**project-architect-bootstrap**](copy-to-project/.claude/skills/project-architect-bootstrap/) | Каркас для новых Python-проектов |

### Документация и совместная работа

| Skill | Описание |
|:------|:---------|
| [**doc-steward**](copy-to-project/.claude/skills/doc-steward/) | Интервью и документация проекта |
| [**subagents**](copy-to-project/.claude/skills/subagents/) | Параллельные задачи через субагентов *(только Claude Code)* |

---

## 📏 Rules (только Claude Code)

Rules загружаются автоматически и всегда в контексте. С `paths:` — только при работе с matching файлами.

| Rule | paths: | Описание |
|:-----|:------:|:---------|
| [**python.md**](copy-to-project/.claude/rules/python.md) | `**/*.py` | Обязательный ruff format + check |
| [**definition-of-done.md**](copy-to-project/.claude/rules/definition-of-done.md) | — | Критерии завершения задачи |

---

## 🪝 Hooks (только Claude Code)

Hooks автоматически применяют правила — обойти их невозможно.

| Hook | Событие | Что делает |
|:-----|:--------|:-----------|
| **require_plan.py** | `PreToolUse` | Блокирует Edit/Write без утверждённого плана |
| **shell_guard.py** | `PreToolUse` | Блокирует опасные команды, отслеживает тесты |
| **mark_dirty.py** | `PostToolUse` | Отслеживает изменённые файлы в state |
| **auto_format.py** | `PostToolUse` | Авто-форматирует файлы (ruff, prettier, sqlfluff) |
| **enforce_verify.py** | `Stop` | Требует верификацию перед остановкой |
| **enforce_subagent_tests.py** | `Stop` | Предупреждает если тесты не запущены после изменений |

---

## 📁 Структура проекта

```
your-project/
├── .claude/                    # Claude Code
│   ├── skills/                 # 12 skills
│   ├── rules/                  # 2 rules (auto-load)
│   ├── hooks/                  # 6 hooks
│   ├── state/                  # State хуков
│   └── settings.local.json
├── .codex/skills/              # Codex (11 skills)
├── .windsurf/skills/           # Windsurf (11 skills)
├── .agent/skills/              # Antigravity (11 skills)
├── docs/
│   ├── notes/                  # Планы и lock-in summaries
│   └── ADR/                    # Architecture Decision Records
├── templates/                  # PLAN.md, TODO.md, CHANGELOG.md
├── CLAUDE.md                   # Инструкции для Claude Code
├── AGENTS.md                   # Инструкции для Codex/Windsurf
└── CODEMAP.md                  # Карта структуры проекта
```

---

## ✨ Ключевые особенности

| Фича | Описание |
|:-----|:---------|
| **State в проекте** | Хуки хранят состояние в `.claude/state/`, не в домашней директории |
| **Lock-in в файл** | Результаты работы сохраняются в `docs/notes/lock-in-*.md` |
| **Переключение между IDE** | Контекст сохраняется при смене агента |
| **Авто-форматирование** | Python (ruff), JSON, MD/YAML/JS/TS (prettier), SQL (sqlfluff) |
| **Шаблоны** | Готовые `PLAN.md`, `TODO.md`, `CHANGELOG.md` |

---

## 🔧 Настройка

### Отключить hook

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

### Добавить свой rule

Создайте `.claude/rules/my-rule.md`:

```yaml
---
paths:
  - "**/*.py"      # Опционально: только для matching файлов
---

Ваши правила здесь...
```

> Rules без `paths:` загружаются всегда. С `paths:` — только при работе с указанными файлами (экономичнее).

---

## 📖 Стандарт

Skills соответствуют открытому стандарту [agentskills.io](https://agentskills.io) для AI-агентов.

---

## 📝 Изменения (2026-01-29)

- **Rules** — добавлена папка `.claude/rules/` для auto-load правил
- **Skills** — убрано дублирование, переименованы: `auto-save-artifacts` → `artifacts`
- **Ссылки на templates** — все шаблоны (`PLAN.md`, `TODO.md`, `CHANGELOG.md`) теперь имеют ссылки в skills
- **CLAUDE.md** — добавлены MD-ссылки на rules и skills

---

## 📜 Лицензия

MIT
