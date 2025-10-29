# Hidden Section Mapping

Track relationships between removed markdown sections and the structured frontmatter
fields that preserve their guidance for IDE adapters.

---

## Legend

- **Section Heading**: Markdown heading removed from `.unified/` content
- **Frontmatter Field**: Destination key in structured metadata
- **Notes**: Additional handling instructions (e.g., whitespace trimming, adapter expectations)

---

## Planned Migrations

| Section Heading | Frontmatter Field | Notes |
|-----------------|-------------------|-------|
| `## Command Metadata` | `ide.hidden_sections` | Store heading name so adapters suppress section while retaining reference |
| `## Rule Metadata` | `ide.hidden_sections` | Same as above; list per workflow to ensure regression tests cover removal |
| `## Workflow References` | `ide.metadata.workflow_refs` | Encode concise list of referenced workflows; adapters can surface when needed |
| `## Integration` | `ide.metadata.integration_notes` | Preserve unique integration steps without rendering boilerplate |
| `Context Loading` block | `ide.metadata.context_loading` | Capture canonical sentence referencing `/rules/` directory |
| `## Anti-Patterns` (generic) | `ide.hidden_sections` | Only record when content is duplicated elsewhere; bespoke warnings stay in body |

---

## Execution Checklist

- [ ] Update this table as sections are removed during Phase 4 batches
- [ ] Ensure every entry has matching coverage in adapter tests and goldens
- [ ] Verify adapters read `ide.hidden_sections` / `ide.metadata` when generating `.windsurf/` and `.cursor/`
- [ ] Record token deltas in `artifacts/token-inventory.md`
- [ ] Document any exceptions or preserved sections with rationale

---

## Follow-up Items

- Automate validation that every removed heading is captured in frontmatter metadata.
- Consider adding schema rules that enforce allowed keys under `ide.metadata`.
