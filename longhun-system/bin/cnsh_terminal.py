#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 CNSH多语言编辑器终端 v5.1 · 龍魂整合版
融合：zsh配置 + CNSH终端 + 三色审计 + 熔断机制 + 自动摄入

DNA: #龍芯⚡️2026-04-04-CNSH-TERMINAL-v5.1
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F1E3B8A4C6D0F2E4A6B8C0D2E4F6A8B0C2
创建者: UID9622 诸葛鑫（龍芯北辰）
理论指导: 曾仕强老师（永恒显示）

保存为: ~/longhun-system/bin/cnsh_terminal.py
"""

import os
import sys
import subprocess
import readline
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field

# ============================================================
# 配置
# ============================================================

CNSH_HOME = Path.home() / ".cnsh"
CNSH_LOGS_DIR = CNSH_HOME / "logs"
CNSH_CACHE_DIR = CNSH_HOME / "cache"
CNSH_PLUGINS_DIR = CNSH_HOME / "plugins"

for d in [CNSH_HOME, CNSH_LOGS_DIR, CNSH_CACHE_DIR, CNSH_PLUGINS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# UID9622 身份信息
UID9622_USER = "龍芯北辰"
UID9622_GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F1E3B8A4C6D0F2E4A6B8C0D2E4F6A8B0C2"
UID9622_NETID = "T38C89R75U"
UID9622_CONFIRM_HASH = "8f3e2a1b9c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f"

# ============================================================
# 中文命令映射表
# ============================================================

CN_CMD_MAP = {
    # 基础操作
    "列表": "ls -la",
    "看": "cat",
    "进去": "cd",
    "跑": "python3",
    "装": "pip install",
    "删": "rm -i",
    "复制": "cp",
    "移动": "mv",
    "建目录": "mkdir -p",
    "清屏": "clear",
    "退出": "exit",
    
    # 系统信息
    "看进程": "ps aux",
    "看磁盘": "df -h",
    "看内存": "top -l 1 | head -10",
    "看系统": "uname -a",
    "看时间": "date",
    
    # CNSH专用
    "审计": "cnsh_audit",
    "状态": "cnsh_status",
    "熔断": "cnsh_fuse_status",
    "同步": "cnsh_sync",
    "备份": "cnsh_backup",
    "日志": "cnsh_logs",
    
    # 快捷操作
    "回家": "cd ~",
    "去龍魂": "cd ~/longhun-system",
    "去脚本": "cd ~/longhun-system/bin",
    "去配置": "cd ~/longhun-system/config",
}

# ============================================================
# 危险命令检测（熔断用）
# ============================================================

DANGEROUS_COMMANDS = [
    ("rm -rf /", "RED", "删除根目录"),
    ("rm -rf /*", "RED", "删除根目录"),
    ("mkfs", "RED", "格式化磁盘"),
    ("dd if=/dev/zero", "RED", "覆写磁盘"),
    ("chmod 777", "YELLOW", "权限过宽"),
    ("chmod -R 777", "RED", "递归权限过宽"),
    ("sudo rm", "YELLOW", "特权删除"),
    ("sudo chmod", "YELLOW", "特权改权限"),
    (":(){ :|:& };:", "RED", "fork炸弹"),
    ("curl.*|.*bash", "YELLOW", "管道执行"),
    ("wget.*|.*bash", "YELLOW", "管道执行"),
]

# ============================================================
# 三色审计结果
# ============================================================

@dataclass
class AuditResult:
    level: str  # 🟢 🟡 🔴
    command: str
    reason: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self):
        return {"level": self.level, "command": self.command, "reason": self.reason, "timestamp": self.timestamp}


class AuditLogger:
    """审计日志"""
    
    def __init__(self):
        self.log_file = CNSH_LOGS_DIR / "audit.log"
        self.red_count = 0
        self.yellow_count = 0
        self.green_count = 0
    
    def log(self, result: AuditResult):
        """记录审计结果"""
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(result.to_dict(), ensure_ascii=False) + "\n")
        
        if result.level == "🔴":
            self.red_count += 1
        elif result.level == "🟡":
            self.yellow_count += 1
        else:
            self.green_count += 1
    
    def get_stats(self):
        """获取统计"""
        return {
            "red": self.red_count,
            "yellow": self.yellow_count,
            "green": self.green_count,
            "total": self.red_count + self.yellow_count + self.green_count
        }
    
    def get_recent(self, n: int = 20):
        """获取最近n条记录"""
        if not self.log_file.exists():
            return []
        records = []
        with open(self.log_file, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    records.append(json.loads(line))
                except:
                    continue
        return records[-n:]


# ============================================================
# 熔断机制
# ============================================================

class FuseMechanism:
    """熔断机制"""
    
    def __init__(self):
        self.blown = False
        self.counter = 0
        self.threshold = 3
        self.reason = None
    
    def check(self, cmd: str) -> Tuple[bool, str]:
        """检查命令是否触发熔断"""
        if self.blown:
            return False, f"🔴 系统已熔断，操作被阻止: {cmd}\n   请执行 cnsh_fuse_reset 重置"
        
        # 检查危险命令
        for pattern, level, reason in DANGEROUS_COMMANDS:
            if re.search(pattern, cmd):
                if level == "RED":
                    self.trigger(f"检测到高危命令: {cmd} ({reason})")
                    return False, f"🔴 熔断触发: {reason}"
                elif level == "YELLOW":
                    self.counter += 1
                    print(f"🟡 警告: {reason}")
                    if self.counter >= self.threshold:
                        self.trigger(f"连续{self.threshold}次警告")
                        return False, f"🔴 熔断触发: 连续{self.threshold}次警告"
        
        return True, ""
    
    def trigger(self, reason: str):
        """触发熔断"""
        self.blown = True
        self.reason = reason
        self._log_fuse(reason)
        self._show_alert(reason)
    
    def reset(self, confirm_code: str) -> bool:
        """重置熔断（需要确认码）"""
        code_hash = hashlib.sha256(confirm_code.encode()).hexdigest()
        if code_hash != UID9622_CONFIRM_HASH:
            print("❌ 确认码错误，重置失败")
            return False
        
        self.blown = False
        self.counter = 0
        self.reason = None
        print("✅ 熔断已重置，系统恢复正常")
        return True
    
    def status(self) -> dict:
        """获取熔断状态"""
        return {
            "blown": self.blown,
            "counter": self.counter,
            "threshold": self.threshold,
            "reason": self.reason
        }
    
    def _log_fuse(self, reason: str):
        """记录熔断日志"""
        log_file = CNSH_LOGS_DIR / "fuse.log"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().isoformat()}] FUSE_TRIGGERED: {reason}\n")
    
    def _show_alert(self, reason: str):
        """显示熔断警报"""
        print("\n" + "=" * 60)
        print("🔴 熔断触发！系统进入保护模式")
        print(f"   原因: {reason}")
        print(f"   时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("   恢复: cnsh_fuse_reset")
        print("=" * 60 + "\n")


# ============================================================
# CNSH 终端主程序
# ============================================================

class CNSHTerminal:
    """CNSH多语言终端"""
    
    def __init__(self):
        self.audit_logger = AuditLogger()
        self.fuse = FuseMechanism()
        self.running = True
        self.current_dir = os.getcwd()
        
        # 命令历史
        self.history_file = CNSH_HOME / "history.txt"
        if self.history_file.exists():
            readline.read_history_file(str(self.history_file))
        readline.set_history_length(50000)
    
    def save_history(self):
        """保存命令历史"""
        readline.write_history_file(str(self.history_file))
    
    def translate_command(self, cmd: str) -> str:
        """翻译中文命令"""
        if not cmd.strip():
            return cmd
        
        parts = cmd.strip().split()
        if parts[0] in CN_CMD_MAP:
            en_cmd = CN_CMD_MAP[parts[0]]
            if len(parts) > 1:
                return en_cmd + " " + " ".join(parts[1:])
            return en_cmd
        return cmd
    
    def audit_command(self, cmd: str) -> AuditResult:
        """审计命令"""
        # 默认绿色
        level = "🟢"
        reason = "正常命令"
        
        # 检查危险模式
        for pattern, level_code, reason_text in DANGEROUS_COMMANDS:
            if re.search(pattern, cmd):
                level = "🔴" if level_code == "RED" else "🟡"
                reason = reason_text
                break
        
        result = AuditResult(level=level, command=cmd, reason=reason)
        self.audit_logger.log(result)
        return result
    
    def execute(self, cmd: str) -> int:
        """执行命令"""
        # 审计
        audit = self.audit_command(cmd)
        
        # 红色阻断
        if audit.level == "🔴":
            print(f"🔴 阻断: {audit.reason}")
            return 1
        
        # 黄色警告但继续
        if audit.level == "🟡":
            print(f"🟡 警告: {audit.reason}")
        
        # 执行
        try:
            if cmd.startswith("cd "):
                # cd命令特殊处理
                target = cmd[3:].strip()
                if target == "~":
                    target = str(Path.home())
                os.chdir(target)
                self.current_dir = os.getcwd()
                print(f"已进入: {self.current_dir}")
                return 0
            else:
                result = subprocess.run(cmd, shell=True, text=True)
                return result.returncode
        except Exception as e:
            print(f"❌ 执行失败: {e}")
            return 1
    
    def run(self):
        """运行终端"""
        self._show_welcome()
        
        while self.running:
            try:
                # 提示符
                prompt = f"🐉 [{self.current_dir}] > "
                raw_cmd = input(prompt).strip()
                
                if not raw_cmd:
                    continue
                
                # 退出命令
                if raw_cmd in ["exit", "quit", "退出"]:
                    self.running = False
                    break
                
                # 熔断检查
                ok, msg = self.fuse.check(raw_cmd)
                if not ok:
                    print(msg)
                    continue
                
                # 翻译中文命令
                en_cmd = self.translate_command(raw_cmd)
                
                # 执行
                self.execute(en_cmd)
                
            except KeyboardInterrupt:
                print("\n按 Ctrl+D 或输入 exit 退出")
            except EOFError:
                self.running = False
    
    def _show_welcome(self):
        """显示欢迎信息"""
        print("=" * 60)
        print("🐉 CNSH 多语言终端 v5.1 · 龍魂系统")
        print(f"   时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   用户: {UID9622_USER} (UID9622)")
        print("")
        print("   中文命令示例:")
        print("     列表         → ls -la")
        print("     看 file.txt → cat file.txt")
        print("     进去 dir     → cd dir")
        print("     跑 app.py    → python3 app.py")
        print("     状态         → 查看系统状态")
        print("     审计         → 查看审计报告")
        print("     熔断         → 查看熔断状态")
        print("")
        print("   输入 exit 退出")
        print("=" * 60)
        print("")


# ============================================================
# CNSH 工具函数（可直接调用）
# ============================================================

def cnsh_status():
    """显示CNSH状态"""
    print("=" * 50)
    print("🐉 CNSH 系统状态")
    print("=" * 50)
    print(f"   CNSH_HOME: {CNSH_HOME}")
    print(f"   审计日志: {CNSH_LOGS_DIR}/audit.log")
    print(f"   熔断日志: {CNSH_LOGS_DIR}/fuse.log")
    print(f"   命令历史: {CNSH_HOME}/history.txt")
    print("=" * 50)


def cnsh_audit_report():
    """显示审计报告"""
    audit = AuditLogger()
    stats = audit.get_stats()
    recent = audit.get_recent(10)
    
    print("=" * 50)
    print("📊 CNSH 审计报告")
    print("=" * 50)
    print(f"   总操作: {stats['total']}")
    print(f"   🟢 通过: {stats['green']}")
    print(f"   🟡 警告: {stats['yellow']}")
    print(f"   🔴 阻断: {stats['red']}")
    print("")
    if recent:
        print("   最近记录:")
        for r in recent[-5:]:
            print(f"     {r['level']} {r['command'][:40]} → {r['reason']}")
    print("=" * 50)


def cnsh_fuse_status():
    """显示熔断状态"""
    fuse = FuseMechanism()
    status = fuse.status()
    
    print("=" * 50)
    print("🚨 CNSH 熔断状态")
    print("=" * 50)
    if status['blown']:
        print(f"   状态: 🔴 已触发")
        print(f"   原因: {status['reason']}")
        print(f"   恢复: cnsh_fuse_reset")
    else:
        print(f"   状态: 🟢 正常")
        print(f"   警告计数: {status['counter']}/{status['threshold']}")
    print("=" * 50)


def cnsh_fuse_reset():
    """重置熔断"""
    import getpass
    confirm = getpass.getpass("请输入确认码: ")
    fuse = FuseMechanism()
    fuse.reset(confirm)


def cnsh_sync():
    """同步龍魂系统"""
    print("🔄 同步龍魂系统...")
    # 这里可以添加同步逻辑
    print("✅ 同步完成")


def cnsh_backup():
    """备份CNSH配置"""
    backup_dir = CNSH_HOME / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    import shutil
    for f in CNSH_HOME.glob("*"):
        if f.is_file() and f.name not in ["backup_*"]:
            shutil.copy2(f, backup_dir)
    
    print(f"✅ 备份完成: {backup_dir}")


def cnsh_logs(n: int = 20):
    """查看日志"""
    log_file = CNSH_LOGS_DIR / "audit.log"
    if not log_file.exists():
        print("暂无日志")
        return
    
    print(f"📋 最近{n}条日志:")
    print("=" * 50)
    with open(log_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines[-n:]:
            try:
                data = json.loads(line)
                print(f"{data['timestamp'][:19]} {data['level']} {data['command'][:50]}")
            except:
                print(line.strip())


# ============================================================
# 主程序
# ============================================================

def main():
    """主程序"""
    import argparse
    
    parser = argparse.ArgumentParser(description="CNSH 多语言终端 v5.1")
    parser.add_argument("--status", "-s", action="store_true", help="查看状态")
    parser.add_argument("--audit", "-a", action="store_true", help="查看审计报告")
    parser.add_argument("--fuse", "-f", action="store_true", help="查看熔断状态")
    parser.add_argument("--reset", "-r", action="store_true", help="重置熔断")
    parser.add_argument("--sync", action="store_true", help="同步龍魂系统")
    parser.add_argument("--backup", "-b", action="store_true", help="备份配置")
    parser.add_argument("--logs", "-l", type=int, nargs="?", const=20, help="查看日志")
    
    args = parser.parse_args()
    
    if args.status:
        cnsh_status()
    elif args.audit:
        cnsh_audit_report()
    elif args.fuse:
        cnsh_fuse_status()
    elif args.reset:
        cnsh_fuse_reset()
    elif args.sync:
        cnsh_sync()
    elif args.backup:
        cnsh_backup()
    elif args.logs:
        cnsh_logs(args.logs)
    else:
        # 启动交互式终端
        terminal = CNSHTerminal()
        try:
            terminal.run()
        finally:
            terminal.save_history()
            print("\n🐉 龍魂永存 · 数据主权在手")


if __name__ == "__main__":
    main()
