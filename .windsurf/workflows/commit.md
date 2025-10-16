---
description: Git commit workflow with validation and review
auto_execution_mode: 3
---

# Git Commit Workflow

Use this workflow for staging and committing changes with proper validation.

## Process

1. **Capture baseline:** Run `mcp2_git_status` to see current working tree state.

2. **Check for auto-fix changes:** If lint/format commands were run (e.g., `task docs:fix`, `task format`), check for unstaged changes:
   - Run `mcp2_git_diff_unstaged` to see auto-fix modifications
   - If auto-fixes present, stage and commit them separately BEFORE main work
   - Use commit message format: `style(scope): apply [tool] auto-fixes`
   - This prevents mixing auto-fixes with feature/fix commits

3. **Review unstaged changes:** Run `mcp2_git_diff_unstaged` with appropriate context to understand all modifications.

4. **Verify ownership:** Ensure every change belongs to the current task. If unrelated work is present, resolve before continuing.

5. **Stage intended changes:** Use `mcp2_git_add` with explicit file paths to stage desired changes.

6. **Confirm staged snapshot:** Run `mcp2_git_diff_staged` to verify only intended changes are staged.

7. **Commit with message:** Use `mcp2_git_commit` with a descriptive conventional commit message.
   - Format: `type(scope): description`
   - Types: `feat`, `fix`, `docs`, `test`, `refactor`, `security`, `chore`
   - Example: `feat(cli): add test-robots command for robots.txt verification`

8. **Optional: Review history:** Run `mcp2_git_log` to see recent commits if needed for context.

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
```text
