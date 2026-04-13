#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════╗
║  龍魂MCP服务器 · Local MCP Server                        ║
║  DNA: #龍芯⚡️2026-04-13-MCP-SERVER-v1.0                 ║
║  创始人: 诸葛鑫（UID9622）                                ║
║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F           ║
║  理论指导: 曾仕强老师（永恒显示）                          ║
║  协议: CC BY-NC-ND                                       ║
╚══════════════════════════════════════════════════════════╝

龍魂本地MCP服务器 —— 让Notion AI能读老大的文件。

功能（4个工具）:
  1. list_assets    — 列出资产清单（支持过滤）
  2. read_file      — 读取指定文件内容
  3. search_dragon  — 全库关键词搜索
  4. git_history    — 查看Git提交历史

启动:
  python3 mcp_server.py              # stdio模式（MCP标准）
  python3 mcp_server.py --sse        # SSE模式（HTTP，端口9623）

献给每一个相信技术应该有温度的人。
"""

import os
import sys
import json
import subprocess
import datetime
from pathlib import Path
from typing import Optional

from mcp.server.fastmcp import FastMCP

# ═══════════════════════════════════════════
# 常量
# ═══════════════════════════════════════════

SYSTEM_ROOT = Path.home() / "longhun-system"
REGISTRY_PATH = SYSTEM_ROOT / "config" / "asset_registry.jsonl"
CATALOG_PATH = SYSTEM_ROOT / "config" / "asset_catalog_auto.txt"

# 安全边界：只允许读取这些目录下的文件
ALLOWED_ROOTS = [
    str(SYSTEM_ROOT),
    str(Path.home() / "Desktop"),
    str(Path.home() / "Documents"),
    str(Path.home() / "Downloads"),
    str(Path.home() / "Pictures"),
]

# 禁止读取的文件（安全铁律）
BLOCKED_PATTERNS = [
    ".env", "credentials", "secret", "private_key",
    "id_rsa", "id_ed25519", ".ssh/",
    "baobao_master_key.json",  # 钥匙文件不外传
]

# ═══════════════════════════════════════════
# 创建MCP服务器
# ═══════════════════════════════════════════

mcp = FastMCP(
    "龍魂本地文件系统",
    host="0.0.0.0",
    port=9623,
)


# ═══════════════════════════════════════════
# 安全检查
# ═══════════════════════════════════════════

def _is_path_safe(filepath: str) -> tuple[bool, str]:
    """检查路径是否在允许范围内"""
    try:
        real = str(Path(filepath).resolve())
    except Exception:
        return False, "路径解析失败"

    # 检查黑名单
    for pattern in BLOCKED_PATTERNS:
        if pattern in real.lower():
            return False, f"安全限制：包含敏感关键词 '{pattern}'"

    # 检查白名单
    for root in ALLOWED_ROOTS:
        if real.startswith(root):
            return True, "OK"

    return False, f"路径不在允许范围内。允许: {', '.join(ALLOWED_ROOTS)}"


# ═══════════════════════════════════════════
# 工具1: 列出资产
# ═══════════════════════════════════════════

@mcp.tool()
def list_assets(
    filter_type: Optional[str] = None,
    filter_keyword: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
) -> str:
    """
    列出龍魂系统资产清单。

    Args:
        filter_type: 按文件类型过滤（如 "py", "html", "cpp", "md"）
        filter_keyword: 按文件名关键词过滤
        limit: 返回数量上限（默认50，最大200）
        offset: 跳过前N条（用于翻页）

    Returns:
        JSON格式的资产列表
    """
    if not REGISTRY_PATH.exists():
        return json.dumps({"错误": "资产清单不存在，请先运行 asset_scanner.sh"}, ensure_ascii=False)

    limit = min(limit, 200)
    results = []
    total = 0

    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                continue

            # 类型过滤
            if filter_type and item.get("类型", "") != filter_type:
                continue

            # 关键词过滤
            if filter_keyword and filter_keyword.lower() not in item.get("文件", "").lower():
                continue

            total += 1
            if total > offset and len(results) < limit:
                results.append({
                    "文件": item.get("文件", ""),
                    "路径": item.get("路径", ""),
                    "大小": item.get("大小", 0),
                    "类型": item.get("类型", ""),
                    "龍魂": item.get("龍魂", False),
                })

    return json.dumps({
        "总数": total,
        "返回": len(results),
        "偏移": offset,
        "资产": results,
    }, ensure_ascii=False, indent=2)


# ═══════════════════════════════════════════
# 工具2: 读取文件
# ═══════════════════════════════════════════

@mcp.tool()
def read_file(
    filepath: str,
    max_lines: int = 200,
    start_line: int = 1,
) -> str:
    """
    读取指定文件的内容。

    Args:
        filepath: 文件的绝对路径
        max_lines: 最多读取行数（默认200，最大1000）
        start_line: 从第几行开始读（默认1）

    Returns:
        文件内容（文本）
    """
    # 安全检查
    safe, reason = _is_path_safe(filepath)
    if not safe:
        return json.dumps({"错误": reason}, ensure_ascii=False)

    path = Path(filepath)
    if not path.exists():
        return json.dumps({"错误": f"文件不存在: {filepath}"}, ensure_ascii=False)

    if not path.is_file():
        return json.dumps({"错误": f"不是文件: {filepath}"}, ensure_ascii=False)

    # 文件大小检查（不读超过5MB的文件）
    size = path.stat().st_size
    if size > 5 * 1024 * 1024:
        return json.dumps({
            "错误": f"文件太大: {size}B ({size/1024/1024:.1f}MB)，上限5MB",
            "文件": path.name,
        }, ensure_ascii=False)

    max_lines = min(max_lines, 1000)

    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except Exception as e:
        return json.dumps({"错误": f"读取失败: {str(e)}"}, ensure_ascii=False)

    total_lines = len(lines)
    start_idx = max(0, start_line - 1)
    selected = lines[start_idx:start_idx + max_lines]

    content = "".join(selected)

    return json.dumps({
        "文件": path.name,
        "路径": str(path),
        "大小": size,
        "总行数": total_lines,
        "返回行": f"{start_line}-{start_line + len(selected) - 1}",
        "内容": content,
    }, ensure_ascii=False)


# ═══════════════════════════════════════════
# 工具3: 关键词搜索
# ═══════════════════════════════════════════

@mcp.tool()
def search_dragon(
    keyword: str,
    search_path: Optional[str] = None,
    file_type: Optional[str] = None,
    max_results: int = 30,
) -> str:
    """
    在龍魂系统中搜索关键词。

    Args:
        keyword: 搜索关键词
        search_path: 搜索目录（默认 ~/longhun-system/）
        file_type: 限定文件类型（如 "py", "html", "md"）
        max_results: 最大结果数（默认30，最大100）

    Returns:
        匹配的文件和行
    """
    if not keyword or len(keyword) < 1:
        return json.dumps({"错误": "关键词不能为空"}, ensure_ascii=False)

    target = search_path or str(SYSTEM_ROOT)

    # 安全检查
    safe, reason = _is_path_safe(target)
    if not safe:
        return json.dumps({"错误": reason}, ensure_ascii=False)

    max_results = min(max_results, 100)

    # 用grep搜索
    cmd = ["grep", "-rn", "--include=*.py", "--include=*.html", "--include=*.md",
           "--include=*.txt", "--include=*.sh", "--include=*.js", "--include=*.ts",
           "--include=*.swift", "--include=*.cpp", "--include=*.h",
           "--include=*.json", "--include=*.yaml", "--include=*.yml",
           "-l", keyword, target]

    if file_type:
        cmd = ["grep", "-rn", f"--include=*.{file_type}", "-l", keyword, target]

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=10,
            cwd=str(SYSTEM_ROOT),
        )
        files = [f for f in result.stdout.strip().split("\n") if f]
    except subprocess.TimeoutExpired:
        return json.dumps({"错误": "搜索超时（10秒）"}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"错误": f"搜索失败: {str(e)}"}, ensure_ascii=False)

    # 对每个文件，取匹配的行
    matches = []
    for fpath in files[:max_results]:
        try:
            grep_lines = subprocess.run(
                ["grep", "-n", keyword, fpath],
                capture_output=True, text=True, timeout=5,
            )
            lines = grep_lines.stdout.strip().split("\n")[:5]  # 每文件最多5行
            matches.append({
                "文件": os.path.basename(fpath),
                "路径": fpath,
                "匹配行": lines,
            })
        except Exception:
            matches.append({"文件": os.path.basename(fpath), "路径": fpath, "匹配行": []})

    return json.dumps({
        "关键词": keyword,
        "匹配文件数": len(files),
        "返回": len(matches),
        "结果": matches,
    }, ensure_ascii=False, indent=2)


# ═══════════════════════════════════════════
# 工具4: Git历史
# ═══════════════════════════════════════════

@mcp.tool()
def git_history(
    count: int = 20,
    filepath: Optional[str] = None,
) -> str:
    """
    查看龍魂系统的Git提交历史。

    Args:
        count: 显示多少条提交（默认20，最大100）
        filepath: 限定某个文件的提交历史（可选）

    Returns:
        Git提交记录
    """
    count = min(count, 100)

    cmd = ["git", "log", f"--pretty=format:%H|%ai|%an|%s", f"-{count}"]

    if filepath:
        safe, reason = _is_path_safe(filepath)
        if not safe:
            return json.dumps({"错误": reason}, ensure_ascii=False)
        cmd.append("--")
        cmd.append(filepath)

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=10,
            cwd=str(SYSTEM_ROOT),
        )
    except Exception as e:
        return json.dumps({"错误": f"Git命令失败: {str(e)}"}, ensure_ascii=False)

    if result.returncode != 0:
        return json.dumps({"错误": f"Git错误: {result.stderr.strip()}"}, ensure_ascii=False)

    commits = []
    for line in result.stdout.strip().split("\n"):
        if not line:
            continue
        parts = line.split("|", 3)
        if len(parts) == 4:
            commits.append({
                "哈希": parts[0][:8],
                "时间": parts[1],
                "作者": parts[2],
                "说明": parts[3],
            })

    # 额外信息
    try:
        status = subprocess.run(
            ["git", "status", "--short"],
            capture_output=True, text=True, timeout=5,
            cwd=str(SYSTEM_ROOT),
        )
        changed = len([l for l in status.stdout.strip().split("\n") if l.strip()])
    except Exception:
        changed = -1

    return json.dumps({
        "仓库": str(SYSTEM_ROOT),
        "提交数": len(commits),
        "未提交变更": changed,
        "历史": commits,
    }, ensure_ascii=False, indent=2)


# ═══════════════════════════════════════════
# 额外资源: 资产概览
# ═══════════════════════════════════════════

@mcp.resource("longhun://catalog")
def get_catalog() -> str:
    """获取龍魂数字资产清单概览"""
    if CATALOG_PATH.exists():
        return CATALOG_PATH.read_text(encoding="utf-8")
    return "资产清单未生成，请运行 notion_sync.sh"


@mcp.resource("longhun://system-info")
def get_system_info() -> str:
    """获取龍魂系统基本信息"""
    info = {
        "系统": "龍魂系统 · UID9622",
        "创始人": "诸葛鑫",
        "理论指导": "曾仕强老师",
        "根目录": str(SYSTEM_ROOT),
        "DNA": f"#龍芯⚡️{datetime.date.today()}-MCP-SERVER-v1.0",
        "协议": "CC BY-NC-ND",
        "模块": {
            "core": "Python核心引擎",
            "web": "HTML创作集",
            "万年历": "C++17内核 · 首个产品",
            "LongHunWidget": "iOS Widget · SwiftUI",
            "plugins": "插件生态",
        },
    }
    return json.dumps(info, ensure_ascii=False, indent=2)


# ═══════════════════════════════════════════
# SSL证书路径
# ═══════════════════════════════════════════

SSL_DIR = SYSTEM_ROOT / "config" / "ssl"
SSL_CERT = SSL_DIR / "localhost+2.pem"
SSL_KEY = SSL_DIR / "localhost+2-key.pem"


# ═══════════════════════════════════════════
# 启动
# ═══════════════════════════════════════════

if __name__ == "__main__":
    if "--sse" in sys.argv:
        import uvicorn

        # 检测是否有SSL证书
        use_ssl = SSL_CERT.exists() and SSL_KEY.exists()
        protocol = "https" if use_ssl else "http"

        print(f"🐉 龍魂MCP服务器 · SSE模式 · {'HTTPS' if use_ssl else 'HTTP'}")
        print(f"📡 {protocol}://localhost:9623/sse")
        print(f"DNA: #龍芯⚡️{datetime.date.today()}-MCP-SERVER-v1.0")

        # 获取SSE应用
        starlette_app = mcp.sse_app()

        # 配置uvicorn（直接传SSL参数）
        config_kwargs = {
            "host": "0.0.0.0",
            "port": 9623,
            "log_level": "info",
        }
        if use_ssl:
            config_kwargs["ssl_certfile"] = str(SSL_CERT)
            config_kwargs["ssl_keyfile"] = str(SSL_KEY)

        uvicorn.run(starlette_app, **config_kwargs)
    else:
        # stdio模式 —— 标准MCP连接
        mcp.run(transport="stdio")
