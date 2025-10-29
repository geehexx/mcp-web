# Metadata Removal Playbook

Document redundant sections and fields targeted for removal from unified workflows and rules.

---

## Section Removal Targets

| Section Heading | Rationale | Replacement / Action | Phase |
|-----------------|-----------|-----------------------|-------|
| `## Command Metadata` / `## Rule Metadata` | Duplicates YAML frontmatter details; adds 100–300 tokens | Remove section entirely | Phase 4 |
| `## Workflow References` | Execution context already implies referenced workflows | Remove or condense into single bullet if unique information exists | Phase 4 |
| `## Integration` (generic text) | Boilerplate repeated across workflows; low informational value | Remove; document integration guidance in central guide if needed | Phase 4 |
| Context loading block (“Load these rules if you determine you need them…”) | Repetitive instructions in every workflow | Replace with single concise sentence referencing `/rules/` directory | Phase 4 |
| Generic `## Anti-Patterns` lists | Duplicates same checklist across files | Move to consolidated documentation or remove if redundant | Phase 4 |

---

## Frontmatter Field Removals

| Field | Reason for Removal | Notes |
|-------|--------------------|-------|
| `title` | Duplicated by filename | Remove globally |
| `type` | Implied by directory structure | Remove globally |
| `status` | Tracked in initiative docs | Remove globally |
| `tags` | Unused by IDEs; adds noise | Remove globally |
| `related` | Better handled via initiative references | Remove globally |
| `windsurf.type` / `windsurf.category` / `windsurf.complexity` / `windsurf.dependencies` | Redundant metadata or empty arrays | Remove across workflows |
| `cursor.pass_through` | Not used by current Cursor versions | Remove |

---

## Execution Notes

- Maintain audit trail: record actual removals and token savings in Phase 4 exit report and `artifacts/token-inventory.md`.
- If a workflow requires a specific warning or compliance statement, keep it but tighten wording to reduce tokens.
- Update this playbook after Phase 4 to reflect actual changes and any exceptions granted.
