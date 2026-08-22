# DNA: #龍芯⚡️丙午·丙申·戊辰·丁巳·䷯井-CODE-补DNA-eded7de5
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 龍芯⚡️丙午·丙申·辛酉·亥时·☳震-CHATTTS-TTS-v1.0
"""
🐉 龍魂 · ChatTTS 本地 TTS 助手

必须在 Python 3.12 venv 中运行：
  /Users/zuimeidedeyihan/longhun-system/.venv/bin/python lh_chattts_tts.py "文本" --out output.wav

模型首次使用会自动从 HuggingFace 下载（公开免费，无 API Key）。
"""

import argparse
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="龍魂 · ChatTTS 本地 TTS")
    parser.add_argument("text", help="要合成的文本")
    parser.add_argument("--out", required=True, help="输出 wav 路径")
    parser.add_argument("--speed", type=float, default=1.0, help="语速")
    parser.add_argument("--temperature", type=float, default=0.3, help="随机性")
    parser.add_argument("--top-p", type=float, default=0.7, help="Top-p")
    parser.add_argument("--top-k", type=int, default=20, help="Top-k")
    args = parser.parse_args()

    try:
        import ChatTTS
        import torch
        import torchaudio
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请在 venv 安装: /Users/zuimeidedeyihan/longhun-system/.venv/bin/python -m pip install ChatTTS")
        sys.exit(1)

    print("🎙️ ChatTTS 加载模型中...")
    chat = ChatTTS.Chat(get_seed=42)
    chat.load(compile=False)  # macOS CPU 不编译

    print(f"🎙️ ChatTTS 合成: {args.text[:40]}...")
    params_infer_code = {
        "prompt": f"[speed_{args.speed}]",
        "temperature": args.temperature,
        "top_P": args.top_p,
        "top_K": args.top_k,
    }
    params_refine_text = {
        "prompt": "[oral_2][laugh_0][break_6]",
    }

    wavs = chat.infer(
        [args.text],
        params_refine_text=params_refine_text,
        params_infer_code=params_infer_code,
    )

    if not wavs or len(wavs) == 0:
        print("❌ 未生成音频")
        sys.exit(1)

    # ChatTTS 返回的是 torch tensor，保存为 wav
    wav_tensor = torch.from_numpy(wavs[0]).unsqueeze(0)
    torchaudio.save(args.out, wav_tensor, 24000)
    print(f"✅ 已保存: {args.out}")


if __name__ == "__main__":
    main()
