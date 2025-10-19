---
created: "2025-10-18"
updated: "2025-10-19"
trigger: model_decision
description: File operations, git operations, context management, and .windsurf/ directory structure enforcement
category: operations
tokens: 2100
applyTo:
  - file_operations
  - git
  - context_loading
  - windsurf_directory_structure
priority: high
status: active
---

# Rule: Context Engineering

**Purpose:** Defines how to efficiently load, manage, and operate on files and git context.

**See also:**

- Core principles: [00_agent_directives.md](./00_agent_directives.md)
- Operational protocols: [05_operational_protocols.md](./05_operational_protocols.md)
- Context loading patterns: [context-loading-patterns.md](../docs/context-loading-patterns.md)
- Batch operations: [batch-operations.md](../docs/batch-operations.md)

---

## 0. .windsurf/ Directory Structure

**Standard Structure:**

```text
.windsurf/
├── docs/              # AI-specific reference documentation (machine-readable)
│   ├── context-loading-patterns.md
│   ├── batch-operations.md
│   └── [other reference guides]
├── rules/             # Agent behavior rules
│   ├── 00_agent_directives.md
│   ├── 01_testing_and_tooling.md
│   └── [...]
├── workflows/         # Executable workflows only
│   ├── work.md
│   ├── implement.md
│   └── [...]
└── templates/         # Code/document templates (deprecated - use docs/)
```

### Critical: .windsurf/docs/ vs .windsurf/workflows/ vs .windsurf/rules/

**STRICT SEPARATION ENFORCED:**

| Directory | Purpose | Allowed Files | Forbidden |
|-----------|---------|---------------|----------|
| **workflows/** | Executable workflows ONLY | `*.md` files invokable via `/workflow-name` | README.md, guides, documentation, indices |
| **docs/** | Reference documentation | Pattern guides, best practices, indices | Executable workflows |
| **rules/** | Agent behavior rules | `*.md` rule files | README.md, guides, documentation |

**workflows/** - Executable workflows ONLY:

- Each `.md` file is invokable via `/workflow-name`
- Contains procedural steps for agent execution
- YAML frontmatter with workflow metadata
- **FORBIDDEN:** README.md, INDEX.md, GUIDE.md, or any non-executable documentation

**docs/** - Reference documentation (machine-readable):

- Pattern libraries, best practices, guides
- Maintained with same rigor as regular documentation
- Provide reference points for AI agents
- Examples: `context-loading-patterns.md`, `batch-operations.md`, `tool-patterns.md`
- **ALLOWED:** README.md, INDEX.md, comprehensive guides

**rules/** - Agent behavior rules ONLY:

- Behavioral directives and constraints
- Conditional rules triggered by context
- **FORBIDDEN:** README.md, guides, documentation

**CRITICAL VIOLATIONS:**

❌ **NEVER create these files:**

- `.windsurf/workflows/README.md` → Use `docs/guides/WORKFLOW_GUIDE.md`
- `.windsurf/rules/README.md` → Use `.windsurf/docs/rules-index.md`
- Any non-workflow file in `workflows/`
- Any non-rule file in `rules/`

**Enforcement:**

- Pre-commit hooks validate directory structure
- `ls-lint` enforces kebab-case for workflow/rule files
- Manual review required for any `.windsurf/` changes

---

## 1. File Operations

### 1.1 Tool Selection

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

## 2. Git Operations

### 2.1 Git Commands via run_command

**Use `run_command` tool for all git operations:**

All git commands executed via `run_command` with appropriate `Cwd` parameter.

**Common operations:**

```bash
# Check status
git status --short

# Review unstaged changes
git diff

# Review staged changes
git diff --cached

# Stage files
git add <files>

# Commit
git commit -m "type(scope): description"

# View recent history
git log --oneline -5
```

### 2.2 Git Workflow

**Before making changes:**

- Run `git status --short` to check working tree state
- Review context to understand recent work

**Before committing:**

- Review all diffs: `git diff` (unstaged) or `git diff --cached` (staged)
- Ensure every change belongs to current task
- Split unrelated changes into separate commits

**Commit message format:**

```text
type(scope): description

- Detail 1
- Detail 2
- Detail 3
```

**Types:** feat, fix, docs, test, refactor, security, chore

### 2.3 Conventional Commits

**Format:** `type(scope): description`

**Types:**

| Type | Use Case | Example |
|------|----------|---------|
| `feat` | New feature | `feat(auth): add API key rotation` |
| `fix` | Bug fix | `fix(cache): handle missing files gracefully` |
| `docs` | Documentation | `docs(adr): create ADR-00XX for caching` |
| `test` | Test changes | `test(security): add XSS injection tests` |
| `refactor` | Code refactor | `refactor(chunker): extract method` |
| `security` | Security fix | `security(llm): add input sanitization` |
| `chore` | Maintenance | `chore(deps): update uv to 0.5.0` |
| `style` | Auto-fixes | `style(docs): apply markdownlint fixes` |

**Scope:** Module, component, or area affected (e.g., `auth`, `cache`, `docs`, `workflows`)

### 2.4 Git Best Practices

**DO:**

- ✅ Check `git status` before and after major changes
- ✅ Review diffs before staging
- ✅ Write descriptive commit messages
- ✅ Split unrelated changes into separate commits
- ✅ Commit auto-fixes separately with `style(scope)` type

**DON'T:**

- ❌ Commit without reviewing diffs
- ❌ Mix unrelated changes in one commit
- ❌ Use vague commit messages ("fix stuff", "update")
- ❌ Leave unstaged changes at session end
- ❌ Commit without running tests (for code changes)

---

## 3. Context Loading Strategies

### 3.1 Overview

Context loading is one of the most frequent operations. Optimize for speed and efficiency.

**See detailed patterns:**

- [Context Loading Patterns](../workflows/context-loading-patterns.md) - Complete pattern library
- [Batch Operations](../workflows/batch-operations.md) - Optimization techniques

### 3.2 Quick Reference

**When to use batch operations:**

- Loading 3+ files: 3-10x faster than sequential
- Known file paths: Use `mcp0_read_multiple_files`
- Optimal batch size: 10-15 files per batch

**Common patterns:**

1. **Initiative work:** Load initiative + source + tests
2. **Planning:** Load PROJECT_SUMMARY + active initiatives + ADRs
3. **Test fixes:** Load test files + module under test

### 3.3 Performance Targets

| Operation | Target | Technique |
|-----------|--------|-----------|
| Load 5 files | <1s | Batch read |
| Load 10 files | <2s | Batch read |
| Load 20 files | <4s | Chunked batch (2 batches of 10) |
| Load initiative context | <10s | Batch read (initiative + related files) |

---

## 4. File Organization Principles

### 4.1 Initiative Organization

**Folder structure for complex initiatives:**

```text
docs/initiatives/active/YYYY-MM-DD-name/
├── initiative.md          # Overview, status, phases
├── phases/
│   ├── phase-1-*.md       # Phase-specific details
│   ├── phase-2-*.md
│   └── phase-3-*.md
└── artifacts/
    ├── research-summary.md
    ├── analysis.md
    └── PROPOSAL-*.md
```

**Flat file for simple initiatives:**

```text
docs/initiatives/active/YYYY-MM-DD-name.md
```

### 4.2 Workflow Organization

**Decomposed workflows:**

```text
.windsurf/workflows/
├── work.md                    # Orchestrator
├── work-routing.md            # Sub-workflow (routing logic)
├── work-session-protocol.md   # Sub-workflow (session end)
└── common-patterns.md         # Reference guide
```

**Template library:**

```text
.windsurf/templates/
└── common-patterns.md         # Shared code examples
```

---

## References

- Core directives: [00_agent_directives.md](./00_agent_directives.md)
- Operational protocols: [05_operational_protocols.md](./05_operational_protocols.md)
- Context loading: [context-loading-patterns.md](../workflows/context-loading-patterns.md)
- Batch operations: [batch-operations.md](../workflows/batch-operations.md)

---

**Version:** 1.0.0 (Extracted from 00_agent_directives.md Phase 4 decomposition)
**Last Updated:** 2025-10-18
