#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·丁酉·亥时·䷀乾-TTS-ENGINE-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# ╔══════════════════════════════════════════════════════════════╗
# ║  龍魂·TTS 引擎 v1.0                                          ║
# ║  DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·䷀乾-TTS-ENGINE-v1.0        ║
# ║  守护人格: 乔前辈(P15·老兵腔)                                ║
# ╚══════════════════════════════════════════════════════════════╝
"""
龍魂 TTS 引擎 — 轻量兜底方案。

依赖:
  - edge-tts (已安装)
  - ffmpeg (已安装)
  - mutagen (可选，用于 MP3 ID3 水印)

用法:
  python3 bin/lh_tts_engine.py --text "为人民服务" --voice 乔前辈 --dna "#..."
  python3 bin/lh_tts_engine.py --text file.txt --voice P77 --output out.mp3
"""

import os
import sys
import argparse
import asyncio
import tempfile
import subprocess
from pathlib import Path
from datetime import datetime

DNA = "#龍芯⚡️丙午·乙未·丁酉·亥时·䷀乾-TTS-ENGINE-v1.0"

# 人格 → edge-tts 音色映射（轻量兜底）
VOICE_MAP = {
    "default": "zh-CN-YunxiNeural",
    "P77": "zh-CN-YunxiNeural",
    "S1": "zh-CN-YunjianNeural",
    "S2": "zh-CN-YunxiNeural",
    "S3": "zh-CN-YunxiNeural",
    "乔前辈": "zh-CN-YunjianNeural",
    "P15": "zh-CN-YunjianNeural",
    "李白": "zh-CN-YunxiNeural",
    "P11": "zh-CN-YunxiNeural",
    "魔瞳": "zh-CN-XiaoxiaoNeural",
    "P01": "zh-CN-XiaoxiaoNeural",
    "通心譯": "zh-CN-YunxiNeural",
}

# 情感参数：语速/音调/强度
# edge-tts 要求 pitch 单位为 Hz，rate/volume 为 %
EMOTION_MAP = {
    "default": {"rate": "-10%", "pitch": "-30Hz", "volume": "+0%"},
    "愤怒": {"rate": "+10%", "pitch": "+80Hz", "volume": "+10%"},
    "悲壮": {"rate": "-10%", "pitch": "-50Hz", "volume": "+0%"},
    "坚定": {"rate": "+0%", "pitch": "+0Hz", "volume": "+5%"},
    "嘲讽": {"rate": "+20%", "pitch": "+100Hz", "volume": "+0%"},
    "希望": {"rate": "+0%", "pitch": "+30Hz", "volume": "+5%"},
}


def resolve_voice(voice_id: str) -> str:
    """解析人格 ID 为 edge-tts voice 名称。"""
    return VOICE_MAP.get(voice_id, VOICE_MAP["default"])


def resolve_emotion(emotion: str) -> dict:
    """解析情感参数。"""
    return EMOTION_MAP.get(emotion, EMOTION_MAP["default"])


async def synthesize_edge_tts(
    text: str,
    voice: str,
    output_path: Path,
    emotion: dict,
) -> None:
    """使用 edge-tts 合成语音并保存。"""
    import edge_tts

    rate = emotion.get("rate", "+0%")
    pitch = emotion.get("pitch", "+0%")
    volume = emotion.get("volume", "+0%")

    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate=rate,
        volume=volume,
        pitch=pitch,
    )
    await communicate.save(str(output_path))


def convert_to_wav(input_path: Path, output_path: Path) -> None:
    """用 ffmpeg 把 MP3 转成 WAV。"""
    cmd = [
        "ffmpeg", "-y", "-i", str(input_path),
        "-ar", "24000", "-ac", "1", "-sample_fmt", "s16",
        str(output_path),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def add_dna_watermark(audio_path: Path, dna: str) -> None:
    """注入 DNA 音频水印。"""
    watermark_script = Path(__file__).parent / "lh_audio_watermark.py"
    subprocess.run(
        ["python3", str(watermark_script), "add", str(audio_path), "--dna", dna],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def read_text_input(text_arg: str) -> str:
    """支持从文件或直接输入读取文本。"""
    p = Path(text_arg)
    if p.exists() and p.is_file():
        return p.read_text(encoding="utf-8")
    return text_arg


async def main_async():
    parser = argparse.ArgumentParser(description="龍魂 TTS 引擎")
    parser.add_argument("--text", required=True, help="要合成的文本，或 .txt 文件路径")
    parser.add_argument("--voice", default="default", help=f"音色/人格 ID，可选: {list(VOICE_MAP.keys())}")
    parser.add_argument("--emotion", default="default", help=f"情感，可选: {list(EMOTION_MAP.keys())}")
    parser.add_argument("--dna", default=DNA, help="DNA 追溯码")
    parser.add_argument("--output", default="output.mp3", help="输出音频路径（默认 output.mp3）")
    parser.add_argument("--format", choices=["mp3", "wav"], default="mp3", help="输出格式")
    args = parser.parse_args()

    text = read_text_input(args.text)
    if not text.strip():
        print("[龍魂TTS] 错误：输入文本为空", file=sys.stderr)
        return 1

    voice = resolve_voice(args.voice)
    emotion = resolve_emotion(args.emotion)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"[龍魂TTS] DNA: {args.dna}")
    print(f"[龍魂TTS] 文本长度: {len(text)} 字")
    print(f"[龍魂TTS] 音色: {args.voice} -> {voice}")
    print(f"[龍魂TTS] 情感: {args.emotion}")

    if args.format == "wav":
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
            tmp_mp3 = Path(tmp.name)
        try:
            await synthesize_edge_tts(text, voice, tmp_mp3, emotion)
            convert_to_wav(tmp_mp3, output_path)
        finally:
            tmp_mp3.unlink(missing_ok=True)
    else:
        await synthesize_edge_tts(text, voice, output_path, emotion)

    add_dna_watermark(output_path, args.dna)

    print(f"[龍魂TTS] 输出: {output_path}")
    print(f"[龍魂TTS] 文件大小: {output_path.stat().st_size} bytes")
    print("[龍魂TTS] ✅ 合成完成")
    return 0


def main():
    try:
        return asyncio.run(main_async())
    except KeyboardInterrupt:
        print("\n[龍魂TTS] 已取消", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"[龍魂TTS] 错误: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
