#!/usr/bin/env python3
"""华为杯（CPGMCM）获奖区间估算：按参赛总队数与本人/本队名次定位奖项临界。

用法示例：
    python scripts/query_award.py --teams 24371 --rank 500
    python scripts/query_award.py --teams 24371 --rank 5000
    python scripts/query_award.py --score 78                 # 不给总队数时用 2025 实际规模
    python scripts/query_award.py                            # 无参 → 示例输出

口径说明（务必向用户转述）：
    * 比例锚点取 2025 年（第二十二届）实际获奖比例：一等 1.00%、二等 12.66%、三等 19.82%，
      即累计前 1.00% / 13.66% / 33.48%。章程上限为 1.5% / 13% / 20%。
    * 各届实际规模与比例随当届参赛情况变化，本脚本输出为**经验估计**，不是官方分数线，
      也不构成任何获奖承诺。当届官方结果为准。
    * 全部逻辑仅用标准库，Python 3.13 兼容；数据文件按脚本位置相对解析。
"""

import argparse
import csv
import json
from pathlib import Path

# 2025（第二十二届）实际比例锚点：奖项 -> 占参赛队伍总数的比例
RATIO_2025 = {"一等奖": 0.0100, "二等奖": 0.1266, "三等奖": 0.1982}
# 章程规定的比例上限
RATIO_CAP = {"一等奖": 0.015, "二等奖": 0.13, "三等奖": 0.20}
# 2025 年实际规模，用于未指定 --teams 时的兜底
TEAMS_2025 = 24371

# 与 award_position.py 一致的分数→超越百分位分段锚点（2025 校准）
ANCHORS = [
    (10.0, 0.1),
    (45.0, 50.0),
    (55.0, 66.52),
    (65.0, 86.34),
    (75.0, 99.0),
    (90.0, 99.9),
]


def score_to_top_percent(score: float) -> float:
    """论文评分 → 预估所处“前百分之几”（分段线性，非官方）。"""
    if score <= ANCHORS[0][0]:
        pct = ANCHORS[0][1]
    elif score >= ANCHORS[-1][0]:
        pct = ANCHORS[-1][1]
    else:
        pct = None
        for (x0, y0), (x1, y1) in zip(ANCHORS, ANCHORS[1:]):
            if x0 <= score <= x1:
                pct = y0 + (score - x0) * (y1 - y0) / (x1 - x0)
                break
        if pct is None:
            pct = ANCHORS[-1][1]
    return round(max(0.01, 100.0 - pct), 2)


def cutoffs(teams: int) -> dict:
    """按比例锚点与上限，给出各奖项的临界名次（向上取整）。"""
    out = {}
    for level, ratio in RATIO_2025.items():
        out[level] = {
            "2025实际比例": "{:.2%}".format(ratio),
            "临界名次": max(1, int(teams * ratio)),
            "章程上限比例": "{:.2%}".format(RATIO_CAP[level]),
            "上限临界名次": max(1, int(teams * RATIO_CAP[level])),
        }
    return out


def band_of(rank: int, teams: int) -> str:
    if rank < 1 or rank > teams:
        return "名次超出参赛队伍范围，请核对输入"
    pct = rank / teams
    if pct <= RATIO_2025["一等奖"]:
        return "一等奖竞争区间（2025 校准：前 1.00%）"
    if pct <= RATIO_2025["一等奖"] + RATIO_2025["二等奖"]:
        return "二等奖竞争区间（2025 校准：前 1.00%—13.66%）"
    if pct <= RATIO_2025["一等奖"] + RATIO_2025["二等奖"] + RATIO_2025["三等奖"]:
        return "三等奖竞争区间（2025 校准：前 13.66%—33.48%）"
    if pct <= 0.50:
        return "未获奖但优于中位数区间（前 33.48%—50%）"
    return "低于研究生赛获奖比例区间（后 50%）"


def huawei_award_note(rank: int) -> str:
    return (
        "若本队选做华为赛题，可在常规奖项之外**另行参评华为专项奖**"
        "（一等奖 4 队、二等奖 12 队，奖金与常规奖项累加）。"
        "华为专项奖名额极少，按“华为赛题参赛队内部排名”评定，"
        "因此同一名次在华为赛题内部的相对位置比全国名次更关键。"
    )


def load_units(path: Path) -> list:
    """读取优秀论文培养单位代码分布（参考统计，非获奖统计）。"""
    if not path.is_file():
        return []
    rows = []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        for line in handle:
            if line.lstrip().startswith("#") or not line.strip():
                continue
            rows.append(line)
    data = list(csv.reader(rows))
    if not data:
        return []
    header, body = data[0], data[1:]
    return [dict(zip(header, r)) for r in body if len(r) >= 2 and r[0].strip()]


def main() -> None:
    parser = argparse.ArgumentParser(description="华为杯获奖区间估算（按参赛总队数与名次）")
    parser.add_argument("--teams", type=int, default=None, help="当届参赛队伍总数；缺省用 2025 实际规模 24371")
    parser.add_argument("--rank", type=int, default=None, help="本队名次（1 为最高）")
    parser.add_argument("--score", type=float, default=None, help="或给出论文质量分（0—100），用于折算所处百分位")
    args = parser.parse_args()

    teams = args.teams or TEAMS_2025
    if teams < 100:
        raise SystemExit("--teams 明显偏小（<100），请确认是否为参赛队伍总数")

    result = {
        "口径": "比例锚点取自 2025 年（第二十二届）实际获奖比例：一等 1.00%、二等 12.66%、三等 19.82%；章程上限 1.5%/13%/20%。",
        "参赛队伍总数": teams,
        "各奖项临界名次": cutoffs(teams),
    }

    if args.rank is not None:
        result["本队名次"] = args.rank
        result["所处区间"] = band_of(args.rank, teams)
        result["名次百分位"] = "{:.4%}".format(args.rank / teams)
        if args.rank <= teams * RATIO_2025["一等奖"] * 3:
            result["华为专项奖提示"] = huawei_award_note(args.rank)
    elif args.score is not None:
        top_pct = score_to_top_percent(args.score)
        implied_rank = max(1, int(teams * top_pct / 100.0))
        result["论文质量分"] = args.score
        result["折算所处前百分位"] = "{:.2f}%".format(top_pct)
        result["折算约当名次"] = implied_rank
        result["所处区间"] = band_of(implied_rank, teams)
        result["说明"] = "分数→百分位为分段线性折算（2025 校准），不是官方分数线。"
    else:
        # 无 --rank / --score 时给出示例输出，便于直接运行验证
        demo = max(1, int(teams * RATIO_2025["二等奖"]))
        result["示例"] = {
            "说明": "未提供 --rank 或 --score，以下为示例（名次 {} / 总队数 {}）".format(demo, teams),
            "本队名次": demo,
            "所处区间": band_of(demo, teams),
            "名次百分位": "{:.4%}".format(demo / teams),
        }

    units = load_units(Path(__file__).resolve().parents[1] / "assets" / "优秀论文培养单位代码分布.csv")
    if units:
        top = units[:10]
        result["参考统计_优秀论文篇次前十培养单位代码"] = [
            {"培养单位代码": u.get("培养单位代码", ""), "优秀论文篇次": u.get("优秀论文篇次", "")} for u in top
        ]
        result["参考统计说明"] = (
            "该表由本地归档全部优秀论文的队伍编号解析而来，**只反映优秀论文样本分布，不等于获奖统计**；"
            "缺失培养单位不在其中，不代表其无获奖或不能获奖。"
        )

    result["免责声明"] = (
        "本输出为基于公开比例与个人名次/得分的经验估计，不是官方获奖概率，不构成任何获奖承诺。"
        "当届实际规模、比例与评奖结果以官方公布为准。"
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
