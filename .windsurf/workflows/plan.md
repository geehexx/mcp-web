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

- ✅ **New feature** (not documented)
- ✅ **Complex refactoring** (affects multiple modules)
- ✅ **Architecture change** (needs ADR)
- ✅ **Multi-session work** (>4 hours estimated)
- ✅ **Cross-cutting concerns** (security, performance, etc.)
- ✅ **Unclear requirements** (needs research)

Do NOT plan for:

- ❌ Simple bug fixes (1-2 files, <1 hour)
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

**Clarifications Needed:**
1. Authentication method? (OAuth, JWT, API keys, or multiple?)
2. User storage? (Database, external provider, or both?)
3. Scope? (API only, or also MCP server?)

**Assumptions** (pending confirmation):
- API key authentication (simplest for API use case)
- In-memory storage for now (future: database)
- Scope: API only (MCP later)
```

### 1.2 Define Success Criteria

**SMART criteria:**

- **Specific:** Exactly what will be delivered?
- **Measurable:** How to verify completion?
- **Achievable:** Realistic given constraints?
- **Relevant:** Aligns with project goals?
- **Time-bound:** Estimated effort?

**Example:**

```markdown
## Success Criteria

- [ ] API accepts API key in Authorization header
- [ ] Invalid keys return 401 Unauthorized
- [ ] Valid keys allow access to endpoints
- [ ] API key management CLI commands
- [ ] 95%+ test coverage for auth module
- [ ] Documentation updated (API.md, README.md)
- [ ] Security review passed (bandit, semgrep)

**Verification:** `task test:security` passes all auth tests
**Estimated Effort:** 6-8 hours (2 sessions)
```

---

## Stage 2: Research & Discovery

### 2.1 Search for Existing Patterns

**Check project first:**

1. **Similar implementations**

   ```bash
   grep_search("authentication\\|auth\\|api.?key", "src/", recursive=true)
   ```

2. **Related ADRs**

   ```bash
   list_dir("docs/adr/")
   # Read any security-related ADRs
   ```

3. **Security guidelines**

   ```bash
   read_file(".windsurf/rules/04_security.md")
   ```

### 2.2 External Research

**ALWAYS use web search for best practices:**

**Critical:** Use the `search_web` tool to find current best practices, not just examples.

```python
# Example web searches
search_web("Python API key authentication best practices 2025")
search_web("FastAPI JWT authentication security OWASP 2025")
search_web("API security patterns microservices 2025")
```

**Why web search is essential:**

- Technology evolves rapidly (2025 best practices differ from 2023)
- Security vulnerabilities discovered regularly
- New libraries and patterns emerge
- Official documentation updates
- Community consensus shifts

**Search strategy:**

1. **Broad context** - General best practices for the domain
2. **Specific technology** - Framework/library-specific patterns
3. **Security focus** - OWASP, CVE, security advisories
4. **Recent updates** - Include year (2025) in queries
5. **Production examples** - Real-world implementations

**Document findings:**

```markdown
## Research Findings

**Best Practices (2025):**
1. Use Bearer token format: `Authorization: Bearer <token>`
2. Hash API keys before storage (argon2 or bcrypt)
3. Rate limit authentication attempts (prevent brute force)
4. Support key rotation and revocation
5. Log authentication failures (security monitoring)

**Libraries:**
- `python-multipart` for form data
- `passlib` for hashing
- `python-jose` for JWT (if expanding later)

**References:**
- [OWASP API Security Top 10 (2023)](https://owasp.org/API-Security/)
- [FastAPI Security Documentation](https://fastapi.tiangolo.com/tutorial/security/)
- [Additional sources from web search]

**Note:** Always cite actual URLs from search results, not placeholder examples
```

### 2.3 Architecture Assessment

**Consider system impact:**

1. **Breaking changes?**
   - Existing API calls need updating?
   - Backward compatibility needed?

2. **New dependencies?**
   - Add to pyproject.toml
   - License compatible?
   - Actively maintained?

3. **Performance impact?**
   - Authentication overhead per request?
   - Caching strategy needed?

4. **Security implications?**
   - Needs security review?
   - Requires ADR?

---

## Stage 3: Decomposition & Task Planning

### 3.1 Break Down into Phases

**Use hierarchical decomposition:**

```markdown
## Implementation Phases

### Phase 1: Core Authentication (4 hours)
**Goal:** Basic API key validation

Tasks:
1. Create `src/mcp_web/auth.py` module
   - APIKey model (Pydantic)
   - Hash generation function
   - Validation function
2. Add FastAPI dependency injection
3. Unit tests (test_auth.py)
4. Integration with one endpoint (test)

**Exit Criteria:** One protected endpoint works with API key

### Phase 2: Key Management (2 hours)
**Goal:** CLI tools for API key operations

Tasks:
1. Add `mcp_web.cli` auth commands
   - `generate-key` - Create new API key
   - `list-keys` - Show active keys
   - `revoke-key` - Disable key
2. In-memory key storage (dict)
3. CLI tests

**Exit Criteria:** Can create, list, revoke keys via CLI

### Phase 3: Apply to All Endpoints (1 hour)
**Goal:** Protect all API endpoints

Tasks:
1. Apply dependency to all routes
2. Update API documentation
3. Add auth tests for each endpoint

**Exit Criteria:** All endpoints require authentication

### Phase 4: Documentation & Review (1 hour)
**Goal:** Production-ready

Tasks:
1. Update docs/API.md with auth examples
2. Update README.md setup instructions
3. Security review (bandit, semgrep)
4. Create ADR-XXXX-api-key-authentication.md

**Exit Criteria:** Documentation complete, security passed
```

### 3.2 Identify Dependencies

**Task dependency graph:**

```markdown
## Dependencies

```

Phase 1 (Core Auth) → Phase 2 (Key Mgmt)
                   ↘
                    → Phase 3 (Apply All)
                                         ↘
                                          → Phase 4 (Docs)

```

**Blockers:**
- None (can start immediately)

**Assumptions:**
- Using FastAPI (already in project)
- Python 3.10+ (already required)
```

### 3.3 Risk Assessment

**Identify potential issues:**

```markdown
## Risks & Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Breaking existing API clients | High | High | Add `/v2/` versioned endpoints |
| Performance degradation | Low | Medium | Benchmark before/after, cache validated keys |
| Security vulnerability | Medium | Critical | Follow OWASP guidelines, security review |
| Scope creep (OAuth, etc.) | Medium | Medium | Document explicitly out of scope |

**Out of Scope:**
- OAuth/OIDC integration (future: ADR needed)
- User management UI (API only)
- Database storage (Phase 2: separate initiative)
```

---

## Stage 4: Initiative Creation

### 4.1 Generate Initiative Document

**Create structured initiative:**

```markdown
# Initiative: API Key Authentication

**Status:** Active
**Created:** 2025-10-15
**Target Completion:** 2025-10-22
**Owner:** @agent
**Priority:** High

## Objective

Implement secure API key authentication for all MCP web service endpoints.

## Success Criteria

- [ ] Core authentication module (src/mcp_web/auth.py)
- [ ] CLI key management tools
- [ ] All endpoints protected
- [ ] 95%+ test coverage
- [ ] Documentation updated
- [ ] Security review passed
- [ ] ADR created

## Phases

[Copy Phase 1-4 from above]

## Research Summary

[Copy key findings from Stage 2]

## ADRs

- [ ] ADR-XXXX: API Key Authentication Strategy

## Related Documentation

- docs/API.md (needs update)
- docs/adr/ (new ADR)
- .windsurf/rules/04_security.md (reference)

## Updates

### 2025-10-15
Initiative created. Ready to begin Phase 1.
```

**Save to:** `docs/initiatives/active/YYYY-MM-DD-descriptive-name.md`

### 4.2 Create ADR (if needed)

**If architectural decision:**

```bash
# Invoke ADR workflow
/new-adr
```

---

## Stage 5: Plan Validation

### 5.1 Review Checklist

Before proceeding, verify:

- [ ] Requirements clearly defined
- [ ] Success criteria measurable
- [ ] Research completed and documented
- [ ] Tasks broken down (each <4 hours)
- [ ] Dependencies identified
- [ ] Risks assessed with mitigations
- [ ] Initiative document created
- [ ] ADR created (if architectural)

### 5.2 Present to User

**Summary format:**

```markdown
## 📋 Plan Complete: API Key Authentication

**Estimated Effort:** 8 hours (2-3 sessions)
**Phases:** 4 (Core → Management → Apply → Docs)
**Risks:** 3 identified, mitigation strategies defined

### Key Decisions

1. **API Keys only** (not OAuth) - simplicity for API use case
2. **In-memory storage** initially - future: database migration
3. **Versioned endpoints** (/v2/) - backward compatibility

### Next Steps

1. Review this plan
2. Approve or request changes
3. I'll begin Phase 1 implementation

**Ready to proceed?**
```

---

## Stage 6: Handoff to Implementation

### 6.1 Prepare Context Package

**For `/implement` workflow:**

```markdown
## Context Package

**Initiative:** docs/initiatives/active/2025-10-15-api-key-auth.md
**Phase:** 1 (Core Authentication)
**Tasks:** [List Phase 1 tasks]
**References:** [List key research links]
**Constraints:** [List out-of-scope items]

**Start with:** Task 1 (Create auth.py module)
```

### 6.2 Invoke Implementation

```markdown
/implement --initiative=docs/initiatives/active/2025-10-15-api-key-auth.md --phase=1
```

---

## Quality Standards

### Good Plan Indicators

✅ **Comprehensive:**

- All requirements captured
- Research documented with sources
- Risks identified

✅ **Actionable:**

- Tasks are concrete (not vague)
- Each task <4 hours
- Clear acceptance criteria

✅ **Realistic:**

- Effort estimates reasonable
- Dependencies identified
- Risks have mitigations

### Poor Plan Indicators

❌ **Vague:**

- "Implement authentication" (what kind?)
- "Make it secure" (how?)
- No specific tasks

❌ **Unrealistic:**

- "Complete in 1 hour" for complex feature
- Ignoring dependencies
- No risk assessment

❌ **Incomplete:**

- No research
- Missing acceptance criteria
- No documentation plan

---

## Anti-Patterns

### ❌ Don't: Plan Too Much Detail

**Bad:** Specify every line of code
**Good:** Identify modules, APIs, patterns

### ❌ Don't: Skip Research

**Bad:** "I assume we should use X"
**Good:** "I researched X vs Y, X is better because..."

### ❌ Don't: Ignore Existing Patterns

**Bad:** Reinvent authentication
**Good:** Follow existing security patterns

### ❌ Don't: Create Plans for Simple Tasks

**Bad:** Plan for "fix typo in README"
**Good:** Just fix it

---

## Templates

### Initiative Template

See: `docs/initiatives/template.md` (if exists) or create inline

### ADR Template

See: `docs/adr/template.md`

---

## Success Metrics

**Good planning results in:**

- ✅ Clear execution path (no ambiguity)
- ✅ Faster implementation (no research mid-work)
- ✅ Fewer mistakes (risks identified)
- ✅ Better code quality (patterns researched)
- ✅ Complete delivery (nothing forgotten)

**Poor planning results in:**

- ❌ Mid-work pivots ("Oh, we need X too")
- ❌ Technical debt ("We'll fix this later")
- ❌ Incomplete features ("Good enough for now")
- ❌ Security issues ("Didn't think of that")

---

## References

### Planning Methodologies

- [Agile User Stories and Acceptance Criteria](https://www.atlassian.com/agile/project-management/user-stories)
- [Work Breakdown Structure (WBS)](https://www.pmi.org/learning/library/applying-work-breakdown-structure-project-lifecycle-6979)
- [SMART Goals Framework](https://www.mindtools.com/pages/article/smart-goals.htm)

### AI Agent Planning

- [Agentic AI Workflows (2025)](https://devcom.com/tech-blog/ai-agentic-workflows/) - Planning and decomposition
- [AI Agent Architecture Best Practices (2025)](https://skywork.ai/blog/claude-agent-sdk-best-practices-ai-agents-2025/) - Orchestrator patterns
- [Enterprise AI Workflows (2025)](https://www.ampcome.com/post/ai-agents-enterprise-workflows-2025-guide) - Strategic assessment phases

### Project-Specific

- `docs/DOCUMENTATION_STRUCTURE.md` - Where to put artifacts
- `docs/adr/README.md` - ADR process
- `.windsurf/workflows/new-adr.md` - ADR creation workflow
- `.windsurf/workflows/work.md` - Integration with work orchestration

---

**Last Updated:** October 15, 2025
**Version:** 1.0
