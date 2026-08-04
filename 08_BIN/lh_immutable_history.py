#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·不可篡改历史引擎 v1.0
Dragon Soul Immutable History Engine

DNA: #龍芯⚡️丙午·乙未·丁酉·午时·既济-IMMUTABLE-HISTORY-v1.0
创建者: UID9622 · 龍芯北辰
协议: CC BY-NC-SA 4.0

设计哲学:
  画布是一本账本，永不清零。
  错就错了，改就改了——但不能假装没发生过。
  外部投喂只能旁听，不能篡改真实历史。

核心能力:
  1. 追加式历史记录（Append-Only）
  2. 哈希链完整性保护（SHA-256 + 前一记录哈希）
  3. GPG 数字签名（可选，推荐关键记录）
  4. 防投喂污染标记（external_feed vs system_truth）
  5. 勘误追加机制（correction，不删除原记录）
  6. 链完整性校验与篡改定位

存储路径:
  主账本: ~/.longhun/ledger/immutable_history.jsonl
  签名目录: ~/.longhun/ledger/signatures/
"""

import os
import sys
import json
import hashlib
import hmac
import socket
import time
import uuid
import argparse
import subprocess
import getpass
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum

# ═══════════════════════════════════════════════════════
# 常量与配置
# ═══════════════════════════════════════════════════════

VERSION = "1.0.0"
DNA = "#龍芯⚡️丙午·乙未·丁酉·午时·既济-IMMUTABLE-HISTORY-v1.0"
GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

LEDGER_DIR = Path(os.environ.get("LH_LEDGER_DIR", Path.home() / ".longhun" / "ledger"))
LEDGER_FILE = Path(os.environ.get("LH_LEDGER_FILE", LEDGER_DIR / "immutable_history.jsonl"))
SIG_DIR = Path(os.environ.get("LH_SIG_DIR", LEDGER_DIR / "signatures"))
THREAT_ACTOR_FILE = Path(os.environ.get("LH_THREAT_ACTOR_FILE", LEDGER_DIR / "threat_actors.json"))
GENESIS_HASH = "0" * 64

CST = timezone(timedelta(hours=8))


# ═══════════════════════════════════════════════════════
# 来源溯源与威胁行为体追踪
# ═══════════════════════════════════════════════════════

def _get_local_ip() -> Optional[str]:
    """尝试获取本机局域网 IP（不依赖外网）"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.5)
        # 连接一个保留地址，不实际发送数据
        s.connect(("10.255.255.255", 1))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return None


def collect_local_provenance(extra: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    收集当前环境的来源溯源信息。
    包含 IP、设备指纹、hostname、username 等，但绝不收集敏感隐私。
    """
    try:
        hostname = socket.gethostname()
    except Exception:
        hostname = "unknown"

    try:
        username = getpass.getuser()
    except Exception:
        username = "unknown"

    try:
        # 基于 MAC 地址 + hostname + username 生成稳定设备指纹
        node = uuid.getnode()
        device_fingerprint = hashlib.sha256(
            f"{node}:{hostname}:{username}".encode()
        ).hexdigest()[:32]
    except Exception:
        device_fingerprint = "unknown"

    local_ip = _get_local_ip()

    provenance = {
        "ip": extra.get("ip") if extra else local_ip,
        "device_fingerprint": extra.get("device_fingerprint") if extra else device_fingerprint,
        "hostname": hostname,
        "username": username,
        "user_agent": extra.get("user_agent") if extra else None,
        "session_id": extra.get("session_id") if extra else None,
        "collected_at": now_iso(),
    }

    # 清理 None 值，保持记录紧凑
    return {k: v for k, v in provenance.items() if v is not None}


def compute_actor_id(provenance: Dict[str, Any]) -> str:
    """
    基于 provenance 计算威胁行为体 ID。
    核心原则：device_fingerprint 相同即视为同一行为体，IP 可变但指纹不变。
    没有 fingerprint 时，退而求其次使用 ip + hostname + username。
    """
    fp = provenance.get("device_fingerprint", "")
    if fp and fp != "unknown":
        seed = f"fp:{fp}".encode("utf-8")
    else:
        ip = provenance.get("ip", "")
        host = provenance.get("hostname", "")
        user = provenance.get("username", "")
        seed = f"{ip}:{host}:{user}".encode("utf-8")

    return hashlib.sha256(seed).hexdigest()[:24]


class ThreatActorTracker:
    """
    威胁行为体追踪器。
    对相同 IP / 设备指纹 / hostname 的攻击来源进行证据叠加。
    """

    def __init__(self):
        LEDGER_DIR.mkdir(parents=True, exist_ok=True)
        self.data = self._load()

    def _load(self) -> Dict[str, Any]:
        if THREAT_ACTOR_FILE.exists():
            try:
                return json.loads(THREAT_ACTOR_FILE.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {
            "version": VERSION,
            "dna": DNA,
            "actors": {},
            "total_incidents": 0,
            "last_updated": now_iso(),
        }

    def _save(self):
        self.data["last_updated"] = now_iso()
        THREAT_ACTOR_FILE.write_text(
            json.dumps(self.data, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def record_incident(
        self,
        provenance: Dict[str, Any],
        incident_type: str,
        record_id: str,
        severity: str = "🟡",
        notes: str = "",
    ) -> Dict[str, Any]:
        """
        记录一次事件，若同一 actor 已存在则叠加证据。
        """
        actor_id = compute_actor_id(provenance)
        actors = self.data.setdefault("actors", {})

        if actor_id not in actors:
            actors[actor_id] = {
                "actor_id": actor_id,
                "first_seen": now_iso(),
                "last_seen": now_iso(),
                "incident_count": 0,
                "fingerprints": [],
                "ips": [],
                "hostnames": [],
                "incidents": [],
                "severity_history": [],
                "notes": [],
            }

        actor = actors[actor_id]
        actor["incident_count"] += 1
        actor["last_seen"] = now_iso()
        self.data["total_incidents"] = self.data.get("total_incidents", 0) + 1

        # 去重累积来源标识
        fp = provenance.get("device_fingerprint")
        if fp and fp not in actor["fingerprints"]:
            actor["fingerprints"].append(fp)
        ip = provenance.get("ip")
        if ip and ip not in actor["ips"]:
            actor["ips"].append(ip)
        host = provenance.get("hostname")
        if host and host not in actor["hostnames"]:
            actor["hostnames"].append(host)

        incident = {
            "timestamp": now_iso(),
            "type": incident_type,
            "record_id": record_id,
            "severity": severity,
            "provenance": provenance,
            "notes": notes,
        }
        actor["incidents"].append(incident)
        actor["severity_history"].append(severity)

        # 只保留最近 10 条备注
        if notes:
            actor["notes"].append(f"[{now_iso()}] {notes}")
            actor["notes"] = actor["notes"][-10:]

        self._save()
        return actor

    def get_actor(self, provenance: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        actor_id = compute_actor_id(provenance)
        return self.data.get("actors", {}).get(actor_id)

    def summary(self) -> Dict[str, Any]:
        actors = self.data.get("actors", {})
        return {
            "total_actors": len(actors),
            "total_incidents": self.data.get("total_incidents", 0),
            "last_updated": self.data.get("last_updated"),
            "top_actors": sorted(
                actors.values(),
                key=lambda a: a.get("incident_count", 0),
                reverse=True,
            )[:10],
        }


class SourceType(Enum):
    """记录来源类型"""
    SYSTEM = "system"           # 系统真实历史
    USER_ACTION = "user_action" # 用户真实操作
    EXTERNAL_FEED = "external_feed"  # 外部投喂（需审计）
    CORRECTION = "correction"   # 勘误记录
    AUDIT = "audit"             # 审计标记


class Tricolor(Enum):
    """三色审计"""
    GREEN = "🟢"
    YELLOW = "🟡"
    RED = "🔴"


# ═══════════════════════════════════════════════════════
# DNA 与时间戳
# ═══════════════════════════════════════════════════════

def make_dna(action: str, seed: str = "") -> str:
    """生成 v∞ 干支卦格式 DNA 追溯码（简化版）"""
    now = datetime.now(CST)
    date_str = now.strftime("%Y%m%d%H%M%S")
    h = hashlib.sha256(f"{action}:{seed}:{date_str}:{uuid.uuid4()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️丙午·乙未·丁酉·午时·既济-{action}-{h}"


def now_iso() -> str:
    """ISO 8601 北京时间"""
    return datetime.now(CST).isoformat()


# ═══════════════════════════════════════════════════════
# 哈希链
# ═══════════════════════════════════════════════════════

def compute_record_hash(record: Dict[str, Any], prev_hash: str) -> str:
    """
    计算单条记录的哈希。
    输入: 记录字典（不含 hash 字段）、前一条记录哈希

    向后兼容：旧记录没有 provenance 字段，使用旧算法；
    新记录包含 provenance 字段，hash 中纳入 provenance。
    """
    payload = {
        "id": record.get("id"),
        "timestamp": record.get("timestamp"),
        "action": record.get("action"),
        "source": record.get("source"),
        "actor": record.get("actor"),
        "payload_hash": record.get("payload_hash"),
        "prev_hash": prev_hash,
        "dna": record.get("dna"),
    }
    # 只有新记录（含 provenance key）才将 provenance 纳入哈希
    if "provenance" in record:
        payload["provenance"] = record.get("provenance")

    content = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def compute_payload_hash(payload: Any) -> str:
    """对记录内容计算哈希"""
    content = json.dumps(payload, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


# ═══════════════════════════════════════════════════════
# GPG 签名
# ═══════════════════════════════════════════════════════

def gpg_sign(text: str) -> Optional[str]:
    """使用 UID9622 GPG 私钥对文本签名（分离签名）"""
    try:
        proc = subprocess.run(
            ["gpg", "--batch", "--yes", "--armor", "--detach-sign",
             "--local-user", GPG_FINGERPRINT, "-o", "-"],
            input=text.encode("utf-8"),
            capture_output=True,
            timeout=10,
        )
        if proc.returncode == 0:
            return proc.stdout.decode("utf-8")
    except Exception:
        pass
    return None


def gpg_verify(text: str, signature: str) -> bool:
    """验证 GPG 签名（使用临时文件避免 stdin 格式歧义）"""
    import tempfile
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".asc", delete=False) as sf, \
             tempfile.NamedTemporaryFile(mode="w", delete=False) as df:
            sf.write(signature)
            df.write(text)
            sig_path = sf.name
            data_path = df.name
        proc = subprocess.run(
            ["gpg", "--verify", sig_path, data_path],
            capture_output=True,
            timeout=10,
        )
        return proc.returncode == 0
    except Exception:
        return False
    finally:
        try:
            os.unlink(sig_path)
            os.unlink(data_path)
        except Exception:
            pass


# ═══════════════════════════════════════════════════════
# 账本操作
# ═══════════════════════════════════════════════════════

class ImmutableHistory:
    """不可篡改历史账本"""

    def __init__(self):
        LEDGER_DIR.mkdir(parents=True, exist_ok=True)
        SIG_DIR.mkdir(parents=True, exist_ok=True)
        if not LEDGER_FILE.exists():
            LEDGER_FILE.touch()
        self.tracker = ThreatActorTracker()

    def _last_record(self) -> Optional[Dict[str, Any]]:
        """读取最后一条记录"""
        if LEDGER_FILE.stat().st_size == 0:
            return None
        with LEDGER_FILE.open("r", encoding="utf-8") as f:
            lines = f.readlines()
            if not lines:
                return None
            return json.loads(lines[-1])

    def _last_record(self) -> Optional[Dict[str, Any]]:
        """读取最后一条记录"""
        if LEDGER_FILE.stat().st_size == 0:
            return None
        with LEDGER_FILE.open("r", encoding="utf-8") as f:
            lines = f.readlines()
            if not lines:
                return None
            return json.loads(lines[-1])

    def _last_hash(self) -> str:
        """获取最后一条记录的哈希，空账本返回创世哈希"""
        last = self._last_record()
        return last["hash"] if last else GENESIS_HASH

    def record(
        self,
        action: str,
        payload: Any,
        source: SourceType = SourceType.SYSTEM,
        actor: str = "UID9622",
        sign: bool = False,
        metadata: Optional[Dict[str, Any]] = None,
        provenance: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        追加一条历史记录。

        Args:
            action: 动作名称，如 "deploy", "config_change", "external_feed"
            payload: 任意可 JSON 序列化的内容
            source: 记录来源类型
            actor: 操作者身份
            sign: 是否使用 GPG 签名
            metadata: 额外元数据
            provenance: 来源溯源信息（ip, device_fingerprint, hostname 等）
        """
        payload_hash = compute_payload_hash(payload)
        dna = make_dna(action, payload_hash)

        # 自动收集本地溯源信息，允许传入字段覆盖
        auto_prov = collect_local_provenance(extra=provenance)

        record = {
            "id": str(uuid.uuid4()),
            "timestamp": now_iso(),
            "action": action,
            "source": source.value,
            "actor": actor,
            "payload_hash": payload_hash,
            "payload": payload,
            "dna": dna,
            "version": VERSION,
            "tricolor": Tricolor.GREEN.value,
            "metadata": metadata or {},
            "provenance": auto_prov,
        }

        # 外部投喂强制标记 + 威胁行为体追踪
        if source == SourceType.EXTERNAL_FEED:
            record["tricolor"] = Tricolor.YELLOW.value
            record["metadata"]["contamination_risk"] = "unverified"
            record["metadata"]["immutable_rule"] = "external_feed_cannot_overwrite_system_truth"

            feed_id = record["metadata"].get("feed_id", "unknown")
            self.tracker.record_incident(
                provenance=auto_prov,
                incident_type="external_feed",
                record_id=record["id"],
                severity="🟡",
                notes=f"外部投喂: {feed_id}",
            )

        prev_hash = self._last_hash()
        record["prev_hash"] = prev_hash
        record["hash"] = compute_record_hash(record, prev_hash)

        # GPG 签名
        if sign:
            signature = gpg_sign(record["hash"])
            if signature:
                record["gpg_signature"] = signature
                sig_file = SIG_DIR / f"{record['id']}.asc"
                sig_file.write_text(signature, encoding="utf-8")

        # 追加写入
        with LEDGER_FILE.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

        return record

    def append_correction(
        self,
        target_id: str,
        reason: str,
        corrected_payload: Any,
        actor: str = "UID9622",
        sign: bool = True,
    ) -> Dict[str, Any]:
        """
        对历史记录追加勘误。
        原则: 原记录保留，勘误作为新记录追加。
        """
        return self.record(
            action="correction",
            payload={
                "target_id": target_id,
                "reason": reason,
                "corrected_payload": corrected_payload,
            },
            source=SourceType.CORRECTION,
            actor=actor,
            sign=sign,
            metadata={
                "rule": "original_record_preserved",
                "note": "错就错了，改就改了，但原记录永远可见。",
            },
        )

    def ingest_external_feed(
        self,
        feed_id: str,
        content: Any,
        actor: str = "UID9622",
        metadata: Optional[Dict[str, Any]] = None,
        provenance: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        接收外部投喂内容。
        原则: 永远追加，永不覆盖系统真实历史。
        """
        meta = metadata or {}
        meta["feed_id"] = feed_id
        meta["processing_rule"] = "verbatim_append_only"
        return self.record(
            action="external_feed",
            payload=content,
            source=SourceType.EXTERNAL_FEED,
            actor=actor,
            sign=False,
            metadata=meta,
            provenance=provenance,
        )

    def all_records(self) -> List[Dict[str, Any]]:
        """读取全部记录"""
        records = []
        if LEDGER_FILE.stat().st_size == 0:
            return records
        with LEDGER_FILE.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    records.append(json.loads(line))
        return records

    def verify_chain(self) -> Tuple[bool, List[str]]:
        """
        验证整个哈希链的完整性。
        同时校验：
          1. payload 内容与 payload_hash 一致（防 payload 级篡改）
          2. 记录哈希与前一条哈希链接一致（防记录级篡改）
          3. GPG 签名有效（防伪造）
        返回: (是否完整, 问题列表)
        """
        records = self.all_records()
        if not records:
            return True, ["账本为空"]

        issues = []
        prev_hash = GENESIS_HASH

        for idx, record in enumerate(records):
            # 1. 验证 payload 自身哈希
            stored_payload_hash = record.get("payload_hash")
            actual_payload_hash = compute_payload_hash(record.get("payload"))
            if stored_payload_hash != actual_payload_hash:
                issues.append(
                    f"🔴 记录 #{idx} (id={record.get('id')}) payload 被篡改: "
                    f"存储 hash {stored_payload_hash[:16]}... 实际 {actual_payload_hash[:16]}..."
                )

            # 2. 验证记录哈希链
            expected_hash = compute_record_hash(record, prev_hash)
            if record.get("hash") != expected_hash:
                issues.append(
                    f"🔴 记录 #{idx} (id={record.get('id')}) 哈希链断裂: "
                    f"期望 {expected_hash[:16]}... 实际 {record.get('hash', 'MISSING')[:16]}..."
                )

            # 3. 验证 GPG 签名
            if "gpg_signature" in record:
                if not gpg_verify(record["hash"], record["gpg_signature"]):
                    issues.append(f"🟡 记录 #{idx} GPG 签名验证失败")

            prev_hash = record.get("hash", expected_hash)

        is_valid = len(issues) == 0
        if is_valid:
            issues.append(f"🟢 全部 {len(records)} 条记录哈希链与 payload 完整")
        return is_valid, issues

    def detect_tampering(self) -> Dict[str, Any]:
        """检测篡改尝试并生成报告"""
        is_valid, issues = self.verify_chain()
        report = {
            "timestamp": now_iso(),
            "ledger_file": str(LEDGER_FILE),
            "total_records": len(self.all_records()),
            "integrity_valid": is_valid,
            "issues": issues,
            "threat_actors": self.tracker.summary(),
            "dna": make_dna("tamper_detection", str(is_valid)),
        }
        return report


# ═══════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="龍魂不可篡改历史引擎")
    parser.add_argument("--record", metavar="ACTION", help="记录一个动作")
    parser.add_argument("--payload", default="{}", help="JSON 格式 payload")
    parser.add_argument("--source", default="system",
                        choices=[s.value for s in SourceType],
                        help="记录来源")
    parser.add_argument("--actor", default="UID9622", help="操作者")
    parser.add_argument("--sign", action="store_true", help="GPG 签名")
    parser.add_argument("--feed", metavar="FEED_ID", help="接收外部投喂")
    parser.add_argument("--feed-content", default="{}", help="外部投喂内容 JSON")
    parser.add_argument("--correct", metavar="TARGET_ID", help="追加勘误")
    parser.add_argument("--reason", default="", help="勘误原因")
    parser.add_argument("--verify", action="store_true", help="验证哈希链")
    parser.add_argument("--report", action="store_true", help="生成篡改检测报告")
    parser.add_argument("--list", action="store_true", help="列出最近记录")
    parser.add_argument("--limit", type=int, default=10, help="列出数量")
    parser.add_argument("--ip", help="来源 IP 地址")
    parser.add_argument("--device-fingerprint", help="设备指纹")
    parser.add_argument("--hostname", help="来源主机名")
    parser.add_argument("--user-agent", help="User-Agent")
    parser.add_argument("--session-id", help="会话 ID")
    parser.add_argument("--threat-actors", action="store_true", help="输出威胁行为体摘要")

    args = parser.parse_args()
    history = ImmutableHistory()

    provenance = {
        "ip": args.ip,
        "device_fingerprint": args.device_fingerprint,
        "hostname": args.hostname,
        "user_agent": args.user_agent,
        "session_id": args.session_id,
    }
    provenance = {k: v for k, v in provenance.items() if v is not None}

    if args.record:
        payload = json.loads(args.payload)
        record = history.record(
            action=args.record,
            payload=payload,
            source=SourceType(args.source),
            actor=args.actor,
            sign=args.sign,
            provenance=provenance or None,
        )
        print(json.dumps(record, ensure_ascii=False, indent=2))

    elif args.feed:
        content = json.loads(args.feed_content)
        record = history.ingest_external_feed(
            feed_id=args.feed,
            content=content,
            actor=args.actor,
            provenance=provenance or None,
        )
        print(json.dumps(record, ensure_ascii=False, indent=2))

    elif args.correct:
        corrected = json.loads(args.payload)
        record = history.append_correction(
            target_id=args.correct,
            reason=args.reason,
            corrected_payload=corrected,
            actor=args.actor,
            sign=args.sign,
        )
        print(json.dumps(record, ensure_ascii=False, indent=2))

    elif args.verify:
        is_valid, issues = history.verify_chain()
        print(f"完整性: {'🟢 通过' if is_valid else '🔴 失败'}")
        for issue in issues:
            print(f"  {issue}")
        sys.exit(0 if is_valid else 1)

    elif args.report:
        report = history.detect_tampering()
        print(json.dumps(report, ensure_ascii=False, indent=2))

    elif args.threat_actors:
        summary = history.tracker.summary()
        print(json.dumps(summary, ensure_ascii=False, indent=2))

    elif args.list:
        records = history.all_records()[-args.limit:]
        for r in records:
            prov = r.get("provenance", {})
            fp = prov.get("device_fingerprint", "")[:8]
            ip = prov.get("ip", "")
            prov_str = f" | fp={fp} ip={ip}" if (fp or ip) else ""
            print(f"[{r['timestamp']}] {r['tricolor']} {r['action']} | {r['source']} | {r['dna']}{prov_str}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
