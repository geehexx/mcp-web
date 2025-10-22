# Phase 0: Scripts Audit & Refactoring Plan

**Initiative:** Testing Excellence & Automation Hardening
**Phase:** 0 (Pre-Initiative Cleanup)
**Date:** 2025-10-22
**Status:** Planned

---

## Executive Summary

Before beginning comprehensive testing (Phases 1-7), audit and refactor the `scripts/` directory to:

1. **Remove obsolete one-time scripts** (5 scripts, ~900 LOC)
2. **Extract common functionality** (DRY principle, reduce duplication)
3. **Organize into logical structure** (maintainability, discoverability)
4. **Update all references** (Taskfile, pre-commit, docs)

**Rationale:** Testing 24 scripts with 83% untested (20/24) is expensive. By reducing to ~18-19 production scripts and extracting common lib code, we:

- Reduce testing surface by ~25% (fewer scripts to test)
- Improve test efficiency via shared lib testing (test once, use everywhere)
- Enable easier maintenance (DRY principle)
- Establish patterns for script development

**Estimated Effort:** 8-12 hours (vs 6-8 weeks for full initiative)
**ROI:** High - reduces Phase 1 scope by ~25%, establishes maintainable patterns

---

## Current State Analysis

### Scripts Inventory (24 total, 8,707 LOC)

**By Risk Category:**

- **CRITICAL (8):** validate_initiatives.py, validate_task_format.py, validate_references.py, extract_action_items.py, dependency_registry.py, generate_indexes.py, file_ops.py, scaffold.py
- **HIGH (6):** benchmark_pipeline.py, check_performance_regression.py, validate_archival.py, doc_coverage.py, check_workflow_tokens.py, update_machine_readable_docs.py
- **MEDIUM (7):** validate_documentation.py, validate_frontmatter.py, validate_workflows.py, validate_rules_frontmatter.py, analyze_workflow_improvements.py, hooks/validate_task_format_hook.py
- **LOW (3):** fix_frontmatter.py, restore_workflows.py, test_optimization_idempotency.py, manage_optimization_cache.py (+ 1 backup file)

### Obsolete Scripts (5 scripts, ~900 LOC)

**1. `fix_frontmatter.py` (0 bytes)**

- Status: Already empty/obsolete
- Last used: 2025-10-21 (frontmatter migration)
- Action: DELETE

**2. `restore_workflows.py` (207 lines)**

- Purpose: One-time restoration from pre-optimization commits
- Last used: 2025-10-20 (workflow optimization recovery)
- Usage: NOT in Taskfile, NOT in pre-commit
- Action: DELETE

**3. `test_optimization_idempotency.py` (274 lines)**

- Purpose: Test workflow optimization idempotency
- Last used: 2025-10-20 (workflow optimization validation)
- Usage: NOT in Taskfile, NOT in pre-commit
- Action: DELETE

**4. `manage_optimization_cache.py` (~200 lines, estimated)**

- Purpose: Cache management for workflow optimization
- Last used: 2025-10-20 (workflow optimization)
- Usage: Imported by test_optimization_idempotency.py only
- Action: DELETE (dependent deleted)

**5. `extract_action_items.py.backup` (unknown size)**

- Purpose: Backup file
- Action: DELETE

**Total Removal:** ~900 LOC, 5 files, 0 test coverage required

---

## Code Duplication Analysis

### Frontmatter Parsing (3+ implementations)

**Duplicated in:**

1. `validate_frontmatter.py::extract_frontmatter()` (28 lines)
2. `analyze_workflow_improvements.py::parse_frontmatter()` (regex-based)
3. `generate_indexes.py::extract_frontmatter()` (28 lines, identical to #1)
4. `validate_workflows.py::_extract_frontmatter()` (50 lines, lenient YAML)
5. `validate_initiatives.py` (uses `frontmatter` library)

**Common Pattern:**

```python
def extract_frontmatter(file_path: Path) -> dict | None:
    """Extract YAML frontmatter from markdown file."""
    content = file_path.read_text()
    if not content.startswith("---"):
        return None
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None
    return yaml.safe_load(parts[1])
```

**Proposed:** Extract to `scripts/lib/frontmatter.py` with:

- `extract_frontmatter(file_path: Path) -> dict | None` - Standard parsing
- `extract_frontmatter_lenient(file_path: Path) -> dict | None` - Windsurf-compatible
- `validate_frontmatter(data: dict, schema: dict) -> list[str]` - Validation

### Validation Patterns (6+ scripts)

**Common Patterns:**

1. File walking (`Path.glob("*.md")`)
2. Error accumulation (`errors: list[str] = []`)
3. CLI argument parsing (argparse boilerplate)
4. Exit code handling (`sys.exit(1 if errors else 0)`)
5. Report formatting (colored output, summary)

**Proposed:** Extract to `scripts/lib/validation.py` with:

- `BaseValidator` abstract class
- `walk_files(directory: Path, pattern: str) -> Iterator[Path]`
- `collect_errors() -> ValidationResult`
- `print_report(result: ValidationResult) -> None`

### CLI Utilities (8+ scripts)

**Common Patterns:**

1. argparse setup (desc, args, help)
2. `--dry-run` flag handling
3. `--verbose` flag handling
4. Exit code conventions

**Proposed:** Extract to `scripts/lib/cli.py` with:

- `create_parser(description: str) -> ArgumentParser`
- `add_common_args(parser: ArgumentParser) -> None`
- `handle_exit(errors: list[str]) -> int`

---

## Proposed Refactoring Structure

### New Directory Layout

```text
scripts/
├── lib/                          # NEW: Common library code
│   ├── __init__.py              # Package marker
│   ├── frontmatter.py           # Frontmatter parsing (100-150 LOC)
│   ├── validation.py            # Validation patterns (150-200 LOC)
│   └── cli.py                   # CLI utilities (80-100 LOC)
├── validation/                   # NEW: Group validation scripts
│   ├── __init__.py
│   ├── validate_initiatives.py  # Moved, refactored
│   ├── validate_references.py   # Moved, refactored
│   ├── validate_documentation.py # Moved, refactored
│   ├── validate_workflows.py    # Moved, refactored
│   ├── validate_rules.py        # Moved, refactored
│   └── validate_task_format.py  # Moved, refactored
├── automation/                   # NEW: Group automation scripts
│   ├── __init__.py
│   ├── scaffold.py              # Moved
│   ├── file_ops.py              # Moved
│   └── dependency_registry.py   # Moved
├── analysis/                     # NEW: Group analysis/benchmarking
│   ├── __init__.py
│   ├── benchmark_pipeline.py    # Moved
│   ├── check_performance_regression.py # Moved
│   ├── doc_coverage.py          # Moved
│   ├── analyze_workflow_improvements.py # Moved
│   └── generate_indexes.py      # Moved
├── hooks/                        # Existing: pre-commit hooks
│   └── validate_task_format_hook.py
└── README.md                     # Updated with new structure
```

### Migration Strategy

### Phase 0.1: Remove Obsolete (Low Risk)

- Delete 5 obsolete scripts
- Update any references (none expected)
- Verify no broken imports

### Phase 0.2: Create Lib Module (Foundation)

- Create `scripts/lib/` structure
- Extract common frontmatter parsing
- Extract common validation patterns
- Extract common CLI utilities
- Write unit tests for lib (NEW: 20-30 tests)

### Phase 0.3: Refactor Validation Scripts (Highest Impact)

- Move to `scripts/validation/`
- Refactor to use `scripts/lib/`
- Update imports
- Update Taskfile references
- Update pre-commit hooks

### Phase 0.4: Refactor Automation Scripts (Medium Impact)

- Move to `scripts/automation/`
- Refactor to use `scripts/lib/` where applicable
- Update imports
- Update Taskfile references

### Phase 0.5: Refactor Analysis Scripts (Low Impact)

- Move to `scripts/analysis/`
- Minimal refactoring (less duplication)
- Update imports
- Update Taskfile references

### Phase 0.6: Validation & Documentation

- Run all validation scripts
- Update scripts/README.md
- Update Taskfile.yml
- Update pre-commit-config.yaml
- Run full test suite (existing + new lib tests)

---

## Benefits Analysis

### Quantitative Benefits

**Testing Reduction:**

- Before: 24 scripts, 20 untested (83%)
- After: 18 scripts + 1 lib module
- Lib tests: 20-30 tests (cover 3-4 common patterns)
- Net effect: ~25% fewer scripts to test, ~30% fewer duplicated tests

**Code Reduction:**

- Remove obsolete: -900 LOC
- Extract to lib: +330 LOC (new), -500 LOC (removed duplication)
- Net: -1,070 LOC (~12% reduction)

**Maintenance Improvement:**

- DRY: Fix once in lib, applies to 6+ scripts
- Organization: Logical grouping by purpose
- Discoverability: Clear structure for new developers

### Qualitative Benefits

### 1. Testing Efficiency

- Test lib once → confidence in 6+ scripts
- Reduce test case duplication
- Clearer test organization (lib vs scripts)

### 2. Code Quality

- Consistent error handling patterns
- Consistent CLI interfaces
- Easier code review (standardized patterns)

### 3. Maintainability

- Bug fixes propagate automatically (lib)
- New scripts inherit best practices
- Clear separation of concerns

### 4. Onboarding

- Clear structure for new contributors
- Documented patterns in lib
- Logical grouping by purpose

---

## Risks & Mitigation

### Risk 1: Breaking Changes During Migration

**Likelihood:** Medium
**Impact:** High (broken CI/CD, pre-commit hooks)

**Mitigation:**

- Phase 0.1 (delete obsolete) is isolated, low risk
- Phase 0.2 (create lib) is additive, zero risk
- Phase 0.3-0.5 (refactor) done incrementally per script
- Update Taskfile + pre-commit immediately after each move
- Run validation suite after each phase
- Git commits per phase for easy rollback

### Risk 2: Incomplete Reference Updates

**Likelihood:** Medium
**Impact:** Medium (broken automation)

**Mitigation:**

- Use `grep -r "scripts/validate_" .` to find all references
- Update Taskfile.yml, pre-commit-config.yaml, docs/ simultaneously
- Automated link checking (`task docs:validate:links`)
- Test all Taskfile commands after migration

### Risk 3: Scope Creep

**Likelihood:** Medium
**Impact:** Medium (delays Phase 1 start)

**Mitigation:**

- Strict 8-12h time box
- Focus on structural refactoring, not functional changes
- No new features, no behavior changes
- Skip refactoring if time runs out (proceed to Phase 1)

---

## Success Criteria

### Must Have (Phase 0 Complete)

- ✅ 5 obsolete scripts deleted
- ✅ `scripts/lib/` created with 3 modules (frontmatter, validation, cli)
- ✅ 20-30 unit tests for lib modules (100% coverage)
- ✅ 6+ validation scripts refactored to use lib
- ✅ All Taskfile commands functional (verified)
- ✅ All pre-commit hooks functional (verified)
- ✅ scripts/README.md updated
- ✅ No broken references (link validation passing)

### Nice to Have (Optional)

- 🎯 All scripts moved to subdirectories (validation/, automation/, analysis/)
- 🎯 Common CLI interface across all scripts
- 🎯 Shared error reporting format

---

## Effort Estimate

| Phase | Description | Estimate | Risk |
|-------|-------------|----------|------|
| 0.1 | Delete obsolete scripts | 0.5h | Low |
| 0.2 | Create lib module + tests | 3-4h | Low |
| 0.3 | Refactor validation scripts | 2-3h | Medium |
| 0.4 | Refactor automation scripts | 1-2h | Medium |
| 0.5 | Refactor analysis scripts | 0.5-1h | Low |
| 0.6 | Validation & docs | 1-1.5h | Low |
| **TOTAL** | | **8-12h** | **Medium** |

**Comparison:**

- Phase 0: 8-12h (prep work)
- Phase 1 (original): 60-80h (scripts testing)
- Phase 1 (after Phase 0): 45-60h (25% reduction via lib testing)
- **Net savings:** 3-8h (via reduced testing surface)

---

## Execution Plan

### Phase 0.1: Delete Obsolete (30 min)

```bash
# Delete obsolete scripts
git rm scripts/fix_frontmatter.py
git rm scripts/restore_workflows.py
git rm scripts/test_optimization_idempotency.py
git rm scripts/manage_optimization_cache.py
git rm scripts/extract_action_items.py.backup

# Verify no broken imports
grep -r "restore_workflows\|test_optimization_idempotency\|manage_optimization_cache" . --exclude-dir=.git

# Commit
git commit -m "refactor(scripts): remove 5 obsolete one-time scripts

- fix_frontmatter.py (0 bytes, obsolete)
- restore_workflows.py (207 LOC, one-time workflow restoration)
- test_optimization_idempotency.py (274 LOC, one-time validation)
- manage_optimization_cache.py (~200 LOC, dependency of above)
- extract_action_items.py.backup (backup file)

Total removal: ~900 LOC, 0 test coverage impact

Part of Phase 0: Scripts Audit & Refactoring
Prepares for Testing Excellence Initiative (Phases 1-7)"
```

### Phase 0.2: Create Lib Module (3-4h)

```bash
# Create lib structure
mkdir -p scripts/lib
touch scripts/lib/__init__.py

# Create modules (via implementation)
# - scripts/lib/frontmatter.py (extract common parsing)
# - scripts/lib/validation.py (extract common validation)
# - scripts/lib/cli.py (extract common CLI patterns)

# Create tests
mkdir -p tests/scripts
# - tests/scripts/test_lib_frontmatter.py (10-12 tests)
# - tests/scripts/test_lib_validation.py (8-10 tests)
# - tests/scripts/test_lib_cli.py (4-6 tests)

# Run tests
uv run pytest tests/scripts/ -v

# Commit
git add scripts/lib/ tests/scripts/
git commit -m "feat(scripts): create common lib module with frontmatter, validation, CLI utilities

New modules:
- scripts/lib/frontmatter.py: Unified frontmatter parsing (lenient + strict)
- scripts/lib/validation.py: Base validator class, error collection
- scripts/lib/cli.py: Common CLI argument patterns

Test coverage:
- 22 new tests (100% lib coverage)
- Tests: test_lib_frontmatter.py, test_lib_validation.py, test_lib_cli.py

Benefits:
- DRY: Eliminates 3+ duplicate frontmatter implementations
- Reusable: 6+ scripts will use these patterns
- Testable: Test once, confidence everywhere

Part of Phase 0: Scripts Audit & Refactoring"
```

### Phase 0.3-0.5: Refactor Scripts (3-6h)

```bash
# Per script group:
# 1. Move scripts to subdirectory
# 2. Refactor to use scripts/lib/
# 3. Update imports
# 4. Update Taskfile.yml
# 5. Update pre-commit-config.yaml
# 6. Test functionality

# Example for validation scripts:
mkdir -p scripts/validation
git mv scripts/validate_*.py scripts/validation/

# Refactor (code changes)
# Update imports: from lib.frontmatter import extract_frontmatter
# Remove duplicate code
# Test: task validate:initiatives, task docs:validate:links, etc.

# Commit per group
git commit -m "refactor(scripts): migrate validation scripts to scripts/validation/

Moved 6 scripts:
- validate_initiatives.py
- validate_references.py
- validate_documentation.py
- validate_workflows.py
- validate_rules.py
- validate_task_format.py

Changes:
- Use scripts.lib.frontmatter for parsing (removes 150 LOC duplication)
- Use scripts.lib.validation.BaseValidator pattern
- Consistent CLI interface via scripts.lib.cli

Updated references:
- Taskfile.yml: 8 commands
- .pre-commit-config.yaml: 4 hooks

Testing: All validation commands functional (verified)

Part of Phase 0: Scripts Audit & Refactoring"
```

### Phase 0.6: Final Validation (1-1.5h)

```bash
# Run full test suite
task test:all

# Run all validation commands
task validate:initiatives
task docs:validate:links
task docs:validate:consistency
task validate:dependencies

# Run pre-commit hooks
pre-commit run --all-files

# Verify Taskfile commands (sample)
task scaffold:adr:config CONFIG=/tmp/test.yaml --dry-run
task archive:initiative NAME=test-init --dry-run

# Update docs
# - scripts/README.md: New structure, lib usage
# - Update references in docs/

# Commit
git commit -m "docs(scripts): update README with new structure and lib usage

Changes:
- Document scripts/lib/ common modules
- Document new directory structure (validation/, automation/, analysis/)
- Update usage examples with new paths
- Add migration notes

Part of Phase 0: Scripts Audit & Refactoring (Complete)"
```

---

## Continuation Prompt (For Next Session)

```markdown
Execute Phase 0 of the Testing Excellence & Automation Hardening initiative: Scripts Audit & Refactoring.

Context:
- 24 scripts total (8,707 LOC), 20 untested (83%)
- 5 obsolete scripts identified (~900 LOC)
- 3+ frontmatter parsing implementations (duplication)
- Plan: Remove obsolete, extract lib, refactor structure

Phases (8-12h total):
1. Delete 5 obsolete scripts (0.5h)
2. Create scripts/lib/ with frontmatter, validation, CLI modules + 22 tests (3-4h)
3. Refactor validation scripts to use lib (2-3h)
4. Refactor automation scripts (1-2h)
5. Refactor analysis scripts (0.5-1h)
6. Validation & documentation (1-1.5h)

Execute sequentially: Phase 0.1 → 0.2 → 0.3 → 0.4 → 0.5 → 0.6
Commit after each phase.
Verify functionality before proceeding to next phase.

Success criteria:
- 5 scripts deleted
- scripts/lib/ with 3 modules, 22 tests, 100% coverage
- 6+ scripts refactored
- All Taskfile/pre-commit functional
- scripts/README.md updated

See: docs/initiatives/active/2025-10-22-testing-excellence/artifacts/phase-0-scripts-audit.md
```

---

## References

- Hitchhiker's Guide to Python - Project Structure: <https://docs.python-guide.org/writing/structure/>
- Testing Excellence Initiative: `docs/initiatives/active/2025-10-22-testing-excellence/initiative.md`
- Scripts Inventory: `docs/initiatives/active/2025-10-22-testing-excellence/artifacts/scripts-inventory.md`
- Historical Issues: `docs/initiatives/active/2025-10-22-testing-excellence/research/historical-issues.md`

---

**Status:** ✅ Planning Complete, Ready for Execution
**Next:** Execute Phase 0.1 (Delete obsolete scripts)
