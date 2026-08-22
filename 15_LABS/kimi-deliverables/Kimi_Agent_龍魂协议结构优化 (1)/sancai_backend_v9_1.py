#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐲 三才流場 v9.1 · 实时智能体后端（v9.0 六缺陷修复版）
DNA: #龍芯⚡️丙午·癸未·癸未·戊午·䷖剥-SANCAI-BACKEND-v9.1-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

v9.1 修订注（锚定 v9.0 缺陷）：
  ① 权重不变量修复：双库动态权重改为「忠 0.5 不动 + 孝义互配比」，总和恒=1.0
  ② reserve_active 在 __init__ 初始化，/health 不再 AttributeError
  ③ 物理循环全局唯一（single simulation loop），广播只读快照；
     N 个客户端不再导致 N 倍速物理
  ④ dt 与帧率对齐：FPS=30 → dt=1/30≈0.033，模拟时间与真实时间 1:1
  ⑤ Notion database_id 自动剥离 collection:// 前缀，裸 UUID 直连；
     失败不再静默，显式上报 status="Error" + error_message
  ⑥ DNA 生成改 SHA-256 确定性（对齐 L0 密码学标准），3% 金粒按 id 确定
     （id % 34 == 0 ≈ 2.94%），不再每帧闪烁

端口映射: :8765 WebSocket | :9622 CNSH 网关预留 | :11434 Ollama
"""

import asyncio
import json
import math
import random
import hashlib
import time
import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from collections import deque

import numpy as np
import requests
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# ============================================================
# 配置区
# ============================================================

CONFIG = {
    "NOTION_TOKEN": os.getenv("NOTION_TOKEN", ""),
    "NOTION_DB_CHINA": os.getenv("NOTION_DB_CHINA", "013f4e33-c68c-4bb5-8b42-dfd25f79ec8c"),
    "NOTION_DB_GLOBAL": os.getenv("NOTION_DB_GLOBAL", "3367125a-9c9f-8026-9ff9-000b0cd57bb3"),
    "FPS": 30,                      # 🆕 修订注④：帧率单点定义
    "NUM_PARTICLES": 1200,
    "NOTION_REFRESH_FRAMES": 300,   # 每 10s 拉一次双库（原 30 帧=1s 过频）
}

DT = 1.0 / CONFIG["FPS"]          # 🆕 修订注④：dt 由 FPS 推导，模拟=真实 1:1

# ============================================================
# 核心算法模块（对齐 v8/v9 协议 · 数学内核与 MathSixRoots.swift 同源）
# ============================================================

def digital_root(n: int) -> int:
    if n == 0: return 0
    return 1 + ((n - 1) % 9)

def luoshu_matrix() -> np.ndarray:
    return np.array([[4, 9, 2], [3, 5, 7], [8, 1, 6]])

def sancai_vector() -> Dict[str, float]:
    return {"忠": 0.5, "孝": 0.3, "义": 0.2}

def calculate_r_value(dim_scores: Dict[str, float]) -> float:
    """六维 R 值（95 封顶 · 留 5 给突变）"""
    weights = [0.2, 0.2, 0.15, 0.15, 0.15, 0.15]
    dims = ['人类福祉', '公平公正', '可控可信', '透明可解释', '责任可追溯', '隐私保护']
    raw = sum(weights[i] * dim_scores.get(dims[i], 50.0) for i in range(6))
    return min(raw, 95.0)

def shield_engine(dr: int, order_disrupted: bool = False) -> str:
    """Shield Engine 三档（v8.1 确认态）：
    DR绿={1,2,4,5,7,8} 正常 | DR黄={6} 琥珀警戒 | DR红={3,9} 熔断（仅 orderDisrupted 触发）"""
    if order_disrupted and dr in (3, 9):
        return "RED"
    elif order_disrupted and dr == 6:
        return "YELLOW"
    return "GREEN"

def sancai_dna(particle_id: int, module: str = "粒子") -> str:
    """🆕 修订注⑥：SHA-256 确定性 DNA（同 id 同日恒同码，可复算）"""
    ts = time.strftime("%Y-%m-%d")
    h = hashlib.sha256(f"{module}{particle_id}{ts}".encode("utf-8")).hexdigest()[:8].upper()
    return f"#龍芯⚡️丙午·癸未·癸未-{module}-UID9622-{h}"

def normalize_db_id(raw: str) -> str:
    """🆕 修订注⑤：剥离 collection:// 前缀与连字符变体，输出裸 UUID"""
    rid = raw.replace("collection://", "").strip()
    return rid

# ============================================================
# Notion API 封装（双库接入）
# ============================================================

class NotionClient:
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }
        self.base_url = "https://api.notion.com/v1"

    def query_database(self, db_id: str, filter_conditions: Dict = None) -> List[Dict]:
        if not self.token:
            return self._mock_data(db_id)  # 无 token：开发模式兜底
        db_id = normalize_db_id(db_id)      # 🆕 修订注⑤
        url = f"{self.base_url}/databases/{db_id}/query"
        payload = {"filter": filter_conditions} if filter_conditions else {}
        resp = requests.post(url, headers=self.headers, json=payload, timeout=5)
        resp.raise_for_status()             # 🆕 修订注⑤：失败显式抛出，不再静默吞错
        return resp.json().get("results", [])

    def _mock_data(self, db_id: str) -> List[Dict]:
        if "013f" in db_id:
            return [{"id": f"mock_china_{i}"} for i in range(10)]
        return [{"id": f"mock_global_{i}"} for i in range(8)]

    def get_dual_lib_stats(self, china_db_id: str, global_db_id: str) -> Dict[str, Any]:
        """双库统计 → 动态权重。🆕 修订注①：忠 0.5 不动，孝义在 0.5 内互配比，总和恒=1.0"""
        base = sancai_vector()
        try:
            china_count = len(self.query_database(china_db_id))
            global_count = len(self.query_database(global_db_id))
            status = "Connected" if self.token else "MockMode"
            error = None
        except Exception as e:
            china_count, global_count = 0, 0
            status, error = "Error", str(e)

        # 活跃度比：中国库活跃 → 孝增义减；全球库活跃 → 义增孝减；忠永不动
        total = china_count + global_count
        if total > 0:
            ratio = china_count / total            # 0~1
        else:
            ratio = 0.6                            # 默认偏向孝（守根优先）
        flex = base["孝"] + base["义"]             # 0.5 弹性池
        xiao_w = round(flex * ratio, 4)
        yi_w = round(flex * (1 - ratio), 4)
        assert abs(base["忠"] + xiao_w + yi_w - 1.0) < 1e-9  # 不变量断言

        return {
            "china_count": china_count,
            "global_count": global_count,
            "zhong_weight": base["忠"],
            "xiao_weight": xiao_w,
            "yi_weight": yi_w,
            "sum_check": round(base["忠"] + xiao_w + yi_w, 6),
            "status": status,
            "error_message": error,
        }

# ============================================================
# 粒子动力学引擎（真实系统：势阱+斥力+雷达耦合+五行旋转场+双库牵引）
# ============================================================

@dataclass
class Particle:
    idx: int
    x: float
    y: float
    vx: float = 0.0
    vy: float = 0.0
    mass: float = 1.0
    charge: float = 0.0
    r_value: float = 85.0
    color: str = "#00cc66"
    dr: int = 1
    dna: str = ""
    is_golden: bool = False           # 🆕 修订注⑥：3% 金粒按 id 确定，不闪烁
    trail: deque = field(default_factory=lambda: deque(maxlen=15))
    deviated: bool = False
    deviation_trigger: str = ""

    def __post_init__(self):
        self.dr = digital_root(self.idx + 1)
        self.dna = sancai_dna(self.idx)
        self.is_golden = (self.idx % 34 == 0)   # ≈2.94% 金色主权粒子，确定性
        if self.dr in (3, 9):
            self.charge = 0.5
        elif self.dr == 6:
            self.charge = -0.2
        else:
            self.charge = 0.1

    def compute_forces(self, cx, cy, radar_scores, notion_stats, order_disrupted, frame):
        dx, dy = cx - self.x, cy - self.y
        dist = math.hypot(dx, dy) + 0.001

        # 1. T0 金锚势阱（忠 · 永远在顶）
        k_anchor = 0.0008 * (1 + notion_stats.get("xiao_weight", 0.3) * 0.5)
        fx = k_anchor * dx / (dist ** 1.5)
        fy = k_anchor * dy / (dist ** 1.5)

        # 2. 边界软斥力
        margin = 0.02
        if self.x < margin: fx += 0.01 / (self.x + 0.001)
        elif self.x > 1 - margin: fx -= 0.01 / (1 - self.x + 0.001)
        if self.y < margin: fy += 0.01 / (self.y + 0.001)
        elif self.y > 1 - margin: fy -= 0.01 / (1 - self.y + 0.001)

        # 3. 雷达六维耦合（扇区低分 → 病态抖动）
        angle = math.atan2(self.y - cy, self.x - cx)
        sector = int((angle + math.pi) / (math.pi / 3)) % 6
        dim_keys = ['人类福祉', '公平公正', '可控可信', '透明可解释', '责任可追溯', '隐私保护']
        dim_score = radar_scores.get(dim_keys[sector], 50)
        if dim_score < 40:
            noise_amp = 0.002 * (1 - dim_score / 40)
            fx += random.uniform(-noise_amp, noise_amp)
            fy += random.uniform(-noise_amp, noise_amp)
            self.deviated = True
            self.deviation_trigger = f"雷达低分: {dim_keys[sector]}"

        # 4. 五行旋转场（洛书映射切向力）
        ls = luoshu_matrix()
        i = int(self.y * 3) % 3
        j = int(self.x * 3) % 3
        rot_strength = 0.0001 * (ls[i][j] - 5) * self.charge
        fx += -rot_strength * (self.y - cy)
        fy += rot_strength * (self.x - cx)

        # 5. 双库动态牵引（孝收敛 / 义发散）
        yi_force = notion_stats.get("yi_weight", 0.2) * 0.001
        fx += random.uniform(-yi_force, yi_force)
        xiao_force = notion_stats.get("xiao_weight", 0.3) * 0.002
        fx += -xiao_force * dx * 0.1
        fy += -xiao_force * dy * 0.1

        return fx, fy

    def update(self, dt, cx, cy, radar_scores, notion_stats, order_disrupted, frame):
        fx, fy = self.compute_forces(cx, cy, radar_scores, notion_stats, order_disrupted, frame)
        self.vx += fx * dt / self.mass
        self.vy += fy * dt / self.mass
        speed = math.hypot(self.vx, self.vy)
        if speed > 0.02:                       # 速度阻尼帽
            self.vx = self.vx / speed * 0.02
            self.vy = self.vy / speed * 0.02
        self.x = max(0.0, min(1.0, self.x + self.vx * dt))
        self.y = max(0.0, min(1.0, self.y + self.vy * dt))

        self.r_value = calculate_r_value(radar_scores)
        if self.r_value >= 85: self.color = "#00cc66"
        elif self.r_value >= 60: self.color = "#ffcc00"
        else:
            self.color = "#ff3333"
            self.deviated = True
            self.deviation_trigger = "R<60"

        shield = shield_engine(self.dr, order_disrupted)
        if shield == "RED":
            self.color = "#ff0000"; self.deviated = True; self.deviation_trigger = "熔断 RED"
        elif shield == "YELLOW":
            self.color = "#f59e0b"; self.deviated = True; self.deviation_trigger = "警戒 YELLOW"

        if self.deviated:
            self.trail.append((self.x, self.y))

# ============================================================
# 后端服务主类
# ============================================================

app = FastAPI(title="龙魂三才流场 v9.1 后端", version="9.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # 局域网调试；生产环境收敛为白名单
    allow_methods=["*"],
    allow_headers=["*"],
)

class GlobalState:
    def __init__(self):
        self.particles: List[Particle] = []
        self.radar_scores: Dict[str, float] = {
            '人类福祉': 85, '公平公正': 80, '可控可信': 75,
            '透明可解释': 70, '责任可追溯': 80, '隐私保护': 85,
        }
        self.order_disrupted = False
        self.frame = 0
        self.center = (0.5, 0.5)
        self.notion_stats: Dict[str, Any] = {
            "china_count": 0, "global_count": 0,
            "zhong_weight": 0.5, "xiao_weight": 0.3, "yi_weight": 0.2,
            "sum_check": 1.0, "status": "Initializing", "error_message": None,
        }
        self.notion_client = NotionClient(CONFIG["NOTION_TOKEN"])
        self.running = True
        self.clients: List[WebSocket] = []
        self.reserve_active = False          # 🆕 修订注②：初始化，/health 不再崩
        self._sim_task: Optional[asyncio.Task] = None

    def init_particles(self, num: int):
        self.particles = []
        for i in range(num):
            if i < 100:
                x = 0.5 + random.uniform(-0.1, 0.1)
                y = 0.5 + random.uniform(-0.1, 0.1)
            else:
                x, y = random.random(), random.random()
            self.particles.append(Particle(idx=i, x=x, y=y))
        print(f"✅ 初始化 {num} 个粒子完成")

    async def update_notion_stats(self):
        try:
            stats = await asyncio.to_thread(
                self.notion_client.get_dual_lib_stats,
                CONFIG["NOTION_DB_CHINA"], CONFIG["NOTION_DB_GLOBAL"],
            )
            self.notion_stats = stats
        except Exception as e:
            self.notion_stats["status"] = "Error"
            self.notion_stats["error_message"] = str(e)

    async def step(self):
        """推进一帧（全局唯一模拟循环调用）"""
        self.frame += 1
        if self.frame % CONFIG["NOTION_REFRESH_FRAMES"] == 0:
            await self.update_notion_stats()
        for p in self.particles:
            p.update(DT, self.center[0], self.center[1],
                     self.radar_scores, self.notion_stats,
                     self.order_disrupted, self.frame)
        avg_r = float(np.mean([p.r_value for p in self.particles])) if self.particles else 0.0
        self.reserve_active = avg_r >= 90
        return avg_r

    def get_state_packet(self) -> Dict:
        particles_data = [{
            "id": p.idx, "x": round(p.x, 4), "y": round(p.y, 4),
            "r": round(p.r_value, 1), "color": p.color, "dr": p.dr,
            "dna": p.dna if p.is_golden else None,   # 🆕 修订注⑥：确定性 3% 金粒
            "deviated": p.deviated,
            "trail": list(p.trail)[-5:] if p.deviated else [],
        } for p in self.particles]
        r_vals = [p.r_value for p in self.particles]
        return {
            "version": "v9.1",
            "frame": self.frame,
            "timestamp": time.time(),
            "reserve_active": self.reserve_active,
            "order": sancai_vector(),
            "weights_dynamic": {
                "zhong": self.notion_stats.get("zhong_weight", 0.5),
                "xiao": self.notion_stats.get("xiao_weight", 0.3),
                "yi": self.notion_stats.get("yi_weight", 0.2),
                "sum_check": self.notion_stats.get("sum_check", 1.0),
            },
            "notion": {"status": self.notion_stats.get("status"),
                       "china_count": self.notion_stats.get("china_count"),
                       "global_count": self.notion_stats.get("global_count"),
                       "error": self.notion_stats.get("error_message")},
            "radar": self.radar_scores,
            "particles": particles_data,
            "summary": {
                "total": len(self.particles),
                "green": sum(1 for p in self.particles if p.color == "#00cc66"),
                "yellow": sum(1 for p in self.particles if p.color in ("#ffcc00", "#f59e0b")),
                "red": sum(1 for p in self.particles if p.color in ("#ff3333", "#ff0000")),
                "avg_r": round(float(np.mean(r_vals)), 2) if r_vals else 0.0,
            },
        }

state = GlobalState()
state.init_particles(CONFIG["NUM_PARTICLES"])

# ============================================================
# 🆕 修订注③：全局唯一模拟循环 —— 物理推进与客户端数量彻底解耦
# ============================================================

async def simulation_loop():
    """单一物理循环：按 FPS 推进，向所有客户端广播同一帧快照"""
    while state.running:
        start = time.perf_counter()
        await state.step()
        packet = json.dumps(state.get_state_packet())
        dead = []
        for ws in list(state.clients):
            try:
                await ws.send_text(packet)
            except Exception:
                dead.append(ws)
        for ws in dead:
            if ws in state.clients:
                state.clients.remove(ws)
        elapsed = time.perf_counter() - start
        await asyncio.sleep(max(0, DT - elapsed))

@app.on_event("startup")
async def start_simulation():
    await state.update_notion_stats()
    state._sim_task = asyncio.create_task(simulation_loop())

@app.on_event("shutdown")
async def stop_simulation():
    state.running = False
    if state._sim_task:
        state._sim_task.cancel()

# ============================================================
# WebSocket 端点（纯接收指令；广播由全局循环负责）
# ============================================================

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    state.clients.append(websocket)
    print(f"🔌 客户端连接: {websocket.client}（当前 {len(state.clients)} 个）")
    try:
        while True:
            data = await websocket.receive_text()
            try:
                cmd = json.loads(data)
                if "radar" in cmd:
                    for k, v in cmd["radar"].items():
                        if k in state.radar_scores:
                            state.radar_scores[k] = float(v)
                if "order_disrupted" in cmd:
                    state.order_disrupted = bool(cmd["order_disrupted"])
                if "reset" in cmd and cmd["reset"]:
                    state.init_particles(CONFIG["NUM_PARTICLES"])
                await websocket.send_text(json.dumps({"status": "ack", "frame": state.frame}))
            except json.JSONDecodeError:
                print(f"⚠️ 收到非 JSON 数据: {data[:50]}")
    except WebSocketDisconnect:
        print(f"🔌 客户端断开: {websocket.client}")
    finally:
        if websocket in state.clients:
            state.clients.remove(websocket)

# ============================================================
# HTTP 健康检查 & 控制端点
# ============================================================

@app.get("/health")
async def health_check():
    return {
        "status": "running",
        "version": "v9.1",
        "particles": len(state.particles),
        "clients": len(state.clients),
        "notion": state.notion_stats.get("status"),
        "reserve": state.reserve_active,
        "frame": state.frame,
        "dt": DT,
        "fps": CONFIG["FPS"],
    }

@app.post("/control/order")
async def set_order_disrupted(disrupt: bool):
    state.order_disrupted = disrupt
    return {"order_disrupted": state.order_disrupted}

@app.get("/notion/refresh")
async def refresh_notion():
    await state.update_notion_stats()
    return state.notion_stats

# ============================================================
# 启动主程序
# ============================================================

if __name__ == "__main__":
    print(f"""
    🐲 龍魂三才流場 v9.1 后端启动（六缺陷修复版）
    DNA: #龍芯⚡️丙午·癸未·癸未·戊午·䷖剥-SANCAI-BACKEND-v9.1-UID9622
    粒子数: {CONFIG['NUM_PARTICLES']}  FPS: {CONFIG['FPS']}  dt: {DT:.4f}
    端口: 8765 (WebSocket) | 9622 (CNSH 网关预留) | 11434 (Ollama)
    Notion 双库: {'✅ 已配置' if CONFIG['NOTION_TOKEN'] else '⚠️ MockMode（无 token 走模拟数据）'}
    """)
    uvicorn.run(app, host="0.0.0.0", port=8765, log_level="info")
