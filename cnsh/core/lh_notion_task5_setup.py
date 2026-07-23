#!/usr/bin/env python3
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# 1 道统层 Dao           : 曾仕强老师
# 2 精神层 Spirit        : Steve Jobs
# 3 设备层 Device        : Apple
# 4 技术层 Technology    : Open Source
# 5 系统层 System        : UID9622
# 6 生命层 Life          : CNSH · LongHun (诸葛鑫 / 龍芯北辰)
# DNA追溯码:#龍芯⚡️2026-06-02-CNSH-SOVEREIGN-PUBLISH-METADATA-FILE1228-v2.0
# 铁律: 来源不可删 · 影响不可覆 · 贡献不可抹 (rule_01 来源必标)
# 文件: notion_task5_setup.py | 标记时间: 2026-06-03T07:46:12+0800
# -*- coding: utf-8 -*-
"""
🐉 龍魂 Task #5 · Notion 知识图谱创建脚本
DNA: #龍芯⚇️2026-06-01-NOTION-TASK5-SETUP-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

为 Task #5 创建四个关键数据库：
1. CNSH 纠错规则库
2. IPA 节点注册表
3. 健康检查日志
4. API 指标库

并优化导航结构（四大导航卡 + 左侧菜单分类）
"""

import os
import json
import hashlib
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 配置
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

from integrated_modules.longhun_config import getenv

NOTION_TOKEN = getenv("NOTION_TOKEN", "")
NOTION_PARENT_PAGE_ID = getenv("DB_LU", "")  # 父页面ID（主脑/核心记忆库）

NOTION_API_URL = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"

HOME = Path.home()
CONFIG_DIR = HOME / ".龍魂_config"
CONFIG_DIR.mkdir(parents=True, exist_ok=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 工具函数
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def make_dna(type_code: str) -> str:
    """生成 DNA 追溯码"""
    h = hashlib.sha256(f"{type_code}|{datetime.now().isoformat()}".encode()).hexdigest()[:12].upper()
    ts = datetime.now().strftime("%Y%m%d")
    return f"#龍芯⚇️{ts}-{type_code}-{h}"

def log(level: str, msg: str, data: Dict[str, Any] = None):
    """日志输出"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if data is None:
        data = {}
    print(f"[{timestamp}] [{level}] {msg} {json.dumps(data, ensure_ascii=False)}")

def make_headers() -> Dict[str, str]:
    """创建 Notion API 请求头"""
    return {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }

def notion_request(method: str, endpoint: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
    """发送 Notion API 请求"""
    url = f"{NOTION_API_URL}{endpoint}"
    headers = make_headers()

    try:
        if method == "GET":
            resp = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            resp = requests.post(url, headers=headers, json=data, timeout=10)
        elif method == "PATCH":
            resp = requests.patch(url, headers=headers, json=data, timeout=10)
        else:
            return {"ok": False, "error": f"未知方法: {method}"}

        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        return {"ok": False, "error": str(e)}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 数据库创建函数
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def create_cnsh_rules_database() -> Dict[str, Any]:
    """创建 CNSH 纠错规则库"""
    log("INFO", "创建 CNSH 纠错规则库...", {})

    # 定义数据库架构
    properties = {
        "名称": {"title": {}},
        "规则ID": {"rich_text": {}},
        "分类": {
            "select": {
                "options": [
                    {"name": "语法规则", "color": "blue"},
                    {"name": "语义规则", "color": "purple"},
                    {"name": "逻辑规则", "color": "yellow"},
                    {"name": "约定规则", "color": "green"},
                    {"name": "安全规则", "color": "red"},
                ]
            }
        },
        "错误示例": {"rich_text": {}},
        "正确示例": {"rich_text": {}},
        "优先级": {
            "select": {
                "options": [
                    {"name": "🔴 Critical", "color": "red"},
                    {"name": "🟠 High", "color": "orange"},
                    {"name": "🟡 Medium", "color": "yellow"},
                    {"name": "🟢 Low", "color": "green"},
                ]
            }
        },
        "说明": {"rich_text": {}},
        "DNA": {"rich_text": {}},
        "创建时间": {"created_time": {}},
        "最后编辑": {"last_edited_time": {}},
    }

    db_config = {
        "parent": {"type": "workspace", "workspace": True},
        "title": [{"type": "text", "text": {"content": "📚 CNSH 纠错规则库"}}],
        "icon": {"type": "emoji", "emoji": "📚"},
        "properties": properties,
    }

    result = notion_request("POST", "/databases", db_config)

    if "id" in result:
        db_id = result["id"]
        log("SUCCESS", "CNSH 纠错规则库创建成功", {"id": db_id})
        return {"ok": True, "name": "CNSH规则库", "id": db_id}
    else:
        log("ERROR", "CNSH 纠错规则库创建失败", result)
        return {"ok": False, "error": result.get("message", "未知错误")}

def create_ipa_nodes_database() -> Dict[str, Any]:
    """创建 IPA 节点注册表"""
    log("INFO", "创建 IPA 节点注册表...", {})

    properties = {
        "节点编号": {"title": {}},
        "节点类型": {
            "select": {
                "options": [
                    {"name": "GATE (门)", "color": "blue"},
                    {"name": "CENTER (中心)", "color": "purple"},
                    {"name": "NODE (节点)", "color": "green"},
                    {"name": "ROUTE (路由)", "color": "yellow"},
                    {"name": "WIDGET (组件)", "color": "red"},
                ]
            }
        },
        "名称": {"rich_text": {}},
        "描述": {"rich_text": {}},
        "状态": {
            "select": {
                "options": [
                    {"name": "🟢 活跃", "color": "green"},
                    {"name": "🟡 待审", "color": "yellow"},
                    {"name": "🔴 禁用", "color": "red"},
                ]
            }
        },
        "父节点": {"rich_text": {}},
        "子节点": {"rich_text": {}},
        "DNA": {"rich_text": {}},
        "创建时间": {"created_time": {}},
    }

    db_config = {
        "parent": {"type": "workspace", "workspace": True},
        "title": [{"type": "text", "text": {"content": "🔗 IPA 节点注册表"}}],
        "icon": {"type": "emoji", "emoji": "🔗"},
        "properties": properties,
    }

    result = notion_request("POST", "/databases", db_config)

    if "id" in result:
        db_id = result["id"]
        log("SUCCESS", "IPA 节点注册表创建成功", {"id": db_id})
        return {"ok": True, "name": "IPA节点表", "id": db_id}
    else:
        log("ERROR", "IPA 节点注册表创建失败", result)
        return {"ok": False, "error": result.get("message", "未知错误")}

def create_health_check_database() -> Dict[str, Any]:
    """创建健康检查日志库"""
    log("INFO", "创建健康检查日志库...", {})

    properties = {
        "时间": {"title": {}},
        "服务": {
            "select": {
                "options": [
                    {"name": "MCP-mini", "color": "blue"},
                    {"name": "API网关", "color": "purple"},
                    {"name": "对话服务", "color": "green"},
                    {"name": "Ollama", "color": "yellow"},
                    {"name": "系统", "color": "orange"},
                ]
            }
        },
        "检查项": {"rich_text": {}},
        "状态": {
            "select": {
                "options": [
                    {"name": "🟢 正常", "color": "green"},
                    {"name": "🟡 警告", "color": "yellow"},
                    {"name": "🔴 异常", "color": "red"},
                ]
            }
        },
        "耗时(ms)": {"number": {"format": "number"}},
        "详情": {"rich_text": {}},
        "DNA": {"rich_text": {}},
        "记录时间": {"created_time": {}},
    }

    db_config = {
        "parent": {"type": "workspace", "workspace": True},
        "title": [{"type": "text", "text": {"content": "📊 健康检查日志"}}],
        "icon": {"type": "emoji", "emoji": "📊"},
        "properties": properties,
    }

    result = notion_request("POST", "/databases", db_config)

    if "id" in result:
        db_id = result["id"]
        log("SUCCESS", "健康检查日志库创建成功", {"id": db_id})
        return {"ok": True, "name": "健康检查日志", "id": db_id}
    else:
        log("ERROR", "健康检查日志库创建失败", result)
        return {"ok": False, "error": result.get("message", "未知错误")}

def create_api_metrics_database() -> Dict[str, Any]:
    """创建 API 指标库"""
    log("INFO", "创建 API 指标库...", {})

    properties = {
        "时间": {"title": {}},
        "端点": {"rich_text": {}},
        "方法": {
            "select": {
                "options": [
                    {"name": "GET", "color": "blue"},
                    {"name": "POST", "color": "green"},
                    {"name": "PUT", "color": "yellow"},
                    {"name": "DELETE", "color": "red"},
                ]
            }
        },
        "吞吐(req/s)": {"number": {"format": "number"}},
        "延迟(ms)": {"number": {"format": "number"}},
        "成功率(%)": {"number": {"format": "percent"}},
        "错误计数": {"number": {"format": "number"}},
        "状态码分布": {"rich_text": {}},
        "DNA": {"rich_text": {}},
        "记录时间": {"created_time": {}},
    }

    db_config = {
        "parent": {"type": "workspace", "workspace": True},
        "title": [{"type": "text", "text": {"content": "📈 API 指标库"}}],
        "icon": {"type": "emoji", "emoji": "📈"},
        "properties": properties,
    }

    result = notion_request("POST", "/databases", db_config)

    if "id" in result:
        db_id = result["id"]
        log("SUCCESS", "API 指标库创建成功", {"id": db_id})
        return {"ok": True, "name": "API指标库", "id": db_id}
    else:
        log("ERROR", "API 指标库创建失败", result)
        return {"ok": False, "error": result.get("message", "未知错误")}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 主程序
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    """主程序"""
    banner = """
╔══════════════════════════════════════╗
║  🐉 Task #5 Notion 数据库创建        ║
║  Knowledge Graph Setup                ║
╚══════════════════════════════════════╝

DNA: #龍芯⚇️2026-06-01-NOTION-TASK5-SETUP-v1.0
"""
    print(banner)

    # 验证 Token
    if not NOTION_TOKEN:
        log("ERROR", "NOTION_TOKEN 未设置", {})
        print("\n请设置环境变量:")
        print("  export NOTION_TOKEN=ntn_xxxxxxxxxxxxx")
        return False

    log("INFO", "Notion Token 已配置", {"token": NOTION_TOKEN[:20] + "..."})

    # 创建数据库
    databases = {}
    results = []

    print("\n📦 开始创建数据库...\n")

    # 1. CNSH 纠错规则库
    result = create_cnsh_rules_database()
    results.append(result)
    if result["ok"]:
        databases["CNSH_RULES"] = result["id"]

    # 2. IPA 节点注册表
    result = create_ipa_nodes_database()
    results.append(result)
    if result["ok"]:
        databases["IPA_NODES"] = result["id"]

    # 3. 健康检查日志
    result = create_health_check_database()
    results.append(result)
    if result["ok"]:
        databases["HEALTH_CHECK"] = result["id"]

    # 4. API 指标库
    result = create_api_metrics_database()
    results.append(result)
    if result["ok"]:
        databases["API_METRICS"] = result["id"]

    # 保存配置
    print("\n💾 保存数据库配置...\n")
    config_file = CONFIG_DIR / "task5_notion_databases.json"
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(
            {
                "created_at": datetime.now().isoformat(),
                "dna": make_dna("NOTION-TASK5"),
                "databases": databases,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

    log("SUCCESS", "配置已保存", {"file": str(config_file)})

    # 总结
    print("\n" + "=" * 50)
    print("📋 创建结果总结")
    print("=" * 50 + "\n")

    successful = sum(1 for r in results if r.get("ok"))
    total = len(results)

    for result in results:
        status = "✅" if result["ok"] else "❌"
        msg = result.get("name", "未知") if result["ok"] else result.get("error", "未知错误")
        print(f"{status} {msg}")
        if result["ok"]:
            print(f"   ID: {result['id']}\n")

    print("=" * 50)
    print(f"成功: {successful}/{total} 个数据库\n")

    if successful == total:
        print("✨ 所有数据库创建成功！")
        print(f"📍 配置文件: {config_file}")
        return True
    else:
        print("⚠️  部分数据库创建失败，请检查 Notion Token 和权限")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
