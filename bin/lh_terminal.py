#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
#龍芯⚡️2026-06-24-LONGHUN-TERMINAL-FILE1-v2.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-

# DNA:#龍芯⚡️2026-06-24-LONGHUN-TERMINAL-FILE1-v2.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

"""
龍魂终端统一入口 · LongHun Terminal v2.0

合并功能：
- longhun-check  系统体检
- cd-lh          进入龍魂根目录（由 shell function 实现）
- lh             龍魂指挥台
- 中文命令注册表：把散落的中文终端命令统一纳管

用法:
    lh                          # 显示指挥台 + 三色状态
    lh 状态                      # 系统状态
    lh 启动                      # 启动服务
    lh 人格                      # 启动人格 API
    lh 技能                      # 启动技能工具
    lh cnsh FILE.cnsh            # 运行 CNSH 脚本
    lh 签名                      # 签名保护
    lh 审计                      # 自检审计
    lh 命令                      # 列出所有命令
"""

import os
import sys
import json
import argparse
import subprocess
import webbrowser
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any


class 龍魂终端:
    DNA = "#龍芯⚡️2026-06-24-LONGHUN-TERMINAL-v2.0"

    def __init__(self):
        self.root = Path(__file__).resolve().parent.parent
        self.registry = self._加载注册表()
        self.ops_console = self.root / "ops-console" / "index.html"
        self.portal_url = "https://longhun888.com/"

    def _加载注册表(self) -> Dict[str, Any]:
        path = self.root / "bin" / "longhun-command-registry.json"
        if not path.exists():
            return {"commands": {}}
        return json.loads(path.read_text(encoding="utf-8"))

    def _查找命令(self, name: str) -> Optional[Dict[str, Any]]:
        commands = self.registry.get("commands", {})
        # 直接匹配中文名
        if name in commands:
            return {**commands[name], "_name": name}
        # 匹配别名
        for cmd_name, info in commands.items():
            if name in info.get("aliases", []):
                return {**info, "_name": cmd_name}
        return None

    def _resolve_path(self, script: str) -> Path:
        if script.startswith("~/"):
            return Path.home() / script[2:]
        return self.root / script

    def _run_script(self, script: str, args: List[str]):
        path = self._resolve_path(script)
        if not path.exists():
            print(f"❌ 脚本未找到: {path}")
            return 1
        # 根据扩展名选择解释器，确保 .py/.sh 都能直接跑
        if str(path).endswith('.py'):
            cmd = [sys.executable, str(path)] + args
        elif str(path).endswith('.sh'):
            cmd = ['bash', str(path)] + args
        else:
            cmd = [str(path)] + args
        try:
            return subprocess.call(cmd, cwd=str(self.root))
        except Exception as e:
            print(f"❌ 运行失败: {e}")
            return 1

    def _run_py(self, script: str, *args) -> str:
        path = self.root / script
        if not path.exists():
            return f"[未找到: {path}]"
        try:
            result = subprocess.run(
                [sys.executable, str(path), *args],
                cwd=str(self.root),
                capture_output=True,
                text=True,
                timeout=60,
            )
            return result.stdout or result.stderr
        except Exception as e:
            return f"[运行错误: {e}]"

    def _color(self, code: str) -> str:
        return f"\033[{code}m"

    def 欢迎板(self):
        C = {
            "cyan": self._color("0;36"),
            "green": self._color("0;32"),
            "yellow": self._color("1;33"),
            "magenta": self._color("0;35"),
            "blue": self._color("0;34"),
            "red": self._color("0;31"),
            "nc": self._color("0"),
        }
        pwd = os.getcwd().replace(str(Path.home()), "~")[:45]
        padding = " " * (46 - len(pwd))
        user = os.environ.get("USER", "unknown")
        print("")
        print(f"{C['cyan']}╔═══════════════════════════════════════════════════════╗{C['nc']}")
        print(f"{C['cyan']}║{C['nc']}  {C['green']}🐉 龍魂终端 v2.0 · UID9622{C['nc']}                        {C['cyan']}║{C['nc']}")
        print(f"{C['cyan']}╠═══════════════════════════════════════════════════════╣{C['nc']}")
        print(f"{C['cyan']}║{C['nc']}  {C['yellow']}📅{C['nc']} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  {C['yellow']}👤{C['nc']}{user}          {C['cyan']}║{C['nc']}")
        print(f"{C['cyan']}║{C['nc']}  {C['yellow']}📍{C['nc']} {pwd}{padding}{C['cyan']}║{C['nc']}")
        print(f"{C['cyan']}╠═══════════════════════════════════════════════════════╣{C['nc']}")
        print(f"{C['cyan']}║{C['nc']}  {C['magenta']}💡 快捷指令:{C['nc']}  lh | longhun-check | cd-lh            {C['cyan']}║{C['nc']}")
        print(f"{C['cyan']}║{C['nc']}  {C['magenta']}🍱 记不住命令:{C['nc']} lh --menu 或 lh 菜单（数字选）     {C['cyan']}║{C['nc']}")
        print(f"{C['cyan']}║{C['nc']}  {C['magenta']}🔧 常用命令:{C['nc']}  状态 启动 停止 技能主控 自动化状态  {C['cyan']}║{C['nc']}")
        print(f"{C['cyan']}║{C['nc']}            人格 审计 签名 万年历 每日复盘 操作台  {C['cyan']}║{C['nc']}")
        print(f"{C['cyan']}╚═══════════════════════════════════════════════════════╝{C['nc']}")
        print("")

    def 系统体检(self):
        C = {
            "cyan": self._color("0;36"),
            "green": self._color("0;32"),
            "red": self._color("0;31"),
            "yellow": self._color("1;33"),
            "nc": self._color("0"),
        }
        print(f"{C['cyan']}━━━━━━━━━━━━━━ 龍魂系统体检 ━━━━━━━━━━━━━━{C['nc']}")
        print(f"{C['cyan']}⏰{C['nc']} 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{C['cyan']}📁{C['nc']} 系统根: {self.root}")

        if self.root.exists():
            print(f"{C['green']}✅{C['nc']} 龍魂系统已部署")
            head = self.root / ".git" / "HEAD"
            if head.exists():
                try:
                    commit = subprocess.check_output(
                        ["git", "rev-parse", "--short", "HEAD"],
                        cwd=str(self.root),
                        text=True,
                    ).strip()
                    print(f"{C['green']}✅{C['nc']} Git HEAD: {commit}")
                except Exception:
                    print(f"{C['yellow']}⚠️{C['nc']} 无法读取 Git HEAD")
            core_files = [
                "longhun_persona_hub.py",
                "personas/runtime/system_status_panel.py",
                "personas/runtime/compression_engine.py",
                "personas/runtime/dna_tracer.py",
                "bin/longhun-command-registry.json",
            ]
            missing = [f for f in core_files if not (self.root / f).exists()]
            if missing:
                print(f"{C['red']}❌{C['nc']} 缺失核心文件: {', '.join(missing)}")
            else:
                print(f"{C['green']}✅{C['nc']} 核心模块齐全")
            try:
                remotes = subprocess.check_output(
                    ["git", "remote", "-v"], cwd=str(self.root), text=True
                ).strip()
                print(f"{C['green']}✅{C['nc']} 已配置远程:")
                for line in remotes.splitlines():
                    print(f"      {line}")
            except Exception:
                pass
        else:
            print(f"{C['red']}❌{C['nc']} 龍魂系统未找到")
        print(f"{C['cyan']}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{C['nc']}")

    def 状态面板(self):
        return self._run_py("personas/runtime/system_status_panel.py")

    def 人格内阁(self):
        return self._run_py("longhun_persona_hub.py", "--list")

    def 当前卦象(self):
        return self._run_py("longhun_persona_hub.py", "--hexagram")

    def 压缩测试(self, file_path: str):
        target = Path(file_path)
        if not target.is_absolute():
            target = Path(os.getcwd()) / file_path
        return self._run_py("personas/runtime/compression_engine.py", "benchmark", str(target))

    def DNA溯源(self, module: str):
        return self._run_py("personas/runtime/dna_tracer.py", "--module", module)

    def 操作台入口(self):
        print("🐉 龍魂操作台入口")
        print(f"   本地 OPS: file://{self.ops_console}")
        print(f"   数字门户: {self.portal_url}")
        print(f"   GitHub:   https://github.com/UID9622/longhun-system")
        print(f"   Gitee:    https://gitee.com/uid9622_admin/longhun-system-core")

    def 列出命令(self):
        print("\n📜 龍魂终端命令清单")
        print("=" * 60)
        commands = self.registry.get("commands", {})
        for name, info in commands.items():
            aliases = ", ".join(info.get("aliases", []))
            cat = info.get("category", "其他")
            print(f"  {name:12s} [{cat:6s}] [{aliases:20s}] {info.get('desc', '')}")
        print("=" * 60)
        print("\n💡 示例:")
        print("  lh 状态")
        print("  lh 人格")
        print("  lh 技能")
        print("  lh cnsh hello.cnsh")
        print("  lh 追溯 longhun_persona_hub")
        print("  lh 分类 启动")
        print("")

    def 分类列表(self, category: Optional[str] = None):
        commands = self.registry.get("commands", {})
        by_cat: Dict[str, List[Tuple[str, Dict]]] = {}
        for name, info in commands.items():
            cat = info.get("category", "其他")
            by_cat.setdefault(cat, []).append((name, info))
        if category:
            print(f"\n📂 分类: {category}")
            print("-" * 60)
            for name, info in by_cat.get(category, []):
                aliases = ", ".join(info.get("aliases", []))
                print(f"  {name:12s} [{aliases:20s}] {info.get('desc', '')}")
        else:
            print("\n📂 命令分类")
            print("=" * 60)
            for cat, items in sorted(by_cat.items()):
                print(f"\n【{cat}】({len(items)} 个)")
                for name, info in items:
                    aliases = ", ".join(info.get("aliases", []))
                    print(f"  {name:12s} [{aliases:20s}] {info.get('desc', '')}")
        print("")

    def 交互菜单(self):
        """交互式数字菜单：适合记不住命令的老大"""
        C = {
            "cyan": self._color("0;36"),
            "green": self._color("0;32"),
            "yellow": self._color("1;33"),
            "blue": self._color("0;34"),
            "nc": self._color("0"),
        }
        commands = self.registry.get("commands", {})
        # 只展示常用分类，按推荐顺序
        priority = ["启动", "状态", "技能", "自动化", "记忆", "同步", "审计", "备份", "部署", "安全", "cnsh", "文档", "签名", "维护", "人格", "反熔断", "其他"]
        by_cat: Dict[str, List[Tuple[str, Dict]]] = {}
        for name, info in commands.items():
            cat = info.get("category", "其他")
            by_cat.setdefault(cat, []).append((name, info))

        while True:
            print(f"\n{C['cyan']}╔═══════════════════════════════════════════════════════╗{C['nc']}")
            print(f"{C['cyan']}║{C['nc']}  {C['green']}🐉 龍魂交互菜单 · 输入编号执行{C['nc']}                     {C['cyan']}║{C['nc']}")
            print(f"{C['cyan']}╠═══════════════════════════════════════════════════════╣{C['nc']}")
            idx = 1
            index_map = {}
            for cat in priority:
                items = by_cat.get(cat, [])
                if not items:
                    continue
                print(f"{C['cyan']}║{C['nc']}  {C['yellow']}【{cat}】{C['nc']}")
                for name, info in sorted(items, key=lambda x: x[0]):
                    aliases = "/".join(info.get("aliases", [])[:2])
                    line = f"{idx:>2}. {name:<12s} {aliases:<16s} {info.get('desc', '')}"[:49]
                    print(f"{C['cyan']}║{C['nc']}  {C['blue']}{line}{C['nc']}")
                    index_map[str(idx)] = (name, info)
                    idx += 1
            print(f"{C['cyan']}║{C['nc']}  {C['yellow']} 0. 退出菜单{C['nc']}")
            print(f"{C['cyan']}╚═══════════════════════════════════════════════════════╝{C['nc']}")
            try:
                choice = input(f"{C['green']}>>> 请输入编号 (或直接输入命令):{C['nc']} ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n👋 退出菜单")
                return 0
            if choice == "0" or choice.lower() in ("q", "quit", "exit"):
                print("👋 退出菜单")
                return 0
            if choice in index_map:
                name, info = index_map[choice]
                print(f"\n🚀 执行: {name}")
                self.执行命令(name, [])
            elif choice:
                # 直接当命令跑
                parts = choice.split()
                self.执行命令(parts[0], parts[1:])
            else:
                continue

    def 执行命令(self, cmd_name: str, args: List[str]) -> int:
        info = self._查找命令(cmd_name)
        if not info:
            print(f"❌ 未知命令: {cmd_name}")
            print("   运行 `lh 命令` 查看可用命令")
            return 1

        cmd_type = info.get("type")

        if cmd_type == "help":
            self.列出命令()
            return 0

        if cmd_type == "list":
            self.列出命令()
            return 0

        if cmd_type == "category":
            self.分类列表(args[0] if args else None)
            return 0

        if cmd_type == "menu":
            return self.交互菜单()

        if cmd_type == "script":
            script = info.get("script", "")
            script_args = list(info.get("args", []))
            if info.get("need_arg") and args:
                script_args.append(args[0])
            elif args:
                script_args.extend(args)
            return self._run_script(script, script_args)

        if cmd_type == "open":
            target = info.get("target", "")
            if target.startswith("http"):
                webbrowser.open(target)
            else:
                full = self._resolve_path(target)
                if full.exists():
                    webbrowser.open(f"file://{full}")
                else:
                    print(f"❌ 目标不存在: {full}")
                    return 1
            return 0

        print(f"❌ 未支持的命令类型: {cmd_type}")
        return 1

    def 运行(self, argv=None):
        if argv is None:
            argv = sys.argv[1:]

        if not argv:
            self.欢迎板()
            print(self.状态面板())
            print("\n💡 提示: 输入 `lh --menu` 或 `lh 菜单` 进入交互式数字菜单")
            # 启动精神燃料
            fuel_script = Path.home() / '.龍魂' / 'victory_lookbacks' / 'startup_fuel.py'
            if fuel_script.exists():
                try:
                    result = subprocess.run([sys.executable, str(fuel_script)], capture_output=True, text=True, timeout=10)
                    if result.stdout:
                        print(result.stdout.rstrip())
                except Exception:
                    pass
            return 0

        # 交互菜单入口
        if argv[0] in ("--menu", "-m", "menu"):
            self.欢迎板()
            return self.交互菜单()

        # 注册表命令优先（支持双字中文命令，如 人格 列表 / 能力 状态）
        if len(argv) >= 2:
            combined = argv[0] + argv[1]
            if self._查找命令(combined):
                return self.执行命令(combined, argv[2:])

        if self._查找命令(argv[0]):
            return self.执行命令(argv[0], argv[1:])

        # 内建英文子命令（兼容旧版）
        legacy_map = {
            "dashboard": self._legacy_dashboard,
            "status": self._legacy_status,
            "check": self._legacy_check,
            "hexagram": self._legacy_hexagram,
            "compress": self._legacy_compress,
            "trace": self._legacy_trace,
            "ops": self._legacy_ops,
            "help": self._legacy_help,
            "voice": self._legacy_voice,
            "sovereign": self._legacy_sovereign,
        }
        if argv[0] in legacy_map:
            return legacy_map[argv[0]](argv[1:])

        print(f"❌ 未知命令: {argv[0]}")
        print("   运行 `lh 命令` 查看可用命令")
        return 1

    # ---- 兼容旧子命令 ----
    def _legacy_dashboard(self, args):
        self.欢迎板()
        print(self.状态面板())
        return 0

    def _legacy_status(self, args):
        print(self.状态面板())
        return 0

    def _legacy_check(self, args):
        self.系统体检()
        return 0

    def _legacy_persona(self, args):
        print(self.人格内阁())
        return 0

    def _legacy_hexagram(self, args):
        print(self.当前卦象())
        return 0

    def _legacy_compress(self, args):
        if not args:
            print("用法: lh compress <file>")
            return 1
        print(self.压缩测试(args[0]))
        return 0

    def _legacy_trace(self, args):
        if not args:
            print("用法: lh trace <module>")
            return 1
        print(self.DNA溯源(args[0]))
        return 0

    def _legacy_ops(self, args):
        self.操作台入口()
        return 0

    def _legacy_help(self, args):
        self.列出命令()
        return 0

    def _legacy_voice(self, args):
        """龍魂声纹 DNA 锚定链入口。"""
        script = self.root / "voice-dna" / "cli.py"
        if not script.exists():
            print("❌ 声纹 DNA 锚定链模块未找到: {script}")
            return 1
        try:
            return subprocess.call([sys.executable, str(script)] + args, cwd=str(self.root))
        except Exception as e:
            print(f"❌ 声纹模块运行失败: {e}")
            return 1

    def _legacy_sovereign(self, args):
        """龍魂 UID9622 主权身份注册入口。"""
        script = self.root / "sovereign-registry" / "cli.py"
        if not script.exists():
            print("❌ 主权身份注册模块未找到: {script}")
            return 1
        try:
            return subprocess.call([sys.executable, str(script)] + args, cwd=str(self.root))
        except Exception as e:
            print(f"❌ 主权身份模块运行失败: {e}")
            return 1


def main():
    sys.exit(龍魂终端().运行())


if __name__ == "__main__":
    main()
