# Windsurf Rules Guide

**Purpose:** Reference guide for creating and managing Windsurf rules with correct front-matter.

**Last Updated:** 2025-10-19

---

## Valid Trigger Types

Windsurf rules support **4 trigger types** (per [official documentation](https://docs.windsurf.com/windsurf/cascade/memories)):

### 1. `always`

**Description:** Rule is always applied to all conversations.

**Use Case:** Core directives, global standards, fundamental principles.

**Front-matter Example:**

```yaml
---
trigger: always
description: Core agent directives and principles
category: core
---
```

**Examples in this project:**

- `00_agent_directives.md` - Core agent behavior
- `05_operational_protocols.md` - Session management protocols
- `06_context_engineering.md` - File and git operations

---

### 2. `model_decision`

**Description:** Model decides whether to apply the rule based on natural language description.

**Use Case:** Context-sensitive rules that should only apply in specific situations.

**Required Fields:**

- `description` - Natural language description for model to evaluate

**Front-matter Example:**

```yaml
---
trigger: model_decision
description: Apply when dealing with security-sensitive code including API calls, user input, LLM interactions, file operations, or authentication
category: security
---
```

**Examples in this project:**

- `04_security.md` - Security-sensitive operations

---

### 3. `glob`

**Description:** Rule applies to files matching glob patterns.

**Use Case:** Language-specific rules, file-type-specific standards.

**Required Fields:**

- `globs` - List of glob patterns (e.g., `["**/*.py", "tests/**/*.py"]`)

**Front-matter Example:**

```yaml
---
trigger: glob
description: Python code style and best practices
globs: ["**/*.py"]
category: language
---
```

**Examples in this project:**

- `01_testing_and_tooling.md` - Python test files
- `02_python_standards.md` - Python source files
- `03_documentation_lifecycle.md` - Markdown documentation

---

### 4. `manual`

**Description:** Rule is activated manually via `@mention` in Cascade.

**Use Case:** Optional rules, specialized workflows, context-specific guidance.

**Front-matter Example:**

```yaml
---
trigger: manual
description: Advanced debugging techniques
category: debugging
---
```

**Usage:** Type `@rule-name` in Cascade to activate.

---

## Common Mistakes

### ❌ Invalid Trigger Types

These are **NOT** valid trigger types:

- `session_management` ❌
- `file_operations` ❌
- `security_sensitive` ❌
- `python_files` ❌
- `documentation` ❌
- Any custom string ❌

**Why?** Windsurf IDE enforces these trigger types at the UI level. Custom trigger types will be rejected.

### ✅ Correct Approach

Instead of inventing trigger types, use the valid ones:

| Invalid | Correct |
|---------|---------|
| `trigger: session_management` | `trigger: always` |
| `trigger: file_operations` | `trigger: always` |
| `trigger: python_files` | `trigger: glob` + `globs: ["**/*.py"]` |
| `trigger: security_sensitive` | `trigger: model_decision` + description |

---

## Validation

### Pre-commit Hook

This project includes automatic validation via pre-commit hook:

```bash
# Runs automatically on commit
git commit -m "fix: update rules"

# Run manually
uv run python scripts/validate_rules_frontmatter.py
```

### Validation Script

**Location:** `scripts/validate_rules_frontmatter.py`

**Checks:**

- ✅ Valid trigger type (`always`, `model_decision`, `glob`, `manual`)
- ✅ Required fields for each trigger type
- ✅ YAML front-matter syntax
- ✅ Front-matter structure

**Example Output:**

```bash
❌ Rules front-matter validation failed:

  • .windsurf/rules/05_operational_protocols.md: Invalid trigger 'session_management'. Must be one of: always, glob, manual, model_decision

📖 Valid trigger types: always, glob, manual, model_decision
📚 Reference: https://docs.windsurf.com/windsurf/cascade/memories
```

---

## Best Practices

### 1. Keep Rules Focused

Each rule should have a single, clear purpose:

- ✅ **Good:** `02_python_standards.md` - Python-specific standards
- ❌ **Bad:** `everything.md` - All standards in one file

### 2. Use Appropriate Triggers

Choose the most specific trigger type:

- **Global behavior?** → `always`
- **File-type specific?** → `glob`
- **Context-dependent?** → `model_decision`
- **Optional/specialized?** → `manual`

### 3. Provide Clear Descriptions

For `model_decision` triggers, be explicit:

- ✅ **Good:** "Apply when dealing with security-sensitive code including API calls, user input, LLM interactions"
- ❌ **Bad:** "Security stuff"

### 4. Test Your Rules

After creating/modifying rules:

```bash
# Validate front-matter
uv run python scripts/validate_rules_frontmatter.py

# Test in Cascade
# Open Cascade and verify rule is loaded correctly
```

---

## Rule File Template

```markdown
---
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
trigger: [always|model_decision|glob|manual]
description: Clear description of when/why this rule applies
category: [core|testing|language|documentation|security|operations]
globs: ["**/*.ext"]  # Only for glob trigger
tokens: XXXX  # Optional: estimated token count
applyTo: [context1, context2]  # Optional: semantic tags
priority: [high|medium|low]  # Optional
status: active  # Optional
---

# Rule: [Name]

## Purpose

Clear statement of what this rule governs.

## Content

Detailed rule content...
```

---

## Troubleshooting

### Issue: "Invalid trigger type" error

**Cause:** Using a custom trigger type not supported by Windsurf.

**Solution:** Use one of the 4 valid trigger types: `always`, `model_decision`, `glob`, `manual`.

### Issue: "Missing required field" error

**Cause:** Trigger type requires additional fields:

- `model_decision` requires `description`
- `glob` requires `globs` array

**Solution:** Add the required field to front-matter.

### Issue: Rule not loading in Cascade

**Cause:** Malformed YAML front-matter or invalid trigger.

**Solution:**

1. Run validation script: `uv run python scripts/validate_rules_frontmatter.py`
2. Fix any reported errors
3. Restart Windsurf IDE

---

## References

- **Official Documentation:** [Windsurf Memories & Rules](https://docs.windsurf.com/windsurf/cascade/memories)
- **Validation Script:** `scripts/validate_rules_frontmatter.py`
- **Pre-commit Hook:** `.pre-commit-config.yaml` (line 112-117)
- **Example Rules:** `.windsurf/rules/*.md`

---

**Maintained By:** mcp-web core team
**Version:** 1.0.0
**Last Validated:** 2025-10-19
