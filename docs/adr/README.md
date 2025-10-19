# Architecture Decision Records (ADRs)

This directory contains Architecture Decision Records for the mcp-web project.

## What is an ADR?

An Architecture Decision Record (ADR) captures an important architectural decision made along with its context and consequences. ADRs help us:

- **Document decisions:** Create a historical record of why choices were made
- **Share context:** Help new team members understand architectural rationale
- **Enable review:** Periodically evaluate if past decisions still make sense
- **Prevent repetition:** Avoid rehashing old debates

## Format

We use a standardized ADR format based on [Michael Nygard's ADR template](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) and [adr.github.io](https://adr.github.io/).

See [template.md](template.md) for the full template.

## Naming Convention

ADRs are numbered sequentially with a descriptive title:

```text
NNNN-verb-noun-phrase.md
```

Examples:

- `0001-use-httpx-playwright-fallback.md`
- `0002-use-trafilatura-extraction.md`
- `0003-implement-map-reduce-summarization.md`

## Lifecycle

```text
Proposed → Accepted → Implemented → [Deprecated/Superseded]
```

- **Proposed:** Initial draft, under discussion
- **Accepted:** Team has agreed, ready for implementation
- **Implemented:** Decision has been put into practice
- **Deprecated:** No longer recommended but code may still exist
- **Superseded:** Replaced by a newer ADR (link to the new one)

## ADRs are Immutable

Once an ADR is accepted, it should not be modified except to:

- Fix typos or formatting
- Add clarifications
- Update status (Accepted → Implemented)
- Mark as superseded (add link to new ADR)

If a decision changes, create a new ADR that supersedes the old one.

## Creating a New ADR

1. Copy `template.md` to a new file with the next sequence number
2. Fill in all sections
3. Open a PR for discussion
4. Update status as it progresses through the lifecycle
5. Link from related ADRs and documentation

## ADR Index

### Active ADRs

| Number | Title | Status | Date |
|--------|-------|--------|------|
| [0001](0001-use-httpx-playwright-fallback.md) | Use httpx with Playwright fallback | Implemented | 2025-10-15 |
| [0002](0002-adopt-windsurf-workflow-system.md) | Adopt Windsurf workflow system | Implemented | 2025-10-15 |
| [0003](0003-documentation-standards-and-structure.md) | Documentation standards and structure | Implemented | 2025-10-15 |
| [0004](0004-trafilatura-content-extraction.md) | Use Trafilatura for content extraction | Implemented | 2025-10-15 |
| [0005](0005-hierarchical-semantic-chunking.md) | Hierarchical and semantic chunking | Implemented | 2025-10-15 |
| [0006](0006-chunk-size-and-overlap.md) | 512-token chunks with 50-token overlap | Implemented | 2025-10-15 |
| [0007](0007-tiktoken-token-counting.md) | Use tiktoken for token counting | Implemented | 2025-10-15 |
| [0008](0008-map-reduce-summarization.md) | Map-reduce summarization strategy | Implemented | 2025-10-15 |
| [0009](0009-disk-cache-seven-day-ttl.md) | Disk cache with 7-day TTL | Implemented | 2025-10-15 |
| [0010](0010-openai-gpt4-default-llm.md) | Use OpenAI GPT-4 as default LLM | Superseded | 2025-10-15 |
| [0011](0011-enable-streaming-output.md) | Enable streaming output | Implemented | 2025-10-15 |
| [0012](0012-monolithic-tool-design.md) | Monolithic tool design | Implemented | 2025-10-15 |
| [0013](0013-initiative-documentation-standards.md) | Initiative documentation standards | Implemented | 2025-10-15 |
| [0016](0016-parallel-map-reduce-optimization.md) | Parallel map-reduce for summarization performance | Accepted | 2025-10-15 |
| [0018](0018-workflow-architecture-v3.md) | Workflow architecture v3 - taxonomy and principles | Implemented | 2025-10-18 |
| [0019](0019-initiative-folder-structure-and-naming.md) | Initiative folder structure and date-based naming | Implemented | 2025-10-18 |
| [0020](0020-markdown-quality-automation.md) | Markdown quality automation and regression prevention | Accepted | 2025-10-18 |
| [0021](0021-initiative-system-lifecycle-improvements.md) | Initiative system lifecycle improvements | Accepted | 2025-10-19 |

### Superseded ADRs

| Number | Title | Superseded By | Date |
|--------|-------|---------------|------|
| [0010](0010-openai-gpt4-default-llm.md) | Use OpenAI GPT-4 as default LLM | [0017](0017-switch-default-llm-to-llama3.md) | 2025-10-16 |

### Proposed ADRs

| Number | Title | Status | Date |
|--------|-------|--------|------|
| TBD | PDF extraction library choice | Proposed | TBD |
| TBD | Link scoring algorithm | Proposed | TBD |
| [0017](0017-switch-default-llm-to-llama3.md) | Switch default LLM to Llama 3 via Ollama | Proposed | 2025-10-16 |

## References

- [Architecture Decision Records (ADR)](https://adr.github.io/)
- [Michael Nygard's ADR template](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [Joel Parker Henderson's ADR repo](https://github.com/joelparkerhenderson/architecture-decision-record)
- [AWS Prescriptive Guidance on ADRs](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/welcome.html)
