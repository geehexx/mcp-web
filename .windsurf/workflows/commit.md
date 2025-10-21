---
created: "2025-10-17"
updated: "2025-10-21"
description: Git commit workflow with validation and review
auto_execution_mode: 3
category: Validation
complexity: 55
tokens: 1400
dependencies:
  - validate
status: active
version: "2.0-intelligent-semantic-preservation"
---

# Git Commit Workflow

Stage and commit with validation and conventional format.

**Chain:** `/commit` → `/validate` → `/bump-version` (conditional)

---

## Process

**1. Auto-Fixes:** Commit separately: `style(scope): apply [tool] auto-fixes`

**2. Validate (MANDATORY):** Call `/validate` - if fails, STOP, fix, re-validate

**3. Review & Stage:**

```bash
git status --short && git diff
git add <files> && git diff --staged
```

**4. Commit:** `type(scope): description`

**Types:** feat, fix, docs, test, refactor, security, perf, chore, style

```bash
feat(cli): add test-robots command
fix(fetcher): handle Playwright timeout
```

**5. Version Bump:** If `feat|fix` or `BREAKING CHANGE`, call `/bump-version`

---

## Integration

**Called By:** `/work`, `/implement`, user
**Calls:** `/validate` (mandatory), `/bump-version` (conditional)

## Anti-Patterns

❌ Never skip validation (`--no-verify`)
❌ Never mix unrelated changes
❌ Never use vague messages

## References

- [Conventional Commits](https://www.conventionalcommits.org/)
- `validate.md`, `09_git_workflows.md`
