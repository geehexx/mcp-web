---
Status: "Deferred"
Created: "2025-10-23"
Owner: "@ai-agent"
Priority: "medium"
Estimated Duration: "1-2 weeks"
Target Completion: ""
Tags: ["documentation", "automation", "agents-md", "summarizer"]
Related:
  - "docs/initiatives/active/2025-10-22-local-summarizer-integration.md"
---

# Initiative: Automate AGENTS.md Generation with Local Summarizer

## Objective

Automate the generation of AGENTS.md using the local summarizer to create high-quality, human-readable content from the .unified rules and commands.

## Sequencing

This initiative is **deferred** and is dependent on the completion of the "Local Summarizer Integration" initiative. It should not be started until the local summarizer is fully functional and available for use in automation scripts.

## Success Criteria

- [ ] The AGENTS.md file is automatically generated and is of high quality.
- [ ] The generation process is integrated into the pre-commit hooks.
- [ ] The generated content is more comprehensive than a simple list of rules and commands.
- [ ] The documentation is treated like code, with version control, code review, and CI/CD integration.

## Motivation

**Problem:** Manually maintaining AGENTS.md is time-consuming and prone to inconsistencies. The current manual version is a temporary solution.

**Impact:** Automating the generation of AGENTS.md will ensure it is always up-to-date and accurately reflects the agent's capabilities.

**Value:** Frees up developer time, improves documentation quality, and provides a reliable source of truth for agent capabilities.

## Scope

### In Scope

- Development of a Python script that uses the local summarizer to generate content for AGENTS.md.
- Integration of the script into the pre-commit hooks to ensure the file is always up-to-date.
- The generated content will include summaries of rules and commands, not just a direct transcription of their titles and descriptions.
- The script will be designed to be run as part of a CI/CD pipeline.

### Out of Scope

- Development of the local summarizer itself. This initiative is dependent on the completion of that work.
- Any changes to the `.unified` rules and commands beyond what is necessary to support the generation of `AGENTS.md`.

## Tasks

### Phase 1: Research and Design (1-2 days)

- [ ] Investigate the API and capabilities of the local summarizer.
- [ ] Design the structure and content of the `AGENTS.md` file to be generated, incorporating best practices for automated documentation.
- [ ] Define the prompts and inputs to be used with the local summarizer to generate the desired content.
- [ ] Create a detailed design document for the generation script.

### Phase 2: Implementation (3-5 days)

- [ ] Develop the Python script to generate the `AGENTS.md` file.
- [ ] Implement the logic for calling the local summarizer and processing its output.
- [ ] Add a `--check` mode to the script for use in pre-commit hooks.
- [ ] Add a `--force` mode to the script for overwriting the existing file.
- [ ] Add logging and error handling to the script.

### Phase 3: Integration and Testing (2-3 days)

- [ ] Add the new script to the `.pre-commit-config.yaml` file.
- [ ] Write unit tests for the generation script.
- [ ] Manually test the end-to-end process to ensure it works as expected.
- [ ] Integrate the script into the CI/CD pipeline.

## Dependencies

**Internal Dependencies:**

- Completion of the local summarizer initiative.

## Risks and Mitigation

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| The local summarizer is not powerful enough to generate high-quality content. | High | Medium | Fall back to a simpler, template-based generation approach. |
| The generation process is too slow to be used in a pre-commit hook. | Medium | Low | Optimize the script and the summarizer prompts. Run the full generation in a nightly build and have the pre-commit hook check against a cached version. |
| The generated content is not as good as the manually written version. | High | Medium | Involve human review in the generation process. The script could generate a draft that is then reviewed and edited by a human. |

## Timeline

- **Week 1:** Complete Phase 1 (Research and Design).
- **Week 2:** Complete Phase 2 (Implementation).
- **Week 3:** Complete Phase 3 (Integration and Testing).
