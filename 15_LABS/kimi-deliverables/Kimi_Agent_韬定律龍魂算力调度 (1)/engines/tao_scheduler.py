#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·韬定律调度器 v2.2
DNA: #龍芯⚡️丙午·乙未·辛酉·甲午·䷫姤-TAO-LAW-INTEGRATED-v2.2

功能：
- L0 直通三重命中校验（设备指纹 + GPG 签名 + 双签）
- 信号词路由 → 热/审计/温/冷四层
- 64 卦执行位分配与蚁群降级接管
- 用量审计日志（8 字段，只传用量不传内容）
- 跨平台后端抽象：Ascend / NVIDIA / CPU / macOS
"""

import hashlib
import json
import os
import re
import sqlite3
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

# ═══════════════════════════════════════════════════════════
# L0 常量
# ═══════════════════════════════════════════════════════════

FOUNDER_GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

# 信号词正则 → 目标层（高温优先）
SIGNAL_RULES: List[Tuple[str, str]] = [
    (r"实时|推理|对话|训练|紧急|中断|恢复|熔断", "hot"),
    (r"审计|取证|合规", "audit"),
    (r"批量|报表|归档|夜间|压缩|索引|重建", "cold"),
]
DEFAULT_LAYER = "warm"

# 64 卦主位 → 任务类型与蚁群备份链（对齐 v2.2 八卦路由矩阵）
GUA_MASTER = {
    "乾": ("hot", "训练主任务"),
    "兑": ("hot", "实时推理"),
    "离": ("warm", "API 网关"),
    "震": ("warm", "常驻服务"),
    "巽": ("cold", "离线批处理"),
    "坎": ("audit", "日志重放/审计"),
    "艮": ("cold", "归档迁移"),
    "坤": ("warm", "路由表维护"),
}

GUA_BACKUP_CHAIN = {
    "乾": [("兑", "hot"), ("离", "warm")],
    "兑": [("乾", "hot"), ("离", "warm")],
    "离": [("震", "warm"), ("巽", "cold")],
    "震": [("离", "warm"), ("巽", "cold")],
    "巽": [("离", "warm"), ("震", "warm")],
    "坎": [("离", "warm"), ("艮", "cold")],
    "艮": [("坎", "audit"), ("坤", "warm")],
    "坤": [("艮", "cold"), ("乾", "hot")],
}

# 温度层 → 后端执行占位命令（生产环境替换）
BACKEND_COMMANDS = {
    "hot": ["ollama", "run", "longhun:latest"],
    "warm": ["ollama", "run", "longhun:latest", "-o", "num_gpu=0"],
    "cold": ["ollama", "run", "longhun:latest", "--keepalive", "0"],
    "audit": ["python3", "-m", "engines.tao_scheduler", "--audit-only"],
}


# ═══════════════════════════════════════════════════════════
# 工具函数
# ═══════════════════════════════════════════════════════════

def now_iso() -> str:
    """返回带时区的 ISO 时间戳"""
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def sha256_hex(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def task_type_hash(req: str) -> str:
    """只取请求类型标签的哈希：先按信号词归一化，再哈希"""
    for pattern, _ in SIGNAL_RULES:
        if re.search(pattern, req):
            return "sha256:" + sha256_hex(pattern)[:16]
    return "sha256:" + sha256_hex(DEFAULT_LAYER)[:16]


# ═══════════════════════════════════════════════════════════
# L0 三重命中校验
# ═══════════════════════════════════════════════════════════

class L0Gate:
    """L0 直通三重命中门：设备指纹 + GPG 签名 + 双签"""

    def __init__(self, cred_dir: str = "/etc/lh"):
        self.cred_dir = Path(cred_dir)

    def check_device_fingerprint(self, req: str) -> bool:
        """条件1：请求串包含本机设备指纹"""
        fp_file = self.cred_dir / "device_fingerprint"
        if not fp_file.exists():
            return False
        fp = fp_file.read_text().strip()
        return fp and fp in req

    def check_gpg_signature(self) -> bool:
        """条件2：/etc/lh/l0_payload 的分离签名有效且签名人指纹匹配创始人"""
        payload = self.cred_dir / "l0_payload"
        sig = self.cred_dir / "l0_payload.sig"
        if not payload.exists() or not sig.exists():
            return False
        try:
            out = subprocess.run(
                ["gpg", "--verify", str(sig), str(payload)],
                capture_output=True,
                text=True,
            )
            combined = (out.stdout or "") + (out.stderr or "")
            return FOUNDER_GPG_FINGERPRINT in combined
        except FileNotFoundError:
            return False

    def check_dual_signature(self) -> bool:
        """条件3：双签文件存在且可被验证"""
        payload = self.cred_dir / "l0_payload"
        dual = self.cred_dir / "l0_dualsign.sig"
        if not payload.exists() or not dual.exists():
            return False
        try:
            out = subprocess.run(
                ["gpg", "--verify", str(dual), str(payload)],
                capture_output=True,
            )
            return out.returncode == 0
        except FileNotFoundError:
            return False

    def validate(self, req: str) -> Tuple[bool, int]:
        """返回 (是否通过, 命中条件数)"""
        hits = 0
        if self.check_device_fingerprint(req):
            hits += 1
        if self.check_gpg_signature():
            hits += 1
        if self.check_dual_signature():
            hits += 1
        return hits >= 3, hits


# ═══════════════════════════════════════════════════════════
# 64 卦执行位管理
# ═══════════════════════════════════════════════════════════

class _JsonSlotBackend:
    """JSON 后端：兼容原有命令行默认行为"""

    def __init__(self, state_file: Path):
        self.state_file = state_file

    def load(self) -> Optional[Dict[str, Dict]]:
        if self.state_file.exists():
            try:
                return json.loads(self.state_file.read_text(encoding="utf-8"))
            except Exception:
                return None
        return None

    def save(self, slots: Dict[str, Dict]):
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state_file.write_text(json.dumps(slots, ensure_ascii=False, indent=2))


class _SQLiteSlotBackend:
    """SQLite 后端：API 并发持久化，支持 WAL 与 upsert"""

    def __init__(self, state_file: Path):
        self.state_file = state_file
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(state_file), check_same_thread=False)
        self._conn.execute("PRAGMA journal_mode=WAL;")
        self._ensure_table()

    def _ensure_table(self):
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS gua_slots (
                addr TEXT PRIMARY KEY,
                exec_addr TEXT NOT NULL,
                bound_resource TEXT NOT NULL,
                task_hash TEXT NOT NULL,
                layer TEXT NOT NULL,
                state TEXT NOT NULL
            )
            """
        )
        self._conn.commit()

    def load(self) -> Optional[Dict[str, Dict]]:
        rows = self._conn.execute("SELECT addr, exec_addr, bound_resource, task_hash, layer, state FROM gua_slots").fetchall()
        if not rows:
            return None
        return {
            addr: {
                "exec_addr": exec_addr,
                "bound_resource": bound_resource,
                "task_hash": task_hash,
                "layer": layer,
                "state": state,
            }
            for addr, exec_addr, bound_resource, task_hash, layer, state in rows
        }

    def save(self, slots: Dict[str, Dict]):
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        with self._conn:
            self._conn.execute("DELETE FROM gua_slots")
            self._conn.executemany(
                """
                INSERT INTO gua_slots (addr, exec_addr, bound_resource, task_hash, layer, state)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        addr,
                        info["exec_addr"],
                        info["bound_resource"],
                        info["task_hash"],
                        info["layer"],
                        info["state"],
                    )
                    for addr, info in slots.items()
                ],
            )


class GuaSlotManager:
    """64 卦执行位：8 主卦 × 8 子位；根据 state_file 后缀自动选择 JSON 或 SQLite 后端"""

    def __init__(self, state_file: str = "/var/lib/lh/gua_slots.json"):
        self.state_file = Path(state_file)
        self.slots: Dict[str, Dict] = {}
        self._lock = threading.RLock()
        if self.state_file.suffix == ".db":
            self._backend: Union[_JsonSlotBackend, _SQLiteSlotBackend] = _SQLiteSlotBackend(self.state_file)
        else:
            self._backend = _JsonSlotBackend(self.state_file)
        self._load()

    def _addr(self, gua: str, sub: int) -> str:
        return f"{gua}-{sub}"

    def _load(self):
        with self._lock:
            loaded = self._backend.load()
            if loaded is not None:
                self.slots = loaded
                return
            # 初始化 64 位全部空闲
            self.slots = {}
            for gua in GUA_MASTER:
                for sub in range(1, 9):
                    self.slots[self._addr(gua, sub)] = {
                        "exec_addr": self._addr(gua, sub),
                        "bound_resource": f"{gua}-res-{sub}",
                        "task_hash": "",
                        "layer": GUA_MASTER[gua][0],
                        "state": "free",
                    }
            self._save()

    def _save(self):
        self._backend.save(self.slots)

    def allocate(self, layer: str, task_hash: str) -> Optional[str]:
        """
        为某温度层任务分配执行位。
        优先分配该层主卦的空闲子位；无则触发蚁群备份链。
        返回执行位地址，失败返回 None。
        """
        with self._lock:
            # 1. 同层主卦内找空闲子位
            candidates = [gua for gua, (ly, _) in GUA_MASTER.items() if ly == layer]
            for gua in candidates:
                for sub in range(1, 9):
                    addr = self._addr(gua, sub)
                    if self.slots[addr]["state"] == "free":
                        self.slots[addr]["state"] = "running"
                        self.slots[addr]["task_hash"] = task_hash
                        self._save()
                        return addr

            # 2. 按备份链跨卦接管（高温层可向低温层借位）
            for gua in candidates:
                for backup_gua, backup_layer in GUA_BACKUP_CHAIN.get(gua, []):
                    if backup_layer == layer:
                        continue
                    for sub in range(1, 9):
                        addr = self._addr(backup_gua, sub)
                        if self.slots[addr]["state"] == "free":
                            self.slots[addr]["state"] = "degraded"
                            self.slots[addr]["task_hash"] = task_hash
                            self._save()
                            return addr
            return None

    def release(self, addr: str):
        with self._lock:
            if addr in self.slots:
                self.slots[addr]["state"] = "free"
                self.slots[addr]["task_hash"] = ""
                self._save()

    def freeze(self, addr: str):
        """P0：只解冻不删除"""
        with self._lock:
            if addr in self.slots:
                self.slots[addr]["state"] = "frozen"
                self._save()


# ═══════════════════════════════════════════════════════════
# 审计日志链
# ═══════════════════════════════════════════════════════════

class AuditLog:
    """用量审计日志：8 字段 + sha256 链"""

    def __init__(self, log_file: str = "/var/log/tao_audit.log"):
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def _last_hash(self) -> str:
        if not self.log_file.exists():
            return "sha256:" + "0" * 64
        lines = self.log_file.read_text().strip().splitlines()
        if not lines:
            return "sha256:" + "0" * 64
        return lines[-1].split(",")[-1]

    def write(
        self,
        layer: str,
        task_type_hash: str,
        duration_sec: int,
        energy_mj: int,
        call_count: int,
        route_priority: str,
    ) -> str:
        """严格写入 8 字段审计日志，维护 sha256 链"""
        prev = self._last_hash()
        timestamp = now_iso()
        payload = f"{timestamp},{layer},{task_type_hash},{duration_sec},{energy_mj},{call_count},{route_priority},{prev}"
        new_hash = "sha256:" + sha256_hex(payload)
        line = payload + "," + new_hash
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(line + "\n")
        return new_hash

    def verify_chain(self) -> Tuple[bool, int]:
        """校验审计链完整性，返回 (是否完整, 断链数)"""
        if not self.log_file.exists():
            return True, 0
        lines = self.log_file.read_text().strip().splitlines()
        breaks = 0
        prev_hash = "sha256:" + "0" * 64
        for line in lines:
            parts = line.rsplit(",", 1)
            if len(parts) != 2:
                breaks += 1
                continue
            payload, stored_hash = parts
            expected = "sha256:" + sha256_hex(payload)
            if stored_hash != expected:
                breaks += 1
            # 链咬合检查：payload 末尾应为上一条的 hash
            payload_prev = payload.rsplit(",", 1)[-1]
            if payload_prev != prev_hash:
                breaks += 1
            prev_hash = stored_hash
        return breaks == 0, breaks


# ═══════════════════════════════════════════════════════════
# 调度器主类
# ═══════════════════════════════════════════════════════════

class TaoScheduler:
    def __init__(
        self,
        cred_dir: str = "/etc/lh",
        log_file: str = "/var/log/tao_audit.log",
        slot_file: str = "/var/lib/lh/gua_slots.json",
    ):
        self.l0 = L0Gate(cred_dir)
        self.slots = GuaSlotManager(slot_file)
        self.audit = AuditLog(log_file)

    def route(self, req: str) -> str:
        """信号词路由，冲突取高温层"""
        # 高温优先遍历
        for pattern, layer in SIGNAL_RULES:
            if re.search(pattern, req):
                return layer
        return DEFAULT_LAYER

    def schedule(self, req: str) -> Dict:
        """调度入口：返回路由结果与执行位"""
        result = {
            "timestamp": now_iso(),
            "req_hash": sha256_hex(req)[:16],
            "layer": "",
            "priority": "L3",
            "exec_addr": "",
            "audit_hash": "",
            "message": "",
        }

        # L0 直通校验
        if "L0-GATE" in req:
            ok, hits = self.l0.validate(req)
            if not ok:
                result["priority"] = "L0_FORGE"
                result["layer"] = "rejected"
                result["message"] = f"L0 三重命中缺一：hits={hits}"
                result["audit_hash"] = self.audit.write(
                    layer="rejected",
                    task_type_hash="sha256:" + result["req_hash"],
                    duration_sec=0,
                    energy_mj=0,
                    call_count=1,
                    route_priority=f"L0_FORGE_REJECT_hits={hits}",
                )
                return result
            result["priority"] = "L0"
            result["layer"] = "hot"
        else:
            result["layer"] = self.route(req)

        # 分配执行位
        task_hash = "sha256:" + result["req_hash"]
        addr = self.slots.allocate(result["layer"], task_hash)
        if addr:
            result["exec_addr"] = addr
        else:
            # 无可用位：降级到更低温层
            fallback_layer = self._fallback(result["layer"])
            result["layer"] = fallback_layer
            result["message"] += f" 无可用执行位，降级至 {fallback_layer}"
            addr = self.slots.allocate(fallback_layer, task_hash)
            result["exec_addr"] = addr or "QUEUE"

        # 写审计日志
        result["audit_hash"] = self.audit.write(
            layer=result["layer"],
            task_type_hash=task_type_hash,
            duration_sec=0,
            energy_mj=0,
            call_count=1,
            route_priority=result["priority"],
        )
        return result

    def _fallback(self, layer: str) -> str:
        order = ["hot", "audit", "warm", "cold"]
        idx = order.index(layer)
        return order[min(idx + 1, len(order) - 1)]

    def execute(self, result: Dict):
        """平台后端执行占位；生产环境替换为真实命令"""
        layer = result["layer"]
        if layer == "rejected":
            print(f"[REJECT] {result['message']}")
            return
        cmd = BACKEND_COMMANDS.get(layer, BACKEND_COMMANDS["warm"])
        print(f"[{layer.upper():5}] exec_addr={result['exec_addr']} cmd={' '.join(cmd)}")


# ═══════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="龍魂·韬定律调度器 v2.2",
        epilog="默认使用 /tmp/lh_test 作为数据目录便于无 root 测试；生产环境请用 --data-dir 指定。",
    )
    parser.add_argument("request", nargs="?", help="请求串")
    parser.add_argument("--verify-chain", action="store_true", help="校验审计链完整性")
    parser.add_argument("--audit-only", action="store_true", help="审计节点占位执行")
    parser.add_argument("--data-dir", default="/tmp/lh_test", help="数据根目录（默认 /tmp/lh_test）")
    parser.add_argument("--cred-dir", help="凭证目录（默认 <data-dir>/etc）")
    parser.add_argument("--log-file", help="审计日志路径（默认 <data-dir>/tao_audit.log）")
    parser.add_argument("--slot-file", help="执行位状态文件（默认 <data-dir>/gua_slots.json）")
    args = parser.parse_args()

    base = Path(args.data_dir)
    cred_dir = args.cred_dir or str(base / "etc")
    log_file = args.log_file or str(base / "tao_audit.log")
    slot_file = args.slot_file or str(base / "gua_slots.json")

    scheduler = TaoScheduler(cred_dir=cred_dir, log_file=log_file, slot_file=slot_file)

    if args.verify_chain:
        ok, breaks = scheduler.audit.verify_chain()
        print(f"审计链完整: {ok}, 断链数: {breaks}")
        sys.exit(0 if ok else 1)

    if args.audit_only:
        print("[AUDIT] 坎☵审计节点占位执行")
        sys.exit(0)

    if not args.request:
        parser.print_help()
        sys.exit(1)

    result = scheduler.schedule(args.request)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    scheduler.execute(result)


if __name__ == "__main__":
    main()
