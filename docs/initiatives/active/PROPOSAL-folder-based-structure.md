# Proposal: Folder-Based Initiative Structure

**Date:** 2025-10-18
**Status:** Proposed
**Problem:** Artifacts being confused with initiatives, no support for phased documentation

---

## Problem Statement

**Current Issues:**

1. **Artifact Confusion:** `2025-10-18-workflow-audit.md` is a research artifact, not an initiative
2. **Flat Structure:** Large initiatives stuck in single files (e.g., 2,265-word audit document)
3. **No Artifact Support:** No place for research, diagrams, analysis documents
4. **Scalability:** Can't split multi-phase initiatives into manageable documents

**Real-World Example:**

```
workflow-architecture-refactor (the initiative)
├── Created workflow-audit.md (the artifact)
└── But audit was placed in initiatives/active/ and treated as initiative
```

---

## Proposed Solution: Folder-Based Structure

### Structure Overview

```text
docs/initiatives/
├── README.md
├── template/                        # Template for new initiatives
│   ├── initiative.md                # Main initiative document (required)
│   ├── phases/                      # Optional: phase-specific docs
│   │   ├── phase-1-planning.md
│   │   └── phase-2-execution.md
│   └── artifacts/                   # Optional: supporting artifacts
│       ├── research/
│       ├── analysis/
│       └── diagrams/
│
├── active/                          # In-progress initiatives
│   ├── 2025-q4-quality-foundation/
│   │   ├── initiative.md           # Main document (required)
│   │   ├── phases/
│   │   │   ├── phase-1-structure.md
│   │   │   ├── phase-2-linting.md
│   │   │   └── phase-3-testing.md
│   │   └── artifacts/
│   │       ├── test-coverage-analysis.md
│   │       └── linting-research.md
│   │
│   ├── 2025-10-18-workflow-architecture/
│   │   ├── initiative.md           # Core plan
│   │   ├── phases/
│   │   │   ├── phase-1-audit.md
│   │   │   ├── phase-2-refactor.md
│   │   │   └── phase-3-validation.md
│   │   └── artifacts/
│   │       ├── workflow-audit.md   # The 2,265-word analysis
│   │       ├── semantic-overlap-matrix.md
│   │       └── taxonomy-validation.md
│   │
│   └── simple-initiative.md        # Small initiatives can remain flat files
│
└── completed/                       # Finished initiatives
    ├── 2025-10-16-convert-decisions/
    │   ├── initiative.md
    │   └── artifacts/
    │       └── conversion-checklist.md
    └── simple-completed.md          # Small initiatives remain flat
```

---

## Design Principles

### 1. **Flexibility: Folder OR File**

- **Small initiatives (<1000 words, single phase):** Remain as `.md` files
- **Large initiatives (>1000 words, multi-phase):** Use folder structure

**Decision Rule:**

```
IF initiative has:
   - Multiple phases (>1) OR
   - Supporting artifacts (research, analysis, diagrams) OR
   - >1000 words in main document
THEN use folder structure
ELSE use flat file
```

### 2. **Required vs Optional Structure**

**Required (in folder-based):**

- `initiative.md` - Main initiative document (follows template)

**Optional (in folder-based):**

- `phases/` - Phase-specific documentation
- `artifacts/` - Supporting documents
  - `research/` - Research findings
  - `analysis/` - Analysis documents
  - `diagrams/` - Visual artifacts

### 3. **Naming Conventions**

**Folders:**

```
YYYY-MM-DD-brief-name/    # Date-based
YYYY-qN-brief-name/       # Quarter-based
```

**Files:**

```
initiative.md             # Main document (required in folders)
phase-N-name.md          # Phase documents
artifact-name.md         # Artifact documents
```

### 4. **Backward Compatibility**

- **Existing flat files:** Can remain as-is (no forced migration)
- **New initiatives:** Can choose flat or folder based on complexity
- **ls-lint:** Must support both patterns

---

## Migration Strategy

### Phase 1: Immediate (This Session)

1. **Fix Current Misclassification:**
   - Move `workflow-audit.md` to proper location as artifact
   - Create `2025-10-18-workflow-architecture/` folder structure
   - Migrate workflow-architecture-refactor initiative

2. **Update Documentation:**
   - Update ADR-0013 (Initiative Documentation Standards)
   - Update `initiatives/README.md` with new structure
   - Create `template/` folder with examples

3. **Update ls-lint:**
   - Support folder-based structure
   - Allow both flat files and folders

### Phase 2: Gradual Migration (As Needed)

- Migrate large initiatives to folder structure when updated
- Leave small initiatives as flat files
- New large initiatives use folder structure from start

### Phase 3: Validation (Ongoing)

- Document which initiatives are folder-based vs flat
- Track artifact organization
- Ensure consistency

---

## Benefits

### 1. **Clarity**

✅ Clear distinction: initiatives vs artifacts
✅ Research documents properly categorized
✅ No confusion about what's a plan vs analysis

### 2. **Scalability**

✅ Large initiatives split across manageable documents
✅ Phases can be worked on independently
✅ Artifacts organized by type

### 3. **Industry Alignment**

✅ Follows PM best practices (artifact lifecycle organization)
✅ Similar to monorepo package structure
✅ Matches ADR folder-based approaches

### 4. **Maintainability**

✅ Easier to find specific information
✅ Phases can be archived independently
✅ Artifacts can be referenced from multiple initiatives

---

## Comparison: Before vs After

### Before (Flat Structure)

```
initiatives/active/
├── 2025-q4-quality-foundation.md     # 3,000 words, 5 phases
├── 2025-10-18-workflow-audit.md      # ❌ ARTIFACT, not initiative!
└── workflow-architecture-refactor.md # 4,000 words, 3 phases

Problems:
- Audit mistaken for initiative
- Large docs hard to navigate
- No place for supporting artifacts
- Can't split phases
```

### After (Hybrid Structure)

```
initiatives/active/
├── 2025-q4-quality-foundation/       # Folder (large, multi-phase)
│   ├── initiative.md                 # 800 words (core plan)
│   ├── phases/
│   │   ├── phase-1-structure.md
│   │   ├── phase-2-linting.md
│   │   └── phase-3-testing.md
│   └── artifacts/
│       └── coverage-analysis.md
│
├── 2025-10-18-workflow-architecture/
│   ├── initiative.md                 # 600 words (core plan)
│   ├── phases/
│   │   ├── phase-1-audit.md
│   │   └── phase-2-refactor.md
│   └── artifacts/
│       └── workflow-audit.md         # ✅ PROPERLY CLASSIFIED!
│
└── 2025-10-16-simple-fix.md         # Flat file (small, single-phase)

Benefits:
- Clear artifact vs initiative distinction
- Manageable document sizes
- Organized supporting materials
- Flexible: folders for complex, files for simple
```

---

## ls-lint Rules Update

```yaml
docs/initiatives/active:
  # Allow both flat files and folders
  .md: regex:(\d{4}-\d{2}-\d{2}|\d{4}-q[1-4])-[a-z0-9-]+  # Flat files
  .dir: regex:(\d{4}-\d{2}-\d{2}|\d{4}-q[1-4])-[a-z0-9-]+ # Folders

docs/initiatives/active/*:
  # Inside initiative folders
  .md: regex:initiative|phase-\d+-[a-z0-9-]+|[a-z0-9-]+  # initiative.md, phase files, artifacts
  .dir: regex:phases|artifacts|research|analysis|diagrams

docs/initiatives/completed:
  # Same rules for completed
  .md: regex:(\d{4}-\d{2}-\d{2}|\d{4}-q[1-4])-[a-z0-9-]+
  .dir: regex:(\d{4}-\d{2}-\d{2}|\d{4}-q[1-4])-[a-z0-9-]+
```

---

## ADR-0013 Update Required

**Current ADR-0013:** Only specifies flat file structure

**Needed Updates:**

1. Add folder-based structure specification
2. Define when to use folder vs file
3. Update template to support both
4. Add artifact organization guidelines
5. Define phase documentation standards

---

## Implementation Checklist

### Immediate Actions

- [ ] Create `docs/initiatives/template/` folder with examples
- [ ] Migrate `workflow-audit.md` to proper artifact location
- [ ] Create `2025-10-18-workflow-architecture/` folder structure
- [ ] Update `initiatives/README.md` with new structure guide
- [ ] Update ls-lint rules to support folders
- [ ] Update ADR-0013 with folder-based standards

### Validation

- [ ] ls-lint passes with new rules
- [ ] All cross-references updated
- [ ] Documentation structure correct
- [ ] Examples provided in template

---

## Open Questions

1. **Archive strategy:** When archiving folder-based initiatives, archive entire folder?
   - **Answer:** Yes, move entire folder to `completed/`

2. **Artifact reuse:** Can artifacts be shared between initiatives?
   - **Answer:** For now, no. Keep artifacts within initiative folder. Consider symlinks if needed.

3. **Phase completion:** How to mark phases as complete?
   - **Answer:** Use checkboxes in main `initiative.md`, reference phase docs

4. **Backwards compatibility:** Migrate existing flat files?
   - **Answer:** No forced migration. Migrate when updated or when they grow large.

---

## Decision

**Recommendation:** ADOPT folder-based structure with hybrid approach

**Rationale:**

- Solves current artifact confusion
- Scales to large initiatives
- Follows industry best practices
- Maintains backward compatibility
- Low migration cost (gradual)

**Next Steps:**

1. Implement immediate actions
2. Create ADR documenting this decision
3. Update all related documentation
4. Migrate workflow-audit as proof-of-concept

---

**Author:** AI Agent (Cascade)
**Review Status:** Awaiting approval
**Impact:** Medium (documentation structure change)
