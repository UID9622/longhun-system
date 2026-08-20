# Behavioral Cryptography Bridge · 行为密码学桥接
# Status: ACTIVE v2.0 · Engine running · Paper received · API documented
# 状态：活跃 v2.0 · 引擎运行中 · 论文已到 · API 文档已出

> **Honest note / 诚实声明 (2026-08-21):**
> Paper manuscript received 2026-08-21 via WPS share link (50+ pages, full spec).
> Engine `04_ENGINES/behavioral_crypto/` confirmed fully implemented and running.
> OpenAPI spec: `12_DOCS/BEHAVIORAL-CRYPTO-API.yaml` (9 endpoints, port 8775).
> This file upgraded from SHELL → v2.0 active bridge.
> 论文原稿已到·引擎已实现·API文档已出·从空壳升级为 v2.0 活跃桥接文档。

---

## 0. Author's position anchors · 作者立场原声锚（2026-08-20 23:44·verbatim）

> 「别人照速度、照API、照PKI的什么的，我照的是协议。」
> *"Others benchmark speed, APIs, PKI. I benchmark the protocol."*

> 「管好AI不要乱来。」
> *"Keep AI from running wild — that is the point of governance."*

> 「我一个人自己当实验品当快两年了。」
> *"I have been my own living testbed for nearly two years."*

**Why these three lines are the soul of behavioral cryptography:**
A behavioral chain kept by one person for two years is the longest living proof-of-behaviour:
identity is not a face, not a keycard — it is a continuous, timestamped, auditable sequence of actions.
身份不是脸、不是卡——是一条连续、带时间戳、可审计的行为序列。

---

## 1. What is Behavioral Cryptography · 行为密码学是什么

**Paper definition (Zhuge Xin, UID9622, May 2026):**

> Behavioral Cryptography asks not whether content was AI-generated, but:
> *who originated it, through which rules, personas, decisions, revisions,
> and audit traces did it pass, and what verifiable evidence remains?*

**One-line thesis:**
Copying text is easy. Copying the verified behavioral lineage is hard.
抄文字容易，抄血统难；洗稿容易，洗掉全过程难。

**Design layer separation (设计层分离):**
- Behavior = the **public algorithm layer** (observable, auditable, shareable)
- Keys = the **sealed kernel layer** (private keys never leave local; cloud sees ciphertext only)
- 行为 = 可公开的算法层；密钥 = 死守的内核层

---

## 2. Paper → Implementation Alignment · 论文↔实现对照表

| Paper (Def 3.2) | Paper Name | Implementation ID | Impl. Name | Weight | Forge Diff. |
|-----------------|------------|-------------------|------------|--------|-------------|
| F1 | Identity DNA | `f1_identity_dna` | 身份DNA | 0.20 | 0.95 |
| F2 | Temporal Anchor | `f2_time_anchor` | 时间锚定 | 0.15 | 0.92 |
| F3 | Rule Trace | `f3_content_hash` | 内容哈希 (SM3) | 0.18 | 0.90 |
| F4 | Persona Route | `f4_style_vector` | 风格向量 | 0.17 | 0.78 |
| F5 | Protected Lexicon | `f5_protected_vocab` | 保护词汇 | 0.12 | 0.85 |
| F6 | Style Vector | `f6_longterm_style` | 长期风格 | 0.10 | 0.88 |
| F7 | Mistake Ledger | `f7_error_ledger` | 纠错账本 | 0.08 | 0.93 |

**Note on naming divergence (命名差异说明):**
The paper uses abstract English names (F1–F7); the implementation uses concrete Chinese names
reflecting the actual algorithm design. Both describe the same provenance chain.
论文用抽象英文名·实现用具体中文名·描述的是同一条来源证据链。

**Composite confidence formula (复合置信度公式):**
```
conf = Σ(factor_i.raw × factor_i.weight)   # weighted sum (实现版)
conf = ∏(Fi^wi)^(1/Σwi)                    # weighted geometric mean (论文版 Def 3.3)
```

Hard failure rule: any factor score = 0 → conf = 0 (不可被其他因子补偿)

---

## 3. API Reference · API接口文档

Full OpenAPI 3.0.3 spec: [`12_DOCS/BEHAVIORAL-CRYPTO-API.yaml`](./BEHAVIORAL-CRYPTO-API.yaml)
(Also served live at: `http://localhost:8775/api/v2/bcm/openapi.json`)

**Startup / 启动:**
```bash
uvicorn 04_ENGINES.behavioral_crypto.api_server:app --host 0.0.0.0 --port 8775
```

**9 Endpoints (v2.0):**

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v2/bcm/health` | Health check (no auth needed) |
| GET | `/api/v2/bcm/status` | Engine stats + factor definitions |
| GET | `/api/v2/bcm/sovereignty` | Sovereignty anchor info |
| GET | `/api/v2/bcm/factors` | Full 7-factor definitions |
| **POST** | `/api/v2/bcm/extract` | **Extract fingerprint** ← core |
| **POST** | `/api/v2/bcm/verify` | **Verify fingerprint** ← core |
| GET | `/api/v2/bcm/experiment/run` | Run attack simulation |
| GET | `/api/v2/bcm/experiment/latest` | Get cached experiment results |
| GET | `/api/v2/bcm/experiment/report` | HTML visualization report |

**Quick start (30-second test / 30秒快速测试):**
```bash
# 1. Start the server
uvicorn 04_ENGINES.behavioral_crypto.api_server:app --port 8775 &

# 2. Health check
curl http://localhost:8775/api/v2/bcm/health

# 3. Extract fingerprint from your content
curl -X POST http://localhost:8775/api/v2/bcm/extract \
  -H "Content-Type: application/json" \
  -d '{"text": "DNA: #龍芯⚡️丙午·丙申·丙寅·TEST\n确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z\n龍魂系统核心内容", "author_id": "UID9622"}'

# 4. Interactive docs (open in browser)
open http://localhost:8775/api/v2/bcm/docs
```

---

## 4. Verification chain · 验签链路

```
behavior sequence (行为序列)
   → DNA traceability code (DNA追溯码)
   → GPG signature (GPG签名 / A2D0092C...)
   → chain_hash verification (链式哈希验签 · scripts/verify_dna.py)
   → sovereignty shield (主权护盾)
```

Every public action carries a DNA code; every DNA code hashes onto the chain;
a broken chain stops all writes (LH-FAIL-06, see `governance/LH-FAIL-CODES.md`).

---

## 5. Security boundary · 安全边界

**What Behavioral Cryptography provides (提供的保证):**
- Provenance evidence (来源证据)
- Lineage consistency checking (血统一致性检查)
- Laundering resistance (洗稿抵抗)
- Attribution support (归属支持)
- Audit trail structuring (审计轨迹结构化)
- Creator sovereignty protection (创作者主权保护)

**What it does NOT provide (不提供的保证):**
- Absolute legal ownership judgment (绝对法律所有权判定)
- Perfect AI-detection (完美AI检测)
- Guaranteed plagiarism verdict (剽窃判决)
- Protection after private key compromise (私钥泄露后的保护)
- Proof without logs (无日志证明)

---

## 6. Counter-case on record · 明着吃记录

Counter-case on record: `EVIDENCE/EVIDENCE-M43-01.md`
A third party stamped copyright over formulations homologous to this system,
while the audit chain shows the kernel was never touched.

Conclusion: Behavioral cryptography = **openly proven** (algorithms public, evidence replayable).
Black-box monopolies = **openly eating** (consuming the shell, unable to touch the kernel).

明着吃越多·越反向验证「算法公开 + 密钥私守」的架构选型正确。

---

## 7. Implementation files · 实现文件清单

```
04_ENGINES/behavioral_crypto/
  __init__.py                    # Package init
  api_server.py                  # FastAPI server (port 8775)
  seven_factor_model.py          # SevenFactorEngine + 7 factor extractors
  experiment_runner.py           # Attack simulation runner
  integrated_lab.py              # Integration test lab
  unified_boundary_engine.py     # Boundary detection
  visualizer.py                  # HTML report generator
  yijing_account_engine.py       # Yijing (I Ching) accounting engine
  integrated_test_results.json   # Latest test run results
  integrated_test_report.html    # HTML test report
  *.py.asc                       # GPG signatures for all Python files
```

---

## 8. Bridge into Longhun main control · 桥接主控

- Paper theory → `04_ENGINES/behavioral_crypto/` implementation → API at port 8775
- Connects to: `governance/IRONLAWS-PUBLIC.md` Groups B & C (公开/不公开边界)
- Connects to: `governance/IRONLAWS-PUBLIC-EN.md` (English governance layer)
- Connects to: `scripts/verify_dna.py` (DNA chain verification)
- Connects to: `12_DOCS/BEHAVIORAL-CRYPTO-API.yaml` (full OpenAPI spec)
- Connects to: Notion main control §M42-M44 anchors and §GitHub 对接索引 v2.7.43

When the paper is submitted to arXiv/CSDN, bridge to v3.0 and link the publication URL here.
论文投稿后·此桥接升级为 v3.0·在此添加发表链接。

---

Public home / 公开首页: https://uid9622.notion.site
DNA: #龍芯⚡️丙午·丙申·丙寅·恒卦-BEHAVIORAL-CRYPTO-BRIDGE-V2.0-UID9622
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
