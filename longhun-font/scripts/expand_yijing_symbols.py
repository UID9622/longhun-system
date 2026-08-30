# DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-369b7497
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# DNA追溯码:#龍芯⚡️2026-06-22-LONGHUN-FONT-YIJING-v1.0
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

"""
LonghunFont 易经、太极、八卦符号扩展
覆盖：64 卦六爻象、8 卦三爻象、太极图、两仪符号
"""

import json
import sys
from pathlib import Path
from datetime import datetime

DNA = "#龍芯⚡️2026-06-22-LONGHUN-FONT-YIJING-v1.0"

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


def hline(y, x1, x2):
    return polyline([(x1, y), (x2, y)])


def circle(cx, cy, r, segments=24):
    import math
    pts = []
    for i in range(segments + 1):
        a = 2 * math.pi * i / segments
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return polyline(pts)


# ============================================================
# 爻绘制
# ============================================================
def yao(y, is_yang, left=100, right=500):
    """绘制单条爻。is_yang=True 为阳爻（—），False 为阴爻（- -）"""
    if is_yang:
        return hline(y, left, right)
    gap = (right - left) * 0.18
    mid = (left + right) / 2
    return hline(y, left, mid - gap) + hline(y, mid + gap, right)


def hexagram(pattern, top_y=100, line_spacing=80, left=80, right=520):
    """pattern: 6 位字符串，'1'=阳，'0'=阴，自上而下"""
    strokes = []
    for i, bit in enumerate(pattern):
        y = top_y + i * line_spacing
        strokes.extend(yao(y, bit == '1', left, right))
    return strokes


def trigram(pattern, top_y=160, line_spacing=120, left=100, right=500):
    """pattern: 3 位字符串，'1'=阳，'0'=阴，自上而下"""
    strokes = []
    for i, bit in enumerate(pattern):
        y = top_y + i * line_spacing
        strokes.extend(yao(y, bit == '1', left, right))
    return strokes


# ============================================================
# 64 卦文王序（自上而下，1=阳，0=阴）
# ============================================================
HEXAGRAMS = [
    "111111",  # 1  乾
    "000000",  # 2  坤
    "010001",  # 3  屯 水雷
    "100010",  # 4  蒙 山水
    "010111",  # 5  需 水天
    "111010",  # 6  讼 天水
    "000010",  # 7  师 地水
    "010000",  # 8  比 水地
    "110111",  # 9  小畜 风天
    "111011",  # 10 履 天泽
    "111000",  # 11 泰 天地
    "000111",  # 12 否 地天
    "111101",  # 13 同人 天火
    "101111",  # 14 大有 火天
    "000100",  # 15 谦 地山
    "001000",  # 16 豫 雷地
    "011001",  # 17 随 泽雷
    "100110",  # 18 蛊 山风
    "000011",  # 19 临 地泽
    "110000",  # 20 观 风地
    "101001",  # 21 噬嗑 火雷
    "100101",  # 22 贲 山火
    "100000",  # 23 剥 山地
    "000001",  # 24 复 地雷
    "111001",  # 25 无妄 天雷
    "100111",  # 26 大畜 山天
    "100001",  # 27 颐 山雷
    "011110",  # 28 大过 泽风
    "010010",  # 29 坎 水水
    "101101",  # 30 离 火火
    "011000",  # 31 咸 泽山
    "001100",  # 32 恒 雷风
    "001111",  # 33 遁 天山
    "111100",  # 34 大壮 雷天
    "101000",  # 35 晋 火地
    "000101",  # 36 明夷 地火
    "101011",  # 37 家人 风火
    "110101",  # 38 睽 泽火
    "010100",  # 39 蹇 水山
    "001010",  # 40 解 雷水
    "100011",  # 41 损 山泽
    "110001",  # 42 益 风雷
    "011111",  # 43 夬 泽天
    "111110",  # 44 姤 天风
    "011000",  # 45 萃 泽地
    "000110",  # 46 升 地风
    "011010",  # 47 困 泽水
    "010110",  # 48 井 水风
    "011101",  # 49 革 泽火
    "101110",  # 50 鼎 火风
    "001001",  # 51 震 雷雷
    "100100",  # 52 艮 山山
    "110100",  # 53 渐 风山
    "001011",  # 54 归妹 雷泽
    "001101",  # 55 丰 雷火
    "101100",  # 56 旅 火山
    "110110",  # 57 巽 风风
    "011011",  # 58 兑 泽泽
    "110010",  # 59 涣 风水
    "010011",  # 60 节 水泽
    "110011",  # 61 中孚 风泽
    "001100",  # 62 小过 雷山
    "010101",  # 63 既济 水火
    "101010",  # 64 未济 火水
]

# 卦名（可选，用于元数据）
HEXAGRAM_NAMES = [
    "乾", "坤", "屯", "蒙", "需", "讼", "师", "比",
    "小畜", "履", "泰", "否", "同人", "大有", "谦", "豫",
    "随", "蛊", "临", "观", "噬嗑", "贲", "剥", "复",
    "无妄", "大畜", "颐", "大过", "坎", "离", "咸", "恒",
    "遁", "大壮", "晋", "明夷", "家人", "睽", "蹇", "解",
    "损", "益", "夬", "姤", "萃", "升", "困", "井",
    "革", "鼎", "震", "艮", "渐", "归妹", "丰", "旅",
    "巽", "兑", "涣", "节", "中孚", "小过", "既济", "未济",
]

# 8 卦符号（自上而下）
TRIGRAMS = {
    '☰': "111",  # 乾
    '☱': "011",  # 兑
    '☲': "101",  # 离
    '☳': "001",  # 震
    '☴': "110",  # 巽
    '☵': "010",  # 坎
    '☶': "100",  # 艮
    '☷': "000",  # 坤
}


def taiji():
    """太极图骨架：外圆 + S 曲线"""
    import math
    strokes = []
    # 外圆
    strokes.extend(circle(300, 300, 260, segments=48))
    # S 曲线：从顶部到底部
    pts = []
    for i in range(-24, 25):
        t = i / 24.0  # -1 ~ 1
        angle = math.pi / 2 - t * math.pi
        # 太极 S 曲线参数方程近似
        r = 130 if t < 0 else -130
        x = 300 + r * math.cos(angle) + (260 - 130) * math.sin(angle) * 0.0
        # 简化：用两个半圆拼 S
        pass
    # 更简单的 S：两个相切的半圆弧线
    # 上半黑鱼：左半圆
    for seg in [circle(300, 170, 130, segments=24)[:13]]:
        strokes.extend(seg)
    # 下半白鱼：右半圆
    for seg in [circle(300, 430, 130, segments=24)[12:]]:
        strokes.extend(seg)
    # 两个鱼眼
    strokes.extend(circle(300, 170, 35, segments=12))
    strokes.extend(circle(300, 430, 35, segments=12))
    return strokes


def yin_yang_monogram(is_yang):
    """两仪符号：阳仪/阴仪"""
    return yao(300, is_yang, left=120, right=480)


def expand(glyph_path: str):
    base_dir = Path(__file__).parent.parent
    glyph_path = Path(glyph_path) if glyph_path else base_dir / "glyphs" / "龍魂字元库_v0004_办公版.json"

    with open(glyph_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    added = 0

    # 64 卦
    for idx, pattern in enumerate(HEXAGRAMS):
        char = chr(0x4DC0 + idx)
        if char in data["字符集_cnsh9622"]:
            continue
        data["字符集_cnsh9622"][char] = {
            "unicode": f"U+{ord(char):04X}",
            "笔画数": 6,
            "结构": "易经六爻",
            "卦名": HEXAGRAM_NAMES[idx],
            "风格参数": {"力度": 0.9, "棱角": 0.2, "节奏": 0.7, "墨色": 0.95},
            "笔画路径_cnsh9622": hexagram(pattern)
        }
        added += 1

    # 8 卦
    for idx, (char, pattern) in enumerate(TRIGRAMS.items()):
        code = 0x2630 + idx
        char = chr(code)
        if char in data["字符集_cnsh9622"]:
            continue
        data["字符集_cnsh9622"][char] = {
            "unicode": f"U+{ord(char):04X}",
            "笔画数": 3,
            "结构": "八卦三爻",
            "风格参数": {"力度": 0.9, "棱角": 0.2, "节奏": 0.7, "墨色": 0.95},
            "笔画路径_cnsh9622": trigram(pattern)
        }
        added += 1

    # 太极
    taiji_char = chr(0x262F)
    if taiji_char not in data["字符集_cnsh9622"]:
        data["字符集_cnsh9622"][taiji_char] = {
            "unicode": "U+262F",
            "笔画数": 4,
            "结构": "太极图",
            "风格参数": {"力度": 0.8, "棱角": 0.1, "节奏": 0.6, "墨色": 0.9},
            "笔画路径_cnsh9622": taiji()
        }
        added += 1

    # 两仪
    for idx, is_yang in enumerate([True, False]):
        char = chr(0x268A + idx)
        if char in data["字符集_cnsh9622"]:
            continue
        data["字符集_cnsh9622"][char] = {
            "unicode": f"U+{ord(char):04X}",
            "笔画数": 1,
            "结构": "两仪",
            "风格参数": {"力度": 0.9, "棱角": 0.2, "节奏": 0.7, "墨色": 0.95},
            "笔画路径_cnsh9622": yin_yang_monogram(is_yang)
        }
        added += 1

    data["元数据"]["版本"] = "v0005-易经版"
    data["元数据"]["描述"] = f"LonghunFont 易经版字元库，含 {len(data['字符集_cnsh9622'])} 个字符"
    data["元数据"]["易经扩展时间"] = datetime.now().isoformat()
    data["元数据"]["易经扩展DNA"] = DNA

    new_path = base_dir / "glyphs" / "龍魂字元库_v0005_易经版.json"
    with open(new_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ 已扩展易经版字元库: {new_path}")
    print(f"   新增字符: {added}")
    print(f"   总字符数: {len(data['字符集_cnsh9622'])}")
    return str(new_path)


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else None
    expand(path)
