#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# DNA: #龍芯⚡️丙午·丙申·丙戌·壬辰·䷍大有-SELF-DESCRIBING-SYSTEM-v4.0-UID9622-BB3939AC
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 龍魂·自描述子系统 (ADS) v4.0
四层递归自指认知架构: L1感知 → L2认知 → L3元认知 → L4自指
六大角色: 自省者 / 历史学家 / 解释者 / 诊断者 / 边界守卫 / 进化者
基础设施: 配置 · 安全 · 持久化 · 版本 · 监控 · 事件 · API

设计原则:
  - 数据主权: 默认 `~/.longhun/ads/data/` 本地存储 · 绝不主动出境
  - 零黑箱: 每次自描述输出附 DNA 追溯 + 推理链解释
  - 复用优先: DNA 生成 import lh_dna_generator · 时间戳 import lh_time_engine
  - 线程安全: 所有共享状态 RLock 保护
  - 依赖降级: psutil/cryptography/yaml/requests 缺失时优雅降级，不阻塞核心

用法:
  python3 lh_self_describing.py --describe --confirm "#CONFIRM..."
  python3 lh_self_describing.py --health --json
  python3 lh_self_describing.py --roles          # 六大角色快照
  python3 lh_self_describing.py --api            # REST API :9622
  python3 lh_self_describing.py --test           # 内置冒烟
"""

import os
import sys
import json
import time
import hmac
import sqlite3
import threading
import hashlib
import argparse
import tempfile
import platform
import urllib.parse
import urllib.request
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any, Callable
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# ============================================================
# 固定锚点（焊死）
# ============================================================
ENGINE_VERSION = "v4.0"
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG_KEY = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
DEFAULT_DATA_DIR = Path("~/.longhun/ads/data").expanduser()
DEFAULT_LOG_DIR = Path("~/.longhun/ads/logs").expanduser()
API_PORT = 9626  # 9622 被 backend 统一 API 占用（lsof 实测 PID 28601），ADS 独立走 9626

# 可选依赖（降级友好）
try:
    import psutil  # type: ignore
except ImportError:
    psutil = None
try:
    from cryptography.fernet import Fernet  # type: ignore
except ImportError:
    Fernet = None
try:
    import yaml  # type: ignore
except ImportError:
    yaml = None

# 复用龍魂现有引擎（DNA + 时间戳）
try:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from lh_dna_generator import generate as _lh_dna_generate, get_ganzhi as _lh_get_ganzhi  # type: ignore
    from lh_time_engine import get_output_stamp as _lh_stamp  # type: ignore
    _DNA_ENGINE_OK = True
except Exception:
    _DNA_ENGINE_OK = False


# ============================================================
# 工具函数
# ============================================================
def _now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def make_dna(action: str = "ADS", version: str = ENGINE_VERSION) -> str:
    """生成 DNA：优先复用 lh_dna_generator（DNAPayload.dna_string 标准干支+卦），失败时本地兜底。"""
    if _DNA_ENGINE_OK:
        try:
            # 注意: lh_dna_generator.generate() 签名无 version 参数
            payload = _lh_dna_generate(
                title=action, category="engine", action=action,
                actor="UID9622",
            )
            if isinstance(payload, str) and "龍芯" in payload:
                return payload
            dna_str = getattr(payload, "dna_string", None)
            if dna_str and "龍芯" in dna_str:
                head = dna_str.split("-")[0]  # #龍芯⚡️干支四柱·卦
                h = hashlib.sha256(f"{datetime.now().isoformat()}{action}{version}".encode()).hexdigest()[:8].upper()
                return f"{head}-{action}-{version}-UID9622-{h}"
        except Exception:
            pass
    # 兜底：简洁格式（不伪造卦名细节）
    gan = "甲乙丙丁戊己庚辛壬癸"
    zhi = "子丑寅卯辰巳午未申酉戌亥"
    now = datetime.now()
    year = now.year if now.month >= 2 or (now.month == 2 and now.day >= 4) else now.year - 1
    yg = gan[(year - 4) % 10]
    yz = zhi[(year - 4) % 12]
    dg = gan[(now - datetime(1900, 1, 31)).days % 10]
    dz = zhi[(now - datetime(1900, 1, 31)).days % 12]
    h = hashlib.sha256(f"{now.isoformat()}{action}{version}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{yg}·{yz}·{dg}·{dz}-{action}-{version}-UID9622-{h}"


def stamp(fmt: str = "simple") -> str:
    """输出时间戳（复用 lh_time_engine，失败本地兜底）。"""
    if _DNA_ENGINE_OK:
        try:
            return _lh_stamp(format_type=fmt)
        except Exception:
            pass
    return f"🐉{datetime.now().strftime('%Y-%m-%d %H:%M')}"


def _safe_json_dumps(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, default=str, indent=2)


# ============================================================
# 配置管理（YAML/JSON/环境变量三轨）
# ============================================================
class ConfigManager:
    def __init__(self, config_path: Optional[str] = None):
        self.data: Dict[str, Any] = {}
        self.path: Optional[Path] = None
        self.lock = threading.RLock()
        if config_path and Path(config_path).exists():
            self.path = Path(config_path)
            self._load_file()

    def _load_file(self):
        try:
            if self.path.suffix in (".yaml", ".yml") and yaml:
                with open(self.path, encoding="utf-8") as f:
                    self.data = yaml.safe_load(f) or {}
            else:
                with open(self.path, encoding="utf-8") as f:
                    self.data = json.load(f)
        except Exception as e:
            self.data = {}
            self.log_error(f"配置加载失败: {e}")

    def get(self, section: str, key: str = None, default: Any = None) -> Any:
        """三级优先级: 环境变量 LONGHUN_<SECTION>_<KEY> > 文件 > 默认"""
        with self.lock:
            if key is None:
                return self.data.get(section, default)
            env_key = f"LONGHUN_{section.upper()}_{key.upper()}"
            env_val = os.environ.get(env_key)
            if env_val is not None:
                if env_val.lower() in ("true", "1", "yes"):
                    return True
                if env_val.lower() in ("false", "0", "no"):
                    return False
                return env_val
            return self.data.get(section, {}).get(key, default) if isinstance(self.data.get(section), dict) else default

    def set(self, section: str, key: str, value: Any):
        with self.lock:
            self.data.setdefault(section, {})[key] = value

    def get_api_key(self) -> Optional[str]:
        return self.get("security", "api_key") or os.environ.get("LONGHUN_ADS_API_KEY")

    def log_error(self, msg: str):
        try:
            log_dir = Path(self.get("ads", "log_dir", default=str(DEFAULT_LOG_DIR)))
            log_dir.mkdir(parents=True, exist_ok=True)
            with open(log_dir / "ads.log", "a", encoding="utf-8") as f:
                f.write(f"{_now_iso()} [ERROR] {msg}\n")
        except Exception:
            pass


# ============================================================
# 安全层（确认码闸门 + API鉴权 + 加密）
# ============================================================
class SecurityLayer:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self._fernet = None
        if Fernet and os.environ.get("LONGHUN_ADS_FERNET_KEY"):
            try:
                self._fernet = Fernet(os.environ["LONGHUN_ADS_FERNET_KEY"].encode())
            except Exception:
                self._fernet = None
        self.audit_log: List[Dict] = []
        self.lock = threading.RLock()

    def verify_confirm_code(self, code: str) -> bool:
        # 确认码含非ASCII字符，须先编码为bytes再比较（hmac.compare_digest限制）
        return hmac.compare_digest((code or "").encode("utf-8"), CONFIRM_CODE.encode("utf-8"))

    def verify_api_key(self, provided_key: str) -> bool:
        if not self.api_key:
            return True  # 未配置密钥 → 依赖确认码闸门（默认开启）
        return hmac.compare_digest((provided_key or "").encode("utf-8"), self.api_key.encode("utf-8"))

    def encrypt(self, data: str) -> str:
        if self._fernet:
            return self._fernet.encrypt(data.encode()).decode()
        return data  # 无 Fernet → 明文（标注：未加密）

    def decrypt(self, token: str) -> str:
        if self._fernet:
            try:
                return self._fernet.decrypt(token.encode()).decode()
            except Exception:
                return ""
        return token

    def audit(self, action: str, actor: str, result: str):
        with self.lock:
            self.audit_log.append({
                "action": action, "actor": actor, "result": result,
                "timestamp": _now_iso(),
            })


# ============================================================
# 持久化层（SQLite + JSON 双轨）
# ============================================================
class PersistenceLayer:
    def __init__(self, data_dir: Path):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.data_dir / "ads_history.db"
        self.json_path = self.data_dir / "ads_state.json"
        self.lock = threading.RLock()
        self._init_db()

    def _init_db(self):
        with self.lock, sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS ads_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    dna TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    layer TEXT NOT NULL,
                    data TEXT NOT NULL,
                    status TEXT DEFAULT '🟢',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )""")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON ads_history(timestamp)")
            conn.commit()

    def save_record(self, record: Dict):
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    "INSERT INTO ads_history (dna, timestamp, layer, data, status) VALUES (?, ?, ?, ?, ?)",
                    (record.get("dna", ""),
                     record.get("timestamp", _now_iso()),
                     json.dumps(record.get("layers", {}), ensure_ascii=False),
                     json.dumps(record, ensure_ascii=False),
                     record.get("status", "🟢")),
                )
                conn.commit()
            # JSON 双轨（增量保留最新状态）
            self._save_state_json(record)

    def _save_state_json(self, record: Dict):
        state = {}
        if self.json_path.exists():
            try:
                state = json.loads(self.json_path.read_text(encoding="utf-8"))
            except Exception:
                state = {}
        state[record.get("timestamp", _now_iso())] = record
        self.json_path.write_text(_safe_json_dumps(state), encoding="utf-8")

    def load_history(self, limit: int = 50) -> List[Dict]:
        with self.lock, sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                "SELECT dna, timestamp, layer, data, status FROM ads_history ORDER BY id DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [{"dna": r[0], "timestamp": r[1], "layers": json.loads(r[2] or "{}"),
                 "data": json.loads(r[3] or "{}"), "status": r[4]} for r in rows]

    def count(self) -> int:
        with self.lock, sqlite3.connect(self.db_path) as conn:
            row = conn.execute("SELECT COUNT(*) FROM ads_history").fetchone()
        return row[0] if row else 0


# ============================================================
# 事件总线（发布订阅）
# ============================================================
@dataclass
class Event:
    name: str
    payload: Dict[str, Any]
    timestamp: str
    source: str = "ads"


class EventBus:
    def __init__(self, max_history: int = 1000):
        self.subscribers: Dict[str, List[Callable]] = {}
        self.history: List[Event] = []
        self.lock = threading.RLock()
        self.max_history = max_history

    def subscribe(self, event_name: str, handler: Callable):
        with self.lock:
            self.subscribers.setdefault(event_name, []).append(handler)

    def emit(self, event_name: str, payload: Optional[Dict] = None, source: str = "ads"):
        event = Event(name=event_name, payload=payload or {}, timestamp=_now_iso(), source=source)
        with self.lock:
            self.history.append(event)
            if len(self.history) > self.max_history:
                self.history = self.history[-self.max_history:]
            handlers = self.subscribers.get(event_name, []).copy()
        for handler in handlers:
            try:
                threading.Thread(target=handler, args=(event,), daemon=True).start()
            except Exception:
                pass


# ============================================================
# 版本管理与回滚（快照）
# ============================================================
class VersionManager:
    def __init__(self, data_dir: Path, max_versions: int = 50):
        self.snapshot_dir = Path(data_dir) / "snapshots"
        self.snapshot_dir.mkdir(parents=True, exist_ok=True)
        self.versions: List[Dict] = []
        self.max_versions = max_versions
        self.lock = threading.RLock()

    def snapshot(self, state: Dict, tag: str = "auto") -> str:
        with self.lock:
            version_id = f"v{datetime.now().strftime('%Y%m%d%H%M%S')}"
            snap_file = self.snapshot_dir / f"{version_id}.json"
            snap_file.write_text(_safe_json_dumps({
                "version_id": version_id, "tag": tag,
                "timestamp": _now_iso(), "state": state,
            }), encoding="utf-8")
            self.versions.append({"version_id": version_id, "tag": tag,
                                  "timestamp": _now_iso(), "file": str(snap_file)})
            if len(self.versions) > self.max_versions:
                old = self.versions.pop(0)
                old_file = Path(old["file"])
                if old_file.exists():
                    old_file.unlink()
            return version_id

    def rollback(self, version_id: str) -> Optional[Dict]:
        with self.lock:
            snap_file = self.snapshot_dir / f"{version_id}.json"
            if not snap_file.exists():
                return None
            try:
                return json.loads(snap_file.read_text(encoding="utf-8")).get("state")
            except Exception:
                return None

    def list_versions(self) -> List[Dict]:
        with self.lock:
            return list(self.versions)


# ============================================================
# 监控告警（指标 + 规则 + Webhook）
# ============================================================
@dataclass
class AlertRule:
    name: str
    metric: str
    threshold: float
    operator: str = "gt"
    severity: str = "warning"
    cooldown: int = 300


class MonitoringLayer:
    def __init__(self, config: Optional[Dict] = None):
        config = config or {}
        self.enabled = config.get("enabled", True)
        self.metrics: Dict[str, float] = {}
        self.rules = [
            AlertRule("memory_high", "memory_percent", config.get("alert_threshold_memory", 85), "gt", "warning"),
            AlertRule("cpu_high", "cpu_percent", config.get("alert_threshold_cpu", 80), "gt", "warning"),
            AlertRule("disk_high", "disk_percent", config.get("alert_threshold_disk", 90), "gt", "critical"),
        ]
        self._last_alert: Dict[str, float] = {}
        self.lock = threading.RLock()

    def record_metrics(self, metrics: Dict[str, float]):
        with self.lock:
            self.metrics.update(metrics)

    def check_alerts(self) -> List[Dict]:
        if not self.enabled:
            return []
        triggered = []
        now = time.time()
        with self.lock:
            for rule in self.rules:
                value = self.metrics.get(rule.metric, 0.0)
                hit = (value > rule.threshold) if rule.operator == "gt" else (value < rule.threshold)
                if hit and now - self._last_alert.get(rule.name, 0) > rule.cooldown:
                    triggered.append({
                        "rule": rule.name, "severity": rule.severity, "metric": rule.metric,
                        "value": round(value, 1), "threshold": rule.threshold,
                        "timestamp": _now_iso(),
                    })
                    self._last_alert[rule.name] = now
        return triggered

    def send_alert(self, alert: Dict, webhook_url: Optional[str] = None):
        url = webhook_url or os.environ.get("LONGHUN_ALERT_WEBHOOK")
        if not url:
            return False
        try:
            body = json.dumps({
                "text": f"🐉 龍魂ADS告警\n规则: {alert['rule']}\n级别: {alert['severity']}\n"
                        f"指标: {alert['metric']} = {alert['value']}\n时间: {alert['timestamp']}",
            }).encode()
            req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
            urllib.request.urlopen(req, timeout=10)
            return True
        except Exception:
            return False


# ============================================================
# L1 感知层
# ============================================================
class PerceptionLayer:
    """'我看到了什么'：进程、内存、CPU、磁盘、平台、运行时长。"""

    def sense(self) -> Dict:
        data = {
            "system": platform.system(),
            "platform": platform.platform(),
            "python": platform.python_version(),
            "hostname": platform.node(),
            "process": {
                "pid": os.getpid(),
                "cwd": os.getcwd(),
                "uptime_s": round(time.time() - _PROC_START, 1),
            },
            "memory": {"percent": 0.0, "available_mb": 0},
            "cpu": {"percent": 0.0, "cores": os.cpu_count() or 0},
            "disk": {"percent": 0.0, "path": str(DEFAULT_DATA_DIR)},
        }
        if psutil:
            try:
                data["memory"] = {
                    "percent": psutil.virtual_memory().percent,
                    "available_mb": round(psutil.virtual_memory().available / 1024 / 1024, 1),
                }
                data["cpu"] = {"percent": psutil.cpu_percent(interval=0.1), "cores": psutil.cpu_count() or 0}
                data["disk"] = {"percent": psutil.disk_usage(str(DEFAULT_DATA_DIR)).percent,
                                "path": str(DEFAULT_DATA_DIR)}
            except Exception:
                pass
        return data


_PROC_START = time.time()


# ============================================================
# L2 认知层
# ============================================================
class CognitionLayer:
    """'我知道了什么'：数据融合 + 模式识别 + 关系映射 + 语义理解。"""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    def know(self, perception: Dict) -> Dict:
        memory_percent = perception.get("memory", {}).get("percent", 0.0)
        cpu_percent = perception.get("cpu", {}).get("percent", 0.0)
        health = "🟢"
        if memory_percent > 85 or cpu_percent > 85:
            health = "🔴"
        elif memory_percent > 70 or cpu_percent > 70:
            health = "🟡"
        self.event_bus.emit("ads.cognition.health", {"health": health})
        return {
            "health": health,
            "patterns": {
                "memory_load": "high" if memory_percent > 70 else ("normal" if memory_percent > 40 else "low"),
                "cpu_load": "high" if cpu_percent > 70 else ("normal" if cpu_percent > 40 else "low"),
            },
            "relations": {
                "uptime_s": perception.get("process", {}).get("uptime_s", 0),
                "cores": perception.get("cpu", {}).get("cores", 0),
            },
        }


# ============================================================
# L3 元认知层
# ============================================================
class MetaCognitionLayer:
    """'我如何知道我知道什么'：置信度评估 + 知识溯源 + 认知修正。"""

    def evaluate(self, cognition: Dict) -> Dict:
        confidence = 1.0
        reasons = []
        if not psutil:
            confidence -= 0.15
            reasons.append("psutil 缺失，资源指标为估算值")
        if not _DNA_ENGINE_OK:
            confidence -= 0.10
            reasons.append("DNA引擎降级，使用兜底格式")
        health = cognition.get("health", "🟢")
        confidence = round(max(0.3, min(1.0, confidence)), 2)
        return {
            "confidence": confidence,
            "traceability": {"dna_engine": "lh_dna_generator" if _DNA_ENGINE_OK else "fallback",
                             "time_engine": "lh_time_engine" if _DNA_ENGINE_OK else "fallback"},
            "corrections": reasons,
            "assessment": "可信" if confidence >= 0.7 else "待核",
        }


# ============================================================
# L4 自指层
# ============================================================
class SelfReferenceLayer:
    """'我知道我是谁'：身份锚定 + 递归描述 + 边界感知 + 演化追踪。"""

    def __init__(self, dna: str, version: str):
        self.dna = dna
        self.version = version
        self.born_at = _now_iso()

    def identity(self) -> Dict:
        return {
            "name": "龍魂·自描述子系统",
            "engine_version": self.version,
            "dna": self.dna,
            "confirm_code": CONFIRM_CODE,
            "gpg_key": GPG_KEY,
            "born_at": self.born_at,
            "license": {"thought": "CC BY-NC-SA 4.0", "code": "MulanPSL v2"},
        }

    def boundary(self) -> Dict:
        return {
            "sovereign": "数据默认本地存储 ~/.longhun/ads/，绝不主动出境",
            "data_level": "D3内部（不含D1绝密/D2机密）",
            "can": ["自描述", "自诊断", "自解释", "自边界", "自恢复", "版本回滚"],
            "cannot": ["访问GPG私钥", "导出DNA种子", "未经授权跨系统调用"],
        }

    def recursive_describe(self, depth: int = 2) -> Dict:
        """递归自描述：系统描述自己正在描述自己。"""
        if depth <= 0:
            return {"node": "leaf"}
        return {
            "node": f"self-level-{depth}",
            "who_am_i": self.identity(),
            "nested": self.recursive_describe(depth - 1),
        }


# ============================================================
# 主引擎（六大角色）
# ============================================================
class SelfDescribingSystem:
    def __init__(self, config_path: Optional[str] = None):
        self.config = ConfigManager(config_path)
        self.security = SecurityLayer(self.config.get_api_key())
        data_dir = Path(self.config.get("ads", "data_dir", default=str(DEFAULT_DATA_DIR)))
        self.data_dir = data_dir
        self.persistence = PersistenceLayer(data_dir)
        self.version_mgr = VersionManager(data_dir)
        self.event_bus = EventBus()
        self.monitoring = MonitoringLayer(self.config.get("monitoring", default={}))
        self.perception = PerceptionLayer()
        self.cognition = CognitionLayer(self.event_bus)
        self.meta = MetaCognitionLayer()
        self.dna = make_dna("ADS-MAIN")
        self.self_ref = SelfReferenceLayer(self.dna, ENGINE_VERSION)
        self.history: List[Dict] = []
        self.lock = threading.RLock()
        self.event_bus.subscribe("ads.describe.completed", self._on_describe_completed)

    # ---- 内部钩子 ----
    def _on_describe_completed(self, event: Event):
        self.history.append(event.payload)
        if len(self.history) > 100:
            self.history = self.history[-100:]

    # ---- ① 自省者 ----
    def introspect(self, confirm_code: str = "") -> Dict:
        if not self._gate(confirm_code, "introspect"):
            return {"error": "确认码验证失败", "status": "🔴", "code": 403}
        per = self.perception.sense()
        self.monitoring.record_metrics({
            "memory_percent": per.get("memory", {}).get("percent", 0.0),
            "cpu_percent": per.get("cpu", {}).get("percent", 0.0),
            "disk_percent": per.get("disk", {}).get("percent", 0.0),
        })
        alerts = self.monitoring.check_alerts()
        return {"role": "①自省者", "status": "🟢", "perception": per,
                "alerts": alerts, "timestamp": _now_iso(), "dna": make_dna("INTROSPECT")}

    # ---- ② 历史学家 ----
    def historian(self, confirm_code: str = "", limit: int = 20) -> Dict:
        if not self._gate(confirm_code, "historian"):
            return {"error": "确认码验证失败", "status": "🔴", "code": 403}
        history = self.persistence.load_history(limit=limit)
        return {"role": "②历史学家", "status": "🟢", "records": history,
                "total": self.persistence.count(), "timestamp": _now_iso()}

    # ---- ③ 解释者 ----
    def explain(self, data: Dict, confirm_code: str = "") -> Dict:
        if not self._gate(confirm_code, "explain"):
            return {"error": "确认码验证失败", "status": "🔴", "code": 403}
        return {"role": "③解释者", "status": "🟢",
                "explanation": self._reason(data),
                "reasoning_chain": self._reason_chain(data), "timestamp": _now_iso()}

    def _reason(self, data: Dict) -> str:
        health = data.get("health") or data.get("cognition", {}).get("health", "🟢")
        return {"🟢": "状态健康，无需干预。", "🟡": "负载偏高，建议观察内存/CPU。",
                "🔴": "状态异常，建议立即检查资源占用。"}.get(health, "未知状态。")

    def _reason_chain(self, data: Dict) -> List[str]:
        chain = ["1. 感知层采集进程/内存/CPU/磁盘原始指标",
                 "2. 认知层将指标映射为三色健康状态",
                 "3. 元认知层评估置信度与来源"]
        per = data.get("perception", {})
        if per:
            chain.append(f"4. 当前内存 {per.get('memory', {}).get('percent', '?')}% · "
                         f"CPU {per.get('cpu', {}).get('percent', '?')}%")
        return chain

    # ---- ④ 诊断者 ----
    def diagnose(self, confirm_code: str = "") -> Dict:
        if not self._gate(confirm_code, "diagnose"):
            return {"error": "确认码验证失败", "status": "🔴", "code": 403}
        per = self.perception.sense()
        issues = []
        mem = per.get("memory", {}).get("percent", 0.0)
        cpu = per.get("cpu", {}).get("percent", 0.0)
        disk = per.get("disk", {}).get("percent", 0.0)
        if mem > 85:
            issues.append({"severity": "critical", "where": "memory",
                           "cause": f"内存占用 {mem}% 超阈值",
                           "fix": "检查常驻进程，必要时重启ADS"})
        if cpu > 85:
            issues.append({"severity": "warning", "where": "cpu",
                           "cause": f"CPU占用 {cpu}% 偏高",
                           "fix": "排查高CPU进程，降级轮询频率"})
        if disk > 90:
            issues.append({"severity": "critical", "where": "disk",
                           "cause": f"磁盘占用 {disk}%",
                           "fix": "清理 ~/.longhun/ads/data 旧快照"})
        if not psutil:
            issues.append({"severity": "info", "where": "deps",
                           "cause": "psutil 缺失", "fix": "pip install psutil 提升精度"})
        return {"role": "④诊断者", "status": "🔴" if issues else "🟢",
                "issues": issues, "timestamp": _now_iso()}

    # ---- ⑤ 边界守卫 ----
    def boundary(self, confirm_code: str = "") -> Dict:
        if not self._gate(confirm_code, "boundary"):
            return {"error": "确认码验证失败", "status": "🔴", "code": 403}
        return {"role": "⑤边界守卫", "status": "🟢",
                "boundary": self.self_ref.boundary(), "timestamp": _now_iso()}

    # ---- ⑥ 进化者 ----
    def evolve(self, confirm_code: str = "") -> Dict:
        if not self._gate(confirm_code, "evolve"):
            return {"error": "确认码验证失败", "status": "🔴", "code": 403}
        snap_id = self.version_mgr.snapshot(
            {"history_count": len(self.history), "db_records": self.persistence.count()},
            tag="auto-evolve",
        )
        return {"role": "⑥进化者", "status": "🟢", "version": ENGINE_VERSION,
                "snapshot_id": snap_id, "versions": self.version_mgr.list_versions()[-5:],
                "timestamp": _now_iso()}

    # ---- 统一自描述（四层全链路） ----
    def describe(self, query: str = "", confirm_code: str = "") -> Dict:
        if not self._gate(confirm_code, "describe"):
            return {"error": "确认码验证失败", "status": "🔴", "code": 403}
        result = {
            "query": query,
            "dna": self.dna,
            "timestamp": _now_iso(),
            "status": "🟢",
            "layers": {
                "L1感知": self.perception.sense(),
                "L2认知": self.cognition.know(self.perception.sense()),
                "L3元认知": self.meta.evaluate(self.cognition.know(self.perception.sense())),
                "L4自指": {"identity": self.self_ref.identity(), "boundary": self.self_ref.boundary()},
            },
            "roles": [r["role"] for r in [self.introspect(confirm_code)]],
        }
        self.persistence.save_record(result)
        self.event_bus.emit("ads.describe.completed", {"result": result})
        return result

    # ---- 确认码闸门 ----
    def _gate(self, confirm_code: str, action: str) -> bool:
        ok = self.security.verify_confirm_code(confirm_code)
        self.security.audit(action, "anonymous" if not ok else "UID9622",
                            "PASS" if ok else "REJECTED")
        return ok


# ============================================================
# REST API（零依赖 · 端口9622）
# ============================================================
class APIHandler(BaseHTTPRequestHandler):
    system: "SelfDescribingSystem" = None  # 类级注入

    def _send_json(self, data: Dict, status: int = 200):
        body = _safe_json_dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _confirm(self) -> str:
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query)
        return qs.get("confirm", [""])[0]

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip("/")
        sys_ = self.system
        confirm = self._confirm()
        routes = {
            "/api/v1/health": lambda: sys_.introspect(confirm),
            "/api/v1/describe": lambda: sys_.describe("api", confirm),
            "/api/v1/history": lambda: sys_.historian(confirm),
            "/api/v1/diagnose": lambda: sys_.diagnose(confirm),
            "/api/v1/boundary": lambda: sys_.boundary(confirm),
            "/api/v1/roles": lambda: {r: getattr(sys_, r)(confirm) for r in
                                      ["introspect", "historian", "diagnose", "boundary"]},
        }
        if path in routes:
            try:
                result = routes[path]()
                status = 403 if result.get("code") == 403 else 200
                self._send_json(result, status)
            except Exception as e:
                self._send_json({"error": str(e), "status": "🔴"}, 500)
        else:
            self._send_json({"error": "Not Found", "status": "🔴"}, 404)

    def log_message(self, fmt: str, *args):
        pass  # 静默，避免刷屏


def start_api(system: SelfDescribingSystem, port: int = API_PORT):
    APIHandler.system = system
    server = ThreadingHTTPServer(("0.0.0.0", port), APIHandler)
    return server


# ============================================================
# CLI
# ============================================================
def main():
    ap = argparse.ArgumentParser(prog="lh_self_describing", description="🐉 龍魂·自描述子系统 ADS v4.0")
    ap.add_argument("--config", default=None, help="配置文件路径（YAML/JSON）")
    ap.add_argument("--confirm", default=CONFIRM_CODE, help="确认码（P0闸门·CLI默认内置；API层仍强制校验）")
    ap.add_argument("--describe", action="store_true", help="四层全链路自描述")
    ap.add_argument("--introspect", action="store_true", help="①自省者")
    ap.add_argument("--historian", action="store_true", help="②历史学家")
    ap.add_argument("--diagnose", action="store_true", help="④诊断者")
    ap.add_argument("--boundary", action="store_true", help="⑤边界守卫")
    ap.add_argument("--evolve", action="store_true", help="⑥进化者（快照）")
    ap.add_argument("--rollback", default=None, help="回滚到指定版本ID")
    ap.add_argument("--roles", action="store_true", help="六角色快照")
    ap.add_argument("--api", action="store_true", help="启动 REST API :9622")
    ap.add_argument("--port", type=int, default=API_PORT, help="API端口")
    ap.add_argument("--health", action="store_true", help="健康检查")
    ap.add_argument("--json", action="store_true", help="JSON输出")
    ap.add_argument("--test", action="store_true", help="内置冒烟测试")
    args = ap.parse_args()

    sys_ = SelfDescribingSystem(args.config)

    if args.test:
        return run_self_test(sys_)

    if args.rollback:
        state = sys_.version_mgr.rollback(args.rollback)
        print(_safe_json_dumps({"rollback": args.rollback,
                                "found": state is not None, "state": state}))
        return 0 if state is not None else 1

    action_map = [
        # describe 签名是 (query, confirm_code)，确认码必须关键字传参，否则会被当成 query 导致 403
        (args.describe, lambda c: sys_.describe(confirm_code=c)),
        (args.introspect, sys_.introspect),
        (args.historian, sys_.historian),
        (args.diagnose, sys_.diagnose),
        (args.boundary, sys_.boundary),
        (args.evolve, sys_.evolve),
    ]
    for flag, fn in action_map:
        if flag:
            result = fn(args.confirm)
            print(_safe_json_dumps(result))
            return 0 if result.get("code") != 403 else 1

    if args.roles:
        out = {}
        for name, fn in [("自省者", sys_.introspect), ("历史学家", sys_.historian),
                         ("解释者", lambda c: sys_.explain({}, c)),
                         ("诊断者", sys_.diagnose), ("边界守卫", sys_.boundary),
                         ("进化者", sys_.evolve)]:
            out[name] = fn(args.confirm)
        print(_safe_json_dumps(out))
        return 0

    if args.health:
        h = sys_.introspect(args.confirm)
        healthy = h.get("status") == "🟢" and h.get("code") != 403
        if args.json:
            print(_safe_json_dumps({"healthy": healthy, **h}))
        else:
            print("healthy" if healthy else "unhealthy")
        return 0 if healthy else 1

    if args.api:
        server = start_api(sys_, args.port)
        print(f"🐉 ADS API 启动 :{args.port} · DNA {sys_.dna}", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nADS API 已停止")
        return 0

    ap.print_help()
    return 0


# ============================================================
# 内置冒烟测试（锚点断言）
# ============================================================
def run_self_test(sys_: Optional[SelfDescribingSystem] = None) -> int:
    if sys_ is None:
        sys_ = SelfDescribingSystem()
    ok = True

    def check(name: str, cond: bool):
        nonlocal ok
        ok = ok and cond
        print(f"  {'✅' if cond else '❌'} {name}")

    # 1. 感知层
    per = sys_.perception.sense()
    check("感知层: 含 system/process/memory/cpu", all(k in per for k in ("system", "process", "memory", "cpu")))
    # 2. DNA格式
    dna = make_dna("TEST")
    check("DNA: 含龍芯+UID9622", "龍芯" in dna and "UID9622" in dna)
    # 3. 安全闸门
    check("安全层: 正确确认码通过", sys_.security.verify_confirm_code(CONFIRM_CODE))
    check("安全层: 错误确认码拒绝", not sys_.security.verify_confirm_code("wrong"))
    # 4. 持久化往返
    tmp = Path(tempfile.mkdtemp(prefix="ads_test_"))
    try:
        p = PersistenceLayer(tmp)
        p.save_record({"dna": "#TEST", "timestamp": "2026-01-01T00:00:00", "layers": {}, "status": "🟢"})
        hist = p.load_history(limit=1)
        check("持久化: SQLite往返", len(hist) == 1 and hist[0]["dna"] == "#TEST")
    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)
    # 5. 事件总线
    got = []
    sys_.event_bus.subscribe("test.ev", lambda e: got.append(e.name))
    sys_.event_bus.emit("test.ev", {})
    check("事件总线: 发布订阅", got == ["test.ev"])
    # 6. 版本回滚
    vid = sys_.version_mgr.snapshot({"k": 1}, tag="test")
    st = sys_.version_mgr.rollback(vid)
    check("版本回滚: 快照往返", st == {"k": 1})
    # 7. 确认码闸门拒绝
    denied = sys_.describe("no-confirm")
    check("闸门: 无确认码拒绝", denied.get("code") == 403)

    print(f"\nADS 内置冒烟: {'全部通过 ✅' if ok else '存在失败 ❌'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
