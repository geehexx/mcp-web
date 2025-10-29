---
pass_through: true
description: Extract structured session information from git and filesystem
title: Extract Session Workflow
tags: ['session', 'extraction', 'analysis', 'git']
---

# Extract Session Workflow

Extract structured data from current session (git history, files, tests) for session summary generation.

**Called by:** `/meta-analysis`

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
git diff --name-only HEAD~10..HEAD

# Added files
git diff --name-only --diff-filter=A HEAD~10..HEAD

# Deleted files
git diff --name-only --diff-filter=D HEAD~10..HEAD
```

### 4. Extract Test Results

```bash
# Run tests and capture results
task test:fast 2>&1 | tee /tmp/test_results.txt

# Extract test summary
grep -E "(PASSED|FAILED|ERROR)" /tmp/test_results.txt | wc -l
```

### 5. Extract Workflow Usage

```bash
# Count workflow invocations
grep -r "Entering /" .windsurf/logs/ 2>/dev/null | wc -l

# Most used workflows
grep -r "Entering /" .windsurf/logs/ 2>/dev/null | \
  grep -oP "Entering /\w+" | sort | uniq -c | sort -nr
```

## Stage 1: Session Metadata

### 1.1 Time Range

**Determine session duration:**
- Start time: Last meta-analysis or session start
- End time: Current timestamp
- Duration: End time - Start time

### 1.2 Session Context

**Identify session context:**
- Active initiatives
- Current phase
- Work focus
- Environment

## Stage 2: Git Analysis

### 2.1 Commit Analysis

**Extract commit information:**
- Commit hash
- Author
- Date
- Message type
- Scope
- Description

### 2.2 File Changes

**Analyze file modifications:**
- Modified files
- Added files
- Deleted files
- File types
- Change patterns

### 2.3 Branch Analysis

**Check branch information:**
- Current branch
- Branch changes
- Merge commits
- Rebase operations

## Stage 3: Test Analysis

### 3.1 Test Execution

**Run tests and capture results:**
- Test suite execution
- Pass/fail counts
- Error details
- Coverage information

### 3.2 Test Changes

**Analyze test modifications:**
- New tests added
- Tests modified
- Tests removed
- Test coverage changes

## Stage 4: Workflow Analysis

### 4.1 Workflow Usage

**Track workflow invocations:**
- Workflows used
- Usage frequency
- Execution time
- Success/failure rates

### 4.2 Workflow Patterns

**Identify usage patterns:**
- Common workflow sequences
- Workflow dependencies
- Execution efficiency
- Error patterns

## Stage 5: File System Analysis

### 5.1 File Modifications

**Track file changes:**
- Files created
- Files modified
- Files deleted
- File size changes

### 5.2 Directory Changes

**Monitor directory structure:**
- New directories
- Directory modifications
- File organization
- Structure changes

## Stage 6: Generate Session Data

### 6.1 Structured Output

**Create session data structure:**
```json
{
  "session": {
    "start_time": "2025-10-22T10:00:00Z",
    "end_time": "2025-10-22T12:00:00Z",
    "duration": "2h",
    "context": "initiative-migration"
  },
  "commits": [
    {
      "hash": "abc123",
      "type": "feat",
      "scope": "workflows",
      "description": "add new workflow"
    }
  ],
  "files": {
    "modified": ["file1.py", "file2.md"],
    "added": ["file3.py"],
    "deleted": ["file4.py"]
  },
  "tests": {
    "total": 100,
    "passed": 95,
    "failed": 5,
    "coverage": 90
  },
  "workflows": {
    "used": ["work", "implement", "commit"],
    "count": 15
  }
}
```

### 6.2 Export Data

**Save session data:**
- JSON format for processing
- Markdown format for readability
- CSV format for analysis

## Context Loading

Load these rules if you determine you need them based on their descriptions:

- **Context Optimization**: `/rules/07_context_optimization.mdc` - Apply when dealing with large files or complex operations
- **Task Orchestration**: `/rules/12_task_orchestration.mdc` - Apply when managing complex task coordination

## Workflow References

When this extract-session workflow is called:

1. **Load**: `/commands/extract-session.md`
2. **Execute**: Follow the extraction stages defined above
3. **Analyze**: Extract session data from various sources
4. **Structure**: Create organized session data
5. **Export**: Save data in multiple formats

## Anti-Patterns

❌ **Don't:**
- Skip git analysis
- Ignore test results
- Skip workflow tracking
- Create incomplete data

✅ **Do:**
- Analyze all git data
- Capture test results
- Track workflow usage
- Create complete data

## Success Metrics

| Metric | Target | Status |
|--------|--------|--------|
| Data completeness | 100% | ✅ |
| Analysis accuracy | 95%+ | ✅ |
| Export success | 100% | ✅ |
| Processing time | <30s | ✅ |

## Integration

**Called By:**
- `/meta-analysis` - Session analysis workflow
- User - Direct invocation for session extraction

**Calls:**
- Git operations
- Test execution
- File system analysis

**Exit:**

```markdown
✅ **Completed /extract-session:** Session extraction finished
```

## Command Metadata

**File:** `extract-session.yaml`
**Type:** Command/Workflow
**Complexity:** Moderate
**Estimated Tokens:** ~1,200
**Last Updated:** 2025-10-22
**Status:** Active

**Topics Covered:**
- Session extraction
- Git analysis
- Test analysis
- Workflow tracking

**Dependencies:**
- None (standalone workflow)
