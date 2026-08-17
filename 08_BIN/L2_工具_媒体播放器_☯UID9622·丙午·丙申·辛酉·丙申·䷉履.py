#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂生态 · 全媒体播放器 v1.1
# 层级: L2_工具层
# DNA: #龍芯⚡️丙午·丙申·辛酉·酉时·䷦蹇-MEDIA-PLAYER-REFINE-V1.1-P0-714d6fd6
# 别名: bin/lh_media_player.py
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 三色: 🟢 通过

功能：
  1. 本地播放视频（mpv / ffplay / vlc）
  2. 提取关键帧并 OCR 识别画面文字，自动去重并跳过无文字帧
  3. 提取音频并 ASR 识别语音，保留分段时间戳并生成准确 WebVTT
  4. 生成可嵌入网页的 Video.js 播放器 + 字幕/文稿叠加
  5. 批量处理视频目录
  6. 支持缓存、配置文件、状态检查与 Python logging 日志
"""

import argparse
import json
import logging
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from bin.ganzhi_dna_engine import DNA生成

# ============================================================
# 项目路径
# ============================================================
PROJECT_DIR = Path(__file__).resolve().parent.parent
BIN_DIR = PROJECT_DIR / "bin"
AUDIT_DIR = PROJECT_DIR / "04_AUDIT"
OUTPUT_DIR = PROJECT_DIR / "08_STATE" / "media_player"
WEB_PLAYER_DIR = PROJECT_DIR / "web_apps" / "longhun-media-player"

AUDIT_FILE = AUDIT_DIR / "media_player.jsonl"
CONFIG_FILE = Path.home() / ".longhun" / "media_player.json"

logger = logging.getLogger("lh_media_player")

DEFAULT_CONFIG = {
    "player": None,
    "interval": 5.0,
    "model_size": "base",
    "language": "zh",
}


# ============================================================
# DNA + 审计
# ============================================================
def make_dna(动作: str, 内容锚点: str = "") -> str:
    """生成 v∞ 干支卦 DNA 追溯码"""
    return DNA生成(
        模块="MEDIA-PLAYER",
        动作=动作,
        版本="V1.1",
        级别="P0",
        内容锚点=内容锚点,
    )


def record_audit(operation: str, detail: Any, status: str = "ok"):
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": datetime.now().isoformat(),
        "dna": make_dna(operation, 内容锚点=str(operation)),
        "operation": operation,
        "detail": detail,
        "status": status,
    }
    with open(AUDIT_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# ============================================================
# 配置
# ============================================================
def load_config(config_path: Optional[Path] = None) -> Dict[str, Any]:
    """读取 ~/.longhun/media_player.json，缺失键使用默认值"""
    cfg = dict(DEFAULT_CONFIG)
    path = config_path or CONFIG_FILE
    if path.exists():
        try:
            user_cfg = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(user_cfg, dict):
                cfg.update(user_cfg)
                logger.debug("已加载配置: %s", path)
        except Exception as e:
            logger.warning("配置文件解析失败 %s: %s", path, e)
    return cfg


def resolve_arg(args: argparse.Namespace, name: str, config: Dict[str, Any]) -> Any:
    """CLI 参数优先，其次配置文件，最后默认值"""
    val = getattr(args, name, None)
    if val is not None:
        return val
    return config.get(name, DEFAULT_CONFIG.get(name))


# ============================================================
# 工具函数
# ============================================================
def run_shell(cmd: str, timeout: int = 120) -> Dict[str, Any]:
    logger.debug("$ %s", cmd)
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=timeout
        )
        return {
            "ok": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "cmd": cmd,
        }
    except Exception as e:
        return {"ok": False, "error": str(e), "cmd": cmd}


def which(tool: str) -> Optional[str]:
    return shutil.which(tool)


def _video_work_dir(video_path: Path, output_dir_override: Optional[Path] = None) -> Path:
    base = output_dir_override or OUTPUT_DIR
    return Path(base) / video_path.stem


def _is_cache_valid(output_path: Path, source_path: Path) -> bool:
    """当输出文件存在、非空且修改时间不早于源文件时视为有效缓存"""
    if not output_path.exists():
        return False
    if output_path.stat().st_size == 0:
        return False
    if not source_path.exists():
        return False
    return output_path.stat().st_mtime >= source_path.stat().st_mtime


def _write_json(path: Path, data: Any):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def format_time(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}"


def get_video_duration(video_path: Path) -> float:
    ffprobe = which("ffprobe")
    if not ffprobe:
        return 0.0
    cmd = (
        f'ffprobe -v error -show_entries format=duration '
        f'-of default=noprint_wrappers=1:nokey=1 "{video_path}"'
    )
    result = run_shell(cmd, timeout=30)
    try:
        return float(result["stdout"])
    except Exception:
        return 0.0


# ============================================================
# 播放器
# ============================================================
def play_video(video_path: Path, player: Optional[str] = None) -> bool:
    """使用系统播放器播放视频"""
    if not video_path.exists():
        logger.error("视频不存在: %s", video_path)
        return False

    players = [player] if player else ["mpv", "ffplay", "vlc"]
    for p in players:
        exe = which(p)
        if exe:
            logger.info("🎬 使用 %s 播放: %s", p, video_path)
            subprocess.run([exe, str(video_path)])
            record_audit("play", {"player": p, "file": str(video_path)})
            return True

    logger.error("未找到可用播放器，请安装 mpv / ffplay / vlc 之一")
    return False


# ============================================================
# 帧提取 + OCR
# ============================================================
def _frames_marker(frames_dir: Path) -> Path:
    return frames_dir / ".frames_extracted"


def extract_frames(
    video_path: Path,
    output_dir: Path,
    interval: float = 5.0,
    force: bool = False,
) -> List[Path]:
    """按间隔提取视频帧，支持缓存跳过"""
    output_dir.mkdir(parents=True, exist_ok=True)
    marker = _frames_marker(output_dir)
    frames = sorted(output_dir.glob("frame_*.jpg"))

    if (
        not force
        and frames
        and marker.exists()
        and _is_cache_valid(marker, video_path)
    ):
        try:
            info = json.loads(marker.read_text(encoding="utf-8"))
            if info.get("interval") == interval:
                logger.info("帧缓存命中，跳过提取（%d 帧）", len(frames))
                return frames
        except Exception:
            pass

    # 清理旧帧
    for f in output_dir.glob("frame_*.jpg"):
        f.unlink()
    if marker.exists():
        marker.unlink()

    ffmpeg = which("ffmpeg")
    if not ffmpeg:
        logger.warning("未安装 ffmpeg，跳过帧提取")
        return []

    cmd = (
        f'ffmpeg -i "{video_path}" -vf "fps=1/{interval},scale=1280:-1" '
        f'-q:v 2 "{output_dir}/frame_%04d.jpg" -y'
    )
    result = run_shell(cmd, timeout=300)
    if not result["ok"]:
        logger.warning("帧提取失败: %s", result.get("stderr", "")[:200])
        return []

    frames = sorted(output_dir.glob("frame_*.jpg"))
    logger.info("已提取 %d 帧", len(frames))
    _write_json(marker, {"interval": interval, "source_mtime": video_path.stat().st_mtime})
    return frames


def ocr_frame(frame_path: Path) -> Dict[str, Any]:
    """对单帧进行 OCR，优先尝试 Tesseract，再 PaddleOCR"""
    # 1. 尝试 Tesseract
    tesseract = which("tesseract")
    if tesseract:
        cmd = f'{tesseract} "{frame_path}" stdout -l chi_sim+eng 2>/dev/null'
        result = run_shell(cmd, timeout=30)
        if result["ok"]:
            text = result["stdout"].strip()
            if text:
                return {"provider": "tesseract", "text": text}
            return {"provider": "tesseract", "text": "[画面未识别到文字]"}

    # 2. 尝试 PaddleOCR（如果已安装）
    try:
        from paddleocr import PaddleOCR
        ocr = PaddleOCR(use_angle_cls=True, lang="ch", show_log=False)
        result = ocr.ocr(str(frame_path), cls=True)
        texts = []
        if result and result[0]:
            for line in result[0]:
                texts.append(line[1][0])
        return {
            "provider": "paddleocr",
            "text": "\n".join(texts) if texts else "[画面未识别到文字]",
        }
    except Exception:
        pass

    # 3. 兜底：返回提示
    return {"provider": "none", "text": "[未检测到 OCR 引擎，请安装 tesseract 或 paddleocr]"}


def filter_ocr_results(raw_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """OCR 后处理：去重连续相同文本，并跳过无文字帧"""
    filtered: List[Dict[str, Any]] = []
    last_text: Optional[str] = None
    no_text_marker = "[画面未识别到文字]"
    for item in raw_results:
        text = item.get("text", "")
        if text == no_text_marker:
            continue
        if text == last_text:
            continue
        last_text = text
        filtered.append(item)
    return filtered


def run_ocr(
    video_path: Path,
    interval: float = 5.0,
    force: bool = False,
    output_dir: Optional[Path] = None,
) -> List[Dict[str, Any]]:
    """对视频按间隔 OCR，支持缓存"""
    work_dir = _video_work_dir(video_path, output_dir)
    frames_dir = work_dir / "frames"
    ocr_json = work_dir / "ocr.json"

    if not force and _is_cache_valid(ocr_json, video_path):
        logger.info("OCR 缓存命中: %s", ocr_json)
        try:
            return json.loads(ocr_json.read_text(encoding="utf-8"))
        except Exception as e:
            logger.warning("OCR 缓存读取失败，将重新识别: %s", e)

    frames = extract_frames(video_path, frames_dir, interval, force)
    raw_results: List[Dict[str, Any]] = []
    for i, frame in enumerate(frames):
        ts = i * interval
        res = ocr_frame(frame)
        raw_results.append({
            "time": ts,
            "frame": str(frame.relative_to(PROJECT_DIR)),
            "provider": res["provider"],
            "text": res["text"],
        })
        logger.info(
            "   [%6.1fs] %s: %s",
            ts,
            res["provider"],
            res["text"][:60].replace("\n", " "),
        )

    results = filter_ocr_results(raw_results)
    _write_json(ocr_json, results)
    logger.info("OCR 完成，有效结果 %d / %d", len(results), len(raw_results))
    return results


# ============================================================
# 音频提取 + ASR
# ============================================================
def extract_audio(
    video_path: Path,
    audio_path: Path,
    force: bool = False,
) -> bool:
    """提取音频为 wav，支持缓存"""
    if not force and _is_cache_valid(audio_path, video_path):
        logger.info("音频缓存命中，跳过提取: %s", audio_path)
        return True

    ffmpeg = which("ffmpeg")
    if not ffmpeg:
        logger.warning("未安装 ffmpeg，跳过音频提取")
        return False

    cmd = (
        f'ffmpeg -i "{video_path}" -vn -acodec pcm_s16le -ar 16000 -ac 1 '
        f'"{audio_path}" -y'
    )
    result = run_shell(cmd, timeout=300)
    return result["ok"]


def _srt_time_to_seconds(t: str) -> float:
    """把 SRT 时间戳 00:00:01,234 或 00:00:01.234 转为秒"""
    t = t.strip().replace(",", ".")
    parts = t.split(":")
    if len(parts) != 3:
        return 0.0
    h, m, s = parts
    return int(h) * 3600 + int(m) * 60 + float(s)


def parse_srt(srt_text: str) -> List[Dict[str, Any]]:
    """解析 SRT 字幕为段列表"""
    segments: List[Dict[str, Any]] = []
    blocks = re.split(r"\n\s*\n", srt_text.strip())
    for block in blocks:
        lines = [ln.strip() for ln in block.splitlines() if ln.strip()]
        if len(lines) < 2:
            continue
        m = re.match(
            r"(\d+:\d+:\d+[,.]\d+)\s*-->\s*(\d+:\d+:\d+[,.]\d+)",
            lines[1],
        )
        if not m:
            continue
        start = _srt_time_to_seconds(m.group(1))
        end = _srt_time_to_seconds(m.group(2))
        text = " ".join(lines[2:]).strip()
        if text:
            segments.append({"start": start, "end": end, "text": text})
    return segments


def _segments_to_text(segments: List[Dict[str, Any]]) -> str:
    return "\n".join(
        f"[{seg['start']:.1f}s] {seg['text']}" for seg in segments
    )


def asr_audio(
    audio_path: Path,
    model_size: str = "base",
    language: str = "zh",
) -> Dict[str, Any]:
    """对音频进行 ASR，返回带时间戳的段列表"""
    segments: List[Dict[str, Any]] = []
    provider = "none"

    # 1. faster-whisper
    try:
        from faster_whisper import WhisperModel
        model = WhisperModel(model_size, device="cpu", compute_type="int8")
        segs, _ = model.transcribe(str(audio_path), language=language, beam_size=5)
        for seg in segs:
            segments.append({"start": seg.start, "end": seg.end, "text": seg.text.strip()})
        provider = "faster-whisper"
        return {
            "provider": provider,
            "text": _segments_to_text(segments),
            "segments": segments,
        }
    except Exception as e:
        logger.debug("faster-whisper 不可用: %s", e)

    # 2. openai-whisper Python 包
    try:
        import whisper
        model = whisper.load_model(model_size)
        result = model.transcribe(str(audio_path), language=language)
        for seg in result.get("segments", []):
            segments.append({
                "start": seg["start"],
                "end": seg["end"],
                "text": seg["text"].strip(),
            })
        provider = "whisper"
        return {
            "provider": provider,
            "text": _segments_to_text(segments),
            "segments": segments,
        }
    except Exception as e:
        logger.debug("openai-whisper 不可用: %s", e)

    # 3. whisper CLI（Homebrew 等安装）
    whisper_cli = which("whisper")
    if whisper_cli:
        out_dir = audio_path.parent / "whisper_out"
        out_dir.mkdir(parents=True, exist_ok=True)
        cmd = (
            f'{whisper_cli} "{audio_path}" --model {model_size} --language {language} '
            f'--output_dir "{out_dir}" --output_format srt --verbose False'
        )
        result = run_shell(cmd, timeout=300)
        srt_file = out_dir / f"{audio_path.stem}.srt"
        if srt_file.exists():
            srt_text = srt_file.read_text(encoding="utf-8")
            segments = parse_srt(srt_text)
            provider = "whisper-cli"
            return {
                "provider": provider,
                "text": _segments_to_text(segments),
                "segments": segments,
            }

    # 4. 兜底
    return {
        "provider": "none",
        "text": "[未检测到 ASR 引擎，请安装 faster-whisper、openai-whisper 或 whisper CLI]",
        "segments": [],
    }


def run_asr(
    video_path: Path,
    force: bool = False,
    model_size: str = "base",
    language: str = "zh",
    output_dir: Optional[Path] = None,
) -> Dict[str, Any]:
    """对视频进行 ASR，支持缓存"""
    work_dir = _video_work_dir(video_path, output_dir)
    work_dir.mkdir(parents=True, exist_ok=True)
    audio_path = work_dir / "audio.wav"
    transcript_json = work_dir / "transcript.json"

    if not force and _is_cache_valid(transcript_json, video_path):
        logger.info("ASR 缓存命中: %s", transcript_json)
        try:
            cached = json.loads(transcript_json.read_text(encoding="utf-8"))
            cached.setdefault("segments", [])
            cached.setdefault("text", "")
            return cached
        except Exception as e:
            logger.warning("ASR 缓存读取失败，将重新识别: %s", e)

    if not extract_audio(video_path, audio_path, force):
        return {"provider": "none", "text": "[音频提取失败]", "segments": []}

    logger.info("🎙️ 正在进行语音识别...")
    result = asr_audio(audio_path, model_size, language)
    result.setdefault("video", str(video_path))
    result.setdefault("generated_at", datetime.now().isoformat())
    _write_json(transcript_json, result)
    logger.info("✅ ASR 完成 (%s)，共 %d 段", result["provider"], len(result["segments"]))
    return result


# ============================================================
# 生成 Web 播放器嵌入页
# ============================================================
WEB_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>龍魂播放器 · {{title}}</title>
  <link href="https://vjs.zencdn.net/8.6.1/video-js.css" rel="stylesheet">
  <style>
    body { background: #0a0a0a; color: #eee; font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", sans-serif; margin: 0; padding: 20px; }
    .container { max-width: 960px; margin: 0 auto; }
    h1 { font-size: 1.4rem; margin-bottom: 10px; }
    .dna { color: #888; font-size: 0.8rem; margin-bottom: 20px; word-break: break-all; }
    .video-wrap { border-radius: 8px; overflow: hidden; background: #111; }
    .panel { background: #161616; border-radius: 8px; padding: 16px; margin-top: 16px; }
    .panel h2 { font-size: 1rem; margin: 0 0 10px; color: #0f0; }
    .transcript { line-height: 1.6; font-size: 0.9rem; max-height: 300px; overflow-y: auto; }
    .transcript-line { cursor: pointer; padding: 4px 0; border-bottom: 1px solid #222; }
    .transcript-line:hover { background: #1e1e1e; }
    .transcript-time { color: #0ff; font-size: 0.8rem; margin-right: 8px; }
    .ocr-item { border-bottom: 1px solid #333; padding: 8px 0; }
    .ocr-time { color: #0ff; font-size: 0.8rem; }
    .embed-code { background: #000; padding: 12px; border-radius: 4px; font-family: monospace; font-size: 0.8rem; word-break: break-all; color: #aaa; }
    .copy-btn { margin-top: 8px; padding: 6px 12px; background: #0f0; color: #000; border: none; border-radius: 4px; cursor: pointer; }
    .copy-btn:hover { background: #00cc52; }
  </style>
</head>
<body>
  <div class="container">
    <h1>🐉 龍魂播放器 · {{title}}</h1>
    <div class="dna">{{dna}}</div>

    <div class="video-wrap">
      <video id="longhun-player" class="video-js vjs-big-play-centered" controls preload="auto" width="960" height="540"
        data-setup='{}'>
        <source src="{{video_src}}" type="video/mp4">
        <track kind="captions" src="{{vtt_src}}" srclang="zh" label="中文" default>
      </video>
    </div>

    <div class="panel">
      <h2>🎙️ 语音文稿 (ASR)</h2>
      <div class="transcript">{{asr_html}}</div>
    </div>

    <div class="panel">
      <h2>🖼️ 画面文字识别 (OCR)</h2>
      {{ocr_html}}
    </div>

    <div class="panel">
      <h2>📎 嵌入代码</h2>
      <div class="embed-code" id="embed-code">&lt;iframe src="{{iframe_src}}" width="960" height="800" frameborder="0"&gt;&lt;/iframe&gt;</div>
      <button class="copy-btn" onclick="copyEmbed()">复制嵌入代码</button>
    </div>
  </div>

  <script src="https://vjs.zencdn.net/8.6.1/video.min.js"></script>
  <script>
    var player = videojs('longhun-player');
    function seekTo(t) { player.currentTime(t); player.play(); }
    function copyEmbed() {
      var code = document.getElementById('embed-code').textContent;
      navigator.clipboard.writeText(code).then(function() { alert('嵌入代码已复制'); });
    }
    document.addEventListener('keydown', function(e) {
      if (e.code === 'Space' && e.target.tagName !== 'INPUT' && e.target.tagName !== 'TEXTAREA') {
        e.preventDefault();
        if (player.paused()) { player.play(); } else { player.pause(); }
      }
    });
  </script>
</body>
</html>
"""


def generate_vtt(segments: List[Dict[str, Any]], duration: float = 0.0) -> str:
    """根据 ASR 段生成准确 WebVTT"""
    vtt = ["WEBVTT", ""]
    for seg in segments:
        start = max(0.0, float(seg.get("start", 0)))
        end = float(seg.get("end", 0))
        if duration and end > duration:
            end = duration
        if end <= start:
            continue
        text = str(seg.get("text", "")).strip()
        if not text:
            continue
        vtt.append(f"{format_time(start)} --> {format_time(end)}")
        vtt.append(text)
        vtt.append("")
    return "\n".join(vtt)


def _asr_segments_to_html(segments: List[Dict[str, Any]]) -> str:
    if not segments:
        return "暂无 ASR 结果"
    parts = []
    for seg in segments:
        t = float(seg.get("start", 0))
        text = str(seg.get("text", "")).replace("<", "&lt;").replace(">", "&gt;")
        parts.append(
            f'<div class="transcript-line" onclick="seekTo({t})">'
            f'<span class="transcript-time">[{t:.1f}s]</span>{text}</div>'
        )
    return "\n".join(parts)


def generate_embed(
    video_path: Path,
    asr_result: Dict[str, Any],
    ocr_results: List[Dict[str, Any]],
    output_dir: Optional[Path] = None,
) -> Path:
    """生成嵌入页面"""
    work_dir = _video_work_dir(video_path, output_dir)
    work_dir.mkdir(parents=True, exist_ok=True)

    # 复制视频到输出目录（硬链接优先，失败则复制）
    dest_video = work_dir / video_path.name
    if not dest_video.exists():
        try:
            os.link(video_path, dest_video)
        except Exception:
            shutil.copy2(video_path, dest_video)

    duration = get_video_duration(video_path)
    segments = asr_result.get("segments") or []
    vtt_content = generate_vtt(segments, duration)
    vtt_path = work_dir / "transcript.vtt"
    vtt_path.write_text(vtt_content, encoding="utf-8")

    # 生成 OCR HTML
    ocr_html_parts = []
    for item in ocr_results:
        text = item["text"].replace("<", "&lt;").replace(">", "&gt;")
        ocr_html_parts.append(
            f'<div class="ocr-item"><div class="ocr-time">[{item["time"]:.1f}s]</div><div>{text}</div></div>'
        )
    ocr_html = "\n".join(ocr_html_parts) if ocr_html_parts else "<div>暂无 OCR 结果</div>"

    # 相对路径
    rel_video = f"{video_path.stem}/{video_path.name}"
    rel_vtt = f"{video_path.stem}/transcript.vtt"

    html = WEB_TEMPLATE
    html = html.replace("{{title}}", video_path.stem)
    html = html.replace("{{dna}}", make_dna("EMBED", 内容锚点=video_path.stem))
    html = html.replace("{{video_src}}", rel_video)
    html = html.replace("{{vtt_src}}", rel_vtt)
    html = html.replace("{{asr_html}}", _asr_segments_to_html(segments))
    html = html.replace("{{ocr_html}}", ocr_html)
    html = html.replace("{{iframe_src}}", f"./{video_path.stem}.html")

    base_dir = output_dir or OUTPUT_DIR
    output_html = Path(base_dir) / f"{video_path.stem}.html"
    output_html.write_text(html, encoding="utf-8")

    logger.info("✅ 嵌入页面已生成: %s", output_html)
    logger.info("   视频副本: %s", dest_video)
    logger.info("   字幕文件: %s", vtt_path)

    record_audit("embed", {"html": str(output_html), "video": str(dest_video)})
    return output_html


# ============================================================
# 批量处理
# ============================================================
def batch_process(
    input_dir: Path,
    interval: float = 5.0,
    force: bool = False,
    output_dir: Optional[Path] = None,
    model_size: str = "base",
    language: str = "zh",
):
    videos = (
        list(input_dir.glob("*.mp4"))
        + list(input_dir.glob("*.mov"))
        + list(input_dir.glob("*.mkv"))
        + list(input_dir.glob("*.avi"))
    )
    logger.info("🎬 发现 %d 个视频文件", len(videos))
    for video in videos:
        logger.info("\n%s", "=" * 60)
        logger.info("处理: %s", video)
        process_video(video, interval, force, output_dir, model_size, language)


def process_video(
    video_path: Path,
    interval: float = 5.0,
    force: bool = False,
    output_dir: Optional[Path] = None,
    model_size: str = "base",
    language: str = "zh",
):
    """完整处理单个视频"""
    logger.info("🖼️ 开始 OCR 画面文字识别...")
    ocr_results = run_ocr(video_path, interval, force, output_dir)

    logger.info("\n🎙️ 开始 ASR 语音识别...")
    asr_result = run_asr(video_path, force, model_size, language, output_dir)

    logger.info("\n📄 生成 Web 嵌入页面...")
    html = generate_embed(video_path, asr_result, ocr_results, output_dir)

    # 保存元数据
    meta = {
        "video": str(video_path),
        "dna": make_dna("META", 内容锚点=video_path.stem),
        "asr": asr_result,
        "ocr_count": len(ocr_results),
        "html": str(html),
    }
    work_dir = _video_work_dir(video_path, output_dir)
    meta_path = work_dir / "meta.json"
    _write_json(meta_path, meta)
    logger.info("✅ 元数据已保存: %s", meta_path)

    record_audit("process_video", {"video": str(video_path), "html": str(html)})


# ============================================================
# 状态检查 + 配置展示
# ============================================================
def _tool_status(name: str) -> str:
    exe = which(name)
    if exe:
        return f"✅ {name}: {exe}"
    return f"❌ {name}: 未找到"


def status_cmd():
    """显示外部工具可用性"""
    tools = ["ffmpeg", "ffprobe", "tesseract", "whisper", "mpv", "ffplay", "vlc"]
    logger.info("龍魂媒体播放器 v1.1 · 工具可用性检查")
    for t in tools:
        logger.info(_tool_status(t))

    # 尝试获取 ffmpeg 版本
    ffmpeg = which("ffmpeg")
    if ffmpeg:
        result = run_shell(f'"{ffmpeg}" -version | head -1', timeout=10)
        if result["ok"]:
            logger.info("   %s", result["stdout"])


def config_cmd(config: Dict[str, Any]):
    """打印当前生效配置"""
    logger.info("配置文件路径: %s", CONFIG_FILE)
    logger.info("当前生效配置:\n%s", json.dumps(config, ensure_ascii=False, indent=2))


# ============================================================
# 命令行入口
# ============================================================
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="lh_media_player.py",
        description="🐉 龍魂 · 全媒体播放器 v1.1",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=CONFIG_FILE,
        help="指定配置文件路径（默认 ~/.longhun/media_player.json）",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="覆盖输出目录（默认 08_STATE/media_player）",
    )
    parser.add_argument(
        "--verbose", "--debug",
        action="store_true",
        help="启用 DEBUG 级日志",
    )

    subparsers = parser.add_subparsers(dest="command", metavar="命令")

    def _add_common_opts(sub):
        """全局选项也可放在子命令之后"""
        sub.add_argument(
            "--output-dir",
            type=Path,
            default=None,
            help="覆盖输出目录（默认 08_STATE/media_player）",
        )
        sub.add_argument(
            "--verbose", "--debug",
            action="store_true",
            help="启用 DEBUG 级日志",
        )

    # play
    play = subparsers.add_parser("play", help="本地播放视频")
    play.add_argument("video", type=Path, help="视频文件路径")
    play.add_argument("--player", default=None, help="指定播放器（mpv/ffplay/vlc）")
    _add_common_opts(play)

    # asr
    asr = subparsers.add_parser("asr", help="语音识别")
    asr.add_argument("video", type=Path, help="视频文件路径")
    asr.add_argument("--model-size", default=None, help="whisper 模型大小")
    asr.add_argument("--language", default=None, help="识别语言")
    asr.add_argument("--force", action="store_true", help="强制重新识别")
    _add_common_opts(asr)

    # ocr
    ocr = subparsers.add_parser("ocr", help="画面文字识别")
    ocr.add_argument("video", type=Path, help="视频文件路径")
    ocr.add_argument("--interval", type=float, default=None, help="帧提取间隔（秒）")
    ocr.add_argument("--force", action="store_true", help="强制重新识别")
    _add_common_opts(ocr)

    # process / embed
    process = subparsers.add_parser("process", help="完整处理（ASR + OCR + 嵌入页）")
    process.add_argument("video", type=Path, help="视频文件路径")
    process.add_argument("--interval", type=float, default=None, help="帧提取间隔（秒）")
    process.add_argument("--player", default=None, help="播放用播放器（暂不影响处理）")
    process.add_argument("--model-size", default=None, help="whisper 模型大小")
    process.add_argument("--language", default=None, help="识别语言")
    process.add_argument("--force", action="store_true", help="强制重新处理")
    _add_common_opts(process)

    embed = subparsers.add_parser("embed", help="生成嵌入页（process 别名）")
    embed.add_argument("video", type=Path, help="视频文件路径")
    embed.add_argument("--interval", type=float, default=None, help="帧提取间隔（秒）")
    embed.add_argument("--model-size", default=None, help="whisper 模型大小")
    embed.add_argument("--language", default=None, help="识别语言")
    embed.add_argument("--force", action="store_true", help="强制重新处理")
    _add_common_opts(embed)

    # batch
    batch = subparsers.add_parser("batch", help="批量处理目录")
    batch.add_argument("directory", type=Path, help="视频目录")
    batch.add_argument("--interval", type=float, default=None, help="帧提取间隔（秒）")
    batch.add_argument("--model-size", default=None, help="whisper 模型大小")
    batch.add_argument("--language", default=None, help="识别语言")
    batch.add_argument("--force", action="store_true", help="强制重新处理")
    _add_common_opts(batch)

    # status
    status_sub = subparsers.add_parser("status", help="检查工具可用性")
    _add_common_opts(status_sub)

    # config
    config_sub = subparsers.add_parser("config", help="显示当前配置")
    _add_common_opts(config_sub)

    return parser


def main(argv: Optional[List[str]] = None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return

    config = load_config(args.config)
    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(levelname)s: %(message)s",
        force=True,
    )

    output_dir = args.output_dir or config.get("output_dir") or OUTPUT_DIR

    if args.command == "status":
        status_cmd()
        return

    if args.command == "config":
        config_cmd(config)
        return

    interval = float(resolve_arg(args, "interval", config))
    model_size = str(resolve_arg(args, "model_size", config))
    language = str(resolve_arg(args, "language", config))
    player = resolve_arg(args, "player", config)
    force = bool(getattr(args, "force", False))

    if args.command == "play":
        play_video(Path(args.video), player)

    elif args.command == "asr":
        result = run_asr(
            Path(args.video),
            force=force,
            model_size=model_size,
            language=language,
            output_dir=output_dir,
        )
        print(result.get("text", ""))

    elif args.command == "ocr":
        results = run_ocr(
            Path(args.video),
            interval=interval,
            force=force,
            output_dir=output_dir,
        )
        print(json.dumps(results, ensure_ascii=False, indent=2))

    elif args.command in ("process", "embed"):
        process_video(
            Path(args.video),
            interval=interval,
            force=force,
            output_dir=output_dir,
            model_size=model_size,
            language=language,
        )

    elif args.command == "batch":
        batch_process(
            Path(args.directory),
            interval=interval,
            force=force,
            output_dir=output_dir,
            model_size=model_size,
            language=language,
        )

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
