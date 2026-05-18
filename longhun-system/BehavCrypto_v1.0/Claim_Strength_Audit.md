# Claim Strength Audit · 主张强度审计表
## Behavioral Cryptography v1.0

> **DNA:** `#龍芯⚡️2026-05-06-BEHAV-CRYPTO-CLAIM-AUDIT-v1.0`  
> **目的:** 统一 Definition / Claim / Proposition / Theorem / Observation 的强度标注，防止越界主张，便于 reviewer 审查。  
> **重建说明:** 2026-05-07 自 `FULL_PAPER_v1.0_Body_Draft.md` 与历史审计结构重建；若与正文编号不一致，以正文为准。

---

## 强度等级说明

| 等级 | 标识 | 含义 | 要求 |
|------|------|------|------|
| **Definition** | Def | 形式化定义，不做真假判断 | 术语清晰即可 |
| **Observation** | Obs | 非正式经验性陈述 | 无需证明，需标注 informal |
| **Claim** | Clm | 有论据支撑的主张，非正式证明 | 需要 Argument 或 Intuition 段 |
| **Security Claim** | SC | 安全主张，依赖假设条件 | 必须列出 Assumption，不得无条件主张 |
| **Proposition** | Prop | 正式命题，有证明草图 | 需 Proof Sketch 或 Reason 段 |
| **Theorem** | Thm | 正式定理，有证明结构 | 需 Proof 段（可为草图，以 ∎ 收束） |
| **Hypothesis** | Hyp | 可证伪的研究假设 | 需 Argument 段，不得写成已证事实 |
| **Recommendation** | Rec | 工程/阈值建议 | 标明经验性，非形式界 |

---

## 第一类：形式化定义（Definition）

| 编号 | 名称 | 位置 | 状态 | 备注 |
|------|------|------|------|------|
| Def 3.1 | Content Artifact | §3.2 | 🟢 | |
| Def 3.2 | Behavioral Signature Σ(C) | §3.2 | 🟢 | |
| Def 3.3 | Verification Oracle V(Σ,E) | §3.2 | 🟢 | WGM 一般式与 ∑w_i=1 简写见正文 |
| Def 3.4 | Hard Failure | §3.2 | 🟢 | |
| Def 3.5 | Evidence Ledger | §3.5.11 | 🟢 | |
| Def 3.6 | Lineage Chain | §3.5.11 | 🟢 | |
| Def 3.7 | Chain Continuity | §3.5.11 | 🟢 | |

---

## 第二类：安全主张（Security Claim）

| 编号 | 名称 | 位置 | 状态 | 备注 |
|------|------|------|------|------|
| SC 3.1 | Identity Anchor Resistance | §3.3/F1 | 🟢 | 须前置 *Assuming GPG secure + key not compromised* |
| SC 3.2 | Temporal Consistency | §3.3/F2 | 🟢 | 无可信时间源时降为一致性检查 |

---

## 第三类：假设与命题（Hypothesis / Proposition）

| 编号 | 名称 | 位置 | 状态 | 备注 |
|------|------|------|------|------|
| Hyp 1.1 | Behavioral Cryptography Hypothesis | §1.2 | 🟢 | 显式标注 + Argument |
| Prop 3.1 | No Single-Factor Compensation | §3.4 | 🟢 | 硬失败 → 乘积为零 |
| Prop 3.2 | Composite Confidence Monotonicity | §3.4 | 🟢 | WGM 对正因子单调 |
| Prop 3.3 | Soundness Under Protocol Compliance | §3.4 | 🟢 | “合规”含义见正文 |
| Prop 3.4 | Forgery Resistance Under Assumptions | §3.4 | 🟢 | 结论为 *raises cost*，非 *impossible* |

---

## 第四类：定理（Theorem）

| 编号 | 名称 | 位置 | 状态 | 备注 |
|------|------|------|------|------|
| Thm 3.10 | Ledger Tamper Evidence | §3.5.11 | 🟢 | Hash chain |
| Thm 3.11 | Lineage Continuity | §3.5.11 | 🟢 | |
| Thm 3.12 | Correction Preservation | §3.5.11 | 🟢 | 追加式 monotonicity 论证 |
| Thm 3.13 | No Silent Laundering | §3.5.11 | 🟢 | 缺链 → F1/F2 硬失败 |

---

## 第五类：非正式主张（Claim / Observation / Recommendation）

| 标签 | 内容摘要 | 位置 | 状态 | 备注 |
|------|---------|------|------|------|
| Clm | 文化-时间语义层三条目的 | §4.6 | 🟢 | 非密码替代 |
| Obs 3.1 | F1+F5 组合防御（未形式证明） | §4.6 | 🟢 | 依赖 §3.5 仿真直觉 |
| Clm 3.5 | 不依赖单一检测器 / F6 演化 | §5.5 | 🟢 | 有 Argument |
| Rec 6.1 | τ=0.85 / 0.95 | §6.5 | 🟢 | 经验阈值，非密码界 |

---

## 越界主张黑名单（One-Vote Veto）

| ❌ 不可写 | ✅ 应改为 |
|---------|----------|
| proves authorship absolutely / 绝对证明作者身份 | increases provenance assurance |
| cannot be forged / 已证明无法伪造 / 数学证明不可伪造 | significantly raises the cost of forgery under stated assumptions |
| 100% 防伪造 / 绝对安全 | under assumptions A1–A5, raises forgery cost; hard failure on any Fi=0 |
| 已严格证明的安全系统 | draft framework with proof sketches; formal reductions open (§9.4.2) |
| guarantees detection | provides evidence for detection |
| cryptographically secure（指文化层） | culturally-anchored semantic layer |
| replaces GPG/C2PA / 可代替密码学 | complements existing provenance systems |
| 顶刊已收录（未接收前） | preprint v1.0 draft · not peer-reviewed |
| 国家级 / 国家认证（无公文） | （删除或附官方文号） |
| 经过 X 万次攻击测试（无数据） | controlled simulation (§6); large-scale empirical TBD |

对外发布前扫描: [`publication/OVERCLAIM_BLACKLIST.md`](./publication/OVERCLAIM_BLACKLIST.md)

---

## 与正文同步检查清单

- [x] Abstract / 摘要 与 Prop 3.4、Thm 3.13 强度一致（2026-05-18 复核）
- [ ] §4.6 文化层边界已反复强调  
- [ ] Appendix A 伪代码可解析（`report` 字典、`verify_ledger_integrity`）  
- [x] 参考文献 ≥25 条种子清单（2026-05-18 补全包 G4）  
- [x] §2.4 / §2.5 初稿展开（2026-05-18 补全包 G3）  
- [x] Prop 3.4 因子近独立性讨论（2026-05-18 补全包 G5）  

---

*Claim Strength Audit · rebuilt 2026-05-07 · UID9622*
