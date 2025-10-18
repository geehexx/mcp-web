---
created: "2025-10-17"
updated: "2025-10-18"
description: Extract structured information from current session
auto_execution_mode: 3
category: Analysis
complexity: 55
tokens: 1196
dependencies: []
status: active
---

# Extract Session Workflow

**Purpose:** Extract structured information from current work session using git history and file system state.

**Invocation:** Called by `/meta-analysis` (not standalone)

**Output:** Structured data for session summary generation

---

## Stage 1: Identify Session Scope

### Determine Boundaries

```bash
# Get last meta-analysis timestamp
LAST_RUN=$(cat .windsurf/.last-meta-analysis 2>/dev/null || echo "24 hours ago")

# Get commits since last run
git log --oneline --since="$LAST_RUN"

# Count duration (approximate from git)
FIRST_COMMIT=$(git log --reverse --since="$LAST_RUN" --format="%ct" | head -1)
LAST_COMMIT=$(git log --since="$LAST_RUN" --format="%ct" | head -1)
DURATION=$(( ($LAST_COMMIT - $FIRST_COMMIT) / 3600 )) # hours
```

### Identify Primary Focus

**Extract from commit messages:**

```bash
# Most common commit type
git log --since="$LAST_RUN" --format="%s" | grep -oE "^[a-z]+\(" | sort | uniq -c | sort -rn | head -1

# Common scope
git log --since="$LAST_RUN" --format="%s" | grep -oE "\([^)]+\)" | sort | uniq -c | sort -rn | head -1
```

**Focus areas:**

- `feat:` → Implementation
- `fix:` → Bug fixing
- `docs:` → Documentation
- `test:` → Testing
- `refactor:` → Refactoring
- `security:` → Security
- Multiple types → Mixed session

---

## Stage 2: Extract Accomplishments

### Get Changed Files

```bash
# Files modified since last run
git diff --name-status "$LAST_RUN"..HEAD

# Group by type (added, modified, deleted)
git diff --name-status "$LAST_RUN"..HEAD | awk '{print $1}' | sort | uniq -c
```

### Extract from Commit Messages

**For each commit:**

```bash
git log --since="$LAST_RUN" --format="%h|%s|%b" | while IFS='|' read hash subject body; do
  # Parse conventional commit
  TYPE=$(echo "$subject" | grep -oE "^[a-z]+")
  SCOPE=$(echo "$subject" | grep -oE "\([^)]+\)" | tr -d '()')
  DESC=$(echo "$subject" | sed 's/^[a-z]*([^)]*): //')

  echo "- **$TYPE**: $DESC ($SCOPE)"
done
```

**Format:** Action verb + what + where + context

---

## Stage 3: Extract Technical Decisions

### Search for Decision Keywords

```bash
# Search commit bodies for decision markers
git log --since="$LAST_RUN" --format="%B" | grep -iE "decided|chose|selected|using.*because"

# Search ADRs created
git log --since="$LAST_RUN" --name-only --diff-filter=A | grep "docs/adr/"
```

**Decision pattern:**

- What was decided
- Why (rationale)
- What alternatives were considered
- Expected impact

**If no decisions:** Write "None - Implementation session"

---

## Stage 4: Extract Learnings

### Search for Measurement Keywords

```bash
# Search for performance measurements
git log --since="$LAST_RUN" --format="%B" | grep -iE "[0-9]+x|speedup|faster|slower|[0-9]+%|seconds|ms"

# Search for insights in commit bodies
git log --since="$LAST_RUN" --format="%B" | grep -iE "discovered|learned|found that|turns out"
```

**Learning pattern:**

- Technology/pattern name
- Specific insight
- Measurement (if applicable)
- Applicability (when to use)

---

## Stage 5: Identify Patterns

### Positive Patterns

**From commits:**

```bash
# Look for repeated successful approaches
git log --since="$LAST_RUN" --format="%B" | grep -iE "worked well|effective|successful"

# Common test patterns
grep -r "pytest.mark" tests/ | cut -d: -f2 | sort | uniq -c | sort -rn
```

**Examples:**

- Batch file operations used → 3x faster
- Test-first approach → Caught N regressions
- Git hooks → Prevented N issues

### Negative Patterns

**From commit history:**

```bash
# Look for fixes, reverts, or corrections
git log --since="$LAST_RUN" --format="%s" | grep -iE "fix:|revert|correct"

# Check for auto-fix commits (sign of not running formatters)
git log --since="$LAST_RUN" --format="%s" | grep -iE "style.*auto-fix"
```

**Pattern:**

- What didn't work
- Why it failed
- Better alternative

---

## Stage 6: Extract Metrics

### Test Metrics

```bash
# Test counts (if pytest used)
pytest --collect-only 2>/dev/null | grep "test session starts" -A 5

# Test duration (if available)
cat .pytest_cache/v/cache/stepwise 2>/dev/null
```

### Coverage Metrics

```bash
# Get coverage percentage (if available)
coverage report --format=total 2>/dev/null
```

### File Counts

```bash
# Count files modified
git diff --name-only "$LAST_RUN"..HEAD | wc -l

# Count commits
git log --oneline --since="$LAST_RUN" | wc -l
```

---

## Stage 7: Protocol Compliance Check

### Check Session End Protocol

**Verify:**

```bash
# All changes committed?
git status --porcelain | wc -l

# Meta-analysis run?
[ -f .windsurf/.last-meta-analysis ] && echo "✓" || echo "✗"

# Session summary exists?
ls -t docs/archive/session-summaries/*.md 2>/dev/null | head -1

# Completed initiatives archived?
grep -l "Status.*Completed" docs/initiatives/active/*.md 2>/dev/null
```

**Flag violations:**

- Uncommitted changes at session end
- Meta-analysis timestamp missing/stale
- Session summary in wrong location
- Completed initiatives not archived

---

## Output Format

**Structured extraction result:**

```yaml
session:
  date: "YYYY-MM-DD"
  duration_hours: N
  primary_focus: "[focus area]"
  workflows_used: ["workflow1", "workflow2"]

commits:
  count: N
  messages:
    - hash: "abc123"
      type: "feat"
      scope: "workflows"
      description: "add sub-workflow primitives"

accomplishments:
  - action: "Created"
    what: "5 new sub-workflow files"
    where: ".windsurf/workflows/"
    context: "Phase 1 foundation"

decisions:
  - topic: "Versioning tool"
    decision: "Use custom /bump-version workflow"
    rationale: "Zero dependencies, full control"
    impact: "AI-friendly automation"

learnings:
  - technology: "MCP batch reads"
    insight: "3x faster than sequential"
    measurement: "1 tool call vs 3+"
    applicability: "Always for 3+ files"

positive_patterns:
  - name: "Batch file operations"
    description: "Using mcp0_read_multiple_files"
    why_worked: "Reduces tool call overhead"
    frequency: "Always"

negative_patterns:
  - name: "Skipping formatters before commit"
    description: "Committing without task format"
    why_failed: "Caused pre-commit failures"
    alternative: "Run task format first"

metrics:
  files_modified: N
  lines_added: N
  lines_removed: N
  tests_added: N
  coverage_percent: N

protocol_compliance:
  violations:
    - "Meta-analysis timestamp missing"
  recommendations:
    - "Update .windsurf/.last-meta-analysis"
```

---

## Integration

### Called By

- `/meta-analysis` - Primary caller

### Calls

- Git commands - History analysis
- File system scans - Context gathering

---

## References

- `.windsurf/workflows/meta-analysis.md` - Parent workflow
- `.windsurf/rules/00_agent_directives.md` - Session End Protocol
