#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-09-06-HEALTH-SYNC-NOTION-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 协议: CC BY-NC-SA 4.0（核心思想层）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""🏥 龍魂健康快照 → Notion 公开数据库同步引擎 v1.0
================================================================
架构: 本地快照(照常) → 本引擎 → Notion 数据库(公开·可查·可回溯)

三个数据库(父页: 🐉 龍魂·系统核心):
  1. 龍魂健康快照    — 每早/晚快照一行(状态/异常数/节点/边/根哈希/DNA)
  2. 拓扑变更事件    — 快照携带的 topo_events 逐条成行(关联快照)
  3. 一周健康报告    — 每周 report md 一行(状态分布/结论)

用法:
  python3 08_BIN/lh_health_sync.py init            # 建库(幂等·已存在跳过)
  python3 08_BIN/lh_health_sync.py sync [--since YYYY-MM-DD] [--quiet]  # 推送未同步快照/报告
  python3 08_BIN/lh_health_sync.py status [--json] # 库ID/已同步数/公开链接
  python3 08_BIN/lh_health_sync.py list            # 列出本地快照与已同步状态
  经 lh: lh health sync / lh health sync-init
Token 链: env NOTION_TOKEN → lh_vault get NOTION_TOKEN → ~/.codebuddy/mcp.json (同 notion MCP)
直连官方 REST · 禁代理 · Notion-Version 2025-09-03 · 指数退避(429/5xx)
"""
import argparse
import contextlib
import hashlib
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BIN = ROOT / "08_BIN"
SNAP_DIR = Path.home() / ".longhun" / "health_snapshots"
WEEKLY_DIR = Path.home() / ".longhun" / "health_weekly"
CONFIG_P = Path.home() / ".longhun" / "health_sync_config.json"
TOPO_AUDIT = Path.home() / ".longhun" / "shame_wall" / "topo_audit.jsonl"

API = "https://api.notion.com/v1"
# 注意: 工作区已升级 Notion data_source 模型(2025-09-03 header 下 database
# 响应不再含 properties→建库属性丢失)。固用 2022-06-28 兼容 header(实测:
# 建库带属性/建行/查询全链路可用·任务池6列可读)。勿升级该版本号!
VERSION = "2022-06-28"
PARENT_PAGE = "5d422c1c-3aab-44f5-8367-d7bc1f0be5ed"  # 🐉 龍魂·系统核心
GPG_FP = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
EMOJI = "🏥"

# 清理代理(直连)
for _k in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy",
           "ALL_PROXY", "all_proxy"):
    os.environ.pop(_k, None)
os.environ["NO_PROXY"] = "*"


# ─────────────────────────── token / api ───────────────────────────

def _vault_token():
    try:
        r = os.popen("python3 bin/lh_vault.py get NOTION_TOKEN 2>/dev/null").read().strip()
        return r if r and not r.lower().startswith("error") and not r.lower().startswith("🔴") else ""
    except Exception:  # noqa: BLE001
        return ""


def get_token():
    """三级 token 链: env → vault → mcp.json"""
    for name, tok in (("env", os.environ.get("NOTION_TOKEN", "").strip()),
                      ("vault", _vault_token())):
        if tok and _probe_token(tok):
            return tok
    try:
        m = json.load(open(os.path.expanduser("~/.codebuddy/mcp.json")))
        tok = m.get("mcpServers", {}).get("Notion MCP Server", {}).get("env",
                                                                       {}).get("NOTION_TOKEN", "")
        if tok:
            return tok
    except Exception:  # noqa: BLE001
        pass
    return ""


def _probe_token(tok):
    if not tok:
        return False
    try:
        req = urllib.request.Request(
            f"{API}/users/me", headers=_headers(tok))
        with urllib.request.urlopen(req, timeout=8) as r:
            return r.status == 200
    except Exception:  # noqa: BLE001
        return False


def _headers(tok):
    return {"Authorization": f"Bearer {tok}", "Notion-Version": VERSION,
            "Content-Type": "application/json"}


def _api(method, path, payload=None, tok=None, tries=4):
    """urllib 直连 + 指数退避(429/5xx) · 403/400/404 即时抛"""
    tok = tok or get_token()
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8") if payload is not None else None
    last = None
    for i in range(tries):
        req = urllib.request.Request(f"{API}{path}", data=data, headers=_headers(tok),
                                     method=method)
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                body = r.read().decode("utf-8", errors="replace")
                return r.status, (json.loads(body) if body else {})
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            code = e.code
            if code in (429,) or code >= 500:
                time.sleep(2 ** (i + 1))
                last = (code, body)
                continue
            return code, (json.loads(body) if body else {"_http": code, "_raw": body[:300]})
        except Exception as e:  # noqa: BLE001
            last = (0, str(e))
            time.sleep(1)
    return (last[0] if last else 500), {"_error": str(last[1] if last else "fail")}


# ─────────────────────────── 配置持久化 ───────────────────────────

def _load_cfg():
    if CONFIG_P.is_file():
        try:
            return json.loads(CONFIG_P.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            pass
    return {"version": "1.0", "parent_page": PARENT_PAGE, "databases": {}}


def _save_cfg(cfg):
    CONFIG_P.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_P.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")


# ─────────────────────────── init: 建库 ───────────────────────────

SCHEMA_EVENTS = {
    "标题": {"title": {}},
    "事件时间": {"date": {}},
    "操作类型": {"select": {"options": [
        {"name": "新增", "color": "green"}, {"name": "更新", "color": "yellow"},
        {"name": "移除", "color": "red"}, {"name": "其他", "color": "gray"}]}},
    "节点名称": {"rich_text": {}},
    "详情": {"rich_text": {}},
    "关联快照DNA": {"rich_text": {}},
}
SCHEMA_REPORTS = {
    "标题": {"title": {}},
    "报告周期": {"date": {}},
    "快照总数": {"number": {"format": "number"}},
    "🟢全绿": {"number": {}}, "🟡待关注": {"number": {}}, "🔴需介入": {"number": {}},
    "异常详情": {"rich_text": {}},
    "结论": {"rich_text": {}},
}
SCHEMA_SNAPS = {
    "标题": {"title": {}},
    "快照时间": {"date": {}},
    "快照类型": {"select": {"options": [
        {"name": "早", "color": "blue"}, {"name": "晚", "color": "purple"},
        {"name": "手动", "color": "gray"}]}},
    "健康状态": {"select": {"options": [
        {"name": "🟢全绿", "color": "green"}, {"name": "🟡待关注", "color": "yellow"},
        {"name": "🔴需介入", "color": "red"}]}},
    "异常项数": {"number": {"format": "number"}},
    "节点总数": {"number": {"format": "number"}},
    "边总数": {"number": {"format": "number"}},
    "根哈希": {"rich_text": {}},
    "根哈希一致": {"checkbox": {}},
    "DNA追溯码": {"rich_text": {}},
    "GPG指纹": {"rich_text": {}},
    "状态说明": {"rich_text": {}},
}


def _make_db(name, icon, schema, tok):
    payload = {"parent": {"type": "page_id", "page_id": PARENT_PAGE},
               "icon": {"type": "emoji", "emoji": icon},
               "title": [{"type": "text", "text": {"content": name}}],
               "properties": schema}
    code, body = _api("POST", "/databases", payload, tok=tok)
    if code in (200, 201):
        return body.get("id", ""), ""
    msg = json.dumps(body, ensure_ascii=False)[:200] if body else "no body"
    return "", f"HTTP {code} {msg}"


def _patch_db(db_id, props, tok):
    code, body = _api("PATCH", f"/databases/{db_id}", props, tok=tok)
    return code in (200, 201), body


def cmd_init(quiet=False):
    """建 3 库(幂等) → 配置持久化。events/reports 建后反向补 relation。"""
    tok = get_token()
    if not tok:
        print("🔴 NOTION_TOKEN 不可用(env/vault/mcp.json 均失败)")
        return 1
    cfg = _load_cfg()
    dbs = cfg.setdefault("databases", {})
    if not quiet:
        print("🏥 初始化龍魂健康快照 Notion 数据库…")

    def need(key):
        db_id = dbs.get(key)
        if db_id:
            code, _ = _api("GET", f"/databases/{db_id}", tok=tok)
            if code == 200:
                if not quiet:
                    print(f"  ⏭️  已存在 {key}: {db_id}")
                return None
        return True

    def create(key, name, icon, schema):
        db_id, err = _make_db(name, icon, schema, tok)
        if not db_id:
            return None, err
        dbs[key] = db_id
        if not quiet:
            print(f"  ✅ {name}: {db_id}")
        return db_id, ""

    # 顺序: 事件库(无relation) → 报告库 → 快照库(带 relation×2) → 反向补 relation
    if need("events"):
        db_id, err = create("events", "🧩 拓扑变更事件", "🧩", SCHEMA_EVENTS)
        if err:
            print(f"  🔴 events 建库失败: {err}")
            return 1
    if need("reports"):
        db_id, err = create("reports", "📋 一周健康报告", "📋", SCHEMA_REPORTS)
        if err:
            print(f"  🔴 reports 建库失败: {err}")
            return 1
    if need("snapshots"):
        schema = dict(SCHEMA_SNAPS)
        rels = {}
        if dbs.get("events"):
            rels["拓扑事件"] = {"relation": {"database_id": dbs["events"],
                                              "single_property": {}}, "type": "relation"}
        if dbs.get("reports"):
            rels["关联周报"] = {"relation": {"database_id": dbs["reports"],
                                              "single_property": {}}, "type": "relation"}
        schema.update(rels)
        db_id, err = create("snapshots", "🏥 龍魂健康快照", "🏥", schema)
        if err:
            print(f"  🔴 snapshots 建库失败: {err}")
            return 1
    # 反向 relation(事件库/报告库 → 快照库)
    if dbs.get("snapshots"):
        snap_id = dbs["snapshots"]
        for key, prop_name in (("events", "关联快照"), ("reports", "关联快照")):
            if dbs.get(key):
                ok, _ = _patch_db(dbs[key], {"properties": {
                    prop_name: {"relation": {"database_id": snap_id,
                                             "single_property": {}},
                                "type": "relation"}}}, tok)
                if not ok:
                    print(f"  🟡 {key} 补 relation 失败(不影响主流程)")
    _save_cfg(cfg)
    if not quiet:
        print("  📝 配置: ~/.longhun/health_sync_config.json")
        print("  ✅ init 完成 · 用 status 查看库链接")
    return 0


# ─────────────────────────── 数据提取 ───────────────────────────

def _dna(day, slot):
    h = hashlib.sha256(f"HEALTH|{day}|{slot}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{day}-{slot}-HEALTH-{h}"


def _load_snaps(since=None):
    """列出本地快照 [{day,slot,data,dna,path}] 按时间正序"""
    out = []
    for day_dir in sorted(SNAP_DIR.iterdir()) if SNAP_DIR.is_dir() else []:
        if not day_dir.is_dir() or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", day_dir.name):
            continue
        if since and day_dir.name < since:
            continue
        for slot in ("07", "21"):
            p = day_dir / f"{slot}.json"
            if not p.is_file():
                continue
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
            except Exception:  # noqa: BLE001
                continue
            day = day_dir.name
            out.append({"day": day, "slot": slot, "data": data,
                        "dna": _dna(day, slot), "path": p})
    return out


def _load_reports(since=None):
    out = []
    if WEEKLY_DIR.is_dir():
        for p in sorted(WEEKLY_DIR.glob("health_report_*.md")):
            m = re.search(r"health_report_(\d{4}-\d{2}-\d{2})\.md$", p.name)
            if not m:
                continue
            if since and m.group(1) < since:
                continue
            out.append({"end": m.group(1), "name": p.name, "path": p,
                        "txt": p.read_text(encoding="utf-8", errors="ignore")})
    return out


def _fmt_ts(iso):
    """2026-09-06T07:00:00+08:00 → 2026-09-06T07:00:00(去 tz 截断 Notion date 时间部分)"""
    return str(iso)[:16] if iso else ""


# ─────────────────────────── 查询已同步(幂等) ───────────────────────────

def _query_exists(db_id, prop, value, tok):
    """filter: 属性文本精确匹配 → 返回 page id 列表"""
    payload = {"filter": {"property": prop, "rich_text": {"equals": value}}}
    page_size = 100
    code, body = _api("POST", f"/databases/{db_id}/query", payload, tok=tok)
    if code != 200:
        return []
    ids = [r["id"] for r in body.get("results", [])]
    return ids


# ─────────────────────────── 推送行 ───────────────────────────

def _create_row(db_id, props, children=None, tok=None):
    payload = {"parent": {"database_id": db_id}, "properties": props}
    if children:
        payload["children"] = children
    code, body = _api("POST", "/pages", payload, tok=tok)
    if code in (200, 201):
        return body.get("id", ""), ""
    return "", f"HTTP {code} {json.dumps(body, ensure_ascii=False)[:200]}"


def _sel(name):
    return {"select": {"name": name}}


def _txt(content, limit=1990):
    s = str(content or "")[:limit]
    return {"rich_text": [{"text": {"content": s}}]}


def _n(v):
    return {"number": int(v or 0)}


def cmd_sync(since=None, quiet=False):
    tok = get_token()
    if not tok:
        print("🔴 NOTION_TOKEN 不可用")
        return 1
    cfg = _load_cfg()
    dbs = cfg.get("databases", {})
    if not (dbs.get("snapshots") and dbs.get("events")):
        print("🟡 数据库未初始化 · 先跑: lh health sync-init (或 python3 08_BIN/lh_health_sync.py init)")
        return 2

    # ── 1. 快照 → 主库 ──
    snaps = _load_snaps(since)
    done = pending = 0
    snap_pages = {}  # day|slot → page id(供 events/reports relation)
    for s in snaps:
        if _query_exists(dbs["snapshots"], "DNA追溯码", s["dna"], tok):
            done += 1
            continue
        data = s["data"]
        status = str(data.get("status", ""))
        st_sel = {"🟢": "🟢全绿", "🟡": "🟡待关注", "🔴": "🔴需介入"}.get(status, "🟡待关注")
        slot_sel = {"07": "早", "21": "晚"}.get(s["slot"], "手动")
        issues = [c for c in data.get("health_checks", [])
                  if (c.get("mark") or "🟢") != "🟢"]
        topo = data.get("topo", {})
        props = {
            "标题": {"title": [{"text": {"content":
                f"{s['day']} {slot_sel}{s['slot']} · {status} {st_sel}"}}]},
            "快照时间": {"date": {"start": _fmt_ts(data.get("ts") or
                                                   f"{s['day']}T{'07' if s['slot']=='07' else '21'}:00:00")}},
            "快照类型": _sel(slot_sel), "健康状态": _sel(st_sel),
            "异常项数": _n(len(issues)), "节点总数": _n(topo.get("nodes", 0)),
            "边总数": _n(topo.get("edges", 0)),
            "根哈希": _txt(topo.get("root_hash", "")),
            "根哈希一致": {"checkbox": bool(topo.get("online_ok", True))},
            "DNA追溯码": _txt(s["dna"]), "GPG指纹": _txt(GPG_FP),
            "状态说明": _txt(data.get("reason", ""), 300),
        }
        # relation 到事件/报告(可为空)
        issues_txt = json.dumps([{"name": c.get("name"), "mark": c.get("mark"),
                                  "ok": c.get("ok")} for c in issues][:8],
                                ensure_ascii=False)
        children = [{"object": "block", "type": "code", "code": {
            "caption": [], "rich_text": [{"text": {"content":
                f"🟢{data.get('health_summary', {}).get('ok', 0)} "
                f"🟡{data.get('health_summary', {}).get('warn', 0)} "
                f"🔴{data.get('health_summary', {}).get('fail', 0)} 异常项: {issues_txt}"}}],
            "language": "json"}}]
        page_id, err = _create_row(dbs["snapshots"], props, children=children, tok=tok)
        if page_id:
            snap_pages[f"{s['day']}|{s['slot']}"] = page_id
            pending += 1
            if not quiet:
                print(f"  ✅ 快照 {s['day']} {s['slot']} → {page_id[:8]}…")
        else:
            print(f"  🔴 快照 {s['day']} {s['slot']} 推送失败: {err}")
            if not quiet:
                pass

    # ── 2. topo_events → 事件库 ──
    ev_done = 0
    for s in snaps:
        if f"{s['day']}|{s['slot']}" not in snap_pages:
            continue
        page_id = snap_pages[f"{s['day']}|{s['slot']}"]
        for ev in s["data"].get("topo_events", []):
            ts_raw = str(ev.get("ts", ""))
            key = f"{s['day']}|{s['slot']}|{hashlib.sha256(str(ev.get('detail','')).encode()).hexdigest()[:12]}"
            if _query_exists(dbs["events"], "关联快照DNA", key, tok):
                continue
            op = "其他"
            det = str(ev.get("detail", ""))[:180]
            if "add" in str(ev.get("ops")) or re.search(r"新增", det):
                op = "新增"
            elif "remove" in str(ev.get("ops")) or re.search(r"移除", det):
                op = "移除"
            elif "update" in str(ev.get("ops")) or re.search(r"更新", det):
                op = "更新"
            props = {
                "标题": {"title": [{"text": {"content":
                    f"{_fmt_ts(ts_raw) or s['day']} · {op} · {det[:40]}"}}]},
                "事件时间": {"date": {"start": _fmt_ts(ts_raw) or s["day"]}},
                "操作类型": _sel(op),
                "节点名称": _txt(re.sub(r"[新增更新移除·：]", "", det)[:60]),
                "详情": _txt(det),
                "关联快照DNA": _txt(key),
                "关联快照": {"relation": [{"id": page_id}]},
            }
            pid, err = _create_row(dbs["events"], props, tok=tok)
            if pid:
                ev_done += 1
            else:
                print(f"  🟡 事件推送失败: {err}")

    # ── 3. 周报 → 报告库 ──
    rp_done = 0
    if dbs.get("reports"):
        for rep in _load_reports(since):
            if _query_exists(dbs["reports"], "标题", rep["name"], tok):
                done += 1
                continue
            g = {"🟢全绿": 0, "🟡待关注": 0, "🔴需介入": 0}
            ex = ""
            m_end = re.search(r"健康报告\s*([\s\S]*?)\s*\n", rep["txt"])
            for line in rep["txt"].splitlines():
                m = re.search(r"-\s*(🟢|🟡|🔴)\s*([^:：]*?)\s*[:：]\s*(\d+)", line)
                if m:
                    mark_map = {"🟢": "🟢全绿", "🟡": "🟡待关注", "🔴": "🔴需介入"}
                    g[mark_map[m.group(1)]] = int(m.group(3))
                if line.startswith("  - "):
                    ex += line.strip() + "\n"
            concl = ""
            for line in rep["txt"].splitlines():
                if line.startswith("🟢") and "本周正常" in line:
                    concl = line[:250]
                elif line.startswith("🟡") or line.startswith("🔴"):
                    if not concl:
                        concl = line[:250]
            # 关联本周快照(到报告周日为止 ≤7天)
            end_d = datetime.strptime(rep["end"], "%Y-%m-%d")
            start_d = end_d - timedelta(days=6)
            rel_ids = [s for k, s in snap_pages.items() if start_d.strftime(
                "%Y-%m-%d") <= k[:10] <= rep["end"]]
            props = {
                "标题": {"title": [{"text": {"content": rep["name"]}}]},
                "报告周期": {"date": {"start": start_d.strftime("%Y-%m-%d"),
                                       "end": rep["end"]}},
                "快照总数": _n(sum(g.values())),
                "🟢全绿": _n(g["🟢全绿"]), "🟡待关注": _n(g["🟡待关注"]),
                "🔴需介入": _n(g["🔴需介入"]),
                "异常详情": _txt(ex[:1990]), "结论": _txt(concl),
                "关联快照": {"relation": [{"id": i} for i in rel_ids]},
            }
            pid, err = _create_row(dbs["reports"], props, tok=tok)
            if pid:
                rp_done += 1
                if not quiet:
                    print(f"  ✅ 报告 {rep['name']} → {pid[:8]}…")
            else:
                print(f"  🔴 报告推送失败: {err}")
    if not quiet:
        print(f"  📊 快照: 新增 {pending} · 已同步 {done} | 事件: +{ev_done} | 报告: +{rp_done}")
    return 0


# ─────────────────────────── status / list ───────────────────────────

def cmd_status(json_out=False):
    cfg = _load_cfg()
    dbs = cfg.get("databases", {})
    out = {"config": str(CONFIG_P), "databases": {}}
    for key in ("snapshots", "events", "reports"):
        db_id = dbs.get(key, "")
        out["databases"][key] = {"id": db_id, "url": f"https://www.notion.so/{db_id.replace('-','')}" if db_id else ""}
    tok = get_token()
    if json_out:
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0
    print("🏥 健康快照 → Notion 同步状态")
    for key, meta in out["databases"].items():
        mark = "✅" if meta["id"] else "❌"
        print(f"  {mark} {key}: {meta['url'] or '未初始化'}")
    snaps = _load_snaps()
    done = 0
    if tok and dbs.get("snapshots"):
        for s in snaps:
            if _query_exists(dbs["snapshots"], "DNA追溯码", s["dna"], tok):
                done += 1
    print(f"  本地快照 {len(snaps)} 条 · Notion 已同步 {done} 条")
    print(f"  公开化提示: 打开上述数据库页面 → Share → Publish(手动一步)")
    return 0


def cmd_list():
    snaps = _load_snaps()
    cfg = _load_cfg()
    snap_db = cfg.get("databases", {}).get("snapshots", "")
    tok = get_token()
    print(f"本地健康快照 ({len(snaps)} 条):")
    for s in snaps:
        st = s["data"].get("status", "?")
        synced = ""
        if tok and snap_db:
            synced = " ✅已同步" if _query_exists(snap_db, "DNA追溯码", s["dna"], tok) else ""
        print(f"  {s['day']} {s['slot']} · {st} · {s['dna']}{synced}")
    return 0


# ─────────────────────────── main ───────────────────────────

def main():
    ap = argparse.ArgumentParser(description="龍魂健康快照 → Notion 公开数据库 (lh health sync)")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("init", help="创建三个数据库(幂等)")
    s = sub.add_parser("sync", help="推送未同步快照/事件/周报到 Notion")
    s.add_argument("--since", default="", help="只推该日期(YYYY-MM-DD)之后")
    s.add_argument("--quiet", action="store_true")
    sub.add_parser("status", help="库状态/链接")
    st = sub.add_parser("list", help="本地快照与同步状态")
    st.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if args.cmd == "init":
        return cmd_init()
    if args.cmd == "sync":
        return cmd_sync(since=args.since, quiet=args.quiet)
    if args.cmd == "status":
        return cmd_status()
    if args.cmd == "list":
        return cmd_list()
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
