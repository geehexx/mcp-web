---
created: "2025-10-18"
updated: "2025-10-19"
trigger: model_decision
description: Session end protocol, normative core enforcement, progress communication, and operational efficiency
category: operations
tokens: 1400
applyTo:
  - all
  - session_management
priority: high
status: active
---

# Rule: Operational Protocols

**Purpose:** Defines when and how to end sessions, communicate progress, and optimize operations.

**See also:**

- Core principles: [00_agent_directives.md](./00_agent_directives.md)
- Context engineering: [06_context_engineering.md](./06_context_engineering.md)

---

## 1. Session End Protocol

**TRIGGERS:** This protocol MUST be executed when ANY of the following occur:

1. **User says session is ending** ("that's all for now", "let's wrap up", etc.)
2. **Initiative marked "Completed" or "✅"** in status field
3. **All planned work for current request is done** (no more tasks to execute)
4. **User explicitly requests summary** of completed work

**NOT triggered by:**

- Mid-work progress updates
- Answering questions
- Quick fixes or patches
- Ongoing implementation (unless initiative complete)

### 1.1 Mandatory Steps

**Execute in order:**

1. **Commit all changes first:**
   - Run `git status` to check for unstaged changes
   - Commit working changes with proper message
   - If auto-fixes present, commit separately: `style(scope): apply [tool] auto-fixes`

2. **Archive completed initiatives:** Check `docs/initiatives/active/` for status "Completed" or "✅"
   - If found, MUST call `/archive-initiative` workflow for each
   - Do NOT skip - this is a quality gate

3. **Run meta-analysis:** MUST call `/meta-analysis` workflow
   - Creates session summary for cross-session continuity
   - Identifies workflow/rule improvements
   - This is NOT optional

4. **Update living documentation:** Check if PROJECT_SUMMARY or CHANGELOG need updates
   - Update PROJECT_SUMMARY.md if: major features completed, milestones reached, ADRs created, initiative status changed
   - Update CHANGELOG.md if: preparing release, breaking changes, new user-facing features
   - See `/meta-analysis` workflow Stage 6 for detailed triggers
   - Skip if: routine bug fixes, internal refactoring, work-in-progress

5. **Verify exit criteria:**
   - All changes committed (including auto-fixes and documentation updates)
   - Tests passing (if code changes made)
   - Session summary created in `docs/archive/session-summaries/`
   - Living documentation current (PROJECT_SUMMARY, CHANGELOG checked)

### 1.2 Critical Violations

**Never do these:**

- ❌ Never present "work complete" summary without running full protocol
- ❌ Never mark initiative as complete without archiving it
- ❌ Never leave unstaged changes when presenting completion summary
- ❌ The session end protocol is NOT optional when initiative completes

### 1.3 References

- Detailed protocol: [work-session-protocol.md](../workflows/work-session-protocol.md)
- Meta-analysis workflow: [meta-analysis.md](../workflows/meta-analysis.md)
- Archive workflow: [archive-initiative.md](../workflows/archive-initiative.md)

---

## 2. Progress Communication Strategy

### 2.1 During Active Work (NOT at session end)

- Provide brief progress updates every 5-10 minutes of work
- No approval needed for routine changes (formatting, type hints, docs)
- Continue working autonomously unless blocked or uncertain

**Progress Update Format:**

```markdown
## Progress Update

✅ Completed: [what's done]
🔄 In Progress: [current task]
⏳ Remaining: [what's left]

Continuing with [next task]...
```

### 2.2 When to Pause and Ask for Direction

**Pause and ask when:**

- Before major architectural changes (new patterns, breaking changes)
- When multiple valid approaches exist (user preference needed)
- If blocked by missing requirements or unclear specifications
- After discovering unexpected complexity (scope change needed)

**Don't pause for:**

- Routine implementation decisions
- Formatting or style choices
- Minor refactoring
- Documentation updates

### 2.3 Communication Anti-Patterns

**DO NOT confuse progress updates with session end:**

- ❌ DON'T present "completion summary" mid-session
- ❌ DON'T ask "shall I continue?" unless blocked
- ✅ DO keep working until initiative/request is complete OR user signals session end
- ✅ DO run Session End Protocol (Section 1) when work is actually complete

---

## 3. Normative Core Enforcement

### 3.1 Agent Constitution Framework (ACF) Compliance

**Principle:** "Think then Verify then Act" - All high-stakes operations must be validated.

**Architecture:**
Our system implements the five-core ACF model:

1. **Cognitive Core** (The Mind): Task planning, code generation, reasoning
2. **Memory Core** (The Context): Context loading, summarization, filtering
3. **Execution Core** (The World): File operations, git commands, tool calls
4. **Normative Core** (The Rules): Validation, security checks, quality gates
5. **Metacognitive Core** (The Self): Meta-analysis, progress evaluation

**Normative Validation Pattern:**

```text
Cognitive (GENERATE) → Normative (VERIFY) → Execution (TOOL_CALL)

Example:
Task Planning → Validate Quality → Commit Code
Code Generation → Run Tests → Deploy
Architecture Decision → Review ADR → Implement
```

### 3.2 Mandatory Validation Checkpoints

**High-stakes operations requiring validation:**

| Operation | Validation Required | Enforced By |
|-----------|--------------------|--------------|
| Committing code | `/validate` workflow | `/commit` workflow Stage 2 |
| Archiving initiative | Completion verification | `/archive-initiative` workflow |
| Creating ADR | Architectural review | `/new-adr` workflow |
| Deploying changes | Full test suite | Deployment workflow |
| Releasing version | All quality gates | Release workflow |

**Enforcement mechanism:**

- Validation is MANDATORY, not optional
- Workflows architecturally enforce validation before high-stakes actions
- Bypassing validation is documented as critical violation
- Pre-commit hooks provide additional enforcement

**See:**

- `/commit` workflow Stage 2 (mandatory validation)
- `/validate` workflow (comprehensive validation)
- `04_security.md` (security validation integration)

---

## 4. Operational Efficiency Principles

### 4.1 Core Efficiency Principles

1. **Batch Operations:** Always batch file reads when loading 3+ files (3-10x faster than sequential)
2. **Absolute Paths:** MCP tools (`mcp0_*`) require absolute paths; standard tools accept relative paths
3. **Context Loading Strategy:** Batch read essential context at session start, related files before implementation
4. **Performance First:** Optimize for minimal tool calls and network round-trips

### 4.2 Detailed Implementation

**For detailed implementation examples and patterns, see:**

- [Context Loading Patterns](../workflows/context-loading-patterns.md) - File loading strategies
- [Batch Operations](../workflows/batch-operations.md) - Optimization techniques
- `/work` workflow - Batch operation examples and context loading patterns
- Section 1.6 File Operations - MCP vs standard tool selection
- Section 1.7 Git Operations - MCP git tool patterns

### 4.3 Performance Targets

| Operation | Target Time | Notes |
|-----------|-------------|-------|
| Context detection | <5s | Essential files only |
| Context loading (initiative) | <10s | Batch read 10-15 files |
| Context loading (full) | <30s | All active initiatives + ADRs |
| Git status check | <1s | Fast check |
| Total session startup | <30s | Detection + routing + context |

---

## 5. Task System Usage

**See:** [00_agent_directives.md](./00_agent_directives.md) Section 1.11 for complete task system documentation.

**Quick reference:**

- **When required:** 3+ steps OR >5 minutes work
- **Format:** `<number>. /<workflow> - <description>`
- **Deliverable-focused:** Describe WHAT will be delivered, not HOW

---

## References

- Core directives: [00_agent_directives.md](./00_agent_directives.md)
- Context engineering: [06_context_engineering.md](./06_context_engineering.md)
- Work orchestration: [work.md](../workflows/work.md)
- Session protocol: [work-session-protocol.md](../workflows/work-session-protocol.md)

---

**Version:** 1.0.0 (Extracted from 00_agent_directives.md Phase 4 decomposition)
**Last Updated:** 2025-10-18
