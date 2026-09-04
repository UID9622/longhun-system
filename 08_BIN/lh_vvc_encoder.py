#!/usr/bin/env python3
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# DNA: #龍芯⚡️丙午·丙酉·壬戌·戌时·䷬萃-VVC_ENCODER-UID9622-C16961E4
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""龍魂·VVC视频编码器 v1.0 — H.266/VVC Fraunhofer开源实现
vvencapp 1.15.0 · 比HEVC省50%码率"""

import sys, os, subprocess

ENCODER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vvencapp')

def run():
    args = sys.argv[1:]
    if not args or '-h' in args or '--help' in args:
        print("龍魂·VVC编码器 (vvencapp 1.15.0)")
        print("  H.266/VVC 开源编码器 — 比H.265省50%码率")
        print("  用法: lh vvcenc -i input.yuv -s 1920x1080 --fps 30 -o output.vvc")
        print("  或直接: vvencapp -i input.yuv -s 1920x1080 --fps 30 -o output.vvc")
        print()
    if not os.path.exists(ENCODER):
        print(f"❌ 编码器未找到: {ENCODER}", file=sys.stderr)
        sys.exit(1)
    result = subprocess.run([ENCODER] + args)
    sys.exit(result.returncode)

if __name__ == '__main__':
    run()
