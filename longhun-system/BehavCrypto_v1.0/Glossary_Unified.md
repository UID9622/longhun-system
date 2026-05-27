# Glossary · 术语表（Unified EN / ZH）
## Behavioral Cryptography v1.0

> **DNA:** `#龍芯⚡️2026-05-06-BEHAV-CRYPTO-GLOSSARY-v1.0`  
> **CONFIRM:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`  
> **重建:** 2026-05-07 — 与 `FULL_PAPER_v1.0_Body_Draft.md` 对齐的精选条目；可随正文增删。

| English | 中文 | 释义 |
|--------|------|------|
| Behavioral Cryptography | 行为密码学 | 多因素来源追溯框架：将真实性建模为可审计的行为谱系，而非单一信号。 |
| Behavioral signature Σ(C) | 行为签名 Σ(C) | 七元组 ⟨F1…F7⟩，每维为 [0,1] 置信度。 |
| Composite confidence | 复合置信度 | 带硬失败语义的加权几何均值（WGM）；任一因子为 0 则整体为 0。 |
| Hard failure | 硬失败 | 某因子得分为 0，表示该通道上存在明确违背协议或伪造迹象。 |
| Verification oracle V(Σ,E) | 验证谕示 V(Σ,E) | 输入签名与辅助证据，输出 (conf, evidence_report)。 |
| Content artifact | 内容工件 | 三元组 (content, format, context)。 |
| Identity DNA (F1) | 身份 DNA（F1） | 密码身份绑定（如 GPG、UID 锚点）。 |
| Temporal anchor (F2) | 时间锚（F2） | 时间序列一致性；强结论依赖可信时间源或只追加账本。 |
| Rule trace (F3) | 规则迹（F3） | 文档化变换规则与编辑/结构变更日志。 |
| Persona route (F4) | 人格路径（F4） | 与人设/协作路径一致的主题与风格约束。 |
| Protected lexicon (F5) | 受保护词表（F5） | 创造者专有词汇标记，抗「洗稿」语义漂移。 |
| Style vector (F6) | 风格向量（F6） | 句法/结构层面的统计指纹（随模型进化需调权）。 |
| Mistake ledger (F7) | 错误账簿（F7） | 修订、纠错与「诚实错误」模式的可审计记录。 |
| Evidence ledger | 证据账本 | 只追加 DNA/证据记录序列，带父链与签名。 |
| Lineage chain | 谱系链 | 从工件记录沿 parent 指向根身份锚的有向路径。 |
| Chain continuity | 链连续性 | 父引用有效、签名链可验证、无环（通常靠时间单调）。 |
| Dynamic DNA Engine | 动态 DNA 引擎 | 生成/校验 DNA 记录与谱系绑定的组件。 |
| DNA record | DNA 记录 | 结构化证据记录（UID、指纹、时间、动作、内容哈希、父哈希、封印等）。 |
| SanCai weights | 三才权重 | 天地人框架下的因子权重；正文示例满足 H≥0.34。 |
| Shield Engine | 盾引擎 | 入口/出口门：入站校验与出站前写账本。 |
| Longhun | 龍芯 / 龍魂民用实例 | 本地优先、开源工具链上的参考实现。 |
| LCP-1.0 | LCP-1.0 共著协议 | 人机协作文档的人类最终责任与 AI 工具边界。 |
| Proof bundle | 证明包 | 可分层的证据包（公开/限制/封存）。 |
| Silent laundering | 静默洗钱（溯源） | 导出内容但不带谱系链，导致验证硬失败。 |
| C2PA | C2PA | 内容凭证工业标准；本框架与其互补。 |
| WGM | 加权几何均值 | 聚合多因子得分；对弱通道惩罚强于算术平均。 |
| Threshold τ | 阈值 τ | 通过线：正文建议 0.85（标准）/ 0.95（高安全），经验值。 |
| Shichen (時辰) | 时辰 | 文化-时间语义层；非密码学根。 |
| Wuxing (五行) | 五行 | 语义映射层；用于人读与异常模式提示，不可替代签名。 |
| Digit root | 数根 | DNA 中的派生数值标记；语义辅助。 |
| Creator sovereignty | 创作者主权 | 数据可携、平台无关验证、证据不被平台单方面抹除。 |
| DNA Inheritance Clause | DNA 继承条款 | 衍生作品须保留父链与归属标签的规范草案。 |
| Selective disclosure | 选择性披露 | 验证方不必见全文即可核对哈希/链/部分因子。 |
| Multi-factor provenance | 多因素溯源 | 独立通道交集提高全谱系伪造成本。 |
| Full-lineage forgery | 全谱系伪造 | 同时骗过七因子与账本一致性的攻击目标。 |
| Protocol compliance | 协议合规 | 七因子均按 Longhun 协议记录且无硬失败等（见正文细化）。 |
| Append-only | 只追加 | 账本不得静默改写历史记录；更正通过新记录追加。 |
| Behavioral residue | 行为残留 | 创作/修订过程中难以一并伪造的交互与修订痕迹。 |
| AI collaborator | AI 协作者 | 写作与形式化助手；非科学贡献的独立主张者（见 LCP-1.0）。 |

---

*约 40 条规模 · 与正文关键词、附录 A–E 一致 · UID9622*
