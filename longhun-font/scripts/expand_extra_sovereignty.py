# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# DNA追溯码:#龍芯⚡️2026-06-22-LONGHUN-FONT-FRAGMENT-EXTRA-SOVEREIGNTY-v1.0

"""
LonghunFont 扩展：20 枚中华文化主权图标碎片
PUA 起点 U+E460，仅输出独立碎片文件，不加载/不修改完整字元库。
"""

import json
import math
from pathlib import Path
from datetime import datetime

DNA = "#龍芯⚡️2026-06-22-LONGHUN-FONT-FRAGMENT-EXTRA-SOVEREIGNTY-v1.0"


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


def star(cx, cy, r, segments=8):
    return circle(cx, cy, r, segments=segments)


# ============================================================
# 20 枚主权文化图标
# ============================================================
SOVEREIGNTY_ICONS = [
    # 1. 北斗七星
    (
        "北斗七星",
        polyline([(180, 220), (240, 200), (300, 230), (360, 260), (420, 250),
                  (460, 300), (500, 360)])
        + star(180, 220, 14, 6) + star(240, 200, 14, 6) + star(300, 230, 14, 6)
        + star(360, 260, 14, 6) + star(420, 250, 14, 6) + star(460, 300, 14, 6)
        + star(500, 360, 14, 6)
    ),

    # 2. 青龍
    (
        "青龍",
        polyline([
            (160, 420), (200, 340), (180, 280), (260, 240), (360, 260),
            (420, 220), (480, 260), (440, 320), (360, 360), (300, 420),
            (220, 460), (160, 420)
        ])
        + circle(230, 290, 18, 8)
        + polyline([(420, 220), (460, 180)])
        + polyline([(420, 220), (460, 240)])
    ),

    # 3. 白虎
    (
        "白虎",
        polyline([
            (180, 440), (220, 360), (200, 280), (280, 240), (380, 260),
            (460, 220), (480, 300), (420, 360), (340, 400), (260, 460), (180, 440)
        ])
        + circle(270, 300, 18, 8)
        + polyline([(460, 220), (490, 180)])
        + polyline([(460, 220), (490, 240)])
        + polyline([(340, 400), (360, 480)])
    ),

    # 4. 朱雀
    (
        "朱雀",
        polyline([
            (300, 160), (360, 260), (460, 300), (380, 360), (340, 460),
            (300, 400), (260, 460), (220, 360), (140, 300), (240, 260), (300, 160)
        ])
        + circle(300, 300, 24, 10)
        + polyline([(300, 160), (300, 120)])
        + polyline([(340, 460), (360, 500)])
        + polyline([(260, 460), (240, 500)])
    ),

    # 5. 玄武
    (
        "玄武",
        circle(300, 340, 110, 18)
        + polyline([
            (250, 280), (280, 250), (330, 270), (360, 320), (340, 380),
            (290, 400), (240, 370), (230, 320), (250, 280)
        ])
        + circle(300, 320, 16, 8)
        + polyline([(300, 230), (300, 180)])
    ),

    # 6. 福
    (
        "福",
        vline(260, 160, 480)
        + hline(220, 180, 340)
        + hline(300, 180, 340)
        + hline(380, 180, 340)
        + vline(340, 220, 380)
        + rect(380, 240, 460, 420)
    ),

    # 7. 禄
    (
        "禄",
        vline(240, 160, 480)
        + hline(220, 180, 320)
        + hline(300, 180, 320)
        + vline(340, 220, 460)
        + polyline([(360, 240), (440, 240), (440, 320), (360, 320), (360, 240)])
        + polyline([(400, 320), (400, 460)])
    ),

    # 8. 寿
    (
        "寿",
        polyline([(220, 200), (300, 160), (380, 200)])
        + hline(240, 200, 400)
        + vline(300, 240, 480)
        + hline(320, 220, 380)
        + hline(400, 220, 380)
        + polyline([(380, 400), (440, 460)])
    ),

    # 9. 喜
    (
        "喜",
        hline(180, 180, 420)
        + hline(260, 180, 420)
        + vline(240, 180, 420)
        + vline(360, 180, 420)
        + hline(340, 180, 420)
        + hline(420, 180, 420)
    ),

    # 10. 财
    (
        "财",
        vline(220, 160, 480)
        + hline(220, 180, 320)
        + hline(300, 180, 320)
        + hline(380, 180, 320)
        + vline(340, 220, 460)
        + polyline([(380, 240), (460, 200), (460, 460), (380, 420)])
    ),

    # 11. 砚台
    (
        "砚台",
        rect(180, 240, 420, 420)
        + rect(240, 300, 360, 380)
        + polyline([(380, 300), (420, 260), (440, 300)])
    ),

    # 12. 笔架
    (
        "笔架",
        hline(460, 160, 440)
        + polyline([(200, 460), (240, 300), (300, 260), (360, 300), (400, 460)])
        + vline(300, 260, 160)
        + vline(240, 300, 180)
        + vline(360, 300, 180)
    ),

    # 13. 印章
    (
        "印章",
        rect(220, 340, 380, 460)
        + polyline([(260, 340), (260, 260), (340, 260), (340, 340)])
        + polyline([(280, 380), (320, 380)])
        + polyline([(280, 420), (320, 420)])
    ),

    # 14. 镇纸
    (
        "镇纸",
        rect(160, 280, 440, 360)
        + hline(310, 180, 420)
        + hline(340, 180, 420)
        + polyline([(220, 320), (260, 320)])
        + polyline([(340, 320), (380, 320)])
    ),

    # 15. 香炉
    (
        "香炉",
        polyline([(200, 400), (260, 400), (300, 340), (340, 400), (400, 400)])
        + circle(300, 420, 70, 14)
        + vline(300, 270, 160)
        + polyline([(300, 200), (320, 160), (280, 160), (300, 200)])
    ),

    # 16. 烛台
    (
        "烛台",
        vline(300, 160, 420)
        + polyline([(260, 420), (340, 420), (340, 480), (260, 480), (260, 420)])
        + polyline([(300, 420), (300, 360)])
        + polyline([(280, 360), (320, 360)])
        + polyline([(300, 300), (300, 240)])
        + polyline([(290, 220), (310, 240), (290, 240), (310, 220)])
    ),

    # 17. 锣鼓
    (
        "锣鼓",
        circle(300, 300, 120, 18)
        + circle(300, 300, 80, 14)
        + vline(180, 300, 460)
        + vline(420, 300, 460)
        + hline(460, 240, 360)
    ),

    # 18. 唢呐
    (
        "唢呐",
        polyline([
            (180, 340), (260, 320), (340, 300), (420, 260), (460, 220)
        ])
        + polyline([(420, 260), (480, 240), (480, 320), (420, 300)])
        + circle(300, 310, 30, 10)
        + circle(340, 300, 20, 8)
    ),

    # 19. 香囊
    (
        "香囊",
        polyline([
            (300, 160), (260, 220), (200, 280), (220, 400), (300, 460),
            (380, 400), (400, 280), (340, 220), (300, 160)
        ])
        + circle(300, 320, 50, 12)
        + polyline([(300, 460), (300, 500)])
        + circle(300, 515, 15, 8)
    ),

    # 20. 麒麟
    (
        "麒麟",
        polyline([
            (180, 400), (220, 320), (300, 280), (400, 300), (460, 260),
            (480, 340), (420, 380), (340, 420), (260, 460), (180, 400)
        ])
        + circle(280, 330, 18, 8)
        + polyline([(460, 260), (490, 220)])
        + polyline([(460, 260), (490, 280)])
        + polyline([(340, 420), (360, 480)])
    ),
]


def build_fragment():
    fragment = {}
    base_code = 0xE460
    for idx, (name, strokes) in enumerate(SOVEREIGNTY_ICONS):
        code = base_code + idx
        char = chr(code)
        fragment[char] = {
            "unicode": f"U+{code:04X}",
            "笔画数": len(strokes),
            "结构": "文化主权图标",
            "名称": name,
            "风格参数": {"力度": 0.85, "棱角": 0.35, "节奏": 0.5, "墨色": 0.9},
            "笔画路径_cnsh9622": strokes,
        }
    return fragment


if __name__ == "__main__":
    base_dir = Path(__file__).parent.parent
    out_path = base_dir / "glyphs" / "fragments" / "extra_sovereignty.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    fragment = build_fragment()
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(fragment, f, ensure_ascii=False, indent=2)

    codes = [int(k.encode("unicode_escape").decode("ascii").replace("\\u", ""), 16)
             for k in fragment.keys()]
    start, end = min(codes), max(codes)

    print(f"✅ 已生成文化主权图标碎片: {out_path}")
    print(f"   数量: {len(fragment)}")
    print(f"   范围: U+{start:04X} .. U+{end:04X}")
    print(f"   DNA: {DNA}")
