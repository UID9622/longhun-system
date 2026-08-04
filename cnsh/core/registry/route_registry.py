#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-

"""
╔══════════════════════════════════════════════════════════════════╗
║     龍魂路由注册表 / LongHun Route Registry                      ║
║                                                                  ║
║  中央路由注册表实现                                             ║
║  O(1)查找·三色状态·DNA追溯·append-only持久化                   ║
║                                                                  ║
║  DNA:#龍芯⚡️2026-06-03-ROUTE-REGISTRY-FILE1-v1.0                   ║
║  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✓              ║
║                                                                  ║
║  来源: IPA路由注册表架构规范                                    ║
║  责任: UID9622·不免责                                            ║
║  状态: 🟢 MAIN·可公开                                            ║
╚══════════════════════════════════════════════════════════════════╝
"""

import os
import json
import importlib
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
from pathlib import Path

from .node import RouteNode, NodeStatus, NodeType, normalize_node_id

# 日志集成（可选）
try:
    from longhun_logging.append_only_logging import log_operation, LogEventType
    HAS_LOGGING = True
except ImportError:
    HAS_LOGGING = False

# 人民主权守护集成
try:
    from ..dna_sovereignty_kernel import PeopleSovereigntyGuard
    HAS_DNA_KERNEL = True
except ImportError:
    try:
        import sys, os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from dna_sovereignty_kernel import PeopleSovereigntyGuard
        HAS_DNA_KERNEL = True
    except ImportError:
        HAS_DNA_KERNEL = False

# 人民权益守门人集成
try:
    from ..people_rights_guard import PeopleRightsGuard
    HAS_RIGHTS_GUARD = True
except ImportError:
    try:
        import sys, os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from people_rights_guard import PeopleRightsGuard
        HAS_RIGHTS_GUARD = True
    except ImportError:
        HAS_RIGHTS_GUARD = False


# ═══════════════════════════════════════════════════════════════
# 【路由注册表】
# ═══════════════════════════════════════════════════════════════

class RouteRegistry:
    """
    龍魂中央路由注册表

    特性:
    - O(1)节点查找（基于内存字典）
    - 三色状态管理（活跃/待归档/废弃）
    - DNA追溯码绑定
    - Append-only持久化（JSONL格式）
    - 完整的健康检查和验证
    """

    def __init__(self, registry_file: str | None = None):
        """
        初始化注册表

        Args:
            registry_file: 注册表文件路径（JSONL格式）
                          默认: ~/longhun-system/01_protocols/IPA-ROUTE-REGISTRY.local.md
        """
        self.registry_file = registry_file or self._default_registry_path()
        self.nodes: Dict[str, RouteNode] = {}
        self._load_registry()

    @staticmethod
    def _default_registry_path() -> str:
        """获取默认注册表路径"""
        home = os.path.expanduser("~")
        return os.path.join(
            home,
            "longhun-system",
            "01_protocols",
            "IPA-ROUTE-REGISTRY.local.md"
        )

    # ═════════════════════════════════════════════════════════
    # 【核心操作】
    # ═════════════════════════════════════════════════════════

    def register(self, node: RouteNode) -> Tuple[bool, str]:
        """
        注册新节点

        Args:
            node: 路由节点

        Returns:
            (success, message)
        """
        # 规范化node_id
        node_id = normalize_node_id(node.node_id)
        node.node_id = node_id

        # 检查重复
        if node_id in self.nodes:
            msg = f"节点已存在: {node_id}"
            if HAS_LOGGING:
                try:
                    log_operation(
                        event_type=LogEventType.CONFIG_CHANGED,
                        message=f"路由注册失败: {msg}",
                        context={"node_id": node_id, "reason": "duplicate"}
                    )
                except Exception:
                    pass
            return False, msg

        # 检查依赖存在
        for dep_id in node.dependencies:
            if normalize_node_id(dep_id) not in self.nodes:
                msg = f"依赖节点不存在: {dep_id}"
                if HAS_LOGGING:
                    try:
                        log_operation(
                            event_type=LogEventType.CONFIG_CHANGED,
                            message=f"路由注册失败: {msg}",
                            context={"node_id": node_id, "missing_dependency": dep_id}
                        )
                    except Exception:
                        pass
                return False, msg

        # 保存到内存
        self.nodes[node_id] = node

        # 保存到文件
        if not self._append_to_file(node):
            # 如果保存失败，从内存中删除
            del self.nodes[node_id]
            msg = "保存到文件失败"
            if HAS_LOGGING:
                try:
                    log_operation(
                        event_type=LogEventType.SYSTEM_ERROR,
                        message=f"路由注册失败: {msg}",
                        context={"node_id": node_id, "reason": "file_write_error"}
                    )
                except Exception:
                    pass
            return False, msg

        # 成功注册，记录日志
        msg = f"节点注册成功: {node_id}"
        if HAS_LOGGING:
            try:
                log_operation(
                    event_type=LogEventType.CONFIG_CHANGED,
                    message=f"注册新节点: {node_id}",
                    context={
                        "node_id": node_id,
                        "node_type": node.node_type.value,
                        "status": node.status.value,
                        "layer": node.layer,
                    }
                )
            except Exception:
                pass

        return True, msg

    def find(self, node_id: str) -> Optional[RouteNode]:
        """
        查找节点 O(1)

        Args:
            node_id: 节点ID (如 "IPA-L0-001" 或 "[IPA-L0-001]")

        Returns:
            RouteNode 或 None
        """
        node_id = normalize_node_id(node_id)
        return self.nodes.get(node_id)

    def update_status(self, node_id: str, new_status: NodeStatus) -> Tuple[bool, str]:
        """
        更新节点状态

        Args:
            node_id: 节点ID
            new_status: 新状态

        Returns:
            (success, message)
        """
        node_id = normalize_node_id(node_id)
        node = self.nodes.get(node_id)

        if not node:
            msg = f"节点不存在: {node_id}"
            if HAS_LOGGING:
                try:
                    log_operation(
                        event_type=LogEventType.CONFIG_CHANGED,
                        message=f"状态更新失败: {msg}",
                        context={"node_id": node_id}
                    )
                except Exception:
                    pass
            return False, msg

        old_status = node.status
        node.status = new_status
        node.updated_at = datetime.now().isoformat()

        # 保存更新
        if not self._save_registry():
            node.status = old_status
            msg = "保存更新失败"
            if HAS_LOGGING:
                try:
                    log_operation(
                        event_type=LogEventType.SYSTEM_ERROR,
                        message=f"状态更新失败: {msg}",
                        context={"node_id": node_id, "reason": "file_write_error"}
                    )
                except Exception:
                    pass
            return False, msg

        # 成功更新，记录日志
        msg = f"状态更新成功: {old_status} → {new_status}"
        if HAS_LOGGING:
            try:
                log_operation(
                    event_type=LogEventType.CONFIG_CHANGED,
                    message=f"节点状态更新: {node_id}",
                    context={
                        "node_id": node_id,
                        "old_status": old_status.value,
                        "new_status": new_status.value,
                    }
                )
            except Exception:
                pass

        return True, msg

    def list_nodes(self,
                   node_type: Optional[NodeType] = None,
                   status: Optional[NodeStatus] = None,
                   layer: Optional[str] = None) -> List[RouteNode]:
        """
        列出节点（支持过滤）

        Args:
            node_type: 按类型过滤
            status: 按状态过滤
            layer: 按层级过滤 (L0/L1/L2/L3/L4)

        Returns:
            匹配的节点列表
        """
        results = []

        for node in self.nodes.values():
            if node.matches_filter(node_type, status, layer):
                results.append(node)

        # 按ID排序
        return sorted(results, key=lambda n: n.node_id)

    def check_health(self, node_id: str) -> Dict[str, Any]:
        """
        检查节点健康度

        Args:
            node_id: 节点ID

        Returns:
            {
                "node_id": str,
                "status": NodeStatus,
                "color": str,
                "reachable": bool,
                "last_checked": str,
                "issues": List[str],
            }
        """
        node_id = normalize_node_id(node_id)
        node = self.nodes.get(node_id)

        if not node:
            return {
                "node_id": node_id,
                "status": "unknown",
                "color": "🔴",
                "reachable": False,
                "last_checked": datetime.now().isoformat(),
                "issues": ["节点不存在"],
            }

        issues = []
        lock_level = None

        # 检查local_path是否可达
        reachable = True
        if node.local_path:
            try:
                importlib.import_module(node.local_path)
            except ImportError as e:
                reachable = False
                issues.append(f"本地路径不可达: {node.local_path}")

        # 检查DNA格式（接入内核严格校验）
        if HAS_DNA_KERNEL:
            try:
                kernel = PeopleSovereigntyGuard()
                entry = kernel.lookup_by_dna(node.dna)
                if entry:
                    if not entry.valid:
                        issues.append(f"DNA格式无效: {node.dna}")
                    # 额外校验：注册表里的 layer 与节点声明的 layer 是否一致
                    if entry.layer != node.layer:
                        issues.append(
                            f"层级不一致: 节点声明 {node.layer} ≠ 注册表 {entry.layer}"
                        )
                    lock_level = kernel.lock_level(entry).value
                else:
                    # 节点DNA不在文件注册表：用严格格式校验 + 基于节点声明计算紧锁
                    import re
                    strict_re = re.compile(
                        r'^#龍芯[\u26a1\ufe0f]*\d{4}-\d{2}-\d{2}-[A-Z][A-Z0-9_-]*-v[\d.]+$'
                    )
                    if not strict_re.match(node.dna or ""):
                        issues.append(f"DNA格式无效: {node.dna}")
                    synthetic = kernel.lookup_by_dna.__self__.entries
                    # 用节点自身信息构造 synthetic entry
                    synthetic_entry = type("DNAEntry", (), {
                        "file": node.local_path or node.name,
                        "dna": node.dna,
                        "date": "",
                        "module": node.name.upper(),
                        "version": "",
                        "valid": bool(strict_re.match(node.dna or "")),
                        "layer": node.layer or "L3_GENERATIONAL",
                        "status": node.status.value if node.status else "🟢",
                        "priority": {"L0_ETERNAL":5,"L1_SEASONAL":20,"L2_DECISION":40,"L3_GENERATIONAL":65,"L4_INSTANT":90}.get(node.layer, 65),
                        "weight": 50.0,
                        "size": 0,
                        "mtime": 0.0,
                    })()
                    lock_level = kernel.lock_level(synthetic_entry).value
            except Exception:
                # 内核不可用则回退到简单前缀检查
                if not node.dna.startswith("#龍芯⚡️"):
                    issues.append("DNA格式错误")
        else:
            if not node.dna.startswith("#龍芯⚡️"):
                issues.append("DNA格式错误")

        # 人民权益守门人：检查节点是否代表资本平台
        if HAS_RIGHTS_GUARD:
            try:
                rights = PeopleRightsGuard()
                text = f"{node.name} {node.description} {' '.join(node.tags)}".lower()
                is_platform_like = any(k in text for k in ("platform", "merchant", "app", "支付", "电商", "广告", "数据"))
                if is_platform_like:
                    provider_id = node.node_id
                    if not rights.is_people_first(provider_id):
                        issues.append(f"节点 {node.node_id} 代表平台/商户，未通过人民权益审查")
            except Exception:
                pass

        return {
            "node_id": node_id,
            "status": node.status,
            "color": node.get_color(),
            "reachable": reachable,
            "last_checked": datetime.now().isoformat(),
            "issues": issues,
            "lock_level": lock_level,
        }

    # ═════════════════════════════════════════════════════════
    # 【持久化】
    # ═════════════════════════════════════════════════════════

    def _load_registry(self) -> None:
        """从文件加载注册表"""
        if not os.path.exists(self.registry_file):
            # 文件不存在，创建空registry
            os.makedirs(os.path.dirname(self.registry_file), exist_ok=True)
            self._create_empty_registry()
            return

        try:
            with open(self.registry_file, 'r', encoding='utf-8') as f:
                for line_no, line in enumerate(f, 1):
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue

                    try:
                        node = RouteNode.from_json(line)
                        self.nodes[normalize_node_id(node.node_id)] = node
                    except json.JSONDecodeError as e:
                        print(f"⚠️ 第 {line_no} 行解析失败: {e}")
        except IOError as e:
            print(f"⚠️ 加载注册表失败: {e}")

    def _create_empty_registry(self) -> None:
        """创建空注册表文件"""
        header = """# 龍魂·IPA路由注册表 (Append-Only JSONL)
# DNA:#龍芯⚡️2026-06-03-IPA-ROUTE-REGISTRY-LOCAL-v1.0
# 格式: JSONL（JSON Lines）- 仅追加，不覆盖
# 每行一条节点记录
# 开始时间: 2026-06-03T{0}
"""
        try:
            with open(self.registry_file, 'w', encoding='utf-8') as f:
                f.write(header.format(datetime.now().isoformat()))
                f.write("# ═══════════════════════════════════════════════════\n")
        except IOError as e:
            print(f"⚠️ 创建注册表文件失败: {e}")

    def _append_to_file(self, node: RouteNode) -> bool:
        """
        追加节点到文件（Append-Only）

        Args:
            node: 路由节点

        Returns:
            成功与否
        """
        try:
            with open(self.registry_file, 'a', encoding='utf-8') as f:
                f.write(node.to_json() + '\n')
                f.flush()
                os.fsync(f.fileno())
            return True
        except IOError as e:
            print(f"⚠️ 追加到注册表失败: {e}")
            return False

    def _save_registry(self) -> bool:
        """
        保存整个注册表（重写）

        注意: 仅在更新状态时使用，应该很少被调用
        """
        try:
            # 备份原文件
            if os.path.exists(self.registry_file):
                backup_file = self.registry_file + ".backup"
                with open(self.registry_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                with open(backup_file, 'w', encoding='utf-8') as f:
                    f.write(content)

            # 重写注册表
            with open(self.registry_file, 'w', encoding='utf-8') as f:
                f.write("# 龍魂·IPA路由注册表 (Append-Only JSONL)\n")
                f.write(f"# 最后更新: {datetime.now().isoformat()}\n")
                f.write("# ═══════════════════════════════════════════════════\n")

                for node in sorted(self.nodes.values(), key=lambda n: n.node_id):
                    f.write(node.to_json() + '\n')

                f.flush()
                os.fsync(f.fileno())

            return True
        except IOError as e:
            print(f"⚠️ 保存注册表失败: {e}")
            return False

    # ═════════════════════════════════════════════════════════
    # 【统计和查询】
    # ═════════════════════════════════════════════════════════

    def get_statistics(self) -> Dict[str, Any]:
        """
        获取统计信息

        Returns:
            统计字典
        """
        by_status = {"🟢": 0, "🟡": 0, "🔴": 0}
        by_type = {}
        by_layer = {}

        for node in self.nodes.values():
            # 按状态统计
            by_status[node.get_color()] += 1

            # 按类型统计
            node_type_str = node.node_type.value
            by_type[node_type_str] = by_type.get(node_type_str, 0) + 1

            # 按层级统计
            if node.layer:
                by_layer[node.layer] = by_layer.get(node.layer, 0) + 1

        return {
            "total_nodes": len(self.nodes),
            "by_status": by_status,
            "by_type": by_type,
            "by_layer": by_layer,
            "registry_file": self.registry_file,
            "file_size_bytes": os.path.getsize(self.registry_file) if os.path.exists(self.registry_file) else 0,
        }

    def selftest(self) -> Tuple[bool, List[str]]:
        """
        自检函数

        Returns:
            (all_pass, error_messages)
        """
        errors = []

        # 检查1: 注册表文件可读写
        if not os.path.exists(self.registry_file):
            errors.append(f"注册表文件不存在: {self.registry_file}")
        elif not os.access(self.registry_file, os.R_OK):
            errors.append(f"注册表文件不可读: {self.registry_file}")
        elif not os.access(self.registry_file, os.W_OK):
            errors.append(f"注册表文件不可写: {self.registry_file}")

        # 检查2: 所有节点的local_path可达
        for node_id, node in self.nodes.items():
            if node.local_path:
                try:
                    importlib.import_module(node.local_path)
                except ImportError:
                    errors.append(f"节点 {node_id} 路径不可达: {node.local_path}")

        # 检查3: DNA格式验证（接入内核严格校验）
        if HAS_DNA_KERNEL:
            try:
                kernel = PeopleSovereigntyGuard()
                for node_id, node in self.nodes.items():
                    entry = kernel.lookup_by_dna(node.dna)
                    if not entry or not entry.valid:
                        errors.append(f"节点 {node_id} DNA无效: {node.dna}")
            except Exception:
                # 回退
                for node_id, node in self.nodes.items():
                    if not node.dna.startswith("#龍芯⚡️"):
                        errors.append(f"节点 {node_id} DNA格式错误: {node.dna}")
        else:
            for node_id, node in self.nodes.items():
                if not node.dna.startswith("#龍芯⚡️"):
                    errors.append(f"节点 {node_id} DNA格式错误: {node.dna}")

        # 检查4: 节点ID规范性
        for node_id in self.nodes.keys():
            if not node_id or "-" not in node_id:
                errors.append(f"节点ID不规范: {node_id}")

        return len(errors) == 0, errors


# ═══════════════════════════════════════════════════════════════
# 【全局单例】（遵循P0模块模式）
# ═══════════════════════════════════════════════════════════════

_GLOBAL_REGISTRY: Optional[RouteRegistry] = None


def get_route_registry() -> RouteRegistry:
    """
    获取全局路由注册表实例

    Returns:
        全局的RouteRegistry实例
    """
    global _GLOBAL_REGISTRY
    if _GLOBAL_REGISTRY is None:
        _GLOBAL_REGISTRY = RouteRegistry()
    return _GLOBAL_REGISTRY


if __name__ == "__main__":
    # 测试
    print("╔═══════════════════════════════════════════════════╗")
    print("║  龍魂路由注册表 · 自检                            ║")
    print("╚═══════════════════════════════════════════════════╝\n")

    registry = get_route_registry()

    # 测试注册
    test_node = RouteNode(
        node_id="TEST-001",
        name="test_node",
        node_type=NodeType.LOCAL,
        status=NodeStatus.ACTIVE,
        local_path="cnsh_core.constitution",
        entry_point="get_system_config",
        dna="#龍芯⚡️2026-06-03-TEST-v1.0",
        layer="L0_ETERNAL",
        description="测试节点",
        tags=["test"],
        dependencies=[],
    )

    success, msg = registry.register(test_node)
    print(f"✅ 节点注册: {msg}")

    # 测试查找
    found = registry.find("TEST-001")
    if found:
        print(f"✅ 节点查找: 找到 {found.name}")
    else:
        print("❌ 节点查找失败")

    # 测试统计
    stats = registry.get_statistics()
    print(f"✅ 统计信息: 共 {stats['total_nodes']} 个节点")

    # 测试自检
    all_pass, errors = registry.selftest()
    if all_pass:
        print(f"✅ 自检通过")
    else:
        print(f"⚠️ 自检有问题:")
        for err in errors:
            print(f"  - {err}")

    print("\n✅ 核心功能测试完成")
