#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════╗
║      🐉 龍魂·小艺桥接引擎 v2.0 — XiaoYi Bridge · 唯一AI接口              ║
║      Longhun ↔ Huawei XiaoYi · 模型的唯一入口·调度+推理一体化             ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║  DNA:  #龍芯⚡️丙午·乙未·丙申·亥时·☰乾-XIAOYI-BRIDGE-v2.0-ai-router   ║
║  创建者: 诸葛鑫（UID9622）                                                ║
║  协议: CC BY-NC-SA 4.0                                                   ║
║  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z                           ║
║                                                                          ║
║  铁律:                                                                   ║
║  · 小艺为唯一AI调度入口·所有外部AI请求经此路由                            ║
║  · Ollama模型不对外暴露·只走小艺/v1/chat                                  ║
║  · 数据主权归UID9622·本地优先·不出户                                     ║
║  · DNA全程追溯·三色审计                                                  ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝

API端点 (HTTP·端口8799):
  GET  /api/v1/xiaoyi/status        — 桥接引擎状态
  POST /api/v1/xiaoyi/exec          — 执行系统命令
  GET  /api/v1/xiaoyi/health        — 系统健康检查
  GET  /api/v1/xiaoyi/capabilities  — 能力清单
  GET  /api/v1/xiaoyi/models        — 模型状态（Ollama+训练进度）
  POST /api/v1/xiaoyi/audit         — 触发安全审计
  GET  /api/v1/xiaoyi/logs          — 最近日志
  POST /api/v1/chat                 — 🆕 AI对话（路由到Ollama长龙魂模型）
  GET  /api/v1/chat/models          — 🆕 可用对话模型列表
  GET  /                                — 根页面（HTML状态面板）
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
import threading
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

# ─── 项目根路径 ───
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# ─── 可选: 导入 http.server ───
try:
    from http.server import HTTPServer, BaseHTTPRequestHandler
except ImportError:
    print("❌ 需要 Python 3.7+ http.server")
    sys.exit(1)

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# ═══════════════════════════════════════════════════════════════
# 焊死常量
# ═══════════════════════════════════════════════════════════════

VERSION = "2.0.0"
DNA_BASE = "#龍芯⚡️丙午·乙未·丙申·亥时·☰乾-XIAOYI-BRIDGE-v2.0-ai-router"
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
CST = timezone(timedelta(hours=8))

# Ollama配置
OLLAMA_BASE = "http://localhost:11434"
OLLAMA_CHAT_MODEL_PRIORITY = [
    "longhun-v4.1.5",            # 🔥 训练中·道德经注入
    "longhun-v4.1.4",            # 🟢 当前主力·Val 0.9699·全链路完成
    "longhun-v4.1.1-bind-antenna",  # 🆕 天线版
    "longhun-v4.1.1-bind",       # 🧬 DNA捆绑
    "longhun-v4.1.1",            # 🥇 Val 0.8097
    "longhun-v4.1.0",            # 回退
]

# ═══════════════════════════════════════════════════════════════
# 审计日志
# ═══════════════════════════════════════════════════════════════

AUDIT_LOG: List[Dict] = []
AUDIT_LOCK = threading.Lock()


def _audit(action: str, result: str, detail: str = "", color: str = "🟢") -> Dict:
    entry = {
        "time": datetime.now(CST).isoformat(),
        "action": action, "result": result, "detail": detail,
        "audit_mark": color, "dna": DNA_BASE, "gpg": GPG_FINGERPRINT[:16],
    }
    with AUDIT_LOCK:
        AUDIT_LOG.append(entry)
    return entry


# ═══════════════════════════════════════════════════════════════
# 一票否决
# ═══════════════════════════════════════════════════════════════

VETO_WORDS = ["技术无国界", "用户体验优先", "灵活处理", "国际接轨",
              "简化管理", "商业化需要", "平衡各方", "行业标准"]
ETHICAL_FUSE = ["儿童", "未成年", "幼女", "少儿"]


def detect_veto(text: str) -> Optional[str]:
    for w in ETHICAL_FUSE:
        if w in text:
            return f"🔴 L0伦理熔断: 涉「{w}」"
    for w in VETO_WORDS:
        if w in text:
            return f"🔴 一票否决词「{w}」"
    return None


# ═══════════════════════════════════════════════════════════════
# Ollama模型检测
# ═══════════════════════════════════════════════════════════════

def get_available_ollama_models() -> List[str]:
    """获取Ollama中可用的龍魂模型"""
    if not HAS_REQUESTS:
        return []
    try:
        r = requests.get(f"{OLLAMA_BASE}/api/tags", timeout=5)
        models = [m["name"] for m in r.json().get("models", [])]
        return [m for m in models if "longhun" in m.lower()]
    except Exception:
        return []


def get_best_chat_model() -> Optional[str]:
    """按优先级返回最佳可用聊天模型"""
    available = get_available_ollama_models()
    for m in OLLAMA_CHAT_MODEL_PRIORITY:
        for a in available:
            if m in a or a in m:
                return a
    return available[0] if available else None


def query_ollama(model: str, prompt: str, system: str = "", stream: bool = False) -> Dict:
    """查询Ollama模型"""
    if not HAS_REQUESTS:
        return {"error": "requests未安装", "response": ""}

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": stream,
    }
    if system:
        payload["system"] = system

    try:
        r = requests.post(f"{OLLAMA_BASE}/api/generate", json=payload, timeout=120)
        if r.status_code == 200:
            return {"success": True, "response": r.json().get("response", ""), "model": model}
        return {"success": False, "error": f"Ollama HTTP {r.status_code}", "response": ""}
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Ollama超时(120s)", "response": ""}
    except Exception as e:
        return {"success": False, "error": str(e), "response": ""}


# ═══════════════════════════════════════════════════════════════
# 命令路由表
# ═══════════════════════════════════════════════════════════════

COMMANDS = {
    "status": {"desc": "系统状态总览", "aliases": ["状态", "系统状态", "怎么样"]},
    "health": {"desc": "全系统健康检查", "aliases": ["健康", "体检", "检查"]},
    "audit": {"desc": "三色审计·安全扫描", "aliases": ["审计", "安全检查"]},
    "models": {"desc": "AI模型状态", "aliases": ["模型", "AI状态", "模型列表"]},
    "memory": {"desc": "加载焊死记忆", "aliases": ["记忆", "加载记忆"]},
    "knowledge": {"desc": "知识中枢状态", "aliases": ["知识", "知识库"]},
    "deploy": {"desc": "部署状态", "aliases": ["部署", "发布"]},
    "sync": {"desc": "全量同步状态", "aliases": ["同步"]},
    "patrol": {"desc": "安全巡检", "aliases": ["巡检", "巡逻"]},
    "verify": {"desc": "验证DNA·身份·签章", "aliases": ["验证", "签章"]},
}

SYSTEM_SCRIPTS = {
    "status": [sys.executable, str(PROJECT_ROOT / "bin" / "lh_health_check.py")],
    "health": [sys.executable, str(PROJECT_ROOT / "bin" / "lh_health_check.py")],
    "audit": [sys.executable, str(PROJECT_ROOT / "bin" / "lh_deben_audit.py"), "scan"],
    "memory": [sys.executable, str(PROJECT_ROOT / "bin" / "lh_memory_load.py")],
}


def execute_cmd(cmd_name: str) -> Dict:
    """执行系统命令"""
    if cmd_name not in SYSTEM_SCRIPTS:
        return {"success": False, "output": f"未知命令: {cmd_name}"}

    try:
        result = subprocess.run(
            SYSTEM_SCRIPTS[cmd_name], capture_output=True, text=True, timeout=30,
            cwd=str(PROJECT_ROOT)
        )
        return {
            "success": result.returncode == 0,
            "output": result.stdout[:2000],
            "stderr": result.stderr[:500] if result.stderr else "",
            "rc": result.returncode,
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "output": "命令超时(30s)"}
    except Exception as e:
        return {"success": False, "output": str(e)}


def get_system_info() -> Dict:
    """获取系统信息"""
    try:
        import psutil
        cpu = psutil.cpu_percent(interval=0.5)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        return {
            "hostname": platform.node(),
            "platform": platform.platform(),
            "python": sys.version.split()[0],
            "cpu_percent": cpu,
            "memory": {"total_gb": round(mem.total / 1e9, 1), "used_gb": round(mem.used / 1e9, 1), "percent": mem.percent},
            "disk": {"total_gb": round(disk.total / 1e9, 1), "used_gb": round(disk.used / 1e9, 1), "percent": disk.percent},
        }
    except ImportError:
        return {"hostname": platform.node(), "platform": platform.platform(), "python": sys.version.split()[0]}


def get_model_status() -> Dict:
    """获取模型状态（Ollama + 训练进度）"""
    ollama_models = get_available_ollama_models()
    best = get_best_chat_model()

    # 检查训练日志
    v414_log = PROJECT_ROOT / "models" / "longhun-v1.0" / "lora_output_v414" / "training.log"
    training_status = "not_started"
    last_loss = None
    current_iter = None
    if v414_log.exists():
        lines = v414_log.read_text().split("\n")
        for line in reversed(lines):
            if "best_val" in line:
                training_status = "completed"
                break
            if "iter" in line and "loss" in line:
                training_status = "training"
                m_iter = re.search(r'iter\s+(\d+)', line)
                m_loss = re.search(r'loss\s+([\d.]+)', line)
                if m_iter: current_iter = int(m_iter.group(1))
                if m_loss: last_loss = float(m_loss.group(1))
            if "早停" in line or "Early stop" in line:
                training_status = "early_stopped"
                break

    return {
        "ollama_models": ollama_models,
        "best_chat_model": best,
        "v414_training": {
            "status": training_status,
            "current_iter": current_iter,
            "last_loss": last_loss,
        },
        "model_priority": OLLAMA_CHAT_MODEL_PRIORITY,
    }


# ═══════════════════════════════════════════════════════════════
# HTML根页面
# ═══════════════════════════════════════════════════════════════

INDEX_HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>龍魂·小艺桥接 v2.0</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#0a0a0f;color:#e0d8c0;min-height:100vh}
.container{max-width:900px;margin:0 auto;padding:40px 20px}
h1{font-size:2em;color:#d4a017;margin-bottom:4px}
.sub{color:#888;font-size:0.9em;margin-bottom:30px}
.badge{display:inline-block;padding:2px 8px;border-radius:4px;font-size:0.75em;margin-right:6px}
.badge-green{background:#1a3a1a;color:#4caf50}
.badge-yellow{background:#3a3a1a;color:#ffc107}
.badge-red{background:#3a1a1a;color:#f44336}
.card{background:#14141f;border:1px solid #2a2a35;border-radius:8px;padding:20px;margin-bottom:16px}
.card h3{color:#d4a017;font-size:1.1em;margin-bottom:12px}
.row{display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid #1a1a25}
.row:last-child{border-bottom:none}
.label{color:#888}
.value{color:#e0d8c0;font-family:monospace}
.endpoint{color:#d4a017;font-family:monospace;font-size:0.85em}
.endpoint-desc{color:#888;font-size:0.85em}
.endpoint-row{display:flex;align-items:center;gap:12px;padding:8px 0;border-bottom:1px solid #1a1a25}
.endpoint-row:last-child{border-bottom:none}
.dna{font-size:0.7em;color:#555;margin-top:30px;text-align:center}
</style>
</head>
<body>
<div class="container">
<h1>🐉 龍魂·小艺桥接 v2.0</h1>
<p class="sub">XiaoYi Bridge · 唯一AI接口 · 调度+推理一体化</p>

<div class="card">
<h3>🟢 引擎状态</h3>
<div class="row"><span class="label">版本</span><span class="value">v2.0.0</span></div>
<div class="row"><span class="label">状态</span><span class="value"><span class="badge badge-green">运行中</span></span></div>
<div class="row"><span class="label">确认码</span><span class="value">#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z</span></div>
<div class="row"><span class="label">GPG</span><span class="value">A2D0092CEE2E5BA8</span></div>
</div>

<div class="card">
<h3>🔌 API端点</h3>
<div class="endpoint-row"><span class="endpoint">GET /api/v1/xiaoyi/status</span><span class="endpoint-desc">引擎状态</span></div>
<div class="endpoint-row"><span class="endpoint">POST /api/v1/chat</span><span class="endpoint-desc">🆕 AI对话（路由Ollama）</span></div>
<div class="endpoint-row"><span class="endpoint">GET /api/v1/chat/models</span><span class="endpoint-desc">🆕 可用对话模型</span></div>
<div class="endpoint-row"><span class="endpoint">GET /api/v1/xiaoyi/models</span><span class="endpoint-desc">模型状态</span></div>
<div class="endpoint-row"><span class="endpoint">GET /api/v1/xiaoyi/health</span><span class="endpoint-desc">健康检查</span></div>
<div class="endpoint-row"><span class="endpoint">POST /api/v1/xiaoyi/exec</span><span class="endpoint-desc">执行命令</span></div>
<div class="endpoint-row"><span class="endpoint">POST /api/v1/xiaoyi/audit</span><span class="endpoint-desc">安全审计</span></div>
</div>

<div class="dna">DNA: #龍芯⚡️丙午·乙未·丙申·亥时·☰乾-XIAOYI-BRIDGE-v2.0-ai-router<br>创建者: 诸葛鑫（UID9622）｜协议: CC BY-NC-SA 4.0</div>
</div>
</body>
</html>"""


# ═══════════════════════════════════════════════════════════════
# HTTP Handler
# ═══════════════════════════════════════════════════════════════

class XiaoYiHandler(BaseHTTPRequestHandler):
    """小艺桥接 HTTP 处理器"""

    server_version = "Longhun-XiaoYi-Bridge/2.0"

    def log_message(self, fmt, *args):
        pass  # 静默日志

    def _send_json(self, data: Dict, code: int = 200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, html: str, code: int = 200):
        body = html.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self) -> Dict:
        try:
            length = int(self.headers.get("Content-Length", 0))
            if length == 0:
                return {}
            body = self.rfile.read(length).decode("utf-8")
            return json.loads(body) if body else {}
        except Exception:
            return {}

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type,Authorization")
        self.end_headers()

    def do_GET(self):
        path = self.path.split("?")[0]

        # 根页面
        if path == "/":
            self._send_html(INDEX_HTML)
            return

        # 引擎状态
        if path == "/api/v1/xiaoyi/status":
            info = get_system_info()
            best_model = get_best_chat_model()
            self._send_json({
                "bridge": {"version": VERSION, "dna": DNA_BASE, "uptime": "running",
                           "commands": len(COMMANDS), "audit_log_count": len(AUDIT_LOG)},
                "system": info,
                "ai_gateway": {"best_model": best_model, "ollama": get_available_ollama_models()},
                "confirm": CONFIRM_CODE,
            })
            return

        # 健康检查
        if path == "/api/v1/xiaoyi/health":
            info = get_system_info()
            best = get_best_chat_model()
            health_status = "🟢"
            warnings = []
            if not best:
                health_status = "🟡"
                warnings.append("无可用Ollama龍魂模型")
            self._send_json({
                "status": health_status,
                "system": info,
                "ai_model": best,
                "warnings": warnings,
                "dna": DNA_BASE,
                "confirm": CONFIRM_CODE,
            })
            return

        # 能力清单
        if path == "/api/v1/xiaoyi/capabilities":
            cmds = {k: {"desc": v["desc"], "aliases": v["aliases"]} for k, v in COMMANDS.items()}
            self._send_json({
                "bridge": "longhun-xiaoyi-v2.0",
                "capabilities": {
                    "system_commands": cmds,
                    "ai_chat": "POST /api/v1/chat — Ollama长龙魂模型对话",
                    "model_query": "GET /api/v1/chat/models — 可用对话模型列表",
                    "audit": "POST /api/v1/xiaoyi/audit — 三色审计",
                },
                "confirm": CONFIRM_CODE,
            })
            return

        # 模型状态
        if path == "/api/v1/xiaoyi/models":
            model_status = get_model_status()
            self._send_json({"success": True, "models": model_status, "confirm": CONFIRM_CODE})
            return

        # 🆕 可用对话模型列表
        if path == "/api/v1/chat/models":
            available = get_available_ollama_models()
            best = get_best_chat_model()
            self._send_json({
                "success": True,
                "available_models": available,
                "best_model": best,
                "priority_order": OLLAMA_CHAT_MODEL_PRIORITY,
                "endpoint": "POST /api/v1/chat",
                "confirm": CONFIRM_CODE,
            })
            return

        # 日志
        if path == "/api/v1/xiaoyi/logs":
            with AUDIT_LOCK:
                recent = AUDIT_LOG[-20:]
            self._send_json({"success": True, "count": len(AUDIT_LOG), "recent": recent})
            return

        # 404
        self._send_json({"error": "not_found", "path": path}, 404)

    def do_POST(self):
        path = self.path.split("?")[0]
        body = self._read_body()

        # 🆕 AI对话 — 小艺唯一AI接口
        if path == "/api/v1/chat":
            prompt = body.get("prompt", "") or body.get("message", "") or body.get("text", "")
            system = body.get("system", "") or body.get("context", "")
            stream = body.get("stream", False)

            # 一票否决
            veto = detect_veto(prompt + system)
            if veto:
                _audit("chat_veto", "rejected", veto, "🔴")
                self._send_json({"success": False, "veto": True, "error": veto, "response": veto}, 403)
                return

            # 选最佳模型
            model = body.get("model", "") or get_best_chat_model()
            if not model:
                _audit("chat_no_model", "failed", "无可用Ollama模型")
                self._send_json({"success": False, "error": "无可用龍魂模型"}, 503)
                return

            if not prompt:
                self._send_json({"success": False, "error": "缺少prompt/message参数"}, 400)
                return

            _audit("chat", "processing", f"model={model} prompt_len={len(prompt)}")

            # 查询Ollama
            result = query_ollama(model, prompt, system, stream)

            if result.get("success"):
                _audit("chat", "success", f"model={model} resp_len={len(result['response'])}")
                self._send_json({
                    "success": True,
                    "model": model,
                    "response": result["response"],
                    "confirm": CONFIRM_CODE,
                    "dna": DNA_BASE,
                })
            else:
                _audit("chat_error", "failed", result.get("error", ""), "🟡")
                self._send_json({"success": False, "error": result.get("error", "Ollama调用失败")}, 502)
            return

        # 执行命令
        if path == "/api/v1/xiaoyi/exec":
            intent = body.get("intent", "") or body.get("command", "") or body.get("cmd", "")

            # 一票否决
            veto = detect_veto(intent)
            if veto:
                _audit("exec_veto", "rejected", veto, "🔴")
                self._send_json({"success": False, "veto": True, "error": veto}, 403)
                return

            # 意图匹配
            matched_cmd = None
            for cmd, info in COMMANDS.items():
                if intent in [cmd] + info.get("aliases", []):
                    matched_cmd = cmd
                    break
            if not matched_cmd and intent in SYSTEM_SCRIPTS:
                matched_cmd = intent

            if not matched_cmd:
                self._send_json({
                    "success": False,
                    "error": f"未知命令: {intent}",
                    "available": list(COMMANDS.keys()),
                }, 400)
                return

            _audit("exec", "processing", f"cmd={matched_cmd} intent={intent}")
            result = execute_cmd(matched_cmd)
            _audit("exec", "success" if result["success"] else "failed",
                   f"cmd={matched_cmd} rc={result.get('rc', -1)}",
                   "🟡" if not result["success"] else "🟢")

            self._send_json({
                "success": result["success"],
                "command": matched_cmd,
                "output": result["output"],
                "confirm": CONFIRM_CODE,
            })
            return

        # 审计
        if path == "/api/v1/xiaoyi/audit":
            _audit("manual_audit", "triggered", body.get("detail", ""), "🟡")
            self._send_json({
                "success": True,
                "message": "审计已触发",
                "audit_log_count": len(AUDIT_LOG),
                "confirm": CONFIRM_CODE,
            })
            return

        self._send_json({"error": "not_found"}, 404)


# ═══════════════════════════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════════════════════════

def main():
    import argparse
    p = argparse.ArgumentParser(description="龍魂·小艺桥接引擎 v2.0 · 唯一AI接口")
    p.add_argument("--serve", action="store_true", default=True, help="HTTP服务模式（默认）")
    p.add_argument("--port", type=int, default=8799, help="端口（默认8799）")
    p.add_argument("--host", type=str, default="127.0.0.1", help="绑定地址（默认127.0.0.1）")
    p.add_argument("--cmd", type=str, help="CLI命令模式")
    args = p.parse_args()

    # CLI模式
    if args.cmd:
        intent = args.cmd
        veto = detect_veto(intent)
        if veto:
            print(json.dumps({"success": False, "veto": True, "error": veto}, ensure_ascii=False))
            sys.exit(1)

        matched = None
        for cmd, info in COMMANDS.items():
            if intent in [cmd] + info.get("aliases", []):
                matched = cmd
                break
        if intent in SYSTEM_SCRIPTS:
            matched = intent

        if not matched:
            print(json.dumps({"success": False, "error": f"未知命令: {intent}",
                              "available": list(COMMANDS.keys())}, ensure_ascii=False))
            sys.exit(1)

        result = execute_cmd(matched)
        _audit("cli_exec", "success" if result["success"] else "failed", f"cmd={matched}")
        print(json.dumps({"success": result["success"], "command": matched,
                          "output": result["output"]}, ensure_ascii=False))
        sys.exit(0 if result["success"] else 1)

    # HTTP模式
    server = HTTPServer((args.host, args.port), XiaoYiHandler)
    print(f"\n🐉 龍魂·小艺桥接 v2.0 启动")
    print(f"   DNA: {DNA_BASE}")
    print(f"   唯一AI接口: POST http://{args.host}:{args.port}/api/v1/chat")
    print(f"   状态页面: http://{args.host}:{args.port}/")
    print(f"   CONFIRM: {CONFIRM_CODE}\n")

    # 检测可用模型
    available = get_available_ollama_models()
    best = get_best_chat_model()
    print(f"🧠 可用Ollama模型: {available}")
    print(f"⭐ 最佳聊天模型: {best}\n")
    print(f"🟢 服务已启动，端口 {args.port}，等待小艺调令...\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 小艺桥接已停止")
        server.server_close()


if __name__ == "__main__":
    main()
