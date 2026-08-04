#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
龍魂 · 声影桥 v1.0
中国文化沉浸式知识矩阵的语音 / 视频 / AI 对话后端
DNA: #龍芯⚡️2026-07-04-LONGHUN-SHENGYING-BRIDGE-v1.0
协议: CC BY-NC-SA 4.0 · 君子協議
"""

import json
import os
import re
import requests
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile  # type: ignore[import-untyped]
from fastapi.middleware.cors import CORSMiddleware  # type: ignore[import-untyped]
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles  # type: ignore[import-untyped]
from pydantic import BaseModel, Field

# ═══════════════════════════════════════════════════════════
# 常量 / 路径
# ═══════════════════════════════════════════════════════════
DNA = "#龍芯⚡️2026-07-04-LONGHUN-SHENGYING-BRIDGE-v1.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
VERSION = "1.0.0"

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CACHE_DIR = BASE_DIR / "cache"
LOGS_DIR = BASE_DIR / "logs"
CHAPTER_FILE = DATA_DIR / "中国文化章节.json"
AUDIT_FILE = LOGS_DIR / "声影桥_audit.jsonl"

CACHE_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# 语音映射
VOICE_MAP = {
    "古风男声": "zh-CN-YunxiNeural",
    "古风女声": "zh-CN-XiaoxiaoNeural",
    "专业男声": "zh-CN-YunyangNeural",
    "活泼女声": "zh-CN-XiaoyiNeural",
}
DEFAULT_VOICE = "古风男声"

# 启动时间
START_AT = time.time()

# ═══════════════════════════════════════════════════════════
# 加载章节数据
# ═══════════════════════════════════════════════════════════
with open(CHAPTER_FILE, "r", encoding="utf-8") as f:
    CHAPTER_DATA = json.load(f)

CHAPTER_META = CHAPTER_DATA.get("metadata", {})
CHAPTERS: Dict[str, Dict[str, Any]] = {
    c["id"]: c for c in CHAPTER_DATA.get("chapters", [])
}

# ═══════════════════════════════════════════════════════════
# FastAPI 应用
# ═══════════════════════════════════════════════════════════
app = FastAPI(
    title="龍魂 · 声影桥",
    version=VERSION,
    description="中国文化沉浸式知识矩阵 · 语音/视频/对话 API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8766", "http://127.0.0.1:8766"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-DNA-TRACE"],
)

# 静态资源：cache 目录暴露为 /media
app.mount("/media", StaticFiles(directory=str(CACHE_DIR)), name="media")


# ═══════════════════════════════════════════════════════════
# 工具函数
# ═══════════════════════════════════════════════════════════
def now_iso() -> str:
    return datetime.now().isoformat()


def audit(颜色: str, 动作: str, 元数据: Optional[Dict[str, Any]] = None):
    """写入三色审计日志"""
    entry = {
        "时间戳": now_iso(),
        "颜色": 颜色,
        "动作": 动作,
        "DNA": DNA,
        "元数据": 元数据 or {},
    }
    with open(AUDIT_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def make_media_filename(ext: str) -> str:
    return f"{uuid.uuid4().hex[:16]}.{ext}"


def tts_with_edge(text: str, voice_name: str) -> Path:
    """调用 edge-tts 命令生成 MP3"""
    voice = VOICE_MAP.get(voice_name, VOICE_MAP[DEFAULT_VOICE])
    out_name = make_media_filename("mp3")
    out_path = CACHE_DIR / out_name
    cmd = [
        "edge-tts",
        "--voice", voice,
        "--text", text,
        "--write-media", str(out_path),
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=120)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        raise RuntimeError(f"edge-tts 失败: {e}")
    return out_path


def tts_with_say(text: str) -> Path:
    """macOS say 兜底，生成 aiff 后转 mp3（如 ffmpeg 可用）"""
    out_name = make_media_filename("mp3")
    out_path = CACHE_DIR / out_name
    tmp_aiff = CACHE_DIR / make_media_filename("aiff")
    voice = "Tingting"
    subprocess.run(["say", "-v", voice, "-o", str(tmp_aiff), text], check=True, capture_output=True, timeout=60)
    if shutil.which("ffmpeg"):
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(tmp_aiff), "-ar", "24000", "-ac", "1", str(out_path)],
            check=True, capture_output=True, timeout=60
        )
        tmp_aiff.unlink(missing_ok=True)
    else:
        # 无 ffmpeg 时直接返回 aiff，前端也可能播放
        out_path = tmp_aiff
    return out_path


def generate_tts(text: str, voice_name: str = DEFAULT_VOICE) -> str:
    """生成 TTS，返回可访问的 /media 相对路径"""
    try:
        out_path = tts_with_edge(text, voice_name)
        audit("绿", "TTS生成成功", {"引擎": "edge-tts", "voice": voice_name, "file": out_path.name})
    except Exception as e:
        out_path = tts_with_say(text)
        audit("黄", "TTS降级say", {"原因": str(e), "file": out_path.name})
    return f"/media/{out_path.name}"


# ═══════════════════════════════════════════════════════════
# ASR 初始化（延迟，避免启动过慢）
# ═══════════════════════════════════════════════════════════
_asr_engine = None


def get_asr_engine():
    global _asr_engine
    if _asr_engine is None:
        asr_script = Path.home() / ".kimi-code/skills/longhun-asr/scripts/语音识别引擎.py"
        if asr_script.exists():
            sys.path.insert(0, str(asr_script.parent))
            import importlib.util
            spec = importlib.util.spec_from_file_location("语音识别引擎", str(asr_script))
            if spec is None or spec.loader is None:
                _asr_engine = None  # sentinel: 引擎不可用
                return _asr_engine
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            # 使用模拟模式，避免加载外部模型
            _asr_engine = module.龍音ASR引擎(模式="模拟模式")
        else:
            _asr_engine = None  # sentinel: 脚本不存在
    return _asr_engine


# ═══════════════════════════════════════════════════════════
# 简单对话逻辑
# ═══════════════════════════════════════════════════════════
def chat_reply(prompt: str, context: Optional[List[Dict[str, str]]] = None) -> str:
    """基于章节关键词做本地回复"""
    p = prompt.lower()

    # 命中章节关键词
    for cid, ch in CHAPTERS.items():
        for kw in ch["keywords"]:
            if kw in p:
                return (
                    f"{ch['title']}。{ch['voice_script']} "
                    f"若欲深究其理，可再问我：{', '.join(ch['keywords'][:3])}。"
                )

    # 通用问候
    if any(w in p for w in ["你好", "是谁", "名字", "自我介绍"]):
        return (
            "吾乃龍魂之声影桥也，承 UID9622 之命，以三才为骨、易经为脉、道德经为魂，"
            "为君朗读中国文化，解析知识矩阵，亦可实时对话。"
        )

    # 通用能力
    if any(w in p for w in ["能干", "做什么", "功能", "怎么用"]):
        return (
            "我可朗读三六九、河图洛书、太极、易经、道德经；可点击矩阵节点听其要义；"
            "亦可按住麦克风与我对谈，或一键生成讲解视频。"
        )

    return (
        "此问甚妙，声影桥尚未习得确切答案。君可换个说法，或从左侧章节中择一而入，"
        "吾当以古音为君诵读。"
    )


# ═══════════════════════════════════════════════════════════
# Pydantic 模型
# ═══════════════════════════════════════════════════════════
class TTSRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)
    voice: str = DEFAULT_VOICE


class ChatRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=2000)
    context: List[Dict[str, str]] = []


class NarrateRequest(BaseModel):
    chapter_id: str
    voice: str = DEFAULT_VOICE


class NotionPushRequest(BaseModel):
    chapter_id: str
    dry_run: bool = True


class NotionPullRequest(BaseModel):
    query: str = "龍魂 章节"
    page_size: int = 10


class VideoMuxRequest(BaseModel):
    audio_url: str
    # video 字段通过 UploadFile 上传


# ═══════════════════════════════════════════════════════════
# API 路由
# ═══════════════════════════════════════════════════════════
@app.get("/health")
def health():
    return {
        "status": "ok",
        "version": VERSION,
        "dna": DNA,
        "confirm": CONFIRM,
        "uptime": round(time.time() - START_AT, 3),
        "chapters": len(CHAPTERS),
    }


@app.get("/chapters")
def list_chapters():
    return {
        "dna": DNA,
        "metadata": CHAPTER_META,
        "chapters": list(CHAPTERS.values()),
    }


@app.get("/chapters/{chapter_id}")
def get_chapter(chapter_id: str):
    if chapter_id not in CHAPTERS:
        raise HTTPException(status_code=404, detail="章节不存在")
    return {"dna": DNA, "chapter": CHAPTERS[chapter_id]}


@app.post("/tts")
def tts(req: TTSRequest, request: Request):
    if req.voice not in VOICE_MAP:
        req.voice = DEFAULT_VOICE
    audio_url = generate_tts(req.text, req.voice)
    full_url = f"{request.base_url.scheme}://{request.base_url.netloc}{audio_url}"
    audit("绿", "TTS接口调用", {"voice": req.voice, "text_len": len(req.text)})
    return {"status": "ok", "audio_url": audio_url, "full_url": full_url, "dna": DNA}


@app.post("/asr")
def asr(audio: UploadFile = File(...)):
    """语音识别（当前为模拟/兜底模式）"""
    suffix = Path(audio.filename or "rec.wav").suffix or ".wav"
    tmp_path = CACHE_DIR / make_media_filename(suffix.lstrip("."))
    with open(tmp_path, "wb") as f:
        shutil.copyfileobj(audio.file, f)

    engine = get_asr_engine()
    text = ""
    confidence = 0.0
    engine_name = "none"
    if engine:
        try:
            结果 = engine.识别音频(str(tmp_path), "zh")
            text = getattr(结果, "文本", "")
            confidence = getattr(结果, "置信度", 0.0)
            engine_name = getattr(结果, "引擎", "longhun-asr")
        except Exception as e:
            text = f"识别出错: {e}"
            audit("红", "ASR识别失败", {"error": str(e)})
    else:
        text = "龍音ASR引擎未找到，已使用浏览器识别兜底。"
        engine_name = "browser-fallback"

    audit("绿", "ASR接口调用", {"engine": engine_name, "text": text, "conf": confidence})
    return {"status": "ok", "text": text, "confidence": confidence, "engine": engine_name, "dna": DNA}


@app.post("/chat")
def chat(req: ChatRequest):
    reply = chat_reply(req.prompt, req.context)
    audit("绿", "对话接口调用", {"prompt": req.prompt[:50], "reply_len": len(reply)})
    return {"status": "ok", "reply": reply, "dna": DNA}


@app.post("/narrate")
def narrate(req: NarrateRequest, request: Request):
    if req.chapter_id not in CHAPTERS:
        raise HTTPException(status_code=404, detail="章节不存在")
    ch = CHAPTERS[req.chapter_id]
    audio_url = generate_tts(ch["voice_script"], req.voice)
    full_url = f"{request.base_url.scheme}://{request.base_url.netloc}{audio_url}"
    audit("绿", "章节朗读", {"chapter": req.chapter_id, "voice": req.voice})
    return {
        "status": "ok",
        "chapter_id": req.chapter_id,
        "title": ch["title"],
        "voice_script": ch["voice_script"],
        "audio_url": audio_url,
        "full_url": full_url,
        "dna": DNA,
    }


@app.post("/video/mux")
def video_mux(audio_url: str = Form(...), video: UploadFile = File(...), request: Request = None):
    """将视频 webm 与音频 mp3 混流为 MP4"""
    if not audio_url.startswith("/media/"):
        raise HTTPException(status_code=400, detail="audio_url 格式错误")

    audio_name = audio_url.replace("/media/", "").split("?")[0]
    audio_path = CACHE_DIR / audio_name
    if not audio_path.exists():
        raise HTTPException(status_code=404, detail="音频文件不存在")

    video_suffix = Path(video.filename or "clip.webm").suffix or ".webm"
    video_name = make_media_filename(video_suffix.lstrip("."))
    video_path = CACHE_DIR / video_name
    with open(video_path, "wb") as f:
        shutil.copyfileobj(video.file, f)

    out_name = make_media_filename("mp4")
    out_path = CACHE_DIR / out_name

    ffmpeg = shutil.which("ffmpeg") or "/opt/homebrew/bin/ffmpeg"
    cmd = [
        ffmpeg, "-y",
        "-i", str(video_path),
        "-i", str(audio_path),
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "128k",
        "-shortest",
        str(out_path),
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True, timeout=120)
    except subprocess.CalledProcessError as e:
        audit("红", "视频混流失败", {"error": e.stderr.decode("utf-8", errors="ignore")[:200]})
        raise HTTPException(status_code=500, detail="视频混流失败")

    # 清理临时 webm
    video_path.unlink(missing_ok=True)

    out_url = f"/media/{out_path.name}"
    full_url = f"{request.base_url.scheme}://{request.base_url.netloc}{out_url}"
    audit("绿", "视频混流成功", {"audio": audio_name, "video": out_name})
    return {"status": "ok", "video_url": out_url, "full_url": full_url, "dna": DNA}


# ═══════════════════════════════════════════════════════════
# Notion 双向同步
# ═══════════════════════════════════════════════════════════
NOTION_TOKEN = os.environ.get("NOTION_TOKEN") or os.environ.get("LONGHUN_NOTION_API_KEY")
NOTION_API_BASE = "https://api.notion.com/v1"
NOTION_PARENT_PAGE = os.environ.get("LONGHUN_NOTION_PARENT_PAGE", "6c03f9ad-afd9-4ce8-bf98-f8439eb9dbbf")
NOTION_VERSION = "2022-06-28"


def notion_headers():
    return {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }


def build_chapter_page(ch: Dict[str, Any], dry_run: bool = True) -> Dict[str, Any]:
    """把本地章节构造为 Notion page payload"""
    title = ch.get("title", "未命名章节")
    payload = {
        "parent": {"page_id": NOTION_PARENT_PAGE},
        "icon": {"emoji": "📜"},
        "properties": {
            "title": {"title": [{"text": {"content": f"龍魂 · {title}"}}]}
        },
        "children": [
            {"object": "block", "type": "heading_1", "heading_1": {"rich_text": [{"text": {"content": ch.get("title", "")}}]}},
            {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": f"副标题：{ch.get('subtitle', '')} | 朝代：{ch.get('era', '')}"}}]}},
            {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": f"视觉主题：{ch.get('visual_theme', '')}"}}]}},
            {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "原文"}}]}},
            {"object": "block", "type": "quote", "quote": {"rich_text": [{"text": {"content": ch.get("classical_text", "")}}]}},
            {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "白话"}}]}},
            {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": ch.get("modern_text", "")}}]}},
            {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "朗读稿"}}]}},
            {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": ch.get("voice_script", "")}}]}},
            {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "视觉不动点"}}]}},
            {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": f"印章文字：{ch.get('seal_text', '')}"}}]}},
            {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": f"推荐字体：{ch.get('font_family', '')}"}}]}},
            {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": f"主色：{ch.get('color_primary', '')} | 辅色：{ch.get('color_secondary', '')}"}}]}},
            {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": f"来源标注：{ch.get('attribution', '')}"}}]}},
            {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": f"本地页面：龍魂-{ch.get('id')}.html"}}]}},
            {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": f"不动点 DNA：{ch.get('visual_anchor_dna', '')}"}}]}},
        ]
    }
    return payload


@app.post("/notion/pull")
def notion_pull(req: NotionPullRequest):
    """从 Notion 拉取与龍魂章节相关的页面"""
    if not NOTION_TOKEN:
        return {
            "status": "ok",
            "mode": "local_fallback",
            "warning": "未配置 NOTION_TOKEN，返回本地章节数据",
            "local_chapters": list(CHAPTERS.values()),
            "dna": DNA,
        }
    try:
        r = requests.post(
            f"{NOTION_API_BASE}/search",
            headers=notion_headers(),
            json={"query": req.query, "page_size": req.page_size},
            timeout=20,
        )
        r.raise_for_status()
        data = r.json()
        pages = [
            {
                "id": p.get("id"),
                "title": p.get("properties", {}).get("title", {}).get("title", [{}])[0].get("text", {}).get("content", ""),
                "url": p.get("url"),
                "last_edited": p.get("last_edited_time"),
            }
            for p in data.get("results", [])
        ]
        audit("绿", "Notion拉取成功", {"query": req.query, "count": len(pages)})
        return {
            "status": "ok",
            "mode": "notion_api",
            "query": req.query,
            "pages": pages,
            "local_chapters": list(CHAPTERS.values()),
            "dna": DNA,
        }
    except Exception as e:
        audit("红", "Notion拉取失败", {"error": str(e)})
        return {
            "status": "error",
            "error": str(e),
            "local_chapters": list(CHAPTERS.values()),
            "dna": DNA,
        }


@app.post("/notion/push")
def notion_push(req: NotionPushRequest):
    """把本地章节推送到 Notion"""
    if req.chapter_id not in CHAPTERS:
        raise HTTPException(status_code=404, detail="章节不存在")
    ch = CHAPTERS[req.chapter_id]
    payload = build_chapter_page(ch, dry_run=req.dry_run)

    if req.dry_run:
        audit("绿", "Notion推送演练", {"chapter": req.chapter_id, "dry_run": True})
        return {
            "status": "ok",
            "mode": "dry_run",
            "chapter_id": req.chapter_id,
            "title": ch["title"],
            "would_create_page": True,
            "payload_size": len(json.dumps(payload)),
            "payload_preview": payload,
            "note": "dry_run=true，未真正创建 Notion 页面。如需真实推送，请传 dry_run=false",
            "dna": DNA,
        }

    if not NOTION_TOKEN:
        raise HTTPException(status_code=400, detail="未配置 NOTION_TOKEN，无法真实推送")

    try:
        r = requests.post(
            f"{NOTION_API_BASE}/pages",
            headers=notion_headers(),
            json=payload,
            timeout=30,
        )
        r.raise_for_status()
        result = r.json()
        audit("绿", "Notion推送成功", {"chapter": req.chapter_id, "notion_page_id": result.get("id")})
        return {
            "status": "ok",
            "mode": "notion_api",
            "chapter_id": req.chapter_id,
            "notion_page_id": result.get("id"),
            "notion_url": result.get("url"),
            "dna": DNA,
        }
    except Exception as e:
        audit("红", "Notion推送失败", {"chapter": req.chapter_id, "error": str(e)})
        raise HTTPException(status_code=500, detail=f"Notion 推送失败: {e}")


@app.get("/")
def root():
    return {
        "service": "龍魂 · 声影桥",
        "version": VERSION,
        "dna": DNA,
        "apis": ["/health", "/chapters", "/tts", "/asr", "/chat", "/narrate", "/video/mux", "/notion/pull", "/notion/push"],
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("SHENGYING_PORT", "8766"))
    audit("绿", "声影桥启动", {"port": port})
    uvicorn.run(app, host="127.0.0.1", port=port)
