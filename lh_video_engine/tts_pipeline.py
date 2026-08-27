#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂视频引擎 · TTS + 字级时间戳流水线 v1.1
DNA: #龍芯⚡️2026-08-22-TTS-PIPELINE-v1.1
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
设计原则:
  - TTS: macOS 原生 say 命令（零依赖）→ aiff → ffmpeg 转 wav
  - 字级时间戳: 基于实际音频时长 + 字速比例插值（无需额外安装）
  - 如有 whisper: 自动切换到词级对齐（更准确）
修复记录 v1.1: 声音名 "Ting-Ting"→"Tingting"(实测 macOS 实际注册名)·DNA 补 sha256
"""

import subprocess, json, hashlib, time, re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

class TtsPipeline:
    """
    TTS 流水线: 文本 → WAV + 字级时间戳
    全部使用 macOS 原生工具，零外部依赖
    """

    VOICE_ZH = "Tingting"    # macOS 内置中文女声（实测注册名，非 Ting-Ting）
    VOICE_EN = "Samantha"    # macOS 内置英文女声
    RATE     = 190           # 语速（词/分钟）

    def __init__(self, output_dir: str):
        self.out = Path(output_dir)
        self.out.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _has_whisper() -> bool:
        return subprocess.run(["which", "whisper"],
                              capture_output=True).returncode == 0

    @staticmethod
    def _has_ffmpeg() -> bool:
        return subprocess.run(["which", "ffmpeg"],
                              capture_output=True).returncode == 0

    def _say_to_wav(self, text: str, seg_id: str) -> str:
        """macOS say 命令生成 WAV"""
        # 文本清理：去掉换行（say 对换行不友好），保留标点
        clean_text = re.sub(r'\s+', ' ', text).strip()
        aiff_path = self.out / f"{seg_id}.aiff"
        wav_path  = self.out / f"{seg_id}.wav"
        # Step 1: say → aiff
        subprocess.run(
            ["say", "-v", self.VOICE_ZH, "-r", str(self.RATE),
             "-o", str(aiff_path), clean_text],
            check=True, capture_output=True)
        # Step 2: ffmpeg aiff → wav 16kHz mono
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(aiff_path),
             "-ar", "16000", "-ac", "1", str(wav_path)],
            check=True, capture_output=True)
        aiff_path.unlink(missing_ok=True)
        return str(wav_path)

    @staticmethod
    def _get_wav_duration(wav_path: str) -> float:
        """ffprobe 获取音频实际时长"""
        result = subprocess.run(
            ["ffprobe", "-v", "quiet", "-show_entries",
             "format=duration", "-of", "json", wav_path],
            capture_output=True, text=True)
        try:
            return float(json.loads(result.stdout)["format"]["duration"])
        except Exception:
            return 5.0  # fallback

    @staticmethod
    def _interpolate_timestamps(text: str, duration: float) -> List[Dict]:
        """
        基于实际音频时长按字符比例插值字级时间戳
        精度: 中文单字级，英文词级
        """
        # 分词: 中文单字拆，英文按空格
        tokens = []
        i = 0
        while i < len(text):
            c = text[i]
            if re.match(r'[\u4e00-\u9fff\u3000-\u303f\uff01-\uff60]', c):
                tokens.append(c)
                i += 1
            elif re.match(r'[a-zA-Z]', c):
                j = i
                while j < len(text) and re.match(r'[a-zA-Z]', text[j]):
                    j += 1
                tokens.append(text[i:j])
                i = j
            elif c in ' \t':
                i += 1
            else:
                tokens.append(c)
                i += 1

        if not tokens:
            return []

        step = duration / len(tokens)
        result = []
        for idx, tok in enumerate(tokens):
            result.append({
                "text":  tok,
                "start": round(idx * step, 3),
                "end":   round((idx + 1) * step, 3),
            })
        return result

    def _whisper_timestamps(self, wav_path: str, text: str) -> List[Dict]:
        """如有 whisper，使用更精确的字级时间戳"""
        try:
            result = subprocess.run(
                ["whisper", wav_path, "--language", "zh",
                 "--word_timestamps", "True", "--output_format", "json",
                 "--output_dir", str(Path(wav_path).parent)],
                capture_output=True, text=True, timeout=120)
            json_out = Path(wav_path).with_suffix(".json")
            if json_out.exists():
                data = json.loads(json_out.read_text("utf-8"))
                words = []
                for seg in data.get("segments", []):
                    for w in seg.get("words", []):
                        words.append({"text": w["word"].strip(),
                                      "start": w["start"],
                                      "end":   w["end"]})
                return words if words else []
        except Exception:
            pass
        return []

    def process_segment(self, seg_id: str, text: str,
                        duration_hint: float) -> Dict[str, Any]:
        """
        处理单个 Segment：生成 WAV + 时间戳
        返回格式就是后续口型同步输入格式
        """
        print(f"  🔊 TTS: {seg_id} | {text[:20]}...")
        wav_path = self._say_to_wav(text, seg_id)
        duration = self._get_wav_duration(wav_path)

        # 时间戳：优先用 whisper，否则插值
        if self._has_whisper():
            words = self._whisper_timestamps(wav_path, text)
        else:
            words = []
        if not words:
            words = self._interpolate_timestamps(text, duration)

        ts = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        h  = hashlib.sha256(f"{seg_id}{text}{ts}".encode()).hexdigest()[:8].upper()
        return {
            "seg_id":   seg_id,
            "text":     text,
            "audio":    wav_path,
            "duration": duration,
            "words":    words,
            "dna":      f"#龍芯⚡️{ts}-TTS-{seg_id.upper()}-{h}",
        }

    def process_all(self, segments: List[Dict]) -> List[Dict]:
        """批量处理所有 Segment 的 TTS"""
        results = []
        for seg in segments:
            r = self.process_segment(
                seg_id=seg["id"],
                text=seg["text"],
                duration_hint=seg["duration_hint"]
            )
            results.append(r)
        return results
