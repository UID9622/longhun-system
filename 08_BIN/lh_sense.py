#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
# ⚡ 龍魂·统一多模态识别引擎 v2.0 — 识别 → 决策 → 编排 → 反馈 完整闭环（全本地·数据不出机）
# DNA: #龍芯⚡️丙午·丁酉·SENSE-v2.0-DECIDE-ORCH-FEEDBACK-UID9622
# 创建者: 诸葛鑫（UID9622）· 龍芯北辰
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
🐉 龍魂·lh_sense 统一多模态识别引擎 v2.0

v2.0 升级: 「识别即输出」→「识别→决策→编排→反馈」完整闭环
  方向一 感知→决策: --auto 自动三色审计 → 🟢入记忆库 / 🟡耻辱墙草稿 / 🔴熔断告警
                     sense monitor 目录监听·新文件自动识别+审计
                     lh health --json 输出 sense_audit 字段
  方向二 感知→技能编排: --pipeline <链名> / sense pipeline list|run
                     内置三链: ocr-chain(OCR→图谱) / asr-chain(转写→摘要→记忆) / vision-chain(识别→标签→图谱)
                     自定义链: ~/.longhun/sense_pipelines.json
  方向三 感知→自我反馈: --feedback 置信度评分 → 低于阈值记"疑似误识别"
                     sense feedback list|correct <id> --text|export [--format jsonl|csv]
                     纠正语料积累 → ~/.longhun/sense_feedback_corpus.jsonl → 微调数据集
  方向间联动: 三方向共享统一配置 ~/.longhun/sense_config.json

用法:
  lh sense <文件> [--auto] [--pipeline 链名] [--feedback] [--json] [--no-ocr] [--no-asr] [--frames N]
  lh sense <目录> --scan
  lh sense monitor [--watch-dir <路径>] [--interval 秒] [--once]
  lh sense pipeline list
  lh sense pipeline run <链名> <文件>
  lh sense feedback list | feedback correct <id> --text "正确内容" | feedback export [--format jsonl|csv]

数据落点(全 ~/.longhun/):
  sense_config.json            统一配置(三方向开关/阈值/watch_dir)
  sense_memory/sense_memory.jsonl   🟢 审计通过记忆(带DNA)
  shame_wall/notices.jsonl      🔴 熔断+🟡 待审(复用 lh_external 耻辱墙格式)
  sense_feedback.log            🔽 疑似误识别
  sense_feedback_corpus.jsonl   ✔️ 人工纠正语料(微调数据集)
  sense_pipelines.json          自定义技能链(可选)
  sense_audit.jsonl             审计日志(health 汇总源)

依赖(已装·全本地): ollama(moondream) / faster-whisper / tesseract / ffmpeg / PIL
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""

import os
import sys
import json
import time
import argparse
import hashlib
import subprocess
import tempfile
from pathlib import Path

try:
    from PIL import Image
    PIL_OK = True
except Exception:
    PIL_OK = False

HOME = str(Path.home())
LONGHUN = os.path.join(HOME, ".longhun")
WHISPER_ROOT = os.path.join(LONGHUN, "longhun-whisper")
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
SHAME_NOTICES = os.path.join(LONGHUN, "shame_wall", "notices.jsonl")
CONFIG_PATH = os.path.join(LONGHUN, "sense_config.json")
MEMORY_LOG = os.path.join(LONGHUN, "sense_memory", "sense_memory.jsonl")
AUDIT_LOG = os.path.join(LONGHUN, "sense_audit.jsonl")
FEEDBACK_LOG = os.path.join(LONGHUN, "sense_feedback.log")
CORPUS_LOG = os.path.join(LONGHUN, "sense_feedback_corpus.jsonl")
PIPELINES_CFG = os.path.join(LONGHUN, "sense_pipelines.json")
PROCESSED_LOG = os.path.join(LONGHUN, "sense_processed.json")

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif", ".heic", ".tiff", ".tif"}
AUDIO_EXTS = {".wav", ".mp3", ".m4a", ".aac", ".flac", ".ogg", ".opus", ".wma", ".aiff", ".caf"}
VIDEO_EXTS = {".mp4", ".mov", ".mkv", ".avi", ".webm", ".flv", ".wmv", ".m4v", ".ts", ".mts"}
PROMPT_DEFAULT = "请用中文详细描述这张图片的内容。如果是图表/截图/文档，请说明其中文字信息。"

DEFAULT_CONFIG = {
    "auto": False,                      # 方向一：自动审计
    "default_pipeline": "",             # 方向二：默认技能链
    "feedback": False,                  # 方向三：自我反馈
    "confidence_threshold": 0.7,        # 方向三：置信度阈值
    "watch_dir": "",                    # 方向一：监控目录
    "audit_verbose": True,              # 审计时输出明细
    "pipeline_brain_after_audit": True, # 🟢 通过后自动入 brain 记忆
}

# 方向二：内置技能链（步骤说明）
BUILTIN_PIPELINES = {
    "ocr-chain": {
        "desc": "图片OCR → 提取文字 → 存入图谱(lh topo)",
        "steps": [{"action": "ocr", "target": "text", "use": "提取全量文字"}],
        "then": [{"action": "topo", "type": "ocr_text"}],
    },
    "asr-chain": {
        "desc": "音频转写 → 自动摘要 → 存入记忆(lh brain)",
        "steps": [{"action": "asr", "target": "transcript", "use": "全量转写"}],
        "then": [{"action": "brain", "kind": "note"}],
    },
    "vision-chain": {
        "desc": "图片识别 → 自动打标签 → 生成知识节点(lh topo)",
        "steps": [{"action": "vision", "target": "vlm_text", "use": "场景描述"}],
        "then": [{"action": "topo", "type": "vision_node"}],
    },
    "ledger-chain": {
        "desc": "发票/收据/口述 → 账法自动记账(lh ledger·DNA+三色审计)",
        "steps": [{"action": "ocr", "target": "text", "use": "提取票面文字"}],
        "then": [{"action": "ledger", "type": "invoice"}],
    },
}


def log(msg):
    print(f"[lh_sense] {msg}")


def _now_iso():
    from datetime import datetime
    return datetime.now().astimezone().isoformat(timespec="seconds")


def _short_hash(text: str, n: int = 8) -> str:
    return hashlib.sha256((text or "empty").encode("utf-8")).hexdigest()[:n]


def _which(cmd):
    for p in os.environ.get("PATH", "").split(":"):
        if os.path.exists(os.path.join(p, cmd)):
            return os.path.join(p, cmd)
    return None


def _ensure_dirs():
    for d in (LONGHUN, os.path.join(LONGHUN, "sense_memory"),
              os.path.join(LONGHUN, "shame_wall")):
        os.makedirs(d, exist_ok=True)


def is_ollama_up():
    """ollama 服务是否存活"""
    try:
        import urllib.request
        urllib.request.urlopen("http://127.0.0.1:11434/api/tags", timeout=3)
        return True
    except Exception:
        return False


# ───────────────────────── 统一配置（方向间共享） ─────────────────────────
def load_config() -> dict:
    cfg = dict(DEFAULT_CONFIG)
    try:
        with open(CONFIG_PATH, encoding="utf-8") as fh:
            cfg.update(json.load(fh))
    except Exception:
        pass
    return cfg


def save_config(cfg: dict) -> None:
    _ensure_dirs()
    with open(CONFIG_PATH, "w", encoding="utf-8") as fh:
        json.dump(cfg, fh, ensure_ascii=False, indent=2)
    print(f"  ✅ 配置已存 {CONFIG_PATH}")


def cmd_config_get(key: str = "") -> int:
    cfg = load_config()
    if key:
        print(f"  {key} = {cfg.get(key)}")
    else:
        print(json.dumps(cfg, ensure_ascii=False, indent=2))
    return 0


def cmd_config_set(key: str, value: str) -> int:
    cfg = load_config()
    if key not in cfg:
        print(f"  ⚠️ 未知配置项: {key}（可用: {', '.join(cfg)}）")
        return 2
    v: object = value
    if isinstance(cfg[key], bool):
        v = value.lower() in ("1", "true", "yes", "on", "开", "启用")
    elif isinstance(cfg[key], (int, float)):
        try:
            v = float(value) if isinstance(cfg[key], float) else int(value)
        except ValueError:
            print(f"  ❌ {key} 需要数字，收到 {value}")
            return 2
    cfg[key] = v
    save_config(cfg)
    return 0


# ───────────────────────── 图片管线 ─────────────────────────
def ocr_image(path: str) -> dict:
    """tesseract OCR：中英双语（返回文本+平均置信度）"""
    tesseract = _which("tesseract")
    if not tesseract:
        return {"ok": False, "error": "tesseract 未安装"}
    langs = "chi_sim+eng"
    try:
        r = subprocess.run([tesseract, path, "stdout", "-l", langs],
                           capture_output=True, text=True, timeout=120)
        text = (r.stdout or "").strip()
        # TSV 求平均置信度（level=5 为字符行, conf 第11列）
        conf = None
        try:
            r2 = subprocess.run([tesseract, path, "stdout", "-l", langs, "--tsv"],
                                capture_output=True, text=True, timeout=120)
            rows = [ln.split("\t") for ln in (r2.stdout or "").splitlines()[1:]]
            confs = []
            for row in rows:
                if len(row) >= 12 and row[0].strip() == "5":
                    try:
                        confs.append(float(row[10]))
                    except ValueError:
                        pass
            if confs:
                conf = round(sum(confs) / len(confs) / 100.0, 2)
        except Exception:
            pass
        return {"ok": True, "text": text[:8000], "chars": len(text),
                "confidence": conf if conf is not None else (0.9 if text else 0.0)}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def vlm_image(path: str, prompt: str = PROMPT_DEFAULT) -> dict:
    """moondream VLM：ollama HTTP API"""
    import base64
    import urllib.request
    if not is_ollama_up():
        return {"ok": False, "error": "ollama 未运行 (brew services start ollama)"}
    try:
        tmp = None
        if PIL_OK:
            with Image.open(path) as im:
                im = im.convert("RGB")
                im.thumbnail((1280, 1280))
                tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
                tmp.close()
                im.save(tmp.name, "PNG")
                img_path = tmp.name
        else:
            img_path = path
        with open(img_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode()
        payload = json.dumps({"model": "moondream", "prompt": prompt,
                              "images": [img_b64], "stream": False}).encode()
        req = urllib.request.Request(OLLAMA_URL, data=payload,
                                     headers={"Content-Type": "application/json"})
        resp = json.loads(urllib.request.urlopen(req, timeout=180).read())
        if tmp:
            os.unlink(tmp.name)
        text = (resp.get("response") or "").strip()
        # VLM 无原生置信度：启发式（内容非空且达一定长度视为可信）
        conf = round(min(0.95, 0.45 + len(text) / 200.0), 2) if text else 0.0
        return {"ok": True, "text": text[:4000], "confidence": conf}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def sense_image(path: str, prompt: str, want_ocr: bool) -> dict:
    out = {"type": "image", "path": str(path), "vlm": None, "ocr": None}
    out["vlm"] = vlm_image(str(path), prompt)
    if want_ocr:
        out["ocr"] = ocr_image(str(path))
    return out


# ───────────────────────── 音频管线 ─────────────────────────
def sense_audio(path: str, language: str = "zh") -> dict:
    """faster-whisper 本地转写（带 avg_logprob 置信度）"""
    out = {"type": "audio", "path": str(path), "transcript": None}
    try:
        from faster_whisper import WhisperModel
    except Exception as e:
        out["error"] = f"faster_whisper 未安装: {e}"
        return out
    try:
        model = WhisperModel("small", device="cpu", compute_type="int8",
                             download_root=WHISPER_ROOT)
        segments, info = model.transcribe(str(path), language=language,
                                          vad_filter=True)
        segs = []
        full = []
        probs = []
        no_speechs = []
        for s in segments:
            segs.append({"start": round(s.start, 2), "end": round(s.end, 2),
                         "text": s.text.strip()})
            full.append(s.text.strip())
            p = getattr(s, "avg_logprob", None)
            if p is not None:
                probs.append(p)
            ns = getattr(s, "no_speech_prob", None)
            if ns is not None:
                no_speechs.append(ns)
        text = " ".join(full).strip()
        avg_logprob = (sum(probs) / len(probs)) if probs else None  # 典型 -2..0
        no_speech = (sum(no_speechs) / len(no_speechs)) if no_speechs else 0.0
        conf = 0.0
        if avg_logprob is not None:
            # 线性映射: -2 → 0.0 · -0.5 → 0.75 · -0.37 → 0.82 · 0 → 1.0
            conf = round(max(0.0, min(1.0, 1.0 + avg_logprob / 2.0)), 2)
            if no_speech and no_speech > 0.5:
                conf = round(min(conf, 0.2), 2)   # 疑似无语音段→低置信
        out["transcript"] = {
            "language": info.language, "duration": round(info.duration, 2),
            "text": text, "segments": segs[:200],
            "avg_logprob": round(avg_logprob, 3) if avg_logprob is not None else None,
            "confidence": conf,
        }
        return out
    except Exception as e:
        out["error"] = str(e)
        return out


# ───────────────────────── 视频管线 ─────────────────────────
def ffprobe_duration(path: str) -> float:
    try:
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                            "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", path],
                           capture_output=True, text=True, timeout=30)
        return float(r.stdout.strip())
    except Exception:
        return 0.0


def extract_audio_track(video: str, out_wav: str) -> bool:
    r = subprocess.run(["ffmpeg", "-y", "-i", video, "-vn", "-ac", "1",
                        "-ar", "16000", out_wav],
                       capture_output=True, text=True, timeout=300)
    return r.returncode == 0


def extract_frames(video: str, frames_dir: str, n_frames: int) -> list:
    dur = ffprobe_duration(video)
    if dur <= 0:
        dur = 10
    n = max(1, min(n_frames, int(dur) // 2 if dur > 2 else 1))
    paths = []
    for i in range(n):
        t = dur * (i + 0.5) / n
        out = os.path.join(frames_dir, f"frame_{i:03d}.png")
        r = subprocess.run(["ffmpeg", "-y", "-ss", str(t), "-i", video,
                            "-frames:v", "1", "-vf", "scale=640:-2", out],
                           capture_output=True, text=True, timeout=120)
        if r.returncode == 0 and os.path.exists(out):
            paths.append((t, out))
    return paths


def sense_video(path: str, prompt: str, n_frames: int, want_asr: bool) -> dict:
    out = {"type": "video", "path": str(path), "duration": ffprobe_duration(str(path)),
           "frames": [], "audio": None}
    tmpdir = tempfile.mkdtemp(prefix="lh_sense_")
    try:
        frames = extract_frames(str(path), tmpdir, n_frames)
        for t, fp in frames:
            v = vlm_image(fp, prompt)
            out["frames"].append({"time_sec": round(t, 2), "vlm": v})
        if want_asr:
            wav = os.path.join(tmpdir, "audio.wav")
            if extract_audio_track(str(path), wav):
                out["audio"] = sense_audio(wav)
    finally:
        import shutil
        shutil.rmtree(tmpdir, ignore_errors=True)
    return out


# ───────────────────────── 统一路由 ─────────────────────────
def sense_file(path: str, prompt: str, want_ocr: bool, want_asr: bool,
               n_frames: int) -> dict:
    p = Path(path)
    ext = p.suffix.lower()
    if not p.exists():
        return {"ok": False, "error": f"文件不存在: {path}"}
    if ext in IMAGE_EXTS:
        return {"ok": True, **sense_image(p, prompt, want_ocr)}
    if ext in AUDIO_EXTS:
        return {"ok": True, **sense_audio(p)}
    if ext in VIDEO_EXTS:
        return {"ok": True, **sense_video(p, prompt, n_frames, want_asr)}
    try:
        import mimetypes
        mime = mimetypes.guess_type(path)[0] or ""
        if mime.startswith("image/"):
            return {"ok": True, **sense_image(p, prompt, want_ocr)}
        if mime.startswith("audio/"):
            return {"ok": True, **sense_audio(p)}
        if mime.startswith("video/"):
            return {"ok": True, **sense_video(p, prompt, n_frames, want_asr)}
    except Exception:
        pass
    return {"ok": False, "error": f"不支持的文件类型: {ext or '(无扩展名)'}"}


# ───────────────────────── 提炼识别文本（供审计/入记忆） ─────────────────────────
def extract_text(result: dict) -> str:
    """从识别结果提炼可读文本"""
    parts = []
    typ = result.get("type")
    if typ == "image":
        v = result.get("vlm") or {}
        if v.get("ok") and v.get("text"):
            parts.append(f"[视觉] {v['text']}")
        o = result.get("ocr") or {}
        if o.get("ok") and o.get("text"):
            parts.append(f"[文字] {o['text']}")
    elif typ == "audio":
        tr = result.get("transcript") or {}
        if tr.get("text"):
            parts.append(f"[语音] {tr['text']}")
    elif typ == "video":
        for fr in result.get("frames", []):
            v = fr.get("vlm") or {}
            if v.get("ok") and v.get("text"):
                parts.append(f"[画面] {v['text']}")
        au = result.get("audio") or {}
        tr = au.get("transcript") or {}
        if tr.get("text"):
            parts.append(f"[音轨] {tr['text']}")
    return "\n".join(parts)


def overall_confidence(result: dict) -> float:
    """多通道置信度汇总：只统计有实质文本(≥10字)的通道·取最低=保守
    短/空描述通道(如 VLM 只吐几个字)不计入，避免拖累真实长文本通道(如 OCR 198字)"""
    def _has(text):
        return text and len(text.strip()) >= 10

    confs = []
    typ = result.get("type")
    if typ == "image":
        v = result.get("vlm") or {}
        if v.get("ok") and v.get("confidence") is not None and _has(v.get("text")):
            confs.append(v["confidence"])
        o = result.get("ocr") or {}
        if o.get("ok") and o.get("confidence") is not None and _has(o.get("text")):
            confs.append(o["confidence"])
    elif typ == "audio":
        tr = result.get("transcript") or {}
        if tr.get("confidence") is not None and _has(tr.get("text")):
            confs.append(tr["confidence"])
    elif typ == "video":
        for fr in result.get("frames", []):
            v = fr.get("vlm") or {}
            if v.get("ok") and v.get("confidence") is not None and _has(v.get("text")):
                confs.append(v["confidence"])
        au = result.get("audio") or {}
        tr = au.get("transcript") or {}
        if tr.get("confidence") is not None and _has(tr.get("text")):
            confs.append(tr["confidence"])
    if not confs:
        return 0.0
    return round(min(confs), 2)   # 有实质文本的通道中保守取低


# ───────────────────────── 方向一：感知 → 决策 ─────────────────────────
def audit_text(text: str) -> str:
    """三色审计：优先接 P05 quick_audit，降级内置规则"""
    text = (text or "").strip()
    if not text:
        return "🔴"
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from lh_three_color_audit import quick_audit
        verdict = quick_audit(text)
        s = str(verdict)
        for color in ("🟢", "🟡", "🔴"):
            if color in s:
                return color
        # quick_audit 返回值可能是 (色, 理由)
        if isinstance(verdict, (list, tuple)) and verdict:
            for color in ("🟢", "🟡", "🔴"):
                if color in str(verdict[0]):
                    return color
        return "🟡"   # 无法判定 → 待审
    except Exception:
        # 内置降级规则：长度/敏感词启发
        if len(text) < 4:
            return "🟡"
        if any(w in text for w in ("无法识别", "识别失败", "空")):
            return "🟡"
        return "🟢"


def _write_jsonl(path: str, entry: dict) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")


def shame_notice(kind: str, message: str, dna: str) -> None:
    """写耻辱墙 notices（复用 lh_external 格式）"""
    _write_jsonl(SHAME_NOTICES, {"ts": _now_iso(), "type": kind,
                                 "repo": "lh-sense", "message": message,
                                 "dna": dna})


def cmd_auto(result: dict, conf_threshold: float, verbose: bool) -> str:
    """方向一：识别结果自动三色审计 → 🟢入记忆库 / 🟡耻辱墙草稿 / 🔴熔断告警"""
    text = extract_text(result)
    color = audit_text(text)
    conf = overall_confidence(result)
    ok = result.get("ok")
    if not ok:
        color = "🔴"
    elif conf > 0.0 and conf < conf_threshold:
        color = "🟡"   # 置信度不足 → 待审（不直接熔断）
    dna = f"#龍芯⚡️丙午·丁酉·SENSE-AUTO-{_short_hash(str(result.get('path')) + text, 8)}"
    entry = {
        "ts": _now_iso(), "dna": dna, "color": color,
        "file": str(result.get("path", "")), "type": result.get("type", "?"),
        "confidence": conf, "text": text[:2000],
        "audit": color + (" · " + ("识别失败" if not ok else "置信度低于阈值" if conf > 0.0 and conf < conf_threshold else "三色审计通过") if verbose else ""),
    }
    _write_jsonl(AUDIT_LOG, entry)
    if color == "🟢":
        _write_jsonl(MEMORY_LOG, entry)
        if verbose:
            print(f"  🟢 审计通过 · 已入记忆库 sense_memory.jsonl")
            print(f"     DNA {dna}")
        cfg = load_config()
        if cfg.get("pipeline_brain_after_audit"):
            try:
                _brain_save(f"[lh_sense {entry['type']}] {text[:800]}",
                            [entry["type"], "lh_sense"], "lh-sense", "sense_auto")
            except Exception as e:
                if verbose:
                    print(f"     (brain 同步失败: {e})")
        return color
    if color == "🟡":
        shame_notice("sense_yellow_draft", f"待审 {entry['file']} conf={conf} · {text[:120]}", dna)
        if verbose:
            print(f"  🟡 待审 · 已写耻辱墙草稿 (conf={conf})")
            print(f"     DNA {dna}")
        return color
    # 🔴
    shame_notice("sense_red_meltdown", f"熔断 {entry['file']} 识别失败/违规 · {text[:120]}", dna)
    print(f"  🔴 熔断 · 已写耻辱墙 + 触发告警")
    print(f"     DNA {dna}")
    _try_alert(entry)
    return color


def _try_alert(entry: dict) -> None:
    """熔断告警（Bark 若配置）——不阻塞"""
    try:
        key = os.path.join(LONGHUN, "bark_key.txt")
        if os.path.exists(key):
            token = open(key).read().strip()
            if token:
                subprocess.Popen(["curl", "-s", "-m", "8",
                                  f"https://api.day.app/{token}/龍魂感知熔断",
                                  "-d", f"body={entry.get('file', '?')} conf={entry.get('confidence')}"],
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass


# ───────────────────────── 方向一：monitor 目录监听 ─────────────────────────
def _media_ext(ext: str) -> bool:
    return ext in IMAGE_EXTS or ext in AUDIO_EXTS or ext in VIDEO_EXTS


def _load_processed() -> dict:
    try:
        with open(PROCESSED_LOG, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return {}


def _save_processed(d: dict) -> None:
    os.makedirs(os.path.dirname(PROCESSED_LOG), exist_ok=True)
    with open(PROCESSED_LOG, "w", encoding="utf-8") as fh:
        json.dump(d, fh, ensure_ascii=False, indent=1)


def cmd_monitor(watch_dir: str, interval: int, once: bool) -> int:
    """方向一：监听目录·新文件自动识别+审计"""
    if not watch_dir:
        cfg = load_config()
        watch_dir = cfg.get("watch_dir", "")
    if not watch_dir or not os.path.isdir(watch_dir):
        print("  ❌ 需 --watch-dir <目录> 或 config set watch_dir <目录>")
        return 2
    processed = _load_processed()
    cfg = load_config()
    print(f"  👁️ 监听 {watch_dir} · interval={interval}s · once={'是' if once else '否'}")
    rounds = 0
    while True:
        rounds += 1
        found = False
        for root, _, files in os.walk(watch_dir):
            for f in sorted(files):
                ext = Path(f).suffix.lower()
                if not _media_ext(ext):
                    continue
                fp = os.path.join(root, f)
                sig = f"{os.path.getmtime(fp):.0f}:{os.path.getsize(fp)}"
                if processed.get(fp) == sig:
                    continue
                found = True
                print(f"  🔍 新文件 {fp}")
                try:
                    result = sense_file(fp, PROMPT_DEFAULT, want_ocr=True,
                                        want_asr=True, n_frames=4)
                    cmd_auto(result, cfg.get("confidence_threshold", 0.7),
                             cfg.get("audit_verbose", True))
                    processed[fp] = sig
                except Exception as e:
                    print(f"     ❌ {e}")
                _save_processed(processed)
        if not found:
            print(f"  ⏳ 第{rounds}轮无新文件" if not once else "  ✅ 单轮完成·无新文件")
        if once:
            break
        time.sleep(max(1, interval))
    return 0


# ───────────────────────── 方向二：感知 → 技能编排 ─────────────────────────
def _brain_save(note: str, kw: list, source: str, kind: str) -> None:
    """接 lh_brain._save（子进程隔离·防 import 副作用）"""
    script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lh_brain.py")
    cmd = [sys.executable, script, "save", "--note", note[:1950],
           "--source", source, "--kind", kind]
    for k in kw[:5]:
        cmd += ["--kw", k]
    subprocess.run(cmd, capture_output=True, text=True, timeout=60)


def _topo_register(keyword: str, display: str) -> None:
    script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lh_topo.py")
    subprocess.run([sys.executable, script, "register", keyword, "--display", display],
                   capture_output=True, text=True, timeout=30)


def _topo_node(keyword: str, group: str, name: str, ntype: str, desc: str,
               source: str = "") -> None:
    script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lh_topo.py")
    cmd = [sys.executable, script, "node", keyword, "--group", group,
           "--name", name[:120], "--type", ntype, "--desc", desc[:800],
           "--source", source[:200]]
    subprocess.run(cmd, capture_output=True, text=True, timeout=30)


def _summarize(text: str, limit: int = 400) -> str:
    """极简抽取式摘要：首句+末句"""
    text = (text or "").strip()
    if len(text) <= limit:
        return text
    lines = [l for l in text.splitlines() if l.strip()]
    if len(lines) >= 3:
        return (lines[0][:200] + " … " + lines[-1][:200])[:limit]
    return text[:limit] + " …"


def _tag_from_text(text: str) -> list:
    """极简打标签：提取前 2 个 ≥2 字短语 + 类型词"""
    tags = []
    for word in text.replace("\n", " ").split():
        w = word.strip("，。！？、；：\"'()[]【】 ")
        if len(w) >= 2 and w not in tags:
            tags.append(w)
        if len(tags) >= 4:
            break
    return tags or ["lh_sense"]


def run_pipeline(name: str, filepath: str, result: dict) -> int:
    """方向二：执行技能链（内置或用户自定义）"""
    pipelines = load_pipelines()
    pipe = pipelines.get(name)
    if not pipe:
        print(f"  ❌ 技能链不存在: {name}")
        print(f"     可用: {', '.join(pipelines)}")
        return 2
    print(f"  🧬 执行技能链 [{name}] · {pipe.get('desc', '')}")
    text = extract_text(result)
    if not text:
        print("  ⚠️ 识别无文本产出，链后动作跳过")
    for step in pipe.get("steps", []):
        act = step.get("action", "")
        if act == "ocr":
            o = (result.get("ocr") or {})
            print(f"     ⚙️ OCR 提取 · {o.get('chars', 0)} 字" if o.get("ok") else "     ⚙️ OCR 无结果")
        elif act == "asr":
            tr = (result.get("transcript") or {})
            print(f"     ⚙️ 转写完成 · {tr.get('duration', 0)}s")
        elif act == "vision":
            print("     ⚙️ 视觉识别完成")
    for then in pipe.get("then", []):
        act = then.get("action", "")
        try:
            if act == "brain":
                _brain_save(f"[{name}] {_summarize(text, 800)}", [name, "sense"],
                            "lh-sense", then.get("kind", "note"))
                print(f"     ✅ 已入记忆 lh brain ({then.get('kind', 'note')})")
            elif act == "topo":
                keyword = "sense-media"
                ntype = then.get("type", "node")
                node_name = f"{Path(filepath).stem}_{_short_hash(text, 6)}"
                desc = _summarize(text, 600)
                _topo_register(keyword, "🧠 识别媒体图谱 v1.0")  # 已存在则内部跳过
                _topo_node(keyword, "识别入库", node_name, ntype, desc, source=filepath)
                print(f"     ✅ 已入图谱 lh topo node {keyword}")
            elif act == "memory":
                _write_jsonl(MEMORY_LOG, {"ts": _now_iso(), "dna": _short_hash(text, 8),
                                          "color": "🟢", "file": filepath,
                                          "type": result.get("type", "?"),
                                          "text": text[:2000], "pipeline": name})
                print("     ✅ 已入 sense_memory")
            elif act == "ledger":
                # 📒 账法记账: OCR/ASR 文本 → lh ledger add-auto → 三色审计
                ledger_script = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                             "lh_ledger.py")
                cmd = [sys.executable, ledger_script, "add-auto", text[:1500],
                       "--tx-type", then.get("tx_type", "T9"), "--source", "lh-sense"]
                r = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
                out = (r.stdout or "").strip().splitlines()
                for ln in out:
                    print(f"     {ln.strip()}")
                if r.returncode != 0:
                    print(f"     ❌ 记账失败: {(r.stderr or '')[:300]}")
        except Exception as e:
            print(f"     ❌ {act} 失败: {e}")
    return 0


def load_pipelines() -> dict:
    pipes = {k: dict(v) for k, v in BUILTIN_PIPELINES.items()}
    try:
        with open(PIPELINES_CFG, encoding="utf-8") as fh:
            user = json.load(fh)
        for k, v in user.items():
            pipes[k] = v
    except Exception:
        pass
    return pipes


def cmd_pipeline_list() -> int:
    pipes = load_pipelines()
    print(f"  🧬 可用技能链 ({len(pipes)}):")
    for name, p in pipes.items():
        flag = "内置" if name in BUILTIN_PIPELINES else "自定义"
        print(f"    · {name}  [{flag}] {p.get('desc', '')}")
        for s in p.get("steps", []):
            print(f"        → {s.get('action')}: {s.get('use', '')}")
    print("\n  自定义链: 编辑 ~/.longhun/sense_pipelines.json")
    print("  执行: lh sense pipeline run <链名> <文件>")
    return 0


def cmd_pipeline_run(name: str, filepath: str) -> int:
    result = sense_file(filepath, PROMPT_DEFAULT, want_ocr=True, want_asr=True, n_frames=4)
    if not result.get("ok"):
        print(f"  ❌ {result.get('error')}")
        return 1
    rc = run_pipeline(name, filepath, result)
    # 方向间联动：链执行后默认过方向一审计 + 方向三置信度
    cfg = load_config()
    if cfg.get("auto") or cfg.get("default_pipeline") == name:
        cmd_auto(result, cfg.get("confidence_threshold", 0.7),
                 cfg.get("audit_verbose", True))
    if cfg.get("feedback"):
        cmd_feedback_check(result, cfg.get("confidence_threshold", 0.7), verbose=False)
    return rc


# ───────────────────────── 方向三：感知 → 自我反馈 ─────────────────────────
def cmd_feedback_check(result: dict, threshold: float, verbose: bool = True) -> None:
    """识别结果置信度评分 → 低于阈值记疑似误识别"""
    text = extract_text(result)
    conf = overall_confidence(result)
    if verbose:
        print(f"  🧪 置信度 {conf} (阈值 {threshold})")
    if text and conf < threshold:
        rid = f"fb_{_short_hash(str(result.get('path')) + text, 10)}"
        entry = {"id": rid, "ts": _now_iso(), "file": str(result.get("path", "")),
                 "type": result.get("type", "?"), "confidence": conf,
                 "threshold": threshold, "text": text[:1200], "status": "pending"}
        _write_jsonl(FEEDBACK_LOG, entry)
        if verbose:
            print(f"  🔽 疑似误识别 conf={conf}<{threshold} · 已记 sense_feedback.log ({rid})")
    elif not text:
        if verbose:
            print("  ⚠️ 无识别文本，跳过反馈记录")


def cmd_feedback_list() -> int:
    if not os.path.exists(FEEDBACK_LOG):
        print("  ✅ 无待纠正记录")
        return 0
    pending = []
    with open(FEEDBACK_LOG, encoding="utf-8") as fh:
        for line in fh:
            try:
                e = json.loads(line)
                if e.get("status") == "pending":
                    pending.append(e)
            except Exception:
                continue
    if not pending:
        print("  ✅ 无待纠正记录")
        return 0
    print(f"  🧪 待纠正记录 ({len(pending)}):")
    for e in pending:
        print(f"    [{e['id']}] {e.get('type')} conf={e.get('confidence')} "
              f"({e.get('ts', '')[:19]})")
        print(f"        识别: {e.get('text', '')[:150]}")
        print(f"        纠正: lh sense feedback correct {e['id']} --text \"正确内容\"")
    return 0


def cmd_feedback_correct(fb_id: str, correct_text: str) -> int:
    if not correct_text.strip():
        print("  ❌ 需 --text \"正确内容\"")
        return 2
    if not os.path.exists(FEEDBACK_LOG):
        print(f"  ❌ 无反馈日志，记录 {fb_id} 不存在")
        return 2
    lines = open(FEEDBACK_LOG, encoding="utf-8").read().splitlines()
    found = None
    for i, line in enumerate(lines):
        try:
            e = json.loads(line)
            if e.get("id") == fb_id and e.get("status") == "pending":
                found = e
                lines[i] = json.dumps({**e, "status": "corrected"}, ensure_ascii=False)
                break
        except Exception:
            continue
    if not found:
        print(f"  ❌ 记录不存在或已纠正: {fb_id}")
        return 2
    corpus = {**found, "corrected": correct_text.strip(),
              "corrected_ts": _now_iso()}
    _write_jsonl(CORPUS_LOG, corpus)
    with open(FEEDBACK_LOG, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"  ✅ 纠正已入库 sense_feedback_corpus.jsonl ({fb_id})")
    print(f"     原: {corpus.get('text', '')[:100]}")
    print(f"     正: {correct_text[:100]}")
    return 0


def cmd_feedback_export(fmt: str, out_path: str) -> int:
    if not os.path.exists(CORPUS_LOG):
        print("  ⚠️ 语料库为空（先用 feedback correct 积累纠正）")
        return 1
    rows = []
    with open(CORPUS_LOG, encoding="utf-8") as fh:
        for line in fh:
            try:
                rows.append(json.loads(line))
            except Exception:
                continue
    if not rows:
        print("  ⚠️ 语料库为空")
        return 1
    target = out_path or os.path.join(LONGHUN,
                                      f"sense_feedback_corpus.{fmt}")
    if fmt == "csv":
        import csv
        keys = ["id", "ts", "file", "type", "confidence", "text", "corrected"]
        with open(target, "w", encoding="utf-8-sig", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=keys, extrasaction="ignore")
            w.writeheader()
            for r in rows:
                w.writerow(r)
    else:
        with open(target, "w", encoding="utf-8") as fh:
            for r in rows:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"  ✅ 纠正数据集已导出 ({len(rows)} 条) → {target}")
    print(f"     CSV/JSONL 可直接用于后续微调（Alpaca/ShareGPT 转写）")
    return 0


# ───────────────────────── 渲染 ─────────────────────────
def render_text(result: dict) -> str:
    lines = []
    if not result.get("ok"):
        return f"❌ {result.get('error', '未知错误')}"
    typ = result.get("type")
    lines.append(f"🎯 类型: {typ} · 路径: {result.get('path')}")
    if typ == "image":
        v = result.get("vlm") or {}
        if v.get("ok"):
            lines.append(f"\n👁️ VLM视觉描述 (conf={v.get('confidence')}):\n{v['text']}")
        else:
            lines.append(f"\n👁️ VLM: ❌ {v.get('error')}")
        ocr = result.get("ocr")
        if ocr and ocr.get("ok") and ocr.get("text"):
            lines.append(f"\n📝 OCR文字提取 ({ocr.get('chars')}字 conf={ocr.get('confidence')}):\n{ocr['text']}")
    elif typ == "audio":
        tr = result.get("transcript")
        if tr:
            lines.append(f"\n🎙️ 语音转写 [{tr['language']} · {tr['duration']}s · conf={tr.get('confidence')}]:\n{tr['text']}")
            if tr.get("segments"):
                lines.append("\n⏱️ 分段:")
                for s in tr["segments"][:20]:
                    lines.append(f"  [{s['start']:>7.2f}-{s['end']:>7.2f}] {s['text']}")
        else:
            lines.append(f"\n🎙️ 转写失败: {result.get('error', '')}")
    elif typ == "video":
        lines.append(f"\n🎬 时长: {result.get('duration', 0):.1f}s")
        for fr in result.get("frames", []):
            v = fr.get("vlm") or {}
            if v.get("ok"):
                lines.append(f"\n🖼️ [t={fr['time_sec']}s] {v['text']}")
            else:
                lines.append(f"\n🖼️ [t={fr['time_sec']}s] ❌ {v.get('error')}")
        au = result.get("audio")
        if au and au.get("transcript"):
            lines.append(f"\n🎙️ 音轨转写:\n{au['transcript']['text']}")
    else:
        lines.append(json.dumps(result, ensure_ascii=False, indent=2))
    return "\n".join(lines)


def _cnsh_safe(text: str, limit: int = 160) -> str:
    """CNSH 字符串安全化：去引号/反斜杠·换行→空格·截断（防破坏 CNSH 语法行）"""
    t = (text or "").replace("\\", " ").replace('"', " ").replace("\n", " ").replace("\r", " ")
    return " ".join(t.split())[:limit]


def render_cnsh(result: dict) -> str:
    """--cnsh: 识别结果 → CNSH 多模态感知语法指令（草案 v1.0 §7 桥接输出）
    一通道一行·语法行可直接作为编译器扩展的验收输入"""
    lines = []
    if not result.get("ok"):
        p = str(result.get("path", ""))
        err = _cnsh_safe(str(result.get("error", "未知错误")), 80)
        return f'感知.理解("{p}") -> "识别失败: {err}"  # 通道异常'
    p = str(result.get("path", ""))
    typ = result.get("type")
    conf = overall_confidence(result)
    if typ == "image":
        v = result.get("vlm") or {}
        if v.get("ok") and v.get("text"):
            lines.append(f'感知.理解("{p}") -> "{_cnsh_safe(v["text"])}"'
                         f'  # 视觉·SenseNova-Vision 任务统一表达 conf={v.get("confidence")}')
        o = result.get("ocr") or {}
        if o.get("ok") and o.get("text"):
            lines.append(f'感知.提取文字("{p}") -> "{_cnsh_safe(o["text"], 400)}"'
                         f'  # 文字·OCR 通道 conf={o.get("confidence")}')
    elif typ == "audio":
        tr = result.get("transcript") or {}
        if tr.get("text"):
            lines.append(f'感知.转写("{p}") -> "{_cnsh_safe(tr["text"], 400)}"'
                         f'  # 语音·ASR 本地通道 conf={tr.get("confidence")}')
    elif typ == "video":
        for fr in result.get("frames", []):
            v = fr.get("vlm") or {}
            if v.get("ok") and v.get("text"):
                lines.append(f'感知.理解("{p}@{fr.get("time_sec")}s") -> "{_cnsh_safe(v["text"])}"'
                             f'  # 视频帧·抽帧 VLM')
        au = result.get("audio") or {}
        tr = au.get("transcript") or {}
        if tr.get("text"):
            lines.append(f'感知.转写("{p}") -> "{_cnsh_safe(tr["text"], 300)}"'
                         f'  # 音轨·AV 联合双通道')
    if not lines:
        lines.append(f'感知.理解("{p}") -> "(无文本产出·conf={conf})"')
    if conf > 0:
        text = extract_text(result)
        color = audit_text(text) if text else "🟡"
        lines.append(f'感知.分层(多通道) -> {color}'
                     f'  # 三色审计 conf={conf} 详见 ~/.longhun/sense_audit.jsonl')
    return "\n".join(lines)


def scan_dir(path: str, prompt: str) -> list:
    results = []
    for root, _, files in os.walk(path):
        for f in sorted(files):
            ext = Path(f).suffix.lower()
            if ext in IMAGE_EXTS or ext in AUDIO_EXTS or ext in VIDEO_EXTS:
                fp = os.path.join(root, f)
                r = sense_file(fp, prompt, want_ocr=True, want_asr=True, n_frames=3)
                results.append({"file": fp, "result": r})
    return results


# ───────────────────────── 主入口 ─────────────────────────
def main(argv: list) -> int:
    _ensure_dirs()
    if not argv:
        print(__doc__.split("用法:")[-1].splitlines()[0].strip())
        print("  子命令: monitor / pipeline list / pipeline run / feedback list / "
              "feedback correct / feedback export / config")
        return 0

    sub = argv[0]
    if sub == "monitor":
        ap = argparse.ArgumentParser(prog="lh sense monitor")
        ap.add_argument("--watch-dir", default="")
        ap.add_argument("--interval", type=int, default=30)
        ap.add_argument("--once", action="store_true")
        a = ap.parse_args(argv[1:])
        return cmd_monitor(a.watch_dir, a.interval, a.once)

    if sub == "pipeline":
        ap = argparse.ArgumentParser(prog="lh sense pipeline")
        ap.add_argument("sub", nargs="?", default="list")
        ap.add_argument("args", nargs="*")
        a = ap.parse_args(argv[1:])
        if a.sub == "list":
            return cmd_pipeline_list()
        if a.sub == "run" and a.args:
            return cmd_pipeline_run(a.args[0], a.args[1])
        if a.sub == "run":
            print("  ❌ 用法: lh sense pipeline run <链名> <文件>")
            return 2
        print("  用法: lh sense pipeline list | run <链名> <文件>")
        return 2

    if sub == "feedback":
        ap = argparse.ArgumentParser(prog="lh sense feedback")
        ap.add_argument("sub", nargs="?", default="list")
        ap.add_argument("--text", default="")
        ap.add_argument("--format", dest="fmt", default="jsonl")
        ap.add_argument("--out", default="")
        ap.add_argument("rest", nargs="*")
        a = ap.parse_args(argv[1:])
        if a.sub == "list":
            return cmd_feedback_list()
        if a.sub == "correct":
            if not a.rest:
                print("  ❌ 用法: lh sense feedback correct <id> --text \"正确内容\"")
                return 2
            return cmd_feedback_correct(a.rest[0], a.text)
        if a.sub == "export":
            return cmd_feedback_export(a.fmt, a.out)
        print("  用法: lh sense feedback list|correct <id> --text …|export")
        return 2

    if sub == "config":
        ap = argparse.ArgumentParser(prog="lh sense config")
        ap.add_argument("sub", nargs="?", default="get")
        ap.add_argument("args", nargs="*")
        a = ap.parse_args(argv[1:])
        if a.sub == "get":
            return cmd_config_get(a.args[0] if a.args else "")
        if a.sub == "set" and len(a.args) == 2:
            return cmd_config_set(a.args[0], a.args[1])
        print("  用法: lh sense config [get [key]] | set <key> <value>")
        return 2

    # ── 默认：文件识别模式（可选三方向开关） ──
    ap = argparse.ArgumentParser(prog="lh sense")
    ap.add_argument("path")
    ap.add_argument("--prompt", default=PROMPT_DEFAULT)
    ap.add_argument("--no-ocr", action="store_true")
    ap.add_argument("--no-asr", action="store_true")
    ap.add_argument("--frames", type=int, default=4)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--scan", action="store_true")
    ap.add_argument("--auto", action="store_true")            # 方向一
    ap.add_argument("--pipeline", default="")                 # 方向二
    ap.add_argument("--feedback", action="store_true")        # 方向三
    ap.add_argument("--cnsh", action="store_true")            # CNSH 语法输出(草案 v1.0)
    a = ap.parse_args(argv)

    cfg = load_config()
    if not a.path:
        return 0
    if a.scan or os.path.isdir(a.path):
        results = scan_dir(a.path, a.prompt)
        if a.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            for item in results:
                print(render_text(item["result"]))
                print("─" * 60)
        return 0

    t0 = time.time()
    result = sense_file(a.path, a.prompt,
                        want_ocr=not a.no_ocr,
                        want_asr=not a.no_asr,
                        n_frames=a.frames)
    result["elapsed_sec"] = round(time.time() - t0, 1)
    if a.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif a.cnsh:
        print(render_cnsh(result))
        if result.get("elapsed_sec"):
            log(f"⏱️ 耗时 {result['elapsed_sec']}s")
    else:
        print(render_text(result))
        if result.get("elapsed_sec"):
            log(f"⏱️ 耗时 {result['elapsed_sec']}s")

    # 方向三：反馈检查（显式 --feedback 或 config.feedback 开启）
    do_feedback = a.feedback or cfg.get("feedback", False)
    # 方向一：自动审计（显式 --auto 或 config.auto 开启）
    do_auto = a.auto or cfg.get("auto", False)
    # 方向二：技能链（显式 --pipeline 或 config.default_pipeline 开启）
    pipe_name = a.pipeline or cfg.get("default_pipeline", "") or ""

    if do_auto or do_feedback or pipe_name:
        if not result.get("ok"):
            print(f"  ❌ 识别失败，方向动作跳过: {result.get('error')}")
            return 1
        if do_feedback:
            cmd_feedback_check(result, cfg.get("confidence_threshold", 0.7))
        if do_auto:
            cmd_auto(result, cfg.get("confidence_threshold", 0.7),
                     cfg.get("audit_verbose", True))
        if pipe_name:
            run_pipeline(pipe_name, a.path, result)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
