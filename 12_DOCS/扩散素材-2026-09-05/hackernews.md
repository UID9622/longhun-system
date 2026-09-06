**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
> 干支时间戳: #龍芯⚡️丙午·丁酉·癸未·子时·䷝离
# Hacker News · Show HN（适配版 · English）

> DNA: #龍芯⚡️2026-09-05-HN-REACH-OUT-UID9622
> Author: Zhuge Xin | UID9622 · LongHun BeiChen
> GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
> License: MulanPSL v2 (code) · CC BY-NC-SA 4.0 (core philosophy)

---

**Title**: Show HN: LongHun System – an open-source AI orchestration platform with DNA traceability and GPG-signed docs

**Body**:

LongHun System is an open-source "AI collaboration backbone" that treats auditability as a first-class citizen. If you let AI automate code, pipelines, and workflows, you need three things: transparency, traceability, and a hard kill switch. That's what this project is about.

What it does:

- **Tricolor audit** (🟢 pass / 🟡 needs-verification / 🔴 red-line): every engine release goes through a gated pipeline. Red lines trip a circuit breaker – the system stops, it doesn't fail quietly.
- **DNA trace codes**: every doc/script/engine carries a `#龍芯⚡️` traceability header (ganzhi pillars + module + action + short hash) so you can always tell where an artifact came from and which protocol change introduced it.
- **GPG-signed public docs**: 30+ public docs ship with detached `.asc` signatures (same dir), and the public site shows the fingerprint in the footer of every page.
- **Zero-backend + data sovereignty (P0)**: no tracking backend, no user-data collection, no default cloud upload. Data stays local.
- **Multi-agent layer**: a matrix of 22 "persona" agents (strategy / execution / culture / guardian tiers).

Public docs site (Chinese, 9 documents: install, quickstart, API, JSON-RPC, MCP guide, troubleshooting…): https://uid9622.cn/docs/

Repo: https://github.com/UID9622/longhun-system
Announcement thread: https://github.com/UID9622/longhun-system/issues/99
Readme walkthrough (guide article): https://github.com/UID9622/longhun-system/blob/main/12_DOCS/龙魂系统导读-2026-09-05.md

Feedback loop: every page footer links to a "wall of shame" issue template (GitHub), and weekly reports classify incoming issues as docs/question/suggestion/bug and drive the next iteration.

I'm posting because I'd value technical critique on the auditability mechanics more than anything else – if you build multi-agent automation, how do you currently verify agent output? Fork it, try it, file issues. Docs are signed so you can verify nothing was tampered with.

Author: Zhuge Xin | UID9622 (LongHun BeiChen) · GPG fingerprint: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
