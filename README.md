# Longhun System · 龍魂

Independent governance, protocol, and provenance artifacts for **UID9622** (Zhuge Xin / 諸葛鑫).

**Maintainer:** [UID9622](https://github.com/UID9622) · **GPG:** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`

---

## Why this layout looks unusual

The Git root uses a **whitelist** (see [`.gitignore`](.gitignore)): almost everything outside [`longhun-system/`](longhun-system/) is ignored on purpose. Treat **`longhun-system/`** as the canonical working tree you care about after clone.

---

## What is in this repo (tracked)

### Protocols · 協議

- [**北辰母協議 v2.0（清理版）**](longhun-system/01_protocols/cnsh/PROTOCOL__20260325__BEICHEN-MOTHER-PROTOCOL__v2.0-clean.md) — P0-ETERNAL constitution-grade protocol (CNSH).

### Research · Behavioral Cryptography

- [**Manuscript bundle (canonical anchor)**](longhun-system/BehavCrypto_v1.0/README.md) — TOC, claim audit, glossary, publication stubs; **master file** is the body draft below. **Lock:** [`CANONICAL_LOCK.md`](longhun-system/BehavCrypto_v1.0/CANONICAL_LOCK.md). **Integrity:** [`CANONICAL_SHA256`](longhun-system/BehavCrypto_v1.0/CANONICAL_SHA256) + pre-commit (`git config core.hooksPath longhun-system/scripts/githooks`) + CI workflow `.github/workflows/canonical-sha256.yml`.
- [**Full paper body draft v1.0**](longhun-system/BehavCrypto_v1.0/FULL_PAPER_v1.0_Body_Draft.md) — *Behavioral Cryptography: A Multi-Factor Provenance Framework for Human-AI Collaborative Content Authentication* / 行为密码学（人机协作内容认证的多因素来源追溯框架）.

### Logs · 運行日誌

- [`longhun-system/logs/`](longhun-system/logs/) — automation / audit output. **Ephemeral diagnostics only**, not a stable contract.

### Obsidian (vault hints)

- [`longhun-system/.obsidian/`](longhun-system/.obsidian/) — editor settings for local knowledge work.

---

## Branch

Active line of work: **`release-snapshot`**. If your default branch differs:

```bash
git fetch origin
git checkout release-snapshot
```

---

## License & boundaries

Rights follow **each file’s own header** (typical manuscript license: **CC BY-NC-SA 4.0** plus **Longhun DNA Inheritance Clause** where stated). Nothing here is legal advice; protocols and papers are **normative documents**, not substitute for counsel or platform ToS.

---

## 中文摘要

本仓库为 **龍魂 / Longhun** 的精选快照：根目录刻意极简，正文与协议集中在 **`longhun-system/`**。当前可见主干包括 **北辰母協議 v2.0** 与 **行为密码学** 论文正文草稿；运行日志仅作排障参考。

---

*README · UID9622 · aligned with `release-snapshot` tree*
