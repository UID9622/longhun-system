#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·未济-FIX_DNA-v1.0
# api/main.py
# 龍魂 · FastAPI主服务 · 教育AI全栈入口

import os
import sys
import time
import hashlib
from datetime import datetime
from typing import List, Dict, Optional

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
import uvicorn

# 添加核心模块路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.rag.rag_service import RAGService
from core.agent.education_agent import EducationAgent
from core.tools.tool_registry import registry

# === DNA常量 ===
MASTER_DNA = "ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️"
MASTER_UID = "9622"
CONFIRM_SEAL = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

# === 初始化服务 ===
rag_service = RAGService()
agent = EducationAgent(rag_service=rag_service)

app = FastAPI(
    title="龍魂教育AI系统",
    description="RAG + Agent + Function Calling 全栈融合",
    version="4.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 安全
security = HTTPBearer()


# === 数据模型 ===

class ChatRequest(BaseModel):
    """聊天请求"""
    message: str = Field(..., description="用户消息")
    session_id: Optional[str] = Field(None, description="会话ID")
    context: Optional[Dict] = Field(None, description="上下文信息")


class ChatResponse(BaseModel):
    """聊天响应"""
    response: str
    intent: str
    sources: List[Dict]
    confidence: float
    tools_used: List[str]
    processing_time: float
    dna_signature: str


class RAGQueryRequest(BaseModel):
    """RAG查询请求"""
    query: str = Field(..., description="查询问题")
    top_k: int = Field(5, description="返回数量")
    filter: Optional[Dict] = Field(None, description="过滤条件")


class RAGQueryResponse(BaseModel):
    """RAG查询响应"""
    answer: str
    sources: List[Dict]
    confidence: float
    processing_time: float


class ToolExecuteRequest(BaseModel):
    """工具执行请求"""
    tool_name: str
    parameters: Dict


class ToolExecuteResponse(BaseModel):
    """工具执行响应"""
    result: str
    status: str
    tool: str


class DocumentUploadRequest(BaseModel):
    """文档上传请求"""
    file_path: str
    metadata: Optional[Dict] = None


# === 中间件 ===

@app.middleware("http")
async def audit_log(request: Request, call_next):
    """审计日志中间件"""
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "method": request.method,
        "path": request.url.path,
        "duration": round(duration, 3),
        "status": response.status_code,
        "client": request.client.host if request.client else "unknown"
    }
    
    print(f"[龍魂·审计] {log_entry}")
    
    return response


# === API路由 ===

@app.get("/")
async def root():
    """根路径"""
    return {
        "name": "龍魂教育AI系统",
        "version": "4.0.0",
        "dna": MASTER_DNA,
        "uid": MASTER_UID,
        "status": "running",
        "modules": ["RAG", "Agent", "FunctionCalling"]
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "rag": rag_service is not None,
            "agent": agent is not None,
            "tools": len(registry.list_tools())
        }
    }


@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """智能对话"""
    start_time = time.time()
    
    # Agent处理
    result = agent.process(request.message)
    
    tools_used = result.get("tools", [])
    processing_time = time.time() - start_time
    
    return ChatResponse(
        response=result["response"],
        intent=result["intent"],
        sources=[],
        confidence=0.9,
        tools_used=tools_used,
        processing_time=processing_time,
        dna_signature=f"SM3-{hashlib.sha256(request.message.encode()).hexdigest()[:16]}"
    )


@app.post("/api/v1/rag/query", response_model=RAGQueryResponse)
async def rag_query(request: RAGQueryRequest):
    """RAG检索"""
    start_time = time.time()
    
    response = rag_service.query(request.query, request.filter)
    processing_time = time.time() - start_time
    
    return RAGQueryResponse(
        answer=response.answer,
        sources=[{
            "content": s.content,
            "source": s.source,
            "page": s.page,
            "score": s.score
        } for s in response.sources],
        confidence=response.confidence,
        processing_time=processing_time
    )


@app.post("/api/v1/tools/execute", response_model=ToolExecuteResponse)
async def execute_tool(request: ToolExecuteRequest):
    """工具执行"""
    result = registry.execute(request.tool_name, request.parameters)
    
    return ToolExecuteResponse(
        result=str(result.get("result", result.get("error", "未知"))),
        status=result.get("status", "unknown"),
        tool=request.tool_name
    )


@app.get("/api/v1/tools/list")
async def list_tools():
    """列出所有可用工具"""
    return {
        "tools": [
            {
                "name": t.name,
                "description": t.description,
                "category": t.category.value,
                "parameters": t.parameters,
                "required": t.required,
                "dangerous": t.dangerous
            }
            for t in registry.list_tools()
        ]
    }


@app.post("/api/v1/documents/ingest")
async def ingest_document(request: DocumentUploadRequest):
    """导入文档到知识库"""
    try:
        rag_service.ingest_documents([request.file_path])
        return {
            "status": "success",
            "message": f"文档导入完成: {request.file_path}",
            "dna": f"SM3-{hashlib.sha256(request.file_path.encode()).hexdigest()[:16]}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/agent/memory")
async def get_agent_memory():
    """获取Agent记忆快照"""
    return agent.get_memory_snapshot()


@app.post("/api/v1/agent/reset")
async def reset_agent_memory():
    """重置Agent短期记忆"""
    agent.memory.short_term = []
    return {"status": "success", "message": "记忆已重置"}


# === 启动 ===
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
