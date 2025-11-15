# Architecture Diagrams

This directory contains visual documentation of the MCP-Web architecture using Mermaid diagrams.

## Diagrams

### 1. System Context Diagram
**File:** `system-context.mermaid`
**Purpose:** High-level view of MCP-Web and its external dependencies

**Shows:**
- MCP-Web system boundary
- Core pipeline components
- Infrastructure services
- External systems (LLM providers, web servers, users)
- Data flow between components

**Use this to:** Understand the overall architecture and external integrations.

---

### 2. Summarization Sequence Diagram
**File:** `summarization-sequence.mermaid`
**Purpose:** Detailed sequence of a complete summarization request

**Shows:**
- Step-by-step request flow
- Component interactions over time
- Caching strategy
- Security validations
- Error handling paths
- Streaming response

**Use this to:** Understand how a request flows through the system and where optimizations/caching occur.

---

### 3. Component Interaction Diagram
**File:** `component-interactions.mermaid`
**Purpose:** Component dependencies and relationships

**Shows:**
- Component layers (API, Fetch, Process, LLM, Infrastructure)
- Dependencies between components
- Cross-cutting concerns (Config, Metrics, Cache)
- Known architectural issues

**Use this to:** Understand component responsibilities and dependencies for development/refactoring.

---

## Viewing Diagrams

### Online (GitHub/GitLab)
Mermaid diagrams render automatically in Markdown viewers.

### VS Code
Install the [Mermaid Preview extension](https://marketplace.visualstudio.com/items?itemName=vstirbu.vscode-mermaid-preview).

### Command Line
```bash
# Install Mermaid CLI
npm install -g @mermaid-js/mermaid-cli

# Render to PNG
mmdc -i system-context.mermaid -o system-context.png

# Render to SVG
mmdc -i system-context.mermaid -o system-context.svg
```

### Online Editor
Use [Mermaid Live Editor](https://mermaid.live) to view and edit diagrams interactively.

---

## Diagram Conventions

### Colors

**System Context Diagram:**
- 🔵 Blue - Core pipeline components
- 🟣 Purple - Infrastructure services
- 🟢 Green - External systems

**Component Interaction Diagram:**
- 🔴 Red - API layer
- 🔵 Teal - Fetch layer
- 🟡 Yellow - Processing layer
- 🟢 Green - LLM layer
- ⚫ Gray - Infrastructure

### Symbols
- `→` - Data flow
- `[(Database)]` - Persistent storage
- `[Component]` - Service/module
- `Actor` - External user/system

---

## Updating Diagrams

When making architectural changes, update relevant diagrams:

1. **Code changes** → Update component diagram
2. **New integrations** → Update system context
3. **Flow changes** → Update sequence diagram

**Commit diagrams with code changes** to keep documentation in sync.

---

## Related Documentation

- [ARCHITECTURE.md](../ARCHITECTURE.md) - Detailed architectural documentation
- [ADRs](../adr/) - Architecture Decision Records
- [SECURITY_ARCHITECTURE.md](../SECURITY_ARCHITECTURE.md) - Security design

---

## Future Diagrams (Planned)

- [ ] Deployment architecture
- [ ] Data flow diagram
- [ ] Security boundaries
- [ ] Cache invalidation flow
- [ ] Error propagation
- [ ] Metrics collection flow

---

**Last Updated:** 2025-11-15
**Maintained By:** MCP-Web Development Team
