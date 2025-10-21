# Windsurf Rules Implementation Plan

**Date:** 2025-10-21  
**Execution:** Single session, complete revamp

---

## Phase 3: Implementation Plan

### 3.1 Pre-Implementation Checklist

**Before starting:**

- [x] Analysis complete (`/tmp/windsurf-rules-analysis.md`)
- [x] Design complete (`/tmp/windsurf-rules-design.md`)
- [ ] Backup current state (DO NOT COMMIT backup)
- [ ] Document all workflow references
- [ ] Verify no active work in progress
- [ ] Clean git state

**Backup command:**

```bash
mkdir -p /tmp/windsurf-backup-2025-10-21
cp -r .windsurf/rules /tmp/windsurf-backup-2025-10-21/
cp -r .windsurf/docs /tmp/windsurf-backup-2025-10-21/
```

---

### 3.2 Implementation Sequence

#### Step 1: Create New Rule Files (18 files)

**Location:** Create in `/tmp/windsurf-rules-new/` first (not in project)

**Process:**

1. **00_core_directives.md** (always_on)
   - Extract from current `00_agent_directives.md`
   - Trim to ~3KB (keep sections 1-4 only)
   - Add post-matter metadata
   - Verify <12KB

2. **01_python_code.md** (glob)
   - Extract from current `02_python_standards.md`
   - Focus: Code style, type hints, async
   - Remove testing content (goes to 02)
   - Globs: `*.py, **/*.py`
   - Target: ~2.2KB

3. **02_testing.md** (glob)
   - Extract from current `01_testing_and_tooling.md` + parts of `02_python_standards.md`
   - Focus: pytest, fixtures, TDD, testing standards
   - Globs: `tests/**/*.py, test_*.py, *_test.py, conftest.py`
   - Target: ~1.8KB

4. **03_documentation.md** (glob)
   - Extract from current `03_documentation_lifecycle.md`
   - Focus: markdown, ADRs, initiatives, doc standards
   - Globs: `docs/**/*.md, *.md, README.md`
   - Target: ~2KB

5. **04_config_files.md** (glob)
   - New rule (consolidate from multiple sources)
   - Content: TOML, YAML, Taskfile patterns
   - Globs: `*.toml, *.ini, *.yml, *.yaml, Taskfile.yml, .pre-commit-config.yaml`
   - Target: ~1.5KB

6. **05_security_practices.md** (model_decision)
   - Extract from current `04_security.md`
   - Remove globs field (model_decision doesn't use globs)
   - Description: "Apply when dealing with security-sensitive code including API calls user input LLM interactions and authentication"
   - Target: ~2.5KB

7. **06_context_optimization.md** (model_decision)
   - Consolidate: `batch-operations.md`, `context-loading-patterns.md`, parts of `tool-patterns.md`
   - Focus: Batch operations, parallel loading, performance
   - Description: "Apply for context loading batch operations or performance optimization work"
   - Target: ~2.5KB

8. **07_file_operations.md** (model_decision)
   - Extract from: Parts of `06_context_engineering.md`, `automation-scripts.md`
   - Focus: File moves, archival, ref updates, directory structure
   - Description: "Apply when moving archiving or reorganizing files and updating cross-references"
   - Target: ~2KB

9. **08_git_workflows.md** (model_decision)
   - Extract from: Parts of `06_context_engineering.md`, `00_agent_directives.md`
   - Focus: Git operations, conventional commits, branching
   - Description: "Apply for git operations commits branching or version control work"
   - Target: ~1.8KB

10. **09_session_protocols.md** (model_decision)
    - Extract from: `05_operational_protocols.md`, parts of `00_agent_directives.md`
    - Focus: Session end protocol, progress communication
    - Description: "Apply at session end when completing work or managing work transitions"
    - Target: ~2KB

11. **10_error_handling.md** (model_decision)
    - Elevate from: `error-handling-patterns.md`
    - Focus: Error patterns, recovery strategies, debugging
    - Description: "Apply when handling errors implementing error recovery or debugging failures"
    - Target: ~2.2KB

12. **11_task_orchestration.md** (model_decision)
    - Trim from: `07_task_system.md` (29KB → 3KB)
    - Keep: Core update_plan usage, attribution, format
    - Description: "Apply when using update_plan creating task lists or orchestrating multi-step workflows"
    - Target: ~3KB

13. **12_workflow_routing.md** (model_decision)
    - Elevate from: `workflow-routing-matrix.md`
    - Focus: Routing decisions, signal detection, confidence levels
    - Description: "Apply when routing work making workflow decisions or detecting project context"
    - Target: ~1.8KB

14. **13_windsurf_structure.md** (glob)
    - Elevate from: `directory-structure.md`
    - Focus: `.windsurf/` structure, frontmatter format, forbidden files
    - Globs: `.windsurf/**/*.md, .windsurf/**/*.json`
    - Target: ~1.2KB

15. **14_automation_reference.md** (manual)
    - Consolidate: `automation-scripts.md`, parts of `01_testing_and_tooling.md`
    - Focus: Taskfile commands, scaffolding, automation scripts
    - Target: ~3.5KB

16. **15_tool_usage_patterns.md** (manual)
    - Consolidate: `tool-patterns.md`, `common-patterns.md`
    - Focus: MCP tool usage, grep/read/edit patterns
    - Target: ~3.8KB

17. **16_task_system_reference.md** (manual)
    - Extract from: `07_task_system.md` (details), `task-system-reference.md`
    - Focus: Detailed format spec, examples, edge cases
    - Target: ~3.5KB

18. **17_batch_optimization.md** (manual)
    - Extract from: `batch-operations.md` (advanced patterns)
    - Focus: Advanced optimization, chunking, rate limiting
    - Target: ~3.2KB

**Verification after each file:**
- [ ] Valid frontmatter (trigger + description/globs as needed)
- [ ] No extra frontmatter fields
- [ ] Globs unquoted (if glob trigger)
- [ ] File size <12KB
- [ ] Post-matter metadata present
- [ ] Content coherent and complete

---

#### Step 2: Regenerate Machine-Readable Docs

**Delete entire `.windsurf/docs/` directory:**

```bash
rm -rf .windsurf/docs/
```

**Regenerate indexes:**

Create only 2 auto-generated files:

1. **`.windsurf/docs/rules-index.md`** - Rule index
2. **`.windsurf/docs/workflow-index.md`** - Workflow index

**Format:**

```markdown
---
type: auto-generated-index
generated: 2025-10-21
maintenance: automated
---

# Rules Index

**Total Rules:** 18

## Always-On Rules (1)

- `00_core_directives.md` - Core agent persona and guiding principles

## Glob Trigger Rules (5)

- `01_python_code.md` (*.py) - Python code style and best practices
- `02_testing.md` (tests/**/*.py) - Testing standards and pytest usage
- `03_documentation.md` (docs/**/*.md) - Documentation standards
- `04_config_files.md` (*.toml, *.yml) - Configuration file best practices
- `13_windsurf_structure.md` (.windsurf/**/*) - Windsurf directory structure

## Model Decision Rules (8)

- `05_security_practices.md` - Security-sensitive code
- `06_context_optimization.md` - Context loading and performance
- `07_file_operations.md` - File moves and archival
- `08_git_workflows.md` - Git operations
- `09_session_protocols.md` - Session end and progress
- `10_error_handling.md` - Error recovery
- `11_task_orchestration.md` - Task system and update_plan
- `12_workflow_routing.md` - Workflow routing decisions

## Manual Rules (4)

- `14_automation_reference.md` - Automation scripts reference
- `15_tool_usage_patterns.md` - MCP tool usage patterns
- `16_task_system_reference.md` - Detailed task system reference
- `17_batch_optimization.md` - Advanced optimization patterns

---

**Last Updated:** 2025-10-21  
**Script:** Auto-generated via workflow
```

**Generation script:**

```python
# scripts/generate_rule_index.py
# Creates .windsurf/docs/rules-index.md from rules frontmatter
```

---

#### Step 3: Update Workflow References

**Search for references:**

```bash
grep -r "\.windsurf/rules/" .windsurf/workflows/
grep -r "\.windsurf/docs/" .windsurf/workflows/
```

**Known references (from grep earlier):**

- `validate.md`: References `04_security.md`
- `meta-analysis.md`: References `00_agent_directives.md`
- `commit.md`: References `00_agent_directives.md`
- `implement.md`: References `01_testing_and_tooling.md`
- `load-context.md`: References `00_agent_directives.md`
- `research.md`: References `04_security.md`, `01_testing_and_tooling.md`

**Update mapping:**

| Old Reference | New Reference |
|---------------|---------------|
| `00_agent_directives.md` | `00_core_directives.md` + `09_session_protocols.md` (depending on section) |
| `01_testing_and_tooling.md` | `02_testing.md` |
| `04_security.md` | `05_security_practices.md` |

**Update strategy:**

1. Replace exact file path references
2. Update section references if sections moved
3. Verify all links resolve

---

#### Step 4: Update Validation and Generation Scripts

**Scripts to update:**

1. **`scripts/validate_workflows.py`**
   - Already updated (schema validation removed)
   - Verify still works with new structure

2. **`scripts/validate_rules_frontmatter.py`**
   - Already updated (minimal format validation)
   - Verify detects all trigger types

3. **`scripts/validate_frontmatter.py`**
   - Update to validate new format
   - Add glob format validation (unquoted)

4. **`scripts/generate_rule_index.py`** (NEW)
   - Create script to generate `rules-index.md`
   - Parse frontmatter from all rules
   - Group by trigger type
   - Output markdown index

5. **Pre-commit hooks** (`.pre-commit-config.yaml`)
   - Update `validate-rules-frontmatter` hook
   - Ensure calls updated script

**Validation checks:**

```python
# Validate glob format
def validate_glob_format(globs_value):
    """Ensure globs are unquoted, comma-separated"""
    if isinstance(globs_value, str):
        # Check no quotes
        if '"' in globs_value or "'" in globs_value:
            return False, "Globs must not have quotes"
        # Check comma-separated
        if ',' in globs_value or len(globs_value.split()) > 1:
            return True, "Valid"
    return False, "Invalid globs format"
```

---

#### Step 5: Atomic Cutover

**Single commit, all changes:**

```bash
# From /tmp/windsurf-rules-new/ to .windsurf/rules/
rm -rf .windsurf/rules/*
cp /tmp/windsurf-rules-new/*.md .windsurf/rules/

# Remove old docs directory
rm -rf .windsurf/docs/

# Create new minimal docs
mkdir -p .windsurf/docs/
python scripts/generate_rule_index.py

# Stage all changes
git add .windsurf/

# Review changes
git diff --cached --stat

# Commit
git commit -m "refactor(windsurf): comprehensive rules revamp for Windsurf compatibility

BREAKING CHANGE: Complete restructuring of rules and docs system

Problem:
- Rules had non-standard frontmatter preventing Windsurf loading
- Globs formatted incorrectly (quoted instead of unquoted)
- 04_security.md had model_decision + globs (mutually exclusive)
- 00_agent_directives.md exceeded 12KB limit (12,867 bytes)
- 07_task_system.md far exceeded limit (29,056 bytes)
- 15 separate docs files should be rules or consolidated

Solution:
- Migrated to strict Windsurf frontmatter specification
- Fixed glob format (unquoted, comma-separated)
- Consolidated 8 rules + 15 docs → 18 optimized rules
- All rules now <12KB (within Windsurf limit)
- Metadata preserved in post-matter sections

Changes:
- Restructured: 18 new rule files (1 always_on, 5 glob, 8 model_decision, 4 manual)
- Removed: .windsurf/docs/ directory (elevated to rules or regenerated)
- Updated: Workflow references to new rule filenames
- Updated: Validation scripts for new format
- Added: scripts/generate_rule_index.py for auto-generation

New Structure:
- 00_core_directives.md (always_on) - Core persona, trimmed to 3KB
- 01_python_code.md (glob) - Python code standards
- 02_testing.md (glob) - Testing standards
- 03_documentation.md (glob) - Documentation standards
- 04_config_files.md (glob) - Config file best practices
- 05_security_practices.md (model_decision) - Security guidelines
- 06_context_optimization.md (model_decision) - Performance patterns
- 07_file_operations.md (model_decision) - File operations
- 08_git_workflows.md (model_decision) - Git best practices
- 09_session_protocols.md (model_decision) - Session end protocol
- 10_error_handling.md (model_decision) - Error recovery
- 11_task_orchestration.md (model_decision) - Task system core
- 12_workflow_routing.md (model_decision) - Routing decisions
- 13_windsurf_structure.md (glob) - Windsurf directory structure
- 14_automation_reference.md (manual) - Automation scripts
- 15_tool_usage_patterns.md (manual) - MCP tool patterns
- 16_task_system_reference.md (manual) - Task system reference
- 17_batch_optimization.md (manual) - Advanced optimization

Validation:
- All rules pass scripts/validate_rules_frontmatter.py
- All rules <12KB (Windsurf limit)
- All globs correctly formatted (unquoted)
- All workflow references updated and verified
- Metadata preserved in post-matter sections

Token Budget:
- Before: ~40,000 tokens (8 rules + 15 docs)
- After: ~30,000 tokens (18 rules)
- Optimization: 25% reduction

References:
- https://docs.windsurf.com/windsurf/cascade/memories
- Verified Windsurf specification (2025-10-21)
- User directive: Comprehensive rules revamp"
```

---

### 3.3 Validation Checklist

**After cutover, verify:**

- [ ] All 18 rule files exist
- [ ] All rules have valid frontmatter
- [ ] All rules <12KB
- [ ] No quoted globs in glob trigger rules
- [ ] No globs in model_decision rules
- [ ] Post-matter metadata present in all rules
- [ ] Workflow references updated
- [ ] `scripts/validate_rules_frontmatter.py` passes
- [ ] `scripts/validate_workflows.py` passes
- [ ] Git status clean after commit
- [ ] No `.windsurf/docs/` directory remains (except regenerated indexes)

**Validation commands:**

```bash
# Count rules
ls -1 .windsurf/rules/*.md | wc -l  # Should be 18

# Check sizes
for f in .windsurf/rules/*.md; do 
  size=$(wc -c <"$f")
  if [ $size -gt 12000 ]; then
    echo "❌ $f exceeds 12KB: $size bytes"
  fi
done

# Validate frontmatter
python scripts/validate_rules_frontmatter.py

# Validate workflows
python scripts/validate_workflows.py

# Check for quoted globs
grep -n 'globs:.*"' .windsurf/rules/*.md  # Should be empty

# Check model_decision rules don't have globs
for f in .windsurf/rules/*.md; do
  if grep -q "^trigger: model_decision" "$f" && grep -q "^globs:" "$f"; then
    echo "❌ $f has model_decision + globs (mutually exclusive)"
  fi
done
```

---

## Phase 4: Testing Protocol

### 4.1 Syntax Testing

**Goal:** Verify Windsurf parses all rules without errors

**Process:**

1. Start Windsurf IDE
2. Open Cascade
3. Check for frontmatter errors in logs
4. Verify rules load indicator (check settings)

**Expected:** No parsing errors, all rules recognized

---

### 4.2 Trigger Testing

**Goal:** Verify each trigger type works as expected

#### Test Always-On

1. Start new Cascade session
2. Verify `00_core_directives.md` is loaded automatically
3. Check response reflects core directives

**Command to test:**
```
What are your guiding principles?
```

**Expected:** Response cites principles from `00_core_directives.md`

#### Test Glob Triggers

1. Create/edit a Python file: `touch test_file.py`
2. Verify `01_python_code.md` and `02_testing.md` load
3. Ask Python-specific question

**Command to test:**
```
What are the type hinting standards?
```

**Expected:** Response cites `01_python_code.md`

#### Test Model Decision

1. Ask security question
2. Verify `05_security_practices.md` loads

**Command to test:**
```
How should I validate user input?
```

**Expected:** Response cites `05_security_practices.md` (OWASP guidelines)

#### Test Manual

1. Mention rule explicitly
2. Verify rule loads only when mentioned

**Command to test:**
```
Load @[14_automation_reference.md] and tell me how to archive an initiative
```

**Expected:** Response cites automation commands

---

### 4.3 Workflow Integration Testing

**Goal:** Verify workflows still function with new rules

**Test workflows:**

1. `/work` - Workflow orchestration
2. `/plan` - Planning workflow
3. `/implement` - Implementation workflow
4. `/validate` - Validation workflow

**Process:**

1. Run each workflow
2. Verify rules load correctly
3. Check for broken references
4. Verify task system works (`update_plan`)

**Expected:** All workflows execute without errors

---

### 4.4 Performance Testing

**Goal:** Verify token usage optimized

**Measure:**

1. Token count when editing Python file
2. Token count when running `/work`
3. Token count when running `/validate`

**Expected:**
- Python editing: ≤6KB loaded (01, 02, maybe 00)
- `/work` execution: ≤12KB loaded (00, 11, 12, 09)
- Overall: ≤30% reduction from baseline

**Baseline:** ~40,000 tokens total  
**Target:** ~30,000 tokens total

---

## Implementation Timeline

**Estimated time:** 6-8 hours (single session)

| Phase | Task | Time | Status |
|-------|------|------|--------|
| Prep | Backup, document references | 30 min | Pending |
| Step 1 | Create 18 new rule files | 3-4 hours | Pending |
| Step 2 | Regenerate docs indexes | 30 min | Pending |
| Step 3 | Update workflow references | 1 hour | Pending |
| Step 4 | Update validation scripts | 1 hour | Pending |
| Step 5 | Atomic cutover (commit) | 30 min | Pending |
| Testing | Syntax, triggers, workflows | 1 hour | Pending |
| **Total** | **Complete revamp** | **6-8 hours** | **Pending** |

---

## Rollback Plan

**If issues discovered:**

```bash
# Restore from backup
rm -rf .windsurf/rules/
rm -rf .windsurf/docs/
cp -r /tmp/windsurf-backup-2025-10-21/rules .windsurf/
cp -r /tmp/windsurf-backup-2025-10-21/docs .windsurf/

# Revert commit
git revert HEAD

# Investigate issues
```

**Note:** Keep backup until thoroughly tested (do not commit backup)

---

## Success Criteria Checklist

- [ ] All 18 rules created and pass validation
- [ ] All rules <12KB (Windsurf limit)
- [ ] All frontmatter Windsurf-compliant
- [ ] Globs correctly formatted (unquoted)
- [ ] Metadata preserved in post-matter
- [ ] Workflow references updated
- [ ] Validation scripts updated
- [ ] All rules load in Windsurf without errors
- [ ] Trigger types work as expected (always_on, glob, model_decision, manual)
- [ ] Workflows function correctly
- [ ] Token usage reduced by ≥20%
- [ ] Documentation updated
- [ ] Single atomic commit
- [ ] Backup retained (not committed)

---

**Implementation Plan Complete**  
**Next:** Execute implementation

