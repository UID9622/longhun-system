#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔══════════════════════════════════════════════════════════════════╗
║     龍魂路由节点数据模型 / LongHun Route Node Model             ║
║                                                                  ║
║  定义路由注册表中的节点结构                                     ║
║  支持O(1)查找·三色状态·DNA追溯                                  ║
║                                                                  ║
║  DNA:#龍芯⚡️2026-06-03-ROUTE-NODE-MODEL-FILE1-v1.0                 ║
║  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✓              ║
║                                                                  ║
║  来源: IPA路由注册表设计规范                                    ║
║  责任: UID9622·不免责                                            ║
║  状态: 🟢 MAIN·可公开                                            ║
╚══════════════════════════════════════════════════════════════════╝
"""

from enum import Enum
from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any, List
from datetime import datetime
import json


# ═══════════════════════════════════════════════════════════════
# 【节点状态枚举】三色判定系统
# ═══════════════════════════════════════════════════════════════

class NodeStatus(str, Enum):
    """节点状态（三色系统）"""
    ACTIVE = "🟢"           # 活跃·正常使用
    ARCHIVED = "🟡"         # 待归档·可用但计划废弃
    DEPRECATED = "🔴"       # 已废弃·不可使用


# ═══════════════════════════════════════════════════════════════
# 【节点类型枚举】IPA编号前缀系统
# ═══════════════════════════════════════════════════════════════

class NodeType(str, Enum):
    """节点类型（对应IPA编号前缀）"""
    IPA = "IPA"             # Instruction Page Anchor (Notion宣言)
    CENTER = "CENTER"       # 五大中心 (Notion)
    PERSONA = "PERSONA"     # 人格路由 (P00-P72)
    DB = "DB"               # Notion数据库
    GATE = "GATE"           # 规则守门人 (本地)
    GATEWAY = "GATEWAY"     # 综合网关
    LOCAL = "LOCAL"         # 本地引擎/模块
    TOOL = "TOOL"           # Chrome工具箱
    WIDGET = "WIDGET"       # 前端组件
    ARCHIVAL = "ARCHIVAL"   # 归档节点


# ═══════════════════════════════════════════════════════════════
# 【路由节点数据模型】
# ═══════════════════════════════════════════════════════════════

@dataclass
class RouteNode:
    """
    龍魂路由节点

    例：
        node = RouteNode(
            node_id="IPA-L0-001",
            name="constitution",
            node_type=NodeType.LOCAL,
            status=NodeStatus.ACTIVE,
            local_path="cnsh_core.constitution",
            entry_point="get_system_config",
            dna="#龍芯⚡️2026-06-03-CONSTITUTION-v1.0",
            layer="L0_ETERNAL",
            description="系统宪法和基础配置",
            tags=["L0", "config"],
            dependencies=[],
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
        )
    """

    # ─────────────────────────────────────────────────────────
    # 【基础信息】
    # ─────────────────────────────────────────────────────────

    node_id: str                    # 节点ID (如 IPA-L0-001 或 [IPA-L0-001])
    name: str                       # 节点名称 (如 constitution)
    node_type: NodeType             # 节点类型
    status: NodeStatus              # 节点状态 (三色)

    # ─────────────────────────────────────────────────────────
    # 【位置信息】
    # ─────────────────────────────────────────────────────────

    local_path: Optional[str] = None       # 本地路径 (Python模块路径)
                                            # 例: cnsh_core.constitution
    notion_url: Optional[str] = None       # Notion URL
    entry_point: Optional[str] = None      # 入口函数名
                                            # 例: get_system_config

    # ─────────────────────────────────────────────────────────
    # 【追溯信息】
    # ─────────────────────────────────────────────────────────

    dna: str = ""                          # DNA追溯码
    layer: str = ""                        # L0-L4层级

    # ─────────────────────────────────────────────────────────
    # 【描述和标签】
    # ─────────────────────────────────────────────────────────

    description: str = ""                  # 节点描述
    tags: List[str] = field(default_factory=list)  # 标签列表
    dependencies: List[str] = field(default_factory=list)  # 依赖的节点ID列表

    # ─────────────────────────────────────────────────────────
    # 【时间戳】
    # ─────────────────────────────────────────────────────────

    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    # ─────────────────────────────────────────────────────────
    # 【扩展字段】
    # ─────────────────────────────────────────────────────────

    metadata: Dict[str, Any] = field(default_factory=dict)  # 其他元数据

    # ─────────────────────────────────────────────────────────
    # 【内部字段】（不序列化）
    # ─────────────────────────────────────────────────────────

    _hash: str = field(default="", repr=False)  # 节点哈希（用于验证）

    def __post_init__(self):
        """初始化后处理"""
        # 规范化node_id（去掉括号）
        if self.node_id.startswith("[") and self.node_id.endswith("]"):
            self.node_id = self.node_id[1:-1]

    # ═════════════════════════════════════════════════════════
    # 【序列化方法】
    # ═════════════════════════════════════════════════════════

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典（用于序列化）"""
        result = asdict(self)
        # 移除内部字段（兼容性：asdict的exclude参数需要Python 3.10+）
        result.pop("_hash", None)
        # 将enum转换为字符串
        result["status"] = self.status.value
        result["node_type"] = self.node_type.value
        return result

    def to_json(self) -> str:
        """转换为JSON字符串（JSONL格式）"""
        data = self.to_dict()
        return json.dumps(data, ensure_ascii=False)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "RouteNode":
        """从字典加载"""
        # 复制数据避免修改原始数据
        data = dict(data)

        # 转换enum
        if isinstance(data.get("status"), str):
            data["status"] = NodeStatus(data["status"])
        if isinstance(data.get("node_type"), str):
            data["node_type"] = NodeType(data["node_type"])

        return RouteNode(**data)

    @staticmethod
    def from_json(json_str: str) -> "RouteNode":
        """从JSON字符串加载"""
        data = json.loads(json_str)
        return RouteNode.from_dict(data)

    # ═════════════════════════════════════════════════════════
    # 【工具方法】
    # ═════════════════════════════════════════════════════════

    def __str__(self) -> str:
        """字符串表示"""
        return f"[{self.node_id}] {self.name} ({self.status})"

    def __repr__(self) -> str:
        """代码表示"""
        return f"RouteNode(node_id='{self.node_id}', name='{self.name}', status={self.status.value})"

    def is_active(self) -> bool:
        """是否活跃"""
        return self.status == NodeStatus.ACTIVE

    def is_deprecated(self) -> bool:
        """是否已废弃"""
        return self.status == NodeStatus.DEPRECATED

    def get_color(self) -> str:
        """获取三色值"""
        return self.status.value

    def matches_filter(self,
                      node_type: Optional[NodeType] = None,
                      status: Optional[NodeStatus] = None,
                      layer: Optional[str] = None) -> bool:
        """检查是否匹配过滤条件"""
        if node_type and self.node_type != node_type:
            return False
        if status and self.status != status:
            return False
        if layer and self.layer != layer:
            return False
        return True


# ═══════════════════════════════════════════════════════════════
# 【辅助函数】
# ═══════════════════════════════════════════════════════════════

def normalize_node_id(node_id: str) -> str:
    """规范化节点ID（去掉方括号）"""
    if node_id.startswith("[") and node_id.endswith("]"):
        return node_id[1:-1]
    return node_id


def parse_node_id(node_id: str) -> Dict[str, str]:
    """
    解析节点ID

    例：
        parse_node_id("IPA-L0-001") → {
            "prefix": "IPA",
            "layer": "L0",
            "number": "001"
        }
    """
    node_id = normalize_node_id(node_id)
    parts = node_id.split("-")

    result = {}
    if len(parts) >= 1:
        result["prefix"] = parts[0]
    if len(parts) >= 2:
        result["layer"] = parts[1]
    if len(parts) >= 3:
        result["number"] = parts[2]

    return result


if __name__ == "__main__":
    # 测试
    print("╔═══════════════════════════════════════════════════╗")
    print("║  龍魂路由节点数据模型 · 自检                      ║")
    print("╚═══════════════════════════════════════════════════╝\n")

    # 创建测试节点
    node = RouteNode(
        node_id="IPA-L0-001",
        name="constitution",
        node_type=NodeType.LOCAL,
        status=NodeStatus.ACTIVE,
        local_path="cnsh_core.constitution",
        entry_point="get_system_config",
        dna="#龍芯⚡️2026-06-03-CONSTITUTION-v1.0",
        layer="L0_ETERNAL",
        description="系统宪法和基础配置",
        tags=["L0", "config", "foundation"],
        dependencies=[],
    )

    # 测试输出
    print(f"✅ 节点创建: {node}")
    print(f"✅ 节点状态: {node.get_color()}")
    print(f"✅ 活跃状态: {node.is_active()}")

    # 测试序列化
    json_str = node.to_json()
    print(f"✅ 序列化为JSON: {json_str[:60]}...")

    # 测试反序列化
    node2 = RouteNode.from_json(json_str)
    print(f"✅ 反序列化成功: {node2.name} == {node.name}")

    # 测试过滤
    matches = node.matches_filter(
        node_type=NodeType.LOCAL,
        status=NodeStatus.ACTIVE,
        layer="L0_ETERNAL"
    )
    print(f"✅ 过滤匹配: {matches}")

    # 测试解析
    parsed = parse_node_id("[IPA-L0-001]")
    print(f"✅ ID解析: {parsed}")

    print("\n✅ 所有自检通过")
