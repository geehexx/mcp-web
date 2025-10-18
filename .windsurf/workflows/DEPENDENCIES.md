# Workflow Dependencies

**Generated:** Auto-generated from frontmatter

## Dependency Graph

```mermaid
graph TD
    commit[commit] --> validate[validate]
    consolidate-summaries[consolidate-summaries] --> extract-session[extract-session]
    consolidate-summaries[consolidate-summaries] --> summarize-session[summarize-session]
    generate-plan[generate-plan] --> research[research]
    implement[implement] --> load-context[load-context]
    implement[implement] --> validate[validate]
    implement[implement] --> commit[commit]
    meta-analysis[meta-analysis] --> extract-session[extract-session]
    meta-analysis[meta-analysis] --> summarize-session[summarize-session]
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
| archive-initiative | None | 40 |
| bump-version | None | 70 |
| commit | validate | 55 |
| consolidate-summaries | extract-session, summarize-session | 65 |
| detect-context | None | 80 |
| extract-session | None | 55 |
| generate-plan | research | 60 |
| implement | load-context, validate, commit | 75 |
| load-context | None | 65 |
| meta-analysis | extract-session, summarize-session | 50 |
| new-adr | None | 45 |
| plan | research, generate-plan, load-context | 70 |
| research | None | 50 |
| summarize-session | extract-session | 55 |
| update-docs | None | 55 |
| validate | None | 60 |
| work | detect-context, load-context, implement, plan, validate, commit, archive-initiative, meta-analysis | 85 |
| work-routing | detect-context | 70 |
| work-session-protocol | archive-initiative, meta-analysis | 75 |
