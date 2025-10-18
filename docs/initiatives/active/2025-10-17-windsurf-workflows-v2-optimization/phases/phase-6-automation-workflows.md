# Phase 6: Automation Workflows

**Status:** ⏳ Planned
**Priority:** MEDIUM
**Duration:** 5-8 hours
**Owner:** AI Agent

---

## Objective

Validate and enhance existing automation workflows for version bumping and documentation updates.

**Target:** Fully automated version management and documentation maintenance

---

## Background

Research recommended automated version management using conventional commits and semantic versioning. Two workflows already exist but need validation and enhancement.

**Existing Workflows:**

- `/bump-version` (10,006 bytes) - Version bumping automation
- `/update-docs` (8,797 bytes) - Documentation update automation

---

## Tasks

### Task 6.1: Validate `/bump-version` Workflow

**Purpose:** Test and refine existing version bump automation

**Current Implementation Review:**

- Read existing workflow:

  ```bash
  cat .windsurf/workflows/bump-version.md
  ```

- Test with actual commit history:

  ```bash
  # Check recent commits
  git log --oneline -20

  # Verify conventional commit format
  git log --format="%s" -20 | grep -E "^(feat|fix|docs|test|refactor|security|chore)"
  ```

- Validate version calculation logic:
  - feat: → minor bump (0.1.0 → 0.2.0)
  - fix: → patch bump (0.1.0 → 0.1.1)
  - BREAKING CHANGE: → major bump (0.1.0 → 1.0.0)

**Testing Checklist:**

- [ ] Parse conventional commit messages correctly
- [ ] Calculate version bump accurately
- [ ] Update all version locations (pyproject.toml, **init**.py, etc.)
- [ ] Generate changelog entry
- [ ] Create git tag
- [ ] Handle edge cases (no commits, invalid format)

**Enhancements Needed:**

- **Add Changelog Generation:**

  ```text
  ## Task: Generate Changelog Entry

  When bumping version, automatically:
  - Extract commit messages since last tag
  - Group by type (Features, Fixes, etc.)
  - Append to CHANGELOG.md
  - Format according to Keep a Changelog standard
  ```

- **Add Validation Step:**

  ```text
  ## Task: Validate Before Bump

  Before bumping version:
  - Verify all tests passing
  - Check no uncommitted changes
  - Verify on main/master branch
  - Confirm last commit follows convention
  ```

- **Add Dry-Run Mode:**

  ```text
  ## Task: Support Dry-Run

  Allow preview of version bump:
  - Show: Current version → New version
  - Display: Commits that triggered bump
  - Preview: Changelog entry
  - Require: Confirmation before applying
  ```

**Effort:** 2-3 hours

---

### Task 6.2: Validate `/update-docs` Workflow

**Purpose:** Test and refine existing documentation update automation

**Current Implementation Review:**

- Read existing workflow:

  ```bash
  cat .windsurf/workflows/update-docs.md
  ```

- Identify update triggers:
  - Major features completed
  - Milestones reached
  - ADRs created
  - Initiative status changed
  - Breaking changes

- Test update logic:

  ```bash
  # Check PROJECT_SUMMARY.md structure
  head -50 PROJECT_SUMMARY.md

  # Check CHANGELOG.md structure
  head -50 CHANGELOG.md
  ```

**Testing Checklist:**

- [ ] Detect when PROJECT_SUMMARY needs update
- [ ] Detect when CHANGELOG needs update
- [ ] Extract relevant information from git history
- [ ] Format updates correctly
- [ ] Preserve existing structure
- [ ] Handle concurrent updates

**Enhancements Needed:**

- **Add Automatic Context Detection:**

  ```text
  ## Task: Detect Update Triggers

  Automatically detect when docs need update:
  - Check git diff for feature additions
  - Scan for new ADR files
  - Check initiative status changes
  - Analyze commit messages for breaking changes
  ```

- **Add Cross-Reference Validation:**

  ```text
  ## Task: Validate Cross-References

  When updating docs:
  - Verify all ADR links valid
  - Check initiative references current
  - Validate external links
  - Update outdated dates
  ```

**Effort:** 2-3 hours

---

### Task 6.3: Create `/generate-workflow-index` Workflow

**Purpose:** Automate generation of workflow indexes from frontmatter

**Background:** Phase 5 creates frontmatter, this workflow keeps indexes current

**Implementation:**

**Workflow Name:** Generate Workflow Index

**Purpose:** Auto-generate workflow and rule indexes from YAML frontmatter

#### Stage 1: Extract Frontmatter

- Parse all workflow files:

  ```bash
  python scripts/generate_indexes.py --workflows
  ```

- Parse all rule files:

  ```bash
  python scripts/generate_indexes.py --rules
  ```

- Extract metadata: category, complexity, tokens, dependencies

#### Stage 2: Generate Indexes

- Generate workflow index:
  - Group by category
  - Sort by complexity (descending)
  - Include token counts and dependencies
  - Output: `.windsurf/workflows/INDEX.md`

- Generate rule index:
  - Sort by priority
  - Include applicability
  - Output: `.windsurf/rules/INDEX.md`

- Generate dependency graph:
  - Extract workflow dependencies
  - Create Mermaid diagram
  - Detect circular dependencies
  - Output: `.windsurf/workflows/DEPENDENCIES.md`

#### Stage 3: Validate Outputs

- Check all indexes generated
- Verify markdown formatting
- Validate Mermaid syntax
- Commit changes if modified

**Success Criteria:**

- ✅ All 3 indexes generated
- ✅ Markdown valid
- ✅ No broken references
- ✅ Committed automatically

**Script Implementation:** (from Phase 5 Task 5.5)

**Effort:** 2-3 hours

---

### Task 6.4: Integrate Automation into CI/CD

**Purpose:** Run automation workflows automatically on relevant triggers

**GitHub Actions Integration:**

### `.github/workflows/auto-version.yml`

```yaml
name: Auto Version Bump

on:
  push:
    branches: [main, master]
    paths-ignore:
      - 'docs/**'
      - '*.md'

jobs:
  version-bump:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0  # Full history for version calculation

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Calculate version bump
        run: python scripts/bump_version.py --dry-run

      - name: Apply version bump
        if: steps.calculate.outputs.should_bump == 'true'
        run: python scripts/bump_version.py --apply

      - name: Commit and tag
        run: |
          git config user.name "github-actions"
          git config user.email "github-actions@github.com"
          git add .
          git commit -m "chore: bump version to ${{ steps.calculate.outputs.new_version }}"
          git tag "v${{ steps.calculate.outputs.new_version }}"
          git push --tags
```

### `.github/workflows/auto-docs.yml`

```yaml
name: Auto Documentation Update

on:
  push:
    branches: [main, master]
    paths:
      - 'docs/adr/*.md'
      - 'docs/initiatives/**/*.md'
      - 'src/**/*.py'

jobs:
  update-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Detect doc updates needed
        run: python scripts/detect_doc_updates.py

      - name: Update PROJECT_SUMMARY
        if: steps.detect.outputs.update_summary == 'true'
        run: python scripts/update_project_summary.py

      - name: Update CHANGELOG
        if: steps.detect.outputs.update_changelog == 'true'
        run: python scripts/update_changelog.py

      - name: Commit changes
        run: |
          git config user.name "github-actions"
          git config user.email "github-actions@github.com"
          git add docs/
          git commit -m "docs: auto-update documentation"
          git push
```

### `.github/workflows/workflow-indexes.yml`

```yaml
name: Update Workflow Indexes

on:
  push:
    branches: [main, master]
    paths:
      - '.windsurf/workflows/*.md'
      - '.windsurf/rules/*.md'

jobs:
  generate-indexes:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Generate indexes
        run: python scripts/generate_indexes.py

      - name: Commit indexes
        run: |
          git config user.name "github-actions"
          git config user.email "github-actions@github.com"
          git add .windsurf/workflows/INDEX.md
          git add .windsurf/rules/INDEX.md
          git add .windsurf/workflows/DEPENDENCIES.md
          git commit -m "docs: update workflow indexes" || echo "No changes"
          git push || echo "No changes to push"
```

**Effort:** 1-2 hours

---

## Success Criteria (Automation)

### Quantitative Metrics

- ✅ `/bump-version` tested and working
- ✅ `/update-docs` tested and working
- ✅ `/generate-workflow-index` created and tested
- ✅ 3 GitHub Actions workflows created
- ✅ 100% automation rate for version bumps

### Qualitative Metrics

- ✅ Zero manual version bumping required
- ✅ Documentation stays current automatically
- ✅ Workflow indexes always accurate
- ✅ CI/CD integration seamless

---

## Validation Steps

### Step 1: Test Version Bumping

```bash
# Create test commit
git checkout -b test-version-bump
echo "test" >> test.txt
git add test.txt
git commit -m "feat: test feature"

# Run bump-version
python scripts/bump_version.py --dry-run

# Expected: Shows version bump (minor)
```

### Step 2: Test Documentation Updates

```bash
# Create test ADR
touch docs/adr/9999-test-decision.md
git add docs/adr/9999-test-decision.md
git commit -m "docs: add test ADR"

# Run update-docs
python scripts/update_project_summary.py --dry-run

# Expected: Shows PROJECT_SUMMARY update needed
```

### Step 3: Test Index Generation

```bash
# Modify workflow frontmatter
echo "updated: 2025-10-18" >> .windsurf/workflows/work.md

# Run index generation
python scripts/generate_indexes.py

# Expected: INDEX.md updated with new date
```

### Step 4: Test CI/CD Integration

```bash
# Push to test branch
git push origin test-automation

# Check GitHub Actions run
# Expected: All 3 workflows execute successfully
```

---

## Deliverables

- ✅ `/bump-version` workflow - Validated and enhanced
- ✅ `/update-docs` workflow - Validated and enhanced
- ✅ `/generate-workflow-index` workflow - Created
- ✅ `scripts/bump_version.py` - Implementation script
- ✅ `scripts/update_project_summary.py` - Implementation script
- ✅ `scripts/update_changelog.py` - Implementation script
- ✅ `scripts/generate_indexes.py` - Implementation script (from Phase 5)
- ✅ `.github/workflows/auto-version.yml` - CI/CD automation
- ✅ `.github/workflows/auto-docs.yml` - CI/CD automation
- ✅ `.github/workflows/workflow-indexes.yml` - CI/CD automation

---

## Dependencies

**Requires:**

- Phase 5 complete (frontmatter provides metadata)

**Enables:**

- Phase 7: Documentation (automation tested and working)
- Phase 8: Quality Automation (CI/CD infrastructure in place)

---

## Completion Notes

**Phase 6 Status:** ⏳ Planned, ready after Phase 5

**Next Phase:** Phase 7 (Documentation & Migration) - Document changes and rollout

**Estimated Timeline:** Week of 2025-10-28 (5-8 hours)
