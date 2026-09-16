# Changelog

## Collection v1.0.0 - 2026-09-16

- 面向**"华为杯"中国研究生数学建模竞赛（研赛）**建立独立 Skills 合集，仓库结构、分类目录与 Skill 骨架与既有数学建模 Skills 组织范式一一对应；
- 新增 `skills/` 标准目录，按 `总控类` / `生成类` / `论文自查类` / `综合评审与自我定位类` 四类组织，共 **19 个 Skill 目录**（其中 `hwb-review-paper` 与 `hwb-ai-usage-disclosure`、`hwb-problem-restatement` 为跨分类的同名副本）；
- 新增 `数模资料/`，以 **2020—2025 年 36 道真题**与 **229 篇历年优秀论文**为核心资料来源，并附 `_索引数据/` 机器可读原始清单；
- 新增 `integrations/claude-code/hwb-review-paper/CLAUDE.md`，说明 Claude Code 下的补充配置方式；
- 新增完整工作流、统一安装说明、调用示例与官方渠道提示；
- 新增 `数模资料/官方文件/华为杯赛事事实基准.md`，作为全仓库赛事规则的唯一事实来源（source of truth）。

### Included Skills

**总控类**

- `hwb-modeling-workflow`

**生成类**

- `hwb-problem-translator`
- `hwb-modeling-ideas`
- `hwb-problem-restatement`
- `hwb-ai-usage-disclosure`

**论文自查类**

- `hwb-paper-format-checker`
- `hwb-abstract-checker`
- `hwb-problem-restatement`
- `hwb-problem-analysis-checker`
- `hwb-model-assumption-checker`
- `hwb-symbol-notation-checker`
- `hwb-model-solution-checker`
- `hwb-reference-appendix-checker`
- `hwb-ai-usage-disclosure`
- `hwb-paper-aigc-auditor`
- `hwb-model-dictionary`
- `hwb-review-paper`

**综合评审与自我定位类**

- `hwb-review-paper`
- `hwb-cpgmcm-award-standing`

### 与本科国赛版本的关键差异

| 维度 | 本科国赛（参考项目口径） | 本项目（研究生赛口径） |
|---|---|---|
| 赛题数 | A—E 五题 | **A—F 六题** |
| 竞争结构 | 赛区 + 组别 + 省奖/国奖双层 | **全国统一评奖**，不设赛区、不设组别、无省奖 |
| 论文格式 | 无封皮页要求 | **首页封皮页（4 个图标不可替换）**、统一摘要页、**严禁目录** |
| 匿名 | 摘要页匿名 | **除首页外任何页面不得出现单位/姓名/队伍编号**，违反即论文无效 |
| 附录 | 15/30 页阶梯扣分 | **不设页数阶梯**；代码作为独立附件（≤50 MB）提交 |
| 特色荣誉 | 无 | **"数模之星"**（每题 2 队答辩）、**华为专项奖**（华为赛题前 16 名） |
| AI 政策 | 需声明 | **可用作辅助工具但不得主导**，须注明来源，并附独立可核查的披露支撑材料 |
| 提交方式 | 上传论文 | **MD5 码 → 上传 PDF → 上传附件** 三步分时段 |
| 标定样例 | CUMCM 历年真题 | **CPGMCM 2020—2025 全部 36 道真题** |

### 数据与脚本

- `hwb-review-paper/scripts/`：`award_position.py`（奖项区间定位）、`competition_context.py`（三维竞争校准：赛题难度 / 参赛单位 / 华为赛题选择）、`score_percentile.py`（分数→百分位）；
- `hwb-cpgmcm-award-standing/scripts/`：`query_award.py`（按参赛总队数与名次估算奖项临界）、`query_unit.py`（培养单位获奖画像，空模板时优雅提示）；
- `hwb-model-dictionary/scripts/`：`build_dictionary.py`（生成精简词典）、`query_dictionary.py`（按关键词/类别/题型查询）；
- 全部脚本**仅用 Python 标准库**，Python 3.13 兼容，路径按脚本位置相对解析，支持无参数运行时给出示例输出。

### 资料来源说明

- 赛题题目名称以本地赛题原件（2020 年 RAR、2021 年加密 ZIP 含官方解压码、2022—2025 年 ZIP/7Z）为准，逐题核对；
- 优秀论文与队伍编号来自本地历年优秀论文选目录，共 229 篇，其中 2021 年含"数模之星"提名奖论文 12 篇；
- 赛事规则、时间节点、奖项比例与奖金标准来自研创网历届《竞赛通知》原文及各培养单位研究生院转发通知；
- 凡官方未明示的内容一律标注「以当年《竞赛通知》为准」或「待核实」，**不做推测性填充**；
- 不含任何第三方社群二维码、群号、网盘提取码与商业引流信息；
- 所有 `.docx` / `.pdf` / `.xlsx` / `.zip` 形态的参考资产一律改写为 **Markdown / CSV / JSON 文本形态**，并附生成或校验脚本。
