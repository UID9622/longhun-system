#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂语音合成服务 v2.1
本地 XTTS v2 推理服务，支持配置化多音色：
  - assistant（女声）：系统助手「宝宝」回复
  - uid9622（本音）：UID9622 本人克隆音色，用于内容播报/读文章/解说稿
DNA: #龍芯⚡️2026-06-27-LONGHUN-TTS-SERVER-v2.1
"""
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock

# 必须在使用 TTS / torch 前设置
os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")
os.environ["COQUI_TOS_AGREED"] = "1"

# 兼容 torch 2.0+ weights_only 默认值变化
import torch
_orig_torch_load = torch.load

def _torch_load_weights_false(*args, **kwargs):
    kwargs.setdefault("weights_only", False)
    return _orig_torch_load(*args, **kwargs)

torch.load = _torch_load_weights_false

# torchaudio.load 在最新 TTS 下可能因 sox 问题失败，用 soundfile 兜底
try:
    import torchaudio
    import soundfile as sf

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
except Exception:
    pass

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

AGENT_DNA = "#龍芯⚡️2026-06-27-LONGHUN-TTS-SERVER-v2.1"

# 路径配置
WORKSPACE = Path("/Users/zuimeidedeyihan/Downloads/Kimi_Agent_小龙虾扩展与人格/UID9622_Workspace")
OUTPUT_DIR = WORKSPACE / "temp" / "voice"
CONFIG_PATH = WORKSPACE / "data" / "voice_profiles.json"

def load_voice_config():
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    return {
        "profiles": {
            "assistant": {"type": "builtin_speaker", "speaker": "Daisy Studious", "language": "zh"},
            "uid9622": {"type": "voice_clone", "speaker_wav": "", "language": "zh"},
        },
        "rules": {"default_profile": "assistant", "max_text_length": 800},
    }

VOICE_CONFIG = load_voice_config()
PROFILES = VOICE_CONFIG.get("profiles", {})
RULES = VOICE_CONFIG.get("rules", {})
DEFAULT_PROFILE = RULES.get("default_profile", "assistant")
MAX_TEXT_LENGTH = RULES.get("max_text_length", 800)

app = FastAPI(title="龍魂语音合成服务", version="2.1.0")

# 延迟加载模型
_tts_model = None
_tts_lock = Lock()


def get_tts():
    global _tts_model
    if _tts_model is None:
        from TTS.api import TTS
        model_name = VOICE_CONFIG.get("server", {}).get("model_name", "tts_models/multilingual/multi-dataset/xtts_v2")
        print(f"[TTS] 正在加载 XTTS v2 模型: {model_name}", flush=True)
        _tts_model = TTS(model_name, gpu=False)
        print("[TTS] 模型加载完成", flush=True)
    return _tts_model


def get_available_speakers():
    """从本地 XTTS 模型中读取内置 speaker 列表。"""
    try:
        model_path = Path.home() / "Library/Application Support/tts/tts_models--multilingual--multi-dataset--xtts_v2/speakers_xtts.pth"
        if not model_path.exists():
            return []
        data = torch.load(str(model_path), map_location="cpu", weights_only=False)
        if isinstance(data, dict):
            return sorted(data.keys())
    except Exception as e:
        print(f"[TTS] 读取 speakers 失败: {e}", flush=True)
    return []


class SpeakRequest(BaseModel):
    text: str
    profile: str = DEFAULT_PROFILE
    speaker: str = ""  # 可选：强制指定内置 speaker，覆盖配置
    output_path: str = ""


def _safe_filename(text: str, profile: str) -> str:
    safe = re.sub(r"[^\w\u4e00-\u9fff]+", "_", text)[:24]
    if not safe:
        safe = "tts"
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    return f"longhun_{profile}_{safe}_{ts}.wav"


def _render_with_builtin(tts, text: str, speaker: str, file_path: Path) -> None:
    tts.tts_to_file(text=text, speaker=speaker, language="zh", file_path=str(file_path))


def _render_with_clone(tts, text: str, wav_path: str, file_path: Path) -> None:
    tts.tts_to_file(text=text, speaker_wav=wav_path, language="zh", file_path=str(file_path))


def _synthesize(text: str, profile_cfg: dict, out_path: Path, speaker_override: str = "") -> dict:
    tts = get_tts()
    ptype = profile_cfg.get("type", "builtin_speaker")
    errors = []

    with _tts_lock:
        start = time.time()
        # 如果请求显式指定 speaker，优先使用
        if speaker_override:
            try:
                _render_with_builtin(tts, text, speaker_override, out_path)
                elapsed = time.time() - start
                return {"speaker": speaker_override, "processing_seconds": round(elapsed, 2)}
            except Exception as e:
                errors.append(f"requested speaker {speaker_override}: {e}")

        if ptype == "voice_clone":
            wav = profile_cfg.get("speaker_wav", "")
            fallback = profile_cfg.get("speaker_wav_fallback", "")
            for wp in [wav, fallback]:
                if wp and Path(wp).exists():
                    try:
                        _render_with_clone(tts, text, wp, out_path)
                        elapsed = time.time() - start
                        return {"speaker_wav": wp, "processing_seconds": round(elapsed, 2)}
                    except Exception as e:
                        errors.append(f"clone {wp}: {e}")
            raise RuntimeError(f"克隆音色生成失败: {'; '.join(errors)}")

        # builtin speaker with fallback
        speakers = [profile_cfg.get("speaker", "Daisy Studious")]
        speakers.extend(profile_cfg.get("fallback_order", []))
        for spk in speakers:
            try:
                _render_with_builtin(tts, text, spk, out_path)
                elapsed = time.time() - start
                return {"speaker": spk, "processing_seconds": round(elapsed, 2)}
            except Exception as e:
                errors.append(f"speaker {spk}: {e}")
        raise RuntimeError(f"内置音色生成失败: {'; '.join(errors)}")


@app.get("/")
def root():
    return {"ok": True, "service": "longhun-tts", "version": "2.1.0", "dna": AGENT_DNA}


@app.get("/health")
def health():
    return {
        "ok": True,
        "model_loaded": _tts_model is not None,
        "default_profile": DEFAULT_PROFILE,
        "profiles": {k: {"name": v.get("name", k), "type": v.get("type"), "description": v.get("description", "")}
                     for k, v in PROFILES.items()},
        "dna": AGENT_DNA,
    }


@app.get("/profiles")
def list_profiles():
    return {"ok": True, "profiles": PROFILES, "default": DEFAULT_PROFILE, "dna": AGENT_DNA}


@app.get("/speakers")
def list_speakers():
    return {"ok": True, "speakers": get_available_speakers(), "dna": AGENT_DNA}


@app.post("/speak")
def speak(req: SpeakRequest):
    text = req.text.strip()
    if not text:
        return JSONResponse(status_code=400, content={"ok": False, "error": "text is empty"})
    if len(text) > MAX_TEXT_LENGTH:
        text = text[:MAX_TEXT_LENGTH]

    profile_name = req.profile.lower() if req.profile else DEFAULT_PROFILE
    profile_cfg = PROFILES.get(profile_name)
    if not profile_cfg:
        return JSONResponse(status_code=400, content={"ok": False, "error": f"unknown profile: {profile_name}"})

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if req.output_path:
        out_path = Path(req.output_path)
    else:
        out_path = OUTPUT_DIR / _safe_filename(text, profile_name)

    try:
        meta = _synthesize(text, profile_cfg, out_path, speaker_override=req.speaker)
        return {
            "ok": True,
            "profile": profile_name,
            "audio_file": str(out_path),
            "dna": AGENT_DNA,
            **meta,
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"ok": False, "error": str(e), "dna": AGENT_DNA})


@app.get("/play")
def play(path: str):
    p = Path(path)
    if not p.exists():
        return JSONResponse(status_code=404, content={"ok": False, "error": "file not found"})
    if sys.platform == "darwin" and subprocess.run(["which", "afplay"], capture_output=True).returncode == 0:
        subprocess.Popen(["afplay", str(p)])
    return {"ok": True, "played": str(p)}


if __name__ == "__main__":
    import uvicorn
    port = VOICE_CONFIG.get("server", {}).get("port", 9624)
    print(f"🐉 龍魂语音合成服务启动: http://localhost:{port}")
    print(f"DNA: {AGENT_DNA}")
    uvicorn.run(app, host="127.0.0.1", port=port)
