---
name: hwb-problem-translator
description: Translate a complete HUAWEI Cup (China Post-Graduate Mathematical Contest in Modeling) problem into a sentence-level interpretation report, identifying definitions, constraints, data semantics, deliverable requirements and cross-question dependencies. Use when a graduate team has just received the A~F problem and needs an exhaustive reading before modeling.
agent_created: true
---

# HWB Problem Translator

把完整研赛赛题（含全部补充说明与附件说明）翻译成一份**可被后续建模与写作直接引用的题意说明**。研赛题干普遍包含工程背景长段落与分散的口径约定，逐句翻译是防止"做错题"的第一道闸。

## Required references

- 完整阅读 [references/cpgmcm-abcdef-translation-signals.md](references/cpgmcm-abcdef-translation-signals.md)——A~F 六类题型的翻译信号与高风险表述；
- 完整阅读 [references/sentence-interpretation-rules.md](references/sentence-interpretation-rules.md)；
- 输出格式遵循 [references/md-output-standard.md](references/md-output-standard.md)；
- 需要理解"命题人想让评委看到什么"时，参考 [references/historical-review-signals.md](references/historical-review-signals.md)。

## 输入

- **主赛题全文**（必填）；
- **补充说明 / 更正说明 / 附录 / 附件说明**（研赛必看，口径常在此处变更）；
- 可选：已有题意笔记。

缺任一项时，先列出"缺失材料"再开始，不要靠推测补齐。

## 工作步骤

1. **切句编号**：把赛题切成可索引的句子单元（`S01`、`S02`……），保留原句以便回溯。
2. **抽取六类要素**：
   - **定义**：题目自定义的术语、缩写、指标；
   - **约束**：硬约束（不能违反）与软约束（偏好）分开；
   - **数据口径**：单位、量纲、时间范围、采样频率、缺失与异常处理约定；
   - **交付要求**：要交什么（数值、表格、方案、图像）、格式、精度；
   - **跨问题关系**：哪几问共享数据/模型/结果，哪一问是前面结果的延伸；
   - **背景与边界**：工程场景中隐含但未明说的物理/业务限制。
3. **标注不确定处**：凡题目表述有歧义、或附件缺失导致无法判定的，写入"待澄清清单"，并给出"若按 A 理解 / 若按 B 理解"的分支影响。
4. **产出跨问题依赖图**：用 Mermaid 表示问题之间的数据流与结果依赖。
5. **输出遗漏审计**：逐项检查是否有句子未被任何要素吸收。

## 输出结构

```markdown
# 赛题翻译报告 · <年份> <题号> <题目全称>

## 0 赛题档案
| 项目 | 内容 |
|---|---|
| 届次/年份 | |
| 题号 | |
| 题目全称 | |
| 命题方 | （华为题 / 中兴题 / 未标注） |
| 题型族 | |
| 赛程 | 四天 |

## 1 逐句解释
| 句号 | 原文 | 白话解释 | 要素类型 | 风险提示 |

## 2 定义表
## 3 约束表（硬/软分离）
## 4 数据口径表
## 5 交付要求表
## 6 跨问题依赖图
```mermaid
flowchart LR
```
## 7 待澄清清单
| 编号 | 歧义点 | 理解A | 理解B | 分支影响 | 建议 |

## 8 遗漏审计
## 9 一句话题意
```

## 硬约束

- 题目名称、年份、题号、命题方必须与本地赛题原件一致；**不得改写题目名称**。
- **不得虚构**题目中不存在的数据、附件或要求。
- 若为**华为赛题**，要在赛题档案中显式标注——选择华为赛题的队伍可额外参评**华为专项奖**（在华为赛题中排名前 16 名者，一等奖 4 队、二等奖 12 队），这会影响后续策略建议。
- 竞赛期间若用户正在参赛：**提醒其不得就赛题内容与队外任何人讨论**（包括网上），本 Skill 的输出仅作为个人读题笔记使用。
- 输出必须是 Markdown，便于被 `hwb-modeling-ideas`、`hwb-problem-restatement` 等下游 Skill 直接引用。
