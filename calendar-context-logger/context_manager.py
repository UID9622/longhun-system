#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂认知上下文管理器 v3.0
LongHun Cognitive Context Manager v3.0

功能：管理对话上下文的全生命周期，包括状态机、压缩、知识图谱联动、DNA追溯
定位：L1认知层，输入过滤协议v3.0的下游
体系：龍魂系统 UID9622

技术规范：
  - Python 3.8+，零外部依赖（仅标准库）
  - DNA追溯每个操作
  - 时间戳精确到毫秒
  - 三色审计（红/黄/绿）
  - 龍字简体（用户可见文本）

DNA: #龍芯⚡️2026-06-27-LONGHUN-CTX-MGR-v3.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬CTX-MGR-v3.0
"""

import json
import os
import hashlib
import time
import shutil
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict


# ═══════════════════════════════════════════════════════════════
# 常量定义
# ═══════════════════════════════════════════════════════════════

class AuditColor(Enum):
    """三色审计颜色"""
    RED = "🔴"      # 阻塞级
    YELLOW = "🟡"   # 警告级
    GREEN = "🟢"    # 通过级


class ContextState(Enum):
    """上下文四态模型"""
    ACTIVE = "active"       # 活跃：上下文全加载
    STANDBY = "standby"     # 待机：上下文未回收，标记时间
    SWITCHED = "switched"   # 已切换：旧上下文归档，新上下文加载中
    CLOSED = "closed"       # 已关闭：完整归档，DNA记录


class CompressionLevel(Enum):
    """四级压缩级别"""
    L0 = "L0"   # 不压缩
    L1 = "L1"   # 摘要压缩
    L2 = "L2"   # 实体提取
    L3 = "L3"   # 长期记忆固化


# 阈值参数（与协议附录A对齐）
THRESHOLD_SIMILARITY_SAME = 70       # 同话题阈值
THRESHOLD_SIMILARITY_DRIFT = 40      # 漂移阈值
THRESHOLD_CTX_WARNING = 4000         # 上下文大小警告（tokens）
THRESHOLD_CTX_BLOCK = 8000           # 上下文大小阻断（tokens）
THRESHOLD_KG_NODES_MAX = 20          # 知识图谱节点上限
THRESHOLD_ROUNDS_ARCHIVE = 50        # 建议归档轮数
TEMPERATURE_COOLDOWN_RATE = 0.9      # 降温速率/秒
TEMPERATURE_SLEEP_THRESHOLD = 0.1    # 休眠阈值
KG_MAX_EXPAND_DEPTH = 2              # 知识图谱最大展开深度
KG_MAX_EXPAND_NODES = 20             # 知识图谱最大展开节点数
STANDBY_TIMEOUT_SECONDS = 30         # 待机检测秒数（仅提醒，不自动操作）

# 用户明确指令白名单（无需确认）
SWITCH_COMMANDS = ["换话题", "换一个话题", "聊别的", "下一个", "下一个话题"]
RETURN_COMMANDS = ["回到", "恢复"]
CLOSE_COMMANDS = ["结束", "结束对话", "拜拜", "再见", "关闭"]

# 目录结构
HOME_DIR = os.path.expanduser("~")
BASE_DIR = os.path.join(HOME_DIR, ".longhun/calendar-context-logger")
WORKSPACE_DIR = os.path.join(BASE_DIR, "workspace")
ACTIVE_DIR = os.path.join(WORKSPACE_DIR, "active")
STANDBY_DIR = os.path.join(WORKSPACE_DIR, "standby")
ARCHIVE_ACTIVE_DIR = os.path.join(WORKSPACE_DIR, "archive", "active")
ARCHIVE_CLOSED_DIR = os.path.join(WORKSPACE_DIR, "archive", "closed")
MEMORY_DIR = os.path.join(WORKSPACE_DIR, "memory", "longterm")
KG_DIR = os.path.join(BASE_DIR, "knowledge-graph")
AUDIT_LOG = os.path.join(BASE_DIR, "audit", "context_audit.log")


# ═══════════════════════════════════════════════════════════════
# 数据类定义
# ═══════════════════════════════════════════════════════════════

@dataclass
class SemanticAnchor:
    """语义锚点（复用输入过滤协议v3.0的输出）"""
    type: str       # entity|action|constraint
    value: str
    position: int = 0


@dataclass
class ContextInput:
    """从输入过滤协议接收的结构化输入"""
    cnsh_header: str = ""
    raw_input: str = ""
    semantic_anchors: List[SemanticAnchor] = field(default_factory=list)
    input_type: str = "user_query"   # user_query|api_call|file_import|sensor_data
    confidence_score: float = 0.0
    risk_flags: List[str] = field(default_factory=list)
    audit_trail: List[Dict] = field(default_factory=list)
    timestamp: str = ""


@dataclass
class KGNode:
    """知识图谱节点（运行时表示）"""
    node_id: str
    name: str
    description: str = ""
    node_type: str = ""
    layer: str = ""
    weight: float = 50.0
    temperature: float = 1.0
    state: str = "active"
    match_score: float = 0.0
    distance: int = 0  # 距离当前话题的层数


@dataclass
class KGEdge:
    """知识图谱边（运行时表示）"""
    edge_id: str
    source: str
    target: str
    relation: str
    weight: float = 5.0


@dataclass
class DNARecord:
    """DNA证据链记录"""
    context_id: str
    session_id: str
    operation_type: str
    timestamp: str
    state_before: str = ""
    state_after: str = ""
    trigger_reason: str = ""
    user_confirmed: str = ""     # 已确认/无需确认/未确认
    compression_level: str = "N/A"
    compression_ratio: str = "N/A"
    kg_nodes_related: int = 0
    confidence_score: float = 0.0
    audit_color: str = AuditColor.GREEN.value
    operator: str = "龍芯上下文引擎"
    dna_signature: str = ""

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class CompressionReport:
    """压缩报告"""
    level: str
    topic_id: str
    timestamp: str
    compression_ratio: str
    items_preserved: int
    items_discarded: int
    dna_signature: str
    audit_color: str


# ═══════════════════════════════════════════════════════════════
# DNA追溯工具
# ═══════════════════════════════════════════════════════════════

class DNATracer:
    """DNA追溯引擎 —— 每个操作都有记录，有时间戳"""

    @staticmethod
    def now() -> str:
        """获取当前时间戳，精确到毫秒"""
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.") + f"{datetime.now().microsecond // 1000:03d}Z"

    @staticmethod
    def sign(data: Dict) -> str:
        """生成DNA签名（SHA256）"""
        content = json.dumps(data, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]

    @staticmethod
    def generate_header(module: str, operation: str, obj_id: str, version: str = "v3.0") -> str:
        """生成CNSH结构化头部"""
        ts = DNATracer.now()
        return f"#龍[{module}]⚡️{ts}-LONGHUN-{operation}-{obj_id}-{version}"

    @staticmethod
    def create_record(
        context_id: str,
        session_id: str,
        operation_type: str,
        state_before: str = "",
        state_after: str = "",
        trigger_reason: str = "",
        user_confirmed: str = "无需确认",
        compression_level: str = "N/A",
        compression_ratio: str = "N/A",
        kg_nodes_related: int = 0,
        confidence_score: float = 0.0,
        audit_color: str = AuditColor.GREEN.value
    ) -> DNARecord:
        """创建完整的DNA记录"""
        ts = DNATracer.now()
        data = {
            "context_id": context_id,
            "session_id": session_id,
            "operation": operation_type,
            "timestamp": ts,
            "state": state_after,
        }
        sig = DNATracer.sign(data)
        return DNARecord(
            context_id=context_id,
            session_id=session_id,
            operation_type=operation_type,
            timestamp=ts,
            state_before=state_before,
            state_after=state_after,
            trigger_reason=trigger_reason,
            user_confirmed=user_confirmed,
            compression_level=compression_level,
            compression_ratio=compression_ratio,
            kg_nodes_related=kg_nodes_related,
            confidence_score=confidence_score,
            audit_color=audit_color,
            dna_signature=sig
        )

    @staticmethod
    def write_audit_log(record: DNARecord):
        """写入审计日志"""
        os.makedirs(os.path.dirname(AUDIT_LOG), exist_ok=True)
        with open(AUDIT_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(record.to_dict(), ensure_ascii=False) + "\n")


# ═══════════════════════════════════════════════════════════════
# 三色审计引擎
# ═══════════════════════════════════════════════════════════════

class AuditEngine:
    """三色审计引擎"""

    @staticmethod
    def evaluate(
        confidence_score: float,
        risk_flags: List[str] = None,
        user_confirmed: bool = True,
        state_transition_valid: bool = True
    ) -> Tuple[str, str]:
        """
        三色审计判定
        返回: (audit_color, decision)
        """
        if risk_flags is None:
            risk_flags = []

        # 红色判定条件
        if confidence_score <= 29 or not state_transition_valid:
            return AuditColor.RED.value, "阻断"
        if "context_overflow" in risk_flags:
            return AuditColor.RED.value, "阻断"

        # 黄色判定条件
        if confidence_score <= 59:
            return AuditColor.YELLOW.value, "警告"
        if not user_confirmed and confidence_score < 70:
            return AuditColor.YELLOW.value, "需确认"
        if any(f in risk_flags for f in ["similarity_drift", "near_limit"]):
            return AuditColor.YELLOW.value, "警告"

        # 绿色
        return AuditColor.GREEN.value, "通过"

    @staticmethod
    def log(color: str, message: str):
        """输出带审计色的日志"""
        ts = DNATracer.now()
        print(f"[{color}] [{ts}] {message}")


# ═══════════════════════════════════════════════════════════════
# 知识图谱联动引擎
# ═══════════════════════════════════════════════════════════════

class KGEngine:
    """知识图谱联动引擎 —— 与65节点·103边对接"""

    def __init__(self, kg_dir: str = KG_DIR):
        self.kg_dir = kg_dir
        self._nodes: Dict[str, Dict] = {}
        self._edges: List[Dict] = []
        self._node_temperatures: Dict[str, float] = {}
        self._loaded = False
        self._load_kg()

    def _load_kg(self):
        """加载知识图谱数据"""
        nodes_file = os.path.join(self.kg_dir, "nodes", "all_nodes.json")
        edges_file = os.path.join(self.kg_dir, "edges", "all_edges.json")

        if os.path.exists(nodes_file):
            try:
                with open(nodes_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for node in data.get("nodes", []):
                        self._nodes[node["node_id"]] = node
                        self._node_temperatures[node["node_id"]] = 1.0
            except Exception as e:
                AuditEngine.log(AuditColor.YELLOW.value, f"知识图谱节点加载警告: {e}")

        if os.path.exists(edges_file):
            try:
                with open(edges_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._edges = data.get("edges", [])
            except Exception as e:
                AuditEngine.log(AuditColor.YELLOW.value, f"知识图谱边加载警告: {e}")

        self._loaded = True
        AuditEngine.log(AuditColor.GREEN.value,
            f"知识图谱加载完成: {len(self._nodes)}节点, {len(self._edges)}边")

    def match(self, keywords: List[str]) -> List[KGNode]:
        """
        根据关键词匹配知识图谱节点
        返回: 按匹配度排序的节点列表
        """
        results = []
        keywords_lower = [k.lower() for k in keywords]

        for node_id, node in self._nodes.items():
            score = 0
            name = node.get("name", "").lower()
            desc = node.get("description", "").lower()

            for kw in keywords_lower:
                if kw in name:
                    score += 30
                if kw in desc:
                    score += 10
                # 编辑距离 ≤ 2 的模糊匹配
                if self._edit_distance(kw, name) <= 2:
                    score += 15

            if score > 0:
                props = node.get("properties", {})
                kg_node = KGNode(
                    node_id=node_id,
                    name=node.get("name", ""),
                    description=node.get("description", ""),
                    node_type=node.get("node_type", ""),
                    layer=node.get("layer", ""),
                    weight=props.get("weight", 50),
                    temperature=self._node_temperatures.get(node_id, 1.0),
                    state=node.get("state", "active"),
                    match_score=min(score, 100),
                    distance=0
                )
                results.append(kg_node)

        results.sort(key=lambda x: x.match_score, reverse=True)
        return results[:KG_MAX_EXPAND_NODES]

    def expand(self, node_ids: List[str], depth: int = KG_MAX_EXPAND_DEPTH) -> List[KGNode]:
        """
        沿关系加载关联节点（最多2层）
        返回: 扩展节点列表
        """
        if depth <= 0:
            return []

        results = []
        related_ids = set(node_ids)

        for edge in self._edges:
            if edge["source"] in node_ids:
                related_ids.add(edge["target"])
            if edge.get("bidirectional") and edge["target"] in node_ids:
                related_ids.add(edge["source"])

        # 递归展开（控制深度）
        if depth > 1:
            next_level = self.expand(list(related_ids - set(node_ids)), depth=depth - 1)
            results.extend(next_level)

        for rid in related_ids:
            if rid not in self._nodes or rid in node_ids:
                continue
            node = self._nodes[rid]
            props = node.get("properties", {})
            results.append(KGNode(
                node_id=rid,
                name=node.get("name", ""),
                description=node.get("description", ""),
                node_type=node.get("node_type", ""),
                layer=node.get("layer", ""),
                weight=props.get("weight", 50),
                temperature=self._node_temperatures.get(rid, 1.0),
                state=node.get("state", "active"),
                match_score=0,
                distance=KG_MAX_EXPAND_DEPTH - depth + 1
            ))

        return results[:KG_MAX_EXPAND_NODES]

    def set_temperature(self, node_ids: List[str], temp: float):
        """设置节点温度"""
        for nid in node_ids:
            self._node_temperatures[nid] = max(0.0, min(1.0, temp))

    def cooldown(self, current_node_ids: List[str], elapsed_seconds: float):
        """
        全局降温 —— 不相关节点自动降温
        """
        cooldown_factor = TEMPERATURE_COOLDOWN_RATE ** elapsed_seconds
        for nid in self._node_temperatures:
            if nid not in current_node_ids:
                self._node_temperatures[nid] *= cooldown_factor

    def get_active_nodes(self) -> List[KGNode]:
        """获取当前活跃的节点（temperature >= 0.1）"""
        active = []
        for nid, temp in self._node_temperatures.items():
            if temp >= TEMPERATURE_SLEEP_THRESHOLD and nid in self._nodes:
                node = self._nodes[nid]
                props = node.get("properties", {})
                active.append(KGNode(
                    node_id=nid,
                    name=node.get("name", ""),
                    node_type=node.get("node_type", ""),
                    layer=node.get("layer", ""),
                    weight=props.get("weight", 50),
                    temperature=temp,
                    state=node.get("state", "active")
                ))
        return active

    @staticmethod
    def _edit_distance(s1: str, s2: str) -> int:
        """计算编辑距离（Levenshtein）"""
        if len(s1) < len(s2):
            return KGEngine._edit_distance(s2, s1)
        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]


# ═══════════════════════════════════════════════════════════════
# 压缩引擎
# ═══════════════════════════════════════════════════════════════

class CompressionEngine:
    """L0-L3 四级压缩引擎"""

    def __init__(self, tracer: DNATracer):
        self.tracer = tracer

    def compress(self, context: Dict, level: CompressionLevel, topic_id: str, session_id: str) -> Tuple[Dict, CompressionReport]:
        """
        执行压缩
        返回: (压缩后数据, 压缩报告)
        """
        ts = self.tracer.now()

        if level == CompressionLevel.L0:
            return self._compress_l0(context, topic_id, session_id, ts)
        elif level == CompressionLevel.L1:
            return self._compress_l1(context, topic_id, session_id, ts)
        elif level == CompressionLevel.L2:
            return self._compress_l2(context, topic_id, session_id, ts)
        elif level == CompressionLevel.L3:
            return self._compress_l3(context, topic_id, session_id, ts)
        else:
            raise ValueError(f"未知压缩级别: {level}")

    def _compress_l0(self, context: Dict, topic_id: str, session_id: str, ts: str) -> Tuple[Dict, CompressionReport]:
        """L0: 不压缩，仅添加DNA标记"""
        header = self.tracer.generate_header("CTX-L0", "ACTIVE", topic_id)
        result = {
            "cnsh_header": header,
            "compression_level": "L0",
            "status": "active_no_compression",
            "context": context,
            "dna": f"#龍芯⚡️{ts}-LONGHUN-CTX-L0-{topic_id}-v3.0"
        }
        report = CompressionReport(
            level="L0",
            topic_id=topic_id,
            timestamp=ts,
            compression_ratio="0%",
            items_preserved=len(str(context)),
            items_discarded=0,
            dna_signature=self.tracer.sign(result),
            audit_color=AuditColor.GREEN.value
        )
        return result, report

    def _compress_l1(self, context: Dict, topic_id: str, session_id: str, ts: str) -> Tuple[Dict, CompressionReport]:
        """L1: 摘要压缩 —— 保留摘要+关键结论+未完成项"""
        # 提取信息
        messages = context.get("messages", [])
        summary = self._generate_summary(messages)
        conclusions = self._extract_conclusions(messages)
        pending = self._extract_pending(messages)
        skills = context.get("skills_triggered", [])
        kg_nodes = context.get("kg_nodes_related", [])

        header = self.tracer.generate_header("CTX-L1", "SUMMARY", topic_id)
        result = {
            "cnsh_header": header,
            "compression_level": "L1",
            "topic_id": topic_id,
            "session_id": session_id,
            "timestamp_start": context.get("timestamp_start", ts),
            "timestamp_end": ts,
            "summary": summary,
            "key_conclusions": conclusions,
            "pending_items": pending,
            "skills_triggered": skills,
            "kg_nodes_related": kg_nodes,
            "confidence_score": 85,
            "audit_color": AuditColor.GREEN.value,
            "dna": f"#龍芯⚡️{ts}-LONGHUN-CTX-L1-{topic_id}-v3.0"
        }

        original_size = len(json.dumps(context))
        compressed_size = len(json.dumps(result))
        ratio = f"{((original_size - compressed_size) / original_size * 100):.0f}%"

        report = CompressionReport(
            level="L1",
            topic_id=topic_id,
            timestamp=ts,
            compression_ratio=ratio,
            items_preserved=3,  # summary + conclusions + pending
            items_discarded=len(messages),
            dna_signature=self.tracer.sign(result),
            audit_color=AuditColor.GREEN.value
        )
        return result, report

    def _compress_l2(self, context: Dict, topic_id: str, session_id: str, ts: str) -> Tuple[Dict, CompressionReport]:
        """L2: 实体提取 —— 保留核心实体+关系图谱节点链接"""
        entities = self._extract_entities(context)
        decisions = context.get("key_decisions", [])
        pref_delta = context.get("user_preferences_delta", [])

        header = self.tracer.generate_header("CTX-L2", "ENTITY", topic_id)
        result = {
            "cnsh_header": header,
            "compression_level": "L2",
            "topic_id": topic_id,
            "session_id": session_id,
            "timestamp_closed": ts,
            "core_entities": entities,
            "key_decisions": decisions,
            "user_preferences_delta": pref_delta,
            "confidence_score": 75,
            "audit_color": AuditColor.GREEN.value,
            "dna": f"#龍芯⚡️{ts}-LONGHUN-CTX-L2-{topic_id}-v3.0"
        }

        original_size = len(json.dumps(context))
        compressed_size = len(json.dumps(result))
        ratio = f"{((original_size - compressed_size) / original_size * 100):.0f}%"

        report = CompressionReport(
            level="L2",
            topic_id=topic_id,
            timestamp=ts,
            compression_ratio=ratio,
            items_preserved=len(entities),
            items_discarded=0,
            dna_signature=self.tracer.sign(result),
            audit_color=AuditColor.GREEN.value
        )
        return result, report

    def _compress_l3(self, context: Dict, topic_id: str, session_id: str, ts: str) -> Tuple[Dict, CompressionReport]:
        """L3: 长期记忆固化 —— 保留关键决策+用户偏好+技能列表"""
        critical_decisions = self._extract_critical_decisions(context)
        pref_profile = self._build_preference_profile(context)
        skill_patterns = context.get("skill_trigger_patterns", [])

        header = self.tracer.generate_header("CTX-L3", "MEMORY", session_id)
        result = {
            "cnsh_header": header,
            "compression_level": "L3",
            "session_id": session_id,
            "timestamp_archived": ts,
            "critical_decisions": critical_decisions,
            "user_preference_profile": pref_profile,
            "skill_trigger_patterns": skill_patterns,
            "confidence_score": 90,
            "audit_color": AuditColor.GREEN.value,
            "dna": f"#龍芯⚡️{ts}-LONGHUN-CTX-L3-{session_id}-v3.0"
        }

        original_size = len(json.dumps(context))
        compressed_size = len(json.dumps(result))
        ratio = f"{((original_size - compressed_size) / original_size * 100):.0f}%"

        report = CompressionReport(
            level="L3",
            topic_id=topic_id,
            timestamp=ts,
            compression_ratio=ratio,
            items_preserved=3,
            items_discarded=0,
            dna_signature=self.tracer.sign(result),
            audit_color=AuditColor.GREEN.value
        )
        return result, report

    # ── 辅助方法 ──

    @staticmethod
    def _generate_summary(messages: List[Dict]) -> str:
        """生成摘要（简化实现）"""
        if not messages:
            return "（无对话内容）"
        # 取首尾各30%的消息作为摘要基础
        n = len(messages)
        start_msgs = messages[:max(1, n // 3)]
        end_msgs = messages[-max(1, n // 3):]
        summary_parts = []
        for m in start_msgs[:2]:
            content = m.get("content", "")
            summary_parts.append(content[:50] + "..." if len(content) > 50 else content)
        if n > 4:
            summary_parts.append("...")
        for m in end_msgs[-2:]:
            content = m.get("content", "")
            summary_parts.append(content[:50] + "..." if len(content) > 50 else content)
        return " | ".join(summary_parts)[:200]

    @staticmethod
    def _extract_conclusions(messages: List[Dict]) -> List[str]:
        """提取关键结论（查找结论性语句）"""
        conclusions = []
        conclusion_markers = ["结论", "总结", "决定", "方案", "结果是", "因此"]
        for m in messages:
            content = m.get("content", "")
            for marker in conclusion_markers:
                if marker in content:
                    # 提取包含标记的句子
                    start = content.find(marker)
                    end = content.find("。", start)
                    if end == -1:
                        end = start + 100
                    sentence = content[start:end + 1].strip()
                    if sentence and sentence not in conclusions:
                        conclusions.append(sentence[:100])
        return conclusions[:5]  # 最多5条

    @staticmethod
    def _extract_pending(messages: List[Dict]) -> List[Dict]:
        """提取未完成项"""
        pending = []
        pending_markers = ["待办", "TODO", "待处理", "后续", "需要"]
        for m in messages:
            content = m.get("content", "")
            for marker in pending_markers:
                if marker in content:
                    start = content.find(marker)
                    end = content.find("。", start)
                    if end == -1:
                        end = start + 100
                    item = content[start:end + 1].strip()
                    if item:
                        pending.append({
                            "item": item[:100],
                            "priority": "medium",
                            "created_at": m.get("timestamp", "")
                        })
        return pending[:10]

    @staticmethod
    def _extract_entities(context: Dict) -> List[Dict]:
        """提取核心实体"""
        entities = []
        # 从语义锚点提取
        for anchor in context.get("semantic_anchors", []):
            if anchor.get("type") in ["entity", "person", "thing", "concept"]:
                entities.append({
                    "entity_type": anchor.get("type", "unknown"),
                    "name": anchor.get("value", ""),
                    "kg_node_link": ""
                })
        # 去重
        seen = set()
        unique = []
        for e in entities:
            if e["name"] not in seen:
                seen.add(e["name"])
                unique.append(e)
        return unique[:20]

    @staticmethod
    def _extract_critical_decisions(context: Dict) -> List[Dict]:
        """提取关键决策"""
        decisions = context.get("key_decisions", [])
        return [{"what": d.get("decision", ""), "why": d.get("reason", ""), "when": d.get("timestamp", "")}
                for d in decisions[:10]]

    @staticmethod
    def _build_preference_profile(context: Dict) -> Dict:
        """构建用户偏好画像"""
        return {
            "communication_style": context.get("communication_style", "balanced"),
            "skill_usage_patterns": context.get("skill_usage_patterns", []),
            "topic_interests": context.get("topic_interests", []),
            "response_preferences": context.get("response_preferences", {"detail_level": "detailed", "language": "zh"})
        }


# ═══════════════════════════════════════════════════════════════
# 上下文管理器（核心类）
# ═══════════════════════════════════════════════════════════════

class ContextManager:
    """
    龍魂认知上下文管理器 —— 核心类
    管理窗口状态机、压缩、知识图谱联动、DNA追溯
    """

    def __init__(self):
        # 初始化目录
        self._init_dirs()

        # 核心引擎
        self.tracer = DNATracer()
        self.audit = AuditEngine()
        self.compression = CompressionEngine(self.tracer)
        self.kg = KGEngine()

        # 当前状态
        self._current_state = ContextState.ACTIVE
        self._current_topic_id = ""
        self._current_session_id = self._generate_session_id()
        self._current_context: Dict = {}
        self._standby_since: Optional[float] = None
        self._message_count = 0
        self._context_size_tokens = 0

        # 历史记录
        self._topic_history: List[Dict] = []

        # DNA记录缓存
        self._dna_records: List[DNARecord] = []

        AuditEngine.log(AuditColor.GREEN.value,
            f"上下文管理器初始化完成 | 会话: {self._current_session_id}")

    def _init_dirs(self):
        """初始化目录结构"""
        for d in [ACTIVE_DIR, STANDBY_DIR, ARCHIVE_ACTIVE_DIR, ARCHIVE_CLOSED_DIR, MEMORY_DIR]:
            os.makedirs(d, exist_ok=True)

    @staticmethod
    def _generate_session_id() -> str:
        """生成会话ID"""
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        rnd = hashlib.sha256(str(time.time()).encode()).hexdigest()[:6]
        return f"session_{ts}_{rnd}"

    @staticmethod
    def _generate_topic_id(title: str) -> str:
        """生成话题ID"""
        h = hashlib.sha256(title.encode()).hexdigest()[:8]
        return f"topic_{h}"

    # ── 状态查询 ──

    def get_status(self) -> Dict:
        """获取当前上下文状态（MCP工具: longhun_ctx_status）"""
        active_nodes = self.kg.get_active_nodes()
        return {
            "cnsh_header": self.tracer.generate_header("CTX-STATUS", "QUERY", self._current_topic_id or "default"),
            "session_id": self._current_session_id,
            "current_state": self._current_state.value,
            "current_topic_id": self._current_topic_id,
            "message_count": self._message_count,
            "context_size_tokens": self._context_size_tokens,
            "standby_since": self._standby_since,
            "kg_active_nodes": len(active_nodes),
            "kg_nodes": [{"node_id": n.node_id, "name": n.name, "temperature": n.temperature}
                         for n in active_nodes[:10]],
            "topic_history_count": len(self._topic_history),
            "timestamp": self.tracer.now(),
            "dna": f"#龍芯⚡️{self.tracer.now()}-LONGHUN-CTX-STATUS-{self._current_session_id}-v3.0"
        }

    # ── 话题切换（核心方法）──

    def switch_topic(self, new_topic: str, user_confirmed: bool = False) -> Dict:
        """
        话题切换（MCP工具: longhun_ctx_switch）
        包含用户确认流程
        """
        ts = self.tracer.now()
        old_topic_id = self._current_topic_id
        old_topic_title = self._current_context.get("title", "未命名话题")
        new_topic_id = self._generate_topic_id(new_topic)

        # 检查是否需要用户确认
        needs_confirmation = self._needs_confirmation(new_topic)

        if needs_confirmation and not user_confirmed:
            # 返回确认请求
            return {
                "action": "request_confirm",
                "message": f"检测到话题切换意图（从「{old_topic_title}」到「{new_topic}」），是否确认切换？已完成的讨论将归档，可随时恢复。",
                "options": ["确认切换", "继续当前话题"],
                "old_topic": old_topic_title,
                "new_topic": new_topic,
                "audit_color": AuditColor.YELLOW.value
            }

        # 执行切换
        # 1. L1压缩旧上下文
        if self._current_context:
            compressed, report = self.compression.compress(
                self._current_context, CompressionLevel.L1, old_topic_id, self._current_session_id
            )
            # 写入归档
            archive_path = os.path.join(ARCHIVE_ACTIVE_DIR,
                f"ctx_{old_topic_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_L1.json")
            with open(archive_path, "w", encoding="utf-8") as f:
                json.dump(compressed, f, ensure_ascii=False, indent=2)
            AuditEngine.log(AuditColor.GREEN.value,
                f"L1压缩完成: {report.compression_ratio} | 归档: {archive_path}")

        # 2. 状态转换
        old_state = self._current_state
        self._current_state = ContextState.SWITCHED

        # 3. DNA记录
        record = self.tracer.create_record(
            context_id=new_topic_id,
            session_id=self._current_session_id,
            operation_type="SWITCH",
            state_before=old_state.value,
            state_after=ContextState.SWITCHED.value,
            trigger_reason="user_confirmed" if user_confirmed else "semantic_detection",
            user_confirmed="已确认" if user_confirmed else "经确认",
            compression_level="L1",
            kg_nodes_related=len(self.kg.get_active_nodes()),
            confidence_score=85 if user_confirmed else 65
        )
        self._dna_records.append(record)
        self.tracer.write_audit_log(record)

        # 4. 知识图谱降温旧节点，加载新节点
        old_nodes = [n.node_id for n in self.kg.get_active_nodes()]
        self.kg.set_temperature(old_nodes, 0.3)  # 降温

        # 新话题关键词匹配
        keywords = self._extract_keywords(new_topic)
        matched = self.kg.match(keywords)
        if matched:
            matched_ids = [n.node_id for n in matched]
            self.kg.set_temperature(matched_ids, 1.0)
            expanded = self.kg.expand(matched_ids, depth=KG_MAX_EXPAND_DEPTH)
            AuditEngine.log(AuditColor.GREEN.value,
                f"知识图谱联动: {len(matched)}直接匹配, {len(expanded)}关联节点")

        # 5. 初始化新上下文
        self._current_topic_id = new_topic_id
        self._current_context = {
            "title": new_topic,
            "topic_id": new_topic_id,
            "timestamp_start": ts,
            "messages": [],
            "semantic_anchors": [],
            "skills_triggered": [],
            "kg_nodes_related": [n.node_id for n in matched] if matched else [],
            "persona": "default"
        }
        self._message_count = 0
        self._context_size_tokens = 0
        self._current_state = ContextState.ACTIVE
        self._standby_since = None

        # 6. 记录历史
        self._topic_history.append({
            "topic_id": new_topic_id,
            "title": new_topic,
            "switched_at": ts,
            "previous_topic": old_topic_id
        })

        # 7. 返回结果
        result = {
            "action": "switched",
            "old_topic": old_topic_title,
            "new_topic": new_topic,
            "new_topic_id": new_topic_id,
            "session_id": self._current_session_id,
            "kg_nodes_loaded": len(matched) + len(expanded) if matched else 0,
            "audit_color": AuditColor.GREEN.value if user_confirmed else AuditColor.YELLOW.value,
            "dna_record": record.to_dict(),
            "timestamp": ts
        }

        AuditEngine.log(result["audit_color"],
            f"话题切换完成: {old_topic_title} → {new_topic}")
        return result

    def _needs_confirmation(self, new_input: str) -> bool:
        """判断是否需要用户确认"""
        # 检查白名单
        lower = new_input.lower()
        for cmd in SWITCH_COMMANDS:
            if cmd in lower:
                return False  # 明确指令，无需确认

        # 语义相似度计算
        if self._current_context:
            current_topic = self._current_context.get("title", "")
            similarity = self._calculate_similarity(current_topic, new_input)
            return similarity < THRESHOLD_SIMILARITY_DRIFT

        return False  # 没有当前上下文，无需确认

    @staticmethod
    def _calculate_similarity(text1: str, text2: str) -> float:
        """计算语义相似度（Jaccard + 简单重叠）"""
        if not text1 or not text2:
            return 0.0

        # Jaccard相似度
        set1 = set(text1.lower())
        set2 = set(text2.lower())
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        jaccard = (intersection / union * 100) if union > 0 else 0

        # 关键词重叠
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        word_overlap = len(words1 & words2) / max(len(words1), 1) * 100

        return jaccard * 0.4 + word_overlap * 0.6

    @staticmethod
    def _extract_keywords(text: str) -> List[str]:
        """从文本中提取关键词"""
        # 简单的关键词提取（按长度和频率）
        words = text.lower().split()
        # 过滤常见停用词
        stopwords = {"的", "了", "是", "在", "我", "有", "和", "就", "不", "人", "都", "一", "一个", "上", "也", "很", "到", "说", "要", "去", "你", "会", "着", "没有", "看", "好", "自己", "这", "那"}
        keywords = [w for w in words if w not in stopwords and len(w) >= 2]
        # 去重并保持顺序
        seen = set()
        unique = []
        for k in keywords:
            if k not in seen:
                seen.add(k)
                unique.append(k)
        return unique[:10]

    # ── 处理用户输入 ──

    def process_input(self, ctx_input: ContextInput) -> Dict:
        """
        处理用户输入（主入口）
        输入: 从输入过滤协议v3.0接收的ContextInput
        输出: 处理结果 + 状态更新
        """
        ts = self.tracer.now()
        raw = ctx_input.raw_input

        # 1. 检查明确指令
        cmd_result = self._check_explicit_commands(raw)
        if cmd_result:
            return cmd_result

        # 2. 如果当前是STANDBY，恢复ACTIVE
        if self._current_state == ContextState.STANDBY:
            self._current_state = ContextState.ACTIVE
            self._standby_since = None
            AuditEngine.log(AuditColor.GREEN.value, "从待机恢复活跃")

        # 3. 检查上下文健康
        health = self._check_context_health()
        if health["blocked"]:
            return {
                "action": "request_action",
                "message": f"上下文即将达到上限（{self._context_size_tokens} tokens），建议压缩归档。",
                "options": ["立即压缩", "继续对话"],
                "audit_color": AuditColor.YELLOW.value
            }

        # 4. 语义相似度检测（话题漂移检测）
        if self._current_context.get("title"):
            similarity = self._calculate_similarity(self._current_context["title"], raw)
            if similarity < THRESHOLD_SIMILARITY_DRIFT:
                # 话题漂移，请求确认
                return {
                    "action": "request_confirm",
                    "message": f"您输入的内容与当前话题「{self._current_context['title']}」差异较大，是否切换话题？",
                    "options": ["切换话题", "继续当前话题"],
                    "similarity_score": round(similarity, 1),
                    "audit_color": AuditColor.YELLOW.value
                }

        # 5. 知识图谱联动
        keywords = self._extract_keywords(raw)
        anchors = [{"type": a.type, "value": a.value} for a in ctx_input.semantic_anchors]
        all_keywords = list(set(keywords + [a["value"] for a in anchors]))

        matched = self.kg.match(all_keywords)
        if matched:
            matched_ids = [n.node_id for n in matched]
            self.kg.set_temperature(matched_ids, 1.0)
            expanded = self.kg.expand(matched_ids, depth=KG_MAX_EXPAND_DEPTH)
        else:
            expanded = []

        # 6. 更新上下文
        self._current_context.setdefault("messages", []).append({
            "role": "user",
            "content": raw,
            "timestamp": ts,
            "semantic_anchors": anchors
        })
        self._message_count += 1
        self._context_size_tokens += len(raw) // 2  # 简化token估算

        # 7. 检查技能触发（简化版，实际由52技能谱系处理）
        triggered_skills = self._detect_skills(raw, all_keywords)
        for skill in triggered_skills:
            self._current_context.setdefault("skills_triggered", []).append(skill)

        # 8. DNA记录
        record = self.tracer.create_record(
            context_id=self._current_topic_id,
            session_id=self._current_session_id,
            operation_type="INPUT_PROCESSED",
            state_after=self._current_state.value,
            trigger_reason="user_input",
            user_confirmed="无需确认",
            kg_nodes_related=len(matched) + len(expanded) if matched else 0,
            confidence_score=ctx_input.confidence_score
        )
        self.tracer.write_audit_log(record)

        return {
            "action": "processed",
            "state": self._current_state.value,
            "topic_id": self._current_topic_id,
            "kg_matched": len(matched) if matched else 0,
            "kg_expanded": len(expanded) if expanded else 0,
            "skills_triggered": triggered_skills,
            "context_health": health,
            "audit_color": AuditColor.GREEN.value,
            "timestamp": ts
        }

    def _check_explicit_commands(self, raw: str) -> Optional[Dict]:
        """检查用户明确指令"""
        lower = raw.lower().strip()

        # 切换指令
        for cmd in SWITCH_COMMANDS:
            if cmd in lower:
                # 提取新话题
                new_topic = raw.replace(cmd, "").strip() or "新话题"
                return self.switch_topic(new_topic, user_confirmed=True)

        # 结束指令
        for cmd in CLOSE_COMMANDS:
            if cmd in lower and len(lower) < 20:
                return self.close_session()

        # 返回指令
        for cmd in RETURN_COMMANDS:
            if cmd in lower:
                # 提取话题名
                topic = lower.replace(cmd, "").strip()
                return self.restore_topic(topic)

        return None

    def _check_context_health(self) -> Dict:
        """检查上下文健康状态"""
        blocked = self._context_size_tokens > THRESHOLD_CTX_BLOCK
        warning = self._context_size_tokens > THRESHOLD_CTX_WARNING
        return {
            "blocked": blocked,
            "warning": warning,
            "token_count": self._context_size_tokens,
            "message_count": self._message_count,
            "near_archive": self._message_count >= THRESHOLD_ROUNDS_ARCHIVE
        }

    @staticmethod
    def _detect_skills(raw: str, keywords: List[str]) -> List[Dict]:
        """检测可能触发的技能（简化版）"""
        skills_map = {
            "代码": {"skill_id": "dev_001", "name": "代码生成"},
            "编程": {"skill_id": "dev_001", "name": "代码生成"},
            "写": {"skill_id": "dev_002", "name": "文档撰写"},
            "分析": {"skill_id": "mgmt_001", "name": "数据分析"},
            "画": {"skill_id": "design_001", "name": "图像生成"},
            "搜索": {"skill_id": "research_001", "name": "信息检索"},
            "翻译": {"skill_id": "lang_001", "name": "多语言翻译"},
            "合规": {"skill_id": "legal_001", "name": "合规检查"},
        }
        triggered = []
        for kw, skill in skills_map.items():
            if kw in raw or kw in " ".join(keywords):
                triggered.append({
                    "skill_id": skill["skill_id"],
                    "skill_name": skill["name"],
                    "trigger_reason": f"关键词匹配: {kw}"
                })
        return triggered[:5]

    # ── 待机检测 ──

    def check_standby(self) -> Dict:
        """
        检查是否需要进入待机状态
        仅标记，不自动切换话题
        """
        if self._current_state != ContextState.ACTIVE:
            return {"action": "none", "state": self._current_state.value}

        # 检查是否30秒无操作
        if self._standby_since is None:
            return {"action": "none"}

        elapsed = time.time() - self._standby_since
        if elapsed >= STANDBY_TIMEOUT_SECONDS:
            self._current_state = ContextState.STANDBY
            # 知识图谱降温
            active_nodes = [n.node_id for n in self.kg.get_active_nodes()]
            self.kg.cooldown(active_nodes, elapsed)

            record = self.tracer.create_record(
                context_id=self._current_topic_id,
                session_id=self._current_session_id,
                operation_type="AUTO_STANDBY",
                state_before=ContextState.ACTIVE.value,
                state_after=ContextState.STANDBY.value,
                trigger_reason="30s_no_input",
                user_confirmed="无需确认"
            )
            self.tracer.write_audit_log(record)

            AuditEngine.log(AuditColor.GREEN.value,
                f"自动进入待机: {self._current_topic_id}")
            return {
                "action": "standby",
                "state": ContextState.STANDBY.value,
                "elapsed_seconds": elapsed,
                "dna_record": record.to_dict()
            }

        return {"action": "none", "elapsed": elapsed}

    def mark_activity(self):
        """标记用户活动（收到输入时调用）"""
        self._standby_since = time.time()

    # ── 压缩 ──

    def compress_context(self, level: CompressionLevel, topic_id: str = "") -> Dict:
        """
        手动触发压缩（MCP工具: longhun_ctx_compress）
        """
        tid = topic_id or self._current_topic_id
        if not tid:
            return {"error": "未指定话题ID", "audit_color": AuditColor.RED.value}

        compressed, report = self.compression.compress(
            self._current_context, level, tid, self._current_session_id
        )

        # 写入对应目录
        if level == CompressionLevel.L1:
            path = os.path.join(ARCHIVE_ACTIVE_DIR,
                f"ctx_{tid}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_L1.json")
        elif level == CompressionLevel.L2:
            path = os.path.join(ARCHIVE_CLOSED_DIR,
                f"session_{self._current_session_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_L2.json")
        else:
            path = os.path.join(MEMORY_DIR,
                f"memory_{datetime.now().strftime('%Y%m%d')}.json")

        with open(path, "w", encoding="utf-8") as f:
            json.dump(compressed, f, ensure_ascii=False, indent=2)

        record = self.tracer.create_record(
            context_id=tid,
            session_id=self._current_session_id,
            operation_type="COMPRESS",
            state_after=self._current_state.value,
            trigger_reason="manual",
            compression_level=level.value,
            compression_ratio=report.compression_ratio,
            confidence_score=85
        )
        self.tracer.write_audit_log(record)

        AuditEngine.log(AuditColor.GREEN.value,
            f"压缩完成 [{level.value}]: {report.compression_ratio} | 保存: {path}")

        return {
            "action": "compressed",
            "level": level.value,
            "topic_id": tid,
            "compression_ratio": report.compression_ratio,
            "saved_to": path,
            "audit_color": AuditColor.GREEN.value,
            "dna_record": record.to_dict()
        }

    # ── 恢复 ──

    def restore_topic(self, topic_id_or_title: str) -> Dict:
        """
        从归档恢复话题（MCP工具: longhun_ctx_restore）
        """
        ts = self.tracer.now()

        # 在归档目录中查找
        found = None
        for d in [ARCHIVE_ACTIVE_DIR, ARCHIVE_CLOSED_DIR]:
            if not os.path.exists(d):
                continue
            for fn in sorted(os.listdir(d), reverse=True):
                if topic_id_or_title in fn:
                    path = os.path.join(d, fn)
                    with open(path, "r", encoding="utf-8") as f:
                        found = json.load(f)
                    break
            if found:
                break

        if not found:
            return {
                "error": f"未找到话题: {topic_id_or_title}",
                "audit_color": AuditColor.RED.value
            }

        # 恢复上下文
        self._current_context = {
            "title": found.get("topic_title", topic_id_or_title),
            "topic_id": found.get("topic_id", topic_id_or_title),
            "restored_from": found.get("cnsh_header", ""),
            "timestamp_start": ts,
            "messages": [],
            "summary": found.get("summary", ""),
            "key_conclusions": found.get("key_conclusions", []),
            "pending_items": found.get("pending_items", []),
            "skills_triggered": found.get("skills_triggered", []),
            "kg_nodes_related": found.get("kg_nodes_related", [])
        }
        self._current_topic_id = found.get("topic_id", topic_id_or_title)
        self._current_state = ContextState.ACTIVE
        self._message_count = 0

        # 知识图谱升温
        kg_nodes = found.get("kg_nodes_related", [])
        if kg_nodes:
            self.kg.set_temperature(kg_nodes, 1.0)

        record = self.tracer.create_record(
            context_id=self._current_topic_id,
            session_id=self._current_session_id,
            operation_type="RESTORE",
            state_after=ContextState.ACTIVE.value,
            trigger_reason="user_request",
            compression_level=found.get("compression_level", "L1"),
            kg_nodes_related=len(kg_nodes),
            confidence_score=90
        )
        self.tracer.write_audit_log(record)

        AuditEngine.log(AuditColor.GREEN.value,
            f"上下文恢复: {self._current_context['title']}")

        return {
            "action": "restored",
            "topic_id": self._current_topic_id,
            "topic_title": self._current_context["title"],
            "compression_level": found.get("compression_level", "L1"),
            "kg_nodes": kg_nodes,
            "audit_color": AuditColor.GREEN.value,
            "dna_record": record.to_dict()
        }

    # ── 关闭会话 ──

    def close_session(self, user_confirmed: bool = False) -> Dict:
        """
        关闭当前会话
        执行L2+L3压缩，完整归档
        """
        ts = self.tracer.now()

        if not user_confirmed and self._message_count > 0:
            return {
                "action": "request_confirm",
                "message": "确认结束对话？讨论内容将完整归档。",
                "options": ["确认结束", "继续对话"],
                "audit_color": AuditColor.YELLOW.value
            }

        old_state = self._current_state
        topic_id = self._current_topic_id

        # L2压缩
        if self._current_context:
            l2_compressed, l2_report = self.compression.compress(
                self._current_context, CompressionLevel.L2, topic_id, self._current_session_id
            )
            l2_path = os.path.join(ARCHIVE_CLOSED_DIR,
                f"session_{self._current_session_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_L2.json")
            with open(l2_path, "w", encoding="utf-8") as f:
                json.dump(l2_compressed, f, ensure_ascii=False, indent=2)

        # L3压缩
        if self._current_context:
            l3_compressed, l3_report = self.compression.compress(
                self._current_context, CompressionLevel.L3, topic_id, self._current_session_id
            )
            l3_path = os.path.join(MEMORY_DIR,
                f"memory_{datetime.now().strftime('%Y%m%d')}.json")
            with open(l3_path, "w", encoding="utf-8") as f:
                json.dump(l3_compressed, f, ensure_ascii=False, indent=2)

        # 状态转换
        self._current_state = ContextState.CLOSED

        # DNA记录
        record = self.tracer.create_record(
            context_id=topic_id,
            session_id=self._current_session_id,
            operation_type="CLOSE",
            state_before=old_state.value,
            state_after=ContextState.CLOSED.value,
            trigger_reason="user_confirmed",
            user_confirmed="已确认",
            compression_level="L2+L3",
            compression_ratio=l2_report.compression_ratio if self._current_context else "N/A",
            kg_nodes_related=len(self.kg.get_active_nodes()),
            confidence_score=90
        )
        self._dna_records.append(record)
        self.tracer.write_audit_log(record)

        AuditEngine.log(AuditColor.GREEN.value,
            f"会话关闭: {self._current_session_id} | L2: {l2_report.compression_ratio if self._current_context else 'N/A'}")

        return {
            "action": "closed",
            "session_id": self._current_session_id,
            "topic_id": topic_id,
            "l2_saved": l2_path if self._current_context else None,
            "l3_saved": l3_path if self._current_context else None,
            "dna_record": record.to_dict(),
            "audit_color": AuditColor.GREEN.value,
            "timestamp": ts
        }

    # ── 审计日志查询 ──

    def get_audit_log(self, limit: int = 50) -> List[Dict]:
        """
        获取审计日志（MCP工具: longhun_ctx_audit）
        """
        try:
            if not os.path.exists(AUDIT_LOG):
                return []
            records = []
            with open(AUDIT_LOG, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        records.append(json.loads(line))
            return records[-limit:]
        except Exception as e:
            AuditEngine.log(AuditColor.RED.value, f"审计日志读取失败: {e}")
            return []

    # ── 列表查询 ──

    def list_contexts(self) -> List[Dict]:
        """列出所有归档的上下文"""
        contexts = []
        for d in [ARCHIVE_ACTIVE_DIR, ARCHIVE_CLOSED_DIR]:
            if not os.path.exists(d):
                continue
            for fn in sorted(os.listdir(d), reverse=True):
                if fn.endswith(".json"):
                    path = os.path.join(d, fn)
                    try:
                        with open(path, "r", encoding="utf-8") as f:
                            data = json.load(f)
                        contexts.append({
                            "file": fn,
                            "path": path,
                            "topic_id": data.get("topic_id", "unknown"),
                            "compression_level": data.get("compression_level", "unknown"),
                            "timestamp": data.get("timestamp_end", data.get("timestamp_closed", "unknown")),
                            "dna": data.get("dna", "")
                        })
                    except:
                        contexts.append({"file": fn, "path": path, "error": "无法解析"})
        return contexts


# ═══════════════════════════════════════════════════════════════
# 命令行接口
# ═══════════════════════════════════════════════════════════════

def main():
    """命令行入口"""
    import sys

    args = sys.argv[1:]
    if not args:
        print("""
龍魂认知上下文管理器 v3.0 —— 命令行接口

用法: python longhun-context-manager-v3.0.py <命令> [选项]

命令:
    status                    显示当前上下文状态
    list                      列出所有上下文历史
    switch <话题>             切换到指定话题
    compress <级别> [话题ID]  手动触发压缩 (L1/L2/L3)
    restore <话题ID>          从归档恢复上下文
    close                     关闭当前对话
    audit [数量]              显示最近审计日志
    kg-status                 显示知识图谱状态

选项:
    --force                   强制执行（跳过确认）
    --json                    JSON格式输出

示例:
    python longhun-context-manager-v3.0.py status
    python longhun-context-manager-v3.0.py switch "新话题"
    python longhun-context-manager-v3.0.py compress L1
    python longhun-context-manager-v3.0.py audit 20
        """)
        return

    cmd = args[0]
    manager = ContextManager()
    output_json = "--json" in args

    def output(data: Dict):
        if output_json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(f"\n{'='*60}")
            for k, v in data.items():
                print(f"  {k}: {v}")
            print(f"{'='*60}")

    try:
        if cmd == "status":
            result = manager.get_status()
            output(result)

        elif cmd == "list":
            contexts = manager.list_contexts()
            output({"total": len(contexts), "contexts": contexts[:20]})

        elif cmd == "switch" and len(args) >= 2:
            topic = " ".join(args[1:]).replace("--force", "").replace("--json", "").strip()
            result = manager.switch_topic(topic, user_confirmed="--force" in args)
            output(result)

        elif cmd == "compress" and len(args) >= 2:
            level_str = args[1].upper()
            topic = args[2] if len(args) > 2 else ""
            try:
                level = CompressionLevel(level_str)
            except ValueError:
                print(f"错误: 无效压缩级别 '{level_str}'。可选: L1, L2, L3")
                return
            result = manager.compress_context(level, topic)
            output(result)

        elif cmd == "restore" and len(args) >= 2:
            topic = args[1]
            result = manager.restore_topic(topic)
            output(result)

        elif cmd == "close":
            result = manager.close_session(user_confirmed="--force" in args)
            output(result)

        elif cmd == "audit":
            limit = int(args[1]) if len(args) > 1 else 50
            records = manager.get_audit_log(limit)
            output({"total_records": len(records), "records": records})

        elif cmd == "kg-status":
            active_nodes = manager.kg.get_active_nodes()
            output({
                "total_kg_nodes": len(manager.kg._nodes),
                "total_kg_edges": len(manager.kg._edges),
                "active_nodes": len(active_nodes),
                "nodes": [{"id": n.node_id, "name": n.name, "temp": round(n.temperature, 2)}
                         for n in active_nodes[:10]]
            })

        else:
            print(f"未知命令: {cmd}")
            print("使用 --help 查看帮助")

    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()


# ═══════════════════════════════════════════════════════════════
# 快捷命令封装（供shell脚本调用）
# ═══════════════════════════════════════════════════════════════

class ContextCLI:
    """
    ctx 快捷命令的Python实现
    等效于 shell 脚本: ~/.longhun/calendar-context-logger/bin/ctx
    """

    @staticmethod
    def status():
        """ctx status"""
        main_with_args(["status"])

    @staticmethod
    def list():
        """ctx list"""
        main_with_args(["list"])

    @staticmethod
    def switch(topic: str, force: bool = False):
        """ctx switch <topic>"""
        args = ["switch", topic]
        if force:
            args.append("--force")
        main_with_args(args)

    @staticmethod
    def compress(level: str, topic: str = ""):
        """ctx compress <L1|L2|L3> [topic]"""
        args = ["compress", level]
        if topic:
            args.append(topic)
        main_with_args(args)

    @staticmethod
    def restore(topic: str):
        """ctx restore <topic>"""
        main_with_args(["restore", topic])

    @staticmethod
    def close(force: bool = False):
        """ctx close"""
        args = ["close"]
        if force:
            args.append("--force")
        main_with_args(args)

    @staticmethod
    def audit(limit: int = 50):
        """ctx audit [limit]"""
        main_with_args(["audit", str(limit)])


def main_with_args(args: List[str]):
    """带参数的内部入口"""
    import sys
    old_argv = sys.argv
    sys.argv = [old_argv[0]] + args
    try:
        main()
    finally:
        sys.argv = old_argv


# ═══════════════════════════════════════════════════════════════
# 模块入口
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    main()
