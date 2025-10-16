# Quick Start: New Workflow System

**TL;DR:** Use `/work` for everything. The agent figures out what to do.

---

## The New Way

### Starting Any Work

```text
You: /work
```

**Agent will:**

1. Scan project in <30 seconds
2. Find active initiatives, test failures, or TODOs
3. Auto-route to appropriate workflow
4. Start working immediately

**70%+ of the time:** No questions asked, just starts working.

---

## Key Workflows

### `/work` - Central Command

**Use it for:** Everything

**It auto-detects:**

- Active initiatives → continues them
- Test failures → fixes them
- Planning markers → creates plans
- Clean state → asks what to do

**Example:**

```text
You: /work

Agent: Detected initiative "Fix Security Tests" (3/10 complete)
 Loading context... Starting next task...
```

### `/plan` - When You Need a Plan

**Use it when:**

- New complex feature
- Multi-session work
- Unclear requirements

**Creates:**

- Research-backed plan
- Broken into phases
- Success criteria defined
- Initiative document

**Example:**

```text
You: /plan add user authentication

Agent: Researching best practices...
 Creating comprehensive plan...
 Phases: 4 (Core → Mgmt → Apply → Docs)
 Estimated: 8 hours
 Ready to implement?
```

### `/implement` - Focused Execution

**Rarely invoked directly** (usually called by `/work`)

**Does:**

- Test-first development
- Incremental commits
- Quality gates
- Progress tracking

---

## Common Scenarios

### Continue Previous Work

```text
You: /work
Agent: [scans files, finds initiative, continues]
```

### Start New Feature

```text
You: /work add API rate limiting
Agent: [detects planning needed, calls /plan, then /implement]
```

### Fix Bugs

```text
You: /work
Agent: [runs tests, finds failures, starts fixing]
```

### Just Commit Changes

```text
You: /commit
Agent: [reviews diff, guides commit message]
```

---

## What Changed?

### Before

- Manual context explanation every time
- Many clarifying questions
- Ad-hoc process

### After

- Auto-detects context from files
- Minimal questions (only if ambiguous)
- Structured workflows

---

## Pro Tips

### 1. Trust the Agent

If it says "Detected X, starting Y" → let it work

### 2. Initiatives Are King

Active initiatives in `docs/initiatives/active/` are the primary context source

### 3. Batch Everything

The agent uses batch file reads for speed. You benefit automatically.

### 4. Test-First Always

New workflows enforce TDD. Tests written before code.

### 5. Check Documentation

- **Workflows:** `.windsurf/workflows/` (detailed guides)
- **Rules:** `.windsurf/rules/` (standards)
- **Full guide:** `docs/WORKFLOW_OPTIMIZATION_2025_10_15.md`

---

## Migration Tips

### Week 1: Try `/work`

Just use `/work` for a few tasks. See how it goes.

### Week 2: Create an Initiative

Use `/plan` for something complex. See the structured approach.

### Week 3: Full Chain

Let workflows chain automatically (work → plan → implement → commit).

### Week 4: Evaluate

What works? What needs tuning?

---

## Workflow Files

**Created:**

- `work.md` (9.6 KB) - Central orchestration
- `plan.md` (12.2 KB) - Research-based planning
- `implement.md` (9.3 KB) - Test-first execution

**Kept:**

- `commit.md` - Git operations
- `new-adr.md` - Architecture decisions
- `archive-initiative.md` - Completion tracking
- `run-tests.md` - Testing guide
- `meta-analysis.md` - Session review
- `test-before-commit.md` - Detailed testing protocol

---

## Quick Reference

| Want to... | Use |
|------------|-----|
| Continue work | `/work` |
| Start new feature | `/work [description]` |
| Create plan | `/plan [description]` |
| Fix tests | `/work` (auto-detects) |
| Commit changes | `/commit` |
| Review session | `/meta-analysis` |
| Create ADR | `/new-adr` |

---

## Need Help?

**Detailed docs:**

- `docs/WORKFLOW_OPTIMIZATION_2025_10_15.md` - Complete guide
- `docs/META_ANALYSIS_TRACKING.md` - Artifact tracking
- `.windsurf/workflows/*.md` - Individual workflow details

**Just start:**

```text
/work
```

**The agent will guide you from there.**

---

**Version:** 1.0
**Last Updated:** October 15, 2025
