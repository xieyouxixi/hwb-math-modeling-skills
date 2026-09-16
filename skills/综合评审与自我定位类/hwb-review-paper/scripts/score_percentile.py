#!/usr/bin/env python3
"""Compute a transparent midrank percentile from a reference score distribution.

If a real same-contest distribution CSV is supplied, use the empirical midrank method.
Otherwise fall back to the CPGMCM 2025 winning-rate anchor interpolation so the script stays
runnable with only `--score`.
"""

import argparse
import csv
import json
from pathlib import Path


# Same anchors as award_position.py, used only as the no-distribution fallback.
ANCHORS = [
    (10.0, 0.1),
    (45.0, 50.0),
    (55.0, 66.52),
    (65.0, 86.34),
    (75.0, 99.0),
    (90.0, 99.9),
]


def anchor_percentile(score: float) -> float:
    if score <= ANCHORS[0][0]:
        return ANCHORS[0][1]
    if score >= ANCHORS[-1][0]:
        return ANCHORS[-1][1]
    for (x0, y0), (x1, y1) in zip(ANCHORS, ANCHORS[1:]):
        if x0 <= score <= x1:
            return y0 + (score - x0) * (y1 - y0) / (x1 - x0)
    raise AssertionError("unreachable")


def load_scores(path: Path, column: str | None) -> list[float]:
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        if isinstance(data, dict):
            data = data[column or "scores"]
        return [float(x[column]) if isinstance(x, dict) else float(x) for x in data]
    with path.open(encoding="utf-8-sig", newline="") as handle:
        lines = [ln for ln in handle if not ln.lstrip().startswith("#")]
    rows = [row for row in csv.DictReader(lines) if row and any(v.strip() for v in row.values())]
    if not rows:
        return []
    selected = column or ("score" if "score" in rows[0] else next(iter(rows[0])))
    return [float(row[selected]) for row in rows if row.get(selected, "").strip()]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--score", type=float, required=True)
    parser.add_argument("--distribution", type=Path, default=None, help="CSV or JSON scores (optional)")
    parser.add_argument("--column", help="CSV column or JSON object key")
    args = parser.parse_args()

    if args.distribution is not None:
        scores = load_scores(args.distribution, args.column)
        if not scores:
            raise SystemExit("Distribution contains no usable scores")
        below = sum(value < args.score for value in scores)
        equal = sum(value == args.score for value in scores)
        percentile = 100 * (below + 0.5 * equal) / len(scores)
        method = "midrank empirical percentile"
    else:
        percentile = anchor_percentile(args.score)
        method = "CPGMCM 2025 winning-rate anchor interpolation (fallback, no distribution supplied)"

    result = {
        "score": args.score,
        "percentile_outperformed": round(percentile, 2),
        "equivalent_top_percent": round(100 - percentile, 2),
        "method": method,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
