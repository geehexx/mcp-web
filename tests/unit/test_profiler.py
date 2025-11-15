"""Unit tests for profiler module."""

import asyncio
import time

import pytest

from mcp_web.profiler import (
    PerformanceCollector,
    ProfileResult,
    ProfilerContext,
    async_profile_context,
    profile,
)


class TestProfilerContext:
    """Tests for ProfilerContext synchronous profiling."""

    def test_basic_profiling(self):
        """Test basic synchronous profiling."""
        with ProfilerContext("test_operation") as ctx:
            time.sleep(0.01)

        assert ctx.name == "test_operation"
        assert ctx.duration_ms >= 10
        assert ctx.success is True
        assert ctx.error is None

    def test_profiling_with_exception(self):
        """Test profiling when exception occurs."""
        with pytest.raises(ValueError):
            with ProfilerContext("failing_operation") as ctx:
                raise ValueError("Test error")

        assert ctx.success is False
        assert "Test error" in ctx.error
        assert ctx.duration_ms > 0

    def test_metadata_tracking(self):
        """Test metadata is captured."""
        with ProfilerContext("test_op", metadata={"key": "value"}) as ctx:
            pass

        assert ctx.metadata == {"key": "value"}

    def test_get_result(self):
        """Test get_result returns ProfileResult."""
        with ProfilerContext("test_op") as ctx:
            pass

        result = ctx.get_result()
        assert isinstance(result, ProfileResult)
        assert result.name == "test_op"
        assert result.duration_ms > 0


@pytest.mark.asyncio
class TestAsyncProfileContext:
    """Tests for async_profile_context."""

    async def test_basic_async_profiling(self):
        """Test basic async profiling."""
        async with async_profile_context("async_operation") as ctx:
            await asyncio.sleep(0.01)

        assert ctx.name == "async_operation"
        assert ctx.duration_ms >= 10
        assert ctx.success is True

    async def test_async_profiling_with_exception(self):
        """Test async profiling with exception."""
        with pytest.raises(RuntimeError):
            async with async_profile_context("failing_async") as ctx:
                raise RuntimeError("Async error")

        assert ctx.success is False
        assert "Async error" in ctx.error

    async def test_async_metadata(self):
        """Test async context with metadata."""
        async with async_profile_context("test", metadata={"async": True}) as ctx:
            await asyncio.sleep(0.001)

        assert ctx.metadata["async"] is True


class TestProfileDecorator:
    """Tests for @profile decorator."""

    def test_profile_sync_function(self):
        """Test profiling synchronous function."""

        @profile
        def slow_function(x: int) -> int:
            time.sleep(0.01)
            return x * 2

        result = slow_function(5)
        assert result == 10

    def test_profile_preserves_function_metadata(self):
        """Test that @profile preserves function metadata."""

        @profile
        def documented_function() -> str:
            """This is a docstring."""
            return "result"

        assert documented_function.__name__ == "documented_function"
        assert documented_function.__doc__ == "This is a docstring."

    @pytest.mark.asyncio
    async def test_profile_async_function(self):
        """Test profiling async function."""

        @profile
        async def async_slow_function(x: int) -> int:
            await asyncio.sleep(0.01)
            return x * 3

        result = await async_slow_function(4)
        assert result == 12

    def test_profile_with_exception(self):
        """Test profiling function that raises exception."""

        @profile
        def failing_function() -> None:
            raise ValueError("Intentional failure")

        with pytest.raises(ValueError, match="Intentional failure"):
            failing_function()

    @pytest.mark.asyncio
    async def test_profile_async_with_exception(self):
        """Test profiling async function with exception."""

        @profile
        async def async_failing_function() -> None:
            await asyncio.sleep(0.001)
            raise RuntimeError("Async failure")

        with pytest.raises(RuntimeError, match="Async failure"):
            await async_failing_function()


class TestPerformanceCollector:
    """Tests for PerformanceCollector singleton."""

    def test_singleton_instance(self):
        """Test that PerformanceCollector is a singleton."""
        instance1 = PerformanceCollector.get_instance()
        instance2 = PerformanceCollector.get_instance()

        assert instance1 is instance2

    def test_record_result(self):
        """Test recording performance results."""
        collector = PerformanceCollector.get_instance()
        collector.clear()

        start = time.time()
        result = ProfileResult(
            name="test_operation",
            duration_ms=123.45,
            start_time=start,
            end_time=start + 0.12345,
            success=True,
        )

        collector.record(result)
        stats = collector.get_statistics()

        assert "test_operation" in stats
        assert stats["test_operation"]["count"] == 1
        assert stats["test_operation"]["avg_duration_ms"] == 123.45

    def test_multiple_recordings(self):
        """Test multiple recordings calculates correct averages."""
        collector = PerformanceCollector.get_instance()
        collector.clear()

        # Record multiple results
        start = time.time()
        for i, duration in enumerate([100, 200, 300]):
            result = ProfileResult(
                name="multi_test",
                duration_ms=duration,
                start_time=start + i,
                end_time=start + i + duration / 1000,
                success=True,
            )
            collector.record(result)

        stats = collector.get_statistics()
        assert stats["multi_test"]["count"] == 3
        assert stats["multi_test"]["avg_duration_ms"] == 200.0
        assert stats["multi_test"]["min_duration_ms"] == 100.0
        assert stats["multi_test"]["max_duration_ms"] == 300.0

    def test_success_failure_tracking(self):
        """Test tracking success and failure counts."""
        collector = PerformanceCollector.get_instance()
        collector.clear()

        # Record successes and failures
        start = time.time()
        for i, success in enumerate([True, True, False, True]):
            result = ProfileResult(
                name="tracked_op",
                duration_ms=100,
                start_time=start + i,
                end_time=start + i + 0.1,
                success=success,
            )
            collector.record(result)

        stats = collector.get_statistics()
        assert stats["tracked_op"]["success_count"] == 3
        assert stats["tracked_op"]["failure_count"] == 1

    def test_clear_results(self):
        """Test clearing all collected results."""
        collector = PerformanceCollector.get_instance()

        start = time.time()
        result = ProfileResult(
            name="to_clear",
            duration_ms=50,
            start_time=start,
            end_time=start + 0.05,
            success=True,
        )
        collector.record(result)

        collector.clear()
        stats = collector.get_statistics()

        assert len(stats) == 0

    def test_get_all_results(self):
        """Test retrieving all raw results."""
        collector = PerformanceCollector.get_instance()
        collector.clear()

        start = time.time()
        results_to_add = [
            ProfileResult(
                name=f"op_{i}",
                duration_ms=i * 10,
                start_time=start + i,
                end_time=start + i + (i * 10 / 1000),
                success=True,
            )
            for i in range(5)
        ]

        for result in results_to_add:
            collector.record(result)

        all_results = collector.get_all_results()
        assert len(all_results) == 5


@pytest.mark.asyncio
class TestIntegrationScenarios:
    """Integration tests for profiler module."""

    async def test_nested_profiling(self):
        """Test nested profiling contexts."""
        async with async_profile_context("outer") as outer_ctx:
            await asyncio.sleep(0.01)

            async with async_profile_context("inner") as inner_ctx:
                await asyncio.sleep(0.01)

            await asyncio.sleep(0.01)

        assert outer_ctx.duration_ms >= 30
        assert inner_ctx.duration_ms >= 10
        assert outer_ctx.duration_ms > inner_ctx.duration_ms

    async def test_concurrent_profiling(self):
        """Test concurrent async operations being profiled."""

        async def profiled_task(name: str, duration: float) -> str:
            async with async_profile_context(name):
                await asyncio.sleep(duration)
            return name

        results = await asyncio.gather(
            profiled_task("task1", 0.01),
            profiled_task("task2", 0.02),
            profiled_task("task3", 0.01),
        )

        assert len(results) == 3
        assert set(results) == {"task1", "task2", "task3"}

    def test_decorator_and_context_integration(self):
        """Test @profile decorator with manual context managers."""

        @profile
        def function_with_internal_profiling() -> int:
            with ProfilerContext("internal_operation"):
                time.sleep(0.01)
            return 42

        result = function_with_internal_profiling()
        assert result == 42

        collector = PerformanceCollector.get_instance()
        stats = collector.get_statistics()

        assert "function_with_internal_profiling" in stats
        assert "internal_operation" in stats
