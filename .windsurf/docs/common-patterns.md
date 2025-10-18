# Common Patterns Library

**Purpose:** Shared code examples referenced across workflows to reduce duplication.

**Usage:** Reference patterns from workflows instead of duplicating code blocks.

---

## Git Operations

### Git Status Check

```bash
git status --short
```

### Git Diff Review (Unstaged)

```bash
git diff
```

### Git Diff Review (Staged)

```bash
git diff --cached
```

### Conventional Commit

```bash
git commit -m "type(scope): description"
```

**Types:** feat, fix, docs, test, refactor, security, chore

### Check Recent Commits

```bash
git log --oneline -5
```

---

## Task Commands

### Run Tests (Fast, Parallel)

```bash
task test:fast:parallel
```

### Run Tests (All, Parallel)

```bash
task test:parallel
```

### Run All Quality Checks

```bash
task validate
```

### Lint Code

```bash
task lint
```

### Format Code

```bash
task format
```

### Security Checks

```bash
task security
```

### Full CI Pipeline (Local)

```bash
task ci
```

---

## File Operations

### Batch Read Files (MCP)

```python
mcp0_read_multiple_files(paths=[
    "/home/gxx/projects/mcp-web/file1.md",
    "/home/gxx/projects/mcp-web/file2.py"
])
```

**Note:** MCP tools require absolute paths.

### Batch Read Files (Standard)

```python
# For non-.windsurf/ files, can use relative paths
read_file("file1.md")
read_file("file2.py")
```

### Search Files

```bash
find .windsurf -name "*.md"
```

### Grep Search

```bash
grep -r "pattern" .windsurf/ --include="*.md"
```

---

## Initiative Operations

### Find Active Initiatives

```bash
ls docs/initiatives/active/
```

### Check Initiative Status

```bash
grep "Status:" docs/initiatives/active/*/initiative.md
```

### Find Unchecked Tasks

```bash
grep "\[ \]" docs/initiatives/active/*/initiative.md
```

---

## Session Summary Operations

### List Recent Summaries

```bash
ls -t docs/archive/session-summaries/*.md | head -3
```

### Find Summaries by Date

```bash
ls docs/archive/session-summaries/YYYY-MM-DD-*.md
```

---

## Test Operations

### Check Test Failures

```bash
task test:fast 2>&1 | tail -20 | grep -E "(FAILED|ERROR)"
```

### Find Skipped Tests

```bash
grep -r "pytest.mark.skip" tests/
```

### Run Specific Test File

```bash
uv run pytest tests/unit/test_file.py
```

---

## Context Detection Patterns

### Load Project Summary

```python
mcp0_read_text_file("/home/gxx/projects/mcp-web/PROJECT_SUMMARY.md")
```

### Check Git Working Tree State

```bash
# Unstaged changes
git diff --name-only

# Staged changes
git diff --staged --name-only

# All changes
git status --short
```

### Find TODO Markers

```bash
grep -r "TODO\|FIXME\|XXX" docs/ --include="*.md"
```

---

## Validation Patterns

### Markdown Linting

```bash
task lint:docs
```

### Python Linting

```bash
task lint:ruff
task lint:mypy
```

### Link Checking

```bash
markdown-link-check file.md
```

---

## Archive Operations

### Archive Initiative

```bash
/archive-initiative <initiative-name>
```

### Consolidate Summaries

```bash
/consolidate-summaries <date>
```

---

## Usage Examples

### From Workflows

**Instead of duplicating code:**

```markdown
❌ DON'T:
Run git status:
[bash]
git status --short
[/bash]

✅ DO:
Run git status (see [Git Status Check](../templates/common-patterns.md#git-status-check))
```

**Or inline reference:**

```markdown
1. Check git status (see common patterns)
2. Run tests (see common patterns)
3. Commit changes (see common patterns)
```

---

## Maintenance

**When adding new patterns:**

1. Verify pattern used in 3+ workflows
2. Add to appropriate section above
3. Update workflows to reference pattern
4. Test that links work correctly

**When updating patterns:**

1. Verify all referencing workflows still work
2. Update pattern documentation
3. Run validation to catch broken references

---

**Last Updated:** 2025-10-18
**Version:** 1.0.0
