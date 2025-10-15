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

```
NNNN-verb-noun-phrase.md
```

Examples:
- `0001-use-httpx-playwright-fallback.md`
- `0002-use-trafilatura-extraction.md`
- `0003-implement-map-reduce-summarization.md`

## Lifecycle

```
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
| [0002](0002-use-trafilatura-extraction.md) | Use trafilatura for content extraction | Implemented | 2025-10-15 |
| [0003](0003-use-hierarchical-chunking.md) | Use hierarchical + semantic chunking | Implemented | 2025-10-15 |
| [0004](0004-set-chunk-size-512-tokens.md) | Set default chunk size to 512 tokens | Implemented | 2025-10-15 |
| [0005](0005-use-tiktoken-counting.md) | Use tiktoken for token counting | Implemented | 2025-10-15 |
| [0006](0006-implement-map-reduce-summarization.md) | Implement map-reduce summarization | Implemented | 2025-10-15 |
| [0007](0007-use-disk-cache-7day-ttl.md) | Use disk cache with 7-day TTL | Implemented | 2025-10-15 |
| [0008](0008-default-to-gpt4-openai.md) | Default to GPT-4 as LLM | Implemented | 2025-10-15 |
| [0009](0009-enable-streaming-output.md) | Enable streaming output | Implemented | 2025-10-15 |
| [0010](0010-use-monolithic-tool-design.md) | Use monolithic tool design | Implemented | 2025-10-15 |

### Superseded ADRs

None yet.

### Proposed ADRs

| Number | Title | Status | Date |
|--------|-------|--------|------|
| TBD | PDF extraction library choice | Proposed | TBD |
| TBD | Link scoring algorithm | Proposed | TBD |

## References

- [Architecture Decision Records (ADR)](https://adr.github.io/)
- [Michael Nygard's ADR template](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [Joel Parker Henderson's ADR repo](https://github.com/joelparkerhenderson/architecture-decision-record)
- [AWS Prescriptive Guidance on ADRs](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/welcome.html)
