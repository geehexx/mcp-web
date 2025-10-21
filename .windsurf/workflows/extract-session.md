---
created: "2025-10-17"
updated: "2025-10-21"
description: Extract structured session information from git and filesystem
auto_execution_mode: 3
category: Analysis
complexity: 65
tokens: 1200
dependencies: []
status: active
version: "2.0-intelligent-semantic-preservation"
---

# Extract Session Workflow

Extract structured data from current session (git history, files, tests) for session summary generation.

**Called by:** `/meta-analysis`

---

## Process

### 1. Get Session Metadata

```bash
# Timestamp
LAST_RUN=$(cat .windsurf/.last-meta-analysis 2>/dev/null || echo "1 week ago")

# Date range
git log --since="$LAST_RUN" --format="%ai" | head -1
git log --since="$LAST_RUN" --format="%ai" | tail -1
```

### 2. Extract Commits

```bash
git log --since="$LAST_RUN" --format="%h|%an|%ai|%s" | \
  while IFS='|' read hash author date msg; do
    type=$(echo "$msg" | grep -oP '^[a-z]+' | head -1)
    scope=$(echo "$msg" | grep -oP '\([^)]+\)' | tr -d '()')
    desc=$(echo "$msg" | sed 's/^[a-z]*(\([^)]*\)): *//')
    echo "$hash|$type|$scope|$desc"
  done
```

### 3. Identify File Changes

```bash
# Modified files
git diff --name-only "$LAST_RUN"..HEAD

# By category
git diff --name-status "$LAST_RUN"..HEAD | \
  awk '{print $2}' | \
  sed 's|^.windsurf/workflows/|workflows:|; s|^.windsurf/rules/|rules:|; \
       s|^tests/|tests:|; s|^src/|src:|; s|^docs/|docs:|' | \
  cut -d: -f1 | sort | uniq -c
```

### 4. Extract Accomplishments

```bash
# Feature additions
git log --since="$LAST_RUN" --format="%s" | grep -E "^feat"

# Files created
git log --since="$LAST_RUN" --name-status --diff-filter=A --format="" | \
  awk '{print $2}' | sort | uniq
```

### 5. Extract Decisions

```bash
# ADRs created
git log --since="$LAST_RUN" --name-status --format="%s" | \
  grep "docs(adr):" || echo "No ADRs"

# Config changes
git diff "$LAST_RUN"..HEAD -- '*.toml' '*.yml' '*.json' --name-only
```

### 6. Search for Learnings

```bash
# Performance
git log --since="$LAST_RUN" --format="%B" | \
  grep -iE "[0-9]+x|speedup|faster|[0-9]+%|ms"

# Insights
git log --since="$LAST_RUN" --format="%B" | \
  grep -iE "discovered|learned|found that"
```

### 7. Identify Patterns

```bash
# Positive
git log --since="$LAST_RUN" --format="%B" | \
  grep -iE "worked well|effective|successful"

# Negative
git log --since="$LAST_RUN" --format="%s" | \
  grep -iE "fix:|revert|correct"
```

### 8. Extract Metrics

```bash
# Tests
pytest --collect-only 2>/dev/null | grep "collected"

# Files/commits
git diff --name-only "$LAST_RUN"..HEAD | wc -l
git log --oneline --since="$LAST_RUN" | wc -l
```

### 9. Protocol Compliance

```bash
# Uncommitted?
git status --porcelain | wc -l

# Meta-analysis timestamp?
[ -f .windsurf/.last-meta-analysis ] && echo "✓" || echo "✗"

# Completed initiatives archived?
grep -l "Status.*Completed" docs/initiatives/active/*.md 2>/dev/null
```

---

## Output Format

```yaml
session:
  date: "YYYY-MM-DD"
  duration_hours: N
  primary_focus: "[focus]"
  workflows_used: ["workflow1"]

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
    rationale: "Zero deps"
    impact: "Automation"

learnings:
  - technology: "MCP batch reads"
    insight: "3x faster"
    measurement: "1 vs 3+ calls"

positive_patterns:
  - name: "Batch operations"
    why_worked: "Reduced overhead"

negative_patterns:
  - name: "Skipped formatters"
    why_failed: "Pre-commit fails"
    alternative: "Run task format first"

metrics:
  files_modified: N
  commits: N
  tests_added: N

protocol_compliance:
  violations: ["Missing timestamp"]
  recommendations: ["Update .last-meta-analysis"]
```

---

## References

- `meta-analysis.md`, `10_session_protocols.md`
