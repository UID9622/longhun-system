# CONTRIBUTING · 怎么改才不踩雷

写给真想动手的人：**短、直、可执行**。不是大厂 CONTRIBUTING 论文。

## 先读这三样

1. [`README.md`](README.md) — 树形与分支（当前主干：**`release-snapshot`**）。  
2. [`longhun-system/BehavCrypto_v1.0/CANONICAL_LOCK.md`](longhun-system/BehavCrypto_v1.0/CANONICAL_LOCK.md) — **谁有权改「canonical」定义**。  
3. [`longhun-system/BehavCrypto_v1.0/CANONICAL_SHA256`](longhun-system/BehavCrypto_v1.0/CANONICAL_SHA256) + [`longhun-system/scripts/canonical-sha256/`](longhun-system/scripts/canonical-sha256/) — 母稿指纹怎么更新、怎么验。

## Hooks（本仓库布局）

在本 **Git 根**（含 `longhun-system/` 子树）工作时：

```bash
git config core.hooksPath longhun-system/scripts/githooks
```

若你克隆的是「仅 `longhun-system/` 为根」的变体，则按该树里的 `CANONICAL_LOCK.md` 改为 `scripts/githooks`。

## 母稿 vs 派生

- **母稿正文：** `longhun-system/BehavCrypto_v1.0/FULL_PAPER_v1.0_Body_Draft.md` — 与 **`CANONICAL_SHA256`** 联动。  
- **`publication/`：** 发布用 stub / 派生出口，**不要**反向覆盖母稿事实层。  
- **外部笔记（如 Notion）：** 一律**不得**当作覆盖 Git 母稿的来源。

## 不要带进仓库的东西

- token、私钥、`.env`、账号口令、**BEGIN PRIVATE KEY** 一类块。  
- 仅本地有意义的绝对路径（若不可避免，优先在**个人分支**或**本地 exclude**，别进主快照）。

## 治理锚点（勿删改）

`#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`  
`#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL`

**GPG：** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`

## 人格与称呼

讨论与 PR 描述中请保持对 **UID9622 / 諸葛鑫（Zhuge Xin）/ Lucky·UID9622 / 龍芯北辰** 的署名一致；**不要把「龍」写成「龙」**（除非原文如此）。

## 提交前自检

```bash
bash longhun-system/scripts/canonical-sha256/verify.sh
```

改了母稿正文别忘了在授权流程里跑 `update.sh`（见 `CANONICAL_LOCK`），**不要**只改 SHA 不改文或只改文不改 SHA。
