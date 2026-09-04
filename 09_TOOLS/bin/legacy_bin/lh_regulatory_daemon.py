#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
龍魂监管守护进程 · Regulatory Daemon v1.0
DNA: #龍芯⚡️丙午·乙未·丁亥·丙午·䷚颐-REGULATORY-DAEMON-v1.0

后台守护进程，持续监控:
- 文件系统变更（创建/修改/删除）
- Git 提交记录
- 系统资源状态
- 自动索引新文档
- 所有事件推送到监管事件总线

用法:
  python3 bin/lh_regulatory_daemon.py              # 前台运行
  python3 bin/lh_regulatory_daemon.py --daemon     # 后台运行
  python3 bin/lh_regulatory_daemon.py --once       # 执行一次
  python3 bin/lh_regulatory_daemon.py --full-index # 全量索引后退出
"""

import sys
import os
import time
import json
import hashlib
import argparse
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

# 确保项目根在 sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.database import ensure_db
from backend.regulatory_db import (
    init_regulatory_db, log_operation, log_file_change,
)
from backend.regulatory_service import (
    should_index, index_document, full_index, get_file_type,
    event_bus, SKIP_DIRS, SKIP_EXTENSIONS,
)


# ── 配置 ──
WATCH_INTERVAL = 10  # 文件扫描间隔（秒）
HEARTBEAT_INTERVAL = 60  # 心跳间隔（秒）
SYSTEM_CHECK_INTERVAL = 300  # 系统资源检查间隔（秒）


class RegulatoryDaemon:
    """监管守护进程。"""
    
    def __init__(self):
        self.root = PROJECT_ROOT
        self.running = True
        self.file_snapshots = {}  # file_path -> {mtime, sha256}
        self.last_heartbeat = 0
        self.last_system_check = 0
    
    def _now(self) -> float:
        return time.time()
    
    def _sha256(self, file_path: str) -> str:
        h = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(65536), b""):
                    h.update(chunk)
            return h.hexdigest()
        except Exception:
            return ""
    
    def log(self, msg: str):
        print(f"[regulatory daemon] {datetime.now().strftime('%H:%M:%S')} {msg}")
    
    def snapshot_directory(self) -> dict[str, Any]:
        """生成当前文件系统快照。"""
        snapshot = {}
        for dirpath, dirnames, filenames in os.walk(self.root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith('.')]
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                ext = Path(filename).suffix.lower()
                if ext in SKIP_EXTENSIONS:
                    continue
                try:
                    stat = os.stat(file_path)
                    snapshot[file_path] = {
                        "mtime": stat.st_mtime,
                        "size": stat.st_size,
                    }
                except OSError:
                    pass
        return snapshot
    
    def detect_changes(self) -> list[tuple[str, ...]]:
        """检测文件变更。"""
        new_snapshot = self.snapshot_directory()
        changes = []
        
        # 检测新增和修改
        for path, info in new_snapshot.items():
            if path not in self.file_snapshots:
                changes.append(("created", path, None))
            elif info["mtime"] != self.file_snapshots[path].get("mtime"):
                old_sha = self.file_snapshots[path].get("sha256", "")
                new_sha = self._sha256(path)
                if old_sha != new_sha:
                    changes.append(("modified", path, old_sha, new_sha))
                self.file_snapshots[path]["sha256"] = new_sha
        
        # 检测删除
        for path in self.file_snapshots:
            if path not in new_snapshot:
                changes.append(("deleted", path, None))
        
        # 更新快照
        for path, info in new_snapshot.items():
            if path not in self.file_snapshots:
                info["sha256"] = self._sha256(path)
        
        self.file_snapshots = new_snapshot
        return changes
    
    def process_changes(self, changes: list[tuple[str, ...]]):
        """处理文件变更。"""
        for change in changes:
            event_type = change[0]
            file_path = change[1]
            old_sha = change[2] if len(change) > 2 else ""
            new_sha = change[3] if len(change) > 3 else ""
            
            # 记录文件变更日志
            file_type = get_file_type(file_path)
            log_file_change(
                event_type=event_type,
                file_path=file_path,
                file_type=file_type,
                sha256=new_sha if event_type != "deleted" else "",
                previous_sha256=old_sha if event_type == "modified" else "",
            )
            
            # 记录操作日志
            log_operation(
                op_type=f"file_{event_type}",
                source="regulatory_daemon",
                target=file_path,
                detail=f"文件{event_type}: {Path(file_path).name}",
                file_path=file_path,
                old_hash=old_sha,
                new_hash=new_sha,
                operator_uid="SYSTEM",
            )
            
            # 索引文档
            if event_type in ("created", "modified") and should_index(file_path):
                try:
                    index_document(file_path)
                    self.log(f"  📄 索引: {Path(file_path).name}")
                except Exception as e:
                    self.log(f"  ⚠️  索引失败: {file_path} - {e}")
            
            # 推送到事件总线
            try:
                import asyncio
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    asyncio.run_coroutine_threadsafe(
                        event_bus.publish({
                            "type": f"file_{event_type}",
                            "file_path": file_path,
                            "file_name": Path(file_path).name,
                            "file_type": file_type,
                        }),
                        loop
                    )
            except Exception:
                pass
    
    def check_git(self):
        """检查 Git 提交记录。"""
        try:
            result = subprocess.run(
                ["git", "log", "--since=5 minutes ago", "--format=%H|%s|%ai|%an"],
                capture_output=True, text=True, timeout=10,
                cwd=str(self.root)
            )
            if result.returncode == 0 and result.stdout.strip():
                for line in result.stdout.strip().split('\n'):
                    parts = line.split('|', 3)
                    if len(parts) >= 3:
                        log_operation(
                            op_type="git_commit",
                            source="git",
                            target="repository",
                            detail=f"提交: {parts[1][:80]}",
                            operator_uid=parts[3] if len(parts) > 3 else "unknown",
                            dna_trace=parts[0][:12],
                        )
        except Exception:
            pass
    
    def check_system(self):
        """检查系统资源。"""
        try:
            import psutil  # type: ignore[reportMissingModuleSource]
            cpu = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            issues = []
            
            if cpu > 90:
                issues.append(f"CPU {cpu}%")
            if mem.percent > 90:
                issues.append(f"内存 {mem.percent}%")
            if disk.percent > 90:
                issues.append(f"磁盘 {disk.percent}%")
            
            log_operation(
                op_type="system_check",
                source="regulatory_daemon",
                detail=f"CPU:{cpu}% MEM:{mem.percent}% DISK:{disk.percent}%",
                operator_uid="SYSTEM",
            )
            
            if issues:
                self.log(f"  ⚠️  系统告警: {', '.join(issues)}")
        except ImportError:
            pass
    
    def heartbeat(self):
        """发送心跳。"""
        try:
            import asyncio
            loop = asyncio.get_event_loop()
            if loop.is_running():
                asyncio.run_coroutine_threadsafe(
                    event_bus.publish({
                        "type": "heartbeat",
                        "source": "regulatory_daemon",
                    }),
                    loop
                )
        except Exception:
            pass
    
    def run_once(self):
        """执行一轮检查。"""
        self.log("开始扫描...")
        
        # 首次运行：建立基准快照
        if not self.file_snapshots:
            self.file_snapshots = self.snapshot_directory()
            self.log(f"基准快照: {len(self.file_snapshots)} 个文件")
            
            # 全量索引
            self.log("开始全量索引...")
            result = full_index()
            self.log(f"索引完成: {result['indexed']} 已索引, {result['errors']} 错误")
        
        # 检测变更
        changes = self.detect_changes()
        if changes:
            self.log(f"检测到 {len(changes)} 个文件变更")
            self.process_changes(changes)
        else:
            self.log("无变更")
        
        # Git 检查
        self.check_git()
    
    def run_loop(self):
        """主循环。"""
        self.log("🐉 龍魂监管守护进程启动")
        
        ensure_db()
        init_regulatory_db()
        
        log_operation(
            op_type="daemon_start",
            source="regulatory_daemon",
            detail="监管守护进程启动",
            operator_uid="SYSTEM",
        )
        
        # 初始化
        self.run_once()
        
        while self.running:
            try:
                time.sleep(WATCH_INTERVAL)
                
                now = self._now()
                
                # 文件变更检测
                changes = self.detect_changes()
                if changes:
                    self.log(f"检测到 {len(changes)} 个文件变更")
                    self.process_changes(changes)
                
                # Git 检查
                self.check_git()
                
                # 心跳
                if now - self.last_heartbeat >= HEARTBEAT_INTERVAL:
                    self.last_heartbeat = now
                    self.heartbeat()
                
                # 系统检查
                if now - self.last_system_check >= SYSTEM_CHECK_INTERVAL:
                    self.last_system_check = now
                    self.check_system()
                
            except KeyboardInterrupt:
                self.log("收到中断信号")
                self.running = False
            except Exception as e:
                self.log(f"异常: {e}")
                time.sleep(5)
        
        log_operation(
            op_type="daemon_stop",
            source="regulatory_daemon",
            detail="监管守护进程停止",
            operator_uid="SYSTEM",
        )
        self.log("守护进程已停止")


def main():
    global WATCH_INTERVAL
    parser = argparse.ArgumentParser(description="龍魂监管守护进程")
    parser.add_argument("--once", action="store_true", help="执行一轮后退出")
    parser.add_argument("--full-index", action="store_true", help="全量索引后退出")
    parser.add_argument("--daemon", action="store_true", help="后台运行")
    parser.add_argument("--interval", type=int, default=WATCH_INTERVAL, help=f"扫描间隔秒 (默认 {WATCH_INTERVAL})")
    args = parser.parse_args()
    
    WATCH_INTERVAL = args.interval
    
    daemon = RegulatoryDaemon()
    
    if args.full_index:
        print("🐉 全量文档索引中...")
        result = full_index()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    
    if args.once:
        daemon.run_once()
        return
    
    if args.daemon:
        # 后台运行
        pid = os.fork()
        if pid > 0:
            print(f"🐉 监管守护进程已后台启动 (PID: {pid})")
            return
        # 子进程
        os.setsid()
        daemon.run_loop()
    else:
        daemon.run_loop()


if __name__ == "__main__":
    main()
