# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# DNA追溯码:#龍芯⚡️2026-06-22-LONGHUN-FONT-FRAGMENT-SUZHOU_MOTIFS-v1.0

"""
LonghunFont 苏州码子 + 传统纹样片段生成器
使用 Unicode Private Use Area (PUA) U+E447 起，共 25 个符号
"""

import json
import math
import sys
from pathlib import Path
from datetime import datetime

DNA = "#龍芯⚡️2026-06-22-LONGHUN-FONT-FRAGMENT-SUZHOU_MOTIFS-v1.0"
SET_NAME = "suzhou_motifs"
SET_DESCRIPTION = "苏州码子 and traditional motifs"
COUNT = 25
START_CODEPOINT = 0xE447


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


def arc(cx, cy, r, start_angle, end_angle, segments=12):
    pts = []
    for i in range(segments + 1):
        a = start_angle + (end_angle - start_angle) * i / segments
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return polyline(pts)


def hline(y, x1, x2):
    return polyline([(x1, y), (x2, y)])


def vline(x, y1, y2):
    return polyline([(x, y1), (x, y2)])


def rect(x1, y1, x2, y2):
    return polyline([(x1, y1), (x2, y1), (x2, y2), (x1, y2), (x1, y1)])


# ============================================================
# 苏州码子（10 个）+ 传统纹样（15 个），共 25 个
# ============================================================
SUZHOU_MOTIFS = [
    # 苏州码子
    ("〇", "苏州码子", "〇"),
    ("〡", "苏州码子", "〡"),
    ("〢", "苏州码子", "〢"),
    ("〣", "苏州码子", "〣"),
    ("〤", "苏州码子", "〤"),
    ("〥", "苏州码子", "〥"),
    ("〦", "苏州码子", "〦"),
    ("〧", "苏州码子", "〧"),
    ("〨", "苏州码子", "〨"),
    ("〩", "苏州码子", "〩"),
    # 传统纹样
    ("如意", "传统纹样", "如意"),
    ("中国结", "传统纹样", "中国结"),
    ("元宝", "传统纹样", "元宝"),
    ("铜钱", "传统纹样", "铜钱"),
    ("寿桃", "传统纹样", "寿桃"),
    ("蝙蝠", "传统纹样", "蝙蝠"),
    ("云纹", "传统纹样", "云纹"),
    ("回纹", "传统纹样", "回纹"),
    ("海浪", "传统纹样", "海浪"),
    ("火焰", "传统纹样", "火焰"),
    ("莲花", "传统纹样", "莲花"),
    ("宝相花", "传统纹样", "宝相花"),
    ("牡丹", "传统纹样", "牡丹"),
    ("梅花", "传统纹样", "梅花"),
    ("竹子", "传统纹样", "竹子"),
]


def build_suzhou_glyph(name):
    """根据苏州码子名称生成简化笔画路径。"""
    if name == "〇":
        return circle(300, 300, 180, segments=20)
    if name == "〡":
        return vline(300, 140, 460)
    if name == "〢":
        return vline(260, 140, 460) + vline(340, 140, 460)
    if name == "〣":
        return vline(220, 140, 460) + vline(300, 140, 460) + vline(380, 140, 460)
    if name == "〤":
        return polyline([(180, 180), (420, 420)]) + polyline([(420, 180), (180, 420)])
    if name == "〥":
        # 横线中点向下斜
        return hline(180, 180, 420) + polyline([(300, 180), (220, 420)])
    if name == "〦":
        # T 形
        return hline(180, 180, 420) + vline(300, 180, 420)
    if name == "〧":
        # 倒 T 形
        return hline(420, 180, 420) + vline(300, 180, 420)
    if name == "〨":
        # 倒八字 / 人字形
        return polyline([(180, 180), (300, 420), (420, 180)])
    if name == "〩":
        # 钩形
        return polyline([(180, 180), (420, 180), (420, 300), (300, 420)])
    return []


def build_motif_glyph(name):
    """根据传统纹样名称生成简化笔画路径。"""
    if name == "如意":
        # 云头 + 柄
        return arc(260, 240, 80, math.pi / 2, 3 * math.pi / 2, segments=12) + \
               arc(340, 240, 80, -math.pi / 2, math.pi / 2, segments=12) + \
               polyline([(260, 320), (300, 460), (340, 320)])
    if name == "中国结":
        # 菱形结 + 流苏
        return polyline([(300, 180), (420, 300), (300, 420), (180, 300), (300, 180)]) + \
               polyline([(300, 420), (260, 480)]) + polyline([(300, 420), (340, 480)])
    if name == "元宝":
        # 船形元宝
        return polyline([(180, 340), (260, 260), (340, 260), (420, 340), (340, 400), (260, 400), (180, 340)])
    if name == "铜钱":
        # 外圆内方
        return circle(300, 300, 160, segments=20) + rect(250, 250, 350, 350)
    if name == "寿桃":
        # 桃形 + 叶
        return polyline([(300, 160), (360, 260), (420, 300), (360, 420), (300, 460), (240, 420), (180, 300), (240, 260), (300, 160)]) + \
               polyline([(300, 160), (360, 140), (380, 180)])
    if name == "蝙蝠":
        # 简笔蝙蝠
        return circle(300, 340, 50, segments=10) + \
               polyline([(300, 300), (220, 220), (180, 280)]) + \
               polyline([(300, 300), (380, 220), (420, 280)])
    if name == "云纹":
        # 卷云
        return arc(240, 300, 80, math.pi, 0, segments=12) + \
               arc(360, 300, 80, 0, math.pi, segments=12) + \
               polyline([(160, 300), (240, 300)]) + polyline([(360, 300), (440, 300)])
    if name == "回纹":
        # 回字形螺旋
        return polyline([(180, 180), (420, 180), (420, 420), (180, 420), (180, 260), (340, 260), (340, 340), (260, 340)])
    if name == "海浪":
        # 三道波浪
        return polyline([(120, 260), (180, 200), (240, 260), (300, 200), (360, 260), (420, 200), (480, 260)]) + \
               polyline([(120, 340), (180, 280), (240, 340), (300, 280), (360, 340), (420, 280), (480, 340)]) + \
               polyline([(120, 420), (180, 360), (240, 420), (300, 360), (360, 420), (420, 360), (480, 420)])
    if name == "火焰":
        # 三焰
        return polyline([(300, 460), (260, 360), (300, 280), (340, 360), (300, 460)]) + \
               polyline([(300, 360), (220, 260), (300, 160), (380, 260), (300, 360)])
    if name == "莲花":
        # 莲瓣 + 花心
        return polyline([(300, 160), (340, 260), (420, 300), (340, 340), (300, 440), (260, 340), (180, 300), (260, 260), (300, 160)]) + \
               circle(300, 300, 40, segments=10)
    if name == "宝相花":
        # 放射花瓣
        center = circle(300, 300, 50, segments=10)
        petals = []
        for angle in [0, math.pi / 4, math.pi / 2, 3 * math.pi / 4, math.pi, 5 * math.pi / 4, 3 * math.pi / 2, 7 * math.pi / 4]:
            x1 = 300 + 60 * math.cos(angle)
            y1 = 300 + 60 * math.sin(angle)
            x2 = 300 + 150 * math.cos(angle)
            y2 = 300 + 150 * math.sin(angle)
            petals.extend(polyline([(x1, y1), (x2, y2)]))
        return center + petals
    if name == "牡丹":
        # 花心 + 层叠花瓣
        return circle(300, 300, 40, segments=10) + \
               circle(300, 300, 90, segments=14) + \
               polyline([(300, 210), (300, 160)]) + polyline([(300, 390), (300, 440)]) + \
               polyline([(210, 300), (160, 300)]) + polyline([(390, 300), (440, 300)])
    if name == "梅花":
        # 五瓣 + 花蕊
        return circle(300, 300, 60, segments=10) + \
               polyline([(300, 220), (300, 140)]) + polyline([(300, 380), (300, 460)]) + \
               polyline([(220, 300), (140, 300)]) + polyline([(380, 300), (460, 300)])
    if name == "竹子":
        # 双竿 + 节
        return vline(260, 160, 480) + vline(340, 160, 480) + \
               hline(220, 250, 350) + hline(300, 250, 350) + hline(380, 250, 350)
    return []


def build_glyph_strokes(name, structure):
    if structure == "苏州码子":
        return build_suzhou_glyph(name)
    return build_motif_glyph(name)


def build_fragment():
    fragment = {}
    for idx, (name, structure, display_name) in enumerate(SUZHOU_MOTIFS):
        code = START_CODEPOINT + idx
        char = chr(code)
        strokes = build_glyph_strokes(name, structure)
        fragment[char] = {
            "unicode": f"U+{code:04X}",
            "笔画数": len(strokes),
            "结构": structure,
            "名称": display_name,
            "风格参数": {"力度": 0.85, "棱角": 0.35, "节奏": 0.5, "墨色": 0.9},
            "笔画路径_cnsh9622": strokes
        }
    return fragment


def main():
    base_dir = Path(__file__).parent.parent
    out_dir = base_dir / "glyphs" / "fragments"
    out_dir.mkdir(parents=True, exist_ok=True)

    fragment = build_fragment()
    out_path = out_dir / f"{SET_NAME}.json"

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(fragment, f, ensure_ascii=False, indent=2)

    start_u = f"U+{START_CODEPOINT:04X}"
    end_u = f"U+{START_CODEPOINT + COUNT - 1:04X}"
    timestamp = datetime.now().isoformat()

    print(f"✅ 已生成符号集片段: {out_path}")
    print(f"   符号集名称: {SET_NAME}")
    print(f"   描述: {SET_DESCRIPTION}")
    print(f"   数量: {COUNT}")
    print(f"   码位范围: {start_u} .. {end_u}")
    print(f"   DNA: {DNA}")
    print(f"   生成时间: {timestamp}")


if __name__ == "__main__":
    main()
