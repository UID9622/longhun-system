#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·壬午·䷇比-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
#!/usr/bin/env python3
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# DNA追溯码:#龍芯⚡️丙午·甲午·丁卯·丙午·䷚颐-LONGHUN-FONT-FRAGMENT-MORE_ORACLE_BONE-v1.0

"""
LonghunFont 更多甲骨文字符扩展
使用 Unicode Private Use Area (PUA) U+E16A 起
选取 50 个常见且形准的甲骨文字形，用折线近似象形轮廓
仅输出碎片 JSON，不加载/保存完整字元库
"""

import json
import math
from pathlib import Path
from datetime import datetime

DNA = "#龍芯⚡️丙午·甲午·丁卯·丙午·䷚颐-LONGHUN-FONT-FRAGMENT-MORE_ORACLE_BONE-v1.0"
SYMBOL_SET = "more_oracle_bone"
DESCRIPTION = "more oracle bone glyphs"
COUNT = 50
START_CODEPOINT = 0xE16A


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
# 50 个更多甲骨文字形（简化象形）
# ============================================================
MORE_ORACLE_BONE = {
    # 农工商贸
    "农": circle(300, 180, 40, segments=10) +
          polyline([(300, 220), (260, 320), (340, 320), (300, 220)]) +
          polyline([(260, 320), (180, 420)]) +
          polyline([(340, 320), (420, 420)]) +
          polyline([(220, 360), (380, 360)]),

    "工": hline(180, 180, 420) + vline(300, 180, 420) + hline(420, 220, 380),

    "商": polyline([(220, 180), (380, 180), (360, 220), (360, 420),
                    (240, 420), (240, 220), (220, 180)]) +
          vline(300, 220, 420) + hline(440, 280, 320),

    "贾": hline(180, 180, 420) +
          polyline([(200, 200), (200, 380), (400, 380), (400, 200)]) +
          polyline([(240, 280), (360, 280), (300, 340), (240, 280)]) +
          hline(400, 240, 360),

    "贝": polyline([(200, 220), (300, 180), (400, 220), (400, 400),
                    (300, 440), (200, 400), (200, 220)]) +
          hline(260, 240, 360) + hline(340, 240, 360),

    "玉": hline(180, 180, 420) + vline(300, 180, 420) +
          hline(300, 220, 380) + hline(420, 220, 380) + circle(300, 340, 30, segments=8),

    "丝": polyline([(200, 180), (200, 420)]) + polyline([(240, 180), (240, 420)]) +
          polyline([(360, 180), (360, 420)]) + polyline([(400, 180), (400, 420)]) +
          polyline([(240, 280), (360, 280), (320, 320), (360, 360)]),

    "帛": rect(200, 200, 400, 400) +
          polyline([(220, 400), (220, 460)]) + polyline([(260, 400), (260, 460)]) +
          polyline([(340, 400), (340, 460)]) + polyline([(380, 400), (380, 460)]),

    "衣": polyline([(300, 160), (180, 280), (180, 440), (420, 440),
                    (420, 280), (300, 160)]) +
          vline(300, 160, 440) + hline(280, 220, 380),

    "冠": polyline([(200, 240), (300, 160), (400, 240), (400, 320),
                    (200, 320), (200, 240)]) +
          hline(360, 180, 420) + vline(300, 320, 420),

    # 交通住行
    "舟": polyline([(160, 300), (220, 220), (380, 220), (440, 300),
                    (380, 380), (220, 380), (160, 300)]) +
          hline(260, 220, 380) + vline(300, 220, 180),

    "车": hline(200, 180, 420) + hline(320, 180, 420) +
          vline(220, 200, 400) + vline(380, 200, 400) +
          circle(220, 400, 50, segments=10) + circle(380, 400, 50, segments=10),

    "行": hline(300, 160, 440) + vline(300, 160, 440) +
          polyline([(200, 200), (160, 240)]) + polyline([(440, 200), (480, 240)]) +
          polyline([(200, 400), (160, 440)]) + polyline([(440, 400), (480, 440)]),

    "走": circle(300, 180, 40, segments=10) +
          polyline([(300, 220), (260, 320), (340, 320), (300, 220)]) +
          polyline([(260, 320), (220, 460)]) +
          polyline([(340, 320), (420, 420)]) +
          hline(420, 220, 380),

    "立": circle(300, 180, 40, segments=10) +
          vline(300, 220, 420) + hline(320, 220, 380) + hline(440, 180, 420),

    "坐": polyline([(220, 260), (260, 220), (340, 220), (380, 260),
                    (380, 360), (340, 400), (260, 400), (220, 360), (220, 260)]) +
          hline(420, 180, 420),

    # 饮食视听
    "食": polyline([(200, 220), (400, 220), (420, 380), (300, 440),
                    (180, 380), (200, 220)]) +
          hline(200, 200, 400) +
          polyline([(260, 280), (340, 280), (300, 340), (260, 280)]),

    "饮": polyline([(240, 160), (240, 320), (360, 320), (360, 160)]) +
          polyline([(240, 240), (180, 260)]) +
          polyline([(360, 240), (420, 260)]) +
          polyline([(300, 320), (300, 420), (380, 420)]),

    "见": rect(220, 180, 380, 320) + circle(300, 250, 40, segments=10) +
          polyline([(220, 320), (180, 420)]) + polyline([(380, 320), (420, 420)]),

    "望": circle(300, 220, 60, segments=12) +
          vline(300, 280, 420) + hline(420, 220, 380) +
          polyline([(420, 220), (460, 260)]),

    "听": polyline([(220, 220), (380, 180), (420, 260), (380, 340),
                    (220, 380), (180, 300), (220, 220)]) +
          polyline([(260, 260), (340, 280), (300, 320), (260, 260)]),

    "闻": polyline([(160, 160), (160, 480), (440, 480), (440, 160)]) +
          polyline([(220, 220), (220, 420), (340, 420), (340, 220)]) +
          circle(400, 300, 40, segments=10),

    # 言语文艺
    "言": polyline([(220, 320), (380, 320), (380, 420), (220, 420), (220, 320)]) +
          hline(220, 200, 400) + hline(180, 220, 380) + hline(160, 240, 360),

    "语": polyline([(180, 220), (280, 220), (280, 300), (180, 300), (180, 220)]) +
          polyline([(320, 220), (420, 220), (420, 300), (320, 300), (320, 220)]) +
          hline(160, 200, 260) + hline(320, 360, 400),

    "诗": polyline([(180, 220), (280, 220), (280, 300), (180, 300), (180, 220)]) +
          polyline([(320, 180), (420, 180), (420, 440), (320, 440), (320, 180)]) +
          hline(420, 340, 400),

    "书": vline(300, 160, 440) +
          polyline([(220, 240), (380, 240), (340, 280), (240, 280), (220, 240)]) +
          hline(440, 260, 340),

    "画": rect(180, 180, 420, 420) +
          polyline([(240, 220), (360, 220), (320, 260), (280, 260), (240, 220)]) +
          vline(300, 260, 400),

    "琴": polyline([(180, 220), (420, 220), (440, 380), (160, 380), (180, 220)]) +
          vline(240, 220, 380) + vline(300, 220, 380) + vline(360, 220, 380),

    "鼓": rect(220, 200, 380, 340) + hline(360, 220, 380) +
          vline(220, 340, 440) + vline(380, 340, 440) +
          polyline([(240, 360), (200, 400)]) + polyline([(360, 360), (400, 400)]),

    "钟": vline(300, 160, 220) +
          polyline([(220, 220), (380, 220), (360, 340), (240, 340), (220, 220)]) +
          hline(380, 240, 360) +
          polyline([(280, 340), (300, 380), (320, 340)]),

    # 医药祭祀
    "医": rect(180, 200, 420, 400) + vline(300, 200, 400) +
          polyline([(220, 260), (260, 260), (240, 300), (220, 260)]) +
          polyline([(340, 260), (380, 260), (360, 300), (340, 260)]),

    "药": polyline([(200, 420), (200, 300), (160, 220)]) +
          polyline([(300, 420), (300, 280), (260, 200)]) +
          polyline([(400, 420), (400, 300), (360, 220)]) +
          rect(220, 320, 380, 440),

    "针": vline(300, 160, 440) +
          polyline([(260, 200), (340, 200), (320, 240), (280, 240), (260, 200)]) +
          circle(300, 400, 30, segments=8),

    "灸": polyline([(180, 260), (300, 220), (420, 260), (420, 340),
                    (300, 380), (180, 340), (180, 260)]) +
          polyline([(260, 380), (300, 460), (340, 380)]) +
          polyline([(220, 420), (300, 480), (380, 420)]),

    "鬼": circle(300, 220, 60, segments=12) +
          polyline([(300, 280), (260, 400), (340, 400), (300, 280)]) +
          polyline([(340, 400), (420, 440)]) +
          hline(220, 260, 340),

    "神": polyline([(220, 420), (300, 160), (380, 420)]) +
          hline(440, 200, 400) +
          polyline([(260, 300), (340, 300), (300, 360), (340, 420)]),

    "巫": vline(300, 160, 440) + hline(260, 180, 420) + hline(340, 180, 420) +
          polyline([(220, 220), (260, 260)]) + polyline([(380, 220), (340, 260)]),

    "祝": polyline([(220, 160), (220, 320), (340, 320), (340, 160)]) +
          polyline([(220, 320), (160, 440)]) +
          polyline([(340, 320), (400, 440)]) +
          hline(440, 240, 320),

    # 印玺典册
    "印": rect(220, 260, 380, 420) +
          polyline([(260, 260), (260, 200), (340, 200), (340, 260)]) +
          hline(180, 240, 360),

    "玺": rect(220, 300, 380, 440) +
          polyline([(220, 300), (300, 180), (380, 300)]) +
          circle(300, 240, 30, segments=8),

    "册": vline(220, 180, 440) + vline(280, 180, 440) +
          vline(360, 180, 440) + hline(200, 220, 360) + hline(420, 220, 360),

    "典": polyline([(200, 220), (400, 220), (400, 360), (200, 360), (200, 220)]) +
          vline(250, 220, 360) + vline(350, 220, 360) + hline(400, 200, 400),

    # 文房器物
    "墨": rect(200, 200, 400, 400) +
          rect(240, 240, 360, 360) +
          polyline([(260, 260), (340, 340)]) + polyline([(340, 260), (260, 340)]),

    "笔": polyline([(280, 160), (320, 160), (340, 240), (260, 240), (280, 160)]) +
          vline(300, 240, 440) + hline(440, 260, 340),

    "砚": rect(180, 260, 420, 420) +
          polyline([(240, 300), (360, 300), (380, 360), (220, 360), (240, 300)]) +
          polyline([(280, 360), (260, 420), (340, 420), (320, 360)]),

    "纸": polyline([(200, 160), (420, 160), (420, 440), (200, 440), (200, 160)]) +
          hline(220, 220, 400) + hline(280, 220, 400) +
          hline(340, 220, 400) + hline(400, 220, 400),

    "章": rect(220, 160, 380, 440) +
          hline(240, 220, 380) + hline(320, 220, 380) +
          hline(400, 220, 380) + vline(300, 240, 420),

    "句": polyline([(220, 180), (380, 180), (420, 240), (420, 380),
                    (360, 440), (240, 440), (220, 380)]) +
          polyline([(220, 180), (180, 240), (180, 300), (220, 340), (260, 300)]),

    # 建筑
    "桥": arc(300, 380, 160, math.pi, 0, 16) +
          polyline([(200, 380), (200, 480)]) + polyline([(400, 380), (400, 480)]) +
          hline(480, 180, 420),

    "楼": polyline([(180, 480), (420, 480), (420, 160), (180, 160), (180, 480)]) +
          hline(260, 180, 420) + hline(340, 180, 420) +
          rect(220, 260, 260, 300) + rect(340, 260, 380, 300),
}


def build_fragment():
    """生成 PUA 字符到甲骨文字形定义的碎片映射。"""
    fragment = {}
    for idx, (hanzi, strokes) in enumerate(MORE_ORACLE_BONE.items()):
        code = START_CODEPOINT + idx
        char = chr(code)
        fragment[char] = {
            "unicode": f"U+{code:04X}",
            "笔画数": max(4, len(strokes) // 2),
            "结构": "甲骨文",
            "名称": f"甲骨文·{hanzi}",
            "对应汉字": hanzi,
            "风格参数": {"力度": 0.85, "棱角": 0.35, "节奏": 0.5, "墨色": 0.9},
            "笔画路径_cnsh9622": strokes
        }
    return fragment


def main():
    base_dir = Path(__file__).parent.parent
    fragment_path = base_dir / "glyphs" / "fragments" / f"{SYMBOL_SET}.json"
    fragment_path.parent.mkdir(parents=True, exist_ok=True)

    fragment = build_fragment()

    with open(fragment_path, "w", encoding="utf-8") as f:
        json.dump(fragment, f, ensure_ascii=False, indent=2)

    end_code = START_CODEPOINT + COUNT - 1
    print(f"Symbol set : {SYMBOL_SET}")
    print(f"Description: {DESCRIPTION}")
    print(f"Count      : {COUNT}")
    print(f"Codepoints : U+{START_CODEPOINT:04X} .. U+{end_code:04X}")
    print(f"Output     : {fragment_path}")
    print(f"DNA        : {DNA}")
    print(f"Timestamp  : {datetime.now().isoformat()}")


if __name__ == "__main__":
    main()
