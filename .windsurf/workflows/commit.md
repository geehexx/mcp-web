---
created: "2025-10-17"
updated: "2025-10-19"
description: Git commit workflow with validation and review
auto_execution_mode: 3
category: Validation
complexity: 55
tokens: 1812
dependencies:
  - validate
status: active
---

# Git Commit Workflow

**Purpose:** Stage and commit changes with proper validation and conventional commit format.

**Category:** Specialized Operation (git operations + validation orchestration)

**Invocation:** `/commit` (called by `/work`, `/implement`, or directly)

**Philosophy:** Every commit should pass quality gates and have clear, conventional messages.

**Workflow Chain:** `/commit` → `/validate` → `/bump-version` (conditionally)

---

## Process

**Steps:** Auto-fixes → Validate → Review → Stage → Commit → Version bump (conditional)

---

### 1. Auto-Fixes (if any)

Commit auto-fixes separately: `style(scope): apply [tool] auto-fixes`

### 2. Validate (⚠️ MANDATORY)

**Call `/validate`** - Cannot skip (normative core)
- If fails: STOP, fix, re-validate
- ACF principle: Verify before high-stakes action

### 3. Review & Stage

```bash
git status --short  # See changes
git diff            # Review
git add <files>     # Stage
git diff --staged   # Confirm
```

### 4. Commit with Conventional Format

**Format:** `type(scope): description`

**Types:** feat, fix, docs, test, refactor, security, perf, chore, style

**Examples:**
```bash
feat(cli): add test-robots command
fix(fetcher): handle Playwright timeout
docs(adr): add ADR-0011 for caching
security(extractor): strip HTML comments
```

### 5. Version Bump (Conditional)

**Auto-check:** If commit type is `feat|fix` or has `BREAKING CHANGE`, call `/bump-version`

---

## Integration

### Called By

- `/work` - After completing work
- `/implement` - After implementation complete
- User - Direct invocation

### Calls

- `/validate` - Pre-commit quality gates (Stage 2)
- `/bump-version` - Semantic version bump (Stage 7, conditional)

---

## Anti-Patterns

### Anti-Patterns

- ❌ **Never skip validation** (--no-verify) - Violates ACF normative core
- ❌ **Never mix unrelated changes** - One concern per commit
- ❌ **Never use vague messages** - Specific type + scope + description

---

## References

- [Conventional Commits](https://www.conventionalcommits.org/)
- `.windsurf/workflows/validate.md` - Quality gate workflow
- `.windsurf/rules/09_git_workflows.md` - Git Operations
