# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂视频引擎 · 字幕生成器 v1.1
DNA: #龍芯⚡️2026-08-22-SUBTITLE-GEN-v1.1
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
设计原则: 字幕与语音严格对齐，不提前不滞后——基于字级时间戳
修复记录 v1.1: 字体 Source Han Sans CN→Heiti SC(macOS自带·否则字幕不显示)·ASS 文本标签转义
"""

from typing import List, Dict, Any
from pathlib import Path

class SubtitleGen:
    """
    生成 ASS 格式字幕（Advanced SubStation Alpha）
    ASS 支持每词/每句高亮效果，可外挂播放器使用
    """

    ASS_HEADER = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Heiti SC,52,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,1,0,0,0,100,100,2,0,1,3,1,2,160,160,80,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    @staticmethod
    def _ts(seconds: float) -> str:
        """秒 → ASS 时间格式 H:MM:SS.cc"""
        h  = int(seconds // 3600)
        m  = int((seconds % 3600) // 60)
        s  = int(seconds % 60)
        cs = int((seconds % 1) * 100)
        return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

    @staticmethod
    def _sanitize(text: str) -> str:
        """
        ASS 文本清洗：
          , → 全角（ASS 里逗号是字段分隔符）
          { } → 全角（ASS 里 {} 是样式标签）
          \\ → 字面
        """
        return (text.replace("\\", "＼")
                    .replace(",", "\uff0c")
                    .replace("{", "\uff5b")
                    .replace("}", "\uff5d"))

    @classmethod
    def generate_ass(cls, tts_results: List[Dict],
                     time_offsets: List[float],
                     output_path: str,
                     mode: str = "sentence") -> str:
        """
        生成 ASS 字幕文件
        time_offsets: 每个 Segment 在最终视频中的起始时间（秒）
        mode: "sentence"（按句）| "word"（按词，更报幕感）
        """
        lines = [cls.ASS_HEADER]
        for seg_result, t_offset in zip(tts_results, time_offsets):
            if mode == "word":
                for w in seg_result["words"]:
                    start = t_offset + w["start"]
                    end   = t_offset + w["end"]
                    text  = cls._sanitize(w["text"])
                    lines.append(
                        f"Dialogue: 0,{cls._ts(start)},{cls._ts(end)},"
                        f"Default,,0,0,0,,{text}"
                    )
            else:  # sentence
                start = t_offset
                end   = t_offset + seg_result["duration"]
                text  = cls._sanitize(seg_result["text"])
                lines.append(
                    f"Dialogue: 0,{cls._ts(start)},{cls._ts(end)},"
                    f"Default,,0,0,0,,{text}"
                )

        content = "\n".join(lines)
        Path(output_path).write_text(content, "utf-8")
        print(f"  📝 Subtitle saved → {output_path}")
        return output_path

    @staticmethod
    def render_subtitle_pngs(tts_results: List[Dict],
                             time_offsets: List[float],
                             output_dir: str,
                             mode: str = "sentence") -> List[str]:
        """
        为每个 Segment 渲染一句底部字幕透明 PNG（烧录用）
        本机 ffmpeg 无 libass/drawtext → 走 PIL 渲染 + overlay 方案
        同时保留 .ass 外挂文件（generate_ass）
        返回 PNG 路径列表（与 tts_results 一一对应）
        """
        from PIL import Image, ImageDraw, ImageFont
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        W, H = 1920, 1080
        try:
            font = ImageFont.truetype(
                "/System/Library/Fonts/STHeiti Medium.ttc", 52)
        except Exception:
            font = ImageFont.load_default()

        pngs = []
        for seg_result, _off in zip(tts_results, time_offsets):
            text = seg_result["text"]
            img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            # 按像素宽度换行
            lines, cur = [], ""
            for ch in text:
                if draw.textlength(cur + ch, font=font) > 1600 and cur:
                    lines.append(cur)
                    cur = ch
                else:
                    cur += ch
            lines.append(cur)
            line_h  = 60
            total_h = line_h * len(lines)
            max_l   = max(draw.textlength(l, font=font) for l in lines)
            x = (W - int(max_l)) // 2
            y = H - 160 - total_h
            for i, line in enumerate(lines):
                # 黑描边 + 白字（描边通过偏移绘制 4 个方向实现）
                for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2)):
                    draw.text((x + dx, y + i * line_h + dy), line,
                              font=font, fill=(0, 0, 0, 255))
                draw.text((x, y + i * line_h), line,
                          font=font, fill=(255, 255, 255, 255))
            sid  = seg_result["seg_id"]
            png  = str(out_dir / f"{sid}_sub.png")
            img.save(png)
            pngs.append(png)
        print(f"  🖼️  字幕 PNG ×{len(pngs)} → {out_dir}")
        return pngs
