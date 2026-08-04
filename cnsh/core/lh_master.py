#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂系统总控制台
DNA: #龍芯⚡️2026-06-29-LONGHUN-MASTER-v1.0

用法（CNSH 风格子命令）：
    python3 longhun_master.py 状态                  # 看所有模块运行状态
    python3 longhun_master.py 启动 全部              # 尝试启动所有未运行模块
    python3 longhun_master.py 停止 心谈             # 停止指定模块
    python3 longhun_master.py 重启 审计             # 重启指定模块
    python3 longhun_master.py 技能                  # 列出所有技能
    python3 longhun_master.py 端口检查              # 检查端口冲突
    python3 longhun_master.py 字体路径              # 显示统一字体位置
    python3 longhun_master.py 复活                  # 启动所有未运行且无冲突的守护进程
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any

from cnsh_unified import 三色审计, 系统路径, DNA工具


INVENTORY_DIR = 系统路径.工作数据目录()
SKILLS_FILE = INVENTORY_DIR / "inventory_skills.json"
MODULES_FILE = INVENTORY_DIR / "inventory_modules.json"
NAMING_FILE = INVENTORY_DIR / "inventory_naming_issues.json"
FONTS_FILE = INVENTORY_DIR / "inventory_fonts.json"


class 控制台:
    def __init__(self):
        self.技能清单 = self._读_json(SKILLS_FILE, {"skills": []})["skills"]
        self.模块清单 = self._读_json(MODULES_FILE, {"modules": []})["modules"]
        self.命名问题 = self._读_json(NAMING_FILE, {"issues": []})["issues"]
        字体数据 = self._读_json(FONTS_FILE, [])
        self.字体清单 = 字体数据 if isinstance(字体数据, list) else 字体数据.get("fonts", [])

    @staticmethod
    def _读_json(路径: Path, 默认值: dict[str, Any]) -> dict[str, Any]:
        if not 路径.exists():
            return 默认值
        try:
            return json.loads(路径.read_text(encoding="utf-8"))
        except Exception:
            return 默认值

    @staticmethod
    def _执行(cmd: List[str]) -> tuple[Any, ...]:
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return r.returncode, r.stdout, r.stderr
        except Exception as e:
            return -1, "", str(e)

    def 状态(self):
        print("\n🐉 龍魂系统模块状态\n")
        运行中 = [m for m in self.模块清单 if m.get("running") == "yes"]
        未运行 = [m for m in self.模块清单 if m.get("running") != "yes"]
        print(f"运行中: {len(运行中)} / 总数: {len(self.模块清单)}\n")
        for m in 运行中:
            port = f" :{m.get('port')}" if m.get("port") else ""
            print(f"  🟢 {m['name']}{port}  {m.get('description', '')}")
        print()
        for m in 未运行[:20]:
            print(f"  ⚪ {m['name']}  {m.get('description', '')}")
        if len(未运行) > 20:
            print(f"  ... 还有 {len(未运行) - 20} 个未运行模块")
        print()

    def 技能列表(self):
        print("\n📚 龍魂技能清单\n")
        print(f"总数: {len(self.技能清单)}\n")
        按来源: Dict[str, List[dict]] = {}
        for s in self.技能清单:
            按来源.setdefault(s.get("scope", "other"), []).append(s)
        for 来源, 技能们 in 按来源.items():
            print(f"【{来源}】{len(技能们)} 个")
            for s in 技能们[:5]:
                dna = s.get("dna", "")
                print(f"  • {s['name']}  {dna}")
            if len(技能们) > 5:
                print(f"  ... 还有 {len(技能们) - 5} 个")
            print()

    def 端口检查(self):
        print("\n🔌 端口占用检查\n")
        端口模块: Dict[str, List[dict]] = {}
        for m in self.模块清单:
            p = m.get("port")
            if p:
                端口模块.setdefault(str(p), []).append(m)
        有冲突 = False
        for port, mods in sorted(端口模块.items(), key=lambda x: int(x[0])):
            color = "🟢" if len(mods) == 1 else "🔴"
            print(f"  {color} 端口 {port}: {len(mods)} 个模块")
            for m in mods:
                print(f"      {m['name']} ({m.get('running', 'unknown')})")
            if len(mods) > 1:
                有冲突 = True
        if 有冲突:
            print("\n⚠️ 发现端口冲突，需要手动调整配置。")
        else:
            print("\n✅ 暂无端口冲突。")
        print()

    def 字体路径(self):
        print("\n🖋 统一字体位置\n")
        # 主字体工程
        主目录 = 系统路径.龍魂系统根目录() / "longhun-font"
        print(f"主字体工程: {主目录}")
        print(f"  存在: {'✅' if 主目录.exists() else '❌'}")

        # 找 Regular otf/ttf
        candidates = [f for f in self.字体清单 if f.get("type") in ("otf", "ttf") and "Regular" in f.get("name", "")]
        print(f"\n候选常规字体: {len(candidates)} 个")
        for c in candidates[:5]:
            print(f"  • {c['path']} ({c.get('size', '?')} bytes)")

        # 创建/检查统一符号链接
        统一字体目录 = 系统路径.龍魂系统根目录() / "字体"
        if not 统一字体目录.exists():
            try:
                统一字体目录.symlink_to(主目录, target_is_directory=True)
                print(f"\n✅ 已创建统一字体入口: {统一字体目录} -> {主目录}")
            except Exception as e:
                print(f"\n⚠️ 创建符号链接失败: {e}")
        else:
            print(f"\n✅ 统一字体入口已存在: {统一字体目录}")
        print()

    def 启动(self, 目标: str):
        if 目标 == "全部":
            self._批量启动([m for m in self.模块清单 if m.get("running") != "yes"])
        else:
            self._操作模块(目标, "start")

    def 停止(self, 目标: str):
        self._操作模块(目标, "stop")

    def 重启(self, 目标: str):
        self._操作模块(目标, "restart")

    def 复活(self):
        print("\n🛠 龍魂复活模式：启动所有未运行且无端口冲突的守护进程\n")
        # 先检查端口冲突，排除冲突端口上的模块
        冲突端口 = set()
        端口模块: Dict[str, List[dict]] = {}
        for m in self.模块清单:
            p = m.get("port")
            if p:
                端口模块.setdefault(str(p), []).append(m)
        for port, mods in 端口模块.items():
            if len(mods) > 1:
                冲突端口.add(port)
                print(f"⚠️ 端口 {port} 冲突，跳过这些模块: {[m['name'] for m in mods]}")

        待启动 = []
        for m in self.模块清单:
            if m.get("running") == "yes":
                continue
            if m.get("port") in 冲突端口:
                continue
            标签 = self._提取_launchctl_label(m.get("description", ""))
            if 标签 or m.get("type") == "daemon":
                待启动.append(m)
        self._批量启动(待启动)

    def _提取_launchctl_label(self, desc: str) -> Optional[str]:
        import re
        m = re.search(r"launchctl\s+([\w.-]+)", desc)
        if m:
            return m.group(1)
        return None

    def _操作模块(self, 目标: str, 动作: str):
        匹配 = [m for m in self.模块清单 if 目标.lower() in m["name"].lower()]
        if not 匹配:
            print(f"❌ 找不到模块: {目标}")
            return
        for m in 匹配[:1]:  # 只操作第一个精确/最近匹配
            标签 = self._提取_launchctl_label(m.get("description", ""))
            if 标签:
                cmd = ["launchctl", 动作, f"~/Library/LaunchAgents/{标签}.plist"]
                # launchctl start/stop 不需要 plist 路径，直接用 label
                cmd = ["launchctl", 动作, 标签]
                rc, out, err = self._执行(cmd)
                print(f"{'✅' if rc == 0 else '❌'} {动作} {m['name']} ({标签})")
                if err and rc != 0:
                    print(f"   {err.strip()}")
            else:
                print(f"⚠️ {m['name']} 没有 launchctl 标签，无法 {动作}")

    def _批量启动(self, 模块们: List[dict]):
        成功 = 0
        失败 = 0
        日志目录 = Path.home() / ".龍魂" / "revive_logs"
        日志目录.mkdir(parents=True, exist_ok=True)
        for m in 模块们:
            标签 = self._提取_launchctl_label(m.get("description", ""))
            if 标签:
                rc, out, err = self._执行(["launchctl", "start", 标签])
                if rc == 0:
                    print(f"🟢 启动 {m['name']} ({标签})")
                    成功 += 1
                else:
                    print(f"🔴 启动失败 {m['name']} ({标签}): {err.strip()}")
                    失败 += 1
                continue

            # 没有 launchctl 标签，尝试直接运行脚本
            路径 = Path(m.get("path", ""))
            if 路径.exists() and 路径.suffix == ".py":
                log = 日志目录 / f"{m['name']}.log"
                try:
                    import subprocess as sp
                    with open(log, "a", encoding="utf-8") as lf:
                        proc = sp.Popen(
                            [sys.executable, str(路径)],
                            stdout=lf,
                            stderr=lf,
                            start_new_session=True,
                            cwd=str(路径.parent),
                        )
                    print(f"🟢 启动 {m['name']} (PID {proc.pid}, 日志 {log})")
                    成功 += 1
                except Exception as e:
                    print(f"🔴 启动失败 {m['name']}: {e}")
                    失败 += 1
            else:
                print(f"⚪ 跳过 {m['name']}：没有 launchctl 标签且找不到可执行脚本")
        print(f"\n结果: 成功 {成功}，失败 {失败}")

    def 命名问题报告(self):
        print("\n📋 CNSH 命名不一致问题（前 10 条）\n")
        for issue in self.命名问题[:10]:
            print(f"【{issue['issue_type']}】{issue['concept']}")
            print(f"  建议统一为: {issue.get('suggested_cnsh_name', '')}")
            for ex in issue.get("examples", [])[:3]:
                print(f"    • {ex}")
            print()


def 主函数():
    parser = argparse.ArgumentParser(description="龍魂系统总控制台")
    subparsers = parser.add_subparsers(dest="命令")

    subparsers.add_parser("状态", help="查看模块运行状态")
    subparsers.add_parser("技能", help="列出所有技能")
    subparsers.add_parser("端口检查", help="检查端口冲突")
    subparsers.add_parser("字体路径", help="显示并创建统一字体入口")
    subparsers.add_parser("命名问题", help="显示命名不一致问题")
    subparsers.add_parser("复活", help="启动未运行且无冲突的守护进程")

    p_start = subparsers.add_parser("启动", help="启动模块")
    p_start.add_argument("目标", help="模块名或'全部'")

    p_stop = subparsers.add_parser("停止", help="停止模块")
    p_stop.add_argument("目标", help="模块名")

    p_restart = subparsers.add_parser("重启", help="重启模块")
    p_restart.add_argument("目标", help="模块名")

    args = parser.parse_args()
    if not args.命令:
        parser.print_help()
        return

    c = 控制台()
    if args.命令 == "状态":
        c.状态()
    elif args.命令 == "技能":
        c.技能列表()
    elif args.命令 == "端口检查":
        c.端口检查()
    elif args.命令 == "字体路径":
        c.字体路径()
    elif args.命令 == "命名问题":
        c.命名问题报告()
    elif args.命令 == "复活":
        c.复活()
    elif args.命令 == "启动":
        c.启动(args.目标)
    elif args.命令 == "停止":
        c.停止(args.目标)
    elif args.命令 == "重启":
        c.重启(args.目标)


if __name__ == "__main__":
    主函数()
