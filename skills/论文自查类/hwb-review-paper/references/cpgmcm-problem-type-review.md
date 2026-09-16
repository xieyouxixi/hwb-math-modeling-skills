# CPGMCM A—F Problem-Type Review Prompts（六题制题型审阅提示）

Use this reference only after reading the complete current problem. These are historically distilled review prompts from 2021—2025 Huawei Cup (CPGMCM) problems, not prescribed answers. The current task always controls; a different method earns full credit when it is correct, suitable, evidenced and complete.

> **重要**：华为杯每届固定 A—F 六题，但**题号含义逐届变化**，历史仅作审阅提示，不能套用。下表给出近年各题号的典型方向，必须依当届赛题独立制定评分细则，接受任何合理替代方案。

## A：工程物理 / 调度优化类

- 典型包含机理建模、几何/物理约束、组合或连续优化、数值求解与工程验证。
- 核查状态变量、控制变量、目标函数、约束是否完整且可解；不要以中心点近似替代完整碰撞/覆盖/可行性判定。
- 要求初始/边界条件、单位、步长、容差、收敛性与取整后可行性。
- 惩罚无依据的几何简化、黑箱优化、缺失离散化与可复现性检查。

## B：华为企业题 / 通信网络数据类

- 华为赛题通常落此（历届多为 B 题），选 B 可参评**华为专项奖**。
- 数据驱动为主：核查数据口径、缺失/异常、特征与可解释性，避免黑箱堆模型。
- 建模对象常为通信/网络/链路/速率等，要求指标定义明确、结果可落到工程决策。
- 选华为赛题者，额外关注其在华为赛题中的相对排名潜力（华为专项奖与常规奖奖金累加）。

## C：数据驱动建模 / 智能诊疗 / 材料器件类

- 识别数据结构（缺失、组成约束、重复测量、时序、层级、跨期依赖）。
- 要求数据生成解释，以及各问之间输出的真实传递。
- 核查泄漏、不合适的普通相关/回归/聚类，以及预测与决策的分离。
- 从最终提交解独立复算目标与硬约束；材料/器件类关注物理可解释性（如斯坦麦茨方程修正）。

## D：空间地理 / 多源数据融合类

- 涉及坐标系统、尺度、多源一致性与空间统计。
- 将自然语言规则翻译为状态、事件、决策、转移、容量与优先级。
- 要求可执行的坐标/区域/路线结果，并进行规则、数值与方案审计。
- 多源数据需做一致性、配准与不确定性处理，不得简单拼接。

## E：信号处理 / 故障诊断 / 交通工程类

- 核查可观测信息、禁用以信息与潜在信息；关注可辨识性、唯一性、退化与噪声敏感。
- 信号/谱/缺陷计数类匹配相应变换与似然；诊断需落到具体检修/控制决策。
- 故障诊断强调可解释性、域适应/无监督方法的合理性，以及稳健性验证。
- 交通工程类关注通行能力、安全与可实施的管控方案。

## F：机理建模 / 量化评价类

- 偏机理推导与评价体系构建，开放性强。
- 要求评价维度定义、权重依据（题目给定或可追溯）、闭环自洽。
- 多模态/主观指标需有可量化映射，避免纯主观打分。
- 创新点易体现但必须自洽、可复现，且有对比或敏感性分析支撑。

## Cross-problem scoring rule

For every explicit question, independently freeze and score `模型建立`, `模型求解`, and `结果与回答`. Historical red flags may generate checks only when the current prompt and paper evidence make them relevant. Do not deduct merely because the paper does not use a historically common model.
