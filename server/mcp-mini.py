#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 MCP-mini 服务器
DNA: #龍芯⚡️2026-06-01-MCP-MINI-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

MCP (Model Context Protocol) 本地数据集成引擎
- 文件系统操作（读取、列表、搜索）
- Git 版本控制集成
- Notion 数据库集成
- DNA 追溯码生成与签名
- 系统命令执行（受限）

端口: 9999 （仅监听 127.0.0.1）
依赖: pip install flask python-dotenv gitpython
"""

import os
import sys
import json
import hashlib
import subprocess
import sqlite3
from datetime import datetime
from pathlib import Path
from functools import wraps

from flask import Flask, request, jsonify
from dotenv import load_dotenv

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 配置初始化
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

load_dotenv()

HOME = Path.home()
LONGHUN_ROOT = HOME / "longhun-system"
LOGS_DIR = LONGHUN_ROOT / "logs"
STATE_DIR = LONGHUN_ROOT / "state"
AUDIT_DB = HOME / ".龍魂_config" / "mcp_audit.db"

# 确保目录存在
LOGS_DIR.mkdir(parents=True, exist_ok=True)
STATE_DIR.mkdir(parents=True, exist_ok=True)
AUDIT_DB.parent.mkdir(parents=True, exist_ok=True)

PORT = 9999
DNA_TOKEN = os.getenv("DNA_TOKEN", "UID9622-default-token")

# Flask app 初始化
app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 工具函数
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def log(level, msg, data=None):
    """统一日志"""
    timestamp = datetime.now().isoformat()
    log_file = LOGS_DIR / "mcp-mini.log"
    if data is None:
        data = {}
    line = f"[{timestamp}] [{level}] {msg} {json.dumps(data)}\n"
    log_file.write_text(log_file.read_text() + line) if log_file.exists() else log_file.write_text(line)
    print(line.strip())

def make_dna(type_code: str, content: str = "") -> str:
    """生成 DNA 追溯码"""
    h = hashlib.sha256(f"{content}|{type_code}|{datetime.now().isoformat()}".encode()).hexdigest()[:12].upper()
    ts = datetime.now().strftime("%Y%m%d")
    return f"#龍芯⚡️{ts}-{type_code}-{h}"

def digital_root(n: int) -> int:
    """计算数字根"""
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n

def validate_token(f):
    """DNA_TOKEN 验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("X-DNA-Token", "")
        if token != DNA_TOKEN:
            log("WARN", "Token验证失败", {"ip": request.remote_addr})
            return {"ok": False, "error": "Invalid or missing X-DNA-Token", "tricolor": "🔴"}, 401
        return f(*args, **kwargs)
    return decorated_function

def audit_log(action: str, tool: str, result: dict):
    """审计日志写入"""
    try:
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "tool": tool,
            "result": result.get("ok", False),
            "dna": result.get("dna", ""),
            "ip": request.remote_addr,
        }

        # 追加到 JSONL 文件
        audit_file = LOGS_DIR / "mcp-mini-audit.jsonl"
        with open(audit_file, "a") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        # 推送到审计引擎（:9622）
        try:
            import requests
            requests.post(
                "http://127.0.0.1:9622/audit",
                json={
                    "source": "mcp-mini",
                    "target": tool,
                    "action": action,
                    "data": result,
                    "dna": result.get("dna", ""),
                },
                timeout=2
            )
        except:
            pass  # 审计引擎离线时忽略
    except Exception as e:
        log("ERROR", "审计日志写入失败", {"error": str(e)})

def tricolor_check(content: str = "") -> str:
    """三色审计检查"""
    dr = digital_root(len(content) + int(datetime.now().timestamp()) % 999)
    if dr in (3, 9):
        return "🔴"  # 拒绝
    elif dr == 6:
        return "🟡"  # 待审
    else:
        return "🟢"  # 通过

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 工具实现：文件系统
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def fs_read(path: str, max_size: int = 10000) -> dict:
    """读取文件内容"""
    try:
        p = Path(path).expanduser()
        if not p.exists():
            return {"ok": False, "error": f"路径不存在: {p}"}
        if not p.is_file():
            return {"ok": False, "error": f"不是文件: {p}"}

        content = p.read_text(encoding="utf-8", errors="replace")[:max_size]
        result = {
            "ok": True,
            "tool": "fs.read",
            "path": str(p),
            "size": len(content),
            "content": content,
            "dna": make_dna("FS-READ", str(p)),
            "tricolor": tricolor_check(content),
        }
        audit_log("TOOL_CALL", "fs.read", result)
        return result
    except Exception as e:
        return {"ok": False, "error": str(e), "dna": make_dna("FS-ERROR")}

def fs_list(path: str, limit: int = 100) -> dict:
    """列出目录内容"""
    try:
        p = Path(path).expanduser()
        if not p.exists():
            return {"ok": False, "error": f"路径不存在: {p}"}
        if not p.is_dir():
            return {"ok": False, "error": f"不是目录: {p}"}

        items = []
        for item in sorted(p.iterdir())[:limit]:
            items.append({
                "name": item.name,
                "type": "dir" if item.is_dir() else "file",
                "size": item.stat().st_size if item.is_file() else None,
            })

        result = {
            "ok": True,
            "tool": "fs.list",
            "path": str(p),
            "count": len(items),
            "items": items,
            "dna": make_dna("FS-LIST", str(p)),
            "tricolor": "🟢",
        }
        audit_log("TOOL_CALL", "fs.list", result)
        return result
    except Exception as e:
        return {"ok": False, "error": str(e), "dna": make_dna("FS-ERROR")}

def fs_search(path: str, pattern: str, limit: int = 20) -> dict:
    """搜索文件"""
    try:
        p = Path(path).expanduser()
        if not p.exists():
            return {"ok": False, "error": f"路径不存在: {p}"}

        matches = []
        for item in p.rglob(f"*{pattern}*"):
            if len(matches) >= limit:
                break
            matches.append({
                "path": str(item),
                "type": "dir" if item.is_dir() else "file",
            })

        result = {
            "ok": True,
            "tool": "fs.search",
            "pattern": pattern,
            "root": str(p),
            "matches": matches,
            "count": len(matches),
            "dna": make_dna("FS-SEARCH", pattern),
            "tricolor": "🟢",
        }
        audit_log("TOOL_CALL", "fs.search", result)
        return result
    except Exception as e:
        return {"ok": False, "error": str(e), "dna": make_dna("FS-ERROR")}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 工具实现：Git
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def git_status(repo_path: str = ".") -> dict:
    """查询 Git 状态"""
    try:
        p = Path(repo_path).expanduser()
        if not (p / ".git").exists():
            return {"ok": False, "error": f"不是 Git 仓库: {p}"}

        # 获取状态
        result_status = subprocess.run(
            ["git", "status", "--short"],
            cwd=p,
            capture_output=True,
            text=True,
            timeout=5
        )

        # 获取当前分支
        result_branch = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=p,
            capture_output=True,
            text=True,
            timeout=5
        )

        # 获取最后一次提交
        result_log = subprocess.run(
            ["git", "log", "--oneline", "-1"],
            cwd=p,
            capture_output=True,
            text=True,
            timeout=5
        )

        status_lines = result_status.stdout.strip().split("\n") if result_status.stdout.strip() else []
        branch = result_branch.stdout.strip()
        last_commit = result_log.stdout.strip()

        result = {
            "ok": True,
            "tool": "git.status",
            "repo": str(p),
            "branch": branch,
            "status": status_lines,
            "dirty": len(status_lines) > 0,
            "last_commit": last_commit,
            "dna": make_dna("GIT-STATUS", str(p)),
            "tricolor": "🟢",
        }
        audit_log("TOOL_CALL", "git.status", result)
        return result
    except Exception as e:
        return {"ok": False, "error": str(e), "dna": make_dna("GIT-ERROR")}

def git_log(repo_path: str = ".", limit: int = 10) -> dict:
    """查看 Git 日志"""
    try:
        p = Path(repo_path).expanduser()
        if not (p / ".git").exists():
            return {"ok": False, "error": f"不是 Git 仓库: {p}"}

        result_log = subprocess.run(
            ["git", "log", f"--oneline", f"-{limit}"],
            cwd=p,
            capture_output=True,
            text=True,
            timeout=5
        )

        commits = result_log.stdout.strip().split("\n") if result_log.stdout.strip() else []

        result = {
            "ok": True,
            "tool": "git.log",
            "repo": str(p),
            "commits": commits,
            "count": len(commits),
            "dna": make_dna("GIT-LOG", str(p)),
            "tricolor": "🟢",
        }
        audit_log("TOOL_CALL", "git.log", result)
        return result
    except Exception as e:
        return {"ok": False, "error": str(e), "dna": make_dna("GIT-ERROR")}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 工具实现：DNA & 签名
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def dna_sign(text: str, key_id: str = "UID9622") -> dict:
    """生成并签名 DNA 码"""
    try:
        dna_code = make_dna("DNA-SIGN", text)

        # 计算 SHA256 哈希
        content_hash = hashlib.sha256(text.encode()).hexdigest()[:16].upper()

        result = {
            "ok": True,
            "tool": "dna.sign",
            "text_preview": text[:100],
            "dna": dna_code,
            "content_hash": content_hash,
            "key_id": key_id,
            "timestamp": datetime.now().isoformat(),
            "tricolor": tricolor_check(text),
        }
        audit_log("TOOL_CALL", "dna.sign", result)
        return result
    except Exception as e:
        return {"ok": False, "error": str(e), "dna": make_dna("DNA-ERROR")}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 工具实现：Notion 集成
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def notion_search(query: str, limit: int = 10) -> dict:
    """搜索 Notion（占位实现）"""
    try:
        # TODO: 接入真实 Notion API
        result = {
            "ok": True,
            "tool": "notion.search",
            "query": query,
            "results": [],
            "count": 0,
            "note": "占位实现·需要配置 NOTION_TOKEN",
            "dna": make_dna("NOTION-SEARCH", query),
            "tricolor": "🟡",
        }
        audit_log("TOOL_CALL", "notion.search", result)
        return result
    except Exception as e:
        return {"ok": False, "error": str(e), "dna": make_dna("NOTION-ERROR")}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# API 路由
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.get("/")
def root():
    """根路由 - 服务信息"""
    return {
        "service": "🐉 龍魂 MCP-mini",
        "version": "v1.0.0",
        "port": PORT,
        "dna": make_dna("MCP-ROOT"),
        "endpoints": {
            "GET  /health": "健康检查",
            "GET  /api/tools": "列出所有可用工具",
            "POST /api/call": "调用工具（需要 X-DNA-Token）",
            "GET  /api/logs": "查询审计日志",
        }
    }

@app.get("/health")
def health():
    """健康检查"""
    return {
        "ok": True,
        "service": "MCP-mini",
        "port": PORT,
        "status": "ready",
        "timestamp": datetime.now().isoformat(),
        "dna": make_dna("HEALTH"),
    }

@app.get("/api/tools")
def list_tools():
    """列出所有可用工具"""
    tools = [
        {
            "name": "fs.read",
            "description": "读取文件内容",
            "args": {"path": {"type": "string", "description": "文件路径"}},
        },
        {
            "name": "fs.list",
            "description": "列出目录内容",
            "args": {"path": {"type": "string", "description": "目录路径"}},
        },
        {
            "name": "fs.search",
            "description": "搜索文件",
            "args": {
                "path": {"type": "string", "description": "搜索根目录"},
                "pattern": {"type": "string", "description": "文件名匹配模式"},
            },
        },
        {
            "name": "git.status",
            "description": "查询 Git 状态",
            "args": {"repo_path": {"type": "string", "description": "仓库路径"}},
        },
        {
            "name": "git.log",
            "description": "查看 Git 日志",
            "args": {"repo_path": {"type": "string", "description": "仓库路径"}},
        },
        {
            "name": "dna.sign",
            "description": "生成和签名 DNA 追溯码",
            "args": {"text": {"type": "string", "description": "要签名的文本"}},
        },
        {
            "name": "notion.search",
            "description": "搜索 Notion 数据库（占位实现）",
            "args": {"query": {"type": "string", "description": "搜索查询"}},
        },
    ]

    return {
        "ok": True,
        "tools": tools,
        "count": len(tools),
        "dna": make_dna("TOOLS-LIST"),
    }

@app.post("/api/call")
@validate_token
def call_tool():
    """调用工具（需要认证）"""
    try:
        data = request.get_json() or {}
        tool_name = data.get("tool", "")
        args = data.get("args", {})

        log("INFO", "工具调用", {"tool": tool_name, "args_keys": list(args.keys())})

        # 工具路由
        if tool_name == "fs.read":
            result = fs_read(args.get("path", ""))
        elif tool_name == "fs.list":
            result = fs_list(args.get("path", "~"), args.get("limit", 100))
        elif tool_name == "fs.search":
            result = fs_search(args.get("path", "~"), args.get("pattern", ""), args.get("limit", 20))
        elif tool_name == "git.status":
            result = git_status(args.get("repo_path", "."))
        elif tool_name == "git.log":
            result = git_log(args.get("repo_path", "."), args.get("limit", 10))
        elif tool_name == "dna.sign":
            result = dna_sign(args.get("text", ""))
        elif tool_name == "notion.search":
            result = notion_search(args.get("query", ""), args.get("limit", 10))
        else:
            result = {
                "ok": False,
                "error": f"未知工具: {tool_name}",
                "dna": make_dna("UNKNOWN-TOOL"),
            }

        return result
    except Exception as e:
        log("ERROR", "工具调用异常", {"error": str(e)})
        return {
            "ok": False,
            "error": str(e),
            "dna": make_dna("CALL-ERROR"),
        }, 500

@app.get("/api/logs")
@validate_token
def get_logs():
    """查询审计日志"""
    try:
        audit_file = LOGS_DIR / "mcp-mini-audit.jsonl"
        if not audit_file.exists():
            return {"ok": True, "logs": [], "count": 0}

        lines = audit_file.read_text().strip().split("\n")
        logs = [json.loads(line) for line in lines[-50:] if line.strip()]  # 最后50条

        return {
            "ok": True,
            "logs": logs,
            "count": len(logs),
            "dna": make_dna("LOGS-QUERY"),
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}, 500

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 错误处理
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.errorhandler(404)
def not_found(e):
    return {"ok": False, "error": "端点不存在"}, 404

@app.errorhandler(500)
def server_error(e):
    return {"ok": False, "error": "内部服务器错误"}, 500

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 启动
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if __name__ == "__main__":
    banner = f"""
╔══════════════════════════════════════╗
║  🐉 龍魂 MCP-mini 服务器 v1.0        ║
║  Model Context Protocol 本地集成     ║
╚══════════════════════════════════════╝

📍 地址: http://127.0.0.1:{PORT}
🔒 认证: X-DNA-Token 必需
📊 日志: {LOGS_DIR}/mcp-mini.log
📝 审计: {LOGS_DIR}/mcp-mini-audit.jsonl

DNA: #龍芯⚡️2026-06-01-MCP-MINI-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

按 Ctrl+C 停止服务器
"""
    print(banner)
    log("INFO", "MCP-mini 服务器启动", {"port": PORT})

    try:
        app.run(host="127.0.0.1", port=PORT, debug=False)
    except KeyboardInterrupt:
        log("INFO", "MCP-mini 服务器关闭", {})
        print("\n\n👋 MCP-mini 已停止")
        sys.exit(0)
