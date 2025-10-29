# External Sources & References

Authoritative references and community insights informing the unified workflows and rules optimization initiative.

---

## Windsurf

- **Windsurf Docs – Workflows:** `https://docs.windsurf.com/windsurf/cascade/workflows`
  - Confirms workflow storage locations, activation modes, and requirement for `auto_execution_mode`
- **Windsurf Docs – Rules Discovery:** (same doc, Rules section)
  - Details activation modes and best practices for concise rule writing

## Cursor

- **Cursor Docs – Rules:** `https://docs.cursor.com/context/rules` _(use cached/mirrored copy due to redirect restrictions)_
  - Describes MDC format, `description`, `globs`, and `alwaysApply` usage
- **Community Notes – Cursor Rule Behaviour Update (Apr 2025):** `https://gist.github.com/bossjones/1fd99aea0e46d427f671f853900a0f2a`
  - Highlights raw comma-separated glob expectation and advises pruning redundant metadata

## Token Optimization & Structure

- Internal baselines from `.unified/README.md` and existing initiatives (Cursor & Windsurf Dual Compatibility, Testing Excellence)
- OWASP LLM Top 10 (2025) – ensure removal of metadata does not weaken security guidance (link to internal security docs if needed)

---

## Research Tasks

- [ ] Capture cached copy or summary of Cursor docs for repository distribution (respecting allowed domains)
- [ ] Extract key activation mode requirements for Windsurf workflows and include in phase notes
- [ ] Track any additional external references discovered during implementation here
