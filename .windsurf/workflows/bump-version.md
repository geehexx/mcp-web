---
created: "2025-10-17"
updated: "2025-10-21"
description: Auto-bump version based on conventional commits
auto_execution_mode: 3
category: Automation
complexity: 70
tokens: 1900
dependencies: []
status: active
version: "2.0-intelligent-semantic-preservation"
---

# Bump Version Workflow

**Purpose:** Automatically determine and apply semantic version bumps based on conventional commit messages.

**Invocation:** `/bump-version` (called by `/commit` or directly)

**Philosophy:** Automate version management using conventional commits.

---

## Prerequisites

- Conventional commit messages (type: description)
- `pyproject.toml` with version field
- Clean git state

**Conventional Commit Types:**

- `feat:` → **Minor** bump (0.1.0 → 0.2.0)
- `fix:` → **Patch** bump (0.1.0 → 0.1.1)
- `BREAKING CHANGE:` → **Major** bump (0.1.0 → 1.0.0)
- `docs:`, `test:`, `chore:` → **No** bump

---

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

---

## Stage 2: Analyze Commits & Calculate Version

### Get Commits Since Last Version

```bash
# Get current version
current_version=$(grep -m 1 'version = ' pyproject.toml | cut -d'"' -f2)

# Get commits since last tag
git log v${current_version}..HEAD --pretty=format:"%s" 2>/dev/null || \
git log --pretty=format:"%s" -10
```

### Determine Bump Type

```bash
# Check for breaking/features/fixes
breaking=$(git log --grep="BREAKING CHANGE" --format="%s" | wc -l)
features=$(git log --grep="^feat" --format="%s" | wc -l)
fixes=$(git log --grep="^fix" --format="%s" | wc -l)
```

**Decision logic:**

```python
if breaking > 0:
    bump = "major"  # 0.1.0 → 1.0.0 (or 0.2.0 if pre-1.0)
elif features > 0:
    bump = "minor"  # 0.1.0 → 0.2.0
elif fixes > 0:
    bump = "patch"  # 0.1.0 → 0.1.1
else:
    bump = None     # No bump needed
```

### Calculate New Version

| Current | Bump | Pre-1.0 Result | Post-1.0 Result |
|---------|------|----------------|-----------------|
| 0.1.0 | major | 0.2.0 | N/A |
| 0.1.0 | minor | 0.2.0 | N/A |
| 0.1.0 | patch | 0.1.1 | N/A |
| 1.0.0 | major | N/A | 2.0.0 |
| 1.0.0 | minor | N/A | 1.1.0 |
| 1.0.0 | patch | N/A | 1.0.1 |

**Note:** Pre-1.0 breaking changes bump minor (not major)

**Update plan:**

```typescript
update_plan({
  explanation: "Version calculated, updating files",
  plan: [
    { step: "1. /bump-version - Analyze commits and calculate version", status: "completed" },
    { step: "2. /bump-version - Update project files", status: "in_progress" },
    // ...
  ]
})
```

---

## Stage 3: Update Project Files

### Update Files

```python
# pyproject.toml
edit(
    file_path="/home/gxx/projects/mcp-web/pyproject.toml",
    old_string=f'version = "{current_version}"',
    new_string=f'version = "{new_version}"',
    explanation=f"Bump version {current_version} → {new_version} ({bump_type})"
)

# PROJECT_SUMMARY.md
edit(
    file_path="/home/gxx/projects/mcp-web/PROJECT_SUMMARY.md",
    old_string=f"**Version:** {current_version}",
    new_string=f"**Version:** {new_version}",
    explanation="Sync version"
)

# CHANGELOG.md (if exists)
edit(
    file_path="/home/gxx/projects/mcp-web/docs/reference/CHANGELOG.md",
    old_string="## [Unreleased]",
    new_string=f"## [Unreleased]\n\n## [{new_version}] - {today()}",
    explanation="Release changes"
)
```

**Update plan:**

```typescript
update_plan({
  explanation: "Files updated, creating tag",
  plan: [
    { step: "2. /bump-version - Update project files", status: "completed" },
    { step: "3. /bump-version - Create git tag and validate", status: "in_progress" }
  ]
})
```

---

## Stage 4: Create Tag & Validate

### Commit & Tag

```bash
# Commit version bump
git add pyproject.toml PROJECT_SUMMARY.md CHANGELOG.md
git commit -m "chore: bump version to ${new_version}

Bump type: ${bump_type}
Automated via /bump-version"

# Create annotated tag
git tag -a "v${new_version}" -m "Release ${new_version}"
```

### Validate

```bash
# Verify consistency
grep 'version = ' pyproject.toml
grep '**Version:**' PROJECT_SUMMARY.md
git describe --tags

# Test build
uv build
```

**All should show:** `${new_version}`

---

## Examples

### Feature Release

**Commits since v0.2.0:**

```text
feat(cli): add test-robots command
feat(cache): implement TTL expiration
fix(fetcher): handle timeout
```

**Result:** `0.2.0` → `0.3.0` (minor bump, features present)

### Patch Release

**Commits since v0.2.1:**

```text
fix(security): sanitize HTML
fix(tests): resolve timing issue
```

**Result:** `0.2.1` → `0.2.2` (patch bump, only fixes)

### Breaking Change (Pre-1.0)

**Commits since v0.9.5:**

```text
feat(api): add async support
BREAKING CHANGE: All methods now async
```

**Result:** `0.9.5` → `0.10.0` (minor bump for pre-1.0)

---

## Decision Matrix

| Commit Types | Current | Bump | New |
|--------------|---------|------|-----|
| feat + fix | 0.2.0 | minor | 0.3.0 |
| fix only | 0.2.1 | patch | 0.2.2 |
| BREAKING | 0.9.0 | minor* | 0.10.0 |
| BREAKING | 1.0.0 | major | 2.0.0 |
| docs/test | 0.2.0 | none | 0.2.0 |

*Pre-1.0: BREAKING → minor

---

## Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| Manually edit version numbers | Use `/bump-version` workflow |
| Skip conventional commits | Use `feat:`, `fix:`, etc. |
| Bump for every commit | Group changes, bump on release |

---

## Tools Considered

| Tool | Pros | Cons | Decision |
|------|------|------|----------|
| **bump-my-version** | Python-native, configurable | Requires config | ✅ Good option |
| **commitizen** | Full workflow, changelog | Opinionated | Alternative |
| **semantic-release** | Comprehensive | Heavy, Node-based | Not needed |
| **Custom workflow** | Zero deps, full control | Manual maintenance | ✅ **Selected** |

**Rationale:** Custom workflow provides full control, zero external dependencies, and perfect fit for AI agent automation.

---

## Integration

**Called By:** `/commit` - After code committed

**Calls:** Git commands, file edits

---

## References

- [Semantic Versioning](https://semver.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [bump-my-version](https://github.com/callowayproject/bump-my-version)

---
