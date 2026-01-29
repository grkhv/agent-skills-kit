---
name: artifacts
description: Сохранение планов, исследований и результатов в файлы. НЕ держи артефакты только в памяти разговора!
---

Все артефакты работы **ОБЯЗАНЫ** быть сохранены в файлы.

## Расположение

| Артефакт | Папка | Формат имени |
|----------|-------|--------------|
| План | `docs/notes/` | `plan-YYYYMMDD-<topic>.md` |
| Исследование | `docs/notes/` | `research-YYYYMMDD-<topic>.md` |
| Lock-in | `docs/notes/` | `lock-in-YYYYMMDD-HHmm-<topic>.md` |
| ADR | `docs/ADR/` | `NNNN-<topic>.md` |
| Changelog | корень проекта | `CHANGELOG.md` (см. `templates/CHANGELOG.md`) |
| TODO | корень проекта | `TODO.md` (см. `templates/TODO.md`) |

## Когда создавать план

- Изменение кода (не только docs)
- Затрагивается >2 файлов
- Меняется логика или поведение

**Формат**: см. `templates/PLAN.md`

## Lock-in summary

После завершения задачи создай `docs/notes/lock-in-YYYYMMDD-HHmm-<topic>.md`:
- Что изменилось (3-8 пунктов)
- Как проверено (команды + результат)
- Остаточные риски

## Запрещено

- Держать план только в памяти разговора
- Завершать работу без lock-in файла
