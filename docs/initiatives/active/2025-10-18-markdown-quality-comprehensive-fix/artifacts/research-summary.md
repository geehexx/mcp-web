# Markdown Validation Research Summary

**Date:** 2025-10-18
**Research Focus:** Best practices for markdown validation, tool comparison, and regression prevention strategies

## Executive Summary

**Recommended Approach:** Continue with markdownlint-cli2 as primary linter, add pytest-based quality tests, enhance pre-commit hooks, and optionally evaluate Vale for prose quality.

**Key Findings:**

1. markdownlint-cli2 is the industry standard (2025) for markdown linting
2. Auto-fix capabilities handle 80% of common violations
3. Code fence language specifiers (MD040) are critical for accessibility and UX
4. Pre-commit hooks + CI checks provide best regression prevention
5. Automated tests can verify markdown quality programmatically

---

## Tool Comparison Matrix

### Primary Linters Evaluated

| Tool | Status (2025) | Auto-fix | Custom Rules | Pros | Cons | Verdict |
|------|---------------|----------|--------------|------|------|---------|
| **markdownlint-cli2** | ✅ Active | ✅ Yes | ✅ Yes | Modern, fast, good ecosystem | Learning curve | ✅ **Primary** |
| markdownlint-cli | ⚠️ Maintenance | ✅ Yes | ✅ Yes | Simple, reliable | Less features | ✅ Backup |
| remark-lint | ✅ Active | ✅ Yes | ✅ Yes | AST-based, powerful | More complex | ⏸️ Optional |
| Vale | ✅ Active | ❌ No | ✅ Yes | Prose quality, style guide enforcement | Different focus | ⏸️ Phase 2 |

### Detailed Tool Analysis

#### markdownlint-cli2 ✅ **RECOMMENDED**

**Repository:** https://github.com/DavidAnson/markdownlint-cli2
**Stars:** ~1.2k (as of Oct 2025)
**Last Update:** Active (monthly releases)
**Language:** Node.js/JavaScript

**Strengths:**

- ✅ Modern architecture built on markdownlint library
- ✅ Excellent glob pattern support
- ✅ Custom rules via JavaScript modules
- ✅ Multiple output formats (JSON, SARIF, etc.)
- ✅ Built-in auto-fix for 24+ rules
- ✅ Configuration via multiple file formats (JSONC, YAML, JS)
- ✅ Pre-commit hook support (official)
- ✅ Docker image available

**Limitations:**

- ⚠️ Requires Node.js runtime
- ⚠️ Configuration can be complex for advanced use cases

**Current Usage:**

- Already integrated via `.markdownlint-cli2.jsonc`
- Pre-commit hook configured
- Taskfile commands available

**Verdict:** **Keep as primary tool**

---

#### markdownlint-cli (Legacy) ✅ **BACKUP**

**Repository:** https://github.com/igorshubovych/markdownlint-cli
**Status:** Maintenance mode (superseded by cli2)

**Strengths:**

- ✅ Simple, straightforward
- ✅ Clear error reporting
- ✅ Reliable for basic linting

**Limitations:**

- ⚠️ Fewer features than cli2
- ⚠️ Less active development

**Verdict:** **Use for validation/comparison only**

---

#### remark-lint ⏸️ **OPTIONAL**

**Repository:** https://github.com/remarkjs/remark-lint
**Stars:** ~1k
**Status:** Active (unified.js ecosystem)

**Strengths:**

- ✅ AST-based analysis (more powerful)
- ✅ Part of unified.js ecosystem
- ✅ Extensive plugin ecosystem
- ✅ Can transform markdown (not just lint)

**Limitations:**

- ⚠️ More complex setup
- ⚠️ Different philosophy (transformation vs validation)
- ⚠️ Steeper learning curve

**Comparison to markdownlint:**

- See https://github.com/remarkjs/remark-lint/blob/main/doc/comparison-to-markdownlint.md
- Most rules have equivalents between both tools
- markdownlint is more prescriptive, remark-lint more flexible

**Verdict:** **Not needed** - markdownlint-cli2 sufficient for our use case

---

#### Vale ⏸️ **EVALUATE IN PHASE 2**

**Repository:** https://github.com/errata-ai/vale
**Stars:** ~4k+
**Status:** Active, well-maintained
**Language:** Go

**Purpose:** Prose quality and style guide enforcement (different from structural linting)

**Strengths:**

- ✅ Enforces style guides (Google, Microsoft, write-good, etc.)
- ✅ Checks grammar, spelling, readability
- ✅ Custom style rules
- ✅ Multiple format support (Markdown, AsciiDoc, reStructuredText, HTML)
- ✅ CI/CD integration

**Limitations:**

- ⚠️ Different focus (prose vs structure)
- ⚠️ Requires style guide configuration
- ⚠️ Can be noisy without tuning

**Use Case:** Complement to markdownlint for documentation quality

**Verdict:** **Evaluate if prose quality is priority** - Not essential for current issue

---

## Best Practices Research (2025)

### Code Fence Language Specifiers (MD040)

**Source:** [CommonMark Spec](https://spec.commonmark.org/)

**Why it matters:**

1. **Accessibility:** Screen readers use language hints
2. **Syntax Highlighting:** GitHub, IDE renderers use language for highlighting
3. **Code Analysis:** Tools can analyze code blocks with language context
4. **SEO:** Search engines use language hints for indexing

**Recommended language specifiers:**

| Content Type | Language Specifier | Notes |
|--------------|-------------------|-------|
| Shell commands | `bash`, `sh`, `zsh` | Use `bash` as default |
| Command output | `text` | Plain text, no highlighting |
| Configuration files | `yaml`, `json`, `toml`, `ini` | Match file type |
| Python code | `python` | Standard identifier |
| Markdown examples | `markdown` | For nested markdown |
| Directory trees | `text` | Or custom language |
| Logs | `text` | Or `log` if supported |
| Empty/placeholder | `text` | Never leave blank |

**Reference:** https://github.com/DavidAnson/markdownlint/blob/main/doc/md040.md

---

### Blank Lines Around Elements (MD022, MD031, MD032)

**Source:** [GitHub Flavored Markdown Spec](https://github.github.com/gfm/)

**Rationale:**

1. **Parser Compatibility:** Some parsers (kramdown) require blank lines
2. **Readability:** Visual separation improves scanning
3. **Consistency:** Uniform spacing reduces cognitive load

**Best practices:**

```markdown
# Correct: Headings with blank lines

Some text here.

## Subheading

More text.

# Correct: Lists with blank lines

Some paragraph.

- List item 1
- List item 2

Another paragraph.

# Correct: Code fences with blank lines

Some text.

```bash
code here
```

More text.

```

---

### Pre-commit Hook Strategies (2025)

**Source:** [Pre-commit Hooks Best Practices](https://gatlenculp.medium.com/effortless-code-quality-the-ultimate-pre-commit-hooks-guide-for-2025-57ca501d9835)

**Recommended approach:**
1. ✅ Use official pre-commit framework (https://pre-commit.com/)
2. ✅ Enable auto-fix where safe (`--fix` flag)
3. ✅ Run hooks in CI to catch bypassed commits
4. ✅ Use `fail_fast: false` for better developer experience
5. ✅ Pin versions for reproducibility

**Current implementation:**
```yaml
# .pre-commit-config.yaml
- repo: https://github.com/DavidAnson/markdownlint-cli2
  rev: v0.18.1
  hooks:
    - id: markdownlint-cli2-docker
      name: "📝 markdown · Lint with markdownlint-cli2 (Docker)"
      args: [--fix, --config, .markdownlint-cli2.jsonc]
      exclude: ^(node_modules/|\.venv/|docs/archive/)
```

**Strengths:**

- ✅ Auto-fix enabled
- ✅ Configuration specified
- ✅ Archive excluded

**Gaps:**

- ⚠️ Docker version may have performance overhead
- ⚠️ Not enforced in CI
- ⚠️ Can be bypassed with `git commit --no-verify`

---

## Regression Prevention Strategies

### Multi-Layer Defense

```
Layer 1: IDE/Editor Integration
    ↓
Layer 2: Pre-commit Hooks (Client-side)
    ↓
Layer 3: CI Checks (Server-side)
    ↓
Layer 4: Automated Tests (Quality Gates)
```

### Layer 1: IDE Integration

**Tools:**

- VS Code: `DavidAnson.vscode-markdownlint` extension
- JetBrains: Built-in markdown support
- Vim/Neovim: ALE, coc-markdownlint

**Benefits:** Immediate feedback while editing

---

### Layer 2: Pre-commit Hooks ✅ **IMPLEMENTED**

**Current Status:** Configured but can be bypassed

**Enhancement opportunities:**

1. Add non-Docker version for speed (fallback to Docker if not available)
2. Add hook success/failure reporting
3. Consider `--strict` flag to block on any violations

---

### Layer 3: CI Checks ⚠️ **MISSING**

**Recommendation:** Add GitHub Actions workflow

**Example workflow:**

```yaml
name: Documentation Quality

on: [push, pull_request]

jobs:
  markdown-lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run markdownlint
        uses: DavidAnson/markdownlint-cli2-action@v18
        with:
          globs: '**/*.md'
          config: '.markdownlint-cli2.jsonc'
          fix: false  # Don't auto-fix in CI, just report
```

**Benefits:**

- Catches violations even if pre-commit bypassed
- Prevents merging of invalid markdown
- Provides PR comments with violations

**Note:** This is different from prose quality checks (Vale)

---

### Layer 4: Automated Tests ⚠️ **MISSING**

**Recommendation:** Add pytest-based markdown quality tests

**Example implementation:**

```python
# tests/test_markdown_quality.py
import subprocess
from pathlib import Path

def test_markdown_lint():
    """Verify all markdown files pass linting."""
    result = subprocess.run(
        ["npx", "markdownlint-cli2", "**/*.md"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Markdown linting failed:\n{result.stdout}"

def test_code_fences_have_language():
    """Verify all code fences have language specifiers."""
    # Parse markdown files and check for empty code fences
    for md_file in Path(".").rglob("*.md"):
        if "archive" in str(md_file) or "node_modules" in str(md_file):
            continue

        content = md_file.read_text()
        lines = content.split("\n")

        for i, line in enumerate(lines):
            if line.strip() == "```":
                assert False, f"{md_file}:{i+1} - Code fence missing language specifier"
```

**Benefits:**

- Programmatic verification
- Can be run in CI
- Provides clear pass/fail status
- Can test specific rules in isolation

---

## Configuration Best Practices

### markdownlint Configuration Hierarchy

1. **Command-line args** (highest precedence)
2. **Configuration file** (`.markdownlint-cli2.jsonc`)
3. **Defaults** (lowest precedence)

### Recommended Configuration Pattern

```jsonc
{
  // Use custom rules for project-specific needs
  "customRules": ["./.markdownlint/custom-rules.cjs"],

  // Format errors as JSON for CI parsing
  "outputFormatters": [
    ["markdownlint-cli2-formatter-json", "/tmp/markdownlint.json"]
  ],

  // Exclude patterns (be specific)
  "ignores": [
    "docs/archive/**",
    "**/.pytest_cache/**",
    "**/node_modules/**"
  ],

  // Rule configuration
  "config": {
    "default": true,  // Enable all rules by default

    // Override specific rules
    "MD013": {
      "line_length": 280,  // Adjusted for technical docs
      "code_blocks": false  // Don't check code blocks
    },

    "MD040": true,  // ENFORCE code fence languages

    "MD033": {
      "allowed_elements": ["br", "details", "summary"]  // Allow specific HTML
    }
  }
}
```

---

## Markdown Quality Checklist

### Pre-commit Checklist

- [ ] All code fences have language specifiers
- [ ] Lists surrounded by blank lines
- [ ] Headings surrounded by blank lines
- [ ] No trailing whitespace
- [ ] No multiple consecutive blank lines
- [ ] Links are descriptive (not "click here")

### Code Fence Language Reference

```markdown
# Shell commands
```bash
npm install
```

# Command output

```text
Installing packages...
Done.
```

# Configuration

```yaml
key: value
```

# Code samples

```python
def hello():
    print("Hello")
```

# Directory trees

```text
src/
├── index.js
└── utils.js
```

```

---

## Decision Matrix

### Should we add Vale?

| Criterion | Score | Notes |
|-----------|-------|-------|
| **Need** | Low | Current issue is structural, not prose |
| **ROI** | Medium | Would improve prose quality long-term |
| **Complexity** | Medium | Requires style guide configuration |
| **Maintenance** | Low | Once configured, minimal maintenance |

**Recommendation:** **Defer to Phase 2 evaluation** - Focus on structural issues first

**If adding Vale:**
- Start with write-good style (general prose)
- Add project-specific terminology rules
- Configure `.vale.ini` with appropriate styles
- Add to pre-commit hooks
- Document exceptions/overrides

---

## References & Further Reading

### Official Documentation
- [markdownlint Rules](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md)
- [markdownlint-cli2 README](https://github.com/DavidAnson/markdownlint-cli2)
- [CommonMark Specification](https://spec.commonmark.org/0.31.2/)
- [GitHub Flavored Markdown Spec](https://github.github.com/gfm/)

### Best Practices Guides
- [Markdown Style Guide (Google)](https://google.github.io/styleguide/docguide/style.html)
- [Markdown Style Guide (Ciro Santilli)](https://cirosantilli.com/markdown-style-guide)
- [Pre-commit Hooks Guide 2025](https://gatlenculp.medium.com/effortless-code-quality-the-ultimate-pre-commit-hooks-guide-for-2025-57ca501d9835)

### Tool Documentation
- [Vale Documentation](https://vale.sh/docs/)
- [remark-lint Documentation](https://github.com/remarkjs/remark-lint)
- [Pre-commit Framework](https://pre-commit.com/)

### Articles
- [Markdown Auto-fix Implementation](https://dlaa.me/blog/post/markdownlintfixinfo)
- [Markdownlint Rules Comparison](https://github.com/remarkjs/remark-lint/blob/main/doc/comparison-to-markdownlint.md)

---

## Conclusion

**Primary Recommendation:**
Continue with markdownlint-cli2 as the primary linting tool, enhance pre-commit hooks, add CI checks, and implement automated tests for regression prevention.

**Phase 2 Decision Points:**
1. Vale integration: Evaluate after structural issues resolved
2. CI workflow: Add GitHub Actions for markdown quality
3. Test suite: Implement pytest-based markdown quality tests

**Success Metrics:**
- Zero markdown linting errors
- Pre-commit hooks catch 100% of new violations
- CI blocks invalid markdown from merging
- Automated tests verify quality gates
