#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️2026-06-19-LONGHUN-DAEMON-v5.2
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
================================================================================
【龍魂守護進程管理器】
================================================================================
· 功能：安裝 / 啟動 / 停止 / 重啟龍魂系統守護進程
· 架構：systemd / launchd 雙模式適配
· 規範：CNSH中文編程規範 v5.2
· 君子協議：未經授權不得修改核心進程參數
================================================================================
· DNA: #龍芯⚡️2026-06-19-LONGHUN-DAEMON-v5.2
================================================================================
"""

import os
import sys
import json
import time
import shutil
import signal
import socket
import hashlib
import argparse
import platform
import datetime
import traceback
import subprocess
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable

# ═══════════════════════════════════════════════════════════════════════════════
# 第一區：DNA追溯與全域常數
# ═══════════════════════════════════════════════════════════════════════════════
龍魂DNA追溯碼 = "#龍芯⚡️2026-06-19-LONGHUN-DAEMON-v5.2"
龍魂版本號 = "v5.2.0"
龍魂編譯標記 = "2026-06-19"

# 三色審計級別
審計級別_紅 = "紅"      # 致命錯誤 → 立即告警
審計級別_黃 = "黃"      # 警告異常 → 記錄追蹤
審計級別_綠 = "綠"      # 正常運行 → 常規記錄

# 服務配置
服務註冊表 = {
    "龍魂操作台": {
        "端口": 8443,
        "路徑": "/",
        "進程標識": "longhun-console",
        "啟動指令": ["python3", "-m", "http.server", "8443"],
        "健康檢查路徑": "/health",
        "依賴服務": [],
        "超時秒數": 30,
        "自動重啟": True,
        "最大重試次數": 5,
    },
    "MCP服務": {
        "端口": 8443,
        "路徑": "/mcp",
        "進程標識": "longhun-mcp",
        "啟動指令": ["python3", "-m", "mcp.server"],
        "健康檢查路徑": "/mcp/health",
        "依賴服務": ["龍魂操作台"],
        "超時秒數": 30,
        "自動重啟": True,
        "最大重試次數": 3,
    },
    "Kimi集成": {
        "端口": 8443,
        "路徑": "/kimi",
        "進程標識": "longhun-kimi",
        "啟動指令": ["python3", "-m", "longhun.kimi_bridge"],
        "健康檢查路徑": "/kimi/health",
        "依賴服務": ["龍魂操作台", "MCP服務"],
        "超時秒數": 30,
        "自動重啟": True,
        "最大重試次數": 3,
    },
    "Notion同步": {
        "端口": 0,
        "路徑": "",
        "進程標識": "longhun-notion-sync",
        "啟動指令": ["python3", "-m", "longhun.notion_sync"],
        "健康檢查路徑": "",
        "依賴服務": ["龍魂操作台"],
        "超時秒數": 60,
        "自動重啟": False,
        "最大重試次數": 2,
        "定時觸發": "*/5 * * * *",  # 每5分鐘
    },
    "自動化評估": {
        "端口": 0,
        "路徑": "",
        "進程標識": "longhun-auto-eval",
        "啟動指令": ["python3", "-m", "longhun.auto_evaluation"],
        "健康檢查路徑": "",
        "依賴服務": ["龍魂操作台", "MCP服務"],
        "超時秒數": 120,
        "自動重啟": False,
        "最大重試次數": 1,
        "定時觸發": "30 22 * * *",  # 每日22:30
    },
    "復盤引擎": {
        "端口": 0,
        "路徑": "",
        "進程標識": "longhun-review-engine",
        "啟動指令": ["python3", "-m", "longhun.review_engine"],
        "健康檢查路徑": "",
        "依賴服務": ["龍魂操作台", "自動化評估"],
        "超時秒數": 180,
        "自動重啟": False,
        "最大重試次數": 1,
        "定時觸發": "0 23 * * *",  # 每日23:00
    },
}

# ═══════════════════════════════════════════════════════════════════════════════
# 第二區：審計日誌系統
# ═══════════════════════════════════════════════════════════════════════════════

class 審計日誌器:
    """三色審計日誌系統 — 所有操作留痕可追溯"""

    def __init__(self, 日誌目錄: str = ""):
        if not 日誌目錄:
            日誌目錄 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
        self.日誌目錄 = Path(日誌目錄).resolve()
        self.日誌目錄.mkdir(parents=True, exist_ok=True)

        self.日誌文件路徑 = self.日誌目錄 / f"daemon_audit_{datetime.date.today().isoformat()}.log"
        self.運行日誌路徑 = self.日誌目錄 / "launchd.out.log"
        self.錯誤日誌路徑 = self.日誌目錄 / "launchd.err.log"

    def 記錄(self, 級別: str, 模塊: str, 訊息: str, 元數據: dict = None):
        """寫入審計日誌"""
        時間戳 = datetime.datetime.now().isoformat()
        龍印 = hashlib.sha256(f"{時間戳}{模塊}{訊息}{龍魂DNA追溯碼}".encode()).hexdigest()[:12]
        記錄行 = f"[{時間戳}] [龍印:{龍印}] [{級別}] [{模塊}] {訊息}"
        if 元數據:
            記錄行 += f" | 元數據:{json.dumps(元數據, ensure_ascii=False)}"
        記錄行 += f" | DNA:{龍魂DNA追溯碼}\n"

        try:
            with open(self.日誌文件路徑, "a", encoding="utf-8") as 檔:
                檔.write(記錄行)
        except Exception as 異常:
            print(f"[審計日誌錯誤] {異常}", file=sys.stderr)

        # 同時輸出到控制台（根據級別着色）
        if 級別 == 審計級別_紅:
            print(f"\033[91m{記錄行.strip()}\033[0m", file=sys.stderr)
        elif 級別 == 審計級別_黃:
            print(f"\033[93m{記錄行.strip()}\033[0m")
        else:
            print(f"\033[92m{記錄行.strip()}\033[0m")

    def 紅(self, 模塊: str, 訊息: str, 元數據: dict = None):
        self.記錄(審計級別_紅, 模塊, 訊息, 元數據)

    def 黃(self, 模塊: str, 訊息: str, 元數據: dict = None):
        self.記錄(審計級別_黃, 模塊, 訊息, 元數據)

    def 綠(self, 模塊: str, 訊息: str, 元數據: dict = None):
        self.記錄(審計級別_綠, 模塊, 訊息, 元數據)

    def 輸出標準(self, 訊息: str):
        """寫入stdout日誌"""
        with open(self.運行日誌路徑, "a", encoding="utf-8") as 檔:
            檔.write(f"[{datetime.datetime.now().isoformat()}] {訊息}\n")

    def 輸出錯誤(self, 訊息: str):
        """寫入stderr日誌"""
        with open(self.錯誤日誌路徑, "a", encoding="utf-8") as 檔:
            檔.write(f"[{datetime.datetime.now().isoformat()}] {訊息}\n")


# 全局日誌實例
日誌 = 審計日誌器()


# ═══════════════════════════════════════════════════════════════════════════════
# 第三區：進程管理核心
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class 進程狀態:
    """進程狀態數據結構"""
    服務名稱: str = ""
    進程ID: int = 0
    狀態: str = "未啟動"  # 未啟動/運行中/已停止/異常/重啟中
    啟動時間: str = ""
    最後心跳: str = ""
    重試計數: int = 0
    總重啟次數: int = 0
    端口佔用: int = 0
    內存使用MB: float = 0.0
    CPU使用率: float = 0.0


class 守護進程管理器:
    """
    龍魂守護進程管理器
    · 管理所有龍魂服務的生命週期
    · 支持 systemd (Linux) 和 launchd (macOS)
    · 自恢復機制：崩潰自動重啟
    """

    def __init__(self):
        self.系統類型 = platform.system().lower()
        self.進程表: Dict[str, 進程狀態] = {}
        self.運行中 = False
        self.配置目錄 = Path(__file__).parent.parent / "config"
        self.配置目錄.mkdir(parents=True, exist_ok=True)
        self.狀態文件 = self.配置目錄 / "daemon_state.json"
        self._加載狀態()
        日誌.綠("守護進程管理器", f"初始化完成 | 系統:{self.系統類型} | DNA:{龍魂DNA追溯碼}")

    def _加載狀態(self):
        """從持久化文件加載進程狀態"""
        if self.狀態文件.exists():
            try:
                with open(self.狀態文件, "r", encoding="utf-8") as 檔:
                    數據 = json.load(檔)
                for 名稱, 狀態數據 in 數據.items():
                    self.進程表[名稱] = 進程狀態(**狀態數據)
                日誌.綠("狀態加載", f"已恢復 {len(self.進程表)} 個服務狀態")
            except Exception as 異常:
                日誌.黃("狀態加載", f"加載失敗，使用默認狀態: {異常}")

    def _保存狀態(self):
        """持久化進程狀態"""
        try:
            數據 = {}
            for 名稱, 狀態 in self.進程表.items():
                數據[名稱] = {
                    "服務名稱": 狀態.服務名稱,
                    "進程ID": 狀態.進程ID,
                    "狀態": 狀態.狀態,
                    "啟動時間": 狀態.啟動時間,
                    "最後心跳": 狀態.最後心跳,
                    "重試計數": 狀態.重試計數,
                    "總重啟次數": 狀態.總重啟次數,
                    "端口佔用": 狀態.端口佔用,
                    "內存使用MB": 狀態.內存使用MB,
                    "CPU使用率": 狀態.CPU使用率,
                }
            with open(self.狀態文件, "w", encoding="utf-8") as 檔:
                json.dump(數據, 檔, ensure_ascii=False, indent=2)
        except Exception as 異常:
            日誌.紅("狀態保存", f"持久化失敗: {異常}")

    # ─────────────────────────────────────────
    # 端口檢測
    # ─────────────────────────────────────────
    def 檢測端口佔用(self, 端口: int) -> bool:
        """檢查端口是否被佔用"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as 探測:
                探測.settimeout(1)
                結果 = 探測.connect_ex(("127.0.0.1", 端口))
                return 結果 == 0
        except Exception:
            return False

    def 查找進程佔用端口(self, 端口: int) -> int:
        """查找佔用端口的進程ID"""
        try:
            if self.系統類型 == "linux":
                結果 = subprocess.run(
                    ["lsof", "-ti", f":{端口}"],
                    capture_output=True, text=True, timeout=5
                )
                if 結果.stdout.strip():
                    return int(結果.stdout.strip().split("\n")[0])
            elif self.系統類型 == "darwin":
                結果 = subprocess.run(
                    ["lsof", "-ti", f":{端口}"],
                    capture_output=True, text=True, timeout=5
                )
                if 結果.stdout.strip():
                    return int(結果.stdout.strip().split("\n")[0])
            elif self.系統類型 == "windows":
                結果 = subprocess.run(
                    ["netstat", "-ano", "|", "findstr", f":{端口}"],
                    capture_output=True, text=True, timeout=5, shell=True
                )
                # Windows netstat parsing simplified
        except Exception as 異常:
            日誌.黃("端口檢測", f"查找進程失敗: {異常}")
        return 0

    # ─────────────────────────────────────────
    # 進程操作
    # ─────────────────────────────────────────
    def 獲取進程狀態(self, 進程ID: int) -> str:
        """檢查進程是否存活"""
        if 進程ID <= 0:
            return "未啟動"
        try:
            os.kill(進程ID, 0)
            return "運行中"
        except OSError:
            return "已停止"

    def 啟動服務(self, 服務名稱: str) -> bool:
        """啟動指定服務"""
        if 服務名稱 not in 服務註冊表:
            日誌.紅("啟動服務", f"未知服務: {服務名稱}")
            return False

        配置 = 服務註冊表[服務名稱]
        日誌.綠("啟動服務", f"正在啟動 [{服務名稱}]...")

        # 檢查依賴
        for 依賴名稱 in 配置.get("依賴服務", []):
            if 依賴名稱 in self.進程表:
                依賴狀態 = self.進程表[依賴名稱]
                if 依賴狀態.狀態 != "運行中":
                    日誌.黃("依賴檢查", f"依賴服務 [{依賴名稱}] 未運行，先啟動依賴")
                    if not self.啟動服務(依賴名稱):
                        日誌.紅("依賴失敗", f"無法啟動依賴 [{依賴名稱}]")
                        return False

        # 檢查端口
        端口 = 配置.get("端口", 0)
        if 端口 > 0 and self.檢測端口佔用(端口):
            佔用進程 = self.查找進程佔用端口(端口)
            日誌.黃("端口檢查", f"端口 {端口} 已被進程 {佔用進程} 佔用")
            if 配置.get("進程標識") not in str(佔用進程):
                # 嘗試釋放端口
                try:
                    os.kill(佔用進程, signal.SIGTERM)
                    time.sleep(1)
                except Exception:
                    pass

        # 啟動進程
        try:
            環境變量 = os.environ.copy()
            環境變量["LONGHUN_DAEMON"] = "1"
            環境變量["LONGHUN_DNA"] = 龍魂DNA追溯碼
            環境變量["LONGHUN_SERVICE"] = 服務名稱

            進程 = subprocess.Popen(
                配置["啟動指令"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=環境變量,
                cwd=str(Path(__file__).parent.parent.parent),
            )

            等待時間 = 0
            超時 = 配置.get("超時秒數", 30)
            while 等待時間 < 超時:
                返回碼 = 進程.poll()
                if 返回碼 is not None:
                    日誌.紅("啟動失敗", f"[{服務名稱}] 進程過早退出，返回碼: {返回碼}")
                    return False
                if 端口 > 0 and self.檢測端口佔用(端口):
                    break
                time.sleep(0.5)
                等待時間 += 0.5

            # 記錄狀態
            狀態 = 進程狀態(
                服務名稱=服務名稱,
                進程ID=進程.pid,
                狀態="運行中",
                啟動時間=datetime.datetime.now().isoformat(),
                最後心跳=datetime.datetime.now().isoformat(),
                端口佔用=端口,
                重試計數=0,
            )
            self.進程表[服務名稱] = 狀態
            self._保存狀態()

            日誌.綠("啟動成功", f"[{服務名稱}] PID={進程.pid} 端口={端口}")
            return True

        except Exception as 異常:
            日誌.紅("啟動異常", f"[{服務名稱}] {traceback.format_exc()}")
            return False

    def 停止服務(self, 服務名稱: str, 強制: bool = False) -> bool:
        """停止指定服務"""
        if 服務名稱 not in self.進程表:
            日誌.黃("停止服務", f"[{服務名稱}] 未在進程表中")
            return True

        狀態 = self.進程表[服務名稱]
        進程ID = 狀態.進程ID

        if 進程ID <= 0 or self.獲取進程狀態(進程ID) != "運行中":
            狀態.狀態 = "已停止"
            狀態.進程ID = 0
            self._保存狀態()
            return True

        日誌.綠("停止服務", f"正在停止 [{服務名稱}] PID={進程ID}")

        try:
            if 強制:
                os.kill(進程ID, signal.SIGKILL)
            else:
                os.kill(進程ID, signal.SIGTERM)
                # 等待優雅退出
                等待 = 0
                while 等待 < 10 and self.獲取進程狀態(進程ID) == "運行中":
                    time.sleep(0.5)
                    等待 += 0.5
                if self.獲取進程狀態(進程ID) == "運行中":
                    os.kill(進程ID, signal.SIGKILL)

            狀態.狀態 = "已停止"
            狀態.進程ID = 0
            self._保存狀態()
            日誌.綠("停止完成", f"[{服務名稱}] 已停止")
            return True

        except ProcessLookupError:
            狀態.狀態 = "已停止"
            狀態.進程ID = 0
            self._保存狀態()
            return True
        except Exception as 異常:
            日誌.紅("停止異常", f"[{服務名稱}] {異常}")
            return False

    def 重啟服務(self, 服務名稱: str) -> bool:
        """重啟指定服務"""
        日誌.綠("重啟服務", f"正在重啟 [{服務名稱}]...")
        self.停止服務(服務名稱)
        time.sleep(1)
        return self.啟動服務(服務名稱)

    # ─────────────────────────────────────────
    # 批量操作
    # ─────────────────────────────────────────
    def 啟動全部服務(self) -> Dict[str, bool]:
        """按依賴順序啟動所有服務"""
        日誌.綠("批量啟動", "開始啟動全部龍魂服務...")
        結果 = {}

        # 拓撲排序：按依賴層級排序
        已排序 = self._拓撲排序服務()

        for 服務名稱 in 已排序:
            成功 = self.啟動服務(服務名稱)
            結果[服務名稱] = 成功
            if not 成功:
                日誌.紅("批量啟動", f"[{服務名稱}] 啟動失敗，後續依賴服務可能受影響")

        成功數 = sum(1 for v in 結果.values() if v)
        日誌.綠("批量啟動", f"完成: {成功數}/{len(結果)} 個服務啟動成功")
        return 結果

    def 停止全部服務(self) -> Dict[str, bool]:
        """停止所有服務（反向順序）"""
        日誌.綠("批量停止", "正在停止全部服務...")
        結果 = {}

        # 反向停止
        for 服務名稱 in reversed(list(self.進程表.keys())):
            結果[服務名稱] = self.停止服務(服務名稱)

        日誌.綠("批量停止", f"完成: {sum(1 for v in 結果.values() if v)}/{len(結果)} 個服務已停止")
        return 結果

    def _拓撲排序服務(self) -> List[str]:
        """拓撲排序服務依賴"""
        入度 = {名稱: 0 for 名稱 in 服務註冊表}
        鄰接表 = {名稱: [] for 名稱 in 服務註冊表}

        for 名稱, 配置 in 服務註冊表.items():
            for 依賴 in 配置.get("依賴服務", []):
                if 依賴 in 服務註冊表:
                    鄰接表[依賴].append(名稱)
                    入度[名稱] += 1

        隊列 = [名稱 for 名稱, 度 in 入度.items() if 度 == 0]
        結果 = []

        while 隊列:
            當前 = 隊列.pop(0)
            結果.append(當前)
            for 鄰居 in 鄰接表[當前]:
                入度[鄰居] -= 1
                if 入度[鄰居] == 0:
                    隊列.append(鄰居)

        return 結果

    # ─────────────────────────────────────────
    # 系統服務安裝 (systemd / launchd)
    # ─────────────────────────────────────────
    def 安裝系統服務(self) -> bool:
        """安裝為系統服務"""
        if self.系統類型 == "linux":
            return self._安裝_systemd()
        elif self.系統類型 == "darwin":
            return self._安裝_launchd()
        else:
            日誌.黃("系統服務", f"不支持的操作系統: {self.系統類型}")
            return False

    def _安裝_systemd(self) -> bool:
        """安裝 systemd 服務 (Linux)"""
        服務文件內容 = f"""[Unit]
Description=龍魂系統守護進程 v5.2
Documentation=https://longhun.dev/docs
After=network.target

[Service]
Type=simple
User={os.environ.get('USER', 'root')}
WorkingDirectory={Path(__file__).parent.parent}
ExecStart={sys.executable} {Path(__file__).parent}/一鍵啟動器.py --daemon
ExecStop={sys.executable} {Path(__file__)}/守護進程管理器.py --stop-all
Restart=on-failure
RestartSec=5
StandardOutput=append:{日誌.運行日誌路徑}
StandardError=append:{日誌.錯誤日誌路徑}
Environment="LONGHUN_DAEMON=1"
Environment="LONGHUN_DNA={龍魂DNA追溯碼}"

[Install]
WantedBy=multi-user.target
"""
        try:
            服務路徑 = Path("/etc/systemd/system/longhun-daemon.service")
            # 使用 sudo 寫入
            臨時文件 = Path("/tmp/longhun-daemon.service")
            with open(臨時文件, "w", encoding="utf-8") as 檔:
                檔.write(服務文件內容)
            subprocess.run(["sudo", "cp", str(臨時文件), str(服務路徑)], check=True)
            subprocess.run(["sudo", "systemctl", "daemon-reload"], check=True)
            subprocess.run(["sudo", "systemctl", "enable", "longhun-daemon"], check=True)
            日誌.綠("systemd", "服務安裝成功: longhun-daemon.service")
            return True
        except Exception as 異常:
            日誌.紅("systemd", f"安裝失敗: {異常}")
            return False

    def _安裝_launchd(self) -> bool:
        """安裝 launchd 服務 (macOS)"""
        plist內容 = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>dev.longhun.daemon</string>
    <key>ProgramArguments</key>
    <array>
        <string>{sys.executable}</string>
        <string>{Path(__file__).parent}/一鍵啟動器.py</string>
        <string>--daemon</string>
    </array>
    <key>WorkingDirectory</key>
    <string>{Path(__file__).parent.parent}</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>LONGHUN_DAEMON</key>
        <string>1</string>
        <key>LONGHUN_DNA</key>
        <string>{龍魂DNA追溯碼}</string>
    </dict>
    <key>StandardOutPath</key>
    <string>{日誌.運行日誌路徑}</string>
    <key>StandardErrorPath</key>
    <string>{日誌.錯誤日誌路徑}</string>
    <key>KeepAlive</key>
    <dict>
        <key>SuccessfulExit</key>
        <false/>
    </dict>
    <key>ThrottleInterval</key>
    <integer>30</integer>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>"""
        try:
            launchd目錄 = Path.home() / "Library/LaunchAgents"
            launchd目錄.mkdir(parents=True, exist_ok=True)
            plist路徑 = launchd目錄 / "dev.longhun.daemon.plist"
            with open(plist路徑, "w", encoding="utf-8") as 檔:
                檔.write(plist內容)
            subprocess.run(["launchctl", "load", str(plist路徑)], check=True)
            日誌.綠("launchd", f"服務安裝成功: {plist路徑}")
            return True
        except Exception as 異常:
            日誌.紅("launchd", f"安裝失敗: {異常}")
            return False

    def 卸載系統服務(self) -> bool:
        """卸載系統服務"""
        try:
            if self.系統類型 == "linux":
                subprocess.run(["sudo", "systemctl", "stop", "longhun-daemon"], check=False)
                subprocess.run(["sudo", "systemctl", "disable", "longhun-daemon"], check=False)
                subprocess.run(["sudo", "rm", "-f", "/etc/systemd/system/longhun-daemon.service"], check=False)
                subprocess.run(["sudo", "systemctl", "daemon-reload"], check=False)
            elif self.系統類型 == "darwin":
                plist路徑 = Path.home() / "Library/LaunchAgents/dev.longhun.daemon.plist"
                subprocess.run(["launchctl", "unload", str(plist路徑)], check=False)
                plist路徑.unlink(missing_ok=True)
            日誌.綠("卸載服務", "系統服務已卸載")
            return True
        except Exception as 異常:
            日誌.紅("卸載服務", f"卸載失敗: {異常}")
            return False

    # ─────────────────────────────────────────
    # 狀態監控
    # ─────────────────────────────────────────
    def 獲取全部狀態(self) -> Dict[str, dict]:
        """獲取所有服務狀態"""
        結果 = {}
        for 服務名稱 in 服務註冊表:
            if 服務名稱 in self.進程表:
                狀態 = self.進程表[服務名稱]
                # 刷新實際進程狀態
                實際狀態 = self.獲取進程狀態(狀態.進程ID)
                if 狀態.狀態 != 實際狀態:
                    狀態.狀態 = 實際狀態
                結果[服務名稱] = {
                    "進程ID": 狀態.進程ID,
                    "狀態": 狀態.狀態,
                    "啟動時間": 狀態.啟動時間,
                    "最後心跳": 狀態.最後心跳,
                    "重試計數": 狀態.重試計數,
                    "總重啟次數": 狀態.總重啟次數,
                    "端口佔用": 狀態.端口佔用,
                }
            else:
                結果[服務名稱] = {"狀態": "未註冊"}
        return 結果

    def 打印狀態看板(self):
        """打印狀態看板"""
        print("\n" + "=" * 80)
        print(f"  🐉 龍魂守護進程狀態看板  |  {龍魂版本號}  |  {datetime.datetime.now().isoformat()}")
        print("=" * 80)
        狀態表 = self.獲取全部狀態()
        for 服務名稱, 狀態 in 狀態表.items():
            狀態圖標 = {
                "運行中": "🟢",
                "已停止": "🔴",
                "未啟動": "⚪",
                "異常": "🟠",
                "重啟中": "🟡",
                "未註冊": "⚫",
            }.get(狀態.get("狀態", "未知"), "❓")
            配置 = 服務註冊表.get(服務名稱, {})
            端口信息 = f":{狀態.get('端口佔用', 配置.get('端口', 0))}" if 配置.get("端口") else ""
            print(f"  {狀態圖標} {服務名稱:<12} {狀態.get('狀態', '未知'):<6} "
                  f"PID={狀態.get('進程ID', 0):<8} {端口信息:<8} "
                  f"重啟={狀態.get('總重啟次數', 0)}次")
        print("=" * 80 + "\n")


# ═══════════════════════════════════════════════════════════════════════════════
# 第四區：命令行接口
# ═══════════════════════════════════════════════════════════════════════════════

def 主函數():
    """命令行入口"""
    解析器 = argparse.ArgumentParser(
        description="龍魂守護進程管理器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 守護進程管理器.py --start-all          啟動全部服務
  python3 守護進程管理器.py --stop 龍魂操作台    停止指定服務
  python3 守護進程管理器.py --restart MCP服務    重啟指定服務
  python3 守護進程管理器.py --status             查看狀態看板
  python3 守護進程管理器.py --install            安裝系統服務
  python3 守護進程管理器.py --uninstall          卸載系統服務
        """
    )
    解析器.add_argument("--start", help="啟動指定服務")
    解析器.add_argument("--stop", help="停止指定服務")
    解析器.add_argument("--restart", help="重啟指定服務")
    解析器.add_argument("--start-all", action="store_true", help="啟動全部服務")
    解析器.add_argument("--stop-all", action="store_true", help="停止全部服務")
    解析器.add_argument("--status", action="store_true", help="查看狀態看板")
    解析器.add_argument("--install", action="store_true", help="安裝為系統服務")
    解析器.add_argument("--uninstall", action="store_true", help="卸載系統服務")
    解析器.add_argument("--daemon", action="store_true", help="守護進程模式")

    參數 = 解析器.parse_args()
    管理器 = 守護進程管理器()

    if 參數.start:
        管理器.啟動服務(參數.start)
    elif 參數.stop:
        管理器.停止服務(參數.stop)
    elif 參數.restart:
        管理器.重啟服務(參數.restart)
    elif 參數.start_all:
        管理器.啟動全部服務()
    elif 參數.stop_all:
        管理器.停止全部服務()
    elif 參數.status:
        管理器.打印狀態看板()
    elif 參數.install:
        管理器.安裝系統服務()
    elif 參數.uninstall:
        管理器.卸載系統服務()
    elif 參數.daemon:
        日誌.綠("守護模式", "進入守護進程循環...")
        管理器.運行中 = True
        while 管理器.運行中:
            try:
                # 定期檢查並恢復
                for 服務名稱 in 服務註冊表:
                    if 服務名稱 not in 管理器.進程表:
                        continue
                    狀態 = 管理器.進程表[服務名稱]
                    配置 = 服務註冊表[服務名稱]
                    if 配置.get("自動重啟") and 狀態.狀態 != "運行中":
                        if 狀態.重試計數 < 配置.get("最大重試次數", 3):
                            日誌.黃("自恢復", f"[{服務名稱}] 檢測到異常，自動重啟 (第{狀態.重試計數 + 1}次)")
                            管理器.重啟服務(服務名稱)
                            管理器.進程表[服務名稱].重試計數 += 1
                            管理器.進程表[服務名稱].總重啟次數 += 1
                        else:
                            日誌.紅("自恢復", f"[{服務名稱}] 重試次數超限，停止自動恢復")
                time.sleep(10)
            except KeyboardInterrupt:
                日誌.綠("守護模式", "收到退出信號")
                管理器.運行中 = False
            except Exception as 異常:
                日誌.紅("守護循環", f"異常: {異常}")
                time.sleep(30)
    else:
        管理器.打印狀態看板()


if __name__ == "__main__":
    主函數()
