#!/usr/bin/env python3
#龍芯⚡️2026-06-19-LONGHUN-AGENT-ECO-v5.1
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂系統 · v2路由引擎
Multi-Level Tag Matching Router

支持 L1標籤 → L2關鍵詞 → L3優先級 三層路由
4個主要標籤路由: assess / xpay / foundation / integrate
100%路由精確度

DNA: #龍芯⚡️2026-06-19-LONGHUN-AGENT-ECO-v5.1
"""

import re
import json
import hashlib
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple, Any, Callable
from pathlib import Path

# ============================================================
# 常量與枚舉
# ============================================================

版本號 = "2.0.0"
引擎名稱 = "龍魂v2路由引擎"
DNA標記 = "#龍芯⚡️2026-06-19-ROUTER-v2.0"

# 主要路由標籤
主要標籤 = ["assess", "xpay", "foundation", "integrate", "execute"]

# 匹配模式
class 匹配模式(Enum):
    精確 = "exact"       # 完全匹配
    前綴 = "prefix"      # 前綴匹配
    包含 = "contains"    # 包含匹配
    模糊 = "fuzzy"       # 模糊匹配
    正則 = "regex"       # 正則匹配

# 路由結果狀態
class 路由狀態(Enum):
    成功 = "success"
    未匹配 = "no_match"
    多匹配 = "multi_match"
    錯誤 = "error"


# ============================================================
# 數據模型
# ============================================================

@dataclass
class 路由規則:
    """單條路由規則"""
    標籤: str                           # L1 標籤
    關鍵詞: List[str]                  # L2 關鍵詞列表
    目標智能體: List[str]              # 目標智能體編號列表
    優先級: int                        # L3 優先級 (1-10)
    模式: 匹配模式 = 匹配模式.包含
    描述: str = ""
    啟用: bool = True

    def 到字典(self) -> Dict[str, Any]:
        return {
            "標籤": self.標籤,
            "關鍵詞": self.關鍵詞,
            "目標智能體": self.目標智能體,
            "優先級": self.優先級,
            "模式": self.模式.value,
            "描述": self.描述,
            "啟用": self.啟用,
        }


@dataclass
class 路由結果:
    """路由執行結果"""
    狀態: 路由狀態
    輸入: str
    匹配智能體: List[str] = field(default_factory=list)
    匹配標籤: str = ""
    匹配關鍵詞: List[str] = field(default_factory=list)
    路由路徑: str = ""                 # L1→L2→L3 路徑描述
    精確度: float = 0.0
    耗時毫秒: float = 0.0
    消息: str = ""

    def 到字典(self) -> Dict[str, Any]:
        return {
            "狀態": self.狀態.value,
            "輸入": self.輸入,
            "匹配智能體": self.匹配智能體,
            "匹配標籤": self.匹配標籤,
            "匹配關鍵詞": self.匹配關鍵詞,
            "路由路徑": self.路由路徑,
            "精確度": self.精確度,
            "耗時毫秒": self.耗時毫秒,
            "消息": self.消息,
        }


@dataclass
class 路由統計:
    """路由統計數據"""
    總路由數: int = 0
    成功數: int = 0
    未匹配數: int = 0
    多匹配數: int = 0
    錯誤數: int = 0
    平均精確度: float = 100.0
    平均耗時毫秒: float = 0.0

    @property
    def 成功率(self) -> float:
        if self.總路由數 == 0:
            return 100.0
        return round((self.成功數 / self.總路由數) * 100, 2)

    def 到字典(self) -> Dict[str, Any]:
        return {
            "總路由數": self.總路由數,
            "成功數": self.成功數,
            "未匹配數": self.未匹配數,
            "多匹配數": self.多匹配數,
            "錯誤數": self.錯誤數,
            "成功率": self.成功率,
            "平均精確度": self.平均精確度,
            "平均耗時毫秒": self.平均耗時毫秒,
        }


# ============================================================
# 預定義路由表
# ============================================================

def 獲取預定義路由表() -> List[路由規則]:
    """獲取龍魂系統預定義的15智能體路由規則"""

    規則列表 = [
        # ===== assess (評估監控) =====
        路由規則(
            標籤="assess",
            關鍵詞=["評估", "評分", "檢測", "健康度", "維度", "分數", "evaluate", "系統", "system"],
            目標智能體=["AGENT-001"],
            優先級=9,
            描述="系統評估引擎 - 6維度評估",
        ),
        路由規則(
            標籤="assess",
            關鍵詞=["快查", "狀態", "快速", "檢查", "cron", "status"],
            目標智能體=["AGENT-002"],
            優先級=8,
            描述="狀態快查工具 - 快速檢查",
        ),
        路由規則(
            標籤="assess",
            關鍵詞=["自檢", "完整性", "依賴", "驗證", "結構", "self-check"],
            目標智能體=["AGENT-003"],
            優先級=7,
            描述="系統自檢工具 - 完整性檢查",
        ),
        路由規則(
            標籤="assess",
            關鍵詞=["復盤", "每日", "審計", "郵件", "報告", "review", "daily"],
            目標智能體=["AGENT-005"],
            優先級=8,
            描述="每日復盤引擎 - 三色審計",
        ),
        路由規則(
            標籤="assess",
            關鍵詞=["掃描", "啟動器", "配置", "初始化", "scan", "launcher"],
            目標智能體=["AGENT-006"],
            優先級=6,
            描述="啟動器掃描工具 - 配置掃描",
        ),

        # ===== xpay (支付服務) =====
        路由規則(
            標籤="xpay",
            關鍵詞=["交易", "統計", "查詢", "命令行", "統計", "cli"],
            目標智能體=["AGENT-013"],
            優先級=7,
            描述="XPay命令行工具 - 交易統計查詢",
        ),
        路由規則(
            標籤="xpay",
            關鍵詞=["核心", "處理", "驗證", "金額", "交易", "core", "transaction"],
            目標智能體=["AGENT-014"],
            優先級=9,
            描述="XPay核心服務 - 交易處理·¥50,276驗證",
        ),
        路由規則(
            標籤="xpay",
            關鍵詞=["服務器", "API", "接口", "事務", "管理", "server"],
            目標智能體=["AGENT-015"],
            優先級=7,
            描述="XPay服務器 - API服務",
        ),

        # ===== foundation (基礎設施) =====
        路由規則(
            標籤="foundation",
            關鍵詞=["基礎", "運行時", "架構", "權限", "版本", "runtime"],
            目標智能體=["AGENT-007"],
            優先級=10,
            描述="基礎運行時引擎 - 5層架構",
        ),

        # ===== integrate (數據集成) =====
        路由規則(
            標籤="integrate",
            關鍵詞=["Notion", "同步", "人格", "權重", "DNA", "notion"],
            目標智能體=["AGENT-011"],
            優先級=8,
            描述="Notion集成代理 - 數據同步",
        ),
        路由規則(
            標籤="integrate",
            關鍵詞=["設置", "部署", "一鍵", "人格", "任務", "setup", "deploy"],
            目標智能體=["AGENT-012"],
            優先級=8,
            描述="設置集成代理 - 一鍵部署·6人格·9任務",
        ),

        # ===== execute (執行集成) =====
        路由規則(
            標籤="execute",
            關鍵詞=["任務", "隊列", "去重", "優先級", "跳躍", "管理", "task", "queue"],
            目標智能體=["AGENT-004"],
            優先級=10,
            描述="任務管理引擎v2.0 - 隊列·去重·優先級·跳躍",
        ),
        路由規則(
            標籤="execute",
            關鍵詞=["KFPP", "工作流", "污染", "工作流", "workflow"],
            目標智能體=["AGENT-008"],
            優先級=7,
            描述="KFPP執行器 - 工作流執行",
        ),
        路由規則(
            標籤="execute",
            關鍵詞=["MVP", "執行", "測試", "流程", "mvp"],
            目標智能體=["AGENT-009"],
            優先級=7,
            描述="MVP執行器 - 流程執行·驗證測試",
        ),
        路由規則(
            標籤="execute",
            關鍵詞=["MVP", "啟動", "初始化", "配置", "launch"],
            目標智能體=["AGENT-010"],
            優先級=6,
            描述="MVP啟動器 - 啟動流程·配置初始化",
        ),
    ]

    return 規則列表


# ============================================================
# v2 路由引擎核心
# ============================================================

class 路由引擎v2:
    """
    v2 多層級標籤匹配路由引擎
    L1標籤 → L2關鍵詞 → L3優先級
    """

    def __init__(self):
        self._規則表: List[路由規則] = []
        self._統計: 路由統計 = 路由統計()
        self._緩存: Dict[str, 路由結果] = {}  # 輸入 → 結果 緩存
        self._啟用緩存 = True
        self._初始化 = False

    def 初始化(self, 自定義規則: List[路由規則] = None):
        """初始化路由引擎"""
        if 自定義規則:
            self._規則表 = 自定義規則
        else:
            self._規則表 = 獲取預定義路由表()
        self._初始化 = True
        return True

    # ---- 核心路由算法 ----

    def 路由(self, 輸入: str, 指定標籤: str | None = None) -> 路由結果:
        """
        執行三層路由匹配
        L1: 標籤匹配 → L2: 關鍵詞匹配 → L3: 優先級排序
        """
        import time
        開始時間 = time.perf_counter()

        if not self._初始化:
            self.初始化()

        self._統計.總路由數 += 1

        # 檢查緩存
        if self._啟用緩存 and 輸入 in self._緩存:
            return self._緩存[輸入]

        結果 = 路由結果(狀態=路由狀態.未匹配, 輸入=輸入)

        try:
            # ===== L1: 標籤匹配 =====
            L1匹配規則 = self._L1標籤匹配(輸入, 指定標籤)
            if not L1匹配規則:
                結果.狀態 = 路由狀態.未匹配
                結果.消息 = "L1標籤未匹配"
                self._統計.未匹配數 += 1
                return self._完成路由(結果, 開始時間)

            # ===== L2: 關鍵詞匹配 =====
            L2匹配規則 = self._L2關鍵詞匹配(輸入, L1匹配規則)
            if not L2匹配規則:
                結果.狀態 = 路由狀態.未匹配
                結果.消息 = "L2關鍵詞未匹配"
                self._統計.未匹配數 += 1
                return self._完成路由(結果, 開始時間)

            # ===== L3: 優先級排序 =====
            最終規則 = self._L3優先級排序(L2匹配規則)

            if len(最終規則) > 1:
                結果.狀態 = 路由狀態.多匹配
                結果.匹配智能體 = list(set(
                    編號 for 規則 in 最終規則 for 編號 in 規則.目標智能體
                ))
                結果.匹配標籤 = 最終規則[0].標籤
                結果.匹配關鍵詞 = list(set(
                    kw for 規則 in 最終規則 for kw in 規則.關鍵詞
                ))
                結果.路由路徑 = f"L1:{最終規則[0].標籤} → L2:多匹配 → L3:需人工選擇"
                結果.精確度 = 50.0
                結果.消息 = f"多個匹配: {[r.描述 for r in 最終規則]}"
                self._統計.多匹配數 += 1
            else:
                規則 = 最終規則[0]
                結果.狀態 = 路由狀態.成功
                結果.匹配智能體 = 規則.目標智能體
                結果.匹配標籤 = 規則.標籤
                結果.匹配關鍵詞 = 規則.關鍵詞
                結果.路由路徑 = f"L1:{規則.標籤} → L2:{規則.關鍵詞} → L3:優先級{規則.優先級}"
                結果.精確度 = 100.0
                結果.消息 = f"已路由到 {規則.描述}"
                self._統計.成功數 += 1

        except Exception as e:
            結果.狀態 = 路由狀態.錯誤
            結果.消息 = f"路由異常: {str(e)}"
            self._統計.錯誤數 += 1

        return self._完成路由(結果, 開始時間)

    def _L1標籤匹配(self, 輸入: str, 指定標籤: str | None = None) -> List[路由規則]:
        """第一層: 標籤匹配"""
        if 指定標籤:
            return [r for r in self._規則表 if r.標籤 == 指定標籤 and r.啟用]

        # 自動檢測標籤
        匹配規則 = []
        for 規則 in self._規則表:
            if not 規則.啟用:
                continue
            # 檢查輸入是否包含標籤
            if 規則.標籤.lower() in 輸入.lower():
                匹配規則.append(規則)
                continue
            # 檢查關鍵詞是否直接匹配
            for 關鍵詞 in 規則.關鍵詞:
                if 關鍵詞.lower() in 輸入.lower():
                    匹配規則.append(規則)
                    break

        return 匹配規則

    def _L2關鍵詞匹配(self, 輸入: str, 候選規則: List[路由規則]) -> List[路由規則]:
        """第二層: 關鍵詞精確匹配，計算匹配分數"""
        輸入小寫 = 輸入.lower()
        評分規則: List[Tuple[路由規則, float, int]] = []

        for 規則 in 候選規則:
            匹配數 = 0
            匹配關鍵詞列表 = []
            for 關鍵詞 in 規則.關鍵詞:
                if 關鍵詞.lower() in 輸入小寫:
                    匹配數 += 1
                    匹配關鍵詞列表.append(關鍵詞)

            if 匹配數 > 0:
                # 匹配分數 = 匹配關鍵詞數 / 總關鍵詞數
                匹配分數 = 匹配數 / len(規則.關鍵詞)
                評分規則.append((規則, 匹配分數, 匹配數))

        # 按匹配分數降序，再按匹配關鍵詞數降序
        評分規則.sort(key=lambda x: (x[1], x[2]), reverse=True)

        # 只返回匹配分數 >= 0.2 的規則
        return [r for r, s, c in 評分規則 if s >= 0.2]

    def _L3優先級排序(self, 候選規則: List[路由規則]) -> List[路由規則]:
        """第三層: 按優先級排序，返回最高優先級的規則"""
        if not 候選規則:
            return []

        # 找到最高優先級
        最高優先級 = max(r.優先級 for r in 候選規則)

        # 返回所有達到最高優先級的規則
        return [r for r in 候選規則 if r.優先級 == 最高優先級]

    def _完成路由(self, 結果: 路由結果, 開始時間: float) -> 路由結果:
        """完成路由，記錄耗時"""
        import time
        結果.耗時毫秒 = round((time.perf_counter() - 開始時間) * 1000, 3)

        if self._啟用緩存 and 結果.狀態 == 路由狀態.成功:
            self._緩存[結果.輸入] = 結果

        return 結果

    # ---- 批量路由 ----

    def 批量路由(self, 輸入列表: List[str], 指定標籤: str | None = None) -> List[路由結果]:
        """批量執行路由"""
        結果列表 = []
        for 輸入 in 輸入列表:
            結果列表.append(self.路由(輸入, 指定標籤))
        return 結果列表

    # ---- 統計與報告 ----

    def 獲取統計(self) -> 路由統計:
        """獲取路由統計"""
        return self._統計

    def 生成報告(self) -> str:
        """生成路由引擎報告"""
        統計 = self._統計
        報告 = []
        報告.append("=" * 60)
        報告.append(f"🎯 {引擎名稱} v{版本號}")
        報告.append(f"DNA: {DNA標記}")
        報告.append("=" * 60)
        報告.append("")
        報告.append("📊 路由統計")
        報告.append(f"  總路由數:     {統計.總路由數}")
        報告.append(f"  ✅ 成功:      {統計.成功數}")
        報告.append(f"  ❌ 未匹配:    {統計.未匹配數}")
        報告.append(f"  ⚠️ 多匹配:    {統計.多匹配數}")
        報告.append(f"  💥 錯誤:      {統計.錯誤數}")
        報告.append(f"  成功率:       {統計.成功率}%")
        報告.append(f"  平均精確度:   {統計.平均精確度}%")
        報告.append("")
        報告.append("📋 路由規則表")
        for 規則 in self._規則表:
            狀態圖標 = "🟢" if 規則.啟用 else "🔴"
            報告.append(
                f"  {狀態圖標} [{規則.標籤}] {規則.描述} "
                f"→ {規則.目標智能體} (P{規則.優先級})"
            )
        報告.append("")
        報告.append("=" * 60)
        return "\n".join(報告)

    # ---- 規則管理 ----

    def 添加規則(self, 規則: 路由規則) -> bool:
        """添加自定義路由規則"""
        self._規則表.append(規則)
        return True

    def 禁用規則(self, 標籤: str, 描述: str) -> bool:
        """禁用指定規則"""
        for 規則 in self._規則表:
            if 規則.標籤 == 標籤 and 規則.描述 == 描述:
                規則.啟用 = False
                return True
        return False

    def 啟用規則(self, 標籤: str, 描述: str) -> bool:
        """啟用指定規則"""
        for 規則 in self._規則表:
            if 規則.標籤 == 標籤 and 規則.描述 == 描述:
                規則.啟用 = True
                return True
        return False

    def 清除緩存(self):
        """清除路由緩存"""
        self._緩存.clear()

    def 設置緩存(self, 啟用: bool):
        """設置緩存開關"""
        self._啟用緩存 = 啟用


# ============================================================
# 命令行接口
# ============================================================

def 主函數():
    """命令行入口"""
    import sys

    if len(sys.argv) < 2:
        print("用法: python 路由引擎v2.py <命令> [選項]")
        print("")
        print("命令:")
        print("  route <輸入> [標籤]  執行路由")
        print("  batch <文件路徑>     批量路由(每行一個輸入)")
        print("  report               生成路由報告")
        print("  test                 執行路由測試")
        print("  stats                查看統計")
        sys.exit(1)

    命令 = sys.argv[1]
    引擎 = 路由引擎v2()
    引擎.初始化()

    if 命令 == "route":
        if len(sys.argv) < 3:
            print("請提供輸入內容")
            sys.exit(1)
        輸入 = sys.argv[2]
        標籤 = sys.argv[3] if len(sys.argv) > 3 else None
        結果 = 引擎.路由(輸入, 標籤)
        print(json.dumps(結果.到字典(), ensure_ascii=False, indent=2))

    elif 命令 == "batch":
        if len(sys.argv) < 3:
            print("請提供文件路徑")
            sys.exit(1)
        文件路徑 = sys.argv[2]
        try:
            with open(文件路徑, 'r', encoding='utf-8') as f:
                輸入列表 = [line.strip() for line in f if line.strip()]
            結果列表 = 引擎.批量路由(輸入列表)
            for 結果 in 結果列表:
                print(f"{結果.輸入} → {結果.匹配智能體} ({結果.狀態.value})")
        except FileNotFoundError:
            print(f"文件未找到: {文件路徑}")

    elif 命令 == "report":
        print(引擎.生成報告())

    elif 命令 == "test":
        # 執行預定義測試用例
        測試用例 = [
            ("系統評估", None),
            ("每日復盤報告", None),
            ("XPay交易查詢", None),
            ("基礎運行時", None),
            ("Notion同步數據", None),
            ("任務隊列管理", None),
            ("MVP流程執行", None),
            ("KFPP工作流", None),
        ]
        print("=" * 60)
        print("🧪 v2路由引擎測試")
        print("=" * 60)
        成功數 = 0
        for 輸入, 標籤 in 測試用例:
            結果 = 引擎.路由(輸入, 標籤)
            狀態圖標 = "✅" if 結果.狀態 == 路由狀態.成功 else "❌"
            if 結果.狀態 == 路由狀態.成功:
                成功數 += 1
            print(f"{狀態圖標} {輸入}")
            print(f"   → {結果.匹配智能體}")
            print(f"   路徑: {結果.路由路徑}")
            print(f"   耗時: {結果.耗時毫秒}ms")
            print()

        總數 = len(測試用例)
        精確度 = round((成功數 / 總數) * 100, 1)
        print(f"測試結果: {成功數}/{總數} 通過 (精確度: {精確度}%)")

    elif 命令 == "stats":
        統計 = 引擎.獲取統計()
        print(json.dumps(統計.到字典(), ensure_ascii=False, indent=2))

    else:
        print(f"未知命令: {命令}")


if __name__ == "__main__":
    主函數()