#!/usr/bin/env python3
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# DNA追溯码:#龍芯⚡️2026-06-22-LONGHUN-FONT-REFINE-ALL-CJK-v1.0

"""
LonghunFont 全量 CJK 骨架精修脚本
使用 glyph_generator v2.0 重新生成所有 CJK 汉字的占位骨架，
保留非 CJK 字形（符号、PUA 图标、拉丁等）不变。
"""

import json
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from glyph_generator import generate_skeleton, structure_of, stroke_count_of

DNA = "#龍芯⚡️2026-06-22-LONGHUN-FONT-REFINE-ALL-CJK-v1.0"


def is_cjk(char: str) -> bool:
    code = ord(char)
    return 0x4E00 <= code <= 0x9FFF


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
    metadata["版本"] = "v0015-精修骨架版"
    metadata["描述"] = (
        metadata.get("描述", "")
        + " | 使用 glyph_generator v2.0 精修全部 CJK 占位骨架"
    )
    metadata["精修时间"] = datetime.now().isoformat()
    metadata["精修DNA"] = DNA
    metadata["精修汉字数"] = refined
    metadata["保留非汉字数"] = preserved
    data["元数据"] = metadata
    data["DNA追溯码"] = DNA

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("✅ CJK 骨架精修完成")
    print(f"   源字元库: {glyph_path}")
    print(f"   输出字元库: {output_path}")
    print(f"   精修 CJK 汉字: {refined}")
    print(f"   保留非 CJK 字形: {preserved}")
    print(f"   总字元数: {len(glyphs)}")
    print(f"   DNA: {DNA}")


if __name__ == "__main__":
    base_dir = Path(__file__).parent.parent
    src = base_dir / "glyphs" / "龍魂字元库_v0015_三千五中文字.json"
    out = base_dir / "glyphs" / "龍魂字元库_v0015_精修骨架版.json"
    if len(sys.argv) > 1:
        src = Path(sys.argv[1])
    if len(sys.argv) > 2:
        out = Path(sys.argv[2])
    refine(str(src), str(out))
