---
name: hwb-ai-usage-disclosure
description: Generate or review an AI-tool usage statement and detailed usage disclosure for a HUAWEI Cup paper, matching the contest's explicit policy that AI products may be used only as auxiliary tools with sources cited. Use when a team used AI assistance and must disclose it truthfully, or wants an existing disclosure checked for completeness and consistency.
agent_created: true
---

# HWB AI Usage Disclosure

为研赛论文生成或检查 **AI 工具使用声明**与**使用详情**材料。

## 研赛的 AI 使用官方政策（原文口径）

研赛自第二十一届（2024）起在《竞赛通知》中明确：

> 各参赛队**可使用人工智能产品，仅作为答题的辅助工具，而非主导手段**，不能代替参赛队伍的独立思考和竞赛答题的主体工作。所有参赛队应遵守科学道德与学术规范，正文、数字模型、公式引用等**所有引用文献、引用程序（包括人工智能产品）均按规定注明来源**。

并且：

> 竞赛专家委员会将对所有论文进行查重处理，重复率高于某阈值（由专家委员会确定）的论文，一般直接判定为"违规论文"……**引用他人程序也需明确标注引用来源**，否则发现程序雷同，按抄袭认定为"违规论文"。

**因此本 Skill 的基本立场是：如实、具体、可核查地披露，比模糊或隐瞒安全得多。** 隐瞒会被查重与程序比对识别，而规范披露本身是合规行为。

## Required references

- [references/statement-rules.md](references/statement-rules.md) — 声明撰写规则（必读）；
- [references/usage-categories.md](references/usage-categories.md) — AI 使用类别划分；
- [references/details-template.md](references/details-template.md) — 使用详情模板；
- [references/compliance-checklist.md](references/compliance-checklist.md) — 合规核对清单。

## 两种模式

### 生成模式

输入：论文（或章节）+ **真实的** AI 使用记录（谁在什么环节、用什么工具、做了什么、产出被如何使用、是否被人工修改）。

输出：AI 工具使用声明 + 使用详情表 + 一致性自查结果。

### 检查模式

输入：论文 + 已有披露材料。

输出：完整性、一致性、匿名性、责任边界四方面的诊断与修改建议。

## 核心原则

| 原则 | 说明 |
|---|---|
| **真实性优先** | 只写实际发生的使用。没有使用就不写；使用了就不能漏。不得编造以显得"规范" |
| **辅助性边界** | 必须体现 AI 是**辅助工具**而非主导手段——说明人的判断在哪里介入、结论由谁负责 |
| **可核查** | 每一条使用记录应能对应到论文中的具体位置（章节/图表/代码文件） |
| **引用即注明** | 引用 AI 产出的程序、公式、文字均须注明来源 |
| **匿名合规** | 披露材料中**不得**出现培养单位、姓名、队伍编号（研赛规定除首页封皮外一律禁止） |
| **不上传敏感材料** | 不得把未公开的当届赛题、内部材料、个人身份信息交给外部 AI 服务 |

## 输出结构

```markdown
# AI 工具使用声明

## 一、总体说明
（本队在竞赛中使用/未使用人工智能产品，用途限于哪些环节，全部结论由队员独立负责）

## 二、使用清单
| 序号 | 使用环节 | 工具名称 | 版本/时间 | 用途 | 产出物 | 人工修改程度 | 论文对应位置 |

## 三、辅助性边界说明
（说明 AI 未参与的部分：问题理解、模型选择、核心推导、结果判断、结论形成）

## 四、责任声明
（全部内容由参赛队员独立完成并负责）

# 附：AI 工具使用详情

（逐条展开，见 details-template.md）
```

## 硬约束

- **不得美化或隐瞒**：不得把"AI 生成了整章正文"写成"AI 仅协助语法检查"。
- **不得夸大**：不得把未用过的工具写进清单以显得"技术先进"——列入即意味着要能说明具体用途。
- **不得透露身份**：全过程匿名。工具账号、邮箱、姓名一律不出现。
- **不得为规避查重而改写**：本 Skill 的用途是合规披露，不是规避检测。若用户明确要求"帮我降低 AI 检测率"，应拒绝并说明正确做法是**自己重写内容并如实披露**。
- 声明与详情必须与论文实际内容**版本一致**；论文改动后须重新核对。
- 若用户所在队伍**完全没有使用 AI 工具**，应输出一份简短的"未使用声明"（如当年模板有对应栏目）或明确说明无需填写，而不是造一份假清单。
