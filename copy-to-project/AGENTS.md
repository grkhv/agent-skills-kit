# Agent Guidelines

This file provides instructions for AI coding agents (Windsurf Cascade, etc.).

## Planning

Before any non-trivial code changes, create a plan:

1. **When to plan**: Code changes affecting >2 files, logic/behavior changes
2. **Create**: `PLAN.md` or `docs/notes/plan-YYYYMMDD-<topic>.md`
3. **Include**: Goal, Boundaries, Risks (2-5), Steps (6-12), Verification command

## Verification

After code changes, always verify:

```bash
# Preferred
make check

# Or standard tools
pytest && ruff check . && mypy .
```

Provide a lock-in summary:
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
