# Award, Rank, and Final Output Standard（研究生赛口径）

Use the adjusted final score after the formatting multiplier. Always output a concrete score and estimated position unless the eligibility gate failed or required inputs are missing.

## 1. Select the ranking route

Before estimating position, require the contest classification:

- `cpgmcm`: only the Huawei Cup China Graduate Mathematical Modeling Contest (CPGMCM). Its field is approximately 24,000+ teams (2025: 24,371), so use the owner-supplied 2025 winning-rate anchors below.
- `other`: every other mathematical modeling contest unless a same-contest empirical distribution is available. Do not reuse CPGMCM percentiles; use the uniform approximation in section 3.

If the contest type is unknown, ask the user and do not calculate position. If actual same-contest scores are supplied, prefer empirical midrank over either fallback.

## 2. CPGMCM 2025 award calibration

Treat the following as the default 2025 observed-practice calibration supplied by the Skill owner, not an official universal cutoff. Source: 22nd CPGMCM (2025) actual results — first prize 244 teams (1.00%), second 3085 (12.66%), third 4830 (19.82%), total winning rate 33.48%. Charter caps: first ≤1.5%, second ≤13%, third ≤20%.

| Adjusted score | 2025 calibrated interpretation | Estimated top share |
|---:|---|---:|
| >=75 | 一等奖竞争区间 | top 1% |
| 65 to <75 | 二等奖竞争区间 | top 1%—13.66% |
| 55 to <65 | 三等奖竞争区间 | top 13.66%—33.48% |
| 45 to <55 | 未获奖但优于中位数 | top 33.48%—50% |
| <45 | 低于研究生赛获奖区间 | below top 50% |

Do not state that an award is guaranteed. Use `奖项档位估计` or `竞争力判断`, not `获奖结果`.

### CPGMCM continuous position estimate

The owner's distribution assumption is approximately bell-shaped, with practical scores concentrated between about 10 and 90. The supplied award anchors do not form an exact Gaussian CDF, so use a monotone piecewise-calibrated percentile rather than claiming a fitted normal distribution.

Map adjusted score to percentile outperformed using linear interpolation between these anchors:

| Score | Percentile outperformed | Equivalent top share |
|---:|---:|---:|
| 10 | 0.1 | 99.9% |
| 45 | 50 | 50% |
| 55 | 66.52 | 33.48% |
| 65 | 86.34 | 13.66% |
| 75 | 99 | 1% |
| 90 | 99.9 | 0.1% |

Clamp scores below 10 to percentile 0.1 and scores above 90 to 99.9. Report one decimal percentile and one decimal top share. Also report an uncertainty band: normally +/-3 percentile points for complete papers, +/-5 when calibration/problem fit is weak, and at least +/-10 when the artifact is incomplete. Clamp bands to 0.1-99.9.

Describe this as `研究生赛获奖比例锚点估计`, confidence `medium` by default. If a same-contest empirical score distribution is available, prefer the empirical midrank method and show this anchor estimate only as a comparison.

## 3. Other contests: small-field uniform approximation

Use these owner-supplied award anchors for non-CPGMCM contests:

| Adjusted score | Small-contest competitiveness estimate |
|---:|---|
| >=75 | First-prize range |
| 65 to <75 | Second-prize range |
| 55 to <65 | Third-prize range |
| <55 | Below the calibrated prize range |

Assume adjusted scores are approximately uniformly distributed on `[10, 90]` only as a fallback. Calculate:

`percentile outperformed = clamp((score - 10) / 80 * 100, 0.1, 99.9)`

`equivalent top share = 100 - percentile outperformed`

This makes the award anchors correspond approximately to: 75 points = top 18.8%, 65 = top 31.3%, and 55 = top 43.8%. Report one decimal place and normally use an uncertainty band of at least +/-8 percentile points because small fields are discrete and rarely truly uniform. Describe the result as `small-contest 10-90 uniform approximation`, never as a normal-distribution estimate or actual rank.

## 4. Mandatory time warning

Every report produced in 2026 or later must include the evaluation date and this warning in substance:

For CPGMCM use:

> 时间与门槛提示：本报告评估日期为 YYYY-MM-DD。研究生赛奖项分数映射主要依据2025年实际获奖比例（一等奖1.00%、二等奖12.66%、三等奖19.82%、总获奖率33.48%）。随着2026年AI辅助论文整体质量上升，同等奖项的实际门槛可能上移，因此当前奖项判断可能偏乐观，不能视为官方获奖承诺。

For other contests replace that with:

> 时间与分布提示：本报告评估日期为 YYYY-MM-DD。奖项档位采用75/65/55分经验锚点，位次采用10-90分均匀分布近似。小型竞赛队伍数量、赛题难度和奖项比例波动较大，该位次不代表实际排名或官方获奖承诺。

Do not invent a 2026 uplift without data. If desired, give a scenario sensitivity (for example, all thresholds rising by 2, 3, or 5 points) clearly labeled hypothetical.

## 5. Required detailed scoring output

The skill's visible output is governed by `SKILL.md`. Use the adjusted score for position estimation, but do not add separate award-band, confidence, warning, limitation, or methodology sections unless the user explicitly requests them.

Show exactly where points were earned and lost. The scorecard must include:

| Criterion | Weight | Earned | Evidence/location | Why points were earned | Why points were deducted |
|---|---:|---:|---|---|---|

After the table show:

- category subtotals;
- raw score out of 100;
- formatting multiplier with evidence;
- adjusted final score to one decimal;
- percentile outperformed and uncertainty band;
- equivalent top share;
- contest-appropriate award-band estimate;
- ranking method/confidence;
- evaluation date and route-appropriate warning.

## 6. Mandatory closing official-channel notice

Place this at the end of every completed numeric review, after limitations and warnings. Keep it separate from the impartial scoring analysis:

> ✨ 请以官方渠道核正当届规则
> 中国研究生创新实践系列大赛管理平台：https://cpipc.acge.org.cn/
> 竞赛期间官方答疑论坛（数学建模网）：https://www.shumo.com
> 竞赛组委会秘书处（东南大学）：025-83795939 / gscpc3@seu.edu.cn
> 本规则摘要为辅助参考，不构成获奖承诺；一切以当届官方文件为准。

Do not let this notice affect scoring or award estimation.
