#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂视觉模块 v1.2 · DNA集成版
DNA: #龍芯⚡️2026-08-21-VISION-v1.2
集成: DNA自动生成 · MEMORY自动写入
"""

import base64
import tempfile
import sys
from pathlib import Path

try:
    import requests
    from PIL import Image, ImageGrab
    PIL_OK = True
except ImportError:
    PIL_OK = False

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "08_BIN"))
from dna_helper import append_with_dna

OLLAMA_URL = "http://localhost:11434/api/chat"
VISION_MODEL = "moondream"
MEMORY_FILE = ROOT / "MEMORY.md"


def _check_ollama() -> bool:
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=3)
        return r.status_code == 200
    except Exception:
        return False


def _image_to_b64(path: str) -> str:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"图片不存在: {p}")
    if PIL_OK:
        img = Image.open(p).convert("RGB")
        if max(img.size) > 1280:
            img.thumbnail((1280, 1280), Image.LANCZOS)
        tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
        img.save(tmp.name, "JPEG", quality=85)
        path = tmp.name
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def _ask(prompt: str, img_b64: str) -> str:
    if not _check_ollama():
        return "ERROR: Ollama未运行 (ollama serve)"
    payload = {
        "model": VISION_MODEL,
        "messages": [{"role": "user", "content": prompt, "images": [img_b64]}],
        "stream": False,
        "options": {"temperature": 0.1},
    }
    try:
        r = requests.post(OLLAMA_URL, json=payload, timeout=90)
        r.raise_for_status()
        return r.json()["message"]["content"].strip()
    except Exception as e:
        return f"ERROR: {e}"


def describe_image(path: str, question: str = "详细描述这张图片") -> str:
    try:
        b64 = _image_to_b64(path)
        result = _ask(question, b64)
        if result and not result.startswith("ERROR"):
            append_with_dna(f"[图片描述] {result[:200]}...",
                           source="vision", category="vision", action="描述")
        return result
    except Exception as e:
        return f"ERROR: {e}"


def analyze_screenshot(question: str = "分析当前屏幕内容") -> str:
    if not PIL_OK:
        return "ERROR: 需要安装 Pillow"
    print("📸 截图中...")
    img = ImageGrab.grab()
    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    img.save(tmp.name)
    return describe_image(tmp.name, question)


def extract_text_from_image(path: str) -> str:
    return describe_image(
        path,
        question="只提取图片中所有可见文字，保持顺序。无文字则回复'无文字'。"
    )


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", help="图片路径")
    parser.add_argument("--screenshot", action="store_true")
    parser.add_argument("--question", default="详细描述这张图片")
    parser.add_argument("--ocr", action="store_true")
    args = parser.parse_args()

    if args.screenshot:
        print(analyze_screenshot(args.question))
    elif args.ocr and args.path:
        print(extract_text_from_image(args.path))
    elif args.path:
        print(describe_image(args.path, args.question))
    else:
        print("用法: vision_input.py <图片路径> [--screenshot] [--ocr]")
