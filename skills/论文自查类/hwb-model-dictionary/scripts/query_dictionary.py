# -*- coding: utf-8 -*-
"""华为杯（CPGMCM）模型字典查询工具。

数据源：`assets/model-dictionary.json`（由 `scripts/build_dictionary.py` 生成，
根节点为 数据集名称 / 制作方 / 使用许可 / 版权与传播声明 / 数据(list)）。

用法示例：
  python query_dictionary.py --stats
  python query_dictionary.py --list-categories
  python query_dictionary.py --problem A
  python query_dictionary.py --major 优化模型
  python query_dictionary.py --group 启发式
  python query_dictionary.py --query 卡尔曼
  python query_dictionary.py --seq 20 -v
  python query_dictionary.py --problem E --major 机器学习模型

纯标准库，Python 3.13 兼容；路径按脚本位置相对解析，不写死绝对路径。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
DICT_PATH = os.path.join(HERE, os.pardir, "assets", "model-dictionary.json")

# 从「适用场景」等自由文本中抽取题号信号，如 “华为杯A/D题”“常见于 E 题”
PROB_RE = re.compile(r"([A-F](?:\s*/\s*[A-F])*)\s*题")

FIELDS_SHORT = ["序号", "模型名称", "模型大类", "具体分组", "模型类别"]
FIELDS_FULL = ["序号", "模型名称", "模型大类", "具体分组", "模型类别", "适用场景",
               "数据要求", "原理讲解", "模型输入", "模型输出", "关键假设",
               "禁忌点", "模型缺陷", "检验方法", "资料使用声明"]


def load() -> dict:
    if not os.path.exists(DICT_PATH):
        sys.exit("找不到词典文件：%s" % os.path.abspath(DICT_PATH))
    with open(DICT_PATH, encoding="utf-8") as handle:
        root = json.load(handle)
    if not isinstance(root, dict) or not isinstance(root.get("数据"), list):
        sys.exit("词典结构异常：根节点缺少「数据」数组。请先运行 scripts/build_dictionary.py。")
    return root


def problem_tags(rec: dict) -> set:
    """返回该模型对应的题号集合。

    优先读取生成器写入的 `适用题号` 字段（检索用经验提示，非官方题型定义）；
    若缺失，则从「适用场景」文本中解析显式题号（如 “华为杯A/D题”“E题常见”）。
    两者都没有信号时返回空集，由调用方视为「通用」。
    """
    hint = rec.get("适用题号")
    if isinstance(hint, list):
        tags = {str(t).strip().upper() for t in hint if str(t).strip()}
        tags.discard("通用")
        return tags
    blob = " ".join(str(rec.get(k, "")) for k in ("适用场景", "模型名称", "模型类别"))
    tags = set()
    for match in PROB_RE.finditer(blob):
        for ch in re.findall(r"[A-F]", match.group(1)):
            tags.add(ch)
    return tags


def show(rec: dict, verbose: bool = False) -> None:
    print("=" * 74)
    print("[%s] %s  |  %s / %s" % (rec.get("序号", "?"), rec.get("模型名称", ""),
                                   rec.get("模型大类", ""), rec.get("具体分组", "")))
    print("  模型类别 : %s" % rec.get("模型类别", ""))
    print("  适用场景 : %s" % rec.get("适用场景", ""))
    print("  数据要求 : %s" % rec.get("数据要求", ""))
    if verbose:
        for key in ("原理讲解", "模型输入", "模型输出", "关键假设",
                    "禁忌点", "模型缺陷", "检验方法", "资料使用声明"):
            print("  %-8s : %s" % (key, rec.get(key, "")))
    else:
        print("  禁忌点   : %s" % rec.get("禁忌点", ""))
        print("  检验方法 : %s" % rec.get("检验方法", ""))
        print("  （加 -v 查看原理讲解、输入输出、关键假设、缺陷与声明）")


def main() -> None:
    parser = argparse.ArgumentParser(description="华为杯（CPGMCM）模型字典查询工具")
    parser.add_argument("--problem", help="题号：A/B/C/D/E/F/通用")
    parser.add_argument("--major", help="模型大类，如 优化模型/预测模型/评价模型")
    parser.add_argument("--group", help="具体分组，如 启发式/连续优化/客观赋权")
    parser.add_argument("--category", help="模型类别模糊匹配，如 LP/TOPSIS/卡尔曼")
    parser.add_argument("--query", help="关键词模糊匹配（名称、类别、适用场景、原理、输入输出）")
    parser.add_argument("--seq", type=int, dest="seq", help="按序号精确查询")
    parser.add_argument("--verbose", "-v", action="store_true", help="输出完整档案")
    parser.add_argument("--list-categories", action="store_true", help="列出全部模型大类与具体分组")
    parser.add_argument("--stats", action="store_true", help="输出词典统计")
    args = parser.parse_args()

    root = load()
    records = root["数据"]

    if args.list_categories:
        print("模型大类：")
        for name, count in Counter(r.get("模型大类", "?") for r in records).most_common():
            print("  - %-16s %d" % (name, count))
        print("\n具体分组（前 30）：")
        for name, count in Counter(r.get("具体分组", "?") for r in records).most_common(30):
            print("  - %-16s %d" % (name, count))
        print("\n题号信号分布（由「适用场景」解析，非官方题型定义）：")
        tag_counter = Counter()
        for rec in records:
            for tag in problem_tags(rec):
                tag_counter[tag] += 1
        generic = sum(1 for rec in records if not problem_tags(rec))
        for tag in "ABCDEF":
            print("  - %s 题  %d" % (tag, tag_counter.get(tag, 0)))
        print("  - 通用/未标注题号  %d" % generic)
        return

    if args.stats:
        print("数据集名称：%s" % root.get("数据集名称", ""))
        print("制作方    ：%s" % root.get("制作方", ""))
        print("使用许可  ：%s" % root.get("使用许可", ""))
        print("模型条目数：%d" % len(records))
        print("\n按模型大类：")
        for name, count in Counter(r.get("模型大类", "?") for r in records).most_common():
            print("  %-18s %d" % (name, count))
        print("\n按题号信号（非官方题型定义）：")
        tag_counter = Counter()
        for rec in records:
            for tag in problem_tags(rec):
                tag_counter[tag] += 1
        for tag in "ABCDEF":
            print("  %-4s题  %d" % (tag, tag_counter.get(tag, 0)))
        print("  %-4s   %d" % ("通用", sum(1 for rec in records if not problem_tags(rec))))
        print("\n%s" % root.get("版权与传播声明", ""))
        return

    result = records
    if args.seq is not None:
        result = [r for r in result if r.get("序号") == args.seq]
    if args.problem:
        want = args.problem.strip().upper()
        if want in ("通用", "OTHER", "GENERAL"):
            result = [r for r in result if not problem_tags(r)]
        else:
            result = [r for r in result if want in problem_tags(r)]
    if args.major:
        result = [r for r in result if args.major in str(r.get("模型大类", ""))]
    if args.group:
        result = [r for r in result if args.group in str(r.get("具体分组", ""))]
    if args.category:
        result = [r for r in result if args.category.lower() in str(r.get("模型类别", "")).lower()]
    if args.query:
        key = args.query.lower()
        searchable = ("模型名称", "模型类别", "具体分组", "适用场景",
                      "原理讲解", "模型输入", "模型输出")
        result = [r for r in result
                  if key in " ".join(str(r.get(k, "")) for k in searchable).lower()]

    if not result:
        print("未匹配到模型。可用 --list-categories 查看分类，或去掉部分筛选条件。")
        print("提示：题号筛选基于「适用场景」中的题号信号，未标注题号的条目请用 --problem 通用 查询。")
        return

    print("匹配 %d 条：\n" % len(result))
    for rec in result:
        show(rec, verbose=args.verbose)


if __name__ == "__main__":
    main()
