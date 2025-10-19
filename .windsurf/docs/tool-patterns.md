---
type: machine-readable-reference
category: pattern-library
purpose: MCP tool usage patterns and best practices for AI agents
token_budget: medium
audience: ai-agent
auto_generated: false
maintenance: manual
last_updated: "2025-10-20"
tags: ["mcp-tools", "patterns", "file-operations", "git", "commands"]
---

# MCP Tool Usage Patterns

**Purpose:** Quick reference for MCP tool selection and usage patterns.

---

## Quick Lookup

| Task | Tool | Example |
|------|------|--------|
| Read 1 file (.windsurf/) | `mcp0_read_text_file` | `mcp0_read_text_file("/abs/path")` |
| Read 3+ files | `mcp0_read_multiple_files` | `mcp0_read_multiple_files([...])` |
| Read 1 file (regular) | `read_file` | `read_file("/abs/path")` |
| Write file (.windsurf/) | `mcp0_write_file` | `mcp0_write_file(path, content)` |
| Write file (regular) | `write_to_file` | `write_to_file(path, content)` |
| Edit file (.windsurf/) | `mcp0_edit_file` | `mcp0_edit_file(path, edits)` |
| Edit file (regular) | `edit` or `multi_edit` | `edit(path, old, new)` |
| Find files | `find_by_name` | `find_by_name(dir, pattern)` |
| Search content | `grep_search` | `grep_search(query, path)` |
| List directory | `mcp0_list_directory` | `mcp0_list_directory(path)` |
| Git command | `run_command` | `run_command("git status", cwd)` |
| Run tests | `run_command` | `run_command("task test", cwd)` |

---

## Tool Selection Matrix

| Operation | Protected (.windsurf/) | Regular Files | Reason |
|-----------|----------------------|---------------|--------|
| Read file | `mcp0_read_text_file` | `read_file` | MCP tools require absolute paths |
| Write file | `mcp0_write_file` | `write_to_file` | Protected directory enforcement |
| Edit file | `mcp0_edit_file` | `edit` or `multi_edit` | Line-based edits |
| Move file | `mcp0_move_file` | `run_command("mv")` | Atomic operations |
| List directory | `mcp0_list_directory` | `list_dir` | Consistent interface |
| Create directory | `mcp0_create_directory` | `run_command("mkdir -p")` | Recursive creation |

---

## Pattern 1: Batch File Reading

**Use when:** Reading 3+ files simultaneously

**Tool:** `mcp0_read_multiple_files`

**Performance:** 3-10x faster than sequential reads

**Example:**

```typescript
mcp0_read_multiple_files([
  "/home/gxx/projects/mcp-web/.windsurf/workflows/work.md",
  "/home/gxx/projects/mcp-web/.windsurf/workflows/plan.md",
  "/home/gxx/projects/mcp-web/.windsurf/workflows/implement.md"
])
```

**Best practices:**

- Batch size: 10-15 files optimal
- Use absolute paths (required for MCP tools)
- Group related files in single call

---

## Pattern 2: Protected Directory Operations

**Use when:** Operating on `.windsurf/` directory

**Tools:** All `mcp0_*` tools

**Critical rules:**

- **ALWAYS** use absolute paths
- **NEVER** use relative paths with MCP tools
- **VERIFY** path starts with `/home/gxx/projects/mcp-web/.windsurf/`

**Example:**

```typescript
// ✅ Correct
mcp0_read_text_file({
  path: "/home/gxx/projects/mcp-web/.windsurf/rules/00_agent_directives.md"
})

// ❌ Wrong
mcp0_read_text_file({
  path: ".windsurf/rules/00_agent_directives.md"  // Relative path fails
})
```

---

## Pattern 3: Git Operations

**Use when:** Any git command

**Tool:** `run_command`

**Required parameters:**

- `CommandLine`: Full git command
- `Cwd`: Repository root (`/home/gxx/projects/mcp-web`)
- `Blocking`: `true` (wait for completion)
- `SafeToAutoRun`: Depends on command

**Example:**

```typescript
run_command({
  CommandLine: "git status --short",
  Cwd: "/home/gxx/projects/mcp-web",
  Blocking: true,
  SafeToAutoRun: true  // Read-only operation
})
```

**Safe commands (SafeToAutoRun: true):**

- `git status`
- `git diff`
- `git log`
- `git show`

**Unsafe commands (SafeToAutoRun: false):**

- `git commit`
- `git push`
- `git reset`
- `git clean`

---

## Pattern 4: Task Commands

**Use when:** Running project tasks

**Tool:** `run_command`

**Format:** `task <task-name>`

**Example:**

```typescript
run_command({
  CommandLine: "task test:fast:parallel",
  Cwd: "/home/gxx/projects/mcp-web",
  Blocking: true,
  SafeToAutoRun: false  // Executes tests
})
```

**Common tasks:**

- `task test:fast:parallel` - Fast tests with parallelization
- `task lint` - Run all linters
- `task validate` - Full quality gate
- `task docs:lint` - Documentation linting

---

## Pattern 5: Multi-File Edits

**Use when:** Editing multiple sections in one file

**Tool:** `multi_edit`

**Benefits:**

- Atomic operation (all or nothing)
- Sequential edits (each operates on previous result)
- More efficient than multiple `edit` calls

**Example:**

```typescript
multi_edit({
  file_path: "/home/gxx/projects/mcp-web/.windsurf/rules/00_agent_directives.md",
  explanation: "Update section references",
  edits: [
    {
      old_string: "## Section 1.8",
      new_string: "## Section 1.9"
    },
    {
      old_string: "See Section 1.8",
      new_string: "See Section 1.9"
    }
  ]
})
```

**Critical rules:**

- Edits apply sequentially
- Each edit operates on result of previous
- All edits must succeed or none apply

---

## Pattern 6: Directory Tree Inspection

**Use when:** Understanding directory structure

**Tool:** `mcp0_directory_tree`

**Returns:** Recursive JSON structure

**Example:**

```typescript
mcp0_directory_tree({
  path: "/home/gxx/projects/mcp-web/.windsurf"
})
```

**Use cases:**

- Discovering file organization
- Validating directory structure
- Finding related files

---

## Pattern 7: File Metadata

**Use when:** Checking file properties without reading content

**Tool:** `mcp0_get_file_info`

**Returns:** Size, timestamps, permissions, type

**Example:**

```typescript
mcp0_get_file_info({
  path: "/home/gxx/projects/mcp-web/.windsurf/workflows/work.md"
})
```

**Use cases:**

- Check if file exists
- Get file size before reading
- Check modification time

---

## Anti-Patterns

### ❌ Don't: Use Relative Paths with MCP Tools

```typescript
// ❌ Wrong
mcp0_read_text_file({ path: ".windsurf/rules/00_agent_directives.md" })

// ✅ Correct
mcp0_read_text_file({ path: "/home/gxx/projects/mcp-web/.windsurf/rules/00_agent_directives.md" })
```

### ❌ Don't: Sequential Reads for Multiple Files

```typescript
// ❌ Slow (3x slower)
for (const file of files) {
  read_file(file)
}

// ✅ Fast (batch operation)
mcp0_read_multiple_files(files)
```

### ❌ Don't: Mix Tool Types for Same Directory

```typescript
// ❌ Inconsistent
mcp0_read_text_file({ path: "/home/gxx/projects/mcp-web/.windsurf/workflows/work.md" })
edit({ file_path: "/home/gxx/projects/mcp-web/.windsurf/workflows/work.md", ... })

// ✅ Consistent (use MCP tools for .windsurf/)
mcp0_read_text_file({ path: "/home/gxx/projects/mcp-web/.windsurf/workflows/work.md" })
mcp0_edit_file({ path: "/home/gxx/projects/mcp-web/.windsurf/workflows/work.md", ... })
```

---

## Performance Guidelines

| Operation | Tool Calls | Estimated Time | Optimization |
|-----------|-----------|----------------|--------------|
| Read 1 file | 1 | ~200ms | Use `read_file` or `mcp0_read_text_file` |
| Read 5 files (sequential) | 5 | ~1000ms | Use `mcp0_read_multiple_files` |
| Read 5 files (batch) | 1 | ~300ms | **3x faster** |
| Read 15 files (batch) | 1 | ~500ms | **Optimal batch size** |
| Read 50 files (batch) | 1 | ~2000ms | Consider chunking |

---

## References

- [06_context_engineering.md](../rules/06_context_engineering.md) - File operations rules
- [batch-operations.md](./batch-operations.md) - Batch operation strategies
- [context-loading-patterns.md](./context-loading-patterns.md) - Context loading patterns
- [MCP Filesystem Server Docs](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem)

---

**Maintained by:** mcp-web core team
**Version:** 1.0.0
