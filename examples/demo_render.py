#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-09-01-DEMO-RENDER-v1.0-MEDIA-SENSE
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
🎨 女娲五彩石渲染引擎 demo — 五行雷达图 / 三色审计仪表盘 / 流场 / 健康看板
用法: python3 examples/demo_render.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "08_BIN"))
from wuwu_renderer import 渲染

OUT = Path(__file__).resolve().parent / "output" / "render"
OUT.mkdir(parents=True, exist_ok=True)


def main():
    print("🎨 女娲五彩石渲染引擎 demo")
    cases = [
        ("wuxing", {"金": 88, "木": 66, "水": 72, "火": 91, "土": 58}, "png", "wuxing_雷达图"),
        ("audit", {"red": 1, "yellow": 132, "green": 1}, "svg", "audit_三色仪表盘"),
        ("flow", {"nodes": [{"id": "a", "label": "网关"}, {"id": "b", "label": "审计"},
                            {"id": "c", "label": "记忆"}, {"id": "d", "label": "视频"}],
                  "edges": [["a", "b"], ["b", "c"], ["a", "d"], ["c", "d"]]}, "png", "flow_流场"),
    ]
    for 类型, 数据, 格式, 名 in cases:
        p = 渲染(类型, 数据, 格式, str(OUT / 名), 路径目录=OUT)
        print(f"  ✅ {类型:6s} → {p}")
    # 健康看板（自动联动 lh health --json）
    try:
        p = 渲染("health", None, "png", str(OUT / "health_看板"), 路径目录=OUT)
        print(f"  ✅ {'health':6s} → {p}")
    except Exception as e:
        print(f"  🟡 health 看板跳过: {e}")
    print(f"📁 输出目录: {OUT}")


if __name__ == "__main__":
    main()
