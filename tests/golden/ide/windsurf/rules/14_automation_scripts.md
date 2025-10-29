---
trigger: model_decision
description: Apply when using automation scripts Taskfile commands or scaffolding operations

---

# Automation Scripts and Taskfile Commands

**Purpose:** Quick reference for automation via `task` commands. All scripts support non-interactive modes for AI agent use.

---

## Quick Reference

| Task | Command | Non-Interactive Mode |
|------|---------|----------------------|
| Archive initiative | `task archive:initiative NAME=<name>` | ✅ Always |
| Move file + refs | `task move:file SRC=<src> DST=<dst>` | ✅ Always |
| Update index | `task update:index DIR=<dir>` | ✅ Always |
| Validate initiatives | `task validate:initiatives` | ✅ Always |
| Validate workflows | `python scripts/validate_workflows.py` | ✅ Always |
| Check tokens | `python scripts/check_workflow_tokens.py` | ✅ Always |
| Validate archival | `python scripts/validate_archival.py <file>` | ✅ Always |

**Scaffolding (AI agents should NOT use interactive mode):**

| Task | Command | Config Required |
|------|---------|-----------------|
| Create initiative | `python scripts/scaffold.py --type initiative --config <config.yaml>` | ✅ Yes |
| Create ADR | `python scripts/scaffold.py --type adr --config <config.yaml>` | ✅ Yes |
| Create summary | `python scripts/scaffold.py --type summary --config <config.yaml>` | ✅ Yes |

**Default configs available:** `scripts/templates/configs/{initiative,adr,summary}-default.yaml`

---

## Script Categories

### File Operations (Non-Interactive)

**file_ops.py** - Archive, move, index operations

```bash
# Archive initiative
python scripts/file_ops.py archive-initiative <name> [--completed-on YYYY-MM-DD] [--dry-run]

# Move file with ref updates
python scripts/file_ops.py move-file <src> <dst> [--no-update-refs] [--dry-run]

# Update index
python scripts/file_ops.py update-index [<dir>] [--dry-run]
```

### Validation Scripts (Non-Interactive)

**All validation scripts run non-interactively:**

- `validate_archival.py <file>` - Check archival gates
- `validate_initiatives.py` - Validate all initiatives
- `validate_workflows.py` - Validate workflows/rules
- `validate_task_format.py` - Validate task format
- `check_workflow_tokens.py` - Monitor token counts

### Scaffolding (Config Mode for AI)

**scaffold.py** - Template generation

**AI Agent Usage:**

```bash
# Create config file with required fields
cat > /tmp/init-config.yaml << 'EOF'
title: "My Initiative"
owner: "AI Agent"
priority: "High"
estimated_duration: "2 weeks"
tags: ["automation"]
success_criteria: ["Criterion 1"]
EOF

# Generate from config
python scripts/scaffold.py --type initiative --config /tmp/init-config.yaml
```

**Available templates:**

- `initiative` - Flat-file initiative
- `initiative-folder` - Folder-based initiative
- `adr` - Architecture Decision Record
- `summary` - Session summary

---

## Taskfile Commands

### High-Impact Automation

```bash
task archive:initiative NAME=2025-10-18-my-feature
task move:file SRC=docs/old.md DST=docs/new.md
task update:index DIR=docs/initiatives
task validate:initiatives
```

### Validation

```bash
task validate:initiatives          # All initiatives
task validate:initiatives:ci       # CI mode (exit 1 on fail)
task validate:dependencies         # Dependency graph
task deps:graph                    # Generate DOT graph
task deps:blockers                 # Show blocker cascade
```

### Scaffolding (For Humans Only)

**Note:** AI agents should use config mode directly, not these interactive tasks.

```bash
task scaffold:initiative           # ❌ Interactive (agents can't use)
task scaffold:adr                  # ❌ Interactive (agents can't use)
task scaffold:summary              # ❌ Interactive (agents can't use)
```

---

## AI Agent Best Practices

### ✅ DO

- Use `task archive:initiative NAME=<name>` for archival
- Use `task move:file` for moves with ref updates
- Create YAML configs for scaffolding operations
- Use validation scripts to check before commits
- Batch file operations when possible (3-8 parallel)

### ❌ DON'T

- Call `task scaffold:*` (interactive mode)
- Use interactive prompts
- Skip validation before archiving
- Archive without checking gates

---

## Config File Examples

### Initiative Config

```yaml
title: "Implement Feature X"
owner: "AI Agent Team"
priority: "High"
estimated_duration: "1 week"
tags: ["feature", "automation"]
success_criteria:
  - "Tests pass"
  - "Documentation updated"
phases:
  - name: "Design"
    status: "completed"
  - name: "Implementation"
    status: "active"
deliverables:
  - "Feature code"
  - "Tests"
```

### ADR Config

```yaml
title: "Use httpx for HTTP requests"
status: "Accepted"
context: "Need robust HTTP client"
decision: "Use httpx with Playwright fallback"
consequences:
  - "Better async support"
  - "Improved error handling"
alternatives:
  - "requests library (sync only)"
```

---

## Performance Metrics

| Operation | Manual | Automated | Speedup |
|-----------|--------|-----------|---------|
| Archive initiative | 15 min | 10 sec | 90x |
| Move + update refs | 10 min | 5 sec | 120x |
| Create initiative | 5 min | 30 sec | 10x |
| Validate all | 20 min | 2 sec | 600x |

---

## References

- Full documentation: [scripts/README.md](../../scripts/README.md)
- Taskfile: [Taskfile.yml](../../Taskfile.yml)
- Config examples: `scripts/templates/configs/`

---

**Maintained by:** mcp-web core team
**Version:** 2.0.0
**Token count:** ~1200 (within medium budget)

---

## Rule Metadata

**File:** `14_automation_scripts.md`
**Trigger:** model_decision
**Estimated Tokens:** ~3,000
**Last Updated:** 2025-10-21
**Status:** Active

**Can be @mentioned:** Yes (hybrid loading)

**Topics Covered:**

- Taskfile commands
- Automation scripts
- Non-interactive scaffolding
- File operations

**Workflow References:**

- /archive-initiative - Archive automation
- /implement - Scaffolding

**Dependencies:**

- Source: automation-scripts.md

**Changelog:**

- 2025-10-21: Changed from manual to model_decision (hybrid approach)
- 2025-10-21: Created from automation-scripts.md
