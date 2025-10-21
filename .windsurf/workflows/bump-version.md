---
created: "2025-10-17"
updated: "2025-10-18"
description: Auto-bump version based on conventional commits
auto_execution_mode: 3
category: Automation
complexity: 70
tokens: 2663
dependencies: []
status: active
---

# Bump Version Workflow

**Purpose:** Automatically determine and apply semantic version bumps based on conventional commit messages.

**Invocation:** `/bump-version` (called by `/commit` or directly)

**Philosophy:** Automate version management using conventional commits to eliminate manual version tracking.

---

## Stage 0: Create Task Plan

🔄 **Entering /bump-version workflow**

**Create task plan:**

```typescript
update_plan({
  explanation: "📦 Starting /bump-version workflow",
  plan: [
    { step: "1. /bump-version - Analyze commits since last version", status: "in_progress" },
    { step: "2. /bump-version - Calculate new version", status: "pending" },
    { step: "3. /bump-version - Update project files", status: "pending" },
    { step: "4. /bump-version - Create git tag", status: "pending" },
    { step: "5. /bump-version - Validate version consistency", status: "pending" }
  ]
})
```

---

## Prerequisites

**Requirements:**

- Conventional commit messages (type: description)
- `pyproject.toml` with version field
- Clean git state (all changes committed)

**Conventional Commit Types:**

- `feat:` → **Minor** bump (0.1.0 → 0.2.0)
- `fix:` → **Patch** bump (0.1.0 → 0.1.1)
- `BREAKING CHANGE:` → **Major** bump (0.1.0 → 1.0.0)
- `docs:`, `test:`, `chore:` → **No** bump

---

## Stage 1: Analyze Commits

### 1.1 Get Commits Since Last Version

```bash
# Get current version from pyproject.toml
current_version=$(grep -m 1 'version = ' pyproject.toml | cut -d'"' -f2)

# Get all commits since last version tag
git log v${current_version}..HEAD --pretty=format:"%s" 2>/dev/null || \
git log --pretty=format:"%s" -10  # Fallback if no version tag
```

### 1.2 Parse Commit Types

**Extract conventional commit types:**

```bash
# Check for breaking changes
breaking=$(git log --grep="BREAKING CHANGE" --pretty=format:"%s" | wc -l)

# Check for features
features=$(git log --grep="^feat" --pretty=format:"%s" | wc -l)

# Check for fixes
fixes=$(git log --grep="^fix" --pretty=format:"%s" | wc -l)
```

### 1.3 Determine Bump Type

**Decision logic:**

```python
if breaking_changes > 0:
    bump_type = "major"  # 0.1.0 → 1.0.0
elif features > 0:
    bump_type = "minor"  # 0.1.0 → 0.2.0
elif fixes > 0:
    bump_type = "patch"  # 0.1.0 → 0.1.1
else:
    bump_type = None     # No version bump needed
```

**Special Cases:**

- **Pre-1.0.0:** Breaking changes bump minor (0.x.y → 0.x+1.0)
- **Multiple types:** Use highest priority (major > minor > patch)
- **No relevant commits:** Skip version bump

---

## Stage 2: Calculate New Version

### 2.1 Read Current Version

```python
# Read pyproject.toml
mcp0_read_text_file("/home/gxx/projects/mcp-web/pyproject.toml")

# Extract version line
# Example: version = "0.2.1"
```

### 2.2 Parse Version Components

```python
import re

version_pattern = r'version = "(\d+)\.(\d+)\.(\d+)"'
match = re.search(version_pattern, pyproject_content)

major = int(match.group(1))
minor = int(match.group(2))
patch = int(match.group(3))
```

### 2.3 Apply Bump

```python
if bump_type == "major":
    if major == 0:
        # Pre-1.0: Breaking change bumps minor
        new_version = f"0.{minor + 1}.0"
    else:
        new_version = f"{major + 1}.0.0"
elif bump_type == "minor":
    new_version = f"{major}.{minor + 1}.0"
elif bump_type == "patch":
    new_version = f"{major}.{minor}.{patch + 1}"
else:
    new_version = None  # No bump
```

**Version Bumping Rules (Semantic Versioning):**

| Current | Bump Type | New Version | Notes |
|---------|-----------|-------------|-------|
| 0.1.0 | major | 0.2.0 | Pre-1.0: BREAKING → minor |
| 0.1.0 | minor | 0.2.0 | Feature added |
| 0.1.0 | patch | 0.1.1 | Bug fix |
| 1.0.0 | major | 2.0.0 | Post-1.0: BREAKING → major |
| 1.0.0 | minor | 1.1.0 | Feature added |
| 1.0.0 | patch | 1.0.1 | Bug fix |

---

## Stage 3: Update Project Files

### 3.1 Update pyproject.toml

```python
# Update version in pyproject.toml
edit(
    file_path="/home/gxx/projects/mcp-web/pyproject.toml",
    old_string=f'version = "{current_version}"',
    new_string=f'version = "{new_version}"',
    explanation=f"Bump version {current_version} → {new_version} ({bump_type})"
)
```

### 3.2 Update PROJECT_SUMMARY.md

```python
# Update version in PROJECT_SUMMARY.md
edit(
    file_path="/home/gxx/projects/mcp-web/PROJECT_SUMMARY.md",
    old_string=f"**Version:** {current_version}",
    new_string=f"**Version:** {new_version}",
    explanation="Sync version with pyproject.toml"
)
```

### 3.3 Update CHANGELOG.md (If Exists)

```python
# Convert [Unreleased] to versioned release
edit(
    file_path="/home/gxx/projects/mcp-web/docs/reference/CHANGELOG.md",
    old_string="## [Unreleased]",
    new_string=f"## [Unreleased]\n\n## [{new_version}] - {date.today()}",
    explanation="Release unreleased changes as new version"
)
```

---

## Stage 4: Create Git Tag

### 4.1 Commit Version Bump

```bash
git add pyproject.toml PROJECT_SUMMARY.md docs/reference/CHANGELOG.md
git commit -m "chore: bump version to ${new_version}

Bump type: ${bump_type}
Changes: ${commit_count} commits since last version

Automated version bump via /bump-version workflow"
```

### 4.2 Create Annotated Tag

```bash
git tag -a "v${new_version}" -m "Release version ${new_version}

$(git log v${previous_version}..HEAD --pretty=format:'- %s' | head -20)"
```

### 4.3 Verify Tag Created

```bash
# Confirm tag exists
git tag -l "v${new_version}"

# Show tag details
git show "v${new_version}" --no-patch
```

---

## Stage 5: Validation

### 5.1 Verify Version Consistency

**Check all version references match:**

```bash
# pyproject.toml
grep 'version = ' pyproject.toml

# PROJECT_SUMMARY.md
grep '**Version:**' PROJECT_SUMMARY.md

# Git tag
git describe --tags
```

**All should show:** `${new_version}`

### 5.2 Test Installation

```bash
# Test package installs with new version
uv build
uv pip install dist/mcp_web-${new_version}-py3-none-any.whl --dry-run
```

### 5.3 Check Changelog Format

```bash
# Validate changelog syntax
npx markdownlint-cli2 docs/reference/CHANGELOG.md
```

---

## Integration

### 5.1 When Called from `/commit`

**Automatic integration:**

```yaml
/commit:
  1. Review and commit code changes
  2. Check commit message type
  3. If feat/fix/breaking → Call /bump-version
  4. Update version files
  5. Create version tag
  6. Complete
```

### 5.2 When Called Directly

**Manual invocation:**

```bash
# User: "/bump-version"
# AI: Analyze commits since last version
# AI: Determine bump type
# AI: Apply version bump
# AI: Create git tag
```

---

## Examples

### Example 1: Feature Release

**Commits since v0.2.0:**

```text
feat(cli): add test-robots command
feat(cache): implement TTL-based expiration
fix(fetcher): handle timeout gracefully
docs: update README with examples
```

**Analysis:**

- Breaking changes: 0
- Features: 2
- Fixes: 1
- **Bump type: minor** (features present)

**Result:**

- Version: `0.2.0` → `0.3.0`
- Files updated: `pyproject.toml`, `PROJECT_SUMMARY.md`, `CHANGELOG.md`
- Tag created: `v0.3.0`

### Example 2: Patch Release

**Commits since v0.2.1:**

```text
fix(security): sanitize HTML in extracted content
fix(tests): resolve async test timing issue
test: add golden data test for summarization
```

**Analysis:**

- Breaking changes: 0
- Features: 0
- Fixes: 2
- **Bump type: patch** (only fixes)

**Result:**

- Version: `0.2.1` → `0.2.2`
- Tag created: `v0.2.2`

### Example 3: Breaking Change

**Commits since v0.9.5:**

```text
feat(api): add async support for all methods

BREAKING CHANGE: All API methods now return coroutines
```

**Analysis:**

- Breaking changes: 1
- **Bump type: minor** (pre-1.0, so breaking → minor)

**Result:**

- Version: `0.9.5` → `0.10.0`
- Tag created: `v0.10.0`

### Example 4: No Bump Needed

**Commits since v0.2.0:**

```text
docs: fix typo in README
test: add unit test for edge case
chore: update .gitignore
```

**Analysis:**

- No feat/fix/breaking commits
- **Bump type: None**

**Result:**

- No version change
- Skip workflow

---

## Decision Matrix

| Commit Types Present | Current Version | Bump Type | New Version |
|---------------------|-----------------|-----------|-------------|
| feat + fix | 0.2.0 | minor | 0.3.0 |
| fix only | 0.2.1 | patch | 0.2.2 |
| BREAKING | 0.9.0 | minor* | 0.10.0 |
| BREAKING | 1.0.0 | major | 2.0.0 |
| docs + test | 0.2.0 | none | 0.2.0 |
| feat + BREAKING | 0.3.0 | minor* | 0.4.0 |
| feat + BREAKING | 1.0.0 | major | 2.0.0 |

*Pre-1.0 versions: BREAKING bumps minor, not major

---

## Anti-Patterns

### ❌ Don't: Manually Edit Version Numbers

**Bad:**

```bash
# Edit pyproject.toml manually
version = "0.3.0"
git commit -m "update version"
```

**Good:**

```bash
# Use workflow
/bump-version
# Analyzes commits, applies correct bump
```

### ❌ Don't: Skip Conventional Commits

**Bad:**

```bash
git commit -m "added feature"
git commit -m "wip"
git commit -m "fixed bug"
```

**Good:**

```bash
git commit -m "feat: add test-robots command"
git commit -m "fix: handle timeout errors"
```

### ❌ Don't: Bump Version for Every Commit

**Bad:**

```markdown
Every commit → bump patch → v0.2.1, v0.2.2, v0.2.3, ...
Result: Version inflation, meaningless releases
```

**Good:**

```markdown
Group related changes → bump once → v0.2.1, v0.3.0, v1.0.0
Result: Semantic versions reflect actual releases
```

---

## Tools & Alternatives

### Python Version Bump Tools

**Evaluated options:**

1. **bump-my-version** ([GitHub](https://github.com/callowayproject/bump-my-version))
   - ✅ Python-native
   - ✅ Configurable
   - ✅ Supports multiple files
   - ❌ Requires configuration

2. **commitizen** ([Documentation](https://commitizen-tools.github.io/commitizen/))
   - ✅ Full conventional commit workflow
   - ✅ Changelog generation
   - ✅ Version bumping
   - ⚠️ Opinionated workflow

3. **semantic-release** ([GitHub](https://github.com/semantic-release/semantic-release))
   - ✅ Industry standard
   - ✅ CI/CD integration
   - ❌ Node.js dependency
   - ❌ Complex for Python projects

**Chosen:** Custom implementation (this workflow)

- No external dependencies
- Full control over logic
- Integrated with Windsurf workflows

---

## References

- [Semantic Versioning 2.0.0](https://semver.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [PEP 440 (Python Versioning)](https://peps.python.org/pep-0440/)

---
