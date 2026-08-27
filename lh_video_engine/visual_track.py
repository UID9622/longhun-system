#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂视频引擎 · 画面轨道 v1.2
DNA: #龍芯⚡️2026-08-22-VISUAL-TRACK-v1.2
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
设计原则:
  - 截图类: macOS screencapture 命令→稳定处理→将图转为视频片段
  - 生成类: 插件接口（对接 SD/Flux/ComfyUI）
  - 标题类: 渲染文字为透明 PNG → overlay 叠底（不依赖 drawtext）
修复记录:
  v1.2: 本机 ffmpeg 无 libfreetype(drawtext 不可用)·改 PIL 渲染透明 PNG + ffmpeg overlay
        文字渲染质量更高·截图失败占位兜底
"""

import subprocess, re
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple

class VisualTrack:
    """
    画面轨道管理器
    将 Segment 的 visual_type 转换为实际视频片段（MP4/MOV）
    """

    # 输出规格
    WIDTH    = 1920
    HEIGHT   = 1080
    FPS      = 30
    BG_COLOR = "0x0a0a1a"  # 深蓝黑背景
    # macOS 自带中文字体（PingFang 不在此路径·实测 STHeiti 存在）
    FONT = "/System/Library/Fonts/STHeiti Medium.ttc"

    def __init__(self, frames_dir: str, videos_dir: str):
        self.frames_dir = Path(frames_dir)
        self.videos_dir = Path(videos_dir)
        self.frames_dir.mkdir(parents=True, exist_ok=True)
        self.videos_dir.mkdir(parents=True, exist_ok=True)

    # ----------------------------------------------------------------
    # 文字渲染（PIL → 透明 PNG）
    # ----------------------------------------------------------------

    @staticmethod
    def _render_text_png(text: str, out_path: str, font_size: int = 72,
                         fill: Tuple[int, int, int, int] = (255, 255, 255, 255),
                         position: str = "center",
                         y_offset: int = 0,
                         max_width: int = 1600) -> str:
        """
        用 PIL 将文字渲染为透明 PNG（中文字体 STHeiti）
        自动按像素宽度换行·支持 居中/左对齐
        返回 PNG 路径
        """
        from PIL import Image, ImageDraw, ImageFont
        img = Image.new("RGBA", (VisualTrack.WIDTH, VisualTrack.HEIGHT),
                        (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype(VisualTrack.FONT, font_size)
        except Exception:
            font = ImageFont.load_default()

        # 按像素宽度换行
        lines, cur = [], ""
        for ch in text:
            if draw.textlength(cur + ch, font=font) > max_width and cur:
                lines.append(cur)
                cur = ch
            else:
                cur += ch
        lines.append(cur)

        line_h   = font_size + 8
        total_h  = line_h * len(lines)
        max_line = max(draw.textlength(l, font=font) for l in lines)

        if position == "center":
            x = (VisualTrack.WIDTH - int(max_line)) // 2
        else:  # left
            x = 100
        y = (VisualTrack.HEIGHT - total_h) // 2 + y_offset

        for i, line in enumerate(lines):
            draw.text((x, y + i * line_h), line, font=font, fill=fill)
        img.save(out_path)
        return out_path

    def _overlay_png(self, bg_color: str, png_path: str, duration: float,
                     out: str, x_expr: str = "(W-w)/2",
                     y_expr: str = "(H-h)/2") -> str:
        """
        纯色背景 + 透明 PNG 文字 overlay → H264 视频
        （本机 ffmpeg 无 drawtext·overlay 是内置滤镜）
        """
        subprocess.run([
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", f"color=c={bg_color}:s={self.WIDTH}x{self.HEIGHT}:r={self.FPS}:d={duration}",
            "-loop", "1", "-i", png_path,
            "-filter_complex",
            f"[0:v][1:v]overlay={x_expr}:{y_expr}:format=auto[v]",
            "-map", "[v]",
            "-t", str(duration),
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-r", str(self.FPS), out
        ], check=True, capture_output=True)
        return out

    def _fallback_frame(self, seg_id: str, duration: float) -> str:
        """截图失败时的占位帧（纯色 + 提示文字）"""
        out   = str(self.videos_dir / f"{seg_id}_visual.mp4")
        png   = str(self.frames_dir / f"{seg_id}_fallback.png")
        self._render_text_png("[截图不可用]", png, font_size=48)
        return self._overlay_png(self.BG_COLOR, png, duration, out)

    # ----------------------------------------------------------------
    # A. 截图类
    # ----------------------------------------------------------------

    def capture_screenshot(self, target: str = "terminal") -> str:
        """macOS screencapture 采集截图（需屏幕录制权限·失败返回空走兜底）"""
        ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = str(self.frames_dir / f"shot_{target}_{ts}.png")
        try:
            subprocess.run(["screencapture", "-x", path], check=True,
                           capture_output=True, timeout=10)
            if Path(path).exists() and Path(path).stat().st_size > 0:
                return path
        except Exception:
            pass
        return ""

    def screenshot_to_video(self, image_path: str, duration: float,
                            seg_id: str) -> str:
        """
        将截图转为指定时长的视频片段
        加轻度缩放（缓推动效，小于 1.05x）避免屏幂感
        """
        out = str(self.videos_dir / f"{seg_id}_visual.mp4")
        end_scale = 1.03
        subprocess.run([
            "ffmpeg", "-y",
            "-loop", "1", "-i", image_path,
            "-vf",
            f"scale={self.WIDTH}:{self.HEIGHT}:force_original_aspect_ratio=decrease,"
            f"pad={self.WIDTH}:{self.HEIGHT}:(ow-iw)/2:(oh-ih)/2:{self.BG_COLOR},"
            f"zoompan=z='min(zoom+0.0003,{end_scale})':d={int(duration*self.FPS)}:s={self.WIDTH}x{self.HEIGHT}",
            "-t", str(duration),
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-r", str(self.FPS), out
        ], check=True, capture_output=True)
        return out

    # ----------------------------------------------------------------
    # B. 标题类
    # ----------------------------------------------------------------

    def make_title_frame(self, text: str, duration: float, seg_id: str) -> str:
        """标题帧：深色背景 + 白色大字（居中）"""
        out = str(self.videos_dir / f"{seg_id}_visual.mp4")
        png = str(self.frames_dir / f"{seg_id}_title.png")
        self._render_text_png(text, png, font_size=80)
        return self._overlay_png(self.BG_COLOR, png, duration, out)

    # ----------------------------------------------------------------
    # C. 生成类接口（预留，对接 SD/Flux）
    # ----------------------------------------------------------------

    def generated_scene_placeholder(self, seg_id: str, prompt: str,
                                    duration: float,
                                    char_config: Optional[Dict] = None) -> str:
        """
        生成式场景占位符——实际项目替换为 SD/Flux/ComfyUI 调用
        当前输出占位背景 + 提示词叠加（左侧青色小字）
        """
        out = str(self.videos_dir / f"{seg_id}_visual.mp4")
        png = str(self.frames_dir / f"{seg_id}_gen.png")
        note = f"[GENERATED] {prompt[:80]}"
        self._render_text_png(note, png, font_size=36,
                              fill=(0, 255, 255, 255), position="left")
        return self._overlay_png("0x111122", png, duration, out,
                                 x_expr="100", y_expr="(H-h)/2")

    # ----------------------------------------------------------------
    # D. 统一入口
    # ----------------------------------------------------------------

    def process_segment(self, seg: Dict[str, Any],
                        tts_result: Dict[str, Any],
                        char_config: Optional[Dict] = None) -> str:
        """
        根据 Segment 类型自动路由到正确的画面生成方式
        返回视频片段路径
        """
        sid      = seg["id"]
        vtype    = seg["visual_type"]
        duration = tts_result["duration"]

        if vtype == "screenshot":
            target = seg.get("visual_target", "terminal")
            print(f"  📷 Screenshot [{target}]: {sid}")
            img = self.capture_screenshot(target)
            if img:
                return self.screenshot_to_video(img, duration, sid)
            print(f"     ⚠️ 截图不可用（需屏幕录制权限）→ 占位帧: {sid}")
            return self._fallback_frame(sid, duration)

        elif vtype == "title":
            print(f"  🎨 Title frame: {sid}")
            return self.make_title_frame(seg["text"], duration, sid)

        elif vtype == "character":
            # 角色画面——如有口型同步，下一步 LipSync 模块会覆盖此输出
            print(f"  👤 Character [{seg.get('character')}]: {sid}")
            if char_config:
                return self.generated_scene_placeholder(
                    sid, char_config.get("prompt", ""), duration, char_config)
            return self.generated_scene_placeholder(sid, seg["text"], duration)

        else:  # generated
            print(f"  ✨ Generated scene: {sid}")
            prompt = seg.get("scene_prompt", seg["text"])
            return self.generated_scene_placeholder(sid, prompt, duration)
