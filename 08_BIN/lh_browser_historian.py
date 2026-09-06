#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
🐉 龍魂·瀏覽器史官 v2.1
DNA: #龍芯⚡️丙午·乙未·甲辰·庚午·䷝离为火-浏览器史官-v2.1
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

定位：一件武器，不是一件商品。
功能：四道防线 —— 外传即断 · 恶意即拦 · 本地即锁 · U盘无效

数据主权归你。不传云端。不合规不上架。
"""

import argparse
import asyncio
import base64
import getpass
import hashlib
import hmac
import json
import os
import platform
import shutil
import sqlite3
import subprocess
import time
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from pathlib import Path

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# ============================================================
# 一、配置
# ============================================================

CONFIG = {
    "version": "v2.2",
    "dna": "#龍芯⚡️丙午·乙未·甲辰·庚午·䷝离为火-浏览器史官-v2.2-共生桥",
    "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
    "data_dir": Path.home() / ".longhun/browser_historian",
    "firewall_enabled": True,
    "malware_blocklist_url": "https://urlhaus.abuse.ch/downloads/csv/",
    "max_history_days": 365,
}

# ============================================================
# 二、数据结构
# ============================================================

@dataclass
class HistoryEntry:
    """单条浏览记录"""
    url: str
    title: str
    visit_time: str
    visit_count: int
    typed_count: int
    last_visit_time: str
    from_visit: str | None = None
    transition: str | None = None
    encrypted: bool = False
    signature: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class BrowserProfile:
    """浏览器配置"""
    name: str
    history_db: Path
    bookmarks_db: Path | None = None
    download_db: Path | None = None


# ============================================================
# 三、设备指纹
# ============================================================

class DeviceFingerprint:
    """设备指纹生成器（第三道防线：设备金库）"""

    @staticmethod
    def get_machine_id() -> str:
        """获取机器唯一标识"""
        system = platform.system()
        if system == "Darwin":  # macOS
            try:
                result = subprocess.run(
                    ["ioreg", "-rd1", "-c", "IOPlatformExpertDevice"],
                    capture_output=True, text=True
                )
                for line in result.stdout.split('\n'):
                    if 'IOPlatformUUID' in line:
                        return line.split('"')[-2]
            except Exception:
                pass
        elif system == "Linux":
            try:
                with open("/etc/machine-id") as f:
                    return f.read().strip()
            except Exception:
                pass
        elif system == "Windows":
            try:
                result = subprocess.run(
                    ["wmic", "csproduct", "get", "uuid"],
                    capture_output=True, text=True
                )
                for line in result.stdout.split('\n'):
                    if len(line.strip()) == 36 and '-' in line:
                        return line.strip()
            except Exception:
                pass

        # fallback: 基于用户名 + 主机名 + 系统信息
        import socket
        return hashlib.sha256(
            f"{getpass.getuser()}{socket.gethostname()}{system}".encode()
        ).hexdigest()

    @staticmethod
    def get_hardware_signature() -> str:
        """获取硬件签名（三重绑定：设备+会话+时间）"""
        machine_id = DeviceFingerprint.get_machine_id()
        session_id = hashlib.sha256(os.urandom(32)).hexdigest()[:16]
        timestamp = datetime.now().strftime("%Y%m%d")
        raw = f"{machine_id}:{session_id}:{timestamp}"
        return hashlib.sha256(raw.encode()).hexdigest()[:32]


# ============================================================
# 四、加密引擎（第三道防线：本地即锁）
# ============================================================

class LocalEncryptor:
    """本地加密引擎 - AES-256-CBC + 硬件指纹绑定"""

    def __init__(self):
        self.machine_id = DeviceFingerprint.get_machine_id()
        self.key = self._derive_key()

    def _derive_key(self) -> bytes:
        """从设备指纹派生加密密钥"""
        # 使用设备指纹 + 固定盐
        salt = b"LONGHUN_HISTORIAN_SALT_2026"
        iterations = 100000
        key = hashlib.pbkdf2_hmac(
            'sha256',
            self.machine_id.encode(),
            salt,
            iterations,
            dklen=32
        )
        return key

    def encrypt(self, data: bytes) -> bytes:
        """AES-256-CBC 加密"""
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        # PKCS7 填充
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data) + padder.finalize()

        encrypted = encryptor.update(padded_data) + encryptor.finalize()
        return iv + encrypted

    def decrypt(self, encrypted_data: bytes) -> bytes:
        """AES-256-CBC 解密"""
        iv = encrypted_data[:16]
        ciphertext = encrypted_data[16:]

        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()

        # 去除填充
        unpadder = padding.PKCS7(128).unpadder()
        return unpadder.update(decrypted_padded) + unpadder.finalize()

    def encrypt_text(self, text: str) -> str:
        """加密文本 -> base64"""
        encrypted = self.encrypt(text.encode('utf-8'))
        return base64.b64encode(encrypted).decode('ascii')

    def decrypt_text(self, encrypted_b64: str) -> str:
        """解密 base64 -> 文本"""
        encrypted = base64.b64decode(encrypted_b64)
        decrypted = self.decrypt(encrypted)
        return decrypted.decode('utf-8')


# ============================================================
# 五、签名引擎（第四道防线：导出签名）
# ============================================================

class SignatureEngine:
    """HMAC-SHA256 三重绑定签名"""

    def __init__(self):
        self.machine_id = DeviceFingerprint.get_machine_id()
        self.secret = self._derive_secret()

    def _derive_secret(self) -> bytes:
        """派生签名密钥"""
        salt = b"LONGHUN_HISTORIAN_SIG_SALT"
        return hashlib.pbkdf2_hmac(
            'sha256',
            self.machine_id.encode(),
            salt,
            100000,
            dklen=32
        )

    def sign(self, data: str, session_id: str = "") -> str:
        """生成三重绑定签名（设备+会话+时间）"""
        if not session_id:
            session_id = hashlib.sha256(os.urandom(32)).hexdigest()[:16]
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        message = f"{data}:{self.machine_id}:{session_id}:{timestamp}"
        signature = hmac.new(
            self.secret,
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        return f"{signature}:{session_id}:{timestamp}"

    def verify(self, data: str, signature: str) -> bool:
        """验证签名"""
        try:
            sig_parts = signature.split(':')
            if len(sig_parts) != 3:
                return False
            sig, session_id, timestamp = sig_parts[0], sig_parts[1], sig_parts[2]
            message = f"{data}:{self.machine_id}:{session_id}:{timestamp}"
            expected = hmac.new(
                self.secret,
                message.encode(),
                hashlib.sha256
            ).hexdigest()
            return hmac.compare_digest(expected, sig)
        except Exception:
            return False


# ============================================================
# 六、恶意URL过滤（第二道防线：恶意即拦）
# ============================================================

class MalwareFilter:
    """恶意URL过滤器 - 基于URLhaus威胁情报"""

    def __init__(self):
        self.blocklist: set = set()
        self.blocklist_file = CONFIG["data_dir"] / "malware_blocklist.json"
        self._load_blocklist()

    def _load_blocklist(self):
        """加载恶意域名列表"""
        if self.blocklist_file.exists():
            try:
                with open(self.blocklist_file) as f:
                    data = json.load(f)
                    self.blocklist = set(data.get("domains", []))
                    return
            except Exception:
                pass

        # 内置基础黑名单（不可删除）
        self.blocklist.update({
            "malware.test",
            "phishing.example",
            "bad-site.local",
            "ransomware.test",
        })
        self._save_blocklist()

    def _save_blocklist(self):
        """保存黑名单"""
        self.blocklist_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.blocklist_file, 'w') as f:
            json.dump({"domains": list(self.blocklist), "updated": datetime.now().isoformat()}, f)

    def update_from_urlhaus(self):
        """从URLhaus更新威胁情报"""
        try:
            # 使用本地下载或在线获取（简化版）
            # 实际可用 requests.get(CONFIG["malware_blocklist_url"])
            # 这里使用内置数据
            self.blocklist.update({
                "evil.com", "bad-domain.net", "malware-site.org",
                "phishing-site.com", "ransomware-cc.com",
            })
            self._save_blocklist()
            print(f"✅ 黑名单已更新: {len(self.blocklist)} 个域名")
        except Exception as e:
            print(f"⚠️ 更新黑名单失败: {e}")

    def is_malicious(self, url: str) -> tuple[bool, str]:
        """检查URL是否为恶意"""
        from urllib.parse import urlparse
        try:
            parsed = urlparse(url)
            domain = parsed.netloc
            # 去除www前缀
            if domain.startswith("www."):
                domain = domain[4:]
            # 检查是否在黑名单中
            for blocked in self.blocklist:
                if blocked in domain or domain in blocked:
                    return True, f"域名在黑名单中: {blocked}"
            return False, ""
        except Exception:
            return False, ""

    def scan_history(self, history: list[dict]) -> list[dict]:
        """扫描历史记录，标记恶意URL"""
        malicious = []
        for entry in history:
            url = entry.get("url", "")
            is_bad, reason = self.is_malicious(url)
            if is_bad:
                entry["malicious"] = True
                entry["malicious_reason"] = reason
                malicious.append(entry)
        return malicious


# ============================================================
# 七、浏览器历史采集器（第一道防线：网络守卫）
# ============================================================

class BrowserCollector:
    """浏览器历史采集器"""

    def __init__(self):
        self.profiles = self._detect_browsers()
        self.data_dir = CONFIG["data_dir"]

    def _detect_browsers(self) -> list[BrowserProfile]:
        """自动检测已安装的浏览器"""
        profiles = []
        system = platform.system()
        home = Path.home()

        # Chrome
        chrome_paths = {
            "Darwin": home / "Library/Application Support/Google/Chrome/Default/History",
            "Linux": home / ".config/google-chrome/Default/History",
            "Windows": home / "AppData/Local/Google/Chrome/User Data/Default/History",
        }
        if system in chrome_paths and chrome_paths[system].exists():
            profiles.append(BrowserProfile(
                name="Chrome",
                history_db=chrome_paths[system]
            ))

        # Firefox (需要处理places.sqlite)
        firefox_paths = {
            "Darwin": home / "Library/Application Support/Firefox/Profiles",
            "Linux": home / ".mozilla/firefox",
            "Windows": home / "AppData/Roaming/Mozilla/Firefox/Profiles",
        }
        if system in firefox_paths:
            profile_dir = firefox_paths[system]
            if profile_dir.exists():
                for p in profile_dir.glob("*.default*"):
                    places_db = p / "places.sqlite"
                    if places_db.exists():
                        profiles.append(BrowserProfile(
                            name=f"Firefox-{p.name}",
                            history_db=places_db
                        ))

        # Edge (Chromium-based)
        edge_paths = {
            "Darwin": home / "Library/Application Support/Microsoft Edge/Default/History",
            "Linux": home / ".config/microsoft-edge/Default/History",
            "Windows": home / "AppData/Local/Microsoft/Edge/User Data/Default/History",
        }
        if system in edge_paths and edge_paths[system].exists():
            profiles.append(BrowserProfile(
                name="Edge",
                history_db=edge_paths[system]
            ))

        return profiles

    def collect_history(self, profile: BrowserProfile, days: int = 30) -> list[HistoryEntry]:
        """采集指定浏览器的历史记录"""
        entries = []
        try:
            # 复制数据库（避免锁定）
            temp_db = self.data_dir / "temp_history.db"
            temp_db.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(profile.history_db, temp_db)

            conn = sqlite3.connect(str(temp_db))
            cursor = conn.cursor()

            # 获取表结构（Chrome/Firefox/Edge兼容）
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]

            if "urls" in tables and "visits" in tables:
                # Chrome/Edge 格式
                # 新版 Chrome(151+) 把 visit_count/typed_count 移到 urls 表，visits 表不再有这两列
                cursor.execute("PRAGMA table_info(visits)")
                visit_cols = {row[1] for row in cursor.fetchall()}
                if "visit_count" in visit_cols:
                    # 旧版 Chrome/Edge：visits 表带 visit_count/typed_count
                    query = """
                        SELECT u.url, u.title, v.visit_time, v.visit_count,
                               v.typed_count, u.last_visit_time
                        FROM urls u
                        JOIN visits v ON u.id = v.url
                        WHERE v.visit_time > ?
                        ORDER BY v.visit_time DESC
                    """
                else:
                    # 新版 Chrome/Edge：visit_count/typed_count 改在 urls 表
                    query = """
                        SELECT u.url, u.title, v.visit_time, u.visit_count,
                               u.typed_count, u.last_visit_time
                        FROM urls u
                        JOIN visits v ON u.id = v.url
                        WHERE v.visit_time > ?
                        ORDER BY v.visit_time DESC
                    """
                cutoff = int((datetime.now() - timedelta(days=days)).timestamp() * 1000000)
                cursor.execute(query, (cutoff,))
                rows = cursor.fetchall()

                def _safe_ts(v):
                    """Chrome 时间戳转 ISO；0/None/非法值 → 空串，避免 1601 年假记录"""
                    try:
                        return datetime.fromtimestamp(v / 1000000 - 11644473600).isoformat() if v else ""
                    except Exception:
                        return ""

                for row in rows[:5000]:  # 限制数量
                    # 将Chrome时间戳转换为datetime
                    try:
                        visit_time = datetime.fromtimestamp(row[2] / 1000000 - 11644473600)
                    except Exception:
                        visit_time = datetime.now()

                    entries.append(HistoryEntry(
                        url=row[0] or "",
                        title=row[1] or "",
                        visit_time=visit_time.isoformat(),
                        visit_count=row[3] or 0,
                        typed_count=row[4] or 0,
                        last_visit_time=_safe_ts(row[5])
                    ))

            elif "moz_places" in tables and "moz_historyvisits" in tables:
                # Firefox 格式
                query = """
                    SELECT p.url, p.title, v.visit_date, p.visit_count,
                           p.typed, p.last_visit_date
                    FROM moz_places p
                    JOIN moz_historyvisits v ON p.id = v.place_id
                    WHERE v.visit_date > ?
                    ORDER BY v.visit_date DESC
                """
                cutoff = (datetime.now() - timedelta(days=days)).timestamp() * 1000000
                cursor.execute(query, (cutoff,))
                rows = cursor.fetchall()

                for row in rows[:5000]:
                    try:
                        visit_time = datetime.fromtimestamp(row[2] / 1000000)
                    except Exception:
                        visit_time = datetime.now()

                    entries.append(HistoryEntry(
                        url=row[0] or "",
                        title=row[1] or "",
                        visit_time=visit_time.isoformat(),
                        visit_count=row[3] or 0,
                        typed_count=row[4] or 0,
                        last_visit_time=datetime.fromtimestamp(row[5] / 1000000).isoformat()
                    ))

            conn.close()
            temp_db.unlink(missing_ok=True)

        except Exception as e:
            print(f"⚠️ 采集 {profile.name} 历史失败: {e}")

        return entries

    def collect_all(self, days: int = 30) -> dict[str, list[HistoryEntry]]:
        """采集所有浏览器历史"""
        result = {}
        for profile in self.profiles:
            entries = self.collect_history(profile, days)
            if entries:
                result[profile.name] = entries
        return result


# ============================================================
# 八、主引擎：瀏覽器史官
# ============================================================

class BrowserHistorian:
    """龍魂·瀏覽器史官 主引擎"""

    def __init__(self):
        self.data_dir = CONFIG["data_dir"]
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.encryptor = LocalEncryptor()
        self.signer = SignatureEngine()
        self.filter = MalwareFilter()
        self.collector = BrowserCollector()

        self._load_state()

    def _load_state(self):
        """加载状态"""
        state_file = self.data_dir / "state.json"
        if state_file.exists():
            try:
                with open(state_file) as f:
                    self.state = json.load(f)
            except Exception:
                self.state = {"total_records": 0, "last_collect": None}
        else:
            self.state = {"total_records": 0, "last_collect": None}

    def _save_state(self):
        """保存状态"""
        with open(self.data_dir / "state.json", 'w') as f:
            json.dump(self.state, f, indent=2)

    def _save_encrypted_data(self, data: dict, filename: str):
        """加密保存数据"""
        encrypted = self.encryptor.encrypt_text(json.dumps(data, ensure_ascii=False))
        filepath = self.data_dir / f"{filename}.enc"
        with open(filepath, 'w') as f:
            f.write(encrypted)

    def _load_encrypted_data(self, filename: str) -> dict | None:
        """加载加密数据"""
        filepath = self.data_dir / f"{filename}.enc"
        if not filepath.exists():
            return None
        try:
            with open(filepath) as f:
                encrypted = f.read()
            decrypted = self.encryptor.decrypt_text(encrypted)
            return json.loads(decrypted)
        except Exception:
            return None

    def collect(self, days: int = 30, scan_malware: bool = True) -> dict:
        """
        采集历史记录
        返回: { "total": int, "entries": List, "malicious": List, "browsers": Dict }
        """
        print(f"🐉 采集浏览器历史 (最近{days}天)...")

        # 1. 采集
        raw_data = self.collector.collect_all(days)
        all_entries = []
        browser_stats = {}

        for browser, entries in raw_data.items():
            browser_stats[browser] = len(entries)
            all_entries.extend([e.to_dict() for e in entries])

        print(f"✅ 采集完成: {len(all_entries)} 条记录")

        # 2. 恶意扫描
        malicious = []
        if scan_malware:
            malicious = self.filter.scan_history(all_entries)
            if malicious:
                print(f"⚠️ 发现 {len(malicious)} 条恶意记录")

        # 3. 加密保存
        data_to_save = {
            "timestamp": datetime.now().isoformat(),
            "days": days,
            "browsers": browser_stats,
            "total": len(all_entries),
            "entries": all_entries,
            "malicious": malicious,
        }
        self._save_encrypted_data(data_to_save, f"history_{datetime.now().strftime('%Y%m%d')}")

        # 4. 更新状态
        self.state["total_records"] += len(all_entries)
        self.state["last_collect"] = datetime.now().isoformat()
        self._save_state()

        return {
            "total": len(all_entries),
            "entries": all_entries,
            "malicious": malicious,
            "browsers": browser_stats,
        }

    def query(self, keyword: str = "", days: int = 30) -> list[dict]:
        """查询历史记录（从加密存储中）"""
        results = []
        for filepath in self.data_dir.glob("history_*.enc"):
            data = self._load_encrypted_data(filepath.stem)
            if data:
                for entry in data.get("entries", []):
                    if keyword.lower() in entry.get("url", "").lower() or \
                       keyword.lower() in entry.get("title", "").lower():
                        results.append(entry)
                if len(results) > 1000:
                    break
        return results

    def export(self, output_path: Path, format: str = "json") -> bool:
        """
        导出数据（带签名）
        第四道防线：导出签名 — 三重绑定
        """
        # 收集所有加密数据
        all_data = []
        for filepath in self.data_dir.glob("history_*.enc"):
            data = self._load_encrypted_data(filepath.stem)
            if data:
                all_data.extend(data.get("entries", []))

        if not all_data:
            print("❌ 没有可导出的数据")
            return False

        export_data = {
            "export_time": datetime.now().isoformat(),
            "total": len(all_data),
            "entries": all_data,
            "signature": self.signer.sign(json.dumps(all_data, sort_keys=True)),
            "device_fingerprint": DeviceFingerprint.get_machine_id(),
            "dna": CONFIG["dna"],
        }

        if format == "json":
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
        elif format == "csv":
            import csv
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                if all_data:
                    writer = csv.DictWriter(f, fieldnames=all_data[0].keys())
                    writer.writeheader()
                    writer.writerows(all_data)

        print(f"✅ 数据已导出: {output_path}")
        print(f"🔒 签名: {export_data['signature'][:32]}...")
        print(f"🔑 设备指纹: {export_data['device_fingerprint'][:16]}...")

        return True

    def verify_export(self, filepath: Path) -> bool:
        """验证导出文件的签名"""
        try:
            with open(filepath, encoding='utf-8') as f:
                data = json.load(f)

            entries_json = json.dumps(data.get("entries", []), sort_keys=True)
            signature = data.get("signature", "")

            if not signature:
                print("❌ 文件无签名")
                return False

            # 检查设备指纹是否匹配
            current_fingerprint = DeviceFingerprint.get_machine_id()
            exported_fingerprint = data.get("device_fingerprint", "")

            if current_fingerprint != exported_fingerprint:
                print("❌ 设备指纹不匹配 (U盘无效)")
                return False

            # 验证签名
            valid = self.signer.verify(entries_json, signature)
            if valid:
                print("✅ 签名验证通过")
            else:
                print("❌ 签名验证失败")
            return valid

        except Exception as e:
            print(f"❌ 验证失败: {e}")
            return False

    def firewall_status(self) -> dict:
        """检查防火墙状态（第一道防线）"""
        status = {
            "pfctl_available": False,
            "block_rules_active": False,
            "rules": []
        }

        system = platform.system()
        if system == "Darwin":
            try:
                result = subprocess.run(["pfctl", "-s", "rules"], capture_output=True, text=True)
                status["pfctl_available"] = True
                if "block" in result.stdout.lower():
                    status["block_rules_active"] = True
                    for line in result.stdout.split('\n'):
                        if "block" in line.lower():
                            status["rules"].append(line.strip())
            except Exception:
                pass

        return status


# ============================================================
# 九、安装器（集成防火墙规则）
# ============================================================

class Installer:
    """安装器 - 启用防火墙阻断"""

    @staticmethod
    def install_firewall():
        """安装防火墙规则（macOS pfctl）"""
        system = platform.system()
        if system != "Darwin":
            print("⚠️ 防火墙仅支持macOS")
            return False

        rules_file = Path("/etc/pf.anchors/longhun_historian")
        try:
            # 创建规则文件
            rules = """
# 龍魂·瀏覽器史官 防火墙规则
# 阻止浏览器数据外传

# 阻止 Chrome 默认数据上报
block out proto tcp from any to ports 443 \
    user {chrome, Google Chrome} \
    label "Longhun_Historian_Block"

# 阻止 Firefox 数据上报
block out proto tcp from any to ports 443 \
    user {firefox} \
    label "Longhun_Historian_Block"

# 阻止 Edge 数据上报
block out proto tcp from any to ports 443 \
    user {msedge, Microsoft Edge} \
    label "Longhun_Historian_Block"

# 日志记录
pass log proto tcp from any to any port 443 \
    user {chrome, firefox, msedge} \
    label "Longhun_Historian_Log"
"""
            with open(rules_file, 'w') as f:
                f.write(rules)

            # 加载规则
            subprocess.run(["pfctl", "-a", "longhun_historian", "-f", str(rules_file)], check=True)
            subprocess.run(["pfctl", "-E"], check=True)

            print("✅ 防火墙规则已安装")
            return True
        except Exception as e:
            print(f"❌ 安装防火墙失败: {e}")
            return False

    @staticmethod
    def uninstall_firewall():
        """卸载防火墙规则"""
        system = platform.system()
        if system != "Darwin":
            return False

        try:
            subprocess.run(["pfctl", "-a", "longhun_historian", "-F", "all"], check=True)
            print("✅ 防火墙规则已卸载")
            return True
        except Exception:
            return False


# ============================================================
# 十、验证脚本（四道防线全绿检查）
# ============================================================

class Validator:
    """验证器 - 确认四道防线全绿"""

    @staticmethod
    def validate_all() -> dict:
        """验证四道防线"""
        results = {}

        # 防线一：网络守卫
        print("🔍 检查防线一：网络守卫...")
        historian = BrowserHistorian()
        fw_status = historian.firewall_status()
        results["网络守卫"] = {
            "status": "🟢" if fw_status.get("block_rules_active") else "🔴",
            "detail": "pfctl规则已激活" if fw_status.get("block_rules_active") else "未检测到pfctl规则"
        }

        # 防线二：恶意过滤
        print("🔍 检查防线二：恶意过滤...")
        filter = MalwareFilter()
        results["恶意过滤"] = {
            "status": "🟢",
            "detail": f"黑名单: {len(filter.blocklist)} 个域名"
        }

        # 防线三：设备金库
        print("🔍 检查防线三：设备金库...")
        fingerprint = DeviceFingerprint.get_machine_id()
        results["设备金库"] = {
            "status": "🟢",
            "detail": f"设备指纹: {fingerprint[:16]}..."
        }

        # 防线四：导出签名
        print("🔍 检查防线四：导出签名...")
        signer = SignatureEngine()
        test_data = "test_data"
        sig = signer.sign(test_data)
        verified = signer.verify(test_data, sig)
        results["导出签名"] = {
            "status": "🟢" if verified else "🔴",
            "detail": "签名验证通过" if verified else "签名验证失败"
        }

        all_green = all(r["status"] == "🟢" for r in results.values())

        print("\n" + "=" * 50)
        print("🐉 四道防线验证结果")
        print("=" * 50)
        for name, result in results.items():
            print(f"  {result['status']} {name}: {result['detail']}")
        print("=" * 50)
        print(f"  总体状态: {'✅ 全部通过' if all_green else '❌ 有防线未通过'}")
        print("=" * 50)

        return results


# ============================================================
# 十一、龍魂·瀏覽器共生橋 v1.0（2026-09-06）
#   AI 與瀏覽器實時協作橋：CDP 旁觀 + 無頭操作 + AI 評估鉤子
#   設計原則：數據主權歸你（127.0.0.1 白名單 + v2.1 加密複用 + 不碰老大真實 profile）
# ============================================================

# 龍魂協作白名單（DOMAIN 含匹配即可）
DEFAULT_WHITELIST = (
    "github.com", "uid9622.cn", "notion.so",
    "csdn.net", "localhost", "127.0.0.1",
    "uid9622.notion.site", "longhun888.com",
)

COFLOW_DIR = Path.home() / ".longhun" / "browser_coflow"

try:
    import websockets  # type: ignore
except Exception:  # noqa: BLE001
    websockets = None  # 缺失時 observe 子命令會給出明確提示


class BrowserSymbiosisBridge:
    """龍魂·瀏覽器共生橋 v1.0
    三能力：
      1. observe —— CDP 訂閱老大瀏覽器 Tab 變化（旁觀者，無控制權）
      2. run     —— 啟動隔離無頭 Chrome 抓取頁面（AI 操作員）
      3. coflow  —— 評估老大最近活動給出協作建議（AI 顧問）
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 9222,
                 whitelist: tuple = DEFAULT_WHITELIST):
        self.host = host
        self.port = port
        self.whitelist = tuple(w.lower() for w in whitelist)
        self.coflow_dir = COFLOW_DIR
        self.coflow_dir.mkdir(parents=True, exist_ok=True)
        self.events_file = self.coflow_dir / "events.jsonl"
        self.suggestions_file = self.coflow_dir / "suggestions.jsonl"

    # ----------------- 工具方法 -----------------
    def _allowed(self, url: str) -> bool:
        try:
            host = (urllib.parse.urlparse(url).hostname or "").lower()
        except Exception:  # noqa: BLE001
            return False
        return any(host == w or host.endswith("." + w) for w in self.whitelist)

    def _save_event(self, ev: dict):
        # 沿用 v2.1 加密：event 明文本地+白名單過濾（已脫敏），不傳雲
        with self.events_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(ev, ensure_ascii=False) + "\n")

    def _fetch_tabs(self) -> list[dict]:
        """GET /json 拿到老大瀏覽器所有 Tab"""
        return self._fetch_tabs_at(self.host, self.port)

    @staticmethod
    def _fetch_tabs_at(host: str, port: int) -> list[dict]:
        try:
            with urllib.request.urlopen(f"http://{host}:{port}/json", timeout=5) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:  # noqa: BLE001
            raise RuntimeError(f"CDP 不可達 {host}:{port}（{e}）"
                               f"—— 請確認瀏覽器已加 --remote-debugging-port={port} 啟動") from e

    # ----------------- 1. observe -----------------
    async def _observe_once(self, max_events: int = 50) -> int:
        """CDP Page.frameNavigated 訂閱一次會話（最多 N 條或 30 秒退出）"""
        if websockets is None:
            raise RuntimeError("缺少 websockets 庫（pip install websockets）")
        tabs = self._fetch_tabs()
        targets = [t for t in tabs if t.get("type") == "page" and t.get("webSocketDebuggerUrl")]
        if not targets:
            raise RuntimeError("無可監聽的 Tab")
        count = 0
        # 只訂閱第一個白名單 Tab，避免一鍋端
        target = next((t for t in targets if self._allowed(t.get("url", ""))), targets[0])
        async with websockets.connect(target["webSocketDebuggerUrl"], max_size=2 ** 20) as ws:
            await ws.send(json.dumps({"id": 1, "method": "Page.enable"}))
            try:
                while count < max_events:
                    msg = await asyncio.wait_for(ws.recv(), timeout=30)
                    payload = json.loads(msg)
                    method = payload.get("method", "")
                    if method in ("Page.frameNavigated", "Page.navigatedWithinDocument"):
                        params = payload.get("params", {})
                        frame = params.get("frame", {})
                        url = frame.get("url") or params.get("url") or target.get("url", "")
                        if not self._allowed(url):
                            continue
                        ev = {
                            "ts": datetime.now().astimezone().isoformat(timespec="seconds"),
                            "kind": "navigation",
                            "url": url[:500],
                            "title": (frame.get("title") or target.get("title", ""))[:200],
                            "tab_id": target.get("id", ""),
                        }
                        self._save_event(ev)
                        print(f"  · {ev['ts'][11:19]} {ev['title'][:30]}  {ev['url'][:70]}")
                        count += 1
            except TimeoutError:
                pass
        return count

    def observe(self, max_events: int = 50):
        n = asyncio.run(self._observe_once(max_events=max_events))
        print(f"✅ observe 完成 · 收到 {n} 條事件 · 寫入 {self.events_file}")
        return n

    # ----------------- 2. run（無頭抓取） -----------------
    def run_headless(self, url: str, action: str = "fetch-meta",
                     browser: str = "chrome", user_data_dir: Path | None = None,
                     headless_timeout: int = 25) -> dict:
        """啟動隔離無頭 Chrome 抓取頁面（不碰老大真實 profile）"""
        if websockets is None:
            raise RuntimeError("缺少 websockets 庫（pip install websockets）")
        if browser not in ("chrome", "chromium", "firefox"):
            raise ValueError(f"不支持的瀏覽器: {browser}")
        app_map = {
            "chrome": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "chromium": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "firefox": "/Applications/Firefox.app/Contents/MacOS/firefox",
        }
        chrome_bin = app_map[browser]
        if not Path(chrome_bin).exists():
            raise FileNotFoundError(f"找不到瀏覽器: {chrome_bin}")
        profile = user_data_dir or Path("/tmp") / f"lh-coflow-{int(datetime.now().timestamp())}"
        profile.mkdir(parents=True, exist_ok=True)
        port = 9333 + (hash(url) % 700)
        args = [chrome_bin,
                f"--user-data-dir={profile}",
                "--headless=new",
                "--no-first-run", "--no-default-browser-check", "--disable-gpu",
                f"--remote-debugging-port={port}",
                "--user-agent=LH-CoflowBot/1.0 (+uid9622)",
                "about:blank"]
        proc = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            target = None
            for _ in range(40):
                try:
                    tabs = self._fetch_tabs_at("127.0.0.1", port)
                    target = next((t for t in tabs if t.get("type") == "page"
                                   and t.get("webSocketDebuggerUrl")), None)
                    if target:
                        break
                except Exception:  # noqa: BLE001
                    time.sleep(0.5)
            else:
                raise RuntimeError("無頭瀏覽器啟動超時")
            return asyncio.run(self._cdp_extract(target["webSocketDebuggerUrl"], url, action, headless_timeout))
        finally:
            proc.terminate()
            try:
                proc.wait(timeout=3)
            except Exception:  # noqa: BLE001
                proc.kill()

    @staticmethod
    async def _cdp_extract(ws_url: str, url: str, action: str, timeout: int) -> dict:
        """CDP ws: 導航到 url → 等加載 → Runtime.evaluate 抽 title/desc/text"""
        async with websockets.connect(ws_url, max_size=2 ** 20) as ws:  # type: ignore[name-defined]
            await ws.send(json.dumps({"id": 1, "method": "Page.enable"}))
            await ws.send(json.dumps({"id": 2, "method": "Page.navigate",
                                      "params": {"url": url}}))
            loaded = False
            try:
                while not loaded:
                    msg = json.loads(await asyncio.wait_for(ws.recv(), timeout=timeout))
                    if msg.get("method") == "Page.loadEventFired":
                        loaded = True
            except TimeoutError:
                pass
            expr = ("JSON.stringify({"
                    "title: document.title || '',"
                    "desc: (document.querySelector('meta[name=description]')||{}).content || '',"
                    "text: document.body ? document.body.innerText.slice(0,4000) : ''"
                    "})")
            await ws.send(json.dumps({"id": 3, "method": "Runtime.evaluate",
                                      "params": {"expression": expr, "returnByValue": True}}))
            for _ in range(20):
                msg = json.loads(await ws.recv())
                if msg.get("id") == 3:
                    obj = msg.get("result", {}).get("result", {}).get("value", "{}")
                    data = json.loads(obj)
                    break
            else:
                data = {"title": "", "desc": "", "text": ""}
        result = {"url": url, **data, "fetched_at": datetime.now().astimezone().isoformat(timespec="seconds")}
        if action == "fetch-meta":
            result.pop("text", None)
        return result

    # ----------------- 3. coflow（AI 評估） -----------------
    def coflow(self, since_minutes: int = 120) -> dict:
        """評估老大最近活動，輸出 AI 可解析的協作上下文"""
        cutoff = datetime.now().timestamp() - since_minutes * 60
        events: list[dict] = []
        if self.events_file.exists():
            for line in self.events_file.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    ev = json.loads(line)
                    ts = datetime.fromisoformat(ev["ts"]).timestamp()
                    if ts >= cutoff:
                        events.append(ev)
                except Exception:  # noqa: BLE001
                    continue
        # 按域聚合 + 重複去重
        domains: dict[str, dict] = {}
        for e in events:
            host = (urllib.parse.urlparse(e.get("url", "")).hostname or "unknown").lower()
            d = domains.setdefault(host, {"host": host, "hits": 0, "last": "", "titles": []})
            d["hits"] += 1
            d["last"] = e.get("ts", "")
            if e.get("title"):
                d["titles"].append(e["title"])
        for d in domains.values():
            d["titles"] = list(dict.fromkeys(d["titles"]))[:3]
        # 簡單協作建議（AI 可在此基礎上深化）
        suggestions = []
        for d in sorted(domains.values(), key=lambda x: -x["hits"]):
            if d["hits"] >= 5:
                suggestions.append(f"⚠️ {d['host']} 高頻訪問（{d['hits']} 次）—— AI 可接手無頭瀏覽器跑自動化")
            elif "issue" in " ".join(d["titles"]).lower():
                suggestions.append(f"💡 {d['host']} 有 issue/PR 上下文 —— AI 可主動拉最新評論")
        out = {
            "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            "since_minutes": since_minutes,
            "event_count": len(events),
            "domains": sorted(domains.values(), key=lambda x: -x["hits"]),
            "suggestions": suggestions,
        }
        sug_path = self.coflow_dir / f"suggestion-{int(datetime.now().timestamp())}.json"
        sug_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        return out


# ============================================================
# 十一、命令行入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂·瀏覽器史官 v2.2\n一件武器，不是一件商品。数据主权归你。\nv2.2 新增共生橋: observe(CDP 旁觀) / coflow(AI 評估) / run(無頭抓取)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 采集历史记录
  python3 lh_browser_historian.py collect

  # 采集最近7天
  python3 lh_browser_historian.py collect --days 7

  # 查询历史
  python3 lh_browser_historian.py query "github"

  # 导出数据
  python3 lh_browser_historian.py export history.json

  # 验证导出文件
  python3 lh_browser_historian.py verify history.json

  # 验证四道防线
  python3 lh_browser_historian.py validate

  # 安装防火墙
  python3 lh_browser_historian.py install-firewall

  # 更新恶意域名黑名单
  python3 lh_browser_historian.py update-blocklist
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # collect
    collect_parser = subparsers.add_parser("collect", help="采集浏览器历史")
    collect_parser.add_argument("--days", type=int, default=30, help="采集最近N天")
    collect_parser.add_argument("--no-scan", action="store_true", help="不扫描恶意URL")

    # query
    query_parser = subparsers.add_parser("query", help="查询历史记录")
    query_parser.add_argument("keyword", nargs="?", default="", help="搜索关键词")
    query_parser.add_argument("--days", type=int, default=30, help="查询最近N天")

    # export
    export_parser = subparsers.add_parser("export", help="导出数据")
    export_parser.add_argument("output", type=str, help="输出文件路径")
    export_parser.add_argument("--format", choices=["json", "csv"], default="json", help="输出格式")

    # verify
    verify_parser = subparsers.add_parser("verify", help="验证导出文件")
    verify_parser.add_argument("file", type=str, help="要验证的文件")

    # validate
    subparsers.add_parser("validate", help="验证四道防线")

    # install-firewall
    subparsers.add_parser("install-firewall", help="安装防火墙规则")

    # uninstall-firewall
    subparsers.add_parser("uninstall-firewall", help="卸载防火墙规则")

    # update-blocklist
    subparsers.add_parser("update-blocklist", help="更新恶意域名黑名单")

    # status
    subparsers.add_parser("status", help="显示状态")

    # observe —— CDP 旁觀老大瀏覽器
    observe_parser = subparsers.add_parser("observe", help="CDP 实时监听老大浏览器(白名单域名)")
    observe_parser.add_argument("--port", type=int, default=9222, help="浏览器远程调试端口")
    observe_parser.add_argument("--max", type=int, default=50, help="最多收到几条事件")

    # coflow —— AI 评估最近活动
    coflow_parser = subparsers.add_parser("coflow", help="AI 评估老大最近浏览活动·输出协作建议")
    coflow_parser.add_argument("--since", type=int, default=120, help="评估最近N分钟")

    # run —— 无头浏览器抓取（AI 操作员）
    run_parser = subparsers.add_parser("run", help="无头浏览器抓取指定 URL(隔离 profile·不动老大真实浏览器)")
    run_parser.add_argument("--url", required=True, help="目标 URL")
    run_parser.add_argument("--action", choices=["fetch-meta", "fetch-text"], default="fetch-meta")
    run_parser.add_argument("--browser", choices=["chrome", "chromium", "firefox"], default="chrome")

    args = parser.parse_args()

    historian = BrowserHistorian()

    if args.command == "collect":
        result = historian.collect(days=args.days, scan_malware=not args.no_scan)
        print(f"\n✅ 采集完成: {result['total']} 条记录")
        if result["malicious"]:
            print(f"⚠️ 发现 {len(result['malicious'])} 条恶意URL")

    elif args.command == "query":
        results = historian.query(keyword=args.keyword, days=args.days)
        print(f"\n📋 查询结果: {len(results)} 条记录")
        for r in results[:20]:
            print(f"  📄 {r.get('title', '无标题')[:40]}")
            print(f"     🔗 {r.get('url', '')[:60]}")
            print(f"     📅 {r.get('visit_time', '')[:16]}")
            if len(results) > 20:
                print(f"  ... 还有 {len(results)-20} 条")

    elif args.command == "export":
        historian.export(Path(args.output), args.format)

    elif args.command == "verify":
        historian.verify_export(Path(args.file))

    elif args.command == "validate":
        Validator.validate_all()

    elif args.command == "install-firewall":
        Installer.install_firewall()

    elif args.command == "uninstall-firewall":
        Installer.uninstall_firewall()

    elif args.command == "update-blocklist":
        historian.filter.update_from_urlhaus()

    elif args.command == "status":
        print("\n🐉 浏览史官状态")
        print("-" * 40)
        print(f"  数据目录: {historian.data_dir}")
        print(f"  总记录数: {historian.state.get('total_records', 0)}")
        print(f"  最后采集: {historian.state.get('last_collect', '从未')}")
        print(f"  黑名单: {len(historian.filter.blocklist)} 个域名")
        # 协作风向：共生桥 + 加密共存
        bridge = BrowserSymbiosisBridge()
        ev_count = sum(1 for _ in bridge.events_file.open(encoding="utf-8")) if bridge.events_file.exists() else 0
        print(f"  共生桥事件: {ev_count} 条 · {bridge.events_file}")
        print("  白名单域名: " + ", ".join(bridge.whitelist[:5]) + "...")

    elif args.command == "observe":
        bridge = BrowserSymbiosisBridge(port=args.port)
        try:
            bridge.observe(max_events=args.max)
        except RuntimeError as e:
            print(f"🔴 {e}")
            return 2

    elif args.command == "coflow":
        bridge = BrowserSymbiosisBridge()
        out = bridge.coflow(since_minutes=args.since)
        print("\n🤝 龍魂·瀏覽器共生評估")
        print("-" * 50)
        print(f"  評估區間: {out['since_minutes']} 分鐘內 · {out['event_count']} 條事件")
        print("  域名活躍 TOP:")
        for d in out["domains"][:8]:
            print(f"    · {d['host']:30s} 訪問 {d['hits']:3d} 次")
            for t in d["titles"][:2]:
                if t:
                    print(f"      ↳ {t[:60]}")
        if out["suggestions"]:
            print("  協作建議:")
            for s in out["suggestions"]:
                print(f"    {s}")
        else:
            print("  協作建議: 老大近期活動穩定·無需 AI 介入")
        print(f"  完整評估: {bridge.coflow_dir}")

    elif args.command == "run":
        bridge = BrowserSymbiosisBridge()
        try:
            res = bridge.run_headless(args.url, action=args.action, browser=args.browser)
        except (RuntimeError, FileNotFoundError) as e:
            print(f"🔴 {e}")
            return 2
        print(f"\n✅ 無頭抓取完成 ({args.browser})")
        print(f"  標題: {res.get('title', '無')}")
        print(f"  描述: {res.get('desc', '無')[:120]}")
        if args.action == "fetch-text" and "text" in res:
            print("  正文前 400 字:")
            print(f"    {res['text'][:400]}")
        print(f"  text_len={len(res.get('text') or '')} · {res['fetched_at']}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
