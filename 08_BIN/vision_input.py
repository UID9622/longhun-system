# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 本地视觉识别模块 v1.0
DNA: #龍芯⚡️丙午·丙申·丁卯·丙午·䷚颐-VISION-INPUT-v1.0
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

后端: Ollama moondream（本地推理·零云端·1.8B 轻量·CPU 可跑）
支持: 图片描述 / OCR文字提取 / 截图分析 / 目标检测 / 双图对比
适配: macOS（screencapture 兜底截图）· 大图自动压缩 · Ollama 在线检查

用法:
    python3 bin/vision_input.py screenshot.png "这里显示什么错误？"
    python3 bin/vision_input.py --screenshot "当前屏幕有什么异常？"
    python3 bin/vision_input.py --ocr screenshot.png
"""

import base64
import os
import subprocess
import sys
import tempfile
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parent.parent

OLLAMA_URL   = "http://localhost:11434/api/chat"
VISION_MODEL = "moondream"          # 可切 "llava:7b"（更强·需更多内存）

try:
    from PIL import Image
    PIL_READY = True
except ImportError:
    PIL_READY = False


def _check_ollama() -> bool:
    """Ollama 服务在线检查 + 视觉模型是否已拉"""
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=3)
        if r.status_code != 200:
            return False
        names = [m.get("name", "") for m in r.json().get("models", [])]
        base = VISION_MODEL.split(":")[0]
        if not any(n.startswith(base) for n in names):
            print(f"[i] 视觉模型 {VISION_MODEL} 未拉取 → ollama pull {VISION_MODEL}")
            return False
        return True
    except Exception:
        return False


def _image_to_b64(image_path: str) -> str:
    """图片 → base64 字符串（大图自动压缩到 1280）"""
    p = Path(image_path)
    if not p.exists():
        raise FileNotFoundError(f"图片不存在: {image_path}")

    if PIL_READY:
        img = Image.open(p).convert("RGB")
        if max(img.size) > 1280:
            img.thumbnail((1280, 1280), Image.LANCZOS)
            tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
            img.save(tmp.name, "JPEG", quality=85)
            image_path = tmp.name

    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def take_screenshot(region=None) -> str:
    """截屏，返回临时 png 路径（macOS screencapture 兜底）"""
    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    path = tmp.name
    tmp.close()

    try:
        if sys.platform == "darwin":
            # screencapture 在 /usr/sbin（PATH 可能不含）→ 绝对路径
            sc = None
            for cand in ("/usr/sbin/screencapture", "/usr/bin/screencapture", "screencapture"):
                import shutil
                if cand.startswith("/") and os.path.exists(cand):
                    sc = cand
                    break
                if shutil.which(cand):
                    sc = cand
                    break
            if sc is None:
                raise RuntimeError("找不到 screencapture")
            subprocess.run([sc, "-x", path], check=True, timeout=10)
            return path
        else:
            from PIL import ImageGrab
            img = ImageGrab.grab(bbox=region)
            img.save(path)
            return path
    except Exception as e:
        raise RuntimeError(f"截图失败: {e}（macOS 需允许 屏幕录制 权限）")


def _ollama_vision(prompt: str, image_b64: str, timeout: int = 90) -> str:
    """调用 Ollama 多模态模型"""
    if not _check_ollama():
        return "ERROR: Ollama 未运行或模型未就绪，请先执行 ollama serve / ollama pull moondream"

    payload = {
        "model": VISION_MODEL,
        "messages": [{
            "role": "user",
            "content": prompt,
            "images": [image_b64],
        }],
        "stream": False,
        "options": {"temperature": 0.1, "num_predict": 1024},
    }
    try:
        resp = requests.post(OLLAMA_URL, json=payload, timeout=timeout)
        resp.raise_for_status()
        return resp.json()["message"]["content"].strip()
    except requests.ConnectionError:
        return "ERROR: Ollama 未运行，请先执行 ollama serve"
    except Exception as e:
        return f"ERROR: {e}"


def describe_image(path: str, question: str = "详细描述这张图片的内容，包括主要物体、场景和文字") -> str:
    """描述图片内容。path: 相对 longhun-system/ 或绝对路径"""
    full_path = str(ROOT / path) if not Path(path).is_absolute() else path
    try:
        b64 = _image_to_b64(full_path)
        result = _ollama_vision(question, b64)
        # DNA 自动记录（CB-002 集成：写 .codebuddy/memory/ 每日日志）
        if result and not result.startswith("ERROR"):
            try:
                sys.path.insert(0, str(Path(__file__).resolve().parent))
                from dna_helper import append_with_dna
                append_with_dna(f"[视觉描述] {result[:300]}", source="vision", category="vision", action="描述", silent=True)
            except Exception:
                pass
        return result
    except Exception as e:
        return f"ERROR: {e}"


def extract_text_from_image(path: str) -> str:
    """OCR：提取图片中的文字"""
    return describe_image(
        path,
        question="请只提取图片中所有可见的文字，保持原始顺序和格式。如果没有文字，只回复「无文字」。不要添加任何解释。"
    )


def analyze_screenshot(question: str = "这个界面显示了什么？有没有明显错误或异常？") -> str:
    """截取当前屏幕并分析"""
    print("📸 截图中…")
    try:
        path = take_screenshot()
    except Exception as e:
        return f"ERROR: {e}"
    print(f"✅ 截图已保存: {path}")
    result = describe_image(path, question)
    try:
        os.unlink(path)
    except Exception:
        pass
    return result


def detect_objects(path: str) -> str:
    """目标检测：识别图片中的主要对象"""
    return describe_image(
        path,
        question="列出图片中所有主要可识别对象，格式严格为：\n对象名 - 大概位置/描述\n每行一个，不要额外解释。"
    )


def compare_images(path1: str, path2: str) -> str:
    """对比两张图片的差异"""
    desc1 = describe_image(path1, "用简洁的中文描述这张图片的核心内容")
    desc2 = describe_image(path2, "用简洁的中文描述这张图片的核心内容")
    prompt = (
        f"图片1描述：{desc1}\n\n图片2描述：{desc2}\n\n"
        "请对比两张图片的主要差异，用条目列出变化点。如果几乎相同，直接说「基本无差异」。"
    )
    try:
        payload = {
            "model": VISION_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "options": {"temperature": 0.1},
        }
        resp = requests.post(OLLAMA_URL, json=payload, timeout=60)
        resp.raise_for_status()
        diff = resp.json()["message"]["content"].strip()
    except Exception:
        diff = "（二次对比失败，仅返回两段描述）"
    return f"【图片1】\n{desc1}\n\n【图片2】\n{desc2}\n\n【差异】\n{diff}"


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="龍魂本地视觉识别 v1.0（Ollama moondream·零云端）")
    ap.add_argument("path", nargs="?", help="图片路径（或 --screenshot）")
    ap.add_argument("question", nargs="?", help="问题（默认描述）")
    ap.add_argument("--screenshot", action="store_true", help="截图并分析")
    ap.add_argument("--ocr", action="store_true", help="OCR 提取图片文字")
    ap.add_argument("--detect", action="store_true", help="目标检测")
    ap.add_argument("--compare", nargs=2, metavar=("IMG1", "IMG2"), help="对比两张图片")
    ap.add_argument("--model", default=None, help=f"视觉模型（默认 {VISION_MODEL}·可切 llava:7b）")
    args = ap.parse_args()

    if args.model:
        VISION_MODEL = args.model

    if args.compare:
        print(compare_images(*args.compare))
    elif args.screenshot:
        q = args.question or "描述当前屏幕内容，有没有异常"
        print(analyze_screenshot(q))
    elif args.ocr and args.path:
        print(extract_text_from_image(args.path))
    elif args.detect and args.path:
        print(detect_objects(args.path))
    elif args.path:
        q = args.question or "详细描述这张图片"
        print(describe_image(args.path, q))
    else:
        ap.print_help()
