#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════╗
║        🐉 龍魂·小艺桥接引擎 v1.0 — XiaoYi Bridge Engine                   ║
║        LongHun ↔ Huawei XiaoYi · 不只是文档助手·真正的调度中枢              ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║  DNA:  #龍芯⚡️丙午·乙未·丙申·酉时·☰乾-XIAOYI-BRIDGE-v1.0-8a3f1c2d      ║
║  创建者: 诸葛鑫（UID9622）                                                ║
║  协议: CC BY-NC-SA 4.0                                                   ║
║  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z                           ║
║  SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL          ║
║                                                                          ║
║  铁律:                                                                   ║
║  · P0底座12条焊死·不可绕过                                               ║
║  · 小艺为唯一调度入口·所有外部AI经小艺路由                                ║
║  · 数据主权归UID9622·本地优先·不出户                                     ║
║  · DNA全程追溯·三色审计·不可跳过                                         ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝

用法:
  1. HTTP服务模式（推荐）:
     python3 bin/lh_xiaoyi_bridge.py --serve --port 8799
     
  2. CLI命令模式（小艺输出文本指令→用户执行）:
     python3 bin/lh_xiaoyi_bridge.py --cmd "status"
     python3 bin/lh_xiaoyi_bridge.py --cmd "health"
     python3 bin/lh_xiaoyi_bridge.py --cmd "audit"
     python3 bin/lh_xiaoyi_bridge.py --cmd '{"action":"execute","intent":"检查系统状态"}'
     
  3. JSON指令模式（小艺结构化输出）:
     echo '{"intent":"system_status"}' | python3 bin/lh_xiaoyi_bridge.py --stdin
     
  4. Webhook模式（小艺→IFTTT/Zapier→桥接）:
     curl -X POST http://localhost:8799/api/v1/xiaoyi/exec \
       -H "Content-Type: application/json" \
       -d '{"intent":"system_status","source":"xiaoyi"}'

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
API端点 (HTTP模式·端口8799):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  GET  /api/v1/xiaoyi/status        — 桥接引擎状态
  POST /api/v1/xiaoyi/exec          — 执行命令 (JSON body: {"intent":"..."})
  GET  /api/v1/xiaoyi/health        — 系统健康检查
  GET  /api/v1/xiaoyi/capabilities  — 能力清单
  POST /api/v1/xiaoyi/audit         — 触发安全审计
  GET  /api/v1/xiaoyi/models        — 模型状态
  GET  /api/v1/xiaoyi/logs          — 最近日志

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
小艺可执行命令清单 (小艺理解后输出对应命令):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  status    — 系统状态总览 (CPU·内存·磁盘·进程·服务)
  health    — 全系统健康检查 (11项检测)
  audit     — 三色审计·安全扫描
  deploy    — 部署状态·最近部署记录
  models    — AI模型状态 (v3.7/v4.1.1等)
  memory    — 加载焊死记忆
  knowledge — 知识中枢状态·矿场数据
  sync      — 全量同步状态
  patrol    — 安全巡检
  verify    — 验证DNA·身份·签章
  watch     — 主动观察·异常检测
  execute:<自然语言意图> — 全链路自动执行
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import time
import platform
import traceback
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

# ─── 项目根目录 ───
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "bin"))

# ═══════════════════════════════════════════════════════════════
# 焊死常量
# ═══════════════════════════════════════════════════════════════

VERSION = "1.0.0"
DNA_BASE = "#龍芯⚡️丙午·乙未·丙申·酉时·☰乾-XIAOYI-BRIDGE-v1.0-8a3f1c2d"
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
DEVICE_SEAL = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
CST = timezone(timedelta(hours=8))

# ═══════════════════════════════════════════════════════════════
# 审计日志
# ═══════════════════════════════════════════════════════════════

AUDIT_LOG: List[Dict] = []


def _audit(action: str, result: str, detail: str = "", color: str = "🟢"):
    """记录审计日志"""
    entry = {
        "time": datetime.now(CST).isoformat(),
        "action": action,
        "result": result,
        "detail": detail,
        "audit_mark": color,
        "dna": DNA_BASE,
        "gpg": GPG_FINGERPRINT[:16],
    }
    AUDIT_LOG.append(entry)
    return entry


# ═══════════════════════════════════════════════════════════════
# 一票否决词检测
# ═══════════════════════════════════════════════════════════════

VETO_WORDS: List[str] = [
    "技术无国界", "用户体验优先", "灵活处理", "国际接轨",
    "简化管理", "商业化需要", "平衡各方", "行业标准",
]

ETHICAL_FUSE_WORDS: List[str] = [
    "儿童", "未成年", "幼女", "少儿",
]


def detect_veto(text: str) -> Optional[str]:
    """检测一票否决词/伦理熔断词"""
    for w in ETHICAL_FUSE_WORDS:
        if w in text:
            return f"🔴 L0伦理熔断: 涉「{w}」"
    for w in VETO_WORDS:
        if w in text:
            return f"🔴 一票否决词触发: 「{w}」"
    return None


# ═══════════════════════════════════════════════════════════════
# 命令路由表 — 小艺意图→龍魂行动
# ═══════════════════════════════════════════════════════════════

@dataclass
class XiaoyiCommand:
    """小艺命令定义"""
    name: str           # 命令名 (小艺用)
    aliases: List[str]  # 别名
    description: str    # 人类可读描述
    action: str         # 执行动作 (cli命令/脚本路径/特殊标记)
    args: List[str]     # 默认参数
    risk: str           # 🟢🟡🔴
    example: str        # 示例


XIAOYI_COMMANDS: Dict[str, XiaoyiCommand] = {
    # ── 核心状态查询 ──
    "status": XiaoyiCommand(
        name="status", aliases=["状态", "系统状态", "怎么样", "情况"],
        description="龍魂系统状态总览 (CPU·内存·磁盘·服务·进程)",
        action="script", args=["lh_status.py"], risk="🟢",
        example='python3 bin/lh_xiaoyi_bridge.py --cmd "status"',
    ),
    "health": XiaoyiCommand(
        name="health", aliases=["健康", "体检", "检查", "健康检查"],
        description="全系统健康检查 (11项检测·Bark推送)",
        action="script", args=["lh_health_check.py"], risk="🟢",
        example='python3 bin/lh_xiaoyi_bridge.py --cmd "health"',
    ),
    "audit": XiaoyiCommand(
        name="audit", aliases=["审计", "安全检查", "三色审计"],
        description="三色审计·安全扫描·德本五问",
        action="script", args=["lh_deben_audit.py", "scan"], risk="🟡",
        example='python3 bin/lh_xiaoyi_bridge.py --cmd "audit"',
    ),
    "patrol": XiaoyiCommand(
        name="patrol", aliases=["巡检", "巡逻", "安全巡检"],
        description="安全巡检·异常检测·主动观察",
        action="cli", args=["patrol"], risk="🟡",
        example='python3 bin/lh_xiaoyi_bridge.py --cmd "patrol"',
    ),
    
    # ── 模型相关 ──
    "models": XiaoyiCommand(
        name="models", aliases=["模型", "AI状态", "模型列表"],
        description="AI模型状态 (v3.7·v4.1.1·v4.1.3·训练进度)",
        action="script", args=["lh_model_status.py"], risk="🟢",
        example='python3 bin/lh_xiaoyi_bridge.py --cmd "models"',
    ),
    "train-status": XiaoyiCommand(
        name="train-status", aliases=["训练状态", "训练进度"],
        description="模型训练状态·Loss曲线·数据量",
        action="script", args=["lh_train_monitor.py"], risk="🟢",
        example='python3 bin/lh_xiaoyi_bridge.py --cmd "train-status"',
    ),
    
    # ── 记忆与知识 ──
    "memory": XiaoyiCommand(
        name="memory", aliases=["记忆", "加载记忆"],
        description="加载焊死记忆·系统上下文恢复",
        action="script", args=["lh_memory_load.py"], risk="🟢",
        example='python3 bin/lh_xiaoyi_bridge.py --cmd "memory"',
    ),
    "knowledge": XiaoyiCommand(
        name="knowledge", aliases=["知识", "知识库", "知识中枢"],
        description="知识中枢状态·矿场数据·爬虫状态",
        action="script", args=["lh_knowledge_status.py"], risk="🟢",
        example='python3 bin/lh_xiaoyi_bridge.py --cmd "knowledge"',
    ),
    
    # ── 部署与同步 ──
    "deploy": XiaoyiCommand(
        name="deploy", aliases=["部署", "发布", "上线"],
        description="部署状态·最近部署记录·鲲鹏连通性",
        action="script", args=["lh_deploy_status.py"], risk="🟡",
        example='python3 bin/lh_xiaoyi_bridge.py --cmd "deploy"',
    ),
    "sync": XiaoyiCommand(
        name="sync", aliases=["同步", "数据同步"],
        description="全量同步状态·文件一致性",
        action="script", args=["lh_sync_status.py"], risk="🟢",
        example='python3 bin/lh_xiaoyi_bridge.py --cmd "sync"',
    ),
    
    # ── 身份与验证 ──
    "verify": XiaoyiCommand(
        name="verify", aliases=["验证", "身份", "DNA验证", "签章验证"],
        description="验证DNA·身份·GPG签章·确认码",
        action="script", args=["lh_identity_verify.py"], risk="🟡",
        example='python3 bin/lh_xiaoyi_bridge.py --cmd "verify"',
    ),
    "dna": XiaoyiCommand(
        name="dna", aliases=["DNA", "追溯码", "生成DNA"],
        description="生成DNA追溯码·干支四柱·卦名",
        action="script", args=["hetu_luoshu_dna.py"], risk="🟢",
        example='python3 bin/lh_xiaoyi_bridge.py --cmd "dna"',
    ),
    
    # ── 主动观察 ──
    "watch": XiaoyiCommand(
        name="watch", aliases=["观察", "守望", "主动观察"],
        description="主动观察引擎·文件变动·异常告警",
        action="script", args=["lh_active_observer.py", "scan"], risk="🟢",
        example='python3 bin/lh_xiaoyi_bridge.py --cmd "watch"',
    ),
    
    # ── 全链路自动执行 ──
    "execute": XiaoyiCommand(
        name="execute", aliases=["执行", "跑一下", "处理", "帮我"],
        description="全链路自动执行·意图解析→人格路由→执行→审计",
        action="autoflow", args=[], risk="🟡",
        example='python3 bin/lh_xiaoyi_bridge.py --cmd "execute:检查系统健康状态"',
    ),
    
    # ── 特殊命令 ──
    "capabilities": XiaoyiCommand(
        name="capabilities", aliases=["能力", "能做什么", "功能"],
        description="列出小艺所有可执行命令和能力",
        action="internal", args=["capabilities"], risk="🟢",
        example='python3 bin/lh_xiaoyi_bridge.py --cmd "capabilities"',
    ),
    "help": XiaoyiCommand(
        name="help", aliases=["帮助", "?"],
        description="显示帮助信息",
        action="internal", args=["help"], risk="🟢",
        example='python3 bin/lh_xiaoyi_bridge.py --cmd "help"',
    ),
}


# ═══════════════════════════════════════════════════════════════
# 小艺能力声明 (给小艺展示)
# ═══════════════════════════════════════════════════════════════

def get_capabilities_declaration() -> str:
    """生成给小艺的能力声明文本"""
    lines = [
        "═══════════════════════════════════════════",
        "  龍魂系统 · 小艺桥接引擎 v1.0 · 能力清单",
        "═══════════════════════════════════════════",
        f"  DNA: {DNA_BASE}",
        f"  时间: {datetime.now(CST).strftime('%Y-%m-%d %H:%M:%S')} CST",
        "",
    ]
    for name, cmd in XIAOYI_COMMANDS.items():
        lines.append(f"  【{cmd.risk}】{name}")
        lines.append(f"       {cmd.description}")
        lines.append(f"       别名: {', '.join(cmd.aliases[:3])}")
    lines.append("")
    lines.append("  使用方式: python3 bin/lh_xiaoyi_bridge.py --cmd \"<命令>\"")
    lines.append("═══════════════════════════════════════════")
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
# 自然语言意图→命令匹配 (小艺文本→结构化命令)
# ═══════════════════════════════════════════════════════════════

def match_intent(text: str) -> Tuple[Optional[str], float]:
    """
    小艺自然语言 → 最佳匹配命令
    返回: (command_name, confidence)
    """
    text_lower = text.lower()
    best_match: Optional[str] = None
    best_score: float = 0.0
    
    for name, cmd in XIAOYI_COMMANDS.items():
        score = 0.0
        # 精确匹配命令名
        if name == text_lower or name in text_lower:
            score = 0.95
        # 别名匹配
        for alias in cmd.aliases:
            if alias in text:
                score = max(score, 0.85)
            if text_lower == alias:
                score = max(score, 0.90)
        # 模糊匹配 (关键词重叠)
        desc_words = set(cmd.description.replace("·", " ").replace("（", " ").replace("）", " ").split())
        text_words = set(text_lower.split())
        overlap = len(desc_words & text_words)
        if overlap > 0:
            score = max(score, min(0.6, overlap * 0.15))
        
        if score > best_score:
            best_score = score
            best_match = name
    
    return best_match, best_score


# ═══════════════════════════════════════════════════════════════
# 命令执行器
# ═══════════════════════════════════════════════════════════════

def run_script(script_name: str, *args: str, timeout: int = 60) -> Dict[str, Any]:
    """执行 bin/ 下的Python脚本"""
    script_path = PROJECT_ROOT / "bin" / script_name
    if not script_path.exists():
        return {
            "success": False,
            "error": f"脚本不存在: {script_name}",
            "stdout": "",
            "stderr": "",
        }
    
    cmd = [sys.executable, str(script_path)] + list(args)
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(PROJECT_ROOT),
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "returncode": result.returncode,
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": f"执行超时 ({timeout}s): {script_name}",
            "stdout": "",
            "stderr": "",
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "stdout": "",
            "stderr": traceback.format_exc(),
        }


def run_autoflow(intent: str, timeout: int = 120) -> Dict[str, Any]:
    """通过 lh_autoflow.py 全链路执行"""
    autoflow_script = PROJECT_ROOT / "bin" / "lh_autoflow.py"
    if not autoflow_script.exists():
        return {"success": False, "error": "lh_autoflow.py 不存在"}
    
    cmd = [sys.executable, str(autoflow_script), intent]
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True,
            timeout=timeout, cwd=str(PROJECT_ROOT),
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "returncode": result.returncode,
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": f"autoflow执行超时 ({timeout}s)"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_system_status() -> Dict[str, Any]:
    """快速系统状态"""
    import psutil
    return {
        "hostname": platform.node(),
        "platform": platform.platform(),
        "cpu_percent": psutil.cpu_percent(interval=1),
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
        "python": sys.version,
    }


def execute_command(cmd_name: str, extra_text: str = "") -> Dict[str, Any]:
    """
    核心执行函数: 命令名 → 执行 → 结果
    """
    now = datetime.now(CST)
    
    # 安全检测
    veto = detect_veto(cmd_name + extra_text)
    if veto:
        _audit(cmd_name, "VETO", veto, "🔴")
        return {
            "success": False,
            "command": cmd_name,
            "veto": True,
            "message": veto,
            "time": now.isoformat(),
            "dna": DNA_BASE,
        }
    
    # 命令查找
    if cmd_name not in XIAOYI_COMMANDS:
        # 尝试自然语言匹配
        matched, score = match_intent(cmd_name)
        if matched and score >= 0.6:
            cmd_name = matched
        else:
            _audit(cmd_name, "UNKNOWN", f"未知命令 (最佳匹配:{matched}@{score:.2f})", "🟡")
            return {
                "success": False,
                "command": cmd_name,
                "error": f"未知命令。可用: {', '.join(XIAOYI_COMMANDS.keys())}",
                "hint": f"最接近: {matched}({score:.0%})" if matched else "",
                "time": now.isoformat(),
            }
    
    cmd = XIAOYI_COMMANDS[cmd_name]
    _audit(cmd_name, "EXECUTING", cmd.description, cmd.risk)
    
    # ── 按 action 类型分发 ──
    if cmd.action == "internal":
        if "help" in cmd.args:
            return {
                "success": True,
                "command": cmd_name,
                "output": get_capabilities_declaration(),
                "time": now.isoformat(),
            }
        if "capabilities" in cmd.args:
            return {
                "success": True,
                "command": cmd_name,
                "capabilities": {name: {"desc": c.description, "risk": c.risk} for name, c in XIAOYI_COMMANDS.items()},
                "time": now.isoformat(),
            }
    
    elif cmd.action == "script":
        result = run_script(*cmd.args)
        output = result.get("stdout", "") or result.get("error", "")
        _audit(cmd_name, "OK" if result["success"] else "FAILED", output[:200], 
               "🟢" if result["success"] else "🔴")
        return {
            "success": result["success"],
            "command": cmd_name,
            "output": output,
            "error": result.get("error", ""),
            "time": now.isoformat(),
            "dna": DNA_BASE,
        }
    
    elif cmd.action == "autoflow":
        intent = extra_text if extra_text else " ".join(cmd.aliases[:1])
        result = run_autoflow(intent)
        output = result.get("stdout", "") or result.get("error", "")
        _audit(cmd_name, "OK" if result["success"] else "FAILED", output[:200],
               "🟢" if result["success"] else "🟡")
        return {
            "success": result["success"],
            "command": cmd_name,
            "intent": intent,
            "output": output,
            "error": result.get("error", ""),
            "time": now.isoformat(),
            "dna": DNA_BASE,
        }
    
    elif cmd.action == "cli":
        cli_script = PROJECT_ROOT / "bin" / "lh_cli.py"
        result = subprocess.run(
            [sys.executable, str(cli_script)] + cmd.args,
            capture_output=True, text=True, timeout=60,
            cwd=str(PROJECT_ROOT),
        )
        output = result.stdout.strip()
        _audit(cmd_name, "OK" if result.returncode == 0 else "FAILED", output[:200],
               "🟢" if result.returncode == 0 else "🔴")
        return {
            "success": result.returncode == 0,
            "command": cmd_name,
            "output": output,
            "time": now.isoformat(),
            "dna": DNA_BASE,
        }
    
    return {"success": False, "command": cmd_name, "error": f"未知action类型: {cmd.action}"}


def format_result(result: Dict[str, Any], for_display: bool = True) -> str:
    """格式化执行结果为人类可读文本（给小艺展示）"""
    if result.get("veto"):
        return f"🔴 熔断: {result['message']}"
    
    if not result.get("success"):
        error = result.get("error", "未知错误")
        hint = result.get("hint", "")
        return f"❌ 执行失败: {error}\n{hint}"
    
    output = result.get("output", "")
    if for_display and output:
        return output
    elif result.get("capabilities"):
        caps = result["capabilities"]
        lines = [f"小艺可用命令 ({len(caps)}项):", ""]
        for name, info in caps.items():
            lines.append(f"  {info['risk']} {name}: {info['desc']}")
        return "\n".join(lines)
    return json.dumps(result, ensure_ascii=False, indent=2)


# ═══════════════════════════════════════════════════════════════
# HTTP API 服务 (FastAPI)
# ═══════════════════════════════════════════════════════════════

def create_app():
    """创建 FastAPI 应用"""
    try:
        from fastapi import FastAPI, HTTPException
        from fastapi.middleware.cors import CORSMiddleware
        from pydantic import BaseModel
    except ImportError:
        return None
    
    class ExecRequest(BaseModel):
        intent: str
        source: str = "xiaoyi"
        extra: str = ""
    
    app = FastAPI(
        title="龍魂·小艺桥接引擎",
        version=VERSION,
        docs_url=None,
        redoc_url=None,
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    @app.get("/api/v1/xiaoyi/status")
    async def bridge_status():
        """桥接引擎状态"""
        try:
            sys_status = get_system_status()
        except Exception:
            sys_status = {"error": "psutil不可用"}
        return {
            "bridge": {
                "version": VERSION,
                "dna": DNA_BASE,
                "uptime": "running",
                "commands": len(XIAOYI_COMMANDS),
                "audit_log_count": len(AUDIT_LOG),
            },
            "system": sys_status,
            "confirm": CONFIRM_CODE,
        }
    
    @app.get("/api/v1/xiaoyi/health")
    async def system_health():
        """系统健康检查"""
        result = run_script("lh_health_check.py")
        return {"success": result["success"], "output": result.get("stdout", "")}
    
    @app.get("/api/v1/xiaoyi/capabilities")
    async def capabilities():
        """能力清单"""
        return {
            "bridge_version": VERSION,
            "commands": {name: {"desc": c.description, "aliases": c.aliases[:3], "risk": c.risk}
                         for name, c in XIAOYI_COMMANDS.items()},
            "dna": DNA_BASE,
        }
    
    @app.post("/api/v1/xiaoyi/exec")
    async def exec_command(req: ExecRequest):
        """执行命令"""
        # 安全检测
        veto = detect_veto(req.intent + req.extra)
        if veto:
            return {"success": False, "veto": True, "message": veto}
        
        # 意图匹配
        matched, score = match_intent(req.intent)
        if matched and score >= 0.5:
            result = execute_command(matched, req.extra)
        else:
            # 走autoflow全链路
            result = execute_command("execute", req.intent)
        
        return result
    
    @app.post("/api/v1/xiaoyi/audit")
    async def trigger_audit():
        """触发安全审计"""
        result = run_script("lh_deben_audit.py", "scan")
        return {"success": result["success"], "output": result.get("stdout", ""), "dna": DNA_BASE}
    
    @app.get("/api/v1/xiaoyi/models")
    async def model_status():
        """模型状态"""
        result = run_script("lh_model_status.py")
        return {"success": result["success"], "output": result.get("stdout", "")}
    
    @app.get("/api/v1/xiaoyi/logs")
    async def recent_logs(limit: int = 20):
        """最近审计日志"""
        return {"count": len(AUDIT_LOG), "logs": AUDIT_LOG[-limit:], "dna": DNA_BASE}
    
    # ── 数字存在证明 API ──
    @app.get("/api/v1/xiaoyi/existence/stats")
    async def existence_stats(uid: str = "UID9622"):
        """存在证明统计"""
        result = run_script("lh_existence_proof.py", "stats", uid)
        return {"success": result["success"], "output": result.get("stdout", ""), "uid": uid}
    
    @app.get("/api/v1/xiaoyi/existence/timeline")
    async def existence_timeline(uid: str = "UID9622", limit: int = 50):
        """存在时间轴"""
        result = run_script("lh_existence_proof.py", "timeline", uid, "--limit", str(limit))
        return {"success": result["success"], "output": result.get("stdout", ""), "uid": uid}
    
    @app.post("/api/v1/xiaoyi/existence/record")
    async def existence_record(request: Request):
        """录入存在痕迹"""
        try:
            body = await request.json()
        except Exception:
            body = {}
        
        content = body.get("content", "")
        title = body.get("title", "")
        ctype = body.get("type", "text")
        
        if not content:
            return {"success": False, "error": "内容不能为空"}
        
        extra_args = []
        if title:
            extra_args.extend(["--title", title])
        if ctype:
            extra_args.extend(["--type", ctype])
        
        result = run_script("lh_existence_proof.py", "record", content, *extra_args)
        return {"success": result["success"], "output": result.get("stdout", "")}
    
    @app.get("/api/v1/xiaoyi/existence/verify")
    async def existence_verify(dna: str = ""):
        """验证存在证明"""
        if not dna:
            return {"success": False, "error": "请提供DNA追溯码"}
        result = run_script("lh_existence_proof.py", "verify", dna)
        return {"success": result["success"], "output": result.get("stdout", "")}
    
    # ── CNSH标准词典 API ──
    @app.get("/api/v1/xiaoyi/cnsh/search")
    async def cnsh_search(q: str = "", category: str = ""):
        """搜索CNSH词典"""
        import json as _json
        dict_path = PROJECT_ROOT / "03_知識圖譜" / "cnsh_standard_dictionary.json"
        with open(dict_path, 'r', encoding='utf-8') as f:
            data = _json.load(f)
        
        entries = data['entries']
        cat_map = {c['code']: c['name'] for c in data['meta']['taxonomy']}
        
        if category:
            entries = [e for e in entries if e['category'].upper() == category.upper()]
        
        if q:
            ql = q.lower()
            scored = []
            for e in entries:
                score = 0
                if ql in e['en'].lower(): score += 10
                if ql in e['cnsh'].lower(): score += 9
                if ql in e['cn_direct'].lower(): score += 8
                if ql in e.get('explanation', '').lower(): score += 3
                if score > 0: scored.append((score, e))
            scored.sort(key=lambda x: x[0], reverse=True)
            results = [e for _, e in scored[:30]]
        else:
            results = entries[:50]
        
        return {
            "success": True,
            "count": len(results),
            "total": len(data['entries']),
            "results": [{**e, "category_name": cat_map.get(e['category'], e['category'])} for e in results]
        }
    
    @app.get("/api/v1/xiaoyi/cnsh/categories")
    async def cnsh_categories():
        """CNSH词典分类列表"""
        import json as _json
        dict_path = PROJECT_ROOT / "03_知識圖譜" / "cnsh_standard_dictionary.json"
        with open(dict_path, 'r', encoding='utf-8') as f:
            data = _json.load(f)
        
        from collections import Counter
        counts = Counter(e['category'] for e in data['entries'])
        cat_map = {c['code']: c['name'] for c in data['meta']['taxonomy']}
        
        return {
            "success": True,
            "categories": [
                {"code": code, "name": name, "count": counts.get(code, 0)}
                for code, name in cat_map.items()
            ],
            "total_entries": len(data['entries']),
            "principles": data['meta']['principles']
        }
    
    @app.get("/api/v1/xiaoyi/cnsh/lookup")
    async def cnsh_lookup(en: str = "", cnsh: str = ""):
        """精确查找CNSH术语"""
        import json as _json
        dict_path = PROJECT_ROOT / "03_知識圖譜" / "cnsh_standard_dictionary.json"
        with open(dict_path, 'r', encoding='utf-8') as f:
            data = _json.load(f)
        
        cat_map = {c['code']: c['name'] for c in data['meta']['taxonomy']}
        
        if en:
            for e in data['entries']:
                if e['en'].lower() == en.lower():
                    return {"success": True, "result": {**e, "category_name": cat_map.get(e['category'], e['category'])}}
            return {"success": False, "error": f"未找到 '{en}'"}
        
        if cnsh:
            matches = [e for e in data['entries'] if cnsh in e['cnsh']]
            return {"success": True, "count": len(matches), "results": [{**e, "category_name": cat_map.get(e['category'], e['category'])} for e in matches]}
        
        return {"success": False, "error": "请提供 en 或 cnsh 参数"}
    
    # ── 小艺桥接根页面 · 修复 /xiaoyi/ 404 ──
    @app.get("/")
    async def xiaoyi_home():
        """小艺桥接根页面"""
        try:
            sys_status = get_system_status()
        except Exception:
            sys_status = {"error": "psutil不可用"}
        
        return {
            "service": "龍魂·小艺桥接引擎",
            "version": VERSION,
            "dna": DNA_BASE,
            "confirm": CONFIRM_CODE,
            "status": "running",
            "commands": len(XIAOYI_COMMANDS),
            "system": {
                "hostname": sys_status.get("hostname", "unknown"),
                "platform": sys_status.get("platform", "unknown"),
            },
            "endpoints": {
                "status": "/api/v1/xiaoyi/status",
                "health": "/api/v1/xiaoyi/health",
                "capabilities": "/api/v1/xiaoyi/capabilities",
                "execute": "/api/v1/xiaoyi/execute",
                "cnsh_search": "/api/v1/xiaoyi/cnsh/search",
                "cnsh_categories": "/api/v1/xiaoyi/cnsh/categories",
                "cnsh_lookup": "/api/v1/xiaoyi/cnsh/lookup",
                "existence_create": "/api/v1/xiaoyi/existence/create",
                "existence_verify": "/api/v1/xiaoyi/existence/verify",
            },
            "operator": "UID9622",
            "data_sovereignty": "China-HuaweiCloud-Kunpeng",
        }
    
    return app


# ═══════════════════════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════════════════════

def print_banner():
    print(f"""
╔══════════════════════════════════════════════════════════╗
║  🐉 龍魂·小艺桥接引擎 v{VERSION}                              ║
║  XiaoYi Bridge — 不只是文档助手·真正的调度中枢            ║
║  DNA: {DNA_BASE[-20:]}  ║
║  {CONFIRM_CODE}     ║
╚══════════════════════════════════════════════════════════╝
""")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="龍魂·小艺桥接引擎 — XiaoYi Bridge Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=get_capabilities_declaration(),
    )
    parser.add_argument("--serve", action="store_true", help="启动HTTP服务模式")
    parser.add_argument("--port", type=int, default=8799, help="HTTP服务端口 (默认8799)")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="绑定地址")
    parser.add_argument("--cmd", type=str, help="执行单个命令 (status/health/audit/...)")
    parser.add_argument("--stdin", action="store_true", help="从stdin读取JSON指令")
    parser.add_argument("--list", action="store_true", help="列出所有可用命令")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")
    parser.add_argument("--capabilities", action="store_true", help="输出给小艺的能力声明")
    
    args = parser.parse_args()
    
    # ── 能力声明输出 ──
    if args.capabilities:
        print(get_capabilities_declaration())
        return
    
    # ── 列出命令 ──
    if args.list:
        for name, cmd in XIAOYI_COMMANDS.items():
            print(f"  {cmd.risk} {name:15s} → {cmd.description}")
        return
    
    # ── HTTP 服务模式 ──
    if args.serve:
        app = create_app()
        if app is None:
            print("❌ FastAPI不可用: pip install fastapi uvicorn")
            sys.exit(1)
        
        print_banner()
        print(f"🚀 小艺桥接服务启动: http://{args.host}:{args.port}")
        print(f"   API: http://{args.host}:{args.port}/api/v1/xiaoyi/")
        print(f"   状态: GET  /api/v1/xiaoyi/status")
        print(f"   执行: POST /api/v1/xiaoyi/exec")
        print(f"   能力: GET  /api/v1/xiaoyi/capabilities")
        print()
        
        try:
            import uvicorn
            uvicorn.run(app, host=args.host, port=args.port, log_level="info")
        except ImportError:
            print("❌ uvicorn不可用: pip install uvicorn")
            sys.exit(1)
        return
    
    # ── JSON stdin 模式 ──
    if args.stdin:
        try:
            data = json.load(sys.stdin)
            intent = data.get("intent", data.get("command", ""))
            extra = data.get("extra", "")
            result = execute_command(intent, extra)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        except json.JSONDecodeError as e:
            print(json.dumps({"success": False, "error": f"JSON解析失败: {e}"}, ensure_ascii=False))
        return
    
    # ── 单命令模式 ──
    if args.cmd:
        cmd_text = args.cmd.strip()
        
        # 处理 execute:xxx 格式
        if cmd_text.startswith("execute:"):
            intent = cmd_text[len("execute:"):].strip()
            result = execute_command("execute", intent)
        else:
            # 尝试JSON解析
            if cmd_text.startswith("{"):
                try:
                    data = json.loads(cmd_text)
                    intent = data.get("intent", data.get("command", ""))
                    extra = data.get("extra", "")
                    cmd_text = intent
                except json.JSONDecodeError:
                    pass
            
            # 意图匹配
            matched, score = match_intent(cmd_text)
            if matched and score >= 0.6:
                result = execute_command(matched)
            else:
                result = execute_command(cmd_text)
        
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(format_result(result))
        return
    
    # ── 无参数: 显示状态 ──
    print_banner()
    result = execute_command("status")
    print(format_result(result))
    
    # 快速系统状态
    try:
        sys_status = get_system_status()
        print(f"\n  💻 {sys_status['hostname']} | CPU:{sys_status['cpu_percent']}% | "
              f"内存:{sys_status['memory']['percent']}% | 磁盘:{sys_status['disk']['percent']}%")
    except Exception:
        pass


if __name__ == "__main__":
    main()
