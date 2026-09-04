# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 本地语音输入模块 v1.0
DNA: #龍芯⚡️丙午·丙申·丁卯·丙午·䷚颐-VOICE-INPUT-v1.0
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

后端: faster-whisper（本地推理·零云端·CPU int8）
支持: 麦克风实时录音（VAD 静音自动停） / 音频文件转写 / 唤醒词单次监听
适配: macOS（sounddevice + portaudio）· 临时文件自动清理 · HF 镜像兜底
模型: 默认 small（快·150MB）· --model large-v3-turbo 切高精度（中文最佳）

用法:
    python3 bin/voice_input.py                       # 录麦克风→转写
    python3 bin/voice_input.py audio.mp3             # 文件转写
    python3 bin/voice_input.py --model small audio.wav
    python3 bin/voice_input.py --wake                # 单次唤醒词监听（说"宝宝/龍魂/截图"等）
"""

import os
import sys
import wave
import tempfile
import atexit
from pathlib import Path
from typing import Optional

# ── HF 镜像兜底（国内拉模型稳）──
os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")
# 清代理：hf-mirror 国内直连·SOCKS 缺 pysocks 会炸（Missing dependencies for SOCKS support）
for _k in ("all_proxy", "ALL_PROXY", "http_proxy", "HTTP_PROXY", "https_proxy", "HTTPS_PROXY"):
    os.environ.pop(_k, None)

try:
    import numpy as np
    import sounddevice as sd
    from faster_whisper import WhisperModel
    VOICE_READY = True
except ImportError:
    VOICE_READY = False

ROOT = Path(__file__).resolve().parent.parent

# ────────────────────────────────────────────────
# § 1  配置
# ────────────────────────────────────────────────
WHISPER_MODEL    = "small"            # small(150MB·快) / medium / large-v3-turbo(中文最佳)
WHISPER_DEVICE   = "cpu"              # Apple Silicon 可用 "cpu"（int8 量化足够快）
COMPUTE_TYPE     = "int8"
SAMPLE_RATE      = 16000              # Whisper 标准采样率
CHANNELS         = 1
SILENCE_THRESH   = 0.015              # 静音能量阈值（可微调）
SILENCE_SECS     = 1.2                # 停顿这么久自动停
MAX_RECORD_SECS  = 45                 # 录音上限

WAKE_WORDS = ["宝宝", "龍魂", "龙魂", "小助手", "截图", "开始", "看看屏幕"]

_model_cache = None
_temp_files: list = []


def _cleanup_temps():
    for f in _temp_files:
        try:
            if os.path.exists(f):
                os.unlink(f)
        except Exception:
            pass


atexit.register(_cleanup_temps)


def _load_model() -> Optional[object]:
    """加载 Whisper 模型（缓存·首次自动从 HF 下载，走镜像）"""
    global _model_cache
    if _model_cache is None:
        if not VOICE_READY:
            raise RuntimeError("请先安装: pip install faster-whisper sounddevice numpy")
        print(f"⏳ 加载 Whisper 模型 ({WHISPER_MODEL}) · 首次下载走 hf-mirror…")
        _model_cache = WhisperModel(
            WHISPER_MODEL,
            device=WHISPER_DEVICE,
            compute_type=COMPUTE_TYPE,
        )
        print("✅ Whisper 模型就绪")
    return _model_cache


# ────────────────────────────────────────────────
# § 2  麦克风录音（VAD 静音自动停）
# ────────────────────────────────────────────────
def record_until_silence(
    max_secs: int = MAX_RECORD_SECS,
    silence_secs: float = SILENCE_SECS,
) -> "np.ndarray":
    """录音直到静音 or 超时。返回 float32 单声道数组。"""
    print("🎤 开始录音…（说话后停顿自动结束，Ctrl+C 强制停）")
    frames = []
    silent_chunks = 0
    chunk_size = int(SAMPLE_RATE * 0.1)          # 100ms
    max_chunks = int(max_secs / 0.1)
    silence_limit = int(silence_secs / 0.1)
    started = False

    try:
        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype="float32",
            blocksize=chunk_size,
        ) as stream:
            for _ in range(max_chunks):
                chunk, overflowed = stream.read(chunk_size)
                if overflowed:
                    print("⚠️  音频溢出，可能丢帧")
                energy = float(np.abs(chunk).mean())
                frames.append(chunk.copy())

                if energy > SILENCE_THRESH:
                    started = True
                    silent_chunks = 0
                elif started:
                    silent_chunks += 1
                    if silent_chunks >= silence_limit:
                        break
    except Exception as e:
        raise RuntimeError(f"录音失败（检查麦克风权限: 系统设置→隐私与安全性→麦克风）: {e}")

    if not frames:
        raise RuntimeError("未录到任何音频")
    audio = np.concatenate(frames, axis=0).flatten()
    print(f"🎤 录音完毕（{len(audio) / SAMPLE_RATE:.1f}s）")
    return audio


# ────────────────────────────────────────────────
# § 3  转写
# ────────────────────────────────────────────────
def transcribe_audio(
    file_path: Optional[str] = None,
    language: str = "zh",
    model: str = None,
) -> str:
    """
    转写音频文件或实时录麦克风。
    file_path=None → 自动录麦克风。
    返回文本；失败返回 "ERROR: ..."。
    """
    global WHISPER_MODEL
    if model:
        WHISPER_MODEL = model
    if not VOICE_READY:
        return "ERROR: 请先安装: pip install faster-whisper sounddevice numpy"

    try:
        model_obj = _load_model()
    except Exception as e:
        return f"ERROR: 模型加载失败 → {e}"

    audio_path = None
    is_temp = False

    try:
        if file_path:
            audio_path = str(Path(file_path).resolve())
            if not Path(audio_path).exists():
                return f"ERROR: 文件不存在 → {audio_path}"
        else:
            audio = record_until_silence()
            tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
            audio_path = tmp.name
            is_temp = True
            _temp_files.append(audio_path)
            with wave.open(audio_path, "wb") as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(2)
                wf.setframerate(SAMPLE_RATE)
                wf.writeframes((audio * 32767).astype(np.int16).tobytes())

        print(f"⚙️  转写中（语言={language}·模型={WHISPER_MODEL}）…")
        segments, _info = model_obj.transcribe(
            audio_path,
            language=language,
            beam_size=5,
            best_of=5,
            temperature=0.0,
            condition_on_previous_text=True,   # 中文长句更稳
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=400),
        )
        text = " ".join(s.text.strip() for s in segments if s.text.strip())
        print(f"📝 转写结果: {text}")
        # DNA 自动记录（CB-002 集成：写 .codebuddy/memory/ 每日日志）
        if text and not text.startswith("ERROR"):
            try:
                sys.path.insert(0, str(Path(__file__).resolve().parent))
                from dna_helper import append_with_dna
                append_with_dna(f"[语音转写] {text}", source="voice", category="voice", action="转写", silent=True)
            except Exception:
                pass
        return text or "(空结果)"
    except Exception as e:
        return f"ERROR: 转写失败 → {e}"
    finally:
        if is_temp and audio_path and os.path.exists(audio_path):
            try:
                os.unlink(audio_path)
                if audio_path in _temp_files:
                    _temp_files.remove(audio_path)
            except Exception:
                pass


# ────────────────────────────────────────────────
# § 4  唤醒词监听（单次）
# ────────────────────────────────────────────────
def listen_once(wake_words: Optional[list] = None, model: str = None) -> str:
    """
    单次唤醒词监听：录一段音，若含唤醒词返回全文，否则返回 None。
    适合被 local_agent / lh 循环调用。
    """
    words = wake_words or WAKE_WORDS
    text = transcribe_audio(model=model)
    if text.startswith("ERROR") or text == "(空结果)":
        return None
    hit = [w for w in words if w in text]
    if hit:
        print(f"🔔 唤醒命中 {hit} → {text}")
        return text
    return None


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="龍魂本地语音输入 v1.0（faster-whisper·零云端）")
    ap.add_argument("file", nargs="?", help="音频文件路径（不传则录麦克风）")
    ap.add_argument("--model", default=None, help=f"模型（默认 {WHISPER_MODEL}·推荐 large-v3-turbo 中文最佳）")
    ap.add_argument("--wake", action="store_true", help="唤醒词监听模式（单次）")
    ap.add_argument("--language", default="zh", help="语言（默认 zh）")
    args = ap.parse_args()

    if args.wake:
        result = listen_once(model=args.model)
        print(f"\n结果: {result}" if result else "\n未命中唤醒词")
    else:
        r = transcribe_audio(file_path=args.file, language=args.language, model=args.model)
        print(f"\n最终文本: {r}")
