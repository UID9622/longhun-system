#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-09-01-DEMO-AUDIO-v1.0-MEDIA-SENSE
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
🔊 龍魂声音引擎 demo — TTS 合成 / 音频指纹 / 声纹比对
用法: python3 examples/demo_audio.py
注意: 本机若无中文语音包，TTS 用英文声音（--voice Alex）演示链路。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "08_BIN"))
from lh_audio import cmd_speak, cmd_fingerprint, cmd_compare

OUT = Path(__file__).resolve().parent / "output" / "audio"
OUT.mkdir(parents=True, exist_ok=True)


def main():
    print("🔊 龍魂声音引擎 demo")
    wav1 = cmd_speak("LongHun audio engine demo one", voice="Alex", fmt="wav",
                     out=str(OUT / "demo_speak_1.wav"))
    wav2 = cmd_speak("A different sentence for fingerprint comparison", voice="Alex", fmt="wav",
                     out=str(OUT / "demo_speak_2.wav"))
    fp1 = cmd_fingerprint(wav1, out=str(OUT / "demo_fp_1.json"))
    fp2 = cmd_fingerprint(wav2, out=str(OUT / "demo_fp_2.json"))
    print("--- 声纹比对 ---")
    cmd_compare(wav1, wav1)   # 同源 → 应 ~100%
    cmd_compare(wav1, wav2)   # 异源 → 应较低
    print(f"📁 输出目录: {OUT}")


if __name__ == "__main__":
    main()
