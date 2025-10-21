---
created: "2025-10-17"
updated: "2025-10-21"
description: Research best practices and existing patterns
auto_execution_mode: 3
category: Planning
complexity: 50
tokens: 2000
dependencies: []
status: active
---

# Research Workflow

**Purpose:** Gather comprehensive research for features, technologies, or architectural decisions.

**Invocation:** Called by `/plan` or standalone

**Philosophy:** Good research prevents mistakes and identifies proven patterns.

---

## Stage 1: Create Task Plan

```typescript
update_plan({
  explanation: "🔍 Starting /research workflow",
  plan: [
    { step: "1. /research - Define scope and search internal patterns", status: "in_progress" },
    { step: "2. /research - Perform web research (5+ queries)", status: "pending" },
    { step: "3. /research - Technical assessment", status: "pending" },
    { step: "4. /research - Compile research summary", status: "pending" }
  ]
})
```

---

## Stage 2: Define Scope & Internal Patterns

### Research Scope

**Identify:**

- Technology/framework specifics
- Security considerations  
- Performance implications
- Best practices for domain
- Similar implementations

### Internal Pattern Discovery

**Search existing codebase:**

```bash
grep_search("relevant|pattern", "src/", includes=["*.py"])
```

**Review related ADRs:**

```bash
grep_search("topic", "docs/adr/", recursive=true)
```

**Check project rules:**

```python
mcp0_read_text_file("/home/gxx/projects/mcp-web/.windsurf/rules/06_security_practices.md")
```

**Update plan:**

```typescript
update_plan({
  explanation: "Internal search complete, proceeding to web research",
  plan: [
    { step: "1. /research - Define scope and search internal patterns", status: "completed" },
    { step: "2. /research - Perform web research (5+ queries)", status: "in_progress" },
    // ...
  ]
})
```

---

## Stage 3: External Research (MANDATORY)

### Web Search Strategy

**ALWAYS perform 5+ searches for current best practices:**

| Query Type | Template | Example |
|------------|----------|---------|
| **Best practices** | `[Tech] best practices 2025` | `Python API auth best practices 2025` |
| **Framework-specific** | `[Framework] [Feature] guide 2025` | `FastAPI security guide 2025` |
| **Security focus** | `OWASP [Feature] 2025` | `OWASP API security 2025` |
| **Real-world** | `[Tech] production examples` | `Python JWT production examples` |
| **Security updates** | `[Library] CVE 2024 2025` | `bcrypt CVE 2024 2025` |

### Document Findings

```markdown
**Query:** [Search query]
**Key Findings:**
- [Finding 1 with URL]
- [Finding 2 with URL]

**Recommendations:**
- [Actionable recommendation]
```

### Compare Alternatives

| Approach | Pros | Cons | Use Case |
|----------|------|------|----------|
| API Keys | Simple, fast | Less secure | Internal APIs |
| JWT | Stateless, scalable | Complex setup | Web apps |
| OAuth2 | Industry standard | Heavy | Public APIs |

**Decision criteria:** Requirements, complexity vs benefit, security needs, maintenance

**Update plan:**

```typescript
update_plan({
  explanation: "Web research complete, moving to technical assessment",
  plan: [
    { step: "2. /research - Perform web research (5+ queries)", status: "completed" },
    { step: "3. /research - Technical assessment", status: "in_progress" },
    // ...
  ]
})
```

---

## Stage 4: Technical Assessment

### Dependency Analysis

**For each library:**

```markdown
**Library:** [name]
- **Maintenance:** [Active? Last release?]
- **Security:** [CVEs? Security policy?]
- **License:** [Compatible?]
- **Dependencies:** [What it pulls in?]
- **Community:** [Stars, downloads, issues]
```

**Check:** `pip show [package]` and `search_web("[package] CVE")`

### Performance & Security

**Performance:**

- Latency impact (ms)
- Memory footprint
- CPU usage
- Caching opportunities

**Security checklist (for sensitive features):**

- [ ] OWASP guidelines reviewed
- [ ] Vulnerabilities checked
- [ ] Input validation planned
- [ ] Output sanitization planned
- [ ] Auth/authz clear
- [ ] Audit logging included
- [ ] Rate limiting considered

**Update plan:**

```typescript
update_plan({
  explanation: "Assessment complete, compiling summary",
  plan: [
    { step: "3. /research - Technical assessment", status: "completed" },
    { step: "4. /research - Compile research summary", status: "in_progress" }
  ]
})
```

---

## Stage 5: Compile Research Summary

### Output Format

```markdown
# Research Summary: [Topic]

**Date:** YYYY-MM-DD
**Scope:** [What was researched]
**Decision Needed:** [What needs deciding]

---

## Best Practices (2025)

**From web research:**
1. [Practice 1] — [Source URL]
2. [Practice 2] — [Source URL]
3. [Practice 3] — [Source URL]

**From project patterns:**
1. [Internal pattern already used]
2. [Existing module with similar approach]

---

## Recommended Approach

**Recommendation:** [Specific approach]

**Rationale:**
- [Aligns with best practices]
- [Fits project constraints]
- [Balances complexity vs benefit]

**Alternatives Considered:**
- [Alternative 1] — Rejected because [reason]
- [Alternative 2] — Deferred because [reason]

---

## Libraries/Tools

| Library | Version | Purpose | Justification |
|---------|---------|---------|---------------|
| [name] | [version] | [use] | [why] |

**Installation:** `uv add [package]`

---

## Implementation Considerations

**Breaking Changes:**
- [Change] — Mitigation: [approach]

**Performance Impact:**
- [Impact area] — Benchmark: [expected result]

**Security Requirements:**
- [Requirement] — Implementation: [how]

---

## References

**External:**
- [URL 1] - [Description]

**Internal:**
- [filepath] - [Description]
- [ADR-XXXX] - [Related decision]

**Standards:**
- OWASP [guide]
- RFC [spec]
```

**Print exit:**

```markdown
✅ **Completed /research:** [N] sources analyzed, recommendation provided
```

---

## Quality Checks

### Completeness

- [ ] Web search performed (5+ queries)
- [ ] Internal patterns checked
- [ ] Security/performance assessed
- [ ] Dependencies evaluated
- [ ] Alternatives compared
- [ ] Sources cited with URLs

### Decision Readiness

- [ ] Clear recommendation
- [ ] Rationale explained
- [ ] Trade-offs identified
- [ ] Implementation path outlined

---

## Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| Skip web research | Research X vs Y vs Z with sources |
| Use outdated sources (pre-2024) | Prioritize 2024-2025 sources |
| Ignore security for speed | Evaluate security first |
| Over-research (4h for 1h task) | Proportional effort |

---

## Integration

### Called By

- `/plan` - Stage 2 (Research & Discovery)
- User - Standalone research

### Output

- Research summary (markdown)
- Recommendation with rationale
- Source citations

---

## External References

- OWASP Top 10: https://owasp.org/
- Python Package Index: https://pypi.org/
- CVE Database: https://cve.mitre.org/
- RFC Standards: https://www.rfc-editor.org/
