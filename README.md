<div align="center">

# 🛠️ Agent Skills Kit

**Готовые skills и hooks для AI coding агентов**

[![Skills](https://img.shields.io/badge/skills-14-blue?style=flat-square)](copy-to-project/.claude/skills/)
[![Hooks](https://img.shields.io/badge/hooks-6-green?style=flat-square)](copy-to-project/.claude/hooks/)
[![Агенты](https://img.shields.io/badge/агенты-4-orange?style=flat-square)](#-поддерживаемые-агенты)
[![Стандарт](https://img.shields.io/badge/стандарт-agentskills.io-purple?style=flat-square)](https://agentskills.io)
[![Лицензия](https://img.shields.io/badge/лицензия-MIT-lightgrey?style=flat-square)](LICENSE)

**Claude Code** · **Codex** · **Windsurf** · **Antigravity**

</div>

---

## 🚀 Быстрый старт

```bash
# Клонируем репозиторий
git clone https://github.com/grkhv/agent-skills-kit.git
cd agent-skills-kit

# Копируем в свой проект (пример для Claude Code)
cp -r copy-to-project/.claude/ your-project/
cp copy-to-project/CLAUDE.md copy-to-project/CODEMAP.md your-project/
cp -r copy-to-project/templates/ copy-to-project/docs/ your-project/
```

<details>
<summary><b>📦 Установка для других агентов</b></summary>

### Codex
```bash
cp -r copy-to-project/.codex/ your-project/
cp copy-to-project/CODEMAP.md your-project/
cp -r copy-to-project/templates/ copy-to-project/docs/ your-project/
```

### Windsurf
```bash
cp -r copy-to-project/.windsurf/ your-project/
cp copy-to-project/AGENTS.md copy-to-project/CODEMAP.md your-project/
cp -r copy-to-project/templates/ copy-to-project/docs/ your-project/
```

### Antigravity
```bash
cp -r copy-to-project/.agent/ your-project/
cp copy-to-project/CODEMAP.md your-project/
cp -r copy-to-project/templates/ copy-to-project/docs/ your-project/
```

</details>

---

## 🤖 Поддерживаемые агенты

| Агент | Skills | Hooks | Что копировать |
|:------|:------:|:-----:|:---------------|
| **Claude Code** | ✅ 14 | ✅ 6 | `.claude/` + `CLAUDE.md` + `CODEMAP.md` |
| **Codex** | ✅ 13 | ❌ | `.codex/` + `CODEMAP.md` |
| **Windsurf** | ✅ 13 | ❌ | `.windsurf/` + `AGENTS.md` + `CODEMAP.md` |
| **Antigravity** | ✅ 13 | ❌ | `.agent/` + `CODEMAP.md` |

---

## 📚 Skills

### Планирование и верификация

| Skill | Описание |
|:------|:---------|
| [**plan-first**](copy-to-project/.claude/skills/plan-first/) | Требует план перед изменениями кода |
| [**verify-and-lock-in**](copy-to-project/.claude/skills/verify-and-lock-in/) | Верификация и lock-in summary после изменений |
| [**task-decomposition**](copy-to-project/.claude/skills/task-decomposition/) | Декомпозиция сложных задач на шаги с feedback loop |

### Качество и безопасность

| Skill | Описание |
|:------|:---------|
| [**qa-gatekeeper**](copy-to-project/.claude/skills/qa-gatekeeper/) | Оценка рисков и планирование тестов |
| [**safe-shell**](copy-to-project/.claude/skills/safe-shell/) | Блокировка опасных shell-команд |
| [**change-budget**](copy-to-project/.claude/skills/change-budget/) | Ограничение масштаба: ≤8 файлов, одна ось изменений |
| [**refactoring-specialist**](copy-to-project/.claude/skills/refactoring-specialist/) | Безопасный рефакторинг и применение паттернов |

### Стиль кода и архитектура

| Skill | Описание |
|:------|:---------|
| [**python-style**](copy-to-project/.claude/skills/python-style/) | Google Python Style Guide + обязательный ruff |
| [**ruff-enforcer**](copy-to-project/.claude/skills/ruff-enforcer/) | Принудительное форматирование через ruff |
| [**project-architect-bootstrap**](copy-to-project/.claude/skills/project-architect-bootstrap/) | Каркас для новых Python-проектов |

### Артефакты и тестирование

| Skill | Описание |
|:------|:---------|
| [**auto-save-artifacts**](copy-to-project/.claude/skills/auto-save-artifacts/) | Обязательное сохранение планов и исследований в файлы |
| [**test-runner**](copy-to-project/.claude/skills/test-runner/) | Обязательный запуск тестов после изменений кода |

### Документация и совместная работа

| Skill | Описание |
|:------|:---------|
| [**doc-steward**](copy-to-project/.claude/skills/doc-steward/) | Интервью и документация проекта |
| [**subagents**](copy-to-project/.claude/skills/subagents/) | Параллельные задачи через субагентов *(только Claude Code)* |

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
│   ├── skills/                 # 14 skills
│   ├── hooks/                  # 6 hooks
│   ├── state/                  # State хуков (hook_state.json)
│   └── settings.local.json
├── .codex/skills/              # Codex (13 skills)
├── .windsurf/skills/           # Windsurf (13 skills)
├── .agent/skills/              # Antigravity (13 skills)
├── docs/
│   ├── notes/                  # Планы и lock-in summaries
│   └── ADR/                    # Architecture Decision Records
├── templates/                  # PLAN.md, TODO.md, CHANGELOG.md
├── CLAUDE.md                   # Инструкции для агента
├── CODEMAP.md                  # Карта структуры проекта
└── AGENTS.md                   # Windsurf guidelines
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

---

## 📖 Стандарт

Skills соответствуют открытому стандарту [agentskills.io](https://agentskills.io) для AI-агентов.

---

## 📜 Лицензия

MIT
