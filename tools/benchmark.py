#!/usr/bin/env python3
"""Small command benchmark helper for tracking performance changes."""

from __future__ import annotations

import argparse
import statistics
import subprocess
import sys
import time
from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class BenchmarkResult:
    runs: int
    minimum: float
    median: float
    p95: float
    maximum: float


def percentile(values: Sequence[float], percent: float) -> float:
    """Return the nearest-rank percentile for a non-empty sequence."""
    if not values:
        raise ValueError("percentile requires at least one value")
    if not 0 < percent <= 100:
        raise ValueError("percent must be in the range (0, 100]")

    ordered = sorted(values)
    rank = max(1, round((percent / 100) * len(ordered)))
    return ordered[rank - 1]


def summarize(durations: Sequence[float]) -> BenchmarkResult:
    """Summarize benchmark durations in seconds."""
    if not durations:
        raise ValueError("at least one duration is required")

    return BenchmarkResult(
        runs=len(durations),
        minimum=min(durations),
        median=statistics.median(durations),
        p95=percentile(durations, 95),
        maximum=max(durations),
    )


def run_command(command: Sequence[str], iterations: int) -> BenchmarkResult:
    """Run a command repeatedly and return timing statistics."""
    if iterations < 1:
        raise ValueError("iterations must be at least 1")

    durations: list[float] = []
    for _ in range(iterations):
        start = time.perf_counter()
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        durations.append(time.perf_counter() - start)
    return summarize(durations)


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Benchmark a command over multiple runs.")
    parser.add_argument("-n", "--iterations", type=int, default=10, help="Number of runs (default: 10).")
    parser.add_argument("command", nargs=argparse.REMAINDER, help="Command and arguments to benchmark.")
    args = parser.parse_args(argv)
    if args.command and args.command[0] == "--":
        args.command = args.command[1:]
    if not args.command:
        parser.error("a command is required")
    return args


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        result = run_command(args.command, args.iterations)
    except (subprocess.CalledProcessError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"runs: {result.runs}")
    print(f"min: {result.minimum:.6f}s")
    print(f"median: {result.median:.6f}s")
    print(f"p95: {result.p95:.6f}s")
    print(f"max: {result.maximum:.6f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
