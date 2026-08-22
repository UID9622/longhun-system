#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
#龍芯⚡️丙午·丙申·戊申·亥时·䷗复-MULTIMEDIA-WATERMARK-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂·多媒体水印引擎 v1.0
按 LH-AI-IDENTITY-INTEROP-PROTOCOL-v3.0 §4.3 落地：
  图片 = EXIF/IPTC X-AI-Identity + 角标水印（Pillow）
  视频 = 元数据轨 + 片头片尾帧标识（FFmpeg）
  音频 = ID3 标签 + 频谱水印（mutagen + FFmpeg，频谱为实验性）
  PDF  = 元数据 + 页眉页脚追溯码（PyPDF2 + reportlab）
双标识原则（战后整顿协议 v1.0）：显式水印（人眼/人耳可见）+ 隐式元数据（机器可读）。

DNA: #龍芯⚡️丙午·丙申·戊申·亥时·䷗复-MULTIMEDIA-WATERMARK-v1.0

A-BOM 算法物料清单（算法审计协议 v1.0 备案）:
- 目标函数: 在不破坏媒体可用性的前提下，将 X-AI-Identity 身份标识写入
  显式（角标/片头帧/ID3注释/页脚）与隐式（EXIF/元数据轨/TXXX/PDF元数据）双通道
- 输入特征: 源媒体 + DNA 追溯码 + 来源声明 + 打标时间戳
- 用户影响: 增强 AI 内容可追溯性，保护创作者权益（标识不影响媒体正常使用）
- 申诉通道: UID9622（诸葛鑫）· GPG A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""
import os
import sys
import json
import time
import shutil
import argparse
import tempfile
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent.parent
DNA_TAG = "#龍芯⚡️丙午·丙申·戊申·亥时·䷗复-MULTIMEDIA-WATERMARK-v1.0"
IDENT_KEY = "X-AI-Identity"
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

# 显式角标默认显示（DNA 过长，取关键段）
EXPLICIT_PREFIX = "AI标识·龍魂"
SHORT_DNA_LEN = 22


# ---------------------------------------------------------------------------
# 工具
# ---------------------------------------------------------------------------
def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def media_sha3(path: Path, length: int = 12) -> str:
    h = hashlib.sha3_256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:length]


def build_ident(dna: str, source: str, ts: str = None) -> str:
    ts = ts or now_utc()
    return f"{IDENT_KEY}: {dna} | 来源: {source} | 时间: {ts} | 引擎: v1.0"


def short_dna(dna: str, n: int = SHORT_DNA_LEN) -> str:
    return dna if len(dna) <= n else dna[:n] + "…"


def find_font() -> str:
    """查找系统中文字体，用于角标渲染。"""
    candidates = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
        "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None


def ffmpeg_available() -> bool:
    return shutil.which("ffmpeg") is not None


def ffprobe_duration(path: Path) -> float:
    """探测媒体时长（秒）。"""
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries",
             "format=duration", "-of", "json", str(path)],
            capture_output=True, text=True, timeout=60,
        )
        data = json.loads(out.stdout)
        return float(data["format"]["duration"])
    except Exception:
        return 0.0


# ---------------------------------------------------------------------------
# 图片水印（Pillow）：角标（显式）+ EXIF UserComment（隐式）
# ---------------------------------------------------------------------------
def watermark_image(src: Path, dst: Path, dna: str, source: str, opacity: float = 0.45) -> dict:
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("[❌] 需要 Pillow: pip install Pillow")
        return {"ok": False, "msg": "Pillow 未安装"}

    img = Image.open(src).convert("RGB")
    ident = build_ident(dna, source)
    font_path = find_font()
    size_px = max(14, int(min(img.size) * 0.022))

    # --- 角标（右下角半透明） ---
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    if font_path:
        font = ImageFont.truetype(font_path, size_px)
    else:
        font = ImageFont.load_default()
    text = f"{EXPLICIT_PREFIX} · {short_dna(dna)}"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad = max(6, size_px // 2)
    x0, y0 = img.size[0] - tw - pad * 3, img.size[1] - th - pad * 3
    draw.rounded_rectangle(
        [x0, y0, x0 + tw + pad * 2, y0 + th + pad * 2],
        radius=pad, fill=(20, 20, 25, int(210 * opacity)),
    )
    draw.text((x0 + pad, y0 + pad // 2), text, font=font, fill=(255, 215, 130, 255))
    marked = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")

    # --- EXIF 隐式标识（UserComment = 0x9286） ---
    exif = Image.Exif()
    exif[0x9286] = (ident + f" | sha3:{media_sha3(src)}").encode("utf-8")
    exif[271] = "LongHun AI Identity v1.0"  # Make
    marked.save(dst, exif=exif)
    return {"ok": True, "ident": ident, "media": "image"}


# ---------------------------------------------------------------------------
# 视频水印（FFmpeg）：片头片尾帧（显式）+ 元数据轨（隐式）
# ---------------------------------------------------------------------------
def watermark_video(src: Path, dst: Path, dna: str, source: str, head_s: float = 2.0, tail_s: float = 2.0) -> dict:
    if not ffmpeg_available():
        return {"ok": False, "msg": "ffmpeg 未安装"}
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return {"ok": False, "msg": "Pillow 未安装"}

    ident = build_ident(dna, source)
    duration = ffprobe_duration(src)
    if duration <= head_s + tail_s:
        head_s, tail_s = duration * 0.1, duration * 0.1
    font_path = find_font()

    with tempfile.TemporaryDirectory() as td:
        tdir = Path(td)
        # 生成标识帧（1280x96 深色横条）
        frame_size = (1280, 96)
        def make_frame(text):
            im = Image.new("RGBA", frame_size, (20, 20, 25, 235))
            d = ImageDraw.Draw(im)
            font = ImageFont.truetype(font_path, 34) if font_path else ImageFont.load_default()
            d.text((24, 28), text, font=font, fill=(255, 215, 130, 255))
            p = tdir / "mark.png"
            im.save(p)
            return p
        start_png = make_frame(f"{EXPLICIT_PREFIX} · {short_dna(dna)} · 起点")
        end_png = make_frame(f"{EXPLICIT_PREFIX} · {short_dna(dna)} · 终点")

        start = max(0.0, duration - tail_s)
        fc = (
            f"[0:v][1:v]overlay=enable='lt(t,{head_s})':x=(W-w)/2:y=H-h-16[v1];"
            f"[v1][2:v]overlay=enable='gte(t,{start})':x=(W-w)/2:y=H-h-16[v]"
        )
        cmd = [
            "ffmpeg", "-y", "-i", str(src),
            "-i", str(start_png), "-i", str(end_png),
            "-filter_complex", fc, "-map", "[v]", "-map", "0:a?",
            "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            "-c:a", "aac", "-b:a", "128k",
            "-metadata", f"comment={ident}",
            "-metadata", f"artist={source}",
            "-metadata", "title=AI标识内容·龍魂",
            str(dst),
        ]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
        if r.returncode != 0:
            return {"ok": False, "msg": r.stderr[-600:]}
    return {"ok": True, "ident": ident, "media": "video", "duration": round(duration, 2)}


# ---------------------------------------------------------------------------
# 音频水印（mutagen）：ID3 COMM（显式）+ TXXX（隐式） + 可选频谱标记（实验性）
# ---------------------------------------------------------------------------
def watermark_audio(src: Path, dst: Path, dna: str, source: str, spectral: bool = False) -> dict:
    try:
        from mutagen.id3 import ID3, TXXX, COMM, ID3NoHeaderError
    except ImportError:
        return {"ok": False, "msg": "mutagen 未安装"}

    ident = build_ident(dna, source)
    shutil.copy2(src, dst)
    try:
        tags = ID3(str(dst))
    except ID3NoHeaderError:
        tags = ID3()
    tags.add(TXXX(encoding=3, desc=IDENT_KEY, text=f"{dna} | {source} | {now_utc()}"))
    tags.add(COMM(encoding=3, lang="zho", desc="龍魂AI标识",
                  text=f"🔍 追溯码: {dna}\n📖 来源: {source}"))
    tags.save(str(dst), v2_version=3)

    # 频谱标记（实验性）：18.5-19.5kHz 低频段注入 2s 短音（人耳基本不可感）
    if spectral and ffmpeg_available():
        with tempfile.TemporaryDirectory() as td:
            tone = Path(td) / "mark.wav"
            r1 = subprocess.run(
                ["ffmpeg", "-y", "-f", "lavfi", "-i", "sine=frequency=19000:duration=2",
                 "-ar", "44100", str(tone)],
                capture_output=True, text=True, timeout=60,
            )
            r2 = subprocess.run(
                ["ffmpeg", "-y", "-i", str(dst), "-i", str(tone),
                 "-filter_complex", "[0:a][1:a]amix=inputs=2:duration=first:dropout_transition=0[a]",
                 "-map", "[a]", "-c:a", "libmp3lame", "-b:a", "192k", "-metadata", f"comment={ident}",
                 str(dst) + ".tmp.mp3"],
                capture_output=True, text=True, timeout=300,
            )
            if r1.returncode == 0 and r2.returncode == 0:
                os.replace(str(dst) + ".tmp.mp3", str(dst))
                return {"ok": True, "ident": ident, "media": "audio", "spectral": True}
        return {"ok": True, "ident": ident, "media": "audio", "spectral": False}
    return {"ok": True, "ident": ident, "media": "audio", "spectral": False}


# ---------------------------------------------------------------------------
# PDF 水印（PyPDF2 + reportlab）：页脚文字（显式）+ 元数据（隐式）
# ---------------------------------------------------------------------------
def watermark_pdf(src: Path, dst: Path, dna: str, source: str) -> dict:
    """PDF 页眉页脚（显式·content stream 注入）+ 元数据（隐式）。

    零三方渲染依赖：直接往每页 /Contents 追加 Helvetica 文字操作符，
    中文用 UTF-16BE 十六进制字符串（<FEFF...>），标准 14 字体无需嵌入。
    """
    try:
        from PyPDF2 import PdfReader, PdfWriter
        from PyPDF2.generic import ArrayObject, DecodedStreamObject, NameObject
    except ImportError:
        return {"ok": False, "msg": "PyPDF2 未安装"}

    ident = build_ident(dna, source)
    reader = PdfReader(str(src))
    n = len(reader.pages)
    text = f"{EXPLICIT_PREFIX} · {short_dna(dna)} · 来源: {source}"

    def pdf_str(s: str) -> str:
        return "<" + s.encode("utf-16-be").hex() + ">"

    writer = PdfWriter()
    for page in reader.pages:
        pw, ph = float(page.mediabox.width), float(page.mediabox.height)
        fs = 7
        w = fs * len(text) * 1.0  # 中文按全角估算宽度
        x = max(18.0, pw - 36 - w)
        ops = (
            f"q BT /Helvetica {fs} Tf 1 0 0 1 {x:.2f} {18:.2f} Tm {pdf_str(text)} Tj ET Q "
            f"q BT /Helvetica {fs} Tf 1 0 0 1 {x:.2f} {ph - 18 - fs:.2f} Tm {pdf_str(text)} Tj ET Q"
        )
        stream = DecodedStreamObject()
        stream.set_data(ops.encode("latin-1"))
        existing = page.get("/Contents")
        if existing is None:
            page[NameObject("/Contents")] = stream
        elif isinstance(existing, ArrayObject):
            existing.append(stream)
        else:
            page[NameObject("/Contents")] = ArrayObject([existing, stream])
        writer.add_page(page)
    writer.add_metadata({
        "/Subject": f"{IDENT_KEY}: {dna} | 来源: {source} | {now_utc()}",
        "/Keywords": f"AI身份标识; 龍魂; {source}",
        "/Creator": "LongHun AI Identity v1.0",
    })
    with open(dst, "wb") as f:
        writer.write(f)
    return {"ok": True, "ident": ident, "media": "pdf", "pages": n}


# ---------------------------------------------------------------------------
# 验证（识别已打标媒体 / 缺失检测）
# ---------------------------------------------------------------------------
def verify_media(path: Path) -> dict:
    suffix = path.suffix.lower()
    result = {"file": str(path), "found": False, "ident": None}

    if suffix in (".jpg", ".jpeg", ".png", ".webp", ".tiff", ".bmp"):
        try:
            from PIL import Image
            exif = Image.open(path).getexif()
            raw = exif.get(0x9286)
            if raw:
                val = raw.decode("utf-8", errors="replace")
                result["found"] = True
                result["ident"] = val
        except Exception as e:
            result["error"] = str(e)

    elif suffix in (".mp4", ".mkv", ".mov", ".avi", ".webm"):
        try:
            out = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries",
                 "format_tags=comment,artist", "-of", "json", str(path)],
                capture_output=True, text=True, timeout=60,
            )
            tags = json.loads(out.stdout).get("format", {}).get("tags", {})
            val = tags.get("comment") or tags.get("artist")
            if val:
                result["found"] = True
                result["ident"] = val
        except Exception as e:
            result["error"] = str(e)

    elif suffix in (".mp3", ".wav", ".flac", ".m4a", ".aac", ".ogg"):
        try:
            from mutagen import File
            mf = File(str(path))
            if mf is not None and mf.tags is not None:
                if hasattr(mf.tags, "getall"):
                    for t in mf.tags.getall("TXXX"):
                        if t.desc == IDENT_KEY:
                            result["found"] = True
                            result["ident"] = f"{IDENT_KEY}: {t.text[0]}"
                            break
                    if not result["found"]:
                        for t in mf.tags.getall("COMM"):
                            if t.desc == "龍魂AI标识":
                                result["found"] = True
                                result["ident"] = t.text[0]
                                break
        except Exception as e:
            result["error"] = str(e)

    elif suffix == ".pdf":
        try:
            from PyPDF2 import PdfReader
            meta = PdfReader(str(path)).metadata or {}
            val = meta.get("/Subject") or meta.get("/Keywords")
            if val:
                result["found"] = True
                result["ident"] = val
        except Exception as e:
            result["error"] = str(e)

    return result


# ---------------------------------------------------------------------------
# 批处理
# ---------------------------------------------------------------------------
DISPATCH = {
    "image": (".jpg", ".jpeg", ".png", ".webp", ".tiff", ".bmp"),
    "video": (".mp4", ".mkv", ".mov", ".avi", ".webm"),
    "audio": (".mp3", ".wav", ".flac", ".m4a", ".aac", ".ogg"),
    "pdf": (".pdf",),
}


def batch_watermark(input_dir: Path, out_dir: Path, dna: str, source: str) -> list:
    out_dir.mkdir(parents=True, exist_ok=True)
    reports = []
    for kind, exts in DISPATCH.items():
        for p in input_dir.rglob("*"):
            if p.suffix.lower() not in exts:
                continue
            rel = p.relative_to(input_dir)
            dst = out_dir / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            if kind == "image":
                r = watermark_image(p, dst, dna, source)
            elif kind == "video":
                r = watermark_video(p, dst, dna, source)
            elif kind == "audio":
                r = watermark_audio(p, dst, dna, source)
            else:
                r = watermark_pdf(p, dst, dna, source)
            r.update({"file": str(rel), "kind": kind})
            reports.append(r)
            flag = "✅" if r.get("ok") else "❌"
            print(f"  {flag} [{kind}] {rel} -> {r.get('msg', 'ok') if not r.get('ok') else '已打标'}")
    return reports


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main() -> int:
    parser = argparse.ArgumentParser(description="龍魂·多媒体水印引擎 v1.0（图片/视频/音频/PDF）")
    sub = parser.add_subparsers(dest="cmd", required=True)

    for name in ("image", "video", "audio", "pdf"):
        sp = sub.add_parser(name, help=f"{name} 打标")
        sp.add_argument("src", help="源文件")
        sp.add_argument("dst", help="输出文件")
        sp.add_argument("--dna", required=True, help="DNA 追溯码")
        sp.add_argument("--source", required=True, help="来源声明，如 UID9622《方案名》")
        if name == "audio":
            sp.add_argument("--spectral", action="store_true", help="附加频谱水印（实验性）")

    vp = sub.add_parser("verify", help="验证已打标媒体")
    vp.add_argument("path", help="媒体文件")

    bp = sub.add_parser("batch", help="目录批量打标")
    bp.add_argument("input_dir", help="输入目录")
    bp.add_argument("output_dir", help="输出目录")
    bp.add_argument("--dna", required=True, help="DNA 追溯码")
    bp.add_argument("--source", required=True, help="来源声明")

    args = parser.parse_args()

    if args.cmd == "image":
        r = watermark_image(Path(args.src), Path(args.dst), args.dna, args.source)
    elif args.cmd == "video":
        r = watermark_video(Path(args.src), Path(args.dst), args.dna, args.source)
    elif args.cmd == "audio":
        r = watermark_audio(Path(args.src), Path(args.dst), args.dna, args.source, args.spectral)
    elif args.cmd == "pdf":
        r = watermark_pdf(Path(args.src), Path(args.dst), args.dna, args.source)
    elif args.cmd == "verify":
        r = verify_media(Path(args.path))
        if r["found"]:
            print(f"✅ 已标识: {r['ident']}")
        else:
            print(f"❌ 未检测到 {IDENT_KEY} 标识（{r.get('error', '无元数据')}）")
        return 0
    elif args.cmd == "batch":
        batch_watermark(Path(args.input_dir), Path(args.output_dir), args.dna, args.source)
        return 0
    else:
        parser.print_help()
        return 1

    if r.get("ok"):
        print(f"✅ [{r.get('media')}] 打标完成: {args.dst}")
        print(f"   {r['ident']}")
    else:
        print(f"[❌] 失败: {r.get('msg')}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
