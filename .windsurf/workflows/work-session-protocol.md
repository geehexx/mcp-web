---
description: /work-session-protocol - Session end protocol and completion detection
title: Work Session Protocol Workflow
type: workflow
category: Sub-workflow
complexity: moderate
dependencies: ['archive-initiative', 'meta-analysis']
status: active
created: 2025-10-22
updated: 2025-10-22
---

# Work Session End Protocol

Detect work completion and execute session end protocol.

**Called by:** `/work` (Stage 5)

## Completion Detection

**Trigger if ANY:**

1. Initiative Status = "Completed" or "✅"
2. All planned tasks complete
3. User signal: "wrap up", "end session", "done"

**NOT triggered:** Progress updates, questions, quick fixes, ongoing work

## Protocol

```typescript
update_plan({
  explanation: "🏁 Session end detected",
  plan: [
    { step: "5.1. /commit - Commit all", status: "in_progress" },
    { step: "5.2. /archive-initiative - Archive completed", status: "pending" },
    { step: "5.3. /meta-analysis - Execute", status: "pending" },
    { step: "5.4. /work-session-protocol - Verify exit criteria", status: "pending" }
  ]
})
```

## Stage 1: Commit All

```bash
git status --short
git add <files> && git commit -m "type(scope): description"
# Auto-fixes separately: style(scope): apply [tool] auto-fixes
```

**Commit strategy:**

- Group related changes
- Use conventional commit format
- Separate auto-fixes
- Include meaningful descriptions

## Stage 2: Archive Completed Initiatives

**Call** `/archive-initiative`:

- Check for completed initiatives
- Validate completion criteria
- Move to archive
- Update documentation

**Archive criteria:**

- Status = "Completed" or "✅"
- All success criteria met
- No blocking issues
- Documentation updated

## Stage 3: Execute Meta-Analysis

**Call** `/meta-analysis`:

- Extract session data
- Generate session summary
- Update living documentation
- Commit changes

**Meta-analysis includes:**

- Session summary
- Pattern analysis
- Documentation updates
- Metrics generation

## Stage 4: Verify Exit Criteria

**Check all criteria met:**

- [ ] All changes committed
- [ ] Tests passing
- [ ] Initiatives archived (if applicable)
- [ ] Meta-analysis completed
- [ ] Session summary created
- [ ] Documentation updated

## Stage 5: Present Session Summary

**Present final summary:**

```markdown
## Session Summary

**Duration:** X hours
**Status:** Completed
**Key Accomplishments:**
- [Accomplishment 1]
- [Accomplishment 2]
- [Accomplishment 3]

**Next Steps:**
- [Next step 1]
- [Next step 2]

**Session Complete** ✅
```

## Context Loading

Load these rules if you determine you need them based on their descriptions:

- **Task Orchestration**: `/rules/12_task_orchestration.mdc` - Apply when managing complex task coordination and workflow orchestration
- **Workflow Routing**: `/rules/13_workflow_routing.mdc` - Apply when determining workflow routing and context analysis

## Workflow References

When this work-session-protocol workflow is called:

1. **Load**: `/commands/work-session-protocol.md`
2. **Execute**: Follow the session end protocol stages defined above
3. **Commit**: Commit all changes
4. **Archive**: Archive completed initiatives
5. **Analyze**: Execute meta-analysis
6. **Verify**: Check exit criteria

## Anti-Patterns

❌ **Don't:**

- Skip commit step
- Ignore completion criteria
- Skip meta-analysis
- Skip verification

✅ **Do:**

- Commit all changes
- Check completion criteria
- Execute meta-analysis
- Verify all criteria met

## Success Metrics

| Metric | Target | Status |
|--------|--------|--------|
| Commit success | 100% | ✅ |
| Archive success | 100% | ✅ |
| Meta-analysis success | 100% | ✅ |
| Exit criteria met | 100% | ✅ |

## Integration

**Called By:**

- `/work` - Main orchestration workflow
- User - Direct invocation for session end

**Calls:**

- `/commit` - Commit changes
- `/archive-initiative` - Archive completed initiatives
- `/meta-analysis` - Session analysis

**Exit:**

```markdown
✅ **Completed /work-session-protocol:** Session end protocol finished
```

---

## Command Metadata

**File:** `work-session-protocol.yaml`
**Type:** Command/Workflow
**Complexity:** Moderate
**Estimated Tokens:** ~1,100
**Last Updated:** 2025-10-22
**Status:** Active

**Topics Covered:**

- Session end protocol
- Completion detection
- Change management
- Documentation updates

**Dependencies:**

- /archive-initiative - Archive completed initiatives
- /meta-analysis - Session analysis
