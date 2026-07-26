#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# #龍芯⚡️2026-07-26-LONGHUN-COMMANDER-v1.0
"""
═══════════════════════════════════════════════════════════════════════
  🐉 龍魂·指挥官模式 v1.0
  LongHun Commander Mode

  你说人话，系统干脏活。
  支持：自然语言指令映射 / 定时任务 / 编组启动 / 流水线闭环
═══════════════════════════════════════════════════════════════════════

用法:
  指挥 "查下芯片状态"
  指挥 "部署芯片"
  指挥 "验证这个图片的DNA /path/to/img.jpg"
  指挥 "每天凌晨3点备份数据"
  指挥 "启动日常巡检组"
  指挥 "列出所有指令"
  指挥 "定时每天晚上8点提醒我检查系统状态"
"""

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

# ═══════════════════════════════════════════════════════════════════════
# 常量
# ═══════════════════════════════════════════════════════════════════════

DNA: str = "#龍芯⚡️2026-07-26-LONGHUN-COMMANDER-v1.0"
CREATOR: str = "诸葛鑫（UID9622）"
SYSTEM_ROOT: Path = Path(__file__).resolve().parent.parent
CONFIG_DIR: Path = SYSTEM_ROOT / ".commander"
CONFIG_FILE: Path = CONFIG_DIR / "registry.json"
SCHEDULE_FILE: Path = CONFIG_DIR / "schedules.json"
LOG_FILE: Path = SYSTEM_ROOT / "logs" / "commander.log"

CONFIG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

# ═══════════════════════════════════════════════════════════════════════
# 默认指令注册表（人话 → 系统命令）
# ═══════════════════════════════════════════════════════════════════════

DEFAULT_REGISTRY: List[Dict[str, Any]] = [
    {
        "name": "芯片状态",
        "patterns": [r"查[一]?下芯片状态", r"芯片状态", r"韬定律状态", r"tao[\s\-]?chip[\s\-]?status"],
        "command": "python3 engines/lh_tao_chip.py status",
        "description": "查看韬定律芯片调度器当前状态",
        "needs_path": False,
    },
    {
        "name": "部署芯片",
        "patterns": [r"部署芯片", r"部署韬定律", r"启动韬定律", r"启动芯片调度"],
        "command": "bash bin/lh_tao_chip_deploy.sh",
        "description": "一键部署并启动韬定律芯片调度器",
        "needs_path": False,
    },
    {
        "name": "停止芯片调度",
        "patterns": [r"停止芯片调度", r"关掉韬定律", r"停止韬定律"],
        "command": "pkill -f 'engines/lh_tao_chip.py daemon' || true",
        "description": "停止韬定律守护进程",
        "needs_path": False,
    },
    {
        "name": "验证媒体DNA",
        "patterns": [r"验证这[个张幅]?(.+?)的DNA", r"验证DNA(.+)", r"验证媒体(.+)", r"检查水印(.+)"],
        "command": "python3 bin/lh_media_mark.py verify {path}",
        "description": "验证图片/视频/音频的龍魂DNA水印",
        "needs_path": True,
    },
    {
        "name": "标记媒体DNA",
        "patterns": [r"给(.+?)加DNA", r"给(.+?)加水印", r"标记(.+?)的DNA"],
        "command": "python3 bin/lh_media_mark.py mark {path}",
        "description": "给媒体文件注入龍魂DNA水印",
        "needs_path": True,
    },
    {
        "name": "记忆加载",
        "patterns": [r"加载记忆", r"读取记忆", r"启动记忆", r"memory load"],
        "command": "python3 bin/lh_memory_load.py",
        "description": "加载龍魂焊死记忆",
        "needs_path": False,
    },
    {
        "name": "系统健康检查",
        "patterns": [r"健康检查", r"系统状态", r"检查身体", r"体检", r"health check"],
        "command": "python3 bin/longhun-self-heal.py --quick || python3 engines/lh_tao_chip.py status",
        "description": "运行系统健康检查",
        "needs_path": False,
    },
    {
        "name": "备份数据",
        "patterns": [r"备份数据", r"数据备份", r"备份"],
        "command": "bash deploy/scripts/backup_data.sh || echo '备份脚本不存在，请检查 deploy/scripts/'",
        "description": "执行全量数据备份",
        "needs_path": False,
    },
    {
        "name": "同步鲲鹏",
        "patterns": [r"同步鲲鹏", r"同步到鲲鹏", r"推送到鲲鹏", r"kunpeng sync"],
        "command": "bash deploy/scripts/sync_to_kunpeng.sh || echo '同步脚本不存在'",
        "description": "同步本地代码到鲲鹏服务器",
        "needs_path": False,
    },
    {
        "name": "提交代码",
        "patterns": [r"提交代码", r"提交并推送", r"git push", r"push 代码"],
        "command": "git add -A && git commit -m 'chore: 自动提交' && git push gh-ssh orphan_main && git push gitcode orphan_main && git push gitee orphan_main",
        "description": "自动提交并推送到三端仓库",
        "needs_path": False,
    },
]

# 编组启动表
GROUP_REGISTRY: Dict[str, Dict[str, Any]] = {
    "日常巡检组": {
        "description": "每日系统巡检：记忆加载 + 健康检查 + 芯片状态",
        "commands": [
            "python3 bin/lh_memory_load.py",
            "python3 engines/lh_tao_chip.py status",
        ],
    },
    "视频生产组": {
        "description": "启动视频生产线相关服务",
        "commands": [
            "python3 engines/lh_tao_chip.py status",
            "python3 bin/lh_video_pipeline.py --help | head -5",
        ],
    },
    "安全加固组": {
        "description": "安全相关检查：芯片状态 + 媒体DNA验证入口",
        "commands": [
            "python3 engines/lh_tao_chip.py status",
            "python3 bin/lh_media_mark.py --help | head -5",
        ],
    },
}

# ═══════════════════════════════════════════════════════════════════════
# 日志
# ═══════════════════════════════════════════════════════════════════════

def log_event(category: str, detail: str):
    ts = datetime.now(timezone.utc).isoformat()
    line = f"{ts} | {category} | {detail}\n"
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line)
    except Exception:
        pass


# ═══════════════════════════════════════════════════════════════════════
# 指令注册表管理
# ═══════════════════════════════════════════════════════════════════════

class CommandRegistry:
    def __init__(self):
        self.registry: List[Dict[str, Any]] = []
        self.groups: Dict[str, Dict[str, Any]] = {}
        self._load()

    def _load(self):
        if CONFIG_FILE.exists():
            try:
                data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
                self.registry = data.get("commands", [])
                self.groups = data.get("groups", {})
            except Exception:
                self.registry = []
                self.groups = {}
        # 合并默认表（默认项不覆盖用户自定义）
        existing_names = {c["name"] for c in self.registry}
        for cmd in DEFAULT_REGISTRY:
            if cmd["name"] not in existing_names:
                self.registry.append(cmd.copy())
        for name, grp in GROUP_REGISTRY.items():
            if name not in self.groups:
                self.groups[name] = grp.copy()
        self._save()

    def _save(self):
        try:
            CONFIG_FILE.write_text(
                json.dumps({"commands": self.registry, "groups": self.groups}, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        except Exception as e:
            log_event("ERROR", f"保存注册表失败: {e}")

    def add_command(self, name: str, patterns: List[str], command: str, description: str = "", needs_path: bool = False):
        self.registry.append({
            "name": name,
            "patterns": patterns,
            "command": command,
            "description": description,
            "needs_path": needs_path,
        })
        self._save()

    def add_group(self, name: str, commands: List[str], description: str = ""):
        self.groups[name] = {"description": description, "commands": commands}
        self._save()

    def list_commands(self) -> List[Tuple[str, str, str]]:
        return [(c["name"], c["description"], c["command"]) for c in self.registry]

    def list_groups(self) -> List[Tuple[str, str, List[str]]]:
        return [(name, g["description"], g["commands"]) for name, g in self.groups.items()]

    def match(self, text: str) -> Optional[Tuple[Dict[str, Any], Dict[str, str]]]:
        for cmd in self.registry:
            for pattern in cmd["patterns"]:
                m = re.search(pattern, text)
                if m:
                    captures = m.groupdict()
                    # 如果模式里没有命名捕获，取最后一个分组作为 path
                    if cmd.get("needs_path") and not captures:
                        groups = m.groups()
                        if groups:
                            captures["path"] = groups[-1].strip()
                    return cmd, captures
        return None, {}


# ═══════════════════════════════════════════════════════════════════════
# 命令执行
# ═══════════════════════════════════════════════════════════════════════

def execute_command(command: str, dry_run: bool = False) -> int:
    print(f"[指挥官] 执行: {command}")
    log_event("EXEC", command)
    if dry_run:
        print("[指挥官] 🟡 演习模式，未实际执行")
        return 0
    try:
        result = subprocess.run(command, shell=True, cwd=SYSTEM_ROOT)
        return result.returncode
    except Exception as e:
        print(f"[指挥官] 🔴 执行失败: {e}", file=sys.stderr)
        log_event("ERROR", str(e))
        return 1


# ═══════════════════════════════════════════════════════════════════════
# 定时任务解析
# ═══════════════════════════════════════════════════════════════════════

def parse_time_phrase(phrase: str) -> Optional[str]:
    """把人话时间翻译成 cron 表达式"""
    phrase = phrase.strip().replace("每个", "每")
    
    # 每天 X 点
    m = re.search(r"每?天(?:凌晨|早上|上午|中午|下午|晚上)?(\d{1,2})点(?:半)?", phrase)
    if m:
        hour = int(m.group(1))
        minute = 30 if "半" in phrase else 0
        # 随机分钟，避免 herd
        minute = (minute + hash(phrase) % 10) % 60
        return f"{minute} {hour} * * *"
    
    # 每小时
    if re.search(r"每?小时", phrase):
        minute = hash(phrase) % 60
        return f"{minute} * * * *"
    
    # 每周几
    days = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "日": 0, "天": 0}
    for cn, num in days.items():
        if re.search(f"每?周{cn}", phrase):
            minute = hash(phrase) % 60
            return f"{minute} 9 * * {num}"
    
    # 每月 X 号
    m = re.search(r"每?月(\d{1,2})号", phrase)
    if m:
        day = int(m.group(1))
        minute = hash(phrase) % 60
        return f"{minute} 9 {day} * *"
    
    return None


def schedule_command(cron: str, command: str, name: str, reminder: str = "", dry_run: bool = False):
    """通过 launchd (macOS) 或 cron 创建定时任务"""
    if dry_run:
        print(f"[指挥官] 🟡 演习模式，以下定时任务未实际写入：")
        print(f"[指挥官]    名称: {name}")
        print(f"[指挥官]    cron: {cron}")
        print(f"[指挥官]    命令: {command}")
        if reminder:
            print(f"[指挥官]    提醒: {reminder}")
        return
    # 保存到本地调度表
    schedules = []
    if SCHEDULE_FILE.exists():
        try:
            schedules = json.loads(SCHEDULE_FILE.read_text(encoding="utf-8"))
        except Exception:
            schedules = []
    schedules.append({
        "name": name,
        "cron": cron,
        "command": command,
        "reminder": reminder,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "dna": DNA,
    })
    SCHEDULE_FILE.write_text(json.dumps(schedules, ensure_ascii=False, indent=2), encoding="utf-8")
    
    # macOS 优先 launchd
    if sys.platform == "darwin":
        plist_path = Path.home() / "Library" / "LaunchAgents" / f"longhun.commander.{name}.plist"
        plist = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>longhun.commander.{name}</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>-lc</string>
        <string>cd {SYSTEM_ROOT} && {command}</string>
    </array>
    <key>StartCalendarInterval</key>
    {cron_to_plist_interval(cron)}
    <key>StandardOutPath</key>
    <string>{SYSTEM_ROOT}/logs/commander_{name}.out.log</string>
    <key>StandardErrorPath</key>
    <string>{SYSTEM_ROOT}/logs/commander_{name}.err.log</string>
</dict>
</plist>"""
        plist_path.write_text(plist, encoding="utf-8")
        subprocess.run(["launchctl", "load", str(plist_path)], check=False)
        print(f"[指挥官] ✅ launchd 任务已加载: {plist_path}")
    else:
        # Linux/Kunpeng 用 cron
        cron_line = f"{cron} cd {SYSTEM_ROOT} && {command} >> {SYSTEM_ROOT}/logs/commander_{name}.out.log 2>&1 # longhun:{name}\n"
        cron_cmd = f"(crontab -l 2>/dev/null | grep -v '# longhun:{name}'; echo '{cron_line}') | crontab -"
        subprocess.run(cron_cmd, shell=True, check=False)
        print(f"[指挥官] ✅ crontab 已写入: {cron_line.strip()}")
    
    if reminder:
        # 同时用 Bark/飞书通知（如果配置了环境变量）
        notify_cmd = f"python3 -c \"import os; print('[提醒] {reminder}')\""
        print(f"[指挥官] 🔔 提醒内容: {reminder}")
    
    log_event("SCHEDULE", f"{name} | {cron} | {command}")


def cron_to_plist_interval(cron: str) -> str:
    """简单 cron → launchd StartCalendarInterval"""
    parts = cron.split()
    if len(parts) != 5:
        return "<dict><key>Minute</key><integer>0</integer></dict>"
    minute, hour, day, month, weekday = parts
    tags = []
    if minute != "*":
        tags.append(f"<key>Minute</key><integer>{minute}</integer>")
    if hour != "*":
        tags.append(f"<key>Hour</key><integer>{hour}</integer>")
    if day != "*":
        tags.append(f"<key>Day</key><integer>{day}</integer>")
    if month != "*":
        tags.append(f"<key>Month</key><integer>{month}</integer>")
    if weekday != "*":
        tags.append(f"<key>Weekday</key><integer>{weekday}</integer>")
    return "<dict>" + "".join(tags) + "</dict>"


# ═══════════════════════════════════════════════════════════════════════
# 编组启动
# ═══════════════════════════════════════════════════════════════════════

def run_group(name: str, registry: CommandRegistry, dry_run: bool = False) -> int:
    if name not in registry.groups:
        print(f"[指挥官] 🔴 未找到编组: {name}")
        print("可用编组:")
        for gname, desc, _ in registry.list_groups():
            print(f"  - {gname}: {desc}")
        return 1
    group = registry.groups[name]
    print(f"[指挥官] 🚀 启动编组: {name}")
    print(f"[指挥官] 说明: {group['description']}")
    for cmd in group["commands"]:
        rc = execute_command(cmd, dry_run=dry_run)
        if rc != 0 and not dry_run:
            print(f"[指挥官] ⚠️ 编组中命令失败，继续执行后续: {cmd}")
    return 0


# ═══════════════════════════════════════════════════════════════════════
# 自然语言处理
# ═══════════════════════════════════════════════════════════════════════

def handle_natural_language(text: str, registry: CommandRegistry, dry_run: bool = False) -> int:
    text = text.strip()
    log_event("INPUT", text)
    
    # 列出所有指令
    if re.search(r"列出所有|有哪些|help|--help|帮助", text):
        print("\n[指挥官] 可用自然语言指令：")
        for name, desc, cmd in registry.list_commands():
            print(f"  • {name}: {desc}")
            print(f"    → {cmd}")
        print("\n[指挥官] 可用编组：")
        for name, desc, cmds in registry.list_groups():
            print(f"  • {name}: {desc}")
            for c in cmds:
                print(f"    → {c}")
        return 0
    
    # 定时任务模式
    sched_match = re.search(r"定时\s*(.+?)\s*(?:提醒|通知|执行|跑|做)\s*(.+)", text)
    if sched_match:
        time_phrase = sched_match.group(1)
        action_phrase = sched_match.group(2)
        cron = parse_time_phrase(time_phrase)
        if not cron:
            print(f"[指挥官] 🔴 无法理解时间: {time_phrase}")
            print("[指挥官] 支持：每天X点、每小时、每周X、每月X号")
            return 1
        # 解析 action_phrase 里的实际命令
        inner_cmd, inner_captures = registry.match(action_phrase)
        if inner_cmd:
            resolved_cmd = resolve_command(inner_cmd, inner_captures)
        else:
            resolved_cmd = action_phrase
        name = f"auto_{int(time.time())}"
        schedule_command(cron, resolved_cmd, name, reminder=action_phrase, dry_run=dry_run)
        if not dry_run:
            print(f"[指挥官] ✅ 已定时: {time_phrase} → {cron}")
        print(f"[指挥官] 📝 执行命令: {resolved_cmd}")
        return 0
    
    # 编组启动
    group_match = re.search(r"启动(.+?)(?:组|服务|流水线)", text)
    if group_match:
        group_name = group_match.group(1).strip()
        # 模糊匹配编组名
        for gname in registry.groups:
            if group_name in gname or gname in group_name:
                return run_group(gname, registry, dry_run=dry_run)
        print(f"[指挥官] 🔴 未找到编组: {group_name}")
        return 1
    
    # 普通指令匹配
    cmd, captures = registry.match(text)
    if cmd:
        resolved = resolve_command(cmd, captures)
        return execute_command(resolved, dry_run=dry_run)
    
    # 都没匹配上
    print(f"[指挥官] 🔴 未能理解指令: {text}")
    print("[指挥官] 试试说：列出所有指令")
    return 1


def resolve_command(cmd: Dict[str, Any], captures: Dict[str, str]) -> str:
    command = cmd["command"]
    if cmd.get("needs_path"):
        path = captures.get("path", "")
        # 如果没从模式里抓到 path，尝试从整句话里抠一个文件路径
        if not path:
            m = re.search(r"[~/]?[\w\-./]+\.(?:jpg|jpeg|png|mp4|mp3|wav|ttf|otf|woff2?)", command)
            if m:
                path = m.group(0)
        path = path.strip()
        if not path:
            raise ValueError(f"指令 [{cmd['name']}] 需要一个文件路径")
        command = command.replace("{path}", path)
    return command


# ═══════════════════════════════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="龍魂·指挥官模式 — 你说人话，系统干脏活",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  指挥 "查下芯片状态"
  指挥 "部署芯片"
  指挥 "验证这个图片的DNA ./test.jpg"
  指挥 "每天凌晨3点备份数据"
  指挥 "启动日常巡检组"
  指挥 "列出所有指令"
        """,
    )
    parser.add_argument("text", nargs="*", help="自然语言指令")
    parser.add_argument("--dry-run", action="store_true", help="演习模式，不实际执行")
    parser.add_argument("--add", action="store_true", help="添加新指令（交互式）")
    parser.add_argument("--list", action="store_true", help="列出所有指令")
    parser.add_argument("--add-group", action="store_true", help="添加新编组（交互式）")
    args = parser.parse_args()
    
    registry = CommandRegistry()
    
    if args.list:
        return handle_natural_language("列出所有指令", registry, dry_run=args.dry_run)
    
    if args.add:
        print("[指挥官] 添加新指令")
        name = input("名称: ")
        patterns = input("匹配正则（多个用逗号）: ").split(",")
        patterns = [p.strip() for p in patterns]
        command = input("执行命令: ")
        desc = input("描述: ")
        needs_path = input("是否需要路径(y/N): ").lower() == "y"
        registry.add_command(name, patterns, command, desc, needs_path)
        print(f"[指挥官] ✅ 已添加: {name}")
        return 0
    
    if args.add_group:
        print("[指挥官] 添加新编组")
        name = input("编组名称: ")
        desc = input("描述: ")
        cmds = []
        while True:
            c = input("命令（空行结束）: ")
            if not c:
                break
            cmds.append(c)
        registry.add_group(name, cmds, desc)
        print(f"[指挥官] ✅ 已添加编组: {name}")
        return 0
    
    if not args.text:
        parser.print_help()
        return 1
    
    text = " ".join(args.text)
    return handle_natural_language(text, registry, dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
