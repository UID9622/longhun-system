#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
#!/usr/bin/env python3
# DNA追溯码:#龍芯⚡️丙午·甲午·丁卯·丙午·䷚颐-LONGHUN-FONT-WUWU-COLOR-FILE1-v1.0
"""
LonghunFont 女娲五彩石彩色字体原型

把选定字符的每个字形拆成 5 个纵向色带，分别绑定红/黄/青/白/黑，
生成 COLR/CPAL 彩色 OTF。这是文化主权在字体层面的直接表达：
每个字都自带女娲五色石光环，不依赖外部 CSS/JS。

用法：
    python3 scripts/build_wuwu_color_font.py \
        glyphs/龍魂字元库_v0019_龍纹书法版.json \
        output/LonghunFont-WuwuColor.otf \
        "红黄青白黑龍魂字体"
"""

import json
import os
import sys
from pathlib import Path

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.t2CharStringPen import T2CharStringPen

# 从 build_font.py 复用辅助函数
sys.path.insert(0, str(Path(__file__).parent))
from build_font import (
    UNITS_PER_EM,
    VIEWBOX,
    ASCENDER,
    DESCENDER,
    LINE_GAP,
    CAP_HEIGHT,
    X_HEIGHT,
    path_to_contours,
    scale_contour,
    compute_bbox,
    is_cjk,
    is_fullwidth_symbol,
)

DNA = "#龍芯⚡️丙午·甲午·丁卯·丙午·䷚颐-LONGHUN-FONT-WUWU-COLOR-v1.0"

# 女娲五彩石色卡（0..1 浮点 RGBA）
WUWU_COLORS = [
    (1.0, 0.0, 0.0, 1.0),  # 红
    (1.0, 1.0, 0.0, 1.0),  # 黄
    (0.0, 1.0, 1.0, 1.0),  # 青
    (1.0, 1.0, 1.0, 1.0),  # 白
    (0.0, 0.0, 0.0, 1.0),  # 黑
]


def rect_contour(x1, y1, x2, y2):
    """返回闭合矩形轮廓（逆时针）。"""
    return [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]


def build_color_otf(glyph_path: str, output_path: str, subset_text: str):
    with open(glyph_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    all_chars = data["字符集_cnsh9622"]
    scale = UNITS_PER_EM / VIEWBOX

    # 去重保留输入顺序
    subset_chars = []
    seen = set()
    for c in subset_text:
        if c in all_chars and c not in seen:
            subset_chars.append(c)
            seen.add(c)

    if not subset_chars:
        print("❌ 子集中没有可用字符", file=sys.stderr)
        sys.exit(1)

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

    color_layers = {}

    for char in subset_chars:
        base_name = f"uni{ord(char):04X}"
        cmap[ord(char)] = base_name
        glyph_order.append(base_name)

        strokes = all_chars[char]["笔画路径_cnsh9622"]
        contours = path_to_contours(strokes)
        bbox = compute_bbox(contours, scale)
        glyph_bboxes[base_name] = bbox

        # 绘制基础单色字形（作为 COLR 的底或主体）
        pen = T2CharStringPen(UNITS_PER_EM, None)
        for contour in contours:
            sc = scale_contour(contour, scale)
            if not sc:
                continue
            pen.moveTo(sc[0])
            for pt in sc[1:]:
                pen.lineTo(pt)
            pen.closePath()
        charstrings[base_name] = pen.getCharString()

        # 为该字生成 5 个纵向色带层
        x_min, y_min, x_max, y_max = bbox
        width = max(1, x_max - x_min)
        height = max(1, y_max - y_min)
        strip_w = width / len(WUWU_COLORS)

        layers = []
        for i, color in enumerate(WUWU_COLORS):
            layer_name = f"{base_name}.lyr{i}"
            glyph_order.append(layer_name)

            x1 = x_min + i * strip_w
            x2 = x_min + (i + 1) * strip_w
            # 色带略大于分割缝，避免渲染间隙
            x1 -= 1
            x2 += 1
            y1 = y_min - 1
            y2 = y_max + 1

            contour = rect_contour(x1, y1, x2, y2)
            pen = T2CharStringPen(UNITS_PER_EM, None)
            pen.moveTo(contour[0])
            for pt in contour[1:]:
                pen.lineTo(pt)
            pen.closePath()
            charstrings[layer_name] = pen.getCharString()
            glyph_bboxes[layer_name] = (x1, y1, x2, y2)

            # COLR v0 格式：[(layerGlyphName, colorID), ...]
            layers.append((layer_name, i))

        color_layers[base_name] = layers

    # 水平字距
    metrics = {}
    for name in glyph_order:
        if name == ".notdef":
            metrics[name] = (1000, 0)
            continue
        if name.startswith("uni") and ".lyr" not in name:
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
        else:
            # 图层字形不需要独立 metrics，给默认值
            metrics[name] = (0, 0)

    global_bbox = [
        min(b[0] for b in glyph_bboxes.values()),
        min(b[1] for b in glyph_bboxes.values()),
        max(b[2] for b in glyph_bboxes.values()),
        max(b[3] for b in glyph_bboxes.values()),
    ]

    fb = FontBuilder(UNITS_PER_EM, isTTF=False)
    fb.setupGlyphOrder(glyph_order)
    fb.setupCFF(
        psName="LonghunFont-WuwuColor",
        fontInfo={
            "version": "1.000",
            "FullName": "LonghunFont Wuwu Color",
            "FamilyName": "LonghunFont Wuwu Color",
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
        "copyright": f"LonghunFont Wuwu Color by UID9622 · DNA追溯 {DNA} · SIL Open Font License 1.1",
        "familyName": "LonghunFont Wuwu Color",
        "styleName": "Regular",
        "uniqueFontIdentifier": "LonghunFont-WuwuColor-1.000",
        "fullName": "LonghunFont Wuwu Color",
        "version": "Version 1.000",
        "psName": "LonghunFont-WuwuColor",
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

    os2 = fb.font["OS/2"]
    if os2.version >= 2:
        os2.sCapHeight = CAP_HEIGHT
        os2.sxHeight = X_HEIGHT

    # CPAL 与 COLR
    fb.setupCPAL([WUWU_COLORS])
    fb.setupCOLR(color_layers, version=0)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fb.save(output_path)
    print(f"✅ 五彩石彩色字体已生成: {output_path}")
    print(f"   基础字形数: {len(cmap)}")
    print(f"   图层字形数: {len(color_layers) * len(WUWU_COLORS)}")
    print(f"   总字形数: {len(glyph_order) - 1}")
    print(f"   全局外框: {global_bbox}")
    print(f"   DNA: {DNA}")


if __name__ == "__main__":
    base_dir = Path(__file__).parent.parent
    glyph_path = base_dir / "glyphs" / "龍魂字元库_v0019_龍纹书法版.json"
    output_path = base_dir / "output" / "LonghunFont-WuwuColor.otf"
    subset_text = "红黄青白黑龍魂字体"

    if len(sys.argv) > 1:
        glyph_path = Path(sys.argv[1])
    if len(sys.argv) > 2:
        output_path = Path(sys.argv[2])
    if len(sys.argv) > 3:
        subset_text = sys.argv[3]

    build_color_otf(str(glyph_path), str(output_path), subset_text)
