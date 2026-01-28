# Agent Guidelines

This file provides instructions for AI coding agents (Windsurf, Codex, Antigravity, etc.).

## КРИТИЧЕСКИЕ ПРАВИЛА

### 1. ОБЯЗАТЕЛЬНО сохраняй артефакты в файлы

| Артефакт | Папка | Формат |
|----------|-------|--------|
| План | `docs/notes/` | `plan-YYYYMMDD-<topic>.md` |
| Исследование | `docs/notes/` | `research-YYYYMMDD-<topic>.md` |
| Lock-in | `docs/notes/` | `lock-in-YYYYMMDD-HHmm-<topic>.md` |

**НЕ держи планы и результаты только в памяти разговора!**

### 2. ОБЯЗАТЕЛЬНО используй ruff

После КАЖДОГО изменения Python файла:
```bash
ruff format <file>
ruff check <file> --fix
```

### 3. ОБЯЗАТЕЛЬНО запускай тесты

После изменений кода:
```bash
pytest tests/ -v
```

## Planning

Before any non-trivial code changes, create a plan:

1. **When to plan**: Code changes affecting >2 files, logic/behavior changes
2. **Create**: `docs/notes/plan-YYYYMMDD-<topic>.md` (preferred) or `PLAN.md`
3. **Include**: Goal, Boundaries, Risks (2-5), Steps (6-12), Verification command

**ВАЖНО**: План ОБЯЗАН быть сохранён в файл, не только в чате.

## Verification

After code changes, always verify:

```bash
# Preferred
make check

# Or standard tools
ruff format . && ruff check . && pytest tests/ -v && mypy src/
```

Provide a lock-in summary in `docs/notes/lock-in-YYYYMMDD-HHmm-<topic>.md`:
- What changed (3-8 points)
- How verified (commands + results)
- Tests added/modified
- Remaining risks

## Safety

**Never execute**:
- `rm -rf /`, `format`, `mkfs`, `shutdown`, `sudo`
- Reading secrets, `.env`, SSH keys without confirmation

**Always**:
- Use read-only commands first (`ls`, `git status`, `grep`)
- Keep commands short and reversible
- Ask confirmation for sensitive operations

## Code Style (Python)

Follow Google Python Style Guide:
- `snake_case` for functions/variables
- `PascalCase` for classes
- Type hints for public API
- Format with `ruff format`

## Quality Gates

For code changes, assess risk level:
- **Low**: cosmetic, local changes
- **Medium**: logic in one module
- **High**: critical paths, payments, security

Match testing depth to risk.

## Skills Reference

Каждый агент имеет skills в своей директории:
- `.claude/skills/` — Claude Code (+ hooks, subagents)
- `.agent/skills/` — Google Antigravity
- `.codex/skills/` — OpenAI Codex
- `.windsurf/skills/` — Windsurf

Доступные skills:
| Skill | Описание |
|-------|----------|
| `plan-first` | Планирование перед изменениями |
| `python-style` | Стиль кода и ruff |
| `auto-save-artifacts` | Сохранение артефактов |
| `ruff-enforcer` | Форматирование Python |
| `test-runner` | Запуск тестов |
| `verify-and-lock-in` | Фиксация результатов |
| `qa-gatekeeper` | Контроль качества |
| `safe-shell` | Безопасные shell-команды |
