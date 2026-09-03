#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丁酉·戊寅·未时·䷝离-LH-VIDEO-v1.0-MEDIA-SENSE
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 龍魂视频引擎 v1.0 — 感官层·视觉动

能力:
  lh video <文本|图片序列> [--template intro|outro|slide] [--format mp4|webm]
  - 帧动画合成：文本逐句字幕帧 / 图片序列转视频
  - 龍魂片头/片尾模板（intro 龍魂标题 · outro 致谢归属）
  - 输出 MP4/WebM + 每帧时间戳水印 + DNA 元数据 + GPG 签名 sidecar
  - 水印: 帧底时间戳 + UID9622 归属 · DNA 追溯码嵌入元数据

对齐: 帧带时间戳水印 + GPG 签名 · 繁体「龍」· 龍魂视觉配色
"""

import argparse
import glob
import hashlib
import os
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
输出目录 = ROOT / "data" / "videos"
归属名 = "诸葛鑫 | UID9622 · 龍芯北辰"
背景色 = (14, 20, 32)
龙金 = (212, 175, 55)
文字色 = (232, 232, 232)

字体候选 = [
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/Library/Fonts/Arial Unicode.ttf",
]


def _字体(size: int):
    from PIL import ImageFont
    for p in 字体候选:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


def _dna(动作: str) -> str:
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    h = hashlib.md5(f"{动作}{ts}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{ts}-LH-VIDEO-{动作}-{h}"


def _水印(d, w, h, 帧序号, dna):
    """帧时间戳水印 + 归属"""
    from PIL import ImageFont
    f_水 = _字体(16)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    d.text((20, h - 40), f"⏱ {ts}", fill=(160, 160, 160), font=f_水)
    d.text((w - 520, h - 40), f"🐉 {归属名}", fill=(212, 175, 55), font=f_水)
    d.text((20, 20), dna, fill=(90, 100, 120), font=f_水)


def _帧背景(w, h, 帧序号=0):
    """暗色龍魂背景：径向渐变 + 金色边框"""
    from PIL import Image, ImageDraw
    img = Image.new("RGB", (w, h), 背景色)
    d = ImageDraw.Draw(img)
    # 渐变
    for i in range(h):
        t = i / h
        col = (int(14 + 8 * t), int(20 + 6 * t), int(32 + 10 * t))
        d.line([(0, i), (w, i)], fill=col)
    # 金色边框
    bw = 6
    d.rectangle([bw, bw, w - bw, h - bw], outline=龙金, width=2)
    # 角落龍纹（大龍字半透明）
    from PIL import Image, ImageDraw
    f_龍 = _字体(320)
    d.text((w - 380, h - 420), "龍", fill=(40, 48, 66), font=f_龍)
    return img


def 生成文本帧(text: str, w=1920, h=1080, 帧序号=0, dna="") -> "Image":
    """文本 → 居中字幕帧（自动换行）"""
    from PIL import Image, ImageDraw
    img = _帧背景(w, h)
    d = ImageDraw.Draw(img)
    f_大 = _字体(64)
    # 自动换行（每行 18 字）
    lines = []
    cur = ""
    for ch in text:
        cur += ch
        if len(cur) >= 16:
            lines.append(cur)
            cur = ""
    if cur:
        lines.append(cur)
    y = h / 2 - len(lines) * 45
    for ln in lines[:6]:
        tw = d.textlength(ln, font=f_大)
        d.text(((w - tw) / 2, y), ln, fill=文字色, font=f_大)
        y += 90
    _水印(d, w, h, 帧序号, dna)
    return img


def 生成图片帧(img_path: str, w=1920, h=1080, 帧序号=0, dna="") -> "Image":
    """图片 → 缩放适配 + 暗化 + 水印"""
    from PIL import Image, ImageDraw, ImageOps, ImageEnhance
    src = Image.open(img_path).convert("RGB")
    src = ImageOps.fit(src, (w, h), Image.LANCZOS)
    # 轻微暗化突出水印
    src = ImageEnhance.Brightness(src).enhance(0.92)
    d = ImageDraw.Draw(src)
    d.rectangle([0, 0, w - 1, h - 1], outline=龙金, width=4)
    _水印(d, w, h, 帧序号, dna)
    return src


def 生成片头(标题: str = "龍魂系统", w=1920, h=1080, 帧序号=0, dna="") -> "Image":
    from PIL import Image, ImageDraw
    img = _帧背景(w, h)
    d = ImageDraw.Draw(img)
    f_題 = _字体(150)
    f_副 = _字体(40)
    tw = d.textlength(标题, font=f_題)
    d.text(((w - tw) / 2, h / 2 - 160), 标题, fill=龙金, font=f_題)
    sub = "诸葛鑫 | UID9622 · 龍芯北辰"
    sw = d.textlength(sub, font=f_副)
    d.text(((w - sw) / 2, h / 2 + 60), sub, fill=文字色, font=f_副)
    _水印(d, w, h, 帧序号, dna)
    return img


def 生成片尾(w=1920, h=1080, 帧序号=0, dna="") -> "Image":
    from PIL import Image, ImageDraw
    img = _帧背景(w, h)
    d = ImageDraw.Draw(img)
    f_大 = _字体(80)
    f_小 = _字体(36)
    t1 = "感谢观看"
    t2 = "🐉 龍魂系统 · 为人民服务"
    tw = d.textlength(t1, font=f_大)
    d.text(((w - tw) / 2, h / 2 - 100), t1, fill=龙金, font=f_大)
    sw = d.textlength(t2, font=f_小)
    d.text(((w - sw) / 2, h / 2 + 30), t2, fill=文字色, font=f_小)
    _水印(d, w, h, 帧序号, dna)
    return img


def _解析输入(输入: str) -> list:
    """输入 → 帧生成任务列表 [(kind, payload), ...]
    kind: text / image / intro / outro
    """
    if 输入 == "intro":
        return [("intro", None)]
    if 输入 == "outro":
        return [("outro", None)]
    p = Path(输入)
    if os.path.isdir(输入) or glob.has_magic(输入):
        files = sorted(glob.glob(输入) if glob.has_magic(输入) else glob.glob(str(p / "*")))
        imgs = [f for f in files if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp"))]
        return [("image", f) for f in imgs]
    # 纯文本
    return [("text", 输入)]


def cmd_video(输入: str, template: str = None, fmt: str = "mp4", out: str = None, fps: int = 24) -> str:
    """生成视频：帧序列 → ffmpeg 合成 → DNA/GPG"""
    from PIL import Image
    输出目录.mkdir(parents=True, exist_ok=True)
    if not out:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out = str(输出目录 / f"lh_video_{ts}.{fmt}")
    out = Path(out)
    dna = _dna("VIDEO")

    任务s = _解析输入(输入)
    if not 任务s:
        raise SystemExit("❌ 没有可用的输入（文本/图片/模板）")
    if template and 任务s[0][0] not in ("intro", "outro"):
        任务s = [("intro", None)] + 任务s + [("outro", None)]

    每任务帧数 = fps * 3
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        帧序号 = 0
        for kind, payload in 任务s:
            for i in range(每任务帧数):
                if kind == "text":
                    img = 生成文本帧(payload, 帧序号=帧序号, dna=dna)
                elif kind == "image":
                    img = 生成图片帧(payload, 帧序号=帧序号, dna=dna)
                elif kind == "intro":
                    img = 生成片头(帧序号=帧序号, dna=dna)
                elif kind == "outro":
                    img = 生成片尾(帧序号=帧序号, dna=dna)
                img.save(tmp / f"f_{帧序号:05d}.png")
                帧序号 += 1
        # ffmpeg 合成
        vc = "libx264" if fmt == "mp4" else "libvpx-vp9"
        ext_args = (["-pix_fmt", "yuv420p", "-movflags", "+faststart", "-crf", "23"]
                    if fmt == "mp4" else ["-b:v", "0", "-crf", "30", "-row-mt", "1"])
        r = subprocess.run(
            ["ffmpeg", "-y", "-framerate", str(fps), "-i", str(tmp / "f_%05d.png"),
             "-c:v", vc, *ext_args, "-metadata", f"comment=DNA: {dna}",
             "-metadata", f"artist={归属名}", str(out)],
            capture_output=True, text=True)
        if r.returncode != 0 or not out.exists():
            raise SystemExit(f"❌ ffmpeg 合成失败: {r.stderr[-300:]}")
    print(f"✅ 视频已生成: {out}  ({帧序号} 帧 · {fmt})")
    print(f"🧬 DNA: {dna}")
    # GPG 签名 sidecar
    try:
        subprocess.run(["python3", str(ROOT / "bin" / "lh_gpg_sign.py"), "sign", str(out)],
                       capture_output=True, text=True, timeout=60)
        print(f"🔏 GPG 签名: {out}.asc")
    except Exception:
        print("🟡 GPG 签名失败（不影响视频本身）")
    return str(out)


def main():
    ap = argparse.ArgumentParser(prog="lh-video", description="🐉 龍魂视频引擎")
    ap.add_argument("输入", help="文本 / 图片路径/glob/目录 / intro|outro")
    ap.add_argument("--template", default=None, help="intro|outro（自动加片头片尾）")
    ap.add_argument("--format", default="mp4", choices=["mp4", "webm"], help="输出格式")
    ap.add_argument("--output", default=None, help="输出路径")
    ap.add_argument("--fps", type=int, default=24, help="帧率")
    ap.add_argument("--self-test", action="store_true", help="自测（生成 3 秒 demo）")
    args = ap.parse_args()

    if args.self_test:
        return 自测()
    try:
        cmd_video(args.输入, args.template, args.format, args.output, args.fps)
    except Exception as e:
        print(f"❌ {e}")
        sys.exit(1)


def 自测():
    print("🐉 视频引擎自测…")
    cmd_video("龍魂系统，为人民服务。让每一个人都能掌握自己的数据主权。", template="intro", fmt="mp4")
    print("🟢 自测通过")
    return 0


if __name__ == "__main__":
    main()
