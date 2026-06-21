#!/usr/bin/env python3
# 龍魂宝宝守护助手 · FastAPI 后端
# DNA:#龍芯⚡️2026-06-04-BAOBAO-BACKEND-FILE1-v1.0

import asyncio
import json
import logging
from typing import Dict, Set
from datetime import datetime

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════
# 全局状态
# ═══════════════════════════════════════════════════════════

class OverlayState:
    def __init__(self):
        self.level: str = "safe"  # safe | warning | danger
        self.color: str = "#00FF00"
        self.intensity: float = 0.05
        self.message: str = ""
        self.last_update: str = datetime.now().isoformat()

    def to_dict(self):
        return {
            "level": self.level,
            "color": self.color,
            "intensity": self.intensity,
            "message": self.message,
            "timestamp": self.last_update,
        }

class ConnectionManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        self.overlay_state = OverlayState()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"✅ 客户端已连接 (总数: {len(self.active_connections)})")

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)
        logger.info(f"❌ 客户端已断开 (总数: {len(self.active_connections)})")

    async def broadcast(self, message: Dict):
        """广播消息给所有连接的客户端"""
        disconnected = set()

        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.warning(f"⚠️  广播失败: {e}")
                disconnected.add(connection)

        # 移除失效连接
        for conn in disconnected:
            self.active_connections.discard(conn)

    async def send_personal(self, websocket: WebSocket, message: Dict):
        """发送个人消息"""
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"❌ 发送失败: {e}")

# ═══════════════════════════════════════════════════════════
# 初始化
# ═══════════════════════════════════════════════════════════

manager = ConnectionManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 龍魂宝宝守护助手后端启动")
    logger.info("🌐 WebSocket 服务: ws://localhost:8000/ws/overlay")
    logger.info("📡 HTTP API: http://localhost:8000")
    yield
    logger.info("🛑 后端服务停止")

app = FastAPI(
    title="龍魂宝宝守护助手",
    description="宝宝助手系统后端 API",
    version="1.0.0",
    lifespan=lifespan,
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ═══════════════════════════════════════════════════════════
# WebSocket 连接
# ═══════════════════════════════════════════════════════════

@app.websocket("/ws/overlay")
async def websocket_endpoint(websocket: WebSocket):
    """Overlay 层 WebSocket"""
    await manager.connect(websocket)

    try:
        while True:
            # 接收来自客户端的消息
            data = await websocket.receive_json()
            logger.info(f"📨 收到消息: {data}")

            # 更新 Overlay 状态
            if "level" in data:
                level = data["level"]
                level_config = {
                    "safe": {
                        "color": "#00FF00",
                        "intensity": 0.05,
                    },
                    "warning": {
                        "color": "#FFA500",
                        "intensity": 0.15,
                    },
                    "danger": {
                        "color": "#FF0000",
                        "intensity": 0.3,
                    },
                }

                if level in level_config:
                    config = level_config[level]
                    manager.overlay_state.level = level
                    manager.overlay_state.color = config["color"]
                    manager.overlay_state.intensity = config["intensity"]
                    manager.overlay_state.last_update = datetime.now().isoformat()

            # 广播给所有客户端
            await manager.broadcast(
                {
                    "type": "overlay",
                    "payload": manager.overlay_state.to_dict(),
                }
            )

    except WebSocketDisconnect:
        await manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"❌ WebSocket 错误: {e}")
        await manager.disconnect(websocket)

# ═══════════════════════════════════════════════════════════
# REST API
# ═══════════════════════════════════════════════════════════

@app.get("/")
async def root():
    """健康检查"""
    return {
        "status": "ok",
        "service": "龍魂宝宝守护助手",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
    }

@app.get("/health")
async def health():
    """健康检查端点"""
    return {
        "status": "healthy",
        "connections": len(manager.active_connections),
        "overlay_state": manager.overlay_state.to_dict(),
    }

@app.post("/api/overlay/level")
async def set_overlay_level(level: str):
    """设置 Overlay 层级别"""
    if level not in ["safe", "warning", "danger"]:
        return {"error": "Invalid level"}

    manager.overlay_state.level = level

    # 广播更新
    await manager.broadcast(
        {
            "type": "overlay",
            "payload": manager.overlay_state.to_dict(),
        }
    )

    return {"status": "ok", "level": level}

@app.post("/api/baobao/speak")
async def baobao_speak(message: str, emotion: str = "happy", duration: int = 3000):
    """宝宝说话"""
    await manager.broadcast(
        {
            "type": "baobao",
            "payload": {
                "message": message,
                "emotion": emotion,
                "duration": duration,
            },
        }
    )

    return {"status": "ok", "message": message}

@app.post("/api/baobao/react")
async def baobao_react(emotion: str):
    """宝宝反应"""
    await manager.broadcast(
        {
            "type": "baobao",
            "payload": {
                "expression": emotion,
            },
        }
    )

    return {"status": "ok", "emotion": emotion}

@app.get("/api/stats")
async def get_stats():
    """获取统计信息"""
    return {
        "active_connections": len(manager.active_connections),
        "overlay_state": manager.overlay_state.to_dict(),
        "timestamp": datetime.now().isoformat(),
    }

# ═══════════════════════════════════════════════════════════
# 启动
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )
