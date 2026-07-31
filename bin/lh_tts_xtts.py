# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂真声 · XTTS v2 本地配音 —— 不依赖网络，直接用 UID9622 真声克隆

DNA: #龍芯⚡️丙午·乙巳·癸酉-TTS-XTTS-V1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
"""

import os, sys, re, json, subprocess
from pathlib import Path
from datetime import datetime

# ── transformers 兼容补丁（模块级·必须在TTS导入前）────
try:
    import transformers.utils.import_utils as _tfu
    if not hasattr(_tfu, 'is_torch_greater_or_equal'):
        import packaging.version
        import torch as _pt
        def _is_torch_ge(version, accept_dev=False):
            return packaging.version.parse(_pt.__version__) >= packaging.version.parse(version)
        _tfu.is_torch_greater_or_equal = _is_torch_ge
except Exception:
    pass

# ── 路径 ──────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
REFERENCE_WAV = PROJECT_ROOT / "docs" / "reference_optimized.wav"
OUTPUT_DIR = None  # 由命令行指定

# ── 文本清洗 ──────────────────────────────────────
def clean_scene_text(text: str) -> str:
    """去掉Markdown标记，只留纯朗读文本"""
    # 去掉 DNA 行、协议行、分隔线
    lines = text.splitlines()
    cleaned = []
    for line in lines:
        line = line.strip()
        # 跳过元数据行
        if line.startswith("> DNA:") or line.startswith("> 创建者:") or line.startswith("> 协议:"):
            continue
        if line in ("---",):
            continue
        # 去掉 markdown 标题标记但保留文字
        line = re.sub(r'^#{1,6}\s+', '', line)
        line = re.sub(r'\*\*([^*]+)\*\*', r'\1', line)  # 粗体
        line = re.sub(r'\*([^*]+)\*', r'\1', line)        # 斜体
        line = re.sub(r'`([^`]+)`', r'\1', line)           # 行内代码
        if line:
            cleaned.append(line)
    return " ".join(cleaned)


# ── XTTS v2 引擎 ──────────────────────────────────
_XTTS = None

def _init_xtts():
    global _XTTS
    if _XTTS is not None:
        return _XTTS

    os.environ["COQUI_TOS_AGREED"] = "1"

    # PyTorch 2.6+ 兼容
    try:
        import torch
        _orig = torch.load
        def _load(*args, **kwargs):
            kwargs.setdefault("weights_only", False)
            return _orig(*args, **kwargs)
        torch.load = _load
    except Exception:
        pass

    # torchaudio 兼容
    try:
        import torch
        import torchaudio
        import soundfile as sf
        def _ta_load(uri, frame_offset=0, num_frames=-1, normalize=True, channels_first=True, **kwargs):
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
        torchaudio.load = _ta_load
    except Exception:
        pass

    from TTS.api import TTS
    print("🎙️ 加载 XTTS v2 模型...")
    _XTTS = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
    print("   ✅ 模型就绪")
    return _XTTS


def generate_tts(text: str, output_path: Path, ref_wav: Path = None) -> Path:
    """用 XTTS v2 生成语音"""
    ref = ref_wav or REFERENCE_WAV
    if not ref.exists():
        raise FileNotFoundError(f"参考音频不存在: {ref}")

    tts = _init_xtts()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 先生成 WAV，再转 MP3（XTTS 直接输出 WAV）
    wav_path = output_path.with_suffix(".wav")
    tts.tts_to_file(text=text, speaker_wav=str(ref), language="zh", file_path=str(wav_path))

    # 转 MP3（视频合成需要 MP3）
    result = subprocess.run([
        "ffmpeg", "-y", "-i", str(wav_path),
        "-codec:a", "libmp3lame", "-b:a", "128k",
        str(output_path)
    ], capture_output=True)

    if result.returncode != 0:
        err_msg = result.stderr.decode("utf-8", errors="replace")[-300:]
        # ffmpeg 失败则保留 WAV 作为备选输出
        wav_path.rename(output_path.with_suffix(".wav"))
        raise RuntimeError(f"ffmpeg失败: {err_msg}")
    else:
        # 清临时 WAV
        wav_path.unlink(missing_ok=True)

    return output_path


# ── 主流程 ────────────────────────────────────────
def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂 XTTS v2 真声配音")
    parser.add_argument("--script", required=True, help="视频脚本 Markdown")
    parser.add_argument("--out", required=True, help="输出目录")
    parser.add_argument("--ref", help="参考音频路径（默认 docs/reference_optimized.wav）")
    args = parser.parse_args()

    # 导入场景解析器
    sys.path.insert(0, str(PROJECT_ROOT / "bin"))
    from lh_video_studio_v5 import parse_script_md

    scenes = parse_script_md(args.script)
    audio_dir = Path(args.out)
    audio_dir.mkdir(parents=True, exist_ok=True)
    ref_wav = Path(args.ref) if args.ref else REFERENCE_WAV

    print(f"🎙️ 龍魂 XTTS v2 真声配音")
    print(f"   参考音: {ref_wav} ({'✅ 存在' if ref_wav.exists() else '❌ 缺失'})")
    print(f"   脚本: {args.script} ({len(scenes)} 个场景)")
    print(f"   输出: {audio_dir}")
    print()

    results = []
    total_start = datetime.now()

    for i, scene in enumerate(scenes):
        raw_text = scene.get("text", "")
        clean_text = clean_scene_text(raw_text)

        if not clean_text or len(clean_text) < 5:
            print(f"  ⏭ scene_{i:02d}: 跳过（文本太短）")
            results.append({"scene": i, "status": "skipped", "text_len": len(clean_text)})
            continue

        output_file = audio_dir / f"scene_{i:02d}.mp3"
        print(f"  🎤 scene_{i:02d}: {len(clean_text)}字 → ", end="", flush=True)

        try:
            t_start = datetime.now()
            generate_tts(clean_text, output_file, ref_wav)
            elapsed = (datetime.now() - t_start).total_seconds()
            size_kb = output_file.stat().st_size / 1024
            print(f"✅ {elapsed:.0f}s / {size_kb:.0f}KB")
            results.append({
                "scene": i,
                "status": "ok",
                "text_len": len(clean_text),
                "file": str(output_file),
                "size_kb": round(size_kb, 1),
                "elapsed_s": round(elapsed, 1),
            })
        except Exception as e:
            print(f"❌ {e}")
            results.append({"scene": i, "status": "error", "text_len": len(clean_text), "error": str(e)})

    # 汇总
    total_elapsed = (datetime.now() - total_start).total_seconds()
    ok = sum(1 for r in results if r["status"] == "ok")
    err = sum(1 for r in results if r["status"] == "error")
    print(f"\n{'='*50}")
    print(f"📊 {ok}/{len(scenes)} 成功 | {err} 失败 | 总耗时 {total_elapsed:.0f}s")

    # 写汇总 JSON
    manifest = {
        "dna": f"#龍芯⚡️{datetime.now().strftime('%Y%m%d-%H%M%S')}-XTTS-VOICE-BATCH",
        "script": args.script,
        "reference": str(ref_wav),
        "scenes": len(scenes),
        "ok": ok,
        "error": err,
        "total_elapsed_s": round(total_elapsed, 1),
        "results": results,
    }
    manifest_path = audio_dir / "tts_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"📦 清单: {manifest_path}")

    if err > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
