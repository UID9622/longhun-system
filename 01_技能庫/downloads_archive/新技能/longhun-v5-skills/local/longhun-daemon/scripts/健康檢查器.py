#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
【龍魂健康檢查器】
================================================================================
· 功能：定時檢查各服務健康狀態，崩潰時自動重啟
· 架構：心跳探測 → 閾值判定 → 自恢復策略
· 規範：CNSH中文編程規範 v5.2
· 君子協議：未經授權不得修改健康閾值
================================================================================
· DNA: #龍芯⚡️2026-06-19-LONGHUN-DAEMON-v5.2
================================================================================
"""

import os
import sys
import json
import time
import socket
import signal
import hashlib
import argparse
import datetime
import subprocess
import threading
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict

# ═══════════════════════════════════════════════════════════════════════════════
# 第一區：DNA追溯與全域常數
# ═══════════════════════════════════════════════════════════════════════════════
龍魂DNA追溯碼 = "#龍芯⚡️2026-06-19-LONGHUN-DAEMON-v5.2"
龍魂版本號 = "v5.2.0"

# 三色審計級別
審計級別_紅 = "紅"
審計級別_黃 = "黃"
審計級別_綠 = "綠"

# 健康閾值配置
健康閾值 = {
    "心跳間隔秒": 30,
    "心跳超時秒": 10,
    "連續失敗閾值": 3,
    "重啟冷卻秒": 60,
    "最大重啟次數": 5,
    "內存告警MB": 512,
    "內存致命MB": 1024,
    "CPU告警百分比": 80,
    "CPU致命百分比": 95,
    "磁盤告警百分比": 85,
    "磁盤致命百分比": 95,
}

# ═══════════════════════════════════════════════════════════════════════════════
# 第二區：審計日誌
# ═══════════════════════════════════════════════════════════════════════════════

class 審計日誌器:
    """三色審計日誌系統"""

    def __init__(self, 日誌目錄: str = ""):
        if not 日誌目錄:
            日誌目錄 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
        self.日誌目錄 = Path(日誌目錄).resolve()
        self.日誌目錄.mkdir(parents=True, exist_ok=True)
        self.日誌文件路徑 = self.日誌目錄 / f"health_audit_{datetime.date.today().isoformat()}.log"
        self.運行日誌路徑 = self.日誌目錄 / "launchd.out.log"
        self.錯誤日誌路徑 = self.日誌目錄 / "launchd.err.log"

    def 記錄(self, 級別: str, 模塊: str, 訊息: str, 元數據: dict = None):
        時間戳 = datetime.datetime.now().isoformat()
        龍印 = hashlib.sha256(f"{時間戳}{模塊}{訊息}{龍魂DNA追溯碼}".encode()).hexdigest()[:12]
        記錄行 = f"[{時間戳}] [龍印:{龍印}] [{級別}] [健康檢查器][{模塊}] {訊息}"
        if 元數據:
            記錄行 += f" | 元數據:{json.dumps(元數據, ensure_ascii=False)}"
        記錄行 += f" | DNA:{龍魂DNA追溯碼}\n"
        try:
            with open(self.日誌文件路徑, "a", encoding="utf-8") as 檔:
                檔.write(記錄行)
        except Exception:
            pass
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


日誌 = 審計日誌器()


# ═══════════════════════════════════════════════════════════════════════════════
# 第三區：健康數據結構
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class 健康指標:
    """單個服務的健康指標"""
    服務名稱: str = ""
    進程ID: int = 0
    狀態: str = "未知"           # 健康/警告/危險/離線/重啟中
    最後心跳: str = ""
    連續失敗: int = 0
    總檢查次數: int = 0
    總失敗次數: int = 0
    響應時間毫秒: float = 0.0
    內存使用MB: float = 0.0
    CPU使用率: float = 0.0
    端口可達: bool = False
    進程存活: bool = False
    重啟次數: int = 0
    最後重啟時間: str = ""
    告警列表: List[str] = field(default_factory=list)


@dataclass
class 系統健康:
    """系統整體健康狀態"""
    檢查時間: str = ""
    系統狀態: str = "未知"       # 健康/警告/危險
    服務指標: Dict[str, 健康指標] = field(default_factory=dict)
    磁盤使用百分比: float = 0.0
    系統負載: float = 0.0
    總內存MB: float = 0.0
    可用內存MB: float = 0.0


# ═══════════════════════════════════════════════════════════════════════════════
# 第四區：健康檢查核心
# ═══════════════════════════════════════════════════════════════════════════════

class 健康檢查器:
    """
    龍魂健康檢查器
    · 定時心跳檢測所有服務
    · 自動判定健康狀態（綠/黃/紅）
    · 自恢復：崩潰時自動重啟
    · 支持日誌輪轉
    """

    def __init__(self):
        self.運行中 = False
        self.服務指標表: Dict[str, 健康指標] = {}
        self.系統指標 = 系統健康()
        self.檢查間隔秒 = 健康閾值["心跳間隔秒"]
        self.腳本目錄 = Path(__file__).parent
        self.鎖 = threading.Lock()

    def 檢測進程存活(self, 進程ID: int) -> bool:
        """檢查進程是否存活"""
        if 進程ID <= 0:
            return False
        try:
            os.kill(進程ID, 0)
            return True
        except (OSError, ProcessLookupError):
            return False

    def 檢測端口可達(self, 主機: str, 端口: int, 超時: int = 5) -> Tuple[bool, float]:
        """檢測端口是否可達，返回 (是否可達, 響應時間毫秒)"""
        if 端口 <= 0:
            return True, 0.0
        開始 = time.time()
        try:
            with socket.create_connection((主機, 端口), timeout=超時):
                耗時 = (time.time() - 開始) * 1000
                return True, 耗時
        except Exception:
            return False, (time.time() - 開始) * 1000

    def 獲取進程資源使用(self, 進程ID: int) -> Tuple[float, float]:
        """獲取進程的內存(MB)和CPU(%)使用"""
        try:
            # 使用 ps 命令獲取資源使用
            結果 = subprocess.run(
                ["ps", "-p", str(進程ID), "-o", "rss=,pcpu="],
                capture_output=True, text=True, timeout=5
            )
            if 結果.returncode == 0:
                行 = 結果.stdout.strip().split()
                if len(行) >= 2:
                    內存KB = int(行[0])
                    CPU = float(行[1])
                    return 內存KB / 1024, CPU
        except Exception:
            pass
        return 0.0, 0.0

    def 獲取系統資源(self) -> dict:
        """獲取系統級資源信息"""
        結果 = {"磁盤使用百分比": 0.0, "系統負載": 0.0, "總內存MB": 0.0, "可用內存MB": 0.0}
        try:
            # 磁盤使用
            磁盤統計 = os.statvfs(self.腳本目錄)
            總空間 = 磁盤統計.f_blocks * 磁盤統計.f_frsize
            可用空間 = 磁盤統計.f_bavail * 磁盤統計.f_frsize
            結果["磁盤使用百分比"] = (1 - 可用空間 / 總空間) * 100

            # 系統負載 (Linux/macOS)
            try:
                結果["系統負載"] = os.getloadavg()[0]
            except AttributeError:
                pass

            # 內存 (Linux)
            try:
                with open("/proc/meminfo", "r") as 檔:
                    內存信息 = 檔.read()
                for 行 in 內存信息.split("\n"):
                    if 行.startswith("MemTotal:"):
                        結果["總內存MB"] = int(行.split()[1]) / 1024
                    elif 行.startswith("MemAvailable:"):
                        結果["可用內存MB"] = int(行.split()[1]) / 1024
            except Exception:
                pass

        except Exception as 異常:
            日誌.黃("系統資源", f"獲取失敗: {異常}")

        return 結果

    def 檢查單個服務(self, 服務名稱: str, 配置: dict) -> 健康指標:
        """檢查單個服務的健康狀態"""
        指標 = 健康指標(服務名稱=服務名稱)
        指標.總檢查次數 += 1
        現在 = datetime.datetime.now()

        # 獲取進程ID
        進程ID = 0
        狀態文件 = self.腳本目錄.parent / "config" / "daemon_state.json"
        try:
            if 狀態文件.exists():
                with open(狀態文件, "r") as 檔:
                    狀態數據 = json.load(檔)
                if 服務名稱 in 狀態數據:
                    進程ID = 狀態數據[服務名稱].get("進程ID", 0)
        except Exception:
            pass

        指標.進程ID = 進程ID

        # 檢查進程存活
        指標.進程存活 = self.檢測進程存活(進程ID)

        # 檢查端口可達
        端口 = 配置.get("端口", 0)
        if 端口 > 0:
            指標.端口可達, 指標.響應時間毫秒 = self.檢測端口可達("127.0.0.1", 端口)
        else:
            指標.端口可達 = True  # 無端口服務默認可達

        # 獲取資源使用
        if 指標.進程存活 and 進程ID > 0:
            指標.內存使用MB, 指標.CPU使用率 = self.獲取進程資源使用(進程ID)

        # 判定狀態
        指標.最後心跳 = 現在.isoformat()
        告警列表 = []

        if not 指標.進程存活 and 端口 > 0:
            告警列表.append("進程未存活")
            指標.連續失敗 += 1
        elif not 指標.端口可達 and 端口 > 0:
            告警列表.append("端口不可達")
            指標.連續失敗 += 1
        else:
            指標.連續失敗 = 0

        if 指標.內存使用MB > 健康閾值["內存致命MB"]:
            告警列表.append(f"內存使用超標: {指標.內存使用MB:.1f}MB")
        elif 指標.內存使用MB > 健康閾值["內存告警MB"]:
            告警列表.append(f"內存使用偏高: {指標.內存使用MB:.1f}MB")

        if 指標.CPU使用率 > 健康閾值["CPU致命百分比"]:
            告警列表.append(f"CPU使用超標: {指標.CPU使用率:.1f}%")
        elif 指標.CPU使用率 > 健康閾值["CPU告警百分比"]:
            告警列表.append(f"CPU使用偏高: {指標.CPU使用率:.1f}%")

        指標.告警列表 = 告警列表
        指標.總失敗次數 += 1 if 指標.連續失敗 > 0 else 0

        # 狀態判定
        if 指標.連續失敗 >= 健康閾值["連續失敗閾值"]:
            指標.狀態 = "危險"
        elif 指標.連續失敗 > 0 or len(告警列表) > 1:
            指標.狀態 = "警告"
        elif len(告警列表) == 1:
            指標.狀態 = "警告"
        else:
            指標.狀態 = "健康"

        return 指標

    def 執行自恢復(self, 服務名稱: str, 指標: 健康指標) -> bool:
        """執行自恢復策略"""
        日誌.紅("自恢復", f"[{服務名稱}] 觸發自恢復策略...")

        # 檢查重啟次數
        if 指標.重啟次數 >= 健康閾值["最大重啟次數"]:
            日誌.紅("自恢復", f"[{服務名稱}] 重啟次數已達上限 ({指標.重啟次數}/{健康閾值['最大重啟次數']})")
            return False

        # 檢查冷卻時間
        if 指標.最後重啟時間:
            最後重啟 = datetime.datetime.fromisoformat(指標.最後重啟時間)
            經過秒 = (datetime.datetime.now() - 最後重啟).total_seconds()
            if 經過秒 < 健康閾值["重啟冷卻秒"]:
                日誌.黃("自恢復", f"[{服務名稱}] 冷卻中，還需 {健康閾值['重啟冷卻秒'] - 經過秒:.0f} 秒")
                return False

        # 調用守護進程管理器重啟
        try:
            管理器路徑 = self.腳本目錄 / "守護進程管理器.py"
            if 管理器路徑.exists():
                結果 = subprocess.run(
                    [sys.executable, str(管理器路徑), "--restart", 服務名稱],
                    capture_output=True, text=True, timeout=60
                )
                if 結果.returncode == 0:
                    指標.重啟次數 += 1
                    指標.最後重啟時間 = datetime.datetime.now().isoformat()
                    指標.連續失敗 = 0
                    日誌.綠("自恢復", f"[{服務名稱}] 重啟成功 (第 {指標.重啟次數} 次)")
                    return True
                else:
                    日誌.紅("自恢復", f"[{服務名稱}] 重啟失敗: {結果.stderr}")
                    return False
        except Exception as 異常:
            日誌.紅("自恢復", f"[{服務名稱}] 異常: {異常}")
            return False

    def 執行全面檢查(self) -> 系統健康:
        """執行一次全面的健康檢查"""
        日誌.綠("健康檢查", f"{'='*50}")
        日誌.綠("健康檢查", f"開始全面健康檢查... {datetime.datetime.now().isoformat()}")

        系統指標 = 系統健康()
        系統指標.檢查時間 = datetime.datetime.now().isoformat()

        # 系統資源
        系統資源 = self.獲取系統資源()
        系統指標.磁盤使用百分比 = 系統資源.get("磁盤使用百分比", 0)
        系統指標.系統負載 = 系統資源.get("系統負載", 0)
        系統指標.總內存MB = 系統資源.get("總內存MB", 0)
        系統指標.可用內存MB = 系統資源.get("可用內存MB", 0)

        # 磁盤告警
        if 系統指標.磁盤使用百分比 > 健康閾值["磁盤致命百分比"]:
            日誌.紅("系統資源", f"磁盤使用嚴重超標: {系統指標.磁盤使用百分比:.1f}%")
        elif 系統指標.磁盤使用百分比 > 健康閾值["磁盤告警百分比"]:
            日誌.黃("系統資源", f"磁盤使用偏高: {系統指標.磁盤使用百分比:.1f}%")

        # 服務檢查
        服務配置表 = {
            "龍魂操作台": {"端口": 8443},
            "MCP服務": {"端口": 8443},
            "Kimi集成": {"端口": 8443},
            "Notion同步": {"端口": 0},
            "自動化評估": {"端口": 0},
            "復盤引擎": {"端口": 0},
        }

        危險數 = 0
        警告數 = 0
        健康數 = 0

        for 服務名稱, 配置 in 服務配置表.items():
            # 獲取或創建指標
            if 服務名稱 not in self.服務指標表:
                self.服務指標表[服務名稱] = 健康指標(服務名稱=服務名稱)

            # 繼承之前的重啟計數
            之前重啟 = self.服務指標表[服務名稱].重啟次數
            之前重啟時間 = self.服務指標表[服務名稱].最後重啟時間

            指標 = self.檢查單個服務(服務名稱, 配置)
            指標.重啟次數 = 之前重啟
            指標.最後重啟時間 = 之前重啟時間

            self.服務指標表[服務名稱] = 指標
            系統指標.服務指標[服務名稱] = 指標

            # 自恢復
            if 指標.狀態 == "危險":
                危險數 += 1
                日誌.紅("服務檢查", f"[{服務名稱}] 狀態: {指標.狀態} | "
                       f"進程:{指標.進程存活} 端口:{指標.端口可達} | "
                       f"記憶體:{指標.內存使用MB:.1f}MB CPU:{指標.CPU使用率:.1f}%")
                self.執行自恢復(服務名稱, 指標)
            elif 指標.狀態 == "警告":
                警告數 += 1
                日誌.黃("服務檢查", f"[{服務名稱}] 狀態: {指標.狀態} | "
                       f"連續失敗:{指標.連續失敗} | 告警: {', '.join(指標.告警列表)}")
            else:
                健康數 += 1
                日誌.綠("服務檢查", f"[{服務名稱}] 狀態: {指標.狀態} | "
                       f"PID={指標.進程ID} 記憶體:{指標.內存使用MB:.1f}MB")

        # 系統狀態判定
        if 危險數 > 0:
            系統指標.系統狀態 = "危險"
        elif 警告數 > 0:
            系統指標.系統狀態 = "警告"
        else:
            系統指標.系統狀態 = "健康"

        日誌.綠("健康檢查", f"檢查完成: 🟢{健康數} 🟡{警告數} 🔴{危險數} | 系統狀態: {系統指標.系統狀態}")
        self.系統指標 = 系統指標

        # 保存健康報告
        self._保存健康報告(系統指標)

        return 系統指標

    def _保存健康報告(self, 系統指標: 系統健康):
        """保存健康檢查報告"""
        try:
            報告路徑 = self.腳本目錄.parent / "logs" / "health_report.json"
            數據 = {
                "檢查時間": 系統指標.檢查時間,
                "系統狀態": 系統指標.系統狀態,
                "磁盤使用百分比": round(系統指標.磁盤使用百分比, 2),
                "系統負載": round(系統指標.系統負載, 2),
                "總內存MB": round(系統指標.總內存MB, 2),
                "可用內存MB": round(系統指標.可用內存MB, 2),
                "服務": {}
            }
            for 名稱, 指標 in 系統指標.服務指標.items():
                數據["服務"][名稱] = {
                    "狀態": 指標.狀態,
                    "進程ID": 指標.進程ID,
                    "進程存活": 指標.進程存活,
                    "端口可達": 指標.端口可達,
                    "響應時間毫秒": round(指標.響應時間毫秒, 2),
                    "內存使用MB": round(指標.內存使用MB, 2),
                    "CPU使用率": round(指標.CPU使用率, 2),
                    "連續失敗": 指標.連續失敗,
                    "重啟次數": 指標.重啟次數,
                    "告警": 指標.告警列表,
                }
            with open(報告路徑, "w", encoding="utf-8") as 檔:
                json.dump(數據, 檔, ensure_ascii=False, indent=2)
        except Exception as 異常:
            日誌.黃("報告保存", f"失敗: {異常}")

    def 打印健康看板(self):
        """打印健康狀態看板"""
        系統 = self.系統指標
        if not 系統.檢查時間:
            self.執行全面檢查()
            系統 = self.系統指標

        print("\n" + "=" * 70)
        狀態圖標 = {"健康": "🟢", "警告": "🟡", "危險": "🔴"}
        print(f"  {狀態圖標.get(系統.系統狀態, '⚪')} 龍魂健康狀態看板  |  {系統.系統狀態}  |  {系統.檢查時間}")
        print("-" * 70)
        print(f"  系統負載: {系統.系統負載:.2f}  |  "
              f"磁盤: {系統.磁盤使用百分比:.1f}%  |  "
              f"記憶體: {系統.可用內存MB:.0f}/{系統.總內存MB:.0f}MB")
        print("-" * 70)

        for 服務名稱, 指標 in 系統.服務指標.items():
            圖標 = {"健康": "🟢", "警告": "🟡", "危險": "🔴", "離線": "⚫", "重啟中": "🟠"}
            print(f"  {圖標.get(指標.狀態, '❓')} {服務名稱:<12} "
                  f"{指標.狀態:<6} PID={指標.進程ID:<8} "
                  f"MEM={指標.內存使用MB:>7.1f}MB CPU={指標.CPU使用率:>5.1f}% "
                  f"RT={指標.響應時間毫秒:>6.1f}ms")
            if 指標.告警列表:
                for 告警 in 指標.告警列表:
                    print(f"     ⚠️ {告警}")

        print("=" * 70 + "\n")

    def 啟動定時檢查(self):
        """啟動定時健康檢查循環"""
        self.運行中 = True
        日誌.綠("定時檢查", f"健康檢查器已啟動，檢查間隔: {self.檢查間隔秒}秒")

        while self.運行中:
            try:
                self.執行全面檢查()
                # 等待下一次檢查（可中斷）
                for _ in range(self.檢查間隔秒):
                    if not self.運行中:
                        break
                    time.sleep(1)
            except KeyboardInterrupt:
                日誌.綠("定時檢查", "收到中斷信號，正在停止...")
                self.運行中 = False
            except Exception as 異常:
                日誌.紅("定時檢查", f"異常: {異常}")
                time.sleep(self.檢查間隔秒)

        日誌.綠("定時檢查", "健康檢查器已停止")


# ═══════════════════════════════════════════════════════════════════════════════
# 第五區：日誌輪轉
# ═══════════════════════════════════════════════════════════════════════════════

class 日誌輪轉器:
    """日誌輪轉管理器"""

    def __init__(self, 日誌目錄: str = ""):
        if not 日誌目錄:
            日誌目錄 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
        self.日誌目錄 = Path(日誌目錄).resolve()
        self.最大保留天數 = 30
        self.單文件最大MB = 100

    def 輪轉日誌(self):
        """執行日誌輪轉"""
        日誌.綠("日誌輪轉", "開始執行日誌輪轉...")
        清理數 = 0

        if not self.日誌目錄.exists():
            return

        截止時間 = datetime.datetime.now() - datetime.timedelta(days=self.最大保留天數)

        for 文件路徑 in self.日誌目錄.iterdir():
            if not 文件路徑.is_file():
                continue

            try:
                # 檢查文件修改時間
                修改時間 = datetime.datetime.fromtimestamp(文件路徑.stat().st_mtime)
                if 修改時間 < 截止時間:
                    文件路徑.unlink()
                    清理數 += 1
                    continue

                # 檢查文件大小
                大小MB = 文件路徑.stat().st_size / (1024 * 1024)
                if 大小MB > self.單文件最大MB:
                    # 壓縮或拆分大文件
                    self._壓縮日誌(文件路徑)
                    清理數 += 1

            except Exception as 異常:
                日誌.黃("日誌輪轉", f"處理 {文件路徑.name} 失敗: {異常}")

        日誌.綠("日誌輪轉", f"完成: 處理了 {清理數} 個文件")

    def _壓縮日誌(self, 文件路徑: Path):
        """壓縮大日誌文件"""
        try:
            import gzip
            壓縮路徑 = Path(str(文件路徑) + ".gz")
            with open(文件路徑, "rb") as 源文件:
                with gzip.open(壓縮路徑, "wb") as 壓縮文件:
                    壓縮文件.write(源文件.read())
            文件路徑.unlink()
            日誌.綠("日誌壓縮", f"已壓縮: {文件路徑.name} → {壓縮路徑.name}")
        except Exception as 異常:
            日誌.黃("日誌壓縮", f"壓縮失敗: {異常}")


# ═══════════════════════════════════════════════════════════════════════════════
# 第六區：命令行接口
# ═══════════════════════════════════════════════════════════════════════════════

def 主函數():
    解析器 = argparse.ArgumentParser(
        description="龍魂健康檢查器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 健康檢查器.py              執行一次全面檢查
  python3 健康檢查器.py --daemon     定時檢查模式
  python3 健康檢查器.py --dashboard  顯示狀態看板
  python3 健康檢查器.py --rotate     執行日誌輪轉
  python3 健康檢查器.py --check 龍魂操作台  檢查指定服務
        """
    )
    解析器.add_argument("--daemon", action="store_true", help="定時檢查模式")
    解析器.add_argument("--dashboard", action="store_true", help="顯示狀態看板")
    解析器.add_argument("--rotate", action="store_true", help="日誌輪轉")
    解析器.add_argument("--check", help="檢查指定服務")
    解析器.add_argument("--interval", type=int, default=30, help="檢查間隔秒數")

    參數 = 解析器.parse_args()

    if 參數.rotate:
        輪轉器 = 日誌輪轉器()
        輪轉器.輪轉日誌()
    elif 參數.dashboard:
        檢查器 = 健康檢查器()
        檢查器.打印健康看板()
    elif 參數.check:
        檢查器 = 健康檢查器()
        服務配置表 = {
            "龍魂操作台": {"端口": 8443},
            "MCP服務": {"端口": 8443},
            "Kimi集成": {"端口": 8443},
            "Notion同步": {"端口": 0},
            "自動化評估": {"端口": 0},
            "復盤引擎": {"端口": 0},
        }
        if 參數.check in 服務配置表:
            指標 = 檢查器.檢查單個服務(參數.check, 服務配置表[參數.check])
            print(f"\n  服務: {指標.服務名稱}")
            print(f"  狀態: {指標.狀態}")
            print(f"  PID: {指標.進程ID}")
            print(f"  進程存活: {指標.進程存活}")
            print(f"  端口可達: {指標.端口可達}")
            print(f"  響應時間: {指標.響應時間毫秒:.1f}ms")
            print(f"  內存: {指標.內存使用MB:.1f}MB")
            print(f"  CPU: {指標.CPU使用率:.1f}%")
            if 指標.告警列表:
                print(f"  告警: {', '.join(指標.告警列表)}")
        else:
            print(f"未知服務: {參數.check}")
            sys.exit(1)
    elif 參數.daemon:
        檢查器 = 健康檢查器()
        檢查器.檢查間隔秒 = 參數.interval
        檢查器.啟動定時檢查()
    else:
        # 默認：執行一次全面檢查
        檢查器 = 健康檢查器()
        檢查器.執行全面檢查()
        檢查器.打印健康看板()


if __name__ == "__main__":
    主函數()
