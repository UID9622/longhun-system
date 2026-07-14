#!/usr/bin/env python3
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# DNA追溯码:#龍芯⚡️2026-06-22-LONGHUN-FONT-BUILD-v2.0

"""
LonghunFont 字体构建器 v2.0
使用 fontTools 将字元库导出为 OTF 字体文件。
支持汉字、拉丁字母、ASCII 数字与符号；
自动计算字面外框 / 安全框 / 水平字距。
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Identity

DNA = "#龍芯⚡️2026-06-22-LONGHUN-FONT-BUILD-v2.0"

# 字框参数
UNITS_PER_EM = 1000
VIEWBOX = 600
STROKE_WIDTH = 24

# 字面外框 / 安全框
ASCENDER = 800
DESCENDER = -200
CAP_HEIGHT = 700
X_HEIGHT = 500
LINE_GAP = 200


def is_cjk(char):
    """判断是否为 CJK 汉字"""
    code = ord(char)
    return (
        0x4E00 <= code <= 0x9FFF or
        0x3400 <= code <= 0x4DBF or
        0xF900 <= code <= 0xFAFF
    )


def is_fullwidth_symbol(char):
    """判断是否为 CJK 全角符号"""
    code = ord(char)
    return 0x3000 <= code <= 0x303F or 0xFF00 <= code <= 0xFFEF


def stroke_line_to_polygon(p1, p2, width=STROKE_WIDTH):
    """将线段加粗为四边形轮廓 (返回逆时针点列表)"""
    x1, y1 = p1
    x2, y2 = p2
    dx = x2 - x1
    dy = y2 - y1
    length = (dx ** 2 + dy ** 2) ** 0.5
    if length < 1e-6:
        return []
    ux = -dy / length
    uy = dx / length
    hw = width / 2
    return [
        (x1 + ux * hw, y1 + uy * hw),
        (x2 + ux * hw, y2 + uy * hw),
        (x2 - ux * hw, y2 - uy * hw),
        (x1 - ux * hw, y1 - uy * hw),
    ]


def path_to_contours(strokes):
    """将笔画路径列表转换为字体轮廓列表"""
    contours = []
    current_point = None

    for stroke in strokes:
        if not isinstance(stroke, dict):
            continue
        t = stroke["类型"]
        if t == "移动到":
            current_point = tuple(stroke["坐标"])
        elif t == "直线段":
            end = tuple(stroke["终点"])
            if current_point is None:
                continue
            poly = stroke_line_to_polygon(current_point, end)
            if poly:
                contours.append(poly)
            current_point = end
        elif t == "三次曲线":
            P1, P2, P3 = [tuple(p) for p in stroke["控制点"]]
            if current_point is None:
                continue
            poly = stroke_line_to_polygon(current_point, P3)
            if poly:
                contours.append(poly)
            current_point = P3

    return contours


def scale_contour(contour, scale):
    """缩放到字体单位"""
    return [(x * scale, y * scale) for x, y in contour]


def compute_bbox(contours, scale):
    """从轮廓计算字面外框 (xMin, yMin, xMax, yMax)"""
    xs = []
    ys = []
    for contour in contours:
        for x, y in scale_contour(contour, scale):
            xs.append(x)
            ys.append(y)
    if not xs:
        return (0, 0, UNITS_PER_EM, UNITS_PER_EM)
    return (min(xs), min(ys), max(xs), max(ys))


def build_otf(glyph_path: str, output_path: str):
    """构建 OTF 字体"""
    with open(glyph_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    chars = data["字符集_cnsh9622"]
    scale = UNITS_PER_EM / VIEWBOX

    cmap = {}
    glyph_order = [".notdef"]
    charstrings = {}
    glyph_bboxes = {}

    # .notdef 字形：简单方块（位于安全框内）
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
        contours = path_to_contours(strokes)
        bbox = compute_bbox(contours, scale)
        glyph_bboxes[glyph_name] = bbox

        pen = T2CharStringPen(UNITS_PER_EM, None)
        if not contours:
            # 空字形（空格）不绘制
            pass
        else:
            for contour in contours:
                sc = scale_contour(contour, scale)
                if not sc:
                    continue
                pen.moveTo(sc[0])
                for pt in sc[1:]:
                    pen.lineTo(pt)
                pen.closePath()

        charstrings[glyph_name] = pen.getCharString()

    # 水平字距：CJK/全角 1000，其他按字面宽 + 安全边距
    metrics = {}
    for name in glyph_order:
        if name == ".notdef":
            metrics[name] = (1000, 0)
            continue
        char = chr(int(name[3:], 16))
        x_min, _, x_max, _ = glyph_bboxes[name]
        if is_cjk(char) or is_fullwidth_symbol(char):
            advance = UNITS_PER_EM
            lsb = 0
        else:
            width = x_max - x_min
            side = max(50, (UNITS_PER_EM - width) / 2)
            advance = int(width + side * 2)
            lsb = int(x_min - side)
            # 保证非负且合理
            if lsb < 0:
                advance -= lsb
                lsb = 0
        metrics[name] = (advance, lsb)

    # 全局边界框
    global_bbox = [
        min(b[0] for b in glyph_bboxes.values()),
        min(b[1] for b in glyph_bboxes.values()),
        max(b[2] for b in glyph_bboxes.values()),
        max(b[3] for b in glyph_bboxes.values()),
    ]

    fb = FontBuilder(UNITS_PER_EM, isTTF=False)
    fb.setupGlyphOrder(glyph_order)
    fb.setupCFF(
        psName="LonghunFont-Regular",
        fontInfo={
            "version": "1.000",
            "FullName": "LonghunFont Regular",
            "FamilyName": "LonghunFont",
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
    fb.setupHorizontalHeader(
        ascent=ASCENDER,
        descent=DESCENDER,
        lineGap=LINE_GAP,
    )
    fb.setupOS2(
        sTypoAscender=ASCENDER,
        sTypoDescender=DESCENDER,
        sTypoLineGap=LINE_GAP,
        usWinAscent=1400,
        usWinDescent=400,
        fsSelection=0x0040,  # REGULAR
    )
    fb.setupPost()
    fb.setupNameTable({
        "copyright": "LonghunFont by UID9622 · DNA追溯 #龍芯⚡️ · Licensed under SIL Open Font License 1.1",
        "familyName": "LonghunFont",
        "styleName": "Regular",
        "uniqueFontIdentifier": "LonghunFont-Regular-1.000",
        "fullName": "LonghunFont Regular",
        "version": "Version 1.000",
        "psName": "LonghunFont-Regular",
        "manufacturer": "龍魂系统 · UID9622",
        "licenseDescription": "This Font Software is licensed under the SIL Open Font License, Version 1.1.",
        "licenseInfoURL": "https://openfontlicense.org",
    })
    fb.setupHead(
        fontRevision=1.000,
        flags=0x000B,
        unitsPerEm=UNITS_PER_EM,
        xMin=global_bbox[0],
        yMin=global_bbox[1],
        xMax=global_bbox[2],
        yMax=global_bbox[3],
    )

    # OS/2 v2+ 额外字段：CapHeight / xHeight
    os2 = fb.font["OS/2"]
    if os2.version >= 2:
        os2.sCapHeight = CAP_HEIGHT
        os2.sxHeight = X_HEIGHT

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fb.save(output_path)
    print(f"✅ OTF 字体已生成: {output_path}")
    print(f"   包含字形: {len(cmap)} 个")
    print(f"   全局外框: {global_bbox}")
    print(f"   水平字距: CJK/全角={UNITS_PER_EM}, 拉丁自适应")
    return output_path


if __name__ == "__main__":
    base_dir = Path(__file__).parent.parent
    glyph_path = base_dir / "glyphs" / "龍魂字元库_v0004_办公版.json"
    output_path = base_dir / "output" / "LonghunFont-Regular.otf"

    if len(sys.argv) > 1:
        glyph_path = Path(sys.argv[1])
    if len(sys.argv) > 2:
        output_path = Path(sys.argv[2])

    build_otf(str(glyph_path), str(output_path))
