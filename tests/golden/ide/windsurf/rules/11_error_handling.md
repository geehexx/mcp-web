---
trigger: model_decision
description: Apply when handling errors implementing error recovery or debugging failures

---

# Error Handling and Recovery

**Purpose:** Quick-reference patterns for robust error handling in workflows.

---

## Quick Lookup

| Scenario | Pattern | Priority |
|----------|---------|----------|
| File not found | Graceful fallback | High |
| API rate limit | Exponential backoff | High |
| Test failure | Fail fast | High |
| Batch operation failure | Individual retry | Medium |
| Validation error | Early exit | High |
| Network timeout | Retry with timeout | Medium |

---

## Pattern 1: Graceful Degradation

**Use:** Handle missing files or resources

```python
# Check before reading
try:
    content = read_file(path)
except FileNotFoundError:
    # Fallback: use default or skip
    content = get_default_content()
    log_warning(f"File not found: {path}, using default")
```

**Workflow example:**

```python
# Load initiative files with fallback
required_files = ["initiative.md", "plan.md"]
optional_files = ["notes.md", "research.md"]

# Load required (fail if missing)
for file in required_files:
    content = read_file(file)  # Raises if missing

# Load optional (skip if missing)
for file in optional_files:
    try:
        content = read_file(file)
        process(content)
    except FileNotFoundError:
        continue  # Skip gracefully
```

---

## Pattern 2: Retry with Exponential Backoff

**Use:** Handle transient failures (API, network)

```python
import time

def retry_with_backoff(func, max_retries=3, base_delay=1.0):
    for attempt in range(max_retries):
        try:
            return func()
        except TransientError as e:
            if attempt == max_retries - 1:
                raise  # Final attempt failed
            delay = base_delay * (2 ** attempt)
            time.sleep(delay)
            continue
```

**Example:**

```python
# Retry API call with backoff
result = retry_with_backoff(
    lambda: api_call(url),
    max_retries=3,
    base_delay=1.0
)
```

---

## Pattern 3: Batch with Individual Fallback

**Use:** Batch operations where some items may fail

```python
def batch_with_fallback(items, batch_func, single_func):
    try:
        # Try batch first (fast)
        return batch_func(items)
    except BatchError:
        # Fallback: process individually
        results = []
        for item in items:
            try:
                results.append(single_func(item))
            except Exception as e:
                results.append(None)  # Mark failure
                log_error(f"Failed to process {item}: {e}")
        return results
```

**Example:**

```python
# Batch file read with fallback
files = ["file1.md", "file2.md", "file3.md"]
contents = batch_with_fallback(
    files,
    batch_func=lambda f: mcp0_read_multiple_files(f),
    single_func=lambda f: read_file(f)
)
```

---

## Pattern 4: Validation with Early Exit

**Use:** Validate inputs before expensive operations

```python
def validate_and_process(data):
    # Validate early
    errors = validate(data)
    if errors:
        raise ValidationError(f"Invalid data: {errors}")

    # Expensive operation only if valid
    return process(data)
```

**Workflow example:**

```python
# Validate before running tests
def run_tests():
    # Check prerequisites
    if not check_dependencies():
        raise ValidationError("Missing dependencies")

    if not check_test_files():
        raise ValidationError("No test files found")

    # Run tests (expensive)
    return run_command("task test", cwd=repo_root)
```

---

## Pattern 5: Fail Fast

**Use:** Stop immediately on critical errors

```python
# ✅ Fail fast on critical errors
def critical_operation():
    if not precondition_met():
        raise CriticalError("Precondition failed")

    # Continue only if safe
    return perform_operation()

# ❌ Don't: Continue after critical failure
def bad_operation():
    try:
        if not precondition_met():
            log_error("Precondition failed")
        # Continues anyway - dangerous!
        return perform_operation()
    except Exception:
        pass  # Swallows errors
```

---

## Pattern 6: Timeout Handling

**Use:** Prevent hanging on long operations

```python
import signal

def with_timeout(func, timeout_seconds=30):
    def timeout_handler(signum, frame):
        raise TimeoutError(f"Operation timed out after {timeout_seconds}s")

    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout_seconds)
    try:
        result = func()
        signal.alarm(0)  # Cancel alarm
        return result
    except TimeoutError:
        signal.alarm(0)
        raise
```

**Example:**

```python
# Run command with timeout
try:
    result = with_timeout(
        lambda: run_command("long_running_test", cwd=repo_root),
        timeout_seconds=300  # 5 minutes
    )
except TimeoutError:
    log_error("Test timed out")
    raise
```

---

## Pattern 7: Context Manager for Cleanup

**Use:** Ensure cleanup even on errors

```python
from contextlib import contextmanager

@contextmanager
def temporary_file(path):
    # Setup
    create_file(path)
    try:
        yield path
    finally:
        # Cleanup (always runs)
        delete_file(path)

# Usage
with temporary_file("/tmp/test.txt") as temp:
    process(temp)  # File deleted even if this fails
```

---

## Validation Patterns

### Input Validation

```python
def validate_file_path(path):
    """Validate file path before operations."""
    if not path:
        raise ValueError("Path cannot be empty")

    if not path.startswith("/"):
        raise ValueError("Path must be absolute")

    if not path.endswith(".md"):
        raise ValueError("Only .md files supported")

    return path
```

### Workflow State Validation

```python
def validate_workflow_state():
    """Validate state before proceeding."""
    # Check git status
    status = run_command("git status --short", cwd=repo_root)
    if "??" in status:
        raise ValidationError("Untracked files present")

    # Check tests
    result = run_command("task test:quick", cwd=repo_root)
    if result.exit_code != 0:
        raise ValidationError("Tests failing")

    return True
```

---

## Error Recovery Strategies

| Error Type | Strategy | Example |
|------------|----------|---------|
| File not found | Use default or skip | Load optional config |
| API rate limit | Exponential backoff | Retry with delay |
| Network timeout | Retry with timeout | API call with 30s limit |
| Validation error | Early exit | Stop before expensive op |
| Test failure | Fail fast | Don't commit if tests fail |
| Batch failure | Individual retry | Process one-by-one |
| Resource exhaustion | Chunked processing | Process in smaller batches |

---

## Anti-Patterns

### ❌ Swallowing Errors

```python
# Bad: Hides problems
try:
    critical_operation()
except Exception:
    pass  # Silent failure

# Good: Log and re-raise or handle
try:
    critical_operation()
except Exception as e:
    log_error(f"Critical operation failed: {e}")
    raise
```

### ❌ Overly Broad Catches

```python
# Bad: Catches everything
try:
    operation()
except Exception:  # Too broad
    handle_error()

# Good: Specific exceptions
try:
    operation()
except FileNotFoundError:
    handle_missing_file()
except PermissionError:
    handle_permission_denied()
```

### ❌ Retry Without Limit

```python
# Bad: Infinite retries
while True:
    try:
        operation()
        break
    except:
        continue  # Never stops

# Good: Limited retries
for attempt in range(3):
    try:
        operation()
        break
    except TransientError:
        if attempt == 2:
            raise
        time.sleep(1)
```

---

## Workflow Integration

### Pre-commit Validation

```python
def pre_commit_checks():
    """Run before committing."""
    # Validate code
    run_command("task lint", cwd=repo_root)

    # Run tests
    run_command("task test:quick", cwd=repo_root)

    # Check for secrets
    run_command("task security:check", cwd=repo_root)
```

### Session End Validation

```python
def session_end_checks():
    """Validate before ending session."""
    # Check git status
    status = run_command("git status --short", cwd=repo_root)
    if status.strip():
        raise ValidationError("Uncommitted changes")

    # Verify tests pass
    result = run_command("task test", cwd=repo_root)
    if result.exit_code != 0:
        raise ValidationError("Tests failing")

    return True
```

---

## Quick Decision Matrix

```text
Operation failed?
├─ Critical error? ─────────────────────┐
│  ├─ Yes: Fail fast, don't continue   │
│  └─ No: Continue to recovery         │
│                                       │
├─ Transient error? ───────────────────┤
│  ├─ Yes: Retry with backoff          │
│  └─ No: Check if recoverable         │
│                                       │
├─ Recoverable? ───────────────────────┤
│  ├─ Yes: Apply recovery strategy     │
│  └─ No: Fail gracefully              │
│                                       │
└─ Batch operation? ───────────────────┤
   ├─ Yes: Try individual items        │
   └─ No: Log and raise                │
```

---

## References

- [batch-operations.md](./15_tool_patterns.md) - Batch error handling
- [tool-patterns.md](./15_tool_patterns.md) - Tool-specific errors
- [04_security.md](./06_security_practices.md) - Security validation

---

**Version:** 1.0.0
**Maintained by:** mcp-web core team

---

## Rule Metadata

**File:** `11_error_handling.md`
**Trigger:** model_decision
**Estimated Tokens:** ~2,200
**Last Updated:** 2025-10-21
**Status:** Active

**Can be @mentioned:** Yes (hybrid loading)

**Topics Covered:**

- Error patterns
- Recovery strategies
- Debugging
- Graceful degradation

**Workflow References:**

- /implement - Error handling
- /validate - Error testing

**Dependencies:**

- Source: error-handling-patterns.md

**Changelog:**

- 2025-10-21: Created from error-handling-patterns.md
