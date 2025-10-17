---
description: Research-driven comprehensive project planning
auto_execution_mode: 2
---

# Planning Workflow

**Purpose:** Create robust, well-researched plans for features, initiatives, or complex changes.

**Invocation:** `/plan [optional: description]`

**Philosophy:** Good plans prevent wasted work. Invest time upfront for better execution.

---

## When to Use

Create a plan when:

- ✅ New feature (not documented)
- ✅ Complex refactoring (affects multiple modules)
- ✅ Architecture change (needs ADR)
- ✅ Multi-session work (>4 hours estimated)
- ✅ Cross-cutting concerns (security, performance)
- ✅ Unclear requirements (needs research)

Do NOT plan for:

- ❌ Simple bug fixes (<1 hour, 1-2 files)
- ❌ Documentation updates
- ❌ Routine dependency updates
- ❌ Following existing patterns

---

## Stage 1: Problem Definition

### 1.1 Capture Requirements

**If user provided description:**

- Restate in own words for confirmation
- Ask clarifying questions (max 3)
- Document assumptions explicitly

**Example:**

```markdown
## Requirement: User Authentication

**User Request:** "Add user authentication"

**Clarifications:**
1. Authentication method? (OAuth, JWT, API keys?)
2. User storage? (Database, external provider?)
3. Scope? (API only, or also MCP server?)

**Assumptions** (pending confirmation):
- API key authentication (simplest)
- In-memory storage initially
- API only (MCP later)
```

### 1.2 Define Success Criteria

**SMART format:**

```markdown
## Success Criteria

- [ ] [Specific deliverable]
- [ ] [Measurable outcome]
- [ ] [Quality gate]
- [ ] [Documentation requirement]

**Verification:** [How to confirm completion]
**Estimated Effort:** [N-M hours]
```

---

## Stage 2: Research & Discovery

**Call `/research` workflow:**

- Searches internal patterns (codebase, ADRs, rules)
- Performs web research for current best practices (MANDATORY)
- Evaluates dependencies and libraries
- Assesses security and performance
- Compares alternatives
- Provides recommendation with sources

**Output:** Research summary with recommended approach

**See:** `.windsurf/workflows/research.md`

---

## Stage 3: Generate Implementation Plan

**Call `/generate-plan` workflow:**

- Decomposes work into phases
- Breaks phases into concrete tasks (<4h each)
- Creates task dependency graph
- Identifies risks with mitigations
- Defines out-of-scope items
- Generates initiative document
- Creates ADR if architectural decision

**Output:** 
- Initiative file in `docs/initiatives/active/`
- Plan summary for approval

**See:** `.windsurf/workflows/generate-plan.md`

---

## Stage 4: Present and Validate

### 4.1 Present to User

**Summary format:**

```markdown
## 📋 Plan Complete: [Title]

**Estimated Effort:** [N hours] ([M sessions])
**Phases:** [Count] ([Names])
**Complexity:** [High/Medium/Low]

### Key Decisions

1. **[Decision 1]:** [What] — [Why]
2. **[Decision 2]:** [What] — [Why]

### Implementation Phases

**Phase 1 ([N]h):** [Brief description]
**Phase 2 ([N]h):** [Brief description]

### Risks Identified

- [Risk 1] - [Mitigation]
- [Risk 2] - [Mitigation]

### Next Steps

1. Review this plan
2. Approve or request changes
3. Begin Phase 1 implementation

**Ready to proceed?**
```

### 4.2 Handle Feedback

**If user requests changes:**

- Update initiative document
- Revise plan sections
- Re-present for approval

**If approved:**

- Proceed to Stage 5

---

## Stage 5: Handoff to Implementation

### 5.1 Load Full Context

**Call `/load-context` with scope="initiative":**

- Loads initiative file
- Loads related source files
- Loads test files
- Loads related ADRs

**See:** `.windsurf/workflows/load-context.md`

### 5.2 Begin Implementation

**Call `/implement` workflow:**

```bash
/implement --initiative=[filepath] --phase=1
```

**Workflow chain:**

```
/plan → /research → /generate-plan → /implement → /validate → /commit
```

---

## Quality Standards

### Good Plan Indicators

✅ **Comprehensive:**
- Requirements captured
- Research documented with sources
- Risks identified

✅ **Actionable:**
- Tasks concrete, not vague
- Each task <4 hours
- Clear acceptance criteria

✅ **Realistic:**
- Effort estimates reasonable
- Dependencies identified
- Risks have mitigations

### Poor Plan Indicators

❌ **Vague:**
- "Implement authentication" (what kind?)
- No specific tasks
- Missing details

❌ **Unrealistic:**
- Complex feature in 1 hour
- Ignoring dependencies
- No risk assessment

❌ **Incomplete:**
- No research
- Missing criteria
- No documentation plan

---

## Anti-Patterns

### ❌ Don't: Plan Too Much Detail

**Bad:** Specify every line of code
**Good:** Identify modules, APIs, patterns

### ❌ Don't: Skip Research

**Bad:** "I assume we should use X"
**Good:** "I researched X vs Y, X is better because [sources]"

### ❌ Don't: Create Plans for Simple Tasks

**Bad:** Plan for "fix typo in README"
**Good:** Just fix it

---

## Success Metrics

**Good planning results in:**

- ✅ Clear execution path
- ✅ Faster implementation (no mid-work research)
- ✅ Fewer mistakes (risks identified)
- ✅ Better quality (patterns researched)
- ✅ Complete delivery

**Poor planning results in:**

- ❌ Mid-work pivots
- ❌ Technical debt
- ❌ Incomplete features
- ❌ Security issues

---

## Integration

### Called By
- `/work` - When planning needed
- User - Direct invocation

### Calls
- `/research` - Best practices and pattern discovery (Stage 2)
- `/generate-plan` - Structure creation and task breakdown (Stage 3)
- `/load-context` - Full context loading (Stage 5)
- `/implement` - Begin execution (Stage 5)

---

## References

- `.windsurf/workflows/research.md` - Research subprocess
- `.windsurf/workflows/generate-plan.md` - Plan generation subprocess
- `.windsurf/workflows/implement.md` - Implementation workflow
- `docs/DOCUMENTATION_STRUCTURE.md` - Initiative file format
- `docs/initiatives/template.md` - Initiative template
