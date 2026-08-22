#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
#!/usr/bin/env python3
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# DNA追溯码:#龍芯⚡️丙午·甲午·丁卯·丙午·䷚颐-LONGHUN-FONT-BATCH-RENDER-v1.0

"""
LonghunFont 批量渲染器
批量将字元库中的所有字元渲染为 SVG，并生成 HTML 样张。
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent / "engines"))
from cnsh_font_engine_uid9622 import CNSH字元基础引擎_UID9622

DNA = "#龍芯⚡️丙午·甲午·丁卯·丙午·䷚颐-LONGHUN-FONT-BATCH-RENDER-v1.0"


def batch_render(glyph_path: str, output_dir: str):
    """批量渲染所有字元"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    engine = CNSH字元基础引擎_UID9622()
    engine.载入_cnsh数据_cnsh龍魂_v1(glyph_path)

    rendered = []
    failed = []
    for char in sorted(engine.字元集_cnsh9622.keys()):
        try:
            # 统一使用 U+XXXX 文件名，避免大小写/特殊字符冲突
            safe_char = f"U{ord(char):04X}"
            out_file = output_dir / f"{safe_char}.svg"
            engine.输出SVG_cnsh龍魂_v1(char, str(out_file))
            rendered.append(char)
        except Exception as e:
            failed.append((char, str(e)))

    print(f"✅ 成功渲染: {len(rendered)} 个字元")
    if failed:
        print(f"❌ 失败: {len(failed)} 个字元")
        for char, err in failed:
            print(f"   {char}: {err}")

    return rendered, failed


def generate_html_sample(glyph_path: str, output_dir: str, html_path: str):
    """生成 HTML 样张"""
    with open(glyph_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    chars = sorted(data["字符集_cnsh9622"].keys())

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>LonghunFont 字元样张</title>
    <style>
        body {{ font-family: sans-serif; background: #1a1a2e; color: #e0e0e0; padding: 20px; }}
        h1 {{ color: #f9ca24; }}
        .dna {{ color: #4ecdc4; font-family: monospace; margin-bottom: 20px; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(80px, 1fr)); gap: 10px; }}
        .cell {{ background: #16213e; border-radius: 8px; padding: 10px; text-align: center; }}
        .cell img {{ width: 60px; height: 60px; }}
        .cell .char {{ margin-top: 5px; font-size: 12px; color: #aaa; }}
    </style>
</head>
<body>
    <h1>🐉 LonghunFont 字元样张</h1>
    <div class="dna">{DNA}</div>
    <div class="dna">字元库: {Path(glyph_path).name} · 总数: {len(chars)}</div>
    <div class="grid">
"""
    for char in chars:
        safe_char = f"U{ord(char):04X}"
        svg_file = f"{safe_char}.svg"
        html += f"""        <div class="cell">
            <img src="{svg_file}" alt="{char}">
            <div class="char">{char}</div>
        </div>
"""

    html += """    </div>
</body>
</html>
"""

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ HTML 样张已生成: {html_path}")


def main():
    base_dir = Path(__file__).parent.parent
    glyph_path = base_dir / "glyphs" / "龍魂字元库_v0008_文化版.json"
    output_dir = base_dir / "output" / "all_glyphs_v0008"
    html_path = base_dir / "output" / "sample_v0008.html"

    if len(sys.argv) > 1:
        glyph_path = Path(sys.argv[1])
    if len(sys.argv) > 2:
        output_dir = Path(sys.argv[2])
    if len(sys.argv) > 3:
        html_path = Path(sys.argv[3])

    rendered, failed = batch_render(str(glyph_path), str(output_dir))
    generate_html_sample(str(glyph_path), str(output_dir), str(html_path))

    print(f"\n📊 批量渲染完成")
    print(f"   字元库: {glyph_path}")
    print(f"   SVG 目录: {output_dir}")
    print(f"   HTML 样张: {html_path}")
    print(f"   DNA: {DNA}")


if __name__ == "__main__":
    main()
