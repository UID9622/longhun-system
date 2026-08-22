#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂生态实时监控器
==================
采集本地资源消耗、模块健康状态、可运行入口，返回给生态仪表盘。

DNA:#龍芯⚡️丙午·甲午·癸亥·戊午·䷚颐-LONGHUN-SYSTEM-MONITOR-FILE1-v1.0
"""
import os
import json
import platform
import time
from pathlib import Path
from datetime import datetime

# 项目根目录
ROOT = Path(__file__).resolve().parent.parent.parent


def _load_module_menus():
    """扫描所有 desktop-menu.json，找出可运行的模块。"""
    modules = []
    for menu_file in ROOT.rglob("desktop-menu.json"):
        try:
            data = json.loads(menu_file.read_text(encoding="utf-8"))
            rel_dir = menu_file.parent.relative_to(ROOT)
            for item in data.get("items", []):
                modules.append({
                    "模块": str(rel_dir),
                    "名称": item.get("label", "未命名"),
                    "命令": item.get("command", ""),
                    "描述": item.get("description", ""),
                    "类型": item.get("type", "shell"),
                })
        except Exception:
            continue
    return modules


def _module_nodes():
    """为生态图生成节点和边。"""
    nodes = [
        {"id": "user", "label": "你", "group": "human", "title": "一句话改变整套逻辑"},
        {"id": "control-panel", "label": "龍魂操作台", "group": "core", "title": "统一调度中心"},
        {"id": "cnsh-terminal", "label": "CNSH 终端", "group": "core", "title": "中文编程终端"},
        {"id": "editor", "label": "龍碼编辑器", "group": "tool", "title": "中文代码编辑器"},
        {"id": "brain", "label": "龍魂大脑", "group": "brain", "title": "记忆与推理"},
        {"id": "memory-universe", "label": "星辰记忆", "group": "brain", "title": "本地记忆库"},
        {"id": "xpay", "label": "XPay 支付", "group": "service", "title": "主权货币支付"},
        {"id": "crypto-stack", "label": "加密堆栈", "group": "service", "title": "六层加密安全"},
        {"id": "agents", "label": "龍魂 Agents", "group": "service", "title": "自动执行器"},
        {"id": "executors", "label": "底座执行器", "group": "service", "title": "MVP 启动/脚本管理"},
        {"id": "baobao-guardian", "label": "宝宝守护", "group": "tool", "title": "桌面风险助手"},
        {"id": "skills", "label": "10 大技能", "group": "skill", "title": "算法艺术/品牌/文档等"},
        {"id": "audit", "label": "三色审计", "group": "guard", "title": "🟢🟡🔴 自动审计"},
        {"id": "dna", "label": "DNA 追溯", "group": "guard", "title": "每个动作都可溯源"},
    ]

    edges = [
        {"from": "user", "to": "control-panel", "label": "一句话指令"},
        {"from": "control-panel", "to": "cnsh-terminal", "label": "调度"},
        {"from": "control-panel", "to": "skills", "label": "调用"},
        {"from": "control-panel", "to": "audit", "label": "审计"},
        {"from": "cnsh-terminal", "to": "brain", "label": "请求记忆"},
        {"from": "cnsh-terminal", "to": "editor", "label": "编辑代码"},
        {"from": "brain", "to": "memory-universe", "label": "读写记忆"},
        {"from": "xpay", "to": "crypto-stack", "label": "加密保护"},
        {"from": "agents", "to": "executors", "label": "执行任务"},
        {"from": "agents", "to": "audit", "label": "上报行为"},
        {"from": "audit", "to": "dna", "label": "生成追溯"},
        {"from": "dna", "to": "control-panel", "label": "展示状态", "dashes": True},
    ]
    return nodes, edges


def _resource_usage():
    """获取 CPU、内存、磁盘使用。优先用 psutil，没有则返回提示。"""
    try:
        import psutil
        cpu = psutil.cpu_percent(interval=0.5)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage(str(ROOT))
        return {
            "cpu_percent": round(cpu, 1),
            "memory_percent": round(mem.percent, 1),
            "memory_used_gb": round(mem.used / (1024 ** 3), 2),
            "memory_total_gb": round(mem.total / (1024 ** 3), 2),
            "disk_percent": round(disk.percent, 1),
            "disk_used_gb": round(disk.used / (1024 ** 3), 2),
            "disk_total_gb": round(disk.total / (1024 ** 3), 2),
        }
    except Exception as e:
        return {
            "error": str(e),
            "note": "如需精确监控，可运行：pip3 install psutil"
        }


def get_system_status():
    """主入口：返回完整生态状态。"""
    nodes, edges = _module_nodes()
    return {
        "timestamp": datetime.now().isoformat(),
        "device": {
            "system": platform.system(),
            "machine": platform.machine(),
            "node": platform.node(),
        },
        "resources": _resource_usage(),
        "modules": _load_module_menus(),
        "ecosystem": {
            "nodes": nodes,
            "edges": edges,
        },
        "dna": "#龍芯⚡️丙午·甲午·癸亥·戊午·䷚颐-LONGHUN-SYSTEM-MONITOR-v1.0",
    }


if __name__ == "__main__":
    print(json.dumps(get_system_status(), ensure_ascii=False, indent=2))
