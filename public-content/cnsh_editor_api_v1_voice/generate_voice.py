#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 CNSH 文章 · UID9622 真声播报生成器

读取 voice_script.json，按段生成语音，最后合并为完整 MP3。
生成链路：
    XTTS v2 本地真声 → Fish Audio 云端真声 → edge-tts 成熟男声 → 系统 TTS

DNA: #龍芯⚡️2026-07-04-CNSH-ARTICLE-VOICE-GENERATOR-v1.0
"""
from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

# ── 路径对齐 ──
HOME = Path.home()
LONGHUN_ROOT = HOME / "longhun-system"
WECHAT_DIR = LONGHUN_ROOT / "integrations" / "wechat_public_account"
FISH_DIR = LONGHUN_ROOT / "integrations" / "fish_audio"

for d in (str(WECHAT_DIR), str(FISH_DIR)):
    if d not in sys.path:
        sys.path.insert(0, d)

# 绕过 services/__init__.py 直接加载 voice_service.py，避免触发其他依赖
_voice_service_path = WECHAT_DIR / "services" / "voice_service.py"
_spec = importlib.util.spec_from_file_location("_voice_service", _voice_service_path)
_voice_service = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_voice_service)
VoiceService = _voice_service.VoiceService


SCRIPT_PATH = Path(__file__).with_name("voice_script.json")
OUTPUT_DIR = Path(__file__).parent


def load_script(path: Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_segment(service: VoiceService, segment: dict[str, Any], output_dir: Path) -> Path:
    """生成单个音频片段，返回 mp3 路径。"""
    seg_id = segment["id"]
    text = segment["text"].strip()
    style = segment.get("style", "educator")
    emotion = segment.get("emotion", "")

    print(f"\n🎙️ [{seg_id}] {emotion}")
    print(f"   文本: {text[:60]}{'...' if len(text) > 60 else ''}")
    print(f"   风格: {style}")

    out_path = output_dir / f"{seg_id}.mp3"
    final_path = service.generate(text, output_path=str(out_path), style=style)

    print(f"   ✅ 已生成: {final_path}")
    return Path(final_path)


def concat_audios(seg_paths: list[Path], output_path: Path) -> Path:
    """使用 ffmpeg concat demuxer 合并多个 mp3。"""
    if not shutil.which("ffmpeg"):
        raise RuntimeError("未找到 ffmpeg，无法合并音频。请安装 ffmpeg 后重试。")

    # 统一转成相同码率/采样率，避免 concat 异常
    normalized = []
    for idx, p in enumerate(seg_paths):
        norm = p.with_suffix(f".norm{idx}.mp3")
        subprocess.run(
            [
                "ffmpeg", "-y", "-i", str(p),
                "-ar", "44100", "-ac", "2", "-b:a", "192k",
                "-af", "apad=pad_dur=0.3",  # 段间 0.3 秒静默
                str(norm),
            ],
            check=True,
            capture_output=True,
        )
        normalized.append(norm)

    # 构造 concat 列表文件
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
        for norm in normalized:
            f.write(f"file '{norm.resolve()}'\n")
        concat_list = f.name

    try:
        subprocess.run(
            [
                "ffmpeg", "-y", "-f", "concat", "-safe", "0",
                "-i", concat_list,
                "-acodec", "libmp3lame", "-b:a", "192k",
                str(output_path),
            ],
            check=True,
            capture_output=True,
        )
    finally:
        os.unlink(concat_list)
        for norm in normalized:
            norm.unlink(missing_ok=True)

    return output_path


def main() -> None:
    print("🐉 龍魂 CNSH 文章 · UID9622 真声播报生成器")
    print(f"DNA: #龍芯⚡️{datetime.now().strftime('%Y%m%d-%H%M%S')}-VOICE-GEN\n")

    script = load_script(SCRIPT_PATH)
    segments = script["segments"]

    output_file = Path(script.get("output_file", OUTPUT_DIR / "cnsh_editor_api_voice.mp3")).expanduser()
    output_file.parent.mkdir(parents=True, exist_ok=True)

    work_dir = OUTPUT_DIR / "voice_segments"
    work_dir.mkdir(parents=True, exist_ok=True)

    service = VoiceService()
    seg_paths: list[Path] = []

    for seg in segments:
        try:
            p = generate_segment(service, seg, work_dir)
            seg_paths.append(p)
        except Exception as e:
            print(f"   ❌ 生成失败，跳过本段: {e}")
            continue

    if not seg_paths:
        raise RuntimeError("没有成功生成任何音频片段。")

    print(f"\n🔧 正在合并 {len(seg_paths)} 个片段...")
    final = concat_audios(seg_paths, output_file)

    print(f"\n✅ 完整语音播报已生成: {final}")
    print(f"   时长可用 ffprobe 查看: ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {final}")
    print(f"   DNA: {script.get('dna', 'N/A')}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"\n❌ 生成失败: {exc}")
        sys.exit(1)
