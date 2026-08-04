#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·比-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# DNA追溯码:#龍芯⚡️2026-06-22-LONGHUN-FONT-SUBSET-v1.0

"""
LonghunFont 字体子集生成器 v1.0
根据文本/字符列表从稳定字元库中提取子集，并生成子集 OTF 字体。
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

DNA = "#龍芯⚡️2026-06-22-LONGHUN-FONT-SUBSET-v1.0"

# 尝试复用 build_font.py 的 build_otf 函数；失败时退化为子进程调用
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))
try:
    from build_font import build_otf as _build_otf

    HAS_BUILD_OTF_IMPORT = True
except Exception:
    HAS_BUILD_OTF_IMPORT = False


def load_glyph_library(path: str) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def collect_wanted_chars(args) -> set[str]:
    wanted = set()

    if args.text:
        wanted.update(args.text)

    if args.text_file:
        with open(args.text_file, "r", encoding="utf-8") as f:
            for line in f:
                wanted.update(line)

    if args.chars:
        wanted.update(args.chars)

    if args.add_ascii:
        # U+0020 ~ U+007E（Basic Latin 可打印字符，含空格）
        for code in range(0x20, 0x7F):
            wanted.add(chr(code))

    return wanted


def build_subset_library(full_data: dict[str, Any], wanted: set[str]) -> dict[str, Any]:
    full_chars = full_data.get("字符集_cnsh9622", {})
    subset_chars = {}
    missing = set()

    for char in wanted:
        if char in full_chars:
            subset_chars[char] = full_chars[char]
        else:
            missing.add(char)

    # 深拷贝元数据并更新子集相关信息
    metadata = json.loads(json.dumps(full_data.get("元数据", {})))
    metadata["版本"] = f"{metadata.get('版本', 'unknown')}-subset"
    metadata["总字符数"] = len(subset_chars)
    metadata["子集生成时间"] = datetime.utcnow().isoformat() + "+00:00"
    metadata["子集DNA"] = DNA
    metadata["前一版本"] = metadata.get("版本", "unknown")
    if "中文字符数" in metadata:
        metadata["中文字符数"] = sum(
            1 for c in subset_chars if 0x4E00 <= ord(c) <= 0x9FFF
        )

    subset_data = {
        "DNA追溯码": DNA,
        "元数据": metadata,
        "三色审计_cnsh9622": full_data.get("三色审计_cnsh9622", {}),
        "字符集_cnsh9622": subset_chars,
    }
    return subset_data, missing


def write_json(data: dict[str, Any], output_path: str) -> str:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return output_path


def generate_otf(json_path: str, otf_path: str) -> str:
    if HAS_BUILD_OTF_IMPORT:
        return _build_otf(json_path, otf_path)

    # 退化为子进程调用，兼容当前 Python 解释器
    build_script = SCRIPT_DIR / "build_font.py"
    result = subprocess.run(
        [sys.executable, str(build_script), json_path, otf_path],
        cwd=str(PROJECT_DIR),
        capture_output=True,
        text=True,
    )
    sys.stdout.write(result.stdout)
    sys.stderr.write(result.stderr)
    if result.returncode != 0:
        raise RuntimeError(f"build_font.py 子进程返回非零退出码: {result.returncode}")
    return otf_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="从龍魂字元库生成字体子集（JSON + OTF）"
    )
    parser.add_argument(
        "--glyphs",
        default="glyphs/龍魂字元库_v0013_稳定版.json",
        help="完整字元库 JSON 路径（默认: glyphs/龍魂字元库_v0013_稳定版.json）",
    )
    parser.add_argument("--text", default="", help="要包含的字符文本串")
    parser.add_argument("--text-file", help="包含目标字符的文本文件路径")
    parser.add_argument("--chars", default="", help="显式指定的字符列表")
    parser.add_argument("--output-json", required=True, help="子集字元库输出路径")
    parser.add_argument("--output-otf", required=True, help="子集 OTF 输出路径")
    parser.add_argument(
        "--add-ascii",
        action="store_true",
        help="额外包含 ASCII 可打印字符（U+0020~U+007E）",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    glyph_path = Path(args.glyphs)
    if not glyph_path.is_absolute():
        glyph_path = PROJECT_DIR / glyph_path

    output_json = Path(args.output_json)
    if not output_json.is_absolute():
        output_json = PROJECT_DIR / output_json

    output_otf = Path(args.output_otf)
    if not output_otf.is_absolute():
        output_otf = PROJECT_DIR / output_otf

    full_data = load_glyph_library(str(glyph_path))
    full_chars = full_data.get("字符集_cnsh9622", {})

    wanted = collect_wanted_chars(args)
    subset_data, missing = build_subset_library(full_data, wanted)

    write_json(subset_data, str(output_json))
    generate_otf(str(output_json), str(output_otf))

    print("\n" + "=" * 60)
    print("龍魂字体子集生成完成")
    print("=" * 60)
    print(f"输入字元库 : {glyph_path}")
    print(f"输入字形数 : {len(full_chars)}")
    print(f"请求字符数 : {len(wanted)}")
    print(f"命中字符数 : {len(subset_data['字符集_cnsh9622'])}")
    print(f"缺失字符数 : {len(missing)}")
    if missing:
        sample = "".join(sorted(missing)[:20])
        print(f"缺失字符样例: {sample}{'...' if len(missing) > 20 else ''}")
    print(f"子集 JSON  : {output_json}")
    print(f"子集 OTF   : {output_otf}")
    print(f"DNA 追溯码 : {DNA}")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
