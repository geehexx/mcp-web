---
description: Create New Architecture Decision Record
title: New ADR Workflow
type: workflow
category: Documentation
complexity: moderate
dependencies: []
status: active
created: 2025-10-22
updated: 2025-10-22
---

# New ADR Workflow

Document significant architectural decisions.

## When to Use

New dependencies, major algorithms, security decisions, performance changes, API design, architecture changes.

## Process

1. **Identify** decision + clarify constraints (performance, security)
2. **Research** alternatives (@web: official docs, RFCs, OWASP)
3. **Draft:**
   - `task scaffold:adr` (auto-numbering, compliant)
   - Manual: `docs/adr/template.md` (NNNN-verb-noun-phrase.md)
4. **Review** - Present trade-offs, await approval
5. **Update** - Rules, ADR index, related docs
6. **Commit** - `docs(adr): add ADR-NNNN for [topic]`

## Template

**Status:** Proposed | Accepted | Implemented | Deprecated | Superseded
**Required:** Context, Decision, Alternatives, Consequences, Implementation, References

## Stage 1: Identify Decision

### 1.1 Decision Scope

**Define the decision:**
- What architectural decision needs to be made?
- What are the key constraints?
- What are the performance requirements?
- What are the security considerations?

### 1.2 Context Analysis

**Understand the context:**

- Why is this decision needed?
- What problem does it solve?
- What are the current limitations?
- What are the business drivers?

## Stage 2: Research Alternatives

### 2.1 Internal Research

**Check existing patterns:**

- Similar decisions in codebase
- Existing ADRs
- Project standards
- Team preferences

### 2.2 External Research

**Research alternatives:**

- Official documentation
- RFCs and standards
- OWASP guidelines
- Community best practices
- Security advisories

### 2.3 Alternative Analysis

**Compare options:**

- Pros and cons
- Performance implications
- Security considerations
- Maintenance requirements
- Community support

## Stage 3: Draft ADR

### 3.1 ADR Structure

```markdown
---
Status: "Proposed"
Created: "YYYY-MM-DD"
Updated: "YYYY-MM-DD"
Owner: "@ai-agent"
Priority: "High"
Tags: ["architecture", "decision", "technology"]
Related: ["/path/to/related/adr"]

# ADR-NNNN: [Verb-Noun-Phrase]

## Status

[Proposed | Accepted | Implemented | Deprecated | Superseded]

## Context

[What is the issue that we're seeing that is motivating this decision or change?]

## Decision

[What is the change that we're proposing or have agreed to implement?]

## Alternatives

[What other options have we considered and why have we rejected them?]

## Consequences

[What becomes easier or more difficult to do and any risks introduced by this change?]

## Implementation

[How will this decision be implemented?]

## References

[Links to relevant documentation, RFCs, or other resources]
```

### 3.2 Content Guidelines

**Context:**

- Clear problem statement
- Business drivers
- Technical constraints
- Current limitations

**Decision:**

- Specific choice made
- Rationale for choice
- Key assumptions
- Implementation approach

**Alternatives:**

- Other options considered
- Why alternatives were rejected
- Trade-offs analyzed
- Risk assessment

**Consequences:**

- Positive impacts
- Negative impacts
- Risks introduced
- Mitigation strategies

## Stage 4: Review Process

### 4.1 Internal Review

**Present to team:**

- Decision rationale
- Alternative analysis
- Trade-offs considered
- Implementation plan

### 4.2 Stakeholder Approval

**Get approval from:**

- Technical lead
- Security team (if applicable)
- Product owner
- Architecture team

### 4.3 Revise Based on Feedback

**Incorporate feedback:**

- Address concerns
- Refine decision
- Update consequences
- Adjust implementation

## Stage 5: Update Documentation

### 5.1 Update ADR Index

**Add to index:**

- ADR number and title
- Status and date
- Brief description
- Related ADRs

### 5.2 Update Related Docs

**Update relevant documentation:**

- Architecture overview
- Implementation guides
- Security documentation
- API documentation

### 5.3 Update Rules

**Update project rules if needed:**

- Coding standards
- Security practices
- Documentation requirements
- Testing requirements

## Stage 6: Commit Changes

### 6.1 Commit ADR

```bash
git add docs/adr/NNNN-verb-noun-phrase.md
git commit -m "docs(adr): add ADR-NNNN for [topic]

- Decision: [Brief description]
- Status: [Status]
- Impact: [Key impacts]"
```

### 6.2 Update Index

```bash
git add docs/adr/README.md
git commit -m "docs(adr): update index for ADR-NNNN"
```

## Context Loading

Load these rules if you determine you need them based on their descriptions:

- **Documentation Standards**: `/rules/03_documentation.mdc` - Apply when creating documentation and ADRs
- **Security Practices**: `/rules/06_security_practices.mdc` - Apply when dealing with security-sensitive decisions
- **Context Optimization**: `/rules/07_context_optimization.mdc` - Apply when dealing with large files or complex operations

## Workflow References

When this new-adr workflow is called:

1. **Load**: `/commands/new-adr.md`
2. **Execute**: Follow the ADR creation stages defined above
3. **Research**: Analyze alternatives thoroughly
4. **Draft**: Create comprehensive ADR document
5. **Review**: Get stakeholder approval
6. **Update**: Update related documentation

## Anti-Patterns

❌ **Don't:**

- Skip research phase
- Ignore alternatives
- Skip stakeholder review
- Create vague decisions

✅ **Do:**

- Research thoroughly
- Consider all alternatives
- Get proper approval
- Make specific decisions

## Success Metrics

| Metric | Target | Status |
|--------|--------|--------|
| Research depth | High | ✅ |
| Alternative coverage | Complete | ✅ |
| Stakeholder approval | 100% | ✅ |
| Documentation quality | High | ✅ |

## Integration

**Called By:**

- User - Direct invocation for ADR creation
- Other workflows - When architectural decisions are needed

**Calls:**

- Research tools
- Documentation review
- Stakeholder approval

**Exit:**

```markdown
✅ **Completed /new-adr:** ADR creation finished
```

## Command Metadata

**File:** `new-adr.yaml`
**Type:** Command/Workflow
**Complexity:** Moderate
**Estimated Tokens:** ~850
**Last Updated:** 2025-10-22
**Status:** Active

**Topics Covered:**

- Architecture decisions
- Documentation creation
- Decision analysis
- Stakeholder review

**Dependencies:**

- None (standalone workflow)
