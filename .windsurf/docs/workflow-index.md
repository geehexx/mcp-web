# Workflow Index

**Generated:** Auto-generated from frontmatter

## Analysis Workflows

| Workflow | Complexity | Tokens | Dependencies | Status |
|----------|------------|--------|--------------|--------|
| [consolidate-summaries](consolidate-summaries.md) | 65 | 1942 | extract-session, summarize-session | active |
| [extract-session](extract-session.md) | 55 | 1196 | - | active |
| [meta-analysis](meta-analysis.md) | 50 | 766 | extract-session, summarize-session | active |
| [summarize-session](summarize-session.md) | 55 | 1430 | extract-session | active |

## Automation Workflows

| Workflow | Complexity | Tokens | Dependencies | Status |
|----------|------------|--------|--------------|--------|
| [bump-version](bump-version.md) | 70 | 1789 | - | active |
| [update-docs](update-docs.md) | 55 | 1533 | - | active |

## Documentation Workflows

| Workflow | Complexity | Tokens | Dependencies | Status |
|----------|------------|--------|--------------|--------|
| [archive-initiative](archive-initiative.md) | 40 | 409 | - | active |
| [new-adr](new-adr.md) | 45 | 482 | - | active |

## Implementation Workflows

| Workflow | Complexity | Tokens | Dependencies | Status |
|----------|------------|--------|--------------|--------|
| [implement](implement.md) | 75 | 2384 | load-context, validate, commit | active |

## Operations Workflows

| Workflow | Complexity | Tokens | Dependencies | Status |
|----------|------------|--------|--------------|--------|
| [detect-context](detect-context.md) | 80 | 1617 | - | active |
| [load-context](load-context.md) | 65 | 1908 | - | active |

## Orchestrator Workflows

| Workflow | Complexity | Tokens | Dependencies | Status |
|----------|------------|--------|--------------|--------|
| [work](work.md) | 85 | 1313 | detect-context, load-context, implement, plan, validate, commit, archive-initiative, meta-analysis | active |

## Planning Workflows

| Workflow | Complexity | Tokens | Dependencies | Status |
|----------|------------|--------|--------------|--------|
| [generate-plan](generate-plan.md) | 60 | 1585 | research | active |
| [plan](plan.md) | 70 | 1729 | research, generate-plan, load-context | active |
| [research](research.md) | 50 | 1300 | - | active |

## Sub-workflow Workflows

| Workflow | Complexity | Tokens | Dependencies | Status |
|----------|------------|--------|--------------|--------|
| [work-routing](work-routing.md) | 70 | 1221 | detect-context | active |
| [work-session-protocol](work-session-protocol.md) | 75 | 1372 | archive-initiative, meta-analysis | active |

## Validation Workflows

| Workflow | Complexity | Tokens | Dependencies | Status |
|----------|------------|--------|--------------|--------|
| [commit](commit.md) | 55 | 1058 | validate | active |
| [validate](validate.md) | 60 | 1884 | - | active |
