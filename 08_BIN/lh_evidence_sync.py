#!/usr/bin/env python3
# DNA: #龍芯⚡️2026-09-05-EVIDENCE-CHAIN-SYNC-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 配套: 07_AUDIT/LH-AUDIT-CHAIN-AUDIT-REPORT-2026-09-05.md（v1.1 中立执行清单 阶段A）
"""
🐉 LH-EVIDENCE-CHAIN v1.0 — 龍魂开源生态证据链同步引擎（阶段A落地·薄封装复用现有引擎）

核心逻辑（v1.1 中立骨架）:
  新条目 → URL快照|文本哈希(SHA-256) → 三色状态机 → 数字人审核JSON回写 → Notion行
  审计对象 = 龍魂生态自身事务（承诺兑现/bounty/roadmap/修复/贡献者协作），不做对外政治定性。

状态机:
  🕐评估中  →(快照+哈希锚定成功)→ 🟢已锚定[三色🟢] / 快照失败→🟡协作核验
  🟡协作核验 →(数字人≥1审+14天内)→ 🟡 或 🟢   · 数字人超时(14d无审) → ⏳逾期
  承诺类(due过期) → ⏳逾期 · due+14d仍无进展 → 🔴未兑现(耻辱墙冻结态标记·不删除)

数据主权: 台账本地 ~/.longhun/evidence/（append-only·哈希链封链）· Notion 为只推脱敏镜像
用法:
  lh evidence add --kind pledge|node --title "..." [--type roadmap|bounty|发布|修复|社区协作|其他]
                  [--party 承诺方] [--url https://...] [--text "原文"] [--due YYYY-MM-DD] [--no-notion]
  lh evidence list [--kind pledge|node] [--status 🟢|🟡|⏳|🔴]
  lh evidence sync            # 状态机推进：due过期→⏳逾期 · 14d无审升级 · 哈希链重封
  lh evidence review <id>     # 数字人四审（知行·明鉴·包青天·诗仙）JSON回写
  lh evidence status          # 台账统计 + 链根哈希
  lh evidence verify          # 哈希链完整性校验
"""

import argparse
import contextlib
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EV_DIR = Path.home() / ".longhun" / "evidence"
SNAP_DIR = EV_DIR / "snapshots"
LEDGER = EV_DIR / "pledges.json"
CHAIN = EV_DIR / "chain.json"

# Notion 库（2026-09-05 建 · 父=🌌元宇宙·开源生态 3fe6db2f-6a5d-4647-8198-6df0eb02ccd7）
DB_PLEDGE = "3d27125a-9c9f-8167-98c5-cecdbd83a1a6"
DB_NODE = "3d27125a-9c9f-8175-bc07-d7c4e65d1238"
NOTION_URL = "https://api.notion.com/v1"
PERSONA_JAIL = 30  # 天：🔴未兑现提示阈值（due+14d 评估 → 满30d落耻辱墙冻结标记）

REVIEW_TEAM = [  # 数字人审核编队（v1.1：对龍魂生态事务核验，非对外指控）
    ("知行", "影响/进展评估"),
    ("明鉴", "技术核验"),
    ("包青天", "逻辑/真实性审计"),
    ("诗仙", "摘要与表述"),
]

# 状态机流转规则（拓扑快照静态定义·与引擎语义同源）
STATE_RULES = [
    {"from": "🕐评估(新录入)", "to": "🟢已锚定", "rule": "URL快照+SHA-256内容哈希成功 · color=🟢"},
    {"from": "🕐评估(新录入)", "to": "🟡协作核验", "rule": "快照失败仅条目锚定哈希(诚实标注非内容哈希)"},
    {"from": "🟡协作核验", "to": "🟢已锚定", "rule": "数字人≥1审通过(lh evidence review) · color=🟢"},
    {"from": "🟡协作核验", "to": "⏳逾期", "rule": "14天无任何数字人审核(sync 升级)"},
    {"from": "🟢已锚定/🟡协作核验(承诺类)", "to": "⏳逾期", "rule": "due < 今天(sync 扫描)"},
    {"from": "⏳逾期", "to": "🔴未兑现", "rule": "due+30天仍无进展 → 耻辱墙冻结态标记(不删除只冻结)"},
    {"from": "🟢/🟡(协作节点)", "to": "🟢活跃/🟡休眠", "rule": "节点按快照与协作活跃度评估"},
]

# Notion 两库属性定义（2026-09-05 建 · 父=🌌元宇宙·开源生态收纳页）
DB_SCHEMA = [
    {"库": "🟡龍魂生态承诺追踪库", "db_id": "3d27125a-9c9f-8167-98c5-cecdbd83a1a6",
     "parent": "🌌元宇宙·开源生态(3fe6db2f-6a5d-4647-8198-6df0eb02ccd7)",
     "属性": ["承诺", "承诺类型", "承诺方", "状态", "三色", "来源URL", "证据哈希",
              "承诺日期", "截止日期", "验证数字人", "审核JSON", "DNA", "备注"]},
    {"库": "📋龍魂生态协作节点库", "db_id": "3d27125a-9c9f-8175-bc07-d7c4e65d1238",
     "parent": "🌌元宇宙·开源生态(3fe6db2f-6a5d-4647-8198-6df0eb02ccd7)",
     "属性": ["节点名称", "节点类型", "协作领域", "协作状态", "铭碑哈希", "加入日期", "主页", "备注"]},
]


def _token() -> str:
    """vault 读取 Notion token（不落盘不打印）。"""
    r = subprocess.run(["python3", "bin/lh_vault.py", "get", "NOTION_TOKEN"],
                       capture_output=True, text=True, cwd=str(ROOT))
    out = r.stdout.strip()
    if not out:
        return ""
    lines = [ln for ln in out.splitlines() if ln.strip()]
    return lines[-1].strip() if lines else ""


def _notion(method, path, body=None):
    tok = _token()
    if not tok or len(tok) < 30:
        return None, {"error": "no token"}
    req = urllib.request.Request(f"{NOTION_URL}/{path}", method=method)
    req.add_header("Authorization", f"Bearer {tok}")
    req.add_header("Notion-Version", "2022-06-28")
    req.add_header("Content-Type", "application/json")
    data = json.dumps(body).encode() if body is not None else None
    try:
        with urllib.request.urlopen(req, data=data) as resp:
            return resp.status, json.loads(resp.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode() or "{}")


def sha256_of(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _clean_env():
    env = {k: v for k, v in os.environ.items()
           if not k.upper() in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY",
                                "http_proxy", "https_proxy", "all_proxy")}
    return env


def snapshot(url: str, text: str = "") -> dict:
    """URL快照|文本存证 → {sha256, kind, saved, title_probe}。"""
    if url:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "longhun-evidence/1.0"})
            with urllib.request.urlopen(req, timeout=25,
                                        context=None) as resp:
                raw = resp.read()
            kind = "url"
        except Exception as e:  # noqa: BLE001
            return {"ok": False, "error": f"url fetch: {e}"}
    else:
        raw = (text or "").encode("utf-8")
        kind = "text"
    h = sha256_of(raw)
    SNAP_DIR.mkdir(parents=True, exist_ok=True)
    ext = ".html" if kind == "url" else ".txt"
    f = SNAP_DIR / f"{h}{ext}"
    if not f.exists():
        f.write_bytes(raw)
    title = ""
    m = re.search(rb"<title[^>]*>(.*?)</title>", raw[:20000], re.S | re.I)
    if m:
        with contextlib.suppress(Exception):
            title = m.group(1).decode("utf-8", "ignore")[:200]
    return {"ok": True, "sha256": h, "kind": kind, "saved_to": str(f),
            "bytes": len(raw), "title_probe": title}


def load_ledger() -> list:
    if LEDGER.exists():
        with LEDGER.open(encoding="utf-8") as fh:
            try:
                return json.load(fh)
            except json.JSONDecodeError:
                return []
    return []


def save_ledger(rows: list):
    EV_DIR.mkdir(parents=True, exist_ok=True)
    tmp = LEDGER.with_suffix(".tmp")
    tmp.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(LEDGER)


def seal_chain(rows: list):
    """哈希链封链：每条含 prev_hash，root=末条。"""
    prev = ""
    for r in rows:
        h = sha256_of(json.dumps(
            {k: r.get(k) for k in ("id", "kind", "title", "sha256", "status", "updated")},
            ensure_ascii=False).encode())
        r["hash"] = h
        r["prev_hash"] = prev
        prev = h
    save_ledger(rows)          # 封链后统一落盘（hash/prev_hash 必须与台账同存）
    EV_DIR.mkdir(parents=True, exist_ok=True)
    CHAIN.write_text(json.dumps({
        "chain": "longhun-evidence-hashchain-v1",
        "count": len(rows),
        "last_id": rows[-1].get("id") if rows else None,
        "root_hash": prev,
        "sealed_at": datetime.now().isoformat(timespec="seconds"),
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    # ── 公开镜像导出（lh-api 只读端点同源·同 shamewall 模式）────────
    try:
        mir = {"tool": "lh-evidence-api", "chain": "longhun-evidence-hashchain-v1",
               "count": len(rows), "root_hash": prev,
               "sealed_at": datetime.now().isoformat(timespec="seconds"),
               "records": [{"id": r.get("id"), "kind": r.get("kind"),
                            "title": r.get("title"), "status": r.get("status"),
                            "color": r.get("color", ""), "sha256": (r.get("sha256") or "")[:16],
                            "review": r.get("review", ""), "updated": r.get("updated")}
                           for r in rows]}
        out = ROOT / "data" / "evidence.json"
        out.parent.mkdir(exist_ok=True, parents=True)
        out.write_text(json.dumps(mir, ensure_ascii=False, indent=1), encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass


def new_id() -> str:
    return f"EVD-{datetime.now().strftime('%Y%m%d%H%M%S')}-{int(time.time() * 1000) % 10000}"


def three_color(snap: dict, has_url: bool) -> str:
    """三色判定：快照+哈希锚定=🟢证据态；仅描述无锚=🟡协作核验。"""
    return "🟢" if snap.get("ok") and has_url else "🟡"


def _notion_props(kind: str, rec: dict) -> dict:
    if kind == "pledge":
        p = {"承诺": {"title": [{"text": {"content": rec["title"]}}]}}
        if rec.get("etype"):
            p["承诺类型"] = {"select": {"name": rec["etype"]}}
        if rec.get("party"):
            p["承诺方"] = {"rich_text": [{"text": {"content": rec["party"][:1999]}}]}
        if rec.get("status"):
            p["状态"] = {"select": {"name": rec["status"]}}
        if rec.get("color"):
            p["三色"] = {"select": {"name": rec["color"]}}
        if rec.get("url"):
            p["来源URL"] = {"url": rec["url"]}
        if rec.get("sha256"):
            p["证据哈希"] = {"rich_text": [{"text": {"content": rec["sha256"]}}]}
        if rec.get("cd"):
            p["承诺日期"] = {"date": {"start": rec["cd"]}}
        if rec.get("due"):
            p["截止日期"] = {"date": {"start": rec["due"]}}
        if rec.get("review"):
            p["验证数字人"] = {"rich_text": [{"text": {"content": rec["review"][:1999]}}]}
        if rec.get("review_json"):
            p["审核JSON"] = {"rich_text": [{"text": {"content": rec["review_json"][:1999]}}]}
        if rec.get("dna"):
            p["DNA"] = {"rich_text": [{"text": {"content": rec["dna"]}}]}
        if rec.get("note"):
            p["备注"] = {"rich_text": [{"text": {"content": rec["note"][:1999]}}]}
        return p
    p = {"节点名称": {"title": [{"text": {"content": rec["title"]}}]}}
    if rec.get("ntype"):
        p["节点类型"] = {"select": {"name": rec["ntype"]}}
    if rec.get("fields"):
        p["协作领域"] = {"multi_select": [{"name": x} for x in rec["fields"]]}
    if rec.get("status"):
        p["协作状态"] = {"select": {"name": rec["status"]}}
    if rec.get("sha256"):
        p["铭碑哈希"] = {"rich_text": [{"text": {"content": rec["sha256"]}}]}
    if rec.get("cd"):
        p["加入日期"] = {"date": {"start": rec["cd"]}}
    if rec.get("url"):
        p["主页"] = {"url": rec["url"]}
    if rec.get("note"):
        p["备注"] = {"rich_text": [{"text": {"content": rec["note"][:1999]}}]}
    return p


def notion_push(kind: str, rec: dict) -> tuple:
    db = DB_PLEDGE if kind == "pledge" else DB_NODE
    st, body = _notion("POST", "pages",
                       {"parent": {"database_id": db},
                        "properties": _notion_props(kind, rec)})
    return st, body


def review_by_digital_humans(rec: dict) -> dict:
    """四数字人协同审核（复用 lh_dh_dispatch 链路·API不可用降级唤起指令）。"""
    sys.path.insert(0, str(ROOT / "08_BIN"))
    out = {}
    try:
        from lh_dh_dispatch import build_system, try_deepseek  # noqa: PLC0415
        for dh, duty in REVIEW_TEAM:
            messages = build_system(
                {"ipa": dh, "name": dh,
                 "metadata": {"persona": dh, "principle": f"龍魂生态证据核验·{duty}"}},
                f"核验龍魂生态证据条目: {rec.get('title','')} | 证据哈希: {rec.get('sha256','')} | "
                f"类型: {rec.get('etype','')} 状态: {rec.get('status','')} | 请输出精简结论(三色+依据)"
                if rec.get("kind") == "pledge" else
                f"核验龍魂协作节点: {rec.get('title','')} | 类型: {rec.get('ntype','')} | "
                f"请输出协作价值评估")
            resp = try_deepseek(messages)
            if isinstance(resp, tuple):
                out[dh] = {"mode": "fallback", "error": resp[1][:300]}
            else:
                out[dh] = {"mode": "ok", "response": (resp or "")[:800]}
        return {"reviews": out, "digits": len(out), "at": datetime.now().isoformat(timespec="seconds")}
    except Exception as e:  # noqa: BLE001
        return {"reviews": {}, "error": str(e)}


# ═══════════════════════ 子命令 ═══════════════════════
def cmd_add(args):
    rows = load_ledger()
    kind = args.kind
    if kind not in ("pledge", "node"):
        print("🔴 kind 须为 pledge|node"); return
    if not args.title:
        print("🔴 缺 --title"); return
    snap = snapshot(args.url or "", args.text or "")
    if not snap.get("ok") and not args.text:
        print(f"🟡 快照失败（{snap.get('error','')}）· 用条目锚定哈希兜底，状态=协作核验")
    rec = {"id": new_id(), "kind": kind, "title": args.title, "url": args.url or "",
           "text": args.text or "",
           "created": datetime.now().isoformat(timespec="seconds"),
           "cd": date.today().isoformat(), "updated": datetime.now().isoformat(timespec="seconds"),
           "note": args.note or ""}
    if snap.get("ok"):
        rec["sha256"] = snap["sha256"]
    else:
        rec["sha256"] = sha256_of(f"{args.title}|{args.url}|{rec['created']}".encode())
        rec["note"] = (rec["note"] + " ·快照失败·哈希为条目锚定(非内容哈希)").strip()
    if kind == "pledge":
        rec.update(etype=args.etype, party=args.party, due=args.due or "",
                   status="🟢已锚定" if snap.get("ok") and args.url else "🟡协作核验",
                   color=three_color(snap, bool(args.url)),
                   review="", review_json="")
    else:
        rec.update(ntype=args.ntype, fields=(args.fields or "代码").split(","),
                   status="🟢活跃" if snap.get("ok") else "🟡休眠")
    rec["dna"] = f"#龍芯⚡️2026-09-05-EVIDENCE-{rec['id']}"
    rows.append(rec)
    seal_chain(rows)
    if not args.no_notion:
        st, body = notion_push(kind, rec)
        st_txt = "✅" if st in (200, 201) else f"🔴{st} {body.get('code','')}"
        print(f"Notion推送到镜像: {st_txt}")
        if st not in (200, 201):
            print("  ⚠️ 本地台账已存 · Notion失败原因:", str(body)[:300])
    print(f"🆕 {rec['id']} | {rec['title']} | sha256={rec['sha256'][:16]}… | 状态={rec.get('status')} 三色={rec.get('color','-')}")
    if rec["sha256"]:
        print(f"🔗 快照: {SNAP_DIR / (rec['sha256'] + ('.html' if args.url else '.txt'))}")
    print(f"🧱 链根哈希: {CHAIN.read_text(encoding='utf-8') and json.loads(CHAIN.read_text(encoding='utf-8')).get('root_hash','')}")


def cmd_list(args):
    rows = load_ledger()
    flt = [r for r in rows if (not args.kind or r.get("kind") == args.kind)
           and (not args.status or r.get("status") == args.status)]
    if not flt:
        print(f"（空）台账共 {len(rows)} 条")
        return
    print(f"台账共 {len(rows)} 条 · 命中 {len(flt)}")
    for r in flt[-25:]:
        tag = {"pledge": "🟡承诺", "node": "📋节点"}.get(r.get("kind"), "?")
        print(f"  {r.get('id')} {tag} [{r.get('status','')}/{r.get('color','-')}] {r.get('title','')[:50]}")
    if len(flt) > 25:
        print(f"  …共 {len(flt)} 条，仅显示最近 25")


def cmd_sync(args):
    rows = load_ledger()
    today = date.today()
    moved = 0
    for r in rows:
        old = r.get("status")
        if r.get("kind") == "pledge":
            due = r.get("due") or ""
            try:
                due_d = date.fromisoformat(due) if due else None
            except ValueError:
                due_d = None
            if r.get("status") in ("🟢已锚定", "🟡协作核验") and due_d and due_d < today:
                r["status"] = "⏳逾期"
            if r.get("status") == "⏳逾期" and due_d and (today - due_d).days >= PERSONA_JAIL:
                r["status"] = "🔴未兑现"
                r["note"] = (r.get("note", "") + " ·🔴未兑现超期冻结标记(不删除只冻结)").strip()
            if r.get("status") == "🟡协作核验":
                upd = r.get("updated", r.get("created", ""))
                with contextlib.suppress(Exception):
                    upd_d = datetime.fromisoformat(upd).date()
                    if (today - upd_d).days >= 14 and not r.get("review_json"):
                        r["status"] = "⏳逾期"
        if r.get("status") != old:
            r["updated"] = datetime.now().isoformat(timespec="seconds")
            moved += 1
    if moved:
        seal_chain(rows)
    print(f"✅ 状态机推进 {moved} 条 · 台账 {len(rows)} 条")
    cmd_status(args)


def cmd_review(args):
    rows = load_ledger()
    rec = next((r for r in rows if r.get("id") == args.id or r.get("title") == args.id), None)
    if not rec:
        print(f"🔴 未找到 {args.id}"); return
    print(f"🧑⚖️ 数字人四审启动: {rec['id']} · {rec.get('title','')[:40]}")
    res = review_by_digital_humans(rec)
    rec["review_json"] = json.dumps(res, ensure_ascii=False)
    names = "、".join(res.get("reviews", {}).keys()) or "（未就绪·唤起指令降级）"
    rec["review"] = names
    rec["updated"] = datetime.now().isoformat(timespec="seconds")
    if res.get("reviews") and rec.get("status") == "🟡协作核验":
        rec["status"] = "🟢已锚定"
        rec["color"] = "🟢"
    seal_chain(rows)
    for dh, v in res.get("reviews", {}).items():
        mode = v.get("mode")
        if mode == "ok":
            print(f"  ✅ {dh}: {str(v.get('response',''))[:90]}")
        else:
            print(f"  🟡 {dh}: 降级 {str(v.get('error',''))[:90]}")
    if not res.get("reviews"):
        print("  ⚠️ API未就绪·审核JSON已留空槽(文本已记录唤起指令):", str(res.get("error", ""))[:200])
    if not args.no_notion and rec.get("kind") == "pledge":
        st, body = _notion("POST", "pages", {
            "parent": {"database_id": DB_PLEDGE},
            "properties": {"承诺": {"title": [{"text": {"content": rec["title"]}}]},
                           "验证数字人": {"rich_text": [{"text": {"content": rec["review"][:1999]}}]},
                           "审核JSON": {"rich_text": [{"text": {"content": rec["review_json"][:1999]}}]}}})
        print("  Notion审核回写:", "✅" if st in (200, 201) else f"🔴{st}")


def cmd_status(args):
    rows = load_ledger()
    chain = {}
    if CHAIN.exists():
        with CHAIN.open(encoding="utf-8") as fh:
            chain = json.load(fh)
    kinds = {}
    for r in rows:
        kinds.setdefault(r.get("kind"), 0)
        kinds[r.get("kind")] += 1
    print(f"台账: {len(rows)} 条（pledge={kinds.get('pledge',0)} · node={kinds.get('node',0)}）")
    print(f"链根哈希: {chain.get('root_hash','(空)')} · 上次封链: {chain.get('sealed_at','-')}")
    print(f"快照目录: {SNAP_DIR}")


def cmd_snapshot(args):
    """lh evidence snapshot — 证据链完整拓扑快照（schema+示例+状态机+台账·任务2 交付物）"""
    rows = load_ledger()
    chain = {}
    if CHAIN.exists():
        with CHAIN.open(encoding="utf-8") as fh:
            chain = json.load(fh)
    snap = {
        "schema": "longhun-evidence-topology-v1",
        "owner": "诸葛鑫 | UID9622 · 龍芯北辰",
        "service": "lh evidence snapshot · LH-AUDIT-CHAIN 阶段A 拓扑交付",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "chain": {"name": chain.get("chain", "longhun-evidence-hashchain-v1"),
                  "count": len(rows),
                  "root_hash": chain.get("root_hash", ""),
                  "sealed_at": chain.get("sealed_at", "")},
        "databases": DB_SCHEMA,
        "state_machine": STATE_RULES,
        "review_team": [{"数字人": dh, "职责": duty} for dh, duty in REVIEW_TEAM],
        "color_map": {"🟢": "已锚定/活跃", "🟡": "协作核验/休眠", "⏳": "逾期", "🔴": "未兑现(冻结)"},
        "records": rows,
        "example": [{
            "库": "🟡龍魂生态承诺追踪库",
            "id": "EVD-20260905221341-1641",
            "title": "CNSH生态完整规划·P1窗口任务状态回填",
            "etype": "roadmap", "party": "龍魂开源生态",
            "status": "🟢已锚定", "color": "🟢",
            "sha256": "80578c4013f940f44d2b1386c0564d7fe…",
            "due": "2026-09-15",
            "dna": "#龍芯⚡️2026-09-05-EVIDENCE-EVD-20260905221341-1641",
            "note": "知识库 5a8427b8 内 P1-T1~T4 状态待老大报实际进度回填(不编造)"},
            {"库": "📋龍魂生态协作节点库", "字段示例": "节点名称/节点类型/协作领域/协作状态/铭碑哈希/加入日期/主页/备注（待真实协作节点录入）"}],
    }
    out = ROOT / "data" / "evidence_topology_snapshot.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(".tmp")
    tmp.write_text(json.dumps(snap, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(out)
    print(f"✅ 拓扑快照生成 {out}")
    print(f"   schema={snap['schema']} · 记录 {len(rows)} · 链根 {snap['chain']['root_hash'][:16]}…"
          f" · 库 {len(DB_SCHEMA)} · 状态机规则 {len(STATE_RULES)}")


def cmd_verify(args):
    rows = load_ledger()
    prev, bad = "", 0
    for r in rows:
        h = sha256_of(json.dumps(
            {k: r.get(k) for k in ("id", "kind", "title", "sha256", "status", "updated")},
            ensure_ascii=False).encode())
        if r.get("hash") != h or r.get("prev_hash") != prev:
            bad += 1
        prev = r.get("hash", "")
    chain = {}
    if CHAIN.exists():
        with CHAIN.open(encoding="utf-8") as fh:
            chain = json.load(fh)
    ok = (bad == 0) and (chain.get("root_hash") == prev)
    print(f"{'🟢 链完整' if ok else '🔴 链破损'} · {len(rows)}条 · 异常{bad} · root={prev[:16]}…")
    print(("✅ 与 chain.json 一致" if ok else "❌ 与 chain.json 不一致"))


def main():
    ap = argparse.ArgumentParser(prog="lh evidence", description="龍魂生态证据链同步 v1.0")
    sub = ap.add_subparsers(dest="cmd")
    a = sub.add_parser("add"); a.add_argument("--kind", choices=["pledge", "node"], default="pledge")
    a.add_argument("--title", required=True); a.add_argument("--type", dest="etype", default="roadmap")
    a.add_argument("--party", default="龍魂开源生态"); a.add_argument("--url", default="")
    a.add_argument("--text", default=""); a.add_argument("--due", default="")
    a.add_argument("--ntype", default="个人贡献者"); a.add_argument("--fields", default="代码")
    a.add_argument("--note", default=""); a.add_argument("--no-notion", action="store_true")
    a.set_defaults(fn=cmd_add)
    s = sub.add_parser("list"); s.add_argument("--kind"); s.add_argument("--status")
    s.set_defaults(fn=cmd_list)
    s = sub.add_parser("sync"); s.set_defaults(fn=cmd_sync)
    r = sub.add_parser("review"); r.add_argument("id"); r.add_argument("--no-notion", action="store_true")
    r.set_defaults(fn=cmd_review)
    s = sub.add_parser("status"); s.set_defaults(fn=cmd_status)
    s = sub.add_parser("snapshot"); s.set_defaults(fn=cmd_snapshot)
    v = sub.add_parser("verify"); v.set_defaults(fn=cmd_verify)
    args = ap.parse_args()
    if not getattr(args, "fn", None):
        ap.print_help(); return
    args.fn(args)


if __name__ == "__main__":
    main()
