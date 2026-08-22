#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·壬午·䷇比-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
#!/usr/bin/env python3
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# DNA追溯码:#龍芯⚡️丙午·甲午·丁卯·丙午·䷚颐-LONGHUN-FONT-QUALITY-REFINE-v1.0

"""
LonghunFont 文化符号质量精修
重点优化：太极、五行、甲骨文、中国风图标的可识别度与美感
"""

import json
import sys
import math
from pathlib import Path
from datetime import datetime

DNA = "#龍芯⚡️丙午·甲午·丁卯·丙午·䷚颐-LONGHUN-FONT-QUALITY-REFINE-v1.0"


def stroke_move(x, y):
    return {"类型": "移动到", "坐标": [x, y]}


def stroke_line(x, y):
    return {"类型": "直线段", "终点": [x, y]}


def polyline(points):
    strokes = [stroke_move(*points[0])]
    for p in points[1:]:
        strokes.append(stroke_line(*p))
    return strokes


def circle(cx, cy, r, segments=16):
    pts = []
    for i in range(segments + 1):
        a = 2 * math.pi * i / segments
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return polyline(pts)


def arc(cx, cy, r, start, end, segments=16):
    pts = []
    for i in range(segments + 1):
        a = start + (end - start) * i / segments
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return polyline(pts)


def hline(y, x1, x2):
    return polyline([(x1, y), (x2, y)])


def vline(x, y1, y2):
    return polyline([(x, y1), (x, y2)])


def rect(x1, y1, x2, y2):
    return polyline([(x1, y1), (x2, y1), (x2, y2), (x1, y2), (x1, y1)])


# ============================================================
# 精修：太极图（更标准的 S 曲线）
# ============================================================
def taiji_refined():
    strokes = []
    # 外圆
    strokes.extend(circle(300, 300, 260, segments=48))
    # 上半黑鱼：左半圆（从顶部到底部中心）
    strokes.extend(arc(300, 150, 150, math.pi, 0, segments=24))
    # 下半白鱼：右半圆（从底部到顶部中心）
    strokes.extend(arc(300, 450, 150, 0, math.pi, segments=24))
    # 中间分隔 S 曲线：上半右弧线 + 下半左弧线
    strokes.extend(arc(300, 150, 150, 0, math.pi, segments=24))
    strokes.extend(arc(300, 450, 150, math.pi, 2 * math.pi, segments=24))
    # 鱼眼
    strokes.extend(circle(300, 150, 38, segments=12))
    strokes.extend(circle(300, 450, 38, segments=12))
    return strokes


# ============================================================
# 精修：五行图标
# ============================================================
def wuxing_metal():
    # 金：钟鼎形，上圆下方
    strokes = arc(300, 220, 120, math.pi, 0, segments=18)
    strokes.extend(polyline([(180, 220), (180, 420), (420, 420), (420, 220)]))
    strokes.extend(vline(300, 220, 420))
    strokes.extend(hline(320, 200, 400))
    return strokes


def wuxing_wood():
    # 木：更挺拔的树形
    strokes = vline(300, 140, 480)
    strokes.extend(polyline([(300, 260), (180, 160)]))
    strokes.extend(polyline([(300, 320), (420, 220)]))
    strokes.extend(polyline([(300, 180), (300, 120)]))
    strokes.extend(polyline([(220, 480), (300, 420), (380, 480)]))
    return strokes


def wuxing_water():
    # 水：三条流畅波浪
    strokes = []
    for y in [200, 300, 400]:
        strokes.extend(polyline([
            (120, y), (180, y - 40), (240, y), (300, y - 40),
            (360, y), (420, y - 40), (480, y)
        ]))
    return strokes


def wuxing_fire():
    # 火：火焰更舒展
    strokes = polyline([
        (300, 120), (360, 220), (320, 280), (400, 340),
        (300, 480), (200, 340), (280, 280), (240, 220), (300, 120)
    ])
    strokes.extend(polyline([(300, 260), (340, 320), (300, 360), (260, 320), (300, 260)]))
    return strokes


def wuxing_earth():
    # 土：山形大地
    strokes = hline(460, 100, 500)
    strokes.extend(polyline([(140, 460), (220, 300), (300, 380), (380, 260), (460, 460)]))
    strokes.extend(hline(420, 120, 480))
    return strokes


# ============================================================
# 精修：部分甲骨文（增强识别度）
# ============================================================
def oracle_sun():
    return circle(300, 300, 130, segments=20) + circle(300, 300, 28, segments=8)


def oracle_moon():
    return arc(300, 300, 150, math.pi / 6, 11 * math.pi / 6, segments=24)


def oracle_mountain():
    return polyline([
        (100, 480), (200, 200), (300, 340), (400, 200), (500, 480)
    ])


def oracle_water():
    return polyline([
        (140, 200), (200, 320), (300, 360), (400, 320), (460, 200)
    ]) + polyline([
        (180, 320), (160, 420)
    ]) + polyline([
        (420, 320), (440, 420)
    ])


def oracle_fire():
    return polyline([
        (300, 120), (360, 260), (320, 320), (420, 400), (300, 480),
        (180, 400), (280, 320), (240, 260), (300, 120)
    ])


def oracle_wood():
    return vline(300, 140, 480) + polyline([(300, 240), (180, 160)]) + \
           polyline([(300, 320), (420, 240)]) + polyline([(300, 180), (300, 120)])


def oracle_dragon():
    return polyline([
        (160, 340), (220, 240), (340, 220), (440, 280), (460, 380),
        (380, 460), (260, 460), (160, 400), (160, 340)
    ]) + circle(260, 300, 22, segments=8) + polyline([(440, 280), (460, 220)])


def oracle_phoenix():
    return polyline([
        (220, 380), (260, 240), (340, 240), (380, 380), (340, 480), (260, 480), (220, 380)
    ]) + polyline([(340, 240), (380, 160)]) + polyline([(300, 480), (300, 520)])


def oracle_ding():
    return polyline([
        (200, 200), (400, 200), (420, 420), (180, 420), (200, 200)
    ]) + vline(220, 420, 480) + vline(380, 420, 480) + hline(180, 220, 380)


# ============================================================
# 精修：中国风图标
# ============================================================
def icon_lantern():
    return circle(300, 280, 110, segments=18) + vline(300, 140, 170) + \
           vline(300, 390, 460) + hline(430, 250, 350) + hline(450, 250, 350)


def icon_cloud():
    return polyline([
        (160, 340), (220, 260), (320, 280), (380, 220), (460, 280), (440, 360),
        (360, 380), (300, 340), (240, 380), (160, 340)
    ])


def icon_bamboo():
    return vline(260, 160, 480) + vline(340, 160, 480) + \
           hline(220, 240, 360) + hline(300, 240, 360) + hline(380, 240, 360)


def icon_lotus():
    return polyline([
        (300, 140), (360, 240), (460, 300), (360, 360), (300, 460),
        (240, 360), (140, 300), (240, 240), (300, 140)
    ]) + circle(300, 300, 45, segments=10)


def icon_mountain_water():
    return polyline([
        (100, 480), (180, 280), (300, 400), (420, 240), (500, 480)
    ]) + polyline([
        (140, 440), (220, 440), (300, 440), (380, 440), (460, 440)
    ])


# 精修映射表
REFINEMENTS = {
    # 太极
    chr(0x262F): ("太极图", taiji_refined),
    # 五行
    chr(0xE000): ("金", wuxing_metal),
    chr(0xE001): ("木", wuxing_wood),
    chr(0xE002): ("水", wuxing_water),
    chr(0xE003): ("火", wuxing_fire),
    chr(0xE004): ("土", wuxing_earth),
    # 甲骨文精选
    chr(0xE100): ("日", oracle_sun),
    chr(0xE101): ("月", oracle_moon),
    chr(0xE102): ("山", oracle_mountain),
    chr(0xE103): ("水", oracle_water),
    chr(0xE104): ("火", oracle_fire),
    chr(0xE114): ("木", oracle_wood),
    chr(0xE120): ("龍", oracle_dragon),
    chr(0xE121): ("凤", oracle_phoenix),
    chr(0xE127): ("鼎", oracle_ding),
    # 中国风图标
    chr(0xE203): ("灯笼", icon_lantern),
    chr(0xE202): ("祥云", icon_cloud),
    chr(0xE206): ("竹子", icon_bamboo),
    chr(0xE207): ("莲花", icon_lotus),
    chr(0xE20C): ("山水", icon_mountain_water),
}


def refine(glyph_path: str):
    base_dir = Path(__file__).parent.parent
    glyph_path = Path(glyph_path) if glyph_path else base_dir / "glyphs" / "龍魂字元库_v0008_文化版.json"

    with open(glyph_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    refined = 0
    for char, (name, generator) in REFINEMENTS.items():
        if char not in data["字符集_cnsh9622"]:
            continue
        strokes = generator()
        data["字符集_cnsh9622"][char]["笔画路径_cnsh9622"] = strokes
        data["字符集_cnsh9622"][char]["笔画数"] = len(strokes)
        data["字符集_cnsh9622"][char]["精修时间"] = datetime.now().isoformat()
        refined += 1

    data["元数据"]["精修DNA"] = DNA
    data["元数据"]["精修时间"] = datetime.now().isoformat()

    new_path = base_dir / "glyphs" / "龍魂字元库_v0008_文化精修版.json"
    with open(new_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ 文化符号质量精修完成: {new_path}")
    print(f"   精修字符数: {refined}")
    return str(new_path)


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else None
    refine(path)
