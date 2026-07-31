# DNA: #龍芯⚡️丙午·乙未·乙丑·比-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# DNA追溯码:#龍芯⚡️2026-06-22-LONGHUN-FONT-LATIN-SYMBOLS-v1.0

"""
LonghunFont 拉丁字母、ASCII 数字与符号扩展
目标：让 LonghunFont 可用于 Office/PDF 中英文混排
"""

import json
import sys
from pathlib import Path
from datetime import datetime

DNA = "#龍芯⚡️2026-06-22-LONGHUN-FONT-LATIN-SYMBOLS-v1.0"

# 拉丁排版参数
BASE = 0          # 基线
CAP = 700         # 大写高度
X_HEIGHT = 500    # x 字高
DESC = -200       # 下伸部
ASC = 750         # 上伸部
WIDTH = 520       # 拉丁字符字身宽
MID = WIDTH // 2  # 中心线


def stroke_move(x, y):
    return {"类型": "移动到", "坐标": [x, y]}


def stroke_line(x, y):
    return {"类型": "直线段", "终点": [x, y]}


def polyline(points):
    """将点列表转为笔画路径"""
    strokes = [stroke_move(*points[0])]
    for p in points[1:]:
        strokes.append(stroke_line(*p))
    return strokes


def hline(y, x1, x2):
    return polyline([(x1, y), (x2, y)])


def vline(x, y1, y2):
    return polyline([(x, y1), (x, y2)])


def rect(x1, y1, x2, y2):
    return polyline([(x1, y1), (x2, y1), (x2, y2), (x1, y2), (x1, y1)])


def circle(cx, cy, r, segments=16):
    """用折线近似圆"""
    import math
    pts = []
    for i in range(segments + 1):
        a = 2 * math.pi * i / segments
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return polyline(pts)


# ============================================================
# 大写字母 A-Z
# ============================================================
UPPERCASE = {
    'A': polyline([(80, BASE), (MID, CAP), (WIDTH-80, BASE)]) +
         hline(350, 180, WIDTH-180),
    'B': vline(80, BASE, CAP) +
         hline(CAP, 80, WIDTH-120) +
         vline(WIDTH-120, CAP, MID) +
         hline(MID, WIDTH-120, 80) +
         vline(80, MID, BASE) +
         hline(BASE, 80, WIDTH-120),
    'C': circle(MID, MID, 300, segments=24)[:13],  # 上半圆+左半
    'D': vline(80, BASE, CAP) +
         hline(CAP, 80, WIDTH-120) +
         [(WIDTH-120, CAP), (WIDTH-80, 500), (WIDTH-120, BASE)] +
         hline(BASE, WIDTH-120, 80),
    'E': vline(80, BASE, CAP) +
         hline(CAP, 80, WIDTH-80) +
         hline(MID, 80, WIDTH-160) +
         hline(BASE, 80, WIDTH-80),
    'F': vline(80, BASE, CAP) +
         hline(CAP, 80, WIDTH-80) +
         hline(MID, 80, WIDTH-160),
    'G': circle(MID, MID, 300, segments=28)[:22] +
         hline(MID, WIDTH-100, WIDTH-40) +
         vline(WIDTH-40, MID, BASE),
    'H': vline(80, BASE, CAP) +
         vline(WIDTH-80, BASE, CAP) +
         hline(MID, 80, WIDTH-80),
    'I': vline(MID, BASE, CAP),
    'J': vline(WIDTH-80, CAP, 200) +
         circle(200, 100, 120, segments=12)[6:],
    'K': vline(80, BASE, CAP) +
         polyline([(WIDTH-80, CAP), (80, MID), (WIDTH-80, BASE)]),
    'L': vline(80, BASE, CAP) +
         hline(BASE, 80, WIDTH-80),
    'M': polyline([(80, BASE), (80, CAP), (MID, 400), (WIDTH-80, CAP), (WIDTH-80, BASE)]),
    'N': polyline([(80, BASE), (80, CAP), (WIDTH-80, BASE), (WIDTH-80, CAP)]),
    'O': circle(MID, MID, 320, segments=24),
    'P': vline(80, BASE, CAP) +
         hline(CAP, 80, WIDTH-120) +
         vline(WIDTH-120, CAP, MID) +
         hline(MID, WIDTH-120, 80),
    'Q': circle(MID, MID, 320, segments=24) +
         polyline([(MID+80, 120), (WIDTH-40, BASE)]),
    'R': vline(80, BASE, CAP) +
         hline(CAP, 80, WIDTH-120) +
         vline(WIDTH-120, CAP, MID) +
         hline(MID, WIDTH-120, 80) +
         polyline([(80, MID), (WIDTH-80, BASE)]),
    'S': polyline([(WIDTH-80, CAP), (80, CAP), (80, MID), (WIDTH-80, MID), (WIDTH-80, BASE), (80, BASE)]),
    'T': hline(CAP, 40, WIDTH-40) +
         vline(MID, BASE, CAP),
    'U': vline(80, CAP, 200) +
         circle(MID, 200, 120, segments=16)[6:14] +
         vline(WIDTH-80, 200, CAP),
    'V': polyline([(80, CAP), (MID, BASE), (WIDTH-80, CAP)]),
    'W': polyline([(80, CAP), (150, BASE), (MID, 400), (WIDTH-150, BASE), (WIDTH-80, CAP)]),
    'X': polyline([(80, CAP), (WIDTH-80, BASE)]) +
         polyline([(WIDTH-80, CAP), (80, BASE)]),
    'Y': polyline([(80, CAP), (MID, MID), (WIDTH-80, CAP)]) +
         vline(MID, BASE, MID),
    'Z': polyline([(80, CAP), (WIDTH-80, CAP), (80, BASE), (WIDTH-80, BASE)]),
}

# ============================================================
# 小写字母 a-z
# ============================================================
LOWERCASE = {
    'a': circle(260, 300, 150, segments=16)[:12] +
         vline(260, 300, BASE),
    'b': vline(80, BASE, ASC) +
         circle(260, 300, 150, segments=16),
    'c': circle(260, 300, 150, segments=16)[:10],
    'd': vline(WIDTH-80, BASE, ASC) +
         circle(260, 300, 150, segments=16),
    'e': circle(260, 300, 150, segments=16) +
         hline(300, 80, WIDTH-80),
    'f': vline(260, BASE, ASC) +
         hline(ASC, 80, WIDTH-80) +
         vline(80, ASC, 500),
    'g': circle(260, 300, 150, segments=16) +
         vline(260, 300, DESC) +
         circle(260, 100, 120, segments=12)[6:],
    'h': vline(80, BASE, ASC) +
         circle(260, 350, 130, segments=16)[:12] +
         vline(260, 350, BASE),
    'i': vline(MID, 150, X_HEIGHT) +
         vline(MID-40, X_HEIGHT+30, X_HEIGHT+80),
    'j': vline(MID, 150, DESC) +
         vline(MID-40, X_HEIGHT+30, X_HEIGHT+80),
    'k': vline(80, BASE, ASC) +
         polyline([(WIDTH-80, X_HEIGHT), (80, 250), (WIDTH-80, BASE)]),
    'l': vline(MID, BASE, ASC),
    'm': vline(60, BASE, X_HEIGHT) +
         circle(180, 370, 100, segments=12)[:10] +
         vline(300, 370, BASE) +
         circle(420, 370, 100, segments=12)[:10] +
         vline(WIDTH-60, 370, BASE),
    'n': vline(80, BASE, X_HEIGHT) +
         circle(260, 380, 120, segments=12)[:10] +
         vline(260, 380, BASE),
    'o': circle(MID, 300, 150, segments=16),
    'p': vline(80, DESC, X_HEIGHT) +
         circle(260, 300, 150, segments=16),
    'q': vline(WIDTH-80, DESC, X_HEIGHT) +
         circle(260, 300, 150, segments=16),
    'r': vline(80, BASE, X_HEIGHT) +
         hline(X_HEIGHT, 80, WIDTH-120),
    's': polyline([(WIDTH-80, X_HEIGHT), (80, X_HEIGHT), (80, MID), (WIDTH-80, MID), (WIDTH-80, BASE), (80, BASE)]),
    't': vline(MID, BASE, X_HEIGHT+50) +
         hline(X_HEIGHT, 80, WIDTH-80),
    'u': vline(80, X_HEIGHT, BASE) +
         circle(260, 200, 120, segments=12)[4:] +
         vline(WIDTH-80, 200, X_HEIGHT),
    'v': polyline([(80, X_HEIGHT), (MID, BASE), (WIDTH-80, X_HEIGHT)]),
    'w': polyline([(80, X_HEIGHT), (150, BASE), (MID, 300), (WIDTH-150, BASE), (WIDTH-80, X_HEIGHT)]),
    'x': polyline([(80, X_HEIGHT), (WIDTH-80, BASE)]) +
         polyline([(WIDTH-80, X_HEIGHT), (80, BASE)]),
    'y': vline(80, X_HEIGHT, DESC) +
         vline(WIDTH-80, X_HEIGHT, BASE) +
         polyline([(80, X_HEIGHT), (WIDTH-80, BASE)]),
    'z': polyline([(80, X_HEIGHT), (WIDTH-80, X_HEIGHT), (80, BASE), (WIDTH-80, BASE)]),
}

# ============================================================
# ASCII 数字 0-9
# ============================================================
DIGITS = {
    '0': circle(MID, MID, 320, segments=24),
    '1': vline(MID, BASE, CAP) +
         polyline([(MID-80, CAP), (MID+80, CAP)]),
    '2': polyline([(80, CAP), (WIDTH-80, CAP), (WIDTH-80, MID), (80, MID), (80, BASE), (WIDTH-80, BASE)]),
    '3': polyline([(80, CAP), (WIDTH-80, CAP), (WIDTH-80, MID), (80, MID)]) +
         polyline([(WIDTH-80, MID), (WIDTH-80, BASE), (80, BASE)]),
    '4': vline(WIDTH-80, BASE, CAP) +
         hline(MID, 80, WIDTH-80) +
         vline(80, MID, CAP),
    '5': polyline([(WIDTH-80, CAP), (80, CAP), (80, MID), (WIDTH-80, MID), (WIDTH-80, BASE), (80, BASE)]),
    '6': hline(CAP, WIDTH-80, 80) +
         vline(80, CAP, MID) +
         circle(MID, 250, 150, segments=16)[:14],
    '7': polyline([(80, CAP), (WIDTH-80, CAP), (WIDTH-80, BASE)]),
    '8': circle(MID, 500, 150, segments=16) +
         circle(MID, 200, 150, segments=16),
    '9': circle(MID, 500, 150, segments=16) +
         vline(WIDTH-80, 500, BASE) +
         hline(BASE, WIDTH-80, 80),
}

# ============================================================
# 基础符号（ASCII 标点 + 常用符号）
# ============================================================
SYMBOLS = {
    ' ': [],
    '!': vline(MID, 200, CAP) +
         circle(MID, 100, 30, segments=8),
    '"': vline(180, CAP-80, CAP) +
         vline(WIDTH-180, CAP-80, CAP),
    '#': vline(140, BASE, CAP) +
         vline(WIDTH-140, BASE, CAP) +
         hline(550, 80, WIDTH-80) +
         hline(450, 80, WIDTH-80),
    '$': vline(MID, DESC, ASC) +
         polyline([(80, 650), (WIDTH-80, 650), (WIDTH-80, MID), (80, MID), (80, BASE), (WIDTH-80, BASE)]),
    '%': vline(80, BASE, CAP) +
         circle(180, 550, 60, segments=8) +
         circle(WIDTH-180, 150, 60, segments=8),
    '&': circle(200, 500, 100, segments=12)[:10] +
         circle(200, 250, 150, segments=16)[:12] +
         polyline([(200, 400), (WIDTH-80, BASE), (80, BASE)]),
    "'": vline(MID, CAP-80, CAP),
    '(': [(0,0)] + circle(-100, MID, 400, segments=24)[6:18],  #  hacky left paren
    ')': [(WIDTH,0)] + circle(WIDTH+100, MID, 400, segments=24)[18:] + circle(WIDTH+100, MID, 400, segments=24)[:6],
    '*': polyline([(MID, 550), (MID, 750)]) +
         polyline([(150, 600), (WIDTH-150, 700)]) +
         polyline([(WIDTH-150, 600), (150, 700)]),
    '+': vline(MID, 200, 600) +
         hline(400, 120, WIDTH-120),
    ',': polyline([(MID, 100), (MID-40, -50)]),
    '-': hline(400, 120, WIDTH-120),
    '.': circle(MID, 80, 30, segments=8),
    '/': polyline([(WIDTH-80, CAP), (80, BASE)]),
    ':': circle(MID, 500, 30, segments=8) +
         circle(MID, 200, 30, segments=8),
    ';': circle(MID, 500, 30, segments=8) +
         polyline([(MID, 200), (MID-40, 50)]),
    '<': polyline([(WIDTH-80, 600), (80, 400), (WIDTH-80, 200)]),
    '=': hline(500, 80, WIDTH-80) +
         hline(300, 80, WIDTH-80),
    '>': polyline([(80, 600), (WIDTH-80, 400), (80, 200)]),
    '?': polyline([(80, CAP), (WIDTH-80, CAP), (WIDTH-80, 500), (MID, 400)]) +
         circle(MID, 200, 30, segments=8),
    '@': circle(MID, MID, 300, segments=24) +
         circle(MID+50, MID-50, 120, segments=12),
    '[': polyline([(120, CAP), (120, BASE), (WIDTH-120, BASE)]),
    '\\': polyline([(80, CAP), (WIDTH-80, BASE)]),
    ']': polyline([(WIDTH-120, CAP), (WIDTH-120, BASE), (120, BASE)]),
    '^': polyline([(80, 500), (MID, CAP), (WIDTH-80, 500)]),
    '_': hline(BASE, 0, WIDTH),
    '`': polyline([(180, CAP), (260, CAP+80)]),
    '{': vline(MID, BASE, CAP),
    '|': vline(MID, BASE, CAP),
    '}': vline(MID, BASE, CAP),
    '~': polyline([(80, 400), (200, 500), (320, 400), (WIDTH-80, 500)]),
}

# 简单修正左右括号：用更直接的方式
SYMBOLS['('] = polyline([(WIDTH-60, CAP), (120, MID), (WIDTH-60, BASE)])
SYMBOLS[')'] = polyline([(60, CAP), (WIDTH-120, MID), (60, BASE)])
SYMBOLS['{'] = polyline([(WIDTH-80, CAP), (80, 650), (80, 550), (MID, 500), (80, 450), (80, 350), (WIDTH-80, BASE)])
SYMBOLS['}'] = polyline([(80, CAP), (WIDTH-80, 650), (WIDTH-80, 550), (MID, 500), (WIDTH-80, 450), (WIDTH-80, 350), (80, BASE)])

# CJK 标点符号（全角）
CJK_PUNCT = {
    '，': circle(MID, 80, 40, segments=8) +
          vline(MID-40, 80, 0),
    '。': circle(MID, 100, 60, segments=12),
    '、': polyline([(180, 120), (MID, 40), (WIDTH-120, 80)]),
    '；': circle(MID, 500, 40, segments=8) +
          polyline([(MID, 200), (MID-40, 50)]),
    '：': circle(MID, 500, 40, segments=8) +
          circle(MID, 200, 40, segments=8),
    '？': polyline([(80, CAP), (WIDTH-80, CAP), (WIDTH-80, 500), (MID, 400)]) +
          circle(MID, 200, 40, segments=8),
    '！': vline(MID, 200, CAP) +
          circle(MID, 100, 40, segments=8),
    '“': [stroke_move(160, CAP), stroke_line(160, CAP-120), stroke_move(WIDTH-160, CAP), stroke_line(WIDTH-160, CAP-120)],
    '”': [stroke_move(160, CAP-120), stroke_line(160, CAP), stroke_move(WIDTH-160, CAP-120), stroke_line(WIDTH-160, CAP)],
    '‘': [stroke_move(160, CAP), stroke_line(160, CAP-80), stroke_move(WIDTH-160, CAP), stroke_line(WIDTH-160, CAP-80)],
    '’': [stroke_move(160, CAP-80), stroke_line(160, CAP), stroke_move(WIDTH-160, CAP-80), stroke_line(WIDTH-160, CAP)],
    '（': polyline([(WIDTH-60, CAP), (120, MID), (WIDTH-60, BASE)]),
    '）': polyline([(60, CAP), (WIDTH-120, MID), (60, BASE)]),
    '【': rect(80, BASE, WIDTH-80, CAP),
    '】': rect(80, BASE, WIDTH-80, CAP),
    '《': polyline([(WIDTH-80, CAP), (80, MID), (WIDTH-80, BASE)]),
    '》': polyline([(80, CAP), (WIDTH-80, MID), (80, BASE)]),
    '…': circle(150, 80, 25, segments=6) +
         circle(MID, 80, 25, segments=6) +
         circle(WIDTH-150, 80, 25, segments=6),
    '—': hline(MID, 0, WIDTH),
}


def expand(glyph_path: str):
    base_dir = Path(__file__).parent.parent
    glyph_path = Path(glyph_path) if glyph_path else base_dir / "glyphs" / "龍魂字元库_v0003_千字符.json"

    with open(glyph_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    added = 0
    all_new = {}
    all_new.update(UPPERCASE)
    all_new.update(LOWERCASE)
    all_new.update(DIGITS)
    all_new.update(SYMBOLS)
    all_new.update(CJK_PUNCT)

    for char, strokes in all_new.items():
        if char in data["字符集_cnsh9622"]:
            continue
        # 过滤掉无效点与非字典项
        clean = []
        last = None
        for s in strokes:
            if not isinstance(s, dict):
                continue
            if s["类型"] == "移动到":
                clean.append(s)
                last = tuple(s["坐标"])
            elif s["类型"] == "直线段":
                pt = tuple(s["终点"])
                if last != pt:
                    clean.append(s)
                    last = pt
        data["字符集_cnsh9622"][char] = {
            "unicode": f"U+{ord(char):04X}",
            "笔画数": len(clean),
            "结构": "拉丁" if ('A' <= char <= 'Z' or 'a' <= char <= 'z') else "符号",
            "风格参数": {"力度": 0.8, "棱角": 0.3, "节奏": 0.6, "墨色": 0.9},
            "笔画路径_cnsh9622": clean
        }
        added += 1

    data["元数据"]["版本"] = "v0004-办公版"
    data["元数据"]["描述"] = f"LonghunFont 办公版字元库，含 {len(data['字符集_cnsh9622'])} 个字符（汉字+拉丁+符号）"
    data["元数据"]["拉丁扩展时间"] = datetime.now().isoformat()
    data["元数据"]["拉丁扩展DNA"] = DNA
    data["元数据"]["许可证"] = "SIL Open Font License 1.1"

    new_path = base_dir / "glyphs" / "龍魂字元库_v0004_办公版.json"
    with open(new_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ 已扩展办公版字元库: {new_path}")
    print(f"   新增字符: {added}")
    print(f"   总字符数: {len(data['字符集_cnsh9622'])}")
    print(f"   汉字: {sum(1 for c in data['字符集_cnsh9622'] if '\\u4e00' <= c <= '\\u9fff')}")
    return str(new_path)


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else None
    expand(path)
