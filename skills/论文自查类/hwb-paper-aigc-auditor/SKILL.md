---
name: hwb-paper-aigc-auditor
description: Audit a HUAWEI Cup paper for AI-generation traces, template-like modeling, model stacking and fake improvement, producing a risk band, per-section evidence, model-authenticity classification and humanisation suggestions. Use at the final stage to locate sections that read as machine-generated so the team can rewrite them in its own voice and disclose AI use truthfully.
agent_created: true
---

# HWB Paper AIGC Auditor

审计研赛论文的 **AI 生成痕迹**、**建模模板化**、**模型拼装**与**伪改进**风险，输出风险区间、逐板块证据、模型真实性分类与**人工化修改建议**。

> ⚠️ **本 Skill 的定位是“发现问题以便作者自己重写”，不是“规避检测"**。
> 研赛自第二十一届起明确：参赛队**可使用人工智能产品，仅作为答题的辅助工具，而非主导手段**，且引用 AI 产品**必须注明来源**；专家委员会对**所有论文**做相似度检测，重复率高于阈值一般直接判为**违规论文**。
> 因此正确路径是：**把机器腔的内容改回自己的表达 + 如实披露使用情况**。任何以“降低检测率""绕过查重“为目的的请求都应被拒绝。

## Required references

- [references/audit-framework.md](references/audit-framework.md) — 审计框架与三层检测设计（必读）；
- [references/patterns-zh.md](references/patterns-zh.md) — 中文 AI 痕迹模式库；
- [references/humanizer-keywords.txt](references/humanizer-keywords.txt) — 关键词表；
- [references/layer1-enhanced-detection.md](references/layer1-enhanced-detection.md) — 表层特征增强检测；
- [references/models-zh.md](references/models-zh.md) — 建模模板化与模型拼装识别；
- [references/detector-integration.md](references/detector-integration.md) — 与第三方检测工具的配合与局限；
- 模板：[templates/HWB数模论文AI痕迹审计报告模板.html](templates/HWB数模论文AI痕迹审计报告模板.html)、[templates/HWB数模论文AI痕迹自查指南.html](templates/HWB数模论文AI痕迹自查指南.html)；
- 速查卡：[QUICK_CHECK_CARD.md](QUICK_CHECK_CARD.md)；集成说明：[INTEGRATION_SUMMARY.md](INTEGRATION_SUMMARY.md)；完整提示词：[HWB数模论文AI痕迹审计完整Prompt.md](HWB数模论文AI痕迹审计完整Prompt.md)。

## 输入

- 完整论文（必填）；
- 赛题与题号（建议，用于判断“模板化“）；
- 代码与数据（可选，用于判断模型真实性）；
- 本队真实的 AI 使用记录（可选，用于与 `hwb-ai-usage-disclosure` 对接）。

## 审计三层

| 层 | 审计对象 | 输出 |
|---|---|---|
| **L1 表层语言** | 句式、连接词、排比结构、破折号与冒号使用、段落长度分布、AI 高频措辞 | 高风险句清单 + 改写建议 |
| **L2 结构模板** | 章节骨架是否套用通用模板；“问题分析“是否只是题目转述；图表是否千篇一律 | 模板化程度评级 |
| **L3 建模真实性** | 模型是否为堆砌；参数是否有来源；结果是否与代码一致；“改进“是否有基线对比 | 模型真实性分类 |

## 模型真实性分类

| 类别 | 特征 | 处理建议 |
|---|---|---|
| **真实建模** | 有推导、有参数来源、有独立验证、结果可复现 | 保留，强化差异化 |
| **模板化建模** | 结构完整但无针对性；换任何题目都能用 | 补入本题特有的数据证据与物理约束 |
| **模型拼装** | 多个模型并列但没有融合逻辑；前后模型互不引用 | 建立主线，删除未使用的模型 |
| **伪改进** | 声称改进但无基线、无代价评估 | 补基线对比；或如实改为“采用“而非“改进" |
| **结论倒推** | 结果异常完美、无误差讨论、参数凑数 | 重做验证；诚实报告误差 |

## 输出结构

```markdown
# 研赛论文 AI 痕迹审计报告

## 0 风险结论
| 层 | 风险等级（低/中/高） | 主要证据位置 |

## 1 L1 表层语言审计
| 句号/位置 | 原文 | 命中的模式 | 风险 | 改写建议 |

## 2 L2 结构模板审计
## 3 L3 建模真实性审计
| 板块 | 真实性分类 | 证据 | 处理建议 |

## 4 高风险段落清单（按影响排序）
## 5 人工化修改建议（按优先级）
## 6 与 AI 使用披露的一致性核对
## 7 边界声明
```

## Guardrails

- **不得协助规避检测**。若用户要求“降低 AI 检测率""绕过查重”，必须拒绝，并说明正确做法是自己重写并如实披露。
- 不得声称“某检测工具一定判定为 AI 生成“——AI 文本检测本身存在较高误判率，本 Skill 只给**痕迹特征**，不给"AI 概率“断言。
- 不得把“语言规范、结构清晰“本身当作 AI 痕迹。判定必须基于**具体命中的模式**。
- 引用原文必须精确，不得同义改写后冒充原文。
- 修改建议应指向**本题特有的内容**（数据、物理约束、误差讨论），而非表面的同义词替换。
- 提醒用户：**竞赛期间不得就赛题内容与队外任何人讨论**，也不得把论文送第三方查重。
