---
created: "2025-10-17"
updated: "2025-10-21"
description: Intelligent context detection for work continuation
auto_execution_mode: 3
category: Operations
complexity: 80
tokens: 2200
dependencies: []
status: active
---

# Detect Context Workflow

**Purpose:** Analyze project state to determine what work should happen next, enabling autonomous continuation.

**Invocation:** `/detect-context` (called by `/work` or directly)

---

## Execution

**Task plan:** Only if called directly (not by parent workflow like `/work`)

## Stage 1: Load Context

**Process:**

1. List `docs/initiatives/active/` (use `mcp0_list_directory`)
2. Build initiative paths: DIR → `{dir}/initiative.md`, FILE → `{file}`
3. Batch read with `mcp0_read_multiple_files` (PROJECT_SUMMARY + initiatives)
4. Check recent session summaries (`ls -t docs/archive/session-summaries/*.md | head -3`)

**⚠️ CRITICAL:** MCP tools do NOT support globs. List directory first, then read explicit paths.

---

## Stage 2: Detect Signals

**Priority 0 (ABSOLUTE):** User explicit @mention or "continue with X" → Confidence 100%, route to specified initiative

**Priority 1-5:**

- Session summary "Next Steps" / "Unresolved"
- Initiative unchecked tasks (`- [ ]`)
- Test failures (`task test:fast | grep FAILED`)
- Git uncommitted changes (`git status --short`)
- TODO markers (`grep -r "TODO\|FIXME\|XXX" docs/`)

**⚠️ CRITICAL:** User explicit mentions override ALL other signals.

---

## Stage 3: Interpret & Route

**Detection Matrix:**

| Pattern | Confidence | Route | Context Extracted |
|---------|------------|-------|-------------------|
| Session "Next Steps" + initiative | High | `/implement` | Summary file, next steps, unresolved |
| Unchecked tasks (3+) | High | `/implement` | Initiative, next 3 tasks, phase |
| Test failures | High | `/implement` | Failures, affected modules |
| "Plan" keywords in summary | High | `/plan` | Planning markers, scope |
| Multiple incomplete features | Medium | `/plan` | All initiatives |
| Recent ADR + "decide" | Medium | `/new-adr` | Decision context |
| Unstaged changes, no context | Medium | Prompt | Changed files |
| Clean state, no initiative | Low | Prompt | Active initiatives list |

---

## Stage 4: Confidence Scoring

**Score calculation:**

- Next steps in summary: +30
- Unresolved in summary: +30
- Unchecked tasks: +25
- Initiative Active: +25
- Test failures: +20
- Unstaged changes: +15
- Recent commits same area: +15
- TODO markers: +10

**Thresholds & Actions:**

| Score | Confidence | Action | User Interaction |
|-------|------------|--------|------------------|
| 80+ | High | Auto-route | None (announce route) |
| 30-79 | Medium | Recommend | State choice, mention alternatives |
| <30 | Low | Prompt | List options, ask for direction |

**Multiple signals:** Present ranked options with recommendation.

---

## Stage 5: Present & Route

**Output format by confidence:**

| Confidence | Format | Example |
|------------|--------|----------|
| High (80+) | Announce route | "✓ Detected continuation from last session → Routing to /implement (Initiative X)" |
| Medium (30-79) | Recommend + alternatives | "Recommendation: Continue initiative\n\nAlternatives:\n1. Continue (recommended)\n2. Run validation\n3. Other" |
| Low (<30) | List options | "Unable to determine next step.\n\nOptions:\n1. Continue Initiative A\n2. Continue Initiative B\n3. Create plan" |

---

## Stage 6: Return Results

**Return to caller (`/work`):** Confidence score, route recommendation, extracted context

**Caller invokes `/load-context`** with appropriate scope based on route

---

---

## Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| Ignore user explicit @mentions | User mention = 100% confidence, route exactly as specified |
| Use glob patterns with MCP tools | List directory first, then read explicit paths |
| Ignore session summaries | Check summaries for "Next Steps" / "Unresolved" |
| Over-rely on git status only | Check summaries + initiatives + git |
| Auto-route on low confidence (<30%) | Prompt user for direction |

---

## Performance Targets

| Phase | Target |
|-------|--------|
| Load context | <1s |
| Search signals | <2s |
| Analyze | <1s |
| **Total** | **<4s** |

**Optimization:** Batch reads, parallel grep, cache git log

---

## References

- [Factory.ai Context Detection](https://factory.ai/news/context-window-problem)
- [Anthropic Long-Context Tips](https://docs.anthropic.com/claude/docs/long-context-window-tips)
- `.windsurf/workflows/work.md`
- `.windsurf/workflows/load-context.md`

---

**Last Updated:** October 21, 2025
**Version:** 2.0.0
