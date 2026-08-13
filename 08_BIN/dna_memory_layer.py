#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
🧬 UID9622 · DNA记忆连接层 | 跨窗口全域记忆同步系统 v2.0

DNA: #龍芯⚡️丙午·乙未·戊戌·申时·☵坎-DNA-MEMORY-SYNC-v2.0-KUNPENG-HUB-a3c4e5f6
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

v2.0 更新:
  - 🔥 鲲鹏归一: store后自动推送、retrieve优先拉取、本地缓存离线兜底
  - 🔥 sync命令: 手动全量同步（推未同步+拉最新）
  - 🔥 --offline: 强制离线模式
  - 🔥 网络不可用自动降级

设计原则：
  1. 公开透明 — 所有记忆操作可审计
  2. 追加不覆盖 — 不删除、不篡改已有记忆
  3. 版本化存储 — 每次写入生成新版本，旧版永久保留
  4. DNA不得抹除 — 每条记忆带DNA追溯码，永不可移除
  5. 本地优先 — 数据主权在本地，云端只做同步中转
  6. 鲲鹏归一 — 本地操作后自动归一到鲲鹏中枢
"""

import json
import hashlib
import hmac
import os
import sys
import time
import uuid
import platform
import subprocess
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Optional
from dataclasses import dataclass, field, asdict

# ═══════════════════════════════════════════════
# 常量·DNA焊死
# ═══════════════════════════════════════════════

CST = timezone(timedelta(hours=8))

IDENTITY = {
    "uid": "UID9622",
    "sovereign": "ZHUGEXIN",
    "account": "fireroot.lad@outlook.com",
    "username": "🚀lucky｜UID9622",
    "gpg": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
    "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
    "device_bind": "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL",
}

VERSION = "v2.0"

MEMORY_DIR = Path.home() / ".longhun" / "memory_sync"
MEMORY_DIR.mkdir(parents=True, exist_ok=True)

MEMORY_INDEX_FILE = MEMORY_DIR / "memory_index.json"
MEMORY_STORE_DIR = MEMORY_DIR / "stores"
MEMORY_STORE_DIR.mkdir(parents=True, exist_ok=True)
AUDIT_LOG_FILE = MEMORY_DIR / "audit_log.jsonl"
SYNC_STATE_FILE = MEMORY_DIR / "sync_state.json"  # v2.0: 同步状态

# ═══════════════════════════════════════════════
# 鲲鹏配置
# ═══════════════════════════════════════════════

KUNPENG_HOST = os.environ.get("KUNPENG_HOST", "119.13.90.27:8080")
KUNPENG_SYNC_URL = f"http://{KUNPENG_HOST}/cnsh"
KUNPENG_TIMEOUT = 10  # 秒

# Token 加载（与记忆API共用）
def _load_sync_token() -> str:
    for f in (
        Path.home() / ".longhun" / ".memory_token",
        Path(__file__).resolve().parent.parent / ".codebuddy" / "memory" / ".api_token",
    ):
        if f.exists():
            t = f.read_text().strip()
            if t:
                return t
    return ""

SYNC_TOKEN = _load_sync_token()

# ═══════════════════════════════════════════════
# 天干地支时间戳引擎（公开算法）
# ═══════════════════════════════════════════════

TIAN_GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
DI_ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
SHENG_XIAO = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
BA_GUA = ["乾", "兑", "离", "震", "巽", "坎", "艮", "坤"]


def _year_ganzhi(year: int) -> str:
    base = (year - 4) % 60
    return TIAN_GAN[base % 10] + DI_ZHI[base % 12]


def _month_ganzhi(year: int, month: int) -> str:
    year_gan = TIAN_GAN[(year - 4) % 10]
    gan_index = TIAN_GAN.index(year_gan)
    month_gan_index = (gan_index * 2 + month - 1) % 10
    month_zhi_index = (month + 1) % 12
    return TIAN_GAN[month_gan_index] + DI_ZHI[month_zhi_index]


def _day_ganzhi(year: int, month: int, day: int) -> str:
    import calendar
    days = 0
    for y in range(2000, year):
        days += 366 if calendar.isleap(y) else 365
    for m in range(1, month):
        days += calendar.monthrange(year, m)[1]
    days += day - 1
    offset = days % 60
    return TIAN_GAN[offset % 10] + DI_ZHI[offset % 12]


def _hour_zhi(hour: int) -> str:
    return DI_ZHI[((hour + 1) // 2) % 12]


def _hour_ganzhi(day_gan: str, hour: int) -> str:
    gan_index = TIAN_GAN.index(day_gan)
    hour_zhi_index = DI_ZHI.index(_hour_zhi(hour))
    hour_gan_index = (gan_index * 2 + hour_zhi_index) % 10
    return TIAN_GAN[hour_gan_index] + DI_ZHI[hour_zhi_index]


def generate_dna_timestamp(dt: Optional[datetime] = None) -> str:
    if dt is None:
        dt = datetime.now(CST)
    year_gz = _year_ganzhi(dt.year)
    month_gz = _month_ganzhi(dt.year, dt.month)
    day_gz = _day_ganzhi(dt.year, dt.month, dt.day)
    day_gan_char = day_gz[0]
    hour_gz = _hour_ganzhi(day_gan_char, dt.hour)
    return f"{year_gz}·{month_gz}·{day_gz}·{hour_gz}"


def generate_dna(module: str, action: str, content: str) -> str:
    ts = generate_dna_timestamp()
    content_hash = hashlib.sha256(content.encode()).hexdigest()[:8]
    dt = datetime.now(CST)
    gua_index = (dt.day - 1) % 8
    gua = BA_GUA[gua_index]
    return f"#龍芯⚡️{ts}·☰{gua}-{module}-{action}-{content_hash}"


# ═══════════════════════════════════════════════
# 设备指纹引擎
# ═══════════════════════════════════════════════

def get_device_fingerprint() -> str:
    components = [
        platform.node(),
        platform.machine(),
        platform.processor(),
        str(uuid.getnode()),
    ]
    if sys.platform == "darwin":
        try:
            hw_uuid = subprocess.check_output(
                ["system_profiler", "SPHardwareDataType"],
                text=True, stderr=subprocess.DEVNULL
            )
            components.append(hw_uuid)
        except Exception:
            pass
    return hashlib.sha256("|".join(components).encode()).hexdigest()[:16]


def get_device_name() -> str:
    return platform.node() or f"Device-{uuid.getnode() % 10000}"


# ═══════════════════════════════════════════════
# 数据模型
# ═══════════════════════════════════════════════

@dataclass
class MemoryEntry:
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    dna: str = ""
    timestamp: str = ""
    device: str = ""
    device_fp: str = ""
    session_id: str = ""
    topic: str = ""
    content: str = ""
    priority: str = "P2"
    tags: list = field(default_factory=list)
    source_window: str = ""
    version: int = 1
    parent_dna: str = ""
    checksum: str = ""
    encrypted: bool = False       # v2.0
    synced_to_kunpeng: bool = False  # v2.0

    def compute_checksum(self) -> str:
        data = json.dumps({
            "content": self.content,
            "topic": self.topic,
            "timestamp": self.timestamp,
            "device": self.device,
        }, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(data.encode()).hexdigest()[:16]


@dataclass
class MemoryIndex:
    version: str = "v2.0"
    device_fingerprints: list = field(default_factory=list)
    last_sync: str = ""
    entries: list = field(default_factory=list)
    audit_count: int = 0


# ═══════════════════════════════════════════════
# 鲲鹏同步桥接器 v2.0
# ═══════════════════════════════════════════════

class KunpengSyncBridge:
    """鲲鹏记忆同步桥接器 — 本地↔鲲鹏双向同步"""

    def __init__(self):
        self.base_url = KUNPENG_SYNC_URL
        self.token = SYNC_TOKEN
        self._online: Optional[bool] = None

    def _request(self, method: str, path: str, data: dict = None) -> Optional[dict]:
        """发送带Token的HTTPS请求"""
        url = f"{self.base_url}{path}"
        body = json.dumps(data).encode() if data else None
        headers = {
            "Content-Type": "application/json",
            "X-API-Token": self.token,
        }
        req = urllib.request.Request(url, data=body, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=KUNPENG_TIMEOUT) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                self._online = True
                return result
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")[:200]
            self._online = True  # 服务器可达但拒绝
            return {"error": True, "status": e.code, "message": body}
        except (urllib.error.URLError, OSError, Exception):
            self._online = False
            return None

    def is_online(self) -> bool:
        """检测鲲鹏是否可达"""
        if self._online is not None:
            return self._online
        result = self._request("GET", "/api/memory/stats")
        return self._online if self._online is not None else False

    def push_entry(self, entry: MemoryEntry) -> bool:
        """推送单条记忆到鲲鹏 CNSH IDE 知识库"""
        payload = {
            "content": entry.content,
            "category": entry.topic or "general",
            "tags": entry.tags or [],
            "source": entry.source_window or "dna_memory_layer",
            "dna": entry.dna,
            "metadata": {
                "device": entry.device or "",
                "local_id": entry.id,
                "checksum": entry.checksum,
                "priority": entry.priority,
                "session_id": entry.session_id,
            },
        }
        result = self._request("POST", "/api/memory/store", payload)
        if result is None:
            return False
        return result.get("success", False)

    def pull_entries(self, limit: int = 50, since: str = "") -> Optional[list]:
        """从鲲鹏 CNSH IDE 知识库检索最近记忆"""
        # 先尝试空查询拉取最新（CNSH IDE search 需要 query，用 since 做查询词兜底）
        query = since if since else "龍芯"
        payload = {"query": query, "top_k": min(limit, 20)}
        result = self._request("POST", "/api/memory/search", payload)
        if result is None:
            return None
        if not result.get("success"):
            return []
        items = result.get("results", [])
        return [
            {
                "entry_id": item.get("entry_id", ""),
                "dna": item.get("dna", ""),
                "content": item.get("content", ""),
                "category": item.get("category", "general"),
                "tags": item.get("tags", []),
                "source": item.get("source", "kunpeng"),
                "created_at": item.get("created_at", ""),
            }
            for item in items
        ]

    def get_summary(self) -> Optional[dict]:
        """从鲲鹏获取全域摘要"""
        return self._request("GET", "/api/memory/stats")

    def get_stats(self) -> Optional[dict]:
        """从鲲鹏获取统计"""
        return self._request("GET", "/api/memory/stats")

    def health(self) -> Optional[dict]:
        """鲲鹏健康检查"""
        return self._request("GET", "/api/memory/stats")


# ═══════════════════════════════════════════════
# 记忆存储引擎 v2.0
# ═══════════════════════════════════════════════

class MemoryStore:
    """本地记忆存储引擎 + 鲲鹏同步"""

    def __init__(self, offline: bool = False):
        self.device_fp = get_device_fingerprint()
        self.device_name = get_device_name()
        self.offline = offline
        self.kunpeng = KunpengSyncBridge() if not offline else None
        self._ensure_index()

    def _ensure_index(self):
        if not MEMORY_INDEX_FILE.exists():
            idx = MemoryIndex(
                device_fingerprints=[self.device_fp],
                last_sync=datetime.now(CST).isoformat(),
            )
            self._save_index(idx)

    def _load_index(self) -> MemoryIndex:
        with open(MEMORY_INDEX_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return MemoryIndex(**data)

    def _save_index(self, idx: MemoryIndex):
        with open(MEMORY_INDEX_FILE, "w", encoding="utf-8") as f:
            json.dump(asdict(idx), f, ensure_ascii=False, indent=2)

    def _audit(self, action: str, dna: str, detail: str):
        log_entry = {
            "timestamp": datetime.now(CST).isoformat(),
            "action": action,
            "dna": dna,
            "detail": detail,
            "device": self.device_name,
            "device_fp": self.device_fp,
        }
        with open(AUDIT_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    def _load_sync_state(self) -> dict:
        if SYNC_STATE_FILE.exists():
            return json.loads(SYNC_STATE_FILE.read_text("utf-8"))
        return {"last_push": "", "last_pull": "", "unsynced_ids": []}

    def _save_sync_state(self, state: dict):
        SYNC_STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), "utf-8")

    def store(self, topic: str, content: str, priority: str = "P2",
              tags: list = None, session_id: str = "") -> MemoryEntry:
        """存储一条新记忆（追加模式，自动推鲲鹏）"""
        entry = MemoryEntry(
            topic=topic,
            content=content,
            priority=priority,
            tags=tags or [],
            session_id=session_id or uuid.uuid4().hex[:8],
            device=self.device_name,
            device_fp=self.device_fp,
            timestamp=datetime.now(CST).isoformat(),
            source_window=f"{self.device_name}:{os.getpid()}",
        )
        entry.dna = generate_dna("MEMORY", "STORE", content)
        entry.checksum = entry.compute_checksum()

        # 本地存储
        store_file = MEMORY_STORE_DIR / f"{entry.id}.json"
        with open(store_file, "w", encoding="utf-8") as f:
            json.dump(asdict(entry), f, ensure_ascii=False, indent=2)

        # 更新本地索引
        idx = self._load_index()
        idx.entries.append({
            "id": entry.id,
            "dna": entry.dna,
            "topic": entry.topic,
            "priority": entry.priority,
            "timestamp": entry.timestamp,
            "device": entry.device,
        })
        idx.audit_count += 1
        self._save_index(idx)

        # 审计
        self._audit("STORE", entry.dna, f"存储记忆: {topic}")

        # 自动推鲲鹏
        if not self.offline and self.kunpeng:
            pushed = self.kunpeng.push_entry(entry)
            entry.synced_to_kunpeng = pushed
            if pushed:
                self._audit("SYNC_PUSH", entry.dna, f"已推鲲鹏: {topic}")
                # 更新存储文件中的同步状态
                entry_dict = asdict(entry)
                with open(store_file, "w", encoding="utf-8") as f:
                    json.dump(entry_dict, f, ensure_ascii=False, indent=2)
            else:
                # 标记未同步
                state = self._load_sync_state()
                if entry.id not in state.get("unsynced_ids", []):
                    state.setdefault("unsynced_ids", []).append(entry.id)
                self._save_sync_state(state)
                self._audit("SYNC_DEFER", entry.dna, f"鲲鹏不可达，延后同步: {topic}")
        elif self.offline:
            # 离线模式标记
            state = self._load_sync_state()
            if entry.id not in state.get("unsynced_ids", []):
                state.setdefault("unsynced_ids", []).append(entry.id)
            self._save_sync_state(state)

        return entry

    def retrieve(self, topic: str = "", priority: str = "",
                 limit: int = 10, days: int = 7,
                 prefer_kunpeng: bool = True) -> list:
        """检索记忆（优先鲲鹏，本地兜底）"""
        # 尝试从鲲鹏拉取
        kunpeng_entries = []
        if prefer_kunpeng and not self.offline and self.kunpeng:
            pulled = self.kunpeng.pull_entries(limit=limit)
            if pulled is not None:
                kunpeng_entries = pulled

        # 合并本地索引
        idx = self._load_index()
        local_entries = idx.entries

        # 去重：以 DNA 为键，鲲鹏优先
        seen_dna = set()
        merged = []
        for e in kunpeng_entries:
            dna = e.get("dna", "")
            if dna and dna not in seen_dna:
                seen_dna.add(dna)
                merged.append(e)

        for meta in local_entries:
            dna = meta.get("dna", "")
            if dna not in seen_dna:
                seen_dna.add(dna)
                store_file = MEMORY_STORE_DIR / f"{meta['id']}.json"
                if store_file.exists():
                    merged.append(json.loads(store_file.read_text("utf-8")))
                else:
                    merged.append(meta)

        # 过滤
        if priority:
            merged = [e for e in merged if e.get("priority") == priority]
        if topic:
            merged = [e for e in merged if topic.lower() in e.get("topic", "").lower()]

        merged.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        return merged[:limit]

    def get_last_session(self) -> Optional[dict]:
        recent = self.retrieve(limit=1)
        return recent[0] if recent else None

    def verify_integrity(self) -> dict:
        idx = self._load_index()
        results = {
            "total": len(idx.entries),
            "valid": 0, "corrupted": 0, "missing": 0,
            "dna_intact": 0, "details": [],
        }
        for meta in idx.entries:
            store_file = MEMORY_STORE_DIR / f"{meta['id']}.json"
            if not store_file.exists():
                results["missing"] += 1
                results["details"].append({"id": meta["id"], "status": "文件丢失"})
                continue
            with open(store_file, "r", encoding="utf-8") as f:
                entry = json.load(f)
            original_checksum = entry.get("checksum", "")
            computed = hashlib.sha256(
                json.dumps({
                    "content": entry.get("content", ""),
                    "topic": entry.get("topic", ""),
                    "timestamp": entry.get("timestamp", ""),
                    "device": entry.get("device", ""),
                }, sort_keys=True, ensure_ascii=False).encode()
            ).hexdigest()[:16]
            if original_checksum == computed:
                results["valid"] += 1
                if entry.get("dna", ""):
                    results["dna_intact"] += 1
            else:
                results["corrupted"] += 1
                results["details"].append({
                    "id": meta["id"], "status": "校验和不匹配",
                })
        return results

    def summary(self) -> str:
        """生成记忆摘要（优先鲲鹏）"""
        lines = [f"🧬 UID9622 记忆同步系统 {VERSION}"]

        # 鲲鹏信息
        if not self.offline and self.kunpeng:
            kp_summary = self.kunpeng.get_summary()
            if kp_summary:
                lines.extend([
                    f"☁️ 鲲鹏中枢: {KUNPENG_HOST}",
                    f"   全域记忆: {kp_summary.get('total_synced', 0)} 条",
                    f"   设备数:   {kp_summary.get('devices', 0)}",
                    f"   最后同步: {kp_summary.get('last_sync', '')[:19]}",
                    "",
                ])
            else:
                lines.append("☁️ 鲲鹏: 不可达（本地模式）")
                lines.append("")
        else:
            lines.append("📴 离线模式")
            lines.append("")

        # 本地信息
        idx = self._load_index()
        lines.append(f"💻 本地: {self.device_name} ({self.device_fp})")
        lines.append(f"   本地记忆: {len(idx.entries)} 条")

        # 未同步计数
        state = self._load_sync_state()
        unsynced = len(state.get("unsynced_ids", []))
        if unsynced:
            lines.append(f"   ⚠️ 待同步: {unsynced} 条（运行 sync 命令补推）")

        lines.append("")

        # 最近记忆
        recent = self.retrieve(limit=5)
        if recent:
            lines.append("📋 最近记忆:")
            for entry in recent:
                origin = "☁️" if entry.get("synced_to_kunpeng") else "💻"
                lines.append(
                    f"  {origin} [{entry.get('priority', 'P2')}] "
                    f"{entry.get('timestamp', '')[:16]} | {entry.get('topic', '')[:40]}"
                )
        else:
            lines.append("📋 暂无记忆记录。")

        return "\n".join(lines)

    def sync(self) -> dict:
        """手动全量同步: 推未同步 → 拉最新"""
        result = {"pushed": 0, "pulled": 0, "errors": 0, "kunpeng_online": False}

        if not self.kunpeng:
            result["error"] = "离线模式，无法同步"
            return result

        if not self.kunpeng.is_online():
            result["error"] = "鲲鹏不可达"
            return result

        result["kunpeng_online"] = True

        # 1. 推送未同步的本地记忆
        state = self._load_sync_state()
        unsynced = state.get("unsynced_ids", [])
        still_unsynced = []

        for eid in unsynced:
            store_file = MEMORY_STORE_DIR / f"{eid}.json"
            if not store_file.exists():
                continue
            entry_data = json.loads(store_file.read_text("utf-8"))
            entry = MemoryEntry(**{k: v for k, v in entry_data.items()
                                   if k in MemoryEntry.__dataclass_fields__})
            if self.kunpeng.push_entry(entry):
                result["pushed"] += 1
                # 更新本地文件标记
                entry.synced_to_kunpeng = True
                with open(store_file, "w", encoding="utf-8") as f:
                    json.dump(asdict(entry), f, ensure_ascii=False, indent=2)
                self._audit("SYNC_PUSH", entry.dna, f"补推成功: {entry.topic}")
            else:
                result["errors"] += 1
                still_unsynced.append(eid)

        state["unsynced_ids"] = still_unsynced
        state["last_push"] = datetime.now(CST).isoformat()

        # 2. 拉取鲲鹏最新记忆到本地
        pulled = self.kunpeng.pull_entries(limit=200, since=state.get("last_pull", ""))
        if pulled:
            idx = self._load_index()
            local_dnas = {e.get("dna", "") for e in idx.entries}
            for remote in pulled:
                r_dna = remote.get("dna", "")
                if r_dna and r_dna not in local_dnas:
                    # 保存到本地
                    store_file = MEMORY_STORE_DIR / f"{remote.get('id', uuid.uuid4().hex[:12])}.json"
                    remote["synced_to_kunpeng"] = True
                    with open(store_file, "w", encoding="utf-8") as f:
                        json.dump(remote, f, ensure_ascii=False, indent=2)
                    idx.entries.append({
                        "id": remote.get("id"),
                        "dna": remote.get("dna"),
                        "topic": remote.get("topic"),
                        "priority": remote.get("priority"),
                        "timestamp": remote.get("timestamp"),
                        "device": remote.get("device"),
                    })
                    result["pulled"] += 1
            self._save_index(idx)

        state["last_pull"] = datetime.now(CST).isoformat()
        self._save_sync_state(state)

        self._audit("SYNC_FULL", f"sync-{datetime.now(CST).strftime('%Y%m%d%H%M%S')}",
                     f"推{result['pushed']}条 拉{result['pulled']}条 错{result['errors']}条")

        # 3. 更新本地索引的last_sync
        idx = self._load_index()
        idx.last_sync = datetime.now(CST).isoformat()
        self._save_index(idx)

        return result

    def stats(self) -> dict:
        idx = self._load_index()
        prio_counts = {}
        for e in idx.entries:
            p = e.get("priority", "P2")
            prio_counts[p] = prio_counts.get(p, 0) + 1
        state = self._load_sync_state()
        kunpeng_stats = {}
        if not self.offline and self.kunpeng:
            kps = self.kunpeng.get_stats()
            if kps:
                kunpeng_stats = kps
        return {
            "local_total": len(idx.entries),
            "audit_count": idx.audit_count,
            "devices": len(set(e.get("device", "") for e in idx.entries)),
            "by_priority": prio_counts,
            "unsynced": len(state.get("unsynced_ids", [])),
            "kunpeng": kunpeng_stats,
        }


# ═══════════════════════════════════════════════
# 命令行入口 v2.0
# ═══════════════════════════════════════════════

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="🧬 UID9622 · DNA记忆连接层 v2.0 | 鲲鹏归一"
    )
    parser.add_argument("--offline", action="store_true",
                        help="强制离线模式，不连接鲲鹏")
    sub = parser.add_subparsers(dest="command")

    # store
    sp = sub.add_parser("store", help="存储新记忆（自动推鲲鹏）")
    sp.add_argument("--topic", required=True, help="记忆主题")
    sp.add_argument("--content", required=True, help="记忆内容")
    sp.add_argument("--priority", default="P2", choices=["P0", "P1", "P2"])
    sp.add_argument("--tags", nargs="*", default=[])

    # retrieve
    rp = sub.add_parser("retrieve", help="检索记忆（优先鲲鹏）")
    rp.add_argument("--topic", default="")
    rp.add_argument("--priority", default="", choices=["", "P0", "P1", "P2"])
    rp.add_argument("--limit", type=int, default=10)

    # sync
    sub.add_parser("sync", help="手动全量同步（推未同步+拉最新）")

    # 其他
    sub.add_parser("summary", help="记忆摘要（含鲲鹏状态）")
    sub.add_parser("verify", help="验证本地记忆完整性")
    sub.add_parser("last", help="最近记忆")
    sub.add_parser("stats", help="统计信息（含鲲鹏）")
    sub.add_parser("health", help="检测鲲鹏连通性")

    args = parser.parse_args()
    store = MemoryStore(offline=args.offline)

    if args.command == "store":
        entry = store.store(
            topic=args.topic,
            content=args.content,
            priority=args.priority,
            tags=args.tags,
        )
        print(f"✅ 记忆已存储")
        print(f"   DNA:     {entry.dna}")
        print(f"   ID:      {entry.id}")
        print(f"   校验:    {entry.checksum}")
        if not args.offline:
            if entry.synced_to_kunpeng:
                print(f"   鲲鹏:    ✅ 已同步")
            else:
                print(f"   鲲鹏:    ⚠️ 不可达，已标记待同步（稍后运行 sync）")

    elif args.command == "retrieve":
        results = store.retrieve(
            topic=args.topic,
            priority=args.priority,
            limit=args.limit,
            prefer_kunpeng=not args.offline,
        )
        if not results:
            print("暂无匹配记忆。")
        for entry in results:
            origin = "☁️" if entry.get("synced_to_kunpeng") else "💻"
            print(f"{origin} [{entry.get('priority', 'P2')}] {entry.get('timestamp', '')[:16]}")
            print(f"   标题: {entry.get('topic', '无标题')}")
            print(f"   DNA:  {entry.get('dna', '无DNA')}")
            print(f"   内容: {entry.get('content', '')[:120]}")
            print()

    elif args.command == "sync":
        print("🔄 开始全量同步...")
        result = store.sync()
        if result.get("error"):
            print(f"❌ {result['error']}")
            return
        print(f"✅ 同步完成")
        print(f"   推送:   {result['pushed']} 条")
        print(f"   拉取:   {result['pulled']} 条")
        print(f"   失败:   {result['errors']} 条")

    elif args.command == "summary":
        print(store.summary())

    elif args.command == "verify":
        results = store.verify_integrity()
        print(f"📊 本地完整性报告")
        print(f"   总数:   {results['total']}")
        print(f"   完整:   {results['valid']} 🟢")
        print(f"   损坏:   {results['corrupted']} 🔴")
        print(f"   丢失:   {results['missing']} 🔴")
        print(f"   DNA完整: {results['dna_intact']} 🟢")
        if results["details"]:
            print(f"\n⚠️ 异常详情:")
            for detail in results["details"]:
                print(f"   - {detail['id']}: {detail['status']}")

    elif args.command == "last":
        last = store.get_last_session()
        if last:
            origin = "☁️" if last.get("synced_to_kunpeng") else "💻"
            print(f"📌 最近记忆 ({origin})")
            print(f"   主题: {last.get('topic', '无')}")
            print(f"   时间: {last.get('timestamp', '')[:19]}")
            print(f"   设备: {last.get('device', '未知')}")
            print(f"   DNA:  {last.get('dna', '无')}")
            print(f"   内容: {last.get('content', '')[:200]}")
        else:
            print("暂无历史记忆。")

    elif args.command == "stats":
        s = store.stats()
        print(f"📊 记忆层统计")
        print(f"   本地记忆: {s['local_total']}")
        print(f"   审计记录: {s['audit_count']}")
        print(f"   设备数:   {s['devices']}")
        print(f"   待同步:   {s['unsynced']}")
        print(f"   优先级:   {s['by_priority']}")
        if s.get("kunpeng"):
            kp = s["kunpeng"]
            print(f"\n☁️ 鲲鹏统计")
            print(f"   全域记忆: {kp.get('total_synced', '?')}")
            print(f"   设备数:   {kp.get('devices', '?')}")

    elif args.command == "health":
        if args.offline:
            print("📴 离线模式，跳过检测")
            return
        if store.kunpeng:
            online = store.kunpeng.is_online()
            if online:
                h = store.kunpeng.health()
                print(f"✅ 鲲鹏可达")
                print(f"   服务: {h.get('service', '?')}")
                print(f"   版本: {h.get('version', '?')}")
                print(f"   DNA:  {h.get('dna', '?')}")
            else:
                print("🔴 鲲鹏不可达")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
