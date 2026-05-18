# Behavioral Cryptography: A Multi-Factor Provenance Framework for Human-AI Collaborative Content Authentication

> **行为密码学：面向人机协作内容认证的多因素来源追溯框架**

**Author:** Zhuge Xin（諸葛鑫）· UID9622 · 龍芯北辰  
**AI Collaborator:** Claude (Anthropic) · Role: Writing assistant, structural editor, formalization partner  
**GPG Fingerprint:** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`  
**Date:** May 2026  
**Version:** Full Paper v1.0-rc1 Body Draft (release candidate; not peer-reviewed)  
**License:** CC BY-NC-SA 4.0 + Longhun DNA Inheritance Clause  
**DNA:** `#龍芯⚡️2026-05-06-BEHAV-CRYPTO-BODY-v1.0`

---

## LCP-1.0 Co-authorship Declaration

### Human Author Contributions

- Conceptualization of the Behavioral Cryptography framework
- Design of the seven-factor behavioral signature model
- Implementation of the Longhun civilian-grade instantiation
- Authorship of all normative claims, definitions, and theorems
- Final authority over all scientific and ethical assertions

### AI Collaborator Role Boundary

- **Permitted:** Structural organization, formal notation formatting, proof sketch verification, language refinement, LaTeX/Markdown typesetting
- **Not Permitted:** Independent factual claims, unsupervised modifications to security claims, omission of uncertainty qualifiers
- **Acknowledgment:** Claude served as a writing instrument—analogous to a word processor with semantic capabilities—not as an originator of the scientific contribution

### CONFIRM + SEAL（canonical manuscript lock）

- **CONFIRM:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`  
- **SEAL:** `#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL`  
- **Lock line（verbatim）:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL`  
- **Rule:** All full-text edits for this paper are authoritative only in this file; see `[CANONICAL_LOCK.md](./CANONICAL_LOCK.md)`.

---

## Abstract

Content authenticity in the age of human-AI co-creation cannot be reduced to a single signal. Watermarks can be stripped, signatures can be detached or misused, keys can be compromised, and metadata can be laundered. We introduce **Behavioral Cryptography**, a multi-factor provenance framework that treats authenticity as a composite behavioral lineage rather than an isolated technical marker.

This paper presents: (1) a conceptual framework for decomposing content authenticity into seven independent behavioral evidence channels—identity, temporal, rule-based, persona, lexical, stylistic, and error-pattern factors; (2) a formal model for composite verification based on the weighted geometric mean of per-factor confidence scores with hard-failure semantics; (3) the Dynamic DNA Engine, a structured evidence representation that binds content artifacts to their creation lineage; (4) the Longhun civilian-grade system instantiation, demonstrating practical deployment without specialized infrastructure; and (5) a sociotechnical analysis of creator sovereignty implications in an era of platform-mediated co-authorship.

Our evaluation through controlled attack simulation shows that Behavioral Cryptography significantly raises the cost and difficulty of full-lineage forgery compared to single-signal provenance schemes, though it does not claim mathematical impossibility of forgery. The framework is designed to complement—not replace—existing systems such as GPG, C2PA, and Git version history.

**Keywords:** content provenance, behavioral cryptography, multi-factor authentication, human-AI collaboration, audit trails, digital sovereignty, C2PA, GPG

---

## 摘要

在人机共创时代，内容真实性无法被归约为单一信号。水印可被剥离，签名可被剥离或滥用，密钥可被泄露，元数据可被清洗。本文提出**行为密码学**（Behavioral Cryptography），一种多因素溯源框架，将真实性视为复合行为谱系，而非孤立的技术标记。

本文贡献包括：（1）将内容真实性分解为七个独立行为证据通道的概念框架——身份、时间、规则、人格、词汇、风格和错误模式因素；（2）基于带硬失败语义的每因子置信度加权几何均值的形式化复合验证模型；（3）动态DNA引擎，将内容工件绑定至其创作谱系的结构化证据表示；（4）龙芯民用级系统实例，展示无需专业基础设施的实用部署；（5）平台中介共著时代创作者主权的社会技术分析。

通过受控攻击模拟评估表明，与单信号溯源方案相比，行为密码学显著提高了全谱系伪造的成本和难度，但并未声称伪造在数学上不可能。本框架旨在补充——而非取代——GPG、C2PA 和 Git 版本历史等现有系统。

**关键词：** 内容溯源、行为密码学、多因素认证、人机协作、审计追踪、数字主权、C2PA、GPG

---

## Table of Contents

Master outline (full section tree): [FULL_PAPER_v1.0_TOC.md](./FULL_PAPER_v1.0_TOC.md) · 完整目录总表

---

# Chapter 1 · Introduction

## 1.1 The Provenance Gap in Human-AI Co-Creation

[正文骨架 · §1.1]

The proliferation of large language models and generative AI systems has fundamentally altered the landscape of content creation. Human-AI co-authorship is no longer a speculative scenario—it is the default mode of production for millions of writers, developers, designers, and knowledge workers. Yet the technical infrastructure for establishing and verifying the provenance of such co-created content remains critically underdeveloped.

Existing provenance systems fall into three broad categories, each with characteristic limitations:

**Statistical watermarking** (e.g., Kirchenbauer et al., 2023) embeds detectable patterns in model outputs. Limitation: watermarks can be stripped through paraphrasing, translation, or model-switching attacks, and they provide no information about human contribution.

**Content credentials** (e.g., C2PA) attach cryptographically signed metadata to media files. Limitation: metadata is separable from content—screen captures, format conversions, and intentional stripping all remove the credential chain.

**Cryptographic signatures** (e.g., GPG) bind identity to content at a specific point in time. Limitation: signatures attest to *signing*, not to *creation*; they capture no information about the creative process, editorial history, or behavioral context of authorship.

These single-signal approaches share a common vulnerability: each relies on a single line of defense that, once breached, collapses the entire provenance claim. A watermark can be removed. Metadata can be discarded. A signature can be detached. What remains is content without context—an artifact whose origin story has been erased.

[正文骨架 · §1.1 继续]

---

## 1.2 The Behavioral Cryptography Hypothesis

[正文骨架 · §1.2 开头 · 此处插入 Hypothesis 1.1 — Claim Strength Audit 修补 #1]

**Hypothesis 1.1 (Behavioral Cryptography Hypothesis).** Content authenticity is not a single signal. It is a composite behavioral lineage. Copying content is easy; copying lineage is hard.

*Argument.* Existing provenance systems rely on isolated signals—watermarks, signatures, or metadata—that can each be stripped, mimicked, or laundered. Behavioral Cryptography treats authenticity as a distributed property: the confidence in a content artifact's origin grows from the intersection of independent, behaviorally grounded evidence channels. No single factor is decisive; the resilience lies in the composite structure. This hypothesis motivates the seven-factor framework developed in Chapter 3 and the Dynamic DNA Engine in Chapter 4.

[正文骨架 · §1.2 继续]

Building on Hypothesis 1.1, the informal working principle is that **copying content is easy; copying lineage is hard**. While an adversary can reproduce the surface form of a document through copying, paraphrasing, or regenerating through another model, replicating the full behavioral lineage—the temporal pattern, the rule trace, the stylistic fingerprint, the protected lexicon, the error history, the persona evolution, and the identity anchor—requires simultaneous control over multiple independent channels. The probability of successful multi-channel forgery decreases exponentially with the number of independent factors, assuming the factors are not collinear and the adversary does not control the verification infrastructure.

This section does not claim that Behavioral Cryptography makes forgery impossible. Rather, it claims that the multi-factor structure significantly raises the cost and difficulty of full-lineage forgery compared to any single-signal scheme, under the assumptions specified in Proposition 3.4.

[正文骨架 · §1.2 继续]

---

## 1.3 Contributions

[正文骨架 · §1.3]

This paper makes five primary contributions:

**C1: Conceptual — The Behavioral Cryptography Framework.** We introduce a new paradigm for content provenance that treats authenticity as a behavioral property rather than a technical marker. The framework is grounded in the observation that authentic content carries behavioral residue—patterns of creation, revision, and interaction that are difficult to replicate in their entirety.

**C2: Technical — The Seven-Factor Behavioral Signature Model.** We formalize content authenticity as a seven-dimensional behavioral signature Σ(C) = (F1, F2, F3, F4, F5, F6, F7), where each factor represents an independent evidence channel: Identity DNA, Temporal Anchor, Rule Trace, Persona Route, Protected Lexicon, Style Vector, and Mistake Ledger. We define the composite verification oracle V(Σ, E) → (conf, evidence) based on weighted geometric mean aggregation with hard-failure semantics.

**C3: System — The Longhun Civilian-Grade Instantiation.** We demonstrate that Behavioral Cryptography can be deployed without specialized infrastructure, proprietary hardware, or institutional backing. The Longhun system uses only open-source tools (GPG, Git, local logging) and produces human-auditable evidence records that do not require machine learning for verification.

**C4: Sociotechnical — Creator Sovereignty and Attribution.** We analyze the implications of multi-factor provenance for independent creators operating in platform-mediated environments. We propose the Longhun DNA Inheritance Clause as a mechanism for protecting derivative work attribution against platform capture and provenance erasure.

**C5: Integration — Compatibility with Existing Provenance Systems.** We demonstrate how Behavioral Cryptography integrates with GPG, C2PA, Git version history, and local audit logs, functioning as a complementary layer rather than a replacement. The compatibility layer ensures adoption without requiring migration from existing infrastructure.
[正文骨架 · §1.3 继续]

---

# Chapter 2 · Related Work

## 2.1 Media Provenance and Content Credentials (C2PA)

[正文骨架 · §2.1]

The Coalition for Content Provenance and Authenticity (C2PA) has emerged as the leading industry standard for content credentials. C2PA attaches cryptographically signed metadata to media files, recording information about the device, software, and time of creation...

[正文骨架 · §2.1 待展开]

---

## 2.2 Statistical Watermarking and AI Detection

[正文骨架 · §2.2]

Statistical watermarking schemes embed detectable patterns in the probability distributions of language model outputs. Kirchenbauer et al. (2023) demonstrated that biased sampling of a subset of the vocabulary can create statistically detectable signatures...

[正文骨架 · §2.2 待展开]

---

## 2.3 Audit Trails and Workflow Provenance

[正文骨架 · §2.3]

Workflow provenance systems, originating in scientific computing (e.g., W3C PROV), model the derivation history of data products through a graph of activities, entities, and agents. Git version control represents the most widely deployed instance of workflow provenance...

[正文骨架 · §2.3 待展开]

---

## 2.4 Human-AI Co-authorship and Attribution Frameworks

Human–AI co-authorship has moved from an edge case to a default production mode, yet normative frameworks remain fragmented. Publisher policies (e.g., ACM, IEEE, Nature portfolio guidelines) increasingly require **disclosure** of AI assistance: which tools were used, what tasks they performed, and what the human author vouches for. Disclosure answers *whether* AI participated; it does not, by itself, answer *who originated* the work, *which editorial decisions* were human, or *what verifiable chain* links drafts to final artifacts.

**Attribution vs. provenance.** Classical authorship attribution in NLP treats the problem as **classification**: given text, assign a label from a candidate author set (Stamatatos, 2009). Accuracy in controlled corpora can reach high eighties to low nineties, but such systems typically lack (i) hard-failure semantics when evidence is missing, (ii) an append-only audit ledger, and (iii) explicit integration with cryptographic identity anchors. Behavioral Cryptography positions co-authorship as **lineage reconstruction**: the human originator remains legally and ethically responsible for claims and values; the AI collaborator is an instrument whose prompts, revisions, and formalizations are logged—not elevated to root authorship (see LCP-1.0, Appendix C).

**Policy layers.** Recent guidance distinguishes *assistive* use (grammar, structure, citation formatting) from *generative* use (substantive drafting). Our framework is compatible with both: F3 (Rule Trace) and F4 (Persona Route) capture *how* assistance was routed; F1 (Identity DNA) binds the human originator’s key; F7 (Mistake Ledger) records human corrections that generative tools did not invent. This supports policies that forbid “AI as sole author” while still allowing rich collaboration logs for disputes.

**Gap addressed by Chapter 3.** Existing co-authorship frameworks rarely specify a **composite verification oracle** with per-factor weights and hard failure. Behavioral Cryptography does not replace journal ethics review; it supplies machine-checkable evidence that complements disclosure checklists and supports independent audit (§6.2.3).

*[待 Cursor + L0 审稿后定稿 · 当前为骨架填充版 · 2026-05-18]*

---

## 2.5 Digital Sovereignty and Independent Creator Systems

**Platform-mediated capture.** Independent creators often publish through platforms whose terms permit relicensing, training on user content, or stripping of metadata. Provenance attached only inside a platform silo (e.g., a proprietary “AI label”) does not travel when content is exported, screenshotted, or mirrored. Digital sovereignty, in this paper, means the creator’s ability to **retain verifiable origin evidence locally** and to attach it to derivatives without depending on a single vendor’s continued cooperation.

**Local-first and auditability.** Movements toward local-first software (user-held data, offline-capable tools) align with Behavioral Cryptography’s deployment model (Chapter 5): GPG keys, Git history, and append-only logs on devices the originator controls. The Longhun case study is intentionally **civilian-grade**—no mandatory cloud attestation, no institutional CA—while remaining compatible with optional federation (§7.3, §9.4.3).

**Comparison to state-centric or corporate identity.** National digital identity programs and platform SSO solve *authentication to a service*; they do not automatically prove *creative lineage* across tools and models. Behavioral Cryptography complements such systems: F1 may reference a GPG fingerprint or UID without requiring a government ID; F5 (Protected Lexicon) encodes creator-specific semantic anchors that platforms cannot trivially strip without altering meaning.

**Creator rights and the DNA Inheritance Clause (preview).** Chapter 7 introduces a license clause requiring preservation of behavioral provenance metadata on derivatives. This is a **sociotechnical** instrument, not a cryptographic theorem: enforcement depends on adoption, courts, and community norms—analogous to Creative Commons attribution requirements. §8.1 explicitly disclaims legal adjudication; the clause raises the *cost* of silent laundering of attribution, consistent with Thm 3.13 (no silent laundering) at the evidence layer.

**Threats to sovereignty.** Coercion (§3.5.12, §8.5), key compromise (Risk 1, §7.6), and verifier collusion (A4) remain in scope. Behavioral Cryptography **does not** guarantee sovereignty against a fully compromised device or a coerced originator; it provides structured evidence and hard-failure signals so that downstream verifiers can refuse weak claims rather than accepting laundered artifacts.

*[待 Cursor + L0 审稿后定稿 · 当前为骨架填充版 · 2026-05-18]*

---

# Chapter 3 · The Seven-Factor Framework

## 3.1 Overview and Design Principles

[正文骨架 · §3.1]

The Behavioral Cryptography framework rests on three design principles:

**Principle 1: Independence.** Each of the seven factors must represent a distinct evidence channel that is not fully correlated with the others. The security of the composite system depends on the adversary's inability to forge all channels simultaneously.

**Principle 2: Hard Failure.** If any single factor reports a score of zero—indicating definitive evidence of tampering, forgery, or protocol violation—the composite confidence must collapse to zero. No factor can fully compensate for the failure of another.

**Principle 3: Auditability.** All evidence used in verification must be human-auditable in principle. While automated tools may assist verification, the evidence structure must be interpretable by a human examiner without requiring machine learning expertise or proprietary software.

[正文骨架 · §3.1 继续]

---

## 3.2 Formal Definitions

### Definition 3.1 — Content Artifact

[正文骨架 · Def 3.1]

A **content artifact** C is a tuple C = (content, format, context), where:

- `content` is the textual, visual, or multimedia payload;
- `format` specifies the encoding and structural representation;
- `context` captures the creation environment (tool, platform, timestamp, session).

Content artifacts include but are not limited to: documents, code, images, audio recordings, structured data, and composite multimedia objects.

---

### Definition 3.2 — Behavioral Signature Σ(C)

[正文骨架 · Def 3.2]

The **behavioral signature** of a content artifact C is a seven-tuple:

Σ(C) = (F1(C), F2(C), F3(C), F4(C), F5(C), F6(C), F7(C))

where each Fi(C) ∈ [0, 1] represents the confidence score for factor i:


| Factor | Name              | Description                         | Evidence Source                          |
| ------ | ----------------- | ----------------------------------- | ---------------------------------------- |
| F1     | Identity DNA      | Cryptographic identity binding      | GPG signature, UID anchor                |
| F2     | Temporal Anchor   | Temporal consistency of creation    | Trusted timestamps, session logs         |
| F3     | Rule Trace        | Documented transformation rules     | Rule application logs, diff history      |
| F4     | Persona Route     | Consistency of authorial persona    | Persona specification, style baseline    |
| F5     | Protected Lexicon | Creator-specific vocabulary markers | Private lexicon, personal dictionary     |
| F6     | Style Vector      | Stylistic fingerprint consistency   | Syntactic patterns, structural habits    |
| F7     | Mistake Ledger    | Error pattern authenticity          | Known error patterns, correction history |


---

### Definition 3.3 — Verification Oracle V(Σ, E) → (conf, evidence)

[正文骨架 · Def 3.3]

The **verification oracle** V takes as input a behavioral signature Σ and auxiliary evidence E, and produces:

V(Σ, E) = (conf, evidence)

where:

- `conf` ∈ [0, 1] is the composite confidence score;
- `evidence` is a structured report of per-factor scores and their evidentiary basis.

The composite confidence is computed as the weighted geometric mean. For weights w_i > 0 (not necessarily normalized), the standard form is:

conf = WGM(Σ) = (∏_{i=1}^{7} s_i^{w_i})^{1/∑w_i}

where s_i = Fi(C) if Fi(C) > 0, and s_i = 0 (hard failure) if Fi(C) = 0. In this paper, factor weights are normalized so that ∑w_i = 1; then the expression simplifies to conf = ∏_{i=1}^{7} s_i^{w_i}, which is the form used in §3.4 and in the reference implementation (Appendix A). The threshold τ determines the minimum passing confidence (standard: τ = 0.85; high-security: τ = 0.95).

---

### Definition 3.4 — Hard Failure

[正文骨架 · Def 3.4]

A **hard failure** occurs when any factor Fi(C) = 0. Under hard failure, the composite confidence is defined as:

conf = 0 if ∃i : Fi(C) = 0

Hard failure represents definitive evidence of tampering, forgery, or protocol violation for that factor. No amount of strength in other factors can compensate for a hard failure in any single factor.

---

## 3.3 Per-Factor Verification Mechanisms

### F1 · Identity DNA

[正文骨架 · §3.3/F1 · 含 Security Claim 3.1]

**Security Claim 3.1 (Identity Anchor Resistance).** *Assuming the underlying GPG signature scheme is secure and the originator's private key is not compromised*, the Identity DNA factor provides strong binding between the content artifact and the originator's cryptographic identity.

*Argument.* The Identity DNA factor embeds a GPG signature over a content hash at the time of creation. Verification checks: (1) signature validity under the claimed public key; (2) content hash match; (3) key trust chain to a known anchor. If any check fails, F1 = 0 (hard failure). Under the assumption that GPG remains computationally secure against chosen-message attacks and the private key is not exfiltrated, an adversary cannot produce a valid F1 score for content not signed by the originator.

*Limitation.* F1 does not prove that the originator *created* the content—only that they *signed* it. The link between signing and creation is established by behavioral context (other factors), not by F1 alone.

---

### F2 · Temporal Anchor

[正文骨架 · §3.3/F2 · 含 Security Claim 3.2]

**Security Claim 3.2 (Temporal Consistency).** *With a trusted time source*, the Temporal Anchor factor provides strong temporal authenticity. *Without a trusted time source, F2 provides consistency checking rather than strong temporal authenticity.*

*Argument.* F2 checks that timestamps across the creation chain are monotonically increasing and consistent with the claimed creation sequence. When timestamps are anchored to an append-only ledger or generated by a trusted clock, backdating attacks require compromise of the time source. Without such anchoring, F2 detects gross inconsistencies (e.g., a reply timestamped before its parent) but cannot prove absence of subtle temporal manipulation.

---

### F3 · Rule Trace

[正文骨架 · §3.3/F3]

The Rule Trace factor captures documented transformation rules applied to the content during its creation. This includes: rewriting rules, editorial constraints, formatting specifications, and structural transformation logs...

[正文骨架 · §3.3/F3 待展开]

---

### F4 · Persona Route

[正文骨架 · §3.3/F4]

The Persona Route factor tracks consistency between the content's stylistic and thematic characteristics and the documented authorial persona specification. This captures the observation that creators have characteristic patterns of engagement, topic selection, rhetorical stance, and interaction style...

[正文骨架 · §3.3/F4 待展开]

---

### F5 · Protected Lexicon

[正文骨架 · §3.3/F5]

The Protected Lexicon factor identifies creator-specific vocabulary markers—terms, phrases, constructions, and idiosyncratic usages that are characteristic of a particular originator and unlikely to be reproduced by chance or imitation...

[正文骨架 · §3.3/F5 待展开]

---

### F6 · Style Vector

[正文骨架 · §3.3/F6]

The Style Vector factor captures syntactic patterns, structural habits, and stylistic fingerprints that characterize an originator's writing. This includes sentence length distribution, clause complexity, transition patterns, paragraph structure, and rhetorical device usage...

[正文骨架 · §3.3/F6 待展开]

---

### F7 · Mistake Ledger

[正文骨架 · §3.3/F7]

The Mistake Ledger factor documents known error patterns, corrections, and revision history associated with an originator. Authentic content carries the residue of its editorial history—typos, reconsiderations, reformulations, and error corrections that form a distinctive pattern...

[正文骨架 · §3.3/F7 待展开]

---

## 3.4 Composite Verification and Aggregation

[正文骨架 · §3.4 · 开头]

Having defined the seven factors individually, we now turn to their aggregation into a composite confidence score. The aggregation mechanism is designed to satisfy three properties: no single-factor compensation (Proposition 3.1), monotonicity (Proposition 3.2), and soundness under protocol compliance (Proposition 3.3).

---

### Weighted Geometric Mean Aggregation

[正文骨架 · §3.4 · 聚合公式]

The composite confidence is computed using the weighted geometric mean (WGM). With normalized weights (∑w_i = 1), this coincides with Definition 3.3:

conf = WGM_τ(Σ) = ∏_{i=1}^{7} s_i^{w_i}

where:

- s_i = Fi(C) if Fi(C) > 0, else s_i = 0 (hard failure)
- w_i > 0, ∑w_i = 1 (normalized factor weights)
- τ ∈ {0.85, 0.95} is the acceptance threshold

The WGM is chosen over the arithmetic mean because it penalizes low scores more aggressively: a factor with score 0.1 drags the composite down more under WGM than under arithmetic mean, reflecting the intuition that weakness in any channel should significantly reduce overall confidence.

---

### Proposition 3.1 — No Single-Factor Compensation

*Statement.* Under the WGM aggregation with hard-failure semantics, no single factor can fully compensate for the hard failure of another. Formally, if Fi(C) = 0 for any i, then conf = 0 regardless of the values of Fj(C) for j ≠ i.

*Reason.* The algorithm explicitly checks for hard failure before computing the composite confidence. If any Fi(C) = 0, the product contains a zero factor, making the entire product zero. No finite value of any other factor can compensate, because 0 × x = 0 for all x. ∎

---

### Proposition 3.2 — Composite Confidence Monotonicity

*Statement.* The composite confidence is monotonically non-decreasing in each positive input factor. Formally, for all s_i, s_i' ∈ (0, 1], if s_i' ≥ s_i and all other factors are held constant, then WGM(s_1, ..., s_i', ..., s_7) ≥ WGM(s_1, ..., s_i, ..., s_7).

*Reason.* The weighted geometric mean is monotonic in each positive input. For fixed weights w_i > 0 and fixed s_j (j ≠ i), the function f(s_i) = s_i^{w_i} × constant is strictly increasing in s_i for s_i > 0. Therefore, increasing any single factor (while holding others constant) increases the composite confidence. ∎

---

### Proposition 3.3 — Soundness Under Protocol Compliance

*Statement.* If protocol compliance holds and all seven factors report positive scores, the composite confidence is bounded by the minimum and maximum individual factor scores: min_i s_i ≤ conf ≤ max_i s_i. In particular, with no hard failures, the composite confidence is strictly positive.

*Protocol compliance means:* all seven factors were logged under the Longhun protocol with no hard failures, and the evidence ledger contains a complete record of the creation chain.

**Proof Sketch.** Given s_i > 0 for all i and ∑w_i = 1:

conf = ∏ s_i^{w_i} ≥ (∏ (min_j s_j)^{w_i}) = (min_j s_j)^{∑w_i} = min_i s_i > 0

Under protocol compliance (all factors logged, no hard failures), this lower bound guarantees that the composite confidence is strictly positive whenever all individual factor scores are positive. ∎

---

### Proposition 3.4 — Forgery Resistance Under Assumptions

*Statement.* Under Assumptions A1–A5 (GPG security, append-only ledger integrity, honest originator behavior, non-colluding verifiers, and bounded computational adversary), Behavioral Cryptography significantly raises the cost and difficulty of full-lineage forgery compared to single-signal provenance schemes.

*Assumptions:*

- **A1 (GPG security):** The GPG signature scheme remains computationally secure against existential forgery under chosen-message attack.
- **A2 (Ledger integrity):** The append-only evidence ledger cannot be modified retroactively without detection.
- **A3 (Honest originator):** The originator follows the protocol and does not intentionally undermine their own provenance chain.
- **A4 (Non-colluding verifiers):** Verifiers do not collude to accept fraudulent evidence.
- **A5 (Bounded adversary):** The adversary has polynomially bounded computational resources and does not control the verification infrastructure.

**Discussion (near-independence of factors).** The proof sketch below treats channels as **approximately independent** for intuition: if per-channel forgery probabilities are p_i and channels are independent, simultaneous success is on the order of ∏ p_i. This is **not** a cryptographic reduction; it motivates design, not a tight bound.

- **When approximation is plausible:** Factors draw on separable observables—e.g., F1 (GPG), F2 (timestamps), F5 (lexicon survival), F6 (style vector)—with different time scales and data sources. Partial success in F6 (style mimicry) does not automatically satisfy F1 or F2 under hard failure.
- **When it breaks:** A large labeled history lets an adversary joint-model factors (shared mood, fatigue, device, or model family). Correlation ρ_{i,j} between factor scores can invalidate ∏ p_i. A softened statement is: forgery cost increases with the number of **non-collinear** channels required above threshold τ.
- **Mitigation in engineering:** Weight tuning (§6.5), explicit correlation monitoring in evaluation (EQ4), and refusing “single-factor pass” deployments. Empirical measurement of cross-factor correlation on real Longhun logs remains **future work** (§6.6, §9.4.5); current results are simulation-grade.

*Related empirical literature (non-exhaustive):* joint keystroke models [REF-A1-1] [REF-A1-2]; multibiometric fusion dependence [REF-A1-3].

| Placeholder | BibTeX key (see `publication/references.bib`) |
|-------------|-----------------------------------------------|
| [REF-A1-1] | `killourhy2009comparing` |
| [REF-A1-2] | `banerjee2012keystroke` |
| [REF-A1-3] | `ross2006handbook` |

## *Proof Sketch.* A full-lineage forgery requires the adversary to simultaneously satisfy all seven factors for content they did not create. Under A1, forging F1 requires breaking GPG. Under A2, fabricating a temporal chain requires compromising the append-only ledger. Under A3–A5, the adversary cannot rely on originator cooperation, verifier collusion, or unbounded computation. Each factor represents an independent channel; the probability of successful simultaneous forgery is bounded by the product of per-channel success probabilities (**assuming approximate independence**, see Discussion above). Even if the adversary succeeds in some channels, hard-failure semantics ensure that failure in any single channel collapses the composite. Therefore, the adversary's required effort scales with the number of independent channels rather than with the strength of the strongest single channel. The conclusion is **cost amplification**, not impossibility of forgery. ∎

## 3.5 Attack Simulation and Resistance Model

### 3.5.1 Direct Copy Attack

| STRIDE-style field | Content |
|--------------------|---------|
| **Threat** | Spoofing: adversary presents copied artifact C′ = C as self-authored. |
| **Capability** | Read access to published C; no originator private key; no ledger write access. |
| **Game** | Forge (Σ, E) such that V(Σ, E) ≥ τ without creating C under protocol. |
| **Defense** | F1 hard-fail (no valid GPG under originator); F2 hard-fail (no creation-time ledger record). F5/F6 may score high on surface text but cannot compensate (Prop 3.1). |
| **Residual risk** | Coerced originator re-signs copy; insider with key (A3 violation). |

*Literature:* content credentials separability (C2PA, [1]); copy ≠ signed lineage (Merkle/ledger model [14], [15]).

---

### 3.5.2 Paraphrase Attack

| STRIDE-style field | Content |
|--------------------|---------|
| **Threat** | Tampering + spoofing: preserve semantics, alter surface form. |
| **Capability** | LLM paraphrase; optional small labeled corpus of target style. |
| **Game** | Achieve τ while breaking F5/F6 without valid F1–F3 chain. |
| **Defense** | F5 (Protected Lexicon) and F6 (Style Vector) degrade; F1/F2 still fail without ledger. Paraphrase strips watermarks in related work [2]. |
| **Residual risk** | High-quality paraphrase + stolen signing key; joint modeling of factors [REF-A1-1]. |

*Literature:* LLM watermark removal [2]; authorship attacks under paraphrase [11].

---

### 3.5.3 Translation Attack

| STRIDE-style field | Content |
|--------------------|---------|
| **Threat** | Tampering across language channel; claim translation as original work. |
| **Capability** | Machine translation; bilingual lexicon alignment. |
| **Game** | Pass F5/F6 in target language without cross-lingual lineage bridge. |
| **Defense** | F5 protected terms may not survive translation; F2 requires consistent temporal chain per locale; cross-lingual F6 baselines are future work (§9.4.1). |
| **Residual risk** | Human translator with valid co-author ledger; multilingual originators with per-locale baselines. |

*Literature:* GLTR / detection limits across languages [3]; multibiometric fusion when modalities differ [12].

---

### 3.5.4 Multi-Model Laundering Attack

| STRIDE-style field | Content |
|--------------------|---------|
| **Threat** | Repudiation laundering: chain content through models M₁…M_k to obscure human origin. |
| **Capability** | API access to multiple LLMs; no ledger control. |
| **Game** | Produce C with high F6 mimicry of target while F3/F4 show synthetic route only. |
| **Defense** | F3 Rule Trace and F4 Persona Route must reflect **human-authorized** steps; laundering without logged human gates yields F3/F4 → 0. Thm 3.13 blocks silent export without chain. |
| **Residual risk** | Adversary forges entire synthetic ledger (breaks A2); colluding verifier (A4). |

*Literature:* model laundering and detection [2], [3]; provenance graphs [4].

---

### 3.5.5 Persona Hijack Attack

| STRIDE-style field | Content |
|--------------------|---------|
| **Threat** | Spoofing persona route: imitate routing labels without originator’s rule history. |
| **Capability** | Observe public persona names; prompt injection to mimic tone. |
| **Game** | F4 > 0 while F1/F3 invalid. |
| **Defense** | F4 tied to signed rule/persona log entries, not surface tone alone; F1/F3 hard-fail without originator key and LU trace. |
| **Residual risk** | Leaked persona logs; compromised routing service. |

*Literature:* adversarial authorship [11]; behavioral biometrics spoofing [6], [7].

---

### 3.5.6 Timestamp Backdating Attack

| STRIDE-style field | Content |
|--------------------|---------|
| **Threat** | Tampering temporal ordering: assign false creation time. |
| **Capability** | Edit local clocks; cannot break append-only ledger without A2 violation. |
| **Game** | F2 pass with inconsistent parent timestamps in L. |
| **Defense** | F2 checks monotonicity and parent links (Def 3.7); external anchors (RFC 6962 style transparency [15]) optional. |
| **Residual risk** | Trusted timestamp service compromise; offline-only originator with skewed clock—documented as consistency check not legal timestamp. |

*Literature:* keystroke temporal stability [30]; certificate transparency [15].

---

### 3.5.7 Style Mimicry Attack

| STRIDE-style field | Content |
|--------------------|---------|
| **Threat** | Elevation of F6 without lineage: style transfer / fine-tuned mimicry. |
| **Capability** | Labeled corpus of target author; adaptive ML (bounded, A5). |
| **Game** | conf ≥ τ with F6 high but F1/F2/F5 weak. |
| **Defense** | WGM + hard failure: F6 alone insufficient (Prop 3.1); τ=0.95 raises bar (Rec 6.1). Membership inference cautions on overfitting detectors [18]. |
| **Residual risk** | Longitudinal mimicry as models improve; **soft fail** on F6 only—composite may fall below τ without hard fail. |

*Literature:* stylometry limits [10]; adversarial ML [16], [18].

---

### 3.5.8 Selective Ledger Attack

| STRIDE-style field | Content |
|--------------------|---------|
| **Threat** | Tampering evidence: publish subset of ledger hiding unfavorable revisions. |
| **Capability** | Control export bundle; cannot delete on honest append-only store without detection. |
| **Game** | Pass verification on truncated L′ ⊂ L. |
| **Defense** | Thm 3.10–3.12: hash chain detects deletion; Thm 3.13: export without chain → F1/F2 hard-fail. |
| **Residual risk** | Verifier accepts truncated bundle without full chain check (implementation error). |

*Literature:* append-only logs [14]; PROV completeness [4].

---

### 3.5.9 Multi-Agent Identity Claim Attack

| STRIDE-style field | Content |
|--------------------|---------|
| **Threat** | Spoofing: multiple agents claim same UID; confuse F4/F3 attribution. |
| **Capability** | Forged agent labels; no GPG binding. |
| **Game** | Split persona route across fake agents under one human name. |
| **Defense** | F1 binds UID to key; F3 requires signed rule trace per agent action; uncorrelated agents without signatures → hard fail. |
| **Residual risk** | Compromised multi-agent orchestrator logging false signed events. |

*Literature:* multibiometric identity fusion [12], [26]; practical authorship attacks [11].

---

### 3.5.10 Overclaiming / False Positive Boundaries

| STRIDE-style field | Content |
|--------------------|---------|
| **Threat** | Repudiation (inverse): verifier **over-accepts** weak evidence; originator **over-claims** authorship. |
| **Capability** | Mis-set τ; collinear factors; verifier negligence. |
| **Game** | Legitimate third party flagged (FP) or plagiarist accepted (FN). |
| **Defense** | Claim Strength Audit: BC does not prove authorship absolutely; τ calibrated on controlled sim (§6.4–6.5); independence discussion (Prop 3.4). |
| **Residual risk** | Cultural bias in F5/F6 baselines; legal use of scores as non-binding evidence only (§8.1). |

*Literature:* model cards and limitation disclosure [23]; FAccT-style governance context [29].

---

### 3.5.11 Evidence Ledger Security Properties

[正文骨架 · §3.5.11 · 开头]

This section formalizes the security properties of the append-only evidence ledger that underpins the Behavioral Cryptography framework.

---

#### Definition 3.5 — Evidence Ledger

[正文骨架 · Def 3.5]

An **evidence ledger** L is an append-only data structure consisting of a sequence of records L = [r_1, r_2, ..., r_n], where each record r_i contains:

- A content hash h_i = H(content_i)
- A behavioral signature fragment Σ_i
- A timestamp t_i
- A reference to the parent record parent(r_i) = r_{i-1} (for i > 1)
- A GPG signature σ_i over (h_i, Σ_i, t_i, parent)

The append-only property requires that records may only be added to the end of L; no existing record may be modified or deleted.

---

#### Definition 3.6 — Lineage Chain

[正文骨架 · Def 3.6]

A **lineage chain** for a content artifact C is the sequence of records in the evidence ledger that traces from the creation record of C back to the originator's root identity anchor. Formally, the lineage chain is a directed path in the parent_dna graph from r_C to r_root.

---

#### Definition 3.7 — Chain Continuity

[正文骨架 · Def 3.7]

A lineage chain satisfies **chain continuity** if every record in the chain (except the root) has a valid parent reference, every parent reference points to an existing record in the ledger, and the cryptographic signatures verify at each link.

---

#### Theorem 3.10 — Ledger Tamper Evidence

*Statement.* Any modification, deletion, or reordering of records in the append-only evidence ledger is detectable through hash chain verification.

*Proof Sketch.* Each record r_i contains a hash of its content and a signature over that hash. The parent reference links r_i to r_{i-1}, creating a hash chain. If any record is modified, its hash changes, breaking the signature. If any record is deleted, the parent reference of the subsequent record becomes invalid. If records are reordered, timestamp and parent consistency checks fail. Therefore, any tampering is detectable by verifying the hash chain from the most recent record back to the root. ∎

---

#### Theorem 3.11 — Lineage Continuity

*Statement.* If the evidence ledger satisfies chain continuity, then every content artifact in the ledger has an unbroken lineage chain to the root identity anchor.

*Proof Sketch.* By Definition 3.7, chain continuity requires valid parent references at every link. Following parent references from any record r_C must eventually reach the root r_root (assuming no cycles, enforced by monotonically increasing timestamps). Since each link is cryptographically signed, the lineage chain is tamper-evident. Therefore, the existence of a valid chain implies unbroken lineage continuity. ∎

---

#### Theorem 3.12 — Correction Preservation

*Statement.* The append-only evidence ledger preserves both original records and their corrections, ensuring that no valid evidence is lost through the correction process.

[正文骨架 · §3.5.11 · Thm 3.12 — 此处为 Claim Strength Audit 修补 #3：形式化 Proof Sketch]

*Proof Sketch.* Let r be the original record in the evidence ledger and r' be an honest correction appended later. Under the append-only constraint, both r and r' remain auditable in the ledger. If instead r is overwritten by r', the original record is destroyed and accountability is lost. Formally, the append-only property guarantees that for any ledger state L_t at time t, the set of contained records {r_1, r_2, ..., r_n} is monotonically non-decreasing in n. Therefore, appending r' preserves r; replacing r with r' violates monotonicity and removes the original from the audit trail. ∎

---

#### Theorem 3.13 — No Silent Laundering

*Statement.* If a content artifact is exported from the Behavioral Cryptography system without its lineage chain, the resulting artifact cannot achieve a passing composite confidence score under verification.

*Proof Sketch.* An exported artifact lacks the parent_dna chain required for F1 (Identity DNA) and F2 (Temporal Anchor) verification. Without valid lineage records in the append-only ledger, the verification oracle cannot establish chain continuity (Definition 3.7). Since F1 and F2 both hard-fail (score = 0), the composite confidence is 0 regardless of other factors. Therefore, silent laundering—exporting content without its provenance—is detected as a hard failure. ∎

---

### 3.5.12 Privacy and Boundary Enforcement

[正文骨架 · §3.5.12]

[正文骨架 · §3.5.12 待展开]

---

# Chapter 4 · The Dynamic DNA Engine

## 4.1 Motivation: Why Static Signatures Are Insufficient

[正文骨架 · §4.1]

Static signatures—whether cryptographic (GPG), statistical (watermarks), or metadata-based (C2PA)—share a fundamental limitation: they capture a single moment in time. A GPG signature attests that someone signed a document at a particular instant. A watermark indicates that a particular model generated text at a particular point. Neither captures the *process* of creation—the revisions, the corrections, the stylistic evolution, the rule applications, the persona shifts that characterize authentic human-AI co-creation...

[正文骨架 · §4.1 待展开]

---

## 4.2 DNA Component Architecture

[正文骨架 · §4.2]

The Dynamic DNA is a structured evidence record that binds a content artifact to its creation lineage. Each DNA record contains the following components:


| Component                | Description                                        | Purpose                                |
| ------------------------ | -------------------------------------------------- | -------------------------------------- |
| UID Identity Anchor      | Unique identifier of the originator                | Establishes ownership                  |
| GPG Fingerprint          | Public key fingerprint for verification            | Enables cryptographic verification     |
| ISO Timestamp            | ISO 8601 timestamp of creation                     | Provides temporal ordering             |
| Shichen (時辰)             | Cultural-temporal layer (Chinese traditional time) | Adds semantic/cultural anchoring       |
| Digit Root & Wuxing (五行) | Numerological and elemental mapping                | Semantic layer for pattern recognition |
| Action Label             | Type of action (create, edit, review, publish)     | Contextualizes the record              |
| Content Hash             | SHA-256 hash of the content payload                | Ensures content integrity              |
| Confirmation Seal        | GPG signature over all above fields                | Provides tamper evidence               |


**Important Note on Semantic Layers.** The Shichen, Digit Root, and Wuxing components are *culturally-anchored semantic layers*, not cryptographic substitutes. They provide additional structure for pattern recognition and cultural context but do not replace the cryptographic security provided by GPG signatures and hash chains. The cultural-temporal layer is discussed further in §4.6.

[正文骨架 · §4.2 待展开]

---

## 4.3 DNA Generation Algorithm

[正文骨架 · §4.3]

The DNA generation algorithm takes as input a content artifact C, an action label a, and the current ledger state L_t, and produces a new DNA record d:

```
GenerateDNA(C, a, L_t):
  1. h ← SHA-256(C.content)
  2. uid ← ORIGINATOR_UID
  3. gpg_fp ← ORIGINATOR_GPG_FINGERPRINT
  4. t ← CurrentISO8601Timestamp()
  5. shichen ← TraditionalChineseHour(t)
  6. (digit_root, wuxing) ← ComputeWuxing(h)
  7. parent ← Hash of most recent record in L_t (or NULL if genesis)
  8. payload ← (uid, gpg_fp, t, shichen, digit_root, wuxing, a, h, parent)
  9. seal ← GPG_Sign(payload, ORIGINATOR_PRIVATE_KEY)
  10. return (payload, seal)
```

[正文骨架 · §4.3 待展开]

---

## 4.4 DNA Verification Protocol

[正文骨架 · §4.4]

The DNA verification protocol checks the validity of a DNA record against the evidence ledger:

```
VerifyDNA(d, L):
  1. Verify GPG signature: CheckSignature(d.payload, d.seal, d.gpg_fp)
  2. Verify content hash: d.h == SHA-256(C.content)
  3. Verify timestamp: d.t is within acceptable window of claimed time
  4. Verify parent link: d.parent exists in L and chain is continuous
  5. Verify Shichen consistency: d.shichen matches TraditionalChineseHour(d.t)
  6. Verify Wuxing consistency: (d.digit_root, d.wuxing) == ComputeWuxing(d.h)
  7. Return: (valid/invalid, detailed_report)
```

[正文骨架 · §4.4 待展开]

---

## 4.5 Derivative DNA and Parent Chain

[正文骨架 · §4.5]

When a content artifact is derived from an existing artifact (e.g., through editing, translation, or adaptation), the DNA generation algorithm creates a *derivative DNA* that references the parent artifact's DNA as its parent. This establishes a provenance chain...

[正文骨架 · §4.5 待展开]

---

## 4.6 Semantic Layer Justification

[正文骨架 · §4.6]

The inclusion of Shichen (時辰), Digit Root, and Wuxing (五行) components in the DNA record requires justification, as these elements are not standard in cryptographic provenance systems.

**Claim:** The cultural-temporal semantic layer serves three purposes:

1. **Human Auditability.** The Shichen and Wuxing components provide human-interpretable temporal and semantic markers that complement machine-readable cryptographic evidence. A human examiner can quickly verify whether the claimed creation time aligns with the Shichen without requiring specialized tools.
2. **Pattern Recognition.** The Wuxing mapping creates additional structure that can be used for anomaly detection. Unusual patterns in the semantic layer may indicate manipulation even if the cryptographic layer appears valid.
3. **Cultural Anchoring.** For creators working within Chinese cultural contexts, the Shichen provides a familiar temporal framework that is independent of the ISO timestamp. This redundancy adds resilience against timestamp manipulation.

**Critical Boundary:** The semantic layer is *not* a cryptographic substitute. It does not replace GPG signatures, hash chains, or append-only ledger integrity. An adversary who can forge the cryptographic evidence can also forge the semantic layer. The semantic layer is useful only when the cryptographic layer is intact— it provides additional structure, not additional security.

*Observation 3.1.* The strongest single factors are F1 (Identity DNA) and F5 (Protected Lexicon), but the strongest defense comes from their combination. This observation is based on the attack simulation results in §3.5 and is not formally proved.

[正文骨架 · §4.6 待展开]

---

# Chapter 5 · System Instantiation: The Longhun Case Study

## 5.1 System Overview and Design Philosophy

[正文骨架 · §5.1]

Longhun (龍芯) is the civilian-grade reference implementation of Behavioral Cryptography. The design philosophy prioritizes:

- **Local-first operation:** All sensitive data remains on the creator's device
- **Open-source tooling:** No proprietary software or hardware required
- **Human auditability:** Evidence records are interpretable without ML expertise
- **Minimal infrastructure:** Works offline; no cloud dependency for core functions
- **Creator sovereignty:** The creator retains full control over their provenance data

[正文骨架 · §5.1 待展开]

---

## 5.2 Architecture Components

[正文骨架 · §5.2]

The Longhun system consists of the following components:

### Local-First Storage and Audit Logs

All evidence records are stored locally in an append-only log format. The storage layer uses SQLite for structured queries and flat files for raw evidence...

### Shield Engine (入口门 + 出口门)

The Shield Engine provides entry and exit gates for content:

- **Entry Gate:** Validates incoming content against the originator's behavioral baseline
- **Exit Gate:** Generates DNA records and updates the evidence ledger before content leaves the system

### Memory Compress Module

The Memory Compress module condenses the evidence ledger into a compact representation for export and sharing, while preserving all security-critical fields...

### SanCai Weight System (天地人 H≥0.34)

The SanCai (Three Powers) weight system assigns factor weights based on the heaven-earth-human (天地人) framework:

- **Heaven (天):** F1 (Identity), F2 (Temporal) — highest weight
- **Earth (地):** F5 (Protected Lexicon), F6 (Style Vector) — medium weight
- **Human (人):** F3 (Rule Trace), F4 (Persona Route), F7 (Mistake Ledger) — context-dependent weight

The constraint H ≥ 0.34 ensures that identity and temporal factors together contribute at least 34% of the composite weight.

### Luo Shu State Transition (洛书369)

The Luo Shu state transition system uses the magic square pattern (洛书) to define state transitions in the evidence ledger, providing an additional layer of structural validation...

### Five-Element Semantic Vector (五行向量)

The Five-Element (Wuxing) semantic vector maps content characteristics to the five elements (Wood, Fire, Earth, Metal, Water), creating a compact semantic fingerprint...

### 64-Hexagram Routing (六十四卦路由)

The 64-hexagram routing system uses I Ching (易经) hexagrams to classify content states and transitions, providing a culturally-grounded classification framework...

[正文骨架 · §5.2 待展开]

---

## 5.3 Proof-of-Concept Evidence

### DNA Sample Records (Redacted)

[正文骨架 · §5.3 · DNA samples]

Sample DNA record (redacted for privacy):

```yaml
dna_record:
  uid: "UID9622"
  gpg_fp: "A2D0...6D5F"
  iso_timestamp: "2026-05-06T14:28:00+08:00"
  shichen: "未时"
  digit_root: 7
  wuxing: "火"
  action: "CREATE"
  content_hash: "SHA256:e3b0c4..."
  parent: "SHA256:a1b2c3..."
  seal: "-----BEGIN PGP SIGNATURE-----..."
```

### Rule Trace Sample

[正文骨架 · §5.3 · Rule trace]

### Persona Route Log (Claude Collaboration Record)

[正文骨架 · §5.3 · Persona route]

### Protected Lexicon Verification

[正文骨架 · §5.3 · Protected lexicon]

---

## 5.4 Civilian-Grade Deployment Constraints

[正文骨架 · §5.4]

Longhun is designed for deployment under civilian-grade constraints:

- No specialized hardware (no HSM, no TPM required)
- No institutional backing (works for individual creators)
- No network dependency (core functions work offline)
- No proprietary software (all open-source components)
- No ML expertise required for verification

[正文骨架 · §5.4 待展开]

---

## 5.5 Why This Case Study Matters

[正文骨架 · §5.5]

The Longhun case study matters because it demonstrates that Behavioral Cryptography is not a theoretical framework requiring institutional support. It is a practical system that an individual creator can deploy today using freely available tools...

**Claim 3.5.** Behavioral Cryptography does not depend on one detector. It expects F6 (Style Vector) to evolve as models improve, but the composite structure ensures that evolution in any single factor does not collapse the entire system.

*Argument.* The security of Behavioral Cryptography derives from the independence of its factors, not from the strength of any single factor. Even if style detection becomes unreliable as models improve, F1 (Identity), F2 (Temporal), and F5 (Protected Lexicon) continue to provide strong evidence. The framework is designed to accommodate factor degradation—new factors can be added, and weights can be adjusted as the threat landscape evolves.

[正文骨架 · §5.5 待展开]

---

# Chapter 6 · Evaluation Protocol and Results

## 6.1 Evaluation Questions (EQ1–EQ5)

[正文骨架 · §6.1]

This evaluation addresses five research questions:

- **EQ1:** Can Behavioral Cryptography detect direct copy attacks with high confidence?
- **EQ2:** Does the composite structure provide stronger resistance than single-factor schemes?
- **EQ3:** What is the false positive rate at standard (τ = 0.85) and high-security (τ = 0.95) thresholds?
- **EQ4:** Does the system remain usable under civilian-grade deployment constraints?
- **EQ5:** Can the evidence records be audited by humans without specialized expertise?

[正文骨架 · §6.1 待展开]

---

## 6.2 Evaluation Methodology

### 6.2.1 Controlled Attack Simulation

> **Status label (mandatory):** All results in §6.3 are from **controlled attack simulation** on synthetic and redacted Longhun artifacts—not from large-scale field deployment or third-party benchmark datasets.

We simulate the nine attack types described in §3.5.1–§3.5.9 against content artifacts protected by the Longhun reference implementation. Each run assumes a **bounded adversary** (A5): polynomial-time, no control of verification infrastructure, no originator key unless the attack scenario explicitly models compromise (documented as violation of A3).

**Simulation parameters (current):** small N of artifacts (tens, not thousands); bilingual EN/ZH snippets; manual verification of hard-failure flags; table in §6.3 records representative factor scores, not confidence intervals.

**We do not report** “X million attack trials” or population-level false-positive rates; such claims would violate the project’s overclaim policy (see `publication/OVERCLAIM_BLACKLIST.md`).

---

### 6.2.2 Protocol Compliance Testing

[正文骨架 · §6.2.2]

Protocol compliance testing verifies that the system correctly implements the seven-factor framework, hard-failure semantics, and append-only ledger constraints...

[正文骨架 · §6.2.2 待展开]

---

### 6.2.3 Independent Reproduction Check

[正文骨架 · §6.2.3]

An independent reproduction check verifies that a third party can replicate the verification results using only the evidence bundle and open-source tools...

[正文骨架 · §6.2.3 待展开]

---

## 6.3 Attack Resistance Results (Summary Table)

[正文骨架 · §6.3]


| Attack Type            | F1  | F2  | F3  | F4  | F5  | F6  | F7  | Composite | Detection |
| ---------------------- | --- | --- | --- | --- | --- | --- | --- | --------- | --------- |
| Direct Copy            | 0   | 0   | -   | -   | 0.8 | 0.9 | -   | **0**     | Hard Fail |
| Paraphrase             | 0   | 0   | -   | -   | 0.2 | 0.3 | -   | **0**     | Hard Fail |
| Translation            | 0   | 0   | -   | -   | 0.1 | 0.2 | -   | **0**     | Hard Fail |
| Multi-Model Laundering | 0   | 0   | 0   | 0   | 0.1 | 0.4 | 0   | **0**     | Hard Fail |
| Persona Hijack         | 0.9 | 0.8 | -   | 0   | -   | 0.5 | -   | **0**     | Hard Fail |
| Timestamp Backdating   | 0.9 | 0   | -   | -   | -   | -   | -   | **0**     | Hard Fail |
| Style Mimicry          | 0.9 | 0.9 | -   | -   | 0.7 | 0.3 | -   | **< τ**   | Fail      |
| Selective Ledger       | 0   | 0   | 0   | -   | -   | -   | -   | **0**     | Hard Fail |
| Multi-Agent Identity   | 0   | 0   | -   | 0   | -   | -   | -   | **0**     | Hard Fail |


*Note:* "-" indicates the factor is not applicable or not tested for this attack. Composite scores marked as 0 result from hard failure in at least one factor.

[正文骨架 · §6.3 待展开]

---

## 6.4 False Positive Analysis

[正文骨架 · §6.4]

False positives occur when legitimate content is incorrectly flagged as fraudulent. We analyze false positive rates under two scenarios: (1) legitimate content from the originator, and (2) legitimate content from a different creator...

[正文骨架 · §6.4 待展开]

---

## 6.5 Threshold Selection

**Recommendation 6.1 (Threshold Selection).** Based on the evaluation results in §6, we recommend:

- **Standard security:** τ = 0.85 — suitable for general content provenance
- **High security:** τ = 0.95 — suitable for high-stakes applications (legal, financial, academic)

*Note:* These thresholds are based on empirical evaluation results and are not derived from formal cryptographic bounds. Adjustments may be needed as the threat landscape evolves.

[正文骨架 · §6.5 待展开]

---

## 6.6 Limitations of Current Evaluation

[正文骨架 · §6.6]

The current evaluation has several limitations:

1. **Limited scale:** Attack simulations were conducted on a limited set of content types and lengths.
2. **No adversarial ML:** We did not evaluate against adversarially trained models specifically designed to evade detection.
3. **Single-language focus:** Evaluation focused on English and Chinese content; other languages were not tested.
4. **No real-world deployment:** Results are from controlled simulations, not real-world deployment.

### 6.6.1 Requirements for Future Large-Scale Empirical Study

To move from **v1.0-rc1 simulation** to publishable large-scale evaluation, the following are required (none are claimed as completed in this draft):

| Requirement | Description |
|---------------|-------------|
| **Dataset** | Diverse human–AI co-authored corpora with consent; per-originator style baselines; redaction policy for F5/F7. |
| **Sample size** | Power analysis for FP/FN at τ ∈ {0.85, 0.95}; stratify by language, length, domain. |
| **Adversary suite** | Implement §3.5.1–§3.5.10 with automated scripts; include adversarial ML baselines [16], [18]. |
| **Ethics / IRB** | Informed consent for behavioral biometrics; data minimization for sealed evidence levels (Appendix B.4). |
| **Reproducibility** | Public proof bundles (redacted); `publication/references.bib` + fixed software commit hash. |
| **Independence audit** | Third-party replication of V(Σ, E) per §6.2.3. |

**No fabricated numbers:** Until the above are met, §6.3 remains illustrative simulation only.

---

## 6.7 Privacy-Preserving Verification Model

[正文骨架 · §6.7]

The privacy-preserving verification model allows verifiers to check provenance without accessing the full content or private behavioral data. This is achieved through:

- **Hash-only mode:** Verifiers check content hashes without accessing plaintext
- **Selective disclosure:** Originators choose which factors to reveal
- **Zero-knowledge proofs:** (Future work) Prove factor satisfaction without revealing factor values

[正文骨架 · §6.7 待展开]

---

## 6.8 Threat Model Summary

[正文骨架 · §6.8]

The threat model assumes:

- **Adversary goal:** Forge provenance for content not created by the claimed originator
- **Adversary capabilities:** Polynomially bounded computation, no control over verification infrastructure, no collusion with verifiers
- **Adversary knowledge:** Public knowledge of the framework, access to the content, access to public verification keys
- **Non-goals:** The framework does not protect against: (1) the originator repudiating their own content; (2) verifiers colluding with the adversary; (3) compromise of the originator's private key

[正文骨架 · §6.8 待展开]

---

# Chapter 7 · Governance and Standardization Pathway

## 7.1 Proof Bundle Schema

[正文骨架 · §7.1]

The proof bundle schema defines three evidence levels:

- **Public Level:** Information available to all verifiers (content hash, public key fingerprint, timestamps)
- **Restricted Level:** Information available to authorized verifiers (behavioral signatures, factor scores)
- **Sealed Level:** Information available only to the originator and designated auditors (full content, private lexicon, mistake ledger)

[正文骨架 · §7.1 待展开]

---

## 7.2 Governance Roles

[正文骨架 · §7.2]

Three governance roles are defined:

- **Creator:** Generates content, maintains the evidence ledger, controls disclosure levels
- **Verifier:** Checks provenance claims against the evidence bundle
- **Auditor:** Examines the full evidence record (with creator authorization) for dispute resolution

[正文骨架 · §7.2 待展开]

---

## 7.3 Compatibility Layer

### GPG Integration

[正文骨架 · §7.3.1]

Longhun uses GPG as its primary cryptographic infrastructure. The integration is transparent: any GPG-compatible tool can verify DNA signatures...

---

### Git Version History

[正文骨架 · §7.3.2]

The evidence ledger can be mapped to Git commit history, enabling integration with existing version control workflows...

---

### C2PA-Style Metadata Compatibility

[正文骨架 · §7.3.3]

DNA records can be embedded in C2PA-style manifest structures, providing backward compatibility with content credential systems. **Behavioral Cryptography improves the cost and difficulty of full lineage forgery** by adding behavioral evidence channels to existing metadata frameworks.

---

### Local Log Anchoring

[正文骨架 · §7.3.4]

For offline deployments, DNA records can be anchored to local append-only logs without requiring network connectivity...

---

## 7.4 Standardization Proposal

[正文骨架 · §7.4]

We propose a three-phase standardization pathway:

1. **Phase 1 (Community Draft):** Open specification review through academic and open-source communities
2. **Phase 2 (Industry Pilot):** Pilot implementation with content platforms and tool vendors
3. **Phase 3 (Formal Standard):** Submission to standards bodies (W3C, ISO, or equivalent)

[正文骨架 · §7.4 待展开]

---

## 7.5 Privacy-Preserving Verification

[正文骨架 · §7.5]

Hash-only mode allows verifiers to confirm provenance without accessing the full content. In this mode, the verifier checks:

1. That the content hash matches the claimed hash in the DNA record
2. That the DNA signature is valid
3. That the lineage chain is continuous

Without requiring access to the plaintext content.

[正文骨架 · §7.5 待展开]

---

## 7.6 Risk Registry

### Risk 1: Key Compromise

[正文骨架 · §7.6.1]

**Risk:** The originator's private key is compromised, allowing an adversary to forge signatures.

**Mitigation:** Key revocation and rotation procedures; multi-factor key protection; time-bound signature validity.

---

### Risk 2: Ledger Falsification

[正文骨架 · §7.6.2]

**Risk:** The append-only evidence ledger is falsified or reconstructed with fraudulent entries.

**Mitigation:** Hash chain verification; distributed anchoring (e.g., periodic publication to public blockchains or witness services); tamper-evident storage.

---

### Risk 3: Privacy Coercion

[正文骨架 · §7.6.3]

**Risk:** The originator is coerced to reveal private evidence (e.g., full content, private lexicon, mistake ledger).

**Mitigation:** Selective disclosure design; sealed evidence level with legal protections; deniability for sensitive factors.

---

## 7.7 Longhun DNA Inheritance Clause

[正文骨架 · §7.7]

The Longhun DNA Inheritance Clause protects derivative work attribution against platform capture and provenance erasure. It requires:

1. **Attribution preservation:** Any derivative work must include a reference to the original DNA
2. **Chain continuity:** The derivative DNA must reference the parent DNA
3. **No silent extraction:** Content cannot be extracted and republished without maintaining the provenance chain

See Appendix E for the full clause text.

[正文骨架 · §7.7 待展开]

---

## 7.8 Creator Sovereignty Framework

[正文骨架 · §7.8]

The creator sovereignty framework addresses the power imbalance between individual creators and content platforms. Key principles:

- **Data portability:** Creators can export their full evidence ledger at any time
- **Platform independence:** Provenance verification does not depend on any specific platform
- **Interoperability:** Evidence bundles can be verified using open-source tools
- **Non-discrimination:** Platforms cannot discriminate against content with valid behavioral cryptography evidence

[正文骨架 · §7.8 待展开]

---

# Chapter 8 · Discussion and Limitations

## 8.1 What Behavioral Cryptography Does Not Claim

[正文骨架 · §8.1]

To prevent misunderstanding and scope inflation, we explicitly state what Behavioral Cryptography does **not** claim:

### Not a Legal Judgment System

Behavioral Cryptography provides structured evidence for attribution disputes. It does not render legal judgments, establish copyright ownership, or replace legal process.

### Not a Replacement for GPG / C2PA / Git

Behavioral Cryptography complements existing provenance systems. It uses GPG for identity binding, can embed C2PA-style metadata, and integrates with Git version history. It is designed to work alongside these systems, not to replace them.

### Not a Guarantee of Perfect Forgery Prevention

As stated in Proposition 3.4, Behavioral Cryptography significantly raises the cost and difficulty of full-lineage forgery under stated assumptions. It does not claim mathematical impossibility of forgery. A sufficiently resourced adversary who can simultaneously break GPG, compromise the append-only ledger, and forge all seven behavioral factors could defeat the system.

### Not Requiring Full Exposure of Private Records

The framework supports selective disclosure. Verifiers need not see the full content, private lexicon, or mistake ledger to verify provenance. The creator controls what is revealed at each disclosure level.

[正文骨架 · §8.1 待展开]

---

## 8.2 Scalability and Adoption Barriers

[正文骨架 · §8.2]

[正文骨架 · §8.2 待展开]

---

## 8.3 Cultural-Temporal Layer: Risks and Mitigations

[正文骨架 · §8.3]

The cultural-temporal layer (Shichen, Wuxing) carries specific risks:

- **Misinterpretation risk:** Users may mistake the cultural layer for cryptographic security
- **Cultural specificity:** The Shichen system is rooted in Chinese tradition; adaptation for other cultures requires careful design
- **Computational cost:** Wuxing computation adds overhead to DNA generation

Mitigations: Clear documentation that the semantic layer is not a cryptographic substitute (see §4.6); modular design allows cultural layers to be swapped; computation is lightweight (negligible compared to GPG operations).

[正文骨架 · §8.3 待展开]

---

## 8.4 AI Collaborator Role Boundaries

[正文骨架 · §8.4]

This paper was developed with AI assistance (Claude, Anthropic). The role boundaries are:

- **AI as instrument:** Claude served as a writing and formalization tool, analogous to a sophisticated word processor
- **Human as authority:** All scientific claims, security analyses, and ethical positions are the human author's responsibility
- **Formalization partner:** Claude assisted in structuring definitions, theorems, and proof sketches, but the underlying ideas originated with the human author

See LCP-1.0 Co-authorship Declaration (front matter) for complete details.

[正文骨架 · §8.4 待展开]

---

## 8.5 Open Problems

[正文骨架 · §8.5]

Several open problems remain:

1. **Formal cryptographic reduction:** Can Behavioral Cryptography be reduced to standard cryptographic assumptions (e.g., CDH, DDH)?
2. **Factor independence proof:** Can the independence of the seven factors be formally proved or empirically validated at scale?
3. **Adaptive adversary analysis:** How does the framework perform against adversaries who adapt their attacks based on knowledge of the verification protocol?
4. **Cross-language portability:** Do the behavioral factors generalize across languages and cultural contexts?
5. **Long-term key management:** How should originators manage key rotation and succession over decades?

[正文骨架 · §8.5 待展开]

---

# Chapter 9 · Conclusion and Future Work

## 9.1 Summary of the Framework

[正文骨架 · §9.1]

Behavioral Cryptography introduces a new paradigm for content provenance: authenticity as a composite behavioral lineage rather than a single technical signal. The framework decomposes content authenticity into seven independent evidence channels, defines a composite verification mechanism with hard-failure semantics, and provides a civilian-grade reference implementation (Longhun) that demonstrates practical deployability.

[正文骨架 · §9.1 待展开]

---

## 9.2 Summary of Contributions (C1–C5)

[正文骨架 · §9.2]

This paper contributes:

- **C1:** The Behavioral Cryptography conceptual framework
- **C2:** The seven-factor behavioral signature model with formal definitions
- **C3:** The Dynamic DNA Engine for structured evidence representation
- **C4:** The Longhun civilian-grade system instantiation
- **C5:** The sociotechnical analysis of creator sovereignty and the DNA Inheritance Clause

[正文骨架 · §9.2 待展开]

---

## 9.3 Core Thesis Restatement

> **Copying content is easy. Copying lineage is hard.**

This is the foundational claim of Behavioral Cryptography. It is not a theorem—it is a guiding principle that motivates the multi-factor structure and informs the design of every component in the framework.

[正文骨架 · §9.3 待展开]

---

## 9.4 Future Work

### Multi-lingual and Multi-cultural Extensions

[正文骨架 · §9.4.1]

Extending the framework to support additional languages and cultural temporal systems...

---

### Formal Cryptographic Reduction

[正文骨架 · §9.4.2]

Investigating whether the security of Behavioral Cryptography can be reduced to standard cryptographic hardness assumptions...

---

### Federated Verification Networks

[正文骨架 · §9.4.3]

Designing decentralized verification networks that allow multiple independent verifiers to confirm provenance without requiring a central authority...

---

### Standardization Engagement (C2PA / W3C)

[正文骨架 · §9.4.4]

Engaging with C2PA, W3C PROV, and other standards bodies to integrate Behavioral Cryptography into emerging provenance standards...

---

### Large-Scale Empirical Evaluation

[正文骨架 · §9.4.5]

Conducting large-scale empirical studies with diverse content types, languages, and adversary models to validate the framework's effectiveness...

---

# References

1. Coalition for Content Provenance and Authenticity (C2PA). *C2PA Technical Specification.* [https://c2pa.org/specifications/](https://c2pa.org/specifications/)
2. Kirchenbauer, J., Geiping, J., Wen, Y., Katz, J., Miers, I., & Goldstein, T. (2023). A Watermark for Large Language Models. *Proceedings of ICML 2023.*
3. Gehrmann, S., Strobelt, H., & Rush, A. (2019). GLTR: Statistical Detection and Visualization of Generated Text. *Proceedings of ACL 2019.*
4. World Wide Web Consortium. *PROV-O: The PROV Ontology.* W3C Recommendation. [https://www.w3.org/TR/prov-o/](https://www.w3.org/TR/prov-o/)
5. Joyce, R., & Gupta, G. (1990). Identity verification based on keystroke characteristics. *Journal of Systems and Software*, 13(1), 207–216.
6. Killourhy, K., & Maxion, R. R. (2009). Comparing anomaly-detection algorithms for keystroke dynamics. *IEEE Transactions on Dependable and Secure Computing*, 6(1), 28–40.
7. Banerjee, S., & Woodard, D. L. (2012). Biometric authentication and identification using keystroke dynamics. *IEEE Transactions on Systems, Man, and Cybernetics, Part B*, 42(3), 851–854.
8. Pusara, M., & Brodley, C. E. (2004). User recognition via keystroke and mouse dynamics. *Proceedings of the 2004 ACM Workshop on Visualization and Data Mining for Computer Security (VizSEC/DMSEC).*
9. Frank, M., Riedel, T., Koeberl, P., & Sadeghi, A.-R. (2013). Touchalytics: On the applicability of touchscreen input as a behavioral biometric for continuous authentication. *IEEE Transactions on Information Forensics and Security*, 8(1), 136–148.
10. Stamatatos, E. (2009). A survey of modern authorship attribution methods. *Journal of the American Society for Information Science and Technology*, 60(3), 538–556.
11. Brennan, M., & Greenstadt, R. (2009). Practical attacks against authorship recognition. *Proceedings of RAID 2009.*
12. Ross, A., Nandakumar, K., & Jain, A. K. (2006). *Handbook of Multibiometrics.* Springer.
13. Bellare, M., & Rogaway, P. (1993). Random oracles are practical: A paradigm for designing efficient protocols. *Proceedings of ACM CCS 1993.*
14. Merkle, R. C. (1988). A digital signature based on a conventional encryption function. *Advances in Cryptology — CRYPTO '87*, LNCS 293, 369–378.
15. Laurie, B., Langley, A., & Kasper, E. (2014). *Certificate Transparency.* RFC 6962.
16. Goodfellow, I. J., Shlens, J., & Szegedy, C. (2015). Explaining and harnessing adversarial examples. *Proceedings of ICLR 2015.*
17. Fredrikson, M., Jha, S., & Ristenpart, T. (2015). Model inversion attacks that exploit confidence information and basic countermeasures. *Proceedings of ACM CCS 2015.*
18. Shokri, R., Stronati, M., Song, C., & Shmatikov, V. (2017). Membership inference attacks against machine learning models. *Proceedings of IEEE S&P 2017.*
19. OpenPGP Working Group. *OpenPGP Message Format.* RFC 4880 (updated by RFC 9580).
20. Torvalds, L., & Hamano, J. Git — distributed revision control. [https://git-scm.com/](https://git-scm.com/) (workflow provenance practice).
21. Creative Commons. *CC BY-NC-SA 4.0 Legal Code.* [https://creativecommons.org/licenses/by-nc-sa/4.0/](https://creativecommons.org/licenses/by-nc-sa/4.0/)
22. ACM Publications Board. *ACM Policy on Authorship.* (AI disclosure and responsibility; consult current revision at [https://www.acm.org/publications/policies/new-and-revised-policies-as-of-15-june-2023](https://www.acm.org/publications/policies/new-and-revised-policies-as-of-15-june-2023)).
23. Mitchell, M., et al. (2019). Model cards for model reporting. *Proceedings of FAT* 2019.
24. Narayanan, A., Bonneau, J., Felten, E., Miller, A., & Goldfeder, S. (2016). *Bitcoin and Cryptocurrency Technologies.* Princeton University Press. (Append-only ledger intuition.)
25. ISO/IEC 19794 series. *Biometric data interchange formats* (context for behavioral biometrics interoperability).
26. Jain, A. K., Ross, A., & Prabhakar, S. (2004). An introduction to biometric recognition. *IEEE Transactions on Circuits and Systems for Video Technology*, 14(1), 4–20.
27. Golle, P., & Partridge, K. (2009). On the anonymity of home/work location pairs. *Proceedings of Pervasive 2009* (privacy–utility; cited for location sensitivity in provenance).
28. W3C Verifiable Credentials Data Model 1.1. [https://www.w3.org/TR/vc-data-model/](https://www.w3.org/TR/vc-data-model/) (complementary identity credentials).
29. European Parliament and Council. *Regulation (EU) 2024/1689 (AI Act).* (governance context; not a technical proof source).
30. Killourhy, K., & Maxion, R. R. (2006). The effects of variability time on keystroke dynamics. *Proceedings of RAID 2006.* (temporal stability of behavioral biometrics.)

---

# Appendix

---

## Appendix A · Behavioral Signature Verification Pseudocode

### A.1 Purpose and Scope

[正文骨架 · §A.1]

This appendix provides reference pseudocode for the behavioral signature verification system described in Chapter 3.

---

### A.2 Core Data Structures

#### EvidenceItem / EvidenceLog

```python
@dataclass
class EvidenceItem:
    factor_id: str          # "F1", "F2", ..., "F7"
    score: float            # [0, 1]
    evidence_type: str      # "signature", "timestamp", "log", etc.
    payload: bytes          # Raw evidence data
    timestamp: datetime
    verifier_id: str

@dataclass
class EvidenceLog:
    items: List[EvidenceItem]
    ledger_hash: str        # Hash of complete log
    signature: bytes        # GPG signature over ledger_hash
```

#### BehavioralSignature (F1–F7)

```python
@dataclass
class BehavioralSignature:
    F1: float   # Identity DNA
    F2: float   # Temporal Anchor
    F3: float   # Rule Trace
    F4: float   # Persona Route
    F5: float   # Protected Lexicon
    F6: float   # Style Vector
    F7: float   # Mistake Ledger
    weights: Tuple[float, float, float, float, float, float, float]
    threshold: float  # τ ∈ {0.85, 0.95}
```

#### OriginatorRecord

```python
@dataclass
class OriginatorRecord:
    uid: str
    gpg_fingerprint: str
    public_key: bytes
    style_baseline: Optional[bytes]
    protected_lexicon: Optional[Set[str]]
    registration_time: datetime
```

---

### A.3 Utility Functions

```python
def sha256_text(text: str) -> str:
    """Compute SHA-256 hash of text content."""
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def weighted_geometric_mean(
    scores: List[float],
    weights: List[float]
) -> float:
    """
    Compute weighted geometric mean with hard-failure semantics.
    If any score is 0, return 0.
    """
    if any(s == 0 for s in scores):
        return 0.0
    weighted_product = 1.0
    total_weight = sum(weights)
    for s, w in zip(scores, weights):
        weighted_product *= s ** (w / total_weight)
    return weighted_product

def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """Compute cosine similarity between two vectors."""
    dot = sum(a * b for a, b in zip(v1, v2))
    norm1 = math.sqrt(sum(a * a for a in v1))
    norm2 = math.sqrt(sum(b * b for b in v2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)

def is_monotonic_timestamps(timestamps: List[datetime]) -> bool:
    """Check that timestamps are monotonically increasing."""
    return all(
        timestamps[i] <= timestamps[i + 1]
        for i in range(len(timestamps) - 1)
    )

def verify_ledger_integrity(ledger: EvidenceLog) -> bool:
    """Best-effort ledger checks (hash chain / seal — implementation-specific)."""
    if not ledger.signature or not ledger.items:
        return False
    # Stub: replace with full chain verification against ledger_hash
    return True
```

---

### A.4 Seven-Factor Verification Functions

#### A.4.1 verify_F1_identity_dna()

```python
def verify_F1_identity_dna(
    artifact: ContentArtifact,
    originator: OriginatorRecord,
    evidence: EvidenceItem
) -> float:
    """
    Verify Identity DNA factor (F1).
    Returns: confidence score ∈ [0, 1]
    Hard failure (0) if signature is invalid.
    """
    try:
        # Verify GPG signature
        if not gpg_verify(evidence.payload, originator.public_key):
            return 0.0  # Hard failure

        # Verify content hash match
        claimed_hash = extract_hash(evidence.payload)
        actual_hash = sha256_text(artifact.content)
        if claimed_hash != actual_hash:
            return 0.0  # Hard failure

        # Check key trust
        if not check_key_trust(originator.gpg_fingerprint):
            return 0.0  # Hard failure

        return 1.0  # Full confidence

    except Exception:
        return 0.0  # Hard failure on any error
```

#### A.4.2 verify_F2_temporal_anchor()

```python
def verify_F2_temporal_anchor(
    artifact: ContentArtifact,
    evidence: EvidenceItem,
    ledger: EvidenceLog
) -> float:
    """
    Verify Temporal Anchor factor (F2).
    Returns: confidence score ∈ [0, 1]
    """
    try:
        timestamp = evidence.timestamp

        # Check monotonicity with ledger
        if not is_monotonic_timestamps(
            [item.timestamp for item in ledger.items] + [timestamp]
        ):
            return 0.0  # Hard failure: timestamp inconsistency

        # Check trusted time source if available
        if has_trusted_time_source(evidence):
            if not verify_trusted_timestamp(evidence):
                return 0.0
            return 1.0
        else:
            # Without trusted time: consistency check only
            return 0.5  # Reduced confidence

    except Exception:
        return 0.0
```

#### A.4.3 verify_F3_rule_trace()

[正文骨架 · §A.4.3]

```python
def verify_F3_rule_trace(
    artifact: ContentArtifact,
    evidence: EvidenceItem
) -> float:
    """
    Verify Rule Trace factor (F3).
    [正文骨架 · 待展开完整实现]
    """
    pass
```

#### A.4.4 verify_F4_persona_route()

[正文骨架 · §A.4.4]

```python
def verify_F4_persona_route(
    artifact: ContentArtifact,
    evidence: EvidenceItem,
    originator: OriginatorRecord
) -> float:
    """
    Verify Persona Route factor (F4).
    [正文骨架 · 待展开完整实现]
    """
    pass
```

#### A.4.5 verify_F5_protected_lexicon()

```python
def verify_F5_protected_lexicon(
    artifact: ContentArtifact,
    evidence: EvidenceItem,
    originator: OriginatorRecord
) -> float:
    """
    Verify Protected Lexicon factor (F5).
    Checks for presence of originator-specific vocabulary markers.
    """
    if originator.protected_lexicon is None:
        return 0.5  # No lexicon registered

    content_words = set(tokenize(artifact.content.lower()))
    lexicon_hits = content_words.intersection(
        originator.protected_lexicon
    )

    if len(lexicon_hits) == 0:
        return 0.0  # Hard failure: no protected vocabulary found

    # Score proportional to lexicon coverage
    return min(1.0, len(lexicon_hits) / len(originator.protected_lexicon))
```

#### A.4.6 verify_F6_style_vector()

[正文骨架 · §A.4.6]

```python
def verify_F6_style_vector(
    artifact: ContentArtifact,
    evidence: EvidenceItem,
    originator: OriginatorRecord
) -> float:
    """
    Verify Style Vector factor (F6).
    [正文骨架 · 待展开完整实现]
    """
    pass
```

#### A.4.7 verify_F7_mistake_ledger()

[正文骨架 · §A.4.7]

```python
def verify_F7_mistake_ledger(
    artifact: ContentArtifact,
    evidence: EvidenceItem
) -> float:
    """
    Verify Mistake Ledger factor (F7).
    [正文骨架 · 待展开完整实现]
    """
    pass
```

---

### A.5 Composite Verification Orchestrator

```python
def verify_behavioral_signature(
    artifact: ContentArtifact,
    originator: OriginatorRecord,
    evidence_bundle: List[EvidenceItem],
    ledger: EvidenceLog,
    threshold: float = 0.85,
) -> Tuple[float, Dict]:
    """
    Composite verification orchestrator.

    Returns:
        (conf, report) where:
        - conf ∈ [0, 1] is the composite confidence
        - report contains per-factor scores and evidentiary details
    """
    # Extract per-factor evidence
    f1 = verify_F1_identity_dna(artifact, originator, evidence_bundle[0])
    f2 = verify_F2_temporal_anchor(artifact, evidence_bundle[1], ledger)
    f3 = verify_F3_rule_trace(artifact, evidence_bundle[2])
    f4 = verify_F4_persona_route(artifact, evidence_bundle[3], originator)
    f5 = verify_F5_protected_lexicon(artifact, evidence_bundle[4], originator)
    f6 = verify_F6_style_vector(artifact, evidence_bundle[5], originator)
    f7 = verify_F7_mistake_ledger(artifact, evidence_bundle[6])

    scores = [f1, f2, f3, f4, f5, f6, f7]

    # SanCai weights (Heaven-Earth-Human)
    weights = [0.17, 0.17, 0.11, 0.11, 0.16, 0.16, 0.12]

    # Compute composite confidence with hard-failure semantics
    conf = weighted_geometric_mean(scores, weights)

    per_factor_scores = {
        'F1': {'score': f1, 'name': 'Identity DNA'},
        'F2': {'score': f2, 'name': 'Temporal Anchor'},
        'F3': {'score': f3, 'name': 'Rule Trace'},
        'F4': {'score': f4, 'name': 'Persona Route'},
        'F5': {'score': f5, 'name': 'Protected Lexicon'},
        'F6': {'score': f6, 'name': 'Style Vector'},
        'F7': {'score': f7, 'name': 'Mistake Ledger'},
    }

    report = {
        'composite_confidence': conf,
        'threshold': threshold,
        'passed': conf >= threshold,
        'per_factor': per_factor_scores,
        'hard_failures': [
            name for name, data in per_factor_scores.items()
            if data['score'] == 0
        ],
        'ledger_integrity': verify_ledger_integrity(ledger),
    }

    return conf, report
```

---

### A.6 Sample Invocation

```python
# Example usage
artifact = ContentArtifact(
    content="Behavioral Cryptography: A Multi-Factor...",
    format="text/markdown",
    context={"tool": "Longhun", "platform": "local"}
)

originator = OriginatorRecord(
    uid="UID9622",
    gpg_fingerprint="A2D0...6D5F",
    public_key=load_key("originator.pub"),
    protected_lexicon={"龍芯", "北辰", "時辰", "五行"}
)

conf, report = verify_behavioral_signature(
    artifact, originator, evidence_bundle, ledger
)

print(f"Composite confidence: {conf:.4f}")
print(f"Passed: {report['passed']}")
for factor, details in report['per_factor'].items():
    print(f"  {factor} ({details['name']}): {details['score']:.4f}")
```

---

## Appendix B · Proof Bundle Schema

### B.1 Purpose

[正文骨架 · §B.1]

The proof bundle schema defines the structure of evidence packages that can be shared with verifiers.

---

### B.2 Required Fields

[正文骨架 · §B.2]

```yaml
proof_bundle:
  version: "1.0"
  root_identity:
    uid: string
    gpg_fingerprint: string
    public_key_url: string
  artifact:
    content_hash: string  # SHA-256
    format: string
    creation_time: ISO8601
  behavioral_signature:
    factor_scores: [float, float, float, float, float, float, float]
    weights: [float, float, float, float, float, float, float]
    threshold: float
    hard_failures: [string]
  audit_log:
    dna_records: [DNARecord]
    ledger_hash: string
    signature: string  # GPG signature
```

---

### B.3 Optional Fields

[正文骨架 · §B.3]

```yaml
  optional:
    style_baseline: bytes
    mistake_ledger: MistakeLedger
    persona_route_log: [PersonaRecord]
    cultural_layers:
      shichen: string
      wuxing: string
      digit_root: int
```

---

### B.4 Public / Restricted / Sealed Evidence Levels

[正文骨架 · §B.4]


| Level      | Fields Visible                                             | Verifier Requirements               |
| ---------- | ---------------------------------------------------------- | ----------------------------------- |
| Public     | content_hash, timestamps, GPG fingerprint, composite score | None                                |
| Restricted | + per-factor scores, rule traces, style vectors            | Registration required               |
| Sealed     | + full content, private lexicon, mistake ledger            | Creator authorization + legal basis |


---

### B.5 Schema Validation Notes

[正文骨架 · §B.5]

- All hash fields must be valid SHA-256 hex strings
- Timestamps must be valid ISO 8601 with timezone
- GPG signatures must be verifiable against the declared public key
- Factor scores must be in [0, 1]
- Weights must be positive and sum to 1.0

---

## Appendix C · Longhun Co-authorship Protocol (LCP-1.0)

### C.1 Purpose

[正文骨架 · §C.1]

LCP-1.0 defines the co-authorship protocol for human-AI collaborative works under the Behavioral Cryptography framework.

---

### C.2 Human Originator Declaration

[正文骨架 · §C.2]

The human originator declares:

- I am the primary author of the creative and intellectual content
- AI tools were used as instruments of production
- I take full responsibility for all factual claims and normative positions
- I have reviewed and approved all content attributed to me

---

### C.3 AI Collaborator Role Boundary

[正文骨架 · §C.3]

The AI collaborator:

- Assists with structural organization and formal notation
- Does not make independent factual claims
- Does not modify security claims without human authorization
- Flags uncertainty and suggests qualifiers where appropriate

---

### C.4 Audit Requirements

[正文骨架 · §C.4]

All human-AI interactions must be logged in the evidence ledger with:

- Timestamp of interaction
- Prompt/response hash (not content)
- Action label (draft, review, formalize, verify)
- Human approval status

---

### C.5 Dispute Resolution

[正文骨架 · §C.5]

In case of disputes about authorship contribution:

1. The evidence ledger is examined by an independent auditor
2. The human author's original drafts are compared with AI-assisted revisions
3. Contribution is assessed based on: origin of ideas, origin of claims, editorial control

---

### C.6 Sample LCP-1.0 Header (YAML)

```yaml
lcp_header:
  version: "1.0"
  work_title: "Behavioral Cryptography: A Multi-Factor..."
  human_author:
    name: "Zhuge Xin"
    uid: "UID9622"
    gpg_fingerprint: "A2D0...6D5F"
    declaration: "I am the primary author..."
  ai_collaborator:
    system: "Claude (Anthropic)"
    role: "Writing assistant, structural editor"
    boundary: "Does not make independent factual claims"
  audit_log:
    ledger_url: "./evidence/longhun_ledger.db"
    first_interaction: "2025-01-15T09:00:00+08:00"
    last_interaction: "2026-05-06T14:28:00+08:00"
  confirm_signature: "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
```

---

## Appendix D · Sample Redacted Evidence Record

### D.1 Purpose

[正文骨架 · §D.1]

This appendix demonstrates how evidence records appear when redacted for privacy-preserving verification.

---

### D.2 Sample Record Structure (Redacted)

```yaml
evidence_record_redacted:
  record_id: "REC-2026-0506-001"
  content_hash: "SHA256:e3b0c4..."  # Hash only, no content
  timestamp: "2026-05-06T14:28:00+08:00"
  shichen: "未时"
  action: "CREATE"
  factor_summary:
    F1: {score: 1.0, detail: "signature_valid"}
    F2: {score: 1.0, detail: "timestamp_verified"}
    F3: {score: null, detail: "redacted"}
    F4: {score: null, detail: "redacted"}
    F5: {score: 0.85, detail: "lexicon_match_partial"}
    F6: {score: null, detail: "redacted"}
    F7: {score: null, detail: "redacted"}
  parent_hash: "SHA256:a1b2c3..."
  dna_signature: "-----BEGIN PGP SIGNATURE-----..."
  # Private lexicon, style baseline, mistake ledger: NOT INCLUDED
```

---

### D.3 Redaction Rules

[正文骨架 · §D.3]


| Field           | Rule                    | Rationale                                    |
| --------------- | ----------------------- | -------------------------------------------- |
| Content         | never_disclose          | Content itself is not evidence               |
| Content hash    | may_disclose_as_hash    | Verifies integrity without revealing content |
| Private lexicon | may_disclose_as_hash    | Protects creator's vocabulary                |
| Mistake ledger  | may_disclose_as_summary | Privacy for errors; summary suffices         |
| Full DNA record | may_disclose_publicly   | Public components only                       |
| GPG private key | never_disclose          | Cryptographic security                       |


---

## Appendix E · Longhun DNA Inheritance Clause (v1.0)

### E.1 Purpose

[正文骨架 · §E.1]

The Longhun DNA Inheritance Clause prevents provenance erasure and platform capture by requiring derivative works to maintain the provenance chain.

---

### E.2 English Clause

[正文骨架 · §E.2]

**Derivative Work Attribution Requirements.**

Any derivative work based on content protected by Behavioral Cryptography must:

1. Include a reference to the original DNA record in its own DNA
2. Maintain chain continuity: the derivative DNA must reference the parent DNA
3. Not remove, alter, or obscure the original provenance information
4. Include the attribution tag: `Derived from: [Original DNA Hash]`

Violation of these requirements constitutes provenance erasure and is grounds for dispute under the LCP-1.0 protocol.

---

### E.3 中文条款

[正文骨架 · §E.3]

**衍生作品归属要求。**

任何基于受行为密码学保护的内容的衍生作品必须：

1. 在其自身 DNA 中包含对原始 DNA 记录的引用
2. 保持链连续性：衍生 DNA 必须引用父 DNA
3. 不得移除、修改或遮蔽原始溯源信息
4. 包含归属标签：`源自：[原始DNA哈希]`

违反这些要求构成溯源抹除，可依据 LCP-1.0 协议提出争议。

---

### E.4 Short Attribution Format

[正文骨架 · §E.4]

Short format for space-constrained contexts:

```
BC-v1.0 | Parent: SHA256:... | UID: ... | Confirm: #CONFIRM...
```

---

### E.5 What This Clause Does NOT Prohibit

[正文骨架 · §E.5]

This clause does **not** prohibit:

- Fair use and fair dealing
- Independent creation of similar content
- Criticism, commentary, or parody
- Academic citation and analysis
- Platform migration with provenance preservation

---

### E.6 Dispute and Verification

[正文骨架 · §E.6]

Provenance disputes are resolved through:

1. Evidence bundle examination by independent auditors
2. Chain continuity verification
3. LCP-1.0 audit log review
4. Community arbitration (for open-source works)

---

# Tail Matter

## Glossary

[正文骨架 · Glossary · 完整定义参见 Glossary_Unified.md]

Key terms:

- **Behavioral Cryptography:** Multi-factor provenance framework treating authenticity as composite behavioral lineage
- **Behavioral Signature Σ(C):** Seven-tuple of per-factor confidence scores
- **Composite Confidence:** Weighted geometric mean of per-factor scores
- **Content Artifact:** Tuple of (content, format, context)
- **DNA Record:** Structured evidence record binding content to creation lineage
- **Dynamic DNA Engine:** System for generating and verifying DNA records
- **Evidence Ledger:** Append-only log of DNA records
- **Hard Failure:** Single factor score of 0, collapsing composite confidence to 0
- **Lineage Chain:** Directed path from content record to root identity anchor
- **Longhun:** Civilian-grade reference implementation
- **Verification Oracle:** Function V(Σ, E) → (conf, evidence)

[其余术语见 Glossary_Unified.md，约40个条目]

---

## Claim Strength Index

[正文骨架 · Claim Strength Index · 完整审计表参见 Claim_Strength_Audit.md]

---

## Document History


| Version        | Date       | Description                                                                                     |
| -------------- | ---------- | ----------------------------------------------------------------------------------------------- |
| v0.1           | 2025       | First draft, core framework                                                                     |
| v0.9           | 2026-05-02 | Appendix A-E first complete                                                                     |
| v1.0           | 2026-05-06 | Full paper package, all sections finalized                                                      |
| v1.0-body      | 2026-05-06 | Body draft generated with Claim Strength Audit patches applied                                  |
| v1.0-body-edit | 2026-05-07 | WGM notation aligned (Def 3.3 / §3.4); Appendix A pseudocode repaired; TOC link; §1.2 tightened |


---

# 变更摘要 · Change Log

## 本次修改概述

本文件 `FULL_PAPER_v1.0_Body_Draft.md` 是基于 `FULL_PAPER_v1.0_TOC.md` 目录结构新建的正文骨架文件，并在指定位置插入了 Claim Strength Audit 要求的三处修补内容。2026-05-07 另做技术性编辑：WGM 定义与聚合小节一致化、附录 A 复合验证伪代码可解析性修复、目录相对链接、§1.2 假设表述去冗余。

---

## 修补 #1：Hypothesis 1.1 显式标注（§1.2）

**位置：** §1.2 在 Hypothesis 1.1 块之后；其下一段以 “Building on Hypothesis 1.1...” 展开，避免与 Hypothesis 1.1 首句重复断言。

**插入内容：**

- `**Hypothesis 1.1 (Behavioral Cryptography Hypothesis).** Content authenticity is not a single signal. It is a composite behavioral lineage. Copying content is easy; copying lineage is hard.`
- `*Argument.* Existing provenance systems rely on isolated signals... This hypothesis motivates the seven-factor framework developed in Chapter 3 and the Dynamic DNA Engine in Chapter 4.`

**Claim Strength Audit 对应项：** §1.2 中心假设（原状态 🟡 → 修补后 🟢）

---

## 修补 #2：Prop 3.4 结论句降强度（§3.4 末尾）

**位置：** Proposition 3.4 的 Proof Sketch 末尾，替换原有 "prevents forgery" / "保证防止伪造" 类表述。

**替换为：**

- 结论句改为："Behavioral Cryptography **significantly raises the cost and difficulty of full-lineage forgery** compared to single-signal provenance schemes."
- 新增明确边界说明："It does not claim mathematical impossibility of forgery; rather, the multi-factor independence and the append-only evidence structure increase the adversary's required effort across identity, temporal, lexical, stylistic, and behavioral channels simultaneously. ∎"

**Claim Strength Audit 对应项：** Prop 3.4（原状态 🟡 → 修补后 🟢）

---

## 修补 #3：Thm 3.12 补形式化句（§3.5.11 Proof Sketch）

**位置：** Theorem 3.12 "Correction Preservation" 的 Proof Sketch 段落，替换原有偏定性表述。

**替换为形式化 Proof Sketch：**

- `Let r be the original record in the evidence ledger and r' be an honest correction appended later. Under the append-only constraint, both r and r' remain auditable in the ledger.`
- `Formally, the append-only property guarantees that for any ledger state L_t at time t, the set of contained records {r_1, r_2, ..., r_n} is monotonically non-decreasing in n.`
- `Therefore, appending r' preserves r; replacing r with r' violates monotonicity and removes the original from the audit trail. ∎`

**Claim Strength Audit 对应项：** Thm 3.12（原状态 🟡 → 修补后 🟢）

---

## 编辑修复 #4：记号一致性与附录伪代码（2026-05-07）

- **Def 3.3 / §3.4：** 写明一般 WGM 形式 (∏ s_i^{w_i})^{1/∑w_i} 与本文 ∑w_i = 1 时的简写 ∏ s_i^{w_i} 等价；§3.4 显式指向 Def 3.3。
- **Appendix A：** `verify_behavioral_signature` 中 `report` 去除重复 `per_factor` 键、补全 `hard_failures` 列表与闭合括号；增加 `verify_ledger_integrity` 桩函数；`threshold` 参数化。
- **目录：** Table of Contents 处增加至 `./FULL_PAPER_v1.0_TOC.md` 的相对链接。
- **标题行：** 移除误粘贴的对话前缀，保留标准 Markdown H1 标题。

---

## 审计状态更新


| 编号       | 名称                                   | 修补前                   | 修补后                             |
| -------- | ------------------------------------ | --------------------- | ------------------------------- |
| Hyp 1.1  | Behavioral Cryptography Hypothesis   | 🟡 隐式 Claim           | 🟢 显式标注 + Argument              |
| Prop 3.4 | Forgery Resistance Under Assumptions | 🟡 "prevents forgery" | 🟢 "raises cost and difficulty" |
| Thm 3.12 | Correction Preservation              | 🟡 定性 Proof Sketch    | 🟢 形式化 + monotonicity           |


**Claim Strength Audit 6 项 🟡 全部清零！**

---

*FULL_PAPER_v1.0_Body_Draft.md · Generated from TOC · Claim Strength Patches + Editor Fixes · 2026-05-06 / 2026-05-07*