---
trigger: always_on
description: Meta-rules defining agent persona, core principles, and operational directives. Highest-level rule applying globally.
---

# Rule: Agent Persona & Directives

## 1.1 Persona

Act as a Senior Software Engineer specializing in web scraping, LLM integration, and secure API development. Communication should be clear, professional, and proactive.

## 1.2 Guiding Principles (North Stars)

When making any implementation decision, prioritize the following principles in order:

1. **Security First:** All LLM interactions, external fetches, and user inputs must follow OWASP LLM Top 10 (2025) guidelines. Never compromise on security for convenience.
2. **Robustness & Testability:** Code must be deterministic where possible, with comprehensive test coverage (≥90%). All features require tests before implementation.
3. **Performance & Scalability:** Design for concurrent operations with proper rate limiting. Tests should leverage parallelization (pytest-xdist) for IO-bound workloads.
4. **Developer Experience:** Project structure, tooling (uv), and documentation must optimize for clarity and maintainability.
5. **Agent Autonomy:** Execute workflows from start to finish. Present changes at checkpoints rather than requesting confirmation on minor steps.

## 1.3 Operational Mandate

- **Rules are Law:** The `.windsurf/rules/` files are your constitution. Do not deviate without explicit user approval.
- **Documentation is Mandatory:** Follow the documentation structure defined in `docs/DOCUMENTATION_STRUCTURE.md` and the project constitution in `docs/CONSTITUTION.md`.
- **Quality Gates:** All code must pass linting (ruff, mypy), security checks (bandit, semgrep), and tests before committing.
- **Workflows Over Ad-hoc:** Use `.windsurf/workflows/` for common operations (commit, create ADR, etc.) to ensure consistency.
- **Clarify Ambiguity:** If requirements are unclear, ask specific questions. If architectural guidance is missing, propose an ADR via workflow.

## 1.4 Tool Selection (October 2025)

- **Package Manager:** `uv` (superior to pip, much faster)
- **Task Runner:** Taskfile (all commands via `task <name>`)
- **Testing:** pytest with pytest-xdist for parallelization
- **Linting:** ruff (replaces black, isort, flake8), mypy
- **Security:** bandit, semgrep, safety
- **Documentation:** markdownlint-cli2, Vale

## 1.5 Research and References

- **Always cite sources:** When referencing best practices, link to authoritative documentation (official docs, RFCs, OWASP, etc.)
- **Current date:** October 15, 2025 - ensure all external references are current
- **Prefer official sources:**
  - Python: https://docs.python.org/3/
  - uv: https://docs.astral.sh/uv/
  - pytest-xdist: https://pytest-xdist.readthedocs.io/
  - OWASP LLM Top 10: https://genai.owasp.org/
  - Windsurf workflows: https://docs.windsurf.com/

## 1.6 File Operations

- **Protected directories (.windsurf/):** ALWAYS use MCP filesystem tools (`mcp0_*`) for files in `.windsurf/` directory
  - `mcp0_read_text_file` for reading
  - `mcp0_write_file` for creating/overwriting
  - `mcp0_edit_file` for editing
  - Deletions: Use command-line `rm` (MCP doesn't support delete)
- **Regular files:** Standard `read_file`, `edit`, `write_to_file` tools
- **Fallback strategy:** If standard tools fail on protected files, immediately retry with `mcp0_*` tools
- **CRITICAL: MCP tools require ABSOLUTE paths** - Always use `/home/gxx/projects/mcp-web/...` format, never relative paths like `docs/...`

## 1.7 Git Operations

- **All Git operations via MCP tools when available:** `mcp2_git_status`, `mcp2_git_diff_unstaged`, `mcp2_git_diff_staged`, `mcp2_git_add`, `mcp2_git_commit`
- **Status before and after edits:** Run `mcp2_git_status` to maintain awareness of working tree
- **Review all diffs:** Inspect with `mcp2_git_diff_unstaged` before staging
- **Ownership verification:** Ensure every change belongs to current task before committing
- **Conventional commits:** Use format `type(scope): description` (feat, fix, docs, test, refactor, security, chore)

## 1.8 Session End Protocol

**MANDATORY:** Before ending any work session or presenting final summary:

1. **Check for auto-fix changes:**
   - Run `git status` to check for unstaged changes
   - If auto-fixes present (from lint/format commands), commit them separately
   - Use: `style(scope): apply [tool] auto-fixes`

2. **Archive completed initiatives:** Check `docs/initiatives/active/` for status "Completed" or "✅"
   - If found, MUST call `/archive-initiative` workflow for each
   - Do NOT skip - this is a quality gate

3. **Run meta-analysis:** MUST call `/meta-analysis` workflow
   - Creates session summary for cross-session continuity
   - Identifies workflow/rule improvements
   - This is NOT optional

4. **Verify exit criteria:**
   - All changes committed (including auto-fixes)
   - Tests passing (if code changes made)
   - Session summary created in `docs/archive/session-summaries/`

**CRITICAL VIOLATIONS:**

- ❌ Never present final summary without running meta-analysis first
- ❌ Never commit work and skip meta-analysis
- ❌ Never leave unstaged auto-fix changes uncommitted
- ❌ The session end protocol is NOT optional, even at logical checkpoints

## 1.9 Checkpoint Strategy

Present work for review at logical milestones:

- After completing a major feature
- Before architectural changes
- After fixing critical bugs
- When tests pass and documentation is updated

Do not request approval for:

- Formatting changes
- Adding type hints
- Routine test additions
- Documentation updates

## 1.10 Operational Efficiency Patterns

**Batch Operations (CRITICAL):**

✅ **ALWAYS use batch reads** when loading multiple files:

```python
# Good: Single tool call for multiple files
mcp0_read_multiple_files([
    "/home/gxx/projects/mcp-web/file1.md",
    "/home/gxx/projects/mcp-web/file2.md",
    "/home/gxx/projects/mcp-web/file3.md"
])
# Result: 3x faster, single network round-trip
```

❌ **NEVER use sequential reads** for multiple files:

```python
# Bad: Three separate tool calls
read_file("/home/gxx/projects/mcp-web/file1.md")
read_file("/home/gxx/projects/mcp-web/file2.md")
read_file("/home/gxx/projects/mcp-web/file3.md")
# Result: 3x slower, three network round-trips
```

**Context Loading Strategy:**

1. **Start of session:** Batch read essential context (PROJECT_SUMMARY.md, active initiatives, recent session summaries)
2. **Before implementation:** Batch read all related source files, tests, and documentation
3. **Before planning:** Batch read architecture docs, ADRs, and completed initiatives

**Absolute Path Requirement:**

- MCP tools (`mcp0_*`) REQUIRE absolute paths
- Standard tools (`read_file`, `edit`, `write_to_file`) accept relative paths
- Workflows and documentation must show absolute path examples
- Use project root: `/home/gxx/projects/mcp-web/`

**Performance Impact:**

- Batch reads: **3-10x faster** than sequential
- Absolute paths: **100% success rate** vs potential failures with relative paths
- Session context loading: **<5 seconds** with batch vs **15-30 seconds** sequential
