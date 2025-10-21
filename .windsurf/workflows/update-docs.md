---
created: "2025-10-17"
updated: "2025-10-21"
description: Update PROJECT_SUMMARY.md and CHANGELOG.md
auto_execution_mode: 3
category: Documentation
complexity: 50
tokens: 1000
dependencies: []
status: active
version: "2.0-intelligent-semantic-preservation"
---

# Update Living Docs Workflow

Update PROJECT_SUMMARY.md and/or CHANGELOG.md when triggered.

## Triggers

| Doc | Update When |
|-----|-------------|
| PROJECT_SUMMARY | Major feature, milestone, ADR, initiative complete, architecture change, metrics shift |
| CHANGELOG | User-facing feature, breaking change, major bug, dependency update, release prep |

## Process

### 1. Analyze Changes

```bash
git log --oneline --since="$(cat .windsurf/.last-meta-analysis 2>/dev/null || echo '1 day ago')"
git diff --name-status HEAD~5..HEAD
```

**Extract:** Feature additions, bug fixes, breaking changes, dependencies, ADRs, initiatives

### 2. Update PROJECT_SUMMARY.md

**Sections to update:**

- **Version** (if release): `**Version:** X.Y.Z`
- **Recent Changes**: Add 2-3 sentence summary
- **Features**: Add new capabilities
- **Active Initiatives**: Update progress/complete
- **ADRs**: Add new ADRs to list

```python
edit(
    file_path="PROJECT_SUMMARY.md",
    old_string="**Recent Changes:**\n[Old text]",
    new_string="**Recent Changes:**\n- [Change summary]\n[Old text]",
    explanation="Add recent accomplishments"
)
```

### 3. Update CHANGELOG.md

**Format (Keep a Changelog):**

```markdown
## [Unreleased]

### Added
- New feature

### Fixed
- Bug fix

### Changed
- Breaking change
```

### 4. Validation

```bash
task docs:lint
git diff PROJECT_SUMMARY.md docs/reference/CHANGELOG.md
```

### 5. Commit

```bash
git add PROJECT_SUMMARY.md docs/reference/CHANGELOG.md
git commit -m "docs: update living documentation

- PROJECT_SUMMARY: [what]
- CHANGELOG: [what]

Related: [initiative/ADR]"
```

## Decision Matrix

| Change | PROJECT_SUMMARY | CHANGELOG |
|--------|-----------------|-----------|
| Initiative complete | ✅ | ⚠️ If user-facing |
| Major feature | ✅ | ✅ |
| Bug (critical) | ❌ | ✅ |
| ADR created | ✅ | ❌ |
| Refactoring | ❌ | ❌ |
| Breaking change | ✅ | ✅ |

## Anti-Patterns

❌ Add every commit to CHANGELOG → ✅ Group significant only
❌ Update for WIP → ✅ Wait for completion
❌ Generic "updated docs" → ✅ Specific changes

## References

[Keep a Changelog](https://keepachangelog.com/), [Semantic Versioning](https://semver.org/)
