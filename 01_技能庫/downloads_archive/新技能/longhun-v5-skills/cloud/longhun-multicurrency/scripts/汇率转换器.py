# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️2026-06-19-LONGHUN-MULTICURRENCY-v5.2
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
================================================================================
汇率转换器 - 龍魂体系金融工具
================================================================================
文件编号    : C9-002
版本號      : v5.2.0
DNA標識     : #龍芯⚡️2026-06-19-LONGHUN-MULTICURRENCY-v5.2
作者        : 龍魂工程師
用途        : 多币种間实时汇率转换，支持批量转换、历史记录、精確計算

審計追蹤    :
  - 2026-06-19 v5.2.0 初始版本，支持10币种雙向轉換
  - 2026-06-19 v5.2.1 新增e-CNY跨境支付轉換支持

君子協議    : 本模組遵循龍魂開源誓約，禁止用於洗錢、逃稅、非法跨境
              資金轉移。所有轉換記錄留痕，可追溯可審計。
================================================================================
"""

import json
import time
import hashlib
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from pathlib import Path

# 添加父目錄到路徑以導入行情中心
_腳本目錄 = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _腳本目錄)

try:
    from 多币种行情中心 import 多幣種行情中心, 匯率記錄, DNA標識, 版本號, 幣種定義, 法幣基準對, 加密基準對
except ImportError:
    # 如果導入失敗，使用內置定義
    DNA標識 = "#龍芯⚡️2026-06-19-LONGHUN-MULTICURRENCY-v5.2"
    版本號 = "5.2.1"
    
    幣種定義 = {
        "CNY": {"名稱": "人民幣", "符號": "¥", "類型": "法幣", "精度": 2},
        "USD": {"名稱": "美元", "符號": "$", "類型": "法幣", "精度": 2},
        "EUR": {"名稱": "歐元", "符號": "€", "類型": "法幣", "精度": 2},
        "GBP": {"名稱": "英鎊", "符號": "£", "類型": "法幣", "精度": 2},
        "JPY": {"名稱": "日元", "符號": "¥", "類型": "法幣", "精度": 0},
        "KRW": {"名稱": "韓元", "符號": "₩", "類型": "法幣", "精度": 0},
        "HKD": {"名稱": "港幣", "符號": "HK$", "類型": "法幣", "精度": 2},
        "SGD": {"名稱": "新加坡元", "符號": "S$", "類型": "法幣", "精度": 2},
        "BTC": {"名稱": "比特幣", "符號": "₿", "類型": "加密", "精度": 8},
        "ETH": {"名稱": "以太坊", "符號": "Ξ", "類型": "加密", "精度": 8},
    }
    法幣基準對 = ["CNY", "USD", "EUR", "GBP", "JPY", "KRW", "HKD", "SGD"]
    加密基準對 = ["BTC", "ETH"]


# ═══════════════════════════════════════════════════════════════════════════════
# 數據類定義
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class 轉換記錄:
    """單次轉換記錄"""
    編號: str              # 唯一編號
    時間戳: float
    來源幣種: str
    目標幣種: str
    金額: float
    匯率: float
    結果: float
    手續費率: float         # 默認 0.1%
    手續費: float
    實際到賬: float
    備註: str = ""
    DNA校驗: str = ""
    
    def __post_init__(self):
        if not self.DNA校驗:
            self.DNA校驗 = self._計算校驗()
    
    def _計算校驗(self) -> str:
        數據 = f"{self.編號}:{self.來源幣種}:{self.目標幣種}:{self.金額}:{self.結果}:{DNA標識}"
        return hashlib.sha256(數據.encode()).hexdigest()[:16]
    
    def 驗證(self) -> bool:
        return self.DNA校驗 == self._計算校驗()
    
    def 轉字典(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class 批量轉換結果:
    """批量轉換結果"""
    批次編號: str
    時間戳: float
    來源幣種: str
    總金額: float
    轉換明細: List[轉換記錄]
    總手續費: float
    總實際到賬: Dict[str, float]  # 幣種 -> 金額


# ═══════════════════════════════════════════════════════════════════════════════
# 核心類：汇率转换器
# ═══════════════════════════════════════════════════════════════════════════════

class 匯率轉換器:
    """
    龍魂汇率转换器
    
    功能：
    1. 任意幣種間實時轉換
    2. 批量轉換支持
    3. 手續費計算
    4. 轉換歷史記錄
    5. 精確度控制
    
    三色審計：
    - 🟢 正常轉換
    - 🟡 使用近似匯率
    - 🔴 轉換失敗或數據異常
    """
    
    def __init__(self, 行情中心: 多幣種行情中心 = None, 數據目錄: str | None = None,
                 默認手續費率: float = 0.001):
        self.行情中心 = 行情中心 or 多幣種行情中心(數據目錄=數據目錄)
        self.數據目錄 = Path(數據目錄 or os.path.expanduser("~/.longhun/multicurrency"))
        self.數據目錄.mkdir(parents=True, exist_ok=True)
        
        self.默認手續費率 = 默認手續費率  # 0.1%
        self.轉換歷史: List[轉換記錄] = []
        self.批次計數器 = 0
        self.轉換計數器 = 0
        
        # 統計
        self.統計 = {
            "總轉換次數": 0,
            "總轉換金額": 0.0,
            "總手續費": 0.0,
            "成功次數": 0,
            "失敗次數": 0
        }
        
        self._加載歷史()
    
    def _加載歷史(self):
        """加載轉換歷史"""
        歷史文件 = self.數據目錄 / "conversion_history.json"
        if 歷史文件.exists():
            try:
                with open(歷史文件, 'r', encoding='utf-8') as f:
                    數據 = json.load(f)
                for 條目 in 數據:
                    記錄 = 轉換記錄(**條目)
                    if 記錄.驗證():
                        self.轉換歷史.append(記錄)
                self.轉換計數器 = len(self.轉換歷史)
                print(f"[🐉] 已加載 {len(self.轉換歷史)} 條轉換記錄")
            except Exception as e:
                print(f"[⚠️] 歷史記錄加載失敗: {e}")
    
    def _保存歷史(self):
        """保存轉換歷史"""
        歷史文件 = self.數據目錄 / "conversion_history.json"
        try:
            with open(歷史文件, 'w', encoding='utf-8') as f:
                json.dump([r.轉字典() for r in self.轉換歷史[-1000:]], f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[⚠️] 歷史記錄保存失敗: {e}")
    
    def _生成編號(self) -> str:
        """生成唯一轉換編號"""
        self.轉換計數器 += 1
        時間戳 = int(time.time())
        隨機 = hashlib.sha256(f"{時間戳}{self.轉換計數器}{DNA標識}".encode()).hexdigest()[:6]
        return f"LH-{時間戳}-{self.轉換計數器}-{隨機}"
    
    def _格式化金額(self, 金額: float, 幣種: str) -> str:
        """根據幣種精度格式化金額"""
        精度 = 幣種定義.get(幣種, {}).get("精度", 2)
        符號 = 幣種定義.get(幣種, {}).get("符號", "")
        return f"{符號}{金額:,.{精度}f}"
    
    # ───────────────────────────────────────────────
    # 核心轉換功能
    # ───────────────────────────────────────────────
    
    def 轉換(self, 金額: float, 來源幣種: str, 目標幣種: str,
             手續費率: float = None, 備註: str = "") -> Optional[轉換記錄]:
        """
        執行幣種轉換
        
        參數:
            金額: 要轉換的金額
            來源幣種: 來源貨幣代碼，如 "USD"
            目標幣種: 目標貨幣代碼，如 "CNY"
            手續費率: 自定義手續費率（默認 0.1%）
            備註: 轉換備註
        
        返回:
            轉換記錄對象，失敗返回 None
        """
        來源幣種 = 來源幣種.upper().strip()
        目標幣種 = 目標幣種.upper().strip()
        費率 = 手續費率 if 手續費率 is not None else self.默認手續費率
        
        print(f"\n{'─'*60}")
        print(f"[💱] 開始轉換: {self._格式化金額(金額, 來源幣種)} → {目標幣種}")
        print(f"{'─'*60}")
        
        # 驗證幣種
        if 來源幣種 not in 幣種定義:
            print(f"[❌] 不支持的來源幣種: {來源幣種}")
            self.統計["失敗次數"] += 1
            return None
        
        if 目標幣種 not in 幣種定義:
            print(f"[❌] 不支持的目標幣種: {目標幣種}")
            self.統計["失敗次數"] += 1
            return None
        
        # 相同幣種直接返回
        if 來源幣種 == 目標幣種:
            print(f"[ℹ️] 來源與目標相同，無需轉換")
            記錄 = 轉換記錄(
                編號=self._生成編號(),
                時間戳=time.time(),
                來源幣種=來源幣種,
                目標幣種=目標幣種,
                金額=金額,
                匯率=1.0,
                結果=金額,
                手續費率=0,
                手續費=0,
                實際到賬=金額,
                備註=備註 or "同幣種"
            )
            return 記錄
        
        # 獲取匯率
        匯率記錄 = self.行情中心.獲取匯率(來源幣種, 目標幣種)
        
        if not 匯率記錄:
            # 嘗試反向查詢
            反向記錄 = self.行情中心.獲取匯率(目標幣種, 來源幣種)
            if 反向記錄 and 反向記錄.中間價 > 0:
                匯率 = 1.0 / 反向記錄.中間價
                print(f"[🟡] 使用反向匯率計算: 1 {來源幣種} = {匯率:.6f} {目標幣種}")
            else:
                print(f"[❌] 無法獲取 {來源幣種}/{目標幣種} 的匯率")
                self.統計["失敗次數"] += 1
                return None
        else:
            匯率 = 匯率記錄.中間價
            print(f"[🟢] 當前匯率: 1 {來源幣種} = {匯率:.6f} {目標幣種}")
        
        # 計算轉換
        轉換結果 = 金額 * 匯率
        手續費 = 轉換結果 * 費率
        實際到賬 = 轉換結果 - 手續費
        
        # 創建記錄
        記錄 = 轉換記錄(
            編號=self._生成編號(),
            時間戳=time.time(),
            來源幣種=來源幣種,
            目標幣種=目標幣種,
            金額=金額,
            匯率=匯率,
            結果=轉換結果,
            手續費率=費率,
            手續費=手續費,
            實際到賬=實際到賬,
            備註=備註
        )
        
        # 保存
        self.轉換歷史.append(記錄)
        self._保存歷史()
        
        # 更新統計
        self.統計["總轉換次數"] += 1
        self.統計["總轉換金額"] += 金額
        self.統計["總手續費"] += 手續費
        self.統計["成功次數"] += 1
        
        # 輸出結果
        精度 = 幣種定義.get(目標幣種, {}).get("精度", 2)
        print(f"\n  轉換明細:")
        print(f"    來源金額:    {self._格式化金額(金額, 來源幣種)}")
        print(f"    匯率:        1 {來源幣種} = {匯率:.{精度}f} {目標幣種}")
        print(f"    轉換結果:    {self._格式化金額(轉換結果, 目標幣種)}")
        print(f"    手續費({費率*100:.2f}%): {self._格式化金額(手續費, 目標幣種)}")
        print(f"    實際到賬:    {self._格式化金額(實際到賬, 目標幣種)}")
        print(f"    編號:        {記錄.編號}")
        print(f"    DNA校驗:     {'✅ 通過' if 記錄.驗證() else '❌ 失敗'}")
        print(f"{'─'*60}\n")
        
        return 記錄
    
    def 批量轉換(self, 金額: float, 來源幣種: str,
                 目標幣種列表: List[str],
                 手續費率: float = None) -> 批量轉換結果:
        """
        批量轉換到多個目標幣種
        
        參數:
            金額: 來源金額
            來源幣種: 來源貨幣
            目標幣種列表: 目標貨幣列表
            手續費率: 手續費率
        
        返回:
            批量轉換結果
        """
        self.批次計數器 += 1
        批次編號 = f"BATCH-{int(time.time())}-{self.批次計數器}"
        
        print(f"\n{'='*60}")
        print(f"[📦] 批量轉換 #{self.批次計數器}")
        print(f"    {self._格式化金額(金額, 來源幣種)} → {', '.join(目標幣種列表)}")
        print(f"{'='*60}")
        
        明細 = []
        總手續費 = 0.0
        總到賬 = {}
        
        for 目標幣種 in 目標幣種列表:
            目標幣種 = 目標幣種.upper().strip()
            記錄 = self.轉換(金額, 來源幣種, 目標幣種, 手續費率,
                           備註=f"批量轉換 #{self.批次計數器}")
            if 記錄:
                明細.append(記錄)
                總手續費 += 記錄.手續費
                總到賬[目標幣種] = 記錄.實際到賬
        
        結果 = 批量轉換結果(
            批次編號=批次編號,
            時間戳=time.time(),
            來源幣種=來源幣種,
            總金額=金額,
            轉換明細=明細,
            總手續費=總手續費,
            總實際到賬=總到賬
        )
        
        print(f"\n[✅] 批量轉換完成: {len(明細)}/{len(目標幣種列表)} 成功")
        print(f"    總手續費: {總手續費:.4f}")
        
        return 結果
    
    def 快速查詢(self, 來源幣種: str, 目標幣種: str) -> Optional[float]:
        """
        快速查詢匯率（僅返回數值）
        
        返回:
            匯率數值，失敗返回 None
        """
        來源幣種 = 來源幣種.upper().strip()
        目標幣種 = 目標幣種.upper().strip()
        
        if 來源幣種 == 目標幣種:
            return 1.0
        
        記錄 = self.行情中心.獲取匯率(來源幣種, 目標幣種)
        if 記錄:
            return 記錄.中間價
        
        # 嘗試反向
        反向 = self.行情中心.獲取匯率(目標幣種, 來源幣種)
        if 反向 and 反向.中間價 > 0:
            return 1.0 / 反向.中間價
        
        return None
    
    def 列出所有匯率(self, 基準幣: str) -> Dict[str, float]:
        """
        列出基準幣對所有其他幣種的匯率
        
        返回:
            {幣種代碼: 匯率} 字典
        """
        基準幣 = 基準幣.upper().strip()
        結果 = {}
        
        for 幣種 in list(幣種定義.keys()):
            if 幣種 == 基準幣:
                結果[幣種] = 1.0
            else:
                匯率 = self.快速查詢(基準幣, 幣種)
                if 匯率:
                    結果[幣種] = 匯率
        
        return 結果
    
    def 轉換明細面板(self, 記錄: 轉換記錄) -> str:
        """生成轉換明細的面板文本"""
        行 = []
        行.append(f"\n{'─'*50}")
        行.append(f"  💱 轉換明細")
        行.append(f"{'─'*50}")
        行.append(f"  編號:     {記錄.編號}")
        行.append(f"  時間:     {datetime.fromtimestamp(記錄.時間戳).strftime('%Y-%m-%d %H:%M:%S')}")
        行.append(f"  來源:     {self._格式化金額(記錄.金額, 記錄.來源幣種)}")
        行.append(f"  目標:     {記錄.目標幣種}")
        行.append(f"  匯率:     1 {記錄.來源幣種} = {記錄.匯率:.6f} {記錄.目標幣種}")
        行.append(f"  轉換結果: {self._格式化金額(記錄.結果, 記錄.目標幣種)}")
        行.append(f"  手續費:   {self._格式化金額(記錄.手續費, 記錄.目標幣種)} ({記錄.手續費率*100:.2f}%)")
        行.append(f"  實際到賬: {self._格式化金額(記錄.實際到賬, 記錄.目標幣種)}")
        if 記錄.備註:
            行.append(f"  備註:     {記錄.備註}")
        行.append(f"  DNA:      {'✅ 通過' if 記錄.驗證() else '❌ 失敗'}")
        行.append(f"{'─'*50}\n")
        return "\n".join(行)
    
    def 獲取歷史(self, 幣種對: str | None = None, 限制: int = 20) -> List[轉換記錄]:
        """
        獲取轉換歷史
        
        參數:
            幣種對: 過濾指定幣種對，如 "USD/CNY"
            限制: 最大返回數量
        """
        結果 = self.轉換歷史
        
        if 幣種對:
            基準, 報價 = None, None
            if "/" in 幣種對:
                基準, 報價 = 幣種對.upper().split("/", 1)
            結果 = [r for r in 結果 
                   if (not 基準 or r.來源幣種 == 基準) 
                   and (not 報價 or r.目標幣種 == 報價)]
        
        return 結果[-限制:]
    
    def 獲取統計(self) -> dict[str, Any]:
        """獲取轉換統計"""
        return {
            **self.統計,
            "歷史記錄數": len(self.轉換歷史),
            "DNA": DNA標識,
            "版本": 版本號
        }


# ═══════════════════════════════════════════════════════════════════════════════
# e-CNY 跨境支付通道
# ═══════════════════════════════════════════════════════════════════════════════

class 數字人民幣跨境通道:
    """
    e-CNY 跨境支付支持
    
    功能：
    1. e-CNY 與各幣種轉換
    2. 跨境支付路徑規劃
    3. 合規檢查提示
    """
    
    def __init__(self, 轉換器: 匯率轉換器 = None):
        self.轉換器 = 轉換器 or 匯率轉換器()
        self.通道狀態 = "就緒"
    
    def CNY轉eCNY(self, 金額: float) -> dict[str, Any]:
        """CNY 轉 e-CNY（1:1 等值轉換）"""
        return {
            "來源": "CNY",
            "目標": "e-CNY",
            "金額": 金額,
            "匯率": 1.0,
            "結果": 金額,
            "手續費": 0,
            "狀態": "🟢 支持",
            "說明": "數字人民幣與紙幣人民幣等值1:1兌換"
        }
    
    def eCNY跨境轉換(self, eCNY金額: float, 目標幣種: str) -> Optional[轉換記錄]:
        """
        e-CNY 跨境轉換到目標幣種
        
        通過 CNY → 目標幣種 進行轉換
        """
        print(f"\n[🇨🇳] e-CNY 跨境轉換: ¥{eCNY金額:,.2f} → {目標幣種}")
        print("[🇨🇳] 通過 CNY 通道進行轉換...")
        
        結果 = self.轉換器.轉換(
            金額=eCNY金額,
            來源幣種="CNY",
            目標幣種=目標幣種,
            備註="e-CNY跨境支付"
        )
        
        if 結果:
            print("[✅] e-CNY 跨境轉換完成")
            print("[📋] 合規提示：請確保交易符合跨境支付相關法規")
        
        return 結果
    
    def 獲取跨境重點匯率(self) -> str:
        """獲取 e-CNY 跨境重點匯率面板"""
        行 = []
        行.append(f"\n{'═'*60}")
        行.append(f"  🇨🇳 e-CNY 跨境支付重點匯率")
        行.append(f"{'═'*60}")
        
        重點幣種 = ["USD", "EUR", "JPY", "HKD", "SGD", "GBP", "KRW"]
        行.append(f"  {'幣種':<8} {'名稱':<12} {'1 e-CNY =':<18} {'漲跌':>10}")
        行.append(f"  {'─'*56}")
        
        for 幣種 in 重點幣種:
            匯率 = self.轉換器.快速查詢("CNY", 幣種)
            名稱 = 幣種定義.get(幣種, {}).get("名稱", 幣種)
            符號 = 幣種定義.get(幣種, {}).get("符號", "")
            if 匯率:
                行.append(f"  {幣種:<8} {名稱:<12} {符號}{1/匯率:>12.4f} {'-':>10}")
            else:
                行.append(f"  {幣種:<8} {名稱:<12} {'N/A':>12} {'N/A':>10}")
        
        行.append(f"\n  💡 提示: e-CNY 與 CNY 等值 1:1")
        行.append(f"  📋 所有 e-CNY 跨境交易均通過 CNY 通道進行")
        行.append(f"{'═'*60}\n")
        
        return "\n".join(行)


# ═══════════════════════════════════════════════════════════════════════════════
# 命令行入口
# ═══════════════════════════════════════════════════════════════════════════════

def 主函數():
    """命令行入口"""
    import argparse
    
    解析器 = argparse.ArgumentParser(
        description="龍魂汇率转换器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
示例:
  python 汇率转换器.py --convert 100 USD CNY       # 轉換 100 USD 到 CNY
  python 汇率转换器.py --rate USD CNY              # 查詢 USD/CNY 匯率
  python 汇率转换器.py --rates USD                 # 列出 USD 對所有幣種匯率
  python 汇率转换器.py --batch 1000 CNY USD EUR    # 批量轉換
  python 汇率转换器.py --ecny 1000 USD             # e-CNY 跨境轉換
  python 汇率转换器.py --history                   # 查看轉換歷史
  python 汇率转换器.py --panel                     # 顯示完整面板

支持幣種: {', '.join(幣種定義.keys())}
DNA: {DNA標識}
        """
    )
    
    解析器.add_argument("--convert", "-c", nargs=3, metavar=("金額", "來源", "目標"),
                        help="轉換金額（如: 100 USD CNY）")
    解析器.add_argument("--rate", "-r", nargs=2, metavar=("來源", "目標"),
                        help="查詢匯率")
    解析器.add_argument("--rates", metavar="基準幣",
                        help="列出基準幣對所有幣種的匯率")
    解析器.add_argument("--batch", nargs='+', metavar=("金額", "來源", "目標1", "目標2"),
                        help="批量轉換")
    解析器.add_argument("--ecny", nargs=2, metavar=("金額", "目標幣"),
                        help="e-CNY 跨境轉換")
    解析器.add_argument("--ecny-panel", action="store_true", help="顯示 e-CNY 面板")
    解析器.add_argument("--history", action="store_true", help="查看轉換歷史")
    解析器.add_argument("--panel", "-p", action="store_true", help="顯示完整面板")
    解析器.add_argument("--fee", type=float, default=None, help="自定義手續費率")
    
    參數 = 解析器.parse_args()
    
    # 創建轉換器
    轉換器 = 匯率轉換器()
    
    if 參數.convert:
        金額 = float(參數.convert[0])
        來源 = 參數.convert[1]
        目標 = 參數.convert[2]
        轉換器.轉換(金額, 來源, 目標, 手續費率=參數.fee)
    
    elif 參數.rate:
        來源, 目標 = 參數.rate
        匯率 = 轉換器.快速查詢(來源, 目標)
        if 匯率:
            來源符號 = 幣種定義.get(來源.upper(), {}).get("符號", "")
            目標符號 = 幣種定義.get(目標.upper(), {}).get("符號", "")
            print(f"\n{'─'*40}")
            print(f"  💱 匯率查詢")
            print(f"{'─'*40}")
            print(f"  1 {來源} = {匯率:.6f} {目標}")
            print(f"  即: {來源符號}1 = {目標符號}{匯率:.4f}")
            print(f"  反向: 1 {目標} = {1/匯率:.6f} {來源}")
            print(f"{'─'*40}\n")
        else:
            print(f"[❌] 無法獲取 {來源}/{目標} 的匯率")
    
    elif 參數.rates:
        基準幣 = 參數.rates.upper()
        匯率表 = 轉換器.列出所有匯率(基準幣)
        
        print(f"\n{'═'*50}")
        print(f"  💱 {基準幣} 對所有幣種匯率")
        print(f"{'═'*50}")
        for 幣種, 匯率 in sorted(匯率表.items()):
            符號 = 幣種定義.get(幣種, {}).get("符號", "")
            名稱 = 幣種定義.get(幣種, {}).get("名稱", 幣種)
            print(f"  1 {基準幣} = {匯率:>12.6f} {幣種} ({名稱}) {符號}")
        print(f"{'═'*50}\n")
    
    elif 參數.batch:
        金額 = float(參數.batch[0])
        來源 = 參數.batch[1]
        目標列表 = 參數.batch[2:]
        轉換器.批量轉換(金額, 來源, 目標列表, 手續費率=參數.fee)
    
    elif 參數.ecny:
        金額 = float(參數.ecny[0])
        目標幣 = 參數.ecny[1]
        通道 = 數字人民幣跨境通道(轉換器)
        通道.eCNY跨境轉換(金額, 目標幣)
    
    elif 參數.ecny_panel:
        通道 = 數字人民幣跨境通道(轉換器)
        print(通道.獲取跨境重點匯率())
    
    elif 參數.history:
        歷史 = 轉換器.獲取歷史(限制=10)
        if 歷史:
            print(f"\n{'═'*60}")
            print(f"  📜 最近轉換歷史")
            print(f"{'═'*60}")
            for 記錄 in 歷史:
                時間 = datetime.fromtimestamp(記錄.時間戳).strftime('%m-%d %H:%M')
                print(f"  [{時間}] {記錄.來源幣種} {記錄.金額:>10,.2f} → "
                      f"{記錄.目標幣種} {記錄.實際到賬:>12,.4f} | {記錄.編號}")
            print(f"{'═'*60}\n")
        else:
            print("[ℹ️] 暫無轉換歷史")
    
    elif 參數.panel:
        # 顯示完整面板
        轉換器.行情中心.更新全部匯率()
        print(轉換器.行情中心.獲取行情面板())
        
        # e-CNY 面板
        通道 = 數字人民幣跨境通道(轉換器)
        print(通道.獲取跨境重點匯率())
    
    else:
        解析器.print_help()


if __name__ == "__main__":
    主函數()
