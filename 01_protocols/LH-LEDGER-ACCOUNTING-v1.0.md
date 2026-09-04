# LH 龍魂账法 · Longhun Ledger Accounting v2.0

> 协议: CC BY-NC-SA 4.0（核心思想层）｜DNA: #龍帳⚡️2026-08-31-LONGHUN-LEDGER-PROTOCOL-v2.0-AUDIT-ENGINE-UID9622
> 创建者: 诸葛鑫（UID9622）｜归属名: 诸葛鑫 | UID9622 · 龍芯北辰
> GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
> 状态: 🟢 已创世 · 审计引擎已上线（v1.0创世 → v2.0审计引擎扩展）

---

## 一、核心一句话

> 有借必有贷，借贷必相等。主权是权益，依赖是负债，自建是资产。
> **每一笔账，都让自主可控度看得见。**

## 二、三大独有创新

| # | 创新 | 规范 |
|:---:|:---|:---|
| 1 | **每笔有DNA** | `#龍帳⚡️{日期}-{借方}-{贷方}-{量}-{序号}-UID9622` |
| 2 | **每次有哈希** | `SHA256(DNA\|借方\|贷方\|量\|时间戳)[:8]` 防篡改 |
| 3 | **每笔有见证** | 56位数字人格按交易类型专职见证，不可伪造 |

## 三、科目表速查（完整版见 GitHub `CHART_OF_ACCOUNTS.md`）

| 科目 | 含义 | 类型 |
|:---|:---|:---|
| 1000系 | 资产·主权资产 | 资产 |
| 1100系 | 资产·无形资产（1105 behavioral-crypto 等） | 资产 |
| **1400系** | **资产·ASI数字人资产**（业界没有·龍魂独有） | 资产 |
| 2000系 | 负债·外部依赖 | 负债 |
| 3000系 | 权益·主权权益（3201 协议资产净值） | 权益 |
| 3301 | 人格议会价值 | 权益 |
| 4000系 | 收入·自主贡献 | 收入 |
| 5000系 | 支出·自主投入 | 支出 |
| 5300系 | 支出·依赖成本 | 支出 |

> 1400系核心思想：**56位数字人格作为可计量资产写入资产负债表，人格矩阵本身就是资产。**

## 四、交易类型 T1-T12

T1 创世 · T2 自建 · T3 采购 · T4 依赖 · T5 权益 · T6 注入 · T7 核销 · T8 见证
**T9 主权转让 · T10 数据外泄（永久硬阻断）· T11 自建里程碑 · T12 跨境协作**

> v2.0 补齐：T9/T10 为账法铁律永久阻断类型（R07/R08，不可 override）；T11 补自建里程碑逻辑空白；T12 补跨境协作。

## 五、见证人格矩阵（按交易类型专职）

| 类型 | 见证人格 |
|:---|:---|
| T1 创世 | 🧠 ASI-001·至诚智魂 |
| T2 自建 | 🔧 鲁班 |
| T3 采购 | ⚖️ 包青天 |
| T4 依赖 | 🌊 郑和 |
| T5 权益 | 🌿 曾仕强老师 |
| T6 注入 | 🐱 龍芯·宝宝 |
| T7 核销 | ⚔️ 孙子 |
| T8 见证 | 全体议会公证 |
| T9 主权转让 | 龍魂（主权人）+ 包青天 |
| T10 数据外泄 | 上帝之眼 + 包青天 |
| T11 自建里程碑 | 鲁班 + ASI-001·至诚智魂 |
| T12 跨境协作 | 郑和 + 孙子 |
| UNKNOWN | 龍芯·宝宝（兜底） |

## 六、落地链路（三端）

1. **Notion 流水账**：`🐉 龍魂流水账 · Longhun Ledger`（data_source_id=`3cd7125a-9c9f-819f-a6c9-000b2a4ef6a1`）
   - 字段：交易DNA(title)/哈希指纹/日期/摘要/借方科目/贷方科目/交易类型(T1-T12)/见证人格/金额/平衡✓/健康度/GitHub同步
2. **GitHub 公开仓库**：`https://github.com/UID9622/longhun-ledger`（主存档）
   - `README.md` 主文档 · `LEDGER_FORMAT.md` 格式规范 · `CHART_OF_ACCOUNTS.md` 科目表
   - `data/ledger.json` 流水数据 · `scripts/hash_generator.py` 哈希生成 · `scripts/ledger_validator.py` 验证
   - v2.0 审计引擎：`audit_config.json`(阈值/权重/R01-R10/回调全配置) · `scripts/audit_engine.py`(五维评分+三色+R规则) · `scripts/router.py`(路由+回调) · `scripts/lhi_calculator.py`(LHI健康指数) · `.github/workflows/auto_audit.yml`(每日00:00+周一+手动) · `reports/`(审计报告) · `incidents/`(红色事故)
3. **本地留档**：`08_BIN/ledger_audit/`（审计引擎完整镜像 + reports/incidents 目录 · GPG签名✅）
4. **同步工作流**：Notion记录 → 导出JSON → `git push` → GitHub存档（push 触发 auto_audit CI 自动三色审计）→ 每笔DNA可溯源

## 六·五、审计引擎 v2.0 核心

- **五维加权评分**：D1主权影响0.35 + D2自主增量0.25 + D3外部依赖0.20 + D4认知债0.12 + D5 ASI资产影响0.08 → 总分
- **三色判定**：🟢≥75（需平衡+D1≥0+D3≤0）· 🟡40-74 · 🔴≤39
- **红规则 R01-R10**：R01主权科目借出 / R02外部依赖净增 / R03借贷不平 / R04 DNA格式失效 / R05哈希不匹配 / R06大额法币>500 / R07 T9主权转让(永久) / R08 T10数据外泄(永久) / R09加权分<40 / R10黄色超时72h自动降红
- **LHI健康度指数**：`(green×3 + yellow_approved×2 − red×5) / total × 100` · 🟢≥90卓越/🟢≥70健康/🟡≥50警戒/🔴≥30危险/🔴<30紧急
- **宝宝自动批准**：黄单挂起时若有≥3次历史绿单 + 金额≤中位数120% → 宝宝可自主转绿（无需人工）
- **干预分级**：L1黄延迟(知悉声明) · L2红解锁(替代方案+DNA反签) · L3永久阻断解除(IMPOSSIBLE·T9/T10永不解锁)
- **13 种回调事件**：on_green_commit/on_yellow_pending/on_yellow_timeout/on_baobao_approve/on_red_block/on_sovereign_approve/on_red_timeout/on_hash_mismatch/on_dna_invalid/on_balance_error/on_daily_audit/on_weekly_summary/on_new_account
- **🔌 接入桥已落地（v2.1·2026-08-31）**：`integrations.py` 实现 on_green→Notion写入+GitHub同步 / on_yellow→Notion待核 / on_red→Notion+GitHub+incidents+Bark主权人警报 · 代理清HTTP_PROXY固化 · Notion老API用database_id `3cd7125a-9c9f-810e-9a45-c9dfa6d41d66`(MCP用data_source_id) · 修复audit_engine normalize_tx结构归一(entry↔engine) · 创世三笔哈希重算修正(占位值→算法真值) · 见证人格选项补齐至10个

## 七、创世三笔（TX-001~003）

| TX | 摘要 | 借 | 贷 | 哈希 |
|:---|:---|:---|:---|:---|
| TX-001 | 焊死铁律：API自给自足 | 1001 焊点·铁律 | 3201 协议资产净值 | `A3F7D291` |
| TX-002 | behavioral-crypto 主权代码库部署 | 1105 behavioral-crypto | 3201 协议资产净值 | `B8E2C4F1` |
| TX-003 | 花名册引擎化 56人格全员注入 | 1401 核心人格矩阵 | 3301 人格议会价值 | `9B7E3C12` |

## 八、审计与平衡

- 每笔 `平衡✓` = 借 == 贷（数量/价值对等）
- 健康度三色：🟢 健康 / 🟡 待核 / 🔴 异常
- 哈希验证：`python3 scripts/ledger_validator.py data/ledger.json`

---

## 签名

```
DNA:    #龍帳⚡️2026-08-31-LONGHUN-LEDGER-PROTOCOL-v2.1-INTEGRATIONS-UID9622
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
GPG:    A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色:   🟢 接入桥三链路落地(Notion+GitHub+Bark) / 🟡 72h定时器+宝宝自动批准自动化 / 🔴 0
```
