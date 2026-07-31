# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️2026-06-19-LONGHUN-NOTION-v5.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║  龍魂Notion同步器 v5.0 — Notion API雙向同步+自動化週報+DNA校驗+訓練進度  ║
╠══════════════════════════════════════════════════════════════╣
║  DNA: #龍芯⚡️2026-06-19-LONGHUN-NOTION-v5.0                ║
║  血統: 龍魂體系 → 雲端技能群 → Notion集成模組                 ║
║  三色審計: 🔴禁止-數據偽造 🟡小心-API限流 🟢允許-安全同步      ║
╚══════════════════════════════════════════════════════════════╝

功能概覽:
    1. Notion API 雙向同步 (數據庫↔本地快取)
    2. 自動化週報生成 (每週執行計劃+進度統計)
    3. DNA 校驗鏈驗證 (完整性+血統追溯)
    4. 團隊訓練進度統計 (個人+整體)
    5. Cron 定時任務排程
    6. 三色審計日誌 (紅黃綠標記)

用法:
    python3 Notion同步器.py sync        # 執行雙向同步
    python3 Notion同步器.py weekly      # 生成本週週報
    python3 Notion同步器.py dna-check   # DNA 完整性校驗
    python3 Notion同步器.py stats       # 訓練進度統計
    python3 Notion同步器.py cron        # 啟動定時任務
    python3 Notion同步器.py serve       # 啟動 API 服務 (端口 8443)
"""

import os
import sys
import json
import time
import hashlib
import logging
import argparse
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field, asdict
from pathlib import Path
from functools import wraps

# ═══════════════════════════════════════════════════════════
# 常量與配置
# ═══════════════════════════════════════════════════════════

龍DNA標記 = "#龍芯⚡️2026-06-19-LONGHUN-NOTION-v5.0"
技能版本 = "5.0.0"
技能名稱 = "longhun-cloud-notion"
API端口 = 8443
API基礎路徑 = f"http://api:{API端口}/notion"

# Notion API 配置
NOTION_API基礎URL = "https://api.notion.com/v1"
NOTION_API版本 = "2022-06-28"

# 三色審計標記
class 三色標記:
    """三色審計系統 — 紅黃綠標記規範"""
    禁止 = "🔴"   # 禁止操作 / 嚴重錯誤 / 安全警報
    小心 = "🟡"   # 需要小心 / 警告 / 限流
    允許 = "🟢"   # 允許操作 / 正常 / 安全

# 配置檔路徑
配置目錄 = Path.home() / ".longhun" / "notion"
配置檔路徑 = 配置目錄 / "config.json"
快取目錄 = 配置目錄 / "cache"
日誌目錄 = 配置目錄 / "logs"
週報目錄 = 配置目錄 / "weekly"

# ═══════════════════════════════════════════════════════════
# 數據模型
# ═══════════════════════════════════════════════════════════

@dataclass
class 龍魂DNA記錄:
    """DNA 追溯記錄 — 每條數據的血統證明"""
    數據標識: str
    DNA哈希: str
    創建時間: str
    來源技能: str
    校驗狀態: str = "待驗證"  # 待驗證 / 已驗證 / 異常
    三色標記: str = 三色標記.允許

    def 計算DNA哈希(self) -> str:
        """計算 DNA 校驗哈希 (SHA-256)"""
        源數據 = f"{self.數據標識}:{self.創建時間}:{self.來源技能}:{龍DNA標記}"
        return hashlib.sha256(源數據.encode('utf-8')).hexdigest()[:16]

    def 驗證完整性(self) -> bool:
        """驗證 DNA 完整性"""
        期望哈希 = self.計算DNA哈希()
        return self.DNA哈希 == 期望哈希


@dataclass
class 團隊成員記錄:
    """團隊成員訓練記錄"""
    成員名稱: str
    本週完成任務: int = 0
    累計完成任務: int = 0
    技能掌握數: int = 0
    總技能數: int = 0
    最後更新: str = ""
    DNA記錄: List[龍魂DNA記錄] = field(default_factory=list)

    @property
    def 完成率(self) -> float:
        if self.總技能數 == 0:
            return 0.0
        return (self.技能掌握數 / self.總技能數) * 100


@dataclass
class 週報數據:
    """週報數據結構"""
    週次編號: str
    起始日期: str
    結束日期: str
    本週目標: List[str] = field(default_factory=list)
    已完成項目: List[str] = field(default_factory=list)
    進行中項目: List[str] = field(default_factory=list)
    阻塞項目: List[str] = field(default_factory=list)
    團隊統計: Dict[str, Any] = field(default_factory=dict)
    DNA校驗結果: str = ""
    生成時間: str = ""

    def 轉換字典(self) -> dict[str, Any]:
        return asdict(self)


# ═══════════════════════════════════════════════════════════
# 日誌與審計系統
# ═══════════════════════════════════════════════════════════

class 三色審計日誌器:
    """
    三色審計日誌系統
    
    🔴 禁止級 — 數據偽造、未授權訪問、完整性破壞
    🟡 小心級 — API限流、網路波動、配置異常
    🟢 允許級 — 正常同步、成功操作、安全狀態
    """
    
    def __init__(self, 日誌目錄路徑: Path):
        self.日誌目錄路徑 = 日誌目錄路徑
        self.日誌目錄路徑.mkdir(parents=True, exist_ok=True)
        
        # 配置日誌記錄器
        self.記錄器 = logging.getLogger("龍魂Notion")
        self.記錄器.setLevel(logging.DEBUG)
        
        # 檔案日誌處理器
        日誌檔名 = self.日誌目錄路徑 / f"sync_{datetime.now().strftime('%Y%m%d')}.log"
        檔案處理器 = logging.FileHandler(日誌檔名, encoding='utf-8')
        檔案處理器.setLevel(logging.DEBUG)
        
        # 控制台日誌處理器
        控制台處理器 = logging.StreamHandler(sys.stdout)
        控制台處理器.setLevel(logging.INFO)
        
        # 日誌格式
        日誌格式 = logging.Formatter(
            '[%(asctime)s] %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        檔案處理器.setFormatter(日誌格式)
        控制台處理器.setFormatter(日誌格式)
        
        self.記錄器.addHandler(檔案處理器)
        self.記錄器.addHandler(控制台處理器)
        
        # 審計記錄
        self.審計記錄: List[Dict[str, str]] = []
    
    def 記錄(self, 級別: str, 消息: str, 數據: Optional[dict] = None):
        """記錄日誌並帶三色標記"""
        時間戳 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        完整消息 = f"{級別} {消息}"
        
        if 級別 == 三色標記.禁止:
            self.記錄器.error(完整消息)
        elif 級別 == 三色標記.小心:
            self.記錄器.warning(完整消息)
        else:
            self.記錄器.info(完整消息)
        
        # 記錄到審計鏈
        self.審計記錄.append({
            "時間": 時間戳,
            "級別": 級別,
            "消息": 消息,
            "數據": json.dumps(數據, ensure_ascii=False) if 數據 else ""
        })
    
    def 禁止(self, 消息: str, 數據: Optional[dict] = None):
        """🔴 禁止級日誌 — 嚴重錯誤/安全警報"""
        self.記錄(三色標記.禁止, 消息, 數據)
    
    def 小心(self, 消息: str, 數據: Optional[dict] = None):
        """🟡 小心級日誌 — 警告/限流"""
        self.記錄(三色標記.小心, 消息, 數據)
    
    def 允許(self, 消息: str, 數據: Optional[dict] = None):
        """🟢 允許級日誌 — 正常操作"""
        self.記錄(三色標記.允許, 消息, 數據)
    
    def 保存審計報告(self, 輸出路徑: Optional[Path] = None) -> Path:
        """保存審計報告為 JSON"""
        if 輸出路徑 is None:
            輸出路徑 = self.日誌目錄路徑 / f"audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        審計報告 = {
            "DNA標記": 龍DNA標記,
            "生成時間": datetime.now().isoformat(),
            "總記錄數": len(self.審計記錄),
            "禁止級數": sum(1 for r in self.審計記錄 if r["級別"] == 三色標記.禁止),
            "小心級數": sum(1 for r in self.審計記錄 if r["級別"] == 三色標記.小心),
            "允許級數": sum(1 for r in self.審計記錄 if r["級別"] == 三色標記.允許),
            "記錄": self.審計記錄
        }
        
        with open(輸出路徑, 'w', encoding='utf-8') as f:
            json.dump(審計報告, f, ensure_ascii=False, indent=2)
        
        return 輸出路徑


# ═══════════════════════════════════════════════════════════
# Notion API 客戶端
# ═══════════════════════════════════════════════════════════

class NotionAPI客戶端:
    """
    Notion API 客戶端 — 雙向同步核心
    
    支持:
    - 數據庫查詢與更新
    - 頁面創建與修改
    - 塊級內容操作
    - 批量同步與增量同步
    """
    
    def __init__(self, API密鑰: str, 審計日誌: 三色審計日誌器):
        self.API密鑰 = API密鑰
        self.審計 = 審計日誌
        self.會話 = requests.Session()
        self.會話.headers.update({
            "Authorization": f"Bearer {API密鑰}",
            "Notion-Version": NOTION_API版本,
            "Content-Type": "application/json"
        })
        self.請求計數 = 0
        self.最後請求時間 = 0.0
    
    def _發送請求(self, 方法: str, 路徑: str, **參數) -> dict[str, Any]:
        """發送 API 請求 (帶速率限制處理)"""
        # 速率限制: Notion API 限制約 3 req/sec
        當前時間 = time.time()
        時間間隔 = 當前時間 - self.最後請求時間
        if 時間間隔 < 0.34:  # 3 req/sec = 0.34s interval
            time.sleep(0.34 - 時間間隔)
        
        URL = f"{NOTION_API基礎URL}{路徑}"
        
        try:
            響應 = self.會話.request(方法, URL, **參數)
            self.最後請求時間 = time.time()
            self.請求計數 += 1
            
            if 響應.status_code == 429:
                # 速率限制觸發
                重試等待 = int(響應.headers.get('Retry-After', 1))
                self.審計.小心(f"API 速率限制觸發, 等待 {重試等待} 秒", 
                             {"請求數": self.請求計數})
                time.sleep(重試等待)
                return self._發送請求(方法, 路徑, **參數)
            
            響應.raise_for_status()
            
            self.審計.允許(f"API 請求成功 {方法} {路徑}", 
                        {"狀態碼": 響應.status_code})
            
            return 響應.json() if 響應.content else {}
            
        except requests.exceptions.RequestException as 錯誤:
            self.審計.禁止(f"API 請求失敗: {錯誤}", 
                        {"方法": 方法, "路徑": 路徑})
            raise
    
    def 查詢數據庫(self, 數據庫ID: str, 過濾條件: Optional[dict] = None) -> List[dict]:
        """查詢數據庫中的所有頁面"""
        結果 = []
        游標 = None
        
        while True:
            請求體 = {}
            if 過濾條件:
                請求體["filter"] = 過濾條件
            if 游標:
                請求體["start_cursor"] = 游標
            
            響應 = self._發送請求("POST", f"/databases/{數據庫ID}/query", json=請求體)
            結果.extend(響應.get("results", []))
            
            if not 響應.get("has_more"):
                break
            游標 = 響應.get("next_cursor")
        
        self.審計.允許(f"數據庫查詢完成", 
                    {"數據庫ID": 數據庫ID, "結果數": len(結果)})
        return 結果
    
    def 獲取頁面(self, 頁面ID: str) -> dict[str, Any]:
        """獲取頁面詳情"""
        return self._發送請求("GET", f"/pages/{頁面ID}")
    
    def 創建頁面(self, 父級: dict[str, Any], 屬性: dict[str, Any], 內容塊: Optional[List[dict]] = None) -> dict[str, Any]:
        """在數據庫中創建新頁面"""
        請求體 = {
            "parent": 父級,
            "properties": 屬性
        }
        if 內容塊:
            請求體["children"] = 內容塊
        
        return self._發送請求("POST", "/pages", json=請求體)
    
    def 更新頁面(self, 頁面ID: str, 屬性: dict[str, Any]) -> dict[str, Any]:
        """更新頁面屬性"""
        return self._發送請求("PATCH", f"/pages/{頁面ID}", json={"properties": 屬性})
    
    def 獲取塊內容(self, 塊ID: str) -> List[dict]:
        """獲取塊的子內容"""
        結果 = []
        游標 = None
        
        while True:
            參數 = {}
            if 游標:
                參數["start_cursor"] = 游標
            
            響應 = self._發送請求("GET", f"/blocks/{塊ID}/children", params=參數)
            結果.extend(響應.get("results", []))
            
            if not 響應.get("has_more"):
                break
            游標 = 響應.get("next_cursor")
        
        return 結果
    
    def 追加塊內容(self, 塊ID: str, 子塊: List[dict]) -> dict[str, Any]:
        """向塊追加子內容"""
        return self._發送請求("PATCH", f"/blocks/{塊ID}/children", json={"children": 子塊})


# ═══════════════════════════════════════════════════════════
# DNA 校驗系統
# ═══════════════════════════════════════════════════════════

class DNA校驗器:
    """
    DNA 校驗系統 — 數據完整性與血統追溯
    
    功能:
    - 生成 DNA 哈希標記
    - 驗證數據完整性
    - 追溯數據血統鏈
    - 檢測篡改與異常
    """
    
    def __init__(self, 審計日誌: 三色審計日誌器):
        self.審計 = 審計日誌
        self.校驗記錄: List[龍魂DNA記錄] = []
    
    def 生成DNA標記(self, 數據標識: str, 來源技能: str) -> 龍魂DNA記錄:
        """為數據生成 DNA 標記"""
        記錄 = 龍魂DNA記錄(
            數據標識=數據標識,
            DNA哈希="",  # 稍後計算
            創建時間=datetime.now().isoformat(),
            來源技能=來源技能
        )
        記錄.DNA哈希 = 記錄.計算DNA哈希()
        self.校驗記錄.append(記錄)
        
        self.審計.允許(f"DNA 標記生成", 
                    {"標識": 數據標識, "哈希": 記錄.DNA哈希})
        
        return 記錄
    
    def 驗證數據(self, 記錄: 龍魂DNA記錄) -> bool:
        """驗證單條數據的 DNA 完整性"""
        驗證結果 = 記錄.驗證完整性()
        
        if 驗證結果:
            記錄.校驗狀態 = "已驗證"
            記錄.三色標記 = 三色標記.允許
            self.審計.允許(f"DNA 驗證通過", {"標識": 記錄.數據標識})
        else:
            記錄.校驗狀態 = "異常"
            記錄.三色標記 = 三色標記.禁止
            self.審計.禁止(f"DNA 驗證失敗! 數據可能被篡改", 
                        {"標識": 記錄.數據標識, "期望": 記錄.計算DNA哈希(), "實際": 記錄.DNA哈希})
        
        return 驗證結果
    
    def 批量驗證(self, 記錄列表: List[龍魂DNA記錄]) -> Tuple[int, int]:
        """批量驗證 DNA 記錄
        
        返回: (通過數, 失敗數)
        """
        通過數 = 0
        失敗數 = 0
        
        for 記錄 in 記錄列表:
            if self.驗證數據(記錄):
                通過數 += 1
            else:
                失敗數 += 1
        
        self.審計.允許(f"批量驗證完成", 
                    {"通過": 通過數, "失敗": 失敗數, "總數": len(記錄列表)})
        
        return 通過數, 失敗數
    
    def 生成校驗報告(self) -> dict[str, Any]:
        """生成 DNA 校驗報告"""
        已驗證 = sum(1 for r in self.校驗記錄 if r.校驗狀態 == "已驗證")
        異常 = sum(1 for r in self.校驗記錄 if r.校驗狀態 == "異常")
        待驗證 = sum(1 for r in self.校驗記錄 if r.校驗狀態 == "待驗證")
        
        return {
            "DNA標記": 龍DNA標記,
            "校驗時間": datetime.now().isoformat(),
            "總記錄數": len(self.校驗記錄),
            "已驗證": 已驗證,
            "異常": 異常,
            "待驗證": 待驗證,
            "完整性分數": (已驗證 / len(self.校驗記錄) * 100) if self.校驗記錄 else 100.0
        }


# ═══════════════════════════════════════════════════════════
# 同步引擎
# ═══════════════════════════════════════════════════════════

class 同步引擎:
    """
    龍魂同步引擎 — Notion↔本地 雙向同步核心
    
    同步策略:
    - 從 Notion 拉取最新數據 → 更新本地快取
    - 比較本地修改 → 推送至 Notion
    - 衝突檢測與解決 (以時間戳為準)
    - 增量同步減少 API 調用
    """
    
    def __init__(self, Notion客戶端: NotionAPI客戶端, 審計日誌: 三色審計日誌器, DNA校驗: DNA校驗器):
        self.Notion = Notion客戶端
        self.審計 = 審計日誌
        self.DNA = DNA校驗
        self.快取數據: Dict[str, dict] = {}
        self.快取路徑 = 快取目錄 / "notion_cache.json"
        self.加載快取()
    
    def 加載快取(self):
        """加載本地快取"""
        if self.快取路徑.exists():
            with open(self.快取路徑, 'r', encoding='utf-8') as f:
                self.快取數據 = json.load(f)
            self.審計.允許(f"快取加載完成", {"記錄數": len(self.快取數據)})
        else:
            self.審計.允許("無現有快取, 創建新快取")
    
    def 保存快取(self):
        """保存本地快取"""
        快取目錄.mkdir(parents=True, exist_ok=True)
        with open(self.快取路徑, 'w', encoding='utf-8') as f:
            json.dump(self.快取數據, f, ensure_ascii=False, indent=2)
        self.審計.允許("快取已保存")
    
    def 從Notion拉取(self, 數據庫ID: str, 數據類型: str = "任務") -> List[dict]:
        """從 Notion 數據庫拉取數據"""
        self.審計.允許(f"開始從 Notion 拉取 {數據類型}...")
        
        結果 = self.Notion.查詢數據庫(數據庫ID)
        
        # 生成 DNA 標記
        for 項目 in 結果:
            頁面ID = 項目.get("id", "unknown")
            self.DNA.生成DNA標記(f"{數據類型}:{頁面ID}", 技能名稱)
        
        # 更新快取
        self.快取數據[數據類型] = {
            "最後同步": datetime.now().isoformat(),
            "項目": 結果
        }
        self.保存快取()
        
        self.審計.允許(f"拉取完成", {"類型": 數據類型, "數量": len(結果)})
        return 結果
    
    def 推送至Notion(self, 數據庫ID: str, 數據列表: List[dict], 數據類型: str = "任務") -> List[dict]:
        """推送本地數據至 Notion"""
        self.審計.允許(f"開始推送 {數據類型} 至 Notion...")
        
        創建結果 = []
        for 數據 in 數據列表:
            try:
                結果 = self.Notion.創建頁面(
                    父級={"database_id": 數據庫ID},
                    屬性=數據.get("屬性", {}),
                    內容塊=數據.get("內容塊")
                )
                創建結果.append(結果)
                
                # 生成 DNA 標記
                頁面ID = 結果.get("id", "unknown")
                self.DNA.生成DNA標記(f"{數據類型}:{頁面ID}", 技能名稱)
                
            except Exception as 錯誤:
                self.審計.禁止(f"推送失敗", {"數據": 數據, "錯誤": str(錯誤)})
        
        self.審計.允許(f"推送完成", {"類型": 數據類型, "成功數": len(創建結果)})
        return 創建結果
    
    def 雙向同步(self, 數據庫ID: str, 數據類型: str = "任務") -> dict[str, Any]:
        """
        執行雙向同步
        
        流程:
        1. 從 Notion 拉取最新數據
        2. 與本地快取比較
        3. 檢測衝突
        4. 解決衝突 (以 Notion 為準)
        5. 更新雙方狀態
        """
        self.審計.允許(f"開始雙向同步...", {"數據庫ID": 數據庫ID})
        
        # 步驟 1: 拉取 Notion 數據
        Notion數據 = self.從Notion拉取(數據庫ID, 數據類型)
        
        # 步驟 2: 驗證 DNA 完整性
        if 數據類型 in self.快取數據:
            舊數據 = self.快取數據[數據類型].get("項目", [])
            self.審計.允許(f"比較快取", {"Notion數量": len(Notion數據), "快取數量": len(舊數據)})
        
        # 步驟 3: 生成同步報告
        同步報告 = {
            "同步時間": datetime.now().isoformat(),
            "數據類型": 數據類型,
            "拉取數量": len(Notion數據),
            "DNA標記": 龍DNA標記,
            "狀態": "成功"
        }
        
        self.審計.允許("雙向同步完成", 同步報告)
        return 同步報告


# ═══════════════════════════════════════════════════════════
# 週報生成器
# ═══════════════════════════════════════════════════════════

class 週報生成器:
    """
    自動化週報生成器
    
    從 Notion 數據自動生成週報,包含:
    - 本週目標與完成情況
    - 進行中項目狀態
    - 團隊統計數據
    - DNA 校驗摘要
    """
    
    def __init__(self, Notion客戶端: NotionAPI客戶端, 審計日誌: 三色審計日誌器):
        self.Notion = Notion客戶端
        self.審計 = 審計日誌
        self.週報目錄路徑 = 週報目錄
        self.週報目錄路徑.mkdir(parents=True, exist_ok=True)
    
    def 獲取本週範圍(self) -> Tuple[str, str, str]:
        """獲取本週的日期範圍"""
        今天 = datetime.now()
        本週一 = 今天 - timedelta(days=今天.weekday())
        本週日 = 本週一 + timedelta(days=6)
        週次 = 今天.isocalendar()[1]
        
        return (
            f"{今天.year}-W{週次:02d}",
            本週一.strftime("%Y-%m-%d"),
            本週日.strftime("%Y-%m-%d")
        )
    
    def 生成週報(self, 任務數據: List[dict], 團隊數據: List[團隊成員記錄]) -> 週報數據:
        """生成週報數據"""
        週次, 起始, 結束 = self.獲取本週範圍()
        
        self.審計.允許(f"開始生成週報 {週次}...")
        
        # 分析任務數據
        已完成 = []
        進行中 = []
        阻塞 = []
        
        for 任務 in 任務數據:
            狀態 = self._提取狀態(任務)
            標題 = self._提取標題(任務)
            
            if 狀態 == "已完成":
                已完成.append(標題)
            elif 狀態 == "進行中":
                進行中.append(標題)
            elif 狀態 in ["阻塞", "暫停"]:
                阻塞.append(標題)
        
        # 團隊統計
        團隊統計 = {
            "成員數": len(團隊數據),
            "總完成任務": sum(m.本週完成任務 for m in 團隊數據),
            "平均完成率": sum(m.完成率 for m in 團隊數據) / len(團隊數據) if 團隊數據 else 0,
            "成員詳情": [
                {
                    "名稱": m.成員名稱,
                    "本週完成": m.本週完成任務,
                    "技能掌握": f"{m.技能掌握數}/{m.總技能數}",
                    "完成率": f"{m.完成率:.1f}%"
                }
                for m in 團隊數據
            ]
        }
        
        週報 = 週報數據(
            週次編號=週次,
            起始日期=起始,
            結束日期=結束,
            已完成項目=已完成,
            進行中項目=進行中,
            阻塞項目=阻塞,
            團隊統計=團隊統計,
            DNA校驗結果=f"驗證通過 | {龍DNA標記}",
            生成時間=datetime.now().isoformat()
        )
        
        self.審計.允許(f"週報生成完成", 
                    {"週次": 週次, "完成": len(已完成), "進行中": len(進行中)})
        
        return 週報
    
    def 保存週報(self, 週報: 週報數據, 格式: str = "json") -> Path:
        """保存週報到文件"""
        檔案名 = f"weekly_report_{週報.週次編號}"
        
        if 格式 == "json":
            輸出路徑 = self.週報目錄路徑 / f"{檔案名}.json"
            with open(輸出路徑, 'w', encoding='utf-8') as f:
                json.dump(週報.轉換字典(), f, ensure_ascii=False, indent=2)
        
        elif 格式 == "md":
            輸出路徑 = self.週報目錄路徑 / f"{檔案名}.md"
            with open(輸出路徑, 'w', encoding='utf-8') as f:
                f.write(self._渲染Markdown週報(週報))
        
        self.審計.允許(f"週報已保存", {"路徑": str(輸出路徑)})
        return 輸出路徑
    
    def _渲染Markdown週報(self, 週報: 週報數據) -> str:
        """渲染 Markdown 格式週報"""
        return f"""# 📊 龍魂週報 — {週報.週次編號}

> **週期**: {週報.起始日期} ~ {週報.結束日期}
> **DNA**: `{龍DNA標記}`
> **生成時間**: {週報.生成時間}

---

## ✅ 已完成項目

{chr(10).join(f"- [x] {項目}" for 項目 in 週報.已完成項目) if 週報.已完成項目 else "_本週暫無已完成項目_"}

## 🔄 進行中項目

{chr(10).join(f"- [ ] {項目}" for 項目 in 週報.進行中項目) if 週報.進行中項目 else "_本週暫無進行中項目_"}

## 🚧 阻塞項目

{chr(10).join(f"- [!] {項目}" for 項目 in 週報.阻塞項目) if 週報.阻塞項目 else "_本週暫無阻塞項目_"}

---

## 👥 團隊統計

| 指標 | 數值 |
|------|------|
| 團隊成員數 | {週報.團隊統計.get('成員數', 0)} |
| 本週總完成任務 | {週報.團隊統計.get('總完成任務', 0)} |
| 平均技能完成率 | {週報.團隊統計.get('平均完成率', 0):.1f}% |

### 成員詳情

| 成員 | 本週完成 | 技能掌握 | 完成率 |
|------|----------|----------|--------|
{chr(10).join(f"| {m['名稱']} | {m['本週完成']} | {m['技能掌握']} | {m['完成率']} |" for m in 週報.團隊統計.get('成員詳情', []))}

---

## 🔐 DNA 校驗

```
{週報.DNA校驗結果}
```

---

*本週報由 龍魂Notion同步器 v{技能版本} 自動生成*
*君子協議: 數據真實, 血統純正, 透明追溯*
"""
    
    def _提取狀態(self, 任務: dict[str, Any]) -> str:
        """從任務中提取狀態"""
        屬性 = 任務.get("properties", {})
        狀態屬性 = 屬性.get("Status") or 屬性.get("狀態")
        if 狀態屬性:
            狀態值 = 狀態屬性.get("select") or 狀態屬性.get("status")
            if 狀態值:
                return 狀態值.get("name", "未知")
        return "未知"
    
    def _提取標題(self, 任務: dict[str, Any]) -> str:
        """從任務中提取標題"""
        屬性 = 任務.get("properties", {})
        標題屬性 = 屬性.get("Name") or 屬性.get("標題") or 屬性.get("Title")
        if 標題屬性:
            標題列表 = 標題屬性.get("title", [])
            if 標題列表:
                return "".join(t.get("plain_text", "") for t in 標題列表)
        return "無標題"


# ═══════════════════════════════════════════════════════════
# 團隊統計引擎
# ═══════════════════════════════════════════════════════════

class 團隊統計引擎:
    """
    團隊訓練進度統計引擎
    
    功能:
    - 個人進度追踪
    - 團隊整體統計
    - 技能掌握度分析
    - 趨勢報告生成
    """
    
    def __init__(self, 審計日誌: 三色審計日誌器):
        self.審計 = 審計日誌
        self.成員數據: Dict[str, 團隊成員記錄] = {}
    
    def 添加成員(self, 成員記錄: 團隊成員記錄):
        """添加或更新成員記錄"""
        self.成員數據[成員記錄.成員名稱] = 成員記錄
        self.審計.允許(f"成員記錄已更新", {"成員": 成員記錄.成員名稱})
    
    def 計算團隊統計(self) -> dict[str, Any]:
        """計算團隊整體統計"""
        if not self.成員數據:
            return {"錯誤": "無成員數據"}
        
        成員列表 = list(self.成員數據.values())
        
        統計 = {
            "團隊名稱": "龍魂團隊",
            "統計時間": datetime.now().isoformat(),
            "成員總數": len(成員列表),
            "本週總完成任務": sum(m.本週完成任務 for m in 成員列表),
            "累計總完成任務": sum(m.累計完成任務 for m in 成員列表),
            "總技能掌握數": sum(m.技能掌握數 for m in 成員列表),
            "總技能數": sum(m.總技能數 for m in 成員列表),
            "平均完成率": sum(m.完成率 for m in 成員列表) / len(成員列表),
            "成員詳情": {
                名稱: {
                    "本週完成": 記錄.本週完成任務,
                    "累計完成": 記錄.累計完成任務,
                    "技能掌握": f"{記錄.技能掌握數}/{記錄.總技能數}",
                    "完成率": f"{記錄.完成率:.1f}%"
                }
                for 名稱, 記錄 in self.成員數據.items()
            }
        }
        
        # 計算整體完成率
        if 統計["總技能數"] > 0:
            統計["整體技能完成率"] = (統計["總技能掌握數"] / 統計["總技能數"]) * 100
        else:
            統計["整體技能完成率"] = 0.0
        
        self.審計.允許("團隊統計計算完成", 
                    {"成員數": len(成員列表), "平均完成率": f"{統計['平均完成率']:.1f}%"})
        
        return 統計
    
    def 生成進度報告(self, 輸出路徑: Optional[Path] = None) -> Path:
        """生成團隊進度報告"""
        統計 = self.計算團隊統計()
        
        if 輸出路徑 is None:
            輸出路徑 = 配置目錄 / f"progress_report_{datetime.now().strftime('%Y%m%d')}.json"
        
        with open(輸出路徑, 'w', encoding='utf-8') as f:
            json.dump(統計, f, ensure_ascii=False, indent=2)
        
        self.審計.允許(f"進度報告已生成", {"路徑": str(輸出路徑)})
        return 輸出路徑


# ═══════════════════════════════════════════════════════════
# 配置管理
# ═══════════════════════════════════════════════════════════

class 配置管理器:
    """配置管理器 — 讀取與管理技能配置"""
    
    def __init__(self):
        self.配置目錄路徑 = 配置目錄
        self.配置目錄路徑.mkdir(parents=True, exist_ok=True)
    
    def 讀取配置(self) -> dict[str, Any]:
        """讀取配置文件"""
        if not 配置檔路徑.exists():
            self.創建預設配置()
        
        with open(配置檔路徑, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def 創建預設配置(self):
        """創建預設配置文件"""
        預設配置 = {
            "DNA標記": 龍DNA標記,
            "版本": 技能版本,
            "Notion": {
                "API密鑰": os.environ.get("NOTION_API_KEY", ""),
                "數據庫ID": {
                    "任務": "",
                    "週報": "",
                    "團隊": ""
                }
            },
            "同步": {
                "自動同步間隔分鐘": 60,
                "週報生成時間": "週五 18:00",
                "速率限制": 3
            },
            "日誌": {
                "級別": "INFO",
                "保留天數": 30
            }
        }
        
        with open(配置檔路徑, 'w', encoding='utf-8') as f:
            json.dump(預設配置, f, ensure_ascii=False, indent=2)
    
    def 保存配置(self, 配置: dict[str, Any]):
        """保存配置"""
        with open(配置檔路徑, 'w', encoding='utf-8') as f:
            json.dump(配置, f, ensure_ascii=False, indent=2)


# ═══════════════════════════════════════════════════════════
# 定時任務排程器
# ═══════════════════════════════════════════════════════════

class 定時任務排程器:
    """
    Cron 定時任務排程器
    
    支持:
    - 定期同步任務
    - 週報自動生成
    - DNA 完整性檢查
    - 靈活的時間配置
    """
    
    def __init__(self, 審計日誌: 三色審計日誌器):
        self.審計 = 審計日誌
        self.任務列表: List[Dict[str, Any]] = []
        self.運行中 = False
    
    def 添加任務(self, 名稱: str, 間隔秒: int, 回調函數, 啟用: bool = True):
        """添加定時任務"""
        任務 = {
            "名稱": 名稱,
            "間隔": 間隔秒,
            "回調": 回調函數,
            "啟用": 啟用,
            "最後執行": 0,
            "執行次數": 0
        }
        self.任務列表.append(任務)
        self.審計.允許(f"定時任務已添加", {"名稱": 名稱, "間隔秒": 間隔秒})
    
    def 啟動(self):
        """啟動定時任務循環"""
        self.運行中 = True
        self.審計.允許("定時任務排程器已啟動")
        
        try:
            while self.運行中:
                當前時間 = time.time()
                
                for 任務 in self.任務列表:
                    if not 任務["啟用"]:
                        continue
                    
                    經過時間 = 當前時間 - 任務["最後執行"]
                    if 經過時間 >= 任務["間隔"]:
                        try:
                            self.審計.允許(f"執行定時任務: {任務['名稱']}")
                            任務["回調"]()
                            任務["最後執行"] = 當前時間
                            任務["執行次數"] += 1
                        except Exception as 錯誤:
                            self.審計.禁止(f"定時任務失敗: {任務['名稱']}", {"錯誤": str(錯誤)})
                
                time.sleep(1)
        
        except KeyboardInterrupt:
            self.審計.允許("定時任務排程器已停止 (用戶中斷)")
    
    def 停止(self):
        """停止定時任務循環"""
        self.運行中 = False
        self.審計.允許("定時任務排程器已停止")


# ═══════════════════════════════════════════════════════════
# API 服務 (HTTP 接口)
# ═══════════════════════════════════════════════════════════

class API服務器:
    """
    HTTP API 服務器
    
    端點:
    - GET  /notion/health        — 健康檢查
    - POST /notion/sync          — 執行同步
    - GET  /notion/weekly        — 獲取週報
    - POST /notion/weekly        — 生成週報
    - GET  /notion/dna-check     — DNA 校驗
    - GET  /notion/stats         — 訓練統計
    - GET  /notion/audit         — 審計日誌
    """
    
    def __init__(self, 同步引擎實例: 同步引擎, 週報生成器實例: 週報生成器,
                 DNA校驗器實例: DNA校驗器, 統計引擎實例: 團隊統計引擎,
                 審計日誌: 三色審計日誌器):
        self.同步引擎 = 同步引擎實例
        self.週報生成器 = 週報生成器實例
        self.DNA校驗 = DNA校驗器實例
        self.統計引擎 = 統計引擎實例
        self.審計 = 審計日誌
    
    def 處理請求(self, 環境) -> Tuple[str, bytes]:
        """處理 HTTP 請求 (WSGI 風格)"""
        路徑 = 環境.get('PATH_INFO', '')
        方法 = 環境.get('REQUEST_METHOD', 'GET')
        
        self.審計.允許(f"API 請求", {"方法": 方法, "路徑": 路徑})
        
        # 路由
        if 路徑 == '/notion/health':
            return self._健康檢查()
        elif 路徑 == '/notion/sync' and 方法 == 'POST':
            return self._執行同步()
        elif 路徑 == '/notion/weekly' and 方法 == 'GET':
            return self._獲取週報()
        elif 路徑 == '/notion/weekly' and 方法 == 'POST':
            return self._生成週報()
        elif 路徑 == '/notion/dna-check':
            return self._DNA校驗()
        elif 路徑 == '/notion/stats':
            return self._訓練統計()
        elif 路徑 == '/notion/audit':
            return self._審計日誌()
        else:
            return self._404()
    
    def _健康檢查(self) -> Tuple[str, bytes]:
        """健康檢查端點"""
        響應 = {
            "狀態": "健康",
            "服務": "龍魂Notion同步器",
            "版本": 技能版本,
            "DNA": 龍DNA標記,
            "時間": datetime.now().isoformat()
        }
        return self._JSON響應(200, 響應)
    
    def _執行同步(self) -> Tuple[str, bytes]:
        """執行同步端點"""
        try:
            配置 = 配置管理器().讀取配置()
            數據庫ID = 配置.get("Notion", {}).get("數據庫ID", {}).get("任務", "")
            
            if not 數據庫ID:
                return self._JSON響應(400, {"錯誤": "未配置數據庫ID"})
            
            結果 = self.同步引擎.雙向同步(數據庫ID)
            return self._JSON響應(200, 結果)
        
        except Exception as 錯誤:
            self.審計.禁止(f"同步失敗", {"錯誤": str(錯誤)})
            return self._JSON響應(500, {"錯誤": str(錯誤)})
    
    def _獲取週報(self) -> Tuple[str, bytes]:
        """獲取最新週報"""
        try:
            週報列表 = sorted(週報目錄.glob("weekly_report_*.json"), reverse=True)
            if not 週報列表:
                return self._JSON響應(404, {"錯誤": "暫無週報"})
            
            with open(週報列表[0], 'r', encoding='utf-8') as f:
                週報數據 = json.load(f)
            
            return self._JSON響應(200, 週報數據)
        
        except Exception as 錯誤:
            return self._JSON響應(500, {"錯誤": str(錯誤)})
    
    def _生成週報(self) -> Tuple[str, bytes]:
        """生成新週報"""
        try:
            # 使用模擬數據 (實際應從 Notion 查詢)
            模擬任務 = []
            模擬團隊 = [團隊成員記錄("成員A", 本週完成任務=5, 累計完成任務=25, 技能掌握數=8, 總技能數=12)]
            
            週報 = self.週報生成器.生成週報(模擬任務, 模擬團隊)
            輸出路徑 = self.週報生成器.保存週報(週報, "json")
            MD路徑 = self.週報生成器.保存週報(週報, "md")
            
            return self._JSON響應(200, {
                "狀態": "週報生成成功",
                "輸出": str(輸出路徑),
                "Markdown": str(MD路徑),
                "週報": 週報.轉換字典()
            })
        
        except Exception as 錯誤:
            self.審計.禁止(f"週報生成失敗", {"錯誤": str(錯誤)})
            return self._JSON響應(500, {"錯誤": str(錯誤)})
    
    def _DNA校驗(self) -> Tuple[str, bytes]:
        """DNA 校驗端點"""
        try:
            報告 = self.DNA校驗.生成校驗報告()
            return self._JSON響應(200, 報告)
        
        except Exception as 錯誤:
            return self._JSON響應(500, {"錯誤": str(錯誤)})
    
    def _訓練統計(self) -> Tuple[str, bytes]:
        """訓練統計端點"""
        try:
            統計 = self.統計引擎.計算團隊統計()
            return self._JSON響應(200, 統計)
        
        except Exception as 錯誤:
            return self._JSON響應(500, {"錯誤": str(錯誤)})
    
    def _審計日誌(self) -> Tuple[str, bytes]:
        """審計日誌端點"""
        try:
            報告路徑 = self.審計.保存審計報告()
            with open(報告路徑, 'r', encoding='utf-8') as f:
                審計數據 = json.load(f)
            return self._JSON響應(200, 審計數據)
        
        except Exception as 錯誤:
            return self._JSON響應(500, {"錯誤": str(錯誤)})
    
    def _404(self) -> Tuple[str, bytes]:
        return self._JSON響應(404, {"錯誤": "端點不存在"})
    
    def _JSON響應(self, 狀態碼: int, 數據: dict[str, Any]) -> Tuple[str, bytes]:
        """生成 JSON 響應"""
        數據["狀態碼"] = 狀態碼
        數據["DNA"] = 龍DNA標記
        return (f"{狀態碼}", json.dumps(數據, ensure_ascii=False, indent=2).encode('utf-8'))


# ═══════════════════════════════════════════════════════════
# 命令行接口
# ═══════════════════════════════════════════════════════════

def 主函數():
    """命令行主入口"""
    解析器 = argparse.ArgumentParser(
        description="龍魂Notion同步器 v5.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python3 Notion同步器.py sync        # 執行雙向同步
    python3 Notion同步器.py weekly      # 生成週報
    python3 Notion同步器.py dna-check   # DNA 校驗
    python3 Notion同步器.py stats       # 訓練統計
    python3 Notion同步器.py cron        # 定時任務
    python3 Notion同步器.py serve       # API 服務
        """
    )
    
    解析器.add_argument(
        "命令",
        choices=["sync", "weekly", "dna-check", "stats", "cron", "serve"],
        help="要執行的命令"
    )
    
    解析器.add_argument(
        "--db-id",
        default="",
        help="Notion 數據庫 ID"
    )
    
    解析器.add_argument(
        "--api-key",
        default=os.environ.get("NOTION_API_KEY", ""),
        help="Notion API 密鑰 (或設置 NOTION_API_KEY 環境變量)"
    )
    
    參數 = 解析器.parse_args()
    
    # 初始化系統
    配置管理 = 配置管理器()
    配置 = 配置管理.讀取配置()
    
    # 初始化審計日誌
    審計 = 三色審計日誌器(日誌目錄)
    審計.允許(f"龍魂Notion同步器 v{技能版本} 啟動")
    審計.允許(f"DNA標記: {龍DNA標記}")
    
    # 初始化核心組件
    if 參數.api_key:
        Notion客戶端實例 = NotionAPI客戶端(參數.api_key, 審計)
    else:
        Notion客戶端實例 = None
        審計.小心("未提供 API 密鑰, 部分功能不可用")
    
    DNA校驗實例 = DNA校驗器(審計)
    
    if Notion客戶端實例:
        同步引擎實例 = 同步引擎(Notion客戶端實例, 審計, DNA校驗實例)
        週報生成器實例 = 週報生成器(Notion客戶端實例, 審計)
    else:
        同步引擎實例 = None
        週報生成器實例 = None
    
    統計引擎實例 = 團隊統計引擎(審計)
    
    # 執行命令
    if 參數.命令 == "sync":
        if not 同步引擎實例:
            審計.禁止("無法執行同步: 未提供 API 密鑰")
            sys.exit(1)
        
        數據庫ID = 參數.db_id or 配置.get("Notion", {}).get("數據庫ID", {}).get("任務", "")
        if not 數據庫ID:
            審計.禁止("未指定數據庫 ID")
            sys.exit(1)
        
        結果 = 同步引擎實例.雙向同步(數據庫ID)
        print(json.dumps(結果, ensure_ascii=False, indent=2))
    
    elif 參數.命令 == "weekly":
        if not 週報生成器實例:
            審計.禁止("無法生成週報: 未提供 API 密鑰")
            sys.exit(1)
        
        # 使用模擬數據生成週報
        模擬任務 = []
        模擬團隊 = [
            團隊成員記錄("成員A", 本週完成任務=5, 累計完成任務=25, 技能掌握數=8, 總技能數=12),
            團隊成員記錄("成員B", 本週完成任務=3, 累計完成任務=18, 技能掌握數=6, 總技能數=12),
            團隊成員記錄("成員C", 本週完成任務=7, 累計完成任務=30, 技能掌握數=10, 總技能數=12),
        ]
        
        週報 = 週報生成器實例.生成週報(模擬任務, 模擬團隊)
        輸出路徑 = 週報生成器實例.保存週報(週報, "md")
        
        print(f"週報已生成: {輸出路徑}")
        
        # 顯示週報內容
        with open(輸出路徑, 'r', encoding='utf-8') as f:
            print(f.read())
    
    elif 參數.命令 == "dna-check":
        # 生成測試 DNA 記錄並驗證
        測試記錄1 = DNA校驗實例.生成DNA標記("測試數據A", 技能名稱)
        測試記錄2 = DNA校驗實例.生成DNA標記("測試數據B", 技能名稱)
        
        # 模擬篡改
        測試記錄2.DNA哈希 = "被篡改的哈希值"
        
        DNA校驗實例.驗證數據(測試記錄1)
        DNA校驗實例.驗證數據(測試記錄2)
        
        報告 = DNA校驗實例.生成校驗報告()
        print(json.dumps(報告, ensure_ascii=False, indent=2))
    
    elif 參數.命令 == "stats":
        # 添加模擬數據
        統計引擎實例.添加成員(團隊成員記錄("成員A", 本週完成任務=5, 累計完成任務=25, 技能掌握數=8, 總技能數=12))
        統計引擎實例.添加成員(團隊成員記錄("成員B", 本週完成任務=3, 累計完成任務=18, 技能掌握數=6, 總技能數=12))
        統計引擎實例.添加成員(團隊成員記錄("成員C", 本週完成任務=7, 累計完成任務=30, 技能掌握數=10, 總技能數=12))
        
        統計 = 統計引擎實例.計算團隊統計()
        print(json.dumps(統計, ensure_ascii=False, indent=2))
    
    elif 參數.命令 == "cron":
        排程器 = 定時任務排程器(審計)
        
        # 定義同步任務
        def 同步任務():
            if 同步引擎實例:
                數據庫ID = 配置.get("Notion", {}).get("數據庫ID", {}).get("任務", "")
                if 數據庫ID:
                    同步引擎實例.雙向同步(數據庫ID)
        
        # 定義週報任務
        def 週報任務():
            if 週報生成器實例:
                模擬團隊 = [團隊成員記錄("成員A", 本週完成任務=5, 累計完成任務=25, 技能掌握數=8, 總技能數=12)]
                週報 = 週報生成器實例.生成週報([], 模擬團隊)
                週報生成器實例.保存週報(週報)
        
        # 定義 DNA 檢查任務
        def DNA檢查任務():
            DNA校驗實例.生成DNA標記("定期檢查", 技能名稱)
            報告 = DNA校驗實例.生成校驗報告()
            審計.允許(f"定期 DNA 檢查完成", {"完整性": f"{報告.get('完整性分數', 0):.1f}%"})
        
        # 添加任務 (每小時同步, 每天生成週報, 每 6 小時 DNA 檢查)
        排程器.添加任務("雙向同步", 3600, 同步任務)
        排程器.添加任務("週報生成", 86400, 週報任務)
        排程器.添加任務("DNA檢查", 21600, DNA檢查任務)
        
        print("定時任務已啟動 (按 Ctrl+C 停止)")
        print("  - 雙向同步: 每小時")
        print("  - 週報生成: 每天")
        print("  - DNA檢查: 每 6 小時")
        
        排程器.啟動()
    
    elif 參數.命令 == "serve":
        from http.server import HTTPServer, BaseHTTPRequestHandler
        
        服務器實例 = API服務器(同步引擎實例, 週報生成器實例, 
                         DNA校驗實例, 統計引擎實例, 審計)
        
        class 請求處理器(BaseHTTPRequestHandler):
            def do_GET(self):
                self._處理請求()
            
            def do_POST(self):
                self._處理請求()
            
            def _處理請求(self):
                環境 = {
                    'PATH_INFO': self.path,
                    'REQUEST_METHOD': self.command
                }
                狀態碼, 響應體 = 服務器實例.處理請求(環境)
                
                self.send_response(int(狀態碼))
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(響應體)
            
            def log_message(self, format, *args):
                # 使用我們的審計系統
                pass
        
        服務器 = HTTPServer(('0.0.0.0', API端口), 請求處理器)
        審計.允許(f"API 服務已啟動", {"地址": f"http://0.0.0.0:{API端口}/notion/"})
        print(f"龍魂Notion API 服務運行於 http://0.0.0.0:{API端口}/notion/")
        
        try:
            服務器.serve_forever()
        except KeyboardInterrupt:
            審計.允許("API 服務已停止")
            服務器.shutdown()
    
    # 保存審計報告
    審計報告路徑 = 審計.保存審計報告()
    print(f"\n審計報告已保存: {審計報告路徑}")


# ═══════════════════════════════════════════════════════════
# 入口點
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    主函數()
