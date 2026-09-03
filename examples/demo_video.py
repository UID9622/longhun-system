#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-09-01-DEMO-VIDEO-v1.0-MEDIA-SENSE
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
🎬 龍魂视频引擎 demo — 帧动画 / 图文转视频 / 片头片尾模板
用法: python3 examples/demo_video.py
输出: examples/output/video/ (mp4 + gpg 签名 sidecar)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "08_BIN"))
from lh_video import cmd_video

OUT = Path(__file__).resolve().parent / "output" / "video"
OUT.mkdir(parents=True, exist_ok=True)


def main():
    print("🎬 龍魂视频引擎 demo")
    # 文本 → 片头+内容+片尾
    p = cmd_video("龍魂系统，为人民服务。感官层全面补全，视觉声音视频一网打尽。",
                  template="intro", fmt="mp4", out=str(OUT / "demo_text.mp4"))
    print(f"  ✅ 文本模板视频 → {p}")
    # 图片序列 → 转视频（生成示例帧）
    from PIL import Image
    frame_dir = OUT / "frames"
    frame_dir.mkdir(exist_ok=True)
    for i, color in enumerate([(212, 175, 55), (46, 139, 87), (30, 144, 255)]):
        img = Image.new("RGB", (640, 360), color)
        img.save(frame_dir / f"demo_frame_{i}.png")
    p = cmd_video(str(frame_dir), fmt="webm", out=str(OUT / "demo_frames.webm"))
    print(f"  ✅ 图片序列转视频 → {p}")
    print(f"📁 输出目录: {OUT}")


if __name__ == "__main__":
    main()
