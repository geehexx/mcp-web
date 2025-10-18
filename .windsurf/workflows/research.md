---
description: Research best practices and existing patterns
auto_execution_mode: 3
---

# Research Workflow

**Purpose:** Gather comprehensive research for features, technologies, or architectural decisions.

**Invocation:** Called by `/plan` or standalone for research tasks

**Philosophy:** Good research prevents mistakes and identifies proven patterns.

---

## Stage 1: Define Research Scope

### Identify What to Research

**From requirement:**

- Technology/framework specifics
- Security considerations
- Performance implications
- Best practices for domain
- Similar implementations

**Example:**

```markdown
**Research Needed:**
- API key authentication best practices
- Python libraries for key hashing
- FastAPI security patterns
- OWASP API security guidelines
```

---

## Stage 2: Internal Pattern Discovery

### 2.1 Search Existing Codebase

**Look for similar patterns:**

```bash
# Search for related implementations
grep_search("auth|authentication|api.?key", "src/", recursive=true, includes=["*.py"])

# Check for existing security patterns
grep_search("hash|encrypt|secret", "src/", recursive=true, includes=["*.py"])
```

### 2.2 Review Related ADRs

```bash
# List all ADRs
ls docs/adr/*.md

# Search for security-related decisions
grep_search("security|auth|encrypt", "docs/adr/", recursive=true)
```

### 2.3 Check Project Rules

**Read relevant rules:**

```python
# Always check security rules for security-related work
mcp0_read_text_file("/home/gxx/projects/mcp-web/.windsurf/rules/04_security.md")

# Check testing standards
mcp0_read_text_file("/home/gxx/projects/mcp-web/.windsurf/rules/01_testing_and_tooling.md")
```

---

## Stage 3: External Research (MANDATORY)

### 3.1 Web Search Strategy

**ALWAYS use web search for current best practices:**

**Search queries to run:**

1. **Broad best practices**

   ```text
   search_web("[Technology] best practices 2025")
   Example: "Python API authentication best practices 2025"
   ```

2. **Framework-specific**

   ```text
   search_web("[Framework] [Feature] guide 2025")
   Example: "FastAPI security authentication guide 2025"
   ```

3. **Security focus**

   ```text
   search_web("OWASP [Feature] security 2025")
   Example: "OWASP API security authentication 2025"
   ```

4. **Real-world examples**

   ```text
   search_web("[Technology] production examples [Feature]")
   Example: "Python JWT production examples authentication"
   ```

5. **Recent updates**

   ```text
   search_web("[Library] security vulnerabilities CVE 2024 2025")
   Example: "bcrypt security vulnerabilities CVE 2024 2025"
   ```

### 3.2 Document Findings

**For each search:**

```markdown
**Query:** [Search query used]
**Key Findings:**
- [Finding 1 with source URL]
- [Finding 2 with source URL]
- [Finding 3 with source URL]

**Recommendations:**
- [Actionable recommendation]
```

### 3.3 Compare Alternatives

**Create comparison table:**

| Approach | Pros | Cons | Use Case |
|----------|------|------|----------|
| API Keys | Simple, fast | Less secure than OAuth | Internal APIs, CLI tools |
| JWT | Stateless, scalable | Complex setup | Web apps, microservices |
| OAuth2 | Industry standard | Heavy implementation | Public APIs, 3rd party |

**Decision criteria:**

- Project requirements
- Complexity vs benefit
- Security needs
- Maintenance burden

---

## Stage 4: Technical Assessment

### 4.1 Dependency Analysis

**For each library considered:**

```markdown
**Library:** [name]
- **Maintenance:** [Active? Last release?]
- **Security:** [Known CVEs? Security policy?]
- **License:** [Compatible with project?]
- **Dependencies:** [What does it pull in?]
- **Community:** [GitHub stars, downloads, issues]
```

**Check with:**

```bash
# PyPI package info
pip show [package-name]

# Security advisories
search_web("[package-name] security advisories CVE")
```

### 4.2 Performance Considerations

**Measure or estimate:**

- Latency impact (ms per request)
- Memory footprint
- CPU usage
- Caching opportunities

### 4.3 Security Review

**For security-sensitive features:**

**Checklist:**

- [ ] OWASP guidelines reviewed
- [ ] Known vulnerabilities checked
- [ ] Input validation planned
- [ ] Output sanitization planned
- [ ] Authentication/authorization clear
- [ ] Audit logging included
- [ ] Rate limiting considered

---

## Stage 5: Compile Research Summary

### Format Output

```markdown
# Research Summary: [Topic]

**Date:** YYYY-MM-DD
**Scope:** [What was researched]
**Decision Needed:** [What needs to be decided]

---

## Best Practices (2025)

**From web research:**
1. [Practice 1] — [Source URL]
2. [Practice 2] — [Source URL]
3. [Practice 3] — [Source URL]

**From project patterns:**
1. [Internal pattern we already use]
2. [Existing module that follows similar approach]

---

## Recommended Approach

**Recommendation:** [Specific approach to take]

**Rationale:**
- [Reason 1: aligns with best practices]
- [Reason 2: fits project constraints]
- [Reason 3: balances complexity vs benefit]

**Alternatives Considered:**
- [Alternative 1] — Rejected because [reason]
- [Alternative 2] — Deferred to future phase because [reason]

---

## Libraries/Tools

| Library | Version | Purpose | Justification |
|---------|---------|---------|---------------|
| [name] | [version] | [use] | [why this one] |

**Installation:**
```bash
uv add [package-name]
```

---

## Implementation Considerations

**Breaking Changes:**

- [Change 1] — Mitigation: [approach]

**Performance Impact:**

- [Impact area] — Benchmark: [expected result]

**Security Requirements:**

- [Requirement 1] — Implementation: [how to satisfy]

---

## References

**External:**

- [URL 1] - [Description]
- [URL 2] - [Description]

**Internal:**

- [filepath 1] - [Description]
- [ADR-XXXX] - [Related decision]

**Standards:**

- OWASP [relevant guide]
- RFC [relevant spec]

```

---

## Quality Checks

### Research Completeness

- [ ] Web search performed for current best practices
- [ ] Internal patterns checked
- [ ] Security considerations documented
- [ ] Performance impact assessed
- [ ] Dependencies evaluated
- [ ] Alternatives compared
- [ ] Sources cited with URLs

### Decision Readiness

- [ ] Clear recommendation provided
- [ ] Rationale explained
- [ ] Trade-offs identified
- [ ] Implementation path outlined
- [ ] Risks documented

---

## Anti-Patterns

### ❌ Don't: Skip Web Research

**Bad:** "I think we should use X"
**Good:** "I researched X vs Y vs Z. X is best because [sources]"

### ❌ Don't: Use Outdated Sources

**Bad:** Using 2020 articles without checking for updates
**Good:** Prioritize 2024-2025 sources, note if using older

### ❌ Don't: Ignore Security

**Bad:** Pick fastest option without security review
**Good:** Evaluate security implications first

### ❌ Don't: Over-Research

**Bad:** Spend 4 hours researching for 1-hour task
**Good:** Research proportional to task complexity

---

## Integration

### Called By
- `/plan` - During Stage 2 (Research & Discovery)
- User - Standalone research tasks

### Output
- Research summary (markdown format)
- Recommendation with rationale
- Source citations

---

## References

- OWASP Top 10: https://owasp.org/
- Python Package Index (PyPI): https://pypi.org/
- Common Vulnerabilities (CVE): https://cve.mitre.org/
- RFC Standards: https://www.rfc-editor.org/
