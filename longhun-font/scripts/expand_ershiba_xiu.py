# DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-1c243070
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# DNA追溯码:#龍芯⚡️2026-06-22-LONGHUN-FONT-FRAGMENT-ERSHIBA_XIU-v1.0
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

"""
LonghunFont 二十八宿（lunar mansions）字元片段生成器
使用 Unicode Private Use Area (PUA) U+E416 起，共 28 个符号
只输出片段 JSON，不加载/不保存完整字元库。
"""

import json
import math
from pathlib import Path
from datetime import datetime

DNA = "#龍芯⚡️2026-06-22-LONGHUN-FONT-FRAGMENT-ERSHIBA_XIU-v1.0"

NAME = "ershiba_xiu"
DESCRIPTION = "二十八宿 lunar mansions"
COUNT = 28
START_CODEPOINT = 0xE416


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


def star(cx, cy, r, points=5):
    """简单星形：中心点 + 放射线"""
    strokes = []
    for i in range(points):
        a = 2 * math.pi * i / points - math.pi / 2
        strokes.extend(polyline([(cx, cy), (cx + r * math.cos(a), cy + r * math.sin(a))]))
    return strokes


# ============================================================
# 二十八宿简化符号：星点 + 简笔动物 / 器物组合
# ============================================================
ERSHIBA_XIU = {
    # 东方青龙七宿
    "角": (
        # 龙角：分叉向上的角
        polyline([(260, 420), (260, 280), (200, 180)]) +
        polyline([(340, 420), (340, 280), (400, 180)]) +
        polyline([(220, 320), (380, 320)])
    ),
    "亢": (
        # 龙颈：弯曲的颈部
        arc(300, 300, 120, math.pi, 2 * math.pi, segments=16) +
        polyline([(180, 300), (180, 420)]) + polyline([(420, 300), (420, 420)])
    ),
    "氐": (
        # 龙根/胸：根基 + 分叉
        vline(300, 160, 440) +
        polyline([(300, 280), (220, 200)]) + polyline([(300, 280), (380, 200)]) +
        polyline([(220, 440), (300, 360), (380, 440)])
    ),
    "房": (
        # 龙房/腹：房屋轮廓
        polyline([(200, 440), (200, 240), (300, 160), (400, 240), (400, 440)]) +
        rect(240, 280, 360, 440)
    ),
    "心": (
        # 心：心形
        polyline([(300, 180), (220, 260), (220, 340), (300, 420), (380, 340), (380, 260), (300, 180)])
    ),
    "尾": (
        # 尾：弯曲的尾巴
        arc(300, 300, 140, 0, math.pi, segments=18) +
        polyline([(440, 300), (480, 200)]) +
        polyline([(440, 300), (480, 400)])
    ),
    "箕": (
        # 箕：簸箕
        polyline([(200, 220), (400, 220), (360, 420), (240, 420), (200, 220)]) +
        polyline([(240, 420), (220, 480)]) + polyline([(360, 420), (380, 480)])
    ),

    # 北方玄武七宿
    "斗": (
        # 斗：斗勺
        polyline([(240, 220), (360, 220), (380, 300), (340, 300), (340, 440), (260, 440), (260, 300), (220, 300), (240, 220)])
    ),
    "牛": (
        # 牛：牛头
        polyline([(220, 300), (260, 220), (340, 220), (380, 300), (340, 400), (260, 400), (220, 300)]) +
        polyline([(260, 220), (240, 160)]) + polyline([(340, 220), (360, 160)])
    ),
    "女": (
        # 女：跪坐女子
        polyline([(300, 160), (220, 300), (300, 400), (380, 300), (300, 160)]) +
        polyline([(220, 300), (160, 440)])
    ),
    "虚": (
        # 虚：空旷 / 几案
        polyline([(180, 240), (420, 240), (420, 300), (180, 300), (180, 240)]) +
        vline(220, 300, 440) + vline(380, 300, 440)
    ),
    "危": (
        # 危：屋脊 / 尖顶
        polyline([(160, 440), (300, 160), (440, 440)]) +
        polyline([(220, 320), (380, 320)]) + polyline([(260, 320), (260, 440)]) + polyline([(340, 320), (340, 440)])
    ),
    "室": (
        # 室：屋室
        rect(180, 200, 420, 440) + polyline([(180, 200), (300, 120), (420, 200)]) +
        rect(260, 300, 340, 440)
    ),
    "壁": (
        # 壁：墙壁
        polyline([(180, 160), (180, 440)]) + polyline([(300, 160), (300, 440)]) +
        hline(240, 180, 300) + hline(360, 180, 300)
    ),

    # 西方白虎七宿
    "奎": (
        # 奎：胯骨 / 两腿
        polyline([(220, 180), (220, 360), (180, 440)]) +
        polyline([(380, 180), (380, 360), (420, 440)]) +
        hline(260, 220, 380)
    ),
    "娄": (
        # 娄：绳索 / 捆绑
        polyline([(200, 200), (400, 200), (360, 300), (400, 400), (200, 400), (240, 300), (200, 200)])
    ),
    "胃": (
        # 胃：胃囊
        polyline([(200, 260), (240, 220), (360, 220), (400, 260), (400, 380), (360, 420), (240, 420), (200, 380), (200, 260)])
    ),
    "昴": (
        # 昴：毛发 / 三星簇
        circle(300, 260, 30, segments=8) + circle(240, 340, 30, segments=8) + circle(360, 340, 30, segments=8) +
        polyline([(300, 290), (300, 420)])
    ),
    "毕": (
        # 毕：网 / 长柄网
        polyline([(300, 160), (300, 420)]) +
        polyline([(180, 260), (420, 260), (380, 420), (220, 420), (180, 260)])
    ),
    "觜": (
        # 觜：鸟嘴 / 龟嘴
        polyline([(200, 320), (300, 240), (400, 320)]) +
        polyline([(300, 240), (300, 400)]) +
        polyline([(240, 400), (360, 400)])
    ),
    "参": (
        # 参：三颗星斜列
        circle(240, 220, 30, segments=8) + circle(300, 320, 30, segments=8) + circle(360, 420, 30, segments=8) +
        polyline([(260, 240), (280, 300)]) + polyline([(320, 340), (340, 400)])
    ),

    # 南方朱雀七宿
    "井": (
        # 井：井字
        rect(200, 200, 400, 400) + hline(300, 200, 400) + vline(300, 200, 400)
    ),
    "鬼": (
        # 鬼：鬼脸 / 面具
        polyline([(220, 220), (380, 220), (420, 320), (380, 420), (220, 420), (180, 320), (220, 220)]) +
        circle(260, 300, 20, segments=6) + circle(340, 300, 20, segments=6) +
        polyline([(280, 360), (300, 380), (320, 360)])
    ),
    "柳": (
        # 柳：柳树
        vline(300, 160, 480) +
        polyline([(300, 240), (220, 200)]) + polyline([(300, 300), (400, 260)]) +
        polyline([(300, 360), (200, 340)]) + polyline([(300, 420), (420, 400)])
    ),
    "星": (
        # 星：四角星
        star(300, 300, 140, points=4)
    ),
    "张": (
        # 张：张开的弓 / 网
        arc(300, 300, 160, -math.pi / 2, math.pi / 2, segments=18) +
        polyline([(300, 140), (300, 460)]) +
        polyline([(300, 220), (420, 220)]) + polyline([(300, 380), (420, 380)])
    ),
    "翼": (
        # 翼：翅膀
        polyline([(180, 320), (260, 200), (340, 240), (420, 200), (420, 360), (340, 440), (260, 400), (180, 440), (180, 320)])
    ),
    "轸": (
        # 轸：车 / 战车
        circle(240, 360, 60, segments=10) + circle(360, 360, 60, segments=10) +
        rect(200, 220, 400, 320) + polyline([(200, 220), (300, 160), (400, 220)])
    ),
}


def build_fragment():
    fragment = {}
    for idx, (hanzi, strokes) in enumerate(ERSHIBA_XIU.items()):
        code = START_CODEPOINT + idx
        char = chr(code)
        fragment[char] = {
            "unicode": f"U+{code:04X}",
            "笔画数": len(strokes),
            "结构": "二十八宿",
            "名称": hanzi,
            "风格参数": {"力度": 0.85, "棱角": 0.35, "节奏": 0.5, "墨色": 0.9},
            "笔画路径_cnsh9622": strokes
        }
    return fragment


def main():
    base_dir = Path(__file__).parent.parent
    out_dir = base_dir / "glyphs" / "fragments"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{NAME}.json"

    fragment = build_fragment()
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(fragment, f, ensure_ascii=False, indent=2)

    end_code = START_CODEPOINT + COUNT - 1
    print(f"✅ 已生成二十八宿字元片段: {out_path}")
    print(f"   符号集: {NAME}")
    print(f"   描述: {DESCRIPTION}")
    print(f"   数量: {COUNT}")
    print(f"   码位范围: U+{START_CODEPOINT:04X} ~ U+{end_code:04X}")
    print(f"   DNA: {DNA}")


if __name__ == "__main__":
    main()
