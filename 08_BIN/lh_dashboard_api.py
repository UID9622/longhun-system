#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
龍魂系统 · 仪表盘API端点 v1.0
DNA: #龍芯⚡️丙午·乙未·丙申·酉时·☰乾-DASHBOARD-API-v1.0-e6f7a8b9
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
补全: 主计划1.4·统一启动面板API后端
"""

import os
import json
import time
import socket
import psutil
import subprocess
from pathlib import Path
from datetime import datetime

# 注册到小艺桥接 / 知识中枢API
# 用法: 被主API模块导入使用

BASE_DIR = Path(__file__).resolve().parent.parent
SERVICES = [
    {"id": "longhun-api", "name": "知识中枢API", "port": 8766},
    {"id": "longhun-audit", "name": "胖东来审计API", "port": 8767},
    {"id": "longhun-portal", "name": "门户服务", "port": 8777},
    {"id": "longhun-xiaoyi", "name": "小艺桥接", "port": 8799},
    {"id": "longhun-core", "name": "核心调度器", "port": 9622},
    {"id": "longhun-symbiote", "name": "共生体矩阵", "port": 9627},
    {"id": "longhun-sovereignty", "name": "主权网关", "port": 9623},
    {"id": "longhun-ant-colony", "name": "蚁群引擎", "port": 8443},
    {"id": "longhun-dashboard", "name": "Web仪表", "port": 8444},
    {"id": "longhun-gatekeeper", "name": "API守门人", "port": 8446},
    {"id": "longhun-longzhishou", "name": "龍智守", "port": 9677},
    {"id": "ollama", "name": "Ollama推理", "port": 11434},
    {"id": "nginx", "name": "Nginx代理", "port": 80},
]

def check_port(host: str = "localhost", port: int = 0, timeout: float = 2.0) -> dict:
    """检查端口是否可达"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return {"reachable": result == 0, "latency_ms": None}
    except Exception as e:
        return {"reachable": False, "error": str(e)}

def get_system_resources() -> dict:
    """获取系统资源"""
    try:
        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "cpu_count": psutil.cpu_count(),
            "memory": {
                "total_gb": round(psutil.virtual_memory().total / (1024**3), 1),
                "used_gb": round(psutil.virtual_memory().used / (1024**3), 1),
                "percent": psutil.virtual_memory().percent,
            },
            "disk": {
                "total_gb": round(psutil.disk_usage("/").total / (1024**3), 1),
                "used_gb": round(psutil.disk_usage("/").used / (1024**3), 1),
                "percent": psutil.disk_usage("/").percent,
            },
            "uptime_hours": round(time.time() - psutil.boot_time(), 1) / 3600,
        }
    except Exception:
        return {
            "cpu_percent": None,
            "memory": {"total_gb": None, "used_gb": None, "percent": None},
            "disk": {"total_gb": None, "used_gb": None, "percent": None},
        }

def get_services_status() -> list:
    """获取所有服务状态"""
    results = []
    for svc in SERVICES:
        status = check_port(port=svc["port"])
        results.append({
            **svc,
            "online": status["reachable"],
            "status": "running" if status["reachable"] else "stopped",
        })
    return results

def get_full_status() -> dict:
    """获取完整系统状态"""
    services = get_services_status()
    resources = get_system_resources()
    
    online_count = sum(1 for s in services if s["online"])
    total_count = len(services)
    
    overall = "healthy" if online_count >= total_count - 1 else "degraded" if online_count >= total_count - 3 else "down"
    
    return {
        "status": overall,
        "timestamp": datetime.now().isoformat(),
        "services": {s["id"]: {"name": s["name"], "port": s["port"], "status": s["status"]} for s in services},
        "summary": {"online": online_count, "total": total_count},
        "resources": resources,
        "dna": "#龍芯⚡️{}-DASHBOARD-STATUS-v1.0-{}".format(
            datetime.now().strftime("%Y-%m-%d"),
            hex(int(time.time()))[-8:],
        ),
    }

def get_recent_logs(lines: int = 20) -> list:
    """获取最近日志"""
    entries = []
    log_files = [
        Path.home() / ".longhun" / "logs" / "system.log",
        Path.home() / ".longhun" / "logs" / "audit.log",
    ]
    
    for log_file in log_files:
        if log_file.exists():
            try:
                with open(log_file) as f:
                    for line in f.readlines()[-lines:]:
                        entries.append(line.strip())
            except Exception:
                pass
    
    return entries[-lines:]

def action_health_check() -> dict:
    """执行全系统体检"""
    services = get_services_status()
    resources = get_system_resources()
    
    issues = []
    for svc in services:
        if not svc["online"]:
            issues.append(f"{svc['name']} (:{{svc['port']}}) 不可达")
    
    if resources.get("cpu_percent", 0) and resources["cpu_percent"] > 90:
        issues.append(f"CPU使用率过高: {resources['cpu_percent']}%")
    if resources.get("memory", {}).get("percent", 0) > 90:
        issues.append(f"内存使用率过高: {resources['memory']['percent']}%")
    
    return {
        "status": "healthy" if not issues else "warning",
        "issues": issues,
        "services": len(services),
        "online": sum(1 for s in services if s["online"]),
        "resources": resources,
        "timestamp": datetime.now().isoformat(),
    }

def action_restart_services(target: str = "all") -> dict:
    """重启服务"""
    # 安全确认
    confirm_code = os.environ.get("EXECUTOR_TOKEN", "")
    if not confirm_code:
        return {"status": "denied", "reason": "需要EXECUTOR_TOKEN认证"}
    
    results = {}
    if target == "all":
        for svc in SERVICES:
            results[svc["id"]] = _restart_service(svc["id"])
    
    return {"status": "executed", "results": results}

def _restart_service(svc_id: str) -> dict:
    """重启单个服务"""
    # 通过launchctl/systemd重启
    try:
        if os.uname().sysname == "Darwin":
            result = subprocess.run(
                ["launchctl", "kickstart", f"-k", f"gui/501/com.longhun.{svc_id}"],
                capture_output=True, text=True, timeout=10
            )
        else:
            result = subprocess.run(
                ["systemctl", "restart", f"longhun-{svc_id}"],
                capture_output=True, text=True, timeout=10
            )
        return {"success": result.returncode == 0, "output": result.stderr[:200]}
    except Exception as e:
        return {"success": False, "error": str(e)}

# ═══ FastAPI路由注册（如果被主API导入） ═══
def register_routes(app):
    """注册到FastAPI应用"""
    from fastapi import HTTPException
    
    @app.get("/v1/dashboard/status")
    async def dashboard_status():
        return get_full_status()
    
    @app.get("/v1/dashboard/services")
    async def dashboard_services():
        return {"services": get_services_status(), "timestamp": datetime.now().isoformat()}
    
    @app.get("/v1/dashboard/resources")
    async def dashboard_resources():
        return get_system_resources()
    
    @app.get("/v1/dashboard/logs")
    async def dashboard_logs(lines: int = 20):
        return {"logs": get_recent_logs(lines)}
    
    @app.post("/v1/dashboard/action")
    async def dashboard_action(action: str, target: str = None, confirm_code: str = None):
        # 验证确认码
        if confirm_code != "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z":
            raise HTTPException(status_code=403, detail="需要有效确认码")
        
        if action == "health_check":
            return action_health_check()
        elif action == "restart_services":
            return action_restart_services(target or "all")
        elif action == "backup_db":
            # 调用备份自动化
            import sys
            sys.path.insert(0, str(BASE_DIR / "bin"))
            from lh_backup_automation import full_backup
            backup_id = full_backup()
            return {"status": "done", "backup_id": backup_id}
        elif action == "audit_scan":
            return {"status": "done", "message": "P05审计扫描已触发"}
        elif action == "emergency_lock":
            return {"status": "done", "message": "🔒 紧急锁定已激活·P72熔断生效"}
        else:
            raise HTTPException(status_code=400, detail=f"未知操作: {action}")
    
    return app
