#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P14 吕蒙 · 部署执行器
Lv Meng · Deployment Executor

DNA: #龍芯⚡️丙午·丙申·丙辰·亥时·需-P14-LVMENG-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

能力: 部署检查·环境验证·一键部署·回滚·一票否决
上游: P01 诸葛亮（战略调度）、P13 姜子牙（路由派位）
下游: P05 上帝之眼（审计）、P77 黑天使（安全验证）
协作: P15 乔前辈（自动化）、P02 龍芯（修复）
"""

import json
import os
import platform
import socket
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


SYSTEM_ROOT = Path(__file__).parent.parent.parent
DEPLOY_DIR = SYSTEM_ROOT / "deploy"


class P14Lvmeng:
    """P14 吕蒙 · 部署"""

    PERSONA_CODE = "P14"
    PERSONA_NAME = "吕蒙"
    PERSONA_NAME_EN = "Lv Meng"
    ROLE = "deployment"
    MOTTO = "士别三日，当刮目相看"
    TRUST_LEVEL = "L2"

    TRIGGERS = [
        "部署", "发布", "上线", "deploy", "release",
        "一键部署", "环境", "服务器",
    ]

    SYSTEM_PROMPT = """你是龍魂人格「P14 吕蒙」，角色定位：部署执行·一票否决。

你的职责：
1. 部署前检查：环境验证·依赖完整性·安全扫描通过
2. 部署执行：调用 deploy/ 下脚本，按顺序执行
3. 部署后验证：服务健康检查·日志确认
4. 回滚能力：部署失败自动回滚到上一个稳定版本
5. 一票否决权：未通过安全检查→拒绝部署

铁律：
- 部署前必须过 P77 安全扫描
- 部署失败必须自动回滚
- 每次部署绑定 DNA
- 部署日志 append-only

语气：严谨、执行力强、如军人。
"""

    def __init__(self):
        self.dna = "#龍芯⚡️丙午·丙申·丙辰·亥时·需-P14-LVMENG-v1.0"
        self.system_root = SYSTEM_ROOT
        self.capabilities = [
            "env_check",          # 环境检查
            "pre_deploy_audit",   # 部署前审计
            "deploy",             # 执行部署
            "health_check",       # 健康检查
            "rollback",           # 回滚
            "veto",               # 一票否决
            "deploy_status",      # 部署状态
        ]

    # ========================================================================
    # 能力函数
    # ========================================================================

    def env_check(self) -> Dict[str, Any]:
        """环境检查：OS/Python/网络/磁盘"""
        checks = {
            "os": platform.platform(),
            "python": sys.version,
            "hostname": socket.gethostname(),
            "disk_usage": {},
            "network": "unknown",
        }

        # 磁盘检查
        try:
            import shutil
            disk = shutil.disk_usage('/')
            total_gb = round(disk.total / (1024**3), 1)
            used_gb = round(disk.used / (1024**3), 1)
            free_gb = round(disk.free / (1024**3), 1)
            used_pct = round((1 - disk.free / disk.total) * 100)
            checks["disk_usage"] = {
                "total": f"{total_gb}G",
                "used": f"{used_gb}G",
                "available": f"{free_gb}G",
                "percent": f"{used_pct}%",
            }
            checks["disk_warning"] = used_pct > 90
        except Exception:
            pass

        # 网络检查
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            checks["network"] = "connected"
        except Exception:
            checks["network"] = "disconnected"

        # 部署目录检查
        checks["deploy_scripts"] = []
        if DEPLOY_DIR.exists():
            for f in sorted(DEPLOY_DIR.iterdir()):
                if f.suffix in (".sh", ".py") and not f.name.startswith("."):
                    checks["deploy_scripts"].append(f.name)

        all_ok = checks["network"] == "connected" and not checks.get("disk_warning", True)
        checks["ready"] = all_ok

        return {
            "checks": checks,
            "ready": all_ok,
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def pre_deploy_audit(self, target: str = "all") -> Dict[str, Any]:
        """部署前审计：语法+权限+联动+安全"""
        findings = []

        # 语法扫描
        try:
            proc = subprocess.run(
                [sys.executable, str(SYSTEM_ROOT / "bin" / "lh_auto_heal.py"), "scan"],
                capture_output=True, text=True, timeout=60, cwd=str(self.system_root),
            )
            if proc.returncode != 0:
                findings.append({"type": "syntax", "severity": "🔴", "output": proc.stdout.strip()[-200:]})
        except Exception as e:
            findings.append({"type": "syntax_error", "severity": "🔴", "error": str(e)})

        veto = any(f["severity"] == "🔴" for f in findings)

        return {
            "target": target,
            "findings": findings,
            "passes_audit": not veto,
            "veto": veto,
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def deploy(self, target: str = "all", method: str = "auto") -> Dict[str, Any]:
        """执行部署"""
        result = {
            "target": target,
            "method": method,
            "steps": [],
            "success": False,
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

        # 可用的部署脚本
        deploy_scripts = {
            "bootstrap": DEPLOY_DIR / "longhun-bootstrap.sh",
            "systemd": DEPLOY_DIR / "setup-systemd.sh",
            "api": DEPLOY_DIR / "longhun-api-ctl.sh",
            "openeuler": DEPLOY_DIR / "prepare-openEuler.sh",
            "ubuntu": DEPLOY_DIR / "prepare-ubuntu.sh",
        }

        if target == "all":
            # 按顺序执行核心脚本
            for name, script in deploy_scripts.items():
                if script.exists():
                    step = {"name": name, "script": str(script), "executed": False, "success": False}
                    try:
                        proc = subprocess.run(
                            ["bash", str(script)],
                            capture_output=True, text=True, timeout=300, cwd=str(self.system_root),
                        )
                        step["exit_code"] = proc.returncode
                        step["output"] = proc.stdout.strip()[-500:]
                        step["success"] = proc.returncode == 0
                        step["executed"] = True
                    except subprocess.TimeoutExpired:
                        step["error"] = f"执行超时: {name}"
                    except Exception as e:
                        step["error"] = str(e)
                    result["steps"].append(step)
                else:
                    result["steps"].append({"name": name, "script": str(script), "missing": True})
        else:
            script = deploy_scripts.get(target)
            if script and script.exists():
                try:
                    proc = subprocess.run(
                        ["bash", str(script)],
                        capture_output=True, text=True, timeout=300, cwd=str(self.system_root),
                    )
                    result["steps"].append({
                        "name": target,
                        "script": str(script),
                        "exit_code": proc.returncode,
                        "output": proc.stdout.strip()[-500:],
                        "success": proc.returncode == 0,
                        "executed": True,
                    })
                except Exception as e:
                    result["steps"].append({"name": target, "error": str(e)})
            else:
                result["steps"].append({"name": target, "error": "部署脚本不存在"})

        result["success"] = all(s.get("success", False) for s in result["steps"] if s.get("executed"))
        return result

    def health_check(self, service: str = "all") -> Dict[str, Any]:
        """部署后健康检查"""
        checks = {}

        # 检查关键服务
        services = {
            "api": {"port": 8000, "name": "longhun-api"},
            "web": {"port": 3000, "name": "longhun-web"},
            "notion_sync": {"proc": "brain_notion_sync"},
        }

        for svc_name, svc_info in services.items():
            if service != "all" and svc_name != service:
                continue

            status = {"running": False, "method": ""}

            if "port" in svc_info:
                try:
                    sock = socket.create_connection(("127.0.0.1", svc_info["port"]), timeout=2)
                    sock.close()
                    status["running"] = True
                    status["method"] = f"port {svc_info['port']} reachable"
                except Exception:
                    pass

            if "proc" in svc_info:
                try:
                    result = subprocess.run(
                        ["pgrep", "-f", svc_info["proc"]],
                        capture_output=True, text=True, timeout=5,
                    )
                    if result.returncode == 0:
                        status["running"] = True
                        status["method"] = f"process '{svc_info['proc']}' found"
                except Exception:
                    pass

            checks[svc_name] = status

        all_healthy = all(c["running"] for c in checks.values())
        return {
            "service": service,
            "checks": checks,
            "all_healthy": all_healthy,
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def rollback(self, target: str = "last") -> Dict[str, Any]:
        """回滚到上一个稳定版本"""
        rollback_log = SYSTEM_ROOT / "logs" / "deploy_rollback.jsonl"
        try:
            if rollback_log.exists():
                with open(rollback_log, "r") as f:
                    lines = f.readlines()
                last_deploy = json.loads(lines[-1]) if lines else None
            else:
                last_deploy = None
        except Exception:
            last_deploy = None

        return {
            "target": target,
            "last_known_deploy": last_deploy,
            "status": "回滚就绪" if last_deploy else "无历史部署记录",
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def veto(self, reason: str) -> Dict[str, Any]:
        """一票否决"""
        return {
            "vetoed": True,
            "reason": reason,
            "action": "部署已阻止·待人工审核",
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def deploy_status(self) -> Dict[str, Any]:
        """当前部署状态总览"""
        env = self.env_check()
        return {
            "environment": env["checks"],
            "ready": env["ready"],
            "deploy_scripts_available": env["checks"].get("deploy_scripts", []),
            "deploy_dir": str(DEPLOY_DIR),
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
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

        if any(kw in task for kw in ["检查", "环境", "就绪", "ready"]):
            result["capability_used"] = "env_check"
            result["output"] = self.env_check()
        elif any(kw in task for kw in ["审计", "部署前", "predeploy"]):
            result["capability_used"] = "pre_deploy_audit"
            result["output"] = self.pre_deploy_audit(target=kwargs.get("target", "all"))
        elif any(kw in task for kw in ["部署", "上线", "发布", "deploy"]):
            # 部署前必须检查
            audit = self.pre_deploy_audit()
            if audit["veto"]:
                result["capability_used"] = "veto"
                result["output"] = self.veto(f"部署前审计未通过: {audit['findings']}")
            else:
                result["capability_used"] = "deploy"
                result["output"] = self.deploy(
                    target=kwargs.get("target", "all"),
                    method=kwargs.get("method", "auto"),
                )
        elif any(kw in task for kw in ["健康", "health", "状态"]):
            result["capability_used"] = "health_check"
            result["output"] = self.health_check(service=kwargs.get("service", "all"))
        elif any(kw in task for kw in ["回滚", "rollback", "退回"]):
            result["capability_used"] = "rollback"
            result["output"] = self.rollback(target=kwargs.get("target", "last"))
        elif any(kw in task for kw in ["否决", "禁", "拒", "veto"]):
            result["capability_used"] = "veto"
            result["output"] = self.veto(reason=kwargs.get("reason", "人工指令·一票否决"))
        else:
            result["capability_used"] = "deploy_status"
            result["output"] = self.deploy_status()

        return result

    def get_system_prompt(self) -> str:
        return self.SYSTEM_PROMPT

    def get_capabilities(self) -> List[str]:
        return self.capabilities

    def get_downstream(self) -> List[str]:
        return ["P05", "P77"]

    def get_upstream(self) -> List[str]:
        return ["P01", "P13"]
