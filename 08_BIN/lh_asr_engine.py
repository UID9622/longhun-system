#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·丁酉·亥时·䷀乾-ASR-ENGINE-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# ╔══════════════════════════════════════════════════════════════╗
# ║  龍魂·ASR 引擎 v1.0                                          ║
# ║  DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·䷀乾-ASR-ENGINE-v1.0        ║
# ║  守护人格: 乔前辈(P15·老兵腔)                                ║
# ╚══════════════════════════════════════════════════════════════╝
"""
龍魂 ASR 引擎 — 本地 whisper 兜底方案。

依赖:
  - openai-whisper (已安装)
  - ffmpeg (已安装)

用法:
  python3 bin/lh_asr_engine.py --input recording.wav
  python3 bin/lh_asr_engine.py --input recording.mp3 --model tiny --lang zh
"""

import os
import sys
import json
import argparse
import tempfile
import subprocess
from pathlib import Path
from datetime import datetime

DNA = "#龍芯⚡️丙午·乙未·丁酉·亥时·䷀乾-ASR-ENGINE-v1.0"

# 模型大小与适用场景
MODEL_PRESETS = {
    "tiny": {"desc": "极速·低精度", "vram": "~1GB"},
    "base": {"desc": "平衡", "vram": "~1GB"},
    "small": {"desc": "较高精度", "vram": "~2GB"},
    "medium": {"desc": "高精度", "vram": "~5GB"},
}


def ensure_wav(input_path: Path) -> Path:
    """把任意 ffmpeg 支持的音频转成 16kHz 单声道 WAV。"""
    if input_path.suffix.lower() == ".wav":
        return input_path
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp_wav = Path(tmp.name)
    cmd = [
        "ffmpeg", "-y", "-i", str(input_path),
        "-ar", "16000", "-ac", "1", "-sample_fmt", "s16",
        str(tmp_wav),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return tmp_wav


def verify_dna(audio_path: Path) -> dict:
    """检测音频中是否包含龍魂 DNA。"""
    watermark_script = Path(__file__).parent / "lh_audio_watermark.py"
    try:
        result = subprocess.run(
            ["python3", str(watermark_script), "verify", str(audio_path)],
            check=False,
            capture_output=True,
            text=True,
        )
        return json.loads(result.stdout) if result.stdout else {"has_dna": False}
    except Exception as e:
        return {"has_dna": False, "error": str(e)}


def transcribe(audio_path: Path, model_name: str, lang: str) -> dict:
    """使用 whisper 进行本地识别。"""
    import whisper

    model = whisper.load_model(model_name)
    result = model.transcribe(str(audio_path), language=lang, fp16=False)

    segments = [
        {
            "id": seg.get("id"),
            "start": seg.get("start"),
            "end": seg.get("end"),
            "text": seg.get("text", "").strip(),
            "confidence": float(seg.get("avg_logprob", 0)),
        }
        for seg in result.get("segments", [])
    ]

    return {
        "text": result.get("text", "").strip(),
        "language": result.get("language", lang),
        "model": model_name,
        "segments": segments,
    }


def main():
    parser = argparse.ArgumentParser(description="龍魂 ASR 引擎")
    parser.add_argument("--input", required=True, help="输入音频路径")
    parser.add_argument("--model", default="tiny", choices=list(MODEL_PRESETS.keys()), help="whisper 模型大小")
    parser.add_argument("--lang", default="zh", help="语言代码，默认 zh")
    parser.add_argument("--dna", default=DNA, help="DNA 追溯码")
    parser.add_argument("--verify", action="store_true", help="先校验 DNA 水印再识别")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"[龍魂ASR] 错误：文件不存在 {input_path}", file=sys.stderr)
        return 1

    print(f"[龍魂ASR] DNA: {args.dna}")
    print(f"[龍魂ASR] 输入: {input_path}")
    print(f"[龍魂ASR] 模型: {args.model}")
    print(f"[龍魂ASR] 语言: {args.lang}")

    # DNA 校验
    dna_info = {"has_dna": False}
    if args.verify:
        dna_info = verify_dna(input_path)
        print(f"[龍魂ASR] DNA 校验: {'通过' if dna_info.get('has_dna') else '未检测到'}")
        if dna_info.get("dna"):
            print(f"[龍魂ASR] DNA 内容: {dna_info['dna']}")

    # 转换并识别
    tmp_wav = None
    try:
        tmp_wav = ensure_wav(input_path)
        result = transcribe(tmp_wav, args.model, args.lang)
    except Exception as e:
        print(f"[龍魂ASR] 识别失败: {e}", file=sys.stderr)
        return 1
    finally:
        if tmp_wav and tmp_wav != input_path:
            tmp_wav.unlink(missing_ok=True)

    result["dna"] = args.dna
    result["dna_verified"] = dna_info.get("has_dna", False)
    result["input"] = str(input_path)
    result["timestamp"] = datetime.now().isoformat()

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"[龍魂ASR] 识别结果: {result['text']}")
        print(f"[龍魂ASR] 语言: {result['language']}")
        print(f"[龍魂ASR] 分段数: {len(result['segments'])}")

    print("[龍魂ASR] ✅ 识别完成")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n[龍魂ASR] 已取消", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"[龍魂ASR] 错误: {e}", file=sys.stderr)
        sys.exit(1)
