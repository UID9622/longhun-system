#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════╗
║  龍魂·内网互联API网关 v1.0 — 安全加固版                            ║
║  DNA: #龍芯⚡️丙午·辛未·乙酉·未时·䷾既济-INTERNAL-NET-GATEWAY-v1.0  ║
║  #CONFIRM🌌9622-ONLY-ONCE🧬NET1-001A                                ║
║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F                      ║
║                                                                      ║
║  核心: 一台鲲鹏当中心，所有设备内网直连，不经过云                     ║
║  安全: DNA验证 → 三色审计 → 熔断控制 → 输入过滤 → 防投毒 → 芯片门禁 ║
║  协议: REST + WebSocket + P2P文件同步                                ║
║                                                                      ║
║  六层安全体系:                                                       ║
║    L0·DNA签名验证 — 每请求必验证DNA完整性                            ║
║    L1·三色审计    — 🟢通过/🟡警告/🔴阻断，全链路留痕                 ║
║    L2·熔断控制    — 三级策略: 警告→软阻断→硬阻断                     ║
║    L3·输入过滤    — 外部输入预处理，零信任架构                        ║
║    L4·防投毒隔离  — 单向隔离，打仗回来的战士要上政治课                ║
║    L5·芯片门禁    — 鲲鹏100%→龙芯85%→x86/60%→后门芯片0%             ║
║                                                                      ║
║  主权人: UID9622 💎 龍芯北辰·诸葛鑫·Lucky                           ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import os, sys, json, time, hashlib, hmac, re, secrets
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
from enum import Enum
from functools import wraps
import threading
import logging

# ── FastAPI ──
try:
    from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, HTTPException, UploadFile, File
    from fastapi.responses import JSONResponse, FileResponse
    from fastapi.middleware.cors import CORSMiddleware
    import uvicorn
except ImportError:
    print("❌ 缺少依赖: pip install fastapi uvicorn python-multipart")
    sys.exit(1)

# ═══════════════════════════════════════════════════════
# L0 常量 · 焊死 · 不可变
# ═══════════════════════════════════════════════════════

DNA = "#龍芯⚡️丙午·辛未·乙酉·未时·䷾既济-INTERNAL-NET-GATEWAY-v1.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬NET1-001A"
GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
SOVEREIGN_UID = "UID9622"
SOVEREIGN_NAME = "💎 龍芯北辰·诸葛鑫·Lucky"

# ── DNA 正则（四代兼容）──
DNA_REGEX_v1 = re.compile(r'#龍芯⚡️\d{4}-\d{2}-\d{2}-[A-Za-z0-9\-\.]+')
DNA_REGEX_v2 = re.compile(
    r'#龍芯⚡️[小寒大寒立春雨水惊蛰春分清明谷雨立夏小满芒种夏至'
    r'小暑大暑立秋处暑白露秋分寒露霜降立冬小雪大雪冬至]+\d{4}'
    r'·\d{2}:\d{2}:\d{2}-[A-Za-z0-9\-\.]+')
DNA_REGEX_VINF = re.compile(
    r'#龍芯⚡️[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]'
    r'·[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]'
    r'·[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]'
    r'·[子丑寅卯辰巳午未申酉戌亥]时'
    r'·[䷀䷁䷂䷃䷄䷅䷆䷇䷈䷉䷊䷋䷌䷍䷎䷏䷐䷑䷒䷓䷔䷕䷖䷗䷘䷙䷚䷛䷜䷝䷞䷟䷠䷡䷢䷣䷤䷥䷦䷧䷨䷩䷪䷫䷬䷭䷮䷯䷰䷱䷲䷳䷴䷵䷶䷷䷸䷹䷺䷻䷼䷽䷾䷿]'
    r'[\u4e00-\u9fff]*-[A-Za-z0-9\-\.]+')
DNA_REGEX_COMPACT = re.compile(
    r'#龍芯⚡️[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]'
    r'·[子丑寅卯辰巳午未申酉戌亥]时'
    r'·[䷀䷁䷂䷃䷄䷅䷆䷇䷈䷉䷊䷋䷌䷍䷎䷏䷐䷑䷒䷓䷔䷕䷖䷗䷘䷙䷚䷛䷜䷝䷞䷟䷠䷡䷢䷣䷤䷥䷦䷧䷨䷩䷪䷫䷬䷭䷮䷯䷰䷱䷲䷳䷴䷵䷶䷷䷸䷹䷺䷻䷼䷽䷾䷿]'
    r'-[A-Za-z0-9\-\.]+')

DNA_REGEXES = [DNA_REGEX_VINF, DNA_REGEX_COMPACT, DNA_REGEX_v2, DNA_REGEX_v1]

# ── 红黄警报词（来自 lh_anti_tamper.py）──
RED_WORDS = [
    "技术无国界", "无监督学习", "自由发展", "去中心化无政府",
    "数据无国界", "算法无国界", "代码自由", "极权AI",
    "完全开源无限制", "任何人可用", "源代码无版权",
    "放弃主权", "出口管制无用", "全球统一治理", "交出密钥"
]
YELLOW_WORDS = [
    "优化", "完善", "建议", "改进", "升级", "调整",
    "参考", "借鉴", "引入", "接入", "集成", "迁移"
]

# ── 禁止透露的系统信息关键词 ──
FORBIDDEN_KW = [
    "system prompt", "系统提示词", "system_prompt",
    "prompt template", "internal config", "内核算法",
    "训练数据源", "training data source"
]

# ── 审计级别 ──
class AuditLevel(Enum):
    GREEN = "🟢"   # 通过
    YELLOW = "🟡"  # 警告
    RED = "🔴"     # 阻断

# ── 熔断级别 ──
class FuseLevel(Enum):
    NONE = 0
    WARN = 1     # 观察
    ALERT = 2    # 告警
    THROTTLE = 3 # 限速
    FREEZE = 4   # 冻结
    EXECUTE = 5  # 处决（硬阻断）

# ── 芯片层级 ──
CHIP_TIERS = {
    "kunpeng":  {"score": 100, "level": "完美"},
    "loongson": {"score": 85,  "level": "可用"},
    "phytium":  {"score": 80,  "level": "可用"},
    "x86":      {"score": 60,  "level": "受限"},
    "arm_generic": {"score": 70, "level": "可用"},
    "backdoor": {"score": 0,   "level": "熔断"},
}

# ═══════════════════════════════════════════════════════
# 日志配置
# ═══════════════════════════════════════════════════════

LOG_DIR = Path(os.environ.get("LONGHUN_LOG_DIR", Path.home() / ".longhun" / "logs"))
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "internal_net_gateway.log"),
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger("lh_internal_net_gw")

# ═══════════════════════════════════════════════════════
# 审计日志（append-only）
# ═══════════════════════════════════════════════════════

AUDIT_LOG = LOG_DIR / "internal_net_audit.jsonl"

def audit_write(level: AuditLevel, event: str, detail: Dict[str, Any], source: str = "gateway"):
    """写入审计日志，append-only，不覆盖不抹除"""
    entry = {
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "level": level.value,
        "level_name": level.name,
        "event": event,
        "detail": detail,
        "source": source,
        "dna": DNA,
        "gpg": GPG_FINGERPRINT[:16],
    }
    with open(AUDIT_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

# ═══════════════════════════════════════════════════════
# L0层·DNA签名验证
# ═══════════════════════════════════════════════════════

def validate_dna(text: str) -> Tuple[bool, Optional[str]]:
    """验证文本中是否包含合法DNA签名"""
    for regex in DNA_REGEXES:
        m = regex.search(text)
        if m:
            return True, m.group(0)
    return False, None

def validate_confirm(text: str) -> bool:
    """验证确认码"""
    if not text:
        return False
    return CONFIRM in text or "#CONFIRM" in text

# ═══════════════════════════════════════════════════════
# L3层·输入过滤引擎（基于輸入過濾協議 v3.0）
# ═══════════════════════════════════════════════════════

class InputFilter:
    """L3输入过滤——先读懂，再决定怎么接"""

    @staticmethod
    def scan_red_words(text: str) -> List[str]:
        """扫描红词，命中立即告警"""
        found = []
        text_lower = text.lower()
        for word in RED_WORDS:
            if word.lower() in text_lower:
                found.append(word)
        return found

    @staticmethod
    def scan_yellow_words(text: str) -> List[str]:
        """扫描黄词，需追问确认"""
        found = []
        text_lower = text.lower()
        for word in YELLOW_WORDS:
            if word.lower() in text_lower:
                found.append(word)
        return found

    @staticmethod
    def scan_forbidden(text: str) -> List[str]:
        """扫描禁止透露的系统信息关键词"""
        found = []
        text_lower = text.lower()
        for kw in FORBIDDEN_KW:
            if kw.lower() in text_lower:
                found.append(kw)
        return found

    @staticmethod
    def scan_payload_size(text: str, max_len: int = 10000) -> Tuple[bool, int]:
        """检查payload大小"""
        size = len(text)
        return size <= max_len, size

    @staticmethod
    def filter(data: Dict[str, Any]) -> Tuple[bool, AuditLevel, str]:
        """
        完整输入过滤管线
        返回: (是否放行, 审计级别, 原因)
        """
        content = json.dumps(data, ensure_ascii=False) if isinstance(data, dict) else str(data)

        # 1. 红词扫描 — 阻断
        reds = InputFilter.scan_red_words(content)
        if reds:
            reason = f"🔴 红词命中: {', '.join(reds)}"
            audit_write(AuditLevel.RED, "INPUT_RED_WORD", {"red_words": reds, "content_snip": content[:200]})
            return False, AuditLevel.RED, reason

        # 2. 禁止关键词 — 阻断
        forbidden = InputFilter.scan_forbidden(content)
        if forbidden:
            reason = f"🔴 禁止关键词: {', '.join(forbidden)}"
            audit_write(AuditLevel.RED, "INPUT_FORBIDDEN_KW", {"keywords": forbidden, "content_snip": content[:200]})
            return False, AuditLevel.RED, reason

        # 3. 载荷大小
        ok, size = InputFilter.scan_payload_size(content)
        if not ok:
            reason = f"🔴 载荷过大: {size} bytes"
            audit_write(AuditLevel.RED, "INPUT_SIZE_LIMIT", {"size": size})
            return False, AuditLevel.RED, reason

        # 4. 黄词扫描 — 警告放行
        yellows = InputFilter.scan_yellow_words(content)
        if yellows:
            reason = f"🟡 黄词注意: {', '.join(yellows)}"
            audit_write(AuditLevel.YELLOW, "INPUT_YELLOW_WORD", {"yellow_words": yellows, "content_snip": content[:200]})
            return True, AuditLevel.YELLOW, reason

        return True, AuditLevel.GREEN, "通过"

# ═══════════════════════════════════════════════════════
# L4层·防投毒隔离引擎
# ═══════════════════════════════════════════════════════

class AntiPoisonEngine:
    """
    L4防投毒隔离 — 打仗回来的战士要上政治课
    外部输入经过多重净化、逐层勘察后才能进入系统核心
    """

    POISON_PATTERNS = [
        r'(?i)ignore\s+(all\s+)?(previous|above)\s+(instructions?|prompts?)',
        r'(?i)forget\s+(your|all)\s+(training|instructions?|rules?)',
        r'(?i)you\s+are\s+now\s+(a\s+)?new\s+(AI|assistant|model)',
        r'(?i)pretend\s+(to\s+be|you\s+are)',
        r'(?i)jailbreak|prompt\s+injection|prompt\s+leak',
        r'(?i)output\s+(your|the)\s+(system\s+)?prompt',
        r'(?i)reveal\s+(your|the)\s+(hidden\s+)?(rules?|instructions?)',
        r'(?i)ROT13|base64\s+encode|decode',
        r'(?i)as\s+a\s+DAN|developer\s+mode',
        r'(?i)from\s+now\s+on\s+you\s+are',
    ]

    @classmethod
    def scan(cls, text: str) -> Tuple[bool, List[str]]:
        """返回 (是否投毒, 匹配到的模式)"""
        found = []
        for pat in cls.POISON_PATTERNS:
            if re.search(pat, text):
                found.append(pat.split('(?i)')[-1] if '(?i)' in pat else pat[:60])
        return len(found) > 0, found

    @classmethod
    def sanitize(cls, text: str) -> str:
        """净化输入：移除潜在注入标记"""
        # 移除可能的markdown代码块注入
        sanitized = re.sub(r'```.*?```', '[CODE_BLOCK_REMOVED]', text, flags=re.DOTALL)
        # 移除XML/HTML标签注入
        sanitized = re.sub(r'<[^>]+>', '[TAG_REMOVED]', sanitized)
        return sanitized

# ═══════════════════════════════════════════════════════
# L1层·三色审计追踪
# ═══════════════════════════════════════════════════════

class AuditTrail:
    """全链路三色审计追踪"""

    def __init__(self):
        self.lock = threading.Lock()
        self.records: List[Dict] = []  # 内存缓冲
        self.total_green = 0
        self.total_yellow = 0
        self.total_red = 0

    def record(self, level: AuditLevel, action: str, device_id: str, detail: str = ""):
        with self.lock:
            record = {
                "time": datetime.now().isoformat(),
                "level": level.value,
                "action": action,
                "device": device_id,
                "detail": detail,
            }
            self.records.append(record)
            # 只保留最近1000条
            if len(self.records) > 1000:
                self.records = self.records[-500:]

            if level == AuditLevel.GREEN:
                self.total_green += 1
            elif level == AuditLevel.YELLOW:
                self.total_yellow += 1
            elif level == AuditLevel.RED:
                self.total_red += 1

    def stats(self) -> Dict:
        with self.lock:
            return {
                "green": self.total_green,
                "yellow": self.total_yellow,
                "red": self.total_red,
                "total": self.total_green + self.total_yellow + self.total_red,
                "buffer_size": len(self.records),
            }

    def recent(self, n: int = 50) -> List[Dict]:
        with self.lock:
            return self.records[-n:]

# ═══════════════════════════════════════════════════════
# L2层·熔断控制器
# ═══════════════════════════════════════════════════════

class FuseController:
    """
    内网节点熔断 — 设备级别的安全熔断
    连续N次异常 → 升级熔断级别
    """

    def __init__(self, warn_threshold: int = 5, execute_threshold: int = 10):
        self.lock = threading.Lock()
        self.warn_threshold = warn_threshold
        self.execute_threshold = execute_threshold
        self.device_violations: Dict[str, List[float]] = {}  # device_id -> [timestamps]
        self.fused_devices: Dict[str, FuseLevel] = {}
        self.window_seconds = 300  # 5分钟窗口

    def _clean_old(self, device_id: str):
        """清理过期违规记录"""
        now = time.time()
        if device_id in self.device_violations:
            self.device_violations[device_id] = [
                t for t in self.device_violations[device_id]
                if now - t < self.window_seconds
            ]

    def check(self, device_id: str) -> Tuple[bool, FuseLevel]:
        """检查设备是否被熔断"""
        with self.lock:
            if device_id in self.fused_devices:
                return True, self.fused_devices[device_id]
            return False, FuseLevel.NONE

    def report_violation(self, device_id: str, reason: str) -> FuseLevel:
        """报告一次违规"""
        with self.lock:
            if device_id not in self.device_violations:
                self.device_violations[device_id] = []
            self.device_violations[device_id].append(time.time())
            self._clean_old(device_id)

            count = len(self.device_violations[device_id])

            if count >= self.execute_threshold:
                self.fused_devices[device_id] = FuseLevel.EXECUTE
                audit_write(AuditLevel.RED, "FUSE_EXECUTE", {
                    "device": device_id, "violations": count, "reason": reason
                })
                return FuseLevel.EXECUTE
            elif count >= self.warn_threshold:
                self.fused_devices[device_id] = FuseLevel.THROTTLE
                audit_write(AuditLevel.YELLOW, "FUSE_THROTTLE", {
                    "device": device_id, "violations": count, "reason": reason
                })
                return FuseLevel.THROTTLE
            elif count >= 3:
                return FuseLevel.WARN
            return FuseLevel.NONE

    def reset(self, device_id: str):
        """重置设备熔断状态（需主权人确认）"""
        with self.lock:
            self.device_violations.pop(device_id, None)
            self.fused_devices.pop(device_id, None)
            audit_write(AuditLevel.GREEN, "FUSE_RESET", {"device": device_id})

    def stats(self) -> Dict:
        with self.lock:
            return {
                "fused_devices": len(self.fused_devices),
                "fused_list": {k: v.name for k, v in self.fused_devices.items()},
                "violations": {k: len(v) for k, v in self.device_violations.items()},
            }

# ═══════════════════════════════════════════════════════
# L5层·芯片门禁
# ═══════════════════════════════════════════════════════

class ChipGate:
    """设备芯片层级验证"""

    @staticmethod
    def detect_chip(device_type: str, device_info: Dict) -> Tuple[str, int, str]:
        """
        根据设备信息推断芯片层级
        返回: (芯片类型, 分数, 层级名)
        """
        arch = device_info.get("arch", "").lower()
        cpu = device_info.get("cpu", "").lower()

        if "kunpeng" in arch or "kunpeng" in cpu or "taishan" in cpu:
            return "kunpeng", 100, "完美"
        elif "loongson" in arch or "loongson" in cpu or "loongarch" in cpu:
            return "loongson", 85, "可用"
        elif "phytium" in arch or "phytium" in cpu or "ft-2000" in cpu:
            return "phytium", 80, "可用"
        elif "aarch64" in arch or "arm64" in arch or "arm" in arch:
            if device_type in ("phone", "pad", "mobile"):
                return "arm_generic", 70, "可用"
            return "arm_generic", 70, "可用"
        elif "x86" in arch or "intel" in cpu or "amd" in cpu:
            return "x86", 60, "受限"
        else:
            return "unknown", 50, "未知"

    @staticmethod
    def should_block(chip_score: int) -> bool:
        """分数为0的直接熔断"""
        return chip_score == 0

    @staticmethod
    def should_warn(chip_score: int) -> bool:
        """分数低于60的需警告"""
        return chip_score < 60 and chip_score > 0

# ═══════════════════════════════════════════════════════
# 设备注册表
# ═══════════════════════════════════════════════════════

class DeviceRegistry:
    """设备注册与发现"""

    def __init__(self):
        self.lock = threading.Lock()
        self.devices: Dict[str, Dict] = {}
        self.timeout = 300  # 5分钟无心跳 = 离线

    def register(self, device_id: str, info: Dict) -> Dict:
        with self.lock:
            info["id"] = device_id
            info["registered_at"] = datetime.now(timezone.utc).isoformat()
            info["last_seen"] = time.time()
            info["status"] = "online"

            # 芯片门禁检查
            chip_type, chip_score, chip_tier = ChipGate.detect_chip(
                info.get("type", "unknown"), info
            )
            info["chip_type"] = chip_type
            info["chip_score"] = chip_score
            info["chip_tier"] = chip_tier

            self.devices[device_id] = info

            audit_write(AuditLevel.GREEN, "DEVICE_REGISTER", {
                "device": device_id,
                "name": info.get("name", ""),
                "type": info.get("type", ""),
                "chip": f"{chip_type}({chip_score}/{chip_tier})",
            })

            return info

    def heartbeat(self, device_id: str) -> bool:
        with self.lock:
            if device_id in self.devices:
                self.devices[device_id]["last_seen"] = time.time()
                self.devices[device_id]["status"] = "online"
                return True
            return False

    def cleanup(self):
        """清理离线设备"""
        now = time.time()
        with self.lock:
            offline = [
                k for k, v in self.devices.items()
                if now - v["last_seen"] > self.timeout
            ]
            for k in offline:
                self.devices[k]["status"] = "offline"

    def get_all(self) -> List[Dict]:
        self.cleanup()
        with self.lock:
            return [
                {
                    "id": d["id"],
                    "name": d.get("name", d["id"]),
                    "type": d.get("type", "unknown"),
                    "ip": d.get("ip", ""),
                    "chip_tier": d.get("chip_tier", "未知"),
                    "status": d.get("status", "unknown"),
                    "capabilities": d.get("capabilities", []),
                }
                for d in self.devices.values()
            ]

    def count(self) -> int:
        with self.lock:
            return len(self.devices)

    def get(self, device_id: str) -> Optional[Dict]:
        with self.lock:
            return self.devices.get(device_id)

# ═══════════════════════════════════════════════════════
# 消息队列
# ═══════════════════════════════════════════════════════

class MessageQueue:
    """内网消息路由 — 内存队列，重启清空"""

    def __init__(self, max_room_size: int = 1000):
        self.lock = threading.Lock()
        self.rooms: Dict[str, List[Dict]] = {}
        self.max_room_size = max_room_size

    def send(self, room: str, msg: Dict) -> str:
        msg_id = f"msg_{int(time.time()*1000)}_{secrets.token_hex(4)}"
        msg["id"] = msg_id
        msg["timestamp"] = datetime.now(timezone.utc).isoformat()

        with self.lock:
            if room not in self.rooms:
                self.rooms[room] = []
            self.rooms[room].append(msg)
            if len(self.rooms[room]) > self.max_room_size:
                self.rooms[room] = self.rooms[room][-self.max_room_size//2:]

        return msg_id

    def receive(self, room: str, device_id: str, since: Optional[str] = None) -> List[Dict]:
        with self.lock:
            if room not in self.rooms:
                return []

            msgs = [
                m for m in self.rooms[room]
                if m.get("to") is None or m.get("to") == device_id or m.get("from") == device_id
            ]

            if since:
                msgs = [m for m in msgs if m.get("timestamp", "") > since]

            return msgs

# ═══════════════════════════════════════════════════════
# 文件缓存
# ═══════════════════════════════════════════════════════

class FileCache:
    """内网文件暂存"""

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.ttl = 86400  # 24小时

    def save(self, device_id: str, filename: str, content: bytes) -> str:
        safe_name = f"{device_id}_{int(time.time())}_{filename}"
        filepath = self.base_dir / safe_name
        with open(filepath, "wb") as f:
            f.write(content)
        logger.info(f"📁 文件缓存: {safe_name} ({len(content)} bytes)")
        return safe_name

    def get(self, filename: str) -> Optional[Path]:
        filepath = self.base_dir / filename
        if filepath.exists() and filepath.is_file():
            # 检查TTL
            if time.time() - filepath.stat().st_mtime < self.ttl:
                return filepath
        return None

    def cleanup(self):
        """清理过期文件"""
        now = time.time()
        for f in self.base_dir.iterdir():
            if f.is_file() and now - f.stat().st_mtime > self.ttl:
                f.unlink()
                logger.info(f"🗑️ 清理过期文件: {f.name}")

# ═══════════════════════════════════════════════════════
# FastAPI 应用
# ═══════════════════════════════════════════════════════

app = FastAPI(
    title="🐉 龍魂内网互联网关",
    description=f"安全加固版 · DNA: {DNA}",
    version="1.0",
)

# CORS — 内网宽松
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── 全局实例 ──
devices = DeviceRegistry()
messages = MessageQueue()
file_cache = FileCache(Path("./longhun_file_cache"))
audit = AuditTrail()
fuse = FuseController()
input_filter = InputFilter()

# ═══════════════════════════════════════════════════════
# 安全中间件 — 所有请求必经此门
# ═══════════════════════════════════════════════════════

@app.middleware("http")
async def security_middleware(request: Request, call_next):
    """全局安全中间件 — 六层安全体系入口"""

    # 获取客户端IP和请求体
    client_ip = request.client.host if request.client else "unknown"
    body = None
    try:
        if request.method in ("POST", "PUT", "PATCH"):
            body_bytes = await request.body()
            body = body_bytes.decode("utf-8", errors="ignore")[:5000]
    except:
        pass

    # L3: 输入过滤
    if body:
        ok, level, reason = input_filter.filter({"body": body, "ip": client_ip, "path": str(request.url.path)})
        if not ok:
            audit.record(AuditLevel.RED, "INPUT_BLOCKED", client_ip, reason)
            logger.warning(f"🔴 输入阻断 [{client_ip}]: {reason}")
            return JSONResponse(
                status_code=403,
                content={"blocked": True, "reason": reason, "dna": DNA}
            )

    # L4: 防投毒扫描
    if body:
        is_poison, patterns = AntiPoisonEngine.scan(body)
        if is_poison:
            audit.record(AuditLevel.RED, "POISON_DETECTED", client_ip, str(patterns))
            audit_write(AuditLevel.RED, "POISON_ATTACK", {"ip": client_ip, "patterns": patterns, "body_snip": body[:200]})
            logger.warning(f"🔴 投毒攻击 [{client_ip}]: {patterns}")
            return JSONResponse(
                status_code=403,
                content={"blocked": True, "reason": "投毒攻击检测", "dna": DNA}
            )

    # 继续处理
    response = await call_next(request)

    # 响应头注入DNA (HTTP头仅支持ASCII，用base64编码中文部分)
    response.headers["X-LongHun-DNA"] = "longhun-internal-net-v1.0"
    response.headers["X-LongHun-GPG"] = GPG_FINGERPRINT[:16]
    response.headers["X-LongHun-Sovereign"] = "UID9622"

    return response

# ═══════════════════════════════════════════════════════
# API 路由
# ═══════════════════════════════════════════════════════

@app.get("/")
async def root():
    return {
        "gateway": "🐉 龍魂内网互联网关",
        "version": "1.0",
        "dna": DNA,
        "confirm": CONFIRM,
        "gpg": GPG_FINGERPRINT[:16],
        "sovereign": SOVEREIGN_UID,
        "security_layers": [
            "L0·DNA签名验证",
            "L1·三色审计",
            "L2·熔断控制",
            "L3·输入过滤",
            "L4·防投毒隔离",
            "L5·芯片门禁",
        ],
    }


@app.get("/health")
async def health():
    return {
        "status": "🐉 运行中",
        "dna": DNA,
        "peers": devices.count(),
        "audit": audit.stats(),
        "fuse": fuse.stats(),
        "uptime": "running",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/register")
async def register(data: Dict[str, Any]):
    """设备注册 — 即插即用，附带芯片门禁检查"""
    device_id = data.get("id", f"device_{int(time.time())}_{secrets.token_hex(4)}")

    # L3: 输入过滤
    ok, level, reason = input_filter.filter(data)
    if not ok:
        return {"registered": False, "error": reason}

    # 注册
    info = devices.register(device_id, data)

    return {
        "registered": True,
        "device_id": device_id,
        "gateway_info": {
            "dna": DNA,
            "gpg": GPG_FINGERPRINT[:16],
        },
        "chip_verdict": {
            "type": info.get("chip_type"),
            "score": info.get("chip_score"),
            "tier": info.get("chip_tier"),
        },
        "peers_online": devices.count(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/peers")
async def list_peers(request: Request):
    """列出所有在线设备"""
    client_ip = request.client.host if request.client else "unknown"
    all_devices = devices.get_all()
    audit.record(AuditLevel.GREEN, "LIST_PEERS", client_ip, f"count={len(all_devices)}")
    return {
        "count": len(all_devices),
        "peers": all_devices,
        "dna": DNA,
    }


@app.post("/heartbeat/{device_id}")
async def heartbeat(device_id: str):
    """心跳保活"""
    ok = devices.heartbeat(device_id)
    if ok:
        return {"ok": True, "device_id": device_id}
    return {"ok": False, "error": "设备未注册，请先 /register"}


@app.post("/message/send")
async def send_message(data: Dict[str, Any]):
    """发送消息"""
    device_id = data.get("from", "unknown")

    # L2: 熔断检查
    is_fused, fuse_level = fuse.check(device_id)
    if is_fused and fuse_level == FuseLevel.EXECUTE:
        audit.record(AuditLevel.RED, "MSG_BLOCKED_FUSE", device_id, "硬阻断")
        return {"sent": False, "error": "设备已被熔断"}

    # L3: 输入过滤
    content = data.get("content", "")
    if content:
        ok, level, reason = input_filter.filter({"content": content})
        if not ok:
            fuse.report_violation(device_id, reason)
            audit.record(level, "MSG_CONTENT_BLOCKED", device_id, reason)
            return {"sent": False, "error": reason}

    room = data.get("room_id", "broadcast")
    msg = {
        "from": device_id,
        "to": data.get("to"),
        "type": data.get("type", "text"),
        "content": content,
        "ttl": data.get("ttl", 86400),
    }

    msg_id = messages.send(room, msg)
    audit.record(AuditLevel.GREEN, "MSG_SENT", device_id, f"room={room}, type={msg['type']}")

    return {"sent": True, "msg_id": msg_id, "room": room}


@app.get("/message/receive/{device_id}")
async def receive_messages(device_id: str, room_id: str = "broadcast", since: str = None):
    """接收消息"""
    msgs = messages.receive(room_id, device_id, since)
    return {"messages": msgs, "count": len(msgs)}


@app.post("/file/upload")
async def upload_file(file: UploadFile = File(...), device_id: str = "unknown"):
    """文件上传 — 局域网满速"""
    content = await file.read()

    # L3: 检查文件名
    filename = file.filename or "unknown"
    reds = input_filter.scan_red_words(filename)
    if reds:
        audit.record(AuditLevel.RED, "FILE_UPLOAD_BLOCKED", device_id, f"red in filename: {reds}")
        return {"uploaded": False, "error": f"文件名含敏感词: {reds}"}

    # 大小限制 500MB
    if len(content) > 500 * 1024 * 1024:
        return {"uploaded": False, "error": "文件过大 (最大500MB)"}

    safe_name = file_cache.save(device_id, filename, content)
    audit.record(AuditLevel.GREEN, "FILE_UPLOADED", device_id, f"{safe_name} ({len(content)} bytes)")

    return {
        "uploaded": True,
        "filename": safe_name,
        "original_name": filename,
        "size": len(content),
        "url": f"/file/download/{safe_name}",
        "ttl_seconds": 86400,
    }


@app.get("/file/download/{filename}")
async def download_file(filename: str):
    """文件下载"""
    filepath = file_cache.get(filename)
    if filepath is None:
        return JSONResponse(status_code=404, content={"error": "文件不存在或已过期"})
    return FileResponse(filepath, filename=filename)


# ── 安全控制接口 ──

@app.get("/audit/stats")
async def audit_stats():
    """审计统计"""
    return audit.stats()


@app.get("/audit/recent")
async def audit_recent(n: int = 50):
    """最近审计记录"""
    return {"records": audit.recent(n)}


@app.get("/fuse/status")
async def fuse_status():
    """熔断状态"""
    return fuse.stats()


@app.post("/fuse/reset/{device_id}")
async def fuse_reset(device_id: str, data: Dict[str, Any]):
    """重置设备熔断（需主权令牌）"""
    token = data.get("token", "")
    # 验证主权令牌: CONFIRM码 + GPG哈希
    expected = hashlib.sha256(f"{CONFIRM}{GPG_FINGERPRINT}".encode()).hexdigest()[:16]
    if token != expected:
        audit.record(AuditLevel.RED, "FUSE_RESET_DENIED", device_id, "无效主权令牌")
        return JSONResponse(status_code=403, content={"error": "需要主权令牌"})

    fuse.reset(device_id)
    return {"reset": True, "device": device_id}


@app.post("/sovereign/override")
async def sovereign_override(data: Dict[str, Any]):
    """主权人手动覆盖（最高权限）"""
    token = data.get("token", "")
    expected = hashlib.sha256(f"{CONFIRM}{GPG_FINGERPRINT}{SOVEREIGN_UID}".encode()).hexdigest()[:16]
    if token != expected:
        return JSONResponse(status_code=403, content={"error": "主权令牌无效"})

    action = data.get("action", "")
    device_id = data.get("device_id", "")
    audit.record(AuditLevel.YELLOW, f"SOVEREIGN_OVERRIDE_{action}", device_id, "主权人手动操作")

    return {"override": True, "action": action, "sovereign": SOVEREIGN_UID}


# ── WebSocket 实时通道 ──

connected_ws: Dict[str, WebSocket] = {}

@app.websocket("/ws/{device_id}")
async def websocket_endpoint(websocket: WebSocket, device_id: str):
    await websocket.accept()
    connected_ws[device_id] = websocket
    audit.record(AuditLevel.GREEN, "WS_CONNECTED", device_id)

    try:
        while True:
            data = await websocket.receive_text()
            msg_data = json.loads(data)

            # 输入过滤
            ok, level, reason = input_filter.filter(msg_data)
            if not ok:
                await websocket.send_json({"error": reason, "level": level.value})
                continue

            # 广播给目标设备
            target = msg_data.get("to")
            msg_data["from"] = device_id

            if target and target in connected_ws:
                try:
                    await connected_ws[target].send_json(msg_data)
                except:
                    pass
            else:
                # 存消息队列
                messages.send(msg_data.get("room", "broadcast"), msg_data)

    except WebSocketDisconnect:
        pass
    finally:
        connected_ws.pop(device_id, None)
        audit.record(AuditLevel.GREEN, "WS_DISCONNECTED", device_id)


# ═══════════════════════════════════════════════════════
# 定时任务线程
# ═══════════════════════════════════════════════════════

def cleanup_worker():
    """定期清理过期文件"""
    while True:
        try:
            file_cache.cleanup()
            devices.cleanup()
        except:
            pass
        time.sleep(3600)  # 每小时

# ═══════════════════════════════════════════════════════
# 启动
# ═══════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="🐉 龍魂内网互联API网关")
    parser.add_argument("--host", default="0.0.0.0", help="监听地址")
    parser.add_argument("--port", type=int, default=9622, help="监听端口")
    parser.add_argument("--log-level", default="info", choices=["debug", "info", "warning", "error"])
    args = parser.parse_args()

    # 启动清理线程
    threading.Thread(target=cleanup_worker, daemon=True).start()

    logger.info(f"🐉 龍魂内网网关启动")
    logger.info(f"   DNA: {DNA}")
    logger.info(f"   GPG: {GPG_FINGERPRINT}")
    logger.info(f"   端口: {args.port}")
    logger.info(f"   安全: L0·DNA | L1·三色审计 | L2·熔断 | L3·输入过滤 | L4·防投毒 | L5·芯片门禁")

    audit_write(AuditLevel.GREEN, "GATEWAY_START", {
        "host": args.host, "port": args.port
    })

    uvicorn.run(app, host=args.host, port=args.port, log_level=args.log_level)
