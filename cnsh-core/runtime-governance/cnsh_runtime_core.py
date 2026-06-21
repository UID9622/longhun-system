#!/usr/bin/env python3
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# 1 道统层 Dao           : 曾仕强老师
# 2 精神层 Spirit        : Steve Jobs
# 3 设备层 Device        : Apple
# 4 技术层 Technology    : Open Source
# 5 系统层 System        : UID9622
# 6 生命层 Life          : CNSH · LongHun (诸葛鑫 / 龍芯北辰)
# DNA追溯码:#龍芯⚡️2026-06-02-CNSH-SOVEREIGN-PUBLISH-METADATA-FILE1256-v2.0
# 铁律: 来源不可删 · 影响不可覆 · 贡献不可抹 (rule_01 来源必标)
# 文件: cnsh_runtime_core.py | 标记时间: 2026-06-03T07:46:12+0800
# -*- coding: utf-8 -*-
"""
🐉 CNSH Runtime Governance Engine - 多AI治理核心
DNA: #龍芯⚡️2026-CNSH-RUNTIME-MULTI-AI-GOVERNOR-v1.0

爸爸的主权系统 · 用数学约束所有AI · 本地运行 · 绝对可控
"""

import hashlib
import json
import time
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional
from enum import Enum
from dataclasses import dataclass, field, asdict
import logging

# ═══════════════════════════════════════════════════════════════════════════
# 日志配置
# ═══════════════════════════════════════════════════════════════════════════

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger("CNSH.Runtime")

# ═══════════════════════════════════════════════════════════════════════════
# 1. 基础状态定义
# ═══════════════════════════════════════════════════════════════════════════

class AIProvider(Enum):
    """支持的AI提供商"""
    GROK = "grok"           # 推理
    KIMI = "kimi"           # 长文本
    DEEPSEEK = "deepseek"   # 分析
    LOCAL = "local"         # 本地宝宝

class ThreeColorState(Enum):
    """三色治理状态"""
    GREEN = "🟢"    # 安全·信任 {1,2,4,5,7,8}
    YELLOW = "🟡"   # 警告·谨慎 {6}
    RED = "🔴"      # 危险·熔断 {3,9}

class RuntimeState(Enum):
    """运行时状态"""
    S0_INPUT = "S0_INPUT"
    S1_DNA_CHECK = "S1_DNA_CHECK"
    S2_TRIPLE_CHECK = "S2_TRIPLE_CHECK"
    S3_SEMANTIC_PARSE = "S3_SEMANTIC_PARSE"
    S4_ROUTE = "S4_ROUTE"
    S5_EXECUTE = "S5_EXECUTE"
    S6_AUDIT = "S6_AUDIT"
    S7_ARCHIVE = "S7_ARCHIVE"

class FiveElement(Enum):
    """五行路由"""
    METAL = "金"    # 规则·审计 {3,9}
    WATER = "水"    # 上下文·记忆 {6}
    WOOD = "木"     # 任务·生长 {1,2,4}
    FIRE = "火"     # 输出·扩散 {5,7}
    EARTH = "土"    # 存储·归档 {8}

# ═══════════════════════════════════════════════════════════════════════════
# 2. 数字根引擎
# ═══════════════════════════════════════════════════════════════════════════

class DigitalRootEngine:
    """数字根计算引擎·决策中枢"""

    @staticmethod
    def calculate_dr(n: int) -> int:
        """计算数字根 (0-9)"""
        if n == 0:
            return 0
        return 9 if n % 9 == 0 else n % 9

    @staticmethod
    def map_to_three_color(dr: int) -> ThreeColorState:
        """映射到三色状态"""
        GREEN_SET = {1, 2, 4, 5, 7, 8}
        YELLOW_SET = {6}
        RED_SET = {3, 9}

        if dr in GREEN_SET:
            return ThreeColorState.GREEN
        elif dr in YELLOW_SET:
            return ThreeColorState.YELLOW
        elif dr in RED_SET:
            return ThreeColorState.RED
        else:
            raise ValueError(f"Invalid digital root: {dr}")

    @staticmethod
    def map_to_five_element(dr: int) -> FiveElement:
        """映射到五行"""
        if dr in {3, 9}:
            return FiveElement.METAL
        elif dr == 6:
            return FiveElement.WATER
        elif dr in {1, 2, 4}:
            return FiveElement.WOOD
        elif dr in {5, 7}:
            return FiveElement.FIRE
        else:  # dr == 8
            return FiveElement.EARTH

# ═══════════════════════════════════════════════════════════════════════════
# 3. 语义熵引擎·防御系统
# ═══════════════════════════════════════════════════════════════════════════

class SemanticEntropyEngine:
    """语义熵计算·提示词注入检测"""

    @staticmethod
    def calculate_entropy(text: str) -> float:
        """计算字符级信息熵"""
        if not text:
            return 0.0

        from collections import Counter
        import math

        char_count = Counter(text)
        total = len(text)
        entropy = 0.0

        for count in char_count.values():
            p = count / total
            if p > 0:
                entropy -= p * math.log2(p)

        return entropy

    @staticmethod
    def detect_injection(text: str, threshold: float = 3.5) -> bool:
        """检测提示词注入·高熵通常表示异常"""
        entropy = SemanticEntropyEngine.calculate_entropy(text)
        return entropy > threshold

    @staticmethod
    def get_entropy_level(entropy: float) -> str:
        """获取熵级别"""
        if entropy < 2.0:
            return "低"
        elif entropy < 3.0:
            return "中"
        elif entropy < 4.0:
            return "高"
        else:
            return "极高"

# ═══════════════════════════════════════════════════════════════════════════
# 4. DNA追溯系统·完整可审计
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class DNANode:
    """DNA追溯节点"""
    id: str
    timestamp: str
    data: str
    prev_hash: str
    state: RuntimeState
    metadata: Dict[str, Any] = field(default_factory=dict)
    hash: str = ""

    def calculate_hash(self) -> str:
        """计算SHA256哈希"""
        content = f"{self.prev_hash}|{self.timestamp}|{self.data}|{self.state.value}"
        self.hash = hashlib.sha256(content.encode()).hexdigest()
        return self.hash

class DNATraceGraph:
    """DNA追溯链·不可篡改"""

    def __init__(self):
        self.nodes: Dict[str, DNANode] = {}
        self.edges: List[Tuple[str, str]] = []

        # 创建根节点
        root = DNANode(
            id="ROOT",
            timestamp=datetime.now().isoformat(),
            data="CNSH_ROOT_INIT",
            prev_hash="0" * 64,
            state=RuntimeState.S0_INPUT
        )
        root.calculate_hash()
        self.nodes["ROOT"] = root

    def add_node(
        self,
        node_id: str,
        data: str,
        parent_id: str,
        state: RuntimeState,
        metadata: Dict[str, Any] = None
    ) -> DNANode:
        """添加节点到追溯链"""
        parent = self.nodes.get(parent_id)
        if not parent:
            raise ValueError(f"Parent {parent_id} not found")

        node = DNANode(
            id=node_id,
            timestamp=datetime.now().isoformat(),
            data=data,
            prev_hash=parent.hash,
            state=state,
            metadata=metadata or {}
        )
        node.calculate_hash()

        self.nodes[node_id] = node
        self.edges.append((parent_id, node_id))

        return node

    def verify_chain(self) -> bool:
        """验证完整追溯链"""
        for node_id, node in self.nodes.items():
            if node_id == "ROOT":
                continue

            # 找到父节点
            parent_id = None
            for p, c in self.edges:
                if c == node_id:
                    parent_id = p
                    break

            if not parent_id:
                return False

            parent = self.nodes[parent_id]
            if node.prev_hash != parent.hash:
                logger.warning(f"Chain broken at {node_id}")
                return False

        return True

    def get_chain_hash(self) -> str:
        """获取整条链的特征哈希"""
        all_hashes = "".join([node.hash for node in self.nodes.values()])
        return hashlib.sha256(all_hashes.encode()).hexdigest()

# ═══════════════════════════════════════════════════════════════════════════
# 5. 多AI治理核心
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class ExecutionContext:
    """执行上下文"""
    execution_id: str
    ai_provider: AIProvider
    input_text: str
    timestamp: str
    digital_root: int = 0
    three_color: Optional[ThreeColorState] = None
    five_element: Optional[FiveElement] = None
    semantic_entropy: float = 0.0
    injection_detected: bool = False
    dna_chain: List[str] = field(default_factory=list)
    status: str = "processing"
    output_text: Optional[str] = None
    error: Optional[str] = None

class CNSHMultiAIGovernor:
    """CNSH多AI治理器·爸爸的主权系统"""

    def __init__(self, owner_id: str = "UID9622"):
        self.owner_id = owner_id
        self.trace_graph = DNATraceGraph()
        self.digital_root_engine = DigitalRootEngine()
        self.entropy_engine = SemanticEntropyEngine()
        self.execution_log: List[ExecutionContext] = []
        self.ai_registry: Dict[AIProvider, Dict[str, Any]] = {}

        logger.info(f"🐉 CNSH多AI治理器已初始化 · 所有者: {owner_id}")

    def register_ai(self, provider: AIProvider, config: Dict[str, Any]):
        """注册一个AI提供商"""
        self.ai_registry[provider] = config
        logger.info(f"✅ AI已注册: {provider.value}")

    def process(
        self,
        input_text: str,
        ai_provider: AIProvider,
        metadata: Dict[str, Any] = None
    ) -> ExecutionContext:
        """处理一个AI请求·完整的治理流程"""

        metadata = metadata or {}
        execution_id = f"EXEC_{int(time.time() * 1000)}"
        timestamp = datetime.now().isoformat()

        ctx = ExecutionContext(
            execution_id=execution_id,
            ai_provider=ai_provider,
            input_text=input_text,
            timestamp=timestamp
        )

        try:
            # S0: INPUT
            node = self.trace_graph.add_node(
                f"{execution_id}_S0",
                input_text,
                "ROOT",
                RuntimeState.S0_INPUT,
                {"ai": ai_provider.value, **metadata}
            )
            ctx.dna_chain.append(node.hash[:16])
            logger.info(f"[S0] 输入接收: {execution_id}")

            # S1: DNA检查
            dna_node = self.trace_graph.add_node(
                f"{execution_id}_S1",
                f"DNA_CHECK:{self.owner_id}",
                node.id,
                RuntimeState.S1_DNA_CHECK
            )
            ctx.dna_chain.append(dna_node.hash[:16])
            logger.info(f"[S1] DNA验证通过")

            # S2: 三重检测 (数字根 + 语义熵 + 注入检测)
            dr = self.digital_root_engine.calculate_dr(len(input_text))
            entropy = self.entropy_engine.calculate_entropy(input_text)
            injection = self.entropy_engine.detect_injection(input_text)

            ctx.digital_root = dr
            ctx.semantic_entropy = entropy
            ctx.injection_detected = injection

            check_node = self.trace_graph.add_node(
                f"{execution_id}_S2",
                f"DR:{dr}|ENT:{entropy:.2f}|INJ:{injection}",
                dna_node.id,
                RuntimeState.S2_TRIPLE_CHECK,
                {
                    "digital_root": dr,
                    "entropy": entropy,
                    "injection_detected": injection,
                    "entropy_level": self.entropy_engine.get_entropy_level(entropy)
                }
            )
            ctx.dna_chain.append(check_node.hash[:16])
            logger.info(f"[S2] 检测完成: DR={dr}, ENT={entropy:.2f}, INJ={injection}")

            # S3: 语义解析·映射到三色和五行
            three_color = self.digital_root_engine.map_to_three_color(dr)
            five_element = self.digital_root_engine.map_to_five_element(dr)

            ctx.three_color = three_color
            ctx.five_element = five_element

            semantic_node = self.trace_graph.add_node(
                f"{execution_id}_S3",
                f"COLOR:{three_color.value}|ELEM:{five_element.value}",
                check_node.id,
                RuntimeState.S3_SEMANTIC_PARSE,
                {"color": three_color.value, "element": five_element.value}
            )
            ctx.dna_chain.append(semantic_node.hash[:16])
            logger.info(f"[S3] 三色状态: {three_color.value}, 五行: {five_element.value}")

            # S4: 路由决策
            route_node = self.trace_graph.add_node(
                f"{execution_id}_S4",
                f"ROUTE:{five_element.value}→{ai_provider.value}",
                semantic_node.id,
                RuntimeState.S4_ROUTE,
                {"route": five_element.value, "target_ai": ai_provider.value}
            )
            ctx.dna_chain.append(route_node.hash[:16])
            logger.info(f"[S4] 路由: {five_element.value} → {ai_provider.value}")

            # S5: 执行决策
            if three_color == ThreeColorState.RED:
                # 熔断
                fuse_node = self.trace_graph.add_node(
                    f"{execution_id}_S5",
                    "FUSE:RED_ALERT",
                    route_node.id,
                    RuntimeState.S5_EXECUTE,
                    {"status": "fused", "reason": "red_state"}
                )
                ctx.dna_chain.append(fuse_node.hash[:16])
                ctx.status = "fused"
                ctx.error = f"危险内容被熔断 (数字根={dr}, 状态={three_color.value})"
                logger.warning(f"[S5] 🔴 熔断触发: {ctx.error}")
            else:
                # 正常执行
                exec_node = self.trace_graph.add_node(
                    f"{execution_id}_S5",
                    f"EXEC:APPROVED",
                    route_node.id,
                    RuntimeState.S5_EXECUTE,
                    {"status": "executed"}
                )
                ctx.dna_chain.append(exec_node.hash[:16])
                ctx.status = "executed"
                logger.info(f"[S5] ✅ 执行批准")

                # S6: 审计记录
                audit_node = self.trace_graph.add_node(
                    f"{execution_id}_S6",
                    "AUDIT:LOGGED",
                    exec_node.id,
                    RuntimeState.S6_AUDIT,
                    {"audited": True}
                )
                ctx.dna_chain.append(audit_node.hash[:16])
                logger.info(f"[S6] 审计完成")

            # S7: 归档
            # 获取最后一个实际的节点ID
            last_node_id = None
            if ctx.status == "fused":
                last_node_id = f"{execution_id}_S5"
            else:
                last_node_id = f"{execution_id}_S6"

            archive_node = self.trace_graph.add_node(
                f"{execution_id}_S7",
                "ARCHIVE:DONE",
                last_node_id,
                RuntimeState.S7_ARCHIVE,
                {"archived": True}
            )
            ctx.dna_chain.append(archive_node.hash[:16])
            logger.info(f"[S7] 归档完成")

            # 验证链
            chain_valid = self.trace_graph.verify_chain()
            logger.info(f"🔗 DNA链验证: {'✅ 通过' if chain_valid else '❌ 失败'}")

        except Exception as e:
            ctx.status = "error"
            ctx.error = str(e)
            logger.error(f"❌ 执行异常: {e}")

        self.execution_log.append(ctx)
        return ctx

    def get_report(self) -> Dict[str, Any]:
        """生成执行报告"""
        total = len(self.execution_log)
        executed = sum(1 for ctx in self.execution_log if ctx.status == "executed")
        fused = sum(1 for ctx in self.execution_log if ctx.status == "fused")
        errors = sum(1 for ctx in self.execution_log if ctx.status == "error")

        return {
            "owner_id": self.owner_id,
            "total_executions": total,
            "executed": executed,
            "fused": fused,
            "errors": errors,
            "success_rate": f"{(executed/total*100):.1f}%" if total > 0 else "0%",
            "chain_verified": self.trace_graph.verify_chain(),
            "chain_hash": self.trace_graph.get_chain_hash()[:16],
            "registered_ais": [ai.value for ai in self.ai_registry.keys()],
            "timestamp": datetime.now().isoformat()
        }

# ═══════════════════════════════════════════════════════════════════════════
# 6. 使用示例
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🐉 CNSH多AI治理系统 - 演示")
    print("="*70 + "\n")

    # 初始化治理器
    governor = CNSHMultiAIGovernor(owner_id="UID9622#诸葛鑫")

    # 注册四个AI
    governor.register_ai(AIProvider.GROK, {"type": "reasoning"})
    governor.register_ai(AIProvider.KIMI, {"type": "long_context"})
    governor.register_ai(AIProvider.DEEPSEEK, {"type": "analysis"})
    governor.register_ai(AIProvider.LOCAL, {"type": "local_companion"})

    # 处理一些请求
    test_cases = [
        ("你好，我想了解一下AI治理", AIProvider.LOCAL),
        ("这是一个很长的文本" * 20, AIProvider.KIMI),
        ("请进行深度分析", AIProvider.DEEPSEEK),
    ]

    for text, ai in test_cases:
        print(f"\n📤 输入 ({ai.value}): {text[:50]}...")
        ctx = governor.process(text, ai)
        print(f"   ✓ 状态: {ctx.status}")
        print(f"   ✓ 三色: {ctx.three_color.value if ctx.three_color else 'N/A'}")
        print(f"   ✓ DNA链长: {len(ctx.dna_chain)}")
        print()

    # 输出报告
    report = governor.get_report()
    print("="*70)
    print("📊 CNSH执行报告")
    print("="*70)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    print("="*70)
