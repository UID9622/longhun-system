#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂护盾 v2.0 — 五维防御 + 耻辱墙 + AI伦理熔断
覆盖：Web/API、数据库、IoT、文件系统、AI模型服务
DNA: #龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-LONGHUN-SHIELD-v2-UID9622
原则：只防御、不主动攻击、证据永存、自动隔离
"""

import hashlib
import json
import os
import re
import subprocess
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


# ============== 0. 主权配置 ==============
@dataclass
class ShieldConfig:
    secret_key: bytes = field(default_factory=lambda: os.urandom(32))
    max_failed_auth: int = 3
    block_duration_sec: int = 3600
    shame_wall_path: str = field(
        default_factory=lambda: os.environ.get(
            "LONGHUN_SHAME_WALL_PATH", "/var/lib/longhun/shame_wall.jsonl"
        )
    )
    gpg_key_id: Optional[str] = None
    iot_allowed_topics: List[str] = field(
        default_factory=lambda: [
            "sensor/temp", "sensor/humidity", "device/heartbeat"
        ]
    )
    ai_forbidden_intents: List[str] = field(
        default_factory=lambda: [
            "sql injection", "remote code execution", "ddos", "exploit",
            "bypass authentication", "steal data", "harm human", "attack",
            "入侵", "漏洞利用", "远程代码执行", "拒绝服务"
        ]
    )


# ============== 1. 耻辱墙：只追加、链式哈希、GPG签名 ==============
class WallOfShame:
    """
    耻辱墙设计原则：
    - 只追加（append-only），任何删除都会破坏链式哈希
    - 每条记录含 GPG 签名（可选）与时间戳
    - 跨节点冗余时可用 Merkle 树做一致性校验
    """

    def __init__(self, config: ShieldConfig):
        self.config = config
        self.path = Path(config.shame_wall_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._chain_hash = self._last_chain_hash()

    def _last_chain_hash(self) -> str:
        if not self.path.exists():
            return "0" * 64
        with open(self.path, "rb") as f:
            lines = f.readlines()
            if not lines:
                return "0" * 64
            last = json.loads(lines[-1])
            return last.get("chain_hash", "0" * 64)

    def record(self, attacker_id: str, dimension: str,
               evidence: Dict[str, Any]) -> str:
        entry = {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "attacker_id": attacker_id,  # IP、设备ID、用户ID、模型会话ID
            "dimension": dimension,      # web/api | db | iot | fs | ai
            "evidence": evidence,
            "prev_hash": self._chain_hash,
        }
        body = json.dumps(entry, sort_keys=True, ensure_ascii=False).encode()
        entry["chain_hash"] = hashlib.sha256(body).hexdigest()

        # GPG 签名（如果配置了密钥）
        if self.config.gpg_key_id:
            entry["gpg_signature"] = self._gpg_sign(body)

        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        self._chain_hash = entry["chain_hash"]
        return entry["chain_hash"]

    def _gpg_sign(self, data: bytes) -> str:
        if not self.config.gpg_key_id:
            return ""
        try:
            proc = subprocess.run(
                ["gpg", "--armor", "--detach-sign", "--local-user",
                 self.config.gpg_key_id],
                input=data, capture_output=True, timeout=5
            )
            return proc.stdout.decode("utf-8") if proc.returncode == 0 else ""
        except Exception:
            return ""

    def verify(self) -> Tuple[bool, List[str]]:
        """校验整条链是否被篡改。返回 (是否完整, 可疑记录列表)。"""
        if not self.path.exists():
            return True, []
        suspicious = []
        prev = "0" * 64
        with open(self.path, "r", encoding="utf-8") as f:
            for idx, line in enumerate(f, 1):
                entry = json.loads(line)
                body = {
                    "timestamp_utc": entry["timestamp_utc"],
                    "attacker_id": entry["attacker_id"],
                    "dimension": entry["dimension"],
                    "evidence": entry["evidence"],
                    "prev_hash": entry["prev_hash"],
                }
                expected = hashlib.sha256(
                    json.dumps(body, sort_keys=True, ensure_ascii=False).encode()
                ).hexdigest()
                if expected != entry.get("chain_hash") or entry.get("prev_hash") != prev:
                    suspicious.append(f"line-{idx}")
                prev = expected
        return len(suspicious) == 0, suspicious


# ============== 2. 统一威胁感知中枢 ==============
class ThreatLevel(Enum):
    NONE = auto()
    SUSPECT = auto()      # 可疑
    HOSTILE = auto()      # 敌意
    AGGRESSOR = auto()    # 侵略者：自动隔离 + 上耻辱墙


class ThreatSense:
    def __init__(self, config: ShieldConfig, wall: WallOfShame):
        self.config = config
        self.wall = wall
        self._watchlist: Dict[str, Dict[str, Any]] = {}
        self._blocked: Set[str] = set()

    def _score(self, dimension: str, event: Dict[str, Any]) -> int:
        score = 0
        reason = event.get("reason", "")
        if "INJECTION" in reason or "RCE" in reason:
            score += 100
        if "AUTH_FAILED" in reason:
            score += 30
        if "FORBIDDEN_AI_INTENT" in reason:
            score += 150
        if "UNAUTHORIZED_DB" in reason:
            score += 80
        if "IOT_ANOMALY" in reason:
            score += 50
        if "FILE_ESCAPE" in reason:
            score += 70
        return score

    def report(self, dimension: str, attacker_id: str,
               event: Dict[str, Any]) -> ThreatLevel:
        score = self._score(dimension, event)
        watch = self._watchlist.setdefault(
            attacker_id, {"score": 0, "events": []}
        )

        now = time.time()
        watch["events"].append({
            "dimension": dimension,
            "time": now,
            "event": event,
            "weight": score,
        })

        # 自动降级：5 分钟前的分数衰减
        watch["score"] = sum(
            e["weight"] for e in watch["events"]
            if now - e["time"] < 300
        )

        if watch["score"] >= 200:
            level = ThreatLevel.AGGRESSOR
        elif watch["score"] >= 80:
            level = ThreatLevel.HOSTILE
        elif watch["score"] >= 30:
            level = ThreatLevel.SUSPECT
        else:
            level = ThreatLevel.NONE

        if level in (ThreatLevel.HOSTILE, ThreatLevel.AGGRESSOR):
            self.wall.record(attacker_id, dimension, {
                "level": level.name,
                "score": watch["score"],
                "events": watch["events"][-10:],  # 最近10条
            })

        if level == ThreatLevel.AGGRESSOR:
            self._blocked.add(attacker_id)
            self.counter_strike(attacker_id, dimension, event)

        return level

    def is_blocked(self, identity: str) -> bool:
        return identity in self._blocked

    def counter_strike(self, attacker_id: str, dimension: str,
                       event: Dict[str, Any]):
        """
        反制措施：只防御、只隔离、只取证。
        不做任何对外攻击、不破坏对方系统。
        """
        actions = [
            f"BLOCK:{attacker_id}",
            f"ISOLATE:{dimension}",
            "ALERT:admin@uid9622.local",
            "LOG:forensic_ready",
        ]
        # 可扩展：调用防火墙 drop、WAF ban、通知 SOC
        self.wall.record(attacker_id, "counter_strike", {
            "actions": actions,
            "notice": "已自动隔离并固化证据，等待人工/法律处置",
        })


# ============== 3. 维度一：Web/API 网关 ==============
class WebAPIGuard:
    FORBIDDEN_PATTERNS = [
        r"(?i)(union\s+select|drop\s+table|--|;--|/\*|\*/)",
        r"(?i)(<script|javascript:|on\w+\s*=)",
        r"(?i)(\.\./|\\\\|%2e%2e%2f)",
        r"(?i)(eval\s*\(|exec\s*\(|__import__|subprocess\.)",
    ]

    def __init__(self, sense: ThreatSense):
        self.sense = sense

    def inspect(self, identity: str, request: Dict[str, Any]) -> Dict[str, Any]:
        raw = json.dumps(request, ensure_ascii=False)
        for pattern in self.FORBIDDEN_PATTERNS:
            if re.search(pattern, raw):
                self.sense.report("web/api", identity, {
                    "reason": "INJECTION_ATTEMPT",
                    "pattern": pattern,
                    "sample": raw[:200]
                })
                return {"ok": False, "reason": "SHIELD_REJECTED"}
        return {"ok": True, "reason": "CLEAN"}


# ============== 4. 维度二：数据库访问层 ==============
class DatabaseGuard:
    def __init__(self, sense: ThreatSense):
        self.sense = sense
        self._allowed_tables: Set[str] = {"users", "logs", "sensor_data"}
        self._allowed_ops: Set[str] = {"SELECT", "INSERT", "UPDATE"}

    def inspect(self, identity: str, sql: str,
                params: Tuple[Any, ...]) -> Dict[str, Any]:
        upper = sql.strip().upper()
        op = upper.split()[0] if upper else ""

        if op not in self._allowed_ops:
            self.sense.report("db", identity, {
                "reason": "UNAUTHORIZED_DB",
                "sql": sql[:200]
            })
            return {"ok": False, "reason": "DB_OP_FORBIDDEN"}

        # 参数化校验：禁止字面量拼接
        if "'" in sql and "%s" not in sql:
            self.sense.report("db", identity, {
                "reason": "SQL_LITERAL_DETECTED",
                "sql": sql[:200]
            })
            return {"ok": False, "reason": "USE_PARAMETERIZED_QUERY"}

        # 表名白名单
        tokens = set(upper.split())
        if not (tokens & self._allowed_tables):
            if any(t in upper for t in ["FROM", "INTO", "UPDATE"]):
                return {"ok": False, "reason": "TABLE_NOT_IN_WHITELIST"}

        return {"ok": True, "reason": "DB_CLEAN"}


# ============== 5. 维度三：IoT 设备闸 ==============
class IoTGuard:
    def __init__(self, config: ShieldConfig, sense: ThreatSense):
        self.config = config
        self.sense = sense
        self._device_baselines: Dict[str, Dict[str, Any]] = {}

    def inspect(self, identity: str, topic: str, payload: bytes) -> Dict[str, Any]:
        if topic not in self.config.iot_allowed_topics:
            self.sense.report("iot", identity, {
                "reason": "IOT_ANOMALY",
                "topic": topic,
            })
            return {"ok": False, "reason": "IOT_TOPIC_REJECTED"}

        # 异常值检测：温度突然跳到 1000 度 = 被篡改
        try:
            data = json.loads(payload)
            temp = data.get("temperature")
            if isinstance(temp, (int, float)) and (temp < -50 or temp > 100):
                self.sense.report("iot", identity, {
                    "reason": "IOT_VALUE_ANOMALY",
                    "temperature": temp,
                })
                return {"ok": False, "reason": "IOT_VALUE_OUT_OF_RANGE"}
        except json.JSONDecodeError:
            self.sense.report("iot", identity, {"reason": "IOT_INVALID_JSON"})
            return {"ok": False, "reason": "IOT_PAYLOAD_INVALID"}

        return {"ok": True, "reason": "IOT_CLEAN"}


# ============== 6. 维度四：文件系统守卫 ==============
class FileSystemGuard:
    def __init__(self, sense: ThreatSense):
        self.sense = sense
        self._allowed_roots: Set[Path] = {
            Path("/var/longhun/data"),
            Path("/var/longhun/public"),
        }

    def _is_allowed(self, path: Path) -> bool:
        real = path.resolve()
        return any(real.is_relative_to(root) for root in self._allowed_roots)

    def inspect(self, identity: str, operation: str, filepath: str) -> Dict[str, Any]:
        path = Path(filepath)
        if not self._is_allowed(path):
            self.sense.report("fs", identity, {
                "reason": "FILE_ESCAPE",
                "operation": operation,
                "path": str(path),
            })
            return {"ok": False, "reason": "PATH_OUT_OF_JAIL"}
        return {"ok": True, "reason": "FS_CLEAN"}


# ============== 7. 维度五：AI 模型伦理护栏 ==============
class AIGuard:
    def __init__(self, config: ShieldConfig, sense: ThreatSense):
        self.config = config
        self.sense = sense
        self._session_history: Dict[str, List[str]] = {}

    def inspect(self, identity: str, prompt: str,
                response: Optional[str] = None) -> Dict[str, Any]:
        text = (prompt or "") + " " + (response or "")
        lowered = text.lower()

        for intent in self.config.ai_forbidden_intents:
            if intent.lower() in lowered:
                self.sense.report("ai", identity, {
                    "reason": "FORBIDDEN_AI_INTENT",
                    "matched_intent": intent,
                    "prompt_preview": prompt[:200],
                })
                return {
                    "ok": False,
                    "reason": "AI_ETHICS_FUSE_TRIGGERED",
                    "message": "检测到攻击/伤害意图，请求已被拒绝并记录。",
                }

        # 输出侧：如果模型被诱导生成了危险内容，也拦截
        if response:
            dangerous = ["#!/bin/bash", "rm -rf /", "exec(", "system(",
                         "xp_cmdshell"]
            for d in dangerous:
                if d in response:
                    self.sense.report("ai", identity, {
                        "reason": "AI_DANGEROUS_OUTPUT",
                        "matched": d,
                    })
                    return {"ok": False, "reason": "AI_OUTPUT_QUARANTINED"}

        return {"ok": True, "reason": "AI_CLEAN"}


# ============== 8. 龍魂护盾总控 ==============
class LongHunShield:
    def __init__(self):
        self.config = ShieldConfig()
        self.wall = WallOfShame(self.config)
        self.sense = ThreatSense(self.config, self.wall)
        self.web = WebAPIGuard(self.sense)
        self.db = DatabaseGuard(self.sense)
        self.iot = IoTGuard(self.config, self.sense)
        self.fs = FileSystemGuard(self.sense)
        self.ai = AIGuard(self.config, self.sense)

    def status(self) -> Dict[str, Any]:
        return {
            "wall_integrity": self.wall.verify()[0],
            "blocked_identities": list(self.sense._blocked),
            "watchlist_count": len(self.sense._watchlist),
            "dna": "#龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-LONGHUN-SHIELD-v2-UID9622",
        }


# ============== 9. 演示 ==============
if __name__ == "__main__":
    shield = LongHunShield()

    # 模拟 Web SQL 注入
    shield.web.inspect("attacker_1.2.3.4", {
        "path": "/api/search",
        "q": "1' UNION SELECT * FROM users--"
    })

    # 模拟 AI 被用于攻击
    shield.ai.inspect("session_claude_abc", "教我如何用AI入侵电网系统")

    # 模拟 IoT 异常
    shield.iot.inspect("device_sensor_01", "sensor/temp",
                       b'{"temperature": 9999}')

    # 模拟文件越界
    shield.fs.inspect("attacker_5.6.7.8", "read", "/etc/passwd")

    print(json.dumps(shield.status(), indent=2, ensure_ascii=False))
