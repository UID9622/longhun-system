# DNA: #龍芯⚡️丙午·乙未·乙丑·比-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# DNA追溯码:#龍芯⚡️2026-06-22-LONGHUN-FONT-WUXING-HETU-LUOSHU-v1.0

"""
LonghunFont 五行、河图、洛书扩展
使用 Unicode Private Use Area (PUA) U+E000 起
"""

import json
import sys
import math
from pathlib import Path
from datetime import datetime

DNA = "#龍芯⚡️2026-06-22-LONGHUN-FONT-WUXING-HETU-LUOSHU-v1.0"

VIEWBOX = 600


def stroke_move(x, y):
    return {"类型": "移动到", "坐标": [x, y]}


def stroke_line(x, y):
    return {"类型": "直线段", "终点": [x, y]}


def polyline(points):
    strokes = [stroke_move(*points[0])]
    for p in points[1:]:
        strokes.append(stroke_line(*p))
    return strokes


def circle(cx, cy, r, segments=12):
    pts = []
    for i in range(segments + 1):
        a = 2 * math.pi * i / segments
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return polyline(pts)


def dot(cx, cy, r=12):
    return circle(cx, cy, r, segments=10)


def rect(x1, y1, x2, y2):
    return polyline([(x1, y1), (x2, y1), (x2, y2), (x1, y2), (x1, y1)])


# ============================================================
# 五行图标
# ============================================================
def wuxing_metal():
    # 金：圆环内加一竖，象征鼎/钟
    strokes = circle(300, 300, 180, segments=24)
    strokes.extend(vline(300, 140, 460))
    return strokes


def wuxing_wood():
    # 木：树干加三枝
    strokes = vline(300, 180, 480)
    strokes.extend(polyline([(300, 280), (180, 180)]))
    strokes.extend(polyline([(300, 360), (420, 260)]))
    strokes.extend(polyline([(300, 200), (300, 120)]))
    return strokes


def wuxing_water():
    # 水：三条波浪线
    strokes = []
    for y in [180, 300, 420]:
        strokes.extend(polyline([(120, y), (220, y - 40), (320, y), (420, y - 40), (480, y)]))
    return strokes


def wuxing_fire():
    # 火：火焰三角形加内焰
    strokes = polyline([(300, 120), (420, 420), (300, 360), (180, 420), (300, 120)])
    strokes.extend(polyline([(300, 260), (340, 340), (300, 320), (260, 340), (300, 260)]))
    return strokes


def wuxing_earth():
    # 土：山形加地平线
    strokes = hline(460, 100, 500)
    strokes.extend(polyline([(160, 460), (260, 220), (360, 340), (440, 180), (500, 460)]))
    return strokes


# ============================================================
# 河图：黑白点阵
# ============================================================
def hetu():
    strokes = []
    # 中心 5/10
    strokes.extend(dot(300, 300, 16))
    strokes.extend(dot(300, 340, 12))
    # 北 1/6
    strokes.extend(dot(300, 120, 16))
    for dx in [-40, 0, 40, -20, 20, 0]:
        strokes.extend(dot(300 + dx, 160 + (abs(dx) % 30), 10))
    # 南 2/7
    for dx in [-30, 30]:
        strokes.extend(dot(300 + dx, 480, 12))
    for i, dx in enumerate([-60, -30, 0, 30, 60, -45, 15]):
        strokes.extend(dot(300 + dx, 520 - (i % 2) * 20, 10))
    # 东 3/8
    for dx in [-40, 0, 40]:
        strokes.extend(dot(480 + dx, 300, 12))
    for i, dx in enumerate([-60, -20, 20, 60, -40, 0, 40, 0]):
        strokes.extend(dot(500 + dx, 340 - (i % 2) * 20, 10))
    # 西 4/9
    for dx in [-60, -20, 20, 60]:
        strokes.extend(dot(120 + dx, 300, 12))
    for i, dx in enumerate([-80, -40, 0, 40, 80, -60, -20, 20, 60]):
        strokes.extend(dot(120 + dx, 340 - (i % 2) * 20, 10))
    return strokes


# ============================================================
# 洛书：九宫格点阵
# ============================================================
def luoshu():
    strokes = []
    grid = [
        [4, 9, 2],
        [3, 5, 7],
        [8, 1, 6],
    ]
    positions = [
        (150, 150), (300, 150), (450, 150),
        (150, 300), (300, 300), (450, 300),
        (150, 450), (300, 450), (450, 450),
    ]
    for (x, y), count in zip(positions, [4, 9, 2, 3, 5, 7, 8, 1, 6]):
        # 每个数字用相应数量的小点表示，呈圆形排列
        if count == 1:
            strokes.extend(dot(x, y, 14))
        else:
            radius = 28
            for i in range(count):
                a = 2 * math.pi * i / count - math.pi / 2
                strokes.extend(dot(x + radius * math.cos(a), y + radius * math.sin(a), 9))
    return strokes


# ============================================================
# 太极八卦图
# ============================================================
def taiji_bagua():
    strokes = []
    # 外圆
    strokes.extend(circle(300, 300, 260, segments=36))
    # 太极 S 曲线（简化：两个半圆弧）
    strokes.extend(circle(300, 170, 130, segments=18)[:10])
    strokes.extend(circle(300, 430, 130, segments=18)[8:])
    # 鱼眼
    strokes.extend(circle(300, 170, 30, segments=10))
    strokes.extend(circle(300, 430, 30, segments=10))
    # 八卦符号围在外圈（简化：用短线表示）
    # 乾三连
    for i, y_offset in enumerate([-220, -200, -180]):
        strokes.extend(polyline([(280, 300 + y_offset), (320, 300 + y_offset)]))
    return strokes


def hline(y, x1, x2):
    return polyline([(x1, y), (x2, y)])


def vline(x, y1, y2):
    return polyline([(x, y1), (x, y2)])


# PUA 编码分配
PUA_GLYPHS = {
    0xE000: ("金", wuxing_metal),
    0xE001: ("木", wuxing_wood),
    0xE002: ("水", wuxing_water),
    0xE003: ("火", wuxing_fire),
    0xE004: ("土", wuxing_earth),
    0xE005: ("河图", hetu),
    0xE006: ("洛书", luoshu),
    0xE007: ("太极八卦", taiji_bagua),
}


def expand(glyph_path: str):
    base_dir = Path(__file__).parent.parent
    glyph_path = Path(glyph_path) if glyph_path else base_dir / "glyphs" / "龍魂字元库_v0005_易经版.json"

    with open(glyph_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    added = 0
    for code, (name, generator) in PUA_GLYPHS.items():
        char = chr(code)
        if char in data["字符集_cnsh9622"]:
            continue
        strokes = generator()
        data["字符集_cnsh9622"][char] = {
            "unicode": f"U+{code:04X}",
            "笔画数": len(strokes),
            "结构": "PUA文化符号",
            "名称": name,
            "风格参数": {"力度": 0.85, "棱角": 0.25, "节奏": 0.65, "墨色": 0.9},
            "笔画路径_cnsh9622": strokes
        }
        added += 1

    data["元数据"]["版本"] = "v0006-五行版"
    data["元数据"]["描述"] = f"LonghunFont 五行版字元库，含 {len(data['字符集_cnsh9622'])} 个字符"
    data["元数据"]["五行扩展时间"] = datetime.now().isoformat()
    data["元数据"]["五行扩展DNA"] = DNA
    data["元数据"]["PUA编码说明"] = {
        "U+E000": "金",
        "U+E001": "木",
        "U+E002": "水",
        "U+E003": "火",
        "U+E004": "土",
        "U+E005": "河图",
        "U+E006": "洛书",
        "U+E007": "太极八卦",
    }

    new_path = base_dir / "glyphs" / "龍魂字元库_v0006_五行版.json"
    with open(new_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ 已扩展五行版字元库: {new_path}")
    print(f"   新增字符: {added}")
    print(f"   总字符数: {len(data['字符集_cnsh9622'])}")
    return str(new_path)


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else None
    expand(path)
