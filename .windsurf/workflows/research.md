---
created: "2025-10-17"
updated: "2025-10-21"
description: Research best practices and existing patterns
auto_execution_mode: 3
category: Planning
complexity: 50
tokens: 1380
version: v2.0-intelligent-semantic-preservation
dependencies: []
status: active
---

# Research Workflow

**Purpose:** Gather comprehensive research for features, technologies, or architectural decisions.

**Invocation:** Called by `/plan` or standalone

**Philosophy:** Good research prevents mistakes, identifies proven patterns.

---

## Stage 1: Create Task Plan

```typescript
update_plan({
  explanation: "🔍 Starting /research workflow",
  plan: [
    { step: "1. /research - Define research scope", status: "in_progress" },
    { step: "2. /research - Search internal patterns", status: "pending" },
    { step: "  2.1. /research - Search codebase", status: "pending" },
    { step: "  2.2. /research - Review ADRs", status: "pending" },
    { step: "  2.3. /research - Check project rules", status: "pending" },
    { step: "3. /research - Perform external web research", status: "pending" },
    { step: "  3.1. /research - Run web searches (5+ queries)", status: "pending" },
    { step: "  3.2. /research - Document findings", status: "pending" },
    { step: "  3.3. /research - Compare alternatives", status: "pending" },
    { step: "4. /research - Technical assessment", status: "pending" },
    { step: "  4.1. /research - Analyze dependencies", status: "pending" },
    { step: "  4.2. /research - Assess performance", status: "pending" },
    { step: "  4.3. /research - Security review", status: "pending" },
    { step: "5. /research - Compile research summary", status: "pending" }
  ]
})
```

---

## Stage 2: Define Research Scope

**From requirement:** Technology/framework specifics, security, performance, best practices, similar implementations

**Example:**
```markdown
**Research Needed:**
- API authentication best practices
- Python libraries for key hashing
- FastAPI security patterns
- OWASP API security guidelines
```

---

## Stage 3: Internal Pattern Discovery

### 3.1 Search Codebase

```bash
grep_search("auth|authentication", "src/", recursive=true, includes=["*.py"])
grep_search("hash|encrypt|secret", "src/", recursive=true, includes=["*.py"])
```

### 3.2 Review ADRs

```bash
ls docs/adr/*.md
grep_search("security|auth|encrypt", "docs/adr/", recursive=true)
```

### 3.3 Check Project Rules

```python
mcp0_read_text_file("/home/gxx/projects/mcp-web/.windsurf/rules/06_security_practices.md")
mcp0_read_text_file("/home/gxx/projects/mcp-web/.windsurf/rules/02_testing.md")
```

---

## Stage 4: External Web Research

### 4.1 Run 5+ Targeted Searches

1. **Best practices:** `search_web("[Technology] [Feature] best practices 2025")`
2. **Performance:** `search_web("[Technology] [Feature] performance benchmarks")`
3. **Security:** `search_web("OWASP [Feature] security 2025")`
4. **Examples:** `search_web("[Technology] production examples [Feature]")`
5. **Recent updates:** `search_web("[Library] security vulnerabilities CVE 2024 2025")`

### 4.2 Document Findings

**Per search:**
```markdown
**Query:** [query]
**Key Findings:** [3 findings with URLs]
**Recommendations:** [actionable items]
```

### 4.3 Compare Alternatives

| Approach | Pros | Cons | Use Case |
|----------|------|------|----------|
| API Keys | Simple, fast | Less secure | Internal APIs, CLI |
| JWT | Stateless, scalable | Complex | Web apps, microservices |
| OAuth2 | Standard | Heavy | Public APIs, 3rd party |

**Decision criteria:** Requirements, complexity vs benefit, security, maintenance

---

## Stage 5: Technical Assessment

### 5.1 Dependency Analysis

**Per library:**
```markdown
**Library:** [name]
- Maintenance: [Active? Last release?]
- Security: [CVEs? Policy?]
- License: [Compatible?]
- Dependencies: [What it pulls]
- Community: [Stars, downloads]
```

**Check:** `pip show [package]`, `search_web("[package] CVE")`

### 5.2 Performance

**Measure/estimate:** Latency, memory, CPU, caching

### 5.3 Security Review

**Checklist:**
- [ ] OWASP guidelines reviewed
- [ ] Vulnerabilities checked
- [ ] Input validation planned
- [ ] Output sanitization planned
- [ ] Auth/authz clear
- [ ] Audit logging included
- [ ] Rate limiting considered

---

## Stage 6: Compile Summary

```markdown
# Research Summary: [Topic]

**Date:** YYYY-MM-DD
**Scope:** [What researched]
**Decision:** [What needs deciding]

## Best Practices (2025)
**Web:** [3 practices with URLs]
**Project:** [2 internal patterns]

## Recommendation
**Approach:** [Specific approach]
**Rationale:** [3 reasons]
**Alternatives:** [2 alternatives with rejection reasons]

## Libraries/Tools
| Library | Version | Purpose | Why |
|---------|---------|---------|-----|
| [name] | [ver] | [use] | [justification] |

**Install:** `uv add [package]`

## Implementation
**Breaking:** [changes + mitigation]
**Performance:** [impact + benchmark]
**Security:** [requirements + implementation]

## References
**External:** [2 URLs]
**Internal:** [2 filepaths/ADRs]
**Standards:** [OWASP/RFC]
```

**Exit:** `✅ **Completed /research:** [N] sources analyzed, recommendation provided`

---

## Quality Checks

**Completeness:** Web search (current), internal patterns, security, performance, dependencies, alternatives, sources cited

**Decision Readiness:** Clear recommendation, rationale, trade-offs, implementation path, risks

---

## Anti-Patterns

| Don't | Do |
|-------|----|
| Skip web research | Research X vs Y vs Z with sources |
| Use outdated sources | Prioritize 2024-2025, note if older |
| Ignore security | Evaluate security first |
| Over-research | Research proportional to complexity |

---

## Integration

**Called By:** `/plan`, user (standalone)
**Output:** Summary, recommendation, citations

## References

- [OWASP](https://owasp.org/)
- [PyPI](https://pypi.org/)
- [CVE](https://cve.mitre.org/)
- [RFC](https://www.rfc-editor.org/)

**Version:** v2.0-intelligent-semantic-preservation
**Last Updated:** 2025-10-21
