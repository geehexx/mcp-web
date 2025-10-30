---
description: "Documentation of Cursor IDE rule application logic and configuration"
status: "active"
tags: ["cursor", "documentation", "rules", "system"]
type: "rule"

windsurf:
  trigger: "model_decision"

cursor:
  alwaysApply: false

ide:
  hidden_sections:
    - "Rule Metadata"
  metadata:
    file: "09_cursor_rule_system.md"
    trigger: "manual (Windsurf) / alwaysApply: false (Cursor)"
    estimated_tokens: 1200
    last_updated: "2025-10-22"
    status: "Active"
    topics_covered:
      - "Cursor rule application logic"
      - "Transformation from Windsurf"
      - "Best practices"
      - "Troubleshooting"
    workflow_references:
      - "All workflows (for understanding rule application)"
    dependencies:
      - "Source: Cursor IDE documentation"
---
# Cursor Rule System Documentation

## Rule Application Logic

Cursor IDE applies rules based on the following logic:

### 1. Always Applied Rules

```yaml
---
alwaysApply: true
description: "Rule description"
---
```

- **Behavior**: Rule is automatically loaded in every session
- **Use Case**: Core directives, fundamental principles
- **Example**: Core agent directives, mention guidance

### 2. File-Based Rules

```yaml
---
alwaysApply: false
globs: "*.py, **/*.py"
description: "Rule description"
---
```

- **Behavior**: Rule is automatically applied when editing files matching the glob patterns
- **Use Case**: Language-specific rules, file type guidelines
- **Example**: Python code standards, testing guidelines
- **Globs Format**: Raw, unquoted comma-separated patterns

### 3. Intelligent Application Rules

```yaml
---
alwaysApply: false
description: "Rule description"
---
```

- **Behavior**: Cursor uses the rule's description to intelligently determine when to apply the rule
- **Use Case**: Context-aware rules, conditional guidelines
- **Example**: Security practices, context optimization
- **Logic**: Cursor analyzes the description and applies the rule when it determines the context is relevant

### 4. Manual Reference Rules

```yaml
---
alwaysApply: false
description: "Rule description"
---
```

- **Behavior**: Rule is only applied when manually referenced
- **Use Case**: Specialized rules, documentation
- **Example**: System documentation, IDE-specific guidance

## Transformation from Windsurf

### Trigger Mode Mapping

| Windsurf Trigger | Cursor Configuration |
|------------------|---------------------|
| `always_on` | `alwaysApply: true` |
| `glob` | `alwaysApply: false` + `globs: "pattern"` |
| `model_decision` | `alwaysApply: false` (no globs, intelligent application) |
| `manual` | `alwaysApply: false` (no globs, manual reference) |

### Globs Format

- **Windsurf**: `globs: "*.py, **/*.py"` (comma-separated string)
- **Cursor**: `globs: "*.py, **/*.py"` (same format, raw unquoted)

### Description Usage

- **Windsurf**: Description used for documentation and manual reference
- **Cursor**: Description used for intelligent application when `alwaysApply: false` and no `globs` present

## Best Practices

### Rule Design

1. **Clear Descriptions**: Write descriptive rule descriptions that clearly indicate when the rule should apply
2. **Specific Patterns**: Use specific glob patterns for file-based rules
3. **Logical Grouping**: Group related functionality in single rules
4. **Avoid Overlap**: Ensure rules don't conflict or overlap unnecessarily

### Performance Considerations

1. **Minimal Always-On Rules**: Limit the number of always-applied rules to essential ones only
2. **Efficient Globs**: Use efficient glob patterns that don't match too many files
3. **Clear Descriptions**: Write clear descriptions to help Cursor's intelligent application

### Testing Rules

1. **Verify Application**: Test that rules apply when expected
2. **Check Non-Application**: Ensure rules don't apply when they shouldn't
3. **Validate Content**: Verify rule content is accurate and helpful

## Common Patterns

### Language-Specific Rules

```yaml
---
alwaysApply: false
globs: "*.py, **/*.py"
description: "Python code standards and best practices"
---
```

### Security Rules

```yaml
---
alwaysApply: false
description: "Apply when dealing with security-sensitive code including API calls, user input, LLM interactions, and authentication"
---
```

### Documentation Rules

```yaml
---
alwaysApply: false
globs: "*.md, docs/**/*.md"
description: "Documentation standards and formatting guidelines"
---
```

### Context-Aware Rules

```yaml
---
alwaysApply: false
description: "Apply when dealing with large files, complex operations, or memory-intensive tasks"
---
```

## Troubleshooting

### Rule Not Applying

1. **Check Format**: Verify YAML frontmatter is correct
2. **Verify Globs**: Ensure glob patterns are correct and match target files
3. **Check Description**: Ensure description is clear and relevant
4. **Test Manually**: Try manually referencing the rule

### Rule Applying Too Often

1. **Refine Globs**: Make glob patterns more specific
2. **Improve Description**: Make description more specific about when to apply
3. **Check Logic**: Verify the rule logic is correct

### Performance Issues

1. **Reduce Always-On Rules**: Minimize rules with `alwaysApply: true`
2. **Optimize Globs**: Use more efficient glob patterns
3. **Review Content**: Ensure rule content is concise and relevant

## Rule Metadata

**File:** `09_cursor_rule_system.yaml`
**Trigger:** manual (Windsurf) / alwaysApply: false (Cursor)
**Estimated Tokens:** ~1,200
**Last Updated:** 2025-10-22
**Status:** Active

**Topics Covered:**
- Cursor rule application logic
- Transformation from Windsurf
- Best practices
- Troubleshooting

**Workflow References:**
- All workflows (for understanding rule application)

**Dependencies:**
- Source: Cursor IDE documentation
