# Workflow Optimization Restoration Protocol

**Version:** 1.0
**Created:** 2025-10-21
**Status:** Active - MANDATORY for all future workflow optimizations

---

## Purpose

This protocol prevents semantic content loss during workflow optimization by enforcing validation checkpoints before committing changes.

---

## Background

**Incident:** 2025-10-21 Batch 1 Optimization
- **What happened:** v2.0 "intelligent semantic preservation" optimization removed 28% of implement.md content
- **Content lost:** Stage 2 (context loading), Stage 2.5 (ADR requirement check), detailed scoring algorithms
- **Root cause:** No validation of semantic preservation before committing
- **Impact:** Critical operational stages removed, requiring full restoration from git history

---

## Mandatory Pre-Commit Validation

### Phase 1: Baseline Snapshot

**BEFORE any optimization:**

```bash
# Create baseline for comparison
git show HEAD:.windsurf/workflows/TARGET.md > /tmp/TARGET-baseline.md

# Record metrics
wc -w /tmp/TARGET-baseline.md
```

### Phase 2: Apply Optimization

Apply intelligent compression techniques per methodology.

### Phase 3: Validation (MANDATORY)

**All checks MUST pass before committing:**

#### 3.1 Quantitative Validation

```bash
# Current metrics
wc -w .windsurf/workflows/TARGET.md

# Compare
diff -u /tmp/TARGET-baseline.md .windsurf/workflows/TARGET.md | wc -l
```

**Thresholds:**
- Word count delta: ≤15% reduction
- Line change count: ≤30% of baseline lines

#### 3.2 Structural Validation

**Check all stages/sections present:**

```bash
# Extract headings from baseline
grep "^##" /tmp/TARGET-baseline.md > /tmp/baseline-structure.txt

# Extract headings from optimized
grep "^##" .windsurf/workflows/TARGET.md > /tmp/optimized-structure.txt

# Compare
diff /tmp/baseline-structure.txt /tmp/optimized-structure.txt
```

**FAIL if:** Any Stage## heading missing

#### 3.3 Critical Element Validation

**Check preservation of:**
- ✅ All `update_plan` code blocks
- ✅ All CRITICAL/MANDATORY markers
- ✅ All decision matrices/tables
- ✅ All anti-pattern sections
- ✅ All code examples
- ✅ All stage completion markers

```bash
# Count critical elements
grep -c "update_plan" /tmp/TARGET-baseline.md
grep -c "update_plan" .windsurf/workflows/TARGET.md

grep -c "CRITICAL\|MANDATORY" /tmp/TARGET-baseline.md
grep -c "CRITICAL\|MANDATORY" .windsurf/workflows/TARGET.md
```

**FAIL if:** Any element count reduced

#### 3.4 Semantic Preservation Score

**Manual review checklist:**
- [ ] All operational instructions preserved
- [ ] All decision logic intact
- [ ] All examples functionally equivalent
- [ ] All cross-references valid
- [ ] No ambiguity introduced

**Score calculation:**
- Structural preservation (stages intact): 40%
- Critical elements (markers, code blocks): 30%
- Content comprehensiveness (instructions complete): 20%
- Cross-reference validity: 10%

**Threshold:** ≥92% semantic preservation required

### Phase 4: Restoration Decision

**IF validation fails:**

```bash
# Restore baseline immediately
cp /tmp/TARGET-baseline.md .windsurf/workflows/TARGET.md

# Document failure
echo "Optimization failed validation - restored baseline" >> OPTIMIZATION_LOG.md
```

**DO NOT COMMIT** if validation score <92%

### Phase 5: Commit Only If Validated

```bash
# Only if ALL validations passed
git add .windsurf/workflows/TARGET.md
git commit -m "feat(workflows): optimize TARGET.md

- Semantic preservation: XX%
- Word reduction: -XX words (-XX%)
- All stages: ✅ preserved
- All critical elements: ✅ intact
- Validation: ✅ passed

Validation log:
- Structural: ✅ all XX stages intact
- Critical markers: ✅ XX/XX preserved
- update_plan blocks: ✅ XX/XX preserved
- Examples: ✅ XX/XX preserved

Related: docs/initiatives/active/workflow-optimization-phase-2/"
```

---

## Automation Script

**TODO:** Create `scripts/validate-workflow-optimization.py`:

```python
#!/usr/bin/env python3
"""Validate workflow optimization before commit."""

import sys
from pathlib import Path

def validate_optimization(baseline_path: str, optimized_path: str) -> bool:
    """
    Returns True if optimization passes all validation checks.
    
    Checks:
    1. Word count delta ≤15%
    2. All stages present
    3. All critical elements intact
    4. Semantic preservation ≥92%
    """
    # Implementation TBD
    pass

if __name__ == "__main__":
    baseline = sys.argv[1]
    optimized = sys.argv[2]
    
    if not validate_optimization(baseline, optimized):
        print("❌ Validation FAILED - restore baseline")
        sys.exit(1)
    
    print("✅ Validation PASSED - safe to commit")
    sys.exit(0)
```

---

## For Future AI Agents

**CRITICAL:** This protocol is MANDATORY for ALL workflow optimizations.

**Before optimizing any workflow:**

1. Read this protocol: `docs/initiatives/active/workflow-optimization-phase-2/artifacts/RESTORATION_PROTOCOL.md`
2. Create baseline snapshot
3. Apply optimization
4. Run ALL validation checks
5. Only commit if validation passes
6. If validation fails: RESTORE baseline immediately

**Never skip validation.** Content loss incidents are critical failures that require full restoration from git history.

---

## References

- Incident report: Git commit `e57edfb` (2025-10-21)
- Intelligent compression methodology: `intelligent-compression-v2.md`
- Phase 2 plan: `phase-2-batch-optimization.md`

---

**Status:** Active - Required for all future optimizations
**Last Updated:** 2025-10-21
