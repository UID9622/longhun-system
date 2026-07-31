#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·乙未·戊寅·午时·大有-VOICE_GATEWAY-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""
龍魂 · 语音网关
语音输入 → 文本 → 执行 → 结果反馈

依赖:
    pip3 install speechrecognition pyaudio

用法:
    python3 bin/lh_voice_gateway.py           # 持续模式
    python3 bin/lh_voice_gateway.py --once    # 一句话模式
    python3 bin/lh_voice_gateway.py --text "健康检查"  # 文本模式
"""

import os
import sys
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LH_CMD = ROOT / "bin" / "lh.py"
LH_AUTO_TRIGGER = ROOT / "bin" / "lh_auto_trigger.py"


def execute_trigger(text: str) -> str:
    """执行触发词，返回输出"""
    try:
        cmd = [sys.executable, str(LH_AUTO_TRIGGER), text]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return result.stdout or result.stderr or "(无输出)"
    except subprocess.TimeoutExpired:
        return "⏰ 执行超时 (60s)"
    except Exception as e:
        return f"❌ 执行错误: {e}"


def text_mode(continuous: bool = True):
    """文本输入模式（无麦克风时）"""
    print("🐉 龍魂语音网关 · 文本模式")
    if continuous:
        print("输入命令 (说'退出'结束):")

    while True:
        try:
            text = input("🗣️ > ").strip()
            if not text:
                continue
        except (EOFError, KeyboardInterrupt):
            print("\n👋 退出语音网关")
            break

        print(f"📝 识别: {text}")

        if text in ("退出", "结束", "停止", "exit", "quit"):
            print("👋 退出语音网关")
            break

        result = execute_trigger(text)
        print(f"✅ 执行结果:\n{result}\n")


def voice_mode(continuous: bool = True):
    """语音输入模式"""
    try:
        import speech_recognition as sr
    except ImportError:
        print("❌ 需要安装: pip3 install speechrecognition pyaudio")
        print("💡 改用文本模式: lh voice --text")
        return

    recognizer = sr.Recognizer()
    try:
        mic = sr.Microphone()
    except Exception:
        print("❌ 无麦克风设备")
        print("💡 改用文本模式: lh voice --text")
        return

    print("🎤 语音网关已启动，请说话...")
    if continuous:
        print("（持续模式，说'退出'结束）")

    while True:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            except sr.WaitTimeoutError:
                continue

        try:
            text = recognizer.recognize_whisper(audio, language="zh")
            print(f"📝 识别: {text}")

            if "退出" in text or "停止" in text or "结束" in text:
                print("👋 退出语音网关")
                break

            result = execute_trigger(text)
            print(f"✅ 执行结果:\n{result}\n")

        except sr.UnknownValueError:
            print("❌ 未识别，请再说一遍")
        except Exception as e:
            print(f"❌ 错误: {e}")


def main():
    import argparse
    ap = argparse.ArgumentParser(description="龍魂语音网关")
    ap.add_argument("--once", action="store_true", help="只说一句就停")
    ap.add_argument("--text", action="store_true", help="文本输入模式（无需麦克风）")
    ap.add_argument("-c", type=str, help="直接执行一条文本命令")
    args = ap.parse_args()

    if args.c:
        print(f"📝 执行: {args.c}")
        result = execute_trigger(args.c)
        print(f"✅ {result}")
        return

    if args.text:
        text_mode(continuous=not args.once)
    else:
        voice_mode(continuous=not args.once)


if __name__ == "__main__":
    main()
