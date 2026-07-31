#!/usr/bin/env python3
# 龍魂宝宝守护助手 · FastAPI 后端
# DNA:#龍芯⚡️2026-06-04-BAOBAO-BACKEND-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

import asyncio
import json
import logging
from typing import Any, Dict, Set, Tuple
from datetime import datetime

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect  # pyright: ignore[reportAttributeAccessIssue]
from fastapi.middleware.cors import CORSMiddleware  # pyright: ignore[reportMissingImports]
from fastapi.responses import Response
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

    async def broadcast(self, message: Dict[str, Any]):
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

    async def send_personal(self, websocket: WebSocket, message: Dict[str, Any]):
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

# 配置 CORS（🛡️ P77修复：白名单替代通配符·allow_credentials 不可与 * 同时使用）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8766", "http://127.0.0.1:8766"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-DNA-TRACE", "X-CNSH-CONFIRM"],
)

# 🛡️ P77 安全加固：注入CSP+安全头部
@app.middleware("http")
async def 安全头部中间件(request: Request, call_next):
    response = await call_next(request)
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: blob:; "
        "connect-src 'self' ws://localhost:* wss://localhost:* http://localhost:*; "
        "frame-ancestors 'none'"
    )
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response

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
# 人格中枢桥接 API（宝宝 ↔ 人格中枢联动）
# ═══════════════════════════════════════════════════════════

from .persona_bridge import get_bridge

@app.post("/api/persona/route")
async def persona_route(task: str):
    """智能路由任务到正确人格"""
    bridge = get_bridge()
    result = bridge.route(task)
    logger.info(f"🧠 人格路由: {task} → {result.get('primary', {}).get('名称', 'unknown')}")
    return result

@app.get("/api/persona/list")
async def persona_list():
    """列出所有可用人格"""
    bridge = get_bridge()
    return {"personas": bridge.list_personas(), "timestamp": datetime.now().isoformat()}

@app.post("/api/baby/ask")
async def baby_ask(query: str):
    """宝宝入口：自然语言查询 → IPA路由分发"""
    bridge = get_bridge()
    result = bridge.get_baby_response(query)

    # IPA路由建议
    ipa_suggestion = _ipa执行器.路由建议(query)

    primary_name = result.get("primary", {}).get("名称", "宝宝")
    primary_code = result.get("primary", {}).get("代码", "P17")

    # 匹配的具体技能
    匹配技能列表 = ipa_suggestion.get("推荐分发", {}).get("匹配技能", [])
    技能提示 = ""
    if isinstance(匹配技能列表, list) and 匹配技能列表:
        技能名列表 = [s.get("技能", "") for s in 匹配技能列表]
        技能提示 = f"·可执行: {', '.join(技能名列表)}"

    await manager.broadcast({
        "type": "baobao",
        "payload": {
            "message": f"宝宝收到！已委托 {primary_name}({primary_code}) 处理「{query[:20]}」{技能提示}",
            "emotion": "happy",
            "duration": 3000,
            "data": {
                "routing": result,
                "ipa_suggestion": ipa_suggestion,
            },
        },
    })
    return {
        "success": True,
        "routing": result,
        "ipa_suggestion": ipa_suggestion,
        "tip": "宝宝(P17)是入口·具体计算由指派人格执行·各司其职",
        "timestamp": datetime.now().isoformat(),
    }

@app.get("/api/persona/info")
async def persona_info():
    """人格中枢系统信息"""
    bridge = get_bridge()
    return bridge.system_info()

# ═══════════════════════════════════════════════════════════
# 🐉 架构技能 API（v2.0 — 数字根·五行·河图洛书·DNA）
# ⚡ v3.1: 所有技能通过 IPA 执行器分发到对应人格·宝宝不再一个人扛
# ═══════════════════════════════════════════════════════════

from .baobao_skills import 宝宝技能引擎, 八卦映射
from .ipa_executor import get_ipa_executor, 技能人格归属表

_技能引擎 = 宝宝技能引擎()
_ipa执行器 = get_ipa_executor(_技能引擎)


def _get_owner_info(技能名: str) -> Tuple[str, str, str]:
    """获取技能的归属人格信息 (owner_id, owner_name, ipa_node)"""
    归属 = 技能人格归属表.get(技能名, {})
    return (归属.get("owner", "P17"), 归属.get("owner_name", "宝宝"), 归属.get("ipa_node", ""))


@app.get("/api/skills/digital-root")
async def digital_root(query: str):
    """数字根+五行查询（P02·张衡 数学引擎）"""
    result = _ipa执行器.执行("数字根查询", 输入=query)
    owner_id, owner_name, _ = _get_owner_info("数字根查询")
    dr = result.get("数字根", "?")
    wx = result.get("五行", "?")
    await manager.broadcast({
        "type": "baobao",
        "payload": {
            "message": f"「{query[:20]}」数字根 {dr}·{wx} | {owner_name}({owner_id})计算",
            "emotion": "happy" if result.get("数字根") in [3, 6, 9] else "thinking",
            "duration": 4000,
            "data": result,
        },
    })
    return result


@app.get("/api/skills/hetu-luoshu")
async def hetu_luoshu():
    """河图洛书展示（P02·张衡 数学引擎）"""
    result = _ipa执行器.执行("河图洛书展示")
    owner_id, owner_name, _ = _get_owner_info("河图洛书展示")
    await manager.broadcast({
        "type": "baobao",
        "payload": {
            "message": f"河图洛书·中五不动点=5·369三才内核 | {owner_name}({owner_id})执行",
            "emotion": "thinking",
            "duration": 5000,
            "data": result,
        },
    })
    return result


@app.get("/api/skills/dna-generate")
async def dna_generate(action: str, user: str = "UID9622"):
    """生成DNA追溯码（P02·张衡 数学引擎）"""
    result = _ipa执行器.执行("DNA生成", 操作=action, 用户=user)
    owner_id, owner_name, _ = _get_owner_info("DNA生成")
    await manager.broadcast({
        "type": "baobao",
        "payload": {
            "message": f"DNA已生成：{result.get('DNA码', '')} | {owner_name}({owner_id})签署",
            "emotion": "happy",
            "duration": 4000,
            "data": result,
        },
    })
    return result


@app.get("/api/skills/wuxing")
async def wuxing_query(element: str = ""):
    """五行关系查询（P02·张衡 数学引擎）"""
    owner_id, owner_name, _ = _get_owner_info("五行关系查询")
    if element:
        result = _ipa执行器.执行("五行关系查询", 属性=element)
        msg = f"{element}·生{result.get('相生', {}).get('我生', '?')}·克{result.get('相克', {}).get('我克', '?')} | {owner_name}({owner_id})"
    else:
        result = {"可用属性": ["金", "木", "水", "火", "土"], "提示": "请指定 /api/skills/wuxing?element=火"}
        msg = "金木水火土·你想查哪个？"
    await manager.broadcast({
        "type": "baobao",
        "payload": {"message": msg, "emotion": "thinking", "duration": 4000, "data": result},
    })
    return result


@app.get("/api/skills/audit")
async def audit_colors():
    """三色/五色审计查询（P05·执行外设 元控制）"""
    result = _ipa执行器.执行("三色审计查询")
    owner_id, owner_name, _ = _get_owner_info("三色审计查询")
    await manager.broadcast({
        "type": "baobao",
        "payload": {
            "message": f"🟢通行·🟡警告·🔴熔断·🟣影子·⚫VOID | {owner_name}({owner_id})审计",
            "emotion": "warning",
            "duration": 4000,
            "data": result,
        },
    })
    return result


@app.get("/api/skills/bagua")
async def bagua_query(name: str = ""):
    """八卦查询（P17·宝宝 入口·轻量级查询）"""
    result = _ipa执行器.执行("八卦查询", 卦名=name)
    owner_id, owner_name, _ = _get_owner_info("八卦查询")
    await manager.broadcast({
        "type": "baobao",
        "payload": {
            "message": f"八卦相重为六十四卦·{'☰☷☳☴☵☲☶☱' if not name else 八卦映射.get(name, {}).get('符号', '?')} | {owner_name}({owner_id})",
            "emotion": "thinking",
            "duration": 4000,
            "data": result,
        },
    })
    return result


@app.get("/api/skills/diagnose")
async def diagnose(query: str):
    """综合诊断（P05·执行外设 元控制）"""
    result = _ipa执行器.执行("综合诊断", 输入=query)
    owner_id, owner_name, _ = _get_owner_info("综合诊断")
    await manager.broadcast({
        "type": "baobao",
        "payload": {
            "message": f"{result.get('宝宝台词', '')} | {owner_name}({owner_id})诊断",
            "emotion": result.get("宝宝反应", "thinking"),
            "duration": 5000,
            "data": result,
        },
    })
    return result


# ═══════════════════════════════════════════════════════════
# 🖥️ 计算机引擎 API（v3.1 — IPA人格分发·各司其职）
# ═══════════════════════════════════════════════════════════

@app.get("/api/skills/sancai")
async def sancai_decision(天: float = 0.5, 地: float = 0.5, 人: float = 0.8):
    """三才决策评分（P01·诸葛亮 战略推理）"""
    result = _ipa执行器.执行("三才决策", 天=天, 地=地, 人=人)
    owner_id, owner_name, _ = _get_owner_info("三才决策")
    score = result.get("综合得分", 0)
    emoji = "🟢" if score >= 0.7 else "🟡" if score >= 0.4 else "🔴"
    await manager.broadcast({
        "type": "baobao",
        "payload": {
            "message": f"三才得分 {score} {emoji}·{result.get('建议', '')} | {owner_name}({owner_id})推演",
            "emotion": "happy" if score >= 0.7 else "warning",
            "duration": 5000,
            "data": result,
        },
    })
    return result


@app.get("/api/skills/yijing-decide")
async def yijing_decide(content: str, motivation: str = "为祖国·为人民"):
    """易经64卦推演决策（P01·诸葛亮 战略推理）"""
    result = _ipa执行器.执行("易经推演决策", 决策内容=content, 动机=motivation)
    owner_id, owner_name, _ = _get_owner_info("易经推演决策")
    risk = result.get("风险数字", 50)
    await manager.broadcast({
        "type": "baobao",
        "payload": {
            "message": f"卦:{result.get('卦象名称', '?')}·{result.get('最终判定', '')}·风险{result.get('风险等级', '')} | {owner_name}({owner_id})起卦",
            "emotion": "happy" if risk < 35 else "thinking" if risk < 65 else "warning",
            "duration": 6000,
            "data": result,
        },
    })
    return result


@app.get("/api/skills/braket-persona")
async def braket_persona(scenario: str):
    """BraKet人格叠加态分析（P13·姜子牙 人格编排）"""
    result = _ipa执行器.执行("BraKet人格分析", 场景需求=scenario)
    owner_id, owner_name, _ = _get_owner_info("BraKet人格分析")
    main = result.get("主力人格", {}).get("名称", "?")
    await manager.broadcast({
        "type": "baobao",
        "payload": {
            "message": f"⟨{result.get('匹配场景', '')}⟩ → 主力{main}·坍缩完成 | {owner_name}({owner_id})编排",
            "emotion": "thinking",
            "duration": 5000,
            "data": result,
        },
    })
    return result


@app.get("/api/skills/cnsh-64")
async def cnsh64_state(query: str = ""):
    """CNSH-64 状态空间探索（P02·张衡 数学引擎）"""
    result = _ipa执行器.执行("CNSH64状态空间", 当前状态=query)
    owner_id, owner_name, _ = _get_owner_info("CNSH64状态空间")
    await manager.broadcast({
        "type": "baobao",
        "payload": {
            "message": f"8卦×8态=64状态空间·数学保证有限可控 | {owner_name}({owner_id})",
            "emotion": "thinking",
            "duration": 5000,
            "data": result,
        },
    })
    return result


@app.get("/api/skills/lu-translate")
async def lu_translate(cmd: str):
    """Lu指令翻译器（P17·宝宝 入口·轻量级）"""
    result = _ipa执行器.执行("Lu指令翻译", 中文指令=cmd)
    owner_id, owner_name, _ = _get_owner_info("Lu指令翻译")
    await manager.broadcast({
        "type": "baobao",
        "payload": {
            "message": f"Lu:{result.get('Lu指令', '')}·{result.get('数字根预检', '')[:2]} | {owner_name}({owner_id})",
            "emotion": "thinking",
            "duration": 4000,
            "data": result,
        },
    })
    return result


@app.get("/api/skills/bazi-wuxing")
async def bazi_wuxing(年干: str = "甲", 年支: str = "子",
                      月干: str = "丙", 月支: str = "寅",
                      日干: str = "戊", 日支: str = "午",
                      时干: str = "庚", 时支: str = "申"):
    """四柱五行强度计算（P02·张衡 数学引擎）"""
    result = _ipa执行器.执行("四柱五行强度",
                           年柱天干=年干, 年柱地支=年支,
                           月柱天干=月干, 月柱地支=月支,
                           日柱天干=日干, 日柱地支=日支,
                           时柱天干=时干, 时柱地支=时支)
    owner_id, owner_name, _ = _get_owner_info("四柱五行强度")
    await manager.broadcast({
        "type": "baobao",
        "payload": {
            "message": f"四柱·最强{result.get('最强', '?')}·均衡{result.get('均衡指数', '?')}·{result.get('健康状态', '')} | {owner_name}({owner_id})",
            "emotion": "happy" if result.get("均衡指数", 0) >= 0.8 else "thinking",
            "duration": 5000,
            "data": result,
        },
    })
    return result


@app.get("/api/skills/formulas")
async def formulas_index(num: int = 0):
    """9大公式速查索引（P02·张衡 数学引擎）"""
    result = _ipa执行器.执行("公式速查", 公式编号=num)
    owner_id, owner_name, _ = _get_owner_info("公式速查")
    if num > 0:
        msg = f"公式{num}·{result.get('详情', {}).get('名称', '')} | {owner_name}({owner_id})"
    else:
        msg = f"龍魂9大核心公式·可追溯到L1内核层 | {owner_name}({owner_id})"
    await manager.broadcast({
        "type": "baobao",
        "payload": {
            "message": msg,
            "emotion": "thinking",
            "duration": 5000,
            "data": result,
        },
    })
    return result


@app.get("/api/skills/compute-diagnose")
async def compute_diagnose(query: str):
    """计算机五维综合诊断（P06·镜像审计者 对抗模拟）"""
    result = _ipa执行器.执行("计算机诊断", 输入=query)
    owner_id, owner_name, _ = _get_owner_info("计算机诊断")
    await manager.broadcast({
        "type": "baobao",
        "payload": {
            "message": f"{result.get('总评价', '')} | {owner_name}({owner_id})审计",
            "emotion": result.get("宝宝反应", "thinking"),
            "duration": 7000,
            "data": result,
        },
    })
    return result


# ═══════════════════════════════════════════════════════════
# 🧭 IPA 路由管理 API（v3.1 — 人格分发·冲突检测·归属总览）
# ═══════════════════════════════════════════════════════════

@app.get("/api/ipa/routing-suggestion")
async def ipa_routing_suggestion(query: str):
    """IPA路由建议：根据输入推荐分发人格"""
    result = _ipa执行器.路由建议(query)
    await manager.broadcast({
        "type": "baobao",
        "payload": {
            "message": f"「{query[:30]}」→ 推荐 {result.get('推荐分发', {}).get('主人格', {}).get('名称', '宝宝')}",
            "emotion": "thinking",
            "duration": 4000,
            "data": result,
        },
    })
    return result


@app.get("/api/ipa/skill-ownership")
async def ipa_skill_ownership():
    """技能归属总览：每个技能归属到哪个人格"""
    result = _ipa执行器.归属总览()
    return result


@app.get("/api/ipa/conflict-check")
async def ipa_conflict_check():
    """冲突检测：技能归属是否与人格矩阵冲突"""
    result = _ipa执行器.冲突检测()
    await manager.broadcast({
        "type": "baobao",
        "payload": {
            "message": f"IPA冲突检测·{result['状态']}",
            "emotion": "warning" if result.get("冲突数", 0) > 0 else "happy",
            "duration": 4000,
            "data": result,
        },
    })
    return result


@app.post("/api/ipa/orchestrate")
async def ipa_orchestrate(task: str, steps: str):
    """
    P13 姜子牙编排多步任务执行

    Args:
        task: 任务描述
        steps: JSON数组 [(技能名, 参数字典), ...]
    """
    try:
        技能序列 = json.loads(steps)
        result = _ipa执行器.编排执行(task, 技能序列)
        await manager.broadcast({
            "type": "baobao",
            "payload": {
                "message": f"P13编排完成·{task}·成功{result.get('成功数', 0)}/失败{result.get('失败数', 0)}",
                "emotion": "happy" if result.get("失败数", 0) == 0 else "warning",
                "duration": 6000,
                "data": result,
            },
        })
        return result
    except json.JSONDecodeError as e:
        return {"success": False, "error": f"steps JSON解析失败: {e}", "格式": '[(技能名, 参数字典), ...]'}


# ═══════════════════════════════════════════════════════════
# 🐉 IPA 统一路由 API（v4.0 — 家族体系·名称归一·自动冲突检测）
# ═══════════════════════════════════════════════════════════

from .ipa_unified_router import (
    get_unified_router, 名称归一 as _名称归一,
    检测所有冲突 as _检测所有冲突,
    家族总览 as _家族总览,
)

_统一路由 = get_unified_router()


@app.get("/api/ipa/unified/name-resolve")
async def ipa_unified_name_resolve(name: str):
    """名称归一：任意别名→规范名称"""
    result = _统一路由.名称归一(name)
    await manager.broadcast({
        "type": "baobao",
        "payload": {
            "message": f"『{name}』→ {result.get('规范名称', '未知')}({result.get('规范码', '?')})·{result.get('家族层级', '')}",
            "emotion": "happy" if result.get("精确匹配") else "thinking",
            "duration": 3000,
            "data": result,
        },
    })
    return result


@app.get("/api/ipa/unified/family-overview")
async def ipa_unified_family():
    """家族体系总览"""
    result = _统一路由.家族层级总览()
    return result


@app.get("/api/ipa/unified/family-group")
async def ipa_unified_family_group(code: str):
    """家族归属查询：某个人格在家族体系中的位置"""
    result = _统一路由.家族归属(code)
    return result


@app.get("/api/ipa/unified/full-conflicts")
async def ipa_unified_full_conflicts():
    """全量冲突检测：名称不一致·家族组归属·别名多义·技能归属"""
    result = _统一路由.检测冲突()
    await manager.broadcast({
        "type": "baobao",
        "payload": {
            "message": f"统一冲突检测·{result['状态']}·冲突{len(result.get('冲突', []))}·警告{len(result.get('警告', []))}",
            "emotion": "warning" if result.get("冲突") else "happy",
            "duration": 5000,
            "data": result,
        },
    })
    return result


@app.get("/api/ipa/unified/stats")
async def ipa_unified_stats():
    """统一路由器统计"""
    result = _统一路由.统计()
    return result


@app.post("/api/ipa/unified/merge")
async def ipa_unified_merge(data: Dict[str, Any]):
    """
    人格合并：新增或覆盖人格到规范表+自动冲突检测

    Body:
      {
        "personas": [["P99", {"规范名称": "测试人格", "家族层级": "L1+·人格层", ...}], ...],
        "strategy": "覆盖"
      }
    """
    personas = data.get("personas", [])
    strategy = data.get("strategy", "覆盖")
    if not personas:
        return {"success": False, "error": "缺少 personas 字段", "格式": "[['P99', {条目}], ...]"}

    bridge = get_bridge()
    result = bridge.合并并检测(personas, strategy)
    await manager.broadcast({
        "type": "baobao",
        "payload": {
            "message": f"合并完成·策略={strategy}·冲突={result.get('冲突检测', {}).get('状态', '?')}",
            "emotion": "happy",
            "duration": 4000,
            "data": result,
        },
    })
    return result


# ═══════════════════════════════════════════════════════════
# 启动
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info",
    )
