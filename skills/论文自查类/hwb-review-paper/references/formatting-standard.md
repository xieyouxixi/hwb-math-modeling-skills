# Mathematical Modeling Paper Formatting Standard（研究生赛口径）

Apply this standard in three stages: eligibility gate, normalized `[-10,10]` formatting score, then deterministic `0-1.00` format-quality coefficient. Keep mandatory contest rules separate from recommended house style.

If the user has already run `hwb-paper-format-checker` on the same paper version, do not repeat this audit from scratch. Import its eligibility evidence and score, convert it with `atomic-deduction-scoring.md`, and recheck only changed or previously unverifiable items. Never deduct the same formatting defect twice.

## 1. Eligibility gate: no score if failed（研究生赛格式硬约束）

Check these items before scoring. If a supplied artifact clearly violates any applicable **hard rule**, report `不具备获奖资格（格式硬性规则未通过）`, list the evidence, and do not calculate a numeric score or percentile.

1. **PDF 格式**：提交的电子版论文（含摘要）必须为 PDF 格式，不得压缩。
2. **命名**：论文命名为 `题号 + 队伍编号`，如 `A24000010001.pdf`；题号用 A—F。队伍编号以当届管理平台公布为准。
3. **官方模板与封皮**：论文必须按当届官方模板编写；**首页为封皮且不可删除**，封皮含团队信息与 4 个图标（不可替换）；**第二页起为摘要页与正文页**。
4. **匿名性**：除首页外，任何页面不得出现单位、参赛人员姓名、队伍编号等信息，否则论文无效。
5. **统一摘要页**：使用官方统一摘要页；摘要须含建模思路、主要方法、模型、结果与结论、创新点等；**摘要内容不超过 2 页**。
6. **严禁目录**：论文中严禁出现目录。
7. **附件（可选）**：非必须；确需提交时命名 `题号 + 队伍编号.rar`，**不得超过 50 MB**，且须在论文中注明。
8. 每处引用文献、引用程序（含 AI 产品）须注明来源；AI 使用须有独立、可核查的披露支撑材料（同样匿名）。

只有当证据证明确实违反时才判 fail。物理纸张属性、未提供页面等不可核验项标记为 `待人工核验`，不得判 fail。当用户的赛事规则不同，以该赛事提供的强制规则为准。

## 2. Formatting score: `-10` to `10` with itemized deductions

Start at 10. Deduct 1-3 points for each distinct error occurrence or repeated error class. Preserve deductions beyond 10 so that severe formatting can produce a negative score, but clamp the score used for coefficient mapping to no lower than `-10`:

`format_score = max(-10, 10 - Σ formatting_deductions)`

For the raw 100-point rubric, the formatting category cannot contribute negatively and remains 90%-capped: `formatting earned = min(9.0, max(0, format_score))`. Label any ceiling-only difference as `评委满分保留（该项90%封顶）`; do not list it as a formatting error.

- **1 point (minor):** isolated inconsistency that does not impede reading, such as one caption alignment issue, occasional spacing mismatch, or a small numbering defect.
- **2 points (moderate):** repeated inconsistency, missing structural element, unclear unit/notation, broken cross-reference, weak citation form, or a defect that slows review.
- **3 points (major):** pervasive inconsistency, seriously unreadable visual/equation/table, missing required substantive appendix material, untraceable citation practice not already triggering the gate, or a structural defect that materially obstructs judging.

Group identical repeated defects into an error class unless their separate occurrences have independent impact. Do not deduct the same defect under abstract, formatting and model quality. Show an itemized ledger and the capped total.

## 3. Deterministic format-quality coefficient

Calculate the coefficient only from `format_score`:

`format_multiplier = clamp((format_score + 10) / 20, 0, 1.00)`

| Format score | Coefficient |
|---:|---:|
| -10 | 0.00 |
| -5 | 0.25 |
| 0 | 0.50 |
| 5 | 0.75 |
| 10 | 1.00 |

Intermediate values use the same linear formula. Use `Final score = Raw score × format_multiplier`, rounded to one decimal. Never reduce below 0 or above 100. Show the format score, formula and resulting coefficient. Do not select or adjust the coefficient impressionistically. A paper that fails the eligibility gate receives no coefficient or numeric score.

## 4. Recommended house style, not mandatory

Use these as consistency references only:

- Chinese body: 小四号宋体; English body: 12 pt-equivalent Times New Roman; single spacing; first-line indent two Chinese characters; zero paragraph spacing.
- Chinese title: 三号黑体, centered. Abstract heading: 四号黑体, centered. Keywords: 小四号黑体 label.
- Level 1 heading: 四号黑体, centered. Level 2: 小四号黑体, left. Level 3: 小四号宋体, left.
- Keep typography, spacing and color internally consistent. A different coherent design earns no deduction.

## 5. Section-specific review checks

### Title, abstract and keywords

Use `title-abstract-keywords.md` for content scoring. Abstract normally uses prose rather than tables, charts or formulas. Keywords normally number 3-5 and represent the problem, model and algorithm. Avoid double deduction.

### Problem restatement

- Cover background, required tasks and relevant existing approaches where useful.
- Rewrite in the team's own words; do not copy the complete prompt.
- Avoid reproducing prompt figures, tables and attachments unless essential.

### Problem analysis

- Explain what must be done, the objective/principle and proposed route for each question.
- Analyze data/attachments and preprocessing where relevant.
- Establish modeling direction but do not reveal final results here; results belong in the abstract/results sections.
- If problem restatement, problem analysis, assumptions, notation or pre-solution exposition reveals a final result or key process-derived numerical result, list all occurrences and apply the one-time 5-point post-score penalty defined in `evidence-centered-scoring.md`.

### Assumptions

- Include only prompt-given, prompt-derived or model-necessary assumptions.
- Keep them plausible, relevant and neatly listed; usually 4-8 is sufficient.
- Do not assume the model or chosen evaluation indicator are correct.

### Symbols

- Give symbol, meaning and unit in a compact consistent list/table, normally no more than about half a page.
- Do not list one-use symbols; remind readers when a symbol reappears after a long gap.
- Prefer conventional notation and avoid overloaded symbols.

### Tables, figures and formulas

- Prefer three-line tables. Put table number/title above, centered; put figure number/title below, centered.
- Number consistently either globally (`表1`, `图1`) or by section (`表1-1`, `图1.1`). Refer to every substantive table/figure in the text.
- Use readable text smaller/lighter than body where appropriate. State units as `quantity/unit symbol` or equivalent.
- Number formulas consistently when referenced. Accept MathType or native Word equations; judge rendering, consistency and editability rather than software choice.

### Model evaluation

- State real strengths, limitations, sensitivity/robustness, improvements and possible extensions.
- Do not manufacture innovation. A limitation can motivate but need not equal the only improvement.

### References

- Start references on a new page. Require in-text citation markers and a consistent complete bibliographic form.
- Use at least five references as a recommended benchmark, not an automatic eligibility rule unless the contest states it.
- Check books, journal articles and web resources for author/title/source/year or access date as applicable.
- Chinese problems and China-specific contexts should include real, relevant Chinese-language sources when suitable sources exist. An entirely English bibliography is a source-balance and judge-impression defect, but irrelevant Chinese items must not be added merely to satisfy appearance.

### Appendices

- Start appendices on a new page.
- Include the core code/commands needed to reproduce every question, including independently sourced data. “Complete code” means that every question's core calculation chain is present, not that every engineering file, third-party library source, repeated utility, debug version or full log is pasted into the paper. Do not duplicate contest-provided data.
- If no program was used, explicitly state so. Missing, non-runnable or body-inconsistent code is a major error and may affect reproducibility/model-solution scoring in addition to formatting only when those are distinct impacts.
- CPGMCM has **no** page-count tier rule: do not apply a "body about 30 pages" target, and do not deduct for appendix pages at 15/30-page thresholds. Whether appendices count toward the submitted PDF, and whether code must ship as a separate attachment instead of inside the PDF, both defer to the current official 《论文格式规范》 and 《论文模板》. When the current rule is unknown, mark `待核对官方规则` — never fabricate a page limit or an ineligibility claim.
- If code ships as the optional attachment package, check only that it is named `题号+队伍编号.rar` and does not exceed 50 MB. An over-limit package is a submission-compliance issue, not a formatting deduction.

## 6. Required formatting output

Report:

1. eligibility gate table: item, status (`pass`, `fail`, `待人工核验`), evidence;
2. itemized 1-3 point deduction ledger;
3. formatting score `max(-10, 10 - total deductions)` and its nonnegative 90%-capped raw-score contribution;
4. deterministic coefficient `(format_score + 10) / 20` and visible calculation;
5. raw total and adjusted final total, unless gate failed.
