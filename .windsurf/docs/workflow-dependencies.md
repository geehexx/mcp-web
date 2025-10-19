---
type: machine-readable-reference
category: auto-generated
purpose: Auto-generated dependency graph of all workflows
token_budget: low
audience: ai-agent
auto_generated: true
maintenance: auto
last_updated: "2025-10-20"
tags: ["workflows", "dependencies", "graph", "auto-generated"]
---

# Workflow Dependencies

**Generated:** Auto-generated from frontmatter

## Dependency Graph

```mermaid
graph TD
    archive-initiative[archive-initiative] --> scripts/validate_archival.py[scripts/validate_archival.py]
    archive-initiative[archive-initiative] --> scripts/dependency_registry.py[scripts/dependency_registry.py]
    commit[commit] --> validate[validate]
    consolidate-summaries[consolidate-summaries] --> extract-session[extract-session]
    consolidate-summaries[consolidate-summaries] --> summarize-session[summarize-session]
    generate-plan[generate-plan] --> research[research]
    implement[implement] --> load-context[load-context]
    implement[implement] --> validate[validate]
    implement[implement] --> commit[commit]
    meta-analysis[meta-analysis] --> extract-session[extract-session]
    meta-analysis[meta-analysis] --> summarize-session[summarize-session]
    meta-analysis[meta-analysis] --> consolidate-summaries[consolidate-summaries]
    plan[plan] --> research[research]
    plan[plan] --> generate-plan[generate-plan]
    plan[plan] --> load-context[load-context]
    summarize-session[summarize-session] --> extract-session[extract-session]
    work-routing[work-routing] --> detect-context[detect-context]
    work-session-protocol[work-session-protocol] --> archive-initiative[archive-initiative]
    work-session-protocol[work-session-protocol] --> meta-analysis[meta-analysis]
    work[work] --> detect-context[detect-context]
    work[work] --> load-context[load-context]
    work[work] --> implement[implement]
    work[work] --> plan[plan]
    work[work] --> validate[validate]
    work[work] --> commit[commit]
    work[work] --> archive-initiative[archive-initiative]
    work[work] --> meta-analysis[meta-analysis]
```

## Dependency Details

| Workflow | Dependencies | Complexity |
|----------|--------------|------------|
| archive-initiative | scripts/validate_archival.py, scripts/dependency_registry.py | 50 |
| bump-version | None | 70 |
| commit | validate | 55 |
| consolidate-summaries | extract-session, summarize-session | 70 |
| detect-context | None | 80 |
| extract-session | None | 55 |
| generate-plan | research | 60 |
| implement | load-context, validate, commit | 75 |
| load-context | None | 65 |
| meta-analysis | extract-session, summarize-session, consolidate-summaries | 60 |
| new-adr | None | 45 |
| plan | research, generate-plan, load-context | 70 |
| research | None | 50 |
| summarize-session | extract-session | 55 |
| update-docs | None | 55 |
| validate | None | 62 |
| work | detect-context, load-context, implement, plan, validate, commit, archive-initiative, meta-analysis | 85 |
| work-routing | detect-context | 70 |
| work-session-protocol | archive-initiative, meta-analysis | 75 |
