import pytest

from tools.benchmark import BenchmarkResult, percentile, summarize


def test_percentile_uses_nearest_rank():
    assert percentile([0.3, 0.1, 0.2, 0.4], 50) == 0.2
    assert percentile([0.3, 0.1, 0.2, 0.4], 95) == 0.4


def test_percentile_rejects_empty_input():
    with pytest.raises(ValueError):
        percentile([], 95)


def test_summarize_returns_core_timing_stats():
    assert summarize([0.3, 0.1, 0.2]) == BenchmarkResult(
        runs=3,
        minimum=0.1,
        median=0.2,
        p95=0.3,
        maximum=0.3,
    )
