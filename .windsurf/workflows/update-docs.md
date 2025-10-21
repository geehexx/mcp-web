---
created: "2025-10-17"
updated: "2025-10-21"
description: Update PROJECT_SUMMARY.md and CHANGELOG.md
auto_execution_mode: 3
category: Automation
complexity: 55
tokens: 1500
dependencies: []
status: active
---

# Update Documentation Workflow

**Purpose:** Update living documentation (PROJECT_SUMMARY.md, CHANGELOG.md) when significant changes occur.

**Invocation:** `/update-docs` (called by `/work`, `/commit`, or directly)

**Philosophy:** Keep living docs synchronized without manual overhead.

---

## When to Update

| Document | Update Triggers |
|----------|----------------|
| **PROJECT_SUMMARY.md** | Major milestones, initiative completion, architecture changes, ADR creation, core features |
| **CHANGELOG.md** | User-facing features, breaking changes, API changes, bug fixes (preparing release) |

**Don't update for:** WIP, internal refactoring, minor docs, test-only changes

---

## Stage 1: Create Task Plan

```typescript
update_plan({
  explanation: "📝 Starting /update-docs workflow",
  plan: [
    { step: "1. /update-docs - Determine what needs updating", status: "in_progress" },
    { step: "2. /update-docs - Update PROJECT_SUMMARY.md", status: "pending" },
    { step: "3. /update-docs - Update CHANGELOG.md", status: "pending" }
  ]
})
```

---

## Stage 2: Analyze Changes

### Get Recent Changes

```bash
# Get commits since last update
git log --oneline --since="7 days ago"

# Analyze commit types
git log --format="%s" --since="7 days ago" | grep -oE "^[a-z]+\(" | sort | uniq -c
```

### Determine Significance

| Commit Type | Significance | Update Docs? |
|-------------|--------------|--------------|
| `feat:` (user-facing) | High | Yes (both) |
| `fix:` (critical) | Medium | CHANGELOG only |
| `BREAKING:` | Critical | Yes (both) |
| `docs:`, `test:`, `refactor:` | Low | No |
| Initiative complete | High | PROJECT_SUMMARY |
| ADR created | Medium | PROJECT_SUMMARY |

---

## Stage 3: Update PROJECT_SUMMARY.md

### What to Update

```markdown
## Updates Needed

**Version:** [If releasing]
**Status:** [Project phase change]
**Key Features:** [New major features]
**Recent Work:** [Completed initiatives]
**Related ADRs:** [New ADRs]
```

### Update Procedure

```python
# Read current content
mcp0_read_text_file("/home/gxx/projects/mcp-web/PROJECT_SUMMARY.md")

# Update sections
edit(
    file_path="/home/gxx/projects/mcp-web/PROJECT_SUMMARY.md",
    old_string="**Status:** [old status]",
    new_string="**Status:** [new status]",
    explanation="Update project status after [milestone]"
)

# Add to Recent Work section
edit(
    file_path="/home/gxx/projects/mcp-web/PROJECT_SUMMARY.md",
    old_string="## Recent Work\n\n",
    new_string="## Recent Work\n\n- **[YYYY-MM-DD]**: [Completed initiative/milestone]\n",
    explanation="Add recent accomplishment"
)
```

---

## Stage 4: Update CHANGELOG.md

### CHANGELOG Structure

```markdown
# Changelog

## [Unreleased]

### Added
- New feature descriptions

### Changed
- Modified behavior descriptions

### Deprecated
- Features to be removed

### Removed
- Deleted features

### Fixed
- Bug fix descriptions

### Security
- Security improvements

## [X.Y.Z] - YYYY-MM-DD

[Released changes...]
```

### Extract Changes from Commits

```bash
# Get commits since last version
current_version=$(grep -m 1 'version = ' pyproject.toml | cut -d'"' -f2)
git log v${current_version}..HEAD --format="- %s"

# Group by type
git log v${current_version}..HEAD --format="%s" | \
  awk -F: '{type=$1; gsub(/\(.*\)/, "", type); print type": "$2}'
```

### Update CHANGELOG.md

```python
# Add to Unreleased section
edit(
    file_path="/home/gxx/projects/mcp-web/docs/reference/CHANGELOG.md",
    old_string="## [Unreleased]\n\n",
    new_string="""## [Unreleased]

### Added
- [New feature]

### Fixed
- [Bug fix]

""",
    explanation="Add unreleased changes from recent commits"
)
```

---

## Stage 5: Validation

### Check Consistency

```bash
# Validate markdown
task docs:lint

# Check version consistency
grep 'version = ' pyproject.toml
grep '**Version:**' PROJECT_SUMMARY.md
grep '## \[' docs/reference/CHANGELOG.md | head -2

# Preview changes
git diff PROJECT_SUMMARY.md docs/reference/CHANGELOG.md
```

### Commit Updates

```bash
git add PROJECT_SUMMARY.md docs/reference/CHANGELOG.md
git commit -m "docs: update living documentation

- PROJECT_SUMMARY.md: [what changed]
- CHANGELOG.md: [what added]

Related: [initiative/ADR if applicable]"
```

---

## Decision Matrix

| Change Type | PROJECT_SUMMARY | CHANGELOG |
|-------------|-----------------|-----------|
| Initiative complete | ✅ Yes | ⚠️ If user-facing |
| Major feature | ✅ Yes | ✅ Yes |
| Bug fix (critical) | ❌ No | ✅ Yes |
| ADR created | ✅ Yes | ❌ No |
| Refactoring | ❌ No | ❌ No |
| Breaking change | ✅ Yes | ✅ Yes |
| Security fix | ⚠️ Maybe | ✅ Yes |

---

## Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| Add every commit to CHANGELOG | Group significant changes only |
| Update for WIP | Wait for completion |
| Generic "updated docs" | Specific: "add MCP server capabilities" |
| Duplicate PROJECT_SUMMARY in CHANGELOG | Different audiences/purposes |
| Mix WIP in Unreleased | Completed, tested changes only |

---

## Integration

**Called By:** `/work`, `/commit`, `/meta-analysis`, User

**Calls:** None (leaf workflow)

---

## References

- [Keep a Changelog](https://keepachangelog.com/)
- [Semantic Versioning](https://semver.org/)
- `PROJECT_SUMMARY.md`
- `docs/reference/CHANGELOG.md`
