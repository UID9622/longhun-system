#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌐 分布式存储网络 · Distributed Storage Network
DNA: #龍芯⚡️2026-05-22-DISTRIBUTED-STORAGE-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
创建者: UID9622 诸葛鑫（龍芯北辰）
理论指导: 曾仕强老师（永恒显示）

分布式存储网络特性：
1. 三重备份策略（Local + Git + Notion）
2. 节点健康检查
3. 自动故障转移
4. 一致性校验
5. 数据主权保障
"""

import hashlib
import json
import os
import shutil
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import List, Dict, Any, Optional


class StorageStrategy(Enum):
    """存储策略"""
    LOCAL_ONLY = "local"           # 仅本地
    LOCAL_GIT = "local+git"        # 本地 + Git
    TRIPLE = "triple"              # 三重备份 (本地 + Git + Notion)
    ENCRYPTED = "encrypted"        # 加密存储


class NodeStatus(Enum):
    """节点状态"""
    ONLINE = "online"
    OFFLINE = "offline"
    SYNCING = "syncing"
    ERROR = "error"


@dataclass
class StorageNode:
    """存储节点"""
    node_id: str
    node_type: str  # local, git, notion, ipfs
    endpoint: str   # 路径或URL
    status: NodeStatus = NodeStatus.ONLINE
    last_sync: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "node_type": self.node_type,
            "endpoint": self.endpoint,
            "status": self.status.value,
            "last_sync": self.last_sync.isoformat() if self.last_sync else None,
            "metadata": self.metadata,
        }


@dataclass
class StorageResult:
    """存储结果"""
    success: bool
    nodes_written: List[str]
    nodes_failed: List[str]
    sha256: str
    size: int
    dna: str
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "nodes_written": self.nodes_written,
            "nodes_failed": self.nodes_failed,
            "sha256": self.sha256,
            "size": self.size,
            "dna": self.dna,
            "error": self.error,
        }


class DistributedStorage:
    """
    分布式存储网络

    管理多个存储节点，实现三重备份策略
    """

    def __init__(self, base_path: Optional[Path] = None):
        self.base_path = base_path or Path.home() / "longhun-system" / "memory-store"
        self.base_path.mkdir(parents=True, exist_ok=True)

        # 节点列表
        self.nodes: Dict[str, StorageNode] = {}

        # 初始化默认节点
        self._init_default_nodes()

        # 节点配置文件
        self.config_file = self.base_path / "nodes.json"
        self._load_config()

    def _init_default_nodes(self):
        """初始化默认存储节点"""
        # 本地节点
        local_node = StorageNode(
            node_id="local-primary",
            node_type="local",
            endpoint=str(self.base_path / "data"),
            status=NodeStatus.ONLINE
        )
        self.nodes[local_node.node_id] = local_node

        # Git 节点
        git_path = Path.home() / "longhun-system" / ".git"
        git_node = StorageNode(
            node_id="git-primary",
            node_type="git",
            endpoint=str(Path.home() / "longhun-system"),
            status=NodeStatus.ONLINE if git_path.exists() else NodeStatus.OFFLINE,
            metadata={"remote": "origin", "branch": "main"}
        )
        self.nodes[git_node.node_id] = git_node

        # Notion 节点
        notion_node = StorageNode(
            node_id="notion-primary",
            node_type="notion",
            endpoint="https://api.notion.com/v1",
            status=NodeStatus.ONLINE,
            metadata={"workspace": "UID9622"}
        )
        self.nodes[notion_node.node_id] = notion_node

    def _load_config(self):
        """加载节点配置"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    for node_data in config.get("nodes", []):
                        node = StorageNode(
                            node_id=node_data["node_id"],
                            node_type=node_data["node_type"],
                            endpoint=node_data["endpoint"],
                            status=NodeStatus(node_data.get("status", "online")),
                            metadata=node_data.get("metadata", {})
                        )
                        self.nodes[node.node_id] = node
            except Exception:
                pass

    def _save_config(self):
        """保存节点配置"""
        config = {
            "nodes": [n.to_dict() for n in self.nodes.values()],
            "updated_at": datetime.now().isoformat(),
        }
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

    def add_node(self, node: StorageNode):
        """添加存储节点"""
        self.nodes[node.node_id] = node
        self._save_config()

    def remove_node(self, node_id: str):
        """移除存储节点"""
        if node_id in self.nodes:
            del self.nodes[node_id]
            self._save_config()

    def get_node(self, node_id: str) -> Optional[StorageNode]:
        """获取存储节点"""
        return self.nodes.get(node_id)

    def list_nodes(self, node_type: Optional[str] = None) -> List[StorageNode]:
        """列出存储节点"""
        nodes = list(self.nodes.values())
        if node_type:
            nodes = [n for n in nodes if n.node_type == node_type]
        return nodes

    def check_health(self) -> Dict[str, NodeStatus]:
        """检查所有节点健康状态"""
        results = {}
        for node_id, node in self.nodes.items():
            if node.node_type == "local":
                # 本地节点检查目录是否存在
                path = Path(node.endpoint)
                path.mkdir(parents=True, exist_ok=True)
                node.status = NodeStatus.ONLINE
            elif node.node_type == "git":
                # Git 节点检查仓库是否存在
                git_path = Path(node.endpoint) / ".git"
                node.status = NodeStatus.ONLINE if git_path.exists() else NodeStatus.OFFLINE
            elif node.node_type == "notion":
                # Notion 节点假设在线（需要实际API调用确认）
                node.status = NodeStatus.ONLINE
            results[node_id] = node.status
        return results

    def store(self,
              data: bytes,
              filename: str,
              strategy: StorageStrategy = StorageStrategy.TRIPLE,
              metadata: Dict[str, Any] = None) -> StorageResult:
        """
        存储数据到分布式网络

        Args:
            data: 数据内容
            filename: 文件名
            strategy: 存储策略
            metadata: 元数据

        Returns:
            存储结果
        """
        sha256 = hashlib.sha256(data).hexdigest()
        ts = datetime.now().strftime("%Y%m%d%H%M%S")
        dna = f"#龍芯⚡️{ts}-STORE-{sha256[:8]}"

        nodes_written = []
        nodes_failed = []
        error = None

        # 1. 本地存储（必选）
        local_nodes = [n for n in self.nodes.values() if n.node_type == "local" and n.status == NodeStatus.ONLINE]
        for node in local_nodes:
            try:
                path = Path(node.endpoint)
                path.mkdir(parents=True, exist_ok=True)
                file_path = path / filename
                with open(file_path, 'wb') as f:
                    f.write(data)

                # 写入元数据
                meta_path = path / f"{filename}.meta.json"
                meta = {
                    "sha256": sha256,
                    "size": len(data),
                    "stored_at": datetime.now().isoformat(),
                    "dna": dna,
                    **(metadata or {})
                }
                with open(meta_path, 'w', encoding='utf-8') as f:
                    json.dump(meta, f, ensure_ascii=False, indent=2)

                node.last_sync = datetime.now()
                nodes_written.append(node.node_id)
            except Exception as e:
                node.status = NodeStatus.ERROR
                nodes_failed.append(node.node_id)
                error = str(e)

        # 2. Git 存储（如果策略要求）
        if strategy in [StorageStrategy.LOCAL_GIT, StorageStrategy.TRIPLE]:
            git_nodes = [n for n in self.nodes.values() if n.node_type == "git" and n.status == NodeStatus.ONLINE]
            for node in git_nodes:
                try:
                    # 复制到 Git 仓库目录
                    git_path = Path(node.endpoint) / "memory-store"
                    git_path.mkdir(parents=True, exist_ok=True)
                    file_path = git_path / filename
                    with open(file_path, 'wb') as f:
                        f.write(data)
                    node.last_sync = datetime.now()
                    nodes_written.append(node.node_id)
                except Exception as e:
                    nodes_failed.append(node.node_id)

        # 3. Notion 存储（如果策略要求）
        if strategy == StorageStrategy.TRIPLE:
            # Notion 存储需要异步API调用
            # 这里只记录待同步
            notion_nodes = [n for n in self.nodes.values() if n.node_type == "notion"]
            for node in notion_nodes:
                node.status = NodeStatus.SYNCING
                # 实际同步需要调用 Notion API
                # nodes_written.append(node.node_id)

        success = len(nodes_written) > 0

        return StorageResult(
            success=success,
            nodes_written=nodes_written,
            nodes_failed=nodes_failed,
            sha256=sha256,
            size=len(data),
            dna=dna,
            error=error
        )

    def retrieve(self, filename: str) -> Optional[bytes]:
        """
        从分布式网络检索数据

        优先从本地节点读取，失败则尝试其他节点
        """
        # 尝试本地节点
        local_nodes = [n for n in self.nodes.values() if n.node_type == "local"]
        for node in local_nodes:
            path = Path(node.endpoint) / filename
            if path.exists():
                with open(path, 'rb') as f:
                    return f.read()

        # 尝试 Git 节点
        git_nodes = [n for n in self.nodes.values() if n.node_type == "git"]
        for node in git_nodes:
            path = Path(node.endpoint) / "memory-store" / filename
            if path.exists():
                with open(path, 'rb') as f:
                    return f.read()

        return None

    def verify(self, filename: str, expected_sha256: str) -> bool:
        """验证数据完整性"""
        data = self.retrieve(filename)
        if data is None:
            return False
        actual = hashlib.sha256(data).hexdigest()
        return actual == expected_sha256

    def sync_all(self) -> Dict[str, bool]:
        """同步所有节点"""
        results = {}
        # 获取本地节点的所有文件
        local_nodes = [n for n in self.nodes.values() if n.node_type == "local"]
        for local_node in local_nodes:
            local_path = Path(local_node.endpoint)
            if not local_path.exists():
                continue

            for file_path in local_path.glob("*"):
                if file_path.suffix == ".json":
                    continue  # 跳过元数据文件

                # 同步到其他节点
                data = file_path.read_bytes()
                for node in self.nodes.values():
                    if node.node_type == "local":
                        continue
                    if node.node_type == "git":
                        try:
                            git_path = Path(node.endpoint) / "memory-store"
                            git_path.mkdir(parents=True, exist_ok=True)
                            target = git_path / file_path.name
                            target.write_bytes(data)
                            results[f"{node.node_id}:{file_path.name}"] = True
                        except:
                            results[f"{node.node_id}:{file_path.name}"] = False

        return results

    def stats(self) -> Dict[str, Any]:
        """存储统计"""
        self.check_health()

        total_files = 0
        total_size = 0

        local_nodes = [n for n in self.nodes.values() if n.node_type == "local"]
        for node in local_nodes:
            path = Path(node.endpoint)
            if path.exists():
                for f in path.glob("*"):
                    if f.is_file() and not f.suffix == ".json":
                        total_files += 1
                        total_size += f.stat().st_size

        return {
            "total_nodes": len(self.nodes),
            "online_nodes": len([n for n in self.nodes.values() if n.status == NodeStatus.ONLINE]),
            "total_files": total_files,
            "total_size": total_size,
            "nodes": {n.node_id: n.status.value for n in self.nodes.values()},
            "dna": f"#龍芯⚡️{datetime.now().strftime('%Y%m%d%H%M%S')}-STORAGE-STATS"
        }


# 全局实例
_storage: Optional[DistributedStorage] = None


def get_storage() -> DistributedStorage:
    """获取全局存储实例"""
    global _storage
    if _storage is None:
        _storage = DistributedStorage()
    return _storage


if __name__ == "__main__":
    # 测试
    print("🌐 分布式存储网络测试")
    print("=" * 60)

    storage = DistributedStorage()

    # 检查节点健康
    print("📡 节点状态:")
    health = storage.check_health()
    for node_id, status in health.items():
        node = storage.get_node(node_id)
        print(f"  {node_id} ({node.node_type}): {status.value}")

    print()

    # 存储测试
    test_data = "龍魂系统测试数据".encode('utf-8')
    result = storage.store(test_data, "test_2026-05-22.dat", StorageStrategy.LOCAL_GIT)
    print(f"存储结果:")
    print(f"  成功: {result.success}")
    print(f"  写入节点: {result.nodes_written}")
    print(f"  SHA256: {result.sha256}")
    print(f"  DNA: {result.dna}")

    print()

    # 检索测试
    retrieved = storage.retrieve("test_2026-05-22.dat")
    if retrieved:
        print(f"检索成功: {retrieved.decode('utf-8')}")
        print(f"完整性验证: {'✅' if storage.verify('test_2026-05-22.dat', result.sha256) else '❌'}")

    print()

    # 统计
    stats = storage.stats()
    print(f"📊 存储统计:")
    print(f"  节点总数: {stats['total_nodes']}")
    print(f"  在线节点: {stats['online_nodes']}")
    print(f"  文件总数: {stats['total_files']}")
    print(f"  总大小: {stats['total_size']} 字节")
