# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# DNA: #龍芯⚡️丙午·丙申·戊辰·丙辰·䷸巽为风-CODE-补DNA-150183db
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂本地声音克隆器 · F5-TTS Zero-Shot Wrapper
固定目录：~/Pictures/龍魂素材仓库/voice_samples/uid9622/
用法：
    python3 lh_f5tts_clone.py \
        --ref ~/Pictures/龍魂素材仓库/voice_samples/uid9622/origin_24k.wav \
        --gen "那一晚雪下得很大，没有人看见，东北未来的格局被重新书写。" \
        --out ~/Pictures/龍魂素材仓库/voice_samples/uid9622/test_clone.wav \
        --pitch -2
"""

import argparse
import os
import subprocess
import sys
import warnings
from pathlib import Path

# 强制走 HF 国内镜像，避免老百姓被外网卡死
os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")

import soundfile as sf
import torch

warnings.filterwarnings("ignore")


def ensure_dir(p: Path):
    p.parent.mkdir(parents=True, exist_ok=True)


def pitch_shift_ffmpeg(src: Path, dst: Path, semitones: float):
    """用 ffmpeg asetrate 降调/升调，并用 atempo 补偿语速，让声音更浑厚或更尖。
    注意：系统 ffmpeg 未编译 rubberband 滤镜，所以用 asetrate+atempo 组合实现。"""
    if abs(semitones) < 0.1:
        return src
    ratio = 2 ** (semitones / 12.0)
    new_rate = int(24000 * ratio)
    tempo = 1.0 / ratio  # 补偿语速
    af = f"asetrate={new_rate},atempo={tempo},aresample=24000"
    cmd = [
        "ffmpeg", "-y", "-i", str(src),
        "-af", af,
        "-ar", "24000", "-ac", "1",
        str(dst),
    ]
    print(f"🎛️  pitch shift {semitones:+.1f} 半音（asetrate+atempo） → {dst}")
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    return dst


def main():
    parser = argparse.ArgumentParser(description="龍魂 F5-TTS 本地声音克隆")
    parser.add_argument("--ref", required=True, help="参考音频路径（24kHz wav 最佳）")
    parser.add_argument("--ref-text", default=None, help="参考音频对应的文本；不提供则自动转写")
    parser.add_argument("--gen", required=True, help="要生成的文本")
    parser.add_argument("--out", required=True, help="输出 wav 路径")
    parser.add_argument("--pitch", type=float, default=0, help="输出后 pitch shift 半音数（负值降调更浑厚）")
    parser.add_argument("--nfe", type=int, default=32, help="扩散步数，默认32；越低越快越糙")
    parser.add_argument("--speed", type=float, default=1.0, help="语速倍率")
    parser.add_argument("--seed", type=int, default=None, help="随机种子")
    parser.add_argument("--device", default=None, help="cpu/mps/cuda；默认自动")
    args = parser.parse_args()

    ref_path = Path(args.ref).expanduser().resolve()
    out_path = Path(args.out).expanduser().resolve()
    ensure_dir(out_path)

    if not ref_path.exists():
        print(f"❌ 参考音频不存在：{ref_path}")
        sys.exit(1)

    # 延迟导入，减少启动时间
    from f5_tts.api import F5TTS

    device = args.device or ("mps" if torch.backends.mps.is_available() else "cpu")
    print(f"🐉 龍魂声音克隆启动 | 设备：{device}")
    print(f"🎙️ 参考音频：{ref_path}")

    # 加载模型（首次会下载约 1.3GB + 300MB，走 HF 镜像）
    print("⏳ 加载 F5-TTS 模型（首次下载约 1.6GB，请耐心等待）...")
    tts = F5TTS(device=device)

    # 自动转写参考文本
    ref_text = args.ref_text
    if not ref_text:
        print("📝 自动转写参考音频文本（首次会下载 Whisper 模型）...")
        ref_text = tts.transcribe(str(ref_path), language="zh")
        print(f"📝 转写结果：{ref_text}")
    else:
        print(f"📝 使用给定参考文本：{ref_text}")

    # 生成
    print(f"🗣️ 开始克隆生成：{args.gen[:40]}...")
    tts.infer(
        ref_file=str(ref_path),
        ref_text=ref_text,
        gen_text=args.gen,
        file_wave=str(out_path),
        nfe_step=args.nfe,
        speed=args.speed,
        seed=args.seed,
        remove_silence=True,
    )

    info = sf.info(out_path)
    print(f"✅ 克隆完成：{out_path} | {info.duration:.2f}s | {info.samplerate}Hz")

    # 可选后处理
    if args.pitch:
        shifted = out_path.with_stem(out_path.stem + f"_pitch{args.pitch:+.0f}")
        pitch_shift_ffmpeg(out_path, shifted, args.pitch)
        print(f"✅ 修饰版：{shifted}")


if __name__ == "__main__":
    main()
