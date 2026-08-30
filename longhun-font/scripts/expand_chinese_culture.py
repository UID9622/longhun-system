# DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-73de537c
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# DNA追溯码:#龍芯⚡️2026-06-22-LONGHUN-FONT-CULTURE-EMOJI-v1.0
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

"""
LonghunFont 道德经/文言文关键字 + 中国风表情扩展
使用 Unicode Private Use Area (PUA) U+E200 起
"""

import json
import sys
import math
from pathlib import Path
from datetime import datetime

DNA = "#龍芯⚡️2026-06-22-LONGHUN-FONT-CULTURE-EMOJI-v1.0"


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
# 中国风表情 / 文化图标
# ============================================================
CULTURE_ICONS = {
    # 神兽祥瑞
    "龙纹": polyline([
        (160, 340), (220, 260), (320, 240), (420, 280), (460, 360),
        (400, 440), (300, 460), (200, 420), (160, 340)
    ]) + circle(260, 300, 20, segments=8) + polyline([(420, 280), (440, 220)]),

    "凤纹": polyline([
        (220, 380), (260, 260), (340, 260), (380, 380), (340, 460), (260, 460), (220, 380)
    ]) + polyline([(340, 260), (380, 180)]) + polyline([(300, 460), (300, 500)]),

    "祥云": polyline([
        (160, 320), (200, 260), (280, 260), (320, 320), (400, 320), (440, 260)
    ]) + polyline([
        (220, 380), (260, 340), (340, 340), (380, 380), (460, 380)
    ]),

    # 器物饮食
    "灯笼": circle(300, 260, 100, segments=16) + vline(300, 140, 160) + vline(300, 360, 440) +
            hline(440, 260, 340) + hline(460, 260, 340),

    "红包": rect(200, 200, 400, 400) + polyline([(300, 260), (340, 300), (260, 300), (300, 260)]) +
            hline(340, 280, 320),

    "饺子": polyline([
        (200, 320), (240, 240), (360, 240), (400, 320), (360, 400), (240, 400), (200, 320)
    ]) + polyline([(240, 320), (300, 360), (360, 320)]),

    "竹子": vline(260, 160, 480) + vline(340, 160, 480) +
            hline(220, 250, 350) + hline(300, 250, 350) + hline(380, 250, 350),

    "莲花": polyline([(300, 160), (340, 260), (420, 300), (340, 340), (300, 440), (260, 340), (180, 300), (260, 260), (300, 160)]) +
            circle(300, 300, 40, segments=10),

    "茶杯": polyline([(200, 240), (200, 360), (360, 360), (360, 240)]) +
            polyline([(360, 280), (400, 260), (400, 340), (360, 320)]) +
            hline(220, 220, 340),

    "筷子": polyline([(260, 160), (260, 460)]) + polyline([(340, 160), (340, 460)]),

    "扇子": polyline([(300, 160), (420, 260), (420, 420), (300, 480), (180, 420), (180, 260), (300, 160)]) +
            polyline([(300, 160), (300, 480)]) + hline(260, 220, 380) + hline(340, 220, 380),

    "宝塔": polyline([(300, 160), (360, 220), (240, 220), (300, 160)]) +
            polyline([(240, 220), (380, 280), (220, 280), (240, 220)]) +
            polyline([(220, 280), (400, 340), (200, 340), (220, 280)]) +
            polyline([(200, 340), (420, 420), (180, 420), (200, 340)]) +
            polyline([(180, 420), (440, 500), (160, 500), (180, 420)]),

    # 自然景物
    "山水": polyline([(120, 480), (200, 280), (300, 380), (400, 240), (480, 480)]) +
            polyline([(160, 420), (240, 420)]) + polyline([(360, 420), (440, 420)]),

    "波浪": polyline([
        (120, 300), (180, 240), (240, 300), (300, 240), (360, 300), (420, 240), (480, 300)
    ]) + polyline([
        (120, 380), (180, 320), (240, 380), (300, 320), (360, 380), (420, 320), (480, 380)
    ]),

    "梅花": circle(300, 300, 50, segments=10) +
            polyline([(300, 220), (300, 140)]) + polyline([(300, 380), (300, 460)]) +
            polyline([(220, 300), (140, 300)]) + polyline([(380, 300), (460, 300)]),

    "明月": circle(300, 300, 140, segments=20) + polyline([(420, 180), (460, 140)]) +
            polyline([(440, 220), (480, 200)]),

    "风铃": vline(300, 160, 240) + circle(300, 280, 40, segments=10) +
            polyline([(300, 320), (300, 420)]) + circle(300, 450, 25, segments=8),

    # 节庆装饰
    "鞭炮": polyline([(240, 160), (240, 400)]) + polyline([(300, 160), (300, 400)]) +
            polyline([(360, 160), (360, 400)]) + polyline([(220, 400), (260, 440)]) +
            polyline([(280, 400), (320, 440)]) + polyline([(340, 400), (380, 440)]),

    "风筝": polyline([(300, 160), (420, 280), (300, 400), (180, 280), (300, 160)]) +
            polyline([(300, 280), (300, 420)]) + polyline([(300, 420), (260, 480)]) +
            polyline([(300, 420), (340, 480)]),

    "锦鲤": polyline([
        (160, 320), (240, 260), (360, 260), (440, 320), (380, 400), (260, 400), (160, 320)
    ]) + polyline([(440, 320), (480, 280)]) + circle(320, 320, 15, segments=6),

    "月饼": circle(300, 300, 160, segments=20) + circle(300, 300, 80, segments=12) +
            polyline([(300, 220), (300, 380)]) + polyline([(220, 300), (380, 300)]),

    "酒坛": polyline([(220, 240), (380, 240), (380, 420), (220, 420), (220, 240)]) +
            hline(220, 240, 380) + hline(260, 240, 360) + polyline([(260, 240), (260, 180), (340, 180), (340, 240)]),

    "笛子": vline(300, 160, 480) + hline(220, 280, 320) + hline(280, 280, 320) +
            hline(340, 280, 320) + hline(400, 280, 320),

    "大鼓": circle(300, 300, 140, segments=18) + circle(300, 300, 100, segments=14) +
            vline(180, 300, 460) + vline(420, 300, 460),

    "门楼": polyline([(160, 480), (160, 200), (300, 120), (440, 200), (440, 480)]) +
            polyline([(240, 480), (240, 320), (360, 320), (360, 480)]) +
            hline(200, 180, 420) + hline(240, 180, 420),

    # 哲学概念艺术字
    "道": polyline([(300, 160), (220, 260), (380, 260), (300, 360), (220, 460)]) +
          polyline([(300, 360), (380, 460)]),

    "德": vline(260, 160, 480) + hline(220, 220, 380) + hline(300, 220, 380) +
          hline(380, 220, 380) + polyline([(340, 220), (340, 460)]),

    "无": polyline([(180, 240), (420, 240)]) + polyline([(240, 240), (240, 440)]) +
          polyline([(360, 240), (360, 440)]) + hline(440, 220, 380),

    "自然": polyline([(200, 300), (260, 200), (320, 300), (380, 200), (420, 300)]) +
            polyline([(180, 400), (300, 460), (420, 400)]),
}


def expand(glyph_path: str):
    base_dir = Path(__file__).parent.parent
    glyph_path = Path(glyph_path) if glyph_path else base_dir / "glyphs" / "龍魂字元库_v0007_甲骨文版.json"

    with open(glyph_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    added = 0
    base_code = 0xE200
    for idx, (name, strokes) in enumerate(CULTURE_ICONS.items()):
        code = base_code + idx
        char = chr(code)
        if char in data["字符集_cnsh9622"]:
            continue
        data["字符集_cnsh9622"][char] = {
            "unicode": f"U+{code:04X}",
            "笔画数": len(strokes),
            "结构": "PUA文化图标",
            "名称": name,
            "风格参数": {"力度": 0.8, "棱角": 0.3, "节奏": 0.6, "墨色": 0.9},
            "笔画路径_cnsh9622": strokes
        }
        added += 1

    data["元数据"]["版本"] = "v0008-文化版"
    data["元数据"]["描述"] = f"LonghunFont 文化版字元库，含 {len(data['字符集_cnsh9622'])} 个字符（汉字+拉丁+易经+五行+甲骨文+中国风图标）"
    data["元数据"]["文化扩展时间"] = datetime.now().isoformat()
    data["元数据"]["文化扩展DNA"] = DNA

    new_path = base_dir / "glyphs" / "龍魂字元库_v0008_文化版.json"
    with open(new_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ 已扩展文化版字元库: {new_path}")
    print(f"   新增文化图标: {added}")
    print(f"   总字符数: {len(data['字符集_cnsh9622'])}")
    return str(new_path)


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else None
    expand(path)
