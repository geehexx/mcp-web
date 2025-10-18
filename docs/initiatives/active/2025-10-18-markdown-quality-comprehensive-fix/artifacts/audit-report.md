# Markdown Quality Audit Report

**Date:** 2025-10-18
**Scope:** All markdown files excluding `docs/archive/`
**Tool:** markdownlint-cli2 v0.18.1 (markdownlint v0.38.0)

## Executive Summary

**Total Files Analyzed:** 93 markdown files
**Current Status:** 75 violations detected (using markdownlint-cli)

**Critical Finding:** Discrepancy between markdownlint-cli2 (4,188 errors reported) and markdownlint-cli (75 errors). This suggests configuration differences or different rule sets.

## Error Breakdown by Rule

| Rule ID | Count | Description | Fixable | Priority |
|---------|-------|-------------|---------|----------|
| MD032 | 46 | Lists should be surrounded by blank lines | ✅ Auto | High |
| MD040 | 11 | Fenced code blocks should have a language specified | ⚠️ Manual | High |
| MD022 | 8 | Headings should be surrounded by blank lines | ✅ Auto | Medium |
| MD031 | 5 | Fenced code blocks should be surrounded by blank lines | ✅ Auto | Medium |
| MD036 | 3 | Emphasis used instead of heading | ⚠️ Manual | Low |
| MD024 | 1 | Multiple headings with the same content | ⚠️ Manual | Low |
| MD009 | 1 | Trailing spaces | ✅ Auto | Low |

**Total:** 75 violations

## Detailed Rule Analysis

### MD032: Lists should be surrounded by blank lines (46 violations)

**Impact:** High - Affects rendering in some parsers (e.g., kramdown)
**Auto-fixable:** Yes
**Fix strategy:** Run `markdownlint-cli2 --fix`

**Example violation:**

```markdown
Some text
* List item

# Should be:
Some text

* List item
```

**Files most affected:**

- Workflow files in `.windsurf/workflows/`
- Guide files in `docs/guides/`
- Initiative files in `docs/initiatives/`

---

### MD040: Fenced code blocks should have a language specified (11 violations)

**Impact:** High - Missing syntax highlighting, degraded UX
**Auto-fixable:** No (requires manual language identification)
**Fix strategy:** Manual review and addition of language specifiers

**Example violation:**

```text
code here
```

# Should be:

```bash
code here
```

**Affected files:**

- `.windsurf/workflows/bump-version.md` (4 violations)
- `.windsurf/workflows/research.md` (6 violations)
- `.windsurf/workflows/plan.md` (1 violation)

**Common language specifiers needed:**

- `bash` - Shell commands
- `text` - Plain text output
- `markdown` - Markdown examples
- `yaml` - YAML configuration
- `python` - Python code
- `json` - JSON data

---

### MD022: Headings should be surrounded by blank lines (8 violations)

**Impact:** Medium - Aesthetic and readability
**Auto-fixable:** Yes
**Fix strategy:** Run `markdownlint-cli2 --fix`

---

### MD031: Fenced code blocks should be surrounded by blank lines (5 violations)

**Impact:** Medium - Affects some parsers
**Auto-fixable:** Yes
**Fix strategy:** Run `markdownlint-cli2 --fix`

---

### MD036: Emphasis used instead of heading (3 violations)

**Impact:** Low - Semantic correctness
**Auto-fixable:** No (requires judgment call)
**Fix strategy:** Manual review - change `**bold text**` to `### Heading` where appropriate

**Affected files:**

- `.windsurf/workflows/detect-context.md` (all 3 violations)

**Example:**

```markdown
**Priority 1: Session Summary Signals**

# Should potentially be:
### Priority 1: Session Summary Signals
```

---

### MD024: Multiple headings with the same content (1 violation)

**Impact:** Low - Navigation and linking issues
**Auto-fixable:** No
**Fix strategy:** Manual review - make headings unique or use `siblings_only` config

---

### MD009: Trailing spaces (1 violation)

**Impact:** Low - Code cleanliness
**Auto-fixable:** Yes
**Fix strategy:** Run `markdownlint-cli2 --fix` or pre-commit hook

---

## Configuration Analysis

### Current Configuration (`.markdownlint-cli2.jsonc`)

**Strengths:**

- Custom rule for closing fence info strings
- Appropriate MD013 line length settings (280 chars)
- Good ignore patterns (archive, pytest_cache)
- Auto-fix enabled in pre-commit hook

**Gaps:**

- MD040 enabled but violations present (11 cases)
- MD032 violations suggest rules not enforced in all contexts
- No automated tests for markdown quality

### Current Pre-commit Hook

**Status:** ✅ Configured with `--fix` flag
**Issue:** Not preventing new violations

**Possible reasons:**

1. Hooks not run consistently (manual commits)
2. Docker version used (`markdownlint-cli2-docker`) may have issues
3. Exclude patterns may be too broad
4. Some violations introduced before hook was added

---

## Tool Comparison Analysis

### markdownlint-cli2 vs markdownlint-cli

**markdownlint-cli2 (current):**

- ✅ Modern, actively maintained
- ✅ Better glob support
- ✅ JSON output formatter support
- ✅ Custom rules support
- ⚠️ Reports 4,188 errors (seems inflated)

**markdownlint-cli (legacy):**

- ✅ Simple, reliable
- ✅ Clear error reporting
- ✅ Reports 75 errors (more realistic)
- ⚠️ Less feature-rich

**Recommendation:** Continue with markdownlint-cli2 but investigate error count discrepancy.

---

## Files Requiring Manual Attention

### High Priority (Code Fence Language Specifiers)

1. `.windsurf/workflows/bump-version.md` (4 violations)
2. `.windsurf/workflows/research.md` (6 violations)
3. `.windsurf/workflows/plan.md` (1 violation)

### Medium Priority (Structural Issues)

1. `.windsurf/workflows/detect-context.md` (3 MD036 violations)

---

## Regression Prevention Analysis

### Current Prevention Mechanisms

1. ✅ Pre-commit hook with markdownlint-cli2-docker
2. ✅ Taskfile command: `task docs:lint:markdown`
3. ✅ Taskfile command: `task docs:fix`
4. ❌ No automated CI checks for markdown quality
5. ❌ No regression tests for markdown quality

### Gaps Identified

1. **No CI enforcement** - Markdown violations can slip through
2. **No test suite** - Can't verify markdown quality programmatically
3. **Manual verification only** - Relies on pre-commit hooks being run
4. **No quality gates** - No automated blocking of invalid markdown

### Recommendations

1. Add markdown quality tests to test suite
2. Add CI check for markdown linting
3. Consider Vale for prose quality (optional)
4. Update documentation standards with examples

---

## Auto-fix vs Manual Fix Breakdown

### Auto-fixable (60 violations - 80%)

- MD032: 46 violations (Lists with blank lines)
- MD022: 8 violations (Headings with blank lines)
- MD031: 5 violations (Fences with blank lines)
- MD009: 1 violation (Trailing spaces)

**Strategy:** Run `npx markdownlint-cli2 --fix "**/*.md"`

### Manual Fixes Required (15 violations - 20%)

- MD040: 11 violations (Code fence language specifiers)
- MD036: 3 violations (Emphasis vs headings)
- MD024: 1 violation (Duplicate headings)

**Strategy:** Manual review and targeted fixes

---

## Recommendations

### Immediate Actions (Phase 3)

1. ✅ Run auto-fix: `task docs:fix`
2. ✅ Commit auto-fixes separately
3. ✅ Verify no breakage

### Manual Fixes (Phase 4)

1. ⚠️ Add language specifiers to 11 code fences
2. ⚠️ Fix 3 emphasis-as-heading issues
3. ⚠️ Resolve 1 duplicate heading

### Long-term Prevention (Phases 5-6)

1. 🔧 Add markdown quality tests to test suite
2. 🔧 Add CI workflow for markdown validation
3. 🔧 Update documentation standards
4. 🔧 Consider Vale for prose linting (research in Phase 2)

---

## Success Criteria

**Phase 3 Complete:**

- [ ] Zero auto-fixable violations (MD032, MD022, MD031, MD009)
- [ ] Auto-fix commit created and reviewed

**Phase 4 Complete:**

- [ ] Zero MD040 violations (language specifiers added)
- [ ] Zero MD036 violations (emphasis/heading fixed)
- [ ] Zero MD024 violations (duplicate headings resolved)

**Phase 5 Complete:**

- [ ] All markdown files pass linting (0 errors)
- [ ] Pre-commit hooks tested and working
- [ ] Markdown quality tests added and passing

**Phase 6 Complete:**

- [ ] Documentation standards updated
- [ ] Quality checklist created
- [ ] Prevention mechanisms documented

---

## References

- [markdownlint Rules](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md)
- [CommonMark Spec](https://spec.commonmark.org/)
- [GitHub Flavored Markdown](https://github.github.com/gfm/)
- [MD040 Documentation](https://github.com/DavidAnson/markdownlint/blob/main/doc/md040.md)
- [Pre-commit Best Practices 2025](https://gatlenculp.medium.com/effortless-code-quality-the-ultimate-pre-commit-hooks-guide-for-2025-57ca501d9835)

---

## Appendix: Error Count Discrepancy

**Investigation needed:** Why does markdownlint-cli2 report 4,188 errors while markdownlint-cli reports only 75?

**Hypotheses:**

1. Different default configurations
2. Different rule sets enabled
3. JSON output formatter counting differently
4. Include/exclude patterns differ
5. Docker version behaves differently

**Action:** Test with both tools on same file set to identify root cause.
