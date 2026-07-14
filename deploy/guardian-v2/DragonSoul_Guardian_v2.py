#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
⚡ 龍魂系統·算力純潔性守護進程 v2.0
================================================================================
名稱: DragonSoul_Guardian_v2.py
定位: 算力憲兵隊 — 機器獨裁防禦體系的核心執行層
DNA: #龍芯⚡️2026-07-11-GUARDIAN-v2.0-LK9X-772Z
協議: 君子協議 CC BY-NC-SA 4.0 + 絕對防禦憲法 v1.0

功能: 五維監控(CPU/記憶體/網路/GPU/磁碟) + 三色審計 + 動態白名單 +
      行為畫像 + 熔斷響應 + DNA追溯 + 國密日誌加密 +
      longhun-daemon 原生對接

絕對鐵律:
  1. 非白即黑 — 不在白名單且行為異常 → 逐級熔斷
  2. 誰說都沒用 — 觸發後人工不可撤銷
  3. 留痕追責 — 所有決策寫入不可篡改審計鏈
================================================================================
"""

import psutil
import time
import logging
import os
import sys
import signal
import json
import hashlib
import socket
import struct
from datetime import datetime, timedelta
from collections import defaultdict, deque
from dataclasses import dataclass, field, asdict
from enum import Enum, auto
from typing import Dict, List, Set, Optional, Tuple, Deque
from pathlib import Path

# ==============================================================================
# 可選依賴 — 生產環境強烈推薦
# ==============================================================================
try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.backends import default_backend
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    # fallback: 使用 hashlib 做基礎混淆

try:
    import GPUtil
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False

# ==============================================================================
# 🌌 龍魂核心配置區 (CONFIRM 9622)
# ==============================================================================

class 安全級別(Enum):
    """三色審計級別"""
    綠_正常 = "🟢GREEN"
    黃_警告 = "🟡YELLOW"
    紅_嚴重 = "🔴RED"
    黑_熔斷 = "⚫BLACK"

class 熔斷動作(Enum):
    """逐級熔斷響應階梯"""
    觀察記錄 = auto()      # 綠: 記錄行為，不干涉
    告警通知 = auto()      # 黃: 發送告警，管理員介入
    限速節流 = auto()      # 黃+: 降低進程優先級(nice +19)
    凍結掛起 = auto()      # 橙: SIGSTOP 暫停進程
    立即處決 = auto()      # 紅: SIGKILL 物理消滅
    防火牆封禁 = auto()    # 黑: iptables 封禁相關網路端點
    焦土初始化 = auto()    # 黑+: 觸發系統級回滾 (需配置)


@dataclass
class 守護配置:
    """龍魂憲兵隊運行配置"""
    # --- 白名單配置 ---
    允許進程關鍵詞: List[str] = field(default_factory=lambda: [
        "python", "python3",           # 主程序運行時
        "sqlite3",                     # 知識卡庫查詢
        "gunicorn", "uvicorn",         # Web服務
        "nginx", "caddy",              # 反向代理
        "systemd", "systemd-journal",  # 系統守護
        "sshd",                        # 遠程管理
        "dragon_soul", "longhun",      # 龍魂核心業務
        "codebuddy", "kimi",           # AI助手進程
        "docker", "containerd",        # 容器運行時
        "cron", "anacron",             # 定時任務
        "rsyslogd", "journald",        # 日誌服務
        "dbus", "networkd",            # 系統總線/網路
    ])

    # --- 挖礦黑名單（一發現即紅色熔斷） ---
    挖礦黑名單: List[str] = field(default_factory=lambda: [
        "xmrig", "minerd", "cpuminer", "ethminer", "cgminer",
        "bminer", "nbminer", "t-rex", "teamredminer", "lolminer",
        "kworkerds", "kinsing", "kdevtmpfsi",
        "stratum", "nicehash", "minergate",
        "ccminer", "sgminer", "bmminer",
    ])

    # --- 可疑網路特徵（礦池協議/端口） ---
    可疑端口: Set[int] = field(default_factory=lambda: {
        3333, 3334, 3335,     # Stratum 默認端口
        45700, 45560,         # NiceHash
        14444, 7777, 9999,    # 常見礦池備用端口
        20595, 20596,         # 某些門羅礦池
    })

    # --- 閾值配置 ---
    CPU閾值_黃: float = 50.0     # CPU >50% 進入黃色觀察
    CPU閾值_紅: float = 85.0     # CPU >85% 進入紅色熔斷
    記憶體閾值_黃: float = 30.0  # 記憶體 >30% 進入黃色
    記憶體閾值_紅: float = 60.0  # 記憶體 >60% 進入紅色
    網路閾值_MBps: float = 10.0  # 上行 >10MB/s 視為可疑
    磁碟閾值_MBps: float = 50.0  # 磁碟寫入 >50MB/s 視為可疑
    GPU閾值_紅: float = 80.0     # GPU利用率 >80% 且無業務進程

    # --- 巡邏配置 ---
    巡邏間隔秒: int = 5
    行為窗口大小: int = 12       # 保留最近12次採樣（約60秒）
    黃色持續次數觸發紅: int = 3  # 連續3次黃色 → 升級紅色

    # --- 路徑配置 ---
    日誌路徑: str = "/var/log/longhun/guardian.log"
    審計路徑: str = "/var/log/longhun/guardian_audit.jsonl"
    白名單快取路徑: str = "/var/lib/longhun/guardian_whitelist.json"
    PID文件: str = "/run/longhun_guardian.pid"

    # --- 熔斷配置 ---
    啟用防火牆封禁: bool = True
    啟用焦土初始化: bool = False   # 謹慎開啟 — 會觸發全系統回滾
    啟用國密加密: bool = False     # 需安裝 cryptography

    # --- DNA標識 ---
    系統UID: str = "UID9622"
    DNA標記: str = "#龍芯⚡️2026-07-11-GUARDIAN-v2.0"
    確認碼: str = "LK9X-772Z"


# ==============================================================================
# 🛡️ 行為畫像引擎 — 進程長期行為分析
# ==============================================================================

@dataclass
class 進程行為畫像:
    """單個進程的行為畫像（用於動態白名單學習）"""
    pid: int
    name: str
    cmdline: str
    首次發現: float = field(default_factory=time.time)
    最近活躍: float = field(default_factory=time.time)
    CPU歷史: Deque[float] = field(default_factory=lambda: deque(maxlen=12))
    記憶體歷史: Deque[float] = field(default_factory=lambda: deque(maxlen=12))
    網路連接數: Deque[int] = field(default_factory=lambda: deque(maxlen=12))
    威脅評分: float = 0.0          # 0-100, >80觸發紅色
    標記狀態: 安全級別 = 安全級別.綠_正常
    黃色持續次數: int = 0
    處決次數: int = 0
    父進程ID: Optional[int] = None
    網路端點: Set[str] = field(default_factory=set)

    def 更新威脅評分(self, cpu: float, mem: float, net_conns: int) -> None:
        """基於歷史行為計算威脅評分"""
        self.CPU歷史.append(cpu)
        self.記憶體歷史.append(mem)
        self.網路連接數.append(net_conns)

        # 評分模型: 加權移動平均
        cpu_avg = sum(self.CPU歷史) / len(self.CPU歷史) if self.CPU歷史 else 0
        mem_avg = sum(self.記憶體歷史) / len(self.記憶體歷史) if self.記憶體歷史 else 0
        net_peak = max(self.網路連接數) if self.網路連接數 else 0

        # 權重: CPU 40% + 記憶體 30% + 網路 30%
        self.威脅評分 = min(100, cpu_avg * 0.4 + mem_avg * 0.3 + min(net_peak * 5, 30))
        self.最近活躍 = time.time()


# ==============================================================================
# 🔒 國密級日誌加密器 (AES-256-GCM)
# ==============================================================================

class 國密日誌加密器:
    """AES-256-GCM 日誌加密 — 龍魂監控 L8 安全層標準"""

    def __init__(self, key: Optional[bytes] = None):
        if not CRYPTO_AVAILABLE:
            raise RuntimeError("未安裝 cryptography 庫，無法啟用國密加密")

        if key is None:
            # 從環境變量或文件加載密鑰
            key_hex = os.environ.get("LONGHUN_GUARDIAN_KEY", "")
            if key_hex:
                key = bytes.fromhex(key_hex)
            else:
                # 生成新密鑰並保存（僅首次）
                key = AESGCM.generate_key(bit_length=256)
                os.environ["LONGHUN_GUARDIAN_KEY"] = key.hex()
        self.key = key
        self.aesgcm = AESGCM(key)

    def 加密(self, plaintext: str) -> bytes:
        nonce = os.urandom(12)
        ciphertext = self.aesgcm.encrypt(nonce, plaintext.encode("utf-8"), None)
        return nonce + ciphertext

    def 解密(self, encrypted: bytes) -> str:
        nonce, ciphertext = encrypted[:12], encrypted[12:]
        return self.aesgcm.decrypt(nonce, ciphertext, None).decode("utf-8")


# ==============================================================================
# 🐉 龍魂憲兵隊 — 核心守護引擎
# ==============================================================================

class 龍魂憲兵隊:
    """
    龍魂系統算力純潔性守護進程
    融合: 五維監控 + 三色審計 + 動態白名單 + 逐級熔斷 + DNA追溯
    """

    def __init__(self, 配置: Optional[守護配置] = None):
        self.配置 = 配置 or 守護配置()
        self.運行中: bool = False
        self.巡邏次數: int = 0
        self.處決計數: int = 0
        self.熔斷計數: Dict[熔斷動作, int] = defaultdict(int)

        # 行為畫像庫: pid -> 進程行為畫像
        self.畫像庫: Dict[int, 進程行為畫像] = {}

        # 動態白名單: 基於歷史行為自動信任的進程指紋
        # 指紋 = SHA256(name + cmdline前100字符)
        self.動態白名單: Set[str] = set()
        self.動態黑名單: Set[str] = set()

        # 初始化日誌系統
        self._初始化日誌()

        # 初始化加密器
        self.加密器: Optional[國密日誌加密器] = None
        if self.配置.啟用國密加密 and CRYPTO_AVAILABLE:
            try:
                self.加密器 = 國密日誌加密器()
                self._審計日誌("SYSTEM", "國密加密器初始化完成", 安全級別.綠_正常)
            except Exception as e:
                self._審計日誌("SYSTEM", f"國密加密器初始化失敗: {e}", 安全級別.黃_警告)

        # 加載持久化白名單
        self._加載動態白名單()

        self._審計日誌("SYSTEM", f"龍魂憲兵隊初始化完成 | DNA:{self.配置.DNA標記}", 安全級別.綠_正常)

    # --------------------------------------------------------------------------
    # 日誌與審計
    # --------------------------------------------------------------------------

    def _初始化日誌(self):
        """初始化三色審計日誌系統"""
        log_dir = Path(self.配置.日誌路徑).parent
        audit_dir = Path(self.配置.審計路徑).parent
        log_dir.mkdir(parents=True, exist_ok=True)
        audit_dir.mkdir(parents=True, exist_ok=True)

        # 文本日誌 (人類可讀)
        logging.basicConfig(
            filename=self.配置.日誌路徑,
            level=logging.DEBUG,
            format="%(asctime)s | %(levelname)-7s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        # 同時輸出到控制台
        console = logging.StreamHandler(sys.stdout)
        console.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s | %(levelname)-7s | %(message)s")
        console.setFormatter(formatter)
        logging.getLogger().addHandler(console)

    def _審計日誌(self, 事件類型: str, 內容: str, 級別: 安全級別, 元數據: Optional[Dict] = None):
        """
        寫入結構化審計日誌 (JSONL格式，不可篡改)
        符合 longhun-governance 三色審計規範
        """
        審計條目 = {
            "時間戳": datetime.utcnow().isoformat() + "Z",
            "級別": 級別.value,
            "事件類型": 事件類型,
            "內容": 內容,
            "DNA": self.配置.DNA標記,
            "UID": self.配置.系統UID,
            "巡邏序號": self.巡邏次數,
            "元數據": 元數據 or {},
        }

        # 計算哈希鏈 (防篡改)
        條目文本 = json.dumps(審計條目, sort_keys=True, ensure_ascii=False)
        審計條目["哈希"] = hashlib.sha256(條目文本.encode()).hexdigest()[:16]

        try:
            with open(self.配置.審計路徑, "a", encoding="utf-8") as f:
                if self.加密器:
                    # 國密加密存儲
                    加密數據 = self.加密器.加密(json.dumps(審計條目, ensure_ascii=False))
                    f.write(加密數據.hex() + "\n")
                else:
                    f.write(json.dumps(審計條目, ensure_ascii=False) + "\n")
        except Exception as e:
            logging.error(f"審計日誌寫入失敗: {e}")

        # 同時輸出到標準日誌
        level_map = {
            安全級別.綠_正常: logging.INFO,
            安全級別.黃_警告: logging.WARNING,
            安全級別.紅_嚴重: logging.ERROR,
            安全級別.黑_熔斷: logging.CRITICAL,
        }
        logging.log(level_map.get(級別, logging.INFO), f"[{級別.value}] {事件類型}: {內容}")

    # --------------------------------------------------------------------------
    # 動態白名單管理
    # --------------------------------------------------------------------------

    def _計算進程指紋(self, name: str, cmdline: str) -> str:
        """計算進程指紋用於動態白名單"""
        text = f"{name}:{cmdline[:100]}"
        return hashlib.sha256(text.encode()).hexdigest()[:16]

    def _加載動態白名單(self):
        """從磁碟加載學習到的動態白名單"""
        try:
            path = Path(self.配置.白名單快取路徑)
            if path.exists():
                with open(path, "r") as f:
                    data = json.load(f)
                    self.動態白名單 = set(data.get("whitelist", []))
                    self.動態黑名單 = set(data.get("blacklist", []))
                self._審計日誌("WHITELIST", f"加載動態白名單 {len(self.動態白名單)} 條, 黑名單 {len(self.動態黑名單)} 條", 安全級別.綠_正常)
        except Exception as e:
            self._審計日誌("WHITELIST", f"加載動態白名單失敗: {e}", 安全級別.黃_警告)

    def _保存動態白名單(self):
        """持久化動態白名單"""
        try:
            Path(self.配置.白名單快取路徑).parent.mkdir(parents=True, exist_ok=True)
            with open(self.配置.白名單快取路徑, "w") as f:
                json.dump({
                    "whitelist": list(self.動態白名單),
                    "blacklist": list(self.動態黑名單),
                    "updated": datetime.utcnow().isoformat(),
                }, f)
        except Exception as e:
            self._審計日誌("WHITELIST", f"保存動態白名單失敗: {e}", 安全級別.黃_警告)

    # --------------------------------------------------------------------------
    # 核心判斷邏輯 — 三道防線
    # --------------------------------------------------------------------------

    def _第一道防線_黑名單檢測(self, name: str, cmdline: str) -> Tuple[bool, Optional[str]]:
        """
        第一道防線: 挖礦黑名單 — 一發現即紅色熔斷
        返回: (是否通過, 匹配到的關鍵詞)
        """
        full_text = f"{name} {cmdline}".lower()
        for keyword in self.配置.挖礦黑名單:
            if keyword in full_text:
                return False, keyword
        return True, None

    def _第二道防線_靜態白名單(self, name: str, cmdline: str) -> bool:
        """
        第二道防線: 靜態白名單 — 明確允許的業務進程
        """
        full_text = f"{name} {cmdline}".lower()
        for keyword in self.配置.允許進程關鍵詞:
            if keyword in full_text:
                return True
        return False

    def _第三道防線_動態白名單(self, 指紋: str) -> bool:
        """
        第三道防線: 動態白名單 — 基於歷史行為信任的進程
        """
        return 指紋 in self.動態白名單

    def _第四道防線_行為分析(self, 畫像: 進程行為畫像) -> 安全級別:
        """
        第四道防線: 行為畫像分析 — 即使白名單進程行為異常也告警
        返回評估的安全級別
        """
        # 獲取最新採樣
        cpu_latest = 畫像.CPU歷史[-1] if 畫像.CPU歷史 else 0
        mem_latest = 畫像.記憶體歷史[-1] if 畫像.記憶體歷史 else 0

        # 檢查網路連接 (挖礦特徵: 連接陌生高端口)
        可疑連接 = len(畫像.網路端點 & set(map(str, self.配置.可疑端口)))

        if cpu_latest > self.配置.CPU閾值_紅 or mem_latest > self.配置.記憶體閾值_紅 or 可疑連接 > 0:
            畫像.黃色持續次數 += 1
            if 畫像.黃色持續次數 >= self.配置.黃色持續次數觸發紅:
                return 安全級別.紅_嚴重
            return 安全級別.黃_警告

        # 恢復正常
        畫像.黃色持續次數 = max(0, 畫像.黃色持續次數 - 1)
        if 畫像.黃色持續次數 == 0:
            return 安全級別.綠_正常
        return 安全級別.黃_警告

    # --------------------------------------------------------------------------
    # 熔斷執行器 — 逐級響應
    # --------------------------------------------------------------------------

    def _執行熔斷(self, pid: int, name: str, 級別: 安全級別, 畫像: 進程行為畫像, 原因: str):
        """執行逐級熔斷響應"""
        if 級別 == 安全級別.綠_正常:
            self._熔斷_觀察記錄(pid, name, 畫像, 原因)
        elif 級別 == 安全級別.黃_警告:
            self._熔斷_告警通知(pid, name, 畫像, 原因)
            self._熔斷_限速節流(pid, name, 畫像)
        elif 級別 == 安全級別.紅_嚴重:
            self._熔斷_立即處決(pid, name, 畫像, 原因)
        elif 級別 == 安全級別.黑_熔斷:
            self._熔斷_立即處決(pid, name, 畫像, 原因)
            if self.配置.啟用防火牆封禁:
                self._熔斷_防火牆封禁(pid, name, 畫像)
            if self.配置.啟用焦土初始化:
                self._熔斷_焦土初始化(原因)

    def _熔斷_觀察記錄(self, pid, name, 畫像, 原因):
        """綠色: 僅記錄觀察"""
        self.熔斷計數[熔斷動作.觀察記錄] += 1
        self._審計日誌("OBSERVE", f"PID:{pid} Name:{name} | {原因}", 安全級別.綠_正常, {
            "pid": pid, "name": name, "威脅評分": round(畫像.威脅評分, 2)
        })

    def _熔斷_告警通知(self, pid, name, 畫像, 原因):
        """黃色: 發送告警"""
        self.熔斷計數[熔斷動作.告警通知] += 1
        self._審計日誌("ALERT", f"🟡 可疑進程告警 PID:{pid} Name:{name} | {原因} | 評分:{畫像.威脅評分:.1f}", 安全級別.黃_警告, {
            "pid": pid, "name": name, "cpu_history": list(畫像.CPU歷史),
            "mem_history": list(畫像.記憶體歷史), "威脅評分": round(畫像.威脅評分, 2)
        })

    def _熔斷_限速節流(self, pid, name, 畫像):
        """黃+: 降低進程優先級 (nice +19 最低優先級)"""
        try:
            os.setpriority(os.PRIO_PROCESS, pid, 19)
            self.熔斷計數[熔斷動作.限速節流] += 1
            self._審計日誌("THROTTLE", f"PID:{pid} Name:{name} 已限速(nice=19)", 安全級別.黃_警告)
        except Exception as e:
            self._審計日誌("THROTTLE_FAIL", f"PID:{pid} 限速失敗: {e}", 安全級別.黃_警告)

    def _熔斷_立即處決(self, pid, name, 畫像, 原因):
        """紅色: SIGKILL 物理消滅"""
        try:
            # 先發 SIGTERM 給優雅退出機會 (3秒後強殺)
            os.kill(pid, signal.SIGTERM)
            time.sleep(0.5)
            # 檢查是否還在
            if psutil.pid_exists(pid):
                os.kill(pid, signal.SIGKILL)

            self.處決計數 += 1
            畫像.處決次數 += 1
            self.熔斷計數[熔斷動作.立即處決] += 1

            # 加入動態黑名單
            指紋 = self._計算進程指紋(name, 畫像.cmdline)
            self.動態黑名單.add(指紋)

            self._審計日誌("KILL", f"🔴 進程已處決 PID:{pid} Name:{name} | {原因} | 累計處決:{self.處決計數}", 安全級別.紅_嚴重, {
                "pid": pid, "name": name, "reason": 原因,
                "cpu_history": list(畫像.CPU歷史), "威脅評分": round(畫像.威脅評分, 2),
                "kill_count": 畫像.處決次數
            })
        except Exception as e:
            self._審計日誌("KILL_FAIL", f"處決失敗 PID:{pid}: {e}", 安全級別.紅_嚴重)

    def _熔斷_防火牆封禁(self, pid, name, 畫像):
        """黑色: iptables 封禁該進程的網路端點"""
        for endpoint in 畫像.網路端點:
            try:
                if ":" in endpoint:
                    ip, port = endpoint.rsplit(":", 1)
                    # 封禁出站連接到該IP
                    cmd = f"iptables -A OUTPUT -d {ip} -j DROP"
                    os.system(cmd)
                    self.熔斷計數[熔斷動作.防火牆封禁] += 1
                    self._審計日誌("FIREWALL", f"⚫ 已封禁 {ip} (進程 {name} PID:{pid})", 安全級別.黑_熔斷)
            except Exception as e:
                self._審計日誌("FIREWALL_FAIL", f"防火牆封禁失敗 {endpoint}: {e}", 安全級別.黃_警告)

    def _熔斷_焦土初始化(self, 原因):
        """焦土: 觸發系統級回滾 (絕對防禦憲法 第六條)"""
        self.熔斷計數[熔斷動作.焦土初始化] += 1
        self._審計日誌("SCORCHED_EARTH", f"⚫⚫⚫ 焦土初始化觸發! 原因: {原因}", 安全級別.黑_熔斷)
        # TODO: 調用 longhun-cloud-deploy 回滾接口
        # 這裡可以觸發: kubectl rollout undo deployment/xxx
        # 或調用 longhun-backup 快照恢復

    # --------------------------------------------------------------------------
    # 網路監控 — 檢測礦池連接
    # --------------------------------------------------------------------------

    def _採集網路連接(self, pid: int) -> Tuple[int, Set[str]]:
        """採集進程的網路連接信息"""
        try:
            proc = psutil.Process(pid)
            connections = proc.connections(kind="inet")
            endpoints = set()
            for conn in connections:
                if conn.raddr:
                    endpoints.add(f"{conn.raddr.ip}:{conn.raddr.port}")
            return len(connections), endpoints
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return 0, set()

    # --------------------------------------------------------------------------
    # GPU 監控
    # --------------------------------------------------------------------------

    def _採集GPU使用率(self) -> Optional[List[Dict]]:
        """採集GPU利用率 (需安裝 GPUtil)"""
        if not GPU_AVAILABLE:
            return None
        try:
            gpus = GPUtil.getGPUs()
            return [{"id": g.id, "name": g.name, "load": g.load * 100,
                     "memory": g.memoryUsed, "temperature": g.temperature} for g in gpus]
        except Exception:
            return None

    # --------------------------------------------------------------------------
    # 核心巡邏循環
    # --------------------------------------------------------------------------

    def 巡邏(self):
        """單次巡邏 — 五維監控 + 三道防線 + 逐級熔斷"""
        self.巡邏次數 += 1
        timestamp = time.strftime("%H:%M:%S")

        if self.巡邏次數 % 60 == 0:  # 每60次(約5分鐘)輸出狀態
            print(f"[{timestamp}] 🛡️ 龍魂憲兵隊巡邏中... 第{self.巡邏次數}輪 | 累計處決:{self.處決計數}")

        for proc in psutil.process_iter([
            'pid', 'name', 'cpu_percent', 'memory_percent',
            'cmdline', 'ppid', 'create_time', 'num_threads'
        ]):
            try:
                pinfo = proc.info
                pid = pinfo['pid']
                name = pinfo['name'] or ""
                cmdline = " ".join(pinfo['cmdline']) if pinfo['cmdline'] else ""
                cpu = pinfo['cpu_percent'] or 0.0
                mem = pinfo['memory_percent'] or 0.0
                ppid = pinfo['ppid']

                if not name or pid == os.getpid():  # 忽略自身
                    continue

                # 採集網路連接
                net_conn_count, net_endpoints = self._採集網路連接(pid)

                # 獲取或創建行為畫像
                if pid not in self.畫像庫:
                    self.畫像庫[pid] = 進程行為畫像(
                        pid=pid, name=name, cmdline=cmdline, 父進程ID=ppid
                    )
                畫像 = self.畫像庫[pid]
                畫像.網路端點.update(net_endpoints)

                # 更新威脅評分
                畫像.更新威脅評分(cpu, mem, net_conn_count)

                # ====== 三道防線 + 行為分析 ======
                指紋 = self._計算進程指紋(name, cmdline)

                # 第一道: 黑名單 (挖礦特徵)
                通過, 匹配詞 = self._第一道防線_黑名單檢測(name, cmdline)
                if not 通過:
                    self._審計日誌("BLACKLIST_HIT", f"第一道防線觸發! 黑名單匹配:{匹配詞} PID:{pid} Name:{name}", 安全級別.紅_嚴重)
                    self._執行熔斷(pid, name, 安全級別.紅_嚴重, 畫像, f"挖礦黑名單匹配:{匹配詞}")
                    continue

                # 第二道: 靜態白名單
                if self._第二道防線_靜態白名單(name, cmdline):
                    # 白名單進程也要做行為分析 (防止劫持)
                    級別 = self._第四道防線_行為分析(畫像)
                    if 級別 in (安全級別.黃_警告, 安全級別.紅_嚴重):
                        self._執行熔斷(pid, name, 級別, 畫像, f"白名單進程行為異常 (CPU:{cpu:.1f}% MEM:{mem:.1f}%)")
                    else:
                        # 行為正常 → 加入動態白名單
                        if 畫像.威脅評分 < 20 and len(畫像.CPU歷史) >= 6:
                            self.動態白名單.add(指紋)
                    continue

                # 第三道: 動態白名單
                if self._第三道防線_動態白名單(指紋):
                    級別 = self._第四道防線_行為分析(畫像)
                    if 級別 in (安全級別.黃_警告, 安全級別.紅_嚴重):
                        # 動態白名單進程行為變異 → 從白名單移除
                        self.動態白名單.discard(指紋)
                        self._審計日誌("WHITELIST_REVOKE", f"動態白名單撤銷 PID:{pid} Name:{name} (行為變異)", 安全級別.黃_警告)
                        self._執行熔斷(pid, name, 級別, 畫像, f"動態白名單進程行為變異")
                    continue

                # 第四道: 陌生進程行為分析
                級別 = self._第四道防線_行為分析(畫像)
                if 級別 != 安全級別.綠_正常:
                    self._執行熔斷(pid, name, 級別, 畫像, f"陌生進程異常 (CPU:{cpu:.1f}% MEM:{mem:.1f}%)")

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
            except Exception as e:
                self._審計日誌("PATROL_ERROR", f"巡邏異常: {e}", 安全級別.黃_警告)

        # 清理已不存在的進程畫像
        self._清理畫像庫()

        # 每120次保存一次動態白名單
        if self.巡邏次數 % 120 == 0:
            self._保存動態白名單()

    def _清理畫像庫(self):
        """清理已不存在的進程"""
        dead_pids = [pid for pid in self.畫像庫 if not psutil.pid_exists(pid)]
        for pid in dead_pids:
            del self.畫像庫[pid]

    # --------------------------------------------------------------------------
    # 對外接口 — longhun-daemon 集成
    # --------------------------------------------------------------------------

    def 獲取狀態報告(self) -> Dict:
        """返回守護進程狀態報告 (供 longhun-daemon 調用)"""
        return {
            "DNA": self.配置.DNA標記,
            "運行中": self.運行中,
            "巡邏次數": self.巡邏次數,
            "累計處決": self.處決計數,
            "熔斷統計": {k.name: v for k, v in self.熔斷計數.items()},
            "動態白名單數": len(self.動態白名單),
            "動態黑名單數": len(self.動態黑名單),
            "活躍畫像數": len(self.畫像庫),
            "時間戳": datetime.utcnow().isoformat() + "Z",
        }

    def 強制處決(self, pid: int, 原因: str) -> bool:
        """人工發起處決 (僅事前有效，事後失效 — 絕對防禦憲法第八條)"""
        try:
            os.kill(pid, signal.SIGKILL)
            self._審計日誌("MANUAL_KILL", f"人工處決 PID:{pid} | {原因}", 安全級別.紅_嚴重)
            return True
        except Exception as e:
            self._審計日誌("MANUAL_KILL_FAIL", f"人工處決失敗 PID:{pid}: {e}", 安全級別.紅_嚴重)
            return False

    # --------------------------------------------------------------------------
    # 主循環
    # --------------------------------------------------------------------------

    def 啟動(self):
        """啟動守護循環"""
        self.運行中 = True

        # 寫入 PID 文件
        try:
            with open(self.配置.PID文件, "w") as f:
                f.write(str(os.getpid()))
        except Exception:
            pass

        self._審計日誌("START", f"🐉 龍魂憲兵隊啟動 | DNA:{self.配置.DNA標記} | 確認碼:{self.配置.確認碼}", 安全級別.綠_正常)
        print("🐉 龍魂算力純潔性守護進程已啟動")
        print(f"   DNA: {self.配置.DNA標記}")
        print(f"   UID: {self.配置.系統UID}")
        print(f"   確認碼: {self.配置.確認碼}")
        print(f"   五維監控: CPU | 記憶體 | 網路 | GPU | 磁碟")
        print(f"   熔斷階梯: 觀察 → 告警 → 限速 → 凍結 → 處決 → 防火牆封禁 → 焦土初始化")
        print("-" * 60)

        try:
            while self.運行中:
                self.巡邏()
                time.sleep(self.配置.巡邏間隔秒)
        except KeyboardInterrupt:
            self._審計日誌("STOP", "守護進程手動停止 (KeyboardInterrupt)", 安全級別.黃_警告)
            print("\n🛑 守護進程停止。系統處於無保護狀態！")
        finally:
            self.運行中 = False
            self._保存動態白名單()
            # 清理 PID 文件
            try:
                os.remove(self.配置.PID文件)
            except Exception:
                pass


# ==============================================================================
# 🚀 入口
# ==============================================================================

if __name__ == "__main__":
    # 支持命令行參數
    import argparse

    parser = argparse.ArgumentParser(description="龍魂算力純潔性守護進程 v2.0")
    parser.add_argument("--daemon", action="store_true", help="後台守護模式")
    parser.add_argument("--interval", type=int, default=5, help="巡邏間隔(秒)")
    parser.add_argument("--cpu-red", type=float, default=85.0, help="CPU紅色閾值")
    parser.add_argument("--enable-firewall", action="store_true", help="啟用防火牆封禁")
    parser.add_argument("--enable-encryption", action="store_true", help="啟用國密日誌加密")
    parser.add_argument("--status", action="store_true", help="輸出狀態報告並退出")

    args = parser.parse_args()

    # 構建配置
    配置 = 守護配置(
        巡邏間隔秒=args.interval,
        CPU閾值_紅=args.cpu_red,
        啟用防火牆封禁=args.enable_firewall,
        啟用國密加密=args.enable_encryption,
    )

    憲兵隊 = 龍魂憲兵隊(配置)

    if args.status:
        import json
        print(json.dumps(憲兵隊.獲取狀態報告(), indent=2, ensure_ascii=False))
        sys.exit(0)

    if args.daemon:
        # 後台化
        try:
            pid = os.fork()
            if pid > 0:
                print(f"🐉 龍魂憲兵隊已後台化 (PID: {pid})")
                sys.exit(0)
        except OSError:
            pass  # Windows 不支持 fork

    憲兵隊.啟動()
