# Frontmatter Field Matrix

Track which frontmatter fields are required, optional, or forbidden for Windsurf and Cursor after optimization.

---

## Legend

- **R:** Required
- **O:** Optional (allowed but not required)
- **F:** Forbidden (should not appear post-optimization)
- **N/A:** Not applicable to the IDE

---

| Field | Description | Windsurf | Cursor | Notes |
|-------|-------------|----------|--------|-------|
| `description` | Human-readable summary of rule/workflow | **R** | **R** | Single source of truth across IDEs |
| `windsurf.trigger` | Activation mode (`always_on`, `glob`, `model_decision`, `manual`) | **R** | N/A | Drives workflow discovery |
| `windsurf.globs` | Comma-separated glob patterns | **O** | N/A | Required when trigger=`glob` |
| `windsurf.auto_execution_mode` | Numeric execution mode (1-3) | **R** (Workflows) | N/A | Missing field breaks execution |
| `cursor.alwaysApply` | Whether rule is always active | N/A | **O** | Optional when description-based matching sufficient |
| `cursor.globs` | Raw comma-separated globs | N/A | **O** | Use raw string, no YAML list |
| `title` | Legacy title field | **F** | **F** | Redundant with filename |
| `type` | Legacy type indicator | **F** | **F** | Directory structure already conveys |
| `status` | Human-friendly status | **F** | **F** | Track via initiative/docs instead |
| `tags` | Arbitrary tags | **F** | **F** | Remove to reduce token bloat |
| `related` | Related links array | **F** | **F** | Use body content or initiative references |
| `windsurf.type` | Mirrors directory type | **F** | N/A | Redundant |
| `windsurf.complexity` | Relative difficulty | **F** | N/A | Document elsewhere |
| `windsurf.dependencies` | Dependency list | **F** | N/A | Prefer narrative section when needed |
| `cursor.pass_through` | Legacy passthrough flag | N/A | **F** | Not used by current Cursor builds |

---

## Action Items

- Confirm whether any workflows require `auto_execution_mode` ≠ 3 (document exceptions if found)
- If additional optional fields become necessary, update this matrix and schema accordingly
