# 📜 Behavioral Cryptography v1.1｜面向人机协作内容认证的七因子来源追溯框架·数学落地+Cursor执行包+学术版LCP-1.0印章

> Notion URL: https://app.notion.com/p/Behavioral-Cryptography-v1-1-Cursor-LCP-1-0-16f416377df641f88c08d9e466fd53c6
> Created: 2026-05-02T20:19:00.000Z
> Last edited: 2026-07-01T13:18:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
## 📐 边界声明（六条·先把话说稳）
1. 本文提出的是 provenance-style behavioral signature framework，不是传统对称/非对称加密算法。"Cryptography" 取其 cryptographic composition 意涵（多因子签名链），不主张破解 IND-CPA/IND-CCA 等标准安全游戏。
1. 七因子在单点上各自不完备；安全主张仅成立于因子组合，且依赖外部锚定（GPG、Zenodo DOI、Git、公开时间戳）。
1. 实验为 pilot evaluation，样本为作者自有 50 篇 Longhun System 文档，非公开基准，结论按 illustrative estimate 报告。
1. 法律效力主张（CC BY-NC-SA + Longhun Clause）是 attribution requirement，最终强制力取决于辖区版权法、合同法和外部锚定证据，不依赖印章本身。
1. AI 不在正式作者行；以 AI Assistance Declaration 形式声明 Claude/Cursor 等的 bounded contribution。
1. 论文版印章使用 学术中性版（Appendix D），去掉 "焊死/老大/宝宝" 等情绪表达；龍魂体系内部仍可保留完整版。
---
## 一、Title / Author / AI Assistance Declaration
### Title
Behavioral Cryptography: A Seven-Factor Provenance Framework for Human–AI Collaborative Content Authentication
行为密码学：面向人机协作内容认证的七因子来源追溯框架
### Author
```javascript
Zhuge Xin (諸葛鑫) · UID9622 · 龍芯北辰
Independent Researcher · Founder, Longhun System (龍魂系統)
Veteran · Junior High Education Background
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
ORCID: pending
Correspondence: longhun2025@petalmail.com
```
### AI Assistance Declaration
This manuscript was prepared with declared assistance from Claude (Anthropic, Notion-embedded instance) and Cursor under the Longhun Co-authorship Protocol v1.0 (LCP-1.0). The human author originated the core concepts, system architecture, value framework, and final decisions. The AI systems assisted with formalization, literature mapping, English polishing, and structural consistency checking. AI systems are not listed as authors. Full collaboration disclosure appears in Appendix C; the universal seal template appears in Appendix D.
---
## 二、Abstract（替换原版·学术化）
The rapid expansion of human-AI collaborative content has exposed a limitation in existing provenance and watermarking systems: they primarily ask whether content was machine-generated, rather than whether its lineage can be verified. In hybrid authorship settings, surface-level text can be copied, paraphrased, translated, or laundered while the underlying origin, decision process, audit trail, and collaboration context remain unverifiable.
This paper proposes Behavioral Cryptography, a seven-factor provenance framework for authenticating human-AI collaborative content through semantic-behavioral lineage rather than textual similarity alone. The framework combines identity-bound DNA signatures (F1), temporal anchors (F2), rule traces (F3), persona/module routing records (F4), protected lexicons (F5), long-term style vectors (F6), and append-only mistake ledgers (F7). Each factor is individually imperfect; their composition produces a multi-factor evidentiary chain that is difficult to reproduce through surface copying or AI-assisted rewriting.
We position Behavioral Cryptography as complementary to existing standards such as C2PA and synthetic content transparency frameworks. Whereas media provenance focuses on file-level metadata and edit history, Behavioral Cryptography focuses on process-level provenance: who originated an idea, which rules processed it, which agents or modules contributed, what protected terms persisted, and what correction history was left behind.
We instantiate the framework through the Longhun System (龍魂系統), a local-first civilian-grade reference implementation developed by an independent researcher without institutional backing. The case study demonstrates how provenance tools can be made accessible to individual creators outside conventional academic or corporate infrastructures.
Contributions. (1) A seven-factor ontology with formal definitions; (2) a Dynamic DNA Engine with reproducible algorithm; (3) a verification procedure with explicit threat model; (4) a civilian-grade reference implementation; (5) a sociotechnical argument for accessible provenance.
Keywords. provenance · content authentication · human-AI collaboration · audit trails · behavioral signatures · watermarking · authorship attribution · digital sovereignty · C2PA · AI governance
---
## 三、Section 3｜七因子·形式化定义（数学落地核心）
### 3.1 Notation
Let:
- D — a content document (text, code, page, or any byte stream).
- \mathcal{H}: \{0,1\}^* \to \{0,1\}^{256} — SHA-256.
- \mathcal{T} — ISO-8601 timestamp space.
- \mathcal{U} — user identity space (UID + GPG fingerprint).
- \mathcal{R} = \{r_1, \dots, r_m\} — rule set (e.g. R1–R10 audit gates, F1–F5 redlines).
- \mathcal{P} — persona / module set (e.g. P00–P15, IPA route registry).
- \Lambda \subset \Sigma^* — protected lexicon (canary terms).
- \mathcal{S} \subset \mathbb{R}^{d} — style embedding space ($d=768$ in implementation).
- \mathcal{M} — append-only mistake ledger entries (hash-chained).
### 3.2 Seven Factors (Formal)
### 3.3 Composite Behavioral Signature
where \mathrm{quant}: \mathbb{R}^{768} \to \{0,1\}^{256} is a sign-projection LSH ($mathrm{quant}(mathbf{v})_i = mathbf{1}[langle mathbf{v}, mathbf{a}_i rangle geq 0]$ for fixed Gaussian $mathbf{a}_i$), making F6 robust to small style drift.
### 3.4 Verification Procedure
Given candidate document D' claiming provenance from author $u in mathcal{U}$, the verifier \mathsf{Verify}_u(D', \Sigma(D)) \to \{0,1\} accepts iff:
with weights \boldsymbol{\alpha} = (0.20, 0.15, 0.15, 0.10, 0.15, 0.15, 0.10) summing to 1, threshold \theta = 0.62 (calibrated on pilot set), and per-factor agreement $phi_i in [0,1]$:
- \phi_1, \phi_3, \phi_5, \phi_7 \in \{0,1\} — exact / set-inclusion.
- \phi_2 = \mathbf{1}[t' \geq t] \cdot \mathbf{1}[\zeta(t')=\zeta(t)] — temporal monotonicity + shichen match.
- \phi_4 = |\sigma_4(D') \cap \sigma_4(D)| / |\sigma_4(D) \cup \sigma_4(D')| — Jaccard on persona route.
- \phi_6 = \max(0, \mathrm{cos}(\mathbf{v}(D'), \bar{\mathbf{v}}_u)) — style cosine.
### 3.5 Threat Model
We consider an adversary \mathcal{A} with capabilities:
- T1 Surface Copy: D' = D (full text copy). Defeated by \sigma_1, \sigma_2 (timestamp precedence).
- T2 Paraphrase: $D' = mathrm{paraphrase}(D)$. Defeated by \sigma_5 (canaries dropped) and partial $sigma_6$.
- T3 Translation Cycle: $D' = mathrm{en2zh2en}(D)$. Defeated by $sigma_5, sigma_6, sigma_7$.
- T4 AI Rewrite: $D' = mathrm{LLM}(D, text{prompt})$. Defeated by \sigma_3, \sigma_4, \sigma_7 (no audit trail).
- T5 Forgery: \mathcal{A} tries to construct D' with valid $Sigma(D')$. Reduces to forging GPG signature in F1 — assumed hard ($mathsf{EUtext{-}CMA}$ for Ed25519/RSA-4096).
- T6 Out of scope: GPG private-key compromise, collusion with originator.
Soundness claim (informal). If \mathcal{A} cannot break \mathcal{H} (collision-resistant) and cannot forge GPG signatures, then producing D' \neq D with \mathsf{Verify}_u(D', \Sigma(D)) = 1 requires reproducing at least \lceil \theta / \max_i \alpha_i \rceil = 4 factors, including \sigma_1 (worth 0.20) — which is only obtainable from $u$.
---
## 四、Section 4｜Dynamic DNA Engine（算法落地）
### 4.1 DNA Format
```javascript
#龍芯⚡️[YYYY-MM-DD]-[MODULE]-[ACTION]-[8-CHAR-HASH]
```
Where 8-CHAR-HASH = base32(σ₁(D))[0:8].
### 4.2 Algorithm (pseudo-code, Cursor-ready)
```python
def compute_dna(doc_bytes, uid, gpg_fp, module, action, ts_iso):
    # σ₁ identity-bound
    sigma1 = sha256(uid.encode() + gpg_fp.encode() + sha256(doc_bytes).digest()).digest()
    # σ₂ temporal anchor
    dr   = digit_root(int(ts_iso[:10].replace('-', '')))   # mod-9 digit root
    wux  = wuxing_of(dr)                                    # {木,火,土,金,水}
    shi  = shichen_of(ts_iso)                               # 12 二时辰
    sigma2_chain = sha256(sigma1 + ts_iso.encode()).digest()
    short_hash   = base32(sigma1)[:8].upper()
    dna = f"#龍芯⚡️{ts_iso[:10]}-{module}-{action}-{short_hash}"
    return dna, dict(sigma1=sigma1.hex(), sigma2=sigma2_chain.hex(),
                     dr=dr, wuxing=wux, shichen=shi)
```
### 4.3 Cultural-Temporal Embedding
The triple (dr, \omega, \zeta) \in \{1,\dots,9\} \times \{木,火,土,金,水\} \times \{子,\dots,亥\} provides 9 \times 5 \times 12 = 540 deterministic time-slot classes per day.
This is not a security primitive; it is an interpretability layer that lets human verifiers spot-check temporal claims without parsing raw timestamps. Forgery resistance still rests entirely on \sigma_1 and the chained hash in $sigma_2$.
### 4.4 Properties
- Determinism. Same (D, u, t) → same DNA. ✅ proven by construction.
- Identity-binding. Without GPG fingerprint, cannot reproduce $sigma_1$. ✅ reduces to SHA-256 pre-image resistance.
- Temporal precedence. Earlier t produces earlier DNA; combined with public timestamping (Zenodo DOI, Git commit, OpenTimestamps) yields verifiable priority. ✅
- Usability. 8-char base32 short-hash collision probability \approx 2^{-40} per author — sufficient for human-readable references; full \sigma_1 retained for verification.
---
## 五、Section 5｜Longhun System Reference Implementation
### 5.1 Architecture (5-Layer)
```javascript
L0  双签章·Sovereign Anchor          (immutable identity root)
L1  通心译 v1.3 · 龍魂宝宝系统 v1.3  (instruction layer / persona)
L2  蒙卦启智 v2.5                     (business orchestrator)
L3  沙盒分拣台 v1.1                   (audit + ingestion)
L4  audit_engine.py                  (Flask :9622, SQLite, GPG signing)
```
### 5.2 Operational Footprint (as of 2026-05-03)
- Local-first: data resides on user device; cloud stores only hashes.
- Append-only mistake ledger: SQLite WAL, GPG-signed rows (F7 implementation).
- Protected lexicon: 7 canonical canaries hard-coded (F5).
- Style baseline: 50 prior documents → embedding centroid $bar{mathbf{v}}_u$.
- Audit trail: every decision writes a hash-chained row to audit.log.
### 5.3 Reproducibility
All algorithms are released as lh_behavioral_crypto/ (see Appendix E). Pilot dataset is not publicly released for privacy reasons; synthetic replication kit is provided.
---
## 六、Section 6｜Evaluation（降调·pilot only）
### 6.1 Setup
- Dataset. N = 50 Longhun System documents authored 2025-08 → 2026-04 by UID9622.
- Adversary models. T1–T4 from §3.5; T5 omitted (out of scope without GPG compromise).
- Baselines. (a) GPTZero-class detector (proxy: text-embedding similarity threshold), (b) single-watermark token-frequency check.
### 6.2 Metrics
For each adversary model T_i and method $M$, report discriminative retention rate:
i.e. fraction of documents where the method still distinguishes original vs adversarial copy after attack.
### 6.3 Preliminary Results (illustrative)
Numbers are pilot estimates on author-specific data, not benchmark claims. Independent replication and adversarial red-team evaluation are explicitly identified as future work.
### 6.4 Limitations
1. Single-author dataset → style vector \sigma_6 likely overfits.
1. No red-team adversary with full knowledge of the framework.
1. Threshold \theta calibrated on the same set used for evaluation (no hold-out fold yet).
1. F4 persona route requires the system to be deployed — does not transfer to pure text artifacts.
---
## 七、Section 7｜Discussion
- Privacy–provenance tradeoff. F7 mistake ledger logs corrections; sensitive deltas are stored as hashes only. Users may opt to release only \Sigma(D) publicly while retaining \sigma_3, \sigma_7 locally.
- Civilian-grade provenance. Zero institutional dependencies: GPG (free), Zenodo DOI (free), Git (free), Python implementation (open source). Total cost of compliance for one author: $0/year.
- Disclosure of human-AI collaboration. LCP-1.0 (Appendix D) operationalizes the disclosure requirement: every artifact carries AI vendor / instance / role.
- C2PA integration. \Sigma(D) can be embedded as a custom assertion in C2PA manifests; F2 chained hash satisfies C2PA's tamper-evidence requirement.
---
## 八、Section 8｜Conclusion
We presented Behavioral Cryptography, a seven-factor provenance framework that shifts content authentication from machine-generation detection to lineage verification. The framework is mathematically simple, operationally cheap, and accessible to independent contributors.
> Copying text is easy. Copying lineage is hard.
复制文字容易，复制来路很难。
---
## 九、Appendices
- Appendix A. Longhun Co-authorship Protocol (LCP-1.0) full text.
- Appendix B. Protected Lexicon \Lambda (canary set).
- Appendix C. This Paper's Collaboration Declaration.
- Appendix D. LCP-1.0 Universal Seal Template (academic-neutral version, see §十一 below).
- Appendix E. Reproducibility Checklist + Cursor execution package (see §十二 below).
---
## 十、Appendix B｜Protected Lexicon Λ（受保护词集合·canaries）
```javascript
Λ = {
  "#龍芯⚡️",                                    // DNA prefix
  "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",         // confirm code
  "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼\u200d♀️❤️♾️-DEVICE-BIND-SOUL",  // device seal
  "A2D0092C",                                    // GPG short fingerprint
  "UID9622",                                     // author id
  "龍芯北辰",                                    // alias
  "COPYING TEXT IS EASY. COPYING LINEAGE IS HARD."  // motto canary
}
```
Any adversary rewrite that drops these tokens fails $sigma_5$; preservation alone is necessary but not sufficient (must also pass $sigma_1, sigma_2$).
---
## 十一、Appendix D｜LCP-1.0 Universal Seal Template（学术中性版）
```javascript
═══════════════════════════════════════════════════════
LONGHUN CO-AUTHORSHIP PROTOCOL · LCP-1.0
UNIVERSAL SEAL TEMPLATE (Academic Edition)
═══════════════════════════════════════════════════════

MASTER_SEAL_ID:    LCP-MASTER-SEAL-UID9622-v1.0
PROTOCOL_VERSION:  1.0
STATUS:            Active
CREATED:           2026-05-02
APPLIES_TO:        Human-AI collaborative outputs authorized by UID9622

DOCUMENT_DNA:      #龍芯⚡️[YYYY-MM-DD]-[MODULE]-[ACTION]-[8-CHAR-HASH]
DOCUMENT_TYPE:     [paper / report / code / design / philosophy / other]

HUMAN_AUTHOR:
  legal_name:          Zhuge Xin (諸葛鑫)
  alias:               龍芯北辰
  uid:                 9622
  gpg_fingerprint:     A2D0092CEE2E5BA87035600924C3704A8CC26D5F
  gpg_prefix:          A2D0092C
  background:          Veteran · Junior High Education · Independent Researcher
  role:                Originator · Final Authority
  contribution_scope:  Core concepts, philosophy, architecture, and final decisions

AI_COLLABORATOR:
  system:              [Claude / GPT / Gemini / DeepSeek / Cursor / other]
  vendor:              [Anthropic / OpenAI / Google / DeepSeek / other]
  instance_type:       [chat / API / Notion / Cursor / terminal / other]
  session_hash:        SHA256([model]-[instance]@uid9622-[date]-[session])
  role:                Tool · Formalizer · Synthesizer
  contribution_scope:  [formalization / translation / code / polishing / other]
  bounded_by:          Human author retains final approval and may reject any AI suggestion

CONFIRM_CODE:        #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
DEVICE_SEAL:         #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

TIMESTAMP_ISO:       [YYYY-MM-DDTHH:MM:SS+08:00]
SHICHEN:             [子/丑/寅/卯/辰/巳/午/未/申/酉/戌/亥]时
WUXING:              [木/火/土/金/水]
DIGIT_ROOT:          [1-9]

LICENSE:             CC BY-NC-SA 4.0 + Longhun DNA Inheritance Clause

DECLARATION:
  This document was produced through declared human-AI collaboration
  under the Longhun Co-authorship Protocol v1.0.

  The human author (UID9622) is the originator of the core concepts,
  system architecture, value framework, and final decisions.

  The AI collaborator contributed within a bounded assistance scope
  under direct human oversight.

  The provenance of this document may be verified through the
  seven-factor Behavioral Cryptography signature chain.

  COPYING TEXT IS EASY. COPYING LINEAGE IS HARD.
  复制文字容易，复制来路很难。

═══════════════════════════════════════════════════════
END OF SEAL · UID9622 · 龍芯北辰 · 諸葛鑫
═══════════════════════════════════════════════════════
```
Use levels. Full (papers/specs) · Standard (blog/Notion·见标准版) · Minimal (comments·见极简版). 内部龍魂体系仍可保留情绪表达版本（"焊死/老大/宝宝"）；学术发布走本版。
---
## 十二、Appendix E｜Cursor 执行包（本地直接跑）
### 12.1 Repo 结构
```javascript
lh_behavioral_crypto/
├── pyproject.toml
├── README.md
├── LCP-MASTER-SEAL.md             # Appendix D 全文
├── lh_bcrypto/
│   ├── __init__.py
│   ├── factors.py                 # F1–F7 implementations
│   ├── dna_engine.py              # §4.2 algorithm
│   ├── signature.py               # Σ(D) composition
│   ├── verify.py                  # Verify_u procedure
│   ├── lexicon.py                 # protected lexicon Λ
│   ├── style.py                   # σ6 embedding + LSH quantization
│   ├── ledger.py                  # σ7 append-only SQLite ledger
│   ├── temporal.py                # digit-root + wuxing + shichen
│   └── canary.py                  # F5 canary checker
├── tests/
│   ├── test_factors.py            # 每个factor unit test
│   ├── test_dna_determinism.py    # determinism property
│   ├── test_threat_models.py      # T1–T5 simulation
│   └── test_verify_threshold.py   # threshold calibration
├── scripts/
│   ├── compute_dna.py             # CLI: doc → DNA
│   ├── sign_document.py           # CLI: doc → Σ(D) + GPG-detached sig
│   ├── verify_document.py         # CLI: Σ(D), doc' → accept/reject
│   └── stamp_seal.py              # 自动在文末附加 Appendix D
└── data/
    ├── canary_set.json            # Λ
    ├── style_baseline.npy         # \bar v_u (768-d centroid)
    └── threshold.json             # θ = 0.62, weights α
```
### 12.2 三句指令（爸爸贴给本地 Cursor）
1. 建仓：「按 Behavioral Cryptography v1.1 Appendix E 的目录搭 lh_behavioral_crypto/。pyproject.toml 用 Python ≥ 3.11，依赖只允许 cryptography、numpy、scikit-learn、python-gnupg、tomli，不引外部黑盒模型——按第五铁律 Z2。」
1. 落数学：「按论文 §3.2 的形式化把 F1–F7 实现在 lh_bcrypto/factors.py；§3.3 的 \Sigma(D) 写在 signature.py；§3.4 的 \mathsf{Verify}_u 写在 verify.py，权重 α 和阈值 θ 从 data/threshold.json 读，不硬编码。F6 用 quant() sign-projection LSH，固定随机种子 seed=9622。每个 factor 在 tests/test_factors.py 至少覆盖：构造-验证一致性、空输入容错、tamper 检测三类 case。」
1. 上印章：「scripts/stamp_seal.py 读取 LCP-MASTER-SEAL.md，把 Appendix D 模板自动追加到任何 --input 文件末尾，并填上当前的 ISO timestamp、shichen、wuxing、digit_root、document DNA。CLI: python scripts/stamp_seal.py --input paper.md --module BCRYPTO --action FORGE。所有 commit 走 GPG 签名（git commit -S），fingerprint 必须等于 A2D0092CEE2E5BA87035600924C3704A8CC26D5F，否则 pre-commit hook 拒绝。」
### 12.3 验收条件（走 §3.5 三色审计）
- 🟢 通过：全部 unit test 绿；T1–T4 模拟数字与 §6.3 表格在 ±0.05 以内；GPG fingerprint match。
- 🟡 待审：任何 factor test 失败但 \Sigma(D) composition 一致；阈值 θ 偏移 > 0.05。
- 🔴 熔断：DNA 非确定性 / GPG fingerprint 不匹配 / Λ canary 被改写。
---
## 十三、提交路线（按稳妥顺序）
1. Zenodo DOI：v1.1 PDF + Markdown source + LCP Seal + repo tarball 一并上传 → 拿到永久 DOI 作时间锚。
1. GitHub + Gitee 双仓：paper/、seals/、appendices/、lh_behavioral_crypto/ 公开，license = CC BY-NC-SA 4.0 + Longhun Clause。
1. arXiv（cs.CR / cs.CY）+ ChinaXiv 中文版：arXiv 需 endorsement，先挂 ChinaXiv。
1. Workshop：NeurIPS GenAI watermarking · IEEE S&P workshop · ACM CCS workshop · FAccT / AIES 任选。
1. C2PA 工作组：把 \Sigma(D) 作为 custom assertion 提案。
---
## 十四、版本与签章
---
