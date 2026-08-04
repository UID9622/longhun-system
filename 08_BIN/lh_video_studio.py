#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
龍魂视频工坊 v4.0 —— UID9622 真声 + 龍魂签章 + AI视觉图示 + 字幕
================================================================================
功能：将文本解说稿一键转换为带 UID9622 真声克隆配音、龍魂签章品牌叠加、
      AI自动生成的流程图/架构图/知识图谱/对比图/时间线的高清视频
风格：黑底金边军事风 · 龍魂视觉主权 · 数字人签章

DNA: #龍芯⚡️丙午-乙巳-2026-07-29-VIDEO-STUDIO-v4.0-SEAL-VOICE
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
声纹引擎: lh_voice_clone.py（XTTS v2 · 31分钟口语样本训练）
签章引擎: lh_gpg_sign.py（GPG分离签名 · GATE-11签章闸）
视觉引擎: lh_visual_engine.py（9种图示自动生成）

使用方式:
    python3 lh_video_studio.py --script 解说稿.txt --style 龍魂 --voice uid9622 --name "标题"
    # uid9622 = UID9622真声克隆（干净有力·退伍军人风格）
    # 其他voice = edge-tts云端语音（兜底）

依赖:
    - Python 3.9+
    - ffmpeg (系统级)
    - edge-tts, moviepy, pillow, numpy
    - (uid9622真声需先运行: bash bin/lh_voice_clone_setup.sh)
================================================================================
"""

import os
import sys

# 确保能从 bin/ 导入龍魂模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import re
import io
import json
import time
import random
import asyncio
import argparse
import subprocess
import textwrap
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Optional

# =============================================================================
# 0. 龍魂签章 & 品牌资产（视频帧叠加用）
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SEAL_DIR = PROJECT_ROOT / "brand" / "seals"
BRAND_DIR = PROJECT_ROOT / "brand"

# 签章资产（生成脚本: python3 longhun-font/calligraphy/seal_generator.py）
SEAL_CORNER = SEAL_DIR / "seal_龙魂_square_128.png"     # 右下角签章（128px）
SEAL_WATERMARK = SEAL_DIR / "seal_龙魂_circle_128.png"   # 水印圆章
BADGE_A = BRAND_DIR / "badge-A.png"                       # 龍魂徽章（左上角）

# 检查资产是否存在，不存在则优雅降级（不阻碍生成）
_SEAL_AVAILABLE = SEAL_CORNER.exists()
_BADGE_AVAILABLE = BADGE_A.exists()

# =============================================================================
# 1. 依赖检查与友好提示
# =============================================================================

def check_dependency(module_name: str, pip_name: str) -> bool:
    """检查Python依赖是否已安装"""
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False

MISSING = []
for mod, pip in [("edge_tts", "edge-tts"), ("moviepy", "moviepy"), ("PIL", "pillow"), ("numpy", "numpy")]:
    if not check_dependency(mod, pip):
        MISSING.append(pip)

if MISSING:
    print("❌ 缺少以下依赖，请先执行安装:")
    print(f"   pip install {' '.join(MISSING)}")
    sys.exit(1)

# 检查 ffmpeg
FFMPEG_OK = subprocess.run(["ffmpeg", "-version"], capture_output=True).returncode == 0
if not FFMPEG_OK:
    print("❌ 未检测到 ffmpeg，请先安装: brew install ffmpeg (macOS) 或 apt install ffmpeg (Linux)")
    sys.exit(1)

from edge_tts import Communicate
from moviepy import (
    ImageClip, ColorClip, TextClip, AudioFileClip,
    CompositeVideoClip, concatenate_videoclips, CompositeAudioClip
)
from moviepy.video.fx import FadeIn, FadeOut
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

# =============================================================================
# 1. 全局配置与常量
# =============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = Path.home() / "Desktop" / "龙魂视频"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 龍魂配色体系 (黑底金边军事风)
COLOR_SCHEME = {
    "龍魂": {
        "bg_top": (10, 8, 20),      # 深黑紫
        "bg_bottom": (25, 15, 5),   # 深褐
        "accent": (212, 175, 55),   # 金色
        "accent2": (180, 50, 30),   # 暗红
        "text": (255, 250, 240),    # 暖白
        "stroke": (0, 0, 0),        # 黑边
        "subtitle_bg": (0, 0, 0, 160),  # 半透明黑底
    },
    "历史": {
        "bg_top": (30, 20, 10),
        "bg_bottom": (60, 40, 20),
        "accent": (200, 160, 80),
        "accent2": (120, 60, 30),
        "text": (255, 245, 220),
        "stroke": (20, 10, 5),
        "subtitle_bg": (20, 10, 5, 180),
    },
    "科技": {
        "bg_top": (5, 10, 25),
        "bg_bottom": (10, 30, 50),
        "accent": (0, 200, 255),
        "accent2": (0, 100, 200),
        "text": (220, 240, 255),
        "stroke": (0, 0, 10),
        "subtitle_bg": (0, 10, 30, 170),
    },
    "战争": {
        "bg_top": (25, 10, 10),
        "bg_bottom": (50, 20, 15),
        "accent": (220, 60, 40),
        "accent2": (180, 40, 20),
        "text": (255, 230, 220),
        "stroke": (30, 5, 5),
        "subtitle_bg": (30, 5, 5, 180),
    },
    "自然": {
        "bg_top": (10, 30, 20),
        "bg_bottom": (20, 50, 35),
        "accent": (100, 220, 120),
        "accent2": (50, 150, 80),
        "text": (240, 255, 245),
        "stroke": (5, 20, 10),
        "subtitle_bg": (5, 20, 10, 160),
    },
    "默认": {
        "bg_top": (15, 15, 25),
        "bg_bottom": (30, 30, 45),
        "accent": (180, 180, 200),
        "accent2": (100, 100, 150),
        "text": (240, 240, 250),
        "stroke": (0, 0, 0),
        "subtitle_bg": (0, 0, 0, 150),
    },
}

# 视频参数
VIDEO_W, VIDEO_H = 1920, 1080
FPS = 24
CODEC = "libx264"
AUDIO_CODEC = "aac"
PRESET = "medium"  # 平衡速度和质量
CRF = "23"         # 质量参数，越小越好

# =============================================================================
# 2. 工具函数
# =============================================================================

def log(msg: str, level: str = "INFO"):
    """统一日志输出，带时间戳"""
    ts = datetime.now().strftime("%H:%M:%S")
    icons = {"INFO": "ℹ️", "OK": "✅", "WARN": "⚠️", "ERROR": "❌", "STEP": "🔥", "DNA": "🧬"}
    icon = icons.get(level, "•")
    print(f"[{ts}] {icon} {msg}")


def find_font() -> str:
    """跨平台自动寻找可用的中文字体"""
    candidates = []
    system = os.uname().sysname if hasattr(os, "uname") else "Unknown"

    if system == "Darwin":  # macOS
        candidates = [
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/STHeiti Light.ttc",
            "/System/Library/Fonts/Hiragino Sans GB.ttc",
            "/Library/Fonts/Arial Unicode.ttf",
        ]
    elif system == "Linux":
        candidates = [
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]
    else:  # Windows or fallback
        candidates = [
            "C:/Windows/Fonts/simhei.ttf",
            "C:/Windows/Fonts/msyh.ttc",
            "C:/Windows/Fonts/simsun.ttc",
        ]

    for path in candidates:
        if os.path.exists(path):
            return path

    # 如果都找不到，返回 None，让 moviepy 用默认字体（但中文可能乱码）
    log("未找到中文字体，字幕可能显示为方框。建议安装: macOS用PingFang, Linux用文泉驿/Noto", "WARN")
    return None


def generate_gradient_background(
    width: int = VIDEO_W,
    height: int = VIDEO_H,
    colors: dict = None,
    seed: int = None
) -> Image.Image:
    """
    生成高质量渐变背景图（龍魂风格）
    支持：线性渐变 + 径向光晕 + 噪点纹理 + 装饰性几何线条
    """
    if seed is not None:
        random.seed(seed)

    if colors is None:
        colors = COLOR_SCHEME["龍魂"]

    top = colors["bg_top"]
    bottom = colors["bg_bottom"]
    accent = colors["accent"]
    accent2 = colors["accent2"]

    # 创建基础渐变
    img = Image.new('RGB', (width, height), top)
    draw = ImageDraw.Draw(img)

    # 线性渐变（从上到下）
    for y in range(height):
        ratio = y / height
        r = int(top[0] * (1 - ratio) + bottom[0] * ratio)
        g = int(top[1] * (1 - ratio) + bottom[1] * ratio)
        b = int(top[2] * (1 - ratio) + bottom[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # 添加径向光晕（模拟聚光灯效果）
    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)

    # 中心光晕
    cx, cy = width // 2, height // 2
    max_radius = int(max(width, height) * 0.8)
    for r in range(max_radius, 0, -5):
        alpha = int(8 * (1 - r / max_radius))
        if alpha <= 0:
            continue
        color = (*accent, alpha)
        overlay_draw.ellipse(
            [cx - r, cy - r, cx + r, cy + r],
            outline=color, width=3
        )

    # 角落暗角
    corner_overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    corner_draw = ImageDraw.Draw(corner_overlay)
    for i in range(200):
        alpha = int(30 * (1 - i / 200))
        corner_draw.rectangle([0, 0, i, i], fill=(0, 0, 0, alpha))
        corner_draw.rectangle([width - i, 0, width, i], fill=(0, 0, 0, alpha))
        corner_draw.rectangle([0, height - i, i, height], fill=(0, 0, 0, alpha))
        corner_draw.rectangle([width - i, height - i, width, height], fill=(0, 0, 0, alpha))

    img = Image.alpha_composite(img.convert('RGBA'), overlay)
    img = Image.alpha_composite(img, corner_overlay)

    # 添加装饰性线条（龍魂金边）
    line_draw = ImageDraw.Draw(img)
    # 顶部金线
    line_draw.line([(50, 50), (width - 50, 50)], fill=(*accent, 120), width=2)
    # 底部金线
    line_draw.line([(50, height - 50), (width - 50, height - 50)], fill=(*accent, 120), width=2)
    # 侧边装饰
    for offset in [0, 4]:
        line_draw.line([(50 + offset, 50), (50 + offset, height - 50)], fill=(*accent, 40), width=1)
        line_draw.line([(width - 50 - offset, 50), (width - 50 - offset, height - 50)], fill=(*accent, 40), width=1)

    # 添加微妙噪点纹理
    pixels = img.load()
    for _ in range(width * height // 20):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        r, g, b, a = pixels[x, y]
        noise = random.randint(-8, 8)
        pixels[x, y] = (
            max(0, min(255, r + noise)),
            max(0, min(255, g + noise)),
            max(0, min(255, b + noise)),
            a
        )

    return img.convert('RGB')


def parse_video_script_md(text: str) -> str:
    """
    从视频脚本 markdown 中提取干净的旁白文本。
    砍掉：元数据头(DNA/创建者/协议)、##标题、>视觉方向、|表格|、---分割线
    保留：【旁白】段落中的实际解说词
    """
    lines = text.split('\n')
    narration_parts = []
    in_narration = False
    in_metadata = True

    for line in lines:
        stripped = line.strip()

        # 空行：在旁白中保留段落分隔
        if not stripped:
            if in_narration:
                narration_parts.append('')
            continue

        # 元数据区：DNA/创建者/协议/确认码 → 全部跳过
        if in_metadata:
            # 标题、分割线、旁白标记 → 退出元数据模式
            if stripped.startswith('##') or stripped == '---' or stripped == '【旁白】':
                in_metadata = False
                # 如果是【旁白】行自身不收入，由下方的【旁白】区块处理
                continue
            # 匹配元数据行：DNA: / 创建者: / 协议: / 时长: / 风格: / 泄密审查:
            if re.match(r'^(DNA|创建者|协议|时长|风格|泄密审查|确认码)', stripped):
                continue
            # 非元数据行 → 退出元数据模式，继续正常处理
            in_metadata = False
            # 不 continue，让下面的逻辑处理它

        # 分割线 → 重置状态
        if stripped == '---':
            in_narration = False
            continue

        # markdown 标题 → 不在旁白中
        if stripped.startswith('##'):
            in_narration = False
            continue

        # 视觉方向行 > 🎬 → 跳过
        if stripped.startswith('>'):
            in_narration = False
            continue

        # 表格行 → 跳过整段
        if stripped.startswith('|'):
            in_narration = False
            continue

        # 【旁白】标记 → 开始收集
        if stripped == '【旁白】':
            in_narration = True
            continue

        # 制作备注/分段建议 等尾部附录 → 停止
        if re.match(r'^##\s*(制作备注|视频分段|制作参数)', stripped):
            break

        # 非旁白区域的任意文本 → 跳过
        if not in_narration:
            continue

        # 清理行内格式
        cleaned = stripped
        cleaned = re.sub(r'\*\*(.+?)\*\*', r'\1', cleaned)   # 去加粗
        cleaned = re.sub(r'__(.+?)__', r'\1', cleaned)       # 去加粗(v2)
        cleaned = re.sub(r'\*(.+?)\*', r'\1', cleaned)       # 去斜体
        cleaned = re.sub(r'`(.+?)`', r'\1', cleaned)         # 去行内代码
        cleaned = re.sub(r'~~(.+?)~~', r'\1', cleaned)       # 去删除线

        narration_parts.append(cleaned)

    # 合并，清理多余空行
    text = '\n'.join(narration_parts)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def split_text_into_scenes(text: str, max_chars: int = 160, min_chars: int = 40) -> List[str]:
    """
    智能切分文本为场景
    策略：优先按段落 → 按句号/感叹号/问号 → 按逗号 → 强制截断
    """
    text = text.strip()
    if not text:
        return []

    # 先按段落分割
    paragraphs = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]

    scenes = []
    for para in paragraphs:
        # 如果段落本身在合理长度内，直接作为一个场景
        if len(para) <= max_chars and len(para) >= min_chars:
            scenes.append(para)
            continue

        # 按句子分割（句号、感叹号、问号）
        sentences = re.split(r'([。！？])', para)
        # 把标点符号合并回句子
        merged = []
        i = 0
        while i < len(sentences):
            if i + 1 < len(sentences) and sentences[i + 1] in "。！？":
                merged.append(sentences[i] + sentences[i + 1])
                i += 2
            else:
                if sentences[i].strip():
                    merged.append(sentences[i])
                i += 1

        # 合并短句，拆分长句
        current = ""
        for sent in merged:
            sent = sent.strip()
            if not sent:
                continue
            if len(current) + len(sent) <= max_chars:
                current += sent
            else:
                if current:
                    scenes.append(current)
                # 如果单句就超过max_chars，需要进一步拆分
                if len(sent) > max_chars:
                    # 按逗号、顿号拆分
                    parts = re.split(r'([，、])', sent)
                    sub_current = ""
                    for part in parts:
                        if len(sub_current) + len(part) <= max_chars:
                            sub_current += part
                        else:
                            if sub_current:
                                scenes.append(sub_current)
                            sub_current = part
                    if sub_current:
                        scenes.append(sub_current)
                else:
                    current = sent
        if current:
            scenes.append(current)

    # 过滤太短的场景（尝试合并）
    final_scenes = []
    buffer = ""
    for s in scenes:
        if len(s) < min_chars:
            if len(buffer) + len(s) <= max_chars:
                buffer += s
            else:
                if buffer:
                    final_scenes.append(buffer)
                buffer = s
        else:
            if buffer:
                if len(buffer) + len(s) <= max_chars:
                    buffer += s
                    final_scenes.append(buffer)
                    buffer = ""
                else:
                    final_scenes.append(buffer)
                    final_scenes.append(s)
            else:
                final_scenes.append(s)
    if buffer:
        final_scenes.append(buffer)

    return [s.strip() for s in final_scenes if s.strip()]


# =============================================================================
# 3. 音频生成（含 XTTS 真声克隆）
# =============================================================================

# XTTS venv Python（用于真声克隆，与 edge-tts 共存）
_VENV_PYTHON = PROJECT_ROOT / ".venv_tts" / "bin" / "python3"
_REFERENCE_WAV = PROJECT_ROOT / "docs" / "reference_optimized.wav"


def _generate_xtts_audio(text: str, output_path: str, language: str = "zh") -> bool:
    """
    调用 XTTS v2（在 .venv_tts 中）合成 UID9622 真声。
    返回 True=成功, False=需要兜底 edge-tts。
    """
    if not _VENV_PYTHON.exists():
        return False
    if not _REFERENCE_WAV.exists():
        return False

    code = f"""
import os, sys
os.environ['COQUI_TOS_AGREED'] = '1'
from pathlib import Path
from TTS.api import TTS
ref = Path('{_REFERENCE_WAV}')
out = Path('{output_path}')
out.parent.mkdir(parents=True, exist_ok=True)
try:
    tts = TTS('tts_models/multilingual/multi-dataset/xtts_v2', gpu=False)
except Exception:
    sys.exit(99)
tts.tts_to_file(text='''{text}''', speaker_wav=str(ref), language='{language}', file_path=str(out))
"""

    try:
        result = subprocess.run(
            [str(_VENV_PYTHON), "-c", code],
            capture_output=True, text=True,
            timeout=120,
            cwd=str(PROJECT_ROOT),
        )
        if result.returncode == 99:
            return False  # XTTS模型加载失败
        return result.returncode == 0 and Path(output_path).exists()
    except Exception:
        return False


async def generate_audio_batch(
    scenes: List[str],
    output_dir: Path,
    voice: str = "zh-CN-YunxiNeural"
) -> List[Tuple[str, float]]:
    """
    批量异步生成音频，返回 (文件路径, 时长秒) 列表。
    支持 voice="uid9622" → XTTS v2 真声克隆（31分钟口语样本训练）。
    其他 voice → edge-tts 云端语音（兜底）。
    """
    # 判断是否使用真声克隆
    use_true_voice = voice.lower() in ("uid9622", "真声", "longhun", "zhugexin")

    async def _gen_one(idx: int, text: str) -> Tuple[str, float]:
        if use_true_voice:
            # XTTS v2 真声克隆路径
            audio_path = output_dir / f"temp_audio_{idx:03d}.wav"
            success = _generate_xtts_audio(text, str(audio_path))
            if not success:
                # XTTS 不可用 → 降级 edge-tts
                audio_path = output_dir / f"temp_audio_{idx:03d}.mp3"
                try:
                    communicate = Communicate(text, "zh-CN-YunxiNeural")
                    await communicate.save(str(audio_path))
                except Exception as e:
                    log(f"场景 {idx+1} 音频降级也失败: {e}", "ERROR")
                    return None, 0.0
        else:
            # edge-tts 云端路径
            audio_path = output_dir / f"temp_audio_{idx:03d}.mp3"
            try:
                communicate = Communicate(text, voice)
                await communicate.save(str(audio_path))
            except Exception as e:
                log(f"场景 {idx+1} 音频生成失败: {e}", "ERROR")
                return None, 0.0

        # 获取音频时长
        try:
            result = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                 "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)],
                capture_output=True, text=True, timeout=10
            )
            duration = float(result.stdout.strip())
        except Exception:
            duration = max(2.0, len(text) / 4.5)

        return str(audio_path), duration

    tasks = [_gen_one(i, text) for i, text in enumerate(scenes)]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    valid_results = []
    for r in results:
        if isinstance(r, tuple) and r[0] is not None:
            valid_results.append(r)

    return valid_results


def pil_render_text(
    text: str,
    font_path: str,
    fontsize: int,
    color: tuple,
    stroke_color: Optional[tuple] = None,
    stroke_width: int = 0,
    bg_color: Optional[tuple] = None,
    max_width: int = 1600,
    padding: int = 20,
) -> bytes:
    """
    用PIL原生渲染文本（替代ImageMagick依赖）
    返回PNG字节流，支持：描边、半透明背景、自动换行
    """
    # 加载字体
    try:
        font = ImageFont.truetype(font_path, fontsize)
    except Exception:
        font = ImageFont.load_default()

    # 自动换行（中文按字符，英文按空格）
    lines = textwrap.wrap(text, width=22)

    # 测量文本尺寸
    temp_img = Image.new('RGBA', (1, 1))
    temp_draw = ImageDraw.Draw(temp_img)

    line_heights = []
    line_widths = []
    for line in lines:
        bbox = temp_draw.textbbox((0, 0), line, font=font)
        line_widths.append(bbox[2] - bbox[0])
        line_heights.append(bbox[3] - bbox[1])

    line_h = max(line_heights) if line_heights else fontsize + 10
    txt_w = min(max(line_widths) if line_widths else 100, max_width)
    txt_h = line_h * len(lines)

    # 画布尺寸
    sw = stroke_width
    img_w = txt_w + padding * 2 + sw * 4
    img_h = txt_h + padding * 2 + sw * 4

    # 创建画布（RGBA）
    if bg_color and len(bg_color) == 4:
        img = Image.new('RGBA', (img_w, img_h), bg_color)
    elif bg_color:
        img = Image.new('RGBA', (img_w, img_h), (*bg_color, 255))
    else:
        img = Image.new('RGBA', (img_w, img_h), (0, 0, 0, 0))

    draw = ImageDraw.Draw(img)

    # 描边（画在文字下面）
    if stroke_color and stroke_width > 0:
        for dx in range(-stroke_width, stroke_width + 1):
            for dy in range(-stroke_width, stroke_width + 1):
                if dx == 0 and dy == 0:
                    continue
                y_off = padding + sw * 2
                for line in lines:
                    draw.text((padding + sw * 2 + dx, y_off + dy), line,
                              font=font, fill=stroke_color)
                    y_off += line_h

    # 主文字
    y_off = padding + sw * 2
    for line in lines:
        draw.text((padding + sw * 2, y_off), line, font=font, fill=color)
        y_off += line_h

    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()


def create_subtitle_clip(
    text: str,
    duration: float,
    colors: dict,
    font_path: Optional[str] = None
):
    """
    龍魂风格字幕（PIL原生渲染，零ImageMagick依赖）
    """
    wrapped = textwrap.fill(text, width=22)
    line_count = wrapped.count('\n') + 1
    if line_count <= 2:
        fontsize = 56
    elif line_count <= 4:
        fontsize = 48
    else:
        fontsize = 40

    font = font_path or find_font() or "Arial"
    subtitle_bg = colors.get("subtitle_bg", (0, 0, 0, 160))
    text_color_rgb = colors.get("text", (255, 250, 240))
    stroke_rgb = colors.get("stroke", (0, 0, 0))

    png_bytes = pil_render_text(
        wrapped, font, fontsize,
        color=text_color_rgb,
        stroke_color=stroke_rgb,
        stroke_width=3,
        bg_color=subtitle_bg,
        max_width=1600,
    )

    pil_img = Image.open(io.BytesIO(png_bytes))
    np_frame = np.array(pil_img)

    clip = ImageClip(np_frame).with_duration(duration)
    txt_h = np_frame.shape[0]
    margin_bottom = 120
    pos_y = VIDEO_H - txt_h - margin_bottom
    return clip.with_position(("center", pos_y))


def simple_text_clip(
    text: str,
    duration: float,
    fontsize: int = 24,
    color: tuple = (255, 255, 255),
    font_path: Optional[str] = None,
    stroke_color: Optional[tuple] = None,
    stroke_width: int = 1,
    bg_color: Optional[tuple] = None,
) -> ImageClip:
    """PIL原生渲染简单文字Clip（替代TextClip，用于标记/水印）"""
    font = font_path or find_font() or "Arial"
    png_bytes = pil_render_text(
        text, font, fontsize,
        color=color,
        stroke_color=stroke_color,
        stroke_width=stroke_width,
        bg_color=bg_color,
        max_width=1920,
        padding=8,
    )
    pil_img = Image.open(io.BytesIO(png_bytes))
    np_frame = np.array(pil_img)
    return ImageClip(np_frame).with_duration(duration)


def create_scene_clip(
    scene_text: str,
    audio_path: str,
    duration: float,
    colors: dict,
    font_path: Optional[str] = None,
    scene_idx: int = 0,
    total_scenes: int = 1,
    section_images: Optional[List[Path]] = None,
) -> CompositeVideoClip:
    """
    创建单个场景的视频片段
    包含：背景图 + 字幕 + 签章品牌叠加 + 音频 + 淡入淡出 + 场景标记
    龍魂签章：右下角「龍魂」方章（128px）
    龍魂徽章：左上角 badge-A（80px）
    """
    # 1. 背景图：优先使用外部AI图解 → 降级为渐变背景
    use_custom_image = section_images and len(section_images) > 0
    if use_custom_image:
        img_idx = scene_idx % len(section_images)
        bg_path = section_images[img_idx]
        bg_clip = ImageClip(str(bg_path)).with_duration(duration)
        bg_clip = bg_clip.resized((VIDEO_W, VIDEO_H))
    else:
        bg_img = generate_gradient_background(
            VIDEO_W, VIDEO_H, colors, seed=scene_idx * 42 + 7
        )
        bg_path = OUTPUT_DIR / f"_temp_bg_{scene_idx:03d}.png"
        bg_img.save(str(bg_path))
        bg_clip = ImageClip(str(bg_path)).with_duration(duration)

    # 2. 创建字幕
    subtitle = create_subtitle_clip(scene_text, duration, colors, font_path)

    # 3. 场景序号标记（右上角，小字）
    marker_text = f"龍魂 · {scene_idx + 1}/{total_scenes}"
    marker = simple_text_clip(
        marker_text, duration, fontsize=24, color=(255, 255, 255),
        font_path=font_path, stroke_color=(0, 0, 0), stroke_width=1,
    ).with_position((VIDEO_W - 220, 30))

    # 4. 龍魂签章（右下角 · 128px 方章）
    seal_clip = None
    if _SEAL_AVAILABLE:
        try:
            seal_img = ImageClip(str(SEAL_CORNER)).with_duration(duration)
            seal_w, seal_h = 96, 96  # 右下角签章大小
            seal_img = seal_img.resized((seal_w, seal_h))
            # 半透明叠加（alpha 0.75 = 签章可见但不喧宾夺主）
            seal_arr = np.array(Image.open(str(SEAL_CORNER)).resize((seal_w, seal_h)).convert("RGBA"))
            seal_arr[:, :, 3] = (seal_arr[:, :, 3] * 0.75).astype(np.uint8)
            seal_pil = Image.fromarray(seal_arr)
            seal_buf = io.BytesIO()
            seal_pil.save(seal_buf, format="PNG")
            seal_buf.seek(0)
            seal_img = ImageClip(np.array(Image.open(seal_buf))).with_duration(duration)
            seal_clip = seal_img.with_position((VIDEO_W - seal_w - 40, VIDEO_H - seal_h - 30))
        except Exception:
            seal_clip = None

    # 5. 龍魂徽章（左上角 · 80px badge-A）
    badge_clip = None
    if _BADGE_AVAILABLE:
        try:
            badge_img = ImageClip(str(BADGE_A)).with_duration(duration)
            badge_w, badge_h = 64, 64
            badge_img = badge_img.resized((badge_w, badge_h))
            # 半透明
            badge_arr = np.array(Image.open(str(BADGE_A)).resize((badge_w, badge_h)).convert("RGBA"))
            badge_arr[:, :, 3] = (badge_arr[:, :, 3] * 0.65).astype(np.uint8)
            badge_pil = Image.fromarray(badge_arr)
            badge_buf = io.BytesIO()
            badge_pil.save(badge_buf, format="PNG")
            badge_buf.seek(0)
            badge_img = ImageClip(np.array(Image.open(badge_buf))).with_duration(duration)
            badge_clip = badge_img.with_position((30, 25))
        except Exception:
            badge_clip = None

    # 6. DNA追溯水印（左下角，极小字）
    dna_text = "#龍芯⚡️UID9622 · 龍魂视频工坊v4.0"
    watermark = simple_text_clip(
        dna_text, duration, fontsize=16, color=(180, 180, 180),
        font_path=font_path,
    ).with_position((50, VIDEO_H - 35))

    # 7. 组合所有图层
    layers = [bg_clip, subtitle, marker, watermark]
    if seal_clip is not None:
        layers.append(seal_clip)
    if badge_clip is not None:
        layers.append(badge_clip)

    composite = CompositeVideoClip(layers, size=(VIDEO_W, VIDEO_H))

    # 7. 添加音频（按音频实际时长clamp duration）
    audio = AudioFileClip(audio_path)
    actual_dur = min(duration, audio.duration)
    if duration != actual_dur:
        composite = composite.with_duration(actual_dur)
    audio = audio.with_duration(actual_dur)
    composite = composite.with_audio(audio)

    # 8. 淡入淡出（首尾场景特殊处理）
    if duration > 1.5:
        fade_dur = min(0.8, duration * 0.15)
        composite = composite.with_effects([FadeIn(fade_dur), FadeOut(fade_dur)])

    return composite


# =============================================================================
# 3. 主流程
# =============================================================================

def generate_dna(output_name: str = "", style: str = "") -> str:
    """生成龍魂标准DNA追溯码（干支四柱+卦象·v∞标准）"""
    try:
        from lh_dna_generator import generate_dna as gen
        tag = f"VIDEO-{output_name[:8]}" if output_name else "VIDEO-STUDIO"
        return gen(action_tag=tag, version="2.0")
    except ImportError:
        # 降级：时间戳DNA
        from datetime import timezone
        now = datetime.now(timezone.utc)
        return f"#龍芯⚡️{now.strftime('%Y%m%d')}-{now.strftime('%H%M%S')}-VIDEO-v4.0"


def create_video(
    scenes: List[str],
    style: str = "龍魂",
    output_name: str = "龍魂解说",
    voice: str = "zh-CN-YunxiNeural",
    font_path: Optional[str] = None,
    image_dir: Optional[str] = None,
) -> str:
    """
    核心视频生成流程
    返回输出视频的文件路径
    """
    # 加载外部图片（如果提供）
    section_images = None
    if image_dir:
        img_dir_path = Path(image_dir)
        if img_dir_path.is_dir():
            section_images = sorted([
                p for p in img_dir_path.iterdir()
                if p.suffix.lower() in ('.png', '.jpg', '.jpeg', '.webp')
            ])
            if section_images:
                log(f"加载自定义图解: {len(section_images)} 张", "OK")
            else:
                log(f"图片目录为空，将使用默认渐变背景", "WARN")
        else:
            log(f"图片目录不存在: {image_dir}，将使用默认渐变背景", "WARN")

    total = len(scenes)
    log(f"开始生成视频 | 风格: {style} | 场景数: {total} | 语音: {voice}", "STEP")

    colors = COLOR_SCHEME.get(style, COLOR_SCHEME["默认"])
    temp_dir = OUTPUT_DIR / "_temp"
    temp_dir.mkdir(exist_ok=True)

    # Step 1: 批量生成音频
    log("Step 1/3: 批量生成配音...", "INFO")
    audio_results = asyncio.run(generate_audio_batch(scenes, temp_dir, voice))

    if not audio_results:
        log("没有成功生成任何音频，退出", "ERROR")
        return ""

    valid_scenes = []
    valid_audios = []
    valid_durations = []

    for i, (path, dur) in enumerate(audio_results):
        valid_scenes.append(scenes[i])
        valid_audios.append(path)
        valid_durations.append(dur)

    log(f"配音完成: {len(valid_audios)}/{total} 个场景", "OK")

    # Step 2: 逐个生成场景视频片段
    log("Step 2/3: 渲染视频场景...", "INFO")
    clips = []
    for idx, (text, audio_path, duration) in enumerate(zip(valid_scenes, valid_audios, valid_durations)):
        log(f"  渲染场景 {idx + 1}/{len(valid_scenes)} ({duration:.1f}s)...", "INFO")
        try:
            clip = create_scene_clip(
                text, audio_path, duration, colors,
                font_path=font_path,
                scene_idx=idx,
                total_scenes=len(valid_scenes),
                section_images=section_images,
            )
            clips.append(clip)
        except Exception as e:
            log(f"场景 {idx + 1} 渲染失败: {e}", "ERROR")
            continue

    if not clips:
        log("没有成功渲染任何场景，退出", "ERROR")
        return ""

    # Step 3: 拼接并输出
    log("Step 3/3: 拼接输出最终视频...", "INFO")
    final = concatenate_videoclips(clips, method="compose")

    # 输出文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"{output_name}_{style}_{timestamp}.mp4"
    output_path = OUTPUT_DIR / output_filename

    # 写入视频（优化参数）
    final.write_videofile(
        str(output_path),
        fps=FPS,
        codec=CODEC,
        audio_codec=AUDIO_CODEC,
        preset=PRESET,
        ffmpeg_params=["-crf", CRF, "-pix_fmt", "yuv420p", "-movflags", "+faststart"],
        threads=4,
        logger=None,  # 禁用moviepy的默认logger，我们用自定义的
    )

    # 清理临时文件
    log("清理临时文件...", "INFO")
    for pattern in ["_temp_bg_*.png", "_temp_visual_*.png"]:
        for f in OUTPUT_DIR.glob(pattern):
            try:
                f.unlink()
            except:
                pass
    for f in temp_dir.glob("temp_audio_*.mp3"):
        try:
            f.unlink()
        except:
            pass

    # 生成DNA
    dna = generate_dna(output_name, style)

    log(f"视频生成成功!", "OK")
    log(f"📁 输出路径: {output_path}", "OK")
    log(f"🧬 DNA追溯: {dna}", "DNA")
    log(f"📊 视频信息: {len(clips)}个场景 | 总时长: {final.duration:.1f}s | 分辨率: {VIDEO_W}x{VIDEO_H}", "INFO")

    # 生成配套信息文件
    info = {
        "dna": dna,
        "output_file": str(output_path),
        "style": style,
        "voice": voice,
        "voice_engine": "xtts-v2-uid9622" if voice.lower() in ("uid9622", "真声", "longhun") else "edge-tts",
        "seal_overlay": str(SEAL_CORNER) if _SEAL_AVAILABLE else None,
        "badge_overlay": str(BADGE_A) if _BADGE_AVAILABLE else None,
        "total_scenes": len(clips),
        "total_duration": final.duration,
        "resolution": f"{VIDEO_W}x{VIDEO_H}",
        "scenes": valid_scenes,
        "generated_at": datetime.now().isoformat(),
        "generator": "龍魂视频工坊 v4.0 · UID9622真声+签章",
        "uid": "龍芯北辰 UID9622",
    }
    info_path = output_path.with_suffix('.json')
    with open(info_path, 'w', encoding='utf-8') as f:
        json.dump(info, f, ensure_ascii=False, indent=2)

    return str(output_path)


# =============================================================================
# 4. CLI 入口
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="龍魂视频工坊 v4.0 —— UID9622真声+签章视频生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 lh_video_studio.py --script speech.txt --style 龍魂 --voice uid9622 --name "AI科普"
  python3 lh_video_studio.py --script speech.txt --style 科技 --voice zh-CN-YunxiaNeural
  # uid9622 = UID9622 XTTS v2 真声克隆（干净有力·退伍军人风格）
  # 其他voice = edge-tts云端语音兜底

风格说明:
  龍魂  - 黑底金边军事风（默认·自带签章品牌叠加）
  科技  - 深蓝冷色调
  历史  - 古铜暖色调
  战争  - 暗红热血风
  自然  - 翠绿生机风
  默认  - 中性灰调

签章说明:
  每个视频帧自动叠加: 右下角「龍魂」方章 + 左上角「龍魂」徽章
  签章由 lh_voice_clone.py 和 GPG 分离签名共同保护
  品牌资产: brand/seals/seal_龙魂_square_128.png · brand/badge-A.png
        """
    )
    parser.add_argument('--script', required=True, 
                        help='解说稿文件路径，或直接粘贴文本内容')
    parser.add_argument('--style', default="龍魂",
                        choices=['龍魂', '历史', '科技', '战争', '自然', '默认'],
                        help='视觉风格（默认: 龍魂）')
    parser.add_argument('--voice', default="zh-CN-YunxiNeural",
                        help='TTS语音角色 (默认: zh-CN-YunxiNeural)')
    parser.add_argument('--name', default="龍魂解说",
                        help='输出文件名前缀')
    parser.add_argument('--font', default=None,
                        help='自定义字体文件路径（可选，自动检测）')
    parser.add_argument('--max-chars', type=int, default=160,
                        help='每场景最大字符数（默认160）')
    parser.add_argument('--image-dir', default=None,
                        help='外部图解目录（png/jpg，循环映射到场景）')

    args = parser.parse_args()

    # 读取脚本
    if os.path.exists(args.script):
        with open(args.script, 'r', encoding='utf-8') as f:
            raw = f.read()
    else:
        raw = args.script

    # 自动检测：如果是 markdown 脚本（含【旁白】标记），提取纯净旁白
    if '【旁白】' in raw:
        text = parse_video_script_md(raw)
        log(f"脚本解析: markdown→纯旁白 {len(raw)}→{len(text)} 字符（已去掉标题/表格/格式符）", "OK")
    else:
        text = raw.strip()

    if len(text) < 10:
        log("解说稿太短（至少10个字），退出", "ERROR")
        return

    # 自动检测字体
    font_path = args.font if args.font else find_font()
    if font_path:
        log(f"使用字体: {font_path}", "INFO")

    # 切分场景
    scenes = split_text_into_scenes(text, max_chars=args.max_chars)
    log(f"文本切分完成: {len(scenes)} 个场景", "OK")
    for i, s in enumerate(scenes):
        preview = s[:40] + "..." if len(s) > 40 else s
        log(f"  [{i+1}] {preview}", "INFO")

    # 生成视频
    output = create_video(
        scenes=scenes,
        style=args.style,
        output_name=args.name,
        voice=args.voice,
        font_path=font_path,
        image_dir=args.image_dir,
    )

    if output and os.path.exists(output):
        log("全部完成！可直接发布到抖音/视频号/CSDN", "OK")
        # macOS 自动打开文件夹
        if os.uname().sysname == "Darwin":
            os.system(f'open "{OUTPUT_DIR}"')


if __name__ == "__main__":
    main()
