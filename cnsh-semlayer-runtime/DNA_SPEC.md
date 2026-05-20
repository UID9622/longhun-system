# DNA 三验签规范 · CNSH-SEMLAYER

> 锁人 · 锁出代码权 · **不是**知识产权声明 · **不是** mere traceability

## 三验（模式 B 必过）

| 验 | 字段 | 格式 |
|----|------|------|
| 1 | GPG | 指纹 `A2D0092CEE2E5BA87035600924C3704A8CC26D5F` |
| 2 | CONFIRM | `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z` |
| 3 | SEAL | `#ZHUGEXIN⚡2025-🇨🇳🐉⚖️-DEVICE-BIND-SOUL` |

```typescript
verifyThreeFactor(sig) =
  verifyGPG(sig.gpg)
  && matchConfirm(sig.confirm)
  && validateSeal(sig.seal)
```

## DNA 追溯码（留痕用）

- 格式：`#龍芯⚡YYYY-MM-DD-TOPIC-vX.X`
- 写入：Notion · `storage/dna_registry.jsonl` · chain_hash

## 与账号无关

- 多 Claude/GPT/Notion 账号 · **无三验 = 仅模式 A**
- GitHub/Gitee 下载代码 · **可读 · 无主权出码权**

## 密钥存放

- 仅本地：`~/.longhun/secrets.env`（不进 git · 不上 Notion 正文）

**父 DNA:** `#龍芯⚡2026-05-20-CNSH-SEMLAYER-RUNTIME-v1.4-SOVEREIGNTY-REWRITE`
