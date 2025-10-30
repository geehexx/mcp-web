# External Sources

This document contains a summary of the research findings from external sources.

## Windsurf Workflows

*   **Official Documentation:** [https://docs.windsurf.com/windsurf/cascade/workflows](https://docs.windsurf.com/windsurf/cascade/workflows)
*   **Key Findings:**
    *   The official documentation is high-level and does not specify the required frontmatter fields.
    *   The `auto_execution_mode` field is not documented, but it is present in the existing `.unified/**/*.yaml` files. It will be treated as a required field based on the initiative's goals.

## Cursor Rules

*   **Community Notes:** [https://gist.github.com/bossjones/1fd99aea0e46d427f671f853900a0f2a](https://gist.github.com/bossjones/1fd99aea0e46d427f671f853900a0f2a)
*   **Key Findings:**
    *   The key frontmatter fields are `description`, `globs`, and `alwaysApply`.
    *   The `globs` field must be a comma-separated list of file patterns.
    *   The values in the `globs` field should not be quoted.
    *   The combination of `description` and `globs` is supported and enables dual use (agent-discoverable and auto-attaching).
    *   The `alwaysApply: true` setting overrides `globs` and `description` filtering.
