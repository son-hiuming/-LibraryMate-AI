"""Measure cold vs warm RAG retrieval without calling Gemini.

Run from repository root after building the index:
    python -m scripts.benchmark_rag

The first run may load an embedding model and initialize Chroma. Later
runs reuse both within the process. Numbers are local observations, not
guaranteed speedups or a benchmark across machines.
"""
from __future__ import annotations

import argparse
from statistics import mean
from time import perf_counter

from src.rag.engine import retrieve, _db, _encoder


def main():
    parser = argparse.ArgumentParser(description="Time local RAG retrieval")
    parser.add_argument("--runs", type=int, default=4, help="number of queries (1..20)")
    args = parser.parse_args()
    if not 1 <= args.runs <= 20:
        parser.error("--runs must be between 1 and 20")

    query = "Tôi có thể giữ sách thêm một tuần nữa không?"
    times = []
    for i in range(args.runs):
        start = perf_counter()
        result = retrieve(query, k=3)
        elapsed = round((perf_counter() - start) * 1000, 1)
        times.append(elapsed)
        sections = [p["section"] for p in result["passages"]]
        print(f"Run {i + 1}: {elapsed:.1f} ms | sections={sections}")

    print(f"First query: {times[0]:.1f} ms")
    if len(times) > 1:
        print(f"Warm mean: {mean(times[1:]):.1f} ms")
    print(f"Chroma client cache: {_db.cache_info()}")
    print("Embedding model cache entries:", _encoder.cache_info().currsize)
    if not any(p["section"] == "P03" for p in result["passages"]):
        raise SystemExit("WARNING: P03 was not retrieved; inspect RAG quality.")


if __name__ == "__main__":
    main()
