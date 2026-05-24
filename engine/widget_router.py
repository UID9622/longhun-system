#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Widget 路由 · 接 web-widgets/.dna/keyword_map.md
DNA: #龍芯⚡️2026-04-19-WIDGET-ROUTER-v1.0

读 ~/Desktop/☰ 龍🇨🇳魂 ☷/web-widgets/.dna/keyword_map.md
按关键词命中返回对应 widget URL（file://）
Chrome 扩展按钮可以调用此端点跳到 widget 界面
"""
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

from fastapi import APIRouter
from pydantic import BaseModel


WEB_WIDGETS = Path.home() / "Desktop" / "☰ 龍🇨🇳魂 ☷" / "web-widgets"
KEYWORD_MAP = WEB_WIDGETS / ".dna" / "keyword_map.md"


router = APIRouter()


def _parse_keyword_map() -> list:
    """解析 keyword_map.md 返回结构化路由表"""
    if not KEYWORD_MAP.exists():
        return []

    rows = []
    try:
        content = KEYWORD_MAP.read_text(encoding="utf-8")
    except Exception:
        return []

    # 解析 Markdown 表格行：| 关键词 | widget | 入口 |
    for line in content.splitlines():
        line = line.strip()
        if not line.startswith("|") or line.startswith("|---") or line.startswith("| 关键词"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 3:
            continue
        kw_field, widget_name, entry = cells[0], cells[1], cells[2]
        # 关键词用 · 分隔
        keywords = [k.strip() for k in re.split(r"[·,，|/]", kw_field) if k.strip()]
        # 解析入口 URL
        m = re.search(r"`([^`]+)`", entry)
        entry_path = m.group(1) if m else entry
        # 判断状态
        status = "ready" if entry_path and entry_path != "—" else "待建"
        rows.append({
            "widget": widget_name,
            "keywords": keywords,
            "entry_rel": entry_path if status == "ready" else None,
            "status": status,
        })
    return rows


def _resolve_entry(entry_rel: str) -> dict:
    """相对路径转绝对路径 + file:// URL（URL 编码）"""
    if not entry_rel:
        return {"abs": None, "file_url": None, "exists": False}
    # keyword_map 里路径是相对于 .dna/ 的，例 ../三才流場/current.html
    abs_path = (KEYWORD_MAP.parent / entry_rel).resolve()
    # 生成 file:// URL（正确处理中文和 emoji）
    posix = abs_path.as_posix()
    file_url = "file://" + quote(posix, safe="/")
    return {
        "abs": str(abs_path),
        "file_url": file_url,
        "exists": abs_path.exists(),
    }


class RouteQuery(BaseModel):
    text: str
    limit: int = 5


@router.get("/api/widget/list")
def widget_list():
    """列出所有注册 widget + 状态"""
    routes = _parse_keyword_map()
    for r in routes:
        if r["entry_rel"]:
            r.update(_resolve_entry(r["entry_rel"]))
    return {
        "widgets": routes,
        "count": len(routes),
        "ready_count": sum(1 for r in routes if r["status"] == "ready"),
        "source": str(KEYWORD_MAP),
        "dna": f"#龍芯⚡️{datetime.now().strftime('%Y%m%d%H%M%S')}-WIDGET-LIST",
    }


@router.post("/api/widget/route")
def widget_route(q: RouteQuery):
    """输入文本·按关键词命中返回匹配的 widget + URL"""
    text = q.text or ""
    routes = _parse_keyword_map()
    hits = []
    for r in routes:
        matched_kws = [kw for kw in r["keywords"] if kw and kw in text]
        if matched_kws:
            info = {
                "widget": r["widget"],
                "matched_keywords": matched_kws,
                "score": len(matched_kws),
                "status": r["status"],
            }
            if r["status"] == "ready":
                info.update(_resolve_entry(r["entry_rel"]))
            hits.append(info)

    hits.sort(key=lambda h: h["score"], reverse=True)
    hits = hits[: q.limit]

    return {
        "input_preview": text[:60],
        "hit_count": len(hits),
        "hits": hits,
        "color": "🟢" if hits else "🟡",
        "title": "🎯 Widget 路由",
        "summary": (
            "命中: " + " / ".join(f"{h['widget']}" for h in hits)
            if hits
            else "未命中任何注册 widget"
        ),
        "dna": f"#龍芯⚡️{datetime.now().strftime('%Y%m%d%H%M%S')}-WIDGET-ROUTE",
    }


@router.get("/api/widget/open/{name}")
def widget_open(name: str):
    """按名称直接开指定 widget（三才流場·DNA易经·洛书五行...）"""
    routes = _parse_keyword_map()
    for r in routes:
        if name in r["widget"] or r["widget"] in name:
            if r["status"] == "ready":
                info = _resolve_entry(r["entry_rel"])
                return {
                    "widget": r["widget"],
                    "status": "ready",
                    **info,
                    "dna": f"#龍芯⚡️{datetime.now().strftime('%Y%m%d%H%M%S')}-WIDGET-OPEN",
                }
            return {
                "widget": r["widget"],
                "status": "待建",
                "keywords": r["keywords"],
            }
    return {"error": f"未注册 widget: {name}"}
