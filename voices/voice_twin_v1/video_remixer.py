#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂真声 · 视频字幕重混器
给现有 9:16 竖屏视频重新烧录字幕，并可选替换/保留音频。

DNA: #龍芯⚡️2026-06-25-VOICE-TWIN-VIDEO-REMIXER-v1.0
"""

import json
import subprocess
from pathlib import Path
from typing import List, Optional

from moviepy import CompositeVideoClip, TextClip, VideoFileClip

ROOT = Path(__file__).resolve().parent


def pick_font() -> str:
    # 优先用有完整中文支持的字体，CNSH 字体兜底
    candidates = [
        "/Library/Fonts/NotoSansSC-VariableFont_wght.ttf",
        "/Library/Fonts/Arial Unicode.ttf",
        "/Library/Fonts/cnsh_uid9622_v1.ttf",
    ]
    for c in candidates:
        if Path(c).exists():
            return c
    return "Arial"


def add_captions_to_video(
    input_video: Path,
    captions: List[str],
    output_video: Path,
    replace_audio: Optional[Path] = None,
) -> Path:
    """
    给视频烧录字幕。如果 replace_audio 提供，则替换原视频音频。
    """
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
            font_size=42,
            color="white",
            stroke_color="black",
            stroke_width=2,
            method="caption",
            size=(int(video.w * 0.9), None),
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
    return output_video


def add_aigc_metadata(video: Path) -> Path:
    """
    给输出视频写入 AIGC 元数据标记（抖音/视频号可识别）。
    """
    meta = {
        "Label": "1",
        "ContentProducer": "UID9622-LONGHUN-DIGITAL-HUMAN",
        "ProduceID": "LH9622-REMIX",
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


def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂视频字幕重混器")
    parser.add_argument("video", help="输入视频路径")
    parser.add_argument("--captions", required=True, help="字幕文本，用 | 分隔多句")
    parser.add_argument("--audio", help="替换音频路径（可选）")
    parser.add_argument("--out", help="输出路径")
    parser.add_argument("--aigc", action="store_true", help="添加 AIGC 元数据标记")
    args = parser.parse_args()

    input_video = Path(args.video)
    captions = [c.strip() for c in args.captions.split("|") if c.strip()]
    output_video = Path(args.out) if args.out else input_video.with_stem(input_video.stem + "_remixed")

    print(f"🎬 正在重混视频: {input_video}")
    print(f"   字幕共 {len(captions)} 句")

    add_captions_to_video(
        input_video, captions, output_video,
        Path(args.audio) if args.audio else None
    )

    if args.aigc:
        add_aigc_metadata(output_video)
        print("   已添加 AIGC 标记")

    print(f"✅ 输出: {output_video}")


if __name__ == "__main__":
    main()
