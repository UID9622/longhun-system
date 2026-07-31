# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·甲子·大壮-VIDEO-COMMENTARY-ENGINE-v1.0
# CREATOR: 诸葛鑫（UID9622）
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
================================================================================
龍魂 · 视频解说稿自动生成引擎 v1.0
================================================================================
功能：统合入口 —— 输入主题/文本/文章，输出带配音解说稿的短视频（或脚本）
       - 自动生成「分镜解说稿」（时间轴 + 画面 + 口播文字）
       - 可选调用 lh_tts_engine.py 合成配音音频
       - 可选调用 ffmpeg 生成简单视频（图片+字幕拼接）
       - 可选调用 lh_video_studio.py 生成完整龍魂风格视频
风格：龍魂 DNA 签章 + 通心译双语 + 三句话总结 + 人格路由
协议：CC BY-NC-SA 4.0 · 数据主权归 UID9622
DNA: #龍芯⚡️丙午·乙未·甲子·大壮-VIDEO-COMMENTARY-ENGINE-v1.0
================================================================================
"""

import os
import re
import sys
import json
import shutil
import argparse
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple

from PIL import Image, ImageDraw, ImageFont

# 确保能从 bin/ 导入龍魂模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from lh_dna_generator import generate_dna
except Exception:  # pragma: no cover - graceful fallback
    def generate_dna(action_tag: str, version: str = "1.0") -> str:
        now = datetime.now()
        return f"#龍芯⚡️{now.strftime('%Y%m%d')}-{action_tag}-v{version}"


# =============================================================================
# 0. 常量与配置
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BIN_DIR = PROJECT_ROOT / "bin"
OUTPUT_DIR = PROJECT_ROOT / "output"
VOICES_DIR = PROJECT_ROOT / "voices"

# 人格路由：视角 + 口播风格
PERSONA_ROUTER = {
    "文心": {
        "id": "P00",
        "title": "文心·永恒锚点",
        "style": "庄重、凝练、以人民为锚",
        "tone": "坚定",
        "voice": "default",
        "intro": "以文心视角，把复杂事理锚回老百姓能懂的根上。",
    },
    "宝宝": {
        "id": "宝宝",
        "title": "龍魂宝宝·民生守护",
        "style": "温暖、直白、带烟火气",
        "tone": "希望",
        "voice": "乔前辈",
        "intro": "以宝宝视角，让老百姓一听就明白这事跟自己有什么关系。",
    },
    "鲁班": {
        "id": "P04",
        "title": "鲁班·技术执行",
        "style": "硬核、步骤清晰、可落地",
        "tone": "坚定",
        "voice": "P77",
        "intro": "以鲁班视角，把技术加固拆成能执行、能验证的动作。",
    },
}

# 分镜默认参数
DEFAULT_SCENE_DURATION = 5.0  # 秒/镜
VIDEO_WIDTH, VIDEO_HEIGHT = 1920, 1080
VIDEO_FPS = 24


# =============================================================================
# 1. 工具函数
# =============================================================================

def log(msg: str, level: str = "INFO"):
    """统一日志输出，带时间戳"""
    ts = datetime.now().strftime("%H:%M:%S")
    icons = {"INFO": "ℹ️", "OK": "✅", "WARN": "⚠️", "ERROR": "❌", "STEP": "🔥", "DNA": "🧬"}
    icon = icons.get(level, "•")
    print(f"[{ts}] {icon} {msg}")


def cmd_exists(name: str) -> bool:
    """检查系统命令是否存在"""
    return shutil.which(name) is not None


def run_cmd(cmd: List[str], cwd: Optional[Path] = None, timeout: int = 180) -> Tuple[bool, str]:
    """安全执行子进程命令，返回 (success, stdout_or_stderr)"""
    try:
        result = subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else None,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if result.returncode == 0:
            return True, result.stdout
        return False, result.stderr or result.stdout
    except subprocess.TimeoutExpired:
        return False, f"命令超时 (> {timeout}s): {' '.join(cmd)}"
    except Exception as e:
        return False, str(e)


def slugify(text: str, max_len: int = 40) -> str:
    """把主题转成文件名安全字符串"""
    text = text.strip().replace(" ", "_")
    text = re.sub(r"[^\w\u4e00-\u9fa5\-]", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text[:max_len] or "commentary"


def estimate_duration(text: str) -> float:
    """按中文字符估算口播时长（约 4.5 字/秒）"""
    return max(2.0, len(text) / 4.5)


def three_sentence_summary(topic: str, persona: str) -> List[str]:
    """生成三句话总结（基于主题和人格）"""
    templates = {
        "文心": [
            f"「{topic}」的本质，是把老百姓的数据主权焊死在本地。",
            f"它不是锦上添花，而是离火运下必须守住的底线。",
            f"文心一锤定音：技术可以迭代，主权一寸不让。",
        ],
        "宝宝": [
            f"{topic}，说白了就是让咱老百姓的信息不被外人拿走。",
            f"不用懂代码，只要记住：数据根留中国，平台服务降级。",
            f"宝宝一句话：自己的东西，自己锁好。",
        ],
        "鲁班": [
            f"{topic}的核心动作：识别资产、加固边界、验证闭环。",
            f"每一步都要留下可审计的日志和 DNA 追溯码。",
            f"鲁班交付标准：能跑通、能复验、能回滚。",
        ],
    }
    return templates.get(persona, templates["文心"])


def tongxinyi_terms(topic: str) -> List[Dict[str, str]]:
    """生成通心译双语关键词对照"""
    # 根据主题动态匹配，通用兜底
    base_terms = [
        {"zh": "数据主权", "en": "Data Sovereignty", "note": "人民数据归人民"},
        {"zh": "龍魂", "en": "Dragon Soul", "note": "文化主权与自主可控"},
        {"zh": "通心译", "en": "Tongxin Translation", "note": "中文语义优先的双语映射"},
        {"zh": "DNA追溯", "en": "DNA Traceability", "note": "来源可查、去向可追"},
    ]
    if "安全" in topic or "加固" in topic:
        base_terms.extend([
            {"zh": "安全加固", "en": "Security Hardening", "note": "缩小攻击面、提升韧性"},
            {"zh": "熔断", "en": "Circuit Breaker", "note": "异常即断、保护主链路"},
            {"zh": "审计", "en": "Audit Trail", "note": "三色审计、全程留痕"},
        ])
    if "视频" in topic or "解说" in topic:
        base_terms.extend([
            {"zh": "分镜", "en": "Storyboard", "note": "时间轴 + 画面 + 口播"},
            {"zh": "口播", "en": "Voice-over", "note": "配音解说的口语化文本"},
        ])
    return base_terms


# =============================================================================
# 2. 内容生成
# =============================================================================

def build_scenes(topic: str, persona: str, source_text: str = "") -> List[Dict[str, str]]:
    """
    基于主题/来源生成分镜时间轴。
    若提供 source_text，则按段落拆分为口播；否则使用主题模板。
    """
    if source_text.strip():
        # 清理 markdown 格式并分句/分段
        raw = source_text
        raw = re.sub(r"^#+\s*", "", raw, flags=re.MULTILINE)
        raw = re.sub(r"\*\*|__|`", "", raw)
        paragraphs = [p.strip() for p in raw.split("\n") if p.strip()]
        # 过滤过短的行，合并相邻短段
        merged = []
        buffer = ""
        for p in paragraphs:
            if len(buffer) + len(p) < 120:
                buffer += (" " if buffer else "") + p
            else:
                if buffer:
                    merged.append(buffer)
                buffer = p
        if buffer:
            merged.append(buffer)
        scenes = []
        for i, text in enumerate(merged[:8]):  # 最多 8 镜
            scenes.append({
                "idx": i + 1,
                "time": f"{int(i * DEFAULT_SCENE_DURATION):02d}:00",
                "visual": f"画面{i+1}：{topic} · 关键信息可视化",
                "narration": text,
                "duration": round(estimate_duration(text), 1),
            })
        return scenes

    # 无来源时，使用主题模板
    persona_id = PERSONA_ROUTER.get(persona, PERSONA_ROUTER["文心"])
    intro = persona_id["intro"]
    templates = {
        "文心": [
            ("开场：龍魂立题", f"今天讲「{topic}」。文心先立锚：任何技术，都要先问一句——它是在帮人，还是在收割人？"),
            ("本质：主权归位", f"「{topic}」的本质，是把数据主权从平台手里拿回来，焊死在老百姓自己手里。"),
            ("方法：三道防线", "第一道，身份主权：谁访问、凭什么，必须可追溯。第二道，数据主权：根留本地，出境熔断。第三道，行为主权：每一次操作都要留下审计痕。"),
            ("通心译：一句话", "用大白话说：自己的数据自己锁，自己的系统自己管。"),
            ("收尾：文心定调", "技术可以更新，主权不能让步。这就是龍魂的底线。"),
        ],
        "宝宝": [
            ("开场：宝宝打招呼", f"大家好，我是龍魂宝宝。今天用大白话讲「{topic}」。"),
            ("痛点：老百姓的事", "很多人不懂技术，但都知道：自己的信息被平台拿走，心里不踏实。"),
            ("办法：三步锁好", f"「{topic}」就是给咱家的大门加三道锁：门钥匙自己拿、进出有记录、外人来了自动报警。"),
            ("好处：睡得踏实", "不用懂代码，只要记住：数据根留中国，坏人就拿不走。"),
            ("收尾：宝宝叮嘱", "自己的东西自己看好，这就是老百姓的数字主权。"),
        ],
        "鲁班": [
            ("开场：鲁班报题", f"本次执行「{topic}」。目标：识别风险、加固边界、输出可验证的审计产物。"),
            ("资产清点", "第一步，清点数字资产：数据在哪里、谁能访问、出过哪些日志。"),
            ("加固动作", "第二步，执行加固：最小权限、加密存储、接口熔断、密钥隔离。"),
            ("验证闭环", "第三步，验证闭环：跑通渗透测试、回归审计、DNA 签章留痕。"),
            ("收尾：鲁班交付", "所有动作写入执行记录，失败可回滚，成功可复制。任务完成。"),
        ],
    }
    rows = templates.get(persona, templates["文心"])
    scenes = []
    elapsed = 0.0
    for i, (visual, narration) in enumerate(rows):
        dur = round(estimate_duration(narration), 1)
        scenes.append({
            "idx": i + 1,
            "time": f"{int(elapsed // 60):02d}:{int(elapsed % 60):02d}",
            "visual": f"画面{i+1}：{visual}",
            "narration": narration,
            "duration": dur,
        })
        elapsed += dur + 0.5
    return scenes


def generate_commentary_markdown(
    topic: str,
    persona: str,
    scenes: List[Dict[str, str]],
    dna: str,
) -> str:
    """生成龍魂风格的分镜解说稿 Markdown"""
    p = PERSONA_ROUTER.get(persona, PERSONA_ROUTER["文心"])
    summary = three_sentence_summary(topic, persona)
    terms = tongxinyi_terms(topic)
    total_duration = round(sum(s["duration"] for s in scenes) + (len(scenes) - 1) * 0.5, 1)

    lines = []
    lines.append("# 龍魂 · 视频分镜解说稿")
    lines.append("")
    lines.append(f"**主题**：{topic}")
    lines.append(f"**人格路由**：{p['title']} ({p['id']})")
    lines.append(f"**预计时长**：{total_duration} 秒")
    lines.append(f"**生成时间**：{datetime.now().isoformat()}")
    lines.append(f"**DNA追溯**：`{dna}`")
    lines.append(f"**协议**：CC BY-NC-SA 4.0 · 数据主权归 UID9622")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 🧬 龍魂 DNA 签章")
    lines.append("")
    lines.append(f"> {dna}")
    lines.append("> 来源可查 · 去向可追 · 责任可究")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 🌐 通心译双语关键词")
    lines.append("")
    lines.append("| 中文 | English | 注解 |")
    lines.append("|------|---------|------|")
    for t in terms:
        lines.append(f"| {t['zh']} | {t['en']} | {t['note']} |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 📝 三句话总结")
    lines.append("")
    for s in summary:
        lines.append(f"1. {s}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 🎬 分镜时间轴")
    lines.append("")
    lines.append(f"> 口播风格：{p['style']}")
    lines.append("")
    lines.append("| 镜号 | 时间 | 画面 | 口播文字 | 时长(秒) |")
    lines.append("|------|------|------|----------|----------|")
    for s in scenes:
        narration_cell = s['narration'].replace('|', '｜').replace('\n', '<br>')
        visual_cell = s['visual'].replace('|', '｜')
        lines.append(
            f"| {s['idx']} | {s['time']} | {visual_cell} | {narration_cell} | {s['duration']} |"
        )
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 🎙️ 纯净口播稿")
    lines.append("")
    lines.append("【旁白】")
    lines.append("")
    for s in scenes:
        lines.append(s["narration"])
        lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 🛠️ 制作参数")
    lines.append("")
    lines.append(f"- 默认分镜时长：{DEFAULT_SCENE_DURATION} 秒")
    lines.append(f"- 口播语速估算：约 4.5 字/秒")
    lines.append(f"- 推荐分辨率：{VIDEO_WIDTH}x{VIDEO_HEIGHT}")
    lines.append(f"- 推荐帧率：{VIDEO_FPS}")
    lines.append(f"- 人格音色建议：{p['voice']}")
    lines.append("")
    lines.append("## ✅ 生成后检查")
    lines.append("")
    lines.append("- [ ] 口播无错别字")
    lines.append("- [ ] 时间轴连续无重叠")
    lines.append("- [ ] DNA 签章已嵌入")
    lines.append("- [ ] 音频/视频生成成功")
    lines.append("")
    return "\n".join(lines)


# =============================================================================
# 3. 媒体生成（可选，优雅降级）
# =============================================================================

class VideoCommentaryEngine:
    """视频解说稿自动生成引擎"""

    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = Path(output_dir) if output_dir else OUTPUT_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.tts_available = (BIN_DIR / "lh_tts_engine.py").exists() and cmd_exists("ffmpeg")
        self.studio_available = (BIN_DIR / "lh_video_studio.py").exists()
        self.ffmpeg_available = cmd_exists("ffmpeg")
        self._warned_missing = set()

    def _warn_once(self, key: str, msg: str):
        if key not in self._warned_missing:
            log(msg, "WARN")
            self._warned_missing.add(key)

    def generate_script(
        self,
        topic: str,
        persona: str = "文心",
        source_text: str = "",
    ) -> Tuple[Path, str, str]:
        """生成分镜解说稿，返回 (文件路径, 内容, DNA)"""
        dna = generate_dna(action_tag="VIDEO-COMMENTARY", version="1.0")
        scenes = build_scenes(topic, persona, source_text)
        md = generate_commentary_markdown(topic, persona, scenes, dna)
        stem = slugify(topic)
        script_path = self.output_dir / f"commentary_{stem}.md"
        script_path.write_text(md, encoding="utf-8")
        log(f"解说稿已生成: {script_path}", "OK")
        log(f"分镜数: {len(scenes)} | 预计时长: {sum(s['duration'] for s in scenes) + (len(scenes)-1)*0.5:.1f}s", "INFO")
        log(f"DNA追溯: {dna}", "DNA")
        return script_path, md, dna

    def extract_narration(self, md_text: str) -> str:
        """从 markdown 解说稿中提取【旁白】区块"""
        in_narration = False
        parts = []
        for line in md_text.splitlines():
            stripped = line.strip()
            if stripped == "【旁白】":
                in_narration = True
                continue
            if in_narration:
                if stripped.startswith("---"):
                    break
                parts.append(line)
        return "\n".join(parts).strip()

    def synthesize_audio(self, narration: str, output_path: Path, persona: str = "文心") -> bool:
        """调用 lh_tts_engine.py 合成音频"""
        if not self.tts_available:
            self._warn_once("tts", "TTS 不可用（缺少 ffmpeg 或 lh_tts_engine.py），跳过配音生成")
            return False

        voice = PERSONA_ROUTER.get(persona, PERSONA_ROUTER["文心"])["voice"]
        # 先把口播写入临时文本文件，避免命令行特殊字符问题
        tmp_txt = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8")
        tmp_txt.write(narration)
        tmp_txt.close()

        cmd = [
            "python3", str(BIN_DIR / "lh_tts_engine.py"),
            "--text", tmp_txt.name,
            "--voice", voice,
            "--output", str(output_path),
            "--format", "mp3",
        ]
        ok, msg = run_cmd(cmd, cwd=PROJECT_ROOT, timeout=120)
        Path(tmp_txt.name).unlink(missing_ok=True)
        if ok and output_path.exists():
            log(f"配音已生成: {output_path} ({output_path.stat().st_size} bytes)", "OK")
            return True
        log(f"配音生成失败: {msg}", "ERROR")
        return False

    def generate_simple_video_ffmpeg(
        self,
        script_path: Path,
        audio_path: Optional[Path],
        output_path: Path,
        scenes: List[Dict[str, str]],
        image_dir: Optional[Path] = None,
    ) -> bool:
        """用 ffmpeg 生成简单视频：渐变背景 + 字幕序列；可选使用外部图片"""
        if not self.ffmpeg_available:
            self._warn_once("ffmpeg", "ffmpeg 不可用，跳过视频生成")
            return False

        # 加载外部图片（如果提供）
        section_images: List[Path] = []
        if image_dir and image_dir.is_dir():
            section_images = sorted([
                p for p in image_dir.iterdir()
                if p.suffix.lower() in ('.png', '.jpg', '.jpeg', '.webp')
            ])
            if section_images:
                log(f"加载自定义图片: {len(section_images)} 张", "OK")

        tmp_dir = Path(tempfile.mkdtemp(prefix="lh_commentary_video_"))
        try:
            frame_paths: List[Path] = []
            for i, s in enumerate(scenes):
                frame = tmp_dir / f"frame_{s['idx']:03d}.png"
                if section_images:
                    # 使用外部图片作为背景，再叠加字幕
                    bg_path = section_images[i % len(section_images)]
                    self._render_frame_with_image(frame, s, bg_path)
                else:
                    self._render_frame(frame, s)
                frame_paths.append(frame)

            if not frame_paths:
                log("没有可渲染的帧", "ERROR")
                return False

            # 写 concat 列表，使用 duration 指定每镜停留时长
            concat_path = tmp_dir / "frames.txt"
            with open(concat_path, "w", encoding="utf-8") as cf:
                for i, fp in enumerate(frame_paths):
                    cf.write(f"file '{fp.name}'\n")
                    cf.write(f"duration {scenes[i]['duration']}\n")
                # concat demuxer 要求最后一行再写一次文件才能正确应用最后一段时长
                if frame_paths:
                    cf.write(f"file '{frame_paths[-1].name}'\n")

            cmd = [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-f", "concat", "-safe", "0",
                "-i", str(concat_path),
            ]
            if audio_path and audio_path.exists():
                cmd.extend(["-i", str(audio_path)])
            cmd.extend([
                "-vf", f"fps={VIDEO_FPS},format=yuv420p",
                "-c:v", "libx264", "-preset", "medium", "-crf", "23",
            ])
            if audio_path and audio_path.exists():
                cmd.extend(["-c:a", "aac", "-b:a", "128k", "-shortest"])
            cmd.append(str(output_path))

            ok, msg = run_cmd(cmd, cwd=tmp_dir, timeout=300)
            if ok and output_path.exists():
                log(f"简单视频已生成: {output_path}", "OK")
                return True
            log(f"视频生成失败: {msg}", "ERROR")
            return False
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)

    def _find_font(self, size: int) -> ImageFont.FreeTypeFont:
        """跨平台寻找可用的中文字体"""
        candidates = [
            Path("/System/Library/Fonts/PingFang.ttc"),
            Path("/System/Library/Fonts/STHeiti Light.ttc"),
            Path("/Library/Fonts/Arial Unicode.ttf"),
            Path("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"),
            Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
            Path("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"),
        ]
        for c in candidates:
            if c.exists():
                try:
                    return ImageFont.truetype(str(c), size)
                except Exception:
                    continue
        return ImageFont.load_default()

    def _render_frame_with_image(self, output_path: Path, scene: Dict[str, str], bg_path: Path):
        """用外部图片作为背景，叠加字幕和 DNA 水印"""
        try:
            img = Image.open(str(bg_path)).convert("RGB")
            img = img.resize((VIDEO_WIDTH, VIDEO_HEIGHT), Image.Resampling.LANCZOS)
            draw = ImageDraw.Draw(img)

            title_font = self._find_font(48)
            text_font = self._find_font(56)
            watermark_font = self._find_font(24)

            # 顶部画面说明（带半透明黑底衬）
            visual_text = scene["visual"]
            bbox = draw.textbbox((0, 0), visual_text, font=title_font)
            title_w, title_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
            overlay = Image.new("RGBA", (VIDEO_WIDTH, VIDEO_HEIGHT), (0, 0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay)
            overlay_draw.rectangle(
                [0, 80, VIDEO_WIDTH, 80 + title_h + 40],
                fill=(0, 0, 0, 160)
            )
            img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
            draw = ImageDraw.Draw(img)
            draw.text(((VIDEO_WIDTH - title_w) // 2, 100),
                      visual_text, font=title_font, fill="#C9A84C")

            # 中部口播文字（带半透明黑底衬）
            wrapped = self._wrap_text(scene["narration"], 24)
            line_h = 70
            text_h = len(wrapped) * line_h
            start_y = (VIDEO_HEIGHT - text_h) // 2
            overlay = Image.new("RGBA", (VIDEO_WIDTH, VIDEO_HEIGHT), (0, 0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay)
            overlay_draw.rectangle(
                [int(VIDEO_WIDTH * 0.1), start_y - 20, int(VIDEO_WIDTH * 0.9), start_y + text_h + 20],
                fill=(0, 0, 0, 160)
            )
            img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
            draw = ImageDraw.Draw(img)
            for i, line in enumerate(wrapped[:8]):
                bbox = draw.textbbox((0, 0), line, font=text_font)
                draw.text(((VIDEO_WIDTH - (bbox[2] - bbox[0])) // 2, start_y + i * line_h),
                          line, font=text_font, fill="#FFF5F0")

            # 右下角 DNA 水印
            watermark = "龍魂 · UID9622 · 数据主权归本地"
            bbox = draw.textbbox((0, 0), watermark, font=watermark_font)
            draw.text((VIDEO_WIDTH - (bbox[2] - bbox[0]) - 50, VIDEO_HEIGHT - 60),
                      watermark, font=watermark_font, fill="#C9A84C")

            img.save(str(output_path), "PNG")
        except Exception as e:
            log(f"图片背景渲染失败: {e}，回退到纯色背景", "WARN")
            self._render_frame(output_path, scene)

    def _render_frame(self, output_path: Path, scene: Dict[str, str]):
        """用 PIL 生成龍魂风格单帧（黑底金边 + 字幕）"""
        try:
            img = Image.new("RGB", (VIDEO_WIDTH, VIDEO_HEIGHT), "#080808")
            draw = ImageDraw.Draw(img)

            # 字体
            title_font = self._find_font(48)
            text_font = self._find_font(56)
            watermark_font = self._find_font(24)

            # 顶部金色装饰线
            draw.line([(80, 60), (VIDEO_WIDTH - 80, 60)], fill="#C9A84C", width=2)
            draw.line([(80, VIDEO_HEIGHT - 60), (VIDEO_WIDTH - 80, VIDEO_HEIGHT - 60)], fill="#C9A84C", width=2)

            # 顶部画面说明
            visual_text = scene["visual"]
            bbox = draw.textbbox((0, 0), visual_text, font=title_font)
            draw.text(((VIDEO_WIDTH - (bbox[2] - bbox[0])) // 2, 100),
                      visual_text, font=title_font, fill="#C9A84C")

            # 中部口播文字（自动折行）
            wrapped = self._wrap_text(scene["narration"], 24)
            line_h = 70
            start_y = (VIDEO_HEIGHT - len(wrapped) * line_h) // 2
            for i, line in enumerate(wrapped[:8]):
                bbox = draw.textbbox((0, 0), line, font=text_font)
                draw.text(((VIDEO_WIDTH - (bbox[2] - bbox[0])) // 2, start_y + i * line_h),
                          line, font=text_font, fill="#FFF5F0")

            # 右下角 DNA 水印
            watermark = "龍魂 · UID9622 · 数据主权归本地"
            bbox = draw.textbbox((0, 0), watermark, font=watermark_font)
            draw.text((VIDEO_WIDTH - (bbox[2] - bbox[0]) - 50, VIDEO_HEIGHT - 60),
                      watermark, font=watermark_font, fill="#6B6B6B")

            img.save(str(output_path), "PNG")
        except Exception as e:
            log(f"PIL 单帧渲染失败: {e}，使用占位图", "WARN")
            # 降级：生成纯黑占位图
            subprocess.run(
                ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                 "-f", "lavfi", "-i", f"color=c=#080808:s={VIDEO_WIDTH}x{VIDEO_HEIGHT}:d=1",
                 "-frames:v", "1", str(output_path)],
                check=False,
            )

    def _wrap_text(self, text: str, width: int) -> List[str]:
        """按字符数折行（中文）"""
        lines = []
        current = ""
        for ch in text:
            if len(current) >= width:
                lines.append(current)
                current = ch
            else:
                current += ch
        if current:
            lines.append(current)
        return lines if lines else [text]

    def generate_studio_video(
        self,
        script_path: Path,
        output_name: str,
        persona: str = "文心",
        image_dir: Optional[Path] = None,
    ) -> Optional[Path]:
        """调用 lh_video_studio.py 生成完整龍魂风格视频"""
        if not self.studio_available:
            self._warn_once("studio", "lh_video_studio.py 不可用，跳过完整视频生成")
            return None

        voice = PERSONA_ROUTER.get(persona, PERSONA_ROUTER["文心"])["voice"]
        # 将人格音色映射为 edge-tts 可用名称；lh_video_studio 的 --voice 接受 edge-tts voice 名
        # 我们的 persona voice 是人格昵称，需要解析
        from lh_tts_engine import resolve_voice
        edge_voice = resolve_voice(voice)

        cmd = [
            "python3", str(BIN_DIR / "lh_video_studio.py"),
            "--script", str(script_path),
            "--style", "龍魂",
            "--voice", edge_voice,
            "--name", output_name,
        ]
        if image_dir and image_dir.is_dir():
            cmd.extend(["--image-dir", str(image_dir)])
        log("调用龍魂视频工坊生成完整视频...", "STEP")
        ok, msg = run_cmd(cmd, cwd=PROJECT_ROOT, timeout=600)
        if ok:
            # studio 输出到 ~/Desktop/龙魂视频，这里尝试找回最近文件
            studio_dir = Path.home() / "Desktop" / "龙魂视频"
            if studio_dir.exists():
                mp4s = sorted(studio_dir.glob(f"{output_name}_*.mp4"), key=lambda p: p.stat().st_mtime, reverse=True)
                if mp4s:
                    log(f"完整视频已生成: {mp4s[0]}", "OK")
                    return mp4s[0]
            log("视频工坊执行成功，但未找到输出文件", "WARN")
            return None
        log(f"视频工坊调用失败: {msg}", "ERROR")
        return None

    def run(self, args: argparse.Namespace) -> int:
        """主入口"""
        # 1. 解析输入
        topic = args.topic or ""
        source_text = ""
        if args.source:
            p = Path(args.source)
            if not p.exists():
                log(f"来源文件不存在: {args.source}", "ERROR")
                return 1
            source_text = p.read_text(encoding="utf-8")
            if not topic:
                # 从文件第一行非空内容提取主题
                first = next((l.strip().lstrip("# ") for l in source_text.splitlines() if l.strip()), "")
                topic = first[:60] or Path(args.source).stem
        if args.script:
            p = Path(args.script)
            if p.exists():
                source_text = p.read_text(encoding="utf-8")
                if not topic:
                    topic = Path(args.script).stem
            else:
                source_text = args.script
                if not topic:
                    topic = args.script[:60]
        if not topic:
            log("必须提供 --topic / --script / --source 之一", "ERROR")
            return 1

        persona = args.persona or "文心"
        if persona not in PERSONA_ROUTER:
            log(f"未知人格 '{persona}'，使用默认 '文心'", "WARN")
            persona = "文心"

        log(f"开始生成解说稿 | 主题: {topic} | 人格: {persona}", "STEP")

        # 2. 生成解说稿
        script_path, md_text, dna = self.generate_script(topic, persona, source_text)

        # 3. dry-run：到此为止
        if args.dry_run:
            log("--dry-run 模式：只输出解说稿，不生成媒体", "WARN")
            print("\n" + "=" * 60)
            print(md_text[:1200] + ("\n..." if len(md_text) > 1200 else ""))
            print("=" * 60)
            return 0

        # 4. 生成配音
        audio_path: Optional[Path] = None
        narration = self.extract_narration(md_text)
        if args.audio or args.video:
            if narration:
                audio_path = self.output_dir / f"commentary_{slugify(topic)}.mp3"
                if self.synthesize_audio(narration, audio_path, persona):
                    pass
                else:
                    audio_path = None
            else:
                log("未从解说稿提取到口播文字，跳过配音", "WARN")

        # 5. 生成视频
        if args.video:
            output_name = slugify(topic)
            image_dir = Path(args.image_dir) if getattr(args, "image_dir", None) else None
            if args.use_studio and self.studio_available:
                self.generate_studio_video(script_path, output_name, persona, image_dir)
            else:
                scenes = self._parse_scenes_from_md(md_text)
                video_path = self.output_dir / f"commentary_{output_name}.mp4"
                self.generate_simple_video_ffmpeg(script_path, audio_path, video_path, scenes, image_dir)

        log("全部完成", "OK")
        return 0

    def _parse_scenes_from_md(self, md_text: str) -> List[Dict[str, str]]:
        """从已生成的 markdown 中解析分镜表格"""
        scenes = []
        in_table = False
        for line in md_text.splitlines():
            if line.startswith("| 镜号 "):
                in_table = True
                continue
            if in_table and line.startswith("|"):
                cells = [c.strip() for c in line.split("|")[1:-1]]
                if len(cells) >= 5 and cells[0].isdigit():
                    scenes.append({
                        "idx": int(cells[0]),
                        "time": cells[1],
                        "visual": cells[2],
                        "narration": cells[3].replace("<br>", "\n"),
                        "duration": float(cells[4]) if cells[4].replace(".", "", 1).isdigit() else DEFAULT_SCENE_DURATION,
                    })
            elif in_table and not line.startswith("|"):
                break
        return scenes


# =============================================================================
# 4. CLI 入口
# =============================================================================

def main() -> int:
    parser = argparse.ArgumentParser(
        description="龍魂 · 视频解说稿自动生成引擎 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 只生成解说稿（dry-run）
  python3 bin/lh_video_commentary_engine.py --topic "龍魂安全加固v1.1" --dry-run

  # 生成解说稿 + 配音
  python3 bin/lh_video_commentary_engine.py --topic "数据主权" --audio

  # 从文章生成完整视频
  python3 bin/lh_video_commentary_engine.py --source articles/主权.md --video --persona 鲁班

  # 使用已有口播脚本
  python3 bin/lh_video_commentary_engine.py --script output/commentary_demo.md --video
        """,
    )
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--topic", help="输入主题，引擎自动生成解说稿")
    input_group.add_argument("--script", help="输入口播/解说稿文件路径（或直接文本）")
    input_group.add_argument("--source", help="输入文章/协议文件路径（.md/.txt）")

    parser.add_argument("--persona", choices=list(PERSONA_ROUTER.keys()), default="文心",
                        help="人格路由视角（默认: 文心）")
    parser.add_argument("--dry-run", action="store_true",
                        help="只生成解说稿，不生成音频/视频")
    parser.add_argument("--audio", action="store_true",
                        help="同时生成配音音频")
    parser.add_argument("--video", action="store_true",
                        help="同时生成视频")
    parser.add_argument("--use-studio", action="store_true",
                        help="视频生成时使用 lh_video_studio.py 完整流程（需 moviepy）")
    parser.add_argument("--image-dir", default=None,
                        help="视频背景图片目录（png/jpg/jpeg/webp，按顺序映射到分镜）")
    parser.add_argument("--output-dir", default=str(OUTPUT_DIR),
                        help=f"输出目录（默认: {OUTPUT_DIR}）")

    args = parser.parse_args()
    engine = VideoCommentaryEngine(output_dir=args.output_dir)
    return engine.run(args)


if __name__ == "__main__":
    sys.exit(main())
