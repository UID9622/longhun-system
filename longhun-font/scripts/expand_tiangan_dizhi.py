# DNA追溯码:#龍芯⚡️2026-06-22-LONGHUN-FONT-FRAGMENT-TIANGAN_DIZHI-v1.0
"""
LonghunFont fragment generator: 天干地支 symbolic icons.
Generates 22 seal/ancient-script style glyph definitions for the 10 Heavenly Stems
and 12 Earthly Branches, starting at PUA codepoint U+E400.
"""
import json
import math
import os

# ---------------------------------------------------------------------------
# Stroke command helpers
# ---------------------------------------------------------------------------
def stroke_move(x, y):
    return {"类型": "移动到", "坐标": [x, y]}


def stroke_line(x, y):
    return {"类型": "直线段", "终点": [x, y]}


def polyline(points):
    """points is a list of (x, y) tuples."""
    if not points:
        return []
    cmds = [stroke_move(points[0][0], points[0][1])]
    for x, y in points[1:]:
        cmds.append(stroke_line(x, y))
    return cmds


def circle(cx, cy, r, segments=12):
    pts = []
    for i in range(segments + 1):
        a = 2 * math.pi * i / segments
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return polyline(pts)


def arc(cx, cy, r, start_angle, end_angle, segments=12):
    pts = []
    for i in range(segments + 1):
        t = i / segments
        a = start_angle + (end_angle - start_angle) * t
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return polyline(pts)


def hline(y, x1, x2):
    return polyline([(x1, y), (x2, y)])


def vline(x, y1, y2):
    return polyline([(x, y1), (x, y2)])


def rect(x1, y1, x2, y2):
    return polyline([(x1, y1), (x2, y1), (x2, y2), (x1, y2), (x1, y1)])


# ---------------------------------------------------------------------------
# Style parameters shared by this fragment
# ---------------------------------------------------------------------------
def style_params():
    return {"力度": 0.85, "棱角": 0.35, "节奏": 0.5, "墨色": 0.9}


# ---------------------------------------------------------------------------
# Glyph builders: 10 Heavenly Stems (天干)
# ---------------------------------------------------------------------------
def glyph_jia():
    # 甲: shell/tree form, vertical spine with cross bars
    strokes = []
    strokes.extend(vline(300, 120, 480))            # main vertical
    strokes.extend(hline(160, 220, 380))             # top cross
    strokes.extend(hline(320, 240, 360))             # middle bar
    strokes.extend(polyline([(240, 440), (360, 440)]))  # bottom bar
    return strokes


def glyph_yi():
    # 乙: curved hook, ancient hook-knife form
    return polyline([
        (160, 140), (440, 140), (440, 280),
        (240, 280), (240, 460), (400, 460)
    ])


def glyph_bing():
    # 丙: three horizontal rays on a vertical
    strokes = []
    strokes.extend(vline(300, 120, 480))
    strokes.extend(hline(180, 220, 380))
    strokes.extend(hline(300, 220, 380))
    strokes.extend(hline(420, 220, 380))
    return strokes


def glyph_ding():
    # 丁: nail / inverted T
    strokes = []
    strokes.extend(hline(160, 180, 420))
    strokes.extend(vline(300, 160, 480))
    return strokes


def glyph_wu():
    # 戊: spear-axe, diagonal shaft with blade hook
    strokes = []
    strokes.extend(polyline([(180, 180), (420, 420)]))
    strokes.extend(polyline([(260, 260), (360, 200), (380, 260)]))
    strokes.extend(polyline([(320, 320), (420, 320), (420, 400)]))
    return strokes


def glyph_ji():
    # 己: hook / coiled rope
    return polyline([
        (420, 140), (220, 140), (220, 460), (380, 460),
        (380, 280), (280, 280)
    ])


def glyph_geng():
    # 庚: winnowing basket / house roof with legs
    strokes = []
    strokes.extend(polyline([(200, 200), (300, 120), (400, 200)]))
    strokes.extend(polyline([(240, 200), (240, 480)]))
    strokes.extend(polyline([(360, 200), (360, 480)]))
    strokes.extend(hline(300, 260, 340))
    return strokes


def glyph_xin():
    # 辛: chisel / cross with top stand
    strokes = []
    strokes.extend(vline(300, 120, 480))
    strokes.extend(hline(240, 220, 380))
    strokes.extend(polyline([(240, 360), (360, 360), (360, 440), (240, 440), (240, 360)]))
    return strokes


def glyph_ren():
    # 壬: burden / three beams carried on shoulder
    strokes = []
    strokes.extend(vline(300, 140, 460))
    strokes.extend(hline(180, 220, 380))
    strokes.extend(hline(300, 220, 380))
    strokes.extend(hline(420, 220, 380))
    return strokes


def glyph_gui():
    # 癸: measuring instrument / cross with four feet
    strokes = []
    strokes.extend(vline(300, 120, 480))
    strokes.extend(hline(300, 220, 380))
    strokes.extend(polyline([(220, 220), (220, 260)]))
    strokes.extend(polyline([(380, 220), (380, 260)]))
    strokes.extend(polyline([(220, 420), (220, 460)]))
    strokes.extend(polyline([(380, 420), (380, 460)]))
    return strokes


# ---------------------------------------------------------------------------
# Glyph builders: 12 Earthly Branches (地支)
# ---------------------------------------------------------------------------
def glyph_zi():
    # 子: rat, small circle body with ears and tail
    strokes = []
    strokes.extend(circle(300, 320, 80, segments=14))
    strokes.extend(polyline([(220, 240), (200, 180), (240, 200)]))  # left ear
    strokes.extend(polyline([(380, 240), (400, 180), (360, 200)]))  # right ear
    strokes.extend(polyline([(380, 360), (460, 400), (440, 440)]))  # tail curl
    return strokes


def glyph_chou():
    # 丑: ox horns, two upward sweeping curves from a yoke
    strokes = []
    strokes.extend(hline(420, 180, 420))
    strokes.extend(arc(180, 420, 70, math.pi, 0, segments=10))
    strokes.extend(arc(420, 420, 70, math.pi, 0, segments=10))
    return strokes


def glyph_yin():
    # 寅: tiger / shelter, peaked roof with three vertical stripes
    strokes = []
    strokes.extend(polyline([(180, 220), (300, 120), (420, 220)]))
    strokes.extend(vline(260, 220, 480))
    strokes.extend(vline(300, 220, 480))
    strokes.extend(vline(340, 220, 480))
    strokes.extend(hline(480, 220, 380))
    return strokes


def glyph_mao():
    # 卯: rabbit ears, two long ears above a small face
    strokes = []
    strokes.extend(polyline([(260, 160), (240, 320)]))
    strokes.extend(polyline([(340, 160), (360, 320)]))
    strokes.extend(circle(300, 380, 60, segments=12))
    strokes.extend(polyline([(260, 360), (280, 380), (260, 400)]))
    strokes.extend(polyline([(340, 360), (320, 380), (340, 400)]))
    return strokes


def glyph_chen():
    # 辰: dragon, wavy S body with head crest
    strokes = []
    strokes.extend(polyline([
        (180, 160), (240, 160), (260, 240), (340, 240),
        (360, 320), (420, 320), (440, 400)
    ]))
    strokes.extend(polyline([(180, 160), (160, 120), (200, 120)]))
    strokes.extend(polyline([(420, 320), (460, 300), (460, 340)]))
    return strokes


def glyph_si():
    # 巳: snake, coiled S curve
    return polyline([
        (180, 180), (300, 180), (340, 260), (260, 340),
        (260, 420), (380, 420), (420, 460)
    ])


def glyph_wu_dizhi():
    # 午: horse, head and mane abstract
    strokes = []
    strokes.extend(polyline([(200, 220), (240, 180), (320, 180), (340, 240)]))
    strokes.extend(polyline([(340, 240), (340, 460)]))
    strokes.extend(polyline([(260, 300), (260, 460)]))
    strokes.extend(polyline([(200, 220), (160, 260), (200, 300)]))
    return strokes


def glyph_wei():
    # 未: goat / tree, branching top with trunk
    strokes = []
    strokes.extend(vline(300, 120, 480))
    strokes.extend(polyline([(300, 200), (220, 160)]))
    strokes.extend(polyline([(300, 240), (380, 180)]))
    strokes.extend(polyline([(300, 360), (220, 420)]))
    strokes.extend(polyline([(300, 360), (380, 420)]))
    return strokes


def glyph_shen():
    # 申: extend / monkey, central line with two reaching arms
    strokes = []
    strokes.extend(vline(300, 120, 480))
    strokes.extend(hline(240, 220, 380))
    strokes.extend(polyline([(220, 240), (160, 240), (160, 300)]))
    strokes.extend(polyline([(380, 240), (440, 240), (440, 300)]))
    return strokes


def glyph_you():
    # 酉: wine vessel, jar with neck
    strokes = []
    strokes.extend(hline(220, 240, 360))
    strokes.extend(polyline([(240, 220), (240, 280), (200, 320), (200, 460), (400, 460), (400, 320), (360, 280), (360, 220)]))
    return strokes


def glyph_xu():
    # 戌: dog, sitting profile with tail
    strokes = []
    strokes.extend(polyline([
        (200, 200), (260, 160), (340, 200), (340, 320),
        (400, 380), (400, 460)
    ]))
    strokes.extend(polyline([(340, 320), (260, 380), (260, 460)]))
    strokes.extend(polyline([(260, 200), (220, 260), (200, 240)]))
    return strokes


def glyph_hai():
    # 亥: pig / boar, round snout with small ears
    strokes = []
    strokes.extend(circle(300, 340, 90, segments=14))
    strokes.extend(polyline([(220, 260), (180, 200), (240, 220)]))
    strokes.extend(polyline([(380, 260), (420, 200), (360, 220)]))
    strokes.extend(polyline([(260, 340), (280, 360), (260, 380)]))
    strokes.extend(polyline([(340, 340), (320, 360), (340, 380)]))
    return strokes


# ---------------------------------------------------------------------------
# Glyph table
# ---------------------------------------------------------------------------
GLYPH_TABLE = [
    # Heavenly Stems
    ("甲", glyph_jia),
    ("乙", glyph_yi),
    ("丙", glyph_bing),
    ("丁", glyph_ding),
    ("戊", glyph_wu),
    ("己", glyph_ji),
    ("庚", glyph_geng),
    ("辛", glyph_xin),
    ("壬", glyph_ren),
    ("癸", glyph_gui),
    # Earthly Branches
    ("子", glyph_zi),
    ("丑", glyph_chou),
    ("寅", glyph_yin),
    ("卯", glyph_mao),
    ("辰", glyph_chen),
    ("巳", glyph_si),
    ("午", glyph_wu_dizhi),
    ("未", glyph_wei),
    ("申", glyph_shen),
    ("酉", glyph_you),
    ("戌", glyph_xu),
    ("亥", glyph_hai),
]


# ---------------------------------------------------------------------------
# Main generator
# ---------------------------------------------------------------------------
def make_fragment(start_codepoint=0xE400):
    fragment = {}
    cp = start_codepoint
    for name, builder in GLYPH_TABLE:
        paths = builder()
        glyph = {
            "unicode": f"U+{cp:04X}",
            "笔画数": len([c for c in paths if c["类型"] == "直线段"]),
            "结构": "天干地支",
            "名称": name,
            "风格参数": style_params(),
            "笔画路径_cnsh9622": paths,
        }
        fragment[chr(cp)] = glyph
        cp += 1
    return fragment, start_codepoint, cp - 1


def main():
    name = "tiangan_dizhi"
    count = 22
    start_codepoint = 0xE400
    dna = "#龍芯⚡️2026-06-22-LONGHUN-FONT-FRAGMENT-TIANGAN_DIZHI-v1.0"

    fragment, first_cp, last_cp = make_fragment(start_codepoint)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(
        script_dir, "..", "glyphs", "fragments", f"{name}.json"
    )
    out_path = os.path.normpath(out_path)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(fragment, f, ensure_ascii=False, indent=2)

    print(f"Symbol set: {name}")
    print(f"Count: {count}")
    print(f"Codepoint range: U+{first_cp:04X} .. U+{last_cp:04X}")
    print(f"DNA: {dna}")
    print(f"Output: {out_path}")


if __name__ == "__main__":
    main()
