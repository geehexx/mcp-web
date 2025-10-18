---
created: "2025-10-17"
updated: "2025-10-19"
description: Git commit workflow with validation and review
auto_execution_mode: 3
category: Validation
complexity: 55
tokens: 1058
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

### 1. Check for Auto-Fix Changes

**If formatters/linters were run:**

```bash
# Check for unstaged changes from auto-fixes
git status --short

# Review auto-fix changes
git diff
```

**If auto-fixes present:**

- Stage and commit separately BEFORE main work
- Use: `style(scope): apply [tool] auto-fixes`
- Prevents mixing auto-fixes with feature/fix commits

### 2. Run Validation (MANDATORY)

**⚠️ CRITICAL: This step CANNOT be skipped. Normative core enforcement.**

**Call `/validate` workflow:**

- Runs all quality checks (linting, tests, security)
- Auto-fixes issues where possible
- Reports blockers

**If validation fails:**

- **STOP**: Do not proceed to commit
- Fix all blocking issues
- Re-run `/validate`
- Continue ONLY when validation passes

**Architectural Guarantee:**
This implements the ACF (Agent Constitution Framework) principle of "think then verify then act" - validation (VERIFY) must precede high-stakes operation (TOOL_CALL: git commit).

**See:** `.windsurf/workflows/validate.md`

### 3. Review Changes

**Examine all modifications:**

```bash
# See all changed files
git status --short

# Review unstaged changes
git diff

# Review staged changes (if any)
git diff --staged
```

**Verify ownership:**

- Every change belongs to current task
- No unrelated work included
- No debug code or TODOs left behind

### 4. Stage Changes

**Stage intended files:**

```bash
# Stage specific files
git add path/to/file1.py path/to/file2.py

# Or stage all (if reviewed)
git add -A
```

**Confirm staged snapshot:**

```bash
# Review what will be committed
git diff --staged
```

### 5. Commit with Conventional Message

**Format:** `type(scope): description`

**Types:**

- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation only
- `test` - Test additions/changes
- `refactor` - Code restructuring (no behavior change)
- `security` - Security improvements
- `perf` - Performance improvements
- `chore` - Maintenance (deps, config)
- `style` - Formatting, whitespace (auto-fixes)

**Examples:**

```bash
# Feature
git commit -m "feat(cli): add test-robots command for robots.txt verification"

# Bug fix
git commit -m "fix(fetcher): handle Playwright timeout errors gracefully"

# Documentation
git commit -m "docs(adr): add ADR-0011 for caching strategy"

# Testing
git commit -m "test(integration): add robots.txt handling scenarios"

# Security
git commit -m "security(extractor): strip HTML comments to prevent injection"

# Performance
git commit -m "perf(summarizer): implement parallel chunk processing (1.17x speedup)"
```

**Multi-paragraph commits:**

```bash
git commit -m "feat(auth): implement API key authentication

- Add auth module with key validation
- Integrate with FastAPI dependency injection
- Include CLI key management tools
- 95% test coverage

Refs: docs/initiatives/active/2025-10-15-api-key-auth.md"
```

### 6. Verify Commit

**Check commit was created:**

```bash
# See recent commits
git log --oneline -3

# See last commit details
git show HEAD
```

### 7. Check Version Bump (Conditional)

**After successful commit, determine if version bump is needed:**

```bash
# Get the commit message
commit_msg=$(git log -1 --pretty=%B HEAD)

# Check if it's a version-bumping type
if echo "$commit_msg" | grep -qE '^(feat|fix)\(' || \
   echo "$commit_msg" | grep -q 'BREAKING CHANGE'; then
    echo "📦 Version bump needed for this commit"
else
    echo "ℹ️ No version bump needed (docs/test/chore/style/refactor)"
fi
```

**If version bump needed:**

```markdown
📦 **Version bump required** - calling `/bump-version` workflow
```

**Call `/bump-version` workflow:**

- Analyzes conventional commit types since last version
- Determines semantic version bump (major/minor/patch)
- Updates `pyproject.toml` version field
- Creates version commit and git tag
- Returns new version number

**See:** `.windsurf/workflows/bump-version.md`

**Report result:**

```markdown
✅ Version bumped: v0.2.0 → v0.3.0 (minor)
```

**If no bump needed:**

```markdown
ℹ️ No version bump needed (commit type: docs/test/chore)
```

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

### ❌ Don't: Skip Validation

**CRITICAL VIOLATION:** Skipping validation breaks the Normative Core guarantee.

**Bad:**

```bash
git commit --no-verify -m "quick fix"
# Bypasses pre-commit hooks and validation
# VIOLATES: ACF normative verification requirement
```

**Good:**

```bash
/commit
# Runs full validation, ensures quality
# ENFORCES: Normative core "verify before act" principle
```

**Why this matters:**
The Agent Constitution Framework requires that probabilistic reasoning (GENERATE) be validated (VERIFY) before high-stakes external actions (TOOL_CALL). Skipping validation removes this architectural safety guarantee.

### ❌ Don't: Mix Unrelated Changes

**Bad:**

```bash
git commit -m "feat(cli): add command and fix typo and update deps"
# Multiple unrelated changes in one commit
```

**Good:**

```bash
git commit -m "fix(docs): correct typo in README"
git commit -m "chore(deps): update pytest to 8.0.0"
git commit -m "feat(cli): add test-robots command"
# Separate commits for separate concerns
```

### ❌ Don't: Use Vague Messages

**Bad:**

```bash
git commit -m "update code"
git commit -m "fix bug"
git commit -m "changes"
```

**Good:**

```bash
git commit -m "fix(fetcher): handle network timeout in async requests"
git commit -m "refactor(cache): extract key generation to separate function"
```

---

## References

- [Conventional Commits](https://www.conventionalcommits.org/)
- `.windsurf/workflows/validate.md` - Quality gate workflow
- `.windsurf/rules/00_agent_directives.md` - Section 1.7 (Git Operations)
