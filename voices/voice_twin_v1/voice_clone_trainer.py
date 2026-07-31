# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂真声 · 本地语音克隆训练套件（仅 UID9622 音源）

功能：
1. 把 iPhone 语音备忘录转成 24kHz 单声道 WAV
2. 自动按静音切分片段
3. 挑选一段干净的参考音频
4. 生成 XTTS / Coqui TTS 可用的数据集清单
5. 可选：用 XTTS v2 做零样本克隆测试

DNA: #龍芯⚡️2026-06-25-VOICE-CLONE-TRAINER-v1.0
"""

import json
import os
import subprocess
import re
import sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent
RAW_DIR = ROOT / "raw"
DATASET_DIR = ROOT / "voice_dataset"
REFERENCE_WAV = DATASET_DIR / "reference.wav"
MANIFEST = DATASET_DIR / "manifest.json"

# 20260620 录音包含与家人对话，非 UID9622 单人音源，训练时排除
EXCLUDE_FILES = {"20260620 221423-E7210E2A.m4a"}
SAMPLE_RATE = 24000


def run(cmd: list[Any], **kwargs):
    print("$ " + " ".join(str(c) for c in cmd))
    return subprocess.run(cmd, check=True, **kwargs)


def get_duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, check=True
    )
    return float(out.stdout.strip())


def detect_speech_regions(wav_path: Path, noise_db: int = -40, min_silence: float = 0.3) -> list[Any]:
    """用 ffmpeg silencedetect 找出有声区间。"""
    proc = subprocess.run(
        ["ffmpeg", "-i", str(wav_path), "-af",
         f"silencedetect=noise={noise_db}dB:d={min_silence}",
         "-f", "null", "-"],
        capture_output=True, text=True
    )
    silence_starts = [float(m) for m in re.findall(r"silence_start: ([\d.]+)", proc.stderr)]
    silence_ends = [float(m) for m in re.findall(r"silence_end: ([\d.]+)", proc.stderr)]
    duration = get_duration(wav_path)

    regions = []
    cursor = 0.0
    for start, end in zip(silence_starts, silence_ends):
        if start - cursor >= 1.0:
            regions.append((cursor, start))
        cursor = end
    if duration - cursor >= 1.0:
        regions.append((cursor, duration))
    return regions


def convert_to_wav(src: Path, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    run([
        "ffmpeg", "-y", "-i", str(src),
        "-ar", str(SAMPLE_RATE), "-ac", "1", "-c:a", "pcm_s16le",
        str(dst)
    ])


def slice_region(src_wav: Path, dst_wav: Path, start: float, end: float):
    run([
        "ffmpeg", "-y", "-i", str(src_wav),
        "-ss", str(start), "-to", str(end),
        "-ar", str(SAMPLE_RATE), "-ac", "1", "-c:a", "pcm_s16le",
        str(dst_wav)
    ])


def pick_reference(wav_files: list[Any]) -> Path:
    """挑一段 6-10 秒、非首尾的干净片段作为参考音。"""
    for wav in wav_files:
        regions = detect_speech_regions(wav, noise_db=-40, min_silence=0.5)
        for start, end in regions:
            duration = end - start
            if 6.0 <= duration <= 10.0:
                REFERENCE_WAV.parent.mkdir(parents=True, exist_ok=True)
                slice_region(wav, REFERENCE_WAV, start, end)
                return REFERENCE_WAV
    # 兜底：取第一个文件的前 8 秒
    first = wav_files[0]
    slice_region(first, REFERENCE_WAV, 0.0, min(8.0, get_duration(first)))
    return REFERENCE_WAV


def normalize_segment(input_path: Path, output_path: Path):
    """对片段做响度归一化 + 高通滤波，提升克隆质量。"""
    run([
        "ffmpeg", "-y", "-i", str(input_path),
        "-af", "highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=11",
        "-ar", str(SAMPLE_RATE), "-ac", "1", "-c:a", "pcm_s16le",
        str(output_path)
    ])


def build_optimized_reference(total_target: float = 20.0) -> Path:
    """从所有干净片段中挑选并拼接一段更饱满的参考音。"""
    wav_dir = DATASET_DIR / "wav"
    wav_files = sorted(wav_dir.glob("*.wav"))
    if not wav_files:
        raise RuntimeError("先运行 --prepare 生成 wav 文件")

    all_regions = []
    for wav in wav_files:
        for start, end in detect_speech_regions(wav, noise_db=-45, min_silence=0.5):
            dur = end - start
            if dur >= 3.0:
                all_regions.append((dur, wav, start, end))

    # 优先用长片段，声音更稳定
    all_regions.sort(reverse=True)

    tmp_dir = DATASET_DIR / "ref_tmp"
    tmp_dir.mkdir(exist_ok=True)
    selected = []
    acc = 0.0
    for dur, wav, start, end in all_regions:
        seg_dur = min(dur, 8.0)
        selected.append((wav, start, start + seg_dur))
        acc += seg_dur
        if acc >= total_target:
            break

    concat_files = []
    for idx, (wav, s, e) in enumerate(selected, 1):
        raw = tmp_dir / f"ref_raw_{idx:03d}.wav"
        norm = tmp_dir / f"ref_norm_{idx:03d}.wav"
        slice_region(wav, raw, s, e)
        normalize_segment(raw, norm)
        concat_files.append(norm)

    list_file = tmp_dir / "concat_list.txt"
    list_file.write_text("\n".join(f"file '{f}'" for f in concat_files), encoding="utf-8")

    out_path = DATASET_DIR / "reference_optimized.wav"
    run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(list_file), "-ar", str(SAMPLE_RATE), "-ac", "1",
        "-c:a", "pcm_s16le", str(out_path)
    ])
    print(f"🎙 优化参考音已生成: {out_path}，总时长 {acc:.1f}s")
    return out_path


def prepare_dataset():
    print("🐉 开始准备 UID9622 真声数据集...\n")
    DATASET_DIR.mkdir(exist_ok=True)
    chunks_dir = DATASET_DIR / "chunks"
    chunks_dir.mkdir(exist_ok=True)

    m4a_files = sorted(RAW_DIR.glob("*.m4a"))
    records = []
    total_seconds = 0.0

    for src in m4a_files:
        if src.name in EXCLUDE_FILES:
            print(f"⏭ 排除非单人音源: {src.name}")
            continue

        wav_name = src.stem + ".wav"
        wav_path = DATASET_DIR / "wav" / wav_name
        convert_to_wav(src, wav_path)
        duration = get_duration(wav_path)
        total_seconds += duration

        txt_path = src.with_suffix(".m4a.txt")
        transcript = ""
        if txt_path.exists():
            transcript = txt_path.read_text(encoding="utf-8").strip()

        regions = detect_speech_regions(wav_path)
        chunk_paths = []
        for idx, (start, end) in enumerate(regions, 1):
            if end - start < 2.0:
                continue
            chunk_path = chunks_dir / f"{src.stem}_{idx:03d}.wav"
            slice_region(wav_path, chunk_path, start, min(end, start + 15.0))
            chunk_paths.append(str(chunk_path.relative_to(ROOT)))

        records.append({
            "source": str(src.relative_to(ROOT)),
            "wav": str(wav_path.relative_to(ROOT)),
            "duration": round(duration, 2),
            "transcript": transcript[:500],
            "chunks": chunk_paths
        })
        print(f"✅ {src.name} -> {len(chunk_paths)} 段有效语音，时长 {duration:.1f}s")

    # 选参考音
    chunk_files = sorted(chunks_dir.glob("*.wav"))
    reference = pick_reference([Path(c) for c in chunk_files]) if chunk_files else None

    manifest = {
        "created_at": datetime.now().isoformat(),
        "dna": "#龍芯⚡️2026-06-25-VOICE-CLONE-UID9622-DATASET",
        "sample_rate": SAMPLE_RATE,
        "speaker": "UID9622",
        "total_source_seconds": round(total_seconds, 2),
        "reference_wav": str(reference.relative_to(ROOT)) if reference else None,
        "records": records
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n🎙 参考音频: {reference}")
    print(f"📦 数据集清单: {MANIFEST}")
    print(f"⏱ 有效音源总时长: {total_seconds/60:.1f} 分钟")
    print(f"🧩 有效片段数: {len(chunk_files)}")
    print("\n下一步可以运行：python voice_clone_trainer.py --test")


def test_clone(text: str = "你好，这里是 UID9622 的龍魂真声测试。", ref_wav: Path = None):
    ref_wav = ref_wav or REFERENCE_WAV
    print(f"🧪 开始 XTTS v2 零样本克隆测试...")
    print(f"   使用参考音: {ref_wav}")
    if not ref_wav.exists():
        print("❌ 参考音不存在，请先运行 --prepare 或 --optimize-reference")
        sys.exit(1)

    # XTTS v2 使用 CPML 非商业许可，龍魂项目为人民服务、非商业优先，符合其条款。
    os.environ["COQUI_TOS_AGREED"] = "1"

    try:
        import torch
        import torchaudio
        import soundfile as sf
        # TTS 0.22.0 未适配 PyTorch 2.6+ 的 weights_only 默认 True，这里恢复旧行为
        _orig_torch_load = torch.load
        def _torch_load_weights_false(*args, **kwargs):
            kwargs.setdefault("weights_only", False)
            return _orig_torch_load(*args, **kwargs)
        torch.load = _torch_load_weights_false
        # torchaudio 2.11+ 默认用 TorchCodec，与当前 FFmpeg/PyTorch 不兼容，改用 soundfile
        def _ta_load_soundfile(uri, frame_offset=0, num_frames=-1, normalize=True, channels_first=True, **kwargs):
            frames = num_frames if num_frames > 0 else -1
            data, sr = sf.read(str(uri), dtype="float32", start=frame_offset, frames=frames)
            if data.ndim == 1:
                data = data.reshape(1, -1)
            else:
                data = data.T
            tensor = torch.from_numpy(data)
            if not channels_first:
                tensor = tensor.transpose(0, 1)
            return tensor, sr
        torchaudio.load = _ta_load_soundfile
        from TTS.api import TTS
    except ImportError:
        print("❌ 未安装 Coqui TTS。请先在独立环境里安装：pip install TTS")
        print("   当前项目隔离环境：voice-twin/.venv-tts")
        sys.exit(1)

    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
    out_path = ROOT / f"voice_clone_test_{datetime.now().strftime('%H%M%S')}.wav"
    tts.tts_to_file(text=text, speaker_wav=str(ref_wav), language="zh", file_path=str(out_path))
    print(f"✅ 测试音频已生成: {out_path}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂真声语音克隆训练套件")
    parser.add_argument("--prepare", action="store_true", help="准备数据集")
    parser.add_argument("--optimize-reference", action="store_true", help="生成优化后的参考音")
    parser.add_argument("--test", action="store_true", help="XTTS v2 零样本测试")
    parser.add_argument("--reference", type=Path, help="指定参考音频路径（默认 voice_dataset/reference.wav）")
    parser.add_argument("--text", default="你好，这里是 UID9622 的龍魂真声测试。", help="测试文本")
    args = parser.parse_args()

    if args.prepare:
        prepare_dataset()
    elif args.optimize_reference:
        build_optimized_reference()
    elif args.test:
        test_clone(args.text, ref_wav=args.reference)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
