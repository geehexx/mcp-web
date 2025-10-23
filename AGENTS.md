# Agents

**Purpose:** Single source of truth for external agents in this repository. This file provides machine-readable context for AI coding agents, MCP clients, and automation tools to understand agent capabilities and configuration in this project.

**Last Updated:** 2025-10-18

---

## Overview

This repository contains two types of agents:

1. **MCP Web Server** - Production MCP server providing web summarization capabilities
2. **Windsurf Agent Configuration** - Development-time AI agent setup for repository maintenance

For human-facing documentation, see [README.md](./README.md). This file focuses on machine-readable agent specifications.

---

## Agent Entry Template

Use this template when adding new agents to this file:

```yaml
### Agent Name

**Type:** [MCP Server | CLI Tool | API Service | Development Agent | Other]
**Status:** [Active | Deprecated | Experimental]
**Entry Point:** `path/to/entry/point`
**Protocol:** [MCP | HTTP | CLI | Other]

**Description:** One-sentence summary of what this agent does.

**Capabilities:**
- Capability 1
- Capability 2
- Capability 3

**Configuration:**
- Config file: `path/to/config`
- Environment variables: See [link to env docs]
- Dependencies: List or link

**Usage Example:**
[bash/python/other]
<usage command or code snippet>
[/bash/python/other]

**Related Documentation:**
- [Link to detailed docs](relative/path/to/docs)
- [Link to API reference](relative/path/to/api)

**Maintainer:** Team/Person responsible
**Last Verified:** YYYY-MM-DD
```

---

## Agents in This Repository

### MCP Web Server

**Type:** MCP Server
**Status:** Active
**Entry Point:** `src/mcp_web/mcp_server.py`
**Protocol:** Model Context Protocol (MCP)

**Description:** Production MCP server providing intelligent web summarization with robust fetching, content extraction, and LLM-powered summarization.

**Capabilities:**

- `summarize_urls` - Fetch and summarize content from one or more URLs with optional query focus
- `get_cache_stats` - Retrieve cache performance metrics
- `clear_cache` - Clear all cached content
- `prune_cache` - Remove expired cache entries

**Configuration:**

- Config file: `config.toml` (optional, uses sane defaults)
- Environment variables: See [ENVIRONMENT_VARIABLES.md](docs/reference/ENVIRONMENT_VARIABLES.md)
- Dependencies: Python 3.10+, httpx, playwright, trafilatura, FastMCP

**Usage Example:**

```bash
# Install
uv sync

# Run server
uv run mcp-web

# Or via Python module
python -m mcp_web.mcp_server
```

**Integration with MCP Clients:**

```json
{
  "mcpServers": {
    "mcp-web": {
      "command": "uv",
      "args": ["run", "mcp-web"],
      "env": {
        "MCP_WEB_CACHE_ENABLED": "true",
        "MCP_WEB_LLM_PROVIDER": "openai"
      }
    }
  }
}
```

**Related Documentation:**

- [Architecture Overview](docs/architecture/ARCHITECTURE.md)
- [API Reference](docs/api/API.md)
- [Configuration Guide](docs/reference/ENVIRONMENT_VARIABLES.md)
- [ADR-0001: httpx/Playwright Fallback](docs/adr/0001-use-httpx-playwright-fallback.md)
- [ADR-0012: Monolithic Tool Design](docs/adr/0012-monolithic-tool-design.md)

**Maintainer:** Core Team
**Last Verified:** 2025-10-18

---

### Unified Agent Configuration

**Type:** Development Agent Configuration
**Status:** Active
**Entry Point:** `.unified/`
**Protocol:** Unified IDE Integration (Windsurf & Cursor)

**Description:** A unified AI agent configuration system for automated repository maintenance, code generation, testing, and documentation management. This system is designed to be IDE-agnostic, with adapters that generate configurations for both Windsurf and Cursor from a single source of truth.

**Capabilities:**

- Automated code generation following project standards
- Test-driven development workflows
- Documentation generation and validation
- Architecture decision recording (ADRs)
- Initiative tracking and session summarization
- Quality gate enforcement (linting, type checking, security)

**Configuration:**

- Rules: `.unified/rules/` (defining agent behavior)
- Commands: `.unified/commands/` (defining workflows and operations)
- Standards: `docs/CONSTITUTION.md`, `docs/DOCUMENTATION_STRUCTURE.md`

**Key Workflows:**

```bash
# Work orchestration (detects context and routes to appropriate workflow)
/work

# Create new architecture decision record
/new-adr

# Git commit with validation
/commit

# Quality validation
/validate

# Full workflow list
ls .unified/commands/
```

**Related Documentation:**

- [Constitution](docs/CONSTITUTION.md) - Project principles and standards
- [Documentation Structure](docs/DOCUMENTATION_STRUCTURE.md) - Documentation organization
- [Core Directives](.unified/rules/00_core_directives.yaml) - Core agent behavior rules
- [ADR-0018: Workflow Architecture V3](docs/adr/0018-workflow-architecture-v3.md)

**Maintainer:** Core Team
**Last Verified:** 2025-10-18

---

## Adding or Updating Agents

### When to Add an Entry

Add a new agent entry when:

- Creating a new MCP server or tool in this repository
- Integrating external agent capabilities
- Adding automation scripts that act autonomously
- Documenting agent-facing APIs or interfaces

### Update Checklist

When adding or updating an agent entry:

- [ ] Use the template format above for consistency
- [ ] Provide concrete usage examples with actual commands
- [ ] Link to detailed documentation (don't duplicate long content)
- [ ] Verify all paths and commands are correct
- [ ] Update "Last Verified" date
- [ ] Ensure entry is machine-readable (structured format)
- [ ] Run validation: `task docs:lint` or `task test:agents-md` (if implemented)

### Validation

To validate this file:

```bash
# Markdown linting
task docs:lint

# Link checking (verify all internal links work)
grep -oP '\[.*?\]\(\K[^)]+' AGENTS.md | while read link; do
  [[ "$link" =~ ^http ]] || [ -f "$link" ] || echo "Broken link: $link"
done

# TODO: Implement automated agent entry validation
# task test:agents-md
```

---

## Machine-Readable Metadata

For automated tools and registries:

```yaml
repository:
  name: mcp-web
  description: Model Context Protocol server for intelligent web summarization
  url: https://github.com/geehexx/mcp-web

agents:
  - name: mcp-web
    type: mcp-server
    protocol: mcp
    entry_point: src/mcp_web/mcp_server.py
    status: active
    tools:
      - summarize_urls
      - get_cache_stats
      - clear_cache
      - prune_cache

  - name: unified-agent
    type: development-agent
    protocol: unified
    entry_point: .unified/
    status: active
    capabilities:
      - code-generation
      - documentation
      - testing
      - validation
```

---

## Standards and References

**This file follows:**

- [AGENTS.md Standard](https://github.com/agentmd/agent.md) - Community-driven format for agent documentation
- [MCP Registry Format](https://github.com/modelcontextprotocol/registry) - Model Context Protocol server registry
- Project documentation standards: [DOCUMENTATION_STRUCTURE.md](docs/DOCUMENTATION_STRUCTURE.md)

**Related Standards:**

- [MCP Specification](https://modelcontextprotocol.io/) - Protocol specification
- [ADR-0002: Windsurf Workflow System](docs/adr/0002-adopt-windsurf-workflow-system.md)
- [ADR-0003: Documentation Standards](docs/adr/0003-documentation-standards-and-structure.md)

---

## Future Agents

Potential agents to document here as they are developed:

- CLI summarization tool (if extracted from MCP server)
- Batch processing agent (for bulk URL summarization)
- Monitoring/alerting agent (for production metrics)
- Documentation generation agent (if automated beyond Windsurf)

When adding future agents, maintain consistency with the template format and ensure all links are valid.

---

**Maintained By:** mcp-web core team
**Version:** 1.0.0
**Format Version:** AGENTS.md 1.0 (2025 standard)
