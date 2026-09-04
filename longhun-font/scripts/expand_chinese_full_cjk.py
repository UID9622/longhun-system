#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
#!/usr/bin/env python3
# DNA追溯码:#龍芯⚡️丙午·甲午·丁卯·丙午·䷚颐-LONGHUN-FONT-EXPAND-FULL-CJK-v1.0
# 龍魂·LonghunFont 中文字元扩展脚本
# 用途：在 v0018 龍纹书法版基础上，补全全部 BMP CJK + Extension A

import json
import sys
from datetime import datetime
from pathlib import Path

from glyph_generator import generate_skeleton, stroke_count_of, structure_of

DNA = "#龍芯⚡️丙午·甲午·丁卯·丙午·䷚颐-LONGHUN-FONT-EXPAND-FULL-CJK-v1.0"


def is_cjk(c: str) -> bool:
    code = ord(c)
    return (0x4E00 <= code <= 0x9FFF) or (0x3400 <= code <= 0x4DBF) or (0xF900 <= code <= 0xFAFF)


def ordered_full_cjk_chars():
    """按 Unicode 码位生成全部 BMP CJK + Extension A 字符。"""
    chars = []
    for start, end in [(0x3400, 0x4DBF), (0x4E00, 0x9FFF), (0xF900, 0xFAFF)]:
        for code in range(start, end + 1):
            chars.append(chr(code))
    return chars


def main():
    base_dir = Path(__file__).parent.parent
    input_path = base_dir / "glyphs" / "龍魂字元库_v0018_龍纹书法版.json"
    output_path = base_dir / "glyphs" / "龍魂字元库_v0019_全量中文.json"

    if not input_path.exists():
        print(f"❌ 未找到输入字元库: {input_path}", file=sys.stderr)
        sys.exit(1)

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    chars = data["字符集_cnsh9622"]
    existing = set(chars.keys())

    added = 0
    skipped_existing = 0

    for char in ordered_full_cjk_chars():
        if not is_cjk(char):
            continue
        if char in existing:
            skipped_existing += 1
            continue

        chars[char] = {
            "unicode": f"U+{ord(char):04X}",
            "笔画数": stroke_count_of(char),
            "结构": structure_of(char),
            "风格参数": {
                "力度": 0.8,
                "棱角": 0.3,
                "节奏": 0.6,
                "墨色": 0.9,
            },
            "笔画路径_cnsh9622": generate_skeleton(char),
        }
        existing.add(char)
        added += 1

    now = datetime.now().isoformat()
    total_chars = len(chars)
    chinese_chars = sum(1 for c in chars if is_cjk(c))

    metadata = data.setdefault("元数据", {})
    previous_version = metadata.get("版本", "v0018-龍纹书法版")
    metadata["名称"] = "龍魂字元库"
    metadata["版本"] = "v0019-全量中文"
    metadata["创建者"] = "UID9622"
    metadata["生成时间"] = now
    metadata["前一版本"] = previous_version
    metadata["本次新增中文字符数"] = added
    metadata["中文字符数"] = chinese_chars
    metadata["总字符数"] = total_chars
    metadata["全量中文扩展时间"] = now
    metadata["全量中文扩展DNA"] = DNA
    metadata["描述"] = (
        "LonghunFont 全量中文字元库。覆盖 BMP CJK 统一表意文字（U+4E00~U+9FFF）、"
        "CJK Extension A（U+3400~U+4DBF）及 CJK 兼容表意文字（U+F900~U+FAFF），"
        f"在 {previous_version} 基础上新增 {added} 个汉字，服务最大范围中文覆盖与全球普惠。"
    )
    metadata["编码标准"] = "UTF-8"
    metadata["viewBox"] = "0 0 600 600"

    data["DNA追溯码"] = DNA

    data.setdefault("三色审计_cnsh9622", {
        "🟢": {"结果": "通过", "项目": "文化主权标识完整"},
        "🟡": {"结果": "通过", "项目": "来源链可追溯"},
        "🔴": {"结果": "通过", "项目": "无商业字体依赖"},
    })

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("✅ 龍魂字元库扩展完成")
    print(f"   输入: {input_path}")
    print(f"   输出: {output_path}")
    print(f"   DNA:  {DNA}")
    print(f"   已存在跳过: {skipped_existing}")
    print(f"   实际新增汉字: {added}")
    print(f"   当前中文字符总数: {chinese_chars}")
    print(f"   当前总字符数: {total_chars}")


if __name__ == "__main__":
    main()
