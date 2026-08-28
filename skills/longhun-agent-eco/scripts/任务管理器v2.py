#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
"""
龍魂系統 · 任務管理器v2.0
Task Management v2.0 with Jump Operations, Deduplication & Priority Decay

特性:
- 跳躍式操作支持 (非線性任務處理)
- 自動去重機制 (24小時窗口)
- 優先級衰減算法 (時間衰減 + 完成獎勵)
- 隊列管理 (優先級排序·並發控制)

DNA: #龍芯⚡️2026-06-19-LONGHUN-AGENT-ECO-v5.1
"""

import json
import time
import hashlib
import datetime
from enum import Enum, auto
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Set, Tuple, Any, Callable
from pathlib import Path
from collections import OrderedDict

# ============================================================
# 常量定義
# ============================================================

版本號 = "2.0.0"
引擎名稱 = "龍魂任務管理器v2.0"
DNA標記 = "#龍芯⚡️2026-06-19-TASKMGR-v2.0"

# 默認配置
默認去重窗口小時 = 24
默認優先級衰減率 = 0.95
默認最大隊列長 = 1000
默認並發數 = 5


# ============================================================
# 枚舉定義
# ============================================================

class 任務狀態(Enum):
    待處理 = "pending"
    處理中 = "processing"
    已完成 = "completed"
    已跳過 = "skipped"
    已取消 = "cancelled"
    失敗 = "failed"


class 任務優先級(Enum):
    緊急 = 10       # P0 - 系統級緊急
    高 = 8          # P1 - 高優先級
    正常 = 5        # P2 - 正常優先級
    低 = 3          # P3 - 低優先級
    最低 = 1        # P4 - 可延後


class 操作類型(Enum):
    創建 = "create"
    更新 = "update"
    完成 = "complete"
    跳過 = "skip"
    跳躍 = "jump"       # v2.0 新增: 跳躍式操作
    取消 = "cancel"
    重試 = "retry"
    刪除 = "delete"


# ============================================================
# 數據模型
# ============================================================

@dataclass
class 任務定義:
    """任務數據定義"""
    編號: str                          # 唯一編號
    標題: str                          # 任務標題
    描述: str = ""                     # 任務描述
    標籤: str = ""                     # 路由標籤 (assess/xpay/foundation/integrate/execute)
    狀態: 任務狀態 = field(default=任務狀態.待處理)
    優先級: 任務優先級 = field(default=任務優先級.正常)
    原始優先級: int = 5                 # 記錄原始優先級值
    衰減後優先級: float = 5.0           # 經過衰減計算後的優先級
    創建時間: str = ""
    更新時間: str = ""
    完成時間: str = ""
    執行智能體: str = ""               # 分配的AGENT編號
    去重哈希: str = ""                 # 去重哈希值
    跳躍歷史: List[str] = field(default_factory=list)  # v2.0 跳躍記錄
    元數據: Dict[str, Any] = field(default_factory=dict)
    DNA鏈: str = ""

    def __post_init__(self):
        if not self.創建時間:
            self.創建時間 = datetime.datetime.now().isoformat()
        if not self.更新時間:
            self.更新時間 = self.創建時間
        if not self.去重哈希:
            self.去重哈希 = self._計算去重哈希()
        if not self.DNA鏈:
            self.DNA鏈 = self._生成DNA()
        self.衰減後優先級 = float(self.優先級.value)

    def _計算去重哈希(self) -> str:
        """計算去重哈希 (基於標題+標籤)"""
        數據 = f"{self.標題}:{self.標籤}"
        return hashlib.md5(數據.encode()).hexdigest()[:12]

    def _生成DNA(self) -> str:
        """生成任務DNA鏈"""
        數據 = f"{self.編號}:{self.標題}:{self.創建時間}"
        return hashlib.sha256(數據.encode()).hexdigest()[:16]

    def 到字典(self) -> Dict:
        return {
            "編號": self.編號,
            "標題": self.標題,
            "描述": self.描述,
            "標籤": self.標籤,
            "狀態": self.狀態.value,
            "優先級": self.優先級.value,
            "原始優先級": self.原始優先級,
            "衰減後優先級": round(self.衰減後優先級, 2),
            "創建時間": self.創建時間,
            "更新時間": self.更新時間,
            "完成時間": self.完成時間,
            "執行智能體": self.執行智能體,
            "去重哈希": self.去重哈希,
            "跳躍歷史": self.跳躍歷史,
            "元數據": self.元數據,
            "DNA鏈": self.DNA鏈,
        }


@dataclass
class 任務統計:
    """任務統計數據"""
    總任務數: int = 0
    待處理數: int = 0
    處理中數: int = 0
    已完成數: int = 0
    已跳過數: int = 0
    已取消數: int = 0
    失敗數: int = 0
    去重次數: int = 0
    跳躍次數: int = 0
    平均處理時間分鐘: float = 0.0

    def 到字典(self) -> Dict:
        return asdict(self)


@dataclass
class 操作日誌:
    """操作日誌記錄"""
    時間戳: str
    操作: str
    任務編號: str
    操作前狀態: str = ""
    操作後狀態: str = ""
    備註: str = ""

    def 到字典(self) -> Dict:
        return asdict(self)


# ============================================================
# 優先級衰減算法
# ============================================================

class 優先級衰減器:
    """
    優先級衰減算法
    - 時間衰減: 任務在隊列中越久，優先級適當下降
    - 完成獎勵: 完成任務後提升後續相似任務優先級
    """

    def __init__(self, 衰減率: float = 默認優先級衰減率):
        self._衰減率 = 衰減率
        self._完成歷史: Dict[str, int] = {}  # 標籤 → 完成次數

    def 計算衰減優先級(self, 任務: 任務定義) -> float:
        """計算經過時間衰減後的優先級"""
        原始值 = float(任務.優先級.value)

        # 計算時間衰減
        try:
            創建時間 = datetime.datetime.fromisoformat(任務.創建時間)
            經過小時 = (datetime.datetime.now() - 創建時間).total_seconds() / 3600
            衰減因子 = self._衰減率 ** (經過小時 / 24)  # 每24小時衰減一次
        except:
            衰減因子 = 1.0

        # 完成獎勵因子
        獎勵因子 = 1.0
        if 任務.標籤 in self._完成歷史:
            獎勵因子 = 1.0 + (self._完成歷史[任務.標籤] * 0.02)  # 每次完成提升2%
            獎勵因子 = min(獎勵因子, 1.2)  # 最高20%獎勵

        return round(原始值 * 衰減因子 * 獎勵因子, 2)

    def 記錄完成(self, 標籤: str):
        """記錄任務完成，用於獎勵計算"""
        if 標籤 not in self._完成歷史:
            self._完成歷史[標籤] = 0
        self._完成歷史[標籤] += 1

    def 獲取獎勵歷史(self) -> Dict[str, int]:
        """獲取完成獎勵歷史"""
        return self._完成歷史.copy()


# ============================================================
# 去重引擎
# ============================================================

class 去重引擎:
    """
    自動去重機制
    - 基於標題+標籤的哈希去重
    - 支持時間窗口配置
    - 記錄去重歷史
    """

    def __init__(self, 窗口小時: int = 默認去重窗口小時):
        self._窗口小時 = 窗口小時
        self._去重登記簿: OrderedDict[str, datetime.datetime] = OrderedDict()
        self._去重次數 = 0

    def 檢查重複(self, 任務: 任務定義) -> Tuple[bool, Optional[str]]:
        """
        檢查任務是否重複
        返回: (是否重複, 原始任務編號)
        """
        當前時間 = datetime.datetime.now()

        # 清理過期條目
        self._清理過期條目(當前時間)

        # 檢查哈希是否已存在
        if 任務.去重哈希 in self._去重登記簿:
            self._去重次數 += 1
            return True, f"hash:{任務.去重哈希}"

        return False, None

    def 登記任務(self, 任務: 任務定義):
        """將任務登記到去重登記簿"""
        self._去重登記簿[任務.去重哈希] = datetime.datetime.now()

    def _清理過期條目(self, 當前時間: datetime.datetime):
        """清理超過窗口時間的條目"""
        過期密鑰 = []
        for 哈希, 時間 in self._去重登記簿.items():
            經過小時 = (當前時間 - 時間).total_seconds() / 3600
            if 經過小時 > self._窗口小時:
                過期密鑰.append(哈希)
        for 密鑰 in 過期密鑰:
            del self._去重登記簿[密鑰]

    def 獲取去重統計(self) -> Dict:
        """獲取去重統計"""
        return {
            "去重次數": self._去重次數,
            "登記簿大小": len(self._去重登記簿),
            "窗口小時": self._窗口小時,
        }

    def 清空登記簿(self):
        """清空去重登記簿"""
        self._去重登記簿.clear()


# ============================================================
# 任務管理器核心
# ============================================================

class 任務管理器v2:
    """
    任務管理器v2.0
    支持跳躍式操作、自動去重、優先級衰減
    """

    def __init__(self):
        self._任務倉庫: Dict[str, 任務定義] = {}
        self._隊列: List[str] = []           # 按優先級排序的任務編號隊列
        self._衰減器 = 優先級衰減器()
        self._去重器 = 去重引擎()
        self._統計 = 任務統計()
        self._操作日誌: List[操作日誌] = []
        self._配置 = {
            "最大隊列長": 默認最大隊列長,
            "並發數": 默認並發數,
            "去重窗口小時": 默認去重窗口小時,
            "優先級衰減率": 默認優先級衰減率,
            "啟用去重": True,
            "啟用衰減": True,
            "啟用跳躍": True,
        }
        self._序列號 = 0
        self._初始化時間 = datetime.datetime.now().isoformat()

    def 初始化(self, 配置: Dict = None) -> bool:
        """初始化任務管理器"""
        if 配置:
            self._配置.update(配置)
            self._衰減器 = 優先級衰減器(self._配置.get("優先級衰減率", 默認優先級衰減率))
            self._去重器 = 去重引擎(self._配置.get("去重窗口小時", 默認去重窗口小時))
        return True

    # ---- 核心操作 ----

    def 添加任務(self, 標題: str, 描述: str = "", 標籤: str = "",
               優先級: 任務優先級 = 任務優先級.正常, 元數據: Dict = None) -> Tuple[bool, str]:
        """
        添加新任務
        返回: (是否成功, 任務編號或錯誤消息)
        """
        # 檢查隊列長度
        if len(self._任務倉庫) >= self._配置["最大隊列長"]:
            return False, "隊列已滿"

        # 生成編號
        self._序列號 += 1
        編號 = f"TASK-{self._序列號:04d}"

        # 創建任務
        任務 = 任務定義(
            編號=編號,
            標題=標題,
            描述=描述,
            標籤=標籤,
            優先級=優先級,
            原始優先級=優先級.value,
            元數據=元數據 or {},
        )

        # 去重檢查
        if self._配置["啟用去重"]:
            是重複, _ = self._去重器.檢查重複(任務)
            if 是重複:
                self._統計.去重次數 += 1
                self._記錄日誌(操作類型.創建, 編號, "", "", "去重:任務已存在")
                return False, f"任務重複: {任務.去重哈希}"

            self._去重器.登記任務(任務)

        # 應用衰減
        if self._配置["啟用衰減"]:
            任務.衰減後優先級 = self._衰減器.計算衰減優先級(任務)

        # 存儲任務
        self._任務倉庫[編號] = 任務
        self._統計.總任務數 += 1
        self._統計.待處理數 += 1

        # 加入隊列並排序
        self._隊列.append(編號)
        self._重新排序隊列()

        self._記錄日誌(操作類型.創建, 編號, "", 任務狀態.待處理.value)

        return True, 編號

    def 獲取下一任務(self) -> Optional[任務定義]:
        """獲取隊列中下一個最高優先級的任務"""
        # 更新衰減優先級
        if self._配置["啟用衰減"]:
            for 編號 in self._隊列:
                任務 = self._任務倉庫.get(編號)
                if 任務 and 任務.狀態 == 任務狀態.待處理:
                    任務.衰減後優先級 = self._衰減器.計算衰減優先級(任務)
            self._重新排序隊列()

        for 編號 in self._隊列:
            任務 = self._任務倉庫.get(編號)
            if 任務 and 任務.狀態 == 任務狀態.待處理:
                任務.狀態 = 任務狀態.處理中
                任務.更新時間 = datetime.datetime.now().isoformat()
                self._統計.待處理數 -= 1
                self._統計.處理中數 += 1
                self._記錄日誌(操作類型.更新, 編號,
                             任務狀態.待處理.value, 任務狀態.處理中.value)
                return 任務
        return None

    def 完成任務(self, 編號: str, 結果: Dict = None) -> bool:
        """標記任務為已完成"""
        任務 = self._任務倉庫.get(編號)
        if not 任務:
            return False

        舊狀態 = 任務.狀態.value
        任務.狀態 = 任務狀態.已完成
        任務.完成時間 = datetime.datetime.now().isoformat()
        任務.更新時間 = 任務.完成時間

        if 結果:
            任務.元數據.update({"結果": 結果})

        self._統計.處理中數 -= 1
        self._統計.已完成數 += 1

        # 記錄完成用於獎勵
        if 任務.標籤:
            self._衰減器.記錄完成(任務.標籤)

        self._記錄日誌(操作類型.完成, 編號, 舊狀態, 任務狀態.已完成.value)
        return True

    # ---- 跳躍式操作 (v2.0 核心特性) ----

    def 跳躍操作(self, 目標編號: str, 來源編號: str = None,
               原因: str = "") -> Tuple[bool, str]:
        """
        跳躍式操作: 直接跳到指定任務
        - 支持從當前處理中的任務跳躍到另一任務
        - 記錄跳躍歷史
        - 自動調整優先級
        """
        if not self._配置["啟用跳躍"]:
            return False, "跳躍操作未啟用"

        目標任務 = self._任務倉庫.get(目標編號)
        if not 目標任務:
            return False, f"目標任務不存在: {目標編號}"

        # 如果有來源任務，記錄跳躍
        if 來源編號 and 來源編號 in self._任務倉庫:
            來源任務 = self._任務倉庫[來源編號]
            跳躍記錄 = f"{來源編號}→{目標編號}"
            目標任務.跳躍歷史.append(
                f"{跳躍記錄}@{datetime.datetime.now().isoformat()}:{原因}"
            )
            來源任務.跳躍歷史.append(
                f"跳至{目標編號}@{datetime.datetime.now().isoformat()}:{原因}"
            )

            # 將來源任務放回到待處理
            if 來源任務.狀態 == 任務狀態.處理中:
                來源任務.狀態 = 任務狀態.待處理
                self._統計.處理中數 -= 1
                self._統計.待處理數 += 1

        # 提升目標任務優先級
        目標任務.衰減後優先級 = min(目標任務.衰減後優先級 + 2, 10)
        目標任務.狀態 = 任務狀態.處理中
        目標任務.更新時間 = datetime.datetime.now().isoformat()

        self._統計.跳躍次數 += 1
        self._重新排序隊列()

        self._記錄日誌(操作類型.跳躍, 目標編號,
                     任務狀態.待處理.value, 任務狀態.處理中.value,
                     f"從{來源編號}跳躍:{原因}")

        return True, f"已跳躍到 {目標編號}"

    # ---- 其他操作 ----

    def 跳過任務(self, 編號: str, 原因: str = "") -> bool:
        """跳過指定任務"""
        任務 = self._任務倉庫.get(編號)
        if not 任務:
            return False

        舊狀態 = 任務.狀態.value
        任務.狀態 = 任務狀態.已跳過
        任務.更新時間 = datetime.datetime.now().isoformat()
        if 原因:
            任務.元數據["跳過原因"] = 原因

        if 舊狀態 == 任務狀態.待處理.value:
            self._統計.待處理數 -= 1
        elif 舊狀態 == 任務狀態.處理中.value:
            self._統計.處理中數 -= 1
        self._統計.已跳過數 += 1

        self._記錄日誌(操作類型.跳過, 編號, 舊狀態, 任務狀態.已跳過.value, 原因)
        return True

    def 取消任務(self, 編號: str, 原因: str = "") -> bool:
        """取消指定任務"""
        任務 = self._任務倉庫.get(編號)
        if not 任務:
            return False

        舊狀態 = 任務.狀態.value
        任務.狀態 = 任務狀態.已取消
        任務.更新時間 = datetime.datetime.now().isoformat()
        if 原因:
            任務.元數據["取消原因"] = 原因

        if 舊狀態 == 任務狀態.待處理.value:
            self._統計.待處理數 -= 1
        elif 舊狀態 == 任務狀態.處理中.value:
            self._統計.處理中數 -= 1
        self._統計.已取消數 += 1

        self._記錄日誌(操作類型.取消, 編號, 舊狀態, 任務狀態.已取消.value, 原因)
        return True

    def 重試任務(self, 編號: str) -> bool:
        """重試失敗的任務"""
        任務 = self._任務倉庫.get(編號)
        if not 任務:
            return False

        舊狀態 = 任務.狀態.value
        任務.狀態 = 任務狀態.待處理
        任務.更新時間 = datetime.datetime.now().isoformat()
        任務.衰減後優先級 = float(任務.優先級.value) + 1  # 重試時略升優先級

        if 舊狀態 == 任務狀態.失敗.value:
            self._統計.失敗數 -= 1
        self._統計.待處理數 += 1

        self._重新排序隊列()
        self._記錄日誌(操作類型.重試, 編號, 舊狀態, 任務狀態.待處理.value)
        return True

    # ---- 隊列管理 ----

    def _重新排序隊列(self):
        """按衰減後優先級重新排序隊列"""
        def 排序鍵(編號):
            任務 = self._任務倉庫.get(編號)
            if not 任務:
                return (0, "")
            # 待處理任務在前，按優先級降序
            if 任務.狀態 == 任務狀態.待處理:
                return (2, 任務.衰減後優先級)
            elif 任務.狀態 == 任務狀態.處理中:
                return (1, 任務.衰減後優先級)
            else:
                return (0, 0)

        self._隊列.sort(key=排序鍵, reverse=True)

    def 獲取隊列(self) -> List[任務定義]:
        """獲取當前隊列 (按優先級排序)"""
        return [self._任務倉庫[編號] for 編號 in self._隊列 if 編號 in self._任務倉庫]

    def 獲取待處理任務(self) -> List[任務定義]:
        """獲取所有待處理任務"""
        return [t for t in self._任務倉庫.values() if t.狀態 == 任務狀態.待處理]

    def 獲取任務(self, 編號: str) -> Optional[任務定義]:
        """獲取指定任務"""
        return self._任務倉庫.get(編號)

    # ---- 日誌與統計 ----

    def _記錄日誌(self, 操作: 操作類型, 任務編號: str,
                 操作前: str = "", 操作後: str = "", 備註: str = ""):
        """記錄操作日誌"""
        self._操作日誌.append(操作日誌(
            時間戳=datetime.datetime.now().isoformat(),
            操作=操作.value,
            任務編號=任務編號,
            操作前狀態=操作前,
            操作後狀態=操作後,
            備註=備註,
        ))

    def 獲取日誌(self, 任務編號: str = None) -> List[操作日誌]:
        """獲取操作日誌"""
        if 任務編號:
            return [log for log in self._操作日誌 if log.任務編號 == 任務編號]
        return self._操作日誌.copy()

    def 獲取統計(self) -> 任務統計:
        """獲取任務統計"""
        return self._統計

    # ---- 報告生成 ----

    def 生成報告(self) -> str:
        """生成任務管理報告"""
        統計 = self._統計
        報告 = []
        報告.append("=" * 60)
        報告.append(f"📋 {引擎名稱} v{版本號}")
        報告.append(f"DNA: {DNA標記}")
        報告.append("=" * 60)
        報告.append("")
        報告.append("📊 任務統計")
        報告.append(f"  總任務數:   {統計.總任務數}")
        報告.append(f"  ⏳ 待處理:   {統計.待處理數}")
        報告.append(f"  🔄 處理中:   {統計.處理中數}")
        報告.append(f"  ✅ 已完成:   {統計.已完成數}")
        報告.append(f"  ⏭️ 已跳過:   {統計.已跳過數}")
        報告.append(f"  🚫 已取消:   {統計.已取消數}")
        報告.append(f"  ❌ 失敗:     {統計.失敗數}")
        報告.append(f"  🦘 跳躍次數: {統計.跳躍次數}")
        報告.append(f"  🔄 去重次數: {統計.去重次數}")
        報告.append("")

        # 去重統計
        去重統計 = self._去重器.獲取去重統計()
        報告.append("🔄 去重引擎狀態")
        報告.append(f"  去重次數:     {去重統計['去重次數']}")
        報告.append(f"  登記簿大小:   {去重統計['登記簿大小']}")
        報告.append(f"  窗口大小:     {去重統計['窗口小時']}小時")
        報告.append("")

        # 獎勵歷史
        獎勵歷史 = self._衰減器.獲取獎勵歷史()
        if 獎勵歷史:
            報告.append("🏆 完成獎勵歷史")
            for 標籤, 次數 in 獎勵歷史.items():
                報告.append(f"  {標籤}: {次數}次完成")
            報告.append("")

        # 待處理任務列表
        待處理 = self.獲取待處理任務()
        if 待處理:
            報告.append("📋 待處理任務隊列 (按優先級排序)")
            for 任務 in sorted(待處理, key=lambda t: t.衰減後優先級, reverse=True):
                報告.append(
                    f"  [P{任務.優先級.value}] {任務.編號}: {任務.標題} "
                    f"(衰減優先級: {任務.衰減後優先級:.2f}) "
                    f"[{任務.標籤}]"
                )
            報告.append("")

        # 最近操作日誌
        報告.append("📝 最近操作日誌")
        for 日誌 in self._操作日誌[-10:]:
            報告.append(
                f"  [{日誌.時間戳[11:19]}] {日誌.操作} "
                f"{日誌.任務編號} {日誌.操作前狀態}→{日誌.操作後狀態}"
            )
            if 日誌.備註:
                報告.append(f"    備註: {日誌.備註}")
        報告.append("")

        報告.append("=" * 60)
        報告.append(f"初始化時間: {self._初始化時間}")
        報告.append("=" * 60)

        return "\n".join(報告)

    def 導出JSON(self) -> str:
        """導出所有數據為JSON"""
        數據 = {
            "系統": {
                "名稱": 引擎名稱,
                "版本": 版本號,
                "DNA": DNA標記,
                "初始化時間": self._初始化時間,
                "配置": self._配置,
            },
            "統計": self._統計.到字典(),
            "任務": {k: v.到字典() for k, v in self._任務倉庫.items()},
            "日誌": [log.到字典() for log in self._操作日誌],
            "去重統計": self._去重器.獲取去重統計(),
            "獎勵歷史": self._衰減器.獲取獎勵歷史(),
        }
        return json.dumps(數據, ensure_ascii=False, indent=2)


# ============================================================
# 命令行接口
# ============================================================

def 主函數():
    """命令行入口"""
    import sys

    if len(sys.argv) < 2:
        print("用法: python 任务管理器v2.py <命令> [選項]")
        print("")
        print("命令:")
        print("  add --title <標題> [--label <標籤>] [--priority <1-10>]")
        print("  next                    獲取下一個任務")
        print("  done <編號>             完成任務")
        print("  skip <編號> [--reason <原因>]")
        print("  jump <目標編號> [--from <來源編號>] [--reason <原因>]")
        print("  cancel <編號>           取消任務")
        print("  retry <編號>            重試任務")
        print("  list                    列出待處理任務")
        print("  report                  生成報告")
        print("  export                  導出JSON")
        sys.exit(1)

    命令 = sys.argv[1]
    管理器 = 任務管理器v2()
    管理器.初始化()

    if 命令 == "add":
        # 解析參數
        標題 = ""
        描述 = ""
        標籤 = ""
        優先級值 = 5
        i = 2
        while i < len(sys.argv):
            if sys.argv[i] == "--title" and i + 1 < len(sys.argv):
                標題 = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--desc" and i + 1 < len(sys.argv):
                描述 = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--label" and i + 1 < len(sys.argv):
                標籤 = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--priority" and i + 1 < len(sys.argv):
                優先級值 = int(sys.argv[i + 1])
                i += 2
            else:
                i += 1

        if not 標題:
            print("請提供任務標題 (--title)")
            sys.exit(1)

        優先級映射 = {
            10: 任務優先級.緊急, 9: 任務優先級.緊急,
            8: 任務優先級.高, 7: 任務優先級.高,
            5: 任務優先級.正常, 6: 任務優先級.正常,
            3: 任務優先級.低, 4: 任務優先級.低,
            1: 任務優先級.最低, 2: 任務優先級.最低,
        }
        優先級 = 優先級映射.get(優先級值, 任務優先級.正常)

        成功, 結果 = 管理器.添加任務(標題, 描述, 標籤, 優先級)
        if 成功:
            print(f"✅ 任務已添加: {結果}")
        else:
            print(f"❌ 添加失敗: {結果}")

    elif 命令 == "next":
        任務 = 管理器.獲取下一任務()
        if 任務:
            print(f"🎯 下一任務: {任務.編號}")
            print(f"   標題: {任務.標題}")
            print(f"   標籤: {任務.標籤}")
            print(f"   優先級: P{任務.優先級.value} (衰減後: {任務.衰減後優先級:.2f})")
        else:
            print("沒有待處理任務")

    elif 命令 == "done":
        if len(sys.argv) < 3:
            print("請提供任務編號")
            sys.exit(1)
        編號 = sys.argv[2]
        if 管理器.完成任務(編號):
            print(f"✅ 任務已完成: {編號}")
        else:
            print(f"❌ 任務不存在: {編號}")

    elif 命令 == "skip":
        if len(sys.argv) < 3:
            print("請提供任務編號")
            sys.exit(1)
        編號 = sys.argv[2]
        原因 = ""
        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "--reason" and i + 1 < len(sys.argv):
                原因 = sys.argv[i + 1]
                i += 2
            else:
                i += 1
        if 管理器.跳過任務(編號, 原因):
            print(f"⏭️ 任務已跳過: {編號}")
        else:
            print(f"❌ 任務不存在: {編號}")

    elif 命令 == "jump":
        if len(sys.argv) < 3:
            print("請提供目標任務編號")
            sys.exit(1)
        目標 = sys.argv[2]
        來源 = None
        原因 = ""
        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "--from" and i + 1 < len(sys.argv):
                來源 = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--reason" and i + 1 < len(sys.argv):
                原因 = sys.argv[i + 1]
                i += 2
            else:
                i += 1
        成功, 消息 = 管理器.跳躍操作(目標, 來源, 原因)
        if 成功:
            print(f"🦘 {消息}")
        else:
            print(f"❌ {消息}")

    elif 命令 == "cancel":
        if len(sys.argv) < 3:
            print("請提供任務編號")
            sys.exit(1)
        編號 = sys.argv[2]
        原因 = ""
        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "--reason" and i + 1 < len(sys.argv):
                原因 = sys.argv[i + 1]
                i += 2
            else:
                i += 1
        if 管理器.取消任務(編號, 原因):
            print(f"🚫 任務已取消: {編號}")
        else:
            print(f"❌ 任務不存在: {編號}")

    elif 命令 == "retry":
        if len(sys.argv) < 3:
            print("請提供任務編號")
            sys.exit(1)
        編號 = sys.argv[2]
        if 管理器.重試任務(編號):
            print(f"🔄 任務已重試: {編號}")
        else:
            print(f"❌ 任務不存在: {編號}")

    elif 命令 == "list":
        待處理 = 管理器.獲取待處理任務()
        if 待處理:
            print(f"待處理任務 ({len(待處理)}):")
            for 任務 in sorted(待處理, key=lambda t: t.衰減後優先級, reverse=True):
                print(f"  [P{任務.優先級.value}] {任務.編號}: {任務.標題}")
        else:
            print("沒有待處理任務")

    elif 命令 == "report":
        print(管理器.生成報告())

    elif 命令 == "export":
        print(管理器.導出JSON())

    else:
        print(f"未知命令: {命令}")


if __name__ == "__main__":
    主函數()
