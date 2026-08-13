#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙酉·壬戌·戌时·䷬萃-AVS3_ENCODER-UID9622-161D9F9B
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""龍魂·AVS3视频编码器 v1.0 — 中国自主知识产权视频编码标准
uavs3e 开源实现，北大深圳研究生院+鹏城实验室+广东博华
BSD 4-clause · 支持8K超高清"""

import sys, os, subprocess

ENCODER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uavs3enc')

def run():
    args = sys.argv[1:]
    if not args or '-h' in args or '--help' in args:
        print("龍魂·AVS3编码器 (uavs3e)")
        print("  中国自主知识产权 AVS3 视频编码标准开源实现")
        print("  用法: lh avs3enc -i input.yuv -w 1920 -h 1080 -o output.avs3")
        print("  或直接: uavs3enc -i input.yuv -w 1920 -h 1080 -o output.avs3")
        print()
    if not os.path.exists(ENCODER):
        print(f"❌ 编码器未找到: {ENCODER}", file=sys.stderr)
        sys.exit(1)
    result = subprocess.run([ENCODER] + args)
    sys.exit(result.returncode)

if __name__ == '__main__':
    run()
