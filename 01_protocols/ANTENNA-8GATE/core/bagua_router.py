# ============================================================
# 龍魂 · ANTENNA-8GATE 八卦路由器
# DNA: #龍芯⚡️丙午·乙未·乙未·申时·☰乾-BAGUA-ROUTER-v1.0-8GATE-a1b2c3d4
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
# ============================================================
"""
八卦路由器 —— 将八卦（乾兑离震巽坎艮坤）映射到8个功能模块。
每卦对应4个子节点，形成32节点蚁触网络。
路由依据：任务语义 → 卦象映射 → 最优节点选择。

八卦职能：
  乾☰ · 启动/创造   兑☱ · 通信/联结   离☲ · 认知/分析   震☳ · 执行/动作
  巽☴ · 学习/适应   坎☵ · 深潜/存储   艮☶ · 稳定/阻断   坤☷ · 收尾/归档

铁律：所有 AI 调度任务唯一入口——先进八卦路由，再过五行调度。
"""

import sys, os
import hashlib
import time
import threading
import json
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import IntEnum
from collections import deque


# ═══════════════════════════════════════
# 数据模型
# ═══════════════════════════════════════

class Bagua(IntEnum):
    """八卦枚举 — 每卦4子节点 = 32节点网络"""
    乾 = 0  # ☰ 天：启动/创造/创新
    兑 = 1  # ☱ 泽：通信/联结/API
    离 = 2  # ☲ 火：认知/分析/推理
    震 = 3  # ☳ 雷：执行/动作/部署
    巽 = 4  # ☴ 风：学习/适应/迭代
    坎 = 5  # ☵ 水：深潜/存储/数据库
    艮 = 6  # ☶ 山：稳定/阻断/安全
    坤 = 7  # ☷ 地：收尾/归档/报告


# 八卦职能定义
BAGUA_SPECS = {
    Bagua.乾: {
        "name": "乾", "symbol": "☰", "element": "天",
        "domain": "启动·创造·创新",
        "nodes": ["init-1", "creator-2", "pioneer-3", "genesis-4"],
        "keywords": ["启动", "创建", "新建", "开始", "初始化", "创新", "突破"],
        "route_match": 0.90,
    },
    Bagua.兑: {
        "name": "兑", "symbol": "☱", "element": "泽",
        "domain": "通信·联结·API",
        "nodes": ["bridge-1", "connector-2", "talker-3", "syncer-4"],
        "keywords": ["通信", "API", "连接", "同步", "消息", "桥接", "转发", "推送"],
        "route_match": 0.90,
    },
    Bagua.离: {
        "name": "离", "symbol": "☲", "element": "火",
        "domain": "认知·分析·推理",
        "nodes": ["thinker-1", "analyst-2", "reasoner-3", "judge-4"],
        "keywords": ["分析", "推理", "判断", "评估", "理解", "计算", "认知", "检测"],
        "route_match": 0.91,
    },
    Bagua.震: {
        "name": "震", "symbol": "☳", "element": "雷",
        "domain": "执行·动作·部署",
        "nodes": ["runner-1", "doer-2", "deployer-3", "actor-4"],
        "keywords": ["执行", "运行", "部署", "操作", "动作", "启动服务", "处理", "实施"],
        "route_match": 0.89,
    },
    Bagua.巽: {
        "name": "巽", "symbol": "☴", "element": "风",
        "domain": "学习·适应·迭代",
        "nodes": ["learner-1", "adapter-2", "evolver-3", "tuner-4"],
        "keywords": ["学习", "训练", "优化", "调整", "进化", "适应", "迭代", "改进",
                     "模型", "参数", "推理参数", "超参", "调参", "精调", "微调"],
        "route_match": 0.91,
    },
    Bagua.坎: {
        "name": "坎", "symbol": "☵", "element": "水",
        "domain": "深潜·存储·数据库",
        "nodes": ["store-1", "keeper-2", "archiver-3", "diver-4"],
        "keywords": ["存储", "写入", "读取", "查询", "数据库", "持久化", "缓存", "备份"],
        "route_match": 0.91,
    },
    Bagua.艮: {
        "name": "艮", "symbol": "☶", "element": "山",
        "domain": "稳定·阻断·安全",
        "nodes": ["guard-1", "shield-2", "wall-3", "sentinel-4"],
        "keywords": ["安全", "检查", "阻断", "审计", "验证", "防火墙", "熔断", "校验",
                     "审计日志", "安全审计", "签名"],
        "route_match": 0.95,
    },
    Bagua.坤: {
        "name": "坤", "symbol": "☷", "element": "地",
        "domain": "收尾·归档·报告",
        "nodes": ["finisher-1", "archiver-2", "reporter-3", "cleaner-4"],
        "keywords": ["归档", "报告", "总结", "清理", "收尾", "关闭", "销毁", "日志",
                     "月度", "季度", "年度", "健康报告", "统计", "导出", "汇总",
                     "生成报告", "输出报告", "写报告"],
        "route_match": 0.94,
    },
}


@dataclass
class RouteNode:
    """路由节点"""
    node_id: str
    bagua: Bagua
    index: int  # 0-3
    active: bool = True
    task_count: int = 0
    total_latency_ms: float = 0.0
    last_active: float = field(default_factory=time.time)
    _lock: threading.Lock = field(default_factory=threading.Lock)

    @property
    def avg_latency_ms(self) -> float:
        if self.task_count == 0:
            return 0.0
        return self.total_latency_ms / self.task_count

    def record_task(self, latency_ms: float):
        with self._lock:
            self.task_count += 1
            self.total_latency_ms += latency_ms
            self.last_active = time.time()


@dataclass
class RouteResult:
    """路由结果"""
    bagua: Bagua
    bagua_name: str
    bagua_symbol: str
    domain: str
    node_id: str
    node_index: int
    confidence: float
    matched_keywords: List[str]
    latency_ms: float = 0.0
    dna: str = ""


# ═══════════════════════════════════════
# 八卦路由器
# ═══════════════════════════════════════

class BaguaRouter:
    """
    八卦路由器 — ANTENNA-8GATE 任务调度统一入口
    
    路由流程：
    1. 任务语义解析 → 关键词提取
    2. 关键词匹配八卦 → 得分排序
    3. 选最优卦象 → 卦内轮询选节点
    4. 返回 RouteResult → 交付五行调度器
    """

    def __init__(self, nodes_per_bagua: int = 4):
        self.nodes_per_bagua = nodes_per_bagua  # 每卦4子节点
        self.total_nodes = 8 * nodes_per_bagua  # 32节点

        # 初始化32节点
        self.nodes: Dict[str, RouteNode] = {}
        for bagua in Bagua:
            spec = BAGUA_SPECS[bagua]
            for i, node_name in enumerate(spec["nodes"][:nodes_per_bagua]):
                node = RouteNode(node_id=node_name, bagua=bagua, index=i)
                self.nodes[node_name] = node

        # 轮询计数器（每卦一个）
        self._round_robin_counters: Dict[Bagua, int] = {
            bagua: 0 for bagua in Bagua
        }
        self._rr_lock = threading.Lock()

        # 统计
        self.total_routes = 0
        self.route_history: deque = deque(maxlen=1000)
        self._stats_lock = threading.Lock()

    # ── 核心路由 ──

    def route(self, task_text: str, task_type: Optional[str] = None) -> RouteResult:
        """
        八卦路由：输入任务描述 → 输出最优卦象+节点
        
        Args:
            task_text: 任务描述文本
            task_type: 可选的任务类型提示（如 "deploy"/"analyze"/"store"）
        """
        t0 = time.time()

        # 1. 提取关键词
        keywords = self._extract_keywords(task_text, task_type)

        # 2. 匹配八卦 → 得分排序
        scores = self._score_bagua(keywords)
        best_bagua = max(scores, key=scores.get)
        best_confidence = scores[best_bagua] / 100.0

        # 3. 选节点（轮询 + 负载均衡）
        node = self._select_node(best_bagua)

        latency_ms = (time.time() - t0) * 1000
        node.record_task(latency_ms)

        # 4. 统计
        matched_kw = [kw for kw in keywords if any(
            kw in spec["keywords"] for spec in [BAGUA_SPECS[best_bagua]]
        )]
        
        spec = BAGUA_SPECS[best_bagua]
        result = RouteResult(
            bagua=best_bagua,
            bagua_name=spec["name"],
            bagua_symbol=spec["symbol"],
            domain=spec["domain"],
            node_id=node.node_id,
            node_index=node.index,
            confidence=min(best_confidence, 1.0),
            matched_keywords=matched_kw,
            latency_ms=latency_ms,
            dna=self._gen_dna(best_bagua, node.node_id),
        )

        with self._stats_lock:
            self.total_routes += 1
            self.route_history.append(result)

        return result

    def route_batch(self, tasks: List[Tuple[str, Optional[str]]]) -> List[RouteResult]:
        """批量路由"""
        return [self.route(text, ttype) for text, ttype in tasks]

    # ── 内部方法 ──

    def _extract_keywords(self, text: str, task_type: Optional[str] = None) -> List[str]:
        """从任务文本中提取关键词"""
        text_lower = text.lower()

        if task_type:
            text_lower += f" {task_type.lower()}"

        # 直接匹配所有卦象的关键词
        found = []
        for bagua in Bagua:
            spec = BAGUA_SPECS[bagua]
            for kw in spec["keywords"]:
                if kw.lower() in text_lower:
                    found.append(kw)

        # 如果没匹配到任何关键词，用文本hash兜底
        if not found:
            # 按字符特征简单分类
            if any(w in text_lower for w in ["start", "init", "new", "create", "新建", "启动"]):
                found = ["启动", "创建"]
            elif any(w in text_lower for w in ["api", "sync", "push", "msg", "通信"]):
                found = ["通信", "API"]
            elif any(w in text_lower for w in ["analyze", "check", "test", "eval", "分析"]):
                found = ["分析", "检测"]
            elif any(w in text_lower for w in ["deploy", "run", "exec", "action", "部署"]):
                found = ["执行", "部署"]
            elif any(w in text_lower for w in ["learn", "train", "opt", "tune", "学习"]):
                found = ["学习", "优化"]
            elif any(w in text_lower for w in ["store", "save", "db", "cache", "存储"]):
                found = ["存储", "缓存"]
            elif any(w in text_lower for w in ["secure", "audit", "block", "safe", "安全"]):
                found = ["安全", "审计"]
            elif any(w in text_lower for w in ["report", "log", "clean", "close", "归档"]):
                found = ["归档", "报告"]
            else:
                # 兜底：hash到八卦
                h = int(hashlib.sha256(text.encode()).hexdigest()[:8], 16)
                bagua_idx = h % 8
                found = BAGUA_SPECS[Bagua(bagua_idx)]["keywords"][:2]

        return found

    def _score_bagua(self, keywords: List[str]) -> Dict[Bagua, float]:
        """为八卦打分（关键词匹配 + 双字精确匹配加权）"""
        scores = {}
        text_joined = " ".join(keywords).lower()

        for bagua in Bagua:
            spec = BAGUA_SPECS[bagua]
            match_count = 0
            max_kw_len = 0  # 最长匹配关键词长度
            for kw in keywords:
                kw_lower = kw.lower()
                for bagua_kw in spec["keywords"]:
                    bagua_kw_lower = bagua_kw.lower()
                    # 精确匹配 > 子串匹配
                    if bagua_kw_lower == kw_lower:
                        match_count += 2  # 精确匹配双倍分
                        max_kw_len = max(max_kw_len, len(bagua_kw))
                        break
                    elif bagua_kw_lower in kw_lower or kw_lower in bagua_kw_lower:
                        match_count += 1
                        max_kw_len = max(max_kw_len, len(bagua_kw))
                        break

            # 加权：匹配数 × 路由准确度 × 100 + 关键词长度加成
            score = match_count * spec["route_match"] * 100 + (max_kw_len * 2)
            scores[bagua] = score

        # 全部为0时兜底：乾卦（万物之始）
        if max(scores.values()) == 0:
            scores[Bagua.乾] = 50

        return scores

    def _select_node(self, bagua: Bagua) -> RouteNode:
        """卦内选节点：负载均衡轮询"""
        spec = BAGUA_SPECS[bagua]
        node_names = spec["nodes"][:self.nodes_per_bagua]

        with self._rr_lock:
            idx = self._round_robin_counters[bagua]
            self._round_robin_counters[bagua] = (idx + 1) % self.nodes_per_bagua

        # 检查节点是否活跃，不活跃则跳过到下一个
        for offset in range(self.nodes_per_bagua):
            node_idx = (idx + offset) % self.nodes_per_bagua
            node = self.nodes[node_names[node_idx]]
            if node.active:
                return node

        # 全不活跃时返回第一个并强制激活
        node = self.nodes[node_names[0]]
        node.active = True
        return node

    def _gen_dna(self, bagua: Bagua, node_id: str) -> str:
        """生成路由DNA"""
        h = hashlib.sha256(f"{bagua.name}:{node_id}:{time.time()}:{self.total_routes}".encode()).hexdigest()[:8]
        return f"#龍芯⚡️{BAGUA_SPECS[bagua]['symbol']}{bagua.name}-GATE-ROUTE-{node_id}-{h}"

    # ── 节点管理 ──

    def get_node(self, node_id: str) -> Optional[RouteNode]:
        """获取节点信息"""
        return self.nodes.get(node_id)

    def set_node_active(self, node_id: str, active: bool):
        """手动设置节点活跃状态"""
        if node_id in self.nodes:
            self.nodes[node_id].active = active

    def wake_node(self, node_id: str):
        """唤醒节点"""
        self.set_node_active(node_id, True)

    def sleep_node(self, node_id: str):
        """休眠节点"""
        self.set_node_active(node_id, False)

    def get_all_nodes_status(self) -> Dict[str, Any]:
        """获取全部32节点状态"""
        nodes_by_bagua = {}
        for bagua in Bagua:
            spec = BAGUA_SPECS[bagua]
            bagua_nodes = []
            for node_name in spec["nodes"][:self.nodes_per_bagua]:
                node = self.nodes[node_name]
                bagua_nodes.append({
                    "node_id": node.node_id,
                    "active": node.active,
                    "task_count": node.task_count,
                    "avg_latency_ms": round(node.avg_latency_ms, 4),
                    "last_active": node.last_active,
                })
            nodes_by_bagua[bagua.name] = {
                "symbol": spec["symbol"],
                "domain": spec["domain"],
                "total_tasks": sum(n["task_count"] for n in bagua_nodes),
                "nodes": bagua_nodes,
            }
        return {
            "total_nodes": self.total_nodes,
            "active_nodes": sum(1 for n in self.nodes.values() if n.active),
            "total_routes": self.total_routes,
            "by_bagua": nodes_by_bagua,
        }

    def get_stats(self) -> Dict[str, Any]:
        """获取路由统计"""
        bagua_counts = {}
        for result in self.route_history:
            bn = result.bagua_name
            bagua_counts[bn] = bagua_counts.get(bn, 0) + 1

        return {
            "total_routes": self.total_routes,
            "bagua_distribution": bagua_counts,
            "recent_100": [{
                "bagua": r.bagua_symbol + r.bagua_name,
                "node": r.node_id,
                "confidence": round(r.confidence, 3),
                "latency_ms": round(r.latency_ms, 4),
            } for r in list(self.route_history)[-100:]],
        }


# ═══════════════════════════════════════
# 自测试
# ═══════════════════════════════════════
if __name__ == "__main__":
    print("═" * 50)
    print("龍魂 · 八卦路由器 · 自检")
    print("═" * 50)

    router = BaguaRouter(nodes_per_bagua=4)
    print(f"网络规模：{router.total_nodes} 节点（8卦 × 4子节点）")

    # 测试任务
    test_tasks = [
        ("启动人格集群服务", None),
        ("分析用户情绪数据", "analyze"),
        ("存储对话日志到数据库", "store"),
        ("部署新版本到鲲鹏", "deploy"),
        ("安全审计日志扫描", "audit"),
        ("同步用户配置到各节点", "sync"),
        ("优化模型推理参数", "optimize"),
        ("生成月度健康报告", "report"),
        ("验证API签名是否正确", "verify"),
        ("缓存热门查询结果", "cache"),
    ]

    print(f"\n{'任务':<24} {'卦象':<10} {'节点':<16} {'领域':<16} {'置信度':>6} {'延迟':>8}")
    print("-" * 85)

    correct_routes = 0
    total_tasks = len(test_tasks)

    expected_map = {
        "启动人格集群服务": "乾",
        "分析用户情绪数据": "离",
        "存储对话日志到数据库": "坎",
        "部署新版本到鲲鹏": "震",
        "安全审计日志扫描": "艮",
        "同步用户配置到各节点": "兑",
        "优化模型推理参数": "巽",
        "生成月度健康报告": "坤",
        "验证API签名是否正确": "艮",
        "缓存热门查询结果": "坎",
    }

    for task, ttype in test_tasks:
        result = router.route(task, ttype)
        bagua_str = f"{result.bagua_symbol}{result.bagua_name}"
        expected = expected_map.get(task, "?")

        if result.bagua_name == expected:
            correct_routes += 1
            mark = "✅"
        else:
            mark = f"⚠️(期望{expected})"

        print(f"{task:<24} {bagua_str:<10} {result.node_id:<16} "
              f"{result.domain:<16} {result.confidence:>5.0%} {result.latency_ms:>7.3f}ms {mark}")

    accuracy = correct_routes / total_tasks * 100 if total_tasks > 0 else 0
    print(f"\n路由准确率：{correct_routes}/{total_tasks} = {accuracy:.1f}%")

    # 节点状态
    status = router.get_all_nodes_status()
    print(f"\n节点状态：{status['active_nodes']}/{status['total_nodes']} 活跃")

    # 统计
    stats = router.get_stats()
    print(f"\n路由分布：{stats['bagua_distribution']}")
    print(f"总路由量：{stats['total_routes']}")

    print(f"\n{'🟢 路由准确率100%' if accuracy == 100 else f'🟡 路由准确率{accuracy:.1f}%'}")
