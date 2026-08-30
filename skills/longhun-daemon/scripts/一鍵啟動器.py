# DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-3fa7fff5
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
================================================================================
【龍魂一鍵啟動器】
================================================================================
· 功能：按依賴順序一鍵啟動全部龍魂服務
· 架構：拓撲排序 → 依賴檢查 → 分階段啟動
· 規範：CNSH中文編程規範 v5.2
· 君子協議：未經授權不得修改啟動順序
================================================================================
· DNA: #龍芯⚡️2026-06-19-LONGHUN-DAEMON-v5.2
================================================================================
"""

import os
import sys
import json
import time
import signal
import socket
import hashlib
import argparse
import datetime
import subprocess
import threading
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ═══════════════════════════════════════════════════════════════════════════════
# 第一區：DNA追溯與全域常數
# ═══════════════════════════════════════════════════════════════════════════════
龍魂DNA追溯碼 = "#龍芯⚡️2026-06-19-LONGHUN-DAEMON-v5.2"
龍魂版本號 = "v5.2.0"
龍魂啟動序列 = "LONGHUN-BOOT-2026"

# 三色審計級別
審計級別_紅 = "紅"
審計級別_黃 = "黃"
審計級別_綠 = "綠"

# 啟動階段定義
啟動階段表 = {
    "第一階段_基礎設施": {
        "描述": "啟動核心基礎服務",
        "服務列表": ["龍魂操作台"],
        "超時秒數": 60,
    },
    "第二階段_中間件": {
        "描述": "啟動中間件服務",
        "服務列表": ["MCP服務"],
        "超時秒數": 45,
        "等待條件": "第一階段_基礎設施",
    },
    "第三階段_集成服務": {
        "描述": "啟動外部集成服務",
        "服務列表": ["Kimi集成", "Notion同步"],
        "超時秒數": 60,
        "等待條件": "第二階段_中間件",
    },
    "第四階段_智能引擎": {
        "描述": "啟動智能分析引擎",
        "服務列表": ["自動化評估", "復盤引擎"],
        "超時秒數": 120,
        "等待條件": "第三階段_集成服務",
    },
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
        self.日誌文件路徑 = self.日誌目錄 / f"startup_audit_{datetime.date.today().isoformat()}.log"
        self.運行日誌路徑 = self.日誌目錄 / "launchd.out.log"
        self.錯誤日誌路徑 = self.日誌目錄 / "launchd.err.log"

    def 記錄(self, 級別: str, 模塊: str, 訊息: str, 元數據: dict = None):
        時間戳 = datetime.datetime.now().isoformat()
        龍印 = hashlib.sha256(f"{時間戳}{模塊}{訊息}{龍魂DNA追溯碼}".encode()).hexdigest()[:12]
        記錄行 = f"[{時間戳}] [龍印:{龍印}] [{級別}] [一鍵啟動器][{模塊}] {訊息}"
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
# 第三區：一鍵啟動器核心
# ═══════════════════════════════════════════════════════════════════════════════

class 一鍵啟動器:
    """
    龍魂一鍵啟動器
    · 按四階段順序啟動全部服務
    · 支持健康檢查和自恢復
    · 提供啟動報告
    """

    def __init__(self):
        self.啟動報告 = {
            "啟動時間": "",
            "完成時間": "",
            "總耗時秒": 0,
            "階段結果": {},
            "服務狀態": {},
            "成功": False,
        }
        self.強制停止 = threading.Event()
        self.腳本目錄 = Path(__file__).parent

    def 檢查前置條件(self) -> Tuple[bool, List[str]]:
        """檢查啟動前置條件"""
        日誌.綠("前置檢查", "開始驗證啟動條件...")
        問題列表 = []

        # 1. Python版本檢查
        if sys.version_info < (3, 9):
            問題列表.append(f"Python版本過低: {sys.version} (需要 >= 3.9)")

        # 2. 網絡檢查
        try:
            socket.create_connection(("127.0.0.1", 1), timeout=1)
        except Exception:
            問題列表.append("本地網絡不可用")

        # 3. 端口衝突預檢
        佔用端口 = []
        for 端口 in [8443]:
            try:
                測試 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                測試.settimeout(1)
                if 測試.connect_ex(("127.0.0.1", 端口)) == 0:
                    佔用端口.append(端口)
                測試.close()
            except Exception:
                pass
        if 佔用端口:
            日誌.黃("端口檢查", f"端口 {佔用端口} 已被佔用，將嘗試接管")

        # 4. 磁盤空間檢查
        try:
            磁盤統計 = os.statvfs(self.腳本目錄)
            可用GB = (磁盤統計.f_bavail * 磁盤統計.f_frsize) / (1024**3)
            if 可用GB < 1.0:
                問題列表.append(f"磁盤空間不足: 僅剩 {可用GB:.2f}GB")
        except Exception:
            pass

        通過 = len(問題列表) == 0
        if 通過:
            日誌.綠("前置檢查", "所有條件滿足，可以啟動")
        else:
            for 問題 in 問題列表:
                日誌.紅("前置檢查", 問題)
        return 通過, 問題列表

    def 啟動服務進程(self, 服務名稱: str, 指令: List[str], 環境: dict = None) -> Optional[subprocess.Popen]:
        """啟動單個服務進程"""
        try:
            服務環境 = os.environ.copy()
            服務環境["LONGHUN_DAEMON"] = "1"
            服務環境["LONGHUN_DNA"] = 龍魂DNA追溯碼
            服務環境["LONGHUN_SERVICE"] = 服務名稱
            服務環境["LONGHUN_BOOT_SEQ"] = 龍魂啟動序列
            if 環境:
                服務環境.update(環境)

            進程 = subprocess.Popen(
                指令,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=服務環境,
                cwd=str(self.腳本目錄.parent.parent),
            )
            日誌.綠("進程啟動", f"[{服務名稱}] PID={進程.pid}")
            return 進程
        except Exception as 異常:
            日誌.紅("進程啟動", f"[{服務名稱}] 失敗: {異常}")
            return None

    def 等待服務就緒(self, 服務名稱: str, 端口: int, 超時秒數: int = 30) -> bool:
        """等待服務端口就緒"""
        if 端口 <= 0:
            # 無端口服務（定時任務），直接返回成功
            return True

        日誌.綠("等待就緒", f"[{服務名稱}] 等待端口 {端口} 就緒 (超時{超時秒數}秒)...")
        開始時間 = time.time()
        while time.time() - 開始時間 < 超時秒數:
            if self.強制停止.is_set():
                return False
            try:
                測試 = socket.create_connection(("127.0.0.1", 端口), timeout=1)
                測試.close()
                耗時 = time.time() - 開始時間
                日誌.綠("服務就緒", f"[{服務名稱}] 已就緒 (耗時 {耗時:.1f}秒)")
                return True
            except Exception:
                time.sleep(0.5)

        日誌.紅("等待超時", f"[{服務名稱}] 端口 {端口} 未就緒")
        return False

    def 執行啟動階段(self, 階段名稱: str, 階段配置: dict) -> Dict[str, bool]:
        """執行單個啟動階段"""
        日誌.綠("階段啟動", f"===== {階段名稱}: {階段配置['描述']} =====")
        結果 = {}

        # 檢查等待條件
        if "等待條件" in 階段配置:
            等待階段 = 階段配置["等待條件"]
            日誌.綠("依賴等待", f"等待 [{等待階段}] 完成...")

        服務配置表 = {
            "龍魂操作台": {
                "端口": 8443,
                "指令": [sys.executable, "-m", "http.server", "8443"],
            },
            "MCP服務": {
                "端口": 8443,
                "指令": [sys.executable, "-m", "mcp.server"],
            },
            "Kimi集成": {
                "端口": 8443,
                "指令": [sys.executable, "-m", "longhun.kimi_bridge"],
            },
            "Notion同步": {
                "端口": 0,
                "指令": [sys.executable, "-m", "longhun.notion_sync"],
            },
            "自動化評估": {
                "端口": 0,
                "指令": [sys.executable, "-m", "longhun.auto_evaluation"],
            },
            "復盤引擎": {
                "端口": 0,
                "指令": [sys.executable, "-m", "longhun.review_engine"],
            },
        }

        for 服務名稱 in 階段配置["服務列表"]:
            if self.強制停止.is_set():
                結果[服務名稱] = False
                break

            if 服務名稱 not in 服務配置表:
                日誌.紅("配置缺失", f"[{服務名稱}] 無啟動配置")
                結果[服務名稱] = False
                continue

            配置 = 服務配置表[服務名稱]
            日誌.綠("啟動服務", f"[{服務名稱}] 啟動中...")

            進程 = self.啟動服務進程(服務名稱, 配置["指令"])
            if not 進程:
                結果[服務名稱] = False
                continue

            # 等待服務就緒
            就緒 = self.等待服務就緒(服務名稱, 配置["端口"], 階段配置.get("超時秒數", 30))
            結果[服務名稱] = 就緒

            if 就緒:
                日誌.綠("階段完成", f"[{服務名稱}] 啟動成功")
            else:
                日誌.紅("階段失敗", f"[{服務名稱}] 未正常就緒")

        return 結果

    def 啟動全部(self) -> dict:
        """按階段順序啟動所有服務"""
        總開始 = time.time()
        self.啟動報告["啟動時間"] = datetime.datetime.now().isoformat()

        日誌.綠("啟動序列", f"{'='*60}")
        日誌.綠("啟動序列", f"龍魂系統一鍵啟動  {龍魂版本號}")
        日誌.綠("啟動序列", f"啟動序列: {龍魂啟動序列}")
        日誌.綠("啟動序列", f"{'='*60}")

        # 前置檢查
        檢查通過, 問題 = self.檢查前置條件()
        if not 檢查通過:
            self.啟動報告["成功"] = False
            self.啟動報告["錯誤"] = 問題
            return self.啟動報告

        # 按階段啟動
        全部成功 = True
        for 階段名稱, 階段配置 in 啟動階段表.items():
            if self.強制停止.is_set():
                日誌.黃("啟動中止", "收到停止信號")
                break

            階段結果 = self.執行啟動階段(階段名稱, 階段配置)
            self.啟動報告["階段結果"][階段名稱] = 階段結果
            self.啟動報告["服務狀態"].update(階段結果)

            if not all(階段結果.values()):
                日誌.黃("階段告警", f"[{階段名稱}] 部分服務未啟動")
                全部成功 = False

        總耗時 = time.time() - 總開始
        self.啟動報告["完成時間"] = datetime.datetime.now().isoformat()
        self.啟動報告["總耗時秒"] = round(總耗時, 2)
        self.啟動報告["成功"] = 全部成功

        self._打印啟動報告()
        return self.啟動報告

    def 停止全部(self):
        """停止所有已啟動的服務"""
        日誌.黃("停止序列", "正在停止所有龍魂服務...")
        self.強制停止.set()

        # 調用守護進程管理器停止全部
        try:
            管理器路徑 = self.腳本目錄 / "守護進程管理器.py"
            if 管理器路徑.exists():
                subprocess.run(
                    [sys.executable, str(管理器路徑), "--stop-all"],
                    timeout=60,
                    capture_output=True,
                )
        except Exception as 異常:
            日誌.黃("停止序列", f"調用管理器失敗: {異常}")

        日誌.綠("停止序列", "所有服務已停止")

    def _打印啟動報告(self):
        """打印啟動報告摘要"""
        報告 = self.啟動報告
        print("\n" + "=" * 70)
        print(f"  🐉 龍魂系統啟動報告")
        print("=" * 70)
        print(f"  啟動時間: {報告['啟動時間']}")
        print(f"  完成時間: {報告['完成時間']}")
        print(f"  總耗時:   {報告['總耗時秒']} 秒")
        print(f"  整體狀態: {'✅ 全部成功' if 報告['成功'] else '⚠️ 部分失敗'}")
        print("-" * 70)

        for 階段名稱, 階段結果 in 報告["階段結果"].items():
            print(f"\n  📦 {階段名稱}")
            for 服務名稱, 狀態 in 階段結果.items():
                圖標 = "✅" if 狀態 else "❌"
                print(f"     {圖標} {服務名稱}")

        print("\n" + "=" * 70)
        print(f"  DNA: {龍魂DNA追溯碼}")
        print("=" * 70 + "\n")

        # 保存報告
        報告路徑 = self.腳本目錄.parent / "logs" / "last_startup_report.json"
        try:
            with open(報告路徑, "w", encoding="utf-8") as 檔:
                json.dump(報告, 檔, ensure_ascii=False, indent=2)
        except Exception:
            pass


# ═══════════════════════════════════════════════════════════════════════════════
# 第四區：信號處理與守護模式
# ═══════════════════════════════════════════════════════════════════════════════

啟動器實例: Optional[一鍵啟動器] = None


def 信號處理(信號編號, 幀):
    """處理系統信號"""
    信號名 = {signal.SIGTERM: "SIGTERM", signal.SIGINT: "SIGINT"}.get(信號編號, str(信號編號))
    日誌.黃("信號處理", f"收到 {信號名}，開始優雅停止...")
    if 啟動器實例:
        啟動器實例.停止全部()
    sys.exit(0)


signal.signal(signal.SIGTERM, 信號處理)
signal.signal(signal.SIGINT, 信號處理)


# ═══════════════════════════════════════════════════════════════════════════════
# 第五區：命令行接口
# ═══════════════════════════════════════════════════════════════════════════════

def 主函數():
    解析器 = argparse.ArgumentParser(
        description="龍魂一鍵啟動器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 一鍵啟動器.py              啟動全部服務
  python3 一鍵啟動器.py --daemon     守護進程模式
  python3 一鍵啟動器.py --stop       停止全部服務
  python3 一鍵啟動器.py --status     查看狀態
  python3 一鍵啟動器.py --check      僅檢查前置條件
        """
    )
    解析器.add_argument("--daemon", action="store_true", help="守護進程模式")
    解析器.add_argument("--stop", action="store_true", help="停止全部服務")
    解析器.add_argument("--status", action="store_true", help="查看狀態")
    解析器.add_argument("--check", action="store_true", help="僅檢查前置條件")
    解析器.add_argument("--phase", help="僅啟動指定階段")

    參數 = 解析器.parse_args()

    global 啟動器實例
    啟動器實例 = 一鍵啟動器()

    if 參數.check:
        通過, 問題 = 啟動器實例.檢查前置條件()
        sys.exit(0 if 通過 else 1)
    elif 參數.stop:
        啟動器實例.停止全部()
    elif 參數.status:
        管理器路徑 = Path(__file__).parent / "守護進程管理器.py"
        if 管理器路徑.exists():
            subprocess.run([sys.executable, str(管理器路徑), "--status"])
    elif 參數.daemon:
        日誌.綠("守護模式", "進入守護進程循環，按 Ctrl+C 或發送 SIGTERM 停止")
        while True:
            報告 = 啟動器實例.啟動全部()
            if not 報告["成功"]:
                日誌.紅("守護模式", "啟動失敗，30秒後重試...")
                time.sleep(30)
            else:
                # 啟動成功後保持運行
                日誌.綠("守護模式", "所有服務運行中，進入監控循環...")
                try:
                    while not 啟動器實例.強制停止.is_set():
                        time.sleep(10)
                except KeyboardInterrupt:
                    break
                啟動器實例.停止全部()
                break
    elif 參數.phase:
        if 參數.phase in 啟動階段表:
            啟動器實例.執行啟動階段(參數.phase, 啟動階段表[參數.phase])
        else:
            日誌.紅("參數錯誤", f"未知階段: {參數.phase}")
            sys.exit(1)
    else:
        # 默認：啟動全部
        報告 = 啟動器實例.啟動全部()
        sys.exit(0 if 報告["成功"] else 1)


if __name__ == "__main__":
    主函數()
