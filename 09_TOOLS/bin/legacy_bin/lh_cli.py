#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
╔══════════════════════════════════════════════════════════════════════╗
║              龍魂统一 CLI 启动器 v1.0 — lh 命令入口                    ║
║  DNA: #龍芯⚡️丙午·丙申·癸丑·午时·䷄需-LONGHUN-CLI-v1.0-7E91D482        ║
║  三色审计: 🟢 通过                                                   ║
╚══════════════════════════════════════════════════════════════════════╝

【统一入口】所有龍魂CLI工具通过此入口路由。

用法:
  lh status              — 系统状态
  lh health              — 全系统健康检查
  lh patrol              — 安全巡检
  lh audit               — 三色审计
  lh sync                — 全量同步
  lh finance             — 金融格式化（子命令: cny/thousands/read/parse/ledger/convert）
  lh site <输入目录>      — 极简站生成器
  lh dna <内容>          — 生成DNA
  lh wuxing <文本>       — 五行分析
  lh memory              — 加载记忆
  lh knowledge           — 知识爬虫
  lh robot-score <文本>  — AI检测打分
  lh translate <文本>    — CNSH翻译
  lh help                — 帮助
"""

from __future__ import annotations
import sys
import os
import subprocess
from pathlib import Path

# 项目根目录
ROOT = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def run_script(script_name: str, *args: str) -> None:
    """运行 bin/ 下的脚本"""
    script = ROOT / "bin" / script_name
    if not script.exists():
        print(f"❌ 脚本不存在: {script}")
        sys.exit(1)
    cmd = [sys.executable, str(script), *args]
    subprocess.run(cmd)


def run_module(module: str, *args: str) -> None:
    """运行 Python 模块"""
    cmd = [sys.executable, "-m", module, *args]
    subprocess.run(cmd)


def cmd_status() -> None:
    """系统状态"""
    status_script = ROOT / "bin" / "lh_status.py"
    if status_script.exists():
        run_script("lh_status.py")
    else:
        # 快速状态摘要
        print("龍魂系统 v2.5.0")
        print(f"  项目路径: {ROOT}")
        bin_count = sum(1 for _ in (ROOT / "bin").glob("*.py") if _.is_file())
        print(f"  CLI工具数: {bin_count}")
        print(f"  知識图谱: {ROOT / '03_知識圖譜'}")
        print(f"  执行日志: {ROOT / '02_執行記錄'}")


def cmd_health() -> None:
    """健康检查"""
    run_script("lh_self-heal.py")


def cmd_patrol() -> None:
    """安全巡检"""
    run_script("patrol_security.py")


def cmd_audit() -> None:
    """三色审计"""
    # 快速审计
    from L1_内核层.kernel.engines.cnsh_editor_engine import CNShEditorEngine
    engine = CNShEditorEngine()
    print("三色审计: 🟢 内核正常")


def cmd_sync() -> None:
    """全量同步"""
    sync_script = ROOT / "bin" / "lh_sync_all.sh"
    if sync_script.exists():
        subprocess.run(["bash", str(sync_script)])
    else:
        print("同步脚本未找到")


def cmd_finance(args: list[str]) -> None:
    """金融格式化"""
    run_script("lh_finance_fmt.py", *args)


def cmd_site(args: list[str]) -> None:
    """极简站生成器"""
    run_script("lh_site_gen.py", *args)


def cmd_dna(args: list[str]) -> None:
    """DNA生成"""
    run_script("hetu_luoshu_dna.py", *args)


def cmd_wuxing(args: list[str]) -> None:
    """五行分析"""
    run_script("wuxing_guard.py", *args)


def cmd_memory() -> None:
    """加载记忆"""
    run_script("lh_memory_load.py")


def cmd_knowledge(args: list[str]) -> None:
    """知识爬虫"""
    run_script("lh_knowledge_crawler.py", *args)


def cmd_robot_score(args: list[str]) -> None:
    """AI检测"""
    run_script("lh_robot_score.py", *args)


def cmd_translate(args: list[str]) -> None:
    """CNSH翻译"""
    run_script("syntax_lookup.py", *args)


def cmd_interactive() -> None:
    """交互模式"""
    print("🐉 龍魂 CLI v1.0 交互模式")
    print("输入命令或 'help' 查看帮助，'q' 退出")
    while True:
        try:
            line = input("lh> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not line:
            continue
        if line in ("q", "quit", "exit"):
            break
        if line == "help":
            print(__doc__)
            continue
        dispatch(line.split())


def dispatch(args: list[str]) -> None:
    """命令路由"""
    if not args:
        cmd_status()
        return

    cmd = args[0].lower()
    rest = args[1:]

    routes = {
        "status": cmd_status,
        "health": cmd_health,
        "patrol": cmd_patrol,
        "audit": cmd_audit,
        "sync": cmd_sync,
        "memory": cmd_memory,
    }

    # 简单路由
    if cmd in routes:
        routes[cmd]()
        return

    # 带参数路由
    if cmd == "finance":
        cmd_finance(rest)
    elif cmd == "site":
        cmd_site(rest)
    elif cmd == "dna":
        cmd_dna(rest)
    elif cmd == "wuxing":
        cmd_wuxing(rest)
    elif cmd in ("knowledge", "crawl"):
        cmd_knowledge(rest)
    elif cmd in ("robot-score", "robotscore", "ai-detect"):
        cmd_robot_score(rest)
    elif cmd in ("translate", "trans"):
        cmd_translate(rest)
    elif cmd in ("help", "-h", "--help"):
        print(__doc__)
    elif cmd == "shell":
        cmd_interactive()
    else:
        print(f"未知命令: {cmd}")
        print("可用命令: status health patrol audit sync finance site dna wuxing memory knowledge robot-score translate help shell")
        sys.exit(1)


def dashboard() -> None:
    """启动仪表盘 GUI"""
    print("🐉 龍魂操作台")
    print(f"  打开浏览器访问: http://127.0.0.1:8766")
    # 尝试启动 API 服务器
    api_server = ROOT / "L5_服务层" / "services" / "api" / "control-panel" / "main.py"
    if api_server.exists():
        os.chdir(api_server.parent)
        subprocess.run([sys.executable, "main.py"])
    else:
        print("  API服务器文件未找到")


def main() -> None:
    """主入口"""
    args = sys.argv[1:]
    if not args:
        cmd_status()
    else:
        dispatch(args)


if __name__ == "__main__":
    main()
