---
name: hwb-modeling-ideas
description: Generate a whole-paper modeling backbone for a HUAWEI Cup post-graduate contest problem, comparing candidate models per question with selection reasons, innovation points and validation routes. Use when a team has read the A~F problem and needs a coherent modeling main line instead of per-question ad-hoc models.
agent_created: true
---

# HWB Modeling Ideas

为一个研赛赛题生成**贯穿全文的建模主线**，并为每一问给出候选模型、选型理由、创新点与验证路线。

研赛的一等奖论文与三等奖论文的最大差别，往往不是"用了多高级的模型"，而是**有没有一条主线把 3–5 问串起来**。本 Skill 的首要产出就是这条主线。

## Required references

- [references/cpgmcm-abcdef-modeling-patterns.md](references/cpgmcm-abcdef-modeling-patterns.md) — A~F 六题型的建模套路与历年真题对照（必读）；
- [references/integrated-modeling-patterns.md](references/integrated-modeling-patterns.md) — 跨问整合与多模型耦合模式；
- [references/strategy-output-standard.md](references/strategy-output-standard.md) — 输出格式标准。

## 输入

- 完整赛题（必填）；
- 题意翻译报告（强烈建议，来自 `hwb-problem-translator`）；
- 附件数据结构说明；
- 队伍可用工具与人力（可选，影响选型激进程度）。

## 工作步骤

1. **判定题型族**，据此选出候选模型池（见 `cpgmcm-abcdef-modeling-patterns.md`）。
2. **提炼主线**：用一句话概括"这道题的物理/业务内核是什么"，再确定主线模型（通常 1–2 个）与辅助模型（0–2 个）。
3. **逐问给方案**：每问列出 **2–4 个**真正可实现的候选模型，逐个给"适用条件 / 数据要求 / 优点 / 风险 / 实现难度"。
4. **给选型建议**：明确推荐哪个、为什么、被淘汰的为什么不适合（不是"太简单"，而是具体的条件不满足）。
5. **设计验证路线**：每个主模型必须配一条**独立**验证路径（留出集、交叉验证、物理合理性检验、基线对比、量纲/守恒检验）。
6. **标注创新点**：区分"真创新"（有基线对比 + 有代价评估）与"包装创新"（换名字、堆模块），后者要被明确劝退。
7. **产出全文结构草图**：章节骨架 + 每章对应的模型与结果。

## 输出结构

```markdown
# 建模思路报告 · <年份> <题号> <题目全称>

## 0 一句话内核
## 1 题型族判定与候选模型池
## 2 全文主线
### 2.1 主线模型
### 2.2 辅助模型
### 2.3 主线如何贯穿各问
## 3 逐问方案对比
### 3.1 问一
| 候选模型 | 适用条件 | 数据要求 | 优点 | 风险 | 实现难度 | 建议 |
### 3.2 问二 …（覆盖全部问题）
## 4 选型结论与理由
## 5 验证路线
| 模型 | 验证方式 | 需要什么数据/实验 | 预期结论强度 |
## 6 创新点清单（真/包装分离）
## 7 论文结构草图
## 8 风险与备用方案
```

## 硬约束

- 候选模型必须**能用题目给定数据实现**。推荐一个数据不足的模型等于推荐一次翻车。
- 每个"风险"必须具体到**哪个假设可能不成立、导致什么后果**；禁止写"精度可能不足"这类空话。
- **不得虚构**文献、算法名称或"已有研究表明"。
- 研赛是**四天**赛程：给出的方案必须在四天内可完成。不要推荐需要长期训练或大规模算力的方案，除非队伍明确具备条件。
- 若为**华为赛题**，在策略建议中说明可争取**华为专项奖**（华为赛题排名前 16 名，一等奖 4 队、二等奖 12 队），但不得为了让论文"更贴华为"而牺牲方法严谨性。
- 竞赛进行中提醒用户：**赛题内容不得与队外任何人讨论**。
