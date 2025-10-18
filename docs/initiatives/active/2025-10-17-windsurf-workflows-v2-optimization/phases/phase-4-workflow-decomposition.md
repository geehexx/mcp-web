# Phase 4: Workflow Decomposition

**Status:** ⏳ Planned
**Priority:** HIGH
**Duration:** 6-10 hours
**Owner:** AI Agent

---

## Objective

Break complex workflows into modular sub-workflows to reduce complexity and improve maintainability.

**Target:** All files <4,000 tokens, complexity <75/100

---

## Problem Statement

Three files exceed complexity thresholds:

| File | Current Size | Complexity | Target |
|------|--------------|------------|--------|
| `work.md` | 2,629 tokens | 82/100 | <60/100 |
| `consolidate-summaries.md` | 5,501 tokens | 80/100 | <70/100 |
| `00_agent_directives.md` | 5,387 tokens | 85/100 | <70/100 |

**Issues:**

- Complex state management
- Repetitive patterns within files
- High cognitive load for readers
- Difficult to maintain

---

## Tasks

### Task 4.1: Decompose `work.md` (Complexity: 82/100)

**Current Issues:**

- 10,519 bytes (2,629 tokens)
- Complex orchestration logic
- Multi-stage state management
- Confidence-based decision trees
- Session end protocol embedded

**Root Cause:** Too many responsibilities in one file

**Proposed Structure:**

```text
work.md (core orchestrator)
├── work-routing.md (confidence-based routing logic)
└── work-session-protocol.md (session end protocol)

Note: work-context-detection.md already exists as detect-context.md
```

**File Breakdown:**

1. **`work.md` (core orchestrator, ~1,500 tokens)**
   - Stage 1: Create initial task plan
   - Stage 2: Call `/detect-context` workflow
   - Stage 3: Route to appropriate workflow (reference `work-routing.md`)
   - Stage 4: Execute routed workflow
   - Stage 5: Detect completion (reference `work-session-protocol.md`)

2. **`work-routing.md` (decision logic, ~800 tokens)**
   - High confidence routing (80%+ → auto-proceed)
   - Medium confidence routing (30-79% → proceed with notice)
   - Low confidence routing (<30% → prompt user)
   - Routing table (context → workflow mappings)

3. **`work-session-protocol.md` (end protocol, ~400 tokens)**
   - Trigger detection
   - Commit changes step
   - Archive initiatives step
   - Meta-analysis step
   - Validation checklist

**Implementation Steps:**

1. Create `work-routing.md`:

   ```bash
   # Extract routing logic from work.md Stage 3
   # Include confidence thresholds
   # Include routing decision table
   ```

2. Create `work-session-protocol.md`:

   ```bash
   # Extract session end protocol from work.md Stage 5
   # Include trigger conditions
   # Include step-by-step checklist
   ```

3. Update `work.md`:

   ```markdown
   ## Stage 3: Route to Appropriate Workflow

   See [Routing Decision Logic](./work-routing.md) for detailed routing rules.

   [Brief summary of routing process]

   ## Stage 5: Detect Work Completion and Execute Session End Protocol

   See [Session End Protocol](./work-session-protocol.md) for detailed steps.

   [Brief summary of when protocol triggers]
   ```

4. Update cross-references:

   ```bash
   # Find all references to work.md routing
   grep -r "work.md.*Stage 3" .windsurf/

   # Update to reference work-routing.md where appropriate
   ```

**Effort:** 3-4 hours

**Expected Outcome:**

- `work.md`: 2,629 → ~1,500 tokens (43% reduction)
- Complexity: 82/100 → <60/100
- Improved readability and maintainability

---

### Task 4.2: Decompose `consolidate-summaries.md` (Complexity: 80/100)

**Current Issues:**

- 22,005 bytes (5,501 tokens) - LARGEST file
- Six context loading scopes with repetitive patterns
- Complex batch operation logic
- Redundant explanations across scopes

**Root Cause:** Repetitive patterns not extracted to shared components

**Proposed Structure:**

```text
consolidate-summaries.md (orchestrator)
├── context-loading-patterns.md (shared loading patterns)
└── batch-operations.md (optimization strategies)
```

**File Breakdown:**

1. **`consolidate-summaries.md` (orchestrator, ~2,000 tokens)**
   - Overview and purpose
   - Stage 1: Select consolidation scope
   - Stage 2-7: Apply scope-specific consolidation (reference patterns)
   - Stage 8: Validation
   - Brief examples per scope

2. **`context-loading-patterns.md` (shared patterns, ~1,000 tokens)**
   - Batch reading pattern
   - Priority-based loading
   - Incremental loading
   - Error handling
   - Performance tips
   - Example implementations

3. **`batch-operations.md` (optimization strategies, ~800 tokens)**
   - Parallel operations
   - Chunking strategies
   - Memory management
   - Rate limiting
   - Caching strategies

**Pattern Extraction Example:**

```markdown
# BEFORE (in consolidate-summaries.md, repeated 6 times):

## Stage 2: Daily Scope

**Load session summaries:**
[bash]
batch_read([
  "docs/archive/session-summaries/2025-10-*.md"
])
[/bash]

Process in batches of 10-15 for optimal performance...

## Stage 3: Weekly Scope

**Load session summaries:**
[bash]
batch_read([
  "docs/archive/session-summaries/2025-W*.md"
])
[/bash]

Process in batches of 10-15 for optimal performance...

# AFTER (in consolidate-summaries.md):

## Stage 2: Daily Scope

Load session summaries using [Batch Reading Pattern](./context-loading-patterns.md#batch-reading).

Target: `docs/archive/session-summaries/2025-10-*.md`

## Stage 3: Weekly Scope

Load session summaries using [Batch Reading Pattern](./context-loading-patterns.md#batch-reading).

Target: `docs/archive/session-summaries/2025-W*.md`

# NEW (in context-loading-patterns.md):

## Batch Reading Pattern

**Purpose:** Load multiple files efficiently in parallel

**Implementation:**
[bash]
batch_read([
  "pattern/*.md"
])
[/bash]

**Best Practices:**
- Process in batches of 10-15 files
- Use parallel operations (3-10x faster)
- Handle errors gracefully
- See [Batch Operations](./batch-operations.md) for optimization details
```

**Implementation Steps:**

1. Create `context-loading-patterns.md`:
   - Extract shared loading patterns from all 6 scopes
   - Add batch reading pattern
   - Add incremental loading pattern
   - Add error handling pattern

2. Create `batch-operations.md`:
   - Extract optimization strategies
   - Add parallel operation examples
   - Add chunking strategies
   - Add performance benchmarks

3. Update `consolidate-summaries.md`:
   - Keep scope-specific logic
   - Reference patterns instead of duplicating
   - Simplify explanations
   - Remove redundant examples

4. Check if `load-context.md` should also reference these patterns:

   ```bash
   # Review load-context.md
   # Consider referencing context-loading-patterns.md
   ```

**Effort:** 3-4 hours

**Expected Outcome:**

- `consolidate-summaries.md`: 5,501 → ~2,000 tokens (64% reduction)
- Complexity: 80/100 → <70/100
- Reusable patterns benefit other workflows

---

### Task 4.3: Review `00_agent_directives.md` (Complexity: 85/100)

**Current Issues:**

- 21,549 bytes (5,387 tokens) - Largest rule file
- 12 major sections covering diverse topics
- High maintenance burden
- Mixing core principles with operational procedures

**Root Cause:** Single file contains multiple concerns

**Proposed Structure:**

```text
00_agent_directives.md (core principles)
├── 05_operational_protocols.md (new - session protocol, task system)
└── 06_context_engineering.md (new - file ops, git ops, efficiency)
```

**Note:** Renamed to avoid numbering conflicts with existing:

- 01_testing_and_tooling.md
- 02_python_standards.md
- 03_documentation_lifecycle.md
- 04_security.md

**File Breakdown:**

1. **`00_agent_directives.md` (core principles, ~2,500 tokens)**
   - Section 1.1: Persona
   - Section 1.2: Guiding Principles (North Stars)
   - Section 1.3: Operational Mandate
   - Section 1.4: Tool Selection
   - Section 1.5: Research and References
   - Section 1.11: Task System Usage (keep - frequently referenced)
   - Reference index to other rule files

2. **`05_operational_protocols.md` (new, ~1,500 tokens)**
   - Session End Protocol (from Section 1.8)
   - Progress Communication Strategy (from Section 1.9)
   - Operational Efficiency Principles (from Section 1.10)
   - When to pause and ask for direction
   - Completion criteria

3. **`06_context_engineering.md` (new, ~1,200 tokens)**
   - File Operations (from Section 1.6)
     - Tool selection (MCP vs standard)
     - Initiative structure decision tree
     - Artifact management
   - Git Operations (from Section 1.7)
     - MCP git tools (after removing mcp2_git references)
     - Commit conventions
     - Status checks

**Implementation Steps:**

1. Create `05_operational_protocols.md`:

   ```bash
   # Extract sections 1.8, 1.9, 1.10 from 00_agent_directives.md
   # Add clear headers and navigation
   # Include when to apply (frontmatter in Phase 5)
   ```

2. Create `06_context_engineering.md`:

   ```bash
   # Extract sections 1.6, 1.7 from 00_agent_directives.md
   # Add tool selection decision trees
   # Add visual examples
   ```

3. Update `00_agent_directives.md`:

   ```markdown
   ## 1.8 Session End Protocol

   See [Operational Protocols](./05_operational_protocols.md#session-end-protocol) for detailed protocol.

   **Summary:** [2-3 sentence summary of when to trigger]

   ## 1.6 File Operations

   See [Context Engineering](./06_context_engineering.md#file-operations) for detailed guidelines.

   **Summary:** [2-3 sentence summary of key principles]
   ```

4. Add reference index at top:

   ```markdown
   # Rule: Agent Persona & Directives

   ## Quick Navigation

   **Core Principles:** (this file)
   - Persona, North Stars, Mandate, Tools

   **Operational Protocols:** [05_operational_protocols.md]
   - Session end, progress communication, efficiency

   **Context Engineering:** [06_context_engineering.md]
   - File operations, git operations

   **Specialized Rules:**
   - Testing: [01_testing_and_tooling.md]
   - Python: [02_python_standards.md]
   - Documentation: [03_documentation_lifecycle.md]
   - Security: [04_security.md]
   ```

**Effort:** 2-3 hours

**Expected Outcome:**

- `00_agent_directives.md`: 5,387 → ~2,500 tokens (54% reduction)
- Complexity: 85/100 → <70/100
- Clearer separation of concerns
- Easier to maintain and update

---

## Success Criteria

### Quantitative Metrics

- ✅ All files <4,000 tokens (currently 3 files exceed)
- ✅ All files complexity <75/100 (currently 3 files exceed)
- ✅ Total file count: +5 files (3 workflows + 2 rules)
- ✅ Net token reduction: ~2,000-3,000 tokens (after adding new files)

### Qualitative Metrics

- ✅ Improved readability (single responsibility per file)
- ✅ Better maintainability (changes localized to relevant file)
- ✅ Easier navigation (clear file names, reference links)
- ✅ Reusable patterns (extracted components benefit multiple workflows)

---

## Validation Steps

1. **Complexity Check:**

   ```bash
   # Run complexity calculation for all modified files
   python scripts/calculate_complexity.py .windsurf/

   # Expected: All files <75/100
   ```

2. **Token Count Verification:**

   ```bash
   # Check each decomposed file
   wc -c .windsurf/workflows/work.md
   wc -c .windsurf/workflows/consolidate-summaries.md
   wc -c .windsurf/rules/00_agent_directives.md

   # All should be <16,000 bytes (~4,000 tokens)
   ```

3. **Cross-Reference Check:**

   ```bash
   # Verify all internal links work
   python scripts/validate_workflows.py --check-links
   ```

4. **Manual Testing:**
   - Execute `/work` workflow (verify routing works)
   - Execute session end protocol (verify steps clear)
   - Load context using new patterns (verify efficiency)

---

## Deliverables

### New Files Created

- ✅ `.windsurf/workflows/work-routing.md` - Routing decision logic
- ✅ `.windsurf/workflows/work-session-protocol.md` - Session end protocol
- ✅ `.windsurf/workflows/context-loading-patterns.md` - Shared loading patterns
- ✅ `.windsurf/workflows/batch-operations.md` - Optimization strategies
- ✅ `.windsurf/rules/05_operational_protocols.md` - Operational procedures
- ✅ `.windsurf/rules/06_context_engineering.md` - Context management

### Files Modified

- ✅ `.windsurf/workflows/work.md` - Simplified to core orchestration
- ✅ `.windsurf/workflows/consolidate-summaries.md` - References patterns
- ✅ `.windsurf/workflows/load-context.md` - May reference patterns
- ✅ `.windsurf/rules/00_agent_directives.md` - Core principles only

### Documentation

- ✅ Decomposition rationale document
- ✅ Migration guide for users (Phase 7)
- ✅ Cross-reference map (file dependencies)

---

## Dependencies

**Requires:**

- Phase 3 complete (token optimization done first makes decomposition easier)

**Enables:**

- Phase 5: YAML Frontmatter (cleaner file structure)
- Phase 6: Automation (smaller files easier to process)
- Phase 8: Quality Automation (complexity monitoring validated)

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Breaking cross-references | HIGH | Comprehensive link validation |
| User confusion (more files) | MEDIUM | Clear navigation, reference index |
| Over-decomposition | LOW | Follow single responsibility principle |
| Maintenance overhead | LOW | Shared patterns reduce total maintenance |

---

## Completion Notes

**Phase 4 Status:** ⏳ Planned, ready after Phase 3

**Next Phase:** Phase 5 (YAML Frontmatter) - Add structured metadata

**Estimated Timeline:** Week of 2025-10-21 (6-10 hours)
