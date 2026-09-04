#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔══════════════════════════════════════════════════════════════════╗
║     龍魂路由注册表 · 包初始化 / LongHun Route Registry Init      ║
║                                                                  ║
║  导出路由系统的公共接口                                         ║
║  O(1)查找·三色状态·DNA追溯                                      ║
║                                                                  ║
║  DNA:#龍芯⚡️2026-06-03-ROUTE-REGISTRY-INIT-FILE1-v1.0              ║
║  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✓              ║
║                                                                  ║
║  来源: IPA路由注册表架构规范                                    ║
║  责任: UID9622·不免责                                            ║
║  状态: 🟢 MAIN·可公开                                            ║
╚══════════════════════════════════════════════════════════════════╝
"""

from typing import List, Optional, Tuple, Any

from .node import RouteNode, NodeStatus, NodeType, normalize_node_id, parse_node_id
from .route_registry import RouteRegistry, get_route_registry


# ═══════════════════════════════════════════════════════════════
# 【便捷函数】遵循P0模块风格
# ═══════════════════════════════════════════════════════════════

def find_route(node_id: str) -> Optional[RouteNode]:
    """
    快速查找路由节点

    Args:
        node_id: 节点ID，如 "IPA-L0-001" 或 "[IPA-L0-001]"

    Returns:
        RouteNode 或 None
    """
    return get_route_registry().find(node_id)


def register_route(node: RouteNode) -> Tuple[bool, str]:
    """
    注册新路由节点

    Args:
        node: 路由节点

    Returns:
        (success, message)
    """
    return get_route_registry().register(node)


def list_routes(
    node_type: Optional[NodeType] = None,
    status: Optional[NodeStatus] = None,
    layer: Optional[str] = None,
) -> List[RouteNode]:
    """
    列出路由节点（支持过滤）

    Args:
        node_type: 按类型过滤
        status: 按状态过滤
        layer: 按层级过滤 (L0/L1/L2/L3/L4)

    Returns:
        匹配的节点列表
    """
    return get_route_registry().list_nodes(node_type, status, layer)


def check_route_health(node_id: str) -> dict[str, Any]:
    """
    检查路由节点健康度

    Args:
        node_id: 节点ID

    Returns:
        健康检查结果字典
    """
    return get_route_registry().check_health(node_id)


def get_route_statistics() -> dict[str, Any]:
    """
    获取路由统计信息

    Returns:
        统计信息字典
    """
    return get_route_registry().get_statistics()


def selftest_registry() -> Tuple[bool, List[str]]:
    """
    自检路由注册表

    Returns:
        (all_pass, error_messages)
    """
    return get_route_registry().selftest()


# ═══════════════════════════════════════════════════════════════
# 【导出清单】
# ═══════════════════════════════════════════════════════════════

__all__ = [
    # 数据模型
    "RouteNode",
    "NodeStatus",
    "NodeType",
    # 核心系统
    "RouteRegistry",
    "get_route_registry",
    # 便捷函数
    "find_route",
    "register_route",
    "list_routes",
    "check_route_health",
    "get_route_statistics",
    "selftest_registry",
    # 工具函数
    "normalize_node_id",
    "parse_node_id",
]
