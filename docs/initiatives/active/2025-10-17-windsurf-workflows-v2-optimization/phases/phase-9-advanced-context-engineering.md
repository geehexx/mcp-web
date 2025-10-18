# Phase 9: Advanced Context Engineering

**Status:** 🆕 New Phase (from gap analysis)
**Priority:** LOW (post-launch optimization)
**Duration:** 10-15 hours
**Owner:** AI Agent

---

## Objective

Implement modular instruction patterns for context-specific rule loading, achieving additional token reduction through advanced context engineering.

**Target:** Additional 10-20% token reduction via selective rule loading

---

## Background

**Industry Best Practice** (GitHub, 2025):

- Apply only relevant instructions via YAML frontmatter
- Use `applyTo` syntax for context-specific rules
- Reduces context pollution, improves AI focus

**Gap #5:** Current system loads all rules always. Opportunity exists for selective loading based on task context.

---

## Tasks

### Task 9.1: Research Modular Instruction Patterns (Gap #5)

**Purpose:** Study industry practices and Windsurf-specific implementation

#### 9.1.1: Research `applyTo` Syntax

**Research Questions:**

- How does GitHub Copilot implement `applyTo` frontmatter?
- Does Windsurf support `applyTo` syntax?
- Is this equivalent to glob patterns?
- What context types are supported?
- How are contexts detected automatically?
- What are best practices for rule scoping?

**Sources to Research:**

- Windsurf documentation: https://docs.windsurf.com/
- GitHub Copilot agent configuration
- Community examples and patterns

**Deliverable:** Research summary document

**Effort:** 2-3 hours

---

#### 9.1.2: Define Context Types

**Purpose:** Establish standard context types for rule scoping

**Proposed Context Types:**

```yaml
# File-based contexts (detected from file path/extension)
- testing          # test/**/*.py, tests/**/*.py
- implementation   # src/**/*.py
- documentation    # docs/**/*.md, *.md
- configuration    # *.toml, *.yaml, *.json

# Task-based contexts (detected from workflow invocation)
- planning         # /plan, /research workflows
- coding           # /implement workflow
- validation       # /validate, /commit workflows
- analysis         # /meta-analysis, /extract-session workflows

# Phase-based contexts (detected from project state)
- prototyping      # Early development
- production       # Stable codebase
- refactoring      # Major changes in progress
```

**Context Detection Logic:**

```python
def detect_context(file_path: str, workflow: str, project_state: dict) -> List[str]:
    """Detect applicable contexts for current task."""
    contexts = set()

    # File-based detection
    if 'test' in file_path:
        contexts.add('testing')
    elif file_path.startswith('src/'):
        contexts.add('implementation')
    elif file_path.endswith('.md'):
        contexts.add('documentation')

    # Task-based detection
    if workflow in ['/plan', '/research']:
        contexts.add('planning')
    elif workflow == '/implement':
        contexts.add('coding')
    elif workflow in ['/validate', '/commit']:
        contexts.add('validation')

    # Phase-based detection
    if project_state['version'].startswith('0.'):
        contexts.add('prototyping')
    else:
        contexts.add('production')

    return list(contexts)
```

**Deliverable:** Context type taxonomy and detection logic

**Effort:** 1-2 hours

---

### Task 9.2: Implement Rule Scoping

**Purpose:** Add `applyTo` frontmatter to all rules and implement selective loading

#### 9.2.1: Add `applyTo` to Rule Frontmatter

**Update all 5 rule files:**

**Example - `01_testing_and_tooling.md`:**

```yaml
---
created: 2025-10-15
updated: 2025-10-18
category: testing
description: Test-driven development practices and quality tooling standards
tokens: 1428
applyTo:
  contexts:
    - testing
    - implementation
    - validation
  files:
    - test/**/*.py
    - tests/**/*.py
    - src/**/*.py  # When implementing (needs testing guidance)
priority: high
status: active
---
```

**Example - `02_python_standards.md`:**

```yaml
---
created: 2025-10-15
updated: 2025-10-18
category: language
description: Python coding standards and best practices
tokens: 2491
applyTo:
  contexts:
    - implementation
    - refactoring
  files:
    - src/**/*.py
    - scripts/**/*.py
exclude:
  contexts:
    - documentation  # Not needed for docs
priority: high
status: active
---
```

**Example - `03_documentation_lifecycle.md`:**

```yaml
---
created: 2025-10-15
updated: 2025-10-18
category: documentation
description: Documentation standards and maintenance procedures
tokens: 1941
applyTo:
  contexts:
    - documentation
    - planning
  files:
    - docs/**/*.md
    - *.md
priority: medium
status: active
---
```

**Example - `04_security.md`:**

```yaml
---
created: 2025-10-15
updated: 2025-10-18
category: security
description: Security best practices for LLM integration and web scraping
tokens: 2525
applyTo:
  contexts:
    - implementation
    - validation
  files:
    - src/**/*.py
  conditions:
    - contains: "requests|httpx|playwright|llm|openai"
priority: high
status: active
---
```

**Example - `00_agent_directives.md`:**

```yaml
---
created: 2025-10-15
updated: 2025-10-18
category: core
description: Core agent persona, principles, and operational mandate
tokens: 5387
applyTo:
  contexts:
    - all  # Core principles always apply
priority: high
status: active
---
```

**Effort:** 1 hour

---

#### 9.2.2: Implement Rule Loading Logic

**Purpose:** Load only applicable rules based on context

**Script:** `scripts/load_applicable_rules.py`

```python
#!/usr/bin/env python3
"""Load only applicable rules based on current context."""

import yaml
from pathlib import Path
from typing import List, Dict
import fnmatch

class RuleLoader:
    def __init__(self, rules_dir: Path):
        self.rules_dir = rules_dir
        self.all_rules = self._load_all_rules()

    def _load_all_rules(self) -> List[Dict]:
        """Load all rule files with frontmatter."""
        rules = []
        for rule_path in self.rules_dir.glob('*.md'):
            frontmatter = self._extract_frontmatter(rule_path)
            if frontmatter:
                frontmatter['_path'] = rule_path
                frontmatter['_name'] = rule_path.stem
                rules.append(frontmatter)
        return rules

    def _extract_frontmatter(self, file_path: Path) -> Dict:
        """Extract YAML frontmatter."""
        content = file_path.read_text()
        if not content.startswith('---'):
            return None
        parts = content.split('---', 2)
        if len(parts) < 3:
            return None
        return yaml.safe_load(parts[1])

    def get_applicable_rules(
        self,
        contexts: List[str],
        file_path: str = None
    ) -> List[Path]:
        """Get list of applicable rule files for given contexts."""
        applicable = []

        for rule in self.all_rules:
            if self._is_applicable(rule, contexts, file_path):
                applicable.append(rule['_path'])

        # Sort by priority
        applicable.sort(
            key=lambda p: self._get_priority_order(p),
            reverse=True
        )

        return applicable

    def _is_applicable(
        self,
        rule: Dict,
        contexts: List[str],
        file_path: str
    ) -> bool:
        """Check if rule applies to given contexts."""
        apply_to = rule.get('applyTo', {})

        # Check for 'all' context
        if apply_to.get('contexts') == ['all']:
            return True

        # Check context match
        rule_contexts = apply_to.get('contexts', [])
        if set(contexts) & set(rule_contexts):
            # Check file pattern if specified
            file_patterns = apply_to.get('files', [])
            if file_patterns and file_path:
                if not any(fnmatch.fnmatch(file_path, pattern) for pattern in file_patterns):
                    return False

            # Check exclusions
            exclude = rule.get('exclude', {})
            exclude_contexts = exclude.get('contexts', [])
            if set(contexts) & set(exclude_contexts):
                return False

            return True

        return False

    def _get_priority_order(self, rule_path: Path) -> int:
        """Convert priority to numeric order."""
        rule = next(r for r in self.all_rules if r['_path'] == rule_path)
        priority_map = {'high': 3, 'medium': 2, 'low': 1}
        return priority_map.get(rule.get('priority', 'medium'), 2)

    def generate_context_summary(self, contexts: List[str], file_path: str = None):
        """Generate summary of applicable rules."""
        applicable = self.get_applicable_rules(contexts, file_path)

        print(f"📋 Applicable Rules for contexts: {', '.join(contexts)}")
        if file_path:
            print(f"   File: {file_path}")
        print()

        for rule_path in applicable:
            rule = next(r for r in self.all_rules if r['_path'] == rule_path)
            print(f"  ✓ {rule['_name']}: {rule['description']}")
            print(f"    Priority: {rule.get('priority', 'medium')} | Tokens: {rule.get('tokens', 'unknown')}")

        # Calculate token savings
        total_tokens = sum(r.get('tokens', 0) for r in self.all_rules)
        applicable_tokens = sum(
            r.get('tokens', 0)
            for r in self.all_rules
            if r['_path'] in applicable
        )
        savings = total_tokens - applicable_tokens
        savings_pct = (savings / total_tokens * 100) if total_tokens > 0 else 0

        print()
        print(f"📊 Token Usage:")
        print(f"  Total available: {total_tokens:,}")
        print(f"  Context-specific: {applicable_tokens:,}")
        print(f"  Savings: {savings:,} ({savings_pct:.1f}%)")

def main():
    import sys

    rules_dir = Path('.windsurf/rules')
    loader = RuleLoader(rules_dir)

    # Example contexts
    if len(sys.argv) > 1:
        contexts = sys.argv[1].split(',')
        file_path = sys.argv[2] if len(sys.argv) > 2 else None
    else:
        # Default example
        contexts = ['implementation']
        file_path = 'src/mcp_web/server.py'

    loader.generate_context_summary(contexts, file_path)

if __name__ == "__main__":
    main()
```

**Testing:**

```bash
# Test different contexts
python scripts/load_applicable_rules.py "testing"
python scripts/load_applicable_rules.py "implementation"
python scripts/load_applicable_rules.py "documentation"

# Test with file path
python scripts/load_applicable_rules.py "implementation" "src/mcp_web/server.py"
python scripts/load_applicable_rules.py "testing" "tests/test_server.py"
```

**Effort:** 4-5 hours

---

### Task 9.3: Create Context-Specific Workflows

**Purpose:** Workflows that auto-specify applicable contexts

#### 9.3.1: Add Context to Workflow Frontmatter

**Update workflows to specify their context:**

**Example - `/implement` workflow:**

```yaml
---
created: 2025-10-17
updated: 2025-10-18
category: implementation
complexity: 70
description: Test-driven implementation workflow with quality gates
tokens: 3225
dependencies: [validate]
context:
  primary: implementation
  secondary: [testing, validation]
load_rules:
  - 00_agent_directives  # Core principles
  - 01_testing_and_tooling  # TDD practices
  - 02_python_standards  # Coding standards
exclude_rules:
  - 03_documentation_lifecycle  # Not needed during implementation
status: active
---
```

**Example - `/plan` workflow:**

```yaml
---
created: 2025-10-17
updated: 2025-10-18
category: planning
complexity: 65
description: Research-driven comprehensive project planning
tokens: 2293
dependencies: [research, generate-plan]
context:
  primary: planning
  secondary: [documentation]
load_rules:
  - 00_agent_directives  # Core principles
  - 03_documentation_lifecycle  # ADR creation
exclude_rules:
  - 01_testing_and_tooling  # Not needed during planning
  - 02_python_standards  # Not needed during planning
  - 04_security  # Not needed during planning
status: active
---
```

**Example - `/validate` workflow:**

```yaml
---
created: 2025-10-17
updated: 2025-10-18
category: validation
complexity: 68
description: Comprehensive quality validation and testing
tokens: 2545
dependencies: []
context:
  primary: validation
  secondary: [testing, implementation]
load_rules:
  - 00_agent_directives  # Core principles
  - 01_testing_and_tooling  # Testing standards
  - 02_python_standards  # Code quality
  - 04_security  # Security checks
exclude_rules:
  - 03_documentation_lifecycle  # Not needed during validation
status: active
---
```

**Effort:** 2-3 hours

---

#### 9.3.2: Update Workflow Invocation

**Purpose:** Automatically load only applicable rules when workflow invoked

**Implementation:** Update `.windsurf/workflows/work.md`

```markdown
## Stage 2: Detect Context and Load Rules

**Call `/detect-context` workflow** to analyze project state.

**Then load applicable rules based on detected workflow:**

[bash]
# Determine target workflow from detection
TARGET_WORKFLOW="implement"  # Example

# Load only applicable rules
python scripts/load_applicable_rules.py \
  --workflow $TARGET_WORKFLOW \
  --file-path $CURRENT_FILE

# This reduces context load by 20-40% depending on workflow
[/bash]

**Rules loaded:** Only those specified in target workflow's frontmatter

**Example for /implement:**
- ✓ 00_agent_directives (5,387 tokens)
- ✓ 01_testing_and_tooling (1,428 tokens)
- ✓ 02_python_standards (2,491 tokens)
- ✗ 03_documentation_lifecycle (1,941 tokens) - excluded
- ✗ 04_security (2,525 tokens) - excluded unless security-related file

**Token savings:** ~4,466 tokens (32% reduction)
```

**Effort:** 1-2 hours

---

### Task 9.4: Measure Context Optimization Impact

**Purpose:** Validate token reduction from modular loading

#### 9.4.1: Baseline Measurement

```bash
# Current: All rules always loaded
BASELINE_TOKENS=13,772  # Sum of all 5 rules

# Breakdown:
# - 00_agent_directives: 5,387
# - 01_testing_and_tooling: 1,428
# - 02_python_standards: 2,491
# - 03_documentation_lifecycle: 1,941
# - 04_security: 2,525
```

#### 9.4.2: Context-Specific Measurements

**Testing Context:**

```bash
python scripts/load_applicable_rules.py "testing"

# Expected loaded:
# - 00_agent_directives: 5,387
# - 01_testing_and_tooling: 1,428
# Total: 6,815 tokens (50% reduction)
```

**Implementation Context:**

```bash
python scripts/load_applicable_rules.py "implementation"

# Expected loaded:
# - 00_agent_directives: 5,387
# - 01_testing_and_tooling: 1,428
# - 02_python_standards: 2,491
# - 04_security: 2,525 (if security-related)
# Total: 9,306-11,831 tokens (14-32% reduction)
```

**Documentation Context:**

```bash
python scripts/load_applicable_rules.py "documentation"

# Expected loaded:
# - 00_agent_directives: 5,387
# - 03_documentation_lifecycle: 1,941
# Total: 7,328 tokens (47% reduction)
```

**Planning Context:**

```bash
python scripts/load_applicable_rules.py "planning"

# Expected loaded:
# - 00_agent_directives: 5,387
# - 03_documentation_lifecycle: 1,941
# Total: 7,328 tokens (47% reduction)
```

#### 9.4.3: Calculate Average Savings

```python
# Weighted average based on workflow frequency
contexts = {
    'testing': 0.20,      # 20% of tasks
    'implementation': 0.40,  # 40% of tasks
    'documentation': 0.15,   # 15% of tasks
    'planning': 0.10,        # 10% of tasks
    'validation': 0.15       # 15% of tasks
}

savings = {
    'testing': 0.50,      # 50% reduction
    'implementation': 0.32,  # 32% reduction
    'documentation': 0.47,   # 47% reduction
    'planning': 0.47,        # 47% reduction
    'validation': 0.18       # 18% reduction
}

avg_savings = sum(contexts[c] * savings[c] for c in contexts)
# Expected: ~0.35 (35% average reduction)
```

**Deliverable:** Impact report with measurements

**Effort:** 1-2 hours

---

## Success Criteria

### Quantitative Metrics

- ✅ `applyTo` frontmatter added to all 5 rules
- ✅ Context detection logic implemented
- ✅ Rule loading script created and tested
- ✅ Average token reduction: ≥20%
- ✅ Workflows updated with context specifications

### Qualitative Metrics

- ✅ Improved AI focus (only relevant rules)
- ✅ Faster context loading
- ✅ Easier to maintain (clear rule applicability)
- ✅ Flexible system (easy to add new contexts)

---

## Validation Steps

1. **Test Context Detection:**

   ```bash
   # Test various contexts
   python scripts/load_applicable_rules.py "testing"
   python scripts/load_applicable_rules.py "implementation"
   python scripts/load_applicable_rules.py "documentation"

   # Verify correct rules loaded for each
   ```

2. **Test Workflow Integration:**

   ```bash
   # Execute workflow with context-specific loading
   /implement

   # Verify only applicable rules loaded
   # Measure performance improvement
   ```

3. **Measure Token Savings:**

   ```bash
   python scripts/measure_context_savings.py

   # Expected: ≥20% average reduction
   ```

4. **User Feedback:**
   - Test with 3-5 different tasks
   - Verify no information gaps (all needed rules present)
   - Confirm performance improvement noticeable

---

## Deliverables

- ✅ Research summary - `applyTo` patterns and best practices
- ✅ Context taxonomy - Defined context types
- ✅ All 5 rules - Updated with `applyTo` frontmatter
- ✅ `scripts/load_applicable_rules.py` - Context-aware rule loading
- ✅ All 17 workflows - Updated with context specifications
- ✅ `scripts/measure_context_savings.py` - Impact measurement
- ✅ Impact report - Token savings analysis

---

## Dependencies

**Requires:**

- Phase 5 complete (frontmatter infrastructure)
- Phase 8 complete (quality automation for validation)

**Enables:**

- Future: Dynamic context detection based on task analysis
- Future: User-customizable context definitions
- Future: Context-aware caching strategies

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Missing rules for specific tasks | HIGH | Conservative approach - load more rather than less |
| Context detection errors | MEDIUM | Fallback to loading all rules if unsure |
| Increased complexity | MEDIUM | Clear documentation, thorough testing |
| User confusion | LOW | Optional feature, default to all rules |

---

## Optional Enhancements

### Future Improvements (beyond Phase 9)

1. **Dynamic Context Detection:**
   - Analyze task description to infer context
   - Machine learning for context classification
   - User feedback loop to improve detection

2. **User-Customizable Contexts:**
   - Allow users to define custom contexts
   - Personal rule preferences
   - Team-specific context definitions

3. **Context Caching:**
   - Cache context-specific rule combinations
   - Reduce loading time further
   - Smart prefetching based on patterns

4. **Context Analytics:**
   - Track which contexts most used
   - Identify opportunities for new contexts
   - Optimize rule organization based on usage

---

## Completion Notes

**Phase 9 Status:** 🆕 New phase, LOW priority (post-launch)

**Next Phase:** None - final phase of initiative

**Estimated Timeline:** Post-launch, Week of 2025-11-18 (10-15 hours)

**Note:** This phase is OPTIONAL and should only be implemented after Phases 1-8 are complete and validated in production.
