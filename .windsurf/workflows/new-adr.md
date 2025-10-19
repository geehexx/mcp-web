---
created: "2025-10-17"
updated: "2025-10-18"
description: Create New Architecture Decision Record
auto_execution_mode: 3
category: Documentation
complexity: 45
tokens: 482
dependencies: []
status: active
---

# New ADR Workflow

Use this workflow when a significant architectural decision needs to be documented.

---

## Stage 0: Create Task Plan

🔄 **Entering /new-adr workflow**

**Create task plan:**

```typescript
update_plan({
  explanation: "📝 Starting /new-adr workflow",
  plan: [
    { step: "1. /new-adr - Identify decision and clarify requirements", status: "in_progress" },
    { step: "2. /new-adr - Research alternatives and best practices", status: "pending" },
    { step: "3. /new-adr - Draft ADR document", status: "pending" },
    { step: "4. /new-adr - Present for review and approval", status: "pending" },
    { step: "5. /new-adr - Update related documentation", status: "pending" },
    { step: "6. /commit - Commit ADR", status: "pending" }
  ]
})
```

---

## When to Use

Create an ADR for:

- New dependencies or technology choices
- Major algorithm or data structure changes
- Security-related decisions
- Performance-critical implementations
- API design decisions
- Changes to core architecture patterns

## Process

1. **Identify the decision:** Agent states, "I have identified a need for an architectural decision regarding [topic]."

2. **Clarify requirements:** Agent asks high-level questions to understand:
   - Business/technical constraints
   - Performance requirements
   - Security considerations
   - Scalability needs
   - Integration points

3. **Research alternatives:** Agent researches options using @web search for authoritative sources:
   - Official documentation
   - RFCs and standards
   - OWASP guidelines
   - Best practices (October 2025)

4. **Draft ADR:** Agent can use automated scaffolding or manual template:

   **Option A: Automated Scaffolding (Recommended)**

   ```bash
   task scaffold:adr
   # Interactive prompts for all fields
   # Automatic numbering from existing ADRs
   # Generates compliant markdown with frontmatter
   # Token savings: 1200 → 50 tokens (96% reduction)
   ```

   **Option B: Manual Template**
   - Use `docs/adr/template.md` as basis
   - Sequential number (check existing ADRs)
   - Title: `NNNN-verb-noun-phrase.md`
   - Status: Can be Proposed, Accepted, or Implemented
   - All sections filled: Context, Decision, Alternatives, Consequences, Implementation
   - Include external references with URLs

5. **Checkpoint: ADR Review**
   - **Presentation:** "The draft ADR is ready for your review. It proposes [decision] to solve [problem]. The key trade-offs are [X vs Y]."
   - **Guided Questions:**
     - "Does this decision align with our long-term goals?"
     - "Are the alternatives adequately considered?"
     - "Are the consequences acceptable?"
   - **Action:** Await approval

6. **Update related docs:** If approved, update:
   - `.windsurf/rules/` to reflect new decision
   - `docs/adr/README.md` to add to index
   - Related architecture documentation
   - Configuration examples if applicable

7. **Commit:** Use conventional commit format:

   ```text
   docs(adr): add ADR-NNNN for [decision topic]
   ```

## ADR Template Reference

Location: `docs/adr/template.md`

Key sections:

- **Status:** Proposed | Accepted | Implemented | Deprecated | Superseded
- **Context:** Why is this needed? What problem does it solve?
- **Decision:** What are we doing? (active voice, present tense)
- **Alternatives:** What else did we consider? Why not chosen?
- **Consequences:** Positive, negative, and neutral impacts
- **Implementation:** Key changes, migration steps, dependencies
- **References:** Links to research, documentation, related ADRs

## Example ADR Titles

- `0001-use-httpx-playwright-fallback.md`
- `0002-use-trafilatura-extraction.md`
- `0003-use-hierarchical-chunking.md`
- `0011-implement-distributed-caching.md`
- `0012-adopt-structured-logging.md`
