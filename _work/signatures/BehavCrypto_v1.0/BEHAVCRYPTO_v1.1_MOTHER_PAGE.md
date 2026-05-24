# Behavioral Cryptography v1.1 · Mother Page Frame (local mirror)

> **Notion source:** https://www.notion.so/uid9622/Behavioral-Cryptography-v1-1-v1-0-75bba634a74b43d78da254f4ecbf76a6  
> **Page ID:** `75bba634a74b43d78da254f4ecbf76a6`  
> **Synced:** 2026-05-16  
> **Role:** Satellite mirror of Notion mother page — **not** canonical full manuscript. Canonical body: [`FULL_PAPER_v1.0_Body_Draft.md`](./FULL_PAPER_v1.0_Body_Draft.md).

**DNA (mother page):** `#龍芯⚡️2026-05-16-02:55-PAPER-MOTHER-PAGE-FRAME-v1.0`  
**DNA (paper):** `#龍芯⚡️2026-05-02-BEHAVIORAL-CRYPTOGRAPHY-v1.1`  
**CONFIRM:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL`

---

## 0 · One sentence (定盘句)

| EN | Behavioral Cryptography asks not whether content was AI-generated, but who originated it, through which rules, personas, decisions, revisions, and audit traces it passed, and what verifiable evidence remains. |
| 中文 | 不问「是不是 AI 写的」·只问「谁发起·走什么规则·调什么人格·上什么决策·何处修订·留什么审计证据」。抄文字容易·抄血统难；洗稿容易·洗掉全过程难。 |

---

## 1 · Seven factors + weights (v1.1 default)

| Factor | w_i | 验证目的 | 主要防御 | 硬熔断 |
|--------|-----|----------|----------|--------|
| F1 Identity DNA | 0.25 | UID + GPG + DNA 格式 | 复制粘贴·去身份 | F1=0 → conf=0 |
| F2 Temporal Anchor | 0.15 | ISO + 时辰 + 数字根 | 时间回滚 | F2=0 → conf=0 |
| F3 Rule Trace | 0.15 | LU 链 + 顺序 + 签章 | 假多 Agent 协作 | F3=0 → conf=0 |
| F4 Persona Route | 0.12 | 九宫人格调度 + 签名轨迹 | 伪造人格路径 | F4=0 → conf=0 |
| F5 Protected Lexicon | 0.12 | 主权词抗洗稿 | 面包洗·翻译漂白 | >30% 丢失 → 硬熔断 |
| F6 Style Vector | 0.11 | 与基线余弦相似 | 模型漂白·风格模仿 | 仅概率分 |
| F7 Mistake Ledger | 0.10 | 错误/修正连续性 | 过于「完美」草稿 | 缺失降分·不硬熔断 |

**Aggregation:** `conf = ∏ s_i^{w_i}` with `∑w_i = 1`; hard failure if any `Fi=0` → `conf=0`. Threshold τ: 0.85 (standard) / 0.95 (high-security).

---

## 2 · Theory ↔ practice (双闭环)

| 论文（理论层） | 龍魂可审计工具协议 v1.0（实践层） |
|----------------|-----------------------------------|
| F1–F7 | §1–§6 + §S-25-EXT 对应字段 |
| Dynamic DNA Engine | §2 字段⑨ DNA 追溯 |
| Evidence Ledger | §2 审计日志 · §5 十五指标 |
| Seven-Factor Verifier | §5 AI 行为审计层⑩ |
| Proof Bundle | §2 十字段回执 = 轻量证明包 |
| Local-First | §S-25-EXT DNA L0 · 密钥不出本机 |

**Practice Notion:** https://www.notion.so/0f6dea05dd944be1a05c188152d4aa6c (`0f6dea05dd944be1a05c188152d4aa6c`)  
**生态压缩真源 v2（机器块+双关键字）：** [`BEHAVCRYPTO_ECOSYSTEM_DNA_COMPACT.md`](./BEHAVCRYPTO_ECOSYSTEM_DNA_COMPACT.md) · DNA `#龍芯⚡️2026-05-16-BEHAVCRYPTO×AUDIT-TOOL-ECOSYSTEM-COMPACT-v2.0`  
**认知 OS 母页焊点（Notion §11）：** `#龍芯⚡️2026-05-16-03:33-PAPER-MOTHER-PAGE-V2-CNSH-DNA-COGNITIVE-OS-v1.0`  
**DNA 编辑器：** `压缩` / `展开` → [`tools/behavcrypto_dna_editor.py`](./tools/behavcrypto_dna_editor.py) · [`tools/dna_editor.html`](./tools/dna_editor.html)  
**实践全文镜像：** [`AUDITABLE_TOOL_PROTOCOL_v1.0_FULL.md`](./AUDITABLE_TOOL_PROTOCOL_v1.0_FULL.md)  
**CNSH 路由：** `01_protocols/cnsh/PROTOCOL__AUDITABLE-TOOL-v1.0.local.md`  
**柱⑥ 共生时间 v2（msg 185）：** https://www.notion.so/9c3946bfd10346ccab90fa600b49fc6e · 本地 `01_protocols/cnsh/PROTOCOL__SYMBIOTIC-TIME-BRIDGE-v2.0.local.md` · DNA `#龍芯⚡️2026-05-16-03:57-SYMBIOTIC-TIME-BRIDGE-V2-CNSH-DNA-INTEGRATED-v1.0`  
**女娲五彩石 · 主权终端 UI v1.0：** `01_protocols/cnsh/PROTOCOL__NUWA-COLOR-TERMINAL-v1.0.local.md` · DNA `#龍芯⚡️2026-05-16-NUWA-COLOR-SOVEREIGN-TERMINAL-v1.0`

---

## 3 · Coverage：主稿 vs 生态侧（拆分「约 40%」）

以前写的「~60% / ~40%」容易误解成 **整本 Notion 还有四成没读**。更准确是 **两条独立进度条**：

| 轨道 | 含义 | 当前口径（2026-05-16） |
|------|------|------------------------|
| **A. 主稿 `FULL_PAPER`** | Notion 母页 **§3.9.17+ · §4–9 · Appendix A–D** 是否 **逐段粘贴并入** [`FULL_PAPER_v1.0_Body_Draft.md`](./FULL_PAPER_v1.0_Body_Draft.md) | **未并入前 = 主稿 backlog** · 不在此文件编造正文 |
| **B. 生态侧镜像** | 公式 HTML · CNSH 协议 · L5 · 道德经 · 共生时间 · **女娲终端 UI** 等 | **可走本地 `01_protocols/`、`docs/` 收口** · **不等于** 主稿已写法条 |

**仍暂缓（主稿 A 轨）**

| Block | Status |
|-------|--------|
| §3.9.17+ | **未并入主稿** · 以 Notion 粘贴为准 |
| §4–§9 full POC | **未并入主稿** · 同上 |
| Appendix A–D extensions | **未并入主稿** · 同上 |

**已本地镜像（生态 B 轨，便于工程与 Cursor，不冒充主稿）**

| 内容 | 本地锚点 |
|------|----------|
| 数学公式体系 v2 · HTML | [`docs/math-formula-series/龍魂数学公式体系_v2.0.html`](../docs/math-formula-series/龍魂数学公式体系_v2.0.html) · 接入说明 [`README`](../docs/math-formula-series/README.md) |
| 女娲主权终端 · 五色 BSI | [`01_protocols/cnsh/PROTOCOL__NUWA-COLOR-TERMINAL-v1.0.local.md`](../01_protocols/cnsh/PROTOCOL__NUWA-COLOR-TERMINAL-v1.0.local.md) |
| 柱⑥ 共生时间 v2 | `PROTOCOL__SYMBIOTIC-TIME-BRIDGE-v2.0.local.md` |
| 道德经 81 引擎 | `PROTOCOL__DAODEJING-81-ENGINE-v1.0.local.md` |
| DNA L5 分层 | `PROTOCOL__DNA-L5-ARCHITECTURE-v1.4.local.md` |

旧表述「**~60% integrated · ~40% deferred**」仅指 **A 轨主稿** 与早期 §3.2–3.8 合并进度；**B 轨请以上表为准**。

---

## 4 · Governance boundaries (7 + 6)

**Seven in-scope commitments**

1. Multi-factor behavioral provenance (not single-signal authorship).
2. Hard-fail semantics for identity, time, rule, persona, lexicon breaches.
3. Append-only evidence ledger; corrections append, never replace.
4. Local-first key material; no cloud exfiltration of signing keys.
5. Transparent audit: technical content may be public; black-box refusal.
6. Theory–practice dual loop with auditable tool protocol.
7. DNA + CONFIRM/SEAL on every canonical artifact.

**Six out-of-scope (this paper does not claim)**

1. Mathematical impossibility of forgery (raises cost, not proves impossible).
2. Proof that a human (not AI) typed every token.
3. Legal non-repudiation without jurisdiction-specific process.
4. Replacement for GPG/PKI root of trust assumptions.
5. Real-time network-wide consensus (local/ledger scope only).
6. Full automation of §3.9.17+ without human paste from source **into `FULL_PAPER_v1.0_Body_Draft.md`**. Local protocol mirrors (`01_protocols/`, `docs/math-formula-series/`) do **not** satisfy this item alone.

---

## 5 · Engineering package tree (Longhun mapping)

```
BehavCrypto_v1.0/
├── FULL_PAPER_v1.0_Body_Draft.md   ← canonical manuscript
├── BEHAVCRYPTO_v1.1_MOTHER_PAGE.md  ← this file (Notion mirror)
├── CANONICAL_LOCK.md / CANONICAL_SHA256
├── publication/Notion_page.md      ← channel stub
└── scripts/canonical-sha256/       ← verify after body edits

00_main_control/龍魂DNA登记/
└── 行为密码学_七因子形式化_与论文对齐_v1.md

engine/ · cnsh/ · 算法仓库/          ← runtime hooks (DNA, audit, roster)
```

---

## 6 · Backlog (next sync)

- [ ] Paste §3.9.17+ from Notion **into** `FULL_PAPER_v1.0_Body_Draft.md` when read (A 轨)
- [ ] Expand §4 POC + Appendix A–D in body draft only after source paste
- [ ] Regenerate `FULL_PAPER_v1.0_TOC.md` from body
- [ ] Run `bash scripts/canonical-sha256/update.sh` after each body change
- [x] 数学公式 HTML v2.0：已入仓 `docs/math-formula-series/龍魂数学公式体系_v2.0.html`（可与 `~/Downloads/…升级版 v2.0…html` 用 `cp` 再同步）
- [x] 女娲主权终端 UI 协议 v1.0：`01_protocols/cnsh/PROTOCOL__NUWA-COLOR-TERMINAL-v1.0.local.md`（B 轨）；VS Code 扩展实装另项

---

*UID9622 · local mirror of Notion mother page · 2026-05-16 · §3 拆分升级 2026-05-16*
