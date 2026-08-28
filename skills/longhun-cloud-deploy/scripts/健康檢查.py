#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
"""
═══════════════════════════════════════════════════════════════════════════════
                    龍魂健康檢查系統 v5.0
═══════════════════════════════════════════════════════════════════════════════
DNA          : #龍芯⚡️2026-06-19-LONGHUN-DEPLOY-v5.0
功能         : 多維度健康檢測 / HTTP探針 / 數據庫檢測 / 緩存檢測 / 外部依賴
作者         : 龍魂体系-技能打包专家
协议         : 君子協議 — 非惡意、非濫用、可審計
三色審計     : 🟢 安全通過 / 🟡 警告需審 / 🔴 阻塞風險
═══════════════════════════════════════════════════════════════════════════════
"""

import os
import sys
import json
import time
import logging
import requests
import subprocess
from datetime import datetime, timezone
from enum import Enum
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Callable, Any, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed

# 全局常數
DNA標識 = "#龍芯⚡️2026-06-19-LONGHUN-DEPLOY-v5.0"
安全通過 = "🟢"
警告需審 = "🟡"
阻塞風險 = "🔴"
龍印標記 = "🐉"


class 健康等級(Enum):
    健康 = "healthy"
    亞健康 = "degraded"
    不健康 = "unhealthy"
    未知 = "unknown"


@dataclass
class 檢查結果:
    檢查名稱: str = ""
    健康等級: 健康等級 = 健康等級.未知
    響應時間毫秒: float = 0.0
    HTTP狀態碼: int = 0
    檢查時間: str = ""
    錯誤信息: str = ""
    詳細數據: Dict = field(default_factory=dict)
    DNA追溯: str = DNA標識

    def to_dict(self) -> Dict:
        return {
            "檢查名稱": self.檢查名稱,
            "健康等級": self.健康等級.value,
            "響應時間毫秒": round(self.響應時間毫秒, 2),
            "HTTP狀態碼": self.HTTP狀態碼,
            "檢查時間": self.檢查時間,
            "錯誤信息": self.錯誤信息,
            "詳細數據": self.詳細數據,
            "DNA": self.DNA追溯
        }


@dataclass
class 健康報告:
    報告ID: str = ""
    總體狀態: 健康等級 = 健康等級.未知
    檢查項總數: int = 0
    通過數: int = 0
    警告數: int = 0
    失敗數: int = 0
    總響應時間: float = 0.0
    檢查結果列表: List[Dict] = field(default_factory=list)
    生成時間: str = ""
    DNA追溯: str = DNA標識


class 健康檢查器:
    """
    龍魂健康檢查器 — 支持多種檢查類型
    - HTTP端點健康檢查
    - 數據庫連接檢查
    - 緩存服務檢查
    - 外部依賴檢查
    - 自定義檢查腳本
    """

    def __init__(self, 基礎URL: str = "", 超時秒: int = 10, 並發數: int = 5):
        self.基礎URL = 基礎URL
        self.超時秒 = 超時秒
        self.並發數 = 並發數
        self.檢查註冊表: Dict[str, Callable] = {}
        self.檢查歷史: List[Dict] = []
        self._初始化日誌()
        self._註冊內置檢查()

    def _初始化日誌(self):
        logging.basicConfig(
            level=logging.INFO,
            format=f'{龍印標記} [%(asctime)s] %(levelname)s — %(message)s'
        )
        self.日誌 = logging.getLogger("健康檢查")

    def _註冊內置檢查(self):
        """註冊內置健康檢查項"""
        self.註冊檢查("http服務", self._檢查HTTP服務)
        self.註冊檢查("數據庫連接", self._檢查數據庫)
        self.註冊檢查("緩存服務", self._檢查緩存)
        self.註冊檢查("磁盤空間", self._檢查磁盤空間)
        self.註冊檢查("內存使用", self._檢查內存使用)
        self.註冊檢查("CPU負載", self._檢查CPU負載)

    def 註冊檢查(self, 名稱: str, 檢查函數: Callable):
        """註冊自定義健康檢查"""
        self.檢查註冊表[名稱] = 檢查函數
        self.日誌.info(f"{安全通過} 已註冊檢查項: {名稱}")

    def 執行全部檢查(self) -> 健康報告:
        """並行執行所有註冊的健康檢查"""
        self.日誌.info(f"{龍印標記} 開始全面健康檢查，共 {len(self.檢查註冊表)} 項")
        開始時間 = time.time()

        報告 = 健康報告(
            報告ID=f"HL-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
            檢查項總數=len(self.檢查註冊表),
            生成時間=datetime.now(timezone.utc).isoformat(),
            DNA追溯=DNA標識
        )

        結果列表: List[檢查結果] = []

        with ThreadPoolExecutor(max_workers=self.並發數) as 執行器:
            未來任務 = {
                執行器.submit(檢查函數, 名稱): 名稱
                for 名稱, 檢查函數 in self.檢查註冊表.items()
            }

            for 未來 in as_completed(未來任務):
                名稱 = 未來任務[未來]
                try:
                    結果 = 未來.result()
                    結果.檢查名稱 = 名稱
                    結果列表.append(結果)

                    if 結果.健康等級 == 健康等級.健康:
                        報告.通過數 += 1
                    elif 結果.健康等級 == 健康等級.亞健康:
                        報告.警告數 += 1
                    else:
                        報告.失敗數 += 1

                except Exception as 異常:
                    self.日誌.error(f"{阻塞風險} 檢查項 '{名稱}' 異常: {異常}")
                    結果列表.append(檢查結果(
                        檢查名稱=名稱,
                        健康等級=健康等級.不健康,
                        錯誤信息=str(異常),
                        檢查時間=datetime.now(timezone.utc).isoformat()
                    ))
                    報告.失敗數 += 1

        # 計算總體狀態
        報告.總響應時間 = (time.time() - 開始時間) * 1000
        報告.檢查結果列表 = [r.to_dict() for r in 結果列表]

        if 報告.失敗數 > 0:
            報告.總體狀態 = 健康等級.不健康
        elif 報告.警告數 > 0:
            報告.總體狀態 = 健康等級.亞健康
        else:
            報告.總體狀態 = 健康等級.健康

        self.檢查歷史.append(asdict(報告))
        self._輸出報告摘要(報告)

        return 報告

    def _輸出報告摘要(self, 報告: 健康報告):
        """輸出報告摘要"""
        狀態標記 = {
            健康等級.健康: 安全通過,
            健康等級.亞健康: 警告需審,
            健康等級.不健康: 阻塞風險
        }.get(報告.總體狀態, "⚪")

        self.日誌.info(f"{'='*50}")
        self.日誌.info(f"{狀態標記} 健康檢查報告: {報告.總體狀態.value}")
        self.日誌.info(f"  通過: {報告.通過數} / 警告: {報告.警告數} / 失敗: {報告.失敗數}")
        self.日誌.info(f"  總響應時間: {報告.總響應時間:.2f}ms")
        self.日誌.info(f"  報告ID: {報告.報告ID}")
        self.日誌.info(f"{'='*50}")

    # ═══════════════════════════════════════════════════════════════════════════
    # 內置檢查實現
    # ═══════════════════════════════════════════════════════════════════════════

    def _檢查HTTP服務(self, 名稱: str) -> 檢查結果:
        """檢查HTTP服務健康端點"""
        開始 = time.time()
        URL = f"{self.基礎URL}/health"

        try:
            響應 = requests.get(URL, timeout=self.超時秒, verify=False)
            耗時 = (time.time() - 開始) * 1000

            if 響應.status_code == 200:
                return 檢查結果(
                    健康等級=健康等級.健康,
                    響應時間毫秒=耗時,
                    HTTP狀態碼=響應.status_code,
                    檢查時間=datetime.now(timezone.utc).isoformat(),
                    詳細數據={"響應內容": 響應.text[:200]}
                )
            else:
                return 檢查結果(
                    健康等級=健康等級.亞健康,
                    響應時間毫秒=耗時,
                    HTTP狀態碼=響應.status_code,
                    檢查時間=datetime.now(timezone.utc).isoformat(),
                    錯誤信息=f"HTTP {響應.status_code}"
                )
        except requests.RequestException as 異常:
            return 檢查結果(
                健康等級=健康等級.不健康,
                錯誤信息=str(異常),
                檢查時間=datetime.now(timezone.utc).isoformat()
            )

    def _檢查數據庫(self, 名稱: str) -> 檢查結果:
        """檢查數據庫連接"""
        開始 = time.time()

        try:
            # 通過HTTP端點檢查數據庫狀態
            URL = f"{self.基礎URL}/health/db"
            響應 = requests.get(URL, timeout=self.超時秒, verify=False)
            耗時 = (time.time() - 開始) * 1000

            if 響應.status_code == 200:
                return 檢查結果(
                    健康等級=健康等級.健康,
                    響應時間毫秒=耗時,
                    HTTP狀態碼=響應.status_code,
                    檢查時間=datetime.now(timezone.utc).isoformat(),
                    詳細數據=json.loads(響應.text) if 響應.text else {}
                )
            else:
                return 檢查結果(
                    健康等級=健康等級.不健康,
                    響應時間毫秒=耗時,
                    HTTP狀態碼=響應.status_code,
                    檢查時間=datetime.now(timezone.utc).isoformat(),
                    錯誤信息="數據庫連接異常"
                )
        except Exception as 異常:
            return 檢查結果(
                健康等級=健康等級.未知,
                錯誤信息=str(異常),
                檢查時間=datetime.now(timezone.utc).isoformat()
            )

    def _檢查緩存(self, 名稱: str) -> 檢查結果:
        """檢查緩存服務狀態"""
        開始 = time.time()

        try:
            URL = f"{self.基礎URL}/health/cache"
            響應 = requests.get(URL, timeout=self.超時秒, verify=False)
            耗時 = (time.time() - 開始) * 1000

            return 檢查結果(
                健康等級=健康等級.健康 if 響應.status_code == 200 else 健康等級.亞健康,
                響應時間毫秒=耗時,
                HTTP狀態碼=響應.status_code,
                檢查時間=datetime.now(timezone.utc).isoformat()
            )
        except Exception as 異常:
            return 檢查結果(
                健康等級=健康等級.未知,
                錯誤信息=str(異常),
                檢查時間=datetime.now(timezone.utc).isoformat()
            )

    def _檢查磁盤空間(self, 名稱: str) -> 檢查結果:
        """檢查磁盤空間使用情況"""
        try:
            結果 = subprocess.run(
                ["df", "-h", "/"],
                capture_output=True, text=True, timeout=5
            )
            輸出行 = 結果.stdout.strip().split("\n")
            if len(輸出行) >= 2:
                數據行 = 輸入行[1].split()
                使用百分比 = int(數據行[4].replace("%", ""))

                等級 = 健康等級.健康
                if 使用百分比 > 90:
                    等級 = 健康等級.不健康
                elif 使用百分比 > 75:
                    等級 = 健康等級.亞健康

                return 檢查結果(
                    健康等級=等級,
                    檢查時間=datetime.now(timezone.utc).isoformat(),
                    詳細數據={
                        "使用百分比": 使用百分比,
                        "可用空間": 數據行[3] if len(數據行) > 3 else "未知"
                    }
                )
        except Exception as 異常:
            return 檢查結果(
                健康等級=健康等級.未知,
                錯誤信息=str(異常),
                檢查時間=datetime.now(timezone.utc).isoformat()
            )

        return 檢查結果(健康等級=健康等級.未知)

    def _檢查內存使用(self, 名稱: str) -> 檢查結果:
        """檢查內存使用情況"""
        try:
            with open("/proc/meminfo", "r") as 文件:
                行列表 = 文件.readlines()

            內存信息 = {}
            for 行 in 行列表[:5]:
                鍵值 = 行.split(":")
                if len(鍵值) == 2:
                    內存信息[鍵值[0].strip()] = 鍵值[1].strip()

            總內存 = int(內存信息.get("MemTotal", "0 kB").split()[0])
            可用內存 = int(內存信息.get("MemAvailable", "0 kB").split()[0])
            使用百分比 = (1 - 可用內存 / 總內存) * 100 if 總內存 > 0 else 0

            等級 = 健康等級.健康
            if 使用百分比 > 90:
                等級 = 健康等級.不健康
            elif 使用百分比 > 80:
                等級 = 健康等級.亞健康

            return 檢查結果(
                健康等級=等級,
                檢查時間=datetime.now(timezone.utc).isoformat(),
                詳細數據={
                    "總內存KB": 總內存,
                    "可用內存KB": 可用內存,
                    "使用百分比": round(使用百分比, 2)
                }
            )

        except Exception as 異常:
            return 檢查結果(
                健康等級=健康等級.未知,
                錯誤信息=str(異常),
                檢查時間=datetime.now(timezone.utc).isoformat()
            )

    def _檢查CPU負載(self, 名稱: str) -> 檢查結果:
        """檢查CPU負載"""
        try:
            with open("/proc/loadavg", "r") as 文件:
                負載數據 = 文件.read().strip().split()

            一分鐘負載 = float(負載數據[0])

            # 獲取CPU核心數
            CPU核心數 = os.cpu_count() or 1
            負載百分比 = (一分鐘負載 / CPU核心數) * 100

            等級 = 健康等級.健康
            if 負載百分比 > 90:
                等級 = 健康等級.不健康
            elif 負載百分比 > 70:
                等級 = 健康等級.亞健康

            return 檢查結果(
                健康等級=等級,
                檢查時間=datetime.now(timezone.utc).isoformat(),
                詳細數據={
                    "一分鐘負載": 一分鐘負載,
                    "CPU核心數": CPU核心數,
                    "負載百分比": round(負載百分比, 2)
                }
            )

        except Exception as 異常:
            return 檢查結果(
                健康等級=健康等級.未知,
                錯誤信息=str(異常),
                檢查時間=datetime.now(timezone.utc).isoformat()
            )

    # ═══════════════════════════════════════════════════════════════════════════
    # 連續監控模式
    # ═══════════════════════════════════════════════════════════════════════════

    def 啟動監控(self, 間隔秒: int = 30, 回調函數: Optional[Callable] = None):
        """啟動連續健康監控"""
        self.日誌.info(f"{龍印標記} 啟動健康監控模式，間隔: {間隔秒}秒")

        try:
            while True:
                報告 = self.執行全部檢查()

                if 回調函數:
                    回調函數(報告)

                # 如果狀態不健康，縮短檢查間隔
                if 報告.總體狀態 == 健康等級.不健康:
                    self.日誌.warning(f"{阻塞風險} 檢測到不健康狀態，縮短檢查間隔")
                    time.sleep(min(間隔秒, 10))
                else:
                    time.sleep(間隔秒)

        except KeyboardInterrupt:
            self.日誌.info(f"{龍印標記} 健康監控已停止")

    def 獲取歷史(self) -> List[Dict]:
        """獲取檢查歷史"""
        return self.檢查歷史


# ═══════════════════════════════════════════════════════════════════════════════
# 命令行入口
# ═══════════════════════════════════════════════════════════════════════════════

def 主函數():
    import argparse

    解析器 = argparse.ArgumentParser(description="龍魂健康檢查系統")
    解析器.add_argument("--url", default="http://localhost:8080", help="服務基礎URL")
    解析器.add_argument("--timeout", type=int, default=10, help="超時秒數")
    解析器.add_argument("--watch", action="store_true", help="持續監控模式")
    解析器.add_argument("--interval", type=int, default=30, help="監控間隔秒數")

    參數 = 解析器.parse_args()

    檢查器 = 健康檢查器(
        基礎URL=參數.url,
        超時秒=參數.timeout
    )

    if 參數.watch:
        檢查器.啟動監控(間隔秒=參數.interval)
    else:
        報告 = 檢查器.執行全部檢查()
        print(json.dumps(asdict(報告), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    主函數()
