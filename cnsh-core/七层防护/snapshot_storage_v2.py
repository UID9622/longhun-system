#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂快照存储策略 v2.0 · 三重存储

DNA: #龍芯⚡️2026-05-21-SNAPSHOT-STORAGE-V2.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

存储策略（三合一）：
1. 本地文件系统（主）：快、离线可用
2. Git 仓库（版本）：完整历史、分支管理
3. Notion 数据库（索引）：跨设备、元数据可视化

理论指导：曾仕强老师（永恒显示）
献礼：中华人民共和国
"""

import os
import json
import hashlib
import subprocess
import time
from datetime import datetime
from typing import Optional, Dict, List, Any, Tuple
from dataclasses import dataclass, field
from pathlib import Path
from enum import Enum

# ============================================================
# 配置
# ============================================================

class SnapshotConfig:
    """快照存储配置"""

    # 路径
    BASE_DIR = Path.home() / "longhun-system"
    SNAPSHOT_DIR = BASE_DIR / "snapshots"
    SNAPSHOT_GIT_DIR = SNAPSHOT_DIR / ".git"

    # Notion 配置（从环境变量读取）
    NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")
    NOTION_SNAPSHOT_DB = os.environ.get("NOTION_SNAPSHOT_DB", "")

    # 策略开关
    ENABLE_LOCAL = True      # 本地存储（必须开）
    ENABLE_GIT = True        # Git 版本控制
    ENABLE_NOTION = True     # Notion 元数据索引

    # 保留策略
    MAX_SNAPSHOTS = 1000
    RETENTION_DAYS = 30

    # Git 配置
    GIT_AUTHOR_NAME = "龍魂快照系统"
    GIT_AUTHOR_EMAIL = "snapshot@longhun.local"


class SnapshotType(Enum):
    """快照类型"""
    PRE_OPERATION = "pre_operation"      # 操作前快照
    CRITICAL_NODE = "critical_node"      # 关键节点
    MANUAL = "manual"                    # 手动创建
    FUSE_RECOVERY = "fuse_recovery"      # 熔断恢复点
    DAILY_BACKUP = "daily_backup"        # 每日备份


class StorageResult(Enum):
    """存储结果"""
    SUCCESS = "SUCCESS"
    PARTIAL = "PARTIAL"  # 部分成功
    FAILED = "FAILED"


# ============================================================
# 数据结构
# ============================================================

@dataclass
class Snapshot:
    """快照对象"""
    snapshot_id: str
    timestamp: str
    snapshot_type: SnapshotType
    trigger: str
    context: Dict
    dna_marker: str

    # 存储状态
    local_path: Optional[str] = None
    git_commit: Optional[str] = None
    notion_page_id: Optional[str] = None

    # 元数据
    size_bytes: int = 0
    hash_sha256: str = ""
    parent_snapshot_id: Optional[str] = None

    def to_dict(self) -> Dict:
        return {
            "snapshot_id": self.snapshot_id,
            "timestamp": self.timestamp,
            "snapshot_type": self.snapshot_type.value,
            "trigger": self.trigger,
            "context": self.context,
            "dna_marker": self.dna_marker,
            "local_path": self.local_path,
            "git_commit": self.git_commit,
            "notion_page_id": self.notion_page_id,
            "size_bytes": self.size_bytes,
            "hash_sha256": self.hash_sha256,
            "parent_snapshot_id": self.parent_snapshot_id,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Snapshot":
        return cls(
            snapshot_id=data["snapshot_id"],
            timestamp=data["timestamp"],
            snapshot_type=SnapshotType(data["snapshot_type"]),
            trigger=data["trigger"],
            context=data["context"],
            dna_marker=data["dna_marker"],
            local_path=data.get("local_path"),
            git_commit=data.get("git_commit"),
            notion_page_id=data.get("notion_page_id"),
            size_bytes=data.get("size_bytes", 0),
            hash_sha256=data.get("hash_sha256", ""),
            parent_snapshot_id=data.get("parent_snapshot_id"),
        )


@dataclass
class StorageReport:
    """存储报告"""
    snapshot_id: str
    overall_status: StorageResult
    local_status: Optional[str] = None
    git_status: Optional[str] = None
    notion_status: Optional[str] = None
    errors: List[str] = field(default_factory=list)


# ============================================================
# 1. 本地文件系统存储
# ============================================================

class LocalStorage:
    """
    本地文件系统存储
    路径结构：~/longhun-system/snapshots/YYYY-MM-DD/snapshot_XXXXXXXX.json
    """

    @staticmethod
    def init() -> bool:
        """初始化本地存储目录"""
        try:
            SnapshotConfig.SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            print(f"[LocalStorage] 初始化失败: {e}")
            return False

    @staticmethod
    def save(snapshot: Snapshot) -> Tuple[bool, str]:
        """保存快照到本地"""
        try:
            # 按日期分目录
            date_dir = SnapshotConfig.SNAPSHOT_DIR / datetime.now().strftime("%Y-%m-%d")
            date_dir.mkdir(parents=True, exist_ok=True)

            # 快照文件
            filename = f"snapshot_{snapshot.snapshot_id}.json"
            filepath = date_dir / filename

            # 序列化
            content = json.dumps(snapshot.to_dict(), ensure_ascii=False, indent=2)

            # 计算哈希
            snapshot.hash_sha256 = hashlib.sha256(content.encode()).hexdigest()
            snapshot.size_bytes = len(content.encode())
            snapshot.local_path = str(filepath)

            # 写入
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)

            return True, str(filepath)

        except Exception as e:
            return False, str(e)

    @staticmethod
    def load(snapshot_id: str) -> Optional[Snapshot]:
        """加载快照"""
        # 搜索所有日期目录
        for date_dir in SnapshotConfig.SNAPSHOT_DIR.glob("????-??-??"):
            filepath = date_dir / f"snapshot_{snapshot_id}.json"
            if filepath.exists():
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return Snapshot.from_dict(data)
        return None

    @staticmethod
    def list_snapshots(limit: int = 100) -> List[Dict]:
        """列出最近的快照"""
        snapshots = []
        for filepath in sorted(
            SnapshotConfig.SNAPSHOT_DIR.glob("????-??-??/snapshot_*.json"),
            reverse=True
        )[:limit]:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                snapshots.append({
                    "snapshot_id": data["snapshot_id"],
                    "timestamp": data["timestamp"],
                    "trigger": data["trigger"],
                    "path": str(filepath),
                })
        return snapshots

    @staticmethod
    def find_last_safe() -> Optional[str]:
        """查找最近的安全快照"""
        snapshots = LocalStorage.list_snapshots(10)
        if snapshots:
            return snapshots[0]["snapshot_id"]
        return None


# ============================================================
# 2. Git 版本控制存储
# ============================================================

class GitStorage:
    """
    Git 仓库版本控制
    每次快照 = 一个 commit，重要快照打 tag
    """

    @staticmethod
    def init() -> bool:
        """初始化 Git 仓库"""
        if not SnapshotConfig.ENABLE_GIT:
            return True

        try:
            SnapshotConfig.SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)

            # 检查是否已初始化
            if not SnapshotConfig.SNAPSHOT_GIT_DIR.exists():
                subprocess.run(
                    ["git", "init"],
                    cwd=SnapshotConfig.SNAPSHOT_DIR,
                    capture_output=True,
                    check=True
                )
                # 配置 Git
                subprocess.run(
                    ["git", "config", "user.name", SnapshotConfig.GIT_AUTHOR_NAME],
                    cwd=SnapshotConfig.SNAPSHOT_DIR,
                    capture_output=True
                )
                subprocess.run(
                    ["git", "config", "user.email", SnapshotConfig.GIT_AUTHOR_EMAIL],
                    cwd=SnapshotConfig.SNAPSHOT_DIR,
                    capture_output=True
                )
                # 创建 .gitignore
                gitignore = SnapshotConfig.SNAPSHOT_DIR / ".gitignore"
                with open(gitignore, "w") as f:
                    f.write("# 忽略临时文件\n*.tmp\n*.swp\n.DS_Store\n")

                # 初始提交
                subprocess.run(
                    ["git", "add", "."],
                    cwd=SnapshotConfig.SNAPSHOT_DIR,
                    capture_output=True
                )
                subprocess.run(
                    ["git", "commit", "-m", "🛡️ 龍魂快照仓库初始化"],
                    cwd=SnapshotConfig.SNAPSHOT_DIR,
                    capture_output=True
                )

            return True

        except Exception as e:
            print(f"[GitStorage] 初始化失败: {e}")
            return False

    @staticmethod
    def commit(snapshot: Snapshot) -> Tuple[bool, str]:
        """提交快照到 Git"""
        if not SnapshotConfig.ENABLE_GIT:
            return True, "GIT_DISABLED"

        try:
            # 添加文件
            subprocess.run(
                ["git", "add", "."],
                cwd=SnapshotConfig.SNAPSHOT_DIR,
                capture_output=True,
                check=True
            )

            # 构建提交信息
            commit_msg = f"""💾 快照 {snapshot.snapshot_id}

类型: {snapshot.snapshot_type.value}
触发: {snapshot.trigger}
DNA: {snapshot.dna_marker}
时间: {snapshot.timestamp}
"""

            # 提交
            result = subprocess.run(
                ["git", "commit", "-m", commit_msg],
                cwd=SnapshotConfig.SNAPSHOT_DIR,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                # 获取 commit hash
                hash_result = subprocess.run(
                    ["git", "rev-parse", "HEAD"],
                    cwd=SnapshotConfig.SNAPSHOT_DIR,
                    capture_output=True,
                    text=True
                )
                commit_hash = hash_result.stdout.strip()[:8]
                snapshot.git_commit = commit_hash

                # 关键节点打 tag
                if snapshot.snapshot_type in [
                    SnapshotType.CRITICAL_NODE,
                    SnapshotType.FUSE_RECOVERY
                ]:
                    tag_name = f"snapshot-{snapshot.snapshot_id}"
                    subprocess.run(
                        ["git", "tag", tag_name],
                        cwd=SnapshotConfig.SNAPSHOT_DIR,
                        capture_output=True
                    )

                return True, commit_hash
            else:
                # 可能没有变更
                if "nothing to commit" in result.stdout:
                    return True, "NO_CHANGES"
                return False, result.stderr

        except Exception as e:
            return False, str(e)

    @staticmethod
    def rollback_to(commit_hash: str) -> Tuple[bool, str]:
        """回滚到指定 commit"""
        try:
            result = subprocess.run(
                ["git", "checkout", commit_hash, "--", "."],
                cwd=SnapshotConfig.SNAPSHOT_DIR,
                capture_output=True,
                text=True
            )
            return result.returncode == 0, result.stderr or "OK"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def get_history(limit: int = 20) -> List[Dict]:
        """获取 Git 历史"""
        try:
            result = subprocess.run(
                ["git", "log", f"-{limit}", "--pretty=format:%h|%s|%ai"],
                cwd=SnapshotConfig.SNAPSHOT_DIR,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                history = []
                for line in result.stdout.strip().split("\n"):
                    if line:
                        parts = line.split("|")
                        if len(parts) >= 3:
                            history.append({
                                "commit": parts[0],
                                "message": parts[1],
                                "date": parts[2],
                            })
                return history
            return []
        except:
            return []


# ============================================================
# 3. Notion 元数据索引
# ============================================================

class NotionStorage:
    """
    Notion 数据库元数据索引
    每个快照 = 一个 Page，属性存元数据
    """

    @staticmethod
    def _load_token() -> str:
        """加载 Notion Token（优先 secrets.env，避免环境变量污染）"""
        secrets_file = Path.home() / ".longhun" / "secrets.env"
        if secrets_file.exists():
            with open(secrets_file, "r") as f:
                for line in f:
                    if line.startswith("NOTION_TOKEN="):
                        return line.strip().split("=", 1)[1]

        # 备选：环境变量
        if SnapshotConfig.NOTION_TOKEN:
            return SnapshotConfig.NOTION_TOKEN
        return ""

    @staticmethod
    def _load_db_id() -> str:
        """加载快照数据库 ID（优先 secrets.env）"""
        secrets_file = Path.home() / ".longhun" / "secrets.env"
        if secrets_file.exists():
            with open(secrets_file, "r") as f:
                for line in f:
                    if line.startswith("NOTION_SNAPSHOT_DB="):
                        return line.strip().split("=", 1)[1]

        # 备选：环境变量
        if SnapshotConfig.NOTION_SNAPSHOT_DB:
            return SnapshotConfig.NOTION_SNAPSHOT_DB
        return ""

    @staticmethod
    def init() -> bool:
        """检查 Notion 配置"""
        if not SnapshotConfig.ENABLE_NOTION:
            return True

        token = NotionStorage._load_token()
        db_id = NotionStorage._load_db_id()

        if not token or not db_id:
            print("[NotionStorage] 未配置 NOTION_TOKEN 或 NOTION_SNAPSHOT_DB")
            return False

        return True

    @staticmethod
    def push_metadata(snapshot: Snapshot) -> Tuple[bool, str]:
        """推送快照元数据到 Notion（使用 curl 确保兼容性）"""
        if not SnapshotConfig.ENABLE_NOTION:
            return True, "NOTION_DISABLED"

        token = NotionStorage._load_token()
        db_id = NotionStorage._load_db_id()

        if not token or not db_id:
            return False, "NOTION_NOT_CONFIGURED"

        try:
            # 页面数据
            data = {
                "parent": {"database_id": db_id},
                "properties": {
                    "Name": {
                        "title": [{"text": {"content": f"快照 {snapshot.snapshot_id}"}}]
                    },
                    "Snapshot ID": {
                        "rich_text": [{"text": {"content": snapshot.snapshot_id}}]
                    },
                    "Type": {
                        "select": {"name": snapshot.snapshot_type.value}
                    },
                    "Trigger": {
                        "rich_text": [{"text": {"content": snapshot.trigger}}]
                    },
                    "DNA": {
                        "rich_text": [{"text": {"content": snapshot.dna_marker}}]
                    },
                    "Git Commit": {
                        "rich_text": [{"text": {"content": snapshot.git_commit or "N/A"}}]
                    },
                    "Local Path": {
                        "rich_text": [{"text": {"content": snapshot.local_path or "N/A"}}]
                    },
                    "Size": {
                        "number": snapshot.size_bytes
                    },
                    "Hash": {
                        "rich_text": [{"text": {"content": snapshot.hash_sha256[:16] + "..."}}]
                    },
                }
            }

            # 使用 curl 调用（已验证可用）
            result = subprocess.run(
                [
                    "curl", "-s", "-X", "POST",
                    "https://api.notion.com/v1/pages",
                    "-H", f"Authorization: Bearer {token}",
                    "-H", "Notion-Version: 2022-06-28",
                    "-H", "Content-Type: application/json",
                    "-d", json.dumps(data)
                ],
                capture_output=True,
                text=True,
                timeout=15
            )

            if result.returncode == 0:
                response = json.loads(result.stdout)
                if "id" in response:
                    page_id = response["id"]
                    snapshot.notion_page_id = page_id
                    return True, page_id[:16]
                else:
                    error_msg = response.get("message", "Unknown error")
                    return False, error_msg[:100]
            else:
                return False, result.stderr[:100]

        except Exception as e:
            return False, str(e)[:100]

    @staticmethod
    def query_snapshots(limit: int = 20) -> List[Dict]:
        """查询 Notion 中的快照索引"""
        token = NotionStorage._load_token()
        db_id = NotionStorage._load_db_id()

        if not token or not db_id:
            return []

        try:
            import urllib.request

            url = f"https://api.notion.com/v1/databases/{db_id}/query"
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "Notion-Version": "2022-06-28",
            }

            data = {
                "page_size": limit,
                "sorts": [{"timestamp": "created_time", "direction": "descending"}]
            }

            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode(),
                headers=headers,
                method="POST"
            )

            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read())
                return result.get("results", [])

        except:
            return []


# ============================================================
# 快照存储管理器（三合一）
# ============================================================

class SnapshotStorageManager:
    """
    快照存储管理器
    协调三重存储策略：本地 + Git + Notion
    """

    @staticmethod
    def init_all() -> Dict[str, bool]:
        """初始化所有存储"""
        results = {
            "local": LocalStorage.init(),
            "git": GitStorage.init() if SnapshotConfig.ENABLE_GIT else True,
            "notion": NotionStorage.init() if SnapshotConfig.ENABLE_NOTION else True,
        }
        return results

    @staticmethod
    def create_snapshot(
        trigger: str,
        context: Dict,
        snapshot_type: SnapshotType = SnapshotType.PRE_OPERATION,
        parent_id: Optional[str] = None
    ) -> Tuple[Snapshot, StorageReport]:
        """
        创建快照并存储到三个位置
        返回: (快照对象, 存储报告)
        """

        # 生成快照 ID
        snapshot_id = hashlib.sha256(
            f"{time.time()}-{trigger}".encode()
        ).hexdigest()[:16]

        # 创建快照对象
        snapshot = Snapshot(
            snapshot_id=snapshot_id,
            timestamp=datetime.now().isoformat(),
            snapshot_type=snapshot_type,
            trigger=trigger,
            context=context,
            dna_marker=f"#龍芯⚡️{datetime.now().strftime('%Y%m%d')}-SNAPSHOT-{snapshot_id}",
            parent_snapshot_id=parent_id,
        )

        # 存储报告
        report = StorageReport(snapshot_id=snapshot_id, overall_status=StorageResult.SUCCESS)
        errors = []

        # 1. 本地存储（必须成功）
        local_ok, local_msg = LocalStorage.save(snapshot)
        if local_ok:
            report.local_status = f"✅ {local_msg}"
        else:
            report.local_status = f"❌ {local_msg}"
            errors.append(f"本地存储失败: {local_msg}")

        # 2. Git 版本控制
        if SnapshotConfig.ENABLE_GIT:
            git_ok, git_msg = GitStorage.commit(snapshot)
            if git_ok:
                report.git_status = f"✅ {git_msg}"
            else:
                report.git_status = f"⚠️ {git_msg}"
                errors.append(f"Git提交失败: {git_msg}")

        # 3. Notion 元数据索引
        if SnapshotConfig.ENABLE_NOTION:
            notion_ok, notion_msg = NotionStorage.push_metadata(snapshot)
            if notion_ok:
                report.notion_status = f"✅ {notion_msg}"
            else:
                report.notion_status = f"⚠️ {notion_msg}"
                errors.append(f"Notion推送失败: {notion_msg}")

        # 判断总体状态
        if not local_ok:
            report.overall_status = StorageResult.FAILED
        elif errors:
            report.overall_status = StorageResult.PARTIAL
        else:
            report.overall_status = StorageResult.SUCCESS

        report.errors = errors

        return snapshot, report

    @staticmethod
    def rollback_to_snapshot(snapshot_id: str) -> Tuple[bool, str]:
        """回滚到指定快照"""

        # 加载快照
        snapshot = LocalStorage.load(snapshot_id)
        if not snapshot:
            return False, f"快照 {snapshot_id} 不存在"

        # 如果有 Git commit，从 Git 回滚
        if snapshot.git_commit and SnapshotConfig.ENABLE_GIT:
            git_ok, git_msg = GitStorage.rollback_to(snapshot.git_commit)
            if not git_ok:
                return False, f"Git回滚失败: {git_msg}"

        return True, f"已回滚到快照 {snapshot_id}"

    @staticmethod
    def get_storage_status() -> Dict:
        """获取存储状态"""
        local_count = len(list(SnapshotConfig.SNAPSHOT_DIR.glob("????-??-??/snapshot_*.json")))
        git_commits = len(GitStorage.get_history(100)) if SnapshotConfig.ENABLE_GIT else 0

        return {
            "local": {
                "enabled": SnapshotConfig.ENABLE_LOCAL,
                "count": local_count,
                "path": str(SnapshotConfig.SNAPSHOT_DIR),
            },
            "git": {
                "enabled": SnapshotConfig.ENABLE_GIT,
                "commits": git_commits,
                "initialized": SnapshotConfig.SNAPSHOT_GIT_DIR.exists(),
            },
            "notion": {
                "enabled": SnapshotConfig.ENABLE_NOTION,
                "configured": bool(NotionStorage._load_token() and NotionStorage._load_db_id()),
            },
        }


# ============================================================
# 命令行测试
# ============================================================

def main():
    """测试入口"""
    print("💾 龍魂快照存储 v2.0 · 三重策略")
    print("=" * 50)

    # 初始化
    print("\n🔧 初始化存储...")
    init_results = SnapshotStorageManager.init_all()
    for name, ok in init_results.items():
        print(f"  {'✅' if ok else '❌'} {name}")

    # 创建测试快照
    print("\n📸 创建测试快照...")
    snapshot, report = SnapshotStorageManager.create_snapshot(
        trigger="test_snapshot",
        context={"test": True, "message": "三重存储测试"},
        snapshot_type=SnapshotType.MANUAL
    )

    print(f"\n快照 ID: {snapshot.snapshot_id}")
    print(f"DNA: {snapshot.dna_marker}")
    print(f"\n存储结果 ({report.overall_status.value}):")
    print(f"  本地: {report.local_status}")
    print(f"  Git:  {report.git_status or 'N/A'}")
    print(f"  Notion: {report.notion_status or 'N/A'}")

    if report.errors:
        print(f"\n⚠️ 错误:")
        for err in report.errors:
            print(f"  - {err}")

    # 存储状态
    print("\n📊 存储状态:")
    status = SnapshotStorageManager.get_storage_status()
    print(f"  本地: {status['local']['count']} 个快照")
    print(f"  Git:  {status['git']['commits']} 个提交")
    print(f"  Notion: {'已配置' if status['notion']['configured'] else '未配置'}")


if __name__ == "__main__":
    main()
