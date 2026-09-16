# HWB-review-paper

When reviewing a China Post-Graduate Mathematical Contest in Modeling (华为杯) paper, first read and strictly follow:

@SKILL.md

Treat `SKILL.md` as the controlling workflow. Read every reference it marks as required before scoring. The user must supply the 赛题题号 (A~F) and both the complete contest problem and the complete paper.

If the user supplies an existing `hwb-paper-format-checker` report for the same paper version, pass it into the review and reuse its format score, eligibility findings and page evidence. Normalize the review-format score to `[-10,10]` and calculate the quality coefficient with `(format_score + 10) / 20`. Do not repeat or double-count the same format defects. For every problem, separately score `模型建立`, `模型求解` and `结果与回答` from their 90%-of-weight ceilings, using visible 1/2/3-point deductions for every unmet rubric item.

Award calibration must use the official caps only: 一等奖 ≤ 1.5%, 二等奖 ≤ 13%, 三等奖 ≤ 20%, and must never assert an official cutoff. Treat any derived 临界名次 as an estimate. Additionally assess `数模之星` sprint potential (每题前 2 队进入答辩, 专家投票 70% + 大众评审 30%) and `华为专项奖` eligibility (only for 华为赛题, 前 16 名).

Hard validity checks come first and are one-vote veto: the official current-year template must be used (首页封皮不可删除, **4 个图标不可替换**); **除首页外任何页面出现培养单位、姓名或队伍编号即论文无效**; 摘要不超过两页; PDF 命名须为 `试题编号+队伍编号`; 附件可选且不超过 50MB 并须在论文中注明; 引用人工智能产品必须注明来源.

Typical request:

```text
请使用 HWB-review-paper 评审以下数学建模论文：
赛题题号：A / B / C / D / E / F
赛题：<赛题文件路径>
论文：<论文文件路径>
参赛总队数：<可选，默认按近年约 20000 队估算>
已有格式自查报告：<可选，hwb-paper-format-checker 输出路径>
请严格按照 SKILL.md 的输出顺序生成报告。
```
