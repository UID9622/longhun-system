#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂多模态命令行入口
====================
把下载包里的感知中枢、语音合成、图像识别、语音识别模块挂到一条简单 CLI 上。

目前可直接使用：
  - speak   : 文字转语音（edge-tts / pyttsx3 自动降级）
  - ocr     : 图像文字识别（PIL + OpenCV + Tesseract）
  - perceive: 自动判断文件类型并提取文字

需要额外安装 openai-whisper 后才能使用：
  - stt     : 语音转文字

用法示例：
  python3 multimodal_cli.py speak "你好，龍魂系统"
  python3 multimodal_cli.py ocr ~/Desktop/screenshot.png
  python3 multimodal_cli.py perceive ~/Downloads/sample.mp3

DNA:#龍芯⚡️2026-06-18-CNSH-MULTIMODAL-CLI-FILE1-v1.0
"""

import os
import sys
import asyncio
import argparse
from pathlib import Path

# 让 Python 找得到中文名称的多模态模块
_MODULE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "modules", "multimodal")
if _MODULE_DIR not in sys.path:
    sys.path.insert(0, _MODULE_DIR)


def _hub():
    """懒加载感知中枢，避免一启动 CLI 就载入所有子引擎。"""
    from 龍魂多模态感知中枢 import 龍魂多模态感知中枢
    return 龍魂多模态感知中枢()


def cmd_speak(args):
    文本 = args.text
    if not 文本:
        return "❌ 请提供要合成的文字"

    输出路径 = args.output or os.path.expanduser(
        f"~/龍魂语音输出/龍魂语音_{os.getpid()}.mp3"
    )
    os.makedirs(os.path.dirname(输出路径), exist_ok=True)

    # 离线模式：macOS 用系统 say 命令，不联网
    if args.offline:
        import platform
        if platform.system() == "Darwin":
            try:
                # say 默认输出 AIFF 格式，按扩展名决定
                if not 输出路径.endswith((".aiff", ".aif", ".wav")):
                    输出路径 = 输出路径.rsplit(".", 1)[0] + ".aiff"
                os.makedirs(os.path.dirname(输出路径), exist_ok=True)
                rate = int(150 * args.speed)
                voice = "Ting-Ting" if "zh" in (args.voice or "").lower() else None
                cmd = ["say", "-o", 输出路径, 文本]
                if voice:
                    cmd[1:1] = ["-v", voice]
                import subprocess
                subprocess.run(cmd, check=True, timeout=60)
                return f"✅ 离线语音已生成（macOS say）\n🎧 {输出路径}"
            except Exception as e:
                return f"❌ 离线语音合成失败：{e}"
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty('rate', int(150 * args.speed))
            engine.save_to_file(文本, 输出路径)
            engine.runAndWait()
            return f"✅ 离线语音已生成（pyttsx3）\n🎧 {输出路径}"
        except Exception as e:
            return f"❌ 离线语音合成失败：{e}"

    # 在线模式：优先 edge-tts，失败自动降级到 pyttsx3
    try:
        路径 = _hub().表达(文本, 输出路径=输出路径, 语音角色=args.voice, 语速=args.speed)
        return f"✅ 语音已生成\n🎧 {路径}"
    except Exception as e:
        return f"❌ 语音合成失败：{e}"


def cmd_ocr(args):
    路径 = args.image
    if not os.path.exists(路径):
        return f"❌ 找不到图像：{路径}"

    try:
        from 龍魂图像识别器 import 龍魂图像识别器
        识别器 = 龍魂图像识别器(识别语言=args.lang or "eng")
        结果 = 识别器.提取文字(路径)
        return (
            f"🖼️ 图像识别结果\n"
            f"置信度：{结果.置信度:.2f}\n"
            f"提取文字：\n{结果.原始文本 or '(未识别到文字)'}"
        )
    except Exception as e:
        return f"❌ 图像识别失败：{e}"


def cmd_stt(args):
    路径 = args.audio
    if not os.path.exists(路径):
        return f"❌ 找不到音频：{路径}"

    try:
        import whisper  # noqa: F401
    except ImportError:
        return (
            "⚠️ 语音识别需要 openai-whisper\n"
            "请运行：pip install openai-whisper soundfile\n"
            "安装后即可使用 stt 命令。"
        )

    try:
        from 龍魂多模态感知中枢 import 感知类型
        结果 = _hub().感知(路径, 感知类型.语音)
        return (
            f"🎙️ 语音识别结果\n"
            f"置信度：{结果.置信度:.2f}\n"
            f"文字：{结果.提取的文字 or '(未识别到文字)'}"
        )
    except Exception as e:
        return f"❌ 语音识别失败：{e}"


def cmd_perceive(args):
    路径 = args.path
    if not os.path.exists(路径):
        return f"❌ 找不到文件：{路径}"

    try:
        结果 = _hub().感知(路径)
        return (
            f"🐉 龍魂多模态感知\n"
            f"类型：{结果.感知类型.value}\n"
            f"模块：{结果.使用模块}\n"
            f"置信度：{结果.置信度:.2f}\n"
            f"提取文字：\n{结果.提取的文字 or '(无文字内容)'}"
        )
    except Exception as e:
        return f"❌ 感知处理失败：{e}"


def main():
    parser = argparse.ArgumentParser(
        prog="multimodal_cli.py",
        description="龍魂多模态感知命令行入口（语音合成 / OCR / 语音识别）"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_speak = sub.add_parser("speak", help="文字转语音")
    p_speak.add_argument("text", help="要合成的文字")
    p_speak.add_argument("--voice", default="zh-CN-XiaoxiaoNeural", help="语音角色")
    p_speak.add_argument("--speed", type=float, default=1.0, help="语速倍率")
    p_speak.add_argument("--output", "-o", default=None, help="输出音频路径")
    p_speak.add_argument("--offline", action="store_true", help="强制使用离线引擎 pyttsx3，不联网")
    p_speak.set_defaults(func=cmd_speak)

    p_ocr = sub.add_parser("ocr", help="图像文字识别")
    p_ocr.add_argument("image", help="图像文件路径")
    p_ocr.add_argument("--lang", default="eng", help="识别语言，默认 eng（可选 chi_sim/chi_tra）")
    p_ocr.set_defaults(func=cmd_ocr)

    p_stt = sub.add_parser("stt", help="语音转文字（需安装 openai-whisper）")
    p_stt.add_argument("audio", help="音频文件路径")
    p_stt.set_defaults(func=cmd_stt)

    p_perceive = sub.add_parser("perceive", help="自动判断文件类型并提取内容")
    p_perceive.add_argument("path", help="文件路径")
    p_perceive.set_defaults(func=cmd_perceive)

    args = parser.parse_args()
    result = args.func(args)
    print(result)


if __name__ == "__main__":
    main()
