#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 流场映射层引擎 v2.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·☴巽-FLOW-MAP-v2.0-UID9622
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

功能：
  1. 物理-信息流场同构映射（粒子、速度、涡旋、压力、热力图）
  2. 实时数据注入 API（/inject）
  3. WebSocket 动态更新（/ws）
  4. 历史流场回放（/replay）
  5. 异常检测与预警（涡旋、压力、湍流）
  6. 统一控制台（/）
  7. 自动部署静态页面到鲲鹏（--deploy）

用法：
  python3 bin/lh_flow_engine.py                    # 启动服务 (端口 8776)
  python3 bin/lh_flow_engine.py --port 8776        # 指定端口
  python3 bin/lh_flow_engine.py --deploy           # 部署静态页面
  python3 bin/lh_flow_engine.py --no-websocket     # 禁用 WebSocket
"""

import os
import sys
import json
import asyncio
import datetime
import hashlib
import time
import shutil
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict, field
from collections import deque
import numpy as np
from scipy.interpolate import griddata

try:
    from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request
    from fastapi.responses import JSONResponse, HTMLResponse
    from fastapi.middleware.cors import CORSMiddleware
    import uvicorn
except ImportError:
    print("❌ 请安装: pip install fastapi uvicorn scipy numpy")
    sys.exit(1)

# ============================================================
# 固定锚点
# ============================================================

CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
DNA_CORE = "丙午·丙申·乙巳·辛巳·☴巽-FLOW-MAP-v2.0-UID9622"
PROJECT_ROOT = Path.home() / "longhun-system"
DATA_DIR = PROJECT_ROOT / "data" / "flow"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# 物理-信息映射表（焊死）
# ============================================================

"""
物理量        符号    信息对应            作用
───────      ────    ────────            ────
粒子          质点    数据点/请求         基本载体
速度场        v       变化率/吞吐量       流动快慢与方向
流线          dx/ds   数据路径/管道       穿越路径
涡旋          ω=∇×v  回环/反馈回路        自我循环
压力          p       负载/积压           堆积压力
热力图        标量φ   密度/频率分布       热点识别
层流/湍流     Re      有序/混沌           可控性
势流          v=∇φ   结构化路由           预定策略
不可压缩      ∇·v=0   保吞吐             流量守恒

‼️ 流场≠雷达：被动观测，不发射不主动探测。
   流场告诉你"气流怎么被扰动、涡旋从哪来"——适合做攻击路径回溯和系统性脆弱点定位。
"""

# ============================================================
# 流场数据结构
# ============================================================

@dataclass
class FlowParticle:
    """流场粒子"""
    x: float
    y: float
    vx: float
    vy: float
    mass: float = 1.0
    id: str = field(default_factory=lambda: hashlib.md5(str(time.time()).encode()).hexdigest()[:8])


@dataclass
class Anomaly:
    """流场异常"""
    type: str  # "vortex" | "pressure" | "turbulence"
    severity: float  # 0-1
    location: Tuple[float, float]
    radius: float
    description: str
    timestamp: str


# ============================================================
# 流场计算引擎
# ============================================================

class FlowEngine:
    """流场核心计算引擎

    被动观测 → 计算反演 → 可视化输出。
    不发射、不主动探测。
    """

    def __init__(self, grid_size: int = 50, domain_size: float = 10.0):
        self.grid_size = grid_size
        self.domain_size = domain_size
        self.dx = domain_size / grid_size
        self.dy = domain_size / grid_size
        self.x_grid = np.linspace(-domain_size / 2, domain_size / 2, grid_size)
        self.y_grid = np.linspace(-domain_size / 2, domain_size / 2, grid_size)
        self.X, self.Y = np.meshgrid(self.x_grid, self.y_grid)

        # 速度场 (u, v)
        self.u = np.zeros((grid_size, grid_size))
        self.v = np.zeros((grid_size, grid_size))
        # 压力场
        self.p = np.zeros((grid_size, grid_size))
        # 涡量场
        self.vorticity = np.zeros((grid_size, grid_size))

        # 粒子系统
        self.particles: List[FlowParticle] = []
        self.max_particles = 5000

        # 历史存储（最近1000帧）
        self.history: deque = deque(maxlen=1000)

        # 异常列表
        self.anomalies: List[Anomaly] = []

        # 注入事件审计日志
        self.inject_log: deque = deque(maxlen=500)

        # 运行状态
        self.running = True
        self.last_update = time.time()
        self.dt = 0.1
        self.frame_count = 0

        # 阈值配置（可调）
        self.vortex_threshold = 0.5
        self.pressure_threshold = 8.0
        self.turbulence_threshold = 1.0

        # 初始化粒子
        self._init_particles(200)

    def _init_particles(self, n: int):
        """初始化随机粒子"""
        for _ in range(n):
            x = np.random.uniform(-self.domain_size / 2, self.domain_size / 2)
            y = np.random.uniform(-self.domain_size / 2, self.domain_size / 2)
            vx = np.random.uniform(-0.5, 0.5)
            vy = np.random.uniform(-0.5, 0.5)
            self.particles.append(FlowParticle(x=x, y=y, vx=vx, vy=vy))

    # ========== 外部注入 ==========

    def inject(self, data: Dict) -> Dict:
        """
        注入外部数据，影响流场。

        data 格式:
        {
            "type": "force" | "source" | "vortex",
            "x": float,        # 注入位置 x
            "y": float,        # 注入位置 y
            "strength": float, # 强度
            "radius": float,   # 影响半径（可选）
            "fx": float,       # x方向力分量（force类型）
            "fy": float,       # y方向力分量（force类型）
        }
        """
        typ = data.get("type", "force")
        x = data.get("x", 0.0)
        y = data.get("y", 0.0)
        strength = data.get("strength", 1.0)
        radius = data.get("radius", self.domain_size / 10)

        if typ == "force":
            fx = data.get("fx", strength * 0.1)
            fy = data.get("fy", strength * 0.1)
            dist = np.sqrt((self.X - x) ** 2 + (self.Y - y) ** 2)
            mask = dist < radius
            decay = np.exp(-dist[mask] / radius)
            self.u[mask] += fx * decay
            self.v[mask] += fy * decay

        elif typ == "source":
            for p in self.particles:
                dx, dy = p.x - x, p.y - y
                dist = np.sqrt(dx ** 2 + dy ** 2)
                if 0.01 < dist < radius:
                    p.vx += strength * dx / dist * 0.5
                    p.vy += strength * dy / dist * 0.5

        elif typ == "vortex":
            for p in self.particles:
                dx, dy = p.x - x, p.y - y
                dist = np.sqrt(dx ** 2 + dy ** 2)
                if 0.01 < dist < radius:
                    # 切向速度
                    p.vx += -strength * dy / dist * 0.5
                    p.vy += strength * dx / dist * 0.5

        else:
            return {"status": "error", "message": f"未知注入类型: {typ}"}

        # 审计日志
        self.inject_log.append({
            "timestamp": datetime.datetime.now().isoformat(),
            "type": typ,
            "x": x,
            "y": y,
            "strength": strength,
            "radius": radius
        })

        return {"status": "injected", "type": typ, "strength": strength, "location": [x, y]}

    # ========== 流场计算 ==========

    def update(self, dt: float = 0.1):
        """更新流场状态（每一步）"""
        self.dt = dt
        self.last_update = time.time()
        self.frame_count += 1

        # 1. 粒子运动（一阶欧拉）
        half = self.domain_size / 2
        for p in self.particles:
            p.x += p.vx * dt
            p.y += p.vy * dt
            # 边界反弹（阻尼）
            if abs(p.x) > half:
                p.vx *= -0.9
                p.x = np.clip(p.x, -half, half)
            if abs(p.y) > half:
                p.vy *= -0.9
                p.y = np.clip(p.y, -half, half)

        # 2. 速度场插值（粒子→网格）
        if len(self.particles) >= 3:
            pos = np.array([[p.x, p.y] for p in self.particles])
            vel = np.array([[p.vx, p.vy] for p in self.particles])
            grid = np.array([[x, y] for x in self.x_grid for y in self.y_grid])
            try:
                u_vals = griddata(pos, vel[:, 0], grid, method='linear', fill_value=0.0)
                v_vals = griddata(pos, vel[:, 1], grid, method='linear', fill_value=0.0)
                self.u = u_vals.reshape(self.grid_size, self.grid_size)
                self.v = v_vals.reshape(self.grid_size, self.grid_size)
            except Exception:
                pass

        # 3. 涡量场 ω = ∂v/∂x - ∂u/∂y
        du_dy = np.gradient(self.u, self.dy, axis=0)
        dv_dx = np.gradient(self.v, self.dx, axis=1)
        self.vorticity = dv_dx - du_dy

        # 4. 压力场（伯努利近似: p = p0 - 0.5ρv²）
        speed = np.sqrt(self.u ** 2 + self.v ** 2)
        self.p = np.clip(1.0 - 0.5 * speed ** 2, 0, None)
        if np.max(self.p) > 0:
            self.p = self.p / np.max(self.p) * 10.0

        # 5. 异常检测
        self._detect_anomalies()

        # 6. 粒子数量控制
        if len(self.particles) > self.max_particles:
            self.particles = self.particles[-self.max_particles:]

        # 7. 历史快照（每2帧一次，省内存）
        if self.frame_count % 2 == 0:
            self.history.append(self._snapshot())

    def _detect_anomalies(self):
        """异常检测：涡旋、压力、湍流"""
        self.anomalies.clear()

        # 涡旋异常：涡量超过阈值
        max_vort = float(np.max(np.abs(self.vorticity)))
        if max_vort > self.vortex_threshold:
            idx = int(np.argmax(np.abs(self.vorticity)))
            iy, ix = divmod(idx, self.grid_size)
            self.anomalies.append(Anomaly(
                type="vortex",
                severity=min(1.0, max_vort / 2.0),
                location=(float(self.x_grid[ix]), float(self.y_grid[iy])),
                radius=0.5,
                description=f"涡旋异常: 涡量 {max_vort:.3f}",
                timestamp=datetime.datetime.now().isoformat()
            ))

        # 压力过高
        max_p = float(np.max(self.p))
        if max_p > self.pressure_threshold:
            idx = int(np.argmax(self.p))
            iy, ix = divmod(idx, self.grid_size)
            self.anomalies.append(Anomaly(
                type="pressure",
                severity=min(1.0, (max_p - self.pressure_threshold) / 5.0),
                location=(float(self.x_grid[ix]), float(self.y_grid[iy])),
                radius=0.5,
                description=f"压力过高: p={max_p:.2f}",
                timestamp=datetime.datetime.now().isoformat()
            ))

        # 湍流：速度散度超过阈值
        div = np.gradient(self.u, self.dx, axis=1) + np.gradient(self.v, self.dy, axis=0)
        max_div = float(np.max(np.abs(div)))
        if max_div > self.turbulence_threshold:
            idx = int(np.argmax(np.abs(div)))
            iy, ix = divmod(idx, self.grid_size)
            self.anomalies.append(Anomaly(
                type="turbulence",
                severity=min(1.0, max_div / 3.0),
                location=(float(self.x_grid[ix]), float(self.y_grid[iy])),
                radius=1.0,
                description=f"湍流异常: div={max_div:.3f}",
                timestamp=datetime.datetime.now().isoformat()
            ))

    def _snapshot(self) -> Dict:
        """生成当前状态快照"""
        return {
            "timestamp": datetime.datetime.now().isoformat(),
            "frame": self.frame_count,
            "particles": [
                {"x": p.x, "y": p.y, "vx": p.vx, "vy": p.vy}
                for p in self.particles[:100]
            ],
            "vorticity": self.vorticity.tolist(),
            "pressure": self.p.tolist(),
            "anomalies": [asdict(a) for a in self.anomalies],
            "stats": {
                "particle_count": len(self.particles),
                "max_vorticity": float(np.max(np.abs(self.vorticity))),
                "max_pressure": float(np.max(self.p)),
                "anomaly_count": len(self.anomalies),
                "frame": self.frame_count,
                "dt": self.dt
            }
        }

    # ========== 查询接口 ==========

    def get_state(self) -> Dict:
        """获取当前完整状态"""
        return self._snapshot()

    def get_history(self, limit: int = 100, from_time: str = None) -> List[Dict]:
        """获取历史快照"""
        if from_time:
            filtered = [s for s in self.history if s["timestamp"] >= from_time]
            return filtered[-limit:]
        return list(self.history)[-limit:]

    def replay(self) -> List[Dict]:
        """回放全部历史"""
        return list(self.history)

    def get_inject_log(self, limit: int = 100) -> List[Dict]:
        """获取注入审计日志"""
        return list(self.inject_log)[-limit:]


# ============================================================
# WebSocket 广播器
# ============================================================

class AnomalyBroadcaster:
    """管理 WebSocket 连接，广播异常"""

    def __init__(self):
        self.connections: List[WebSocket] = []
        self.last_anomaly_sig = ""  # 去重

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.connections:
            self.connections.remove(websocket)

    async def broadcast(self, message: Dict):
        """广播消息"""
        dead = []
        for ws in self.connections:
            try:
                await ws.send_text(json.dumps(message, ensure_ascii=False))
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(ws)

    def count(self) -> int:
        return len(self.connections)


# ============================================================
# FastAPI 应用
# ============================================================

app = FastAPI(
    title="🐉 龍魂 · 流场映射层 API",
    description="物理-信息流场同构映射：被动观测速度场、涡旋检测、压力计算、热力图、异常预警",
    version="2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局实例
engine = FlowEngine()
broadcaster = AnomalyBroadcaster()


# ========== 后台更新循环 ==========

async def flow_update_loop():
    """后台持续更新流场并广播异常"""
    while True:
        if engine.running:
            engine.update(0.1)
            if engine.anomalies:
                anomaly_data = [asdict(a) for a in engine.anomalies]
                sig = hashlib.md5(json.dumps(anomaly_data, sort_keys=True).encode()).hexdigest()
                if sig != broadcaster.last_anomaly_sig:
                    await broadcaster.broadcast({
                        "type": "anomaly",
                        "data": anomaly_data,
                        "timestamp": datetime.datetime.now().isoformat()
                    })
                    broadcaster.last_anomaly_sig = sig
        await asyncio.sleep(0.3)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(flow_update_loop())


# ============================================================
# REST API 端点
# ============================================================

@app.get("/health")
async def health():
    """健康检查"""
    return {
        "status": "ok",
        "engine": "flow-field-mapping-v2.0",
        "particles": len(engine.particles),
        "frame": engine.frame_count,
        "ws_connections": broadcaster.count(),
        "uptime_seconds": time.time() - engine.last_update if engine.frame_count > 0 else 0
    }


@app.post("/inject")
async def inject_data(request: Request):
    """注入数据到流场

    POST body: {"type":"force|source|vortex","x":0,"y":0,"strength":1.0,"radius":1.0}
    """
    try:
        data = await request.json()
        result = engine.inject(data)
        return JSONResponse(result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/state")
async def get_state():
    """获取当前流场完整状态"""
    return JSONResponse(engine.get_state())


@app.get("/history")
async def get_history(limit: int = 100, from_time: str = None):
    """获取历史快照"""
    history = engine.get_history(limit, from_time)
    return JSONResponse({"history": history, "count": len(history)})


@app.get("/replay")
async def replay_history(speed: float = 1.0):
    """回放全部历史"""
    history = engine.replay()
    return JSONResponse({"replay": history, "count": len(history)})


@app.get("/anomalies")
async def get_anomalies():
    """获取当前异常列表"""
    return JSONResponse({
        "anomalies": [asdict(a) for a in engine.anomalies],
        "count": len(engine.anomalies)
    })


@app.get("/inject-log")
async def get_inject_log(limit: int = 100):
    """获取注入审计日志"""
    return JSONResponse({
        "log": engine.get_inject_log(limit),
        "count": len(engine.inject_log)
    })


@app.post("/reset")
async def reset_engine():
    """重置流场"""
    global engine
    engine = FlowEngine()
    return {"status": "reset", "particles": len(engine.particles)}


# ============================================================
# WebSocket 端点
# ============================================================

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket 实时推送"""
    await broadcaster.connect(websocket)
    try:
        # 发送初始状态
        state = engine.get_state()
        await websocket.send_text(json.dumps({
            "type": "init",
            "data": state,
            "timestamp": datetime.datetime.now().isoformat()
        }, ensure_ascii=False))

        # 监听客户端消息
        while True:
            raw = await websocket.receive_text()
            try:
                msg = json.loads(raw)
                action = msg.get("action", "")
                if action == "ping":
                    await websocket.send_text(json.dumps({
                        "type": "pong",
                        "timestamp": datetime.datetime.now().isoformat()
                    }))
                elif action == "inject":
                    result = engine.inject(msg.get("data", {}))
                    await websocket.send_text(json.dumps({
                        "type": "inject_result",
                        "data": result
                    }, ensure_ascii=False))
                elif action == "get_state":
                    state = engine.get_state()
                    await websocket.send_text(json.dumps({
                        "type": "state",
                        "data": state
                    }, ensure_ascii=False))
            except json.JSONDecodeError:
                pass
    except WebSocketDisconnect:
        broadcaster.disconnect(websocket)


# ============================================================
# 控制台 HTML 页面
# ============================================================

CONSOLE_HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🐉 流场映射层 · 控制台</title>
<style>
:root {
    --bg: #0d1117; --card: #161b22; --border: #30363d;
    --text: #c9d1d9; --text-dim: #8b949e; --accent: #f0c040;
    --blue: #1f6feb; --blue-hover: #388bfd;
    --red: #f05454; --yellow: #d29922; --green: #2ea043;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, "SF Pro Text", "PingFang SC", sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; }
.header { background: var(--card); border-bottom: 1px solid var(--border); padding: 16px 24px; display: flex; align-items: center; gap: 16px; }
.header h1 { font-size: 1.3em; color: var(--accent); }
.header .subtitle { font-size: 0.85em; color: var(--text-dim); }
.container { max-width: 1400px; margin: 0 auto; padding: 20px; }
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px; margin-bottom: 16px; }
.card { background: var(--card); border-radius: 12px; padding: 20px; border: 1px solid var(--border); }
.card h3 { font-size: 1em; margin-bottom: 12px; color: var(--text); display: flex; align-items: center; gap: 8px; }
.stat-row { display: flex; justify-content: space-between; padding: 4px 0; font-size: 0.9em; }
.stat-row .label { color: var(--text-dim); }
.stat-row .value { font-weight: 600; font-variant-numeric: tabular-nums; }
.stat-row .value.green { color: var(--green); }
.stat-row .value.red { color: var(--red); }
.stat-row .value.yellow { color: var(--yellow); }
.ws-indicator { display: inline-flex; align-items: center; gap: 6px; font-size: 0.85em; }
.ws-dot { width: 8px; height: 8px; border-radius: 50%; }
.ws-dot.on { background: var(--green); box-shadow: 0 0 6px var(--green); }
.ws-dot.off { background: var(--red); }
.btn { padding: 8px 18px; border: none; border-radius: 6px; cursor: pointer; font-size: 0.85em; font-weight: 500; transition: background 0.2s; }
.btn-primary { background: var(--blue); color: #fff; }
.btn-primary:hover { background: var(--blue-hover); }
.btn-danger { background: var(--red); color: #fff; }
.btn-sm { padding: 4px 12px; font-size: 0.8em; }
.input-group { display: flex; gap: 8px; margin: 8px 0; flex-wrap: wrap; align-items: center; }
.input-group input, .input-group select { padding: 7px 10px; background: var(--bg); border: 1px solid var(--border); border-radius: 6px; color: var(--text); font-size: 0.85em; }
.input-group input { width: 100px; }
.input-group select { width: 110px; }
.result-msg { padding: 8px 12px; border-radius: 6px; font-size: 0.85em; margin-top: 8px; }
.result-msg.success { background: rgba(46,160,67,0.15); color: var(--green); }
.result-msg.error { background: rgba(240,84,84,0.15); color: var(--red); }
.log-panel { background: var(--bg); border-radius: 8px; padding: 12px; max-height: 260px; overflow-y: auto; font-size: 0.8em; font-family: "SF Mono", Menlo, monospace; white-space: pre-wrap; color: var(--text-dim); }
.anomaly-item { padding: 6px 10px; border-radius: 6px; margin: 4px 0; font-size: 0.85em; }
.anomaly-item.vortex { background: rgba(240,84,84,0.1); border-left: 3px solid var(--red); }
.anomaly-item.pressure { background: rgba(210,153,34,0.1); border-left: 3px solid var(--yellow); }
.anomaly-item.turbulence { background: rgba(31,111,235,0.1); border-left: 3px solid var(--blue); }
.anomaly-badge { display: inline-block; padding: 1px 8px; border-radius: 10px; font-size: 0.75em; font-weight: 600; }
.anomaly-badge.vortex { background: var(--red); color: #fff; }
.anomaly-badge.pressure { background: var(--yellow); color: #000; }
.anomaly-badge.turbulence { background: var(--blue); color: #fff; }
.footer-bar { text-align: center; padding: 16px; color: var(--text-dim); font-size: 0.75em; border-top: 1px solid var(--border); margin-top: 20px; }
.flow-legend { font-size: 0.8em; color: var(--text-dim); padding: 8px 0; }
.flow-legend span { margin-right: 12px; }
.mapping-table { width: 100%; font-size: 0.8em; border-collapse: collapse; margin-top: 8px; }
.mapping-table th { text-align: left; padding: 4px 8px; border-bottom: 1px solid var(--border); color: var(--accent); font-weight: 500; }
.mapping-table td { padding: 4px 8px; border-bottom: 1px solid rgba(48,54,61,0.5); }
</style>
</head>
<body>

<div class="header">
    <h1>🐉 流场映射层</h1>
    <span class="subtitle">被动观测 · 涡旋检测 · 压力梯度 · 攻击溯源</span>
    <div style="flex:1"></div>
    <div class="ws-indicator">
        <span class="ws-dot off" id="wsDot"></span>
        <span id="wsLabel">未连接</span>
    </div>
</div>

<div class="container">

<!-- 状态卡片 -->
<div class="grid">
    <div class="card">
        <h3>📊 流场状态 <button class="btn btn-primary btn-sm" onclick="fetchState()" style="margin-left:auto">刷新</button></h3>
        <div id="stateStats">
            <div class="stat-row"><span class="label">粒子数</span><span class="value">—</span></div>
            <div class="stat-row"><span class="label">最大涡量</span><span class="value">—</span></div>
            <div class="stat-row"><span class="label">最大压力</span><span class="value">—</span></div>
            <div class="stat-row"><span class="label">异常数</span><span class="value green">0</span></div>
            <div class="stat-row"><span class="label">帧数</span><span class="value">—</span></div>
            <div class="stat-row"><span class="label">WS连接</span><span class="value">—</span></div>
        </div>
    </div>

    <div class="card">
        <h3>🚨 异常预警</h3>
        <div id="anomalyPanel" style="min-height:80px;color:var(--text-dim)">✅ 暂无异常</div>
    </div>
</div>

<!-- 注入 & 控制 -->
<div class="grid">
    <div class="card">
        <h3>💉 数据注入</h3>
        <div class="input-group">
            <select id="injType">
                <option value="force">力 (force)</option>
                <option value="source">源 (source)</option>
                <option value="vortex">涡旋 (vortex)</option>
            </select>
            <input id="injX" type="number" placeholder="X" value="0" step="0.1">
            <input id="injY" type="number" placeholder="Y" value="0" step="0.1">
            <input id="injS" type="number" placeholder="强度" value="2.0" step="0.1" style="width:80px">
            <button class="btn btn-primary" onclick="doInject()">注入</button>
        </div>
        <div id="injectResult"></div>
    </div>

    <div class="card">
        <h3>🎛️ 控制</h3>
        <div style="display:flex;gap:8px;flex-wrap:wrap">
            <button class="btn btn-primary" id="btnConnect" onclick="connectWS()">连接 WS</button>
            <button class="btn btn-danger" id="btnDisconnect" onclick="disconnectWS()">断开 WS</button>
            <button class="btn btn-sm" onclick="fetchHistory()" style="background:#30363d;color:var(--text)">历史</button>
            <button class="btn btn-sm" onclick="resetEngine()" style="background:#30363d;color:var(--text)">重置</button>
        </div>
        <div id="controlResult" style="margin-top:8px;font-size:0.85em;color:var(--text-dim)"></div>
    </div>
</div>

<!-- 物理-信息映射表 -->
<div class="card" style="margin-bottom:16px">
    <h3>🧬 物理-信息映射（焊死） <span style="font-size:0.75em;color:var(--accent);margin-left:8px">流场≠雷达·被动观测</span></h3>
    <table class="mapping-table">
        <tr><th>物理量</th><th>符号</th><th>信息对应</th><th>作用</th></tr>
        <tr><td>粒子</td><td>质点</td><td>数据点/请求</td><td>基本载体</td></tr>
        <tr><td>速度场</td><td>v</td><td>变化率/吞吐量</td><td>流动快慢与方向</td></tr>
        <tr><td>流线</td><td>dx/ds</td><td>数据路径/管道</td><td>穿越路径</td></tr>
        <tr><td>涡旋</td><td>ω=∇×v</td><td>回环/反馈回路</td><td>自我循环</td></tr>
        <tr><td>压力</td><td>p</td><td>负载/积压</td><td>堆积压力</td></tr>
        <tr><td>热力图</td><td>标量φ</td><td>密度/频率分布</td><td>热点识别</td></tr>
        <tr><td>层流/湍流</td><td>Re</td><td>有序/混沌</td><td>可控性</td></tr>
        <tr><td>势流</td><td>v=∇φ</td><td>结构化路由</td><td>预定策略</td></tr>
        <tr><td>不可压缩</td><td>∇·v=0</td><td>保吞吐</td><td>流量守恒</td></tr>
    </table>
</div>

<!-- 日志 -->
<div class="card">
    <h3>📋 事件日志 <button class="btn btn-sm" onclick="document.getElementById('logPanel').textContent=''" style="margin-left:8px;background:#30363d;color:var(--text)">清空</button></h3>
    <div id="logPanel" class="log-panel">🟢 控制台已启动 · 等待事件...</div>
</div>

</div>

<div class="footer-bar">
    DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·☴巽-FLOW-MAP-v2.0-UID9622 |
    GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F |
    流场≠雷达 · 被动观测 · 不发射不主动探测
</div>

<script>
let ws = null;
let reconnectTimer = null;
const logEl = document.getElementById('logPanel');

function log(msg) {
    const t = new Date().toLocaleTimeString();
    const line = `[${t}] ${msg}`;
    logEl.textContent = line + '\\n' + logEl.textContent;
    if (logEl.textContent.length > 5000) logEl.textContent = logEl.textContent.slice(0, 5000);
}

function updateWSStatus(connected) {
    const dot = document.getElementById('wsDot');
    const label = document.getElementById('wsLabel');
    if (connected) {
        dot.className = 'ws-dot on';
        label.textContent = 'WS 已连接';
        document.getElementById('btnConnect').style.opacity = '0.5';
        document.getElementById('btnDisconnect').style.opacity = '1';
    } else {
        dot.className = 'ws-dot off';
        label.textContent = 'WS 未连接';
        document.getElementById('btnConnect').style.opacity = '1';
        document.getElementById('btnDisconnect').style.opacity = '0.5';
    }
}

function connectWS() {
    if (ws && ws.readyState === WebSocket.OPEN) return;
    const proto = location.protocol === 'https:' ? 'wss:' : 'ws:';
    const url = proto + '//' + location.host + '/ws';
    ws = new WebSocket(url);

    ws.onopen = () => {
        updateWSStatus(true);
        log('WebSocket 已连接');
    };

    ws.onmessage = (e) => {
        try {
            const msg = JSON.parse(e.data);
            if (msg.type === 'init') {
                updateStateDisplay(msg.data);
                log('收到初始状态 · 粒子: ' + (msg.data.stats?.particle_count || '?'));
            } else if (msg.type === 'anomaly') {
                const descs = msg.data.map(a => a.description).join(', ');
                log('⚠️ 异常广播: ' + descs);
                updateAnomalies(msg.data);
            } else if (msg.type === 'state') {
                updateStateDisplay(msg.data);
            } else if (msg.type === 'pong') {
                log('🏓 Pong');
            } else if (msg.type === 'inject_result') {
                const r = msg.data;
                document.getElementById('injectResult').innerHTML =
                    '<div class="result-msg success">✅ 注入成功: ' + r.type + ' (' + r.strength + ')</div>';
                log('注入完成: ' + r.type + ' 强度=' + r.strength);
            }
        } catch(err) {
            log('收到消息: ' + e.data.slice(0, 100));
        }
    };

    ws.onclose = () => {
        updateWSStatus(false);
        log('WebSocket 已断开');
        if (!reconnectTimer) {
            reconnectTimer = setInterval(() => {
                if (!ws || ws.readyState === WebSocket.CLOSED) {
                    log('尝试重连...');
                    connectWS();
                }
            }, 5000);
        }
    };

    ws.onerror = () => log('WebSocket 连接错误');
}

function disconnectWS() {
    if (ws) { ws.close(); ws = null; }
    if (reconnectTimer) { clearInterval(reconnectTimer); reconnectTimer = null; }
    updateWSStatus(false);
    log('WebSocket 已手动断开');
}

function updateStateDisplay(state) {
    if (!state || !state.stats) return;
    const s = state.stats;
    document.getElementById('stateStats').innerHTML = `
        <div class="stat-row"><span class="label">粒子数</span><span class="value">${s.particle_count}</span></div>
        <div class="stat-row"><span class="label">最大涡量</span><span class="value ${s.max_vorticity > 0.5 ? 'red' : ''}">${s.max_vorticity.toFixed(3)}</span></div>
        <div class="stat-row"><span class="label">最大压力</span><span class="value ${s.max_pressure > 8 ? 'yellow' : ''}">${s.max_pressure.toFixed(2)}</span></div>
        <div class="stat-row"><span class="label">异常数</span><span class="value ${s.anomaly_count > 0 ? 'red' : 'green'}">${s.anomaly_count}</span></div>
        <div class="stat-row"><span class="label">帧数</span><span class="value">${s.frame || '—'}</span></div>
        <div class="stat-row"><span class="label">WS连接</span><span class="value">—</span></div>
    `;
    if (state.anomalies) updateAnomalies(state.anomalies);
}

function updateAnomalies(anomalies) {
    const panel = document.getElementById('anomalyPanel');
    if (!anomalies || anomalies.length === 0) {
        panel.innerHTML = '<div style="color:var(--green)">✅ 暂无异常</div>';
        return;
    }
    panel.innerHTML = anomalies.map(a => `
        <div class="anomaly-item ${a.type}">
            <span class="anomaly-badge ${a.type}">${a.type}</span>
            严重度: ${(a.severity * 100).toFixed(0)}% |
            ${a.description} |
            位置: (${a.location[0].toFixed(1)}, ${a.location[1].toFixed(1)})
        </div>
    `).join('');
}

async function fetchState() {
    try {
        const r = await fetch('/state');
        const d = await r.json();
        updateStateDisplay(d);
        log('状态已刷新');
    } catch(e) {
        log('获取状态失败: ' + e.message);
    }
}

async function doInject() {
    const type = document.getElementById('injType').value;
    const x = parseFloat(document.getElementById('injX').value) || 0;
    const y = parseFloat(document.getElementById('injY').value) || 0;
    const strength = parseFloat(document.getElementById('injS').value) || 1.0;
    const data = { type, x, y, strength };

    try {
        const r = await fetch('/inject', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const d = await r.json();
        document.getElementById('injectResult').innerHTML =
            '<div class="result-msg success">✅ 注入成功: ' + d.type + ' 强度=' + d.strength + '</div>';
        log('注入: ' + type + ' @(' + x + ',' + y + ') 强度=' + strength);
        // 同时通过WS发（双重保障）
        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({ action: 'inject', data }));
        }
    } catch(e) {
        document.getElementById('injectResult').innerHTML =
            '<div class="result-msg error">❌ 注入失败: ' + e.message + '</div>';
    }
}

async function fetchHistory() {
    try {
        const r = await fetch('/history?limit=20');
        const d = await r.json();
        document.getElementById('controlResult').textContent =
            '历史快照: ' + d.count + ' 帧可用';
        log('历史查询: ' + d.count + ' 帧');
    } catch(e) {
        log('获取历史失败: ' + e.message);
    }
}

async function resetEngine() {
    try {
        const r = await fetch('/reset', { method: 'POST' });
        const d = await r.json();
        document.getElementById('controlResult').textContent =
            '✅ 流场已重置 · 粒子: ' + d.particles;
        log('流场已重置');
        fetchState();
    } catch(e) {
        log('重置失败: ' + e.message);
    }
}

// 自动连接
connectWS();
// 定时刷新
setInterval(fetchState, 5000);
</script>
</body>
</html>"""


@app.get("/", response_class=HTMLResponse)
async def console():
    """流场控制台页面"""
    return HTMLResponse(CONSOLE_HTML)


# ============================================================
# 部署工具
# ============================================================

def deploy_static(dry_run: bool = False, target: str = "/var/www/longhun/flow/") -> Dict:
    """部署控制台HTML到目标目录"""
    dst = Path(target)
    if dry_run:
        return {"status": "dry_run", "would_deploy_to": str(dst), "files": ["console.html"]}

    dst.mkdir(parents=True, exist_ok=True)
    out = dst / "flow-console.html"
    out.write_text(CONSOLE_HTML)
    return {"status": "deployed", "target": str(out), "size": len(CONSOLE_HTML)}


# ============================================================
# 命令行入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂 · 流场映射层引擎 v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 bin/lh_flow_engine.py                    启动服务 (端口8776)
  python3 bin/lh_flow_engine.py --port 8888        指定端口
  python3 bin/lh_flow_engine.py --deploy           部署控制台HTML
  python3 bin/lh_flow_engine.py --no-ws            禁用WebSocket
        """
    )
    parser.add_argument("--host", default="127.0.0.1", help="监听地址 (默认: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8776, help="监听端口 (默认: 8776)")
    parser.add_argument("--deploy", action="store_true", help="部署控制台HTML页面")
    parser.add_argument("--deploy-target", default="/var/www/longhun/flow/", help="部署目标目录")
    parser.add_argument("--dry-run", action="store_true", help="预览部署（不实际写入）")
    parser.add_argument("--no-ws", action="store_true", help="禁用 WebSocket")
    args = parser.parse_args()

    if args.deploy or args.dry_run:
        result = deploy_static(dry_run=args.dry_run, target=args.deploy_target)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    banner = f"""
🐉 龍魂 · 流场映射层引擎 v2.0
{'='*50}
  地址:    http://{args.host}:{args.port}
  控制台:  http://{args.host}:{args.port}/
  API:     /state /inject /history /replay /anomalies /inject-log
  WS:      /ws {'✅ 启用' if not args.no_ws else '❌ 禁用'}
{'='*50}
  DNA:     #龍芯⚡️{DNA_CORE}
  CONFIRM: {CONFIRM}
  GPG:     {GPG[:32]}...
{'='*50}
  流场≠雷达 · 被动观测 · 不发射不主动探测
"""
    print(banner)

    uvicorn.run(app, host=args.host, port=args.port, log_level="info")


if __name__ == "__main__":
    main()
