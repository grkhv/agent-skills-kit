---
name: auto-save-artifacts
description: Автоматическое сохранение планов, исследований и результатов в нужные папки.
---

# Auto-Save Artifacts

Все артефакты работы **ОБЯЗАНЫ** быть сохранены в соответствующие папки.

## Обязательные артефакты и их расположение

| Артефакт | Папка | Формат имени |
|----------|-------|--------------|
| План | `docs/notes/` | `plan-YYYYMMDD-<topic>.md` |
| Исследование | `docs/notes/` | `research-YYYYMMDD-<topic>.md` |
| Lock-in | `docs/notes/` | `lock-in-YYYYMMDD-HHmm-<topic>.md` |
| ADR | `docs/ADR/` | `NNNN-<topic>.md` |
| Proposal | `docs/proposals/` | `<topic>.md` |

## Workflow

### 1. Начало задачи
Создай план в `docs/notes/plan-*.md`:
```bash
# Пример имени файла
docs/notes/plan-20260128-refactoring-processor.md
```

### 2. Исследование
Сохрани результаты в `docs/notes/research-*.md`:
```bash
docs/notes/research-20260128-auth-options.md
```

### 3. Завершение
Создай lock-in в `docs/notes/lock-in-*.md`:
```bash
docs/notes/lock-in-20260128-1430-add-auth.md
```

## ЗАПРЕЩЕНО

- Держать план только в памяти разговора
- Завершать работу без lock-in файла
- Оставлять исследования только в чате
- Сохранять артефакты в корень проекта (кроме PLAN.md для быстрых задач)

## Пример структуры docs/notes/

```
docs/notes/
├── plan-20260125-add-logging.md
├── plan-20260128-refactor-auth.md
├── research-20260126-logging-libs.md
├── lock-in-20260125-1530-add-logging.md
└── lock-in-20260128-1645-refactor-auth.md
```
