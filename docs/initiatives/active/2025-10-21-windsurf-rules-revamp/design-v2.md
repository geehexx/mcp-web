# Windsurf Rules System Design v2 (Hybrid Approach)

**Date:** 2025-10-21  
**Revision:** Hybrid trigger strategy confirmed

---

## Design Philosophy: Hybrid Loading

**Key insight:** Rules with `model_decision` or `glob` triggers can ALSO be explicitly @mentioned for reinforcement.

**Benefits:**
- Semantic loading when model detects need (automatic)
- Explicit loading when workflow knows it needs full context (@mention)
- Reduces need for `manual` trigger (only for truly rare reference material)

---

## Revised Structure (16 rules, not 18)

### Always-On (1 rule, ~3KB)

| Rule | Content | Why Always-On |
|------|---------|---------------|
| `00_core_directives.md` | Trimmed persona, guiding principles, tool selection | Core identity, always relevant |

**Token budget:** ~3,000 tokens (always loaded)

---

### Glob Triggers (5 rules, ~9KB)

| Rule | Globs | Topics | Tokens | Can @mention? |
|------|-------|--------|--------|---------------|
| `01_python_code.md` | *.py, **/*.py | Python style, type hints, async | ~2,200 | ✅ Yes (workflows can reinforce) |
| `02_testing.md` | tests/**/*.py, test_*.py, *_test.py | pytest, TDD, fixtures | ~1,800 | ✅ Yes |
| `03_documentation.md` | docs/**/*.md, *.md | markdown, ADRs, initiatives | ~2,000 | ✅ Yes |
| `04_config_files.md` | pyproject.toml, *.ini, Taskfile.yml, .pre-commit-config.yaml | Config best practices | ~1,500 | ✅ Yes |
| `05_windsurf_structure.md` | .windsurf/**/*.md, .windsurf/**/*.json | Windsurf directory structure | ~1,200 | ✅ Yes |

**Total:** ~8,700 tokens

---

### Model Decision Triggers (10 rules, ~22KB)

**Hybrid usage:** Load automatically when semantically relevant, OR explicitly @mention in workflows

| Rule | Description | Topics | Tokens | Workflow @mentions |
|------|-------------|--------|--------|--------------------|
| `06_security_practices.md` | Apply when dealing with security-sensitive code including API calls user input LLM interactions and authentication | OWASP LLM Top 10, input validation | ~2,500 | `/validate`, `/implement` |
| `07_context_optimization.md` | Apply for context loading batch operations or performance optimization work | Batch ops, parallelization | ~2,500 | `/load-context`, `/work` |
| `08_file_operations.md` | Apply when moving archiving or reorganizing files and updating cross-references | File moves, initiative archival | ~2,000 | `/archive-initiative` |
| `09_git_workflows.md` | Apply for git operations commits branching or version control work | Git, conventional commits | ~1,800 | `/commit` |
| `10_session_protocols.md` | Apply at session end when completing work or managing work transitions | Session end protocol | ~2,000 | `/work-session-protocol` |
| `11_error_handling.md` | Apply when handling errors implementing error recovery or debugging failures | Error patterns, recovery | ~2,200 | `/implement`, `/validate` |
| `12_task_orchestration.md` | Apply when using update_plan creating task lists or orchestrating multi-step workflows | update_plan usage, task attribution | ~3,000 | `/work`, `/plan`, `/implement` |
| `13_workflow_routing.md` | Apply when routing work making workflow decisions or detecting project context | Routing matrix, signals | ~1,800 | `/work`, `/work-routing` |
| `14_automation_scripts.md` | Apply when using automation scripts Taskfile commands or scaffolding operations | Automation scripts, Taskfile | ~3,000 | `/archive-initiative`, `/implement` |
| `15_tool_patterns.md` | Apply when using MCP tools or needing guidance on tool calling patterns | MCP tools, grep/read/edit | ~2,500 | All workflows (frequently needed) |

**Total:** ~22,300 tokens

**Key change:** `14_automation_scripts.md` is now `model_decision` (was manual in v1) - workflows will @mention it when needed

---

### Manual Triggers (0 rules)

**None!** All former "manual" rules are now `model_decision` with @mention capability.

**Rationale:**
- If a rule is useful enough to @mention, it's useful enough for semantic loading
- Manual trigger forces explicit loading every time (friction)
- Hybrid approach gives best of both worlds

---

## Total Structure: 16 Rules

```
00_core_directives.md        (always_on)  ~3KB
01_python_code.md             (glob)       ~2KB
02_testing.md                 (glob)       ~2KB
03_documentation.md           (glob)       ~2KB
04_config_files.md            (glob)       ~2KB
05_windsurf_structure.md      (glob)       ~1KB
06_security_practices.md      (model_decision) ~3KB
07_context_optimization.md    (model_decision) ~3KB
08_file_operations.md         (model_decision) ~2KB
09_git_workflows.md           (model_decision) ~2KB
10_session_protocols.md       (model_decision) ~2KB
11_error_handling.md          (model_decision) ~2KB
12_task_orchestration.md      (model_decision) ~3KB
13_workflow_routing.md        (model_decision) ~2KB
14_automation_scripts.md      (model_decision) ~3KB
15_tool_patterns.md           (model_decision) ~3KB
```

**Total:** ~41KB, ~28,000 tokens (30% reduction from 40K baseline)

---

## Workflow @mention Strategy

### When to @mention

**Workflows should @mention rules when:**
1. Workflow REQUIRES specific rule content (e.g., `/commit` needs git standards)
2. Rule provides decision-making data (e.g., `/work-routing` needs routing matrix)
3. Full context needed upfront (e.g., `/archive-initiative` needs automation commands)

**Format:**

```markdown
## Stage 1: Load Context

**Load required rules:**

- @[06_security_practices.md] - Security guidelines
- @[14_automation_scripts.md] - Automation commands

**Then proceed with...**
```

### Workflow-Rule Mapping

| Workflow | @mention These Rules | Why |
|----------|----------------------|-----|
| `/work` | `12_task_orchestration.md`, `13_workflow_routing.md` | Task format, routing decisions |
| `/plan` | `12_task_orchestration.md` | Task planning |
| `/implement` | `12_task_orchestration.md`, `02_testing.md` (if not auto-loaded) | TDD workflow, task tracking |
| `/validate` | `06_security_practices.md` (reinforce) | Security checklist |
| `/commit` | `09_git_workflows.md` (reinforce) | Git standards, conventional commits |
| `/archive-initiative` | `08_file_operations.md`, `14_automation_scripts.md` | Archival process, automation |
| `/load-context` | `07_context_optimization.md` | Batch loading strategies |
| `/meta-analysis` | `10_session_protocols.md` | Session end requirements |

---

## Content Organization Changes from V1

### Consolidated Content

**`14_automation_scripts.md`** (model_decision, ~3KB):
- **Elevate from:** `.windsurf/docs/automation-scripts.md`
- **Content:** Taskfile commands, scaffolding (non-interactive), archival automation
- **Why model_decision:** Frequently needed, semantic loading works well

**`15_tool_patterns.md`** (model_decision, ~2.5KB):
- **Merge:** `tool-patterns.md`, `common-patterns.md`
- **Content:** MCP tool usage, batch operations (quick ref)
- **Why model_decision:** Tool usage is frequent across all workflows

**`07_context_optimization.md`** (model_decision, ~2.5KB):
- **Merge:** `batch-operations.md` (core patterns), `context-loading-patterns.md`
- **Content:** When to batch, optimal sizes, pattern examples
- **Drop:** Advanced edge cases (not needed in rules)

### Split Content

**`01_python_code.md` + `02_testing.md`** (split from `02_python_standards.md`):
- Testing frequent enough for separate glob trigger
- Reduces tokens loaded when editing non-test Python files

**`12_task_orchestration.md`** (core only, 3KB):
- **Extract from:** `07_task_system.md` (29KB → 3KB)
- **Keep:** update_plan format, attribution, core rules
- **Drop:** Detailed examples (move to inline workflow documentation)

**`06_security_practices.md`** (model_decision, remove globs):
- **Remove:** `globs` field (was incorrectly combined with model_decision)
- **Keep:** OWASP LLM Top 10, security patterns
- **Trigger:** model_decision only

---

## Frontmatter Examples

### Always-On

```yaml
---
trigger: always_on
---
```

### Glob (unquoted, comma-separated)

```yaml
---
trigger: glob
globs: *.py, **/*.py
---
```

### Model Decision (hybrid - auto OR @mention)

```yaml
---
trigger: model_decision
description: Apply when using automation scripts Taskfile commands or scaffolding operations
---
```

---

## Post-Matter Format (All Rules)

```markdown
---

## Rule Metadata

**File:** `14_automation_scripts.md`  
**Trigger:** model_decision  
**Estimated Tokens:** ~3,000  
**Last Updated:** 2025-10-21

**Can be @mentioned:** Yes (hybrid loading)

**Topics:**
- Automation scripts via `task` commands
- Non-interactive scaffolding
- Initiative archival automation
- Validation workflows

**Workflow References:**
- `/archive-initiative` - Always @mentions this rule
- `/implement` - @mentions when scaffolding needed
- `/validate` - @mentions for validation commands

**Dependencies:**
- References: `Taskfile.yml`, `scripts/*.py`
- Related rules: `08_file_operations.md`

**Changelog:**
- 2025-10-21: Changed from manual to model_decision trigger (hybrid approach)
- 2025-10-20: Created from `.windsurf/docs/automation-scripts.md`
```

---

## Token Budget Analysis

### Worst-Case Loading Scenarios

**Scenario 1: Editing Python test file**
```
always_on:        00_core_directives.md         ~3,000
glob (Python):    01_python_code.md             ~2,200
glob (test):      02_testing.md                 ~1,800
                                        TOTAL:  ~7,000 tokens
```

**Scenario 2: Running `/work` workflow**
```
always_on:        00_core_directives.md         ~3,000
@mention:         12_task_orchestration.md      ~3,000
@mention:         13_workflow_routing.md        ~1,800
model_decision:   07_context_optimization.md    ~2,500 (likely loaded)
                                        TOTAL:  ~10,300 tokens
```

**Scenario 3: Security-focused implementation**
```
always_on:        00_core_directives.md         ~3,000
glob:             01_python_code.md             ~2,200
@mention:         06_security_practices.md      ~2,500
@mention:         12_task_orchestration.md      ~3,000
model_decision:   15_tool_patterns.md           ~2,500 (semantic)
                                        TOTAL:  ~13,200 tokens
```

**Max realistic:** ~15,000 tokens loaded simultaneously (well within budget)

---

## Advantages of Hybrid Approach

### ✅ Better Than V1 (Pure Manual)

1. **Automatic loading:** Rules available when semantically relevant (no @mention needed)
2. **Fewer rules:** 16 instead of 18 (no manual-only rules)
3. **Less friction:** Workflows don't need to @mention common rules every time

### ✅ Better Than Pure Model Decision

1. **Guaranteed loading:** Critical rules explicitly loaded in workflows
2. **Full context upfront:** No waiting for model to decide mid-workflow
3. **Deterministic:** Workflow behavior consistent across runs

### ✅ Combined Benefits

- **Graceful degradation:** If model doesn't load rule semantically, @mention ensures it
- **Flexible usage:** User can @mention any rule anytime for reference
- **Optimal token usage:** Only load full context when actually needed

---

## Migration from V1

**Changes:**
- Remove 2 manual rules (consolidated into model_decision)
- Update `14_automation_scripts.md`: manual → model_decision
- Remove `16_task_system_reference.md` (consolidate into workflows)
- Remove `17_batch_optimization.md` (advanced patterns not needed)
- All model_decision rules can be @mentioned (document this)

**Result:** Simpler, more flexible, better semantic loading

---

## Implementation Priority

1. **Create 16 rule files** (not 18)
2. **Update workflows with @mention strategy** (explicit loading where critical)
3. **Test hybrid loading** (verify model_decision + @mention both work)
4. **Document hybrid usage** in rule post-matter

---

**Design Complete - Ready for Implementation**

