# 越界主张黑名单 · 对外文案扫描清单

> **DNA:** `#龍芯⚡2026-05-18-BEHAVCRYPTO-OVERCLAIM-BLACKLIST-v1.0`  
> **CONFIRM:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`  
> 与 [`Claim_Strength_Audit.md`](../Claim_Strength_Audit.md) 同步 · 发布前必扫

---

## 禁止措辞（🔴 One-Vote Veto）

| # | 禁止 |
|---|------|
| 1 | 「已证明无法伪造」/「数学证明不可伪造」 |
| 2 | 「100% 防伪造」/「绝对安全」 |
| 3 | 「已严格证明的安全系统」 |
| 4 | 「可代替密码学」/ replaces GPG/C2PA |
| 5 | 「绝对证明作者身份」/ proves authorship absolutely |
| 6 | 「顶刊已收录」（未被实际接收前） |
| 7 | 「国家级」/「国家认证」（无官方文件背书） |
| 8 | 「经过 X 万次攻击测试」（无可复现实验数据） |

## 允许措辞（✅）

- 「在 [假设清单 A1–A5] 下显著提高全谱系伪造成本」
- 「行为密码学框架草案 · 含数学骨架与受控仿真」
- 「预印本 · 工作进展中 · 欢迎独立审计」
- 「受控仿真下 composite confidence 分布 · 大规模实证待补」

## 仓库扫描（发布前）

从 **monorepo 根** 执行:

```bash
grep -rE "(无法伪造|100%.*防|绝对证明|不可能伪造|顶刊已收录|国家认证)" \
  longhun-system/BehavCrypto_v1.0/README.md \
  longhun-system/BehavCrypto_v1.0/publication/ \
  BehavCrypto_v1.0/ 2>/dev/null || true
```

英文母稿另扫:

```bash
grep -nE "(cannot be forged|100% secure|proves authorship absolutely|cryptographically secure)" \
  longhun-system/BehavCrypto_v1.0/FULL_PAPER_v1.0_Body_Draft.md
```

命中 🔴 项须改写法或删除后再对外发布。
