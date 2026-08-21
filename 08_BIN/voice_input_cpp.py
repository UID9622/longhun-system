#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂语音模块 v1.5 · DNA集成版
DNA: #龍芯⚡️2026-08-21-VOICE-v1.5
集成: DNA自动生成 · MEMORY自动写入 · 视觉联动
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime

# ── 配置 ──
ROOT = Path(__file__).resolve().parent.parent
WHISPER_CLI = ROOT / "08_BIN" / "whisper-cli"
WHISPER_STREAM = ROOT / "08_BIN" / "whisper-stream"
MODEL_PATH = ROOT / "models" / "ggml-large-v3-turbo.bin"
LANGUAGE = "zh"
N_THREADS = 6
STREAM_VAD_TH = 0.6

# ── 导入DNA助手 ──
sys.path.insert(0, str(ROOT / "08_BIN"))
from dna_helper import append_with_dna, make_dna

# ── 唤醒词 & 视觉触发词 ──
WAKE_WORDS = ["宝宝", "龍魂", "小助手", "开始", "龙魂", "截图", "看看屏幕"]
VISION_TRIGGERS = {
    "截图": "analyze_screenshot",
    "看看屏幕": "analyze_screenshot",
    "分析屏幕": "analyze_screenshot",
}
CUSTOM_PROMPT = "中文语音，包含唤醒词：宝宝、龍魂、小助手、截图。"
MEMORY_FILE = ROOT / "MEMORY.md"


def transcribe_file(file_path: str) -> str:
    path = Path(file_path).resolve()
    if not path.exists():
        return f"ERROR: 文件不存在 {path}"

    cmd = [
        str(WHISPER_CLI), "-m", str(MODEL_PATH),
        "-f", str(path), "-l", LANGUAGE,
        "-t", str(N_THREADS), "--prompt", CUSTOM_PROMPT,
        "--no-timestamps", "-np", "-nt",
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        text = result.stdout.strip()
        if text and not text.startswith("ERROR"):
            append_with_dna(f"[文件转写] {text}", source="voice", category="voice", action="转写")
        return text or "(空)"
    except Exception as e:
        return f"ERROR: {e}"


def start_streaming(use_vad: bool = True):
    cmd = [
        str(WHISPER_STREAM), "-m", str(MODEL_PATH),
        "-t", str(N_THREADS), "-l", LANGUAGE,
        "--prompt", CUSTOM_PROMPT,
        "--step", "0" if use_vad else "500",
        "--length", "5000", "-vth", str(STREAM_VAD_TH), "-np",
    ]

    print("🎤 流式监听中 (Ctrl+C停止)...")
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            text=True, bufsize=1)
    try:
        for line in proc.stdout:
            line = line.strip()
            if not line or line.startswith("["):
                continue
            print(f"🔊 {line}")

            if any(w in line for w in WAKE_WORDS):
                append_with_dna(line, source="wake", category="voice", action="唤醒")
                for trigger in VISION_TRIGGERS:
                    if trigger in line:
                        print(f"📸 触发视觉: {trigger}")
                        try:
                            from vision_input import analyze_screenshot
                            result = analyze_screenshot(f"用户说: {line}")
                            append_with_dna(f"[视觉联动] {result}",
                                           source="vision", category="vision", action="分析")
                        except Exception as e:
                            append_with_dna(f"[视觉联动失败] {e}",
                                           source="vision", category="vision", action="错误")
    except KeyboardInterrupt:
        print("\n停止")
    finally:
        proc.terminate()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="?")
    parser.add_argument("--stream", action="store_true")
    parser.add_argument("--service", action="store_true")
    args = parser.parse_args()

    if args.service or args.stream:
        start_streaming()
    elif args.file:
        print(transcribe_file(args.file))
    else:
        start_streaming()
