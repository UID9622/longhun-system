#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
"""
🐉 龍魂统一引擎 · 启动器
=========================
一个命令启动所有通道。

用法:
  python3 引擎/launcher.py                    # 启动所有通道
  python3 引擎/launcher.py --feishu           # 仅飞书
  python3 引擎/launcher.py --wechat           # 仅微信
  python3 引擎/launcher.py --web              # 仅Web
  python3 引擎/launcher.py --cli              # 交互式CLI
  python3 引擎/launcher.py --health           # 健康检查

DNA: #龍芯⚡️丙午·乙未·甲子·申时·需-LAUNCHER-v1.0
"""

from __future__ import annotations
import sys
import os
import argparse
import subprocess
import signal
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

DNA = "#龍芯⚡️丙午·乙未·甲子·申时·需-LAUNCHER-v1.0"

SERVICES = {
    "feishu": {
        "name": "飞书通道",
        "script": ROOT / "引擎/channels/feishu_adapter.py",
        "port": int(os.getenv("FEISHU_BOT_PORT", "9637")),
        "emoji": "💬",
    },
    "wechat": {
        "name": "微信通道",
        "script": ROOT / "引擎/channels/wechat_adapter.py",
        "port": int(os.getenv("WECHAT_BOT_PORT", "9638")),
        "emoji": "💚",
    },
    "web": {
        "name": "Web通道",
        "script": ROOT / "引擎/channels/web_adapter.py",
        "port": int(os.getenv("WEB_BOT_PORT", "9639")),
        "emoji": "🌐",
    },
    "ant_colony": {
        "name": "蚁群守护",
        "script": ROOT / "bin/lh_ant_colony_daemon.py",
        "port": int(os.getenv("ANT_COLONY_PORT", "9677")),
        "emoji": "🐜",
        # 蚁群守护不是通道适配器，需要用 serve 子命令启动
        "extra_args": ["serve", "--port", str(int(os.getenv("ANT_COLONY_PORT", "9677")))],
    },
}


def print_banner(active: List[str]):
    """打印启动横幅"""
    print(f"""
╔══════════════════════════════════════════════════════════╗
║     🐉 龍魂统一引擎 v2.0 · 启动器                      ║
╠══════════════════════════════════════════════════════════╣
║     {DNA}
║     一个引擎 · 多个出口 · 数据主权归本地               ║
╚══════════════════════════════════════════════════════════╝
""")
    for key in active:
        svc = SERVICES[key]
        print(f"  {svc['emoji']} {svc['name']:8s}  :{svc['port']:<6} python3 {svc['script'].relative_to(ROOT)}")
    print()


def run_cli():
    """交互式命令行模式"""
    from 引擎.message import Message, Channel
    from 引擎.engine_core import LonghunEngine

    engine = LonghunEngine(safe_mode=False)
    print(f"""
🐉 龍魂引擎 · CLI 模式
   输入消息，回车发送。输入 q 退出。
   已注册 {len(engine.registry.list_all())} 项能力。
""")
    while True:
        try:
            text = input("> ").strip()
            if text.lower() in ("q", "quit", "exit"):
                print("👋 再见")
                break
            if text:
                msg = Message(channel=Channel.CLI, content=text)
                response = engine.process(msg)
                print()
                print(response.to_text())
                print()
        except (KeyboardInterrupt, EOFError):
            print("\n👋 再见")
            break


def start_services(active: List[str]):
    """启动选中的通道服务"""
    processes = []
    
    def cleanup(sig, frame):
        print("\n🛑 停止所有服务...")
        for p in processes:
            p.terminate()
        for p in processes:
            p.wait(timeout=5)
        print("✅ 所有服务已停止")
        sys.exit(0)

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    for key in active:
        svc = SERVICES[key]
        script = svc["script"]
        if not script.exists():
            print(f"  🔴 {svc['name']}: 脚本不存在 {script}")
            continue
        
        env = os.environ.copy()
        env["PYTHONPATH"] = str(ROOT) + ":" + env.get("PYTHONPATH", "")
        
        cmd = [sys.executable, str(script)]
        if "extra_args" in svc:
            cmd.extend(svc["extra_args"])

        p = subprocess.Popen(
            cmd,
            cwd=str(ROOT),
            env=env,
        )
        processes.append(p)
        print(f"  {svc['emoji']} {svc['name']:8s} :{svc['port']}  PID={p.pid}")

    print(f"\n  ✅ {len(processes)} 个通道服务已启动")
    print(f"  📡 按 Ctrl+C 停止所有\n")

    # 等待任一进程退出
    try:
        for p in processes:
            p.wait()
    except KeyboardInterrupt:
        cleanup(None, None)


VIDEO_ENGINES = {
    "video-gen": {
        "name": "视频生成",
        "script": ROOT / "bin/lh_video_generator.py",
        "emoji": "🎬",
        "args": ["--prompt", "--dna", "--output"],
    },
    "video-analyze": {
        "name": "视频分析",
        "script": ROOT / "bin/lh_video_analyzer.py",
        "emoji": "🔍",
        "args": ["--input", "--dna", "--audit"],
    },
    "video-dna": {
        "name": "视频DNA嵌入",
        "script": ROOT / "bin/lh_video_dna_embedder.py",
        "emoji": "🧬",
        "args": ["--input", "--dna", "--method", "--strength"],
    },
}

AUDIO_ENGINES = {
    "tts": {
        "name": "TTS语音合成",
        "script": ROOT / "bin/lh_tts_engine.py",
        "emoji": "🔊",
        "args": ["--text", "--voice", "--dna", "--output"],
    },
    "asr": {
        "name": "ASR语音识别",
        "script": ROOT / "bin/lh_asr_engine.py",
        "emoji": "🎤",
        "args": ["--input", "--lang", "--dna"],
    },
    "voice-clone": {
        "name": "语音克隆",
        "script": ROOT / "bin/lh_voice_clone.py",
        "emoji": "🗣️",
        "args": ["--sample", "--target", "--auth", "--output"],
        "dangerous": True,
    },
    "voice-chat": {
        "name": "语音对话",
        "script": ROOT / "bin/lh_voice_chat.py",
        "emoji": "💬",
        "args": ["--dna", "--voice", "--model", "--lang"],
    },
}

SEARCH_ENGINES = {
    "global-search": {
        "name": "全球全量搜索",
        "script": ROOT / "bin/lh_global_search_v2.py",
        "emoji": "🔍",
        "args": ["--query", "--persona", "--top-k"],
    },
}

CNSH_ENGINES = {
    "cnsh-compile": {
        "name": "CNSH多语言编译",
        "script": ROOT / "bin/lh_cnsh_compiler.py",
        "emoji": "🌐",
        "args": ["--input", "--lang", "--output", "--target"],
    },
    "cnsh-run": {
        "name": "CNSH终端执行",
        "script": ROOT / "bin/lh_cnsh_run.sh",
        "emoji": "▶️",
        "type": "shell",
        "args": ["FILE", "LANG"],
    },
}


def run_video_tool(tool: str, tool_args: argparse.Namespace):
    """运行视频引擎工具"""
    eng = VIDEO_ENGINES.get(tool)
    if not eng:
        print(f"❌ 未知视频工具: {tool}")
        print(f"   可用: {', '.join(VIDEO_ENGINES.keys())}")
        return
    script = eng["script"]
    if not script.exists():
        print(f"🔴 {eng['name']}: 脚本不存在 {script}")
        return
    # 构建命令行参数
    cmd = [sys.executable, str(script)]
    for arg_name in eng["args"]:
        arg_key = arg_name.lstrip("-").replace("-", "_")
        val = getattr(tool_args, arg_key, None)
        if val is not None:
            if isinstance(val, bool) and val:
                cmd.append(arg_name)
            elif not isinstance(val, bool):
                cmd.append(arg_name)
                cmd.append(str(val))
    print(f"  {eng['emoji']} {eng['name']}")
    print(f"  ▶️ {' '.join(cmd)}")
    subprocess.run(cmd, cwd=str(ROOT))


def run_audio_tool(tool: str, tool_args: argparse.Namespace):
    """运行语音引擎工具"""
    eng = AUDIO_ENGINES.get(tool)
    if not eng:
        print(f"❌ 未知语音工具: {tool}")
        print(f"   可用: {', '.join(AUDIO_ENGINES.keys())}")
        return
    if eng.get("dangerous"):
        print(f"  {eng['emoji']} {eng['name']} ⚠️ 需#CONFIRM授权")
    script = eng["script"]
    if not script.exists():
        print(f"🔴 {eng['name']}: 脚本不存在 {script}")
        return
    cmd = [sys.executable, str(script)]
    for arg_name in eng["args"]:
        arg_key = arg_name.lstrip("-").replace("-", "_")
        val = getattr(tool_args, arg_key, None)
        if val is not None:
            if isinstance(val, bool) and val:
                cmd.append(arg_name)
            elif not isinstance(val, bool):
                cmd.append(arg_name)
                cmd.append(str(val))
    print(f"  {eng['emoji']} {eng['name']}")
    print(f"  ▶️ {' '.join(cmd)}")
    subprocess.run(cmd, cwd=str(ROOT))


def run_search_tool(tool: str, tool_args: argparse.Namespace):
    """运行搜索引擎工具"""
    eng = SEARCH_ENGINES.get(tool)
    if not eng:
        print(f"❌ 未知搜索工具: {tool}")
        print(f"   可用: {', '.join(SEARCH_ENGINES.keys())}")
        return
    script = eng["script"]
    if not script.exists():
        print(f"🔴 {eng['name']}: 脚本不存在 {script}")
        return
    cmd = [sys.executable, str(script)]
    if tool_args.query:
        cmd.extend(["--query", tool_args.query])
    if tool_args.persona:
        cmd.extend(["--persona", tool_args.persona])
    if tool_args.top_k:
        cmd.extend(["--top-k", str(tool_args.top_k)])
    print(f"  {eng['emoji']} {eng['name']}")
    print(f"  ▶️ {' '.join(cmd)}")
    subprocess.run(cmd, cwd=str(ROOT))


def run_cnsh_tool(tool: str, tool_args: argparse.Namespace):
    """运行CNSH工具"""
    eng = CNSH_ENGINES.get(tool)
    if not eng:
        print(f"❌ 未知CNSH工具: {tool}")
        print(f"   可用: {', '.join(CNSH_ENGINES.keys())}")
        return
    script = eng["script"]
    if not script.exists():
        print(f"🔴 {eng['name']}: 脚本不存在 {script}")
        return
    if eng.get("type") == "shell":
        cmd = ["bash", str(script)]
        if tool_args.cnsh_file:
            cmd.append(tool_args.cnsh_file)
        if tool_args.lang:
            cmd.append(tool_args.lang)
    else:
        cmd = [sys.executable, str(script)]
        for arg_name in eng["args"]:
            arg_key = arg_name.lstrip("-").replace("-", "_").lower()
            val = getattr(tool_args, arg_key, None)
            if val is not None:
                if isinstance(val, bool) and val:
                    cmd.append(arg_name)
                elif not isinstance(val, bool):
                    cmd.append(arg_name)
                    cmd.append(str(val))
    print(f"  {eng['emoji']} {eng['name']}")
    print(f"  ▶️ {' '.join(cmd)}")
    subprocess.run(cmd, cwd=str(ROOT))


def list_video_audio_tools():
    """列出所有视频/音频/搜索/CNSH工具"""
    print("\n🎬 视频引擎:")
    for key, eng in VIDEO_ENGINES.items():
        print(f"  {eng['emoji']} {key:16s} — {eng['name']}")
    print("\n🎤 语音引擎:")
    for key, eng in AUDIO_ENGINES.items():
        tag = " ⚠️需授权" if eng.get("dangerous") else ""
        print(f"  {eng['emoji']} {key:16s} — {eng['name']}{tag}")
    print("\n🔍 搜索引擎:")
    for key, eng in SEARCH_ENGINES.items():
        print(f"  {eng['emoji']} {key:16s} — {eng['name']}")
    print("\n🌐 CNSH引擎:")
    for key, eng in CNSH_ENGINES.items():
        print(f"  {eng['emoji']} {key:16s} — {eng['name']}")
    print()


def run_health():
    """健康检查（检查所有通道是否在线）"""
    import urllib.request
    import json as _json
    for key, svc in SERVICES.items():
        url = f"http://127.0.0.1:{svc['port']}/health"
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=3) as resp:
                data = _json.loads(resp.read())
                status = data.get("status", "unknown")
                print(f"  {svc['emoji']} {svc['name']:8s} :{svc['port']}  {'🟢' if status == 'ok' else '🟡'}  {status}")
        except Exception as e:
            print(f"  {svc['emoji']} {svc['name']:8s} :{svc['port']}  🔴 离线 ({e})")


def main():
    parser = argparse.ArgumentParser(description="🐉 龍魂统一引擎启动器")
    parser.add_argument("--feishu", action="store_true", help="启动飞书通道")
    parser.add_argument("--wechat", action="store_true", help="启动微信通道")
    parser.add_argument("--web", action="store_true", help="启动Web通道")
    parser.add_argument("--ant-colony", "--ant", action="store_true", help="启动蚁群守护")
    parser.add_argument("--all", action="store_true", help="启动所有通道")
    parser.add_argument("--cli", action="store_true", help="交互式CLI模式")
    parser.add_argument("--health", action="store_true", help="健康检查")
    parser.add_argument("--port", type=int, help="指定Web通道端口")
    parser.add_argument("--list-tools", action="store_true", help="列出所有视频/音频工具")

    # 子命令: video <tool>
    sub = parser.add_subparsers(dest="command")
    video_sub = sub.add_parser("video", help="视频引擎工具")
    video_sub.add_argument("tool", choices=list(VIDEO_ENGINES.keys()), help="视频工具名")
    video_sub.add_argument("--prompt", help="生成提示词")
    video_sub.add_argument("--input", help="输入路径")
    video_sub.add_argument("--dna", help="DNA追溯码")
    video_sub.add_argument("--output", help="输出路径")
    video_sub.add_argument("--audit", action="store_true", help="启用审计")
    video_sub.add_argument("--method", choices=["dct","lsb","dwt"], help="水印方法")
    video_sub.add_argument("--strength", type=int, help="嵌入强度")

    audio_sub = sub.add_parser("audio", help="语音引擎工具")
    audio_sub.add_argument("tool", choices=list(AUDIO_ENGINES.keys()), help="语音工具名")
    audio_sub.add_argument("--text", help="输入文本")
    audio_sub.add_argument("--input", help="输入音频路径")
    audio_sub.add_argument("--dna", help="DNA追溯码")
    audio_sub.add_argument("--output", help="输出路径")
    audio_sub.add_argument("--voice", help="TTS音色")
    audio_sub.add_argument("--lang", default="zh", help="语言")
    audio_sub.add_argument("--model", help="LLM后端")
    audio_sub.add_argument("--sample", help="样本音频")
    audio_sub.add_argument("--target", help="目标文本")
    audio_sub.add_argument("--auth", help="DNA授权码")

    search_sub = sub.add_parser("search", help="全球搜索引擎")
    search_sub.add_argument("tool", choices=list(SEARCH_ENGINES.keys()), help="搜索工具名")
    search_sub.add_argument("--query", help="搜索关键词")
    search_sub.add_argument("--persona", choices=["military","history","philosophy","economy","political"], help="人格模式")
    search_sub.add_argument("--top-k", type=int, default=10, help="返回结果数")

    cnsh_sub = sub.add_parser("cnsh", help="CNSH编译/运行工具")
    cnsh_sub.add_argument("tool", choices=list(CNSH_ENGINES.keys()), help="CNSH工具名")
    cnsh_sub.add_argument("--input", help="输入文件路径")
    cnsh_sub.add_argument("--lang", help="目标语言")
    cnsh_sub.add_argument("--output", help="输出路径")
    cnsh_sub.add_argument("--target", help="输出目标语言")
    cnsh_sub.add_argument("--cnsh-file", help="CNSH脚本文件")

    args = parser.parse_args()

    if args.command == "video":
        run_video_tool(args.tool, args)
        return
    if args.command == "audio":
        run_audio_tool(args.tool, args)
        return
    if args.command == "search":
        run_search_tool(args.tool, args)
        return
    if args.command == "cnsh":
        run_cnsh_tool(args.tool, args)
        return

    if args.port:
        os.environ["WEB_BOT_PORT"] = str(args.port)

    # 确定启动哪些
    active = []
    if args.feishu:
        active.append("feishu")
    if args.wechat:
        active.append("wechat")
    if args.web:
        active.append("web")
    if args.ant_colony:
        active.append("ant_colony")
    if args.all:
        active = ["feishu", "wechat", "web", "ant_colony"]
    
    # 默认启动 Web
    if not active and not args.cli and not args.health:
        active = ["web"]

    if args.health:
        run_health()
        return

    if args.list_tools:
        list_video_audio_tools()
        return

    if args.cli:
        run_cli()
        return

    print_banner(active)
    start_services(active)


if __name__ == "__main__":
    main()
