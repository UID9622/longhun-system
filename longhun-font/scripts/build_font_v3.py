#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
#!/usr/bin/env python3
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# DNA追溯码:#龍芯⚡️丙午·甲午·丁卯·丙午·䷚颐-LONGHUN-FONT-BUILD-v3.0
"""
LonghunFont 字体构建器 v3.0 —— 书法笔意轮廓

在 v2.0 的骨架基础上，把每条笔画（多段线）转换成可变宽度的闭合轮廓：
- 起笔/收笔做 tapered brush tip，模拟毛笔锋颖。
- 横画略粗、竖画略细、撇捺有锋。
- 笔画交接处自然重叠，保持书法气韵。

输出文件默认：output/LonghunFont-Regular-v3.otf
"""

import json
import math
import os
import sys
from pathlib import Path
from datetime import datetime

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.t2CharStringPen import T2CharStringPen

DNA = "#龍芯⚡️丙午·甲午·丁卯·丙午·䷚颐-LONGHUN-FONT-BUILD-v3.0"

UNITS_PER_EM = 1000
VIEWBOX = 600

# 基准笔画宽度（视图坐标）
BASE_WIDTH = 26
HORIZONTAL_WIDTH = 30
VERTICAL_WIDTH = 20
DIAGONAL_WIDTH = 24

ASCENDER = 800
DESCENDER = -200
CAP_HEIGHT = 700
X_HEIGHT = 500
LINE_GAP = 200


def is_cjk(char):
    code = ord(char)
    return (0x4E00 <= code <= 0x9FFF) or (0x3400 <= code <= 0x4DBF) or (0xF900 <= code <= 0xFAFF)


def is_fullwidth_symbol(char):
    code = ord(char)
    return 0x3000 <= code <= 0x303F or 0xFF00 <= code <= 0xFFEF


def _normalize(v):
    d = math.hypot(v[0], v[1])
    if d < 1e-9:
        return (0.0, 0.0)
    return (v[0] / d, v[1] / d)


def _perp(v):
    return (-v[1], v[0])


def _add(a, b, s=1.0):
    return (a[0] + b[0] * s, a[1] + b[1] * s)


def stroke_width_for_segment(p1, p2):
    """根据笔画走向选择宽度：横粗、竖细、斜中。"""
    dx = abs(p2[0] - p1[0])
    dy = abs(p2[1] - p1[1])
    if dx < 1e-6 and dy < 1e-6:
        return BASE_WIDTH
    # 水平主导
    if dx > dy * 2:
        return HORIZONTAL_WIDTH
    # 垂直主导
    if dy > dx * 2:
        return VERTICAL_WIDTH
    return DIAGONAL_WIDTH


def variable_width_polyline(points, base_width=BASE_WIDTH, tip_ratio=0.25):
    """
    把一条折线 points 转换为可变宽度的闭合轮廓。
    宽度沿笔画中心变化：两端 taper 到 base_width*tip_ratio，中间为 base_width。
    返回逆时针闭合点列表（用于 CFF 填充）。
    """
    if len(points) < 2:
        return []

    # 计算累计长度参数 t in [0,1]
    seg_lengths = []
    total = 0.0
    for i in range(len(points) - 1):
        d = math.hypot(points[i + 1][0] - points[i][0], points[i + 1][1] - points[i][1])
        seg_lengths.append(d)
        total += d
    if total < 1e-6:
        return []

    ts = [0.0]
    acc = 0.0
    for d in seg_lengths:
        acc += d
        ts.append(acc / total)

    def width_at(t):
        # 两端锥形，中间饱满；使用 smoothstep
        a = 2 * abs(t - 0.5)
        profile = 1.0 - (1.0 - tip_ratio) * (a * a * (3 - 2 * a))
        return base_width * profile

    lefts = []
    rights = []

    for i, p in enumerate(points):
        # 切线方向
        if i == 0:
            tan = _normalize((points[1][0] - points[0][0], points[1][1] - points[0][1]))
        elif i == len(points) - 1:
            tan = _normalize((points[-1][0] - points[-2][0], points[-1][1] - points[-2][1]))
        else:
            tan = _normalize((points[i + 1][0] - points[i - 1][0], points[i + 1][1] - points[i - 1][1]))

        n = _perp(tan)
        hw = width_at(ts[i]) / 2
        lefts.append(_add(p, n, hw))
        rights.append(_add(p, n, -hw))

    # 闭合：左边缘从头到尾，右边缘从尾到头
    contour = lefts + rights[::-1]
    return contour


def path_to_strokes(strokes):
    """把笔画路径列表拆分为一条条 stroke（每条 stroke 是点的列表）。"""
    result = []
    current = []
    last = None
    for s in strokes:
        if not isinstance(s, dict):
            continue
        t = s["类型"]
        if t == "移动到":
            if len(current) >= 2:
                result.append(current)
            current = [tuple(s["坐标"])]
            last = current[-1]
        elif t == "直线段":
            if current:
                current.append(tuple(s["终点"]))
                last = current[-1]
            else:
                current = [last, tuple(s["终点"])] if last else [tuple(s["终点"])]
        elif t == "三次曲线":
            # 简化：取起点、控制点重心、终点
            if current:
                p0 = current[-1]
                cp = s["控制点"]
                p1, p2, p3 = tuple(cp[0]), tuple(cp[1]), tuple(cp[2])
                # 采样两次贝塞尔近似
                for k in (1, 2, 3):
                    tt = k / 3
                    x = (1 - tt) ** 3 * p0[0] + 3 * (1 - tt) ** 2 * tt * p1[0] + 3 * (1 - tt) * tt ** 2 * p2[0] + tt ** 3 * p3[0]
                    y = (1 - tt) ** 3 * p0[1] + 3 * (1 - tt) ** 2 * tt * p1[1] + 3 * (1 - tt) * tt ** 2 * p2[1] + tt ** 3 * p3[1]
                    current.append((x, y))
    if len(current) >= 2:
        result.append(current)
    return result


def build_otf_v3(glyph_path: str, output_path: str):
    with open(glyph_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    chars = data["字符集_cnsh9622"]
    scale = UNITS_PER_EM / VIEWBOX

    cmap = {}
    glyph_order = [".notdef"]
    charstrings = {}
    glyph_bboxes = {}

    # .notdef
    pen = T2CharStringPen(UNITS_PER_EM, None)
    pen.moveTo((100, 100))
    pen.lineTo((900, 100))
    pen.lineTo((900, 900))
    pen.lineTo((100, 900))
    pen.closePath()
    charstrings[".notdef"] = pen.getCharString()
    glyph_bboxes[".notdef"] = (100, 100, 900, 900)

    for char in sorted(chars.keys()):
        glyph_name = f"uni{ord(char):04X}"
        cmap[ord(char)] = glyph_name
        glyph_order.append(glyph_name)

        strokes = chars[char]["笔画路径_cnsh9622"]
        stroke_polylines = path_to_strokes(strokes)

        contours = []
        for poly in stroke_polylines:
            # 根据笔画首段走向选宽度
            w = stroke_width_for_segment(poly[0], poly[1]) if len(poly) >= 2 else BASE_WIDTH
            contour = variable_width_polyline(poly, base_width=w)
            if contour:
                contours.append(contour)

        # bbox
        xs = [p[0] for c in contours for p in c]
        ys = [p[1] for c in contours for p in c]
        if xs:
            bbox = (min(xs) * scale, min(ys) * scale, max(xs) * scale, max(ys) * scale)
        else:
            bbox = (0, 0, UNITS_PER_EM, UNITS_PER_EM)
        glyph_bboxes[glyph_name] = bbox

        pen = T2CharStringPen(UNITS_PER_EM, None)
        for contour in contours:
            sc = [(x * scale, y * scale) for x, y in contour]
            if not sc:
                continue
            pen.moveTo(sc[0])
            for pt in sc[1:]:
                pen.lineTo(pt)
            pen.closePath()
        charstrings[glyph_name] = pen.getCharString()

    metrics = {}
    for name in glyph_order:
        if name == ".notdef":
            metrics[name] = (1000, 0)
            continue
        char = chr(int(name[3:], 16))
        x_min, _, x_max, _ = glyph_bboxes[name]
        if is_cjk(char) or is_fullwidth_symbol(char):
            metrics[name] = (UNITS_PER_EM, 0)
        else:
            width = x_max - x_min
            side = max(50, (UNITS_PER_EM - width) / 2)
            advance = int(width + side * 2)
            lsb = int(x_min - side)
            if lsb < 0:
                advance -= lsb
                lsb = 0
            metrics[name] = (advance, lsb)

    global_bbox = [
        min(b[0] for b in glyph_bboxes.values()),
        min(b[1] for b in glyph_bboxes.values()),
        max(b[2] for b in glyph_bboxes.values()),
        max(b[3] for b in glyph_bboxes.values()),
    ]

    fb = FontBuilder(UNITS_PER_EM, isTTF=False)
    fb.setupGlyphOrder(glyph_order)
    fb.setupCFF(
        psName="LonghunFont-Regular-v3",
        fontInfo={
            "version": "1.300",
            "FullName": "LonghunFont Regular v3",
            "FamilyName": "LonghunFont v3",
            "Weight": "Regular",
            "isFixedPitch": False,
            "ItalicAngle": 0,
            "UnderlinePosition": -100,
            "UnderlineThickness": 50,
        },
        charStringsDict=charstrings,
        privateDict={"defaultWidthX": 600, "nominalWidthX": 600},
    )
    fb.setupCharacterMap(cmap)
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=ASCENDER, descent=DESCENDER, lineGap=LINE_GAP)
    fb.setupOS2(
        sTypoAscender=ASCENDER,
        sTypoDescender=DESCENDER,
        sTypoLineGap=LINE_GAP,
        usWinAscent=1400,
        usWinDescent=400,
        fsSelection=0x0040,
    )
    fb.setupPost()
    fb.setupNameTable({
        "copyright": f"LonghunFont v3 by UID9622 · DNA追溯 {DNA} · SIL Open Font License 1.1",
        "familyName": "LonghunFont v3",
        "styleName": "Regular",
        "uniqueFontIdentifier": "LonghunFont-Regular-v3-1.300",
        "fullName": "LonghunFont Regular v3",
        "version": "Version 1.300",
        "psName": "LonghunFont-Regular-v3",
        "manufacturer": "龍魂系统 · UID9622",
        "licenseDescription": "This Font Software is licensed under the SIL Open Font License, Version 1.1.",
        "licenseInfoURL": "https://openfontlicense.org",
    })
    fb.setupHead(
        fontRevision=1.300,
        flags=0x000B,
        unitsPerEm=UNITS_PER_EM,
        xMin=global_bbox[0],
        yMin=global_bbox[1],
        xMax=global_bbox[2],
        yMax=global_bbox[3],
    )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fb.save(output_path)
    print(f"✅ v3.0 书法轮廓字体已生成: {output_path}")
    print(f"   总字元数: {len(cmap)}")
    print(f"   全局外框: {global_bbox}")
    print(f"   DNA: {DNA}")


if __name__ == "__main__":
    base_dir = Path(__file__).parent.parent
    glyph_path = base_dir / "glyphs" / "龍魂字元库_v0019_龍纹书法版.json"
    output_path = base_dir / "output" / "LonghunFont-Regular-v3.otf"

    if len(sys.argv) > 1:
        glyph_path = Path(sys.argv[1])
    if len(sys.argv) > 2:
        output_path = Path(sys.argv[2])

    build_otf_v3(str(glyph_path), str(output_path))
