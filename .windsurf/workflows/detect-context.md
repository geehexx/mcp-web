---
created: "2025-10-17"
updated: "2025-10-21"
description: Intelligent context detection for work continuation
auto_execution_mode: 3
category: Operations
complexity: 80
tokens: 1870
version: v2.0-intelligent-semantic-preservation
dependencies: []
status: active
---

# Detect Context Workflow

**Purpose:** Analyze project state to determine next work, enabling autonomous continuation.

**Invocation:** `/detect-context` (called by `/work` or directly)

**Task plan:** Only if called directly (not by parent like `/work`)

## Stage 1: Load Context

1. List `docs/initiatives/active/` (`mcp0_list_directory`)
2. Build paths: DIR → `{dir}/initiative.md`, FILE → `{file}`
3. Batch read `mcp0_read_multiple_files` (PROJECT_SUMMARY + initiatives)
4. Check recent summaries (`ls -t docs/archive/session-summaries/*.md | head -3`)

**⚠️ CRITICAL:** MCP tools do NOT support globs. List directory first, then read explicit paths.

---

## Stage 2: Detect Signals

**Priority 0 (ABSOLUTE):** User explicit @mention or "continue with X" → Confidence 100%, route to specified

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

**Score calculation:** Next steps +30, Unresolved +30, Unchecked tasks +25, Initiative Active +25, Test failures +20, Unstaged changes +15, Recent commits +15, TODO markers +10

**Thresholds & Actions:**

| Score | Confidence | Action | User Interaction |
|-------|------------|--------|------------------|
| 80+ | High | Auto-route | None (announce) |
| 30-79 | Medium | Recommend | State choice, mention alternatives |
| <30 | Low | Prompt | List options, ask |

**Multiple signals:** Present ranked options with recommendation.

---

## Stage 5: Present & Route

| Confidence | Format | Example |
|------------|--------|-----------|
| High (80+) | Announce | "✓ Detected continuation → Routing to /implement (Initiative X)" |
| Medium (30-79) | Recommend | "Recommendation: Continue initiative\n\nAlternatives:\n1. Continue\n2. Run validation\n3. Other" |
| Low (<30) | List options | "Unable to determine.\n\nOptions:\n1. Initiative A\n2. Initiative B\n3. Create plan" |

## Stage 6: Return Results

**Return to `/work`:** Confidence score, route recommendation, extracted context

**Caller invokes `/load-context`** with appropriate scope

---

## Anti-Patterns

| Don't | Do |
|-------|----|
| Ignore user @mentions | User mention = 100% confidence, route exactly |
| Use globs with MCP tools | List directory first, then explicit paths |
| Ignore session summaries | Check summaries for "Next Steps" / "Unresolved" |
| Over-rely on git only | Check summaries + initiatives + git |
| Auto-route low confidence | Prompt user for direction |

---

## Performance Targets

| Phase | Target |
|-------|--------|
| Load | <1s |
| Search | <2s |
| Analyze | <1s |
| **Total** | **<4s** |

**Optimization:** Batch reads, parallel grep, cache git log

---

## References

- [Factory.ai Context Detection](https://factory.ai/news/context-window-problem)
- [Anthropic Long-Context Tips](https://docs.anthropic.com/claude/docs/long-context-window-tips)
- `.windsurf/workflows/work.md`
- `.windsurf/workflows/load-context.md`

**Version:** v2.0-intelligent-semantic-preservation
**Last Updated:** 2025-10-21
