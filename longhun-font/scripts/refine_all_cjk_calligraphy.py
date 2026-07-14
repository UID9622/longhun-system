#!/usr/bin/env python3
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# DNA追溯码:#龍芯⚡️2026-06-22-LONGHUN-FONT-REFINE-ALL-CJK-CALLIGRAPHY-v1.0

"""
LonghunFont 全量 CJK 书法骨架精修脚本

使用 glyph_generator_calligraphy.py 重新生成所有 CJK 统一表意文字
（U+4E00 ~ U+9FFF）的书法风格占位骨架，保留非 CJK 字形不变。
"""

import json
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from glyph_generator_calligraphy import generate_skeleton, structure_of, stroke_count_of

DNA = "#龍芯⚡️2026-06-22-LONGHUN-FONT-REFINE-ALL-CJK-CALLIGRAPHY-v1.0"


def is_cjk(char: str) -> bool:
    code = ord(char)
    return (0x4E00 <= code <= 0x9FFF) or (0x3400 <= code <= 0x4DBF) or (0xF900 <= code <= 0xFAFF)


def refine(glyph_path: str, output_path: str):
    glyph_path = Path(glyph_path)
    output_path = Path(output_path)

    with open(glyph_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    glyphs = data["字符集_cnsh9622"]
    refined = 0
    preserved = 0

    for char, glyph in glyphs.items():
        if is_cjk(char):
            glyph["结构"] = structure_of(char)
            glyph["笔画数"] = stroke_count_of(char)
            glyph["笔画路径_cnsh9622"] = generate_skeleton(char)
            refined += 1
        else:
            preserved += 1

    metadata = data.get("元数据", {})
    stem_parts = output_path.stem.split("_")
    if len(stem_parts) >= 3 and stem_parts[1].startswith("v"):
        version_hint = f"{stem_parts[1]}-{stem_parts[2]}"
    else:
        version_hint = output_path.stem.split("_")[-1] if "_" in output_path.stem else "书法骨架版"
    metadata["版本"] = version_hint
    metadata["描述"] = (
        metadata.get("描述", "")
        + " | 使用 glyph_generator_calligraphy v1.0 生成全量 CJK 书法骨架"
    )
    metadata["书法骨架时间"] = datetime.now().isoformat()
    metadata["书法骨架DNA"] = DNA
    metadata["书法骨架中文字符数"] = refined
    metadata["书法骨架保留非汉字数"] = preserved
    metadata["总字符数"] = len(glyphs)
    data["元数据"] = metadata
    data["DNA追溯码"] = DNA

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("✅ CJK 书法骨架精修完成")
    print(f"   源字元库: {glyph_path}")
    print(f"   输出字元库: {output_path}")
    print(f"   精修 CJK 汉字: {refined}")
    print(f"   保留非 CJK 字形: {preserved}")
    print(f"   总字元数: {len(glyphs)}")
    print(f"   DNA: {DNA}")


if __name__ == "__main__":
    base_dir = Path(__file__).parent.parent
    src = base_dir / "glyphs" / "龍魂字元库_v0019_全量中文.json"
    out = base_dir / "glyphs" / "龍魂字元库_v0019_书法骨架版.json"
    if len(sys.argv) > 1:
        src = Path(sys.argv[1])
    if len(sys.argv) > 2:
        out = Path(sys.argv[2])
    refine(str(src), str(out))
