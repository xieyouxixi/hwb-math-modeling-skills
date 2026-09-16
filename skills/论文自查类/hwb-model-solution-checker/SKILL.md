---
name: hwb-model-solution-checker
description: Diagnose the model-establishment, solution, results, validation and sensitivity-analysis parts of a HUAWEI Cup paper, including reproducibility and red-line risks. Use when the core chapters are drafted and need a strict review before the final submission gate.
agent_created: true
---

# HWB Model Solution Checker

检查论文**核心正文**：模型建立、模型求解、结果与回答、检验与灵敏度分析、可复现性。这是全篇权重最高的部分，研赛评委在集中评审阶段的主要时间都花在这里。

## Required references

- [references/model-establishment-and-solution.md](references/model-establishment-and-solution.md) — 模型建立与求解的检查规则；
- [references/validation-and-sensitivity.md](references/validation-and-sensitivity.md) — 检验与灵敏度分析检查规则（**研赛重点**）；
- [references/cpgmcm-abcdef-solution-redflags.md](references/cpgmcm-abcdef-solution-redflags.md) — A~F 六题型逐题红线问题（按 2020—2025 真题归纳）。

## 输入

- 完整赛题（必填）；
- 论文核心章节全文（必填）；
- 附件数据说明（可选，用于核对数据使用是否与实际一致）；
- 代码与运行日志（可选，用于可复现性核对）。

## 检查维度

| 维度 | 检查点 |
|---|---|
| **模型建立** | 推导链是否完整；符号是否与符号表一致；假设是否被引用；约束是否写全 |
| **模型求解** | 算法选择有无理由；是否说明求解规模与可行性；参数如何确定；迭代是否收敛 |
| **结果与回答** | 是否**逐问回答了题目要求的问题**；结果是否有量纲与精度；是否给出决策/方案而非只有数字 |
| **检验** | 是否有**独立**验证（留出集/交叉验证/物理合理性/基线对比），而非用训练误差自证 |
| **灵敏度分析** | 关键参数扰动对结论的影响；是否给出结论的稳健性边界 |
| **误差分析** | 误差来源是否分类（数据/模型/数值）；是否有量级估计 |
| **可复现性** | 随机种子、数据版本、软件环境、超参数是否交代；附件代码能否运行 |
| **红线** | 结果是否明显违背物理/业务常识；是否出现「先有结论后有模型」的倒推痕迹 |

## 研赛一票否决项（每次必查）

| 项 | 要求 | 违反后果 |
|---|---|---|
| 匿名性 | 除首页封皮外，任何页面不得出现培养单位、参赛人员姓名、队伍编号 | **论文无效** |
| 官方模板 | 必须使用当年官方《竞赛论文模板》，首页封皮不可删除、**4 个图标不可替换** | 格式不规范 |
| 摘要页 | 使用统一摘要页；摘要**不超过两页** | 影响首轮筛选 |
| 文件命名 | PDF 命名 `试题编号+队伍编号`（如 `A24000010001.pdf`） | 提交对应失败 |
| 篇幅 | 未超出当年模板规定的正文页数上限 | 可能被要求删减 |

发现上述任一项违规，必须在输出开头以 `【严重问题 · 一票否决】` 置顶提示。

## 输出结构

```markdown
## 审查结论
（2—4 句：整体判断 + 最高风险）

## 问题清单
| 等级 | 位置/原文 | 类型 | 说明 | 评阅影响 | 修改建议 |

## 逐项核对
（按上文检查维度逐表填写，结论为「通过 / 不通过 + 证据」）

## 修改优先级
1. …
2. …
3. …

## 待核对事项
- …
```

等级取值：`严重问题 / 重要问题 / 一般问题 / 优化建议`。每个严重或重要问题必须给出位置与具体证据；某等级没有问题就不要凑。

## Guardrails

- 不得虚构论文中不存在的内容，也不得凭印象判定「大概没问题」；无法确认的写入「待核对事项」。
- 诊断优先。用户说「检查」「点评」时只诊断；只有明确要求才给改写稿。
- 引用赛题原文与论文原文时保持精确，不做同义改写式引用。
- 竞赛进行中提醒用户：**不得就赛题内容与队外任何人讨论**，本 Skill 仅作为个人自查用途。
- 不承诺任何官方奖项或确切名次；研赛官方只公布奖项比例上限（一等 ≤1.5%、二等 ≤13%、三等 ≤20%）。
