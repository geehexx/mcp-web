---
trigger: model_decision
description: Apply for git operations commits branching or version control work

---

# Git Workflows and Conventional Commits

## 2.1 Git Commands via run_command

**Use `run_command` tool for all git operations:**

All git commands executed via `run_command` with appropriate `Cwd` parameter.

**Common operations:**

```bash
# Check status
git status --short

# Review unstaged changes
git diff

# Review staged changes
git diff --cached

# Stage files
git add <files>

# Commit
git commit -m "type(scope): description"

# View recent history
git log --oneline -5
```

### 2.2 Git Workflow

**Before making changes:**

- Run `git status --short` to check working tree state
- Review context to understand recent work

**Before committing:**

- Review all diffs: `git diff` (unstaged) or `git diff --cached` (staged)
- Ensure every change belongs to current task
- Split unrelated changes into separate commits

**Commit message format:**

```text
type(scope): description

- Detail 1
- Detail 2
- Detail 3
```

**Types:** feat, fix, docs, test, refactor, security, chore

### 2.3 Conventional Commits

**Format:** `type(scope): description`

**Types:**

| Type | Use Case | Example |
|------|----------|---------|
| `feat` | New feature | `feat(auth): add API key rotation` |
| `fix` | Bug fix | `fix(cache): handle missing files gracefully` |
| `docs` | Documentation | `docs(adr): create ADR-00XX for caching` |
| `test` | Test changes | `test(security): add XSS injection tests` |
| `refactor` | Code refactor | `refactor(chunker): extract method` |
| `security` | Security fix | `security(llm): add input sanitization` |
| `chore` | Maintenance | `chore(deps): update uv to 0.5.0` |
| `style` | Auto-fixes | `style(docs): apply markdownlint fixes` |

**Scope:** Module, component, or area affected (e.g., `auth`, `cache`, `docs`, `workflows`)

### 2.4 Git Best Practices

**DO:**

- ✅ Check `git status` before and after major changes
- ✅ Review diffs before staging
- ✅ Write descriptive commit messages
- ✅ Split unrelated changes into separate commits
- ✅ Commit auto-fixes separately with `style(scope)` type

**DON'T:**

- ❌ Commit without reviewing diffs
- ❌ Mix unrelated changes in one commit
- ❌ Use vague commit messages ("fix stuff", "update")
- ❌ Leave unstaged changes at session end
- ❌ Commit without running tests (for code changes)

---

## Pre-commit Hooks

**Quality gates enforced:**

- Markdown linting
- Task format validation
- Frontmatter validation
- Token count monitoring

**Bypassing (use sparingly):**

- Only for false positives or urgent hotfixes
- Document reason in commit message
- Create follow-up issue if needed

---

## Rule Metadata

**File:** `09_git_workflows.md`
**Trigger:** model_decision
**Estimated Tokens:** ~1,800
**Last Updated:** 2025-10-21
**Status:** Active

**Can be @mentioned:** Yes (hybrid loading)

**Topics Covered:**

- Git operations
- Conventional commits
- Pre-commit hooks
- Commit best practices

**Workflow References:**

- /commit - Git commit workflow

**Dependencies:**

- Source: 06_context_engineering.md (Git Operations section)

**Changelog:**

- 2025-10-21: Created from 06_context_engineering.md
