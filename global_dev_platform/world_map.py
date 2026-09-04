#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂全球开发者平台 · 全球开发者地图 v1.0
DNA: #龍芯⚡️丙午·丙申·壬戌·亥时·䷲震-WORLD-MAP-v1.0
创建者: 诸葛鑫（UID9622）
协议: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
设计原则:
  把全球每个人的「存在痕迹」投影到一张地图上。
  让世界看见：每一个普通人都能成为开发者。
  数据来源: GlobalTrace 的 world_traces.jsonl（匿名化）。
  DNA 一律走统一干支卦引擎。
"""

import json
from pathlib import Path
from collections import Counter
from datetime import datetime
from typing import Optional, Dict, Any, List

from lh_dna import lh_dna

TRACE_ROOT = Path.home() / "longhun-system" / "global_dev_platform" / "traces"
OUTPUT_DIR = Path.home() / "longhun-system" / "global_dev_platform" / "output"


class WorldMap:
    """
    全球开发者地图
    - 聚合全球痕迹 → 国家/地区分布
    - 生成可视化 HTML（纯前端 · 无需服务端）
    """

    def __init__(self, trace_root: Optional[Path] = None):
        self.trace_root = Path(trace_root) if trace_root else TRACE_ROOT
        self.world_file = self.trace_root / "world_traces.jsonl"

    @staticmethod
    def _dna(action: str) -> str:
        return lh_dna(module="WORLD-MAP", action=action, version="v1.0")

    def _load_world_traces(self) -> List[Dict]:
        """读取全球痕迹（匿名）"""
        if not self.world_file.exists():
            return []
        try:
            lines = self.world_file.read_text("utf-8").strip().splitlines()
            return [json.loads(l) for l in lines if l.strip()]
        except Exception:
            return []

    def stats(self) -> Dict[str, Any]:
        """全球痕迹统计"""
        traces = self._load_world_traces()
        total = len(traces)
        locations = Counter(t.get("location") or "未知" for t in traces)
        platforms = Counter(t.get("platform") or "unknown" for t in traces)
        event_types = Counter(t.get("event_type") for t in traces)
        return {
            "total":      total,
            "locations":  dict(locations.most_common(20)),
            "platforms":  dict(platforms),
            "events":     dict(event_types),
            "generated":  datetime.now().isoformat(),
        }

    def render_html(self, output_path: Optional[Path] = None) -> str:
        """
        生成全球开发者地图可视化页面
        - 顶部统计卡
        - 位置排行榜（文本条形图）
        - 平台分布
        纯静态 HTML · 双击即开
        """
        stats = self.stats()
        dna = self._dna("RENDER")
        out = Path(output_path) if output_path else OUTPUT_DIR / "world_map.html"
        out.parent.mkdir(parents=True, exist_ok=True)

        total = stats["total"]
        # 位置排行 HTML
        rank_rows = ""
        for loc, cnt in stats["locations"].items():
            width = min(100, int(cnt / max(total, 1) * 100))
            rank_rows += (
                f'<div class="row"><span class="loc">{loc}</span>'
                f'<div class="bar"><div class="fill" style="width:{width}%"></div></div>'
                f'<span class="cnt">{cnt}</span></div>'
            )
        if not rank_rows:
            rank_rows = '<p class="empty">还没有世界足迹——成为第一个开发者 🌱</p>'

        # 平台分布
        plats = stats["platforms"]
        plat_rows = "".join(
            f'<span class="tag">{k}: {v}</span>' for k, v in plats.items()
        ) or '<span class="tag">无</span>'

        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>龍魂全球开发者地图 v1.0</title>
<style>
  body {{ font-family: -apple-system, "PingFang SC", sans-serif; background:#0b1023;
         color:#e8ecf5; margin:0; padding:32px; }}
  .wrap {{ max-width:820px; margin:0 auto; }}
  h1 {{ font-size:28px; margin:0 0 4px; }}
  .sub {{ color:#8fa0c9; font-size:14px; margin-bottom:24px; }}
  .cards {{ display:flex; gap:16px; flex-wrap:wrap; margin-bottom:24px; }}
  .card {{ background:#151c38; border-radius:12px; padding:18px 22px; flex:1; min-width:160px;
           border:1px solid #232e5c; }}
  .card .num {{ font-size:34px; font-weight:700; color:#5ad0ff; }}
  .card .label {{ color:#8fa0c9; font-size:13px; margin-top:4px; }}
  .panel {{ background:#151c38; border-radius:12px; padding:20px; margin-bottom:16px;
            border:1px solid #232e5c; }}
  .panel h2 {{ font-size:16px; margin:0 0 14px; color:#5ad0ff; }}
  .row {{ display:flex; align-items:center; gap:10px; margin-bottom:8px; }}
  .loc {{ width:110px; font-size:13px; color:#c6cfe8; }}
  .bar {{ flex:1; background:#1e2a52; border-radius:6px; height:14px; overflow:hidden; }}
  .fill {{ background:linear-gradient(90deg,#2f6bff,#5ad0ff); height:100%; border-radius:6px; }}
  .cnt {{ width:40px; text-align:right; font-size:13px; color:#8fa0c9; }}
  .tag {{ background:#1e2a52; border-radius:20px; padding:5px 12px; font-size:13px;
          margin-right:8px; display:inline-block; margin-bottom:6px; }}
  .empty {{ color:#8fa0c9; }}
  .foot {{ color:#5b6a92; font-size:12px; margin-top:20px; text-align:center; }}
</style>
</head>
<body>
<div class="wrap">
  <h1>🌏 龍魂全球开发者地图</h1>
  <div class="sub">让全世界每个人的存在痕迹，都被看见 · 让每个人都成为开发者</div>
  <div class="cards">
    <div class="card"><div class="num">{total}</div><div class="label">全球存在痕迹</div></div>
    <div class="card"><div class="num">{len(stats["locations"])}</div><div class="label">地点覆盖</div></div>
    <div class="card"><div class="num">{len(stats["events"])}</div><div class="label">事件类型</div></div>
  </div>
  <div class="panel">
    <h2>📍 足迹分布</h2>
    {rank_rows}
  </div>
  <div class="panel">
    <h2>📱 平台分布</h2>
    {plat_rows}
  </div>
  <div class="foot">DNA: {dna} · 龍魂全球开发者平台 v1.0 · 诸葛鑫 UID9622 · 数据匿名化</div>
</div>
</body>
</html>
"""
        out.write_text(html, "utf-8")
        print(f"  🌏 全球开发者地图已生成: {out}")
        print(f"     DNA: {dna}")
        return str(out)


if __name__ == "__main__":
    world = WorldMap()
    stats = world.stats()
    print(f"全球痕迹: {stats['total']} 条")
    path = world.render_html()
    print(f"\n用浏览器打开: open {path}")
