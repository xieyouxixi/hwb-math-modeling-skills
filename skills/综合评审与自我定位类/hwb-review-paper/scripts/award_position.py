#!/usr/bin/env python3
"""Estimate award band and position for CPGMCM (Huawei Cup graduate contest) or a smaller contest."""

import argparse
import json


# Piecewise-calibrated anchors for the 22nd CPGMCM (2025): score -> percentile outperformed.
# Anchors are derived from the actual 2025 award shares:
#   first prize 244 teams = 1.00% (top 1%), second 3085 = 12.66% (cumulative top 13.66%),
#   third 4830 = 19.82% (cumulative top 33.48%), total winning rate 33.48%.
# Not an official cutoff; a monotonic piecewise-linear interpolation, not a fitted normal CDF.
ANCHORS = [
    (10.0, 0.1),
    (45.0, 50.0),
    (55.0, 66.52),
    (65.0, 86.34),
    (75.0, 99.0),
    (90.0, 99.9),
]


def interpolate_cpgmcm(score: float) -> float:
    if score <= ANCHORS[0][0]:
        return ANCHORS[0][1]
    if score >= ANCHORS[-1][0]:
        return ANCHORS[-1][1]
    for (x0, y0), (x1, y1) in zip(ANCHORS, ANCHORS[1:]):
        if x0 <= score <= x1:
            return y0 + (score - x0) * (y1 - y0) / (x1 - x0)
    raise AssertionError("unreachable")


def cpgmcm_award_band(score: float) -> str:
    if score >= 75:
        return "一等奖竞争区间（2025校准：前1%）"
    if score >= 65:
        return "二等奖竞争区间（2025校准：前1%—13.66%）"
    if score >= 55:
        return "三等奖竞争区间（2025校准：前13.66%—33.48%）"
    if score >= 45:
        return "未获奖但优于中位数区间（2025校准：前33.48%—50%）"
    return "低于研究生赛获奖区间"


def interpolate_small(score: float) -> float:
    """Uniform fallback on the practical 10-90 score interval."""
    return min(99.9, max(0.1, (score - 10.0) / 80.0 * 100.0))


def small_award_band(score: float) -> str:
    if score >= 75:
        return "一等奖竞争区间（小型竞赛经验锚点）"
    if score >= 65:
        return "二等奖竞争区间（小型竞赛经验锚点）"
    if score >= 55:
        return "三等奖竞争区间（小型竞赛经验锚点）"
    return "低于小型竞赛经验获奖区间"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--score", type=float, required=True)
    parser.add_argument("--contest-type", choices=("cpgmcm", "other"), required=True)
    parser.add_argument("--uncertainty", type=float, default=None, help="percentile half-width")
    args = parser.parse_args()
    if args.contest_type == "cpgmcm":
        percentile = interpolate_cpgmcm(args.score)
        uncertainty = 3.0 if args.uncertainty is None else args.uncertainty
        band = cpgmcm_award_band(args.score)
        method = "CPGMCM 2025 winning-rate anchor interpolation (1.00%/12.66%/19.82%)"
    else:
        percentile = interpolate_small(args.score)
        uncertainty = 8.0 if args.uncertainty is None else args.uncertainty
        band = small_award_band(args.score)
        method = "small-contest 10-90 uniform approximation"
    low = max(0.1, percentile - uncertainty)
    high = min(99.9, percentile + uncertainty)
    result = {
        "adjusted_score": round(args.score, 1),
        "percentile_outperformed": round(percentile, 1),
        "percentile_interval": [round(low, 1), round(high, 1)],
        "equivalent_top_percent": round(100 - percentile, 1),
        "contest_type": args.contest_type,
        "award_band": band,
        "method": method,
        "confidence": "medium" if args.contest_type == "cpgmcm" else "low",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
