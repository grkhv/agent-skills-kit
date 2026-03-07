# AGENTS.md

Instructions for AI coding agents (Codex, Windsurf, Antigravity).

## Обязательные правила

IMPORTANT: Эти правила нельзя пропускать.

1. **Артефакты — в файлы** — планы, исследования, lock-in ОБЯЗАТЕЛЬНО сохраняй в `docs/notes/`.
2. **Линтер** — после каждого изменения кода запусти линтер. Определи команду из конфигов проекта (pyproject.toml, package.json, Makefile).
3. **Тесты** — после изменений кода запусти тесты. Без прохождения тестов задача считается незавершённой.
4. **Definition of Done** — план соответствует diff, тесты существуют и проходят, верификация пройдена.

## Git

- Ветки: `{type}/{description}` (feat/add-auth, fix/login-bug)
- Коммиты: Conventional Commits — feat, fix, docs, refactor, test

## Safety

- Сначала read-only операции, потом короткие обратимые изменения
- Чтение `.env` / SSH keys — только с подтверждением пользователя

## Контекст проекта

См. README.md
