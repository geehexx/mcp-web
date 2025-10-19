# Phase 8: Quality Automation

**Status:** 🆕 New Phase (from gap analysis)
**Priority:** MEDIUM
**Duration:** 7-10 hours
**Owner:** AI Agent

---

## Objective

Implement automated quality gates and monitoring to prevent regression and maintain optimization gains.

**Target:** Full quality automation with CI/CD integration

---

## Background

Gap analysis identified need for:

- Workflow validation automation (Gap #2)
- Performance monitoring in CI/CD (Gap #3)
- Cross-reference validation (Gap #4)

These prevent backsliding after optimization and catch issues before merge.

---

## Tasks

### Task 8.1: Create Workflow Validation Script (Gap #2)

**Purpose:** Automated validation of workflow consistency

**Script:** `scripts/validate_workflows.py`

**Features:**

1. **Cross-Reference Validation:**
   - Check all workflow-to-workflow references
   - Check all rule-to-workflow references
   - Verify referenced files exist
   - Detect broken links

2. **Frontmatter Schema Validation:**
   - Verify all required fields present
   - Check data types correct
   - Validate enum values
   - Ensure dates valid (YYYY-MM-DD format)

3. **Complexity Metrics:**
   - Calculate complexity score (0-100)
   - Warn if >75/100
   - Fail if >85/100
   - Track trend over time

4. **Token Count Verification:**
   - Calculate actual token count
   - Compare to frontmatter value
   - Warn if difference >5%
   - Fail if file >4,000 tokens

5. **Dependency Graph Validation:**
   - Extract workflow dependencies
   - Detect circular dependencies
   - Verify dependency graph acyclic
   - Generate visualization

**Implementation:**

```python
#!/usr/bin/env python3
"""Comprehensive workflow and rule validation."""

import re
import yaml
from pathlib import Path
from typing import Dict, List, Tuple
import networkx as nx

class WorkflowValidator:
    def __init__(self, workflow_dir: Path, rules_dir: Path):
        self.workflow_dir = workflow_dir
        self.rules_dir = rules_dir
        self.errors = []
        self.warnings = []

    def validate_all(self) -> bool:
        """Run all validation checks."""
        self.validate_cross_references()
        self.validate_frontmatter()
        self.validate_complexity()
        self.validate_token_counts()
        self.validate_dependencies()
        return len(self.errors) == 0

    def validate_cross_references(self):
        """Check all workflow references valid."""
        for file_path in self.workflow_dir.glob("*.md"):
            content = file_path.read_text()
            # Find markdown links [text](path)
            links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', content)
            for text, link in links:
                if link.startswith(('http://', 'https://')):
                    continue  # Skip external links
                target = (file_path.parent / link).resolve()
                if not target.exists():
                    self.errors.append(
                        f"{file_path.name}: Broken link to {link}"
                    )

    def validate_frontmatter(self):
        """Validate YAML frontmatter schema."""
        for file_path in self.workflow_dir.glob("*.md"):
            frontmatter = self._extract_frontmatter(file_path)
            if not frontmatter:
                self.errors.append(
                    f"{file_path.name}: Missing frontmatter"
                )
                continue

            # Check required fields
            required = ['created', 'updated', 'category', 'description']
            for field in required:
                if field not in frontmatter:
                    self.errors.append(
                        f"{file_path.name}: Missing required field '{field}'"
                    )

    def validate_complexity(self):
        """Calculate and validate complexity scores."""
        for file_path in self.workflow_dir.glob("*.md"):
            complexity = self._calculate_complexity(file_path)
            frontmatter = self._extract_frontmatter(file_path)

            if complexity > 85:
                self.errors.append(
                    f"{file_path.name}: Complexity {complexity}/100 exceeds limit"
                )
            elif complexity > 75:
                self.warnings.append(
                    f"{file_path.name}: Complexity {complexity}/100 approaching limit"
                )

            # Check frontmatter matches
            if frontmatter and 'complexity' in frontmatter:
                fm_complexity = frontmatter['complexity']
                if abs(complexity - fm_complexity) > 5:
                    self.warnings.append(
                        f"{file_path.name}: Complexity mismatch (actual: {complexity}, frontmatter: {fm_complexity})"
                    )

    def validate_token_counts(self):
        """Verify token counts in frontmatter accurate."""
        for file_path in self.workflow_dir.glob("*.md"):
            actual_tokens = self._calculate_tokens(file_path)
            frontmatter = self._extract_frontmatter(file_path)

            if actual_tokens > 4000:
                self.errors.append(
                    f"{file_path.name}: Token count {actual_tokens} exceeds 4,000 limit"
                )

            if frontmatter and 'tokens' in frontmatter:
                fm_tokens = frontmatter['tokens']
                diff_pct = abs(actual_tokens - fm_tokens) / fm_tokens * 100
                if diff_pct > 5:
                    self.warnings.append(
                        f"{file_path.name}: Token count mismatch {diff_pct:.1f}% (actual: {actual_tokens}, frontmatter: {fm_tokens})"
                    )

    def validate_dependencies(self):
        """Check for circular dependencies."""
        graph = nx.DiGraph()

        # Build dependency graph
        for file_path in self.workflow_dir.glob("*.md"):
            workflow_name = file_path.stem
            frontmatter = self._extract_frontmatter(file_path)
            if frontmatter and 'dependencies' in frontmatter:
                for dep in frontmatter['dependencies']:
                    graph.add_edge(workflow_name, dep)

        # Check for cycles
        try:
            cycles = list(nx.simple_cycles(graph))
            if cycles:
                for cycle in cycles:
                    self.errors.append(
                        f"Circular dependency detected: {' -> '.join(cycle)}"
                    )
        except:
            pass

    def _extract_frontmatter(self, file_path: Path) -> Dict:
        """Extract YAML frontmatter from file."""
        content = file_path.read_text()
        if not content.startswith('---'):
            return None
        parts = content.split('---', 2)
        if len(parts) < 3:
            return None
        return yaml.safe_load(parts[1])

    def _calculate_complexity(self, file_path: Path) -> int:
        """Calculate complexity score 0-100."""
        content = file_path.read_text()

        # Structural (30%)
        sections = len(re.findall(r'^#{1,3}\s', content, re.MULTILINE))
        code_blocks = len(re.findall(r'```', content))
        lists = len(re.findall(r'^\s*[-*]\s', content, re.MULTILINE))
        tables = len(re.findall(r'\|', content))
        structural = min(30, (sections * 2 + code_blocks + lists * 0.5 + tables * 0.3))

        # Operational (40%)
        decisions = len(re.findall(r'\bif\b|\bwhen\b|\bchoose\b', content, re.IGNORECASE))
        stages = len(re.findall(r'stage|phase|step', content, re.IGNORECASE))
        operational = min(40, (decisions * 3 + stages * 2))

        # Density (20%)
        words = len(content.split())
        references = len(re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', content))
        density = min(20, (words / 500 + references * 2))

        # Maintenance (10%)
        lines = len(content.split('\n'))
        maintenance = min(10, lines / 100)

        return int(structural + operational + density + maintenance)

    def _calculate_tokens(self, file_path: Path) -> int:
        """Estimate token count (rough: 4 chars per token)."""
        content = file_path.read_text()
        return len(content) // 4

    def print_report(self):
        """Print validation report."""
        if self.errors:
            print("❌ ERRORS:")
            for error in self.errors:
                print(f"  - {error}")

        if self.warnings:
            print("\n⚠️  WARNINGS:")
            for warning in self.warnings:
                print(f"  - {warning}")

        if not self.errors and not self.warnings:
            print("✅ All validations passed!")

        return len(self.errors) == 0

def main():
    workflow_dir = Path(".windsurf/workflows")
    rules_dir = Path(".windsurf/rules")

    validator = WorkflowValidator(workflow_dir, rules_dir)
    success = validator.validate_all()
    validator.print_report()

    exit(0 if success else 1)

if __name__ == "__main__":
    main()
```

**Testing:**

```bash
# Run validation
python scripts/validate_workflows.py

# Expected output:
# ✅ All validations passed!
# Or list of errors/warnings
```

**Effort:** 4-5 hours

---

### Task 8.2: Integrate Performance Monitoring (Gap #3)

**Purpose:** Track token usage over time, prevent regression

**Implementation:**

#### 8.2.1: Create Token Tracking Script

**Script:** `scripts/check_workflow_tokens.py`

```python
#!/usr/bin/env python3
"""Track workflow token usage over time."""

import json
from pathlib import Path
from datetime import datetime

def calculate_total_tokens():
    """Calculate total tokens across all workflows and rules."""
    total = 0
    breakdown = {}

    for dir_name in ['.windsurf/workflows', '.windsurf/rules']:
        dir_path = Path(dir_name)
        dir_total = 0
        for file_path in dir_path.glob('*.md'):
            tokens = len(file_path.read_text()) // 4
            dir_total += tokens
            breakdown[str(file_path)] = tokens
        total += dir_total
        breakdown[dir_name] = dir_total

    breakdown['total'] = total
    return breakdown

def save_metrics(breakdown: dict):
    """Save metrics to benchmarks directory."""
    metrics_dir = Path('.benchmarks')
    metrics_dir.mkdir(exist_ok=True)

    # Save current metrics
    timestamp = datetime.now().isoformat()
    metrics = {
        'timestamp': timestamp,
        'breakdown': breakdown
    }

    # Append to history
    history_file = metrics_dir / 'workflow-tokens-history.jsonl'
    with open(history_file, 'a') as f:
        f.write(json.dumps(metrics) + '\n')

    # Save latest
    latest_file = metrics_dir / 'workflow-tokens-latest.json'
    with open(latest_file, 'w') as f:
        json.dump(metrics, f, indent=2)

    # Save simple total for CI
    total_file = metrics_dir / 'workflow-tokens-total.txt'
    with open(total_file, 'w') as f:
        f.write(str(breakdown['total']))

def check_thresholds(breakdown: dict) -> bool:
    """Check if metrics exceed thresholds."""
    total = breakdown['total']
    max_total = 60000  # Maximum total tokens
    max_file = 4000    # Maximum per file

    errors = []

    if total > max_total:
        errors.append(f"Total tokens {total} exceeds limit {max_total}")

    for path, tokens in breakdown.items():
        if path.endswith('.md') and tokens > max_file:
            errors.append(f"{path}: {tokens} tokens exceeds limit {max_file}")

    if errors:
        print("❌ Token thresholds exceeded:")
        for error in errors:
            print(f"  - {error}")
        return False

    print(f"✅ Token count: {total} (within limits)")
    return True

def main():
    breakdown = calculate_total_tokens()
    save_metrics(breakdown)
    success = check_thresholds(breakdown)
    exit(0 if success else 1)

if __name__ == "__main__":
    main()
```

#### 8.2.2: Create GitHub Actions Workflow

**File:** `.github/workflows/workflow-quality.yml`

```yaml
name: Workflow Quality Checks

on:
  push:
    paths:
      - '.windsurf/**/*.md'
  pull_request:
    paths:
      - '.windsurf/**/*.md'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install pyyaml networkx

      - name: Validate workflows
        run: python scripts/validate_workflows.py

      - name: Check token counts
        run: python scripts/check_workflow_tokens.py

      - name: Upload metrics
        uses: actions/upload-artifact@v3
        with:
          name: workflow-metrics
          path: .benchmarks/workflow-tokens-latest.json

      - name: Comment on PR
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const metrics = JSON.parse(fs.readFileSync('.benchmarks/workflow-tokens-latest.json'));
            const total = metrics.breakdown.total;
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `📊 Workflow Metrics:\n\nTotal tokens: ${total}\n\nSee artifacts for details.`
            });
```

**Effort:** 3-4 hours

---

### Task 8.3: Create Monitoring Dashboard

**Purpose:** Visualize token trends over time

**Implementation:** `scripts/generate_dashboard.py`

```python
#!/usr/bin/env python3
"""Generate workflow metrics dashboard."""

import json
from pathlib import Path
from datetime import datetime

def load_history():
    """Load historical metrics."""
    history_file = Path('.benchmarks/workflow-tokens-history.jsonl')
    if not history_file.exists():
        return []

    history = []
    with open(history_file) as f:
        for line in f:
            history.append(json.loads(line))
    return history

def generate_markdown_dashboard(history):
    """Generate markdown dashboard."""
    if not history:
        return "No historical data available."

    # Latest metrics
    latest = history[-1]
    total = latest['breakdown']['total']
    timestamp = latest['timestamp']

    # Calculate trend
    if len(history) > 1:
        previous = history[-2]['breakdown']['total']
        change = total - previous
        change_pct = (change / previous) * 100
        trend = f"{'📉' if change < 0 else '📈'} {change:+d} tokens ({change_pct:+.1f}%)"
    else:
        trend = "N/A (first measurement)"

    dashboard = f"""# Workflow Metrics Dashboard

**Last Updated:** {timestamp}

## Summary

- **Total Tokens:** {total:,}
- **Trend:** {trend}
- **Target:** ≤60,000 tokens
- **Status:** {'✅ Within limits' if total <= 60000 else '❌ Exceeds limit'}

## Breakdown

| Directory | Tokens | % of Total |
|-----------|--------|------------|
| Workflows | {latest['breakdown']['.windsurf/workflows']:,} | {latest['breakdown']['.windsurf/workflows']/total*100:.1f}% |
| Rules | {latest['breakdown']['.windsurf/rules']:,} | {latest['breakdown']['.windsurf/rules']/total*100:.1f}% |

## Historical Trend

"""

    # Add last 10 measurements
    for entry in history[-10:]:
        date = entry['timestamp'][:10]
        total = entry['breakdown']['total']
        dashboard += f"- {date}: {total:,} tokens\n"

    return dashboard

def main():
    history = load_history()
    dashboard = generate_markdown_dashboard(history)

    output_file = Path('.benchmarks/DASHBOARD.md')
    output_file.write_text(dashboard)

    print("✅ Dashboard generated: .benchmarks/DASHBOARD.md")

if __name__ == "__main__":
    main()
```

**Effort:** 1 hour

---

## Success Criteria

### Quantitative Metrics

- ✅ Validation script created and tested
- ✅ Token tracking script created and tested
- ✅ GitHub Actions workflow created
- ✅ Dashboard generation working
- ✅ All validations passing on existing files

### Qualitative Metrics

- ✅ Catch errors before merge
- ✅ Prevent token regression
- ✅ Easy to interpret metrics
- ✅ Actionable feedback

---

## Validation Steps

1. **Test Validation Script:**

   ```bash
   python scripts/validate_workflows.py
   # Expected: ✅ All validations passed
   ```

2. **Test Token Tracking:**

   ```bash
   python scripts/check_workflow_tokens.py
   # Expected: ✅ Token count within limits
   ```

3. **Test CI/CD:**

   ```bash
   git checkout -b test-quality-automation
   # Modify a workflow file
   git push origin test-quality-automation
   # Check GitHub Actions run successfully
   ```

4. **Test Dashboard:**

   ```bash
   python scripts/generate_dashboard.py
   cat .benchmarks/DASHBOARD.md
   # Expected: Dashboard with current metrics
   ```

---

## Deliverables

- ✅ `scripts/validate_workflows.py` - Comprehensive validation
- ✅ `scripts/check_workflow_tokens.py` - Token tracking
- ✅ `scripts/generate_dashboard.py` - Dashboard generation
- ✅ `.github/workflows/workflow-quality.yml` - CI/CD integration
- ✅ `.benchmarks/DASHBOARD.md` - Metrics dashboard
- ✅ Validation passing on all existing files

---

## Dependencies

**Requires:**

- Phase 5 complete (frontmatter exists)
- Phase 7 complete (validation tested)

**Enables:**

- Phase 9: Advanced features (quality gates in place)
- Future: Continuous improvement (metrics tracked)

---

## Completion Notes

**Phase 8 Status:** 🆕 New phase, ready after Phase 7

**Next Phase:** Phase 9 (Advanced Context Engineering) - Optional advanced features

**Estimated Timeline:** Week of 2025-11-11 (7-10 hours)
