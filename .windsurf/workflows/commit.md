---
description: Git commit workflow with validation and review
auto_execution_mode: 3
---

# Git Commit Workflow

Use this workflow for staging and committing changes with proper validation.

## Process

1. **Capture baseline:** Run `mcp2_git_status` to see current working tree state.

2. **Review unstaged changes:** Run `mcp2_git_diff_unstaged` with appropriate context to understand all modifications.

3. **Verify ownership:** Ensure every change belongs to the current task. If unrelated work is present, resolve before continuing.

4. **Stage intended changes:** Use `mcp2_git_add` with explicit file paths to stage desired changes.

5. **Confirm staged snapshot:** Run `mcp2_git_diff_staged` to verify only intended changes are staged.

6. **Commit with message:** Use `mcp2_git_commit` with a descriptive conventional commit message.
   - Format: `type(scope): description`
   - Types: `feat`, `fix`, `docs`, `test`, `refactor`, `security`, `chore`
   - Example: `feat(cli): add test-robots command for robots.txt verification`

7. **Optional: Review history:** Run `mcp2_git_log` to see recent commits if needed for context.

## Validation Checklist

Before committing:

- [ ] All tests pass (`task test:fast`)
- [ ] Linting passes (`task lint`)
- [ ] Documentation updated
- [ ] No unrelated changes in diff
- [ ] Commit message follows conventional format

## Examples

```bash
# Feature commit
feat(summarizer): implement query-aware chunk selection

# Bug fix
fix(fetcher): handle Playwright timeout errors gracefully

# Documentation
docs(adr): add ADR-0011 for caching strategy

# Testing
test(integration): add robots.txt handling test scenarios

# Security improvement
security(extractor): strip HTML comments to prevent injection
```
