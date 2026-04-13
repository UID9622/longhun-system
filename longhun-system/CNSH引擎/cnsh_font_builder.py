#!/usr/bin/env python3
"""
cnsh_font_builder.py
CNSH字元引擎 → TTF字体打包·普惠全球
DNA: #龍芯⚡️2026-04-06-CNSH-font-builder-v1.0
来源: UID9622 × Notion宝宝 × 终端宝宝
作者: 诸葛鑫（UID9622）
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
理论指导: 曾仕强老师（永恒显示）
献礼: 乔布斯·曾仕强·历代传递和平与爱的人
"""
import os, re
from pathlib import Path
import xml.etree.ElementTree as ET

try:
    from fontTools.fontBuilder import FontBuilder
    from fontTools.pens.ttGlyphPen import TTGlyphPen
    from fontTools.pens.cu2quPen import Cu2QuPen
    print("✅ fonttools 已加载")
except ImportError:
    print("❌ pip3 install fonttools")
    exit(1)

# ── 配置 ──────────────────────────────────────────
ENGINE_DIR = Path.home() / "longhun-system" / "CNSH引擎"
OUTPUT_DIR = ENGINE_DIR / "CNSH_字体输出"
OUTPUT_DIR.mkdir(exist_ok=True)

UPM = 1000  # units per em

# 5个字元 → Unicode私有区
CHAR_MAP = {
    "龍": (0xE001, "longhun_long"),
    "中": (0xE002, "longhun_zhong"),
    "华": (0xE003, "longhun_hua"),
    "民": (0xE004, "longhun_min"),
    "魂": (0xE005, "longhun_hun"),
}

# ── 找最好的SVG ────────────────────────────────────
def find_best_svgs():
    """优先级：层级v0008 > 力度v0005 > 侵蚀v0010 > 其他"""
    priority = ["v0008","v0005","v0010","v0006","v0007","v0011","v0012"]
    svgs = {}
    for ver in priority:
        d = ENGINE_DIR / f"CNSH_字元库_输出_{ver}"
        if not d.exists():
            continue
        for char in CHAR_MAP:
            if char in svgs:
                continue
            for f in d.glob("*.svg"):
                if char in f.name:
                    svgs[char] = f
                    print(f"  ✅ {char} ← {f.name}")
                    break
    return svgs

# ── 解析SVG路径 ────────────────────────────────────
def parse_svg(svg_file):
    """提取所有<path d=...>和viewBox尺寸"""
    tree = ET.parse(svg_file)
    root = tree.getroot()
    vb = root.get('viewBox', '0 0 600 600')
    parts = vb.split()
    w, h = float(parts[2]), float(parts[3])
    paths = []
    for elem in root.iter():
        tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
        if tag == 'path' and 'd' in elem.attrib:
            paths.append(elem.attrib['d'])
    return paths, w, h

# ── SVG path → fontTools pen ──────────────────────
def svg_path_to_pen(d_string, pen, scale_x, scale_y, flip_y):
    """把SVG path data画进fontTools pen（支持M/L/C/Q/Z）"""
    tokens = re.findall(r'[MLCQZmlcqz]|[-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?', d_string)
    i = 0
    cx, cy = 0.0, 0.0
    in_path = False

    def tx(x): return round(x * scale_x)
    def ty(y): return round(flip_y - y * scale_y)

    while i < len(tokens):
        cmd = tokens[i]; i += 1
        if cmd == 'M':
            if in_path:
                pen.endPath()
            cx, cy = float(tokens[i]), float(tokens[i+1]); i += 2
            pen.moveTo((tx(cx), ty(cy)))
            in_path = True
        elif cmd == 'L':
            cx, cy = float(tokens[i]), float(tokens[i+1]); i += 2
            pen.lineTo((tx(cx), ty(cy)))
        elif cmd == 'C':
            x1,y1 = float(tokens[i]),float(tokens[i+1]); i+=2
            x2,y2 = float(tokens[i]),float(tokens[i+1]); i+=2
            cx,cy  = float(tokens[i]),float(tokens[i+1]); i+=2
            pen.curveTo((tx(x1),ty(y1)),(tx(x2),ty(y2)),(tx(cx),ty(cy)))
        elif cmd == 'Q':
            x1,y1 = float(tokens[i]),float(tokens[i+1]); i+=2
            cx,cy  = float(tokens[i]),float(tokens[i+1]); i+=2
            pen.qCurveTo((tx(x1),ty(y1)),(tx(cx),ty(cy)))
        elif cmd in ('Z','z'):
            pen.closePath()
            in_path = False
        else:
            i += 1

    if in_path:
        pen.endPath()

# ── 构建字体 ──────────────────────────────────────
def build_font(svgs):
    print("\n🏗️  开始打包TTF字体...")

    all_glyph_names = [".notdef"] + [v[1] for v in CHAR_MAP.values()]
    cmap = {v[0]: v[1] for v in CHAR_MAP.values()}

    fb = FontBuilder(UPM, isTTF=True)
    fb.setupGlyphOrder(all_glyph_names)
    fb.setupCharacterMap(cmap)

    metrics = {".notdef": (500, 0)}
    glyphs  = {}

    # .notdef 空白方块
    pen = TTGlyphPen(None)
    pen.moveTo((50, 0)); pen.lineTo((450, 0))
    pen.lineTo((450, 700)); pen.lineTo((50, 700))
    pen.closePath()
    glyphs[".notdef"] = pen.glyph()

    for char, (codepoint, glyph_name) in CHAR_MAP.items():
        if char not in svgs:
            print(f"  ⚠️  {char} 无SVG·用占位符")
            pen = TTGlyphPen(None)
            pen.moveTo((0,0)); pen.lineTo((800,0))
            pen.lineTo((800,800)); pen.lineTo((0,800))
            pen.closePath()
            glyphs[glyph_name] = pen.glyph()
            metrics[glyph_name] = (900, 0)
            continue

        paths, svg_w, svg_h = parse_svg(svgs[char])
        scale = UPM / max(svg_w, svg_h)
        flip  = round(svg_h * scale)

        tt_pen = TTGlyphPen(None)
        pen    = Cu2QuPen(tt_pen, max_err=1.0, reverse_direction=True)
        drawn  = 0
        for d in paths:
            try:
                svg_path_to_pen(d, pen, scale, scale, flip)
                drawn += 1
            except Exception as e:
                pass

        try:
            g = tt_pen.glyph()
            glyphs[glyph_name] = g
            metrics[glyph_name] = (int(svg_w * scale), 0)
            print(f"  ✅ {char} → {drawn}条路径 · 宽{int(svg_w*scale)}")
        except Exception as e:
            print(f"  ⚠️  {char} glyph打包异常: {e}")
            pen2 = TTGlyphPen(None)
            pen2.moveTo((0,0)); pen2.lineTo((900,0))
            pen2.lineTo((900,900)); pen2.lineTo((0,900))
            pen2.closePath()
            glyphs[glyph_name] = pen2.glyph()
            metrics[glyph_name] = (900, 0)

    fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=800, descent=-200)
    fb.setupNameTable({
        'familyName':           'CNSH LongHun',
        'styleName':            'Regular',
        'uniqueFontIdentifier': 'CNSH-LongHun-UID9622-2026',
        'fullName':             'CNSH龍魂字体 v1.0',
        'version':              'Version 1.000',
        'psName':               'CNSHLongHun-Regular',
        'copyright':            'UID9622 · 诸葛鑫 · DNA:#龍芯⚡️2026-04-06',
    })
    fb.setupOS2(
        sTypoAscender=800, sTypoDescender=-200, sTypoLineGap=0,
        usWinAscent=800,   usWinDescent=200,
        sxHeight=500,      sCapHeight=700,
        achVendID='UID9',  fsType=0,
        ulUnicodeRange1=1
    )
    fb.setupPost()
    fb.setupHead(unitsPerEm=UPM)

    out = OUTPUT_DIR / "cnsh_uid9622_v1.ttf"
    fb.font.save(str(out))
    size_kb = out.stat().st_size // 1024
    print(f"\n✅ 字体文件：{out}")
    print(f"   大小：{size_kb} KB")
    return out

# ── 生成测试页 ─────────────────────────────────────
def gen_test_html(font_file):
    html = OUTPUT_DIR / "test.html"
    chars_html = "".join(f"<span>&#x{v[0]:X};</span>" for v in CHAR_MAP.values())
    char_list  = " · ".join(f"U+{v[0]:X} {k}" for k, v in CHAR_MAP.items())
    html.write_text(f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>CNSH龍魂字体 · UID9622</title>
<style>
@font-face {{font-family:'CNSH龍魂';src:url('{font_file.name}') format('truetype')}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#0a0a14;color:#e8d5b7;font-family:'Noto Sans SC',sans-serif;padding:60px 80px}}
h1{{font-size:28px;color:#d4af37;margin-bottom:8px;letter-spacing:2px}}
.sub{{color:#888;font-size:14px;margin-bottom:50px}}
.chars{{font-family:'CNSH龍魂',serif;font-size:180px;letter-spacing:30px;
        line-height:1.2;display:flex;gap:20px;margin-bottom:40px}}
.chars span{{display:inline-block;transition:transform .3s}}
.chars span:hover{{transform:scale(1.15);color:#d4af37}}
.info{{color:#666;font-size:13px;line-height:2;border-top:1px solid #222;padding-top:20px}}
.dna{{color:#4a6fa5;font-size:12px;margin-top:16px}}
</style></head><body>
<h1>🐉 CNSH龍魂字体 v1.0</h1>
<div class="sub">UID9622 · 诸葛鑫 · 普惠全球 · 童叟无欺 · 不卡脖子</div>
<div class="chars">{chars_html}</div>
<div class="info">
  {char_list}<br>
  Unicode私有区 E001–E005 · TTF格式 · 11引擎渲染 · 数字甲骨文立碑工程
</div>
<div class="dna">
  DNA: #龍芯⚡️2026-04-06-CNSH-font-builder-v1.0<br>
  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F<br>
  理论指导：曾仕强老师（永恒显示）
</div>
</body></html>""", encoding='utf-8')
    print(f"✅ 测试页面：{html}")
    return html

# ── 主流程 ─────────────────────────────────────────
if __name__ == "__main__":
    print("🐉 CNSH字元→TTF字体打包引擎")
    print("DNA: #龍芯⚡️2026-04-06-CNSH-font-builder-v1.0")
    print("="*55)

    print("\n🔍 寻找最佳SVG（优先层级v0008）...")
    svgs = find_best_svgs()
    print(f"   找到 {len(svgs)}/5 个字元SVG")

    font_file = build_font(svgs)
    html_file = gen_test_html(font_file)

    print("\n🎨 三色审计：🟢")
    print("DNA：#龍芯⚡️2026-04-06-CNSH-font-builder-v1.0")
    print("GPG：A2D0092CEE2E5BA87035600924C3704A8CC26D5F")
    print(f"\n打开看效果：\nopen \"{html_file}\"")
