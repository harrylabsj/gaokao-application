# 高考志愿填报助手 · gaokao-application

> 一个帮大陆高考家长和考生**把分数和位次变成一份谨慎、可核验的志愿方案**的 AI 技能。
> 它不替你做决定，也**不保证录取**——它帮你把数据理清楚、把风险讲明白、把该核验的清单列出来。

适用于 Hermes / OpenClaw / Codex 等能读取 `SKILL.md` 的 AI Agent。

---

## 给谁用

- **家长 / 考生**：分数出来了，面对几百个院校专业组不知从何下手，想要一份分得清「冲、稳、保、垫」的草案，而不是一句「你能上 XX 大学」。
- **帮人填志愿的老师 / 朋友**：手里有往年录取数据，想快速按位次筛出候选、标注风险、生成可解释的方案。
- **开发者**：想要一个边界清晰、带脚本、可复现的教育类 Agent 技能样例。

## 解决什么问题

把零散的官方录取数据和个人偏好，走通一条链路：

```
确认省份/年份/科类/位次  →  规范化往年录取数据(CSV)
   →  按位次筛候选  →  按位次差分冲稳保垫  →  解释每个选择的风险
   →  给出排序草案 + 提交前必须核验的清单
```

核心原则：

- **以位次为主**，分数只作辅助解释。
- **不跨省套规则**，每次都确认省份、年份、批次、选科、投档模式。
- **历史最低位次不等于未来确定线**，必须解释计划变化、专业冷热、组内调剂等波动。

## 明确不做什么(安全边界)

- ❌ 不保证录取，不输出「稳上」「必中」「包录」这类结论。
- ❌ 不编造当年的录取线、招生计划、院校专业组代码或政策。
- ❌ 不冒充付费咨询机构、不伪造资质、不参与任何招生作假。
- ❌ 不建议绕开体检、单科、语种、性别、政审等官方限制。

完整边界见 [`docs/safety.md`](docs/safety.md)。

---

## 3 分钟看一个完整例子

下面是用本仓库自带的**脱敏示例数据**(`examples/sample_admissions.csv`，校名与录取线均为虚构)跑出的结果。考生设定：湖南 · 物理类 · 本科批 · 位次 24567。

```text
 档位   位次差     院校(示例)          专业组              历史最低位次
 冲    -18.1%    示范理工大学         计算机与电子专业组      20120
 小冲   -2.3%    示范第一大学         电子信息专业组         24010
 稳    +5.4%     示范工程大学         机械与自动化专业组      25900 (2024)
 稳    +7.8%     示范工程大学         机械与自动化专业组      26480 (2025)
 稳    +11.1%    示范师范大学         数学与统计专业组        27300
 保    +22.3%    示范财经大学         经济管理试验班组        30050
 垫    +41.6%    示范海洋大学         海洋与环境专业组        34800
```

完整方案样例(含风险解释、排序建议、核验清单)见 [`examples/sample_output.md`](examples/sample_output.md)。

## 开发者：30 秒复现上面的结果

只需 `python3`，无第三方依赖：

```bash
# 1. 校验数据格式(必需列：school_name, min_rank)
python3 scripts/validate_dataset.py examples/sample_admissions.csv

# 2. 按位次窗口筛出候选
python3 scripts/shortlist_builder.py examples/sample_admissions.csv \
  --rank 24567 --province 湖南 --subject 物理 --window 0.45 --out shortlist.csv

# 3. 按位次差打上冲/稳/保/垫风险档
python3 scripts/risk_scoring.py shortlist.csv --rank 24567 --out scored.csv
```

把你**自己导出的官方往年录取 CSV** 换进第一步即可。列名映射和规范化规则见 [`references/data-contract.md`](references/data-contract.md)。

---

## 安装

SkillHub 页面：

```text
https://skillhub.cn/skills/gaokao-application
```

### Hermes

```bash
hermes skills install harrylabsj/gaokao-application --yes
```

或从 `SKILL.md` 原始 URL 安装：

```bash
hermes skills install https://raw.githubusercontent.com/harrylabsj/gaokao-application/main/SKILL.md --yes
```

### OpenClaw

```bash
openclaw plugins install https://github.com/harrylabsj/gaokao-application
```

本地开发：

```bash
openclaw plugins install ./gaokao-application --link
```

## 怎么用(作为 AI 技能)

1. 把整个 `gaokao-application/` 目录作为 skill 安装到你的 Agent，或直接提供 `SKILL.md` 的 URL。
2. 对 Agent 说明你的情况：省份、年份、科类/选科、分数、位次、批次、偏好、不接受项。
3. 如果你还没有官方数据，Agent 会先给你一份**数据收集清单和官方来源**，而不是假装知道今年的线。
4. 有数据后，Agent 走上面的链路，产出冲稳保垫候选表、风险解释和提交前核验清单。

技能内部结构：

| 路径 | 作用 |
|---|---|
| `SKILL.md` | 技能定义、原则、工作流、边界 |
| `references/` | 工作流、数据契约、各省规则、风险口径、输出模板、官方来源清单 |
| `scripts/` | 数据规范化、按位次筛选、风险打分等可选辅助脚本(纯 `python3`) |
| `examples/` | 脱敏示例数据集与完整输出样例 |
| `docs/safety.md` | 安全边界与风险提示 |

## 重要免责声明

本工具用于**结构化整理和教育性提示**，不是录取预测，也不替代省级考试院、院校招生章程、阳光高考等官方信息和有资质的人工指导。任何志愿决定，请以官方最新数据为准并自行核验。详见 [`docs/safety.md`](docs/safety.md)。

## License

MIT
