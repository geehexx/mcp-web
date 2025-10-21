---
created: "2025-10-17"
updated: "2025-10-21"
description: Extract structured information from current session
auto_execution_mode: 3
category: Analysis
complexity: 55
tokens: 1700
dependencies: []
status: active
---

# Extract Session Workflow

**Purpose:** Extract structured data from git history and session context for summary generation.

**Invocation:** Called by `/meta-analysis` (subtask)

**Philosophy:** Automated data extraction enables consistent, comprehensive session summaries.

---

## Stage 1: Create Task Plan

**Note:** Parent workflow (`/meta-analysis`) handles task tracking. If called directly:

```typescript
update_plan({
  explanation: "🔍 Starting /extract-session workflow",
  plan: [
    { step: "1. /extract-session - Identify session scope", status: "in_progress" },
    { step: "2. /extract-session - Extract accomplishments and decisions", status: "pending" },
    { step: "3. /extract-session - Identify patterns and metrics", status: "pending" },
    { step: "4. /extract-session - Check protocol compliance", status: "pending" }
  ]
})
```

---

## Stage 2: Identify Session Scope

### Determine Boundaries

```bash
# Get last meta-analysis timestamp
LAST_RUN=$(cat .windsurf/.last-meta-analysis 2>/dev/null || echo "24 hours ago")

# Get commits since last run
git log --oneline --since="$LAST_RUN"

# Calculate duration
FIRST=$(git log --reverse --since="$LAST_RUN" --format="%ct" | head -1)
LAST=$(git log --since="$LAST_RUN" --format="%ct" | head -1)
DURATION=$(( ($LAST - $FIRST) / 3600 ))  # hours
```

### Identify Primary Focus

```bash
# Most common commit type
git log --since="$LAST_RUN" --format="%s" | \
  grep -oE "^[a-z]+\(" | sort | uniq -c | sort -rn | head -1

# Common scope
git log --since="$LAST_RUN" --format="%s" | \
  grep -oE "\([^)]+\)" | sort | uniq -c | sort -rn | head -1
```

**Focus mapping:**

- `feat:` → Implementation
- `fix:` → Bug fixing
- `docs:` → Documentation
- `refactor:` → Refactoring
- Multiple → Mixed session

---

## Stage 3: Extract Accomplishments

### Get Changed Files

```bash
# Files modified
git diff --name-status "$LAST_RUN"..HEAD

# Group by type (A/M/D)
git diff --name-status "$LAST_RUN"..HEAD | awk '{print $1}' | sort | uniq -c
```

### Parse Commits

```bash
git log --since="$LAST_RUN" --format="%h|%s|%b" | \
while IFS='|' read hash subject body; do
  TYPE=$(echo "$subject" | grep -oE "^[a-z]+")
  SCOPE=$(echo "$subject" | grep -oE "\([^)]+\)" | tr -d '()')
  DESC=$(echo "$subject" | sed 's/^[a-z]*([^)]*): //')
  echo "- **$TYPE**: $DESC ($SCOPE)"
done
```

**Format:** Action verb + what + where + context

---

## Stage 4: Extract Decisions & Learnings

### Search for Decisions

```bash
# Decision markers in commit bodies
git log --since="$LAST_RUN" --format="%B" | \
  grep -iE "decided|chose|selected|using.*because"

# ADRs created
git log --since="$LAST_RUN" --name-only --diff-filter=A | grep "docs/adr/"
```

**Decision pattern:**

- What was decided
- Why (rationale)
- Alternatives considered
- Expected impact

### Search for Learnings

```bash
# Performance measurements
git log --since="$LAST_RUN" --format="%B" | \
  grep -iE "[0-9]+x|speedup|faster|[0-9]+%|ms"

# Insights
git log --since="$LAST_RUN" --format="%B" | \
  grep -iE "discovered|learned|found that"
```

**Learning pattern:**

- Technology/pattern
- Specific insight
- Measurement (if any)
- Applicability

---

## Stage 5: Identify Patterns

### Positive Patterns

```bash
# Successful approaches
git log --since="$LAST_RUN" --format="%B" | \
  grep -iE "worked well|effective|successful"

# Test patterns
grep -r "pytest.mark" tests/ | cut -d: -f2 | sort | uniq -c | sort -rn
```

**Examples:**

- Batch operations → 3x faster
- Test-first → Caught N regressions
- Git hooks → Prevented N issues

### Negative Patterns

```bash
# Fixes, reverts, corrections
git log --since="$LAST_RUN" --format="%s" | grep -iE "fix:|revert|correct"

# Auto-fix commits (sign of skipped formatters)
git log --since="$LAST_RUN" --format="%s" | grep -iE "style.*auto-fix"
```

**Pattern:**

- What didn't work
- Why it failed
- Better alternative

---

## Stage 6: Extract Metrics

### Test & Coverage Metrics

```bash
# Test counts
pytest --collect-only 2>/dev/null | grep "collected"

# Coverage
coverage report --format=total 2>/dev/null
```

### File Counts

```bash
# Files modified
git diff --name-only "$LAST_RUN"..HEAD | wc -l

# Commits
git log --oneline --since="$LAST_RUN" | wc -l
```

---

## Stage 7: Protocol Compliance Check

### Verify Session End Protocol

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

- Uncommitted changes
- Missing meta-analysis timestamp
- Missing session summary
- Unarchived completed initiatives

---

## Output Format

```yaml
session:
  date: "YYYY-MM-DD"
  duration_hours: N
  primary_focus: "[focus]"
  workflows_used: ["workflow1", "workflow2"]

commits:
  count: N
  messages:
    - hash: "abc123"
      type: "feat"
      scope: "workflows"
      description: "add sub-workflow"

accomplishments:
  - action: "Created"
    what: "5 new workflows"
    where: ".windsurf/workflows/"
    context: "Phase 1"

decisions:
  - topic: "Versioning"
    decision: "Custom workflow"
    rationale: "Zero deps, AI-friendly"
    impact: "Automation"

learnings:
  - technology: "MCP batch reads"
    insight: "3x faster"
    measurement: "1 vs 3+ calls"
    applicability: "Always for 3+ files"

positive_patterns:
  - name: "Batch operations"
    why_worked: "Reduced overhead"
    frequency: "Always"

negative_patterns:
  - name: "Skipped formatters"
    why_failed: "Pre-commit fails"
    alternative: "Run task format first"

metrics:
  files_modified: N
  lines_added: N
  tests_added: N
  coverage_percent: N

protocol_compliance:
  violations: ["Missing timestamp"]
  recommendations: ["Update .last-meta-analysis"]
```

---

## Integration

**Called By:** `/meta-analysis` - Primary caller

**Calls:** Git commands, file system scans

**Print exit:**

```markdown
✅ **Completed /extract-session:** Session data extracted and structured
```

---

## References

- `.windsurf/workflows/meta-analysis.md` - Parent workflow
- `.windsurf/rules/10_session_protocols.md` - Session End Protocol
