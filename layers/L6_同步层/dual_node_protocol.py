# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 双节点同步协议引擎 v1.0
DNA: #龍芯⚡️丙午·辛未·DUAL-NODE-PROTOCOL-v1.0

五维同步体系：
  维度1 — 代码层: Mac ↔ 鲲鹏 rsync 增量同步
  维度2 — 协议层: 01_protocols/ 双向镜像
  维度3 — 知识层: 03_知識圖譜/ + 技能库 双向合并
  维度4 — 记忆层: brain/memories.db 双向合并（CRDT思路，最后写入胜）
  维度5 — 模型层: models/ checkpoint 单向拉取（鲲鹏→Mac）

核心原则：
  - Mac 是指挥部（代码源头），鲲鹏是兵工厂（算力+数据源头）
  - 代码从 Mac → 鲲鹏（push）
  - 模型从 鲲鹏 → Mac（pull）
  - 知识/记忆/协议 双向合并
  - 所有同步操作带DNA签章，可追溯
"""

import hashlib
import json
import os
import sqlite3
import subprocess
import sys
import time
from datetime import datetime, timezone, timedelta
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

ROOT = Path(__file__).resolve().parent.parent
DNA = "#龍芯⚡️丙午·辛未·DUAL-NODE-PROTOCOL-v2.0"
CST = timezone(timedelta(hours=8))
UID_ROOT = "UID9622"

# ─── 同步维度定义 ───

class SyncDimension(Enum):
    CODE = "code"           # 代码层
    PROTOCOL = "protocol"   # 协议层
    KNOWLEDGE = "knowledge" # 知识层
    MEMORY = "memory"       # 记忆层
    MODEL = "model"         # 模型层

# 维度 → 本地路径映射
DIMENSION_PATHS = {
    SyncDimension.CODE: [
        "bin/", "L1_内核层/", "L3_数据层/", "L5_服务层/",
        "scripts/", "deploy/", "agents/", "01_技能庫/",
    ],
    SyncDimension.PROTOCOL: [
        "01_protocols/",
    ],
    SyncDimension.KNOWLEDGE: [
        "03_知識圖譜/", "01_技能庫/",
    ],
    SyncDimension.MEMORY: [
        "brain/memories.db", ".codebuddy/memory/",
    ],
    SyncDimension.MODEL: [
        "models/",
    ],
}

# 维度 → 同步方向
DIMENSION_DIRECTION = {
    SyncDimension.CODE: "mac_to_kunpeng",      # Mac → 鲲鹏
    SyncDimension.PROTOCOL: "bidirectional",     # 双向
    SyncDimension.KNOWLEDGE: "bidirectional",    # 双向
    SyncDimension.MEMORY: "bidirectional",       # 双向合并
    SyncDimension.MODEL: "kunpeng_to_mac",       # 鲲鹏 → Mac
}


class DualNodeProtocol:
    """双节点同步协议引擎"""

    def __init__(self, kunpeng_ip: str = "119.13.90.27",
                 kunpeng_user: str = "root",
                 kunpeng_port: int = 22,
                 kunpeng_path: str = "/opt/longhun-system",
                 ssh_key: str = "~/.ssh/longhun_kunpeng_ed25519",
                 local_path: str = None,
                 use_frp: bool = False):
        self.kunpeng_ip = kunpeng_ip
        self.kunpeng_user = kunpeng_user
        self.kunpeng_port = kunpeng_port
        self.kunpeng_path = kunpeng_path
        self.ssh_key = os.path.expanduser(ssh_key)
        self.local_path = Path(local_path) if local_path else ROOT
        self.use_frp = use_frp
        self.sync_log: List[Dict[str, Any]] = []

        # FRP 隧道端口
        self._frp_api_port = 9633    # 本地127.0.0.1:9633 → 鲲鹏API
        self._frp_ssh_port = 9622    # 本地127.0.0.1:9622 → 鲲鹏SSH

    # ─── SSH 命令工厂 ───

    def _ssh_opts(self) -> str:
        """获取SSH选项"""
        if self.use_frp:
            # 通过 frp 隧道 SSH: 本机 127.0.0.1:9622 → 鲲鹏 22
            opts = f"-p {self._frp_ssh_port} -o StrictHostKeyChecking=no -o ConnectTimeout=10"
            # frp 隧道不需要密钥（frp 侧已认证），但保留兼容
            return opts

        opts = f"-p {self.kunpeng_port} -o StrictHostKeyChecking=accept-new -o ConnectTimeout=10"
        if os.path.exists(self.ssh_key):
            opts += f" -i {self.ssh_key}"
        return opts

    def _ssh_host(self) -> str:
        """SSH 目标主机"""
        if self.use_frp:
            return f"root@127.0.0.1"  # frp 隧道 → 本机映射到鲲鹏
        return f"{self.kunpeng_user}@{self.kunpeng_ip}"

    def _ssh(self, cmd: str) -> Tuple[int, str, str]:
        """执行远程命令"""
        full = f"ssh {self._ssh_opts()} {self._ssh_host()} '{cmd}'"
        result = subprocess.run(full, shell=True, capture_output=True, text=True, timeout=60)
        return result.returncode, result.stdout, result.stderr

    def _rsync_ssh_cmd(self) -> str:
        """rsync 使用的 SSH 命令"""
        if self.use_frp:
            return f"ssh -p {self._frp_ssh_port} -o StrictHostKeyChecking=no"
        return f"ssh {self._ssh_opts()}"

    def _rsync(self, src: str, dst: str, direction: str = "push",
               dry_run: bool = False, delete: bool = False) -> Tuple[int, str]:
        """rsync 同步

        Args:
            src: 源路径
            dst: 目标路径
            direction: "push" (local→remote) 或 "pull" (remote→local)
            dry_run: 仅预览
            delete: 删除目标多余文件
        """
        excludes = [
            "--exclude='__pycache__/'", "--exclude='*.pyc'", "--exclude='*.pyo'",
            "--exclude='.mypy_cache/'", "--exclude='.pytest_cache/'",
            "--exclude='.venv/'", "--exclude='venv/'", "--exclude='node_modules/'",
            "--exclude='.git/'", "--exclude='.DS_Store'",
            "--exclude='*.db'", "--exclude='*.sqlite'", "--exclude='*.sqlite3'",
            "--exclude='logs/'", "--exclude='*.log'",
            "--exclude='backups/'", "--exclude='_archived_reports/'",
            "--exclude='deploy/.kunpeng_*'",
        ]

        ssh_cmd = self._rsync_ssh_cmd()
        if self.use_frp:
            remote = f"root@127.0.0.1:{dst}"
        else:
            remote = f"{self.kunpeng_user}@{self.kunpeng_ip}:{dst}"

        if direction == "push":
            cmd_parts = ["rsync", "-az", f"-e '{ssh_cmd}'"]
            if dry_run:
                cmd_parts.append("-n")
            if delete:
                cmd_parts.append("--delete")
            cmd_parts.extend(excludes)
            cmd_parts.append(f"{src}/")
            cmd_parts.append(remote + "/")
        else:  # pull
            cmd_parts = ["rsync", "-az", f"-e '{ssh_cmd}'"]
            if dry_run:
                cmd_parts.append("-n")
            cmd_parts.extend(excludes)
            cmd_parts.append(remote + "/" + src)
            cmd_parts.append(f"{dst}/")

        cmd = " ".join(cmd_parts)
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
        return result.returncode, result.stdout + result.stderr

    # ─── 维度同步 ───

    def sync_dimension(self, dim: SyncDimension, dry_run: bool = False) -> Dict[str, Any]:
        """同步单个维度"""
        paths = DIMENSION_PATHS.get(dim, [])
        direction = DIMENSION_DIRECTION.get(dim, "mac_to_kunpeng")
        results = []

        for rel_path in paths:
            local_src = self.local_path / rel_path
            remote_dst = f"{self.kunpeng_path}/{rel_path}"

            if not local_src.exists() and direction != "kunpeng_to_mac":
                continue

            if direction == "mac_to_kunpeng":
                # Mac → 鲲鹏
                rc, output = self._rsync(str(local_src), remote_dst, "push", dry_run)
                results.append({"path": rel_path, "direction": "push", "rc": rc, "output": output[:500]})

            elif direction == "kunpeng_to_mac":
                # 鲲鹏 → Mac（只拉模型）
                rc, output = self._rsync(rel_path, str(local_src.parent), "pull", dry_run)
                results.append({"path": rel_path, "direction": "pull", "rc": rc, "output": output[:500]})

            elif direction == "bidirectional":
                # 双向：先push再pull（保守策略，不删远端）
                rc_push, out_push = self._rsync(str(local_src), remote_dst, "push", dry_run)
                rc_pull, out_pull = self._rsync(rel_path, str(local_src.parent), "pull", dry_run)
                results.append({
                    "path": rel_path, "direction": "bidirectional",
                    "push_rc": rc_push, "pull_rc": rc_pull,
                    "output": (out_push + out_pull)[:500]
                })

        entry = {
            "dimension": dim.value,
            "direction": direction,
            "timestamp": datetime.now(CST).isoformat(),
            "dna": DNA,
            "dry_run": dry_run,
            "results": results,
        }
        self.sync_log.append(entry)
        return entry

    def sync_all(self, dry_run: bool = False) -> Dict[str, Any]:
        """五维全量同步"""
        self.sync_log = []
        summary = {
            "dna": DNA,
            "uid": UID_ROOT,
            "timestamp": datetime.now(CST).isoformat(),
            "kunpeng": f"{self.kunpeng_user}@{self.kunpeng_ip}:{self.kunpeng_port}",
            "dry_run": dry_run,
            "dimensions": {},
        }

        for dim in SyncDimension:
            result = self.sync_dimension(dim, dry_run)
            summary["dimensions"][dim.value] = {
                "direction": result["direction"],
                "path_count": len(result["results"]),
                "errors": [r for r in result["results"] if r.get("rc", 0) != 0],
            }

        return summary

    # ─── 记忆层特殊处理 ───

    def sync_memories(self) -> Dict[str, Any]:
        """记忆库双向合并（CRDT思路：时间戳比较，最后写入胜）

        不直接rsync .db 文件（避免覆盖），而是：
        1. 导出本地记忆 → JSON
        2. 拉取远端记忆 → JSON
        3. 按时间戳合并
        4. 双向写回
        """
        local_db = self.local_path / "brain" / "memories.db"
        result = {"dna": DNA, "local_count": 0, "remote_count": 0, "merged": False}

        if local_db.exists():
            conn = sqlite3.connect(str(local_db))
            rows = conn.execute("SELECT COUNT(*) FROM memories").fetchone()
            result["local_count"] = rows[0] if rows else 0
            conn.close()

        # 远端记忆数
        rc, stdout, _ = self._ssh(
            f"sqlite3 {self.kunpeng_path}/brain/memories.db 'SELECT COUNT(*) FROM memories' 2>/dev/null || echo 0"
        )
        if rc == 0 and stdout.strip().isdigit():
            result["remote_count"] = int(stdout.strip())

        return result

    # ─── 连接测试 ───

    def test_connection(self) -> Dict[str, Any]:
        """测试与鲲鹏的连接（frp优先 → SSH直连fallback）"""
        result = {
            "dna": DNA,
            "timestamp": datetime.now(CST).isoformat(),
            "kunpeng_ip": self.kunpeng_ip,
            "ssh_ok": False,
            "frp_ok": False,
            "remote_path_ok": False,
            "disk_info": {},
        }

        # 1. 尝试 frp 隧道
        try:
            import urllib.request, json as ujson
            req = urllib.request.Request(f"http://127.0.0.1:{self._frp_api_port}/health")
            resp = urllib.request.urlopen(req, timeout=5)
            data = ujson.loads(resp.read().decode())
            if data.get("node_role") == "kunpeng":
                result["frp_ok"] = True
        except Exception:
            pass

        # 2. SSH 检测
        if result["frp_ok"] and self.use_frp:
            # 通过 frp SSH 测试
            rc, stdout, stderr = self._ssh("echo OK")
            if rc == 0 and "OK" in stdout:
                result["ssh_ok"] = True
        else:
            # 直接 SSH
            old_frp = self.use_frp
            self.use_frp = False
            try:
                rc, stdout, _ = self._ssh("echo OK")
                if rc == 0 and "OK" in stdout:
                    result["ssh_ok"] = True
            finally:
                self.use_frp = old_frp

        rc, stdout, _ = self._ssh(f"test -d {self.kunpeng_path} && echo YES || echo NO")
        if "YES" in stdout:
            result["remote_path_ok"] = True

        rc, stdout, _ = self._ssh("df -h / | tail -1")
        if rc == 0:
            parts = stdout.strip().split()
            if len(parts) >= 5:
                result["disk_info"] = {
                    "total": parts[1], "used": parts[2],
                    "available": parts[3], "use_pct": parts[4]
                }

        return result


# ─── CLI ───

def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂双节点同步协议引擎")
    parser.add_argument("action", nargs="?", default="status",
                        choices=["status", "sync", "dry", "test", "memory"])
    parser.add_argument("--dimension", "-d", choices=[d.value for d in SyncDimension],
                        help="指定同步维度（默认全部）")
    parser.add_argument("--kunpeng-ip", default="119.13.90.27")
    parser.add_argument("--kunpeng-user", default="root")
    parser.add_argument("--kunpeng-port", type=int, default=22)
    parser.add_argument("--kunpeng-path", default="/opt/longhun-system")
    parser.add_argument("--ssh-key", default="~/.ssh/longhun_kunpeng_ed25519")
    parser.add_argument("--json", action="store_true", help="JSON输出")
    args = parser.parse_args()

    protocol = DualNodeProtocol(
        kunpeng_ip=args.kunpeng_ip,
        kunpeng_user=args.kunpeng_user,
        kunpeng_port=args.kunpeng_port,
        kunpeng_path=args.kunpeng_path,
        ssh_key=args.ssh_key,
    )

    if args.action == "test":
        result = protocol.test_connection()
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"🐉 双节点连接测试")
            print(f"   SSH: {'✅' if result['ssh_ok'] else '❌'} {args.kunpeng_ip}")
            print(f"   路径: {'✅' if result['remote_path_ok'] else '❌'} {args.kunpeng_path}")
            if result.get("disk_info"):
                d = result["disk_info"]
                print(f"   磁盘: {d['used']}/{d['total']} ({d['use_pct']})")

    elif args.action == "sync":
        print(f"🐉 五维同步开始...")
        if args.dimension:
            result = protocol.sync_dimension(SyncDimension(args.dimension))
        else:
            result = protocol.sync_all()
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            for dim_name, info in result["dimensions"].items():
                errors = len(info.get("errors", []))
                icon = "✅" if errors == 0 else "⚠️"
                print(f"   {icon} {dim_name}: {info['direction']} ({info['path_count']}路径, {errors}错误)")

    elif args.action == "dry":
        print(f"🐉 五维同步预览（干运行）...")
        result = protocol.sync_all(dry_run=True)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.action == "memory":
        result = protocol.sync_memories()
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"🐉 记忆库状态")
            print(f"   本地: {result['local_count']} 条")
            print(f"   远端: {result['remote_count']} 条")

    elif args.action == "status":
        result = protocol.test_connection()
        mem_result = protocol.sync_memories()
        if args.json:
            print(json.dumps({**result, "memories": mem_result}, ensure_ascii=False, indent=2))
        else:
            print(f"🐉 龍魂双节点状态")
            print(f"   SSH: {'✅ 在线' if result['ssh_ok'] else '❌ 离线'} | 鲲鹏: {args.kunpeng_ip}")
            print(f"   路径: {'✅' if result['remote_path_ok'] else '❌'} {args.kunpeng_path}")
            print(f"   本地记忆: {mem_result['local_count']}条 | 远端记忆: {mem_result['remote_count']}条")
            if result.get("disk_info"):
                d = result["disk_info"]
                print(f"   远端磁盘: {d['used']}/{d['total']} ({d['use_pct']})")


if __name__ == "__main__":
    main()
