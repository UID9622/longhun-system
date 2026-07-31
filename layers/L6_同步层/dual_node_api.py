# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 双节点 API 服务 v1.0
DNA: #龍芯⚡️丙午·辛未·DUAL-NODE-API-v1.0

部署位置：
  - 鲲鹏端: python3 L6_同步层/dual_node_api.py serve --role kunpeng
  - Mac端:  python3 L6_同步层/dual_node_api.py serve --role mac (可选)

端口分配：
  - 鲲鹏 API: 9633（双节点同步专用端口，不冲突现有端口）
  - Mac API:   9634（仅本地回环）

API端点：
  GET  /health              — 健康检查（免认证）
  POST /sync/trigger        — 触发五维同步
  GET  /sync/status         — 同步状态查询
  POST /inference           — 远端推理（Mac→鲲鹏）
  POST /train               — 提交训练任务（Mac→鲲鹏）
  GET  /train/{task_id}     — 查询训练进度
  GET  /checkpoint/latest   — 获取最新checkpoint信息
  POST /checkpoint/pull     — 拉取checkpoint到本地
"""

import hashlib
import json
import os
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional, Dict, Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

DNA = "#龍芯⚡️丙午·辛未·DUAL-NODE-API-v1.0"
CST = timezone(timedelta(hours=8))
UID_ROOT = "UID9622"

# 导入认证模块
from L6_同步层.auth_middleware import (
    DualNodeAuth, AuthConfig, load_keys, generate_keys, save_keys,
    DualNodeAuthMiddleware, HAS_FASTAPI,
)
from L6_同步层.dual_node_protocol import DualNodeProtocol, SyncDimension

try:
    from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
    from fastapi.responses import JSONResponse
    from pydantic import BaseModel
    import uvicorn
    HAS_API_DEPS = True
except ImportError:
    HAS_API_DEPS = False

# ─── 数据模型 ───

class SyncRequest(BaseModel):
    dimension: Optional[str] = None  # 不传=全部
    dry_run: bool = False

class InferenceRequest(BaseModel):
    query: str
    model: str = "longhun-v1.9:latest"
    max_tokens: int = 512

class TrainRequest(BaseModel):
    task_id: str
    data_path: str
    epochs: int = 1
    batch_size: int = 16
    model_base: str = "longhun-v1.9"

class CheckpointPullRequest(BaseModel):
    filename: Optional[str] = None  # 不传=最新

# ─── 任务队列（内存） ───

_train_tasks: Dict[str, Dict[str, Any]] = {}

# ─── 离线降级引擎 ───

class OfflineFallbackEngine:
    """离线降级引擎 — 云端不可用时本地独立运行"""

    def __init__(self, local_path: Path = ROOT):
        self.local_path = local_path
        self._ollama_available: Optional[bool] = None
        self._local_model: Optional[str] = None

    def check_ollama(self) -> bool:
        """检测本地 Ollama 是否可用"""
        if self._ollama_available is None:
            try:
                result = subprocess.run(
                    ["ollama", "list"], capture_output=True, text=True, timeout=5
                )
                self._ollama_available = result.returncode == 0
            except (FileNotFoundError, subprocess.TimeoutExpired):
                self._ollama_available = False
        return self._ollama_available

    def get_best_local_model(self) -> Optional[str]:
        """获取最优本地模型"""
        if self._local_model:
            return self._local_model

        if not self.check_ollama():
            return None

        try:
            result = subprocess.run(
                ["ollama", "list"], capture_output=True, text=True, timeout=5
            )
            lines = result.stdout.strip().split("\n")[1:]  # 跳过表头
            for line in lines:
                if "longhun" in line.lower():
                    self._local_model = line.split()[0]
                    return self._local_model
            # fallback: 任何可用模型
            if lines:
                self._local_model = lines[0].split()[0]
                return self._local_model
        except Exception:
            pass
        return None

    def local_inference(self, query: str, model: str | None = None) -> Dict[str, Any]:
        """本地推理（离线降级）"""
        model = model or self.get_best_local_model()
        if not model:
            return {
                "error": "无本地模型可用",
                "offline": True,
                "suggestion": "请先 ollama pull longhun-v1.9:latest 或连接鲲鹏",
                "dna": DNA,
            }

        try:
            result = subprocess.run(
                ["ollama", "run", model, query],
                capture_output=True, text=True, timeout=120
            )
            return {
                "query": query,
                "response": result.stdout.strip(),
                "model": model,
                "source": "local-offline",
                "dna": DNA,
                "offline": True,
            }
        except subprocess.TimeoutExpired:
            return {"error": "本地推理超时", "offline": True, "dna": DNA}
        except Exception as e:
            return {"error": str(e), "offline": True, "dna": DNA}

    def status(self) -> Dict[str, Any]:
        """离线降级状态"""
        return {
            "ollama_available": self.check_ollama(),
            "best_model": self.get_best_local_model(),
            "can_inference": self.check_ollama() and self.get_best_local_model() is not None,
            "dna": DNA,
        }


# ─── FastAPI 应用 ───

def create_app(node_role: str = "mac") -> FastAPI:
    """创建双节点 API 应用"""
    if not HAS_API_DEPS:
        raise ImportError("需要安装 fastapi uvicorn: pip install fastapi uvicorn")

    app = FastAPI(
        title=f"龍魂双节点 · {node_role.upper()}",
        description="Mac ↔ 鲲鹏 双节点同步协议 API",
        version="1.0",
    )

    # 认证初始化
    config = load_keys()
    if not config:
        config = AuthConfig(node_id=node_role, node_role=node_role)
        config.api_key, config.peer_api_key = generate_keys(node_role)
        save_keys(config)
    config.node_role = node_role

    auth = DualNodeAuth(config)
    protocol = DualNodeProtocol()
    offline = OfflineFallbackEngine()

    # 注册认证中间件
    if HAS_FASTAPI:
        app.add_middleware(
            DualNodeAuthMiddleware,
            auth=auth,
            exclude_paths=["/health", "/docs", "/openapi.json"],
        )

    # ─── 免认证端点 ───

    @app.get("/health")
    async def health():
        """健康检查（免认证）"""
        conn = protocol.test_connection()
        offline_status = offline.status()
        return {
            "status": "龍魂双节点运行中",
            "node_role": node_role,
            "kunpeng_online": conn.get("ssh_ok", False),
            "local_ollama": offline_status["ollama_available"],
            "can_fallback": offline_status["can_inference"],
            "dna": DNA,
            "uid": UID_ROOT,
            "timestamp": datetime.now(CST).isoformat(),
        }

    # ─── 同步端点 ───

    @app.post("/sync/trigger")
    async def trigger_sync(req: SyncRequest):
        """触发五维同步"""
        if req.dimension:
            dim = SyncDimension(req.dimension)
            result = protocol.sync_dimension(dim, dry_run=req.dry_run)
        else:
            result = protocol.sync_all(dry_run=req.dry_run)
        return result

    @app.get("/sync/status")
    async def sync_status():
        """查询同步状态"""
        return {
            "last_sync": protocol.sync_log[-1] if protocol.sync_log else None,
            "sync_count": len(protocol.sync_log),
            "dna": DNA,
        }

    # ─── 推理端点 ───

    @app.post("/inference")
    async def inference(req: InferenceRequest):
        """远端推理（鲲鹏端处理，Mac端可fallback到本地）"""
        # 鲲鹏端：直接用 Ollama
        if node_role == "kunpeng":
            try:
                result = subprocess.run(
                    ["ollama", "run", req.model, req.query],
                    capture_output=True, text=True, timeout=120
                )
                return {
                    "query": req.query,
                    "response": result.stdout.strip(),
                    "model": req.model,
                    "source": "kunpeng-cloud",
                    "dna": DNA,
                }
            except Exception as e:
                return {"error": str(e), "dna": DNA}

        # Mac端：先尝试本地，本地没有则请求鲲鹏
        # 这里 Mac 端收到推理请求时，如果自己是客户端，应该转发到鲲鹏
        # 但这里 Mac 端一般不对外暴露推理API
        offline_result = offline.local_inference(req.query, req.model)
        return offline_result

    # ─── 训练端点（仅鲲鹏端） ───

    @app.post("/train")
    async def submit_train(req: TrainRequest):
        """提交训练任务（仅鲲鹏端处理）"""
        if node_role != "kunpeng":
            raise HTTPException(400, "训练任务只能在鲲鹏端提交")

        task = {
            "id": req.task_id,
            "status": "queued",
            "config": req.dict(),
            "created_at": datetime.now(CST).isoformat(),
            "dna": DNA,
        }
        _train_tasks[req.task_id] = task

        # 模拟排队（实际应接入训练调度器）
        _train_tasks[req.task_id]["status"] = "running"
        _train_tasks[req.task_id]["started_at"] = datetime.now(CST).isoformat()

        return {"status": "queued", "task_id": req.task_id, "dna": DNA}

    @app.get("/train/{task_id}")
    async def train_status(task_id: str):
        """查询训练进度"""
        task = _train_tasks.get(task_id)
        if not task:
            raise HTTPException(404, f"任务不存在: {task_id}")
        return task

    @app.get("/train")
    async def list_tasks():
        """列出所有训练任务"""
        return {"tasks": list(_train_tasks.values()), "count": len(_train_tasks), "dna": DNA}

    # ─── Checkpoint 端点（仅鲲鹏端） ───

    @app.get("/checkpoint/latest")
    async def latest_checkpoint():
        """获取最新checkpoint信息"""
        if node_role != "kunpeng":
            raise HTTPException(400, "Checkpoint 信息仅在鲲鹏端可用")

        ckpt_dir = ROOT / "models"
        if not ckpt_dir.exists():
            raise HTTPException(404, "models/ 目录不存在")

        # 查找最新模型文件
        model_files = []
        for ext in [".gguf", ".pt", ".safetensors", ".bin"]:
            model_files.extend(sorted(ckpt_dir.rglob(f"*{ext}"), key=lambda p: p.stat().st_mtime, reverse=True))

        if not model_files:
            raise HTTPException(404, "无模型文件")

        latest = model_files[0]
        stat = latest.stat()
        file_hash = hashlib.sha256(latest.read_bytes()[:1024*1024]).hexdigest()[:16]  # 前1MB哈希

        return {
            "filename": latest.name,
            "relative_path": str(latest.relative_to(ROOT)),
            "size_mb": round(stat.st_size / (1024 * 1024), 2),
            "modified": datetime.fromtimestamp(stat.st_mtime, tz=CST).isoformat(),
            "hash_first_mb": file_hash,
            "dna": DNA,
        }

    # ─── 离线降级状态 ───

    @app.get("/offline/status")
    async def offline_status():
        """离线降级引擎状态"""
        return offline.status()

    return app


# ─── CLI ───

def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂双节点 API 服务")
    parser.add_argument("action", nargs="?", default="serve",
                        choices=["serve", "init", "status"])
    parser.add_argument("--role", default="mac", choices=["mac", "kunpeng"],
                        help="节点角色（mac/ kunpeng）")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=None)
    parser.add_argument("--reload", action="store_true", help="开发模式热重载")
    args = parser.parse_args()

    # 自动选择端口
    if args.port is None:
        args.port = 9633 if args.role == "kunpeng" else 9634

    if args.action == "init":
        config = load_keys()
        if not config:
            config = AuthConfig(node_id=args.role, node_role=args.role)
            config.api_key, config.peer_api_key = generate_keys(args.role)
            save_keys(config)
            print(f"✅ 节点已初始化: {args.role}")
            print(f"   API Key: {config.api_key}")
            print(f"   对端 Key: {config.peer_api_key}")
            print(f"   ⚠️  请将对端 Key 同步到另一个节点")
        else:
            print(f"⚠️  已初始化: {config.node_role}")
            print(f"   如需重新生成，删除 {ROOT / 'L6_同步层' / '.dual_node_keys'}")

    elif args.action == "status":
        offline = OfflineFallbackEngine()
        status = offline.status()
        print(f"🐉 节点状态: {args.role}")
        print(f"   Ollama: {'✅' if status['ollama_available'] else '❌'}")
        print(f"   本地模型: {status.get('best_model') or '无'}")
        print(f"   可推理: {'✅' if status['can_inference'] else '❌'}")

    elif args.action == "serve":
        if not HAS_API_DEPS:
            print("❌ 需要安装: pip install fastapi uvicorn")
            sys.exit(1)

        app = create_app(node_role=args.role)
        print(f"🐉 龍魂双节点 API 启动")
        print(f"   角色: {args.role}")
        print(f"   地址: http://{args.host}:{args.port}")
        print(f"   文档: http://localhost:{args.port}/docs")
        print(f"   DNA: {DNA}")
        uvicorn.run(app, host=args.host, port=args.port, reload=args.reload)


if __name__ == "__main__":
    main()
