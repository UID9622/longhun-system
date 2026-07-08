#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 中国国家数字身份统一认证入口 v2.0 · API 服务
China National Digital Identity Unified Authentication Portal v2.0 API

提供：
  - / 主权宣言 + 网页入口
  - /api/info 信息接口
  - /issue 签发魂灵ID通行令牌
  - /verify 服务商验证身份
  - /register 服务商接入注册

监听：0.0.0.0:8444

DNA:#龍芯⚡️2026-06-20-CHINA-DIGITAL-IDENTITY-API-FILE1-v2.0
"""

import sys
import os
import json
from pathlib import Path
from typing import Any, Dict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 挂载新路由
from model_router import router as model_router
from knowledge_api import router as knowledge_router, _get_graph, _archive_docs_list

# 确保能找到 static 目录
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

# 尝试加载审计模块（支持本地开发和服务器两种目录结构）
_BASE = os.path.dirname(os.path.abspath(__file__))
_AUDIT_CANDIDATES = [
    os.path.join(_BASE, "audit"),
    os.path.join(_BASE, "..", "audit"),
    os.path.join(_BASE, "..", "..", "audit"),
]
for _audit_path in _AUDIT_CANDIDATES:
    if os.path.isdir(_audit_path):
        sys.path.insert(0, os.path.abspath(_audit_path))
        break

try:
    from system_guardian import 系统守护者  # type: ignore[import-untyped]
except Exception:
    系统守护者 = None

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles  # type: ignore[import-untyped]
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware  # type: ignore[import-untyped]
from pydantic import BaseModel
from 国家数字身份统一认证入口 import 魂灵ID, 服务商接入点, 国家数字身份统一认证中心

app = FastAPI(
    title="中国国家数字身份统一认证入口 v2.0",
    description="人民数据主权，平台服务降级。龍芯 × 华为 × CNSH 融合。",
    version="2.0.0"
)

# 允许本地文件 / 任何来源访问公开状态接口（健康检查与信息接口）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# 挂载新路由
app.include_router(model_router)
app.include_router(knowledge_router)

# 挂载静态页面
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

中心 = 国家数字身份统一认证中心()


def _find_skills_registry() -> Path:
    candidates = [
        os.environ.get("LONGHUN_SKILLS_REGISTRY", ""),
        str(Path.home() / "Downloads" / "Kimi_Agent_终端升级与结构优化 7" / "skills" / "registry.json"),
        str(Path.home() / "Downloads" / "Kimi_Agent_终端升级与结构优化 6" / "skills" / "registry.json"),
        "/root/longhun-sovereignty/skills/registry.json",
    ]
    for c in candidates:
        if c and Path(c).exists():
            return Path(c)
    return None  # type: ignore[return-value]


class 签发请求(BaseModel):
    身份证编号: str
    姓名: str = ""
    有效期小时: int = 24


class 验证请求(BaseModel):
    令牌: Dict[str, Any]
    服务商名称: str
    服务类型: str


class 注册请求(BaseModel):
    服务商名称: str
    服务类型: str


@app.get("/")
def 根节点():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


@app.get("/developer.html")
def 开发者门户页():
    return FileResponse(os.path.join(STATIC_DIR, "developer.html"))


@app.get("/health")
def 健康检查():
    base: Dict[str, Any] = {"status": "unknown", "note": "system guardian not loaded"}
    if 系统守护者 is not None:
        base = 系统守护者().全检()

    # 附加公开知识库与模型可用性摘要（不触发网络探测，仅环境配置摘要）
    try:
        graph = _get_graph()
        knowledge_summary = {
            "archive_docs": len(_archive_docs_list()),
            "graph_nodes": len(graph.get("nodes", [])),
            "graph_edges": len(graph.get("edges", [])),
        }
    except Exception as e:
        knowledge_summary = {"error": str(e)[:120]}

    model_summary = {
        "local_ollama_host": os.getenv("OLLAMA_HOST", "http://localhost:11434"),
        "deepseek_configured": bool(os.getenv("DEEPSEEK_API_KEY")),
        "kimi_configured": bool(os.getenv("KIMI_API_KEY")),
        "azure_configured": bool(
            os.getenv("AZURE_OPENAI_API_KEY")
            and os.getenv("AZURE_OPENAI_ENDPOINT")
            and os.getenv("AZURE_OPENAI_DEPLOYMENT")
        ),
    }

    base["knowledge"] = knowledge_summary
    base["models"] = model_summary
    base["developer_portal"] = "/developer.html"
    return base


@app.get("/api/docs")
def api_docs():
    """公开 API 文档索引"""
    return {
        "title": "龍魂开发者门户 API 文档",
        "description": "公开端点：身份认证、模型路由、知识库与图谱、技能注册表",
        "developer_portal": "/developer.html",
        "endpoints": [
            {"path": "/", "method": "GET", "desc": "主权门户首页"},
            {"path": "/health", "method": "GET", "desc": "系统健康与知识/模型摘要"},
            {"path": "/api/info", "method": "GET", "desc": "系统信息与主权宣言"},
            {"path": "/api/docs", "method": "GET", "desc": "本 API 文档"},
            {"path": "/api/skills/registry", "method": "GET", "desc": "龍魂技能注册表"},
            {"path": "/issue", "method": "POST", "desc": "签发魂灵ID通行令牌"},
            {"path": "/verify", "method": "POST", "desc": "服务商验证身份令牌"},
            {"path": "/register", "method": "POST", "desc": "服务商接入注册"},
            {"path": "/api/models", "method": "GET", "desc": "列出可用模型与状态"},
            {"path": "/api/models/status", "method": "GET", "desc": "模型状态摘要"},
            {"path": "/api/chat", "method": "POST", "desc": "统一对话（本地 > DeepSeek > Kimi > Azure）"},
            {"path": "/api/embed", "method": "POST", "desc": "文本嵌入（本地优先）"},
            {"path": "/api/archive/docs", "method": "GET", "desc": "中央藏经阁文档列表"},
            {"path": "/api/archive/doc/{name}", "method": "GET", "desc": "单篇文档详情"},
            {"path": "/api/knowledge/search", "method": "GET/POST", "desc": "代码收割知识库检索"},
            {"path": "/api/graph/nodes", "method": "GET", "desc": "知识图谱节点"},
            {"path": "/api/graph/edges", "method": "GET", "desc": "知识图谱边"},
            {"path": "/api/graph/query", "method": "POST", "desc": "节点子图查询"},
            {"path": "/api/graph/stats", "method": "GET", "desc": "图谱统计"},
        ],
    }


@app.get("/api/skills/registry")
def skills_registry():
    """返回龍魂技能注册表"""
    path = _find_skills_registry()
    if not path:
        return {"error": "skills registry not found"}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {
            "count": len(data),
            "registry": data,
        }
    except Exception as e:
        return {"error": str(e)[:200]}


@app.get("/api/info")
def 信息():
    return {
        "title": "中国国家数字身份统一认证入口 v2.0",
        "principle": "一次认证，全网通行",
        "slogan": "芯可龍，云可私，网可断，心不可失",
        "tech_stack": 中心.技术栈,
        "declaration": 中心.生成主权宣言(),
        "dna": "#龍芯⚡️2026-06-20-CHINA-DIGITAL-IDENTITY-API-v2.0"
    }


@app.post("/issue")
def 签发令牌(请求: 签发请求):
    公民 = 魂灵ID(请求.身份证编号, 请求.姓名)
    令牌 = 公民.生成通行令牌(请求.有效期小时)
    return {
        "status": "ok",
        "token": 令牌,
        "note": "此魂灵ID令牌可在所有接入服务商使用，服务商只验证不采集"
    }


@app.post("/register")
def 注册服务商(请求: 注册请求):
    服务商 = 服务商接入点(请求.服务商名称, 请求.服务类型)
    结果 = 中心.注册服务商(服务商)
    return {"status": "ok", "result": 结果}


@app.post("/verify")
def 验证身份(请求: 验证请求):
    服务商 = 服务商接入点(请求.服务商名称, 请求.服务类型)
    结果 = 服务商.验证身份(请求.令牌)
    return {"status": "ok", "result": 结果}


if __name__ == "__main__":
    import uvicorn
    print("🐉 中国国家数字身份统一认证入口 v2.0 启动")
    print("   地址: http://127.0.0.1:8444")
    print("   DNA:#龍芯⚡️2026-06-20-CHINA-DIGITAL-IDENTITY-API-v2.0")
    uvicorn.run(app, host="127.0.0.1", port=8444)
