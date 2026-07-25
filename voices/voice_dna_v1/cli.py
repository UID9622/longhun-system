#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂声纹 DNA 锚定链 CLI（多用户注册版）
用法:
    lh voice anchor "文本内容"            录入声纹并生成DNA锚定链
    lh voice register <user_id> "文本"    用户注册声纹
    lh voice verify "数字人ID"            验证数字人身份
    lh voice list                         列出所有已锚定的数字人身份
    lh voice personas <user_id>           列出某用户的数字人身份
    lh voice audit [N]                    查看最近 N 条审计日志
    lh voice backup                       执行本地每日备份
    lh voice snapshot [label]             创建完整快照
    lh voice export <user_id> [pid]       导出用户声纹DNA包
    lh voice serve [port]                 启动官网注册 API

DNA: #龍芯⚡️20260628-VOICE-CLI-v2.0
"""

import os
import sys
import json
import argparse

sys.path.insert(0, os.path.dirname(__file__))

from voice_anchor import anchor_voice, generate_test_audio
from register import register_user_voice, get_user_personas
from digital_persona import list_personas
from verify_anchor import verify_voice, show_audit_tail
from backup import daily_backup, create_snapshot, list_backups, export_user_package, auto_backup_if_needed


def cmd_anchor(args):
    text = args.text or "我是UID9622，龍魂系统唯一主权者"
    if args.test:
        print("🧪 测试模式：使用合成音频")
        audio = generate_test_audio(frequency=args.test_freq)
        result = anchor_voice(text, audio=audio, source="test", encrypt=not args.no_encrypt)
    else:
        result = anchor_voice(text, encrypt=not args.no_encrypt)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("status") in ("success", "duplicate") else 1


def cmd_register(args):
    if not args.user_id:
        print("❌ 请提供 user_id")
        return 1
    text = args.text or "我是UID9622，龍魂系统唯一主权者"
    if args.test:
        print("🧪 测试模式：使用合成音频")
        audio = generate_test_audio(frequency=args.test_freq)
        result = register_user_voice(args.user_id, text, audio=audio, source="test")
    else:
        result = register_user_voice(args.user_id, text)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("status") in ("success", "duplicate") else 1


def cmd_verify(args):
    if not args.persona_id:
        print("❌ 请提供数字人ID")
        return 1
    if args.test:
        print("🧪 测试模式：使用合成音频验证")
        audio = generate_test_audio(frequency=args.test_freq)
        result = verify_voice(args.persona_id, audio=audio, user_id=args.user_id)
    else:
        result = verify_voice(args.persona_id, user_id=args.user_id)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("status") == "match" else 1


def cmd_list(args):
    anchors = list_personas()
    print(json.dumps(anchors, ensure_ascii=False, indent=2))
    print(f"\n📊 共 {len(anchors)} 条已锚定数字人身份")
    return 0


def cmd_personas(args):
    if not args.user_id:
        print("❌ 请提供 user_id")
        return 1
    result = get_user_personas(args.user_id)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def cmd_audit(args):
    n = args.n if hasattr(args, "n") else 10
    records = show_audit_tail(n)
    print(json.dumps(records, ensure_ascii=False, indent=2))
    print(f"\n📋 最近 {len(records)} 条审计记录")
    return 0


def cmd_backup(args):
    r = daily_backup()
    print(json.dumps(r, ensure_ascii=False, indent=2))
    return 0


def cmd_snapshot(args):
    r = create_snapshot(label=args.label)
    print(json.dumps(r, ensure_ascii=False, indent=2))
    return 0


def cmd_list_backups(args):
    r = list_backups()
    print(json.dumps(r, ensure_ascii=False, indent=2))
    return 0


def cmd_export(args):
    if not args.user_id:
        print("❌ 请提供 user_id")
        return 1
    password = args.password or "longhun-voice"
    result = export_user_package(args.user_id, args.persona_id, password=password)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("status") == "success" else 1


def cmd_serve(args):
    port = args.port if hasattr(args, "port") else 8444
    print(f"🚀 启动龍魂声纹DNA API: http://127.0.0.1:{port}")
    from web_api import app
    app.run(host="127.0.0.1", port=port, debug=False)
    return 0


def print_usage():
    print("""
🐉 龍魂声纹 DNA 锚定链 CLI

用法:
    lh voice anchor "文本内容"              录入声纹并生成 DNA 锚定链
    lh voice register <user_id> "文本"      用户注册声纹
    lh voice verify "数字人ID"              验证数字人身份
    lh voice list                           列出所有已锚定的数字人身份
    lh voice personas <user_id>             列出某用户的数字人身份
    lh voice audit [N]                      查看最近 N 条审计日志
    lh voice backup                         执行本地每日备份
    lh voice snapshot [label]               创建完整快照
    lh voice backups                        列出备份与快照
    lh voice export <user_id> [persona_id]  导出用户声纹DNA包
    lh voice serve [port]                   启动官网注册 API

测试模式（无需麦克风）:
    lh voice anchor "文本" --test [--freq 210]
    lh voice register user1 "文本" --test [--freq 210]
    lh voice verify "ID" --test [--freq 210]
""")


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    if not argv or argv[0] in ("-h", "--help", "help"):
        print_usage()
        return 0

    sub = argv[0]
    rest = argv[1:]

    base_parser = argparse.ArgumentParser(prog=f"lh voice {sub}", add_help=False)
    base_parser.add_argument("--test", action="store_true", help="使用合成音频测试，无需麦克风")
    base_parser.add_argument("--freq", type=float, dest="test_freq", default=230.0, help="测试音频基频")

    if sub == "anchor":
        parser = argparse.ArgumentParser(parents=[base_parser], add_help=False)
        parser.add_argument("text", nargs="?", default=None, help="锚定文本内容")
        parser.add_argument("--no-encrypt", action="store_true", help="不加密特征向量（仅测试）")
        args = parser.parse_args(rest)
        return cmd_anchor(args)

    if sub == "register":
        parser = argparse.ArgumentParser(parents=[base_parser], add_help=False)
        parser.add_argument("user_id", nargs="?", default=None, help="用户ID")
        parser.add_argument("text", nargs="?", default=None, help="锚定文本")
        args = parser.parse_args(rest)
        return cmd_register(args)

    if sub == "verify":
        parser = argparse.ArgumentParser(parents=[base_parser], add_help=False)
        parser.add_argument("persona_id", nargs="?", default=None, help="数字人ID")
        parser.add_argument("--user-id", dest="user_id", default=None, help="限定用户ID")
        args = parser.parse_args(rest)
        return cmd_verify(args)

    if sub == "list":
        return cmd_list(None)

    if sub == "personas":
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument("user_id", nargs="?", default=None, help="用户ID")
        args = parser.parse_args(rest)
        return cmd_personas(args)

    if sub == "audit":
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument("n", nargs="?", type=int, default=10, help="显示条数")
        args = parser.parse_args(rest)
        return cmd_audit(args)

    if sub == "backup":
        return cmd_backup(None)

    if sub == "snapshot":
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument("label", nargs="?", default=None, help="快照标签")
        args = parser.parse_args(rest)
        return cmd_snapshot(args)

    if sub == "backups":
        return cmd_list_backups(None)

    if sub == "export":
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument("user_id", nargs="?", default=None, help="用户ID")
        parser.add_argument("persona_id", nargs="?", default=None, help="数字人ID（可选）")
        parser.add_argument("--password", default="longhun-voice", help="导出包密码")
        args = parser.parse_args(rest)
        return cmd_export(args)

    if sub == "serve":
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument("port", nargs="?", type=int, default=8444, help="监听端口")
        args = parser.parse_args(rest)
        return cmd_serve(args)

    print(f"❌ 未知子命令: {sub}")
    print_usage()
    return 1


if __name__ == "__main__":
    sys.exit(main())
