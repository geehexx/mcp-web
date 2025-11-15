"""Unit tests for metrics module.

Tests MetricsCollector singleton, metric recording, statistics generation,
and all metric types (fetch, extract, chunking, summarization, cache).
"""

import json
import tempfile
import time
from pathlib import Path
from unittest.mock import patch

import pytest

from mcp_web.metrics import (
    CacheMetrics,
    ChunkingMetrics,
    ExtractionMetrics,
    FetchMetrics,
    MetricsCollector,
    SummarizationMetrics,
    configure_logging,
    get_metrics_collector,
)


@pytest.mark.unit
class TestMetricDataclasses:
    """Tests for metric dataclasses."""

    def test_fetch_metrics_creation(self):
        """Test FetchMetrics creation."""
        metrics = FetchMetrics(
            url="https://example.com",
            method="httpx",
            duration_ms=125.5,
            status_code=200,
            content_size=5000,
            success=True,
        )

        assert metrics.url == "https://example.com"
        assert metrics.method == "httpx"
        assert metrics.duration_ms == 125.5
        assert metrics.status_code == 200
        assert metrics.content_size == 5000
        assert metrics.success is True
        assert metrics.error is None

    def test_fetch_metrics_with_error(self):
        """Test FetchMetrics with error."""
        metrics = FetchMetrics(
            url="https://example.com",
            method="httpx",
            duration_ms=50.0,
            status_code=404,
            content_size=0,
            success=False,
            error="Not Found",
        )

        assert metrics.success is False
        assert metrics.error == "Not Found"

    def test_extraction_metrics_creation(self):
        """Test ExtractionMetrics creation."""
        metrics = ExtractionMetrics(
            url="https://example.com",
            content_length=10000,
            extracted_length=5000,
            extraction_ratio=0.5,
            duration_ms=75.3,
            success=True,
        )

        assert metrics.url == "https://example.com"
        assert metrics.content_length == 10000
        assert metrics.extracted_length == 5000
        assert metrics.extraction_ratio == 0.5
        assert metrics.duration_ms == 75.3
        assert metrics.success is True

    def test_chunking_metrics_creation(self):
        """Test ChunkingMetrics creation."""
        metrics = ChunkingMetrics(
            content_length=5000,
            num_chunks=10,
            avg_chunk_size=512.5,
            duration_ms=25.0,
            strategy="hierarchical",
            adaptive_enabled=True,
            target_chunk_size=512,
        )

        assert metrics.content_length == 5000
        assert metrics.num_chunks == 10
        assert metrics.avg_chunk_size == 512.5
        assert metrics.strategy == "hierarchical"
        assert metrics.adaptive_enabled is True
        assert metrics.target_chunk_size == 512

    def test_summarization_metrics_creation(self):
        """Test SummarizationMetrics creation."""
        metrics = SummarizationMetrics(
            input_tokens=1000,
            output_tokens=200,
            model="gpt-4",
            duration_ms=2500.0,
            cost_estimate=0.015,
            success=True,
        )

        assert metrics.input_tokens == 1000
        assert metrics.output_tokens == 200
        assert metrics.model == "gpt-4"
        assert metrics.duration_ms == 2500.0
        assert metrics.cost_estimate == 0.015
        assert metrics.success is True

    def test_cache_metrics_creation(self):
        """Test CacheMetrics creation."""
        metrics = CacheMetrics(
            operation="hit",
            key="test_key",
            size_bytes=1024,
        )

        assert metrics.operation == "hit"
        assert metrics.key == "test_key"
        assert metrics.size_bytes == 1024


@pytest.mark.unit
class TestMetricsCollector:
    """Tests for MetricsCollector."""

    @pytest.fixture
    def collector(self):
        """Create a fresh MetricsCollector instance."""
        collector = MetricsCollector(enabled=True)
        yield collector
        collector.reset()

    def test_collector_initialization(self, collector):
        """Test MetricsCollector initialization."""
        assert collector.enabled is True
        assert len(collector.fetch_metrics) == 0
        assert len(collector.extraction_metrics) == 0
        assert len(collector.counters) == 0

    def test_collector_disabled(self):
        """Test that disabled collector doesn't record metrics."""
        collector = MetricsCollector(enabled=False)

        collector.record_fetch("https://example.com", "httpx", 100, 200, 5000, True)

        assert len(collector.fetch_metrics) == 0
        assert len(collector.counters) == 0

    def test_record_fetch_success(self, collector):
        """Test recording successful fetch metrics."""
        collector.record_fetch(
            url="https://example.com",
            method="httpx",
            duration_ms=125.5,
            status_code=200,
            content_size=5000,
            success=True,
        )

        assert len(collector.fetch_metrics) == 1
        metric = collector.fetch_metrics[0]
        assert metric.url == "https://example.com"
        assert metric.method == "httpx"
        assert metric.duration_ms == 125.5
        assert metric.success is True

        # Check counters
        assert collector.counters["fetch_httpx"] == 1
        assert collector.timers["fetch_httpx_duration"] == [125.5]

    def test_record_fetch_error(self, collector):
        """Test recording failed fetch metrics."""
        collector.record_fetch(
            url="https://example.com",
            method="playwright",
            duration_ms=500.0,
            status_code=500,
            content_size=0,
            success=False,
            error="Server Error",
        )

        assert len(collector.fetch_metrics) == 1
        assert collector.fetch_metrics[0].success is False
        assert collector.fetch_metrics[0].error == "Server Error"
        assert collector.counters["fetch_errors"] == 1

    def test_record_extraction_success(self, collector):
        """Test recording successful extraction metrics."""
        collector.record_extraction(
            url="https://example.com",
            content_length=10000,
            extracted_length=5000,
            duration_ms=75.3,
            success=True,
        )

        assert len(collector.extraction_metrics) == 1
        metric = collector.extraction_metrics[0]
        assert metric.url == "https://example.com"
        assert metric.content_length == 10000
        assert metric.extracted_length == 5000
        assert metric.extraction_ratio == 0.5
        assert metric.success is True

        assert collector.counters["extractions"] == 1
        assert collector.timers["extraction_duration"] == [75.3]

    def test_record_extraction_error(self, collector):
        """Test recording failed extraction metrics."""
        collector.record_extraction(
            url="https://example.com",
            content_length=10000,
            extracted_length=0,
            duration_ms=25.0,
            success=False,
            error="Extraction failed",
        )

        assert collector.extraction_metrics[0].success is False
        assert collector.extraction_metrics[0].error == "Extraction failed"
        assert collector.counters["extraction_errors"] == 1

    def test_record_chunking(self, collector):
        """Test recording chunking metrics."""
        collector.record_chunking(
            content_length=5000,
            num_chunks=10,
            avg_chunk_size=512.5,
            duration_ms=25.0,
            strategy="hierarchical",
            adaptive_enabled=True,
            target_chunk_size=512,
        )

        assert len(collector.chunking_metrics) == 1
        metric = collector.chunking_metrics[0]
        assert metric.num_chunks == 10
        assert metric.strategy == "hierarchical"
        assert metric.adaptive_enabled is True

        assert collector.counters["chunking_operations"] == 1
        assert collector.counters["chunking_strategy_hierarchical"] == 1
        assert collector.counters["chunking_adaptive_enabled"] == 1

    def test_record_chunking_multiple_strategies(self, collector):
        """Test recording chunking with different strategies."""
        collector.record_chunking(
            content_length=5000,
            num_chunks=10,
            avg_chunk_size=512,
            duration_ms=25.0,
            strategy="hierarchical",
            adaptive_enabled=False,
            target_chunk_size=512,
        )

        collector.record_chunking(
            content_length=5000,
            num_chunks=12,
            avg_chunk_size=416,
            duration_ms=20.0,
            strategy="semantic",
            adaptive_enabled=True,
            target_chunk_size=512,
        )

        assert collector.counters["chunking_strategy_hierarchical"] == 1
        assert collector.counters["chunking_strategy_semantic"] == 1
        assert collector.counters["chunking_adaptive_enabled"] == 1

    def test_record_summarization_success(self, collector):
        """Test recording successful summarization metrics."""
        collector.record_summarization(
            input_tokens=1000,
            output_tokens=200,
            model="gpt-4o-mini",
            duration_ms=2500.0,
            success=True,
        )

        assert len(collector.summarization_metrics) == 1
        metric = collector.summarization_metrics[0]
        assert metric.input_tokens == 1000
        assert metric.output_tokens == 200
        assert metric.model == "gpt-4o-mini"
        assert metric.cost_estimate > 0  # Should calculate cost

        assert collector.counters["summarizations"] == 1
        assert collector.counters["total_input_tokens"] == 1000
        assert collector.counters["total_output_tokens"] == 200

    def test_record_summarization_error(self, collector):
        """Test recording failed summarization metrics."""
        collector.record_summarization(
            input_tokens=1000,
            output_tokens=0,
            model="gpt-4",
            duration_ms=100.0,
            success=False,
            error="API timeout",
        )

        assert collector.summarization_metrics[0].success is False
        assert collector.summarization_metrics[0].error == "API timeout"
        assert collector.counters["summarization_errors"] == 1

    def test_record_cache_operations(self, collector):
        """Test recording cache operation metrics."""
        collector.record_cache_operation("hit", "key1", 1024)
        collector.record_cache_operation("miss", "key2")
        collector.record_cache_operation("set", "key3", 2048)
        collector.record_cache_operation("evict", "key4", 512)

        assert len(collector.cache_metrics) == 4
        assert collector.counters["cache_hit"] == 1
        assert collector.counters["cache_miss"] == 1
        assert collector.counters["cache_set"] == 1
        assert collector.counters["cache_evict"] == 1

    def test_record_error(self, collector):
        """Test recording errors."""
        error = ValueError("Test error")
        collector.record_error("test_module", error, {"url": "https://example.com"})

        assert len(collector.errors) == 1
        error_data = collector.errors[0]
        assert error_data["module"] == "test_module"
        assert error_data["error_type"] == "ValueError"
        assert error_data["error_message"] == "Test error"
        assert error_data["context"]["url"] == "https://example.com"
        assert collector.counters["error_test_module"] == 1

    def test_timer_context_manager(self, collector):
        """Test timer context manager."""
        with collector.timer("test_operation"):
            time.sleep(0.01)  # Sleep for 10ms

        assert "test_operation" in collector.timers
        assert len(collector.timers["test_operation"]) == 1
        # Should be >= 10ms
        assert collector.timers["test_operation"][0] >= 10.0

    def test_timer_context_manager_with_exception(self, collector):
        """Test timer records duration even with exception."""
        try:
            with collector.timer("failing_operation"):
                raise ValueError("Test error")
        except ValueError:
            pass

        # Timer should still record
        assert "failing_operation" in collector.timers
        assert len(collector.timers["failing_operation"]) == 1

    def test_export_metrics(self, collector):
        """Test exporting metrics."""
        # Record some metrics
        collector.record_fetch("https://example.com", "httpx", 100, 200, 5000, True)
        collector.record_extraction("https://example.com", 5000, 2500, 50, True)
        collector.record_summarization(1000, 200, "gpt-4", 2000, True)
        collector.record_cache_operation("hit", "key1")
        collector.record_cache_operation("miss", "key2")

        metrics = collector.export_metrics()

        assert "summary" in metrics
        assert "counters" in metrics
        assert "avg_durations_ms" in metrics
        assert "errors" in metrics

        # Check summary
        assert metrics["summary"]["total_fetches"] == 1
        assert metrics["summary"]["total_extractions"] == 1
        assert metrics["summary"]["total_summarizations"] == 1
        assert metrics["summary"]["cache_hit_rate"] == 0.5  # 1 hit, 1 miss
        assert metrics["summary"]["total_cost_usd"] > 0

    def test_export_metrics_empty(self, collector):
        """Test exporting empty metrics."""
        metrics = collector.export_metrics()

        assert metrics["summary"]["total_fetches"] == 0
        assert metrics["summary"]["total_errors"] == 0
        assert metrics["summary"]["cache_hit_rate"] == 0.0

    def test_cache_hit_rate_calculation(self, collector):
        """Test cache hit rate calculation."""
        # 3 hits, 2 misses = 60% hit rate
        for _ in range(3):
            collector.record_cache_operation("hit", "key")
        for _ in range(2):
            collector.record_cache_operation("miss", "key")

        metrics = collector.export_metrics()
        assert metrics["summary"]["cache_hit_rate"] == 0.6

    def test_save_metrics_to_file(self, collector):
        """Test saving metrics to JSON file."""
        collector.record_fetch("https://example.com", "httpx", 100, 200, 5000, True)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "metrics.json"
            collector.save_metrics(output_path)

            assert output_path.exists()

            # Load and verify
            with open(output_path) as f:
                data = json.load(f)

            assert "summary" in data
            assert data["summary"]["total_fetches"] == 1

    def test_save_metrics_creates_directory(self, collector):
        """Test that save_metrics creates parent directories."""
        collector.record_fetch("https://example.com", "httpx", 100, 200, 5000, True)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "subdir" / "metrics.json"
            collector.save_metrics(output_path)

            assert output_path.exists()

    def test_save_metrics_no_path(self, collector):
        """Test save_metrics with no path (should not save)."""
        collector.record_fetch("https://example.com", "httpx", 100, 200, 5000, True)
        # Should not raise error
        collector.save_metrics()

    def test_reset_metrics(self, collector):
        """Test resetting all metrics."""
        # Add various metrics
        collector.record_fetch("https://example.com", "httpx", 100, 200, 5000, True)
        collector.record_extraction("https://example.com", 5000, 2500, 50, True)
        collector.record_cache_operation("hit", "key")
        collector.record_error("test", ValueError("error"))

        assert len(collector.fetch_metrics) > 0
        assert len(collector.counters) > 0
        assert len(collector.errors) > 0

        # Reset
        collector.reset()

        assert len(collector.fetch_metrics) == 0
        assert len(collector.extraction_metrics) == 0
        assert len(collector.chunking_metrics) == 0
        assert len(collector.summarization_metrics) == 0
        assert len(collector.cache_metrics) == 0
        assert len(collector.counters) == 0
        assert len(collector.timers) == 0
        assert len(collector.errors) == 0

    def test_average_duration_calculation(self, collector):
        """Test average duration calculation."""
        collector.record_fetch("url1", "httpx", 100, 200, 5000, True)
        collector.record_fetch("url2", "httpx", 200, 200, 5000, True)
        collector.record_fetch("url3", "httpx", 300, 200, 5000, True)

        metrics = collector.export_metrics()
        avg_duration = metrics["avg_durations_ms"]["fetch_httpx_duration"]

        assert avg_duration == 200.0  # (100 + 200 + 300) / 3

    def test_multiple_fetch_methods(self, collector):
        """Test recording different fetch methods."""
        collector.record_fetch("url1", "httpx", 100, 200, 5000, True)
        collector.record_fetch("url2", "playwright", 500, 200, 5000, True)

        assert collector.counters["fetch_httpx"] == 1
        assert collector.counters["fetch_playwright"] == 1
        assert len(collector.timers["fetch_httpx_duration"]) == 1
        assert len(collector.timers["fetch_playwright_duration"]) == 1

    def test_cost_estimation(self, collector):
        """Test cost estimation for summarization."""
        # Use known token counts to verify cost calculation
        collector.record_summarization(1000, 200, "gpt-4o-mini", 100, True)

        metric = collector.summarization_metrics[0]
        # Cost should be: (1000 * 0.00015 / 1000) + (200 * 0.0006 / 1000)
        expected_cost = (1000 * 0.00015 / 1000) + (200 * 0.0006 / 1000)
        assert abs(metric.cost_estimate - expected_cost) < 0.0001

    def test_total_cost_aggregation(self, collector):
        """Test total cost aggregation across multiple summarizations."""
        collector.record_summarization(1000, 200, "gpt-4", 100, True)
        collector.record_summarization(2000, 400, "gpt-4", 200, True)

        metrics = collector.export_metrics()
        total_cost = metrics["summary"]["total_cost_usd"]

        # Should be sum of both
        assert total_cost > 0
        assert total_cost == sum(m.cost_estimate for m in collector.summarization_metrics)


@pytest.mark.unit
class TestGlobalCollector:
    """Tests for global metrics collector singleton."""

    def test_get_metrics_collector_singleton(self):
        """Test that get_metrics_collector returns singleton."""
        collector1 = get_metrics_collector()
        collector2 = get_metrics_collector()

        assert collector1 is collector2

    def test_get_metrics_collector_creates_instance(self):
        """Test that get_metrics_collector creates instance on first call."""
        # Reset global state
        import mcp_web.metrics

        mcp_web.metrics._global_collector = None

        collector = get_metrics_collector()
        assert collector is not None
        assert isinstance(collector, MetricsCollector)

        # Cleanup
        collector.reset()

    def test_global_collector_shared_state(self):
        """Test that global collector maintains state across calls."""
        collector1 = get_metrics_collector()
        collector1.record_fetch("url", "httpx", 100, 200, 5000, True)

        collector2 = get_metrics_collector()
        assert len(collector2.fetch_metrics) == 1

        # Cleanup
        collector1.reset()


@pytest.mark.unit
class TestConfigureLogging:
    """Tests for logging configuration."""

    def test_configure_logging_info_level(self):
        """Test configuring logging with INFO level."""
        # Should not raise error
        configure_logging(level="INFO", structured=True)

    def test_configure_logging_debug_level(self):
        """Test configuring logging with DEBUG level."""
        configure_logging(level="DEBUG", structured=False)

    def test_configure_logging_structured(self):
        """Test configuring structured JSON logging."""
        configure_logging(level="INFO", structured=True)

    def test_configure_logging_console(self):
        """Test configuring console logging."""
        configure_logging(level="INFO", structured=False)


@pytest.mark.unit
class TestMetricsIntegration:
    """Integration tests for metrics collection."""

    def test_full_pipeline_metrics(self):
        """Test metrics collection for a full pipeline."""
        collector = MetricsCollector(enabled=True)

        # Simulate full pipeline
        collector.record_fetch("https://example.com", "httpx", 125, 200, 10000, True)
        collector.record_extraction("https://example.com", 10000, 5000, 75, True)
        collector.record_chunking(
            content_length=5000,
            num_chunks=10,
            avg_chunk_size=512,
            duration_ms=25,
            strategy="hierarchical",
            adaptive_enabled=True,
            target_chunk_size=512,
        )
        collector.record_summarization(5000, 500, "gpt-4", 3000, True)

        metrics = collector.export_metrics()

        assert metrics["summary"]["total_fetches"] == 1
        assert metrics["summary"]["total_extractions"] == 1
        assert metrics["counters"]["chunking_operations"] == 1
        assert metrics["summary"]["total_summarizations"] == 1

        # Cleanup
        collector.reset()

    def test_error_tracking_across_modules(self):
        """Test error tracking from multiple modules."""
        collector = MetricsCollector(enabled=True)

        collector.record_error("fetcher", ValueError("Fetch error"))
        collector.record_error("extractor", RuntimeError("Extract error"))
        collector.record_error("summarizer", Exception("Summary error"))

        assert len(collector.errors) == 3
        assert collector.counters["error_fetcher"] == 1
        assert collector.counters["error_extractor"] == 1
        assert collector.counters["error_summarizer"] == 1

        # Cleanup
        collector.reset()
