"""
Unit tests for task format validation.

Tests validation of task system compliance per Section 1.11 of agent directives,
including workflow prefix presence, completed task preservation, and correct attribution.

Based on violations from 2025-10-19 sessions (Phase 5 implementation).
"""

from typing import Any

import pytest


@pytest.fixture
def valid_task_updates() -> list[dict[str, Any]]:
    """Valid task update examples that should pass validation."""
    return [
        # Valid simple task list
        {
            "plan": [
                {"step": "1. /detect-context - Analyze project state", "status": "completed"},
                {"step": "2. /work-routing - Route to workflow", "status": "completed"},
                {"step": "3. /implement - Execute implementation", "status": "in_progress"},
                {"step": "4. /validate - Run validation", "status": "pending"},
            ]
        },
        # Valid hierarchical tasks
        {
            "plan": [
                {"step": "1. /work - Orchestrate work", "status": "in_progress"},
                {"step": "  1.1. /load-context - Load files", "status": "completed"},
                {"step": "  1.2. /implement - Design tests", "status": "in_progress"},
                {"step": "  1.3. /implement - Write code", "status": "pending"},
            ]
        },
        # Valid deep nesting
        {
            "plan": [
                {"step": "1. /work - Main workflow", "status": "in_progress"},
                {"step": "  1.1. /implement - Phase 1", "status": "in_progress"},
                {"step": "    1.1.1. /implement - Subtask A", "status": "completed"},
                {"step": "    1.1.2. /implement - Subtask B", "status": "in_progress"},
            ]
        },
    ]


@pytest.fixture
def missing_prefix_violations() -> list[dict[str, Any]]:
    """Task updates missing workflow prefixes (real violations from Phase 5)."""
    return [
        # Violation 1: No workflow prefix at all
        {
            "plan": [
                {"step": "1. Analyze project state", "status": "in_progress"},
                {"step": "2. Execute implementation", "status": "pending"},
            ],
            "expected_violations": [
                "Task '1. Analyze project state' missing workflow prefix",
                "Task '2. Execute implementation' missing workflow prefix",
            ],
        },
        # Violation 2: Real examples from Phase 5
        {
            "plan": [
                {"step": "4. Execute Phase 5", "status": "in_progress"},
                {
                    "step": "  4.2. Add frontmatter to all workflows (batch 1-8)",
                    "status": "completed",
                },
                {
                    "step": "  4.3. Add frontmatter to all workflows (batch 9-19)",
                    "status": "completed",
                },
                {"step": "  4.5. Create validation script", "status": "in_progress"},
            ],
            "expected_violations": [
                "Task '4. Execute Phase 5' missing workflow prefix",
                "Task '  4.2. Add frontmatter to all workflows (batch 1-8)' missing workflow prefix",
                "Task '  4.3. Add frontmatter to all workflows (batch 9-19)' missing workflow prefix",
                "Task '  4.5. Create validation script' missing workflow prefix",
            ],
        },
        # Violation 3: Subtask missing prefix
        {
            "plan": [
                {"step": "3. /work - Orchestrate work", "status": "in_progress"},
                {"step": "  3.1. Create directory structure", "status": "completed"},
                {"step": "  3.2. /implement - Write code", "status": "pending"},
            ],
            "expected_violations": [
                "Task '  3.1. Create directory structure' missing workflow prefix",
            ],
        },
    ]


@pytest.fixture
def removed_tasks_violations() -> list[dict[str, Any]]:
    """Task updates that removed completed tasks (history loss)."""
    return [
        # Violation 1: Removed completed tasks 1-6, only showing 7-8
        {
            "previous": {
                "plan": [
                    {"step": "4. /work - Execute Phase 5", "status": "in_progress"},
                    {"step": "  4.1. /implement - Define schema", "status": "completed"},
                    {"step": "  4.2. /implement - Add frontmatter batch 1", "status": "completed"},
                    {"step": "  4.3. /implement - Add frontmatter batch 2", "status": "completed"},
                    {"step": "  4.4. /implement - Add to rules", "status": "completed"},
                    {"step": "  4.5. /implement - Create validator", "status": "completed"},
                    {"step": "  4.6. /implement - Generate indexes", "status": "completed"},
                ]
            },
            "current": {
                "plan": [
                    {"step": "4. /work - Execute Phase 5", "status": "in_progress"},
                    {"step": "  4.7. /implement - Fix validation issues", "status": "in_progress"},
                    {"step": "  4.8. /implement - Commit changes", "status": "pending"},
                ]
            },
            "expected_violations": [
                "Removed completed task: '  4.1. /implement - Define schema'",
                "Removed completed task: '  4.2. /implement - Add frontmatter batch 1'",
                "Removed completed task: '  4.3. /implement - Add frontmatter batch 2'",
                "Removed completed task: '  4.4. /implement - Add to rules'",
                "Removed completed task: '  4.5. /implement - Create validator'",
                "Removed completed task: '  4.6. /implement - Generate indexes'",
            ],
        },
        # Violation 2: Removed parent task
        {
            "previous": {
                "plan": [
                    {"step": "1. /detect-context - Analyze state", "status": "completed"},
                    {"step": "2. /work-routing - Route workflow", "status": "completed"},
                    {"step": "3. /implement - Execute work", "status": "in_progress"},
                ]
            },
            "current": {
                "plan": [
                    {"step": "3. /implement - Execute work", "status": "in_progress"},
                    {"step": "  3.1. /implement - Write tests", "status": "pending"},
                ]
            },
            "expected_violations": [
                "Removed completed task: '1. /detect-context - Analyze state'",
                "Removed completed task: '2. /work-routing - Route workflow'",
            ],
        },
    ]


@pytest.fixture
def wrong_attribution_violations() -> list[dict[str, Any]]:
    """Tasks with wrong workflow attribution (orchestrator vs executor)."""
    return [
        # Violation 1: /work doing execution work
        {
            "plan": [
                {"step": "1. /work - Fix prerequisite issues", "status": "in_progress"},
                {"step": "2. /work - Create validation script", "status": "pending"},
            ],
            "expected_violations": [
                "Task '1. /work - Fix prerequisite issues' uses orchestrator /work for execution",
                "Task '2. /work - Create validation script' uses orchestrator /work for execution",
            ],
        },
        # Violation 2: Wrong sub-workflow attribution
        {
            "plan": [
                {"step": "5. /work - Session end protocol", "status": "pending"},
            ],
            "expected_violations": [
                "Task '5. /work - Session end protocol' should use /work-session-protocol",
            ],
        },
        # Violation 3: /plan doing implementation
        {
            "plan": [
                {"step": "3. /plan - Write implementation code", "status": "in_progress"},
            ],
            "expected_violations": [
                "Task '3. /plan - Write implementation code' uses /plan for execution work",
            ],
        },
    ]


@pytest.fixture
def invalid_numbering_violations() -> list[dict[str, Any]]:
    """Tasks with invalid hierarchical numbering."""
    return [
        # Violation 1: Skipped number
        {
            "plan": [
                {"step": "1. /implement - Task 1", "status": "completed"},
                {"step": "3. /implement - Task 3", "status": "in_progress"},  # Skipped 2
            ],
            "expected_violations": [
                "Numbering gap: expected 2, found 3",
            ],
        },
        # Violation 2: Invalid subtask numbering
        {
            "plan": [
                {"step": "1. /work - Main task", "status": "in_progress"},
                {"step": "  1.1. /implement - Subtask 1", "status": "completed"},
                {"step": "  1.3. /implement - Subtask 3", "status": "pending"},  # Skipped 1.2
            ],
            "expected_violations": [
                "Numbering gap in subtasks: expected 1.2, found 1.3",
            ],
        },
    ]


@pytest.fixture
def multiple_in_progress_violations() -> list[dict[str, Any]]:
    """Multiple tasks marked in_progress simultaneously."""
    return [
        {
            "plan": [
                {"step": "1. /implement - Task A", "status": "in_progress"},
                {"step": "2. /implement - Task B", "status": "in_progress"},  # Violation!
                {"step": "3. /implement - Task C", "status": "pending"},
            ],
            "expected_violations": [
                "Multiple tasks in_progress: only one task can be in_progress at a time",
            ],
        },
    ]


class TestTaskFormatValidator:
    """Test task format validation logic."""

    def test_valid_tasks_pass(self, valid_task_updates: list[dict[str, Any]]) -> None:
        """Test that valid task formats pass validation."""
        # Import will fail until we create the validator
        from scripts.validate_task_format import TaskFormatValidator

        validator = TaskFormatValidator()

        for task_update in valid_task_updates:
            violations = validator.validate_task_update(task_update["plan"])
            assert len(violations) == 0, f"Valid tasks should not have violations: {violations}"

    def test_missing_prefix_detected(self, missing_prefix_violations: list[dict[str, Any]]) -> None:
        """Test detection of missing workflow prefixes."""
        from scripts.validate_task_format import TaskFormatValidator

        validator = TaskFormatValidator()

        for case in missing_prefix_violations:
            violations = validator.validate_task_update(case["plan"])

            # Check that all expected violations are detected
            for expected in case["expected_violations"]:
                assert any(expected in v.message for v in violations), (
                    f"Expected violation not detected: {expected}"
                )

    def test_removed_tasks_detected(self, removed_tasks_violations: list[dict[str, Any]]) -> None:
        """Test detection of removed completed tasks."""
        from scripts.validate_task_format import TaskFormatValidator

        validator = TaskFormatValidator()

        for case in removed_tasks_violations:
            violations = validator.validate_task_history(
                previous_plan=case["previous"]["plan"], current_plan=case["current"]["plan"]
            )

            # Check that all expected violations are detected
            for expected in case["expected_violations"]:
                assert any(expected in v.message for v in violations), (
                    f"Expected violation not detected: {expected}"
                )

    def test_wrong_attribution_detected(
        self, wrong_attribution_violations: list[dict[str, Any]]
    ) -> None:
        """Test detection of wrong workflow attribution."""
        from scripts.validate_task_format import TaskFormatValidator

        validator = TaskFormatValidator()

        for case in wrong_attribution_violations:
            violations = validator.validate_task_update(case["plan"])

            # Check that all expected violations are detected
            for expected in case["expected_violations"]:
                assert any(expected in v.message for v in violations), (
                    f"Expected violation not detected: {expected}"
                )

    def test_invalid_numbering_detected(
        self, invalid_numbering_violations: list[dict[str, Any]]
    ) -> None:
        """Test detection of invalid task numbering."""
        from scripts.validate_task_format import TaskFormatValidator

        validator = TaskFormatValidator()

        for case in invalid_numbering_violations:
            violations = validator.validate_task_update(case["plan"])

            # Check that all expected violations are detected
            for expected in case["expected_violations"]:
                assert any(expected in v.message for v in violations), (
                    f"Expected violation not detected: {expected}"
                )

    def test_multiple_in_progress_detected(
        self, multiple_in_progress_violations: list[dict[str, Any]]
    ) -> None:
        """Test detection of multiple in_progress tasks."""
        from scripts.validate_task_format import TaskFormatValidator

        validator = TaskFormatValidator()

        for case in multiple_in_progress_violations:
            violations = validator.validate_task_update(case["plan"])

            # Check that all expected violations are detected
            for expected in case["expected_violations"]:
                assert any(expected in v.message for v in violations), (
                    f"Expected violation not detected: {expected}"
                )

    def test_severity_levels(self) -> None:
        """Test that violations have correct severity levels."""
        from scripts.validate_task_format import TaskFormatValidator

        validator = TaskFormatValidator()

        # Missing prefix = critical
        result = validator.validate_task_update(
            [{"step": "1. Do something", "status": "in_progress"}]
        )
        assert any(v.severity == "critical" for v in result)

        # Multiple in_progress = warning
        result = validator.validate_task_update(
            [
                {"step": "1. /implement - Task A", "status": "in_progress"},
                {"step": "2. /implement - Task B", "status": "in_progress"},
            ]
        )
        assert any(v.severity == "warning" for v in result)


class TestViolationMessages:
    """Test that violation messages are clear and actionable."""

    def test_missing_prefix_message_shows_example(self) -> None:
        """Test that missing prefix errors show correct format."""
        from scripts.validate_task_format import TaskFormatValidator

        validator = TaskFormatValidator()
        violations = validator.validate_task_update(
            [{"step": "1. Add feature", "status": "pending"}]
        )

        # Should suggest correct format
        assert any("/<workflow>" in v.message for v in violations)
        assert any("1. /implement - Add feature" in v.message for v in violations)

    def test_removed_task_message_shows_which_tasks(self) -> None:
        """Test that removed task errors list specific removed tasks."""
        from scripts.validate_task_format import TaskFormatValidator

        validator = TaskFormatValidator()
        previous = [
            {"step": "1. /implement - Task A", "status": "completed"},
            {"step": "2. /implement - Task B", "status": "in_progress"},
        ]
        current = [{"step": "2. /implement - Task B", "status": "in_progress"}]

        violations = validator.validate_task_history(previous, current)

        # Should specifically mention Task A was removed
        assert any("Task A" in v.message for v in violations)

    def test_wrong_attribution_shows_correct_workflow(self) -> None:
        """Test that attribution errors suggest correct workflow."""
        from scripts.validate_task_format import TaskFormatValidator

        validator = TaskFormatValidator()
        violations = validator.validate_task_update(
            [{"step": "1. /work - Fix bug", "status": "in_progress"}]
        )

        # Should suggest /implement for execution work
        assert any("/implement" in v.message for v in violations)
