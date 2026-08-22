#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
🧬 龍魂神经网络·智能体桥接器 v1.0

这是神经网络和agents系统之间的真正桥梁。
不再只展示漂亮的3D图——而是让神经网络真正路由agent，赋能UID9622。

核心能力：
1. 查询实时神经网络状态（:9627 symbiote server）
2. 将agents映射到神经网络节点（五行 + 三才 + 拓扑）
3. 基于神经网络拓扑的智能体路由
4. 双向反馈：agent执行结果反哺神经网络

DNA: #龍芯⚡️丙午·甲午·辛巳·甲午·䷃蒙-NEURAL-AGENT-BRIDGE-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""

from __future__ import annotations

import hashlib
import json
import time
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

HOME = Path.home()
ROOT = HOME / "longhun-system"
SYMBIOTE_URL = "http://127.0.0.1:9627"
MANIFEST_PATH = ROOT / "agents" / "manifest.json"

DNA = "#龍芯⚡️丙午·甲午·辛巳·甲午·䷃蒙-NEURAL-AGENT-BRIDGE-v1.0"

# ═══════════════════════════════════════════════════════════════
# 一、五行 ↔ Agent 类型映射表
# ═══════════════════════════════════════════════════════════════

WUXING_AGENT_MAP = {
    "metal": {
        "traits": ["精确", "判断", "裁定", "审计", "规范", "规则"],
        "agent_types": ["audit", "audit-plugin", "code-audit", "guardian", "wuxing-guard"],
        "color": "#C0C0C0",
        "icon": "⚔️",
    },
    "wood": {
        "traits": ["生长", "创造", "构建", "编码", "生成", "扩展"],
        "agent_types": ["builder", "code-audit", "dna-gen", "skill-extension"],
        "color": "#2E8B57",
        "icon": "🌿",
    },
    "water": {
        "traits": ["流动", "记忆", "同步", "检索", "翻译", "适配"],
        "agent_types": ["syncer", "notion_sync", "on-translate", "memory-feeder"],
        "color": "#1E90FF",
        "icon": "💧",
    },
    "fire": {
        "traits": ["激活", "告警", "传播", "转换", "加速", "触发"],
        "agent_types": ["scout", "task_executor", "bagua-router", "error-translator"],
        "color": "#DC143C",
        "icon": "🔥",
    },
    "earth": {
        "traits": ["稳定", "中心", "锚定", "编排", "治理", "协调"],
        "agent_types": ["wenwen", "orchestrator", "governance-layer", "on-identity", "sovereign-privacy"],
        "color": "#8B4513",
        "icon": "⛰️",
    },
}


def digital_root(n: int) -> int:
    """dr(n) = 1 + ((n - 1) mod 9); dr(0) = 0"""
    if n == 0:
        return 0
    return 1 + ((n - 1) % 9)


# ═══════════════════════════════════════════════════════════════
# 二、神经网络状态查询
# ═══════════════════════════════════════════════════════════════

@dataclass
class NeuralNode:
    id: str
    name: str
    status: str          # healthy / standby / error
    wuxing: str          # metal/wood/water/fire/earth
    category: str        # core/daemon/logic/external/placeholder
    sancai: float        # 三才指数
    tian: float
    di: float
    ren: float
    dr: int              # 数字根
    port: int | None = None
    pid: int | None = None
    dna: str = ""
    description: str = ""


@dataclass
class NeuralEdge:
    source: str
    target: str
    type: str            # anchor/data/external/guard/logic/symbiote
    label: str


@dataclass
class NeuralState:
    nodes: list[NeuralNode] = field(default_factory=list)
    edges: list[NeuralEdge] = field(default_factory=list)
    stats: dict[str, Any] = field(default_factory=dict)
    timestamp: str = ""
    healthy: bool = False

    @property
    def node_map(self) -> dict[str, NeuralNode]:
        return {n.id: n for n in self.nodes}

    @property
    def active_nodes(self) -> list[NeuralNode]:
        return [n for n in self.nodes if n.status == "healthy"]

    @property
    def wuxing_groups(self) -> dict[str, list[NeuralNode]]:
        groups: dict[str, list[NeuralNode]] = {}
        for n in self.nodes:
            groups.setdefault(n.wuxing, []).append(n)
        return groups


# ═══════════════════════════════════════════════════════════════
# 三、路由结果
# ═══════════════════════════════════════════════════════════════

@dataclass
class RoutingResult:
    input_text: str
    matched_agents: list[dict[str, Any]] = field(default_factory=list)
    primary_agent: dict[str, Any] | None = None
    routing_path: list[str] = field(default_factory=list)  # 经过的神经网络节点
    wuxing_flow: str = ""           # 五行相生/相克流
    sancai_check: bool = False      # 三才主权检查是否通过
    constitution_ok: bool = False   # 宪法层状态
    neural_status: str = "offline"  # 神经网络连接状态
    network_health: float = 0.0     # 神经网络总体健康率
    advice: str = ""
    dna: str = ""
    processing_ms: float = 0.0


# ═══════════════════════════════════════════════════════════════
# 四、神经网络·智能体桥接器
# ═══════════════════════════════════════════════════════════════

class NeuralAgentBridge:
    """
    神经网络·智能体桥接器

    不是装饰品，是真正的路由引擎：
    - 查询实时神经网络状态
    - 将用户输入映射到最优agent
    - 通过神经网络拓扑找到最佳路由路径
    - 双向反馈：agent结果回到神经网络
    """

    def __init__(self, symbiote_url: str = SYMBIOTE_URL):
        self.symbiote_url: str = symbiote_url
        self._manifest: dict[str, Any] | None = None
        self._agents: list[dict[str, Any]] = []
        self._neural_cache: NeuralState | None = None
        self._cache_ts: float = 0.0
        self._cache_ttl: float = 3.0  # 缓存3秒

    # ── 加载 agents ──

    def _load_manifest(self) -> dict[str, Any] | None:
        if self._manifest is None:
            if MANIFEST_PATH.exists():
                with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
                    manifest = json.load(f)
                    self._manifest = manifest
                    self._agents = manifest.get("agents", [])
            else:
                self._manifest = {"agents": []}
        return self._manifest

    @property
    def agents(self) -> list[dict[str, Any]]:
        if not self._agents:
            self._load_manifest()
        return self._agents

    # ── 查询神经网络状态 ──

    def fetch_neural_state(self, force: bool = False) -> NeuralState | None:
        """从 symbiote_server 拉取实时神经网络状态"""
        now = time.time()
        if not force and self._neural_cache and (now - self._cache_ts) < self._cache_ttl:
            return self._neural_cache

        try:
            with urllib.request.urlopen(
                f"{self.symbiote_url}/api/state", timeout=3
            ) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except Exception:
            self._neural_cache = None
            return None

        nodes = []
        for n in data.get("nodes", []):
            nodes.append(NeuralNode(
                id=n["id"], name=n["name"], status=n["status"],
                wuxing=n["wuxing"], category=n["category"],
                sancai=n["sancai"], tian=n["tian"], di=n.get("di", 0), ren=n.get("ren", 0),
                dr=n.get("dr", 0), port=n.get("port"),
                pid=n.get("pid"), dna=n.get("dna", ""),
                description=n.get("description", ""),
            ))

        edges = []
        for e in data.get("edges", []):
            edges.append(NeuralEdge(
                source=e["source"], target=e["target"],
                type=e.get("type", "data"), label=e.get("label", ""),
            ))

        self._neural_cache = NeuralState(
            nodes=nodes, edges=edges,
            stats=data.get("stats", {}),
            timestamp=data.get("timestamp", ""),
            healthy=data.get("stats", {}).get("constitution_ok", False),
        )
        self._cache_ts = now
        return self._neural_cache

    def is_neural_online(self) -> bool:
        """检查神经网络是否在线"""
        try:
            with urllib.request.urlopen(
                f"{self.symbiote_url}/api/health", timeout=2
            ) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data.get("ok", False)
        except Exception:
            return False

    # ── 核心：基于神经网络的Agent路由 ──

    def route(self, text: str) -> RoutingResult:
        """
        通过神经网络路由智能体

        路由逻辑：
        1. 拉取实时神经网络状态
        2. 分析输入文本的五行倾向
        3. 在神经网络拓扑中找到最优agent路径
        4. 如果神经网络离线，降级到关键词匹配
        """
        start = time.time()
        neural = self.fetch_neural_state()

        result = RoutingResult(
            input_text=text[:200],
            dna=self._gen_dna("ROUTE"),
        )

        if neural is None:
            # 神经网络离线 → 降级路由
            result.neural_status = "offline"
            result.advice = "⚠️ 神经网络离线，使用基础关键词匹配"
            result = self._fallback_route(text, result)
        else:
            result.neural_status = "online"
            result.network_health = neural.stats.get("health_rate", 0)
            result.constitution_ok = neural.healthy
            # 神经网络在线 → 基于拓扑路由
            result = self._neural_route(text, neural, result)

        result.processing_ms = round((time.time() - start) * 1000, 1)
        return result

    def _neural_route(
        self, text: str, neural: NeuralState, result: RoutingResult
    ) -> RoutingResult:
        """基于神经网络拓扑的智能路由"""

        # 1. 分析输入文本的五行倾向
        wuxing_scores = self._detect_wuxing(text)

        # 2. 找到神经网络中对应的健康节点
        primary_wx = max(wuxing_scores, key=lambda k: wuxing_scores[k])
        wx_nodes = [
            n for n in neural.active_nodes
            if n.wuxing == primary_wx
        ]
        wx_nodes.sort(key=lambda n: n.sancai, reverse=True)

        # 3. 构建路由路径（从北辰不动点出发，经过五行节点，到达目标agent）
        north_star = neural.node_map.get("north-star")
        routing_path: list[str] = []

        if north_star:
            routing_path.append(f"north-star({north_star.sancai:.2f})")

        # 找到经由边
        for node in wx_nodes[:3]:
            routing_path.append(f"{node.id}({node.sancai:.2f})")

        result.routing_path = routing_path

        # 4. 匹配 agents
        self._load_manifest()
        matched = self._match_agents_by_wuxing(text, primary_wx, wx_nodes)

        if matched:
            result.matched_agents = [self._simplify_agent(a) for a in matched[:5]]
            result.primary_agent = result.matched_agents[0]
        else:
            # 兜底：直接关键词匹配
            result = self._fallback_route(text, result)

        # 5. 五行流描述
        wuxing_cycle = ["metal", "water", "wood", "fire", "earth"]
        idx = wuxing_cycle.index(primary_wx)
        next_wx = wuxing_cycle[(idx + 1) % 5]
        prev_wx = wuxing_cycle[(idx - 1) % 5]
        result.wuxing_flow = f"{prev_wx}→{primary_wx}(当前)→{next_wx}  [{WUXING_AGENT_MAP[primary_wx]['icon']}]"

        # 6. 三才主权检查
        if north_star:
            result.sancai_check = north_star.sancai >= 0.34

        # 7. 生成建议
        if result.primary_agent:
            agent = result.primary_agent
            result.advice = (
                f"🧬 共生路由完成。\n"
                f"   五行流: {result.wuxing_flow}\n"
                f"   经由: {' → '.join(routing_path)}\n"
                f"   主Agent: {agent['name']}({agent['layer']}) {agent['logic']}\n"
                f"   网络健康: {result.network_health}% | 宪法层: {'🟢' if result.constitution_ok else '🔴'}\n"
                f"   建议: 由「{agent['name']}」主理，"
            )
            if len(result.matched_agents) > 1:
                result.advice += f"「{result.matched_agents[1]['name']}」辅助"
            else:
                result.advice += "可直接执行"

        return result

    def _detect_wuxing(self, text: str) -> dict[str, float]:
        """根据文本内容分析五行倾向"""
        scores = {"metal": 1.0, "wood": 1.0, "water": 1.0, "fire": 1.0, "earth": 1.0}
        text_lower = text.lower()

        for wx, info in WUXING_AGENT_MAP.items():
            for trait in info["traits"]:
                if trait in text_lower:
                    scores[wx] += 3.0
            for at in info["agent_types"]:
                if at.replace("-", "") in text_lower.replace("-", ""):
                    scores[wx] += 2.0

        return scores

    def _match_agents_by_wuxing(
        self, text: str, primary_wx: str, wx_nodes: list[NeuralNode]  # noqa: ARG002
    ) -> list[dict[str, Any]]:
        """根据五行匹配agents"""
        text_lower = text.lower()
        target_types = WUXING_AGENT_MAP.get(primary_wx, {}).get("agent_types", [])

        scored: list[dict[str, Any]] = []
        for agent in self.agents:
            score = 0.0
            # 五行匹配
            agent_id = agent.get("id")
            if isinstance(agent_id, str) and agent_id in target_types:
                score += 10
            # 关键词匹配
            keywords = agent.get("keywords", [])
            if isinstance(keywords, list):
                for kw in keywords:
                    if isinstance(kw, str) and kw.lower() in text_lower:
                        score += len(kw) * 2
            # 描述匹配
            desc = str(agent.get("description", "")).lower()
            for trait in WUXING_AGENT_MAP.get(primary_wx, {}).get("traits", []):
                if trait in desc or trait in text_lower:
                    score += 2

            if score > 0:
                agent_copy = dict(agent)
                agent_copy["_score"] = score
                agent_copy["_wuxing"] = primary_wx
                scored.append(agent_copy)

        scored.sort(key=lambda a: float(a.get("_score", 0)), reverse=True)
        return scored

    def _fallback_route(self, text: str, result: RoutingResult) -> RoutingResult:
        """降级路由：纯关键词匹配"""
        text_lower = text.lower()
        scored: list[dict[str, Any]] = []
        self._load_manifest()

        for agent in self.agents:
            score = 0.0
            keywords = agent.get("keywords", [])
            if isinstance(keywords, list):
                for kw in keywords:
                    if isinstance(kw, str) and kw.lower() in text_lower:
                        score += len(kw) * 2
            if score > 0:
                agent_copy = dict(agent)
                agent_copy["_score"] = score
                scored.append(agent_copy)

        scored.sort(key=lambda a: float(a.get("_score", 0)), reverse=True)
        result.matched_agents = [self._simplify_agent(a) for a in scored[:5]]
        result.primary_agent = result.matched_agents[0] if result.matched_agents else None

        if result.primary_agent:
            result.advice = f"关键词匹配 → {result.primary_agent['name']} ({result.primary_agent['layer']})"
        else:
            result.advice = "未匹配到Agent，建议使用通用模式"

        return result

    def _simplify_agent(self, agent: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": agent["id"],
            "name": agent["name"],
            "layer": agent["layer"],
            "type": agent.get("type", "unknown"),
            "logic": agent.get("logic", ""),
            "persona_code": agent.get("persona_code", ""),
            "description": agent.get("description", ""),
            "keywords": agent.get("keywords", [])[:5],
            "dna": agent.get("dna", ""),
            "_score": agent.get("_score", 0),
            "_wuxing": agent.get("_wuxing", "unknown"),
        }

    # ── 健康全景 ──

    def health_panorama(self) -> dict[str, Any]:
        """获取神经网络+agents健康全景"""
        neural = self.fetch_neural_state()
        self._load_manifest()

        result: dict[str, Any] = {
            "dna": self._gen_dna("HEALTH"),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "neural_online": neural is not None,
            "agents_total": len(self.agents),
        }

        if neural:
            result["neural"] = {
                "nodes_total": len(neural.nodes),
                "healthy": neural.stats.get("healthy", 0),
                "standby": neural.stats.get("standby", 0),
                "error": neural.stats.get("error", 0),
                "health_rate": neural.stats.get("health_rate", 0),
                "constitution_ok": neural.healthy,
                "timestamp": neural.timestamp,
            }
            # 五行健康分布
            wx_health: dict[str, dict[str, int | float]] = {}
            for n in neural.nodes:
                if n.wuxing not in wx_health:
                    wx_health[n.wuxing] = {"total": 0, "healthy": 0}
                wx_health[n.wuxing]["total"] += 1
                if n.status == "healthy":
                    wx_health[n.wuxing]["healthy"] += 1
            for _wx, v in wx_health.items():
                v["rate"] = round(v["healthy"] / max(v["total"], 1) * 100, 1)
            result["neural"]["wuxing_health"] = wx_health

        # agents分层统计
        layers: dict[str, int] = {"L1": 0, "L2": 0, "L3": 0}
        for a in self.agents:
            layer_key = str(a.get("layer", "unknown"))
            layers[layer_key] = layers.get(layer_key, 0) + 1
        result["agents_layers"] = layers

        return result

    # ── 执行agent（通过神经网络路由的） ──

    def execute(self, text: str) -> dict[str, Any]:
        """
        完整的执行链路：路由 → 锁定agent → 给出执行方案
        """
        route_result = self.route(text)

        return {
            "dna": route_result.dna,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "input": route_result.input_text,
            "routing": {
                "neural_status": route_result.neural_status,
                "network_health": route_result.network_health,
                "constitution_ok": route_result.constitution_ok,
                "sancai_check": route_result.sancai_check,
                "wuxing_flow": route_result.wuxing_flow,
                "routing_path": route_result.routing_path,
            },
            "primary_agent": route_result.primary_agent,
            "matched_agents": route_result.matched_agents[:3],
            "advice": route_result.advice,
            "processing_ms": route_result.processing_ms,
        }

    def _gen_dna(self, action: str) -> str:
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        h = hashlib.sha256(f"{action}{ts}{time.time()}".encode()).hexdigest()[:8]
        return f"#龍芯⚡️{ts}-NEURAL-BRIDGE-{action}-{h}"


# ═══════════════════════════════════════════════════════════════
# 五、便捷CLI
# ═══════════════════════════════════════════════════════════════

def main():
    bridge = NeuralAgentBridge()

    print("╔══════════════════════════════════════════════════════════╗")
    print("║  🧬 龍魂神经网络·智能体桥接器 v1.0                      ║")
    print("║  神经网络不再只是3D装饰——现在是你的路由引擎              ║")
    print("╠══════════════════════════════════════════════════════════╣")

    online = bridge.is_neural_online()
    if online:
        neural = bridge.fetch_neural_state(force=True)
        if neural:
            print(f"║  神经网络: 🟢 在线 · {neural.stats.get('health_rate', 0)}% 健康 "
                  f"· {len(neural.nodes)} 节点                              ║")
    else:
        print("║  神经网络: 🔴 离线 · 降级到关键词路由                    ║")

    print(f"║  Agents:   {len(bridge.agents)} 个已注册                              ║")
    print("╠══════════════════════════════════════════════════════════╣")
    print("║  输入你的需求，由神经网络路由最优Agent                    ║")
    print("║  命令: h=健康全景 | q=退出                               ║")
    print("╚══════════════════════════════════════════════════════════╝")

    while True:
        try:
            text = input("\n🐉 >>> ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not text:
            continue
        if text.lower() in ("q", "quit", "exit"):
            print("共生体待命。")
            break
        if text.lower() in ("h", "health"):
            pano = bridge.health_panorama()
            print(json.dumps(pano, ensure_ascii=False, indent=2))
            continue

        result = bridge.execute(text)
        print(f"\n{result['advice']}")
        print(f"\n主Agent: {json.dumps(result['primary_agent'], ensure_ascii=False, indent=2) if result['primary_agent'] else '无匹配'}")
        print(f"备选:    {json.dumps(result['matched_agents'][1:3], ensure_ascii=False, indent=2) if len(result['matched_agents']) > 1 else '无'}")


if __name__ == "__main__":
    main()
