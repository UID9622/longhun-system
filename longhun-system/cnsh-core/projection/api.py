"""
CNSH Projection API — FastAPI 路由

挂载路径：/projection

端点：
  GET /projection/nodes          — 获取公域DNA节点（去敏）
  GET /projection/nodes.geojson  — GeoJSON格式
  GET /projection/stats          — 统计数据
  GET /projection/palette        — 心情颜色表

Author: 诸葛鑫 (UID9622)
"""

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import Optional

from .aggregator import get_projection_nodes, get_projection_stats, to_geojson
from .privacy    import MOOD_PALETTE

router = APIRouter(prefix="/projection", tags=["Projection"])


@router.get("/nodes")
def projection_nodes(
    limit:       int            = 300,
    date_from:   Optional[str]  = None,
    date_to:     Optional[str]  = None,
    city:        Optional[str]  = None,
    fuzz_radius: float          = 100.0,
):
    """
    获取公域DNA节点（已去敏）。

    返回内容：
      - GPS（模糊化）
      - 城市名
      - 心情颜色（不含心情文字）
      - 天气描述 + 粒子效果标签
      - DNA追溯码（公开哈希）
      - 时间戳

    不返回：标题 / 备注 / 内容（私域保留）
    """
    nodes = get_projection_nodes(
        limit       = min(limit, 1000),
        date_from   = date_from or "",
        date_to     = date_to   or "",
        city        = city      or "",
        fuzz_radius = fuzz_radius,
    )
    return {
        "count":       len(nodes),
        "nodes":       nodes,
        "privacy_note": "GPS已模糊(±100m)·内容哈希保护·私域不投影",
    }


@router.get("/nodes.geojson")
def projection_nodes_geojson(
    limit:     int           = 300,
    date_from: Optional[str] = None,
    date_to:   Optional[str] = None,
):
    """GeoJSON格式，兼容 Leaflet / Mapbox / QGIS"""
    nodes = get_projection_nodes(
        limit     = min(limit, 1000),
        date_from = date_from or "",
        date_to   = date_to   or "",
    )
    geojson = to_geojson(nodes)
    return JSONResponse(content=geojson, media_type="application/geo+json")


@router.get("/stats")
def projection_stats():
    """投影层统计：总节点数 / 有GPS数 / 城市数 / 心情分布"""
    return get_projection_stats()


@router.get("/palette")
def projection_palette():
    """心情颜色表（供前端渲染图例）"""
    return {"palette": MOOD_PALETTE}
