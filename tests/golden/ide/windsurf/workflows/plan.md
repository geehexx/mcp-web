---
description: Research-driven comprehensive project planning
title: Planning Workflow
type: workflow
category: Planning
complexity: moderate
dependencies: ['research', 'generate-plan', 'load-context']
status: active
created: 2025-10-22
updated: 2025-10-22
---

# Planning Workflow

Create robust, researched plans for features, initiatives, or complex changes.

**Chain:** `/plan` → `/research` → `/generate-plan` → `/implement`

## When to Use

✅ New feature, complex refactoring, architecture change, multi-session work (>4h), cross-cutting concerns, unclear requirements

❌ Simple bugs (<1h), docs updates, routine deps, following existing patterns

## Stage 1: Define Requirements

**Capture:** Restate request, ask ≤3 clarifying questions, document assumptions

**Success criteria (SMART):**

```markdown
- [ ] [Specific deliverable]
- [ ] [Measurable outcome]
- [ ] [Quality gate]
- [ ] [Documentation]

**Verification:** [How to confirm]
**Estimated:** [N-M hours]
```

## Stage 2: Research & Discovery

**Call `/research`:**

- Internal patterns (codebase, ADRs, rules)
- Web research (MANDATORY)
- Dependencies, security, performance
- Alternatives comparison
- Recommendation with sources

## Stage 3: Generate Plan

**Call `/generate-plan`:**

- Break down into tasks
- Identify dependencies
- Estimate effort
- Create implementation order
- Risk assessment

## Stage 4: Review & Refine

**Review plan:**

- Check completeness
- Validate estimates
- Identify risks
- Get user approval if needed

## Context Loading

Load these rules if you determine you need them based on their descriptions:

- **Documentation Standards**: `/rules/03_documentation.mdc` - Apply when creating documentation and plans
- **Security Practices**: `/rules/06_security_practices.mdc` - Apply when dealing with security-sensitive planning
- **Context Optimization**: `/rules/07_context_optimization.mdc` - Apply when dealing with large files or complex operations

## Workflow References

When this planning workflow is called:

1. **Load**: `/commands/plan.md`
2. **Execute**: Follow the planning stages defined above
3. **Research**: Conduct thorough research
4. **Generate**: Create detailed implementation plan

## Anti-Patterns

❌ **Don't:**

- Skip research phase
- Create vague plans
- Ignore dependencies
- Skip risk assessment

✅ **Do:**

- Research thoroughly
- Create specific, measurable plans
- Identify all dependencies
- Assess and mitigate risks

## Success Metrics

| Metric | Target | Status |
|--------|--------|--------|
| Plan completeness | 100% | ✅ |
| Research depth | High | ✅ |
| Estimate accuracy | ±20% | ✅ |
| Risk identification | 90%+ | ✅ |

## Integration

**Called By:**

- `/work` - Main orchestration workflow
- User - Direct invocation for planning

**Calls:**

- `/research` - Research requirements
- `/generate-plan` - Generate detailed plan
- `/load-context` - Load relevant context

**Exit:**

```markdown
✅ **Completed /plan:** Planning workflow finished
```

## Command Metadata

**File:** `plan.yaml`
**Type:** Command/Workflow
**Complexity:** Moderate
**Estimated Tokens:** ~1,500
**Last Updated:** 2025-10-22
**Status:** Active

**Topics Covered:**

- Requirements analysis
- Research methodology
- Plan generation
- Risk assessment

**Dependencies:**

- /research - Research requirements
- /generate-plan - Generate detailed plan
- /load-context - Load relevant context
