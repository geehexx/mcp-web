---
pass_through: true
description: Auto-bump version based on conventional commits
title: Bump Version Workflow
tags: ['version', 'automation', 'conventional-commits', 'semantic-versioning']
related: []
---

# Bump Version Workflow

**Purpose:** Automatically determine and apply semantic version bumps based on conventional commit messages.

**Invocation:** `/bump-version` (called by `/commit` or directly)

**Philosophy:** Automate version management using conventional commits.

## Prerequisites

- Conventional commit messages (type: description)
- `pyproject.toml` with version field
- Clean git state

**Conventional Commit Types:**

- `feat:` → **Minor** bump (0.1.0 → 0.2.0)
- `fix:` → **Patch** bump (0.1.0 → 0.1.1)
- `BREAKING CHANGE:` → **Major** bump (0.1.0 → 1.0.0)
- `docs:`, `test:`, `chore:` → **No** bump

## Stage 1: Create Task Plan

```typescript
update_plan({
  explanation: "📦 Starting /bump-version workflow",
  plan: [
    { step: "1. /bump-version - Analyze commits and calculate version", status: "in_progress" },
    { step: "2. /bump-version - Update project files", status: "pending" },
    { step: "3. /bump-version - Create git tag and validate", status: "pending" }
  ]
})
```

## Stage 2: Analyze Commits

### 2.1 Get Recent Commits

**Get commits since last tag:**

```bash
git log --oneline --since="$(git describe --tags --abbrev=0 2>/dev/null || echo '1970-01-01')" --pretty=format:"%s"
```

### 2.2 Parse Commit Messages

**Identify conventional commit types:**

- `feat:` - New features
- `fix:` - Bug fixes
- `BREAKING CHANGE:` - Breaking changes
- `docs:` - Documentation
- `test:` - Tests
- `chore:` - Maintenance

### 2.3 Calculate Version Bump

**Determine bump type:**

- **Major** (1.0.0 → 2.0.0): Breaking changes
- **Minor** (1.0.0 → 1.1.0): New features
- **Patch** (1.0.0 → 1.0.1): Bug fixes
- **None**: Documentation, tests, chores

## Stage 3: Update Project Files

### 3.1 Update pyproject.toml

**Update version field:**

```toml
[project]
version = "1.1.0"  # Updated version
```

### 3.2 Update **init**.py

**Update version in package:**

```python
__version__ = "1.1.0"
```

### 3.3 Update CHANGELOG.md

**Add new version entry:**

```markdown
## [1.1.0] - 2025-10-22

### Added
- New feature 1
- New feature 2

### Fixed
- Bug fix 1
- Bug fix 2

### Changed
- Breaking change 1
- Breaking change 2
```

## Stage 4: Create Git Tag

### 4.1 Create Tag

**Create annotated tag:**

```bash
git tag -a v1.1.0 -m "Release version 1.1.0

- New features: [list]
- Bug fixes: [list]
- Breaking changes: [list]"
```

### 4.2 Validate Tag

**Verify tag creation:**

```bash
git tag -l | grep v1.1.0
git show v1.1.0
```

## Stage 5: Update Documentation

### 5.1 Update README

**Update version references:**

```markdown
## Installation

```bash
pip install mcp-web==1.1.0
```

### 5.2 Update API Documentation

**Update version in API docs:**
```markdown
# API Version 1.1.0

[API documentation content]
```

## Stage 6: Commit Changes

### 6.1 Commit Version Bump

```bash
git add pyproject.toml src/mcp_web/__init__.py CHANGELOG.md
git commit -m "chore: bump version to 1.1.0

- Version: 1.1.0
- Changes: [list of changes]
- Tag: v1.1.0"
```

### 6.2 Push Tag

```bash
git push origin v1.1.0
```

## Context Loading

Load these rules if you determine you need them based on their descriptions:

- **Documentation Standards**: `/rules/03_documentation.mdc` - Apply when updating documentation
- **Context Optimization**: `/rules/07_context_optimization.mdc` - Apply when dealing with large files or complex operations

## Workflow References

When this bump-version workflow is called:

1. **Load**: `/commands/bump-version.md`
2. **Execute**: Follow the version bumping stages defined above
3. **Analyze**: Parse conventional commits
4. **Update**: Update project files
5. **Tag**: Create git tag

## Anti-Patterns

❌ **Don't:**

- Skip commit analysis
- Ignore conventional commits
- Skip validation
- Create invalid tags

✅ **Do:**

- Analyze all commits
- Follow conventional commit format
- Validate version changes
- Create proper tags

## Success Metrics

| Metric | Target | Status |
|--------|--------|--------|
| Commit analysis | 100% | ✅ |
| Version accuracy | 100% | ✅ |
| Tag creation | 100% | ✅ |
| Documentation update | 100% | ✅ |

## Integration

**Called By:**

- `/commit` - After commits
- User - Direct invocation for version bumping

**Calls:**

- Git operations
- File updates
- Tag creation

**Exit:**

```markdown
✅ **Completed /bump-version:** Version bumping finished
```

---

## Command Metadata

**File:** `bump-version.yaml`
**Type:** Command/Workflow
**Complexity:** Moderate
**Estimated Tokens:** ~1,900
**Last Updated:** 2025-10-22
**Status:** Active

**Topics Covered:**

- Version management
- Conventional commits
- Semantic versioning
- Automation

**Dependencies:**

- None (standalone workflow)
