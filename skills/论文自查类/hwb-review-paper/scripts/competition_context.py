#!/usr/bin/env python3
"""Apply transparent CPGMCM problem-type, participating-unit and Huawei-problem adjustments.

研究生赛（华为杯/CPGMCM）不设赛区、不设本科组/高职高专组、也无"省奖/国奖"双层模型。
竞争校准维度改为：
  1) 赛题（A—F）难度与选题拥挤度；
  2) 参赛单位（研究生培养单位）历史获奖记录（组委会规定每单位最多 3 项一等奖）；
  3) 是否选择华为赛题（可选评华为专项奖，与常规奖奖金累加）。

本脚本仅输出"奖项竞争力修正分"，绝不修改论文质量原始判断，不代表官方名额分配或确定获奖结果。
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "references" / "data"


def clamp(value: float, low: float, high: float) -> float:
    return min(high, max(low, value))


def normalize(value: str) -> str:
    value = (value or "").strip().replace("（", "(").replace("）", ")")
    return re.sub(r"\s+", "", value).casefold()


def read_rows(name: str) -> list[dict[str, str]]:
    path = DATA / name
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        lines = [ln for ln in handle if not ln.lstrip().startswith("#")]
    return [row for row in csv.DictReader(lines) if row and any(v.strip() for v in row.values())]


def exact_row(rows: list[dict[str, str]], column: str, value: str) -> dict[str, str] | None:
    key = normalize(value)
    matches = [row for row in rows if normalize(row.get(column, "")) == key]
    return matches[0] if len(matches) == 1 else None


def number(row: dict[str, str] | None, key: str) -> float | None:
    if not row:
        return None
    raw = (row.get(key) or "").strip()
    try:
        return float(raw)
    except ValueError:
        return None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--score", type=float, required=True, help="论文质量最终得分 (raw × 格式质量系数)")
    parser.add_argument("--problem", required=True, choices=("A", "B", "C", "D", "E", "F"),
                        help="赛题编号 A—F")
    parser.add_argument("--unit", default="", help="参赛单位全称（可选，留空则单位修正标记为无法计算）")
    parser.add_argument("--huawei", choices=("yes", "no"), default="no",
                        help="是否选择华为赛题")
    args = parser.parse_args()

    problems = read_rows("problem_difficulty_scores.csv")
    units = read_rows("unit_awards_template.csv")
    problem_row = exact_row(problems, "problem_id", args.problem)
    unit_row = exact_row(units, "unit_name", args.unit) if args.unit else None

    # 1) 赛题难度修正：difficulty_score 在 0—100，越高表示技术门槛越高、同质量论文相对更易突出。
    difficulty = number(problem_row, "difficulty_score")
    problem_adj = 0.0
    if difficulty is not None:
        problem_adj = clamp((difficulty - 50) / 50 * 15.0, -15.0, 15.0)

    # 2) 参赛单位修正：模板为空白，未填则无法计算，修正为 0。
    unit_adj = 0.0
    unit_context = None
    if unit_row is None:
        unit_status = "not_provided" if not args.unit else "not_in_template"
    else:
        fp = number(unit_row, "first_prize_count") or 0.0
        sp = number(unit_row, "second_prize_count") or 0.0
        tp = number(unit_row, "third_prize_count") or 0.0
        # 单位历史越强，单位内竞争越激烈（每单位最多3项一等奖），给一个温和负向先验。
        unit_adj = clamp(-(fp + sp + tp) / 60.0 * 5.0, -5.0, 0.0)
        unit_context = {
            "first_prize_count": fp,
            "second_prize_count": sp,
            "third_prize_count": tp,
            "note": unit_row.get("note", ""),
        }
        unit_status = "matched"

    # 3) 华为赛题修正：选择华为赛题且质量达到一定门槛，开启额外奖项通道（华为专项奖）。
    huawei_adj = 0.0
    huawei_competition_score = None
    if args.huawei == "yes":
        if args.score >= 55:
            huawei_adj = 8.0
        elif args.score >= 45:
            huawei_adj = 4.0
        huawei_competition_score = clamp(args.score + huawei_adj, 0, 90)

    problem_competition_score = clamp(args.score + problem_adj + unit_adj, 0, 90)

    confidence = "中等"
    if unit_status != "matched":
        confidence = "低"

    result = {
        "paper_quality_final_score": round(args.score, 1),
        "problem": args.problem,
        "problem_name": problem_row.get("problem_name", "") if problem_row else "",
        "huawei_problem": args.huawei == "yes",
        "problem_adjustment": {
            "difficulty_score": difficulty,
            "problem_delta": round(problem_adj, 2),
        },
        "unit_match": unit_status,
        "unit_context": unit_context,
        "unit_delta": round(unit_adj, 2),
        "huawei_adjustment": {
            "status": "applied" if args.huawei == "yes" else "not_applicable",
            "delta": round(huawei_adj, 2),
            "huawei_competition_score": round(huawei_competition_score, 1) if huawei_competition_score is not None else None,
        },
        "problem_competition_score": round(problem_competition_score, 1),
        "confidence": confidence,
        "method": "CPGMCM 三维竞争校准启发式（赛题难度 + 参赛单位历史 + 华为赛题）；非官方获奖模型",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
