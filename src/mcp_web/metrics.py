"""Metrics collection and logging for mcp-web.

Tracks:
- Fetch performance (httpx vs Playwright)
- Extraction success rates
- Token usage
- Cache hit/miss ratios
- Error frequencies

Design Decision DD-018: Structured logging for observability.
"""

import json
import time
from collections import defaultdict
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

import structlog

logger = structlog.get_logger()


@dataclass
class FetchMetrics:
    """Metrics for URL fetching operations."""

    url: str
    method: str  # 'httpx' or 'playwright'
    duration_ms: float
    status_code: int
    content_size: int
    success: bool
    error: str | None = None
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ExtractionMetrics:
    """Metrics for content extraction."""

    url: str
    content_length: int
    extracted_length: int
    extraction_ratio: float
    duration_ms: float
    success: bool
    error: str | None = None
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ChunkingMetrics:
    """Metrics for content chunking."""

    content_length: int
    num_chunks: int
    avg_chunk_size: float
    duration_ms: float
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class SummarizationMetrics:
    """Metrics for summarization."""

    input_tokens: int
    output_tokens: int
    model: str
    duration_ms: float
    cost_estimate: float  # USD
    success: bool
    error: str | None = None
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class CacheMetrics:
    """Metrics for cache operations."""

    operation: str  # 'hit', 'miss', 'set', 'evict'
    key: str
    size_bytes: int | None = None
    timestamp: datetime = field(default_factory=datetime.now)


class MetricsCollector:
    """Centralized metrics collection.

    Example:
        >>> collector = MetricsCollector()
        >>> collector.record_fetch("https://example.com", "httpx", 125.5, 200, 5000, True)
        >>> metrics = collector.export_metrics()
    """

    def __init__(self, enabled: bool = True, export_path: Path | None = None):
        """Initialize metrics collector.

        Args:
            enabled: Whether to collect metrics
            export_path: Optional path to export metrics JSON
        """
        self.enabled = enabled
        self.export_path = export_path

        # Metric storage
        self.fetch_metrics: list[FetchMetrics] = []
        self.extraction_metrics: list[ExtractionMetrics] = []
        self.chunking_metrics: list[ChunkingMetrics] = []
        self.summarization_metrics: list[SummarizationMetrics] = []
        self.cache_metrics: list[CacheMetrics] = []

        # Aggregated counters
        self.counters: dict[str, int] = defaultdict(int)
        self.timers: dict[str, list[float]] = defaultdict(list)
        self.errors: list[dict[str, Any]] = []

    def record_fetch(
        self,
        url: str,
        method: str,
        duration_ms: float,
        status_code: int,
        content_size: int,
        success: bool,
        error: str | None = None,
    ) -> None:
        """Record fetch metrics."""
        if not self.enabled:
            return

        metric = FetchMetrics(
            url=url,
            method=method,
            duration_ms=duration_ms,
            status_code=status_code,
            content_size=content_size,
            success=success,
            error=error,
        )
        self.fetch_metrics.append(metric)
        self.counters[f"fetch_{method}"] += 1
        self.timers[f"fetch_{method}_duration"].append(duration_ms)

        if not success:
            self.counters["fetch_errors"] += 1

        logger.info(
            "fetch_completed",
            url=url,
            method=method,
            duration_ms=duration_ms,
            success=success,
        )

    def record_extraction(
        self,
        url: str,
        content_length: int,
        extracted_length: int,
        duration_ms: float,
        success: bool,
        error: str | None = None,
    ) -> None:
        """Record extraction metrics."""
        if not self.enabled:
            return

        ratio = extracted_length / content_length if content_length > 0 else 0.0
        metric = ExtractionMetrics(
            url=url,
            content_length=content_length,
            extracted_length=extracted_length,
            extraction_ratio=ratio,
            duration_ms=duration_ms,
            success=success,
            error=error,
        )
        self.extraction_metrics.append(metric)
        self.counters["extractions"] += 1
        self.timers["extraction_duration"].append(duration_ms)

        if not success:
            self.counters["extraction_errors"] += 1

        logger.info(
            "extraction_completed",
            url=url,
            extracted_length=extracted_length,
            ratio=ratio,
            success=success,
        )

    def record_chunking(
        self,
        content_length: int,
        num_chunks: int,
        avg_chunk_size: float,
        duration_ms: float,
    ) -> None:
        """Record chunking metrics."""
        if not self.enabled:
            return

        metric = ChunkingMetrics(
            content_length=content_length,
            num_chunks=num_chunks,
            avg_chunk_size=avg_chunk_size,
            duration_ms=duration_ms,
        )
        self.chunking_metrics.append(metric)
        self.counters["chunking_operations"] += 1
        self.timers["chunking_duration"].append(duration_ms)

        logger.info(
            "chunking_completed",
            content_length=content_length,
            num_chunks=num_chunks,
            avg_chunk_size=avg_chunk_size,
        )

    def record_summarization(
        self,
        input_tokens: int,
        output_tokens: int,
        model: str,
        duration_ms: float,
        success: bool,
        error: str | None = None,
    ) -> None:
        """Record summarization metrics."""
        if not self.enabled:
            return

        # Rough cost estimation (GPT-4o-mini pricing as of 2025)
        cost_estimate = (input_tokens * 0.00015 / 1000) + (output_tokens * 0.0006 / 1000)

        metric = SummarizationMetrics(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            model=model,
            duration_ms=duration_ms,
            cost_estimate=cost_estimate,
            success=success,
            error=error,
        )
        self.summarization_metrics.append(metric)
        self.counters["summarizations"] += 1
        self.counters["total_input_tokens"] += input_tokens
        self.counters["total_output_tokens"] += output_tokens
        self.timers["summarization_duration"].append(duration_ms)

        if not success:
            self.counters["summarization_errors"] += 1

        logger.info(
            "summarization_completed",
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            model=model,
            cost_usd=cost_estimate,
            success=success,
        )

    def record_cache_operation(
        self,
        operation: str,
        key: str,
        size_bytes: int | None = None,
    ) -> None:
        """Record cache operation."""
        if not self.enabled:
            return

        metric = CacheMetrics(
            operation=operation,
            key=key,
            size_bytes=size_bytes,
        )
        self.cache_metrics.append(metric)
        self.counters[f"cache_{operation}"] += 1

        logger.debug("cache_operation", operation=operation, key=key[:50])

    def record_error(
        self, module: str, error: Exception, context: dict[str, Any] | None = None
    ) -> None:
        """Record error for diagnostics."""
        if not self.enabled:
            return

        error_data = {
            "module": module,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context or {},
            "timestamp": datetime.now().isoformat(),
        }
        self.errors.append(error_data)
        self.counters[f"error_{module}"] += 1

        logger.error(
            "error_recorded",
            module=module,
            error_type=type(error).__name__,
            error_message=str(error),
        )

    @contextmanager
    def timer(self, operation: str) -> Iterator[None]:
        """Context manager for timing operations.

        Example:
            >>> with collector.timer("fetch"):
            ...     # operation
            ...     pass
        """
        start = time.perf_counter()
        try:
            yield
        finally:
            duration_ms = (time.perf_counter() - start) * 1000
            self.timers[operation].append(duration_ms)

    def export_metrics(self) -> dict[str, Any]:
        """Export all metrics as dict.

        Returns:
            Dictionary with aggregated metrics
        """
        # Calculate aggregated statistics
        avg_durations = {
            key: sum(vals) / len(vals) if vals else 0.0 for key, vals in self.timers.items()
        }

        cache_hit_rate = 0.0
        cache_hits = self.counters.get("cache_hit", 0)
        cache_misses = self.counters.get("cache_miss", 0)
        if cache_hits + cache_misses > 0:
            cache_hit_rate = cache_hits / (cache_hits + cache_misses)

        total_cost = sum(m.cost_estimate for m in self.summarization_metrics)

        return {
            "summary": {
                "total_fetches": len(self.fetch_metrics),
                "total_extractions": len(self.extraction_metrics),
                "total_summarizations": len(self.summarization_metrics),
                "total_errors": len(self.errors),
                "cache_hit_rate": cache_hit_rate,
                "total_cost_usd": round(total_cost, 4),
            },
            "counters": dict(self.counters),
            "avg_durations_ms": avg_durations,
            "errors": self.errors,
        }

    def save_metrics(self, path: Path | None = None) -> None:
        """Save metrics to JSON file.

        Args:
            path: Output path (defaults to self.export_path)
        """
        output_path = path or self.export_path
        if not output_path:
            return

        metrics = self.export_metrics()
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w") as f:
            json.dump(metrics, f, indent=2)

        logger.info("metrics_exported", path=str(output_path))

    def reset(self) -> None:
        """Reset all metrics."""
        self.fetch_metrics.clear()
        self.extraction_metrics.clear()
        self.chunking_metrics.clear()
        self.summarization_metrics.clear()
        self.cache_metrics.clear()
        self.counters.clear()
        self.timers.clear()
        self.errors.clear()


# Global metrics collector instance
_global_collector: MetricsCollector | None = None


def get_metrics_collector() -> MetricsCollector:
    """Get or create global metrics collector.

    Returns:
        Global MetricsCollector instance
    """
    global _global_collector
    if _global_collector is None:
        _global_collector = MetricsCollector()
    return _global_collector


def configure_logging(level: str = "INFO", structured: bool = True) -> None:
    """Configure structlog logging.

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR)
        structured: Use structured JSON output
    """
    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
    ]

    if structured:
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(structlog.stdlib, level.upper(), structlog.INFO)
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )
