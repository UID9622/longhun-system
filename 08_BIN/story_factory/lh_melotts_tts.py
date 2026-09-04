#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 龍魂 · MeloTTS 本地中文 TTS 包装器
零 API、本地推理、保护 torch/transformers 版本。

用法:
    python lh_melotts_tts.py "你好，龍魂" --out ./out.wav --speed 1.0 --speaker ZH
    python lh_melotts_tts.py --list-speakers
"""
import argparse
import hashlib
import json
import os
import sys
import time
import warnings
from datetime import datetime
from pathlib import Path

# ============================================================
# 路径与镜像
# ============================================================
FACTORY_ROOT = Path(__file__).resolve().parent
MELO_ROOT = FACTORY_ROOT / "third_party" / "MeloTTS"
if str(MELO_ROOT) not in sys.path:
    sys.path.insert(0, str(MELO_ROOT))

# 默认走 hf-mirror，国内可访问；用户可在环境变量覆盖
if "HF_ENDPOINT" not in os.environ:
    os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

# ============================================================
# DNA
# ============================================================
def generate_dna(tag: str = "MELO-TTS") -> str:
    h = hashlib.sha256(f"{tag}{time.time()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-{tag}-{h}-UID9622"


# ============================================================
# 模型缓存（避免重复加载）
# ============================================================
_MODEL_CACHE = {}

def get_model(language: str = "ZH", device: str = "auto"):
    """懒加载 MeloTTS 模型。"""
    key = (language, device)
    if key not in _MODEL_CACHE:
        # 延迟 import，避免安装未完成时脚本整体崩溃
        try:
            from melo.api import TTS
        except ImportError as e:
            raise RuntimeError(
                f"MeloTTS 未正确安装: {e}\n"
                f"请先运行: python {FACTORY_ROOT / 'install_melotts_deps.py'}"
            ) from e
        print(f"🔄 加载 MeloTTS [{language}] 模型...")
        model = TTS(language=language, device=device, use_hf=True)
        _MODEL_CACHE[key] = model
        print(f"✅ 模型加载完成，设备: {model.device}")
    return _MODEL_CACHE[key]


def list_speakers(language: str = "ZH"):
    model = get_model(language)
    return dict(model.hps.data.spk2id)


def synthesize(
    text: str,
    out_path: Path,
    language: str = "ZH",
    speaker: str = "ZH",
    speed: float = 1.0,
    device: str = "auto",
    quiet: bool = True,
) -> dict:
    """合成语音，返回元数据。"""
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    model = get_model(language, device)
    spk2id = model.hps.data.spk2id
    if speaker not in spk2id:
        raise ValueError(
            f"不支持的 speaker '{speaker}'。可用: {list(spk2id.keys())}"
        )
    speaker_id = spk2id[speaker]

    dna = generate_dna("MELO-TTS")
    meta = {
        "dna": dna,
        "text": text,
        "language": language,
        "speaker": speaker,
        "speaker_id": int(speaker_id),
        "speed": speed,
        "device": str(model.device),
        "created": datetime.now().isoformat(),
        "engine": "MeloTTS",
    }

    if not quiet:
        print(f"🎙️ 合成: {text[:40]}...")

    model.tts_to_file(text, speaker_id, str(out_path), speed=speed, quiet=quiet)

    # 写入 sidecar JSON 元数据
    meta_path = out_path.with_suffix(out_path.suffix + ".json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    return meta


def main():
    parser = argparse.ArgumentParser(description="龍魂 · MeloTTS 本地 TTS")
    parser.add_argument("text", nargs="?", help="要合成的文本")
    parser.add_argument("--out", type=Path, default=None, help="输出 wav 路径")
    parser.add_argument("--language", default="ZH", help="语言代码，默认 ZH")
    parser.add_argument("--speaker", default="ZH", help="说话人，默认 ZH")
    parser.add_argument("--speed", type=float, default=1.0, help="语速，默认 1.0")
    parser.add_argument("--device", default="auto", help="auto/cpu/mps")
    parser.add_argument("--list-speakers", action="store_true", help="列出可用说话人")
    parser.add_argument("--verbose", action="store_true", help="显示详细日志")
    args = parser.parse_args()

    if args.list_speakers:
        spks = list_speakers(args.language)
        print(f"🎙️ [{args.language}] 可用说话人:")
        for name, sid in spks.items():
            print(f"   {name}: id={sid}")
        return

    if not args.text:
        parser.error("缺少 text；或用 --list-speakers 查看说话人")
    if not args.out:
        parser.error("缺少 --out 输出路径")

    meta = synthesize(
        text=args.text,
        out_path=args.out,
        language=args.language,
        speaker=args.speaker,
        speed=args.speed,
        device=args.device,
        quiet=not args.verbose,
    )
    print(f"✅ 已生成: {args.out}")
    print(f"🧬 DNA: {meta['dna']}")


if __name__ == "__main__":
    main()
