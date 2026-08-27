#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂视频引擎 · 时间轴合成器 v1.1
DNA: #龍芯⚡️2026-08-22-TIMELINE-COMPOSER-v1.1
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
设计原则:
  - 画面切换点落在句尾
  - 口型片段时长 = 对应语音时长
  - 字幕按词对齐，不提前不滞后
  - 全程只用 ffmpeg，零外部依赖
修复记录 v1.1: 空列表保护·ass= 路径 : 转义
"""

import subprocess, json, os
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

class TimelineComposer:
    """
    最终合成器: 将所有轨道锁在一起
    输入: TTS 结果 + 画面片段 + 口型视频 + ASS 字幕
    输出: 音画同步·字幕对齐·不动点角色的最终 MP4
    """

    def __init__(self, output_dir: str):
        self.out = Path(output_dir)
        self.out.mkdir(parents=True, exist_ok=True)

    def _concat_video_segments(self, video_paths: List[str],
                                concat_list: str) -> str:
        """生成 ffmpeg concat 文件并拼接"""
        with open(concat_list, "w", encoding="utf-8") as f:
            for vp in video_paths:
                f.write(f"file '{vp}'\n")
        merged = str(self.out / "_merged_video.mp4")
        subprocess.run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", concat_list,
            "-c:v", "libx264", "-pix_fmt", "yuv420p", merged
        ], check=True, capture_output=True)
        return merged

    def _concat_audio_segments(self, audio_paths: List[str],
                                concat_list: str) -> str:
        """拼接所有语音片段"""
        with open(concat_list, "w", encoding="utf-8") as f:
            for ap in audio_paths:
                f.write(f"file '{ap}'\n")
        merged = str(self.out / "_merged_audio.wav")
        subprocess.run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", concat_list,
            "-c:a", "pcm_s16le", merged
        ], check=True, capture_output=True)
        return merged

    def compose(self,
                tts_results:    List[Dict],
                visual_videos:  List[str],
                subtitle_images: List[str],
                time_offsets:   List[float],
                output_name:    str = "final_output") -> str:
        """
        主合成入口
        1. 拼接所有画面片段
        2. 拼接所有语音片段
        3. 合成：画面 + 语音 + 字幕(PNG overlay) → 最终 MP4
        说明: 本机 ffmpeg 无 libass/drawtext → 字幕用透明 PNG + overlay enable 链烧录
        """
        print("\n🎬 开始合成...")

        if not tts_results or not visual_videos:
            raise ValueError("合成失败: tts_results / visual_videos 为空")
        if len(subtitle_images) != len(tts_results):
            raise ValueError("字幕 PNG 数量与镜头数不一致")

        tmp      = self.out / "_tmp"
        tmp.mkdir(exist_ok=True)
        v_concat = str(tmp / "vlist.txt")
        a_concat = str(tmp / "alist.txt")

        audio_paths = [r["audio"] for r in tts_results]

        print("  🔗 拼接画面...")
        merged_video = self._concat_video_segments(visual_videos, v_concat)
        print("  🔗 拼接语音...")
        merged_audio = self._concat_audio_segments(audio_paths, a_concat)

        total = sum(r["duration"] for r in tts_results)

        # 字幕 PNG → overlay enable 链（每句在对应时间窗口显示）
        # 输入: 0=画面 1=音频 2..N=字幕PNG(循环)
        cmd = ["ffmpeg", "-y", "-i", merged_video, "-i", merged_audio]
        for png in subtitle_images:
            cmd += ["-loop", "1", "-t", f"{total:.3f}", "-i", png]

        fc_parts, prev = [], "[0:v]"
        for i, (r, off) in enumerate(zip(tts_results, time_offsets)):
            start, end = off, off + r["duration"]
            out_tag = "[vout]" if i == len(tts_results) - 1 else f"[v{i}]"
            fc_parts.append(
                f"{prev}[{i+2}:v]overlay=0:0:"
                f"enable='between(t,{start:.3f},{end:.3f})':format=auto{out_tag}")
            prev = f"[v{i}]"
        cmd += ["-filter_complex", ";".join(fc_parts),
                "-map", "[vout]", "-map", "1:a",
                "-c:v", "libx264", "-crf", "18", "-c:a", "aac"]

        final = str(self.out / f"{output_name}.mp4")
        cmd += [final]
        subprocess.run(cmd, check=True, capture_output=True)

        print(f"\n✅ 最终视频 → {final}")
        return final
