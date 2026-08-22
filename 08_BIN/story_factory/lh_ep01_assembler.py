#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 龍芯⚡️丙午·丙申·辛酉·戌时·☵坎-EP01-ASSEMBLER-v1.0
"""
🐉 龍魂 · EP01「雪夜初见」低成本本地装配器 v1.0

输入: bad-project-ep01-full-storyboard.json
输出:
  - 固定成片目录: ~/Pictures/龍魂素材仓库/videos/EP01_雪夜初见/
  - 每条台词的独立音频 (.wav)
  - 每个镜头的视频片段 (.mp4)
  - 154 秒完整成片 (.mp4)
  - 装配清单 (.json)
  - 快捷入口: ~/longhun-system/龍魂成片 、~/Pictures/龍魂素材仓库/龍魂成片 、~/Movies/龍魂成片

技术栈:
  - 语音: macOS say + ffmpeg (零模型本地 TTS) / F5-TTS 本地声音克隆(UID9622官方声线)
  - 画面: 静态素材 + ffmpeg zoompan 运镜模拟 / AnimateDiff 真实动态(ComfyUI)
  - 剪辑: ffmpeg concat + amix

限制（诚实标注）:
  - system 声线为系统默认中文语音，非专业配音
  - f5tts 声线基于用户本人语音克隆，需本地模型(约1.6GB)
  - 画面为图片序列+运镜/AnimateDiff，非电影级视频生成
  - 口型未对齐，作为「动态分镜」级成片
"""

import argparse
import json
import hashlib
import time
import subprocess
import re
import shutil
from pathlib import Path
from datetime import datetime

FACTORY_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = FACTORY_ROOT.parent.parent
STORYBOARD_PATH = PROJECT_ROOT / "12_DOCS" / "dragon-soul-open-hub" / "bad-project-ep01-full-storyboard.json"
WAREHOUSE_ROOT = Path.home() / "Pictures" / "龍魂素材仓库"
# 固定成片主目录：素材仓库 videos（用户要求），同时同步快捷入口到 Movies
FINAL_OUTPUT_ROOT = WAREHOUSE_ROOT / "videos"
OUTPUT_ROOT = FINAL_OUTPUT_ROOT / "EP01_雪夜初见"
SHORTCUT_ROOT = Path.home() / "Movies" / "龍魂成片" / "EP01_雪夜初见"
VENV_PYTHON = Path.home() / "longhun-system" / ".venv" / "bin" / "python"

FPS = 24
RESOLUTION = "1280x720"
AUDIO_RATE = 22050


# ============================================================
# DNA & helpers
# ============================================================
def generate_dna(tag: str = "EP01") -> str:
    h = hashlib.sha256(f"{tag}{time.time()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-{tag}-{h}-UID9622"


def clean_name(name: str) -> str:
    """去掉括号备注，取人格名。"""
    return re.sub(r"（.*?）", "", name).strip()


def get_duration(path: Path) -> float:
    """获取音频时长（秒）。"""
    try:
        out = subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
            text=True
        ).strip()
        return float(out)
    except Exception:
        return 0.0


# ============================================================
# 人格 → 声线映射
# ============================================================
# macOS say 系统声线
VOICE_MAP_SYSTEM = {
    "龍慧慧": {"voice": "Meijia", "rate": 170, "pitch": 0},
    "旁白": {"voice": "Meijia", "rate": 165, "pitch": 0},
    "谢文东": {"voice": "Reed (中文（中国大陆）)", "rate": 155, "pitch": -20},
    "三眼": {"voice": "Rocko (中文（中国大陆）)", "rate": 185, "pitch": 20},
    "李爽": {"voice": "Sandy (中文（中国大陆）)", "rate": 200, "pitch": 30},
    "高强": {"voice": "Grandpa (中文（中国大陆）)", "rate": 145, "pitch": -40},
    "向问天": {"voice": "Grandpa (中文（中国大陆）)", "rate": 150, "pitch": -30},
    "混混头": {"voice": "Rocko (中文（中国大陆）)", "rate": 175, "pitch": 10},
    "学生甲": {"voice": "Tingting", "rate": 180, "pitch": 0},
    "default": {"voice": "Tingting", "rate": 175, "pitch": 0},
}

# Kokoro 本地声线（中文 lang_code='z'）
VOICE_MAP_KOKORO = {
    "龍慧慧": {"voice": "zf_xiaoxiao", "speed": 0.95},
    "旁白": {"voice": "zf_xiaoxiao", "speed": 0.95},
    "谢文东": {"voice": "zm_yunxi", "speed": 0.92},
    "三眼": {"voice": "zm_yunxi", "speed": 1.05},
    "李爽": {"voice": "zf_xiaoxiao", "speed": 1.15},
    "高强": {"voice": "zm_yunjian", "speed": 0.88},
    "向问天": {"voice": "zm_yunjian", "speed": 0.90},
    "混混头": {"voice": "zm_yunyang", "speed": 1.0},
    "学生甲": {"voice": "zf_xiaoyi", "speed": 1.0},
    "default": {"voice": "zf_xiaoxiao", "speed": 1.0},
}

# MeloTTS 本地中文声线（零 API，CPU/MPS 实时）
VOICE_MAP_MELOTTS = {
    "龍慧慧": {"speaker": "ZH", "speed": 0.95},
    "旁白": {"speaker": "ZH", "speed": 0.95},
    "谢文东": {"speaker": "ZH", "speed": 0.92},
    "三眼": {"speaker": "ZH", "speed": 1.05},
    "李爽": {"speaker": "ZH", "speed": 1.10},
    "高强": {"speaker": "ZH", "speed": 0.88},
    "向问天": {"speaker": "ZH", "speed": 0.90},
    "混混头": {"speaker": "ZH", "speed": 1.0},
    "学生甲": {"speaker": "ZH", "speed": 1.0},
    "default": {"speaker": "ZH", "speed": 1.0},
}

# edge-tts 免费在线声线（零 API 成本，需联网）
VOICE_MAP_EDGE = {
    "龍慧慧": {"voice": "zh-CN-XiaoxiaoNeural", "rate": "-10%", "pitch": "+0Hz", "volume": "+0%"},
    "旁白": {"voice": "zh-CN-XiaoxiaoNeural", "rate": "-10%", "pitch": "+0Hz", "volume": "+0%"},
    "谢文东": {"voice": "zh-CN-YunxiNeural", "rate": "-15%", "pitch": "-30Hz", "volume": "+0%"},
    "三眼": {"voice": "zh-CN-YunxiNeural", "rate": "+0%", "pitch": "+20Hz", "volume": "+5%"},
    "李爽": {"voice": "zh-CN-YunxiNeural", "rate": "+10%", "pitch": "+30Hz", "volume": "+5%"},
    "高强": {"voice": "zh-CN-YunjianNeural", "rate": "-15%", "pitch": "-50Hz", "volume": "+0%"},
    "向问天": {"voice": "zh-CN-YunjianNeural", "rate": "-15%", "pitch": "-40Hz", "volume": "+0%"},
    "混混头": {"voice": "zh-CN-YunyangNeural", "rate": "+5%", "pitch": "+10Hz", "volume": "+5%"},
    "学生甲": {"voice": "zh-CN-YunxiaNeural", "rate": "+0%", "pitch": "+0Hz", "volume": "+0%"},
    "default": {"voice": "zh-CN-YunxiNeural", "rate": "+0%", "pitch": "+0Hz", "volume": "+0%"},
}


def voice_for(speaker: str, backend: str = "system") -> dict:
    speaker = clean_name(speaker)
    if backend == "kokoro":
        return VOICE_MAP_KOKORO.get(speaker, VOICE_MAP_KOKORO["default"])
    if backend == "edge":
        return VOICE_MAP_EDGE.get(speaker, VOICE_MAP_EDGE["default"])
    if backend == "melotts":
        return VOICE_MAP_MELOTTS.get(speaker, VOICE_MAP_MELOTTS["default"])
    return VOICE_MAP_SYSTEM.get(speaker, VOICE_MAP_SYSTEM["default"])


# ============================================================
# 素材解析
# ============================================================
def find_asset(ref: str) -> Path:
    """通过编码、文件名或模糊匹配找素材。"""
    if not ref:
        return None

    # 1. 完整文件名直接匹配
    p = WAREHOUSE_ROOT / ref
    if p.exists():
        return p

    # 2. 按编码前缀匹配
    code = ref.split("_")[0] if "_" in ref else ref.split(".")[0]
    candidates = []
    for f in WAREHOUSE_ROOT.rglob("*.png"):
        fname = f.name
        if fname == ref or fname.startswith(code + "_") or f.stem == code:
            candidates.append(f)

    if len(candidates) == 1:
        return candidates[0]

    # 3. 模糊语义匹配
    keywords = []
    if "持刀" in ref or "雨夜" in ref:
        keywords.append("持刀")
    if "锚点" in ref:
        keywords.append("锚点")
    if "侧面" in ref:
        keywords.append("侧面")
    if "全身" in ref:
        keywords.append("全身")
    if "特写" in ref:
        keywords.append("特写")
    if "抱拳" in ref:
        keywords.append("抱拳")
    if "伏案" in ref:
        keywords.append("伏案")
    if "举杯" in ref:
        keywords.append("举杯")

    for kw in keywords:
        for c in candidates:
            if kw in c.name:
                return c

    # 4. 兜底：返回第一个候选
    if candidates:
        return candidates[0]

    return None


def pick_shot_image(shot: dict) -> Path:
    """为镜头挑选一张可用素材。"""
    refs = shot.get("asset_refs", [])
    for ref in refs:
        asset = find_asset(ref)
        if asset:
            return asset

    # 兜底：按角色或场景编码找
    chars = shot.get("characters", [])
    for char in chars:
        code = char.split("-")[0] if "-" in char else char
        if code.startswith("HD-"):
            asset = find_asset(code)
            if asset:
                return asset

    scene = shot.get("scene_id", "ENV-02")
    asset = find_asset(scene)
    if asset:
        return asset

    # 最终兜底：任意场景
    for f in WAREHOUSE_ROOT.rglob("ENV-*.png"):
        return f

    return None


# F5-TTS 本地声音克隆声线（UID9622 官方声线）
# 速度统一放慢、pitch 轻微下沉，让整体更稳重、清晰、正经
VOICE_MAP_F5TTS = {
    "龍慧慧": {"ref": "origin_24k.wav", "pitch": -1, "speed": 0.82},
    "旁白":   {"ref": "origin_24k.wav", "pitch": -1, "speed": 0.82},
    "谢文东": {"ref": "origin_24k.wav", "pitch": -1, "speed": 0.80},
    "三眼":   {"ref": "origin_24k.wav", "pitch": -1, "speed": 0.88},
    "李爽":   {"ref": "origin_24k.wav", "pitch": -1, "speed": 0.90},
    "高强":   {"ref": "origin_24k.wav", "pitch": -2, "speed": 0.78},
    "向问天": {"ref": "origin_24k.wav", "pitch": -2, "speed": 0.80},
    "混混头": {"ref": "origin_24k.wav", "pitch": -1, "speed": 0.88},
    "学生甲": {"ref": "origin_24k.wav", "pitch": -1, "speed": 0.88},
    "default": {"ref": "origin_24k.wav", "pitch": -1, "speed": 0.85},
}


# ============================================================
# 语音合成
# ============================================================
def synthesize_line(text: str, speaker: str, out_path: Path, backend: str = "system") -> Path:
    """合成单句台词。backend: system / edge / kokoro / melotts / f5tts"""
    if backend == "f5tts":
        cfg = VOICE_MAP_F5TTS.get(clean_name(speaker), VOICE_MAP_F5TTS["default"])
        ref_file = WAREHOUSE_ROOT / "voice_samples" / "uid9622" / cfg["ref"]
        raw_path = out_path.with_suffix(".raw.wav")
        cmd = [
            str(VENV_PYTHON), str(FACTORY_ROOT / "lh_f5tts_clone.py"),
            "--ref", str(ref_file),
            "--gen", text,
            "--out", str(raw_path),
            "--pitch", str(cfg["pitch"]),
            "--speed", str(cfg["speed"]),
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # 统一采样率
        subprocess.run([
            "ffmpeg", "-y", "-i", str(raw_path),
            "-ar", str(AUDIO_RATE), "-ac", "1",
            str(out_path)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        raw_path.unlink(missing_ok=True)
        return out_path

    if backend == "melotts":
        cfg = voice_for(speaker, backend="melotts")
        raw_path = out_path.with_suffix(".raw.wav")
        cmd = [
            str(VENV_PYTHON), str(FACTORY_ROOT / "lh_melotts_tts.py"),
            text, "--out", str(raw_path),
            "--speaker", cfg["speaker"], "--speed", str(cfg["speed"]),
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # 统一采样率
        subprocess.run([
            "ffmpeg", "-y", "-i", str(raw_path),
            "-ar", str(AUDIO_RATE), "-ac", "1",
            str(out_path)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        raw_path.unlink(missing_ok=True)
        return out_path

    if backend == "kokoro":
        cfg = voice_for(speaker, backend="kokoro")
        voice = cfg["voice"]
        speed = cfg["speed"]
        raw_path = out_path.with_suffix(".raw.wav")
        cmd = [
            str(VENV_PYTHON), str(FACTORY_ROOT / "lh_kokoro_tts.py"),
            text, "--voice", voice, "--lang", "z", "--speed", str(speed),
            "--out", str(raw_path)
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # 统一采样率
        subprocess.run([
            "ffmpeg", "-y", "-i", str(raw_path),
            "-ar", str(AUDIO_RATE), "-ac", "1",
            str(out_path)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        raw_path.unlink(missing_ok=True)
        return out_path

    if backend == "edge":
        cfg = voice_for(speaker, backend="edge")
        voice = cfg["voice"]
        rate = cfg["rate"]
        pitch = cfg["pitch"]
        volume = cfg["volume"]
        mp3_path = out_path.with_suffix(".mp3")
        import asyncio
        try:
            import edge_tts
        except ImportError as e:
            raise RuntimeError(f"缺少 edge-tts: {e}") from e
        asyncio.run(edge_tts.Communicate(text, voice, rate=rate, pitch=pitch, volume=volume).save(str(mp3_path)))
        subprocess.run([
            "ffmpeg", "-y", "-i", str(mp3_path),
            "-ar", str(AUDIO_RATE), "-ac", "1",
            str(out_path)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        mp3_path.unlink(missing_ok=True)
        return out_path

    # 默认 system (macOS say)
    cfg = voice_for(speaker, backend="system")
    voice = cfg["voice"]
    rate = cfg["rate"]
    pitch = cfg["pitch"]

    aiff_path = out_path.with_suffix(".aiff")

    cmd = ["say", "-v", voice, "-r", str(rate), "-o", str(aiff_path), text]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # ffmpeg 转 wav，可选音高微调
    af = f"asetrate={AUDIO_RATE}*{2 ** (pitch / 1200):.4f},aresample={AUDIO_RATE}"
    subprocess.run([
        "ffmpeg", "-y", "-i", str(aiff_path),
        "-af", af,
        "-ar", str(AUDIO_RATE), "-ac", "1",
        str(out_path)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    aiff_path.unlink(missing_ok=True)
    return out_path


def parse_dialogue(dialogue: str) -> list:
    """把分镜表的 dialogue 字段拆成 [(说话人, 台词), ...]。"""
    if not dialogue:
        return []

    lines = []
    for raw in dialogue.split("\n"):
        raw = raw.strip()
        if not raw:
            continue
        if "：" in raw:
            speaker, text = raw.split("：", 1)
        elif ":" in raw:
            speaker, text = raw.split(":", 1)
        else:
            speaker, text = "旁白", raw
        text = text.strip()
        # 去掉语气括号，保留给 TTS 读？保留更有戏感
        lines.append((speaker.strip(), text))
    return lines


# ============================================================
# 画面生成（静态图 + 运镜模拟）
# ============================================================
def motion_for_shot(shot: dict, duration: int) -> str:
    """根据镜头类型生成 zoompan 表达式。"""
    shot_type = shot.get("shot_type", "中景")
    camera = shot.get("camera", "")
    frames = max(int(duration * FPS), 1)

    base = "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,"

    if "手持" in camera or "微抖" in camera:
        return base + (
            f"zoompan=z='min(1.05+on*0.0008,1.25)':"
            f"x='iw/2-(iw/zoom/2)+sin(on*0.5)*12':"
            f"y='ih/2-(ih/zoom/2)+cos(on*0.4)*8':"
            f"d={frames}:s={RESOLUTION}:fps={FPS}"
        )
    if "特写" in shot_type:
        return base + (
            f"zoompan=z='min(1.1+on*0.0025,1.6)':"
            f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
            f"d={frames}:s={RESOLUTION}:fps={FPS}"
        )
    if "双人" in shot_type or "过肩" in shot_type:
        return base + (
            f"zoompan=z='1.15':"
            f"x='iw/2-(iw/zoom/2)+on*{1280 / frames}':"
            f"y='ih/2-(ih/zoom/2)':"
            f"d={frames}:s={RESOLUTION}:fps={FPS}"
        )
    if "全景" in shot_type or "远景" in shot_type or "空镜" in shot_type:
        return base + (
            f"zoompan=z='max(1.3-on*0.0015,1.0)':"
            f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
            f"d={frames}:s={RESOLUTION}:fps={FPS}"
        )

    # 默认：中景慢推
    return base + (
        f"zoompan=z='min(1.05+on*0.0010,1.3)':"
        f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        f"d={frames}:s={RESOLUTION}:fps={FPS}"
    )


def _prompt_for_shot(shot: dict) -> str:
    """从分镜信息生成 AnimateDiff 提示词。"""
    parts = []
    visual = shot.get("visual", "")
    if visual:
        parts.append(visual)
    camera = shot.get("camera", "")
    if camera:
        parts.append(f"camera: {camera}")
    emotion = shot.get("emotion", "")
    if emotion:
        parts.append(f"mood: {emotion}")
    shot_type = shot.get("shot_type", "")
    if shot_type:
        parts.append(f"{shot_type} shot")
    prompt = ", ".join(parts)
    # 简单英化（AnimateDiff 对英文提示词更稳）
    return prompt


def generate_shot_video(image_path: Path, shot: dict, out_path: Path, backend: str = "zoompan") -> Path:
    """生成镜头视频。backend: zoompan / animatediff。"""
    duration = shot.get("duration_sec", 3)
    shot_id = shot.get("shot_id", "SHOT")

    if backend == "animatediff":
        # 调用视频引擎的 AnimateDiff 后端
        import lh_video_engine as ve
        result = ve.generate(
            image_path=str(image_path),
            prompt=_prompt_for_shot(shot),
            backend="animatediff",
            duration=duration,
            shot_code=shot_id,
        )
        if result and Path(result).exists():
            # 视频引擎已经把文件放到固定目录，复制到 assembler 期望的位置
            shutil.copy2(result, out_path)
            # AnimateDiff 单段最多 2s，用循环铺满镜头时长
            actual_dur = get_duration(out_path)
            if actual_dur and actual_dur < duration - 0.5:
                looped = out_path.with_suffix(".loop.mp4")
                subprocess.run([
                    "ffmpeg", "-y", "-stream_loop", "-1", "-i", str(out_path),
                    "-t", str(duration), "-c:v", "libx264", "-pix_fmt", "yuv420p",
                    "-r", str(FPS), "-an", str(looped)
                ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                shutil.move(looped, out_path)
            return out_path
        # 失败回退 zoompan
        print(f"   ⚠️ [{shot_id}] AnimateDiff 失败，回退 zoompan")

    # zoompan 兜底
    vf = motion_for_shot(shot, duration)
    subprocess.run([
        "ffmpeg", "-y", "-loop", "1", "-i", str(image_path),
        "-vf", vf,
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-r", str(FPS), "-t", str(duration),
        "-an", str(out_path)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return out_path


# ============================================================
# 总装
# ============================================================
def assemble_ep01(storyboard_path: Path, output_root: Path, backend_voice: str = "system", backend_video: str = "zoompan") -> dict:
    output_root.mkdir(parents=True, exist_ok=True)
    audio_dir = output_root / "audio"
    video_dir = output_root / "video"
    final_dir = output_root / "final"
    for d in (audio_dir, video_dir, final_dir):
        d.mkdir(parents=True, exist_ok=True)

    with open(storyboard_path, "r", encoding="utf-8") as f:
        sb = json.load(f)

    shots = sb.get("shots", [])
    pipeline_dna = generate_dna("EP01-ASSEMBLE")
    print(f"🐉 龍魂 EP01 装配器启动")
    print(f"🧬 Pipeline DNA: {pipeline_dna}")
    print(f"🎙️ 语音后端: {backend_voice}")
    print(f"🎬 视频后端: {backend_video}")
    print(f"🎞️ 镜头数: {len(shots)}，目标总长: {sb.get('total_duration_sec')} 秒\n")

    # ============================================================
    # 1. 生成每条台词音频
    # ============================================================
    print("🎙️ 第一步：生成台词音频...")
    # 先计算每个镜头的起始时间，用于台词内部顺序编排
    shot_starts = {}
    t = 0.0
    for shot in shots:
        shot_starts[shot["shot_id"]] = t
        t += shot.get("duration_sec", 3)

    audio_manifest = []
    shot_line_cursor = {}  # 记录每个镜头已用掉的音频时长
    for shot in shots:
        shot_id = shot["shot_id"]
        lines = parse_dialogue(shot.get("dialogue", ""))
        shot_line_cursor[shot_id] = 0.0
        for idx, (speaker, text) in enumerate(lines):
            safe_text = re.sub(r"[^\u4e00-\u9fa5a-zA-Z0-9]", "_", text[:12])
            out_name = f"{shot_id}_A{idx:02d}_{clean_name(speaker)}_{safe_text}.wav"
            out_path = audio_dir / out_name
            print(f"   [{shot_id}] {speaker}: {text[:24]}...")
            try:
                synthesize_line(text, speaker, out_path, backend_voice)
                dur = get_duration(out_path)
                line_start = shot_starts[shot_id] + shot_line_cursor[shot_id]
                shot_line_cursor[shot_id] += dur
                audio_manifest.append({
                    "shot_id": shot_id,
                    "speaker": speaker,
                    "text": text,
                    "path": str(out_path),
                    "duration": dur,
                    "start_time": line_start,
                })
            except Exception as e:
                print(f"   ⚠️ 语音失败: {e}")

    # ============================================================
    # 2. 生成每个镜头视频
    # ============================================================
    print("\n🎬 第二步：生成镜头视频...")
    video_manifest = []
    for shot in shots:
        shot_id = shot["shot_id"]
        shot["dna"] = generate_dna(shot_id)
        img = pick_shot_image(shot)
        out_path = video_dir / f"{shot_id}.mp4"
        if img:
            print(f"   [{shot_id}] 素材: {img.name}")
            try:
                generate_shot_video(img, shot, out_path, backend=backend_video)
                video_manifest.append({
                    "shot_id": shot_id,
                    "image": str(img),
                    "video": str(out_path),
                    "duration": shot.get("duration_sec", 3),
                })
            except Exception as e:
                print(f"   ⚠️ 视频生成失败: {e}")
        else:
            print(f"   ⚠️ [{shot_id}] 未找到素材，生成占位图")
            # 生成纯色占位（无 drawtext，因为本机 ffmpeg 未编译 freetype）
            subprocess.run([
                "ffmpeg", "-y", "-f", "lavfi", "-i",
                f"color=c=black:s={RESOLUTION}:d={shot.get('duration_sec', 3)}",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(FPS),
                str(out_path)
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            video_manifest.append({
                "shot_id": shot_id,
                "image": None,
                "video": str(out_path),
                "duration": shot.get("duration_sec", 3),
            })

    # ============================================================
    # 3. 拼接视频
    # ============================================================
    print("\n🧩 第三步：拼接视频轨道...")
    concat_list = video_dir / "concat.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for vm in video_manifest:
            f.write(f"file '{vm['video']}'\n")

    video_final = final_dir / "EP01_video_only.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy", str(video_final)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # ============================================================
    # 4. 拼接音频（按镜头时间码对齐）
    # ============================================================
    print("\n🔊 第四步：合成对白音轨...")
    total_video_duration = sum(s.get("duration_sec", 3) for s in shots)

    # 创建空白底噪轨
    silent_base = final_dir / "silence.wav"
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi", "-i",
        f"anullsrc=r={AUDIO_RATE}:cl=mono", "-t", str(total_video_duration),
        "-acodec", "pcm_s16le", str(silent_base)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 构建 amix filter：每条音频 delay 到对应台词起点
    # 输入 0 是空白底噪，filter_complex 中用 [0:a] 引用
    inputs = ["-i", str(silent_base)]
    amix_inputs = ["[0:a]"]
    am_input_idx = 1

    for am in audio_manifest:
        inputs.extend(["-i", str(am["path"])])
        amix_inputs.append(f"[a{am_input_idx}d]")
        am_input_idx += 1

    # 延迟 filter：使用每条台词的 start_time
    delay_filters = []
    for i in range(1, am_input_idx):
        delay_ms = int(audio_manifest[i - 1]["start_time"] * 1000)
        delay_filters.append(f"[{i}:a]adelay={delay_ms}|{delay_ms}[a{i}d]")

    amix_filter = "".join(amix_inputs) + f"amix=inputs={am_input_idx}:duration=first:dropout_transition=0:normalize=0[aout]"
    full_filter = ";".join(delay_filters + [amix_filter])

    audio_final = final_dir / "EP01_audio_only.wav"
    cmd = ["ffmpeg", "-y"] + inputs + ["-filter_complex", full_filter, "-map", "[aout]", "-ac", "1", str(audio_final)]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # ============================================================
    # 5. 合并音视频
    # ============================================================
    print("\n🎞️ 第五步：合并音画...")
    final_mp4 = final_dir / "EP01_雪夜初见_成片_v1.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-i", str(video_final), "-i", str(audio_final),
        "-c:v", "copy", "-c:a", "aac", "-b:a", "128k",
        "-shortest", str(final_mp4)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    final_duration = get_duration(final_mp4)

    # ============================================================
    # 6. 保存清单
    # ============================================================
    manifest = {
        "dna": pipeline_dna,
        "project": "badai",
        "storyboard": str(storyboard_path),
        "final_video": str(final_mp4),
        "final_duration": final_duration,
        "resolution": RESOLUTION,
        "fps": FPS,
        "audio_manifest": audio_manifest,
        "video_manifest": video_manifest,
        "total_shots": len(shots),
        "target_duration": sb.get("total_duration_sec"),
        "backend_voice": backend_voice,
        "created": datetime.now().isoformat(),
        "note": f"低成本本地装配：本地TTS + 视频后端({backend_video})。",
    }
    manifest_path = final_dir / "EP01_assembly_manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    # 创建快捷入口，方便用户找到成片
    project_link = Path.home() / "longhun-system" / "龍魂成片"
    warehouse_link = WAREHOUSE_ROOT / "龍魂成片"
    movies_link = Path.home() / "Movies" / "龍魂成片"
    try:
        for link in (project_link, warehouse_link):
            if link.exists() or link.is_symlink():
                link.unlink()
            link.symlink_to(FINAL_OUTPUT_ROOT, target_is_directory=True)
        if movies_link.exists() or movies_link.is_symlink():
            movies_link.unlink()
        movies_link.symlink_to(SHORTCUT_ROOT, target_is_directory=True)
    except Exception as e:
        print(f"   ⚠️ 快捷入口创建失败: {e}")

    print(f"\n✅ EP01 装配完成")
    print(f"   成片: {final_mp4}")
    print(f"   固定目录: {FINAL_OUTPUT_ROOT}")
    print(f"   快捷入口: {project_link}  /  {warehouse_link}  /  {movies_link}")
    print(f"   时长: {final_duration:.2f} 秒")
    print(f"   清单: {manifest_path}")

    return manifest


def main():
    parser = argparse.ArgumentParser(description="龍魂 · EP01 低成本本地装配器")
    parser.add_argument("--storyboard", default=str(STORYBOARD_PATH), help="分镜表 JSON 路径")
    parser.add_argument("--output", default=str(OUTPUT_ROOT), help="输出目录")
    parser.add_argument("--backend-voice", default="system", choices=["system", "edge", "kokoro", "melotts", "f5tts"], help="TTS 后端: system=macOS say, edge=免费在线TTS, kokoro=本地模型, melotts=本地MeloTTS, f5tts=本地F5-TTS声音克隆(UID9622官方声线)")
    parser.add_argument("--backend-video", default="zoompan", choices=["zoompan", "animatediff"], help="视频后端: zoompan=静态图运镜模拟, animatediff=ComfyUI真实运动生成")
    args = parser.parse_args()

    assemble_ep01(Path(args.storyboard), Path(args.output), args.backend_voice, args.backend_video)


if __name__ == "__main__":
    main()
