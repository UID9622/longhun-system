#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂语音播报引擎 v1.0
优先使用本地 ChatTTS 生成自然中文语音；未安装或失败时回退到系统 TTS。
DNA: #龍芯⚡️2026-06-27-LONGHUN-AUDIO-ENGINE-v1.0
"""
import argparse
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import warnings
from datetime import datetime, timezone
from pathlib import Path

AGENT_DNA = "#龍芯⚡️2026-06-27-LONGHUN-AUDIO-ENGINE-v1.0"


def _log(msg: str):
    ts = datetime.now(timezone.utc).isoformat()
    print(f"[{ts}] {msg}", file=sys.stderr)


def _which(cmd: str) -> str:
    return shutil.which(cmd) or ""


def _play_macos(path: Path) -> bool:
    afplay = _which("afplay")
    if not afplay:
        return False
    try:
        subprocess.run([afplay, str(path)], check=True, timeout=120)
        return True
    except Exception as e:
        _log(f"afplay 播放失败: {e}")
        return False


def _fallback_say(text: str) -> bool:
    """回退到 macOS say 命令。"""
    say = _which("say")
    if not say:
        return False
    voices = ["Yue (Premium)", "Tingting", "Ting-Ting", "Sin-ji"]
    for v in voices:
        try:
            subprocess.run([say, "-v", v, text], check=True, timeout=30)
            return True
        except Exception:
            continue
    try:
        subprocess.run([say, text], check=True, timeout=30)
        return True
    except Exception as e:
        _log(f"say 回退失败: {e}")
        return False


def chattts_speak(text: str, output_path: Path = None, play: bool = True) -> Path:
    """
    使用 ChatTTS 生成语音。若 ChatTTS 不可用则回退系统 TTS。
    返回生成的音频文件路径；回退时返回 None。
    """
    if output_path is None:
        output_path = Path(tempfile.gettempdir()) / f"longhun_tts_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.wav"
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 优先使用国内镜像下载模型权重
    os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")

    try:
        import ChatTTS
        import torch
        import torchaudio
    except ImportError as e:
        _log(f"ChatTTS 环境未就绪: {e}，回退系统 TTS")
        if play:
            _fallback_say(text)
        return None

    try:
        _log("正在加载 ChatTTS 模型（首次使用需下载权重）...")
        chat = ChatTTS.Chat()
        chat.load_models(source="huggingface")

        _log("正在推理语音...")
        wavs = chat.infer([text])
        if not wavs or not len(wavs):
            raise RuntimeError("ChatTTS 返回空音频")

        wav = wavs[0]
        tensor = torch.from_numpy(wav)
        if tensor.dim() == 1:
            tensor = tensor.unsqueeze(0)
        elif tensor.dim() == 3:
            tensor = tensor.squeeze(0)
        # 确保 (channels, samples)
        if tensor.dim() != 2:
            tensor = tensor.view(1, -1)

        torchaudio.save(str(output_path), tensor, 24000)
        _log(f"语音已生成: {output_path}")

        if play and platform.system() == "Darwin":
            _play_macos(output_path)
        return output_path

    except Exception as e:
        _log(f"ChatTTS 生成失败: {e}，回退系统 TTS")
        if play:
            _fallback_say(text)
        return None


def main():
    parser = argparse.ArgumentParser(description="龍魂语音播报引擎")
    parser.add_argument("--text", required=True, help="要播报的中文文本")
    parser.add_argument("--output", help="输出 WAV 路径")
    parser.add_argument("--no-play", action="store_true", help="只生成不播放")
    args = parser.parse_args()

    output = Path(args.output) if args.output else None
    path = chattts_speak(args.text, output, play=not args.no_play)
    if path:
        print(path)
    else:
        print("FALLBACK_TTS")
    print(f"DNA: {AGENT_DNA}")


if __name__ == "__main__":
    main()
