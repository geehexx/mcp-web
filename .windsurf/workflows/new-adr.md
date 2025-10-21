---
created: "2025-10-17"
updated: "2025-10-21"
description: Create New Architecture Decision Record
auto_execution_mode: 3
category: Documentation
complexity: 45
tokens: 850
dependencies: []
status: active
version: "2.0-intelligent-semantic-preservation"
---

# New ADR Workflow

Document significant architectural decisions.

---

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
