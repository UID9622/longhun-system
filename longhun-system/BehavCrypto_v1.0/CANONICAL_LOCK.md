# Canonical lock · 全文主稿锁死规则

> **Status:** ACTIVE · UID9622 · 龍芯北辰  
> **Effective:** 2026-05-07

## 锁死声明（单一真源）

此后凡涉及 **Behavioral Cryptography / 行为密码学** 的**全文级**撰写、修订、合并、导出与版本对齐，**一律以本目录内**  **`FULL_PAPER_v1.0_Body_Draft.md`** **为唯一权威母稿**。

- **母稿地位不可由代理人改写：** 上一条所称「唯一母稿」**仅指** `FULL_PAPER_v1.0_Body_Draft.md`。除非 **UID9622 亲自修改本文件 `CANONICAL_LOCK.md`** 以变更定义，否则**任何** AI / 自动化 / 协作者**不得**另行指定、重命名或替换「主稿」角色。
- **Clean / 清洗稿：** 凡文件名或用途为 **Clean**、**清洗**、**scrub** 的副本（例如 `FULL_PAPER_v1.0_Body_Draft_Clean.md` 或 `~/Downloads/` 下同类文件）**只能**作为**临时清洗工作稿**（去噪、分段整理、格式试验）。**最终定稿内容必须合并回** `FULL_PAPER_v1.0_Body_Draft.md`；**不得**把 Clean 稿当作仓库内权威正文长期顶替母稿。
- **不得**以 `~/Downloads/`、`~/Documents/` 或其他路径的**非母稿**文件**覆盖** `FULL_PAPER_v1.0_Body_Draft.md`，除非已 diff、由你确认，且把变更**写回母稿**（Clean 稿亦同：合并目标只能是母稿）。
- **`FULL_PAPER_v1.0_TOC.md`**：由母稿标题同步生成或手工对齐母稿，**不得**反过来定义与母稿冲突的章节真源。
- **`Claim_Strength_Audit.md` / `Glossary_Unified.md` / `publication/*`**：为母稿的**卫星文件**，修订须与母稿主张一致；**不**取代母稿正文。

## CANONICAL_SHA256（完整性指纹）

- **`CANONICAL_SHA256`**：单行 `shasum -a 256` / `sha256sum` 格式；第二列路径为 **`BehavCrypto_v1.0/FULL_PAPER_v1.0_Body_Draft.md`**（相对于**本包根目录**：即同时含有 `BehavCrypto_v1.0/` 与 `scripts/` 的那一层——在独立仓库中就是 Git 根；若仍嵌在上级 monorepo 的 `longhun-system/` 子目录中，则相对于该子目录）。用于检出「母稿字节级」是否与登记一致。
- **更新：** 在包根执行 `bash scripts/canonical-sha256/update.sh`（修改母稿后若未走 pre-commit，请手跑并按 monorepo 前缀 `git add`）。
- **校验：** `bash scripts/canonical-sha256/verify.sh`；**pre-commit**（见下）与 **CI** 均调用该校验。
- **若变更母稿文件名：** 须同步改 `CANONICAL_SHA256` 内路径、`update.sh` / `verify.sh` 常量，以及 CI 路径过滤器——此类变更视为对锁规则的结构性修改，**须由 UID9622 亲自改 `CANONICAL_LOCK.md` 与相关脚本并审阅**。

### 启用 pre-commit（一次性）

在 **Git 仓库根** 执行（`git rev-parse --show-toplevel` 所在目录）：

**独立仓库（根目录即本包，含 `BehavCrypto_v1.0` 与 `scripts`）：**

```bash
git config core.hooksPath scripts/githooks
chmod +x scripts/githooks/pre-commit
chmod +x scripts/canonical-sha256/update.sh
chmod +x scripts/canonical-sha256/verify.sh
```

**上级 monorepo（Git 根在上一级，正文路径为 `longhun-system/BehavCrypto_v1.0/...`）：**

```bash
git config core.hooksPath longhun-system/scripts/githooks
chmod +x longhun-system/scripts/githooks/pre-commit
chmod +x longhun-system/scripts/canonical-sha256/update.sh
chmod +x longhun-system/scripts/canonical-sha256/verify.sh
```

钩子行为：若暂存区包含母稿，则**自动**重写并 `git add` 对应路径下的 `CANONICAL_SHA256`；每次提交前**始终**运行 `verify.sh`。

## 封印线（CONFIRM + SEAL）

以下两行一并视为本锁规则的**执行锚**（复制时保持完整、勿拆）：

```text
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
```

（等价分行书写：`CONFIRM` 与 `SEAL` 两行，与论文 front matter 一致亦可。）

## DNA 引用

`#龍芯⚡️2026-05-06-BEHAV-CRYPTO-BODY-v1.0` · GPG `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`

---

*本文件与 `README.md` 同目录；**仅 UID9622 亲自**变更锁规则（含母稿路径/定义）；须保留 CONFIRM/SEAL 行。*

---

**DNA（路径修正锚）：** `#龍芯⚡️2026-05-07-CANONICAL-SHA256-PATH-FIX-v1.0`
