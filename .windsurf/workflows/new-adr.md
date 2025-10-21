---
created: "2025-10-17"
updated: "2025-10-18"
description: Create New Architecture Decision Record
auto_execution_mode: 3
category: Documentation
complexity: 45
tokens: 995
dependencies: []
status: active
---

# New ADR Workflow

Use this workflow when a significant architectural decision needs to be documented.

---

## When to Use

**Create ADR for:** New dependencies, major algorithms, security decisions, performance-critical changes, API design, architecture changes

## Process

1. **Identify decision** + clarify requirements (constraints, performance, security)
2. **Research alternatives** (@web: official docs, RFCs, OWASP, best practices)
3. **Draft ADR:**
   - **Recommended:** `task scaffold:adr` (auto-numbering, compliant format)
   - **Manual:** `docs/adr/template.md` (NNNN-verb-noun-phrase.md)
4. **Review checkpoint** - Present trade-offs, await approval
5. **Update docs** - Rules, ADR index, related docs
6. **Commit** - `docs(adr): add ADR-NNNN for [topic]`

## Template Sections

**Status:** Proposed | Accepted | Implemented | Deprecated | Superseded
**Required:** Context, Decision, Alternatives, Consequences, Implementation, References
