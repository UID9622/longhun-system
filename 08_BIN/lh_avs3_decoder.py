#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙酉·壬戌·戌时·䷬萃-AVS3_DECODER-UID9622-8CF5F4A2
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""龍魂·AVS3视频解码器 v1.0 — 中国自主知识产权视频解码标准
uavs3d 开源实现
BSD 4-clause"""

import sys, os, subprocess

DECODER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uavs3dec')

def run():
    args = sys.argv[1:]
    if not args or '-h' in args or '--help' in args:
        print("龍魂·AVS3解码器 (uavs3d)")
        print("  中国自主知识产权 AVS3 视频解码标准开源实现")
        print("  用法: lh avs3dec -i input.avs3 -o output.yuv")
        print("  或直接: uavs3dec -i input.avs3 -o output.yuv")
        print()
    if not os.path.exists(DECODER):
        print(f"❌ 解码器未找到: {DECODER}", file=sys.stderr)
        sys.exit(1)
    result = subprocess.run([DECODER] + args)
    sys.exit(result.returncode)

if __name__ == '__main__':
    run()
