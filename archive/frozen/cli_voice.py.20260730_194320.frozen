#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 龍芯⚡️2026-06-18-CNSH-CLI-VOICE-v1.0
"""
通心译 | TongXinYi: CNSH Voice Command Line Interface
龍魂体系·语音命令行入口 — `cnsh-voice` 控制台脚本

提供语音合成（TTS）与语音识别（ASR）的命令行调用能力。
"""

import argparse
import asyncio
import sys
import os


def _ensure_cnsh_path():
    """Add the bundled CNSH root to sys.path so absolute imports work."""
    cnsh_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cnsh")
    if cnsh_root not in sys.path:
        sys.path.insert(0, cnsh_root)
    return cnsh_root


def cmd_tts(args):
    """Text-to-speech command."""
    _ensure_cnsh_path()
    from cnsh_runtime.cnsh.voice import 龍魂语音合成器

    合成器 = 龍魂语音合成器(
        语音角色=args.voice,
        输出目录=args.output_dir,
    )

    if args.text == "-":
        文本 = sys.stdin.read()
    else:
        文本 = args.text

    if not 文本.strip():
        print("[cnsh-voice] 🔴 文本为空", file=sys.stderr)
        return 1

    try:
        结果 = 合成器.文字转语音同步(
            文本,
            输出路径=args.output,
            语速=args.rate,
            音调=args.pitch,
        )
        print(f"[cnsh-voice] 🟢 合成成功")
        print(f"  输出: {结果.音频路径}")
        print(f"  时长: {结果.音频时长:.2f}s")
        print(f"  引擎: {结果.合成引擎}")
        print(f"  DNA: {结果.DNA追溯}")
        return 0
    except Exception as exc:
        print(f"[cnsh-voice] 🔴 合成失败: {exc}", file=sys.stderr)
        return 1


def cmd_asr(args):
    """Automatic speech recognition command."""
    _ensure_cnsh_path()
    from cnsh_runtime.cnsh.voice import 龍魂语音识别器

    识别器 = 龍魂语音识别器(
        模型名称=args.model,
        设备=args.device,
    )

    try:
        结果 = 识别器.语音转文字(
            args.audio,
            语言=args.language,
            温度=args.temperature,
        )
        print(f"[cnsh-voice] 🟢 识别成功")
        print(f"  文本: {结果.文本}")
        print(f"  置信度: {结果.置信度:.4f}")
        print(f"  语言: {结果.语言}")
        print(f"  模型: {结果.识别模型}")
        print(f"  DNA: {结果.DNA追溯}")
        return 0
    except Exception as exc:
        print(f"[cnsh-voice] 🔴 识别失败: {exc}", file=sys.stderr)
        return 1


def cmd_roles(args):
    """List available TTS voice roles."""
    _ensure_cnsh_path()
    from cnsh_runtime.cnsh.voice import 语音角色管理器
    语音角色管理器.列出角色(args.language)
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="cnsh-voice",
        description="龍魂 CNSH 语音能力命令行工具（TTS / ASR）",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # TTS subcommand
    tts_parser = subparsers.add_parser("tts", help="文字转语音")
    tts_parser.add_argument("text", help="要合成的文本，使用 '-' 从标准输入读取")
    tts_parser.add_argument("-o", "--output", help="输出音频文件路径")
    tts_parser.add_argument("-d", "--output-dir", default=None, help="输出目录")
    tts_parser.add_argument("-v", "--voice", default="xiaoxiao", help="语音角色代码")
    tts_parser.add_argument("-r", "--rate", type=float, default=1.0, help="语速倍率")
    tts_parser.add_argument("-p", "--pitch", type=float, default=0.0, help="音调偏移(Hz)")
    tts_parser.set_defaults(func=cmd_tts)

    # ASR subcommand
    asr_parser = subparsers.add_parser("asr", help="语音转文字")
    asr_parser.add_argument("audio", help="音频文件路径")
    asr_parser.add_argument("-m", "--model", default="base", help="Whisper 模型")
    asr_parser.add_argument("-l", "--language", default=None, help="语言代码")
    asr_parser.add_argument("--device", default="auto", help="计算设备")
    asr_parser.add_argument("-t", "--temperature", type=float, default=0.0, help="采样温度")
    asr_parser.set_defaults(func=cmd_asr)

    # Roles subcommand
    roles_parser = subparsers.add_parser("roles", help="列出可用语音角色")
    roles_parser.add_argument("-l", "--language", default=None, help="语言过滤")
    roles_parser.set_defaults(func=cmd_roles)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
