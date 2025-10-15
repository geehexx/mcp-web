# Session Summary Standards

**Purpose:** Standardize AI agent session summary creation, naming, and placement.
**Scope:** All significant AI agent work sessions (2+ hours or major changes).
**Last Updated:** October 15, 2025

---

## When to Create

Create a session summary when:

- ✅ **Session duration ≥ 2 hours** of active work
- ✅ **Major changes:** 10+ files modified or significant refactoring
- ✅ **New features:** Complete feature implementation
- ✅ **Infrastructure changes:** Build system, CI/CD, tooling updates
- ✅ **Documentation overhaul:** Major docs restructuring or additions
- ✅ **Initiative completion:** Finishing a tracked initiative

Do NOT create for:

- ❌ Minor bug fixes (< 5 files)
- ❌ Simple documentation updates
- ❌ Routine dependency updates
- ❌ Quick experiments or WIP sessions

---

## Naming Convention

### Format

```
YYYY-MM-DD-descriptive-kebab-case-name.md
```

### Components

1. **Date:** `YYYY-MM-DD` format (ISO 8601)
2. **Description:** 2-5 words, kebab-case, descriptive

### Examples

**Good:**
- `2025-10-15-comprehensive-overhaul-v3.md`
- `2024-12-20-security-testing-implementation.md`
- `2025-01-15-migration-to-uv-package-manager.md`

**Bad:**
- `session.md` (not descriptive, no date)
- `2025-10-15.md` (no description)
- `big-refactor.md` (no date)
- `2025_10_15_session_summary.md` (wrong format)

---

## File Location

All session summaries go in:

```
docs/archive/session-summaries/
```

**DO NOT** place in:
- Root directory
- `docs/` directly
- `.windsurf/` directory
- Version control root

---

## Content Structure

### Required Sections

```markdown
# Session Summary: [Descriptive Title]

**Date:** YYYY-MM-DD, HH:MM [Timezone]
**Duration:** Approximately X hours
**Agent:** [Agent name/version if relevant]
**Status:** [Complete/Partial/Checkpoint]

---

## Executive Summary

[2-3 sentence high-level overview of what was accomplished]

---

## Objectives

[What the session aimed to accomplish]

- Objective 1
- Objective 2
- Objective 3

---

## What Was Accomplished

### 1. [Category 1]

[Description of changes]

**Files Changed:**
- `path/to/file1.py`
- `path/to/file2.md`

**Key Changes:**
- Specific change 1
- Specific change 2

### 2. [Category 2]

[Continue for each major category of work]

---

## Git Commits

List significant commits with brief explanations:

```
abc1234 feat(module): add new feature
def5678 fix(security): resolve vulnerability
ghi9012 docs: update documentation
```

Total commits: X

---

## Known Issues

### Resolved
- [Issue that was fixed during session]

### Unresolved
- [Issue identified but not yet fixed]
- [Technical debt noted]

---

## Next Steps

**CRITICAL:** This section enables cross-session context detection.

For the next agent or session:

1. [Specific actionable item 1] - **Include file paths and test names**
2. [Specific actionable item 2] - **Include specific commands to run**
3. [Specific actionable item 3] - **Link to related initiatives/ADRs**

**Format requirements for AI agent context detection:**
- ✅ **Be explicit:** "Fix 4 failing tests in tests/unit/test_security.py"
- ✅ **Include paths:** "Continue ADR conversion in docs/adr/"
- ✅ **Reference initiatives:** "Resume docs/initiatives/active/quality-foundation.md Phase 2"
- ❌ **Avoid vague:** "Continue the work" or "Fix remaining issues"

**Priority indicators:**
- 🔴 **Critical:** Blocks all other work
- 🟡 **High:** Should do next session
- 🟢 **Medium:** Do when convenient
- ⚪ **Low:** Nice to have

---

## Key Decisions

[Important decisions made during the session]

- **Decision 1:** [What was decided and why]
- **Decision 2:** [What was decided and why]

---

## Resources Created/Updated

**Documentation:**
- New: [list new docs]
- Updated: [list updated docs]

**Workflows:**
- New: [list new workflows]
- Updated: [list updated workflows]

**Tests:**
- Added: X tests
- Fixed: Y tests
- Coverage: Z%

---

## Metrics

- **Files Modified:** X
- **Lines Added:** +Y
- **Lines Deleted:** -Z
- **Test Coverage:** N% → M%
- **Linting Issues:** Before: N, After: M

---

## References

- [Link to related ADR if applicable]
- [Link to related initiative if applicable]
- [External references consulted]

---

**Created by:** [Agent/User]
**Reviewed by:** [If applicable]
```

### Optional Sections

Include if relevant:

- **Performance Improvements:** Benchmark comparisons
- **Breaking Changes:** What users need to know
- **Migration Guide:** If breaking changes exist
- **Lessons Learned:** Insights for future work
- **Tool/Dependency Changes:** Major additions/removals

---

## Content Guidelines

### Executive Summary

**Purpose:** Allow quick understanding without reading full document

**Length:** 2-3 sentences, maximum 100 words

**Example:**
```markdown
## Executive Summary

Completed comprehensive modernization of mcp-web testing infrastructure.
Migrated to parallel testing by default (7.5x faster), established
pre-commit hooks, restructured documentation with AI-friendly standards,
and resolved all auto-fixable code quality issues.
```

### What Was Accomplished

**Group by category:**
- Code changes (by module/feature)
- Testing improvements
- Documentation updates
- Infrastructure changes
- Tooling updates

**Be specific:**
- ✅ "Added 15 unit tests for security module, achieving 95% coverage"
- ❌ "Improved tests"

### Known Issues

**Categorize:**
1. **Resolved** - Fixed during session
2. **Unresolved** - Identified but deferred

**Format:**
```markdown
### Unresolved

- **Issue:** Brief description
  - **Impact:** How it affects system
  - **Workaround:** Temporary solution (if any)
  - **Tracked:** Link to issue/initiative
```

### Next Steps

**Be actionable and AI-parseable:**
- ✅ "Fix 4 remaining async test timeouts in `tests/unit/test_security.py`"
- ✅ "Continue initiative: docs/initiatives/active/quality-foundation.md Phase 2"
- ✅ "Create ADR-0007 through ADR-0012 per docs/initiatives/active/convert-decisions-to-adrs.md"
- ❌ "Fix tests" (which tests? where?)
- ❌ "Continue work" (what work? what context?)

**Prioritize with clear indicators:**
1. 🔴 **Critical** (blocks progress) - "MUST fix before any other work"
2. 🟡 **High** (should do soon) - "Next session priority"
3. 🟢 **Medium** (do when convenient) - "When time permits"
4. ⚪ **Low** (nice-to-have) - "Future enhancement"

**Cross-session context requirements:**
- Include enough context that a new AI agent can pick up work
- No assumptions about prior conversation history
- File paths, test names, command examples
- Links to related documentation

---

## Style Guidelines

### Language

- **Use past tense** for accomplished work
- **Use imperative mood** for next steps
- **Be specific** with numbers and metrics
- **Link liberally** to related docs and code

### Formatting

- Use **bold** for emphasis
- Use `code` for file names, commands, technical terms
- Use lists for clarity
- Use tables for comparisons or metrics
- Use headings to organize hierarchically

### Examples

**Good:**
```markdown
### Testing Infrastructure

Implemented parallel testing as default across all test commands.

**Changes:**
- Updated `Taskfile.yml`: Added `-n {{.PARALLEL_WORKERS}}` to test commands
- Modified `pytest.ini`: Excluded benchmarks from parallel runs
- Created `test-before-commit.md` workflow for AI testing guidance

**Impact:**
- Test execution time: 60s → 8s (7.5x faster)
- CI pipeline duration: 10min → 3min
- Developer feedback loop significantly improved
```

**Bad:**
```markdown
### Testing

Made tests faster by using parallel execution. Updated some files.
```

---

## Archival Process

### When to Archive

Archive summaries immediately after creation. Do not leave them in root or `docs/` directly.

### Steps

```bash
1. Create summary: docs/archive/session-summaries/2025-10-15-description.md
2. Commit with appropriate message:
   git add docs/archive/session-summaries/
   git commit -m "docs: add session summary for [description]"
```

### Index Maintenance

Keep an index if many summaries accumulate:

```markdown
# Session Summaries Index

## 2025

### October
- [2025-10-15: Comprehensive Overhaul v3](./2025-10-15-comprehensive-overhaul-v3.md)

### September
- [2025-09-20: Security Implementation](./2025-09-20-security-implementation.md)
```

---

## Validation Checklist

Before committing a session summary:

- [ ] **Naming:** Follows `YYYY-MM-DD-description.md` format
- [ ] **Location:** In `docs/archive/session-summaries/`
- [ ] **Required sections:** All present and filled
- [ ] **Specificity:** Concrete details, not vague descriptions
- [ ] **Links:** All internal links valid
- [ ] **Metrics:** Quantitative data where applicable
- [ ] **Next steps:** Clear, actionable items listed
- [ ] **Grammar:** Proofread for clarity
- [ ] **Markdown:** Passes linting (`task lint:markdown`)

---

## Anti-Patterns

### ❌ Vague Descriptions

**Bad:**
```markdown
## What Was Accomplished

Made some improvements to the code. Fixed bugs and updated docs.
```

**Good:**
```markdown
## What Was Accomplished

### Security Module Enhancements

- Fixed 6 test failures in `tests/unit/test_security.py`
- Added IPv6 localhost validation
- Updated API key regex to support `sk-proj-` prefix
- Improved input sanitization logic with character variety check
```

### ❌ Missing Context

**Bad:**
```markdown
Fixed the tests that were broken.
```

**Good:**
```markdown
Fixed 6 security tests that were failing due to implementation changes:
- `test_no_false_positives`: Exclude exact matches from typoglycemia detection
- `test_sanitize_input`: Apply character variety check before repetition reduction
- `test_detect_api_key_exposure`: Add support for sk-proj- prefixed OpenAI keys
```

### ❌ No Actionable Next Steps

**Bad:**
```markdown
## Next Steps

Continue improving the project.
```

**Good:**
```markdown
## Next Steps

1. **High Priority:** Fix 4 async test timeouts in ConsumptionLimits and RateLimiter tests
2. **Medium Priority:** Resolve 95 mypy type errors (focus on mcp_server.py)
3. **Low Priority:** Create ADRs for extraction strategy and chunking algorithm
```

---

## Examples

### Minimal Example

```markdown
# Session Summary: Quick Bug Fixes

**Date:** 2025-10-15, 14:30 UTC+07
**Duration:** 1 hour
**Status:** Complete

---

## Executive Summary

Fixed 3 critical bugs in cache module affecting production deployments.

---

## Objectives

- Fix cache key generation for special characters
- Resolve Redis connection timeout
- Update cache eviction policy

---

## What Was Accomplished

### Bug Fixes

1. **Cache Key Sanitization**
   - Fixed URL encoding in cache keys
   - Added tests for special characters
   - File: `src/mcp_web/cache.py`

2. **Redis Timeout**
   - Increased connection timeout to 5s
   - Added retry logic
   - File: `src/mcp_web/config.py`

3. **Eviction Policy**
   - Changed from LRU to LFU
   - Updated configuration defaults
   - File: `src/mcp_web/cache.py`

---

## Git Commits

```
a1b2c3d fix(cache): sanitize URLs in cache keys
e4f5g6h fix(cache): increase Redis connection timeout
i7j8k9l refactor(cache): change eviction policy to LFU
```

---

## Next Steps

1. Monitor cache hit rate in production
2. Consider adding cache warming on startup

---

## Metrics

- **Files Modified:** 3
- **Tests Added:** 5
- **Bugs Fixed:** 3
```

### Comprehensive Example

See: `docs/archive/session-summaries/2024-10-15-comprehensive-overhaul-v3.md`

---

## Tools

### Template Generator (Future)

```bash
# Not yet implemented
# task summary:new --title "Description" --date 2025-10-15
```

### Summary Validator (Future)

```bash
# Not yet implemented
# task summary:validate docs/archive/session-summaries/2025-10-15-description.md
```

---

## References

- [Documentation Standards](./DOCUMENTATION_STANDARDS.md)
- [Commit Style Guide](./COMMIT_STYLE_GUIDE.md)
- [Google Technical Writing](https://developers.google.com/tech-writing)
- [Diátaxis Documentation System](https://diataxis.fr/)

---

**Version:** 1.0
**Maintained By:** mcp-web core team
