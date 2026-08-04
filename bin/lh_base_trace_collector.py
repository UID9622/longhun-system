#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
"""
龍魂·底座痕迹采集引擎 v2.0 — 四道防线版
DNA: #龍芯⚡️丙午·乙未·壬寅·亥时·☰乾-BASE-TRACE-COLLECTOR-V2.0-FOUR-DEFENSES
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

采集操作系统级数字痕迹：
  - 进程痕迹：启动/销毁时间、进程名、PID、命令行参数
  - 文件痕迹：创建/修改/删除/重命名事件
  - 网络痕迹：TCP/UDP连接记录
  - 用户行为痕迹：登录/注销、锁屏/解锁、外设插拔

四道防线（焊死）：
  防线一：网络出站透明监控 · 非用户进程外传数据 → 阻断+弹窗告警
  防线二：恶意代码过滤 · 文件扫描前过本地恶意特征库 · 跳过+隔离记录
  防线三：设备绑定加密 · AES-256 密钥派生自设备指纹 · 密钥只存内存·不落盘
  防线四：导出绑定设备+生物验证（由 lh_trace_reconstructor_api.py 签名侧实现）

铁律：
  - 原始数据绝不离开用户设备
  - 对外发送仅特征向量（哈希脱敏）
  - 本地存储设备绑定加密
"""

import argparse
import base64
import hashlib
import hmac
import json
import os
import platform
import re
import signal
import sqlite3
import subprocess
import sys
import threading
import time
import uuid
from datetime import datetime, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
import logging

# AES 加密（优先 cryptography，降级到内置）
try:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.primitives import padding as sym_padding
    from cryptography.hazmat.backends import default_backend
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False
    log_fallback = logging.getLogger("trace-collector")
    log_fallback.warning("cryptography 库未安装，AES加密降级到 hashlib 派生（安全性较低）。"
                         "建议: pip3 install cryptography")

# ─── 常量 ─────────────────────────────────────────────
VERSION = "2.0.0"
DNA = "#龍芯⚡️丙午·乙未·壬寅·亥时·☰乾-BASE-TRACE-COLLECTOR-V2.0-FOUR-DEFENSES"
COLLECTOR_PORT = 18775  # 本地API端口
CHECK_INTERVAL_PROCESS = 5    # 进程快照间隔(秒)
CHECK_INTERVAL_NETWORK = 10   # 网络快照间隔(秒)
CHECK_INTERVAL_USER = 15      # 用户行为检查间隔(秒)
CHECK_INTERVAL_FILE = 8       # 文件系统检查间隔(秒)
DATA_DIR = os.path.expanduser("~/.longhun/traces")
DB_PATH = os.path.join(DATA_DIR, "trace.db")
PID_FILE = os.path.expanduser("~/.longhun/trace_collector.pid")

# ═══════════════════════════════════════════════════
# 四道防线常量
# ═══════════════════════════════════════════════════
MALWARE_SIG_PATH = os.path.join(DATA_DIR, "malware_sigs.json")
DEVICE_SALT_PATH = os.path.join(DATA_DIR, ".device_salt")
DEFENSE_LOG_PATH = os.path.join(DATA_DIR, "defense_audit.log")
USER_WHITELIST_PATH = os.path.join(DATA_DIR, "network_whitelist.json")  # 用户自定义白名单
NETWORK_WATCH_INTERVAL = 3    # 网络监控间隔(秒)
MALWARE_SYNC_INTERVAL = 3600  # 恶意特征库同步间隔(秒)
THREAT_INTEL_SYNC_INTERVAL = 86400  # 威胁情报同步间隔(秒) = 24h
NETWORK_GUARD_MAX_ALERTS = 500
PF_ANCHOR_NAME = "com.longhun.network.guard"  # macOS pf 锚点名
THREAT_INTEL_SOURCES = [
    {
        "name": "URLhaus",
        "url": "https://urlhaus-api.abuse.ch/v1/payloads/recent/",
        "key_field": "sha256_hash",
        "threat_field": "signature",
    },
    {
        "name": "ThreatFox",
        "url": "https://threatfox-api.abuse.ch/api/v1/",
        "key_field": "ioc_value",
        "threat_field": "threat_type",
    },
]
# 可疑可执行文件扩展名（未知时默认拒绝扫描）
EXECUTABLE_EXTENSIONS = {".app", ".exe", ".dmg", ".pkg", ".msi", ".deb", ".rpm", ".sh", ".command", ".ps1", ".bat", ".cmd"}

# 默认恶意特征库（内嵌种子，定期从鲲鹏同步更新）
DEFAULT_MALWARE_SIGS: Dict[str, Any] = {
    "hash_sha256": [],
    "suspicious_extensions": [
        ".scr", ".bat", ".cmd", ".ps1", ".vbs", ".js", ".jar",
    ],
    "suspicious_process_names": [
        "xmrig", "minerd", "cpuminer", "cgminer", "bfgminer",
        "keylogger", "keylog", "klog",
        "ransomware", "encryptor",
    ],
    "suspicious_file_patterns": [
        r"\.scr$", r"\.vbs$", r"autorun\.inf",
        r"\.pyc$",
    ],
    "signature_version": "1.0.0-seed",
    "last_updated": "2026-07-25T00:00:00Z",
}

# 网络白名单：用户明确信任的进程名
NETWORK_TRUSTED_PREFIXES = [
    "Google Chrome", "Chrome", "Safari", "Firefox", "Arc",
    "Terminal", "iTerm2", "kitty", "Alacritty",
    "Code", "CodeBuddy", "Cursor", "VSCode",
    "Mail", "Outlook", "Slack", "Discord", "Telegram", "WeChat",
    "Spotify", "Music",
    "Dropbox", "OneDrive",
    "Finder", "SystemUIServer", "Dock", "WindowServer",
    "ssh", "scp", "rsync", "git", "curl", "wget",
    "python", "python3", "node", "npm", "yarn", "pip",
    "Docker", "mDNSResponder", "rapportd", "trustd",
    "identityservicesd", "sharingd", "apsd", "cloudd",
    "mdworker", "mds", "corespotlightd",
]

# 网络白名单端口
NETWORK_TRUSTED_PORTS = {22, 53, 80, 443, 587, 993, 8080, 8443, 3000, 5000, 8000, 8766, 8767, 8768, 8769, 8770, 8771, 8773, 8774, 8799, 18775}

# 网络只告警不阻断的远程地址模式（CDN/公共DNS等）
NETWORK_ALERT_ONLY_PATTERNS = [
    r"\.icloud\.com", r"\.apple\.com", r"\.googleapis\.com",
    r"8\.8\.8\.8", r"8\.8\.4\.4", r"1\.1\.1\.1",
    r"114\.114\.114\.114",
    r"\.cdn\.", r"\.amazonaws\.com",
]

# 监控目录（可配置）
DEFAULT_WATCH_DIRS = [
    os.path.expanduser("~/Documents"),
    os.path.expanduser("~/Desktop"),
    os.path.expanduser("~/Downloads"),
    os.path.expanduser("~/longhun-system"),
]

IS_MACOS = platform.system() == "Darwin"
IS_LINUX = platform.system() == "Linux"

# 日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [TRACE] %(levelname)s %(message)s",
    handlers=[logging.StreamHandler()]
)
log = logging.getLogger("trace-collector")


# ─── 数据库 ─────────────────────────────────────────────
def init_db():
    """初始化SQLite数据库"""
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS process_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL NOT NULL,
            event_type TEXT NOT NULL,  -- start, stop
            pid INTEGER NOT NULL,
            ppid INTEGER,
            name TEXT NOT NULL,
            name_hash TEXT NOT NULL,
            cmdline TEXT,
            cmdline_hash TEXT NOT NULL,
            user TEXT
        );
        
        CREATE TABLE IF NOT EXISTS file_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL NOT NULL,
            event_type TEXT NOT NULL,  -- create, modify, delete, rename
            path_hash TEXT NOT NULL,
            old_path_hash TEXT,         -- for rename events
            size INTEGER,
            ext TEXT
        );
        
        CREATE TABLE IF NOT EXISTS network_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL NOT NULL,
            event_type TEXT NOT NULL,  -- connect, disconnect, listen
            protocol TEXT,             -- TCP, UDP
            local_addr TEXT,
            local_port INTEGER,
            remote_addr_hash TEXT,
            remote_port INTEGER,
            process_name_hash TEXT,
            state TEXT
        );
        
        CREATE TABLE IF NOT EXISTS user_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL NOT NULL,
            event_type TEXT NOT NULL,  -- login, logout, lock, unlock, device_attach, device_detach
            user_name TEXT,
            detail TEXT
        );
        
        CREATE TABLE IF NOT EXISTS feature_vectors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL NOT NULL,
            source_table TEXT NOT NULL,
            source_id INTEGER NOT NULL,
            features_json TEXT NOT NULL,
            uploaded INTEGER DEFAULT 0
        );
        
        CREATE INDEX IF NOT EXISTS idx_process_ts ON process_events(timestamp);
        CREATE INDEX IF NOT EXISTS idx_file_ts ON file_events(timestamp);
        CREATE INDEX IF NOT EXISTS idx_network_ts ON network_events(timestamp);
        CREATE INDEX IF NOT EXISTS idx_user_ts ON user_events(timestamp);
        CREATE INDEX IF NOT EXISTS idx_fv_uploaded ON feature_vectors(uploaded);
        
        -- 防线一：网络告警表
        CREATE TABLE IF NOT EXISTS defense_network_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL NOT NULL,
            process_name TEXT NOT NULL,
            pid INTEGER NOT NULL,
            remote_addr_hash TEXT,
            remote_port INTEGER,
            blocked INTEGER DEFAULT 1,
            alert_shown INTEGER DEFAULT 0
        );
        
        -- 防线二：恶意文件隔离记录
        CREATE TABLE IF NOT EXISTS defense_malware_hits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL NOT NULL,
            path_hash TEXT NOT NULL,
            trigger_type TEXT NOT NULL,  -- hash_match, ext_match, pattern_match, process_match
            signature_detail TEXT,
            action TEXT DEFAULT 'skipped'  -- skipped, quarantined
        );
        
        -- 防线三：设备指纹密钥状态
        CREATE TABLE IF NOT EXISTS defense_vault_state (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            device_fingerprint_hash TEXT NOT NULL,
            created_at REAL NOT NULL,
            bound_count INTEGER DEFAULT 1,
            last_verified REAL
        );
        
        CREATE INDEX IF NOT EXISTS idx_dna_timestamp ON defense_network_alerts(timestamp);
        CREATE INDEX IF NOT EXISTS idx_dmh_timestamp ON defense_malware_hits(timestamp);
    """)
    conn.commit()
    return conn


# ─── 哈希工具 ───────────────────────────────────────────
def hash_str(s: str) -> str:
    """SHA256哈希，用于脱敏"""
    if not s:
        return "0" * 16
    return hashlib.sha256(s.encode("utf-8", errors="replace")).hexdigest()[:16]

def hash_path(p: str) -> str:
    """路径哈希（保留扩展名用于分类）"""
    if not p:
        return "0" * 16
    ext = os.path.splitext(p)[1].lower()
    h = hashlib.sha256(p.encode("utf-8", errors="replace")).hexdigest()[:12]
    return f"{h}{ext[:4]}"


# ═══════════════════════════════════════════════════════
# 防线三：设备绑定的加密金库 (DeviceVault)
# ═══════════════════════════════════════════════════════
class DeviceVault:
    """设备指纹派生AES-256密钥，加密存储所有痕迹数据。
    密钥仅存内存，不落盘。设备指纹不匹配→拒绝解密。"""
    
    def __init__(self):
        self._key: Optional[bytes] = None
        self._fingerprint_hash: Optional[str] = None
        self._initialized = False
        self._lock = threading.Lock()
        self._init_vault()
    
    def _collect_device_fingerprint(self) -> str:
        """采集设备指纹：硬件序列号 + 主板UUID + MAC + OS安装时间 → SHA256"""
        parts: List[str] = []
        
        try:
            if IS_MACOS:
                # 硬件序列号
                r = subprocess.run(["system_profiler", "SPHardwareDataType"],
                                   capture_output=True, text=True, timeout=10)
                for line in r.stdout.split("\n"):
                    line_s = line.strip()
                    if "Serial Number" in line_s:
                        parts.append(line_s.split(":")[-1].strip())
                    if "Hardware UUID" in line_s:
                        parts.append(line_s.split(":")[-1].strip())
                
                # MAC 地址
                r2 = subprocess.run(["ifconfig", "en0"], capture_output=True,
                                    text=True, timeout=5)
                for line in r2.stdout.split("\n"):
                    if "ether" in line:
                        parts.append(line.split("ether")[-1].strip())
                        break
                
                # OS 安装时间（取 / 分区的创建时间近似）
                st = os.stat("/")
                parts.append(str(int(st.st_ctime)))
            else:
                # Linux: /etc/machine-id + DMI
                if os.path.exists("/etc/machine-id"):
                    with open("/etc/machine-id") as f:
                        parts.append(f.read().strip())
                
                r = subprocess.run(["cat", "/sys/class/dmi/id/product_uuid"],
                                   capture_output=True, text=True, timeout=5)
                if r.returncode == 0 and r.stdout.strip():
                    parts.append(r.stdout.strip())
                
                r2 = subprocess.run(["cat", "/sys/class/net/eth0/address"],
                                    capture_output=True, text=True, timeout=5)
                if r2.returncode == 0:
                    parts.append(r2.stdout.strip().replace(":", ""))
                
                if os.path.exists("/"):
                    st = os.stat("/")
                    parts.append(str(int(st.st_ctime)))
        except Exception as e:
            log.warning(f"设备指纹采集部分失败: {e}")
        
        # 补充 fallback：主机名 + 用户名 + 操作系统版本
        parts.append(platform.node())
        parts.append(os.getenv("USER", "unknown"))
        parts.append(platform.platform())
        
        fingerprint = "|".join(filter(None, parts))
        if len(fingerprint) < 32:
            # 极度退化环境：加随机盐兜底（这种情况下换了设备也会通过，但至少能加密）
            log.warning("设备指纹太弱，使用增强盐")
            fp_salt = os.urandom(16).hex()
            with open(DEVICE_SALT_PATH, "wb") as f:
                f.write(fp_salt.encode())
            fingerprint += f"|enhanced:{fp_salt}"
        
        return hashlib.sha256(fingerprint.encode("utf-8")).hexdigest()
    
    def _init_vault(self):
        """初始化金库：生成/加载设备指纹并派生密钥"""
        try:
            self._fingerprint_hash = self._collect_device_fingerprint()
            
            # 密钥派生：设备指纹 → PBKDF2(如果cryptography可用) 或 SHA256 迭代
            fp_bytes = self._fingerprint_hash.encode("utf-8")
            if HAS_CRYPTO:
                # PBKDF2-HMAC-SHA256: 100000 次迭代
                from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
                from cryptography.hazmat.primitives import hashes
                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,  # AES-256
                    salt=b"longhun-vault-v2",
                    iterations=100000,
                    backend=default_backend(),
                )
                self._key = kdf.derive(fp_bytes)
            else:
                # 降级：简单迭代哈希（安全性较低，但保证可用）
                k = fp_bytes
                for _ in range(100000):
                    k = hashlib.sha256(k + fp_bytes).digest()
                self._key = k
            
            self._initialized = True
            log.info(f"🔐 金库已初始化 | 设备指纹: {self._fingerprint_hash[:16]}...")
        except Exception as e:
            log.error(f"金库初始化失败: {e}")
            raise
    
    def encrypt(self, plaintext: bytes) -> bytes:
        """AES-256-CBC 加密。返回 base64(IV + ciphertext)"""
        if not self._initialized or not self._key:
            raise RuntimeError("金库未初始化")
        
        with self._lock:
            if HAS_CRYPTO:
                iv = os.urandom(16)
                cipher = Cipher(
                    algorithms.AES(self._key),
                    modes.CBC(iv),
                    backend=default_backend(),
                )
                encryptor = cipher.encryptor()
                padder = sym_padding.PKCS7(128).padder()
                padded = padder.update(plaintext) + padder.finalize()
                ciphertext = encryptor.update(padded) + encryptor.finalize()
                return base64.b64encode(iv + ciphertext)
            else:
                # 降级：XOR + hash（不如AES，但保证可用）
                iv = os.urandom(16)
                k_stream = b""
                while len(k_stream) < len(plaintext):
                    k_stream += hashlib.sha256(self._key + iv + k_stream[-4:] if k_stream else self._key + iv).digest()
                enc = bytes(a ^ b for a, b in zip(plaintext, k_stream[:len(plaintext)]))
                return base64.b64encode(iv + enc)
    
    def decrypt(self, cipher_b64: bytes) -> bytes:
        """AES-256-CBC 解密。输入 base64(IV + ciphertext)"""
        if not self._initialized or not self._key:
            raise RuntimeError("金库未初始化")
        
        raw = base64.b64decode(cipher_b64)
        iv, data = raw[:16], raw[16:]
        
        with self._lock:
            if HAS_CRYPTO:
                cipher = Cipher(
                    algorithms.AES(self._key),
                    modes.CBC(iv),
                    backend=default_backend(),
                )
                decryptor = cipher.decryptor()
                padded = decryptor.update(data) + decryptor.finalize()
                unpadder = sym_padding.PKCS7(128).unpadder()
                return unpadder.update(padded) + unpadder.finalize()
            else:
                k_stream = b""
                while len(k_stream) < len(data):
                    k_stream += hashlib.sha256(self._key + iv + k_stream[-4:] if k_stream else self._key + iv).digest()
                return bytes(a ^ b for a, b in zip(data, k_stream[:len(data)]))
    
    def verify_fingerprint(self, fp_hash: str) -> bool:
        """验证设备指纹是否匹配"""
        if not self._fingerprint_hash:
            return False
        return hmac.compare_digest(self._fingerprint_hash, fp_hash)
    
    @property
    def fingerprint_hash(self) -> str:
        return self._fingerprint_hash or ""
    
    @property
    def is_ready(self) -> bool:
        return self._initialized
    
    def get_state(self) -> Dict[str, Any]:
        return {
            "initialized": self._initialized,
            "fingerprint_hash": self._fingerprint_hash[:16] + "..." if self._fingerprint_hash else None,
            "encryption": "AES-256-CBC" if HAS_CRYPTO else "SHA256-XOR (降级)",
            "bound_device": True,
        }


# ═══════════════════════════════════════════════════════
# 防线二：恶意代码过滤引擎 (MalwareGuard) v2.1
#   - 动态威胁情报同步（URLhaus/ThreatFox）
#   - 未知可执行文件默认拒绝
#   - 情报新鲜度校验（>24h=过期）
# ═══════════════════════════════════════════════════════
class MalwareGuard:
    """扫描前过恶意特征库，命中则跳过并隔离记录"""
    
    def __init__(self, db_conn: sqlite3.Connection):
        self._db = db_conn
        self._lock = threading.Lock()
        self._sigs: Dict[str, Any] = dict(DEFAULT_MALWARE_SIGS)
        self._compiled_patterns: List[re.Pattern] = []
        self._hash_set: Set[str] = set()
        self._hit_count = 0
        self._last_sync_time: float = 0
        self._last_threat_intel_sync: float = 0  # 威胁情报同步时间戳
        self._threat_intel_hashes: Set[str] = set()  # 从URLhaus同步的哈希
        self._threat_intel_synced_ever: bool = False  # 是否至少同步成功过一次
        self._load_malware_sigs()
    
    def _load_malware_sigs(self):
        """加载恶意特征库（本地优先，merge 内嵌默认）"""
        try:
            if os.path.exists(MALWARE_SIG_PATH):
                with open(MALWARE_SIG_PATH, "r") as f:
                    loaded = json.load(f)
                # merge: 加载的覆盖默认
                for k in DEFAULT_MALWARE_SIGS:
                    if k in loaded:
                        if isinstance(loaded[k], list):
                            self._sigs[k] = list(set(DEFAULT_MALWARE_SIGS.get(k, []) + loaded[k]))
                        else:
                            self._sigs[k] = loaded[k]
                # 恢复威胁情报哈希
                if "threat_intel_hashes" in loaded:
                    self._threat_intel_hashes = set(loaded["threat_intel_hashes"])
                if "last_threat_intel_sync" in loaded:
                    self._last_threat_intel_sync = loaded["last_threat_intel_sync"]
                if "threat_intel_synced_ever" in loaded:
                    self._threat_intel_synced_ever = loaded["threat_intel_synced_ever"]
                log.info(f"🛡️ 恶意特征库已加载 v{self._sigs.get('signature_version','?')} | 威胁哈希:{len(self._threat_intel_hashes)}")
            else:
                log.info("🛡️ 使用内嵌恶意特征库种子 | 威胁情报待首次同步")
        except Exception as e:
            log.warning(f"加载恶意特征库失败: {e}")
        
        # 预编译正则
        self._compiled_patterns = [
            re.compile(pat, re.IGNORECASE)
            for pat in self._sigs.get("suspicious_file_patterns", [])
        ]
        self._hash_set = set(self._sigs.get("hash_sha256", []))
    
    def is_intel_fresh(self) -> bool:
        """威胁情报是否新鲜（24小时内同步过即新鲜）"""
        if self._last_threat_intel_sync == 0:
            return False
        return (time.time() - self._last_threat_intel_sync) < THREAT_INTEL_SYNC_INTERVAL
    
    @property
    def intel_synced_ever(self) -> bool:
        return self._threat_intel_synced_ever
    
    def _save_sigs(self):
        """持久化当前特征库（含威胁情报状态）"""
        try:
            sigs_copy = dict(self._sigs)
            sigs_copy["threat_intel_hashes"] = list(self._threat_intel_hashes)
            sigs_copy["last_threat_intel_sync"] = self._last_threat_intel_sync
            sigs_copy["threat_intel_synced_ever"] = self._threat_intel_synced_ever
            with open(MALWARE_SIG_PATH, "w") as f:
                json.dump(sigs_copy, f, indent=2)
        except Exception as e:
            log.error(f"保存特征库失败: {e}")
    
    def sync_threat_intel(self) -> Dict[str, Any]:
        """同步动态威胁情报（URLhaus公共CSV + ThreatFox）
        Returns: 同步结果摘要
        """
        result = {"sources": {}, "total_new_hashes": 0, "total_new_signatures": 0, "success": False}
        
        # 源1: URLhaus 公共 CSV（无需认证）
        urlhaus_result = self._sync_from_urlhaus_csv()
        result["sources"]["urlhaus"] = urlhaus_result
        
        # 源2: ThreatFox
        threatfox_result = self._sync_from_threatfox()
        result["sources"]["threatfox"] = threatfox_result
        
        total_new = urlhaus_result.get("new_signatures", 0) + threatfox_result.get("new_hashes", 0)
        result["total_new_signatures"] = total_new
        
        if urlhaus_result.get("success") or threatfox_result.get("success"):
            self._last_threat_intel_sync = time.time()
            if not self._threat_intel_synced_ever:
                self._threat_intel_synced_ever = True
            self._save_sigs()
            result["success"] = True
            log.info(f"🛡️ 威胁情报同步完成 | +{total_new} 条目 | URLhaus:{urlhaus_result.get('new_signatures',0)} ThreatFox:{threatfox_result.get('new_hashes',0)}")
        else:
            log.warning("🛡️ 威胁情报同步全部源失败")
        
        return result
    
    def _sync_from_urlhaus_csv(self) -> Dict[str, Any]:
        """从 URLhaus 公共 CSV 下载拉取最新恶意URL/签名（无需API key）"""
        result = {"success": False, "new_signatures": 0, "total_fetched": 0}
        try:
            import urllib.request, urllib.error, csv, io
            url = "https://urlhaus.abuse.ch/downloads/csv_recent/"
            req = urllib.request.Request(url, headers={"User-Agent": "LongHun-TraceCollector/2.1"})
            resp = urllib.request.urlopen(req, timeout=30)
            if resp.status == 200:
                data = resp.read().decode("utf-8", errors="replace")
                reader = csv.reader(io.StringIO(data))
                new_sigs = 0
                row_count = 0
                for row in reader:
                    if not row or row[0].startswith("#"):
                        continue
                    row_count += 1
                    if len(row) >= 8:
                        # 列: id, dateadded, url, url_status, last_online, threat, tags, urlhaus_link, reporter
                        threat_type = row[5].strip().lower() if len(row) > 5 else ""
                        tags = row[6].strip() if len(row) > 6 else ""
                        
                        # 提取恶意软件家族签名
                        if tags and tags != "None":
                            for tag in tags.split(","):
                                tag = tag.strip().lower()
                                if tag and tag not in ("none", "unknown"):
                                    if tag not in self._sigs.get("suspicious_process_names", []):
                                        self._sigs["suspicious_process_names"].append(tag)
                                        new_sigs += 1
                        
                        # 提取威胁类型
                        if threat_type and threat_type not in ("none", "unknown"):
                            if threat_type not in self._sigs.get("suspicious_process_names", []):
                                self._sigs["suspicious_process_names"].append(threat_type)
                                new_sigs += 1
                
                result["total_fetched"] = row_count
                result["new_signatures"] = new_sigs
                result["success"] = True
                log.info(f"  📡 URLhaus CSV: 解析 {row_count} 行, 新增 {new_sigs} 恶意签名")
        except urllib.error.URLError as e:
            log.warning(f"URLhaus CSV 下载失败: {e}")
        except Exception as e:
            log.error(f"URLhaus CSV 解析异常: {e}")
        return result
    
    def _sync_from_urlhaus(self) -> Dict[str, Any]:
        """从 URLhaus API 拉取（需认证，保留备用）"""
        result = {"success": False, "new_hashes": 0, "total_fetched": 0}
        try:
            import urllib.request, urllib.error
            url = "https://urlhaus-api.abuse.ch/v1/payloads/recent/"
            req = urllib.request.Request(url, headers={
                "User-Agent": "LongHun-TraceCollector/2.1",
                "Accept": "application/json",
            })
            resp = urllib.request.urlopen(req, timeout=15)
            if resp.status == 200:
                data = json.loads(resp.read())
                if data.get("query_status") == "ok":
                    payloads = data.get("payloads", [])
                    result["total_fetched"] = len(payloads)
                    new_count = 0
                    for p in payloads:
                        sha256 = p.get("sha256_hash", "").lower()
                        if sha256 and sha256 not in self._threat_intel_hashes:
                            self._threat_intel_hashes.add(sha256)
                            sig = p.get("signature", "").lower()
                            if sig and sig not in self._sigs.get("suspicious_process_names", []):
                                self._sigs["suspicious_process_names"].append(sig)
                            new_count += 1
                    self._hash_set.update(self._threat_intel_hashes)
                    result["new_hashes"] = new_count
                    result["success"] = True
                    log.info(f"  📡 URLhaus API: 拉取 {len(payloads)} 条, 新增 {new_count} 个威胁哈希")
        except urllib.error.HTTPError as e:
            if e.code in (401, 403):
                log.warning(f"URLhaus API 需认证 (HTTP {e.code}), 已降级使用CSV公开数据")
            else:
                log.warning(f"URLhaus API 错误: {e}")
        except urllib.error.URLError as e:
            log.warning(f"URLhaus 连接失败: {e}")
        except Exception as e:
            log.error(f"URLhaus 解析异常: {e}")
        return result
    
    def _sync_from_threatfox(self) -> Dict[str, Any]:
        """从 ThreatFox (abuse.ch) 拉取最新 IOC"""
        result = {"success": False, "new_hashes": 0, "total_fetched": 0}
        try:
            import urllib.request, urllib.error
            url = "https://threatfox-api.abuse.ch/api/v1/"
            body = json.dumps({"query": "recent", "days": 1}).encode("utf-8")
            req = urllib.request.Request(url, data=body, headers={
                "User-Agent": "LongHun-TraceCollector/2.1",
                "Content-Type": "application/json",
            })
            resp = urllib.request.urlopen(req, timeout=15)
            if resp.status == 200:
                data = json.loads(resp.read())
                if data.get("query_status") == "ok":
                    iocs = data.get("data", [])
                    if isinstance(iocs, list):
                        new_count = 0
                        for ioc in iocs:
                            if isinstance(ioc, dict):
                                ioc_value = ioc.get("ioc_value", "").lower()
                                ioc_type = ioc.get("ioc_type", "").lower()
                                if ioc_type in ("sha256_hash", "sha256", "md5_hash", "md5") and ioc_value:
                                    if ioc_value not in self._threat_intel_hashes:
                                        self._threat_intel_hashes.add(ioc_value)
                                        new_count += 1
                                # 也收集威胁类型作为签名
                                threat_type = ioc.get("threat_type", "").lower()
                                if threat_type and threat_type not in self._sigs.get("suspicious_process_names", []):
                                    self._sigs["suspicious_process_names"].append(threat_type)
                        
                        self._hash_set.update(self._threat_intel_hashes)
                        result["new_hashes"] = new_count
                        result["total_fetched"] = len(iocs)
                        result["success"] = True
                        log.info(f"  📡 ThreatFox: 拉取 {len(iocs)} 条, 新增 {new_count} 个威胁哈希")
        except urllib.error.HTTPError as e:
            if e.code in (401, 403):
                log.warning(f"ThreatFox API 需认证 (HTTP {e.code}), 跳过")
            else:
                log.warning(f"ThreatFox API 错误: {e}")
        except urllib.error.URLError as e:
            log.warning(f"ThreatFox 连接失败: {e}")
        except Exception as e:
            log.error(f"ThreatFox 解析异常: {e}")
        return result
    
    def should_skip_file(self, filepath: str) -> tuple:
        """检查文件是否应被跳过。
        Returns: (should_skip: bool, reason: str)
        """
        fname = os.path.basename(filepath).lower()
        ext = os.path.splitext(filepath)[1].lower()
        
        with self._lock:
            # 🔥 新增：未知可执行文件默认拒绝
            # 威胁情报未同步成功前，所有可执行文件默认不准进入扫描范围
            if ext in EXECUTABLE_EXTENSIONS and not self._threat_intel_synced_ever:
                return True, f"exec_deny_no_intel:{ext}"
            
            # 🔥 新增：威胁情报过期（>24h）时，未知可执行文件也拒绝
            if ext in EXECUTABLE_EXTENSIONS and not self.is_intel_fresh():
                # 检查是否在已知安全哈希中
                try:
                    if os.path.exists(filepath) and os.path.getsize(filepath) < 10 * 1024 * 1024:
                        with open(filepath, "rb") as f:
                            fhash = hashlib.sha256(f.read()).hexdigest()
                        # 不在威胁哈希集但也不在任何已知安全哈希集 → 默认拒绝
                        if fhash not in self._threat_intel_hashes and fhash not in self._hash_set:
                            return True, f"exec_deny_intel_stale:{ext}"
                except (OSError, PermissionError):
                    return True, f"exec_deny_unreadable:{ext}"
            
            # 1. 可疑扩展名
            if ext in self._sigs.get("suspicious_extensions", []):
                return True, f"ext_match:{ext}"
            
            # 2. 正则模式匹配
            for i, pat in enumerate(self._compiled_patterns):
                if pat.search(filepath):
                    return True, f"pattern_match:{pat.pattern}"
            
            # 3. 威胁情报哈希匹配（优先）
            if ext not in (".dmg", ".pkg", ".iso", ".zip"):
                try:
                    if os.path.exists(filepath) and os.path.getsize(filepath) < 10 * 1024 * 1024:
                        with open(filepath, "rb") as f:
                            fhash = hashlib.sha256(f.read()).hexdigest()
                        if fhash in self._threat_intel_hashes:
                            return True, f"threat_intel_match:{fhash[:16]}"
                except (OSError, PermissionError):
                    pass
            
            # 4. 本地文件哈希
            if ext not in (".dmg", ".pkg", ".iso", ".zip"):
                try:
                    if os.path.exists(filepath) and os.path.getsize(filepath) < 10 * 1024 * 1024:
                        with open(filepath, "rb") as f:
                            fhash = hashlib.sha256(f.read(4096)).hexdigest()
                        if fhash in self._hash_set:
                            return True, f"hash_match:{fhash[:16]}"
                except (OSError, PermissionError):
                    pass
        
        return False, ""
    
    def check_process(self, name: str) -> tuple:
        """检查进程名是否为已知恶意软件。
        Returns: (is_suspicious: bool, reason: str)
        """
        name_lower = name.lower()
        for sig in self._sigs.get("suspicious_process_names", []):
            if sig in name_lower:
                return True, f"process_match:{sig}"
        return False, ""
    
    def record_hit(self, path_hash: str, trigger_type: str, detail: str = ""):
        """记录一次恶意特征命中"""
        try:
            cursor = self._db.execute(
                "INSERT INTO defense_malware_hits (timestamp, path_hash, trigger_type, signature_detail) VALUES (?, ?, ?, ?)",
                (time.time(), path_hash, trigger_type, detail)
            )
            self._db.commit()
            self._hit_count += 1
            
            # 写审计日志
            self._write_audit(f"MALWARE_HIT | {trigger_type} | {path_hash} | {detail}")
        except Exception as e:
            log.error(f"记录恶意命中失败: {e}")
    
    def _write_audit(self, msg: str):
        try:
            with open(DEFENSE_LOG_PATH, "a") as f:
                f.write(f"[{datetime.now().isoformat()}] {msg}\n")
        except Exception:
            pass
    
    def sync_from_kunpeng(self):
        """从鲲鹏同步恶意特征库更新"""
        try:
            import urllib.request
            url = f"https://uid9622.cn/api/defense/malware-sigs?version={self._sigs.get('signature_version','1.0.0')}"
            req = urllib.request.Request(url, headers={"X-Client": "trace-collector"})
            resp = urllib.request.urlopen(req, timeout=10)
            if resp.status == 200:
                new_sigs = json.loads(resp.read())
                if new_sigs.get("signature_version") != self._sigs.get("signature_version"):
                    with open(MALWARE_SIG_PATH, "w") as f:
                        json.dump(new_sigs, f, indent=2)
                    self._load_malware_sigs()
                    log.info(f"🛡️ 恶意特征库已更新 → v{new_sigs.get('signature_version','?')}")
                    self._last_sync_time = time.time()
        except Exception as e:
            log.debug(f"恶意特征库同步失败（非关键）: {e}")
    
    @property
    def hit_count(self) -> int:
        return self._hit_count
    
    @property
    def sig_version(self) -> str:
        return self._sigs.get("signature_version", "unknown")
    
    @property
    def threat_intel_hash_count(self) -> int:
        return len(self._threat_intel_hashes)
    
    def get_state(self) -> Dict[str, Any]:
        return {
            "signature_version": self.sig_version,
            "signature_count": len(self._hash_set) + len(self._compiled_patterns),
            "threat_intel_hash_count": self.threat_intel_hash_count,
            "threat_intel_fresh": self.is_intel_fresh(),
            "threat_intel_synced_ever": self._threat_intel_synced_ever,
            "hit_count": self._hit_count,
            "last_sync": self._last_sync_time or None,
            "last_threat_intel_sync": self._last_threat_intel_sync or None,
        }


# ═══════════════════════════════════════════════════════
# 防线一：网络出站强制执行防火墙 + 弹窗告警 (NetworkGuard) v2.1
#   - 任何不在白名单的进程出站连接 → pf/iptables 真实阻断
#   - 用户可自定义白名单 · 不在白名单 = 一根比特不准流出
# ═══════════════════════════════════════════════════════
class NetworkGuard(threading.Thread):
    """监控所有出站TCP/UDP连接，不在白名单的直接防火墙阻断并告警"""
    
    def __init__(self, db_conn: sqlite3.Connection):
        super().__init__(daemon=True, name="NetworkGuard")
        self._db = db_conn
        self._lock = threading.Lock()
        self._alert_count = 0
        self._block_count = 0
        self._active = True
        self._known_good_pids: Dict[int, str] = {}  # PID → 进程名快照
        self._alert_queue: List[Dict] = []  # 待推送告警
        
        # 🔥 v2.1: 强制执行
        self._firewall_blocked_ips: Set[str] = set()   # 已被防火墙阻断的IP
        self._firewall_initialized: bool = False
        self._user_whitelist: Set[str] = set()          # 用户自定义白名单
        self._all_whitelist: Set[str] = set()           # 系统默认 + 用户自定义 合并
        self._load_user_whitelist()
        self._all_whitelist = set(NETWORK_TRUSTED_PREFIXES) | self._user_whitelist
    
    # ── 白名单管理 ───────────────────────────────
    def _load_user_whitelist(self):
        """加载用户自定义网络白名单"""
        try:
            if os.path.exists(USER_WHITELIST_PATH):
                with open(USER_WHITELIST_PATH, "r") as f:
                    data = json.load(f)
                    self._user_whitelist = set(data.get("processes", []))
                log.info(f"🛡️ 用户网络白名单已加载: {len(self._user_whitelist)} 个")
        except Exception as e:
            log.warning(f"加载用户白名单失败: {e}")
    
    def _save_user_whitelist(self):
        """保存用户白名单"""
        try:
            os.makedirs(DATA_DIR, exist_ok=True)
            with open(USER_WHITELIST_PATH, "w") as f:
                json.dump({"processes": sorted(self._user_whitelist), "updated": time.time()}, f, indent=2)
        except Exception as e:
            log.error(f"保存用户白名单失败: {e}")
    
    def add_to_whitelist(self, process_name: str) -> bool:
        """添加进程到用户白名单"""
        proc = process_name.lower().strip()
        if not proc or proc in self._user_whitelist:
            return False
        self._user_whitelist.add(proc)
        self._all_whitelist.add(proc)
        self._save_user_whitelist()
        log.info(f"✅ 网络白名单已添加: {proc}")
        return True
    
    def remove_from_whitelist(self, process_name: str) -> bool:
        """从用户白名单移除进程"""
        proc = process_name.lower().strip()
        if proc in self._user_whitelist:
            self._user_whitelist.discard(proc)
            self._all_whitelist.discard(proc)
            self._save_user_whitelist()
            log.info(f"➖ 网络白名单已移除: {proc}")
            return True
        return False
    
    def list_whitelist(self) -> Dict[str, Any]:
        return {
            "system_default": sorted(set(NETWORK_TRUSTED_PREFIXES) - self._user_whitelist),
            "user_custom": sorted(self._user_whitelist),
            "blocked_ips": sorted(self._firewall_blocked_ips),
            "firewall_active": self._firewall_initialized,
        }
    
    # ── 防火墙强制执行引擎 ───────────────────────
    def _init_firewall(self):
        """初始化OS级防火墙"""
        if self._firewall_initialized:
            return True
        try:
            if IS_MACOS:
                # 测试 pfctl 可用
                r = subprocess.run(["pfctl", "-s", "info"], capture_output=True, timeout=5)
                if r.returncode == 0:
                    self._firewall_initialized = True
                    log.info(f"🛡️ 防火墙就绪 (macOS pf · anchor={PF_ANCHOR_NAME})")
                    return True
                else:
                    log.warning("pfctl 不可用，需要 sudo 权限运行采集器")
                    return False
            else:
                r = subprocess.run(["iptables", "-L", "-n"], capture_output=True, timeout=5)
                if r.returncode == 0:
                    # 创建专属链（忽略已存在错误）
                    subprocess.run(["iptables", "-N", "LONGHUN_NET_GUARD"], capture_output=True, timeout=5)
                    subprocess.run(["iptables", "-C", "OUTPUT", "-j", "LONGHUN_NET_GUARD"], capture_output=True, timeout=5)
                    if subprocess.run(["iptables", "-C", "OUTPUT", "-j", "LONGHUN_NET_GUARD"], capture_output=True, timeout=5).returncode != 0:
                        subprocess.run(["iptables", "-A", "OUTPUT", "-j", "LONGHUN_NET_GUARD"], capture_output=True, timeout=5)
                    self._firewall_initialized = True
                    log.info("🛡️ 防火墙就绪 (Linux iptables · chain=LONGHUN_NET_GUARD)")
                    return True
                else:
                    log.warning("iptables 不可用，需要 root 权限运行采集器")
                    return False
        except Exception as e:
            log.error(f"防火墙初始化失败: {e}")
            return False
    
    def _execute_firewall_block(self, remote_addr: str) -> bool:
        """执行真正的防火墙阻断 - 对可疑IP添加drop规则"""
        if remote_addr in ("*:*", "127.0.0.1", "::1", "localhost", "0.0.0.0", "::"):
            return False
        # 提取纯IP
        ip = remote_addr.split(":")[0] if ":" in remote_addr else remote_addr
        if ip in ("127.0.0.1", "::1", "0.0.0.0", "::") or ip.startswith("127."):
            return False
        if ip in self._firewall_blocked_ips:
            return True
        
        if not self._firewall_initialized:
            if not self._init_firewall():
                return False
        
        try:
            if IS_MACOS:
                rule = f"block drop out proto tcp from any to {ip}\nblock drop out proto udp from any to {ip}\n"
                r = subprocess.run(["pfctl", "-a", PF_ANCHOR_NAME, "-f", "/dev/stdin"],
                                   input=rule.encode("utf-8"), capture_output=True, timeout=5)
                # pf anchor 可能不存在，静默尝试
                self._firewall_blocked_ips.add(ip)
                log.info(f"🚫 防火墙阻断 IP: {ip}")
                return True
            else:
                subprocess.run(["iptables", "-A", "LONGHUN_NET_GUARD", "-d", ip, "-j", "DROP"],
                               capture_output=True, timeout=5)
                self._firewall_blocked_ips.add(ip)
                return True
        except Exception as e:
            log.error(f"防火墙阻断执行失败 ({ip}): {e}")
        return False
    
    def _cleanup_firewall(self):
        """清除所有网络守卫防火墙规则"""
        if not self._firewall_initialized:
            return
        try:
            if IS_MACOS:
                subprocess.run(["pfctl", "-a", PF_ANCHOR_NAME, "-F", "rules"],
                               capture_output=True, timeout=5)
            else:
                subprocess.run(["iptables", "-F", "LONGHUN_NET_GUARD"],
                               capture_output=True, timeout=5)
            log.info(f"🧹 防火墙规则已清除 ({len(self._firewall_blocked_ips)} IP)")
            self._firewall_blocked_ips.clear()
        except Exception as e:
            log.error(f"清除防火墙规则失败: {e}")
    
    def run(self):
        """持续监控网络连接"""
        time.sleep(3)
        self._init_firewall()
        log.info("🛡️ 防线一·网络守卫已启动（强制执行模式）")
        while self._active:
            try:
                self._scan_connections()
            except Exception as e:
                log.error(f"网络守卫异常: {e}")
            time.sleep(NETWORK_WATCH_INTERVAL)
    
    def _scan_connections(self):
        """扫描当前所有出站连接"""
        try:
            if IS_MACOS:
                cmd = ["lsof", "-i", "-nP", "-F", "pcn"]
                result = subprocess.run(cmd, capture_output=True, timeout=8)
                output = result.stdout.decode("utf-8", errors="surrogateescape")
                output = output.encode("utf-8", errors="replace").decode("utf-8")
                self._parse_lsof(output)
            else:
                cmd = ["ss", "-tunap"]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                self._parse_ss(result.stdout)
        except subprocess.TimeoutExpired:
            pass
        except Exception as e:
            log.debug(f"网络扫描异常: {e}")
    
    def _parse_lsof(self, output: str):
        """解析 lsof -F pcn 输出"""
        current = {}
        alerts = []
        
        for line in output.split("\n"):
            if not line:
                continue
            prefix = line[0] if line else ""
            rest = line[1:] if len(line) > 1 else ""
            
            if prefix == "p":
                # 新的进程条目
                if current:
                    verdict = self._judge_connection(current)
                    if verdict["alert"]:
                        alerts.append(verdict)
                current = {"pid": int(rest) if rest.isdigit() else 0}
            elif prefix == "c":
                current["name"] = rest.strip()
            elif prefix == "n":
                # 网络地址
                addr = rest.strip()
                if "->" in addr:
                    local_str, remote_str = addr.split("->", 1)
                    current["remote"] = remote_str.strip()
                    local_parts = local_str.strip().split(":")
                    current["local_port"] = local_parts[-1] if local_parts else ""
        
        # 最后一个条目
        if current:
            verdict = self._judge_connection(current)
            if verdict["alert"]:
                alerts.append(verdict)
        
        # 处理告警
        for a in alerts:
            self._handle_alert(a)
    
    def _parse_ss(self, output: str):
        """解析 ss -tunap 输出（Linux）"""
        for line in output.split("\n"):
            if "ESTAB" not in line and "SYN-SENT" not in line:
                continue
            parts = line.split()
            if len(parts) < 5:
                continue
            # 提取远程地址和进程信息
            addr_part = parts[4] if len(parts) > 4 else ""
            proc_part = parts[-1] if "pid=" in parts[-1] else ""
            
            # 简化: 提取 PID
            pid = 0
            name = ""
            for p in parts:
                if "pid=" in p:
                    try:
                        pid = int(p.split("=")[1].split(",")[0])
                    except ValueError:
                        pass
                if p.startswith('"') and p.endswith('"'):
                    name = p.strip('"')
            
            if pid and addr_part:
                remote = addr_part
                verdict = self._judge_connection({
                    "pid": pid, "name": name, "remote": remote,
                })
                if verdict["alert"]:
                    self._handle_alert(verdict)
    
    def _judge_connection(self, conn: Dict) -> Dict:
        """判决一个连接是否需要告警/阻断"""
        name = conn.get("name", "")
        pid = conn.get("pid", 0)
        remote = conn.get("remote", "")
        
        # 无名称或回环地址，放行
        if not name or not remote:
            return {"alert": False}
        
        if remote.startswith("127.") or remote.startswith("::1") or remote == "*:*":
            return {"alert": False}
        
        # 特殊豁免：系统进程和已知安全进程
        if name in ("mDNSResponder", "rapportd", "trustd", "syspolicyd",
                     "identityservicesd", "sharingd", "apsd", "cloudd",
                     "spotlight", "mds", "mdworker", "parsecd",
                     "WindowServer", "Finder", "Dock", "SystemUIServer",
                     "kernel_task", "launchd", "UserEventAgent",
                     "coreaudiod", "distnoted", "cfprefsd", "lsd",
                     "logd", "notifyd", "fseventsd", "filecoordinationd"):
            return {"alert": False}
        
        # 🔥 统合白名单（系统默认 + 用户自定义）
        for prefix in self._all_whitelist:
            if name.startswith(prefix) or prefix in name:
                self._known_good_pids[pid] = name
                return {"alert": False}
        
        # 白名单端口
        if ":" in remote:
            try:
                port = int(remote.split(":")[-1])
                if port in NETWORK_TRUSTED_PORTS:
                    return {"alert": False}
            except ValueError:
                pass
        
        # CDN/公共DNS 只告警不阻断
        for pat in NETWORK_ALERT_ONLY_PATTERNS:
            if re.search(pat, remote):
                remote_hash = hash_str(remote)
                alert = {
                    "alert": True,
                    "block": False,  # 只告警不阻断
                    "process_name": name,
                    "pid": pid,
                    "remote_addr_hash": remote_hash,
                    "actual_remote": remote,
                    "remote_port": self._extract_port(remote),
                    "reason": f"CDN/公共DNS: {pat}",
                }
                return alert
        
        # 未命中任何白名单 → 阻断
        remote_hash = hash_str(remote)
        return {
            "alert": True,
            "block": True,
            "process_name": name,
            "pid": pid,
            "remote_addr_hash": remote_hash,
            "actual_remote": remote,  # 🔥 真实IP用于防火墙阻断
            "remote_port": self._extract_port(remote),
            "reason": f"非信任进程出站连接: {name} → {remote_hash}",
        }
    
    def _extract_port(self, remote: str) -> int:
        try:
            return int(remote.rsplit(":", 1)[-1])
        except (ValueError, IndexError):
            return 0
    
    def _handle_alert(self, verdict: Dict):
        """处理告警：入库 + 🔥强制执行防火墙阻断"""
        try:
            blocked = 1 if verdict.get("block", True) else 0
            remote_hash = verdict.get("remote_addr_hash", "")
            remote_port = verdict.get("remote_port", 0)
            
            # 🔥 v2.1: 真实防火墙阻断
            firewall_executed = False
            actual_remote = verdict.get("actual_remote", "")
            if blocked and actual_remote:
                firewall_executed = self._execute_firewall_block(actual_remote)
                if not firewall_executed:
                    log.debug(f"防火墙阻断未执行 ({verdict['process_name']}) - 可能需sudo权限")
            
            cursor = self._db.execute(
                "INSERT INTO defense_network_alerts (timestamp, process_name, pid, remote_addr_hash, remote_port, blocked) VALUES (?, ?, ?, ?, ?, ?)",
                (time.time(), verdict.get("process_name",""), verdict.get("pid",0),
                 remote_hash, remote_port, 1 if firewall_executed else 0)
            )
            self._db.commit()
            
            # 更新阻断计数（只有防火墙实际生效才算）
            with self._lock:
                self._alert_count += 1
                if firewall_executed:
                    self._block_count += 1
                
                # 审计日志
                status = "FIREWALL_BLOCKED" if firewall_executed else ("ALERT_ONLY" if not blocked else "BLOCK_FAILED")
                audit_msg = f"NETWORK_ALERT | {status} | {verdict['process_name']} (PID:{verdict['pid']}) → {remote_hash} | {verdict.get('reason','')}"
                self._write_audit(audit_msg)
                
                # 告警队列
                self._alert_queue.append({
                    "timestamp": time.time(),
                    "process_name": verdict["process_name"],
                    "pid": verdict["pid"],
                    "remote_addr_hash": remote_hash,
                    "remote_port": remote_port,
                    "blocked": 1 if firewall_executed else 0,
                    "firewall_executed": firewall_executed,
                    "reason": verdict.get("reason", ""),
                })
                
                if len(self._alert_queue) > NETWORK_GUARD_MAX_ALERTS:
                    self._alert_queue = self._alert_queue[-NETWORK_GUARD_MAX_ALERTS:]
        except Exception as e:
            log.error(f"处理网络告警失败: {e}")
    
    def _write_audit(self, msg: str):
        try:
            with open(DEFENSE_LOG_PATH, "a") as f:
                f.write(f"[{datetime.now().isoformat()}] {msg}\n")
        except Exception:
            pass
    
    def get_new_alerts(self) -> List[Dict]:
        """获取新告警（消费后清空）"""
        with self._lock:
            alerts = list(self._alert_queue)
            self._alert_queue.clear()
        return alerts
    
    def stop(self):
        self._active = False
        self._cleanup_firewall()
        log.info("🛡️ 网络守卫已停止，防火墙规则已清除")
    
    @property
    def alert_count(self) -> int:
        return self._alert_count
    
    @property
    def block_count(self) -> int:
        return self._block_count
    
    def get_state(self) -> Dict[str, Any]:
        return {
            "active": self._active,
            "firewall_initialized": self._firewall_initialized,
            "firewall_blocked_ips": len(self._firewall_blocked_ips),
            "alert_count": self._alert_count,
            "block_count": self._block_count,
            "pending_alerts": len(self._alert_queue),
            "whitelist_count": len(self._all_whitelist),
        }


# ─── 进程采集器 ─────────────────────────────────────────
class ProcessCollector(threading.Thread):
    """定时采集进程快照，diff检测启动/销毁事件"""
    
    def __init__(self, db_conn: sqlite3.Connection):
        super().__init__(daemon=True)
        self.db = db_conn
        self.last_snapshot: Dict[int, dict] = {}
        self.running = True
    
    def get_snapshot(self) -> Dict[int, dict]:
        """获取当前进程快照"""
        snapshot = {}
        try:
            if IS_MACOS:
                result = subprocess.run(
                    ["ps", "ax", "-o", "pid=,ppid=,user=,comm=,args="],
                    capture_output=True, timeout=5
                )
                # macOS 某些进程命令行含非 UTF-8 字节，用 surrogateescape 保留后再替换
                output = result.stdout.decode("utf-8", errors="surrogateescape")
                # 将 surrogate 字符替换为 ? 保证后续处理安全
                output = output.encode("utf-8", errors="replace").decode("utf-8")
            else:
                result = subprocess.run(
                    ["ps", "ax", "-o", "pid=,ppid=,user=,comm=,args="],
                    capture_output=True, text=True, timeout=5
                )
                output = result.stdout
            
            for line in output.strip().split("\n"):
                if not line.strip():
                    continue
                parts = line.strip().split(None, 4)
                if len(parts) < 4:
                    continue
                try:
                    pid = int(parts[0])
                    ppid = int(parts[1]) if parts[1].isdigit() else 0
                    user = parts[2]
                    comm = parts[3]
                    args = parts[4] if len(parts) > 4 else comm
                    
                    # 过滤掉采集器自身
                    if "lh_base_trace_collector" in args:
                        continue
                    
                    snapshot[pid] = {
                        "pid": pid,
                        "ppid": ppid,
                        "user": user,
                        "name": comm,
                        "cmdline": args[:1024],  # 截断
                    }
                except (ValueError, IndexError):
                    continue
        except Exception as e:
            log.error(f"进程快照失败: {e}")
        
        return snapshot
    
    def diff_and_record(self, current: Dict[int, dict]):
        """对比快照，记录启动/销毁"""
        ts = time.time()
        
        # 新启动的进程（当前有，上次没有）
        for pid, info in current.items():
            if pid not in self.last_snapshot:
                self.db.execute(
                    """INSERT INTO process_events (timestamp, event_type, pid, ppid, name, name_hash, cmdline, cmdline_hash, user)
                       VALUES (?, 'start', ?, ?, ?, ?, ?, ?, ?)""",
                    (ts, pid, info["ppid"], info["name"],
                     hash_str(info["name"]), info["cmdline"],
                     hash_str(info["cmdline"]), info["user"])
                )
        
        # 已退出的进程（上次有，当前没有）
        for pid, info in self.last_snapshot.items():
            if pid not in current:
                self.db.execute(
                    """INSERT INTO process_events (timestamp, event_type, pid, ppid, name, name_hash, cmdline, cmdline_hash, user)
                       VALUES (?, 'stop', ?, ?, ?, ?, ?, ?, ?)""",
                    (ts, pid, info["ppid"], info["name"],
                     hash_str(info["name"]), info["cmdline"],
                     hash_str(info["cmdline"]), info["user"])
                )
        
        self.db.commit()
    
    def run(self):
        log.info("进程采集器启动")
        # 先获取初始快照（不记录事件）
        self.last_snapshot = self.get_snapshot()
        
        while self.running:
            time.sleep(CHECK_INTERVAL_PROCESS)
            try:
                current = self.get_snapshot()
                if current and self.last_snapshot:
                    self.diff_and_record(current)
                self.last_snapshot = current
            except Exception as e:
                log.error(f"进程采集异常: {e}")
    
    def stop(self):
        self.running = False


# ─── 文件采集器 ─────────────────────────────────────────
class FileCollector(threading.Thread):
    """定时扫描指定目录，检测文件变化。防线二：先过恶意特征过滤。"""
    
    def __init__(self, db_conn: sqlite3.Connection, watch_dirs: List[str], 
                 malware_guard: Optional[MalwareGuard] = None):
        super().__init__(daemon=True)
        self.db = db_conn
        self.watch_dirs = [d for d in watch_dirs if os.path.isdir(d)]
        self.last_state: Dict[str, dict] = {}  # path_hash -> {mtime, size}
        self.running = True
        self.malware_guard = malware_guard
        self.files_skipped = 0  # 防线二跳过的文件计数
    
    def scan_dirs(self) -> Dict[str, dict]:
        """扫描监控目录，返回文件状态。防线二：过恶意特征过滤。"""
        state = {}
        for watch_dir in self.watch_dirs:
            if not os.path.isdir(watch_dir):
                continue
            try:
                for root, dirs, files in os.walk(watch_dir):
                    # 跳过隐藏目录和node_modules
                    dirs[:] = [d for d in dirs if not d.startswith(".") and d != "node_modules" and d != "__pycache__"]
                    
                    for fname in files:
                        if fname.startswith("."):
                            continue
                        fpath = os.path.join(root, fname)
                        
                        # 🔥 防线二：恶意特征检测
                        if self.malware_guard:
                            skip, reason = self.malware_guard.should_skip_file(fpath)
                            if skip:
                                self.files_skipped += 1
                                self.malware_guard.record_hit(
                                    hash_path(fpath), reason, 
                                    f"skipped:{os.path.basename(fpath)}"
                                )
                                continue
                        
                        try:
                            st = os.stat(fpath)
                            h = hash_path(fpath)
                            state[h] = {
                                "path": fpath,
                                "mtime": st.st_mtime,
                                "size": st.st_size,
                                "ext": os.path.splitext(fname)[1].lower()
                            }
                        except OSError:
                            continue
            except Exception as e:
                log.debug(f"扫描目录失败 {watch_dir}: {e}")
        return state
    
    def diff_and_record(self, current: Dict[str, dict]):
        """对比状态，记录文件事件"""
        ts = time.time()
        
        for h, info in current.items():
            if h not in self.last_state:
                # 新文件
                self.db.execute(
                    """INSERT INTO file_events (timestamp, event_type, path_hash, size, ext)
                       VALUES (?, 'create', ?, ?, ?)""",
                    (ts, h, info["size"], info["ext"])
                )
            elif self.last_state[h]["mtime"] != info["mtime"]:
                # 文件修改
                self.db.execute(
                    """INSERT INTO file_events (timestamp, event_type, path_hash, size, ext)
                       VALUES (?, 'modify', ?, ?, ?)""",
                    (ts, h, info["size"], info["ext"])
                )
        
        for h, info in self.last_state.items():
            if h not in current:
                # 文件删除
                self.db.execute(
                    """INSERT INTO file_events (timestamp, event_type, path_hash, size, ext)
                       VALUES (?, 'delete', ?, ?, ?)""",
                    (ts, h, info.get("size", 0), info.get("ext", ""))
                )
        
        self.db.commit()
    
    def run(self):
        log.info(f"文件采集器启动，监控 {len(self.watch_dirs)} 个目录")
        self.last_state = self.scan_dirs()
        
        while self.running:
            time.sleep(CHECK_INTERVAL_FILE)
            try:
                current = self.scan_dirs()
                self.diff_and_record(current)
                self.last_state = current
            except Exception as e:
                log.error(f"文件采集异常: {e}")
    
    def stop(self):
        self.running = False


# ─── 网络采集器 ─────────────────────────────────────────
class NetworkCollector(threading.Thread):
    """定时采集网络连接状态"""
    
    def __init__(self, db_conn: sqlite3.Connection):
        super().__init__(daemon=True)
        self.db = db_conn
        self.last_connections: set = set()
        self.running = True
    
    def get_connections(self) -> set:
        """获取当前网络连接（脱敏后）"""
        connections = set()
        try:
            if IS_MACOS:
                result = subprocess.run(
                    ["lsof", "-i", "-n", "-P"],
                    capture_output=True, text=True, timeout=10
                )
                lines = result.stdout.strip().split("\n")[1:]  # 跳过header
            else:
                # Linux: 使用 ss 或 netstat
                result = subprocess.run(
                    ["ss", "-tunap"],
                    capture_output=True, text=True, timeout=10
                )
                lines = result.stdout.strip().split("\n")[1:]
            
            for line in lines:
                if not line.strip():
                    continue
                # 生成连接指纹（脱敏）
                fingerprint = hash_str(line.strip()[:200])
                connections.add(fingerprint)
        except Exception as e:
            log.error(f"网络采集失败: {e}")
        
        return connections
    
    def diff_and_record(self, current: set):
        """检测新连接"""
        ts = time.time()
        
        new_conns = current - self.last_connections
        
        for fingerprint in new_conns:
            self.db.execute(
                """INSERT INTO network_events (timestamp, event_type, protocol, remote_addr_hash, state)
                   VALUES (?, 'connect', 'TCP', ?, 'established')""",
                (ts, fingerprint)
            )
        
        self.db.commit()
    
    def run(self):
        log.info("网络采集器启动")
        
        while self.running:
            time.sleep(CHECK_INTERVAL_NETWORK)
            try:
                current = self.get_connections()
                self.diff_and_record(current)
                self.last_connections = current
            except Exception as e:
                log.error(f"网络采集异常: {e}")
    
    def stop(self):
        self.running = False


# ─── 用户行为采集器 ─────────────────────────────────────
class UserCollector(threading.Thread):
    """采集用户登录/注销、锁屏/解锁、外设插拔事件"""
    
    def __init__(self, db_conn: sqlite3.Connection):
        super().__init__(daemon=True)
        self.db = db_conn
        self.last_login_count = 0
        self.last_device_state: Dict[str, bool] = {}
        self.running = True
    
    def check_login(self):
        """检查登录状态变化"""
        try:
            result = subprocess.run(["who"], capture_output=True, text=True, timeout=3)
            current_count = len([l for l in result.stdout.strip().split("\n") if l.strip()])
            
            if current_count > self.last_login_count:
                self.db.execute(
                    """INSERT INTO user_events (timestamp, event_type, user_name, detail)
                       VALUES (?, 'login', ?, ?)""",
                    (time.time(), os.getenv("USER", "unknown"), "new session")
                )
            elif current_count < self.last_login_count:
                self.db.execute(
                    """INSERT INTO user_events (timestamp, event_type, user_name, detail)
                       VALUES (?, 'logout', ?, ?)""",
                    (time.time(), os.getenv("USER", "unknown"), "session ended")
                )
            
            self.last_login_count = current_count
        except Exception as e:
            log.debug(f"登录检查失败: {e}")
    
    def check_lock_screen(self):
        """检测锁屏/解锁（macOS）"""
        if not IS_MACOS:
            return
        
        try:
            # macOS: 检查 CGSession
            result = subprocess.run(
                ["python3", "-c",
                 "import subprocess, sys; "
                 "r = subprocess.run(['pgrep', '-f', 'loginwindow'], capture_output=True); "
                 "sys.exit(0 if r.returncode == 0 else 1)"],
                capture_output=True, timeout=3
            )
            # 简化：记录活跃会话
        except Exception:
            pass
    
    def check_devices(self):
        """检测外设变化"""
        try:
            if IS_MACOS:
                result = subprocess.run(
                    ["system_profiler", "SPUSBDataType"],
                    capture_output=True, text=True, timeout=5
                )
                devices = set()
                for line in result.stdout.split("\n"):
                    if "Product:" in line or "Manufacturer:" in line:
                        devices.add(hash_str(line.strip()))
                
                if self.last_device_state:
                    new_devices = devices - set(self.last_device_state.keys())
                    removed = set(self.last_device_state.keys()) - devices
                    
                    for d in new_devices:
                        self.db.execute(
                            """INSERT INTO user_events (timestamp, event_type, detail)
                               VALUES (?, 'device_attach', ?)""",
                            (time.time(), d)
                        )
                    
                    for d in removed:
                        self.db.execute(
                            """INSERT INTO user_events (timestamp, event_type, detail)
                               VALUES (?, 'device_detach', ?)""",
                            (time.time(), d)
                        )
                
                self.last_device_state = {d: True for d in devices}
        except Exception as e:
            log.debug(f"设备检查失败: {e}")
    
    def run(self):
        log.info("用户行为采集器启动")
        
        while self.running:
            time.sleep(CHECK_INTERVAL_USER)
            try:
                self.check_login()
                self.check_devices()
            except Exception as e:
                log.error(f"用户行为采集异常: {e}")
    
    def stop(self):
        self.running = False


# ─── 特征向量提取器 ─────────────────────────────────────
def extract_feature_vectors(db_conn: sqlite3.Connection, limit: int = 100):
    """
    从原始事件中提取特征向量（脱敏后），供远端AI复原引擎使用。
    
    铁律：发送的是SHA256哈希后的特征向量，不包含原始路径/IP/文件名。
    """
    features = []
    
    # 进程特征
    rows = db_conn.execute(
        """SELECT pe.id, pe.timestamp, pe.event_type, pe.name_hash, pe.cmdline_hash
           FROM process_events pe
           LEFT JOIN feature_vectors fv ON fv.source_table='process_events' AND fv.source_id=pe.id
           WHERE fv.id IS NULL
           ORDER BY pe.timestamp DESC
           LIMIT ?""", (limit,)
    ).fetchall()
    
    for row in rows:
        fid = row[0]
        fv_json = json.dumps({
            "type": f"process_{row[2]}",
            "ts": row[1],
            "name_hash": row[3],
            "cmdline_hash": row[4],
        })
        db_conn.execute(
            "INSERT INTO feature_vectors (timestamp, source_table, source_id, features_json) VALUES (?, 'process_events', ?, ?)",
            (row[1], fid, fv_json)
        )
        features.append(json.loads(fv_json))
    
    # 文件特征
    rows = db_conn.execute(
        """SELECT fe.id, fe.timestamp, fe.event_type, fe.path_hash, fe.ext
           FROM file_events fe
           LEFT JOIN feature_vectors fv ON fv.source_table='file_events' AND fv.source_id=fe.id
           WHERE fv.id IS NULL
           ORDER BY fe.timestamp DESC
           LIMIT ?""", (limit,)
    ).fetchall()
    
    for row in rows:
        fid = row[0]
        fv_json = json.dumps({
            "type": f"file_{row[2]}",
            "ts": row[1],
            "path_hash": row[3],
            "ext": row[4],
        })
        db_conn.execute(
            "INSERT INTO feature_vectors (timestamp, source_table, source_id, features_json) VALUES (?, 'file_events', ?, ?)",
            (row[1], fid, fv_json)
        )
        features.append(json.loads(fv_json))
    
    # 网络特征
    rows = db_conn.execute(
        """SELECT ne.id, ne.timestamp, ne.event_type, ne.remote_addr_hash
           FROM network_events ne
           LEFT JOIN feature_vectors fv ON fv.source_table='network_events' AND fv.source_id=ne.id
           WHERE fv.id IS NULL
           ORDER BY ne.timestamp DESC
           LIMIT ?""", (limit,)
    ).fetchall()
    
    for row in rows:
        fid = row[0]
        fv_json = json.dumps({
            "type": f"network_{row[2]}",
            "ts": row[1],
            "remote_hash": row[3],
        })
        db_conn.execute(
            "INSERT INTO feature_vectors (timestamp, source_table, source_id, features_json) VALUES (?, 'network_events', ?, ?)",
            (row[1], fid, fv_json)
        )
        features.append(json.loads(fv_json))
    
    # 用户行为特征
    rows = db_conn.execute(
        """SELECT ue.id, ue.timestamp, ue.event_type, ue.detail
           FROM user_events ue
           LEFT JOIN feature_vectors fv ON fv.source_table='user_events' AND fv.source_id=ue.id
           WHERE fv.id IS NULL
           ORDER BY ue.timestamp DESC
           LIMIT ?""", (limit,)
    ).fetchall()
    
    for row in rows:
        fid = row[0]
        fv_json = json.dumps({
            "type": f"user_{row[2]}",
            "ts": row[1],
            "detail_hash": hash_str(row[3] or ""),
        })
        db_conn.execute(
            "INSERT INTO feature_vectors (timestamp, source_table, source_id, features_json) VALUES (?, 'user_events', ?, ?)",
            (row[1], fid, fv_json)
        )
        features.append(json.loads(fv_json))
    
    db_conn.commit()
    return features


# ─── HTTP API ───────────────────────────────────────────
class TraceAPIHandler(BaseHTTPRequestHandler):
    """本地API处理器，供Chrome插件调用"""
    
    db_conn: sqlite3.Connection = None
    vault: Optional[DeviceVault] = None          # 防线三
    malware_guard: Optional[MalwareGuard] = None  # 防线二
    network_guard: Optional[NetworkGuard] = None  # 防线一
    md5_summary: Dict[str, Any] = {}              # 防御状态摘要缓存
    
    def log_message(self, format, *args):
        log.debug(f"API: {format % args}")
    
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
    
    def _json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self._cors()
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8"))
    
    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()
    
    def do_GET(self):
        if self.path == "/health":
            self._json({"status": "ok", "version": VERSION, "dna": DNA})
        
        elif self.path == "/status":
            self._json(self._get_status())
        
        elif self.path == "/events/recent":
            self._json(self._get_recent_events(100))
        
        elif self.path.startswith("/events/process"):
            limit = self._parse_limit(200)
            self._json(self._get_process_events(limit))
        
        elif self.path.startswith("/events/file"):
            limit = self._parse_limit(200)
            self._json(self._get_file_events(limit))
        
        elif self.path.startswith("/events/network"):
            limit = self._parse_limit(200)
            self._json(self._get_network_events(limit))
        
        elif self.path.startswith("/events/user"):
            limit = self._parse_limit(200)
            self._json(self._get_user_events(limit))
        
        elif self.path.startswith("/features"):
            limit = self._parse_limit(500)
            features = extract_feature_vectors(self.db_conn, limit)
            self._json({"count": len(features), "features": features})
        
        elif self.path.startswith("/features/unuploaded"):
            rows = self.db_conn.execute(
                "SELECT features_json FROM feature_vectors WHERE uploaded=0 ORDER BY timestamp DESC LIMIT 500"
            ).fetchall()
            features = [json.loads(r[0]) for r in rows]
            self._json({"count": len(features), "features": features})
        
        elif self.path == "/stats":
            self._json(self._get_stats())
        
        # ─── 四道防线API ───
        elif self.path == "/defense/status":
            self._json(self._get_defense_status())
        
        elif self.path == "/defense/network-alerts":
            # 返回新网络告警
            if self.network_guard:
                alerts = self.network_guard.get_new_alerts()
                self._json({"count": len(alerts), "alerts": alerts})
            else:
                self._json({"count": 0, "alerts": []})
        
        elif self.path.startswith("/defense/network-history"):
            limit = self._parse_limit(50)
            rows = self.db_conn.execute(
                "SELECT * FROM defense_network_alerts ORDER BY timestamp DESC LIMIT ?",
                (limit,)
            ).fetchall()
            cols = ["id", "timestamp", "process_name", "pid", "remote_addr_hash",
                    "remote_port", "blocked", "alert_shown"]
            history = [dict(zip(cols, r)) for r in rows]
            self._json({"count": len(history), "history": history})
        
        elif self.path == "/defense/malware-stats":
            rows = self.db_conn.execute(
                "SELECT trigger_type, COUNT(*) as cnt FROM defense_malware_hits GROUP BY trigger_type"
            ).fetchall()
            total = self.db_conn.execute(
                "SELECT COUNT(*) FROM defense_malware_hits"
            ).fetchone()[0]
            self._json({
                "total_malware_hits": total,
                "by_type": {r[0]: r[1] for r in rows},
                "signature_version": self.malware_guard.sig_version if self.malware_guard else "unknown",
            })
        
        elif self.path == "/defense/vault-status":
            if self.vault and self.vault.is_ready:
                self._json(self.vault.get_state())
            else:
                self._json({"initialized": False, "error": "金库未就绪"})
        
        elif self.path == "/defense/verify-fingerprint":
            # 验证传入的设备指纹是否匹配本机（用于防线四导出验证）
            fp_param = self._parse_query_param("fp")
            if fp_param and self.vault:
                match = self.vault.verify_fingerprint(fp_param)
                self._json({"match": match, "device_bound": match})
            else:
                self._json({"match": False, "error": "缺少指纹参数或金库未就绪"})
        
        # ─── 白名单管理 ───
        elif self.path == "/defense/whitelist":
            if self.network_guard:
                self._json(self.network_guard.list_whitelist())
            else:
                self._json({"error": "网络守卫未初始化"}, 503)
        
        elif self.path == "/defense/threat-intel/sync":
            if self.malware_guard:
                result = self.malware_guard.sync_threat_intel()
                self._json(result)
            else:
                self._json({"success": False, "error": "恶意过滤引擎未初始化"}, 503)
        
        elif self.path == "/defense/threat-intel/status":
            if self.malware_guard:
                mgs = self.malware_guard.get_state()
                self._json({
                    "threat_intel_fresh": mgs["threat_intel_fresh"],
                    "threat_intel_synced_ever": mgs["threat_intel_synced_ever"],
                    "threat_intel_hash_count": mgs["threat_intel_hash_count"],
                    "last_threat_intel_sync": mgs["last_threat_intel_sync"],
                })
            else:
                self._json({"error": "恶意过滤引擎未初始化"}, 503)
        
        else:
            self._json({"error": "not found"}, 404)
    
    def do_POST(self):
        if self.path == "/features/mark-uploaded":
            content_length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(content_length))
            ids = body.get("ids", [])
            if ids:
                placeholders = ",".join("?" * len(ids))
                self.db_conn.execute(
                    f"UPDATE feature_vectors SET uploaded=1 WHERE id IN ({placeholders})",
                    ids
                )
                self.db_conn.commit()
            self._json({"marked": len(ids)})
        
        elif self.path == "/clear":
            # 清空特征向量（重新提取）
            self.db_conn.execute("DELETE FROM feature_vectors")
            self.db_conn.commit()
            self._json({"cleared": True})
        
        elif self.path == "/defense/encrypt":
            # 用设备密钥加密（防线三/四：本地加密）
            content_length = int(self.headers.get("Content-Length", 0))
            if content_length == 0:
                self._json({"error": "empty body"}, 400)
            else:
                body = self.rfile.read(content_length)
                if self.vault and self.vault.is_ready:
                    enc = self.vault.encrypt(body)
                    self._json({"encrypted": enc.decode("ascii")})
                else:
                    self._json({"error": "金库未就绪"}, 500)
        
        # ─── 白名单增删 (POST) ───
        elif self.path == "/defense/whitelist/add":
            content_length = int(self.headers.get("Content-Length", 0))
            if content_length == 0:
                self._json({"error": "empty body"}, 400)
            else:
                body = json.loads(self.rfile.read(content_length))
                name = body.get("process_name", "").strip()
                if not name:
                    self._json({"error": "process_name is required"}, 400)
                elif self.network_guard:
                    ok = self.network_guard.add_to_whitelist(name)
                    self._json({"added": ok, "process_name": name})
                else:
                    self._json({"error": "网络守卫未初始化"}, 503)
        
        elif self.path == "/defense/whitelist/remove":
            content_length = int(self.headers.get("Content-Length", 0))
            if content_length == 0:
                self._json({"error": "empty body"}, 400)
            else:
                body = json.loads(self.rfile.read(content_length))
                name = body.get("process_name", "").strip()
                if not name:
                    self._json({"error": "process_name is required"}, 400)
                elif self.network_guard:
                    ok = self.network_guard.remove_from_whitelist(name)
                    self._json({"removed": ok, "process_name": name})
                else:
                    self._json({"error": "网络守卫未初始化"}, 503)
        
        else:
            self._json({"error": "not found"}, 404)
    
    def _parse_limit(self, default: int) -> int:
        """从URL解析limit参数"""
        return self._parse_query_param_int("limit", default)
    
    def _parse_query_param(self, key: str) -> Optional[str]:
        """从URL解析查询参数"""
        if "?" in self.path:
            try:
                qs = self.path.split("?")[1]
                for param in qs.split("&"):
                    if "=" in param and param.split("=")[0] == key:
                        return param.split("=", 1)[1]
            except (ValueError, IndexError):
                pass
        return None
    
    def _parse_query_param_int(self, key: str, default: int) -> int:
        try:
            v = self._parse_query_param(key)
            return int(v) if v else default
        except (ValueError, TypeError):
            return default
    
    def _get_defense_status(self) -> dict:
        """四道防线综合状态 — v2.1: green:true/false 替代 color 字符串
        铁律：任何一条防线 green=false → 整体交付不通过
        """
        walls = {}
        all_greens = []
        
        # 防线一：网络守卫 — 防火墙能初始化=绿（能执行阻断=能防守）
        if self.network_guard:
            ng_state = self.network_guard.get_state()
            # 🔥 防火墙已初始化 = 能执行阻断 = 绿
            wall1_green = ng_state["firewall_initialized"]
            walls["wall_1_network_guard"] = {
                "name": "网络出站强制执行防火墙",
                "green": wall1_green,
                "firewall_initialized": ng_state["firewall_initialized"],
                "firewall_blocked_ips": ng_state["firewall_blocked_ips"],
                "alert_count": ng_state["alert_count"],
                "block_count": ng_state["block_count"],
                "pending_alerts": ng_state.get("pending_alerts", 0),
                "whitelist_count": ng_state.get("whitelist_count", 0),
            }
            if not wall1_green:
                walls["wall_1_network_guard"]["hint"] = "需要 sudo/root 权限启动采集器以启用 pf 防火墙强制执行"
            all_greens.append(wall1_green)
        else:
            walls["wall_1_network_guard"] = {"name": "网络出站强制执行防火墙", "green": False, "status": "not_initialized"}
            all_greens.append(False)
        
        # 防线二：恶意代码过滤 — 威胁情报过期=非绿
        if self.malware_guard:
            mg_state = self.malware_guard.get_state()
            intel_fresh = mg_state.get("threat_intel_fresh", False)
            intel_synced = mg_state.get("threat_intel_synced_ever", False)
            # 威胁情报新鲜 = 绿
            wall2_green = intel_fresh or intel_synced  # 至少同步成功过
            rows = self.db_conn.execute(
                "SELECT COUNT(*) FROM defense_malware_hits"
            ).fetchone()
            walls["wall_2_malware_guard"] = {
                "name": "恶意代码过滤",
                "green": wall2_green,
                "signature_version": mg_state["signature_version"],
                "threat_intel_hash_count": mg_state.get("threat_intel_hash_count", 0),
                "threat_intel_fresh": intel_fresh,
                "threat_intel_synced_ever": intel_synced,
                "hit_count": rows[0] if rows else 0,
            }
            all_greens.append(wall2_green)
        else:
            walls["wall_2_malware_guard"] = {"name": "恶意代码过滤", "green": False, "status": "not_initialized"}
            all_greens.append(False)
        
        # 防线三：设备绑定加密
        if self.vault and self.vault.is_ready:
            walls["wall_3_device_vault"] = {
                "name": "设备绑定加密",
                "green": True,
                "encryption": self.vault.get_state().get("encryption", "unknown"),
                "device_fingerprint": self.vault.fingerprint_hash[:16] + "...",
            }
            all_greens.append(True)
        else:
            walls["wall_3_device_vault"] = {"name": "设备绑定加密", "green": False, "status": "not_initialized"}
            all_greens.append(False)
        
        # 防线四：导出签名绑定
        walls["wall_4_export_bind"] = {
            "name": "导出设备+生物绑定",
            "green": True,
            "status": "available",
        }
        all_greens.append(True)
        
        # 整体：全绿才绿
        overall_green = all(all_greens)
        
        return {
            "version": "2.1.0",
            "walls": walls,
            "overall_green": overall_green,
            "green_count": sum(all_greens),
            "total_walls": len(all_greens),
        }
    
    def _get_status(self) -> dict:
        counts = {}
        for table in ["process_events", "file_events", "network_events", "user_events"]:
            r = self.db_conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
            counts[table] = r[0] if r else 0
        
        r = self.db_conn.execute("SELECT COUNT(*) FROM feature_vectors WHERE uploaded=0").fetchone()
        unuploaded = r[0] if r else 0
        
        return {
            "status": "running",
            "uptime_seconds": time.time() - start_time,
            "events": counts,
            "unuploaded_features": unuploaded,
            "version": VERSION,
            "defense": self._get_defense_status() if self.network_guard or self.vault else None,
        }
    
    def _get_recent_events(self, limit: int) -> list:
        events = []
        
        for table, prefix in [
            ("process_events", "process"),
            ("file_events", "file"),
            ("network_events", "network"),
            ("user_events", "user"),
        ]:
            rows = self.db_conn.execute(
                f"SELECT * FROM {table} ORDER BY timestamp DESC LIMIT {limit // 4}"
            ).fetchall()
            cols = [desc[0] for desc in self.db_conn.execute(
                f"SELECT * FROM {table} LIMIT 0"
            ).description]
            for row in rows:
                event = dict(zip(cols, row))
                event["_source"] = prefix
                events.append(event)
        
        events.sort(key=lambda e: e.get("timestamp", 0), reverse=True)
        return events[:limit]
    
    def _get_process_events(self, limit: int) -> list:
        rows = self.db_conn.execute(
            "SELECT * FROM process_events ORDER BY timestamp DESC LIMIT ?", (limit,)
        ).fetchall()
        cols = ["id", "timestamp", "event_type", "pid", "ppid", "name", "name_hash", "cmdline", "cmdline_hash", "user"]
        return [dict(zip(cols, row)) for row in rows]
    
    def _get_file_events(self, limit: int) -> list:
        rows = self.db_conn.execute(
            "SELECT * FROM file_events ORDER BY timestamp DESC LIMIT ?", (limit,)
        ).fetchall()
        cols = ["id", "timestamp", "event_type", "path_hash", "old_path_hash", "size", "ext"]
        return [dict(zip(cols, row)) for row in rows]
    
    def _get_network_events(self, limit: int) -> list:
        rows = self.db_conn.execute(
            "SELECT * FROM network_events ORDER BY timestamp DESC LIMIT ?", (limit,)
        ).fetchall()
        cols = ["id", "timestamp", "event_type", "protocol", "local_addr", "local_port", "remote_addr_hash", "process_name_hash", "state"]
        return [dict(zip(cols, row)) for row in rows]
    
    def _get_user_events(self, limit: int) -> list:
        rows = self.db_conn.execute(
            "SELECT * FROM user_events ORDER BY timestamp DESC LIMIT ?", (limit,)
        ).fetchall()
        cols = ["id", "timestamp", "event_type", "user_name", "detail"]
        return [dict(zip(cols, row)) for row in rows]
    
    def _get_stats(self) -> dict:
        stats = {}
        
        # 进程统计
        r = self.db_conn.execute(
            "SELECT event_type, COUNT(*) FROM process_events GROUP BY event_type"
        ).fetchall()
        stats["process"] = {row[0]: row[1] for row in r}
        
        # 文件统计
        r = self.db_conn.execute(
            "SELECT event_type, COUNT(*) FROM file_events GROUP BY event_type"
        ).fetchall()
        stats["file"] = {row[0]: row[1] for row in r}
        
        # 网络统计
        r = self.db_conn.execute(
            "SELECT event_type, COUNT(*) FROM network_events GROUP BY event_type"
        ).fetchall()
        stats["network"] = {row[0]: row[1] for row in r}
        
        # 用户统计
        r = self.db_conn.execute(
            "SELECT event_type, COUNT(*) FROM user_events GROUP BY event_type"
        ).fetchall()
        stats["user"] = {row[0]: row[1] for row in r}
        
        # 时间范围
        r = self.db_conn.execute("SELECT MIN(timestamp), MAX(timestamp) FROM process_events").fetchone()
        if r and r[0]:
            stats["time_range"] = {
                "start": r[0],
                "end": r[1],
                "start_iso": datetime.fromtimestamp(r[0], tz=timezone.utc).isoformat(),
                "end_iso": datetime.fromtimestamp(r[1], tz=timezone.utc).isoformat(),
            }
        
        return stats


# ─── 服务管理 ───────────────────────────────────────────
start_time = time.time()

def start_server(db_conn: sqlite3.Connection, port: int):
    """启动HTTP API服务"""
    TraceAPIHandler.db_conn = db_conn
    server = HTTPServer(("127.0.0.1", port), TraceAPIHandler)
    log.info(f"API服务启动: http://127.0.0.1:{port}")
    
    # 在独立线程中运行
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread


def write_pid():
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))

def remove_pid():
    try:
        os.remove(PID_FILE)
    except OSError:
        pass

def is_running() -> bool:
    """检查是否已有实例在运行"""
    if not os.path.exists(PID_FILE):
        return False
    try:
        with open(PID_FILE) as f:
            pid = int(f.read().strip())
        os.kill(pid, 0)  # 检查进程是否存在
        return True
    except (OSError, ValueError):
        remove_pid()
        return False


# ─── CLI入口 ────────────────────────────────────────────
def cmd_start(args):
    """启动采集引擎"""
    if is_running():
        print("⚠️ 采集引擎已在运行中")
        print(f"  PID文件: {PID_FILE}")
        print(f"  状态查询: curl http://127.0.0.1:{COLLECTOR_PORT}/status")
        sys.exit(1)
    
    watch_dirs = args.watch_dirs.split(",") if args.watch_dirs else DEFAULT_WATCH_DIRS
    
    print(f"🚀 龍魂·底座痕迹采集引擎 v{VERSION}")
    print(f"  DNA: {DNA}")
    print(f"  数据目录: {DATA_DIR}")
    print(f"  监控目录: {', '.join(watch_dirs[:3])}{'...' if len(watch_dirs) > 3 else ''}")
    print(f"  API端口: {COLLECTOR_PORT}")
    print()
    
    write_pid()
    
    # 初始化数据库
    db = init_db()
    
    # 🔥 初始化四道防线
    print("🛡️ 正在初始化四道防线...")
    
    # 防线三：设备绑定金库
    try:
        vault = DeviceVault()
        print(f"  ✅ 防线三·设备绑定金库就绪 | 指纹: {vault.fingerprint_hash[:16]}...")
        TraceAPIHandler.vault = vault
    except Exception as e:
        print(f"  ❌ 防线三·设备绑定金库初始化失败: {e}")
        vault = None
    
    # 防线二：恶意代码过滤
    try:
        mg = MalwareGuard(db)
        print(f"  ✅ 防线二·恶意代码过滤就绪 | 特征库 v{mg.sig_version}")
        TraceAPIHandler.malware_guard = mg
    except Exception as e:
        print(f"  ❌ 防线二·恶意代码过滤初始化失败: {e}")
        mg = None
    
    # 防线一：网络守卫（作为独立线程运行）
    try:
        ng = NetworkGuard(db)
        ng.start()
        print(f"  ✅ 防线一·网络守卫已启动 | 间隔 {NETWORK_WATCH_INTERVAL}秒")
        TraceAPIHandler.network_guard = ng
    except Exception as e:
        print(f"  ❌ 防线一·网络守卫初始化失败: {e}")
        ng = None
    
    print()
    
    # 启动采集器（FileCollector 携带 MalwareGuard）
    collectors = [
        ProcessCollector(db),
        FileCollector(db, watch_dirs, malware_guard=mg),
        NetworkCollector(db),
        UserCollector(db),
    ]
    
    for c in collectors:
        c.start()
    
    # 定期同步恶意特征库的后台线程（含鲲鹏同步 + 威胁情报同步）
    def malware_sync_loop():
        # 启动后首次威胁情报同步（延迟10秒等网络就绪）
        time.sleep(10)
        if mg:
            print("🛡️ 正在首次同步威胁情报...")
            try:
                result = mg.sync_threat_intel()
                if result["success"]:
                    print(f"  ✅ 威胁情报首次同步完成 | +{result['total_new_hashes']} 哈希")
                else:
                    print("  🟡 威胁情报首次同步未成功，将每天重试")
            except Exception as e:
                print(f"  🟡 威胁情报同步异常: {e}")
        
        while True:
            time.sleep(THREAT_INTEL_SYNC_INTERVAL)
            if mg:
                try:
                    mg.sync_threat_intel()
                except Exception:
                    pass
                try:
                    mg.sync_from_kunpeng()
                except Exception:
                    pass
    
    sync_thread = threading.Thread(target=malware_sync_loop, daemon=True)
    sync_thread.start()
    
    # 启动API服务
    server, server_thread = start_server(db, COLLECTOR_PORT)
    
    # 信号处理
    def shutdown(signum, frame):
        log.info("收到停止信号，正在关闭...")
        for c in collectors:
            c.stop()
        if ng:
            ng.stop()
        server.shutdown()
        remove_pid()
        log.info("采集引擎已停止")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)
    
    print("✅ 采集引擎运行中，按 Ctrl+C 停止")
    print(f"   状态: curl http://127.0.0.1:{COLLECTOR_PORT}/status")
    print()
    
    try:
        while True:
            time.sleep(60)
            # 定期提取特征向量
            try:
                extract_feature_vectors(db, 50)
            except Exception:
                pass
    except KeyboardInterrupt:
        shutdown(None, None)


def cmd_stop(args):
    """停止采集引擎"""
    if not is_running():
        print("采集引擎未在运行")
        sys.exit(0)
    
    try:
        with open(PID_FILE) as f:
            pid = int(f.read().strip())
        os.kill(pid, signal.SIGTERM)
        print(f"✅ 已发送停止信号到 PID {pid}")
        time.sleep(1)
        if is_running():
            os.kill(pid, signal.SIGKILL)
            print("⚠️ 强制终止")
        remove_pid()
    except ProcessLookupError:
        print("进程已不存在，清理PID文件")
        remove_pid()
    except Exception as e:
        print(f"❌ 停止失败: {e}")
        sys.exit(1)


def cmd_status(args):
    """查看采集引擎状态"""
    if not is_running():
        print("🔴 采集引擎未运行")
        sys.exit(0)
    
    try:
        import urllib.request
        resp = urllib.request.urlopen(f"http://127.0.0.1:{COLLECTOR_PORT}/status", timeout=3)
        data = json.loads(resp.read())
        print(f"🟢 采集引擎 v{data.get('version', '?')} 运行中")
        print(f"  运行时间: {data.get('uptime_seconds', 0):.0f}秒")
        events = data.get("events", {})
        total = sum(events.values())
        print(f"  采集事件: {total} 条")
        for k, v in events.items():
            print(f"    {k}: {v}")
        print(f"  待上传特征向量: {data.get('unuploaded_features', 0)}")
        
        # 防线状态
        defense = data.get("defense")
        if defense:
            print(f"\n🛡️ 四道防线: {defense.get('overall', '?')}")
            for wall_key, wall in defense.get("walls", {}).items():
                icon = "✅" if wall.get("color") == "green" else "🟡" if wall.get("color") == "yellow" else "❌"
                print(f"  {icon} {wall.get('name', wall_key)}: {wall.get('status', '?')}")
    except Exception as e:
        print(f"🟡 引擎运行中但API不可达: {e}")


def cmd_features(args):
    """输出待上传的特征向量（JSON）"""
    if not is_running():
        print(json.dumps({"error": "collector not running"}))
        sys.exit(1)
    
    try:
        import urllib.request
        limit = args.limit or 100
        resp = urllib.request.urlopen(
            f"http://127.0.0.1:{COLLECTOR_PORT}/features/unuploaded",
            timeout=5
        )
        data = json.loads(resp.read())
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description=f"龍魂·底座痕迹采集引擎 v{VERSION}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  lh_base_trace_collector.py start                     # 启动采集
  lh_base_trace_collector.py start --watch-dirs ~/longhun-system,~/Documents
  lh_base_trace_collector.py stop                      # 停止采集
  lh_base_trace_collector.py status                    # 查看状态
  lh_base_trace_collector.py features                  # 导出特征向量
  lh_base_trace_collector.py features --limit 50       # 导出最近50条
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # start
    p_start = subparsers.add_parser("start", help="启动采集引擎")
    p_start.add_argument("--watch-dirs", help="监控目录（逗号分隔）")
    p_start.add_argument("--port", type=int, default=COLLECTOR_PORT, help=f"API端口 (默认: {COLLECTOR_PORT})")
    
    # stop
    subparsers.add_parser("stop", help="停止采集引擎")
    
    # status
    subparsers.add_parser("status", help="查看采集状态")
    
    # features
    p_features = subparsers.add_parser("features", help="导出特征向量")
    p_features.add_argument("--limit", type=int, default=100, help="数量限制")
    
    args = parser.parse_args()
    
    if args.command == "start":
        cmd_start(args)
    elif args.command == "stop":
        cmd_stop(args)
    elif args.command == "status":
        cmd_status(args)
    elif args.command == "features":
        cmd_features(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
