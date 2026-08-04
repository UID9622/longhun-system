#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
#龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-IDENTITY-CORE-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂·主权身份核心模块
设备指纹 + 行为密码学 + 广播信号签名/验证

DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-IDENTITY-CORE-v1.0
"""
import os
import re
import json
import time
import hashlib
import base64
import platform
import subprocess
from pathlib import Path
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, asdict
from typing import Any

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature


SOVEREIGN_UID = "9622"
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
DNA_TAG = "#龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-IDENTITY-v1.0"


# ---------------------------------------------------------------------------
# 工具函数
# ---------------------------------------------------------------------------
def stable_hash(text: str, length: int = 32) -> str:
    """稳定哈希，用于设备指纹特征脱敏。"""
    return hashlib.sha3_256(text.encode("utf-8")).hexdigest()[:length]


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_public_key(pem_path: Path) -> Ed25519PublicKey:
    pem_bytes = pem_path.read_bytes()
    return serialization.load_pem_public_key(pem_bytes)


# ---------------------------------------------------------------------------
# 设备指纹
# ---------------------------------------------------------------------------
@dataclass
class DeviceFingerprint:
    platform: str
    hostname_hash: str
    os_version_hash: str
    hardware_uuid_hash: str | None
    boot_disk_uuid_hash: str | None
    mac_address_hash: str | None
    cpu_brand_hash: str | None
    memory_gb: int | None
    fingerprint_hash: str

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "DeviceFingerprint":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


def _run(cmd: list[str], timeout: int = 5) -> str:
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, check=False
        )
        return result.stdout.strip()
    except Exception:
        return ""


def collect_device_fingerprint() -> DeviceFingerprint:
    """采集设备指纹。所有敏感字段均哈希脱敏，原始数据不落盘。"""
    hostname = platform.node()
    system = platform.system()
    os_version = platform.platform(aliased=True)

    hardware_uuid = ""
    boot_disk_uuid = ""
    mac_address = ""
    cpu_brand = ""
    memory_gb = None

    if system == "Darwin":
        sp = _run(["system_profiler", "SPHardwareDataType", "-json"])
        if sp:
            try:
                sp_data = json.loads(sp)
                hw = sp_data["SPHardwareDataType"][0]
                hardware_uuid = hw.get("hardware_uuid", "")
                cpu_brand = hw.get("cpu_type", hw.get("chip_type", ""))
                memory_gb = hw.get("physical_memory", None)
                if isinstance(memory_gb, str):
                    mem_match = re.search(r"(\d+)", memory_gb)
                    if mem_match:
                        memory_gb = int(mem_match.group(1))
            except Exception:
                pass

        boot_disk = _run(["diskutil", "info", "-plist", "/"])
        if boot_disk:
            try:
                import plistlib
                plist = plistlib.loads(boot_disk.encode("utf-8"))
                boot_disk_uuid = plist.get("VolumeUUID", "")
            except Exception:
                pass

        ifconfig = _run(["ifconfig"])
        # 取第一个 ether 地址
        ether_match = re.search(r"ether\s+([0-9a-fA-F:]{17})", ifconfig)
        if ether_match:
            mac_address = ether_match.group(1)

    # 构造稳定指纹串
    fingerprint_raw = "|".join([
        system,
        hostname,
        os_version,
        hardware_uuid,
        boot_disk_uuid,
        mac_address,
        str(memory_gb) if memory_gb else "",
        cpu_brand,
    ])
    fingerprint_hash = stable_hash(fingerprint_raw, 64)

    return DeviceFingerprint(
        platform=system,
        hostname_hash=stable_hash(hostname),
        os_version_hash=stable_hash(os_version),
        hardware_uuid_hash=stable_hash(hardware_uuid) if hardware_uuid else None,
        boot_disk_uuid_hash=stable_hash(boot_disk_uuid) if boot_disk_uuid else None,
        mac_address_hash=stable_hash(mac_address) if mac_address else None,
        cpu_brand_hash=stable_hash(cpu_brand) if cpu_brand else None,
        memory_gb=memory_gb,
        fingerprint_hash=fingerprint_hash,
    )


# ---------------------------------------------------------------------------
# 行为密码学
# ---------------------------------------------------------------------------
@dataclass
class BehaviorProfile:
    """行为密码学轮廓：打字节奏 + 命令习惯 + 停顿模式。"""
    avg_dwell_ms: float
    avg_flight_ms: float
    rhythm_vector: list[float]
    top_commands: list[str]
    pause_pattern_ms: list[float]
    sample_count: int
    updated_at: str

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "BehaviorProfile":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


class BehaviorCollector:
    """轻量级行为采集器。记录按键按下/释放时间戳，计算节奏向量。"""

    def __init__(self):
        self.events: list[tuple[str, str, float]] = []  # (key, action, timestamp)
        self.started = False

    def record(self, key: str, action: str) -> None:
        """记录一次按键事件。action 为 'down' 或 'up'。"""
        self.events.append((key, action, time.perf_counter()))
        self.started = True

    def build_profile(self, top_commands: list[str] | None = None) -> BehaviorProfile:
        """从原始事件计算行为轮廓。"""
        down_times: dict[str, float] = {}
        dwells: list[float] = []
        flights: list[float] = []
        last_up_time: float | None = None

        for key, action, ts in self.events:
            if action == "down":
                down_times[key] = ts
            elif action == "up":
                down_ts = down_times.pop(key, None)
                if down_ts is not None:
                    dwell_ms = (ts - down_ts) * 1000
                    dwells.append(dwell_ms)
                    if last_up_time is not None:
                        flight_ms = (down_ts - last_up_time) * 1000
                        flights.append(flight_ms)
                    last_up_time = ts

        avg_dwell = sum(dwells) / len(dwells) if dwells else 0.0
        avg_flight = sum(flights) / len(flights) if flights else 0.0

        # 节奏向量：把 dwell/flight 序列切成 16 段，每段取中位数
        rhythm: list[float] = []
        combined = []
        for d, f in zip(dwells, flights):
            combined.extend([d, f])
        if combined:
            n = len(combined)
            segment_size = max(1, n // 16)
            for i in range(16):
                seg = combined[i * segment_size:(i + 1) * segment_size]
                if seg:
                    seg.sort()
                    rhythm.append(seg[len(seg) // 2])
                else:
                    rhythm.append(0.0)
        else:
            rhythm = [0.0] * 16

        # 停顿模式：相邻事件间隔 > 500ms 的统计
        pauses: list[float] = []
        for i in range(1, len(self.events)):
            delta_ms = (self.events[i][2] - self.events[i - 1][2]) * 1000
            if delta_ms > 500:
                pauses.append(delta_ms)

        return BehaviorProfile(
            avg_dwell_ms=round(avg_dwell, 2),
            avg_flight_ms=round(avg_flight, 2),
            rhythm_vector=[round(x, 2) for x in rhythm],
            top_commands=top_commands or [],
            pause_pattern_ms=[round(x, 2) for x in pauses[:20]],
            sample_count=len(dwells),
            updated_at=now_utc(),
        )


def behavior_similarity(a: BehaviorProfile, b: BehaviorProfile) -> float:
    """计算两个行为轮廓的余弦相似度，返回 0~1。"""
    def _vec_sim(v1: list[float], v2: list[float]) -> float:
        if len(v1) != len(v2):
            return 0.0
        dot = sum(x * y for x, y in zip(v1, v2))
        norm1 = sum(x * x for x in v1) ** 0.5
        norm2 = sum(x * x for x in v2) ** 0.5
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return max(0.0, min(1.0, dot / (norm1 * norm2)))

    rhythm_sim = _vec_sim(a.rhythm_vector, b.rhythm_vector)
    dwell_sim = 1.0 - min(abs(a.avg_dwell_ms - b.avg_dwell_ms) / 200.0, 1.0)
    flight_sim = 1.0 - min(abs(a.avg_flight_ms - b.avg_flight_ms) / 200.0, 1.0)

    # 命令习惯：Jaccard
    set_a = set(a.top_commands)
    set_b = set(b.top_commands)
    if set_a and set_b:
        cmd_sim = len(set_a & set_b) / len(set_a | set_b)
    else:
        cmd_sim = 0.0

    return round(rhythm_sim * 0.5 + dwell_sim * 0.2 + flight_sim * 0.2 + cmd_sim * 0.1, 4)


# ---------------------------------------------------------------------------
# 主权人格广播信号
# ---------------------------------------------------------------------------
@dataclass
class SovereignBroadcast:
    confirm_code: str
    uid: str
    dna: str
    timestamp: str
    session_nonce: str
    device_fingerprint: dict
    behavior_profile: dict | None
    signature: str

    def canonical_payload(self) -> bytes:
        """生成待签名的规范载荷。"""
        payload = {
            "confirm_code": self.confirm_code,
            "uid": self.uid,
            "dna": self.dna,
            "timestamp": self.timestamp,
            "session_nonce": self.session_nonce,
            "device_fingerprint": self.device_fingerprint,
            "behavior_profile": self.behavior_profile,
        }
        return json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")

    def to_compact_string(self) -> str:
        """生成人类可读的广播信号。"""
        core = {
            "uid": self.uid,
            "ts": self.timestamp,
            "nonce": self.session_nonce,
            "fp": self.device_fingerprint.get("fingerprint_hash", "")[:16],
            "sig": self.signature[:24],
        }
        encoded = base64.urlsafe_b64encode(
            json.dumps(core, ensure_ascii=False).encode("utf-8")
        ).decode("ascii")
        return f"{self.confirm_code}|{encoded}"

    def to_dict(self) -> dict:
        return {
            "confirm_code": self.confirm_code,
            "uid": self.uid,
            "dna": self.dna,
            "timestamp": self.timestamp,
            "session_nonce": self.session_nonce,
            "device_fingerprint": self.device_fingerprint,
            "behavior_profile": self.behavior_profile,
            "signature": self.signature,
        }


def generate_broadcast(
    private_key: Ed25519PrivateKey,
    device_fp: DeviceFingerprint,
    behavior: BehaviorProfile | None = None,
    ttl_seconds: int = 60,
) -> SovereignBroadcast:
    """生成一次性的主权人格广播信号。"""
    nonce = base64.urlsafe_b64encode(os.urandom(16)).decode("ascii").rstrip("=")
    timestamp = datetime.now(timezone.utc).isoformat()

    bc = SovereignBroadcast(
        confirm_code=CONFIRM_CODE,
        uid=SOVEREIGN_UID,
        dna=DNA_TAG,
        timestamp=timestamp,
        session_nonce=nonce,
        device_fingerprint=device_fp.to_dict(),
        behavior_profile=behavior.to_dict() if behavior else None,
        signature="",
    )

    signature = private_key.sign(bc.canonical_payload())
    bc.signature = base64.b64encode(signature).decode("ascii")
    return bc


def verify_broadcast(
    public_key: Ed25519PublicKey,
    broadcast: SovereignBroadcast,
    expected_device_fp_hash: str | None = None,
    registered_behavior: BehaviorProfile | None = None,
    behavior_threshold: float = 0.7,
    ttl_seconds: int = 60,
) -> dict:
    """验证广播信号。返回验证结果字典。"""
    result = {
        "uid_match": False,
        "confirm_code_valid": False,
        "signature_valid": False,
        "timestamp_fresh": False,
        "device_fingerprint_match": False,
        "behavior_valid": False,
        "overall": False,
        "details": {},
    }

    # 1. UID
    if broadcast.uid == SOVEREIGN_UID:
        result["uid_match"] = True

    # 2. 确认码格式
    expected_prefix = "#CONFIRM🌌9622-ONLY-ONCE🧬"
    if broadcast.confirm_code.startswith(expected_prefix):
        result["confirm_code_valid"] = True

    # 3. 时间戳 freshness
    try:
        ts = datetime.fromisoformat(broadcast.timestamp)
        now = datetime.now(timezone.utc)
        if abs((now - ts).total_seconds()) <= ttl_seconds:
            result["timestamp_fresh"] = True
    except Exception:
        pass

    # 4. 设备指纹
    fp = broadcast.device_fingerprint
    if expected_device_fp_hash and fp.get("fingerprint_hash") == expected_device_fp_hash:
        result["device_fingerprint_match"] = True
    elif expected_device_fp_hash is None:
        # 未注册期望指纹时，仅验证指纹结构完整
        result["device_fingerprint_match"] = bool(fp.get("fingerprint_hash"))

    # 5. 行为密码学
    if registered_behavior and broadcast.behavior_profile:
        incoming = BehaviorProfile.from_dict(broadcast.behavior_profile)
        sim = behavior_similarity(registered_behavior, incoming)
        result["behavior_valid"] = sim >= behavior_threshold
        result["details"]["behavior_similarity"] = sim
    else:
        # 无注册轮廓时跳过
        result["behavior_valid"] = True

    # 6. 签名
    try:
        public_key.verify(
            base64.b64decode(broadcast.signature),
            broadcast.canonical_payload(),
        )
        result["signature_valid"] = True
    except (InvalidSignature, Exception):
        pass

    result["overall"] = all([
        result["uid_match"],
        result["confirm_code_valid"],
        result["signature_valid"],
        result["timestamp_fresh"],
        result["device_fingerprint_match"],
        result["behavior_valid"],
    ])

    return result


if __name__ == "__main__":
    # 简单自测
    fp = collect_device_fingerprint()
    print(json.dumps(fp.to_dict(), ensure_ascii=False, indent=2))
