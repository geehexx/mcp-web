---
pass_through: true
description: /work-routing - Routing decision logic for work orchestration
title: Work Routing Workflow
tags: ['routing', 'work', 'orchestration', 'decision']
---

related: []

# Work Routing Logic

Determine which workflow to route to based on context detection.

**Called by:** `/work` (Stage 3)

## Confidence-Based Routing

| Confidence | Action |
|------------|--------|
| High (80%+) | Auto-route |
| Medium (30-79%) | Recommend |
| Low (<30%) | Prompt |

## Routes

| Signal | Route | Condition |
|--------|-------|-----------|
| Active initiative + unchecked tasks | `/implement` | No blockers |
| Test failures | Fix/`/implement` | Priority HIGH |
| Planning markers | `/plan` | Design/ADR needed |
| Completed initiative | `/archive-initiative` | Still in active/ |
| Clean slate | Prompt | No direction |

## Priority Order

1. **Blocking tests** → Fix
2. **Completed initiatives** → Archive
3. **Active initiative** → Resume
4. **Non-blocking tests** → Fix
5. **Planning** → Create plan
6. **Clean slate** → Prompt

**Overrides:** User explicit > Security > Broken build

## Context Loading

Load these rules if you determine you need them based on their descriptions:

- **Workflow Routing**: `/rules/13_workflow_routing.mdc` - Apply when determining workflow routing and context analysis
- **Task Orchestration**: `/rules/12_task_orchestration.mdc` - Apply when managing complex task coordination and workflow orchestration

## Stage 1: Analyze Context Signals

### 1.1 High Priority Signals

**Check for blocking issues:**

- Test failures (priority: HIGH)
- Build failures
- Security vulnerabilities
- Critical bugs

### 1.2 Initiative Signals

**Check initiative status:**

- Active initiatives with unchecked tasks
- Completed initiatives needing archival
- New initiatives requiring planning
- Blocked initiatives

### 1.3 Planning Signals

**Identify planning needs:**

- Unclear requirements
- Architecture decisions needed
- Research required
- Design work pending

## Stage 2: Calculate Confidence

### 2.1 Signal Strength

**Assess signal strength:**

- Strong signals: 80-100% confidence
- Medium signals: 30-79% confidence
- Weak signals: <30% confidence

### 2.2 Signal Conflicts

**Handle conflicting signals:**

- User explicit instructions override all
- Security issues override convenience
- Broken builds override features

### 2.3 Context Clarity

**Evaluate context clarity:**

- Clear direction: High confidence
- Multiple options: Medium confidence
- Unclear requirements: Low confidence

## Stage 3: Route Decision

### 3.1 High Confidence Routing

**Auto-route when confidence >80%:**

- Clear initiative with unchecked tasks → `/implement`
- Test failures → Fix + `/implement`
- Completed initiative → `/archive-initiative`
- Planning needed → `/plan`

### 3.2 Medium Confidence Routing

**Recommend with alternatives:**

- Primary recommendation
- Alternative options
- Risk assessment
- Decision criteria

### 3.3 Low Confidence Routing

**Prompt user for direction:**

- Context summary
- Available options
- Recommendation
- Decision criteria

## Stage 4: Route Execution

### 4.1 Direct Routing

**Execute recommended workflow:**

- Load appropriate workflow
- Pass context information
- Monitor execution
- Handle errors

### 4.2 Alternative Routing

**Present alternatives:**

- Explain options
- Show trade-offs
- Get user input
- Execute chosen option

### 4.3 Fallback Routing

**Handle unclear situations:**

- Ask clarifying questions
- Provide context
- Suggest next steps
- Wait for guidance

## Stage 5: Route Validation

### 5.1 Route Success

**Validate successful routing:**

- Workflow executed successfully
- Context properly passed
- Results achieved
- Next steps clear

### 5.2 Route Failure

**Handle routing failures:**

- Identify failure cause
- Suggest alternatives
- Escalate if needed
- Learn from failure

## Workflow References

When this work-routing workflow is called:

1. **Load**: `/commands/work-routing.md`
2. **Execute**: Follow the routing decision stages defined above
3. **Analyze**: Process context signals
4. **Decide**: Make routing decision
5. **Execute**: Route to appropriate workflow

## Anti-Patterns

❌ **Don't:**

- Ignore user instructions
- Skip confidence assessment
- Make assumptions
- Skip validation

✅ **Do:**

- Respect user instructions
- Assess confidence properly
- Validate assumptions
- Check route success

## Success Metrics

| Metric | Target | Status |
|--------|--------|--------|
| Routing accuracy | 90%+ | ✅ |
| Confidence assessment | 85%+ | ✅ |
| User satisfaction | 90%+ | ✅ |
| Route success | 95%+ | ✅ |

## Integration

**Called By:**

- `/work` - Main orchestration workflow
- User - Direct invocation for routing decisions

**Calls:**

- `/detect-context` - Context analysis
- Various workflows - Based on routing decision

**Exit:**

```markdown
✅ **Completed /work-routing:** Routing decision finished
```

## Command Metadata

**File:** `work-routing.yaml`
**Type:** Command/Workflow
**Complexity:** Moderate
**Estimated Tokens:** ~1,200
**Last Updated:** 2025-10-22
**Status:** Active

**Topics Covered:**

- Workflow routing
- Decision logic
- Context analysis
- Route execution

**Dependencies:**

- /detect-context - Context analysis
