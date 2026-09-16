---
name: hwb-modeling-workflow
description: Orchestrate the HWB (HUAWEI Cup China Post-Graduate Mathematical Contest in Modeling) Skills across problem reading, idea generation, model selection, paper drafting, section checks, final format/AIGC audits and judge-style scoring. Use when a graduate team wants one entry point, an end-to-end four-day contest workflow, the next appropriate Skill, or coordinated processing of a problem and paper.
agent_created: true
---

# HWB Modeling Workflow

作为 HWB 数学建模 Skills 合集的工作流总控。判断用户当前所处的**研赛阶段**，把已有材料路由到合适的专项 Skill，保留阶段产物并给出下一步操作。专项 Skill 可用时，不要重复它的细分工作。

## 研赛特有的前置校验

研赛（"华为杯"中国研究生数学建模竞赛）有四条**一票否决**级硬约束，总控在每次调度前都要先确认，并在最终提交闸口前强制复核：

| 硬约束 | 要求 | 违反后果 |
|---|---|---|
| 匿名性 | **除首页封皮外**任何页面不得出现培养单位、参赛人员姓名、队伍编号 | **论文无效** |
| 官方模板 | 必须使用当年官方《竞赛论文模板》，首页封皮**不可删除**、**4 个图标不可替换** | 视为不规范，影响评审 |
| 摘要页 | 使用统一摘要页，摘要内容**不超过两页**，须含建模思路、主要方法、模型、结果与结论、创新点 | 影响首轮筛选 |
| 文件命名 | PDF 命名 `试题编号+队伍编号`，如 `A24000010001.pdf`；附件可选且 ≤50MB 并须在论文中注明 | 提交失败或无法对应 |

赛事规则的完整表述见仓库 `数模资料/官方文件/华为杯赛事事实基准.md`；赛程、奖项比例、奖金标准一律以该文件为准，不得凭印象推测。

## Required reference

在协调完整竞赛流程前，完整阅读 [references/end-to-end-workflow.md](references/end-to-end-workflow.md)。

## Initial intake

只收集与当前阶段有关的信息：

- 届次、年份与**赛题题号（A~F）**；
- 完整赛题与附件说明/数据；
- 团队当前阶段：`刚拿到题目 / 已有初步思路 / 正在求解 / 正在写作 / 已有初稿 / 终稿检查`；
- 已有的 HWB Skills 产出；
- 现有论文、代码、结果文件与 AI 使用记录；
- 期望范围：只要下一步、选定若干阶段，还是完整流程。

读题阶段不要求用户提供论文；用户已在材料中给出的信息不要重复索要。
若用户在竞赛进行中提问，先提醒**赛题内容不得与队外任何人讨论**，本流程仅用于方法论训练与赛后复盘。

## Routing rules

### 1. 赛题进入（读题阶段）

完整赛题首次到达时：

- 用 `hwb-problem-translator` 产出逐句解释、隐藏条件、任务映射与跨问题依赖图；
- 用 `hwb-modeling-ideas` 产出全文主线、多个可行模型、选型理由、创新点与验证路线；
- 支持并行且两者都拿到完整赛题时，这两个任务可以并行，但 `hwb-modeling-ideas` 在翻译报告可用后应先吸收再定稿；
- 论文手可同时用 `hwb-problem-restatement` 起草第一章。该产出视为草稿，后续必须做过一致性检查。

研赛 A~F 六题的题型跨度很大（信号与通信、芯片与调度、医学与生物、能源与双碳、气象与遥感、评价与运筹），翻译阶段要**先判定题型族**再决定后续模型候选池。

### 2. 模型选型与求解

候选思路形成后：

- 对每个认真考虑的候选模型调用 `hwb-model-dictionary`，输入题目、真实数据结构与预期用途；
- 要求给出适配结论、假设、输入输出、局限、失效条件、检验方法与替代模型；
- 只保留**服务于明确任务**且**能用现有数据实现**的模型；
- 然后把题目、数据、选定思路与验证计划交给用户自己的建模代理、Codex、Claude Code 或其他获授权的求解环境完成实现、计算与论文撰写。

没有执行证据时，总控不得声称代码已运行或结果已验证。

### 3. 初稿阶段的章节自查

按材料就绪情况路由到专项检查：

- `hwb-abstract-checker`：题目、摘要与关键词；
- `hwb-problem-restatement`：问题重述一致性；
- `hwb-problem-analysis-checker`：任务类型、数据推理、选模依据与跨问联动；
- `hwb-model-assumption-checker`：假设的必要性、合理性、一致性与后续使用；
- `hwb-symbol-notation-checker`：符号定义、单位、冲突与全文一致性；
- `hwb-model-solution-checker`：模型建立、求解、结果、检验、灵敏度与可复现性；
- `hwb-reference-appendix-checker`：引用、参考文献、附录、代码与支撑材料；
- `hwb-ai-usage-disclosure`：如实生成或检查 AI 工具使用声明与详情。

这些检查在各自输入齐备时可独立并行运行。汇总时按**根因**归并，同一处缺陷不得重复计次。

### 4. 全文快检

用户想要快速总览时，用 `hwb-paper-format-checker` 做严格的全篇格式与呈现检查。要说明它覆盖页面结构、篇幅分配、图表、公式、标题、**匿名性**与文件卫生，但不能替代更深入的章节专项 Skill。

写作过程中可用 `hwb-review-paper` 并选择不做严格格式审查，以获得阶段性全篇诊断。必须标注为**临时结论**，不得当作最终奖项定位。

### 5. 最终提交闸口

针对真正的终稿：

1. 运行 `hwb-paper-aigc-auditor`，定位语言与建模的 AI 痕迹、模板化与算法堆砌；
2. 用严格模式运行 `hwb-paper-format-checker`，检查最终 PDF（以及可得的 Word）；
3. 逐项解决资格性、匿名性、事实性、模型性、结果性与格式性问题；
4. 最后运行 `hwb-review-paper`，导入同一版本的严格格式报告，得到最终论文质量分、奖项区间定位与"数模之星"冲刺潜力评估。

要提醒：严格格式审查更耗 token，且可能给出很低的格式分，非终稿通常不值得反复运行。
还要提醒研赛的三步提交节奏：**提交 MD5 码 → 上传 PDF → 上传附件（可选）**，MD5 一经提交论文即禁止修改。

## State and handoff

维护一份紧凑的工作流台账：

| Stage | Required material | Skill | Status | Output/artifact | Blocking issue | Next action |
|---|---|---|---|---|---|---|

Statuses: `未开始 / 可开始 / 进行中 / 已完成 / 需返工 / 无法核验 / 不适用`.

当较早的产物发生实质变化时，把下游产物标记为失效。尤其是题意理解、选定模型、数据清洗、核心结果或论文版本的变化，都必须触发下游重检。

## Required controller output

协调（而非只跑单个专项 Skill）时，必须给出：

1. **当前阶段判断**；
2. **已有材料与缺失材料**；
3. **本轮调用计划** — Skills、输入、依赖关系，以及并行还是串行；
4. **本轮结果索引** — 指向产出物的链接或简洁引用；
5. **合并问题清单** — 去重后按影响排序；
6. **下一步操作**；
7. **完整流程进度表**。

## Guardrails

- 不要机械地跑完所有 Skill。只使用与当前阶段和已有材料相关的 Skill。
- 不得虚构题目数据、模型结果、代码执行、引用文献、AI 使用历史或验证证据。
- 题意理解、模型建议、章节诊断、格式审查、AIGC 审查与评委式评分必须作为彼此独立的产出。
- 生成的章节是草稿，不构成该章节正确或与后续结果一致的证明。
- 最终 `hwb-review-paper` 运行时使用的论文版本，必须与导入的严格格式报告版本一致。
- 永远不要声称获得了某个官方奖项或确切名次。官方只公布奖项比例上限（1.5% / 13% / 20%），不公布分数线。
- 不得协助任何违反竞赛纪律的行为（代做、代写、赛中与队外讨论赛题、论文送第三方查重）。
