# -*- coding: utf-8 -*-
"""
龍芯家族花名册 · Notion → 本机大脑镜像
正本: https://www.notion.so/4cf99c3e7a014e919fdab705ceb4cbc4
DNA: #龍芯⚡️2026-05-16-ROSTER-NOTION-SYNC-v1.0
"""
from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).resolve().parent / ".env")
except ImportError:
    pass

import httpx

NOTION_TOKEN = os.getenv("NOTION_TOKEN", "")
NOTION_VERSION = os.getenv("NOTION_VERSION", "2022-06-28")
ROSTER_DB_ID = os.getenv(
    "NOTION_ROSTER_DB_ID",
    "4cf99c3e7a014e919fdab705ceb4cbc4",
).replace("-", "")

CACHE_DIR = Path.home() / ".longhun" / "roster"
CACHE_FILE = CACHE_DIR / "notion_mirror.json"
ALERT_FILE = CACHE_DIR / "urgent_latest.txt"
LOG_FILE = Path.home() / ".longhun" / "审计留痕" / "roster_sync.jsonl"

NOTION_ROSTER_URL = "https://www.notion.so/4cf99c3e7a014e919fdab705ceb4cbc4"

MODULE_TYPES = {
    "⚙️ 功能模块",
    "📄 白皮书",
    "🏛️ 北辰母协议",
    "🌟 P0愿景",
    "🤖 AI执行P0",
    "💎 价值观内核",
    "👤 数字人",
    "🧠 内核人格",
}


def _uuid(id_raw: str) -> str:
    s = id_raw.replace("-", "")
    if len(s) != 32:
        return id_raw
    return f"{s[:8]}-{s[8:12]}-{s[12:16]}-{s[16:20]}-{s[20:]}"


def _now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat()


def _prop_text(prop: Optional[Dict[str, Any]]) -> str:
    if not prop:
        return ""
    t = prop.get("type")
    if t == "title":
        return "".join(x.get("plain_text", "") for x in prop.get("title") or [])
    if t == "rich_text":
        return "".join(x.get("plain_text", "") for x in prop.get("rich_text") or [])
    if t == "select" and prop.get("select"):
        return str(prop["select"].get("name") or "")
    if t == "status" and prop.get("status"):
        return str(prop["status"].get("name") or "")
    if t == "url":
        return str(prop.get("url") or "")
    if t == "number":
        v = prop.get("number")
        return "" if v is None else str(v)
    if t == "checkbox":
        return "是" if prop.get("checkbox") else ""
    if t == "multi_select":
        return ",".join(x.get("name", "") for x in prop.get("multi_select") or [])
    if t == "formula" and prop.get("formula"):
        f = prop["formula"]
        if f.get("type") == "string":
            return str(f.get("string") or "")
        if f.get("type") == "number":
            v = f.get("number")
            return "" if v is None else str(v)
    return ""


def _split_signals(text: str) -> List[str]:
    if not text:
        return []
    parts = re.split(r"[,，、;；\s]+", text.strip())
    return [p for p in parts if p]


def _extract_persona_id(*fields: str) -> Optional[str]:
    blob = " ".join(f for f in fields if f)
    if "L0" in blob and "真人" in blob:
        return "L0"
    m = re.search(r"\bP(\d{2})\b", blob)
    if m:
        return f"P{m.group(1)}"
    m = re.search(r"PERSONA-([PL]?\d{2}|L0)", blob, re.I)
    if m:
        pid = m.group(1).upper()
        return pid if pid.startswith("L") else f"P{pid}"
    return None


def _tricolor_from_status(status: str) -> str:
    if "🔴" in status or "熔断" in status:
        return "🔴"
    if "🟡" in status or "观察" in status:
        return "🟡"
    if "🟢" in status or "活跃" in status:
        return "🟢"
    return "🟡"


def _normalize_page(page: Dict[str, Any]) -> Dict[str, Any]:
    props = page.get("properties") or {}
    name = _prop_text(props.get("名字"))
    status = _prop_text(props.get("当前状态"))
    module_type = _prop_text(props.get("模块类型"))
    ipa_tpl = _prop_text(props.get("IPA·触发模版"))
    dna = _prop_text(props.get("DNA追溯码"))
    signals = _prop_text(props.get("信号词"))
    tier_level = _prop_text(props.get("人格层级"))
    route_code = _prop_text(props.get("路由编号"))
    what = _prop_text(props.get("做什么")) or _prop_text(props.get("功能定位"))
    sancai = _prop_text(props.get("三才归属"))
    online = _prop_text(props.get("上线状态"))
    consistency = _prop_text(props.get("一致性评分"))
    warnings = _prop_text(props.get("警告次数"))
    fuse_count = _prop_text(props.get("熔断次数"))

    persona_id = _extract_persona_id(tier_level, ipa_tpl, route_code, name)

    ipa = ipa_tpl.strip()
    if ipa and not ipa.startswith("["):
        if "IPA-" in ipa:
            ipa = f"[{ipa.split()[0]}]"

    row = {
        "notion_page_id": page.get("id", ""),
        "notion_url": page.get("url", ""),
        "title": name,
        "dna": dna,
        "ipa": ipa,
        "persona_id": persona_id,
        "module_type": module_type,
        "role": what[:200] if what else "",
        "route_hints": _split_signals(signals),
        "sancai": sancai,
        "status": status,
        "online": online,
        "consistency": consistency,
        "warnings": warnings,
        "fuse_count": fuse_count,
        "audit": _tricolor_from_status(status),
        "tier": "L2" if module_type in MODULE_TYPES else (tier_level or "L3日常"),
    }
    return row


def _is_module_row(row: Dict[str, Any]) -> bool:
    if row.get("module_type") in MODULE_TYPES:
        return True
    ipa = row.get("ipa") or ""
    return ipa.startswith("[IPA-") and "PERSONA" not in ipa.upper()


def _row_to_module(row: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "ipa": row.get("ipa") or f"[NOTION-{row.get('notion_page_id', '')[:8]}]",
        "title": row.get("title") or "未命名",
        "dna": row.get("dna", ""),
        "tier": row.get("tier", "L2"),
        "vault": "花名册模块",
        "roster_bucket": "Notion同步",
        "persona_route": f"[PERSONA-{row['persona_id']}]" if row.get("persona_id") else "",
        "persona_id": row.get("persona_id"),
        "notion_url": row.get("notion_url"),
        "notion_page_id": row.get("notion_page_id"),
        "audit": row.get("audit", "🟢"),
        "execute_allowed": False,
        "hold_acknowledged": [],
        "source": "notion_sync",
    }


def _detect_urgent(row: Dict[str, Any]) -> Optional[Dict[str, str]]:
    reasons: List[str] = []
    st = row.get("status") or ""
    if "🔴" in st or "熔断" in st:
        reasons.append(f"当前状态={st}")
    if row.get("consistency") and "❌" in row["consistency"]:
        reasons.append(f"一致性={row['consistency']}")
    try:
        if float(row.get("warnings") or 0) > 0:
            reasons.append(f"警告次数={row['warnings']}")
    except ValueError:
        pass
    try:
        if float(row.get("fuse_count") or 0) > 0:
            reasons.append(f"熔断次数={row['fuse_count']}")
    except ValueError:
        pass
    if not reasons:
        return None
    return {
        "title": row.get("title") or row.get("notion_page_id", ""),
        "reason": " · ".join(reasons),
        "url": row.get("notion_url", ""),
        "audit": "🔴" if "🔴" in st else "🟡",
    }


def _query_all_pages(database_id: str) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    if not NOTION_TOKEN:
        return [], "未配置 NOTION_TOKEN（engine/.env）"

    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }
    db = _uuid(database_id)
    pages: List[Dict[str, Any]] = []
    cursor: Optional[str] = None

    try:
        with httpx.Client(timeout=30) as client:
            while True:
                body: Dict[str, Any] = {"page_size": 100}
                if cursor:
                    body["start_cursor"] = cursor
                r = client.post(
                    f"https://api.notion.com/v1/databases/{db}/query",
                    headers=headers,
                    json=body,
                )
                data = r.json()
                if data.get("object") == "error":
                    return [], data.get("message", str(data))
                pages.extend(data.get("results") or [])
                if not data.get("has_more"):
                    break
                cursor = data.get("next_cursor")
    except Exception as e:
        return [], str(e)

    return pages, None


def sync_roster_from_notion(*, force: bool = True) -> Dict[str, Any]:
    """
    从 Notion 花名册拉全量 → ~/.longhun/roster/notion_mirror.json
    人不用管；只看 urgent 通知。
    """
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    pages, err = _query_all_pages(ROSTER_DB_ID)
    if err:
        out = {
            "ok": False,
            "error": err,
            "synced_at": _now_iso(),
            "notion_db": NOTION_ROSTER_URL,
        }
        _append_log(out)
        return out

    entries = [_normalize_page(p) for p in pages]
    modules = [_row_to_module(r) for r in entries if _is_module_row(r)]
    urgent = [u for r in entries if (u := _detect_urgent(r))]

    persona_patches: Dict[str, Dict[str, Any]] = {}
    for r in entries:
        pid = r.get("persona_id")
        if not pid:
            continue
        patch = persona_patches.setdefault(
            pid,
            {"route_hints": [], "notion_titles": []},
        )
        patch["route_hints"].extend(r.get("route_hints") or [])
        if r.get("title"):
            patch["notion_titles"].append(r["title"])
        if r.get("dna"):
            patch["dna"] = r["dna"]

    for pid, patch in persona_patches.items():
        patch["route_hints"] = list(dict.fromkeys(patch["route_hints"]))

    mirror = {
        "ok": True,
        "synced_at": _now_iso(),
        "notion_db": NOTION_ROSTER_URL,
        "notion_database_id": ROSTER_DB_ID,
        "row_count": len(entries),
        "module_count": len(modules),
        "entries": entries,
        "modules": modules,
        "persona_patches": persona_patches,
        "urgent": urgent,
    }

    CACHE_FILE.write_text(
        json.dumps(mirror, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    alert_lines = [
        f"龍魂花名册同步 · {mirror['synced_at']}",
        f"共 {len(entries)} 条 · 模块 {len(modules)} · 需关注 {len(urgent)} 条",
        "",
    ]
    if urgent:
        alert_lines.append("══ 仅看这些（紧急）══")
        for u in urgent[:20]:
            alert_lines.append(f"{u['audit']} {u['title']} — {u['reason']}")
            if u.get("url"):
                alert_lines.append(f"   {u['url']}")
    else:
        alert_lines.append("🟢 无紧急项 · 其余在 Notion 照常改即可")
    ALERT_FILE.write_text("\n".join(alert_lines) + "\n", encoding="utf-8")

    _append_log(
        {
            "ok": True,
            "row_count": len(entries),
            "urgent_count": len(urgent),
            "synced_at": mirror["synced_at"],
        }
    )

    return mirror


def _append_log(rec: Dict[str, Any]) -> None:
    line = json.dumps({"ts": _now_iso(), **rec}, ensure_ascii=False)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def load_notion_mirror() -> Optional[Dict[str, Any]]:
    if not CACHE_FILE.is_file():
        return None
    try:
        return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return None


if __name__ == "__main__":
    import sys

    r = sync_roster_from_notion()
    print(json.dumps(r, ensure_ascii=False, indent=2))
    if r.get("urgent"):
        print("\n--- 紧急通知 ---")
        for u in r["urgent"][:10]:
            print(f"{u['audit']} {u['title']}: {u['reason']}")
    sys.exit(0 if r.get("ok") else 1)
