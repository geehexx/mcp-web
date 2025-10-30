# Metadata Removal Playbook

This document outlines the plan for removing redundant sections from the `.unified/**/*.yaml` files. The goal is to reduce token bloat and improve the signal-to-noise ratio of the source files.

| Section to Remove | Rationale | Priority |
|---|---|---|
| `## Command Metadata` | This section duplicates information that is already present in the YAML frontmatter. It adds significant token bloat to every command file. | High |
| `## Rule Metadata` | Similar to the command metadata, this section duplicates frontmatter information and contributes to token bloat in every rule file. | High |
| Boilerplate Context Sections | Many files contain boilerplate sections that explain how to load context or use the workflows. This information can be consolidated into a central guide and removed from the individual files. | Medium |
| Redundant Examples | Some files contain multiple examples that demonstrate the same concept. These can be consolidated to a single, clear example. | Low |
