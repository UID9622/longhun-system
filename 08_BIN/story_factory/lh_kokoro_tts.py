# DNA: #龍芯⚡️丙午·丙申·戊辰·丁巳·䷯井-CODE-补DNA-bff7a6ee
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 龍芯⚡️丙午·丙申·辛酉·亥时·☳震-KOKORO-TTS-v1.0
"""
🐉 龍魂 · Kokoro 本地 TTS 助手（kokoro-onnx 版）

必须在 Python 3.12 venv 中运行：
  /Users/zuimeidedeyihan/longhun-system/.venv/bin/python lh_kokoro_tts.py "文本" --voice zf_001 --out output.wav

模型文件（需提前下载）：
  /Users/zuimeidedeyihan/longhun-system/models/voice/kokoro/kokoro-v1.0.onnx
  /Users/zuimeidedeyihan/longhun-system/models/voice/kokoro/voices-v1.0.bin
"""

import argparse
import sys
from pathlib import Path

MODEL_DIR = Path.home() / "longhun-system" / "models" / "voice" / "kokoro"
MODEL_PATH = MODEL_DIR / "kokoro-v1.0.onnx"
VOICES_PATH = MODEL_DIR / "voices-v1.0.bin"


def main():
    parser = argparse.ArgumentParser(description="龍魂 · Kokoro 本地 TTS")
    parser.add_argument("text", help="要合成的文本")
    parser.add_argument("--voice", default="zf_001", help="声线编码")
    parser.add_argument("--lang", default="z", help="语言代码（z=中文）")
    parser.add_argument("--out", required=True, help="输出 wav 路径")
    parser.add_argument("--speed", type=float, default=1.0, help="语速")
    args = parser.parse_args()

    if not MODEL_PATH.exists() or not VOICES_PATH.exists():
        print(f"❌ 模型文件不存在: {MODEL_DIR}")
        print("请先下载：")
        print("  curl -L -o kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx")
        print("  curl -L -o voices-v1.0.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin")
        sys.exit(1)

    try:
        from kokoro_onnx import Kokoro
        import soundfile as sf
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请在 venv 安装: /Users/zuimeidedeyihan/longhun-system/.venv/bin/python -m pip install kokoro-onnx soundfile")
        sys.exit(1)

    print(f"🎙️ Kokoro 合成: [{args.voice}] {args.text[:40]}...")
    kokoro = Kokoro(str(MODEL_PATH), str(VOICES_PATH))
    samples, sample_rate = kokoro.create(args.text, voice=args.voice, speed=args.speed, lang=args.lang)
    sf.write(args.out, samples, sample_rate)
    print(f"✅ 已保存: {args.out} ({len(samples)/sample_rate:.2f}s @ {sample_rate}Hz)")


if __name__ == "__main__":
    main()
