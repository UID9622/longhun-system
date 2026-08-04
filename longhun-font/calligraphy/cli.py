#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# #龍芯⚡️20260624010825157-AUTO-DNA-99C72831 自动注入·分层治理自愈引擎 · 来源可查
#!/usr/bin/env python3
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# DNA追溯码:#龍芯⚡️2026-06-23-LONGHUN-FONT-CALLIGRAPHY-CLI-v1.0
"""
书法渲染命令行入口

用法：
    python3 -m calligraphy.cli --text "自强不息" --style YZQ-KA --seal 龍魂 --classic YIJING
    python3 -m calligraphy.cli --list
"""

import argparse
import sys
from pathlib import Path

# 支持直接运行脚本时把项目根目录加入路径
ROOT = Path(__file__).parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from calligraphy import render, list_styles

DNA = "#龍芯⚡️2026-06-23-LONGHUN-FONT-CALLIGRAPHY-CLI-v1.0"


def main():
    parser = argparse.ArgumentParser(description="LonghunFont 书法渲染器")
    parser.add_argument("--text", "-t", help="要渲染的文字")
    parser.add_argument("--style", "-s", default="YZQ-KA", help="书法样式代码，默认 YZQ-KA")
    parser.add_argument("--layout", "-l", default="horizontal", choices=["horizontal", "vertical"], help="排版方向")
    parser.add_argument("--seal", help="印章文字")
    parser.add_argument("--classic", "-c", default="GENERAL", help="典籍代码，如 YIJING/DAODEJING/HUANGDI")
    parser.add_argument("--output", "-o", help="输出文件名（不含扩展名）")
    parser.add_argument("--width", type=int, help="画布宽度")
    parser.add_argument("--height", type=int, help="画布高度")
    parser.add_argument("--list", action="store_true", help="列出所有可用样式")

    args = parser.parse_args()

    if not args.list and not args.text:
        parser.error("--text 是必需的（使用 --list 时可省略）")

    if args.list:
        print("可用书法样式：")
        for st in list_styles():
            print(f"  {st['code']:12s} {st['name']:20s} {st['category']:6s} {st['era']}")
        return

    size = None
    if args.width and args.height:
        size = (args.width, args.height)

    result = render(
        text=args.text,
        style_code=args.style,
        layout=args.layout,
        seal_text=args.seal,
        classic=args.classic,
        output_name=args.output,
        size=size,
    )

    print("✅ 书法作品渲染完成")
    print(f"   编号: {result['work_id']}")
    print(f"   样式: {result['style']}")
    print(f"   文件: {result['output']}")
    print(f"   尺寸: {result['size'][0]}x{result['size'][1]}")
    print(f"   DNA: {DNA}")


if __name__ == "__main__":
    main()
