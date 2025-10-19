# Windsurf Rules Guide

**Purpose:** Reference guide for creating and managing Windsurf rules with correct front-matter.

**Last Updated:** 2025-10-19

---

## Valid Trigger Types

Windsurf rules support **3 trigger types** (verified through IDE implementation):

### 1. `always_on`

**Description:** Rule is always applied to all conversations.

**Use Case:** Core directives, global standards, fundamental principles.

**Front-matter Example:**

```yaml
---
created: "2025-10-15"
updated: "2025-10-19"
trigger: always_on
description: Core agent directives and principles
category: core
tokens: 3200
applyTo:
  - all
priority: high
status: active
---
```

**Examples in this project:**

- `00_agent_directives.md` - Core agent behavior

---

### 2. `model_decision`

**Description:** Model decides whether to apply the rule based on natural language description.

**Use Case:** Context-sensitive rules that should only apply in specific situations.

**Required Fields:**

- `description` - Natural language description for model to evaluate

**Front-matter Example:**

```yaml
---
created: "2025-10-15"
updated: "2025-10-19"
trigger: model_decision
description: Apply when dealing with security-sensitive code including API calls, user input, LLM interactions, file operations, or authentication
category: security
globs:
  - "**/*.py"
  - "**/*.ini"
  - "**/*.yml"
  - "**/*.yaml"
tokens: 1385
applyTo:
  - security
  - api
  - llm
  - authentication
priority: high
status: active
---
```

**Examples in this project:**

- `04_security.md` - Security-sensitive operations
- `05_operational_protocols.md` - Session management protocols
- `06_context_engineering.md` - File and git operations

---

### 3. `glob`

**Description:** Rule applies to files matching glob patterns.

**Use Case:** Language-specific rules, file-type-specific standards.

**Required Fields:**

- `globs` - YAML array of glob patterns

**Front-matter Example:**

```yaml
---
created: "2025-10-15"
updated: "2025-10-18"
trigger: glob
description: Python code style and best practices
globs:
  - "**/*.py"
category: language
tokens: 1549
applyTo:
  - python
  - implementation
priority: high
status: active
---
```

**Examples in this project:**

- `01_testing_and_tooling.md` - Python test files
- `02_python_standards.md` - Python source files
- `03_documentation_lifecycle.md` - Markdown documentation

**Important:** The `globs` field must be a proper YAML array:

```yaml
# ✅ CORRECT
globs:
  - "**/*.py"
  - tests/**/*.py
  - "*.md"

# ❌ WRONG
globs: **/*.py, tests/**/*.py, *.md
```

---

## Common Mistakes

### ❌ Invalid Trigger Types

These are **NOT** valid trigger types:

- `always` ❌ (use `always_on`)
- `manual` ❌ (not supported in current version)
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
| `trigger: always` | `trigger: always_on` |
| `trigger: session_management` | `trigger: always_on` or `model_decision` |
| `trigger: file_operations` | `trigger: always_on` or `model_decision` |
| `trigger: python_files` | `trigger: glob` + `globs: ["**/*.py"]` |
| `trigger: security_sensitive` | `trigger: model_decision` + description |

---

## Frontmatter Fields

### Required Fields

- `trigger` - One of: `always_on`, `model_decision`, `glob`
- `description` - Clear description of rule purpose

### Recommended Fields

- `created` - Creation date in "YYYY-MM-DD" format
- `updated` - Last update date in "YYYY-MM-DD" format
- `category` - Rule category (core, testing, language, documentation, security, operations)
- `tokens` - Estimated token count
- `priority` - Priority level (high, medium, low)
- `status` - Status (active, deprecated, experimental)

### Conditional Fields

- `globs` - Required for `glob` trigger (YAML array of patterns)
- `applyTo` - Optional semantic tags for rule application

### Example Complete Frontmatter

```yaml
---
created: "2025-10-15"
updated: "2025-10-19"
trigger: glob
description: Enforces testing standards, tool usage, and development environment practices.
globs:
  - tests/**/*.py
  - src/**/*.py
  - "*.toml"
  - "*.ini"
  - Taskfile.yml
category: testing
tokens: 989
applyTo:
  - testing
  - implementation
priority: high
status: active
---
```

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

- ✅ Valid trigger type (`always_on`, `model_decision`, `glob`)
- ✅ Required fields for each trigger type
- ✅ YAML front-matter syntax
- ✅ Front-matter structure
- ✅ Glob format (YAML array for `glob` trigger)
- ✅ Created/updated field format

**Example Output:**

```bash
❌ Rules front-matter validation failed:

  • .windsurf/rules/05_operational_protocols.md: Invalid trigger 'session_management'. Must be one of: always_on, glob, model_decision

📖 Valid trigger types: always_on, glob, model_decision
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

- **Global behavior?** → `always_on`
- **File-type specific?** → `glob`
- **Context-dependent?** → `model_decision`

### 3. Provide Clear Descriptions

For `model_decision` triggers, be explicit:

- ✅ **Good:** "Apply when dealing with security-sensitive code including API calls, user input, LLM interactions"
- ❌ **Bad:** "Security stuff"

### 4. Maintain Frontmatter Consistency

Always include `created` and `updated` dates:

- Update `updated` field when modifying rules
- Keep `created` field unchanged
- Use "YYYY-MM-DD" format

### 5. Test Your Rules

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
trigger: [always_on|model_decision|glob]
description: Clear description of when/why this rule applies
globs:  # Only for glob trigger
  - "**/*.ext"
  - path/to/files/**
category: [core|testing|language|documentation|security|operations]
tokens: XXXX
applyTo:
  - context1
  - context2
priority: [high|medium|low]
status: active
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

**Solution:** Use one of the 3 valid trigger types: `always_on`, `model_decision`, `glob`.

### Issue: "Missing required field" error

**Cause:** Trigger type requires additional fields:

- `model_decision` requires `description`
- `glob` requires `globs` array

**Solution:** Add the required field to front-matter.

### Issue: "globs field must be a YAML array" error

**Cause:** Globs specified as comma-separated string instead of YAML array.

**Solution:**

```yaml
# ❌ WRONG
globs: **/*.py, tests/**/*.py

# ✅ CORRECT
globs:
  - "**/*.py"
  - tests/**/*.py
```

### Issue: Rule not loading in Cascade

**Cause:** Malformed YAML front-matter or invalid trigger.

**Solution:**

1. Run validation script: `uv run python scripts/validate_rules_frontmatter.py`
2. Fix any reported errors
3. Restart Windsurf IDE

---

## References

- **Validation Script:** `scripts/validate_rules_frontmatter.py`
- **Pre-commit Hook:** `.pre-commit-config.yaml` (line 112-117)
- **Example Rules:** `.windsurf/rules/*.md`

---

**Maintained By:** mcp-web core team
**Version:** 2.0.0
**Last Validated:** 2025-10-19
