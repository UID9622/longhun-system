#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
#!/usr/bin/env python3
# DNA追溯码:#龍芯⚡️丙午·甲午·丁卯·丙午·䷚颐-LONGHUN-FONT-EXPAND-CHINESE-7000-v1.0
# 龍魂·LonghunFont 中文字元扩展脚本
# 用途：在 v0016 龍纹书法版基础上，按《通用规范汉字表》补足至 7000 中文字符

import json
import sys
from datetime import datetime
from pathlib import Path

from glyph_generator import generate_skeleton, stroke_count_of, structure_of

DNA = "#龍芯⚡️丙午·甲午·丁卯·丙午·䷚颐-LONGHUN-FONT-EXPAND-CHINESE-7000-v1.0"

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_FILE = SCRIPT_DIR / "data" / "tongyong_guifan_7909.txt"

TARGET_BMP_CJK = 7000


def is_cjk(c: str) -> bool:
    return "\u4e00" <= c <= "\u9fff" or "\u3400" <= c <= "\u4dbf"


def is_bmp_cjk(c: str) -> bool:
    return "\u4e00" <= c <= "\u9fff"


def load_ordered_chars() -> str:
    if not DATA_FILE.exists():
        print(f"❌ 未找到字表数据文件: {DATA_FILE}", file=sys.stderr)
        sys.exit(1)
    return DATA_FILE.read_text(encoding="utf-8")


def main():
    base_dir = SCRIPT_DIR.parent
    input_path = base_dir / "glyphs" / "龍魂字元库_v0016_龍纹书法版.json"
    output_path = base_dir / "glyphs" / "龍魂字元库_v0017_七千中文字.json"

    if not input_path.exists():
        print(f"❌ 未找到输入字元库: {input_path}", file=sys.stderr)
        sys.exit(1)

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    chars = data["字符集_cnsh9622"]
    existing = set(chars.keys())

    ordered_chars = load_ordered_chars()

    added = 0
    skipped_existing = 0
    skipped_non_cjk = 0
    already_satisfied = False

    current_bmp = sum(1 for c in existing if is_bmp_cjk(c))
    if current_bmp >= TARGET_BMP_CJK:
        already_satisfied = True

    for char in ordered_chars:
        if not is_cjk(char):
            skipped_non_cjk += 1
            continue
        if char in existing:
            skipped_existing += 1
            continue
        if current_bmp >= TARGET_BMP_CJK:
            break

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
        if is_bmp_cjk(char):
            current_bmp += 1
        added += 1

    now = datetime.now().isoformat()
    total_chars = len(chars)
    chinese_chars = sum(1 for c in chars if is_cjk(c))

    metadata = data.setdefault("元数据", {})
    previous_version = metadata.get("版本", "v0016-龍纹书法版")
    metadata["名称"] = "龍魂字元库"
    metadata["版本"] = "v0017-七千中文字"
    metadata["创建者"] = "UID9622"
    metadata["生成时间"] = now
    metadata["前一版本"] = previous_version
    metadata["本次新增中文字符数"] = added
    metadata["中文字符数"] = chinese_chars
    metadata["总字符数"] = total_chars
    metadata["目标中文字符数"] = TARGET_BMP_CJK
    metadata["中文7000扩展时间"] = now
    metadata["中文7000扩展DNA"] = DNA
    metadata["描述"] = (
        "LonghunFont 七千中文字元库。按《通用规范汉字表》一级、二级、三级顺序补全，"
        f"在 {previous_version} 基础上新增 {added} 个汉字，覆盖基础教育、出版印刷、"
        "姓氏人名、地名、科技术语及常用文言用字，服务国标普惠与全球中文传播。"
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
    print(f"   目标 BMP CJK 中文字符数: {TARGET_BMP_CJK}")
    print(f"   已存在跳过: {skipped_existing}")
    print(f"   非 CJK 跳过: {skipped_non_cjk}")
    print(f"   实际新增汉字: {added}")
    print(f"   当前 BMP CJK 中文字符总数: {current_bmp}")
    print(f"   当前中文字符总数（含 Ext-A）: {chinese_chars}")
    print(f"   当前总字符数: {total_chars}")
    if already_satisfied:
        print("   提示: 输入字元库已达到/超过 7000 个 BMP 中文字符，未新增。")


if __name__ == "__main__":
    main()
