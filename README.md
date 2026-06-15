# First Public Repo

This repository now includes a lightweight performance benchmarking helper that can be used to measure command runtime before and after future optimizations.

## Benchmark commands

Run any command multiple times and report key timing statistics:

```bash
python tools/benchmark.py --iterations 10 -- python -c "print('hello')"
```

The helper reports minimum, median, p95, and maximum durations so changes can be evaluated with repeatable measurements instead of single-run timings.
