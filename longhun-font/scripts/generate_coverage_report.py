#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# DNA追溯码:#龍芯⚡️2026-06-22-LONGHUN-FONT-COVERAGE-REPORT-FILE1-v1.0
"""Generate a Markdown coverage report for the LonghunFont glyph library."""

import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Any


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DEFAULT_GLYPH_LIBRARY = PROJECT_ROOT / "glyphs" / "龍魂字元库_v0019_龍纹书法版.json"
PUA_TABLE_PATH = PROJECT_ROOT / "docs" / "PUA编码表.md"
REPORT_OUTPUT_PATH = PROJECT_ROOT / "docs" / "字体覆盖报告.md"

DNA_CODE = "#龍芯⚡️2026-06-22-LONGHUN-FONT-COVERAGE-REPORT-v1.0"


# ---------------------------------------------------------------------------
# Unicode helpers
# ---------------------------------------------------------------------------
def parse_codepoint(value: str) -> int:
    """Parse 'U+4E00' -> 0x4E00."""
    value = value.strip()
    if value.upper().startswith("U+"):
        return int(value[2:], 16)
    return int(value, 16)


def fmt_codepoint(code: int) -> str:
    if code <= 0xFFFF:
        return f"U+{code:04X}"
    return f"U+{code:04X}"


def fmt_range(start: int, end: int) -> str:
    if start == end:
        return fmt_codepoint(start)
    return f"{fmt_codepoint(start)} ~ {fmt_codepoint(end)}"


# ---------------------------------------------------------------------------
# Unicode block definitions
# ---------------------------------------------------------------------------
UNICODE_BLOCKS = [
    ("Basic Latin", 0x0000, 0x007F),
    ("Latin-1 Supplement", 0x0080, 0x00FF),
    ("Latin Extended-A", 0x0100, 0x017F),
    ("Latin Extended-B", 0x0180, 0x024F),
    ("IPA Extensions", 0x0250, 0x02AF),
    ("Spacing Modifier Letters", 0x02B0, 0x02FF),
    ("Combining Diacritical Marks", 0x0300, 0x036F),
    ("Greek and Coptic", 0x0370, 0x03FF),
    ("Cyrillic", 0x0400, 0x04FF),
    ("Yiijing Hexagram Symbols", 0x4DC0, 0x4DFF),
    ("CJK Unified Ideographs", 0x4E00, 0x9FFF),
    ("Hangul Syllables", 0xAC00, 0xD7AF),
    ("Private Use Area", 0xE000, 0xF8FF),
    ("CJK Unified Ideographs Extension A", 0x3400, 0x4DBF),
    ("CJK Unified Ideographs Extension B", 0x20000, 0x2A6DF),
    ("CJK Unified Ideographs Extension C", 0x2A700, 0x2B73F),
    ("CJK Unified Ideographs Extension D", 0x2B740, 0x2B81F),
    ("General Punctuation", 0x2000, 0x206F),
    ("Superscripts and Subscripts", 0x2070, 0x209F),
    ("Currency Symbols", 0x20A0, 0x20CF),
    ("Letterlike Symbols", 0x2100, 0x214F),
    ("Number Forms", 0x2150, 0x218F),
    ("Arrows", 0x2190, 0x21FF),
    ("Mathematical Operators", 0x2200, 0x22FF),
    ("Miscellaneous Technical", 0x2300, 0x23FF),
    ("Enclosed Alphanumerics", 0x2460, 0x24FF),
    ("Box Drawing", 0x2500, 0x257F),
    ("Block Elements", 0x2580, 0x259F),
    ("Geometric Shapes", 0x25A0, 0x25FF),
    ("Miscellaneous Symbols", 0x2600, 0x26FF),
    ("Dingbats", 0x2700, 0x27BF),
    ("Braille Patterns", 0x2800, 0x28FF),
    ("CJK Symbols and Punctuation", 0x3000, 0x303F),
    ("Hiragana", 0x3040, 0x309F),
    ("Katakana", 0x30A0, 0x30FF),
    ("Bopomofo", 0x3100, 0x312F),
    ("Hangul Compatibility Jamo", 0x3130, 0x318F),
    ("Kanbun", 0x3190, 0x319F),
    ("Bopomofo Extended", 0x31A0, 0x31BF),
    ("CJK Strokes", 0x31C0, 0x31EF),
    ("Katakana Phonetic Extensions", 0x31F0, 0x31FF),
    ("Enclosed CJK Letters and Months", 0x3200, 0x32FF),
    ("CJK Compatibility", 0x3300, 0x33FF),
    ("Yijing Monogram/Diagram Symbols", 0x268A, 0x268B),
    ("Private Use Area-A", 0xF0000, 0xFFFFD),
    ("Private Use Area-B", 0x100000, 0x10FFFD),
]

CULTURAL_SYMBOL_RANGES = [
    ("Yiijing 64 Hexagrams", 0x4DC0, 0x4DFF),
    ("Bagua Trigrams", 0x2630, 0x2637),
    ("Taiji (Yin-Yang)", 0x262F, 0x262F),
    ("Liangyi (Monograms)", 0x268A, 0x268B),
]

PUA_ZONES = [
    ("BMP PUA", 0xE000, 0xF8FF),
    ("PUA-A", 0xF0000, 0xFFFFD),
    ("PUA-B", 0x100000, 0x10FFFD),
]


# ---------------------------------------------------------------------------
# PUA table parser
# ---------------------------------------------------------------------------
def parse_pua_table_sections(path: Path) -> List[Tuple[str, int, int]]:
    """Parse section headers like '## 五行、河图、洛书（U+E000 ~ U+E007）'."""
    sections: List[Tuple[str, int, int]] = []
    if not path.exists():
        return sections
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(r"##\s+(.+?)\s*[（(](U\+[0-9A-Fa-f]+)\s*[~～-]\s*(U\+[0-9A-Fa-f]+)[)）]", re.IGNORECASE)
    for match in pattern.finditer(text):
        title = match.group(1).strip()
        start = parse_codepoint(match.group(2))
        end = parse_codepoint(match.group(3))
        sections.append((title, start, end))
    return sections


def parse_pua_table_codepoints(path: Path) -> List[int]:
    """Return all U+XXXX codepoints explicitly mentioned in the PUA table."""
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    return sorted({parse_codepoint(m.group(0)) for m in re.finditer(r"U\+[0-9A-Fa-f]+", text)})


# ---------------------------------------------------------------------------
# Glyph library loader
# ---------------------------------------------------------------------------
def load_glyph_library(path: Path) -> Tuple[Dict, List[Tuple[str, Dict]]]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    glyph_dict = data.get("字符集_cnsh9622", data)
    glyphs = [(char, info) for char, info in glyph_dict.items()]
    return data, glyphs


def get_glyph_codepoint(info: Dict[str, Any]) -> int:
    raw = info.get("unicode", info.get("Unicode", ""))
    return parse_codepoint(raw)


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------
def analyze(glyphs: List[Tuple[str, Dict]]) -> Dict[str, Any]:
    total = len(glyphs)
    codepoints = []
    pua_by_structure: Counter = Counter()
    chinese_count = 0
    latin_digit_symbol_count = 0
    block_counts: Counter = Counter()
    cultural_counts: Dict[str, int] = {name: 0 for name, _, _ in CULTURAL_SYMBOL_RANGES}
    pua_used_codepoints: List[int] = []

    for char, info in glyphs:
        try:
            cp = get_glyph_codepoint(info)
        except Exception:
            continue
        codepoints.append(cp)

        # Chinese CJK Unified Ideographs (BMP)
        if 0x4E00 <= cp <= 0x9FFF:
            chinese_count += 1

        # Latin / digits / basic symbols
        if 0x0000 <= cp <= 0x00FF:
            latin_digit_symbol_count += 1

        # Unicode blocks
        for name, start, end in UNICODE_BLOCKS:
            if start <= cp <= end:
                block_counts[name] += 1

        # Cultural symbols
        for name, start, end in CULTURAL_SYMBOL_RANGES:
            if start <= cp <= end:
                cultural_counts[name] += 1

        # PUA
        is_pua = any(start <= cp <= end for _, start, end in PUA_ZONES)
        if is_pua:
            pua_used_codepoints.append(cp)
            structure = info.get("结构", info.get("structure", "未分类"))
            if not structure or structure == "None":
                structure = "未分类"
            pua_by_structure[structure] += 1

    return {
        "total": total,
        "codepoints": sorted(set(codepoints)),
        "chinese_count": chinese_count,
        "latin_digit_symbol_count": latin_digit_symbol_count,
        "block_counts": block_counts,
        "cultural_counts": cultural_counts,
        "pua_used_codepoints": sorted(set(pua_used_codepoints)),
        "pua_by_structure": pua_by_structure,
    }


# ---------------------------------------------------------------------------
# Range computation
# ---------------------------------------------------------------------------
def contiguous_ranges(codepoints: List[int]) -> List[Tuple[int, int]]:
    if not codepoints:
        return []
    ranges = []
    start = prev = codepoints[0]
    for cp in codepoints[1:]:
        if cp == prev + 1:
            prev = cp
        else:
            ranges.append((start, prev))
            start = prev = cp
    ranges.append((start, prev))
    return ranges


def compute_pua_usage_map(pua_used: List[int]) -> Tuple[List[Tuple[str, int, int]], List[Tuple[str, int, int]]]:
    """Return (used_ranges, free_ranges) per PUA zone."""
    used_by_zone: Dict[str, List[int]] = defaultdict(list)
    for cp in pua_used:
        for zone_name, start, end in PUA_ZONES:
            if start <= cp <= end:
                used_by_zone[zone_name].append(cp)
                break

    used_ranges: List[Tuple[str, int, int]] = []
    free_ranges: List[Tuple[str, int, int]] = []

    for zone_name, start, end in PUA_ZONES:
        zone_used = sorted(set(used_by_zone.get(zone_name, [])))
        used_ranges.extend((zone_name, s, e) for s, e in contiguous_ranges(zone_used))

        pos = start
        for s, e in contiguous_ranges(zone_used):
            if s > pos:
                free_ranges.append((zone_name, pos, s - 1))
            pos = e + 1
        if pos <= end:
            free_ranges.append((zone_name, pos, end))

    return used_ranges, free_ranges


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------
def render_table(headers: List[str], rows: List[List[str]]) -> str:
    if not rows:
        return ""
    col_widths = [max(len(headers[i]), max((len(row[i]) for row in rows), default=0)) for i in range(len(headers))]
    sep = "|" + "|".join("-" * (w + 2) for w in col_widths) + "|"
    header_line = "|" + "|".join(f" {headers[i]:^{col_widths[i]}} " for i in range(len(headers))) + "|"
    row_lines = [
        "|" + "|".join(f" {row[i]:^{col_widths[i]}} " for i in range(len(headers))) + "|"
        for row in rows
    ]
    return "\n".join([header_line, sep] + row_lines)


def generate_report(data: Dict[str, Any], glyphs: List[Tuple[str, Dict]], stats: Dict[str, Any], pua_sections: List[Tuple[str, int, int]]) -> str:
    library_dna = data.get("DNA追溯码", "未记录")
    total = stats["total"]
    chinese = stats["chinese_count"]
    latin = stats["latin_digit_symbol_count"]
    pua_used = stats["pua_used_codepoints"]
    pua_by_structure = stats["pua_by_structure"]
    block_counts = stats["block_counts"]
    cultural_counts = stats["cultural_counts"]

    pua_count = len(pua_used)
    other_count = total - chinese - latin - pua_count
    if other_count < 0:
        other_count = 0

    used_ranges, free_ranges = compute_pua_usage_map(pua_used)

    block_rows = []
    for name, _, _ in UNICODE_BLOCKS:
        count = block_counts.get(name, 0)
        if count > 0:
            block_rows.append([name, str(count), f"{count / total * 100:.2f}%"])

    cultural_rows = [[name, f"U+{start:04X} ~ U+{end:04X}", str(cultural_counts[name])] for name, start, end in CULTURAL_SYMBOL_RANGES]

    pua_structure_rows = [[structure, str(count), f"{count / pua_count * 100:.2f}%"] for structure, count in pua_by_structure.most_common()]

    used_range_rows = [[zone, f"U+{s:04X}", f"U+{e:04X}", str(e - s + 1)] for zone, s, e in used_ranges]
    free_range_rows = [[zone, f"U+{s:04X}", f"U+{e:04X}", str(e - s + 1)] for zone, s, e in free_ranges]

    # Cap free ranges table size for readability (list first 30)
    free_range_rows_display = free_range_rows[:30]
    if len(free_range_rows) > 30:
        free_range_rows_display.append(["…", "…", "…", f"还有 {len(free_range_rows) - 30} 个空闲段"])

    now = datetime.now().isoformat()

    lines = [
        "# 龍魂字体覆盖报告",
        "",
        f"**DNA追溯码**: `{DNA_CODE}`",
        "",
        f"**字元库 DNA**: `{library_dna}`",
        "",
        f"**生成时间**: {now}",
        "",
        "## 执行摘要",
        "",
        f"当前稳定版字元库共收录 **{total}** 个字元。",
        "",
        "- **CJK 统一表意文字**：{0} 字元（占比 {1:.2f}%）。".format(chinese, chinese / total * 100 if total else 0),
        "- **拉丁字母、数字与基础符号**：{0} 字元（占比 {1:.2f}%）。".format(latin, latin / total * 100 if total else 0),
        "- **PUA 私有区文化图标**：{0} 字元（占比 {1:.2f}%）。".format(pua_count, pua_count / total * 100 if total else 0),
        "- **其他标准 Unicode 字符**：{0} 字元。".format(other_count),
        "",
        "本报告覆盖常见 Unicode 区段统计、标准文化符号、PUA 编码表使用情况以及字体渲染示例。",
        "",
        "## 字符分类统计",
        "",
        render_table(
            ["类别", "数量", "占比"],
            [
                ["总计", str(total), "100.00%"],
                ["CJK 统一表意文字 (U+4E00~U+9FFF)", str(chinese), f"{chinese / total * 100:.2f}%"],
                ["拉丁字母、数字与基础符号 (U+0000~U+00FF)", str(latin), f"{latin / total * 100:.2f}%"],
                ["PUA 文化图标", str(pua_count), f"{pua_count / total * 100:.2f}%"],
                ["其他标准 Unicode 字符", str(other_count), f"{other_count / total * 100:.2f}%"],
            ],
        ),
        "",
        "## Unicode 区段覆盖",
        "",
        render_table(["Unicode 区段", "命中字元数", "占比"], block_rows),
        "",
        "## 标准 Unicode 文化符号",
        "",
        render_table(["文化符号", "Unicode 范围", "命中数量"], cultural_rows),
        "",
        "## PUA 图标按结构分类",
        "",
        render_table(["结构", "数量", "占 PUA 总数"], pua_structure_rows),
        "",
        "## PUA 编码表段落",
        "",
        render_table(
            ["段落", "起始", "结束", "容量"],
            [[title, f"U+{start:04X}", f"U+{end:04X}", str(end - start + 1)] for title, start, end in pua_sections],
        ),
        "",
        "## PUA 码位使用图",
        "",
        "### 已用区段",
        "",
        render_table(["PUA 区", "起始", "结束", "长度"], used_range_rows),
        "",
        "### 空闲区段",
        "",
        render_table(["PUA 区", "起始", "结束", "长度"], free_range_rows_display),
        "",
        "## 字体渲染示例",
        "",
        "以下文本使用 `LonghunFont` 字体族渲染，仅在本字体已安装的终端或浏览器中可见：",
        "",
        "```html",
        '<p style="font-family: \'LonghunFont\', \'Noto Serif CJK SC\', serif; font-size: 18px;">',
        "龍魂字体，承载中华文脉，通心译世界。",
        "Lónghún zìtǐ, chéngzài Zhōnghuá wénmài, tōngxīn yì shìjiè.",
        "Αα Ββ Γγ Δδ Εε Ζζ",
        "∑ ∏ ∫ √ ∞ ≈ ≠ ≤ ≥",
        "易有太极，是生两仪，两仪生四象，四象生八卦。",
        "</p>",
        "```",
        "",
        "> 注：PUA 区字符依赖字体安装；标准 Unicode 文化符号（如 ☰☷☯）在支持字体下可直接显示。",
        "",
        "## 关于算法生成 CJK 占位骨架的说明",
        "",
        "当前字元库中的大量 CJK 字形采用 **算法生成的占位骨架**（placeholder skeletons）。",
        "这些骨架依据笔画数、结构和风格参数自动生成基础笔画路径，用于快速扩充覆盖范围、",
        "验证排版与渲染管线，以及支撑早期字体构建。后续版本将逐步替换为人工精修或",
        "AI 辅助优化的最终轮廓，以达到印刷级质量。",
        "",
        "占位骨架的主要用途：",
        "",
        "1. 保证字体文件在目标字符集下可正常编译与打包。",
        "2. 为人工设计提供统一的网格、比例与笔画参数基准。",
        "3. 支持通心译（Tongxin Translation）与 CNSH 中文原生脚本的多语言混排验证。",
        "",
        "---",
        "",
        "*报告由 `generate_coverage_report.py` 自动生成，仅供内部审计使用。*",
    ]

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> int:
    glyph_library_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_GLYPH_LIBRARY
    if not glyph_library_path.exists():
        print(f"错误：字元库不存在: {glyph_library_path}", file=sys.stderr)
        return 1

    data, glyphs = load_glyph_library(glyph_library_path)
    stats = analyze(glyphs)
    pua_sections = parse_pua_table_sections(PUA_TABLE_PATH)

    report = generate_report(data, glyphs, stats, pua_sections)

    REPORT_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_OUTPUT_PATH.write_text(report, encoding="utf-8")

    print(f"龍魂字体覆盖报告已生成: {REPORT_OUTPUT_PATH}")
    print(f"  总字元数: {stats['total']}")
    print(f"  CJK 汉字: {stats['chinese_count']}")
    print(f"  拉丁/数字/基础符号: {stats['latin_digit_symbol_count']}")
    print(f"  PUA 图标: {len(stats['pua_used_codepoints'])}")
    print(f"  DNA: {DNA_CODE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
