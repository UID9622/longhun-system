# DNA: #龍芯⚡️丙午·乙未·乙丑·比-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# DNA追溯码:#龍芯⚡️2026-06-22-LONGHUN-FONT-ORACLE-BONE-v1.0

"""
LonghunFont 甲骨文字符扩展
使用 Unicode Private Use Area (PUA) U+E100 起
选取 50 个高频甲骨文字形，用折线近似象形轮廓
"""

import json
import sys
import math
from pathlib import Path
from datetime import datetime

DNA = "#龍芯⚡️2026-06-22-LONGHUN-FONT-ORACLE-BONE-v1.0"


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
# 50 个甲骨文字形（简化象形）
# ============================================================
ORACLE_BONE = {
    # 天文地理
    "日": circle(300, 300, 120, segments=16) + circle(300, 300, 20, segments=8),
    "月": arc(300, 300, 140, math.pi / 4, 7 * math.pi / 4, segments=20),
    "山": polyline([(120, 480), (220, 180), (300, 320), (380, 180), (480, 480)]),
    "水": polyline([(150, 180), (200, 320), (300, 360), (400, 320), (450, 180)]) +
          polyline([(200, 320), (180, 420)]) +
          polyline([(400, 320), (420, 420)]),
    "火": polyline([(300, 120), (360, 280), (300, 240), (240, 280), (300, 120)]) +
          polyline([(300, 280), (300, 420)]),
    "土": hline(440, 120, 480) + polyline([(180, 440), (260, 280), (340, 440)]),
    "石": polyline([(180, 420), (240, 240), (360, 240), (420, 420), (180, 420)]),
    "田": rect(160, 200, 440, 440) + hline(320, 160, 440) + vline(300, 200, 440),
    "雨": hline(160, 140, 460) + polyline([(180, 160), (160, 260)]) +
          polyline([(260, 160), (240, 260)]) +
          polyline([(340, 160), (320, 260)]) +
          polyline([(420, 160), (400, 260)]),
    "雪": hline(160, 140, 460) + polyline([(200, 180), (200, 260)]) +
          polyline([(300, 180), (300, 260)]) +
          polyline([(400, 180), (400, 260)]),

    # 人物
    "人": polyline([(300, 160), (200, 360), (300, 480), (400, 360), (300, 160)]),
    "大": polyline([(300, 120), (300, 480)]) +
          polyline([(180, 220), (300, 320), (420, 220)]) +
          polyline([(200, 460), (300, 360), (400, 460)]),
    "天": polyline([(300, 160), (220, 320), (300, 420), (380, 320), (300, 160)]) +
          hline(120, 180, 420),
    "王": hline(160, 160, 440) + vline(300, 160, 440) + hline(300, 180, 420) + hline(440, 180, 420),
    "父": vline(300, 140, 440) + polyline([(200, 200), (300, 280), (400, 200)]),
    "母": polyline([(240, 160), (240, 360), (360, 360), (360, 160)]) +
          circle(260, 260, 30, segments=8) + circle(340, 260, 30, segments=8),
    "子": circle(300, 220, 60, segments=12) + polyline([(300, 280), (260, 440), (340, 440)]),
    "女": polyline([(300, 160), (220, 320), (300, 420), (380, 320), (300, 160)]) +
          polyline([(220, 320), (160, 460)]),
    "夫": polyline([(300, 160), (220, 320), (300, 420), (380, 320), (300, 160)]) +
          hline(120, 180, 420),
    "老": polyline([(260, 160), (260, 280), (340, 280), (340, 160)]) +
          polyline([(240, 320), (240, 460), (360, 460), (360, 320)]),

    # 动植物
    "木": vline(300, 160, 480) + polyline([(300, 260), (180, 180)]) +
          polyline([(300, 340), (420, 260)]) + polyline([(300, 180), (300, 120)]),
    "禾": vline(300, 220, 480) + polyline([(300, 280), (200, 200)]) +
          polyline([(300, 280), (400, 200)]) + polyline([(300, 180), (300, 140)]),
    "草": polyline([(200, 420), (200, 240), (160, 160)]) +
          polyline([(300, 420), (300, 220), (260, 140)]) +
          polyline([(400, 420), (400, 240), (360, 160)]),
    "虫": polyline([(180, 300), (220, 220), (300, 200), (380, 220), (420, 300)]) +
          circle(220, 320, 30, segments=8) + circle(300, 360, 35, segments=8) + circle(380, 320, 30, segments=8),
    "鱼": polyline([(160, 300), (260, 220), (380, 220), (440, 300), (360, 380), (240, 380), (160, 300)]) +
          circle(320, 300, 20, segments=8) + polyline([(440, 300), (480, 260)]),
    "鸟": polyline([(200, 360), (260, 260), (360, 260), (420, 360), (360, 440), (260, 440), (200, 360)]) +
          polyline([(360, 260), (400, 180)]) + circle(300, 320, 15, segments=6),
    "犬": polyline([(200, 300), (260, 220), (340, 220), (400, 300), (340, 400), (260, 400), (200, 300)]) +
          polyline([(340, 220), (360, 160)]) + polyline([(260, 400), (240, 460)]),
    "牛": polyline([(220, 340), (260, 240), (340, 240), (380, 340), (340, 440), (260, 440), (220, 340)]) +
          polyline([(260, 240), (220, 180)]) + polyline([(340, 240), (380, 180)]),
    "羊": polyline([(220, 340), (260, 240), (340, 240), (380, 340), (340, 440), (260, 440), (220, 340)]) +
          polyline([(260, 240), (240, 160)]) + polyline([(340, 240), (360, 160)]),
    "马": polyline([(180, 360), (240, 260), (360, 260), (420, 360), (380, 440), (280, 440), (220, 360)]) +
          polyline([(360, 260), (400, 180)]) + polyline([(380, 440), (420, 480)]),
    "鹿": polyline([(200, 340), (260, 240), (340, 240), (400, 340), (340, 440), (260, 440), (200, 340)]) +
          polyline([(260, 240), (240, 140)]) + polyline([(340, 240), (360, 140)]) +
          polyline([(200, 340), (160, 300)]),
    "虎": polyline([(200, 340), (260, 220), (340, 220), (400, 340), (340, 460), (260, 460), (200, 340)]) +
          polyline([(260, 280), (340, 280)]) + polyline([(260, 360), (340, 360)]),
    "龍": polyline([(160, 340), (220, 240), (320, 220), (420, 260), (440, 360), (380, 440), (280, 460), (180, 420), (160, 340)]) +
          circle(260, 300, 20, segments=8),
    "凤": polyline([(220, 380), (260, 260), (340, 260), (380, 380), (340, 460), (260, 460), (220, 380)]) +
          polyline([(340, 260), (380, 180)]) + polyline([(300, 460), (300, 500)]),
    "龟": polyline([(220, 320), (260, 240), (340, 240), (380, 320), (340, 420), (260, 420), (220, 320)]) +
          polyline([(260, 420), (240, 480)]) + polyline([(340, 420), (360, 480)]) +
          polyline([(260, 240), (240, 180)]) + polyline([(340, 240), (360, 180)]),

    # 器物建筑
    "刀": polyline([(160, 180), (400, 180), (440, 240), (220, 240), (160, 180)]) +
          polyline([(220, 240), (180, 420)]),
    "弓": arc(300, 300, 180, -math.pi / 2, math.pi / 2, segments=20) +
          polyline([(300, 140), (300, 460)]),
    "矢": vline(300, 160, 440) + polyline([(220, 240), (380, 240)]) + polyline([(280, 440), (320, 440)]),
    "戈": vline(300, 140, 460) + hline(260, 160, 440) + hline(340, 180, 420) + polyline([(300, 460), (260, 500)]),
    "鼎": polyline([(200, 200), (400, 200), (420, 420), (180, 420), (200, 200)]) +
          vline(220, 420, 480) + vline(380, 420, 480) + hline(180, 220, 380),
    "门": polyline([(160, 160), (160, 480)]) + polyline([(440, 160), (440, 480)]) +
          hline(160, 160, 440) + vline(300, 160, 480),
    "户": polyline([(160, 160), (160, 480)]) + hline(160, 160, 440) + polyline([(440, 160), (440, 320)]),
    "井": rect(200, 200, 400, 400) + hline(300, 200, 400) + vline(300, 200, 400),
    "邑": rect(160, 180, 440, 460) + polyline([(220, 240), (220, 320), (300, 320), (300, 240)]) +
          polyline([(340, 360), (340, 420), (400, 420), (400, 360)]),

    # 占卜吉凶
    "卜": vline(300, 160, 440) + polyline([(220, 260), (300, 320), (380, 260)]),
    "占": polyline([(200, 200), (200, 320), (400, 320), (400, 200)]) + vline(300, 320, 460),
    "吉": polyline([(180, 220), (300, 160), (420, 220), (420, 320), (300, 380), (180, 320), (180, 220)]) +
          hline(420, 180, 420),
    "凶": polyline([(180, 200), (420, 200), (420, 440), (180, 440), (180, 200)]) +
          polyline([(240, 280), (360, 360)]) + polyline([(360, 280), (240, 360)]),

    # 时间方位
    "东": polyline([(300, 140), (300, 460)]) +
          polyline([(180, 260), (420, 260)]) + polyline([(200, 340), (400, 340)]),
    "西": polyline([(180, 220), (420, 220)]) + polyline([(180, 300), (420, 300)]) +
          polyline([(180, 380), (420, 380)]),
    "南": vline(260, 160, 440) + polyline([(260, 160), (420, 220), (420, 380), (260, 440)]),
    "北": polyline([(180, 300), (420, 300)]) + polyline([(300, 180), (240, 300), (300, 420)]) +
          polyline([(300, 180), (360, 300), (300, 420)]),
    "上": vline(300, 160, 440) + hline(160, 180, 420) + polyline([(260, 200), (300, 160), (340, 200)]),
    "下": vline(300, 160, 440) + hline(440, 180, 420) + polyline([(260, 400), (300, 440), (340, 400)]),
    "中": hline(220, 180, 420) + vline(300, 220, 420) + hline(420, 180, 420),
}


def expand(glyph_path: str):
    base_dir = Path(__file__).parent.parent
    glyph_path = Path(glyph_path) if glyph_path else base_dir / "glyphs" / "龍魂字元库_v0006_五行版.json"

    with open(glyph_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    added = 0
    base_code = 0xE100
    for idx, (name, strokes) in enumerate(ORACLE_BONE.items()):
        code = base_code + idx
        char = chr(code)
        if char in data["字符集_cnsh9622"]:
            continue
        data["字符集_cnsh9622"][char] = {
            "unicode": f"U+{code:04X}",
            "笔画数": len(strokes),
            "结构": "甲骨文",
            "对应汉字": name,
            "风格参数": {"力度": 0.85, "棱角": 0.35, "节奏": 0.5, "墨色": 0.9},
            "笔画路径_cnsh9622": strokes
        }
        added += 1

    data["元数据"]["版本"] = "v0007-甲骨文版"
    data["元数据"]["描述"] = f"LonghunFont 甲骨文版字元库，含 {len(data['字符集_cnsh9622'])} 个字符"
    data["元数据"]["甲骨文扩展时间"] = datetime.now().isoformat()
    data["元数据"]["甲骨文扩展DNA"] = DNA

    new_path = base_dir / "glyphs" / "龍魂字元库_v0007_甲骨文版.json"
    with open(new_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ 已扩展甲骨文版字元库: {new_path}")
    print(f"   新增甲骨文字符: {added}")
    print(f"   总字符数: {len(data['字符集_cnsh9622'])}")
    return str(new_path)


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else None
    expand(path)
