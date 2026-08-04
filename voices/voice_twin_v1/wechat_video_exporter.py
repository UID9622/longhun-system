#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂真声 · 视频号/抖音导出器

功能：
- 把现有 9:16 竖屏视频重新烧录字幕，输出适合视频号/抖音发布的 MP4
- 自动注入 AIGC 元数据（UID9622-LONGHUN-DIGITAL-HUMAN）
- 可选替换为克隆/系统 TTS 音频

DNA: #龍芯⚡️2026-06-25-VOICE-TWIN-WECHAT-EXPORTER-v1.0
"""

import json
import re
import subprocess
from pathlib import Path
from typing import List, Optional

from moviepy import CompositeVideoClip, TextClip, VideoFileClip

ROOT = Path(__file__).resolve().parent


def pick_font() -> str:
    candidates = [
        "/Library/Fonts/NotoSansSC-VariableFont_wght.ttf",
        "/Library/Fonts/Arial Unicode.ttf",
    ]
    for c in candidates:
        if Path(c).exists():
            return c
    return "Arial"


def add_aigc_metadata(video: Path) -> Path:
    meta = {
        "Label": "1",
        "ContentProducer": "UID9622-LONGHUN-DIGITAL-HUMAN",
        "ProduceID": "LH9622-WECHAT-EXPORT",
        "ReservedCode1": ""
    }
    tmp = video.with_suffix(".tmp.mp4")
    cmd = [
        "ffmpeg", "-y", "-i", str(video),
        "-metadata", f'AIGC={json.dumps(meta)}',
        "-c", "copy", str(tmp)
    ]
    subprocess.run(cmd, check=True)
    tmp.replace(video)
    return video


def split_into_captions(text: str, max_chars: int = 18) -> List[str]:
    """把长句按标点切成适合竖屏显示的字幕。"""
    parts = [p.strip() for p in re.split(r"([，。！？；,!?;]\s*)", text) if p.strip()]
    captions = []
    buf = ""
    for p in parts:
        if len(buf) + len(p) > max_chars and buf:
            captions.append(buf)
            buf = p
        else:
            buf += p
    if buf:
        captions.append(buf)
    return captions


def export_wechat_video(
    input_video: Path,
    captions: List[str],
    output_video: Path,
    replace_audio: Optional[Path] = None,
    add_aigc: bool = True,
) -> Path:
    video = VideoFileClip(str(input_video))
    duration = video.duration
    segment = duration / len(captions) if captions else duration
    font = pick_font()

    text_clips = []
    for i, text in enumerate(captions):
        start = i * segment
        end = (i + 1) * segment
        txt = TextClip(
            font=font,
            text=text,
            font_size=48,
            color="white",
            stroke_color="black",
            stroke_width=3,
            method="caption",
            size=(int(video.w * 0.88), None),
            text_align="center",
            horizontal_align="center",
            vertical_align="center",
        )
        txt = txt.with_position(("center", "center")).with_start(start).with_duration(end - start)
        text_clips.append(txt)

    composite = CompositeVideoClip([video] + text_clips, size=video.size)
    if replace_audio:
        audio = VideoFileClip(str(replace_audio)).audio
        composite = composite.with_audio(audio)
    else:
        composite = composite.with_audio(video.audio)

    composite.write_videofile(
        str(output_video),
        fps=video.fps,
        codec="libx264",
        audio_codec="aac",
        temp_audiofile=str(output_video.with_suffix(".m4a")),
        remove_temp=True,
        threads=4,
    )

    video.close()
    composite.close()

    if add_aigc:
        add_aigc_metadata(output_video)
    return output_video


def main():
    import argparse
    import re
    parser = argparse.ArgumentParser(description="龍魂视频号/抖音导出器")
    parser.add_argument("video", help="输入视频路径")
    parser.add_argument("--captions", required=True, help="字幕文本，用 | 分隔；或用 --auto-captions 自动切分")
    parser.add_argument("--auto-captions", action="store_true", help="自动按标点切分字幕")
    parser.add_argument("--audio", help="替换音频路径（TTS 生成音频，可选）")
    parser.add_argument("--out", help="输出路径")
    parser.add_argument("--no-aigc", action="store_true", help="不注入 AIGC 元数据")
    args = parser.parse_args()

    input_video = Path(args.video)
    if args.auto_captions:
        captions = split_into_captions(args.captions)
    else:
        captions = [c.strip() for c in args.captions.split("|") if c.strip()]

    output_video = Path(args.out) if args.out else input_video.with_stem(input_video.stem + "_wechat_export")

    print(f"🎬 正在导出视频号/抖音视频: {input_video}")
    print(f"   字幕共 {len(captions)} 句")

    export_wechat_video(
        input_video, captions, output_video,
        Path(args.audio) if args.audio else None,
        add_aigc=not args.no_aigc,
    )
    print(f"✅ 输出: {output_video}")


if __name__ == "__main__":
    main()
