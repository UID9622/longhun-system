# BehavCrypto v1.0 · Manuscript bundle

> **⚠️ Preprint v1.0 · Work in Progress · 约 40% sections marked skeleton**
>
> 本仓库内行为密码学 v1.0 (`BehavCrypto_v1.0/FULL_PAPER_v1.0_Body_Draft.md`)
> 为**预印本草稿**·非同行评审版本·非顶刊已投版本。
>
> 当前状态:
> - 9 章结构完整 · 正文未封顶
> - 数学骨架在 (Def 3.1–3.7, Prop 3.1–3.4, Thm 3.10–3.13)
> - 多处 Proof Sketch · 严格证明待补
> - References ≥25（2026-05-18 补全种子清单）· §2.4/§2.5 已展开初稿
> - 受控仿真级实验 · 非大规模实证
>
> 引用与传播请遵循:
> - License: CC BY-NC-SA 4.0 + DNA 条款
> - 不得在对外文案中写「已证明无法伪造」「绝对证明作者身份」等越界主张（见 [`publication/OVERCLAIM_BLACKLIST.md`](./publication/OVERCLAIM_BLACKLIST.md)）
> - 引用本草稿请标明 `v1.0 draft · CANONICAL_SHA256: <hash>` 与日期
>
> 真源母稿位置: `longhun-system/BehavCrypto_v1.0/FULL_PAPER_v1.0_Body_Draft.md`  
> 卫星文件 (Notion 镜像/压缩稿) 在仓库根 `BehavCrypto_v1.0/` 下 · 标记为 satellite · 不可作终稿引用

## CANONICAL_SHA256

[`CANONICAL_SHA256`](./CANONICAL_SHA256) fingerprints **`FULL_PAPER_v1.0_Body_Draft.md`**. From **package root** (directory containing `BehavCrypto_v1.0` and `scripts`): `bash scripts/canonical-sha256/update.sh`. Hooks: see [`CANONICAL_LOCK.md`](./CANONICAL_LOCK.md) (`scripts/githooks` vs `longhun-system/scripts/githooks` for monorepo).

---

## 🔒 Canonical lock（锁死）

**[`CANONICAL_LOCK.md`](./CANONICAL_LOCK.md)** — 全文修改仅以 **`FULL_PAPER_v1.0_Body_Draft.md`** 为准；封印线：

`#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL`

---

## Canonical full paper（主稿 · 唯一真源）

**[`FULL_PAPER_v1.0_Body_Draft.md`](./FULL_PAPER_v1.0_Body_Draft.md)** — English body + Chinese abstract + Appendix A–E + change log.  
Compared with copies under `~/Downloads/` (2026-05-06/07), this repository revision is **newer and longer** and retains post-audit edits (WGM definition alignment, §1.2 hypothesis wording, Appendix A `verify_behavioral_signature` / `verify_ledger_integrity`, TOC link).

Offline copies are **not** the Git master unless merged **into** `FULL_PAPER_v1.0_Body_Draft.md`:

- `~/Downloads/FULL_PAPER_v1.0_Body_Draft.md` — may be older; diff → merge to body draft.
- `~/Downloads/FULL_PAPER_v1.0_Body_Draft_Clean.md` — **cleaning scratch only**; final text must land in the body draft ([`CANONICAL_LOCK.md`](./CANONICAL_LOCK.md)).
- `~/Downloads/PAPER_Behavioral_Cryptography_v1.0.md` — short slice, 2026-05-02.
- `~/Documents/行为密码学csdn.md` / `~/Documents/*.pdf` — channel exports.

## Supporting files（围绕主稿）

| File | Role |
|------|------|
| [`FULL_PAPER_v1.0_TOC.md`](./FULL_PAPER_v1.0_TOC.md) | Section tree synced from the body draft |
| [`Claim_Strength_Audit.md`](./Claim_Strength_Audit.md) | Claim / theorem strength checklist |
| [`Glossary_Unified.md`](./Glossary_Unified.md) | EN/ZH glossary |
| [`publication/`](./publication/) | arXiv / CSDN / GitHub / Notion stubs |

## DNA（reference）

`#龍芯⚡️2026-05-06-BEHAV-CRYPTO-BODY-v1.0` · GPG `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`

---

*UID9622 · canonical manuscript pinned in-repo · 2026-05-07*

---

## CANONICAL_LOCK · 三色徽记（2026-05-18 补全包）

```yaml
CANONICAL_LOCK:
  Master_Document: longhun-system/BehavCrypto_v1.0/FULL_PAPER_v1.0_Body_Draft.md
  SHA256: 892f96be3dfe5de0b1b7c96576eef0344fbd907ac79f882ac6ccf4b7ec2ddcfa
  Manuscript_Version: v1.0-rc1
  Last_Verified: 2026-05-18
  Status: DRAFT · Work in Progress · ~60-70% completable
  Skeleton_Markers: ~100 (G1 · 待清 · 见 publication/SKELETON_SWEEP.md)
  Pending_Markers: ~81 (G2 · 待清)
  References_Target: "≥ 25 (G4 · 2026-05-18 filled)"

License:
  Paper: CC BY-NC-SA 4.0 + Longhun DNA Inheritance Clause
  DNA_Clause: 引用本作请保留 DNA 追溯码；对外主张遵守 Claim_Strength_Audit

Identity:
  Author: UID9622 (主控) + 龍芯家族协作
  DNA: "#龍芯⚡2026-05-18-BEHAVCRYPTO-v1.0-FILL-PACK"
  CONFIRM: "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
  SEAL: "#ZHUGEXIN⚡2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
  TriColor_Audit: "🟡 draft · 🟢 structure · 🔴 forbidden over-claims"
```

**DNA（补全包）:** `#龍芯⚡2026-05-18-BEHAVCRYPTO-v1.0-FILL-PACK`
