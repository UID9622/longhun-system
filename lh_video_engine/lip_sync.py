#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂视频引擎 · 口型同步模块 v1.1
DNA: #龍芯⚡️2026-08-22-LIP-SYNC-v1.1
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
设计原则:
  口型模型只负责嘴部运动，不重新生成整张脸——不动点优先。
  支持模式:
    1. Wav2Lip 模式（本地安装后）
    2. 占位模式（未安装时直接返回角色视频）
"""

import subprocess
from pathlib import Path
from typing import Optional, Dict, Any

class LipSync:
    """
    口型同步模块
    输入: 角色视频片段 + 语音 WAV → 口型对齐视频
    """

    def __init__(self, wav2lip_dir: Optional[str] = None):
        """
        wav2lip_dir: Wav2Lip 仓库目录，如 ~/Wav2Lip
                     为 None 则工作在占位模式
        """
        self.wav2lip_dir = Path(wav2lip_dir) if wav2lip_dir else None
        self._mode = "wav2lip" if (
            self.wav2lip_dir and (self.wav2lip_dir / "inference.py").exists()
        ) else "placeholder"
        print(f"  👄 LipSync 模式: {self._mode}")

    def drive(self, video_path: str, audio_path: str,
              output_path: str, face_strength: float = 0.85) -> str:
        """
        执行口型驱动
        返回输出视频路径
        """
        if self._mode == "wav2lip":
            return self._wav2lip_drive(video_path, audio_path, output_path)
        else:
            return self._placeholder_drive(video_path, audio_path, output_path)

    def _wav2lip_drive(self, video: str, audio: str, out: str) -> str:
        """
        调用 Wav2Lip inference.py
        需要: ~/Wav2Lip/ 目录存在 inference.py + checkpoints/wav2lip_gan.pth
        """
        ckpt = self.wav2lip_dir / "checkpoints" / "wav2lip_gan.pth"
        cmd = [
            "python3",
            str(self.wav2lip_dir / "inference.py"),
            "--checkpoint_path", str(ckpt),
            "--face",           video,
            "--audio",          audio,
            "--outfile",        out,
            "--resize_factor",  "1",  # 不缩小，保持原始分辨率
        ]
        subprocess.run(cmd, check=True)
        return out

    @staticmethod
    def _placeholder_drive(video: str, audio: str, out: str) -> str:
        """
        占位模式: 直接用 ffmpeg 将语音嵌入角色视频
        Wav2Lip 安装后自动切换到真实口型
        """
        subprocess.run([
            "ffmpeg", "-y",
            "-i", video, "-i", audio,
            "-c:v", "copy", "-c:a", "aac",
            "-shortest", out
        ], check=True, capture_output=True)
        return out

    def process_segment(self, seg: Dict[str, Any],
                        tts_result: Dict[str, Any],
                        visual_video: str,
                        output_path: str) -> str:
        """
        处理单个角色 Segment 的口型对齐
        仅对 lip_sync=True 的 Segment 生效
        """
        if not seg.get("lip_sync", False):
            return visual_video  # 非口型 Segment 直接返回画面
        print(f"  👌 LipSync: {seg['id']}")
        return self.drive(
            video_path  = visual_video,
            audio_path  = tts_result["audio"],
            output_path = output_path,
        )
