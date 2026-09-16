---
name: hwb-model-dictionary
description: Judge whether a candidate model actually fits a HUAWEI Cup problem, its data and its intended use, returning a model archive with requirements, assumptions, strengths, limitations, failure conditions, validation routes and alternative models. Use when a team is choosing models and needs a data-driven fit decision instead of a generic model list.
agent_created: true
---

# HWB Model Dictionary

判断**候选模型**与研赛题目、数据及预期用途之间是否**真的适配**。禁止给通用教科书式的“这个模型很好用”结论——必须有数据支撑的适配判定。

## Required references

- [references/fit-assessment.md](references/fit-assessment.md) — 适配性评估方法与判定规则（必读）；
- [assets/model-dictionary.json](assets/model-dictionary.json) — 研赛题型→方法词典（含方法档案与替代方案）；
- 查询工具：[scripts/query_dictionary.py](scripts/query_dictionary.py)。

## 输入

- 题目内容或赛题题号（A~F）；
- 数据结构：样本量、变量类型、量纲、缺失情况、时空结构；
- 候选模型名称；
- 求解思路：该模型在本题中的**具体用途**（做预测？做优化？做评价？）。

## 检查维度

| 维度 | 检查点 |
|---|---|
| **任务匹配** | 模型的输出形态是否正是题目要求的形态（数值/方案/排序/判别） |
| **数据充分性** | 样本量、特征维度、标注质量是否满足模型最低要求 |
| **假设成立性** | 模型核心假设在本题是否成立；不成立时的补救代价 |
| **可辨识性** | 参数能否从数据中被唯一确定 |
| **失效条件** | 明确写出该模型在什么条件下会给出错误结论 |
| **验证路线** | 给出**独立**验证方式（不能自证） |
| **替代方案** | 若不适配，给出 1—3 个可行替代与其代价 |
| **实现成本** | 在四天赛程内可完成的最低实现路径 |

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
