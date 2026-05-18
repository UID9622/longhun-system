# 目录方案 · 待 L0 批复

**DNA:** `#龍芯⚡2026-05-18-BEHAVCRYPTO-DIR-PROPOSAL-v1.0`  
**状态:** 🟡 待 UID9622 点头 · **Cursor 不自动 git mv**

## 现状

| 路径 | 角色 |
|------|------|
| `longhun-system/BehavCrypto_v1.0/` | 母稿 + CANONICAL_LOCK + SHA256 |
| `BehavCrypto_v1.0/`（仓库根） | 卫星 · `CANONICAL_POINTER.md` |

## 方案 A · 不动（当前）

- **利:** 零迁移风险 · SHA256 路径不变  
- **弊:** 双层 `longhun-system` 易引用错路径  
- **缓解:** 根卫星 `CANONICAL_POINTER.md` + README 双写真源路径  

## 方案 B · 母稿提升到仓库根（推荐）

- `git mv longhun-system/BehavCrypto_v1.0 ./BehavCrypto_v1.0_canonical`  
- 卫星并入 `BehavCrypto_v1.0_canonical/satellites/`  
- **工作量:** 中 · 重算 SHA256 · 改 `.cursor/rules` · CI 路径  

## 方案 C · 卫星下沉

- 根 `BehavCrypto_v1.0/*` → `longhun-system/BehavCrypto_v1.0/satellites/`  
- **工作量:** 小 · 嵌套仍深  

## 决策栏（老大填）

- [ ] 方案 A  
- [ ] 方案 B  
- [ ] 方案 C  
- 批复 DNA: _______________
