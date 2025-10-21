---
trigger: glob
description: Apply when editing .windsurf/ files or moving archiving reorganizing files
globs: .windsurf/**/*.md, .windsurf/**/*.json
---

# File Operations and Archival

## 1.1 Tool Selection

**Protected directories (.windsurf/):** ALWAYS use MCP filesystem tools for files in `.windsurf/` directory

- `mcp0_read_text_file` for reading
- `mcp0_write_file` for creating/overwriting
- `mcp0_edit_file` for editing
- Deletions: Use command-line `rm` (MCP doesn't support delete)

**Regular files:** Standard `read_file`, `edit`, `write_to_file` tools

**Fallback strategy:** If standard tools fail on protected files, immediately retry with `mcp0_*` tools

**CRITICAL: MCP tools require ABSOLUTE paths** - Always use `/home/gxx/projects/mcp-web/...` format, never relative paths like `docs/...`

### 1.2 Tool Selection Decision Tree

```text
Is file in .windsurf/ directory?
│
├── YES → Use MCP tools (mcp0_*)
│   ├─ Use absolute path: /home/gxx/projects/mcp-web/.windsurf/...
│   └─ Example: mcp0_read_text_file("/home/gxx/projects/mcp-web/.windsurf/workflows/work.md")
│
└── NO → Use standard tools
    ├─ Can use relative path: docs/file.md
    └─ Example: read_file("docs/file.md")
```

### 1.3 Initiative Structure Decision Tree

**Use scaffolding system when creating new initiatives:** `task scaffold:initiative`

#### Decision: Flat File vs Folder Structure

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

### 1.4 Artifact Management

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

## Initiative Archival

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
**Estimated Tokens:** ~2,000
**Last Updated:** 2025-10-21
**Status:** Active

**Can be @mentioned:** Yes (hybrid loading)

**Topics Covered:**

- File moves
- Initiative archival
- Cross-reference updates
- MCP vs standard tools

**Workflow References:**

- /archive-initiative - Initiative archival
- /implement - File reorganization

**Dependencies:**

- Source: 06_context_engineering.md (File Operations section)

**Changelog:**

- 2025-10-21: Created from 06_context_engineering.md
