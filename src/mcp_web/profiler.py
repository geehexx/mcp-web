"""Performance profiling utilities for mcp-web.

Provides decorators, context managers, and utilities for profiling
and monitoring performance of the summarization pipeline.

Example:
    >>> from mcp_web.profiler import profile, ProfilerContext
    >>>
    >>> @profile
    >>> async def my_function():
    ...     await do_work()
    >>>
    >>> with ProfilerContext("my_operation") as ctx:
    ...     do_work()
    >>> print(f"Took {ctx.duration_ms:.2f}ms")
"""

import asyncio
import cProfile
import functools
import json
import pstats
import time
from collections import defaultdict
from collections.abc import AsyncIterator, Callable, Iterator
from contextlib import asynccontextmanager, contextmanager
from dataclasses import asdict, dataclass, field
from io import StringIO
from pathlib import Path
from typing import Any, TypeVar

import structlog

F = TypeVar("F", bound=Callable[..., Any])

logger: structlog.stdlib.BoundLogger | None = None


def _get_logger() -> structlog.stdlib.BoundLogger:
    """Lazy logger initialization."""
    global logger
    if logger is None:
        logger = structlog.get_logger(__name__)
    return logger


@dataclass
class ProfileResult:
    """Result of a profiled operation.

    Attributes:
        name: Operation name
        duration_ms: Duration in milliseconds
        start_time: Start timestamp
        end_time: End timestamp
        metadata: Additional metadata
        success: Whether operation succeeded
        error: Error message if failed
    """

    name: str
    duration_ms: float
    start_time: float
    end_time: float
    metadata: dict[str, Any] = field(default_factory=dict)
    success: bool = True
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


class ProfilerContext:
    """Context manager for profiling a code block.

    Example:
        >>> with ProfilerContext("database_query") as ctx:
        ...     result = execute_query()
        >>> print(f"Query took {ctx.duration_ms:.2f}ms")
    """

    def __init__(self, name: str, metadata: dict[str, Any] | None = None):
        """Initialize profiler context.

        Args:
            name: Operation name
            metadata: Additional metadata
        """
        self.name = name
        self.metadata = metadata or {}
        self.start_time = 0.0
        self.end_time = 0.0
        self.duration_ms = 0.0
        self.success = True
        self.error: str | None = None

    def __enter__(self) -> "ProfilerContext":
        """Start timing."""
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Stop timing and record result."""
        self.end_time = time.perf_counter()
        self.duration_ms = (self.end_time - self.start_time) * 1000

        if exc_type is not None:
            self.success = False
            self.error = str(exc_val)

        _get_logger().debug(
            "profile_complete",
            name=self.name,
            duration_ms=self.duration_ms,
            success=self.success,
            **self.metadata,
        )

        # Record to global collector
        PerformanceCollector.get_instance().record(
            ProfileResult(
                name=self.name,
                duration_ms=self.duration_ms,
                start_time=self.start_time,
                end_time=self.end_time,
                metadata=self.metadata,
                success=self.success,
                error=self.error,
            )
        )

    def get_result(self) -> ProfileResult:
        """Get the profile result."""
        return ProfileResult(
            name=self.name,
            duration_ms=self.duration_ms,
            start_time=self.start_time,
            end_time=self.end_time,
            metadata=self.metadata,
            success=self.success,
            error=self.error,
        )


@asynccontextmanager
async def async_profile_context(
    name: str, metadata: dict[str, Any] | None = None
) -> AsyncIterator[ProfilerContext]:
    """Async context manager for profiling.

    Example:
        >>> async with async_profile_context("api_call") as ctx:
        ...     result = await call_api()
    """
    ctx = ProfilerContext(name, metadata)
    ctx.start_time = time.perf_counter()

    try:
        yield ctx
    except Exception as e:
        ctx.success = False
        ctx.error = str(e)
        raise
    finally:
        ctx.end_time = time.perf_counter()
        ctx.duration_ms = (ctx.end_time - ctx.start_time) * 1000

        _get_logger().debug(
            "async_profile_complete",
            name=ctx.name,
            duration_ms=ctx.duration_ms,
            success=ctx.success,
            **ctx.metadata,
        )

        PerformanceCollector.get_instance().record(ctx.get_result())


def profile(func: F) -> F:
    """Decorator to profile a function.

    Example:
        >>> @profile
        >>> def expensive_function():
        ...     time.sleep(1)
        >>>
        >>> @profile
        >>> async def async_function():
        ...     await asyncio.sleep(1)
    """

    if asyncio.iscoroutinefunction(func):

        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            async with async_profile_context(func.__name__):
                result = await func(*args, **kwargs)
                return result

        return async_wrapper  # type: ignore

    else:

        @functools.wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            with ProfilerContext(func.__name__):
                result = func(*args, **kwargs)
                return result

        return sync_wrapper  # type: ignore


class PerformanceCollector:
    """Global performance data collector.

    Singleton that collects all ProfileResult instances for later analysis.

    Example:
        >>> collector = PerformanceCollector.get_instance()
        >>> results = collector.get_results()
        >>> collector.export_json("performance.json")
    """

    _instance: "PerformanceCollector | None" = None

    def __init__(self) -> None:
        """Initialize collector."""
        self.results: list[ProfileResult] = []
        self.enabled = True

    @classmethod
    def get_instance(cls) -> "PerformanceCollector":
        """Get singleton instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def reset(cls) -> None:
        """Reset singleton instance."""
        cls._instance = None

    def record(self, result: ProfileResult) -> None:
        """Record a profile result."""
        if self.enabled:
            self.results.append(result)

    def get_results(self) -> list[ProfileResult]:
        """Get all collected results."""
        return self.results.copy()

    def get_by_name(self, name: str) -> list[ProfileResult]:
        """Get results filtered by name."""
        return [r for r in self.results if r.name == name]

    def get_statistics(self) -> dict[str, dict[str, float]]:
        """Get statistics grouped by operation name.

        Returns:
            Dictionary mapping operation names to statistics:
            - count: Number of executions
            - total_ms: Total time
            - mean_ms: Average time
            - min_ms: Minimum time
            - max_ms: Maximum time
            - success_rate: Success rate (0-1)
        """
        grouped: dict[str, list[float]] = defaultdict(list)
        success_counts: dict[str, int] = defaultdict(int)
        total_counts: dict[str, int] = defaultdict(int)

        for result in self.results:
            grouped[result.name].append(result.duration_ms)
            total_counts[result.name] += 1
            if result.success:
                success_counts[result.name] += 1

        stats = {}
        for name, durations in grouped.items():
            stats[name] = {
                "count": len(durations),
                "total_ms": sum(durations),
                "mean_ms": sum(durations) / len(durations),
                "min_ms": min(durations),
                "max_ms": max(durations),
                "success_rate": success_counts[name] / total_counts[name],
            }

        return stats

    def export_json(self, path: str | Path) -> None:
        """Export results to JSON file.

        Args:
            path: Output file path
        """
        path = Path(path)
        data = {
            "results": [r.to_dict() for r in self.results],
            "statistics": self.get_statistics(),
            "total_operations": len(self.results),
        }

        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

        _get_logger().info("performance_data_exported", path=str(path))

    def clear(self) -> None:
        """Clear all collected results."""
        self.results.clear()
        _get_logger().info("performance_data_cleared")

    def disable(self) -> None:
        """Disable collection."""
        self.enabled = False

    def enable(self) -> None:
        """Enable collection."""
        self.enabled = True


@contextmanager
def cprofile_context(
    output_path: str | Path | None = None, top_n: int = 30
) -> Iterator[cProfile.Profile]:
    """Context manager for cProfile profiling.

    Example:
        >>> with cprofile_context("profile.stats", top_n=50):
        ...     expensive_function()
    """
    profiler = cProfile.Profile()
    profiler.enable()

    try:
        yield profiler
    finally:
        profiler.disable()

        if output_path:
            profiler.dump_stats(str(output_path))
            _get_logger().info("cprofile_saved", path=str(output_path))

        # Print stats to stdout
        stream = StringIO()
        stats = pstats.Stats(profiler, stream=stream)
        stats.sort_stats("cumulative")
        stats.print_stats(top_n)

        print("\n=== cProfile Results ===")
        print(stream.getvalue())


class ComponentTimer:
    """Track timing for pipeline components.

    Example:
        >>> timer = ComponentTimer()
        >>> timer.start("fetch")
        >>> await fetch_url()
        >>> timer.stop("fetch")
        >>> timer.start("summarize")
        >>> await summarize()
        >>> timer.stop("summarize")
        >>> print(timer.get_summary())
    """

    def __init__(self) -> None:
        """Initialize timer."""
        self.timings: dict[str, list[float]] = defaultdict(list)
        self._active: dict[str, float] = {}

    def start(self, component: str) -> None:
        """Start timing a component."""
        self._active[component] = time.perf_counter()

    def stop(self, component: str) -> float:
        """Stop timing a component and return duration.

        Args:
            component: Component name

        Returns:
            Duration in milliseconds

        Raises:
            ValueError: If component wasn't started
        """
        if component not in self._active:
            raise ValueError(f"Component '{component}' not started")

        start_time = self._active.pop(component)
        duration_ms = (time.perf_counter() - start_time) * 1000
        self.timings[component].append(duration_ms)
        return duration_ms

    @contextmanager
    def time(self, component: str) -> Iterator[None]:
        """Context manager for timing.

        Example:
            >>> timer = ComponentTimer()
            >>> with timer.time("fetch"):
            ...     await fetch_url()
        """
        self.start(component)
        try:
            yield
        finally:
            self.stop(component)

    def get_summary(self) -> dict[str, dict[str, float]]:
        """Get timing summary.

        Returns:
            Dictionary with statistics for each component
        """
        summary = {}
        for component, durations in self.timings.items():
            summary[component] = {
                "count": len(durations),
                "total_ms": sum(durations),
                "mean_ms": sum(durations) / len(durations),
                "min_ms": min(durations),
                "max_ms": max(durations),
            }
        return summary

    def reset(self) -> None:
        """Reset all timings."""
        self.timings.clear()
        self._active.clear()


def format_duration(ms: float) -> str:
    """Format duration in human-readable form.

    Example:
        >>> format_duration(1500)
        '1.50s'
        >>> format_duration(250)
        '250ms'
    """
    if ms >= 1000:
        return f"{ms / 1000:.2f}s"
    else:
        return f"{ms:.0f}ms"
