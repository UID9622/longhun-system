"""
CNSH Projection · 公域节点聚合器

从 DNA-Calendar SQLite 读取事件
→ 过滤有GPS坐标的公域节点
→ 经隐私层净化
→ 返回可供Three.js渲染的节点列表

Author: 诸葛鑫 (UID9622)
"""

import sqlite3
import os
import time
from typing import List, Dict, Optional

from .privacy import sanitize_node, MOOD_PALETTE, mood_to_color, mood_to_category

DB_PATH = os.path.expanduser("~/.longhun/dna_calendar.db")


# ── 节点获取 ──────────────────────────────────────────────────────

def get_projection_nodes(
    limit:       int   = 500,
    date_from:   str   = "",   # YYYY-MM-DD
    date_to:     str   = "",   # YYYY-MM-DD
    city:        str   = "",
    fuzz_radius: float = 100.0,
) -> List[Dict]:
    """
    获取可投影的公域节点（已去敏）。

    仅返回有GPS坐标的事件（lat/lng非零）。
    私域保护：内容/标题不出现在返回值中。
    """
    if not os.path.exists(DB_PATH):
        return []

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    sql    = _build_query(date_from, date_to, city, limit)
    params = _build_params(date_from, date_to, city, limit)

    try:
        rows = conn.execute(sql, params).fetchall()
    except Exception:
        # 兼容旧版表结构
        rows = _fallback_query(conn, limit)
    finally:
        conn.close()

    nodes = []
    for r in rows:
        raw = dict(r)
        # 跳过无坐标节点
        if not raw.get("lat") or float(raw.get("lat") or 0) == 0:
            continue
        node = sanitize_node(raw, fuzz_radius)
        if node["lat"] == 0 and node["lng"] == 0:
            continue
        nodes.append(node)

    return nodes


def _build_query(date_from, date_to, city, limit) -> str:
    # 实际列名：geo_lat/geo_lng/geo_city/wx_desc/wx_temp
    sql = """
        SELECT dna_trace,
               geo_lat  AS lat,
               geo_lng  AS lng,
               geo_city AS city,
               mood, tags, timestamp,
               wx_desc  AS weather_desc,
               wx_temp  AS weather_temp,
               NULL     AS weather_emoji
        FROM calendar_events
        WHERE geo_lat IS NOT NULL AND geo_lat != 0
    """
    if date_from:
        sql += " AND date(datetime(timestamp, 'unixepoch')) >= date(?)"
    if date_to:
        sql += " AND date(datetime(timestamp, 'unixepoch')) <= date(?)"
    if city:
        sql += " AND geo_city LIKE ?"
    sql += " ORDER BY timestamp DESC LIMIT ?"
    return sql


def _build_params(date_from, date_to, city, limit) -> list:
    params = []
    if date_from: params.append(date_from)
    if date_to:   params.append(date_to)
    if city:      params.append(f"%{city}%")
    params.append(limit)
    return params


def _fallback_query(conn, limit) -> list:
    """兼容旧版表，字段可能不全"""
    try:
        return conn.execute(
            "SELECT * FROM calendar_events WHERE lat IS NOT NULL LIMIT ?",
            (limit,)
        ).fetchall()
    except Exception:
        return []


# ── 统计 ──────────────────────────────────────────────────────────

def get_projection_stats() -> Dict:
    """投影层统计数据"""
    if not os.path.exists(DB_PATH):
        return {
            "total": 0, "with_gps": 0, "cities": 0,
            "mood_dist": {}, "color_map": MOOD_PALETTE,
        }

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    try:
        total    = conn.execute("SELECT COUNT(*) as c FROM calendar_events").fetchone()["c"]
        with_gps = conn.execute(
            "SELECT COUNT(*) as c FROM calendar_events WHERE geo_lat IS NOT NULL AND geo_lat != 0"
        ).fetchone()["c"]
        cities   = conn.execute(
            "SELECT COUNT(DISTINCT geo_city) as c FROM calendar_events WHERE geo_city IS NOT NULL AND geo_city != ''"
        ).fetchone()["c"]
        mood_rows = conn.execute(
            "SELECT mood, COUNT(*) as c FROM calendar_events GROUP BY mood ORDER BY c DESC LIMIT 10"
        ).fetchall()
    except Exception:
        total = with_gps = cities = 0
        mood_rows = []
    finally:
        conn.close()

    mood_dist = {}
    for r in mood_rows:
        if r["mood"]:
            mood_dist[r["mood"]] = {
                "count": r["c"],
                "color": mood_to_color(r["mood"]),
                "category": mood_to_category(r["mood"]),
            }

    return {
        "total":     total,
        "with_gps":  with_gps,
        "cities":    cities,
        "mood_dist": mood_dist,
        "color_map": MOOD_PALETTE,
        "updated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }


# ── GeoJSON 格式输出（供未来地图引擎使用）────────────────────────

def to_geojson(nodes: List[Dict]) -> Dict:
    """将节点列表转换为 GeoJSON FeatureCollection"""
    features = []
    for node in nodes:
        if not node["lng"] or not node["lat"]:
            continue
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [node["lng"], node["lat"]],
            },
            "properties": {
                "dna":      node["dna"],
                "city":     node["city"],
                "color":    node["color"],
                "mood_cat": node["mood_cat"],
                "effect":   node["effect"],
                "emoji":    node["emoji"],
                "time":     node["time"],
            }
        })
    return {
        "type": "FeatureCollection",
        "features": features,
        "meta": {"count": len(features)},
    }
