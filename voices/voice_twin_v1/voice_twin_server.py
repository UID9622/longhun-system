#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂真声 · 本地浏览器控制台
提供：草稿生成 / 阅读稿生成 / 视频脚本生成 / TTS 试听

DNA: #龍芯⚡️丙午·甲午·庚午·壬午·䷳艮为山-VOICE-TWIN-WEB-UI-v1.0
"""

import json
import os
import subprocess
import uuid
import zipfile
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from pydantic import BaseModel

from draft_generator import generate
from reading_generator import generate_reading
from video_script_generator import generate_video_script
from military_memory_generator import generate_captions
from sage_dialogue import generate_sage_dialogue
from video_remixer import add_captions_to_video, add_aigc_metadata
from wechat_video_exporter import export_wechat_video

# Fish Audio 真声桥接（网络不可达时自动回退 edge-tts）
try:
    import sys
    sys.path.insert(0, str(Path.home() / "longhun-system" / "integrations" / "fish_audio"))
    from fish_audio_bridge import LongHunFishAudioBridge
    FISH_AUDIO_AVAILABLE = True
except Exception:
    LongHunFishAudioBridge = None
    FISH_AUDIO_AVAILABLE = False

ROOT = Path(__file__).resolve().parent
STATIC_DIR = ROOT / "static"
DOWNLOADS_DIR = ROOT / "downloads"
OUTPUT_DIR = Path.home() / "Downloads" / "重混输出"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
TTS_OUTPUT_DIR = ROOT / "tts_outputs"
TTS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 文本生成内容落盘目录
OUTPUTS_DIR = Path.home() / "longhun-system" / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
MANIFEST_PATH = OUTPUTS_DIR / "manifest.json"

# 优先使用优化后的参考音（更长、更饱满、已响度归一化）
REFERENCE_WAV = ROOT / "voice_dataset" / "reference_optimized.wav"
if not REFERENCE_WAV.exists():
    REFERENCE_WAV = ROOT / "voice_dataset" / "reference.wav"

app = FastAPI(title="龍魂真声控制台")


# ---------- 输出落盘 + DNA 追溯 ----------

def _dna_stamp(module: str, label: str = "") -> str:
    """生成 DNA 追溯码"""
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    short = uuid.uuid4().hex[:8].upper()
    return f"#龍芯⚡️{ts}-{module}-{short}"


def _safe_filename(text: str, max_len: int = 30) -> str:
    """把任意文本转成安全文件名"""
    return "".join(c if c.isalnum() or c in "_-" else "_" for c in text)[:max_len]


def save_text_output(content_type: str, topic: str, content: str) -> dict[str, Any]:
    """
    保存生成的文本内容到 ~/longhun-system/outputs/YYYYMMDD/
    并返回包含 DNA、路径等信息的字典。
    """
    today = datetime.now().strftime("%Y%m%d")
    day_dir = OUTPUTS_DIR / today
    day_dir.mkdir(parents=True, exist_ok=True)

    ts = datetime.now().strftime("%H%M%S")
    safe_topic = _safe_filename(topic)
    filename = f"{content_type}_{ts}_{safe_topic}.md"
    file_path = day_dir / filename

    header = f"""---
content_type: {content_type}
topic: {topic}
dna: {_dna_stamp(content_type, safe_topic)}
created_at: {datetime.now().isoformat()}
---

# {content_type}: {topic}

{content}
"""
    file_path.write_text(header, encoding="utf-8")

    record = {
        "dna": _dna_stamp(content_type, safe_topic),
        "content_type": content_type,
        "topic": topic,
        "file_path": str(file_path),
        "created_at": datetime.now().isoformat(),
    }
    _append_manifest(record)
    return record


def _append_manifest(record: dict[str, Any]):
    """把记录追加到 manifest.json"""
    manifest = []
    if MANIFEST_PATH.exists():
        try:
            manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
            if not isinstance(manifest, list):
                manifest = []
        except Exception:
            manifest = []
    manifest.insert(0, record)
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def _load_manifest() -> list[Any]:
    if MANIFEST_PATH.exists():
        try:
            data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else []
        except Exception:
            return []
    return []


class TopicRequest(BaseModel):
    topic: str


class TTSRequest(BaseModel):
    text: str
    voice: str = "zh-CN-YunjianNeural"  # 默认成熟男声，避免奶狗感
    rate: str = "-5%"
    volume: str = "+0%"
    pitch: str = "+0Hz"


def _edge_tts_generate(text: str, voice: str, rate: str, volume: str, pitch: str, audio_path: Path) -> dict[str, Any]:
    """edge-tts 生成，失败回退 Mac say。"""
    try:
        import asyncio
        import edge_tts
        communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate, volume=volume, pitch=pitch)
        asyncio.run(communicate.save(str(audio_path)))
        return {"ok": True, "audio_file": f"/tts-outputs/{audio_path.name}", "absolute_path": str(audio_path),
                "voice": voice, "note": f"edge-tts 试听语音（{voice}）"}
    except Exception as e:
        print(f"edge-tts 失败，回退 Mac 系统 TTS: {e}")
        aiff_path = audio_path.with_suffix(".aiff")
        subprocess.run(["say", "-o", str(aiff_path), text], check=True)
        return {"ok": True, "audio_file": f"/tts-outputs/{aiff_path.name}", "absolute_path": str(aiff_path),
                "note": "Mac 系统默认声音（edge-tts 失败回退）"}


def _fish_audio_generate(text: str, audio_path: Path) -> dict[str, Any]:
    """Fish Audio 真声生成，失败抛出异常由上层回退。"""
    if not FISH_AUDIO_AVAILABLE:
        raise RuntimeError("Fish Audio 桥接未就绪")
    bridge = LongHunFishAudioBridge()
    if not bridge.api_key:
        raise RuntimeError("FISH_AUDIO_API_KEY 未配置")
    output = bridge.text_to_speech(text, output_file=audio_path)
    return {"ok": True, "audio_file": f"/tts-outputs/{output.name}", "absolute_path": str(output),
            "voice": "fish-audio-uid9622", "note": "Fish Audio UID9622 真声克隆"}


# XTTS v2 本地真声模型（懒加载 + 单例缓存）
_XTTS_MODEL = None


def _get_xtts_model():
    """懒加载 XTTS v2 模型。"""
    global _XTTS_MODEL
    if _XTTS_MODEL is not None:
        return _XTTS_MODEL
    if not REFERENCE_WAV.exists():
        raise RuntimeError(f"参考音频不存在: {REFERENCE_WAV}")
    os.environ["COQUI_TOS_AGREED"] = "1"
    # 兼容 PyTorch 2.6+ 的 weights_only 默认值变化
    try:
        import torch
        _orig_torch_load = torch.load
        def _torch_load_weights_false(*args, **kwargs):
            kwargs.setdefault("weights_only", False)
            return _orig_torch_load(*args, **kwargs)
        torch.load = _torch_load_weights_false
    except Exception:
        pass
    # torchaudio 高版本兼容：改用 soundfile
    try:
        import torch
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
    from TTS.api import TTS
    print("🎙️ 正在加载 XTTS v2 本地真声模型（首次约 3-5 秒）...")
    _XTTS_MODEL = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
    return _XTTS_MODEL


def _xtts_generate(text: str, audio_path: Path) -> dict[str, Any]:
    """本地 XTTS v2 真声生成。"""
    tts = _get_xtts_model()
    tts.tts_to_file(text=text, speaker_wav=str(REFERENCE_WAV), language="zh", file_path=str(audio_path))
    return {"ok": True, "audio_file": f"/tts-outputs/{audio_path.name}", "absolute_path": str(audio_path),
            "voice": "xtts-v2-uid9622", "note": "本地 XTTS v2 UID9622 真声克隆"}


class RemixRequest(BaseModel):
    video_file: str
    captions: str
    aigc: bool = True


class SageRequest(BaseModel):
    question: str
    sages: str = "伏羲,诸葛亮,曾老师"


class WechatExportRequest(BaseModel):
    video_file: str
    captions: str
    aigc: bool = True


@app.post("/api/draft")
def api_draft(req: TopicRequest):
    text = generate(req.topic)
    record = save_text_output("draft", req.topic, text)
    return {"ok": True, "type": "draft", "topic": req.topic, "content": text,
            "dna": record["dna"], "file_path": record["file_path"]}


@app.post("/api/reading")
def api_reading(req: TopicRequest):
    text = generate_reading(req.topic)
    record = save_text_output("reading", req.topic, text)
    return {"ok": True, "type": "reading", "topic": req.topic, "content": text,
            "dna": record["dna"], "file_path": record["file_path"]}


@app.post("/api/video")
def api_video(req: TopicRequest):
    text = generate_video_script(req.topic)
    record = save_text_output("video", req.topic, text)
    return {"ok": True, "type": "video", "topic": req.topic, "content": text,
            "dna": record["dna"], "file_path": record["file_path"]}


@app.post("/api/captions")
def api_captions(req: TopicRequest):
    text = generate_captions(req.topic)
    record = save_text_output("captions", req.topic, text)
    return {"ok": True, "type": "captions", "topic": req.topic, "content": text,
            "dna": record["dna"], "file_path": record["file_path"]}


@app.post("/api/remix")
def api_remix(req: RemixRequest):
    video_path = DOWNLOADS_DIR / req.video_file
    if not video_path.exists():
        return JSONResponse(status_code=404, content={"ok": False, "error": f"找不到视频: {req.video_file}"})
    captions = [c.strip() for c in req.captions.split("|") if c.strip()]
    if not captions:
        return JSONResponse(status_code=400, content={"ok": False, "error": "字幕不能为空"})
    timestamp = datetime.now().strftime("%H%M%S")
    out_filename = f"{video_path.stem}_web_remixed_{timestamp}.mp4"
    out_path = OUTPUT_DIR / out_filename
    try:
        add_captions_to_video(video_path, captions, out_path)
        if req.aigc:
            add_aigc_metadata(out_path)
        return {"ok": True, "type": "remix", "output": f"/remix-outputs/{out_filename}",
                "absolute_path": str(out_path), "aigc": req.aigc}
    except Exception as e:
        return JSONResponse(status_code=500, content={"ok": False, "error": str(e)})


@app.post("/api/sage")
def api_sage(req: SageRequest):
    sages = [s.strip() for s in req.sages.split(",") if s.strip()]
    try:
        text = generate_sage_dialogue(req.question, sages)
        record = save_text_output("sage", req.question, text)
        return {"ok": True, "type": "sage", "sages": sages, "question": req.question,
                "content": text, "dna": record["dna"], "file_path": record["file_path"]}
    except Exception as e:
        return JSONResponse(status_code=500, content={"ok": False, "error": str(e)})


@app.post("/api/export-wechat")
def api_export_wechat(req: WechatExportRequest):
    video_path = DOWNLOADS_DIR / req.video_file
    if not video_path.exists():
        return JSONResponse(status_code=404, content={"ok": False, "error": f"找不到视频: {req.video_file}"})
    captions = [c.strip() for c in req.captions.split("|") if c.strip()]
    if not captions:
        return JSONResponse(status_code=400, content={"ok": False, "error": "字幕不能为空"})
    timestamp = datetime.now().strftime("%H%M%S")
    out_filename = f"{video_path.stem}_wechat_export_{timestamp}.mp4"
    out_path = OUTPUT_DIR / out_filename
    try:
        export_wechat_video(video_path, captions, out_path, add_aigc=req.aigc)
        return {"ok": True, "type": "export-wechat", "output": f"/remix-outputs/{out_filename}",
                "absolute_path": str(out_path), "aigc": req.aigc}
    except Exception as e:
        return JSONResponse(status_code=500, content={"ok": False, "error": str(e)})


@app.post("/api/tts")
def api_tts(req: TTSRequest):
    """TTS 主路径：真声优先（本地 XTTS → Fish Audio 云端），失败回退 edge-tts / Mac say。"""
    text = req.text[:2000]
    safe = "".join(c if c.isalnum() or c in "_-" else "_" for c in req.text)[:20]
    if not safe:
        safe = "preview"
    timestamp = datetime.now().strftime("%H%M%S")

    voice = req.voice.lower()
    use_true_voice = voice in ("xtts-v2-uid9622", "fish-audio-uid9622", "uid9622", "longhun", "真声")

    if use_true_voice:
        # 第一梯队：本地 XTTS v2 真声（已验证可用）
        if voice in ("xtts-v2-uid9622", "uid9622", "longhun", "真声"):
            filename = f"tts_xtts_{safe}_{timestamp}.wav"
            audio_path = TTS_OUTPUT_DIR / filename
            try:
                result = _xtts_generate(text, audio_path)
                result["type"] = "tts"
                result["rate"] = req.rate
                result["volume"] = req.volume
                result["pitch"] = req.pitch
                return result
            except Exception as e:
                print(f"本地 XTTS 真声失败，尝试 Fish Audio: {e}")
        # 第二梯队：Fish Audio 云端真声（需网络通达）
        filename = f"tts_fish_{safe}_{timestamp}.mp3"
        audio_path = TTS_OUTPUT_DIR / filename
        try:
            result = _fish_audio_generate(text, audio_path)
            result["type"] = "tts"
            result["rate"] = req.rate
            result["volume"] = req.volume
            result["pitch"] = req.pitch
            return result
        except Exception as e:
            print(f"Fish Audio 真声失败，回退 edge-tts: {e}")
            filename = f"tts_{safe}_{timestamp}.mp3"
            audio_path = TTS_OUTPUT_DIR / filename
            result = _edge_tts_generate(text, "zh-CN-YunjianNeural", req.rate, req.volume, req.pitch, audio_path)
            result["type"] = "tts"
            result["fallback"] = True
            result["fallback_reason"] = f"真声引擎不可用: {e}"
            return result

    filename = f"tts_{safe}_{timestamp}.mp3"
    audio_path = TTS_OUTPUT_DIR / filename
    result = _edge_tts_generate(text, req.voice, req.rate, req.volume, req.pitch, audio_path)
    result["type"] = "tts"
    return result


@app.get("/")
def index():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/export-session")
def api_export_session():
    """
    一键导出所有已生成的文本内容（草稿/阅读稿/视频脚本/字幕/圣贤对话）为 ZIP。
    视频和音频文件较大，不打包；只打包 manifest 中记录的文本内容。
    """
    manifest = _load_manifest()
    if not manifest:
        return JSONResponse(status_code=404, content={"ok": False, "error": "当前没有可导出的生成内容"})

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"longhun_outputs_{timestamp}.zip"
    zip_path = OUTPUTS_DIR / zip_filename

    included_files = set()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # 写入 manifest
        manifest_info = zipfile.ZipInfo(filename="manifest.json", date_time=datetime.now().timetuple()[:6])
        zf.writestr(manifest_info, json.dumps(manifest, ensure_ascii=False, indent=2))

        # 写入每个文本文件（UTF-8 文件名标记，避免中文乱码）
        for item in manifest:
            fp = Path(item.get("file_path", ""))
            if fp.exists() and fp.is_file() and str(fp) not in included_files:
                arcname = f"{fp.parent.name}/{fp.name}"
                zip_info = zipfile.ZipInfo(filename=arcname, date_time=datetime.now().timetuple()[:6])
                # 0x800 = UTF-8 文件名编码标志
                zip_info.flag_bits |= 0x800
                data = fp.read_bytes()
                zf.writestr(zip_info, data)
                included_files.add(str(fp))

    return {
        "ok": True,
        "type": "export-session",
        "zip_file": f"/output-zips/{zip_filename}",
        "absolute_path": str(zip_path),
        "count": len(included_files),
    }


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/tts-outputs", StaticFiles(directory=TTS_OUTPUT_DIR), name="tts_outputs")
app.mount("/remix-outputs", StaticFiles(directory=OUTPUT_DIR), name="remix_outputs")
app.mount("/output-zips", StaticFiles(directory=OUTPUTS_DIR), name="output_zips")


if __name__ == "__main__":
    import uvicorn
    print("🐉 龍魂真声控制台启动：http://localhost:9623")
    uvicorn.run(app, host="127.0.0.1", port=9623)
