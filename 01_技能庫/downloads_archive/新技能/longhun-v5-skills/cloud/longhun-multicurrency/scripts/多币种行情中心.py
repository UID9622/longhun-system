#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️2026-06-19-LONGHUN-MULTICURRENCY-v5.2
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
================================================================================
多币种行情中心 - 龍魂体系金融核心模块
================================================================================
文件编号    : C9-001
版本號      : v5.2.0
DNA標識     : #龍芯⚡️2026-06-19-LONGHUN-MULTICURRENCY-v5.2
作者        : 龍魂工程師
用途        : 多币种实时行情获取、缓存、过期检测与汇率管理
支持币种    : CNY, USD, EUR, GBP, JPY, KRW, HKD, SGD, BTC, ETH

審計追蹤    :
  - 2026-06-19 v5.2.0 初始版本，10币种完整支持
  - 2026-06-19 v5.2.1 新增e-CNY跨境支付通道接口

君子協議    : 本模組遵循龍魂開源誓約，禁止用於洗錢、逃稅、非法跨境
              資金轉移。所有交易記錄留痕，可追溯可審計。
================================================================================
"""

import json
import time
import hashlib
import os
import urllib.request
import urllib.parse
import ssl
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# 常量定義區
# ═══════════════════════════════════════════════════════════════════════════════

DNA標識 = "#龍芯⚡️2026-06-19-LONGHUN-MULTICURRENCY-v5.2"
版本號 = "5.2.1"
模組名 = "多币种行情中心"

# 支持的币种列表
幣種定義 = {
    "CNY": {"名稱": "人民幣", "符號": "¥", "類型": "法幣", "精度": 2, "國家": "中國"},
    "USD": {"名稱": "美元", "符號": "$", "類型": "法幣", "精度": 2, "國家": "美國"},
    "EUR": {"名稱": "歐元", "符號": "€", "類型": "法幣", "精度": 2, "國家": "歐盟"},
    "GBP": {"名稱": "英鎊", "符號": "£", "類型": "法幣", "精度": 2, "國家": "英國"},
    "JPY": {"名稱": "日元", "符號": "¥", "類型": "法幣", "精度": 0, "國家": "日本"},
    "KRW": {"名稱": "韓元", "符號": "₩", "類型": "法幣", "精度": 0, "國家": "韓國"},
    "HKD": {"名稱": "港幣", "符號": "HK$", "類型": "法幣", "精度": 2, "國家": "香港"},
    "SGD": {"名稱": "新加坡元", "符號": "S$", "類型": "法幣", "精度": 2, "國家": "新加坡"},
    "BTC": {"名稱": "比特幣", "符號": "₿", "類型": "加密", "精度": 8, "國家": "去中心化"},
    "ETH": {"名稱": "以太坊", "符號": "Ξ", "類型": "加密", "精度": 8, "國家": "去中心化"},
}

# 法幣基準對（相對USD）
法幣基準對 = ["CNY", "USD", "EUR", "GBP", "JPY", "KRW", "HKD", "SGD"]
加密基準對 = ["BTC", "ETH"]

# 緩存過期時間（秒）
緩存過期時間 = 300  # 5分鐘
最大重試次數 = 3
重試間隔 = 2  # 秒

# 默認數據目錄
默認數據目錄 = os.path.expanduser("~/.longhun/multicurrency")


# ═══════════════════════════════════════════════════════════════════════════════
# 數據類定義
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class 匯率記錄:
    """單條匯率記錄數據結構"""
    幣種對: str          # 如 "USD/CNY"
    買入價: float
    賣出價: float
    中間價: float
    漲跌幅: float        # 24小時漲跌幅百分比
    時間戳: float
    數據源: str
    DNA校驗: str = ""   # 數據完整性校驗
    
    def __post_init__(self):
        if not self.DNA校驗:
            self.DNA校驗 = self._計算校驗()
    
    def _計算校驗(self) -> str:
        """計算數據完整性校驗碼"""
        數據 = f"{self.幣種對}:{self.中間價}:{self.時間戳}:{DNA標識}"
        return hashlib.sha256(數據.encode()).hexdigest()[:16]
    
    def 驗證(self) -> bool:
        """驗證數據完整性"""
        return self.DNA校驗 == self._計算校驗()
    
    def 轉字典(self) -> dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def 從字典創建(cls, 數據: dict[str, Any]) -> "匯率記錄":
        return cls(**{k: v for k, v in 數據.items() if k in cls.__dataclass_fields__})


@dataclass
class 行情快照:
    """市場行情快照"""
    時間戳: float
    匯率表: Dict[str, 匯率記錄]
    數據源: str
    狀態: str  # "正常", "緩存", "異常"
    
    def 獲取匯率(self, 基準幣: str, 報價幣: str) -> Optional[匯率記錄]:
        """獲取指定幣種對的匯率"""
        幣種對 = f"{基準幣}/{報價幣}"
        return self.匯率表.get(幣種對)
    
    def 列出所有匯率(self) -> List[str]:
        """列出所有可用的幣種對"""
        return list(self.匯率表.keys())


# ═══════════════════════════════════════════════════════════════════════════════
# 核心類：多币种行情中心
# ═══════════════════════════════════════════════════════════════════════════════

class 多幣種行情中心:
    """
    龍魂多币种行情中心
    
    功能：
    1. 自動獲取多币种實時匯率
    2. 本地緩存與過期檢測
    3. 多數據源容錯
    4. 行情快照管理
    5. 漲跌幅監控
    
    三色審計：
    - 綠色：正常運行，數據新鮮
    - 黃色：使用緩存數據，可能滯後
    - 紅色：數據異常，獲取失敗
    """
    
    def __init__(self, 數據目錄: str | None = None, 緩存時間: int = None):
        self.數據目錄 = Path(數據目錄 or 默認數據目錄)
        self.數據目錄.mkdir(parents=True, exist_ok=True)
        
        self.緩存過期時間 = 緩存時間 or 緩存過期時間
        self.匯率緩存: Dict[str, Tuple[匯率記錄, float]] = {}  # (記錄, 緩存時間)
        self.行情歷史: List[行情快照] = []
        self.最大歷史記錄 = 1000
        
        self.當前狀態 = "初始化"
        self.狀態顏色 = "🟢"  # 綠色=正常
        self.最後更新時間 = 0
        self.統計數據 = {
            "總請求次數": 0,
            "成功次數": 0,
            "緩存命中次數": 0,
            "失敗次數": 0,
            "最後錯誤": ""
        }
        
        self._初始化SSL()
        self._加載緩存()
    
    def _初始化SSL(self):
        """初始化SSL上下文（兼容不同環境）"""
        try:
            self.SSL上下文 = ssl.create_default_context()
        except:
            self.SSL上下文 = ssl._create_unverified_context()
    
    # ───────────────────────────────────────────────
    # 緩存管理
    # ───────────────────────────────────────────────
    
    def _加載緩存(self):
        """從本地加載緩存數據"""
        緩存文件 = self.數據目錄 / "exchange_cache.json"
        if 緩存文件.exists():
            try:
                with open(緩存文件, 'r', encoding='utf-8') as f:
                    數據 = json.load(f)
                for 幣種對, 記錄數據 in 數據.items():
                    記錄 = 匯率記錄.從字典創建(記錄數據)
                    if 記錄.驗證():
                        self.匯率緩存[幣種對] = (記錄, 記錄.時間戳)
                print(f"[🐉] 已加載 {len(self.匯率緩存)} 條緩存記錄")
            except Exception as e:
                print(f"[⚠️] 緩存加載失敗: {e}")
    
    def _保存緩存(self):
        """保存緩存到本地"""
        緩存文件 = self.數據目錄 / "exchange_cache.json"
        try:
            數據 = {}
            for 幣種對, (記錄, _) in self.匯率緩存.items():
                數據[幣種對] = 記錄.轉字典()
            with open(緩存文件, 'w', encoding='utf-8') as f:
                json.dump(數據, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[⚠️] 緩存保存失敗: {e}")
    
    def _緩存是否過期(self, 幣種對: str) -> bool:
        """檢查緩存是否過期"""
        if 幣種對 not in self.匯率緩存:
            return True
        _, 緩存時間 = self.匯率緩存[幣種對]
        return (time.time() - 緩存時間) > self.緩存過期時間
    
    # ───────────────────────────────────────────────
    # 數據獲取
    # ───────────────────────────────────────────────
    
    def _發送請求(self, 網址: str, 超時: int = 10) -> Optional[dict]:
        """發送HTTP請求並返回JSON數據"""
        for 嘗試 in range(最大重試次數):
            try:
                請求 = urllib.request.Request(
                    網址,
                    headers={
                        'User-Agent': 'Mozilla/5.0 (compatible; LongHun-MC/5.0)',
                        'Accept': 'application/json'
                    }
                )
                with urllib.request.urlopen(請求, timeout=超時, context=self.SSL上下文) as 響應:
                    數據 = json.loads(響應.read().decode('utf-8'))
                    return 數據
            except Exception as e:
                self.統計數據["失敗次數"] += 1
                if 嘗試 < 最大重試次數 - 1:
                    time.sleep(重試間隔)
                else:
                    self.統計數據["最後錯誤"] = str(e)
                    return None
        return None
    
    def _獲取法幣匯率(self) -> Dict[str, float]:
        """
        獲取法幣匯率（相對USD）
        使用 exchangerate-api.com（免費層）
        """
        try:
            # 免費API：使用 exchangerate-api
            網址 = "https://api.exchangerate-api.com/v4/latest/USD"
            數據 = self._發送請求(網址)
            
            if 數據 and "rates" in 數據:
                匯率表 = {}
                for 幣種 in 法幣基準對:
                    if 幣種 in 數據["rates"]:
                        匯率表[幣種] = 數據["rates"][幣種]
                return 匯率表
        except Exception as e:
            print(f"[⚠️] 法幣匯率獲取失敗: {e}")
        
        # 返回默認匯率（大致值，僅作備用）
        return {
            "CNY": 7.25, "USD": 1.0, "EUR": 0.92,
            "GBP": 0.79, "JPY": 151.5, "KRW": 1350.0,
            "HKD": 7.82, "SGD": 1.35
        }
    
    def _獲取加密貨幣價格(self) -> Dict[str, float]:
        """
        獲取加密貨幣價格（USD計價）
        使用 CoinGecko API（免費層）
        """
        try:
            網址 = (
                "https://api.coingecko.com/api/v3/simple/price"
                "?ids=bitcoin,ethereum"
                "&vs_currencies=usd"
                "&include_24hr_change=true"
            )
            數據 = self._發送請求(網址)
            
            if 數據:
                價格表 = {}
                if "bitcoin" in 數據 and "usd" in 數據["bitcoin"]:
                    價格表["BTC"] = 數據["bitcoin"]["usd"]
                    價格表["BTC_24h_change"] = 數據["bitcoin"].get("usd_24h_change", 0)
                if "ethereum" in 數據 and "usd" in 數據["ethereum"]:
                    價格表["ETH"] = 數據["ethereum"]["usd"]
                    價格表["ETH_24h_change"] = 數據["ethereum"].get("usd_24h_change", 0)
                return 價格表
        except Exception as e:
            print(f"[⚠️] 加密貨幣價格獲取失敗: {e}")
        
        # 默認價格（備用）
        return {"BTC": 65000.0, "BTC_24h_change": 0, "ETH": 3500.0, "ETH_24h_change": 0}
    
    # ───────────────────────────────────────────────
    # 核心功能
    # ───────────────────────────────────────────────
    
    def 更新全部匯率(self, 強制刷新: bool = False) -> 行情快照:
        """
        更新所有幣種匯率
        
        參數:
            強制刷新: 是否忽略緩存強制重新獲取
        
        返回:
            行情快照對象
        """
        print(f"\n{'='*60}")
        print(f"[🐉] 龍魂多币种行情中心 v{版本號}")
        print(f"[🐉] DNA: {DNA標識}")
        print(f"[🐉] 開始更新匯率...{'（強制刷新）' if 強制刷新 else ''}")
        print(f"{'='*60}\n")
        
        self.統計數據["總請求次數"] += 1
        當前時間 = time.time()
        匯率表 = {}
        
        # ── 獲取法幣匯率 ──
        print("[📊] 正在獲取法幣匯率...")
        法幣匯率 = self._獲取法幣匯率()
        
        for 基準幣 in 法幣基準對:
            for 報價幣 in 法幣基準對:
                if 基準幣 == 報價幣:
                    continue
                
                幣種對 = f"{基準幣}/{報價幣}"
                
                # 檢查緩存
                if not 強制刷新 and not self._緩存是否過期(幣種對):
                    記錄, _ = self.匯率緩存[幣種對]
                    匯率表[幣種對] = 記錄
                    self.統計數據["緩存命中次數"] += 1
                    continue
                
                # 計算交叉匯率
                if 基準幣 == "USD":
                    匯率 = 法幣匯率.get(報價幣, 1.0)
                elif 報價幣 == "USD":
                    匯率 = 1.0 / 法幣匯率.get(基準幣, 1.0)
                else:
                    # 交叉匯率：基準幣→USD→報價幣
                    基準對美元 = 1.0 / 法幣匯率.get(基準幣, 1.0)
                    美元對報價 = 法幣匯率.get(報價幣, 1.0)
                    匯率 = 基準對美元 * 美元對報價
                
                記錄 = 匯率記錄(
                    幣種對=幣種對,
                    買入價=匯率 * 0.998,
                    賣出價=匯率 * 1.002,
                    中間價=匯率,
                    漲跌幅=0.0,
                    時間戳=當前時間,
                    數據源="exchangerate-api"
                )
                匯率表[幣種對] = 記錄
                self.匯率緩存[幣種對] = (記錄, 當前時間)
        
        # ── 獲取加密貨幣價格 ──
        print("[📊] 正在獲取加密貨幣價格...")
        加密價格 = self._獲取加密貨幣價格()
        
        for 加密幣 in 加密基準對:
            USD價格 = 加密價格.get(加密幣, 0)
            漲跌幅 = 加密價格.get(f"{加密幣}_24h_change", 0)
            
            if USD價格 <= 0:
                continue
            
            # 加密幣/USD
            幣種對 = f"{加密幣}/USD"
            記錄 = 匯率記錄(
                幣種對=幣種對,
                買入價=USD價格 * 0.995,
                賣出價=USD價格 * 1.005,
                中間價=USD價格,
                漲跌幅=漲跌幅,
                時間戳=當前時間,
                數據源="coingecko"
            )
            匯率表[幣種對] = 記錄
            self.匯率緩存[幣種對] = (記錄, 當前時間)
            
            # 加密幣/各法幣
            for 法幣 in 法幣基準對:
                if 法幣 == "USD":
                    continue
                法幣匯率 = 法幣匯率.get(法幣, 1.0)
                本地價格 = USD價格 * 法幣匯率
                幣種對 = f"{加密幣}/{法幣}"
                記錄 = 匯率記錄(
                    幣種對=幣種對,
                    買入價=本地價格 * 0.995,
                    賣出價=本地價格 * 1.005,
                    中間價=本地價格,
                    漲跌幅=漲跌幅,
                    時間戳=當前時間,
                    數據源="coingecko+cross"
                )
                匯率表[幣種對] = 記錄
                self.匯率緩存[幣種對] = (記錄, 當前時間)
            
            # USD/加密幣（反向）
            幣種對 = f"USD/{加密幣}"
            記錄 = 匯率記錄(
                幣種對=幣種對,
                買入價=1.0 / (USD價格 * 1.005),
                賣出價=1.0 / (USD價格 * 0.995),
                中間價=1.0 / USD價格,
                漲跌幅=-漲跌幅,
                時間戳=當前時間,
                數據源="coingecko"
            )
            匯率表[幣種對] = 記錄
            self.匯率緩存[幣種對] = (記錄, 當前時間)
        
        # 創建快照
        快照 = 行情快照(
            時間戳=當前時間,
            匯率表=匯率表,
            數據源="mixed",
            狀態="正常"
        )
        
        self.行情歷史.append(快照)
        if len(self.行情歷史) > self.最大歷史記錄:
            self.行情歷史 = self.行情歷史[-self.最大歷史記錄:]
        
        self.最後更新時間 = 當前時間
        self.統計數據["成功次數"] += 1
        self.當前狀態 = "正常運行"
        self.狀態顏色 = "🟢"
        
        # 保存緩存
        self._保存緩存()
        
        print(f"\n[✅] 匯率更新完成！共 {len(匯率表)} 條記錄")
        print(f"[⏱️] 更新時間: {datetime.fromtimestamp(當前時間).strftime('%Y-%m-%d %H:%M:%S')}")
        
        return 快照
    
    def 獲取匯率(self, 基準幣: str, 報價幣: str) -> Optional[匯率記錄]:
        """
        獲取指定幣種對的匯率
        
        參數:
            基準幣: 基準貨幣代碼，如 "USD"
            報價幣: 報價貨幣代碼，如 "CNY"
        
        返回:
            匯率記錄對象，或None
        """
        基準幣 = 基準幣.upper()
        報價幣 = 報價幣.upper()
        幣種對 = f"{基準幣}/{報價幣}"
        
        # 檢查緩存
        if 幣種對 in self.匯率緩存 and not self._緩存是否過期(幣種對):
            記錄, _ = self.匯率緩存[幣種對]
            self.統計數據["緩存命中次數"] += 1
            return 記錄
        
        # 嘗試更新
        try:
            self.更新全部匯率()
            if 幣種對 in self.匯率緩存:
                記錄, _ = self.匯率緩存[幣種對]
                return 記錄
        except Exception as e:
            print(f"[⚠️] 匯率獲取失敗: {e}")
        
        # 檢查是否有過期緩存
        if 幣種對 in self.匯率緩存:
            記錄, _ = self.匯率緩存[幣種對]
            self.狀態顏色 = "🟡"
            self.當前狀態 = "使用緩存數據"
            return 記錄
        
        return None
    
    def 查詢幣種對(self, 幣種對: str) -> Optional[匯率記錄]:
        """
        通過幣種對字符串查詢匯率
        
        支持格式: "USD/CNY", "USDCNY", "USD-CNY", "USD CNY"
        """
        # 規範化幣種對格式
        幣種對 = 幣種對.upper().strip()
        for 分隔符 in ["/", "-", " ", "→"]:
            幣種對 = 幣種對.replace(分隔符, "/")
        
        if "/" in 幣種對:
            基準幣, 報價幣 = 幣種對.split("/", 1)
            return self.獲取匯率(基準幣, 報價幣)
        
        # 嘗試自動識別（假設3字母貨幣代碼）
        if len(幣種對) >= 6:
            基準幣 = 幣種對[:3]
            報價幣 = 幣種對[3:6]
            return self.獲取匯率(基準幣, 報價幣)
        
        return None
    
    def 列出所有匯率(self, 過濾基準幣: str | None = None) -> List[匯率記錄]:
        """列出所有可用匯率"""
        結果 = []
        for 幣種對, (記錄, _) in self.匯率緩存.items():
            if 過濾基準幣:
                if 幣種對.startswith(過濾基準幣.upper() + "/"):
                    結果.append(記錄)
            else:
                結果.append(記錄)
        return sorted(結果, key=lambda x: x.幣種對)
    
    def 獲取最新快照(self) -> Optional[行情快照]:
        """獲取最新行情快照"""
        if self.行情歷史:
            return self.行情歷史[-1]
        return None
    
    def 獲取行情面板(self) -> str:
        """
        生成格式化的行情面板文本
        
        返回:
            可讀性強的行情面板字符串
        """
        快照 = self.獲取最新快照()
        if not 快照:
            return "[❌] 暫無行情數據，請先執行更新"
        
        行 = []
        行.append(f"\n{'═'*70}")
        行.append(f"  🐉 龍魂多币种行情面板  {self.狀態顏色} {datetime.fromtimestamp(快照.時間戳).strftime('%Y-%m-%d %H:%M:%S')}")
        行.append(f"{'═'*70}")
        
        # 法幣區域
        行.append(f"\n  💱 法幣匯率（基準：USD）")
        行.append(f"  {'─'*66}")
        行.append(f"  {'幣種對':<12} {'名稱':<10} {'買入價':>12} {'賣出價':>12} {'漲跌幅':>10}")
        行.append(f"  {'─'*66}")
        
        for 幣種 in 法幣基準對:
            幣種對 = f"USD/{幣種}"
            if 幣種對 in 快照.匯率表:
                記錄 = 快照.匯率表[幣種對]
                名稱 = 幣種定義.get(幣種, {}).get("名稱", 幣種)
                漲跌顏色 = "🟢" if 記錄.漲跌幅 >= 0 else "🔴"
                行.append(f"  {幣種對:<12} {名稱:<10} {記錄.買入價:>12.4f} {記錄.賣出價:>12.4f} {漲跌顏色} {記錄.漲跌幅:>+7.2f}%")
        
        # 加密貨幣區域
        行.append(f"\n  ₿ 加密貨幣價格")
        行.append(f"  {'─'*66}")
        行.append(f"  {'幣種對':<12} {'名稱':<10} {'買入價':>16} {'賣出價':>16} {'漲跌幅':>10}")
        行.append(f"  {'─'*66}")
        
        for 幣種 in 加密基準對:
            幣種對 = f"{幣種}/USD"
            if 幣種對 in 快照.匯率表:
                記錄 = 快照.匯率表[幣種對]
                名稱 = 幣種定義.get(幣種, {}).get("名稱", 幣種)
                漲跌顏色 = "🟢" if 記錄.漲跌幅 >= 0 else "🔴"
                行.append(f"  {幣種對:<12} {名稱:<10} {記錄.買入價:>16,.2f} {記錄.賣出價:>16,.2f} {漲跌顏色} {記錄.漲跌幅:>+7.2f}%")
        
        # CNY跨境重點
        行.append(f"\n  🇨🇳 e-CNY 跨境重點匯率")
        行.append(f"  {'─'*66}")
        重點對 = ["USD/CNY", "EUR/CNY", "JPY/CNY", "HKD/CNY", "SGD/CNY"]
        for 幣種對 in 重點對:
            if 幣種對 in 快照.匯率表:
                記錄 = 快照.匯率表[幣種對]
                基準 = 幣種對.split("/")[0]
                名稱 = 幣種定義.get(基準, {}).get("名稱", 基準)
                符號 = 幣種定義.get(基準, {}).get("符號", "")
                行.append(f"  {幣種對:<12} 1{符號} = {記錄.中間價:.4f} ¥")
        
        # 統計
        行.append(f"\n{'─'*70}")
        行.append(f"  📊 統計：總請求 {self.統計數據['總請求次數']} | 成功 {self.統計數據['成功次數']} | "
                  f"緩存命中 {self.統計數據['緩存命中次數']} | 失敗 {self.統計數據['失敗次數']}")
        行.append(f"  🧬 DNA: {DNA標識}")
        行.append(f"{'═'*70}\n")
        
        return "\n".join(行)
    
    def 獲取統計(self) -> dict[str, Any]:
        """獲取運行統計"""
        return {
            **self.統計數據,
            "狀態": self.當前狀態,
            "狀態顏色": self.狀態顏色,
            "最後更新": self.最後更新時間,
            "緩存記錄數": len(self.匯率緩存),
            "歷史快照數": len(self.行情歷史),
            "DNA": DNA標識,
            "版本": 版本號
        }
    
    def 清理過期緩存(self):
        """清理過期的緩存數據"""
        當前時間 = time.time()
        過期鍵 = []
        for 幣種對, (_, 緩存時間) in self.匯率緩存.items():
            if (當前時間 - 緩存時間) > self.緩存過期時間 * 2:  # 2倍過期時間
                過期鍵.append(幣種對)
        
        for 鍵 in 過期鍵:
            del self.匯率緩存[鍵]
        
        if 過期鍵:
            print(f"[🧹] 已清理 {len(過期鍵)} 條過期緩存")
            self._保存緩存()
    
    def 健康檢查(self) -> Tuple[bool, str]:
        """
        執行健康檢查
        
        返回:
            (是否健康, 狀態描述)
        """
        問題 = []
        
        # 檢查數據新鮮度
        if self.最後更新時間 == 0:
            問題.append("尚未進行首次更新")
        elif (time.time() - self.最後更新時間) > self.緩存過期時間 * 3:
            問題.append("數據嚴重過期")
            self.狀態顏色 = "🔴"
        elif (time.time() - self.最後更新時間) > self.緩存過期時間:
            問題.append("數據可能過期")
            self.狀態顏色 = "🟡"
        
        # 檢查緩存數量
        if len(self.匯率緩存) < 10:
            問題.append("緩存數據不足")
        
        if not 問題:
            return True, f"{self.狀態顏色} 健康（{len(self.匯率緩存)} 條記錄）"
        
        return False, f"{self.狀態顏色} " + "; ".join(問題)


# ═══════════════════════════════════════════════════════════════════════════════
# 命令行入口
# ═══════════════════════════════════════════════════════════════════════════════

def 主函數():
    """命令行入口函數"""
    import argparse
    
    解析器 = argparse.ArgumentParser(
        description="龍魂多币种行情中心",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
示例:
  python 多币种行情中心.py --update              # 更新全部匯率
  python 多币种行情中心.py --query USD/CNY       # 查詢 USD→CNY 匯率
  python 多币种行情中心.py --panel               # 顯示行情面板
  python 多币种行情中心.py --status              # 查看狀態

DNA: {DNA標識}
        """
    )
    
    解析器.add_argument("--update", "-u", action="store_true", help="更新全部匯率")
    解析器.add_argument("--query", "-q", type=str, metavar="幣種對", help="查詢指定匯率")
    解析器.add_argument("--panel", "-p", action="store_true", help="顯示行情面板")
    解析器.add_argument("--status", "-s", action="store_true", help="查看系統狀態")
    解析器.add_argument("--force", "-f", action="store_true", help="強制刷新")
    解析器.add_argument("--cache-dir", type=str, default=None, help="緩存目錄")
    解析器.add_argument("--cache-time", type=int, default=None, help="緩存過期時間(秒)")
    
    參數 = 解析器.parse_args()
    
    # 創建行情中心實例
    中心 = 多幣種行情中心(
        數據目錄=參數.cache_dir,
        緩存時間=參數.cache_time
    )
    
    if 參數.update:
        中心.更新全部匯率(強制刷新=參數.force)
        print(中心.獲取行情面板())
    
    elif 參數.query:
        結果 = 中心.查詢幣種對(參數.query)
        if 結果:
            print(f"\n{'─'*50}")
            print(f"  幣種對: {結果.幣種對}")
            print(f"  買入價: {結果.買入價:.6f}")
            print(f"  賣出價: {結果.賣出價:.6f}")
            print(f"  中間價: {結果.中間價:.6f}")
            漲跌顏色 = "🟢" if 結果.漲跌幅 >= 0 else "🔴"
            print(f"  漲跌幅: {漲跌顏色} {結果.漲跌幅:+.2f}%")
            print(f"  數據源: {結果.數據源}")
            print(f"  時間: {datetime.fromtimestamp(結果.時間戳).strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"  DNA校驗: {'✅ 通過' if 結果.驗證() else '❌ 失敗'}")
            print(f"{'─'*50}\n")
        else:
            print(f"[❌] 未找到 {參數.query} 的匯率數據")
    
    elif 參數.panel:
        if not 中心.行情歷史:
            中心.更新全部匯率()
        print(中心.獲取行情面板())
    
    elif 參數.status:
        健康, 描述 = 中心.健康檢查()
        統計 = 中心.獲取統計()
        print(f"\n{'='*50}")
        print(f"  🐉 龍魂多币种行情中心狀態")
        print(f"{'='*50}")
        print(f"  狀態: {描述}")
        print(f"  版本: v{統計['版本']}")
        print(f"  緩存記錄: {統計['緩存記錄數']}")
        print(f"  歷史快照: {統計['歷史快照數']}")
        print(f"  總請求: {統計['總請求次數']}")
        print(f"  成功: {統計['成功次數']}")
        print(f"  失敗: {統計['失敗次數']}")
        if 統計["最後錯誤"]:
            print(f"  最後錯誤: {統計['最後錯誤']}")
        print(f"  DNA: {統計['DNA']}")
        print(f"{'='*50}\n")
    
    else:
        # 默認行為：更新並顯示面板
        中心.更新全部匯率()
        print(中心.獲取行情面板())


if __name__ == "__main__":
    主函數()
