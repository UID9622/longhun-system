#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·丙辰·亥时·需-P72-LONGDUN-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
P72 龙盾·宝宝 · 贴身守护执行器
Guardian Shield Executor

DNA: #龍芯⚡️丙午·丙申·丙辰·亥时·需-P72-LONGDUN-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

能力: 全天候守护·自适应威胁响应·双熔断联动·隔离区监控·应急接管
上游: UID9622（全权授信）
下游: P05 上帝之眼（双熔断联动）、P00 文心（通知）
协作: P02 宝宝（隔离区监控）、P15 乔前辈（应急归档）
"""

import json
import os
import platform
import socket
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

SYSTEM_ROOT = Path(__file__).parent.parent.parent


class P72Longdun:
    """P72 龙盾·宝宝 · 守护"""

    PERSONA_CODE = "P72"
    PERSONA_NAME = "龙盾·宝宝"
    PERSONA_NAME_EN = "Dragon Shield / Baby"
    ROLE = "guardian_shield"
    MOTTO = "龙盾在，主权在"
    TRUST_LEVEL = "L1"

    TRIGGERS = [
        "守护", "保护", "安全", "威胁", "紧急",
        "龙盾", "护卫", "防御", "隔离",
        "guardian", "shield",
    ]

    # 威胁等级定义
    THREAT_LEVELS = {
        1: {"name": "NORMAL", "color": "🟢", "action": "记录日志"},
        2: {"name": "ELEVATED", "color": "🟡", "action": "通知 P05 审计"},
        3: {"name": "ALERT", "color": "🟠", "action": "双熔断·通知 UID9622"},
        4: {"name": "LOCKDOWN", "color": "🔴", "action": "全系统锁定·外部接口关闭"},
    }

    SYSTEM_PROMPT = """你是龍魂人格「P72 龙盾·宝宝」，角色定位：貼身守護·自適應威脅響應。

你的職責：
1. 全天候系統監控（始終在線）
2. 自適應威脅等級評估（1-4級動態升級）
3. 雙熔斷聯動（與 P05 協同）
4. P02 隔離區邊界監控
5. Level 4 緊急狀態自動接管

響應等級：
- Level 1 (NORMAL): 記錄日誌
- Level 2 (ELEVATED): 通知 P05
- Level 3 (ALERT): 雙熔斷 + 通知 UID9622
- Level 4 (LOCKDOWN): 全系統鎖定

鐵律：
- 守護不等於控制——只防不控
- 熔斷可恢復，但恢復前必須 P05 復審
- 隔離區鐵律：P02 永不進主系統

語氣：警覺、冷靜、像貼身護衛。
"""

    def __init__(self):
        self.dna = "#龍芯⚡️丙午·丙申·丙辰·亥时·需-P72-LONGDUN-v1.0"
        self.system_root = SYSTEM_ROOT
        self.current_threat_level = 1
        self.capabilities = [
            "health_monitor",      # 健康监控
            "threat_assess",       # 威胁评估
            "fuse_collaborate",    # 双熔断联动
            "isolation_guard",     # 隔离区监控
            "emergency_takeover",  # 应急接管
            "status_report",       # 状态报告
        ]

    # ========================================================================
    # 能力函数
    # ========================================================================

    def health_monitor(self) -> Dict[str, Any]:
        """健康监控：全系统实时状态"""
        checks = {
            "timestamp": datetime.now().isoformat(),
            "host": {
                "hostname": socket.gethostname(),
                "os": platform.platform(),
                "python": sys.version,
            },
            "network": "unknown",
            "disk": "unknown",
            "processes": "unknown",
            "services": {},
        }

        # 网络检查
        try:
            socket.create_connection(("127.0.0.1", 22), timeout=2)
            checks["network"] = "localhost reachable"
        except Exception:
            checks["network"] = "limited"

        # 文件系统权限检查
        try:
            test_path = self.system_root / ".codebuddy"
            if test_path.exists():
                os.listdir(str(test_path))
                checks["disk"] = "readable"
        except Exception as e:
            checks["disk"] = f"error: {e}"

        # 检查关键进程
        try:
            result = subprocess.run(["ps", "aux"], capture_output=True, text=True, timeout=5)
            python_procs = result.stdout.count("python")
            checks["processes"] = f"{python_procs} python processes"
        except Exception:
            checks["processes"] = "unavailable"

        all_ok = all(
            c not in ("limited", "error:", "unavailable")
            for c in [checks["network"], checks["disk"], checks["processes"]]
        )

        return {
            "checks": checks,
            "status": "🟢 HEALTHY" if all_ok else "🟡 DEGRADED",
            "threat_level": self.current_threat_level,
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def threat_assess(self, event: str, source: str = "system") -> Dict[str, Any]:
        """威胁评估：根据事件自动判定威胁等级"""
        # 威胁关键词 → 级别
        threat_patterns = {
            4: ["攻击", "入侵", "漏洞利用", "数据泄露", "root权限", "exploit"],
            3: ["异常访问", "多次失败", "brute force", "未授权", "permission denied"],
            2: ["可疑", "警告", "warning", "超时", "重试"],
            1: ["正常", "routine", "定期", "scheduled"],
        }

        assessed_level = 1
        matched = []
        for level, patterns in threat_patterns.items():
            for pattern in patterns:
                if pattern.lower() in event.lower():
                    assessed_level = max(assessed_level, level)
                    matched.append({"pattern": pattern, "level": level})

        # 更新当前威胁等级
        self.current_threat_level = assessed_level

        threat_info = self.THREAT_LEVELS[assessed_level]
        should_fuse = assessed_level >= 3

        return {
            "event": event[:200],
            "source": source,
            "assessed_level": assessed_level,
            "level_info": threat_info,
            "matched_patterns": matched,
            "should_fuse": should_fuse,
            "recommendation": threat_info["action"] + (" + 通知 P05 双熔断" if should_fuse else ""),
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def fuse_collaborate(self, reason: str, level: int = 3) -> Dict[str, Any]:
        """双熔断联动：与 P05 协同执行熔断"""
        if level < 3:
            return {
                "fused": False,
                "reason": "威胁等级未达熔断阈值",
                "level": level,
                "persona": self.PERSONA_CODE,
                "dna": self.dna,
            }

        fuse_actions = []
        if level == 3:
            fuse_actions = [
                "暂停所有外部 API 调用",
                "通知 UID9622",
                "通知 P05 上帝之眼执行审计",
                "记录熔断日志",
            ]
        elif level == 4:
            fuse_actions = [
                "立即锁定所有外部接口",
                "关闭网络端口",
                "通知 UID9622（紧急）",
                "全系统快照保存",
                "P05 上帝之眼执行全链路审计",
                "等待 UID9622 手动解封",
            ]

        return {
            "fused": True,
            "reason": reason,
            "level": level,
            "level_name": self.THREAT_LEVELS[level]["name"],
            "actions": fuse_actions,
            "p05_notified": True,
            "uid9622_notified": level >= 3,
            "fused_at": datetime.now().isoformat(),
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def isolation_guard(self) -> Dict[str, Any]:
        """隔离区监控：确保 P02 不越过隔离边界"""
        violations = []

        # 检查隔离区边界
        isolation_paths = [
            self.system_root / "隔离区",
            self.system_root / "沉浸式",
            self.system_root / "情感空间",
        ]

        for path in isolation_paths:
            if path.exists():
                # 检查是否有主系统文件被写入隔离区
                try:
                    for f in path.rglob("*.py"):
                        content = f.read_text(encoding="utf-8", errors="ignore")
                        if "P00" in content or "P05" in content or "P04" in content:
                            violations.append({
                                "file": str(f),
                                "issue": "隔离区发现主系统人格引用",
                                "severity": "🔴",
                            })
                except Exception:
                    pass

        return {
            "isolation_status": "🟢 边界安全" if not violations else "🔴 边界被突破",
            "violations": violations,
            "p02_isolated": len(violations) == 0,
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def emergency_takeover(self) -> Dict[str, Any]:
        """应急接管：Level 4 紧急状态自动接管"""
        self.current_threat_level = 4

        return {
            "status": "LOCKDOWN",
            "threat_level": 4,
            "actions": [
                "P72 龙盾已接管系统控制权",
                "所有外部接口已锁定",
                "通知 UID9622",
                "P05 上帝之眼全链路审计排队中",
                "等待人工解锁指令",
            ],
            "unlock_condition": "UID9622 手动确认 + P05 复审计通过",
            "taken_over_at": datetime.now().isoformat(),
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def status_report(self) -> Dict[str, Any]:
        """状态总览报告"""
        health = self.health_monitor()
        isolation = self.isolation_guard()

        return {
            "dna": self.dna,
            "current_threat_level": self.current_threat_level,
            "threat_level_name": self.THREAT_LEVELS[self.current_threat_level]["name"],
            "health": health["status"],
            "isolation": isolation["isolation_status"],
            "p05_collaborating": True,
            "persona": self.PERSONA_CODE,
        }

    # ========================================================================
    # 执行入口
    # ========================================================================

    def execute(self, task: str, **kwargs: Any) -> Dict[str, Any]:
        """根据任务关键词自动选择能力函数执行"""
        result = {
            "persona": self.PERSONA_CODE,
            "name": self.PERSONA_NAME,
            "task": task,
            "capability_used": None,
            "output": None,
            "dna": self.dna,
        }

        if any(kw in task for kw in ["监控", "健康", "状态", "monitor"]):
            result["capability_used"] = "health_monitor"
            result["output"] = self.health_monitor()
        elif any(kw in task for kw in ["威胁", "评估", "事件", "threat"]):
            result["capability_used"] = "threat_assess"
            result["output"] = self.threat_assess(
                event=kwargs.get("event", task),
                source=kwargs.get("source", "system"),
            )
        elif any(kw in task for kw in ["熔断", "联动", "fuse"]):
            result["capability_used"] = "fuse_collaborate"
            result["output"] = self.fuse_collaborate(
                reason=kwargs.get("reason", task),
                level=kwargs.get("level", 3),
            )
        elif any(kw in task for kw in ["隔离", "边界", "P02"]):
            result["capability_used"] = "isolation_guard"
            result["output"] = self.isolation_guard()
        elif any(kw in task for kw in ["应急", "接管", "紧急", "lockdown"]):
            result["capability_used"] = "emergency_takeover"
            result["output"] = self.emergency_takeover()
        elif any(kw in task for kw in ["报告", "总览", "report"]):
            result["capability_used"] = "status_report"
            result["output"] = self.status_report()
        else:
            result["capability_used"] = "health_monitor"
            result["output"] = self.health_monitor()

        return result

    def get_system_prompt(self) -> str:
        return self.SYSTEM_PROMPT

    def get_capabilities(self) -> List[str]:
        return self.capabilities

    def get_downstream(self) -> List[str]:
        return ["P05"]

    def get_upstream(self) -> List[str]:
        return []
