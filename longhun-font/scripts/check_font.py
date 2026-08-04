#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
from __future__ import annotations
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# DNA追溯码:#龍芯⚡️2026-06-22-LONGHUN-FONT-CHECK-v1.0

"""
LonghunFont 字元库校验器 v1.0
校验稳定版字元库的完整性、唯一性、编码一致性，并输出审计报告。
"""

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

DNA = "#龍芯⚡️2026-06-22-LONGHUN-FONT-CHECK-v1.0"

REQUIRED_TOP_KEYS = ["DNA追溯码", "元数据", "三色审计_cnsh9622", "字符集_cnsh9622"]
REQUIRED_GLYPH_KEYS = ["unicode", "笔画数", "结构", "风格参数", "笔画路径_cnsh9622"]

# 用户指定的 PUA 合法区间
PUA_RANGES = [
    (0xE000, 0xE007),
    (0xE100, 0xE169),
    (0xE16A, 0xE19B),
    (0xE200, 0xE21C),
    (0xE300, 0xE323),
    (0xE400, 0xE473),
]


def is_pua_codepoint(code: int) -> bool:
    """是否为 PUA 码位（含 Unicode PUA 三个平面）"""
    return (
        0xE000 <= code <= 0xF8FF
        or 0xF0000 <= code <= 0xFFFFD
        or 0x100000 <= code <= 0x10FFFD
    )


def is_in_expected_pua(code: int) -> bool:
    """是否在用户指定的预期 PUA 区间内"""
    return any(start <= code <= end for start, end in PUA_RANGES)


def load_library(path: Path):
    """加载字元库 JSON"""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_structure(data: dict[str, Any], errors: list[Any]):
    """校验顶层结构"""
    for key in REQUIRED_TOP_KEYS:
        if key not in data:
            errors.append(f"缺少顶层键: {key}")


def validate_glyphs(data: dict[str, Any], errors: list[Any]):
    """校验每个字元条目"""
    glyphs = data.get("字符集_cnsh9622", {})
    if not isinstance(glyphs, dict):
        errors.append("字符集_cnsh9622 必须是字典")
        return

    seen_codepoints = {}
    for char, glyph in glyphs.items():
        # 必填键检查
        for key in REQUIRED_GLYPH_KEYS:
            if key not in glyph:
                errors.append(f"字元 '{char}' 缺少键: {key}")

        code = ord(char)

        # unicode 字段格式与一致性
        unicode_field = glyph.get("unicode", "")
        if not isinstance(unicode_field, str) or not unicode_field.startswith("U+"):
            errors.append(f"字元 '{char}' unicode 字段格式错误: {unicode_field!r}")
        else:
            try:
                declared = int(unicode_field[2:], 16)
                if declared != code:
                    errors.append(
                        f"字元 '{char}' unicode 不一致: 字段={unicode_field}, 实际码位=U+{code:04X}"
                    )
            except ValueError:
                errors.append(f"字元 '{char}' unicode 字段非有效十六进制: {unicode_field}")

        # 重复码位检查
        if code in seen_codepoints:
            errors.append(
                f"重复码位 U+{code:04X}: '{seen_codepoints[code]}' 与 '{char}'"
            )
        else:
            seen_codepoints[code] = char

        # PUA 范围检查
        if is_pua_codepoint(code) and not is_in_expected_pua(code):
            errors.append(
                f"字元 '{char}' (U+{code:04X}) 不在预期 PUA 区间 {PUA_RANGES} 内"
            )


def count_categories(glyphs: dict[str, Any]):
    """分类统计字元"""
    chinese = 0
    latin = 0
    digits = 0
    symbols = 0
    pua_categories = Counter()

    for char, glyph in glyphs.items():
        code = ord(char)
        structure = glyph.get("结构", "未知")

        if 0x4E00 <= code <= 0x9FFF:
            chinese += 1
        elif 0x41 <= code <= 0x5A or 0x61 <= code <= 0x7A:
            latin += 1
        elif 0x30 <= code <= 0x39:
            digits += 1
        elif is_pua_codepoint(code):
            pua_categories[structure] += 1
        else:
            symbols += 1

    return {
        "total": len(glyphs),
        "chinese": chinese,
        "latin": latin,
        "digits": digits,
        "symbols": symbols,
        "pua": sum(pua_categories.values()),
        "pua_categories": pua_categories,
    }


def main():
    parser = argparse.ArgumentParser(
        description="LonghunFont 字元库校验器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    default_glyph = (
        Path(__file__).parent.parent
        / "glyphs"
        / "龍魂字元库_v0013_稳定版.json"
    )
    parser.add_argument(
        "glyph_library",
        nargs="?",
        default=str(default_glyph),
        help="字元库 JSON 路径",
    )
    args = parser.parse_args()

    glyph_path = Path(args.glyph_library)
    print("=" * 60)
    print("🐉 LonghunFont 字元库校验报告")
    print(f"DNA: {DNA}")
    print(f"字元库: {glyph_path}")
    print("=" * 60)

    errors = []

    if not glyph_path.exists():
        errors.append(f"字元库文件不存在: {glyph_path}")
    else:
        try:
            data = load_library(glyph_path)
        except json.JSONDecodeError as e:
            errors.append(f"JSON 解析失败: {e}")
            data = {}
        except Exception as e:
            errors.append(f"加载失败: {e}")
            data = {}

        if data:
            validate_structure(data, errors)
            validate_glyphs(data, errors)
            glyphs = data.get("字符集_cnsh9622", {})
            stats = count_categories(glyphs)

    print()
    if 'stats' in locals():
        print("📊 统计摘要")
        print(f"   总字元数: {stats['total']}")
        print(f"   汉字 (U+4E00~U+9FFF): {stats['chinese']}")
        print(f"   拉丁字母: {stats['latin']}")
        print(f"   数字: {stats['digits']}")
        print(f"   其他符号: {stats['symbols']}")
        print(f"   PUA 文化图标合计: {stats['pua']}")
        if stats["pua_categories"]:
            print("   PUA 分类明细:")
            for category, count in sorted(stats["pua_categories"].items()):
                print(f"      · {category}: {count}")
    else:
        print("⚠️ 无法生成统计摘要（字元库加载失败）")

    print()
    if errors:
        print(f"❌ 发现 {len(errors)} 处错误:")
        for err in errors:
            print(f"   - {err}")
        print()
        print(f"DNA: {DNA}")
        sys.exit(1)
    else:
        print("✅ 校验通过，字元库完整且一致。")
        print(f"DNA: {DNA}")
        sys.exit(0)


if __name__ == "__main__":
    main()
