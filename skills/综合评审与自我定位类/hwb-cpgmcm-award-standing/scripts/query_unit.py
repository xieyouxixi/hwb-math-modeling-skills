#!/usr/bin/env python3
"""华为杯（CPGMCM）研究生培养单位获奖查询与备赛定位。

读取 assets/unit_awards_template.csv（空白模板，须由使用者从官方获奖名单自行填写）。
- 模板为空时，优雅提示“数据未填写”，仅给方法性建议，不虚构单位历史。
- 支持按培养单位名称模糊查询，输出奖项画像与基于 1%/12.66%/19.82% 锚点的备赛定位建议。
- 纯标准库，Python 3.13 兼容；路径按脚本位置相对解析，不写死绝对路径。
"""
import argparse
import csv
import json
import re
from difflib import SequenceMatcher
from pathlib import Path

# 2025（第二十二届）实际比例基线（锚点）。其余年份不确定字段应留 NA，不编造。
ANCHORS = {"一等": 0.0100, "二等": 0.1266, "三等": 0.1982}
YEAR_LEVEL_RE = re.compile(r"^(\d{4})_(一等奖|二等奖|三等奖)$")


def norm(v):
    return re.sub(r"\s+", "", str(v or "").strip().lower().replace("（", "(").replace("）", ")"))


def sim(a, b):
    a, b = norm(a), norm(b)
    if a == b:
        return 1.0
    if a and (a in b or b in a):
        return 0.9
    return SequenceMatcher(None, a, b).ratio()


def is_blank(v):
    return v is None or str(v).strip() == "" or str(v).strip().upper() == "NA"


def load_rows(path):
    """跳过以 # 开头的注释行与空行，返回 (表头, 数据行)。"""
    kept = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        for line in f:
            if line.lstrip().startswith("#") or not line.strip():
                continue
            kept.append(line)
    if not kept:
        return [], []
    reader = list(csv.reader(kept))
    header = reader[0]
    data = [r for r in reader[1:] if r and any(c.strip() for c in r)]
    return header, data


def year_level_cols(header):
    """返回 [(列索引, 年份, 等级)]。"""
    out = []
    for i, name in enumerate(header):
        m = YEAR_LEVEL_RE.match(name.strip())
        if m:
            out.append((i, m.group(1), m.group(2)))
    return out


def to_int(v):
    try:
        return int(str(v).strip())
    except (ValueError, TypeError):
        return 0


def probability_interval(first_total, has_history):
    """基于历史一等奖累计数与全国基线，给出经验估计区间（明确标注非官方）。"""
    if not has_history:
        return "约 0%–1.00%（接近全国基线，不确定性高）"
    if first_total == 0:
        return "约 0%–1.00%（接近全国基线，不确定性高）"
    if first_total <= 3:
        return "约 1.00%–3%（高于基线，经验估计）"
    if first_total <= 10:
        return "约 3%–6%（高于基线，经验估计）"
    return "约 6%–12%（明显高于基线，经验估计）"


def build_profile(header, row, cols):
    name = row[0].strip()
    year_records = {}
    totals = {"一等奖": 0, "二等奖": 0, "三等奖": 0}
    for idx, year, level in cols:
        val = row[idx] if idx < len(row) else ""
        if is_blank(val):
            year_records[year] = year_records.get(year, {})
            year_records[year][level] = "NA"
        else:
            n = to_int(val)
            year_records.setdefault(year, {})[level] = n
            totals[level] += n
    huawei_idx = None
    for i, h in enumerate(header):
        if h.strip().startswith("华为专项奖"):
            huawei_idx = i
            break
    huawei = "NA"
    if huawei_idx is not None and huawei_idx < len(row) and not is_blank(row[huawei_idx]):
        huawei = to_int(row[huawei_idx])

    has_history = any(
        v not in ("NA", 0) for yr in year_records.values() for v in yr.values()
    )
    first_total = totals["一等奖"]

    profile = {
        "status": "ok",
        "培养单位名称": name,
        "年度记录": {yr: year_records[yr] for yr in sorted(year_records)},
        "合计": totals,
        "华为专项奖命中次数": huawei,
        "经验预测": {
            "下一届一等奖概率区间": probability_interval(first_total, has_history),
            "下一届二等奖概率区间": "约 12.66% 基线附近，历史强队可上探至 15%–20%（经验估计）",
            "下一届三等奖概率区间": "约 19.82% 基线附近，历史强队可上探至 22%–28%（经验估计）",
            "说明": "以上为基于全国基线（一等≈1.00%、二等≈12.66%、三等≈19.82%）与单位历史的经验估计，非官方概率，不构成获奖承诺。",
        },
        "选题建议": (
            "若队伍建模基础扎实且熟悉工程数据，可优先考虑华为赛题（历届多为 B 题）以参评华为专项奖；"
            "否则按团队专长匹配 A—F 六题。选题前核对当届官方赛题说明与数据口径。"
        ),
        "备赛建议": (
            "以全国基线为参照设定备赛目标：先确保论文符合格式与匿名硬约束（封皮、无目录、统一摘要页、命名合规），"
            "再针对一等奖所需完整性做全真模拟。历史强队应着重稳健性与创新点；无历史记录的单位不应被预先判定为不能获奖，"
            "差距主要来自团队与论文质量而非单位标签。"
        ),
    }
    return profile


def not_found_message(unit):
    return {
        "status": "not_found",
        "查询单位": unit,
        "消息": (
            "按当前已填写的榜单口径，未找到该培养单位的获奖记录。这不代表该单位本年度不能获奖，"
            "也可能仅是模板尚未填写该单位。请以官方获奖名单为准，必要时在 unit_awards_template.csv 中补充该单位记录。"
        ),
        "方法性建议": (
            "以全国基线（一等≈1.00%、二等≈12.66%、三等≈19.82%）作为先验，结合个人竞赛经历与模拟经历评估备赛差距；"
            "数据仅作先验并带有不确定性，不得仅因单位无历史获奖而断定学生不能获奖。"
        ),
    }


def main():
    p = argparse.ArgumentParser(description="华为杯研究生培养单位获奖查询与备赛定位")
    p.add_argument("--unit", required=True, help="研究生培养单位名称（支持模糊匹配）")
    p.add_argument("--file", default=None, help="可选：指定 CSV 路径，默认读取脚本同目录 assets/unit_awards_template.csv")
    a = p.parse_args()

    base = Path(__file__).resolve().parents[1] / "assets" / "unit_awards_template.csv"
    fpath = Path(a.file) if a.file else base

    try:
        header, data = load_rows(fpath)
    except FileNotFoundError:
        o = {
            "status": "data_not_filled",
            "消息": "数据未填写：未找到 unit_awards_template.csv。请确认模板文件存在，并按注释从官方获奖名单自行填写培养单位记录；本工具不虚构任何单位历史。",
            "建议": "仅提供方法性建议：以全国基线（一等≈1.00%、二等≈12.66%、三等≈19.82%）作为先验评估备赛差距，详见 SKILL.md。",
        }
        print(json.dumps(o, ensure_ascii=False, indent=2))
        return

    if not header or not data:
        o = {
            "status": "data_not_filled",
            "消息": (
                "数据未填写：unit_awards_template.csv 当前为空白模板（仅有表头与填写说明）。"
                "请按模板注释，从官方公布的获奖名单公告（https://cpipc.acge.org.cn/）或各培养单位公开获奖通报中，"
                "自行逐行填入培养单位记录。本工具不提供、也不伪造任何未经核实的单位获奖数据。"
            ),
            "建议": (
                "在模板填写前，只能给出方法性建议：以全国基线（一等≈1.00%、二等≈12.66%、三等≈19.82%）作为先验，"
                "结合个人竞赛经历与模拟经历评估备赛差距。不得虚构单位历史记录。"
            ),
        }
        print(json.dumps(o, ensure_ascii=False, indent=2))
        return

    cols = year_level_cols(header)
    scored = sorted(((sim(a.unit, r[0]), r) for r in data), key=lambda x: x[0], reverse=True)
    good = [m for m in scored if m[0] >= 0.72]

    if good and (len(good) == 1 or good[0][0] - good[1][0] >= 0.08):
        o = build_profile(header, good[0][1], cols)
    elif good:
        o = {
            "status": "ambiguous",
            "candidates": [r[1][0].strip() for r in good[:8]],
            "消息": "匹配到多个相近的培养单位，请确认具体名称后重试。",
        }
    else:
        o = not_found_message(a.unit)

    print(json.dumps(o, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
