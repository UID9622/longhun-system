#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 CNSH 文章 · UID9622 真声播报生成器（voice_twin_server 高速版）

复用本地已缓存的 XTTS v2 模型，避免每次重新加载，10 段语音 30 秒内出片。

DNA: #龍芯⚡️2026-07-04-CNSH-ARTICLE-VOICE-GEN-SERVER-v1.0
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path

import requests

HOME = Path.home()
LONGHUN_ROOT = HOME / "longhun-system"
SCRIPT_PATH = Path(__file__).with_name("voice_script.json")
OUTPUT_DIR = Path(__file__).parent
SERVER_URL = "http://localhost:9623"


def load_script(path: Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def wait_for_server(timeout: int = 30) -> bool:
    """简单探测 voice_twin_server 是否就绪。"""
    for _ in range(timeout):
        try:
            r = requests.get(f"{SERVER_URL}/", timeout=2)
            if r.status_code == 200:
                return True
        except Exception:
            pass
        time.sleep(1)
    return False


def generate_segment(seg: dict[str, Any]) -> Path:
    """调用 /api/tts 生成单段语音，返回 wav 路径。"""
    seg_id = seg["id"]
    text = seg["text"].strip()
    style = seg.get("style", "educator")
    rate = seg.get("rate", "-5%")
    emotion = seg.get("emotion", "")

    # 风格 → edge-tts 音色兜底；真声用 xtts-v2-uid9622
    voice = "xtts-v2-uid9622"

    print(f"\n🎙️ [{seg_id}] {emotion}")
    print(f"   文本: {text[:60]}{'...' if len(text) > 60 else ''}")
    print(f"   风格: {style} | 语速: {rate}")

    resp = requests.post(
        f"{SERVER_URL}/api/tts",
        json={"text": text, "voice": voice, "rate": rate, "volume": "+0%", "pitch": "+0Hz"},
        timeout=120,
    )
    resp.raise_for_status()
    data = resp.json()
    if not data.get("ok"):
        raise RuntimeError(f"TTS 接口返回失败: {data}")

    wav_path = Path(data["absolute_path"])
    print(f"   ✅ 已生成: {wav_path.name}")
    return wav_path


def wav_to_mp3(wav_path: Path, mp3_path: Path, pad_sec: float = 0.3) -> None:
    """wav 转 mp3，并追加段间静默。"""
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", str(wav_path),
            "-ar", "44100", "-ac", "2", "-b:a", "192k",
            "-af", f"apad=pad_dur={pad_sec}",
            str(mp3_path),
        ],
        check=True,
        capture_output=True,
    )


def concat_mp3s(mp3_paths: list[Path], output_path: Path) -> Path:
    """ffmpeg concat demuxer 合并。"""
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
        for p in mp3_paths:
            f.write(f"file '{p.resolve()}'\n")
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

    return output_path


def main() -> None:
    print("🐉 龍魂 CNSH 文章 · UID9622 真声播报生成器（高速版）")
    print(f"DNA: #龍芯⚡️{datetime.now().strftime('%Y%m%d-%H%M%S')}-VOICE-GEN-SERVER-v1.0\n")

    if not shutil.which("ffmpeg"):
        print("❌ 请先安装 ffmpeg")
        sys.exit(1)

    print("⏳ 等待 voice_twin_server 就绪...")
    if not wait_for_server():
        print(f"❌ {SERVER_URL} 未启动。请先运行：")
        print("   cd ~/longhun-system/voice-twin && ./.venv-tts/bin/python3 voice_twin_server.py")
        sys.exit(1)
    print("✅ 服务已就绪\n")

    script = load_script(SCRIPT_PATH)
    segments = script["segments"]
    output_file = Path(script.get("output_file", OUTPUT_DIR / "cnsh_editor_api_voice.mp3")).expanduser()
    output_file.parent.mkdir(parents=True, exist_ok=True)

    work_dir = OUTPUT_DIR / "voice_segments"
    work_dir.mkdir(parents=True, exist_ok=True)

    mp3_paths: list[Path] = []
    for seg in segments:
        try:
            wav = generate_segment(seg)
            mp3 = work_dir / f"{seg['id']}.mp3"
            wav_to_mp3(wav, mp3)
            mp3_paths.append(mp3)
        except Exception as e:
            print(f"   ❌ 本段失败，跳过: {e}")
            continue

    if not mp3_paths:
        raise RuntimeError("没有成功生成任何音频片段。")

    print(f"\n🔧 正在合并 {len(mp3_paths)} 个片段...")
    final = concat_mp3s(mp3_paths, output_file)

    print(f"\n✅ 完整语音播报已生成: {final}")
    print(f"   DNA: {script.get('dna', 'N/A')}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"\n❌ 生成失败: {exc}")
        sys.exit(1)
