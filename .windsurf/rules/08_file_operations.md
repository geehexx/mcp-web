---
trigger: model_decision
description: Apply when moving archiving or reorganizing files
---

# File Operations and Archival

**Purpose:** Guidance for file operations, initiative structure, and archival procedures.

**Note:** For `.windsurf/` file editing, see `05_windsurf_structure.md` for MCP tool requirements.

---

## 1.1 Initiative Structure Decision Tree

**Use scaffolding system when creating new initiatives:** `task scaffold:initiative`

### Decision: Flat File vs Folder Structure

```text
Does initiative meet ANY of these criteria?
├─ Word count > 1000?
├─ Multiple phases (2+)?
├─ Needs research artifacts?
├─ Complex enough for sub-documents?
│
├── YES → Use FOLDER structure
│   ├─ Create: docs/initiatives/active/YYYY-MM-DD-name/
│   ├─ Files: initiative.md, phases/, artifacts/
│   └─ Use: task scaffold:initiative --folder
│
└── NO → Use FLAT file
    ├─ Create: docs/initiatives/active/YYYY-MM-DD-name.md
    └─ Use: task scaffold:initiative --flat
```

**Examples:**

| Initiative | Structure | Reason |
|------------|-----------|--------|
| "Add robots.txt support" | Flat | Simple, 1 phase, <500 words |
| "Performance Optimization Pipeline" | Folder | Multiple phases, research needed |
| "Workflow Architecture V3" | Folder | Complex, multiple ADRs, artifacts |
| "Fix typo in README" | None | Too trivial for initiative |

**NEVER create both** - this violates ADR-0013.

### 1.2 Artifact Management

**Artifacts belong in initiative folders:**

```text
docs/initiatives/active/YYYY-MM-DD-name/
├── initiative.md          # Main document
├── phases/
│   ├── phase-1-*.md
│   └── phase-2-*.md
└── artifacts/             # Supporting documents
    ├── research-summary.md  # Research findings
    ├── analysis.md          # Problem analysis
    ├── implementation-plan.md
    └── PROPOSAL-*.md        # Decision proposals
```

**Artifact Types:**

1. **Research summaries:** `research-summary.md` - External research with sources
2. **Analysis documents:** `analysis.md` - Root cause analysis, problem decomposition
3. **Implementation plans:** `implementation-plan.md` - Detailed execution steps
4. **Proposals:** `PROPOSAL-*.md` - Design proposals needing decision
5. **Technical designs:** `technical-design.md` - Detailed technical specifications

**When to create artifacts:**

- Research phase produces findings → `artifacts/research-summary.md`
- Complex problem needs analysis → `artifacts/analysis.md`
- Multiple implementation options → `artifacts/PROPOSAL-*.md`
- Detailed specs needed → `artifacts/technical-design.md`

**Artifact Lifecycle:**

1. **Created:** During initiative work (research, analysis, planning)
2. **Referenced:** From `initiative.md` with relative links
3. **Archived:** Moved with initiative to `docs/initiatives/completed/`
4. **Never standalone:** Always part of initiative folder

---

## 1.3 Initiative Archival

**Use automation:** Always use `task archive:initiative NAME=<name>` for archival

**Process:**

1. Verify completion gates
2. Run archival script
3. Update references
4. Commit changes

**See:** Automation scripts for detailed commands

---

## Rule Metadata

**File:** `08_file_operations.md`
**Trigger:** model_decision
**Estimated Tokens:** ~1,500
**Last Updated:** 2025-10-21
**Status:** Active

**Can be @mentioned:** Yes (hybrid loading)

**Topics Covered:**

- Initiative structure decision (flat vs folder)
- Artifact management
- Initiative archival
- File organization

**Workflow References:**

- /archive-initiative - Initiative archival
- /implement - File reorganization

**Dependencies:**

- Related: 05_windsurf_structure.md (for .windsurf/ file tool selection)
- Source: 06_context_engineering.md (File Operations section)

**Changelog:**

- 2025-10-21: Created from 06_context_engineering.md
- 2025-10-21: Moved MCP tool selection to 05_windsurf_structure.md, changed trigger to model_decision
