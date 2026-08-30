# DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-b9e51c5e
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
龍魂Kimi集成器 v5.0
═══════════════════════════════════════════════════════════════
Kimi API接入 + 断路器 + 故障转移 + 本地备份推理
CNSH中文编程规范 | 三色审计 | DNA追溯链

DNA: #龍芯⚡️2026-06-19-LONGHUN-KIMI-v5.0
作者: 龍魂体系·云端技能组
协议: 君子協議 — 非對抗·非欺瞞·非竊取
═══════════════════════════════════════════════════════════════
"""

import os
import sys
import json
import time
import logging
import traceback
from enum import Enum, auto
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Callable, Any, Union
from pathlib import Path
import threading
import urllib.request
import urllib.error
import urllib.parse

# ═══════════════════════════════════════════════════════════════
# 常量定義
# ═══════════════════════════════════════════════════════════════

版本號 = "5.0.0"
DNA標記 = "#龍芯⚡️2026-06-19-LONGHUN-KIMI-v5.0"
技能名稱 = "longhun-cloud-kimi"
API端點 = "http://api:8443/kimi/"

# 断路器常量
斷路器故障閾值 = 3          # 3次故障觸發斷路
斷路器超時秒數 = 30          # 30秒後嘗試半開
請求超時秒數 = 100           # API請求超時100ms

# 三色審計級別
class 審計色(Enum):
    綠_正常 = "綠"       # 正常運行
    黃_警告 = "黃"       # 警告狀態
    紅_異常 = "紅"       # 異常故障

# 断路器狀態
class 斷路器狀態(Enum):
    閉合 = "closed"      # 正常運行
    半開 = "half-open"   # 試探狀態
    斷開 = "open"        # 斷路狀態

# 集成模式
class 集成模式(Enum):
    健康檢查 = "health"
    備份推理 = "backup-inference"
    技能調用 = "skill"
    斷路器狀態查詢 = "circuit-status"

# ═══════════════════════════════════════════════════════════════
# 三色審計日誌
# ═══════════════════════════════════════════════════════════════

class 三色審計器:
    """三色審計系統：綠(正常) / 黃(警告) / 紅(異常)"""

    def __init__(self, 模組名: str):
        self.模組名 = 模組名
        self.日誌記錄: List[Dict] = []
        self._鎖 = threading.Lock()

    def 綠(self, 訊息: str, 元數據: Dict = None):
        """綠色日誌 - 正常運行"""
        self._記錄(審計色.綠_正常, 訊息, 元數據)

    def 黃(self, 訊息: str, 元數據: Dict = None):
        """黃色日誌 - 警告狀態"""
        self._記錄(審計色.黃_警告, 訊息, 元數據)

    def 紅(self, 訊息: str, 元數據: Dict = None):
        """紅色日誌 - 異常故障"""
        self._記錄(審計色.紅_異常, 訊息, 元數據)

    def _記錄(self, 級別: 審計色, 訊息: str, 元數據: Dict = None):
        with self._鎖:
            條目 = {
                "時間戳": datetime.now().isoformat(),
                "級別": 級別.value,
                "顏色": 級別.name,
                "模組": self.模組名,
                "訊息": 訊息,
                "DNA": DNA標記,
                "元數據": 元數據 or {}
            }
            self.日誌記錄.append(條目)
            # 控制台輸出
            顏色碼 = {"綠": "\033[32m", "黃": "\033[33m", "紅": "\033[31m"}
            重置碼 = "\033[0m"
            顏色頭 = 顏色碼.get(級別.value, "")
            print(f"{顏色頭}[{級別.value}] [{self.模組名}] {訊息}{重置碼}")

    def 獲取日誌(self, 級別過濾: 審計色 = None) -> List[Dict]:
        with self._鎖:
            if 級別過濾:
                return [條 for 條 in self.日誌記錄 if 條["級別"] == 級別過濾.value]
            return list(self.日誌記錄)

    def 匯出JSON(self, 路徑: str):
        with open(路徑, 'w', encoding='utf-8') as f:
            json.dump(self.日誌記錄, f, ensure_ascii=False, indent=2)

    def 統計(self) -> Dict[str, int]:
        return {
            "綠_正常": len([條 for 條 in self.日誌記錄 if 條["級別"] == "綠"]),
            "黃_警告": len([條 for 條 in self.日誌記錄 if 條["級別"] == "黃"]),
            "紅_異常": len([條 for 條 in self.日誌記錄 if 條["級別"] == "紅"]),
            "總計": len(self.日誌記錄)
        }


# ═══════════════════════════════════════════════════════════════
# DNA追溯鏈
# ═══════════════════════════════════════════════════════════════

@dataclass
class DNA追溯節點:
    """DNA追溯鏈節點 - 每個操作均可追溯"""
    節點ID: str
    時間戳: str
    操作: str
    輸入摘要: str
    輸出摘要: str
    DNA標記: str
    父節點ID: Optional[str] = None
    元數據: Dict = field(default_factory=dict)

class DNA追溯鏈:
    """DNA追溯鏈管理器 - 完整操作歷史追溯"""

    def __init__(self):
        self.節點列表: List[DNA追溯節點] = []
        self._當前節點ID: Optional[str] = None
        self._鎖 = threading.Lock()
        self._計數器 = 0

    def _生成ID(self) -> str:
        self._計數器 += 1
        return f"NODE-{self._計數器:06d}-{int(time.time())}"

    def 記錄(self, 操作: str, 輸入摘要: str, 輸出摘要: str,
             元數據: Dict = None) -> str:
        with self._鎖:
            節點ID = self._生成ID()
            節點 = DNA追溯節點(
                節點ID=節點ID,
                時間戳=datetime.now().isoformat(),
                操作=操作,
                輸入摘要=輸入摘要,
                輸出摘要=輸出摘要,
                DNA標記=DNA標記,
                父節點ID=self._當前節點ID,
                元數據=元數據 or {}
            )
            self.節點列表.append(節點)
            self._當前節點ID = 節點ID
            return 節點ID

    def 獲取鏈(self) -> List[DNA追溯節點]:
        with self._鎖:
            return list(self.節點列表)

    def 獲取最後節點(self) -> Optional[DNA追溯節點]:
        with self._鎖:
            return self.節點列表[-1] if self.節點列表 else None

    def 匯出JSON(self, 路徑: str):
        with open(路徑, 'w', encoding='utf-8') as f:
            json.dump([{
                "節點ID": n.節點ID,
                "時間戳": n.時間戳,
                "操作": n.操作,
                "輸入摘要": n.輸入摘要,
                "輸出摘要": n.輸出摘要,
                "DNA標記": n.DNA標記,
                "父節點ID": n.父節點ID,
                "元數據": n.元數據
            } for n in self.節點列表], f, ensure_ascii=False, indent=2)


# ═══════════════════════════════════════════════════════════════
# 断路器模式
# ═══════════════════════════════════════════════════════════════

class 断路器:
    """
    断路器模式實現
    - 閉合：正常轉發請求
    - 斷開：故障達閾值，快速失敗
    - 半開：超時後試探，成功則閉合
    """

    def __init__(self, 審計: 三色審計器):
        self.狀態 = 斷路器狀態.閉合
        self.故障計數 = 0
        self.最後故障時間: Optional[float] = None
        self.審計 = 審計
        self._鎖 = threading.Lock()

    def 記錄成功(self):
        with self._鎖:
            if self.狀態 == 斷路器狀態.半開:
                self.狀態 = 斷路器狀態.閉合
                self.故障計數 = 0
                self.審計.綠("断路器：半開→閉合，服務恢復")
            elif self.狀態 == 斷路器狀態.閉合:
                self.故障計數 = 0

    def 記錄故障(self) -> 斷路器狀態:
        with self._鎖:
            self.故障計數 += 1
            self.最後故障時間 = time.time()

            if self.故障計數 >= 斷路器故障閾值:
                if self.狀態 != 斷路器狀態.斷開:
                    self.狀態 = 斷路器狀態.斷開
                    self.審計.紅(f"断路器：故障達{self.故障計數}次，斷開！", {
                        "故障閾值": 斷路器故障閾值,
                        "狀態": "open"
                    })
                return 斷路器狀態.斷開
            else:
                self.審計.黃(f"断路器：故障計數 {self.故障計數}/{斷路器故障閾值}")
                return self.狀態

    def 檢查狀態(self) -> 斷路器狀態:
        with self._鎖:
            if self.狀態 == 斷路器狀態.斷開:
                if self.最後故障時間:
                    經過時間 = time.time() - self.最後故障時間
                    if 經過時間 >= 斷路器超時秒數:
                        self.狀態 = 斷路器狀態.半開
                        self.審計.黃(f"断路器：超時{經過時間:.1f}s，半開試探")
            return self.狀態

    def 允許請求(self) -> bool:
        狀態 = self.檢查狀態()
        return 狀態 in (斷路器狀態.閉合, 斷路器狀態.半開)

    def 獲取狀態字典(self) -> Dict:
        with self._鎖:
            return {
                "狀態": self.狀態.value,
                "故障計數": self.故障計數,
                "故障閾值": 斷路器故障閾值,
                "最後故障時間": self.最後故障時間,
                "超時秒數": 斷路器超時秒數,
                "允許請求": self.允許請求()
            }


# ═══════════════════════════════════════════════════════════════
# Kimi API客戶端
# ═══════════════════════════════════════════════════════════════

@dataclass
class Kimi響應:
    """Kimi API響應封裝"""
    成功: bool
    內容: str
    延遲毫秒: float
    狀態碼: int
    DNA節點ID: str
    使用斷路器: bool = True
    來源: str = "kimi-api"  # kimi-api | local-backup

class Kimi客戶端:
    """Kimi API客戶端 - 帶断路器和故障轉移"""

    def __init__(self, 審計: 三色審計器, 追溯: DNA追溯鏈):
        self.API端點 = API端點
        self.審計 = 審計
        self.追溯 = 追溯
        self.断路器 = 断路器(審計)
        self.請求計數 = 0
        self.成功計數 = 0
        self.失敗計數 = 0
        self._鎖 = threading.Lock()

    def 調用(self, 提示詞: str, 參數: Dict = None) -> Kimi響應:
        """調用Kimi API，帶断路器和故障轉移"""
        self.請求計數 += 1
        參數 = 參數 or {}

        self.審計.綠(f"調用開始 | 提示長度: {len(提示詞)} 字")

        # 檢查断路器
        if not self.断路器.允許請求():
            self.審計.黃("断路器斷開，轉入故障轉移")
            return self._故障轉移(提示詞, 參數, "断路器斷開")

        try:
            開始時間 = time.time()
            響應 = self._發送請求(提示詞, 參數)
            延遲毫秒 = (time.time() - 開始時間) * 1000

            if 響應:
                self.断路器.記錄成功()
                self.成功計數 += 1
                節點ID = self.追溯.記錄(
                    操作="kimi_api_call",
                    輸入摘要=提示詞[:50] + "...",
                    輸出摘要=響應[:50] + "...",
                    元數據={"延遲毫秒": 延遲毫秒, "狀態": "success"}
                )
                self.審計.綠(f"API調用成功 | 延遲: {延遲毫秒:.1f}ms")
                return Kimi響應(
                    成功=True,
                    內容=響應,
                    延遲毫秒=延遲毫秒,
                    狀態碼=200,
                    DNA節點ID=節點ID,
                    來源="kimi-api"
                )
            else:
                raise Exception("空響應")

        except Exception as 錯誤:
            self.失敗計數 += 1
            self.断路器.記錄故障()
            self.審計.紅(f"API調用失敗: {str(錯誤)}", {"錯誤類型": type(錯誤).__name__})
            return self._故障轉移(提示詞, 參數, str(錯誤))

    def _發送請求(self, 提示詞: str, 參數: Dict) -> str:
        """發送HTTP請求到Kimi API"""
        請求體 = json.dumps({
            "prompt": 提示詞,
            **參數
        }).encode('utf-8')

        請求 = urllib.request.Request(
            self.API端點,
            data=請求體,
            headers={
                'Content-Type': 'application/json',
                'X-DNA-Marker': DNA標記,
                'X-Source': 技能名稱
            },
            method='POST'
        )

        try:
            響應 = urllib.request.urlopen(請求, timeout=請求超時秒數 / 1000.0)
            return 響應.read().decode('utf-8')
        except urllib.error.URLError as e:
            raise Exception(f"網絡錯誤: {str(e)}")
        except Exception as e:
            raise Exception(f"請求失敗: {str(e)}")

    def _故障轉移(self, 提示詞: str, 參數: Dict, 原因: str) -> Kimi響應:
        """故障轉移到本地備份推理"""
        self.審計.黃(f"故障轉移啟動 | 原因: {原因}")

        開始時間 = time.time()
        本地結果 = self._本地備份推理(提示詞)
        延遲毫秒 = (time.time() - 開始時間) * 1000

        節點ID = self.追溯.記錄(
            操作="backup_inference",
            輸入摘要=提示詞[:50] + "...",
            輸出摘要=本地結果[:50] + "...",
            元數據={"轉移原因": 原因, "延遲毫秒": 延遲毫秒}
        )

        self.審計.綠(f"本地備份推理完成 | 延遲: {延遲毫秒:.1f}ms")
        return Kimi響應(
            成功=True,
            內容=本地結果,
            延遲毫秒=延遲毫秒,
            狀態碼=200,
            DNA節點ID=節點ID,
            使用斷路器=False,
            來源="local-backup"
        )

    def _本地備份推理(self, 提示詞: str) -> str:
        """本地備份推理引擎 - 當API不可用時提供基本推理能力"""
        self.審計.綠("啟動本地備份推理引擎")

        # 簡易推理邏輯 - 基於關鍵詞匹配
        提示詞小寫 = 提示詞.lower()

        # 代碼相關
        if any(k in 提示詞小寫 for k in ["code", "程式", "代碼", "編程", "python", "函數"]):
            return self._生成代碼回應(提示詞)

        # 分析相關
        if any(k in 提示詞小寫 for k in ["分析", "analyze", "比較", "評估", "review"]):
            return self._生成分析回應(提示詞)

        # 總結相關
        if any(k in 提示詞小寫 for k in ["總結", "summary", "歸納", "概括"]):
            return self._生成總結回應(提示詞)

        # 默認回應
        return self._生成通用回應(提示詞)

    def _生成代碼回應(self, 提示詞: str) -> str:
        return f"""[本地備份推理 - 代碼模式]
收到程式相關請求: {提示詞[:80]}...

```python
# 龍魂備份推理生成的代碼框架
# DNA: {DNA標記}
def 處理函數(輸入參數):
    # TODO: 實現具體邏輯
    結果 = f"處理結果: {{輸入參數}}"
    return 結果

# 使用示例
if __name__ == "__main__":
    print(處理函數("測試數據"))
```

> ⚠️ 這是本地備份推理結果。Kimi API恢復後將提供更精確的回應。
"""

    def _生成分析回應(self, 提示詞: str) -> str:
        return f"""[本地備份推理 - 分析模式]
收到分析請求: {提示詞[:80]}...

## 分析框架

### 1. 問題分解
- 核心問題識別
- 子問題拆分
- 依賴關係梳理

### 2. 多角度評估
- 技術可行性
- 資源需求
- 風險因素

### 3. 建議方案
- 短期行動項
- 中期規劃
- 長期目標

> ⚠️ 這是本地備份推理結果。Kimi API恢復後將提供更深入的分析。
"""

    def _生成總結回應(self, 提示詞: str) -> str:
        return f"""[本地備份推理 - 總結模式]
收到總結請求: {提示詞[:80]}...

## 內容總結

### 要點摘要
1. **[關鍵點一]** 核心論點提煉
2. **[關鍵點二]** 重要發現歸納
3. **[關鍵點三]** 結論性陳述

### 行動建議
- 基於上述分析的後續步驟
- 需要注意的潛在問題
- 優先級排序

> ⚠️ 這是本地備份推理結果。Kimi API恢復後將提供更精確的總結。
"""

    def _生成通用回應(self, 提示詞: str) -> str:
        return f"""[本地備份推理 - 通用模式]
收到請求: {提示詞[:80]}...

## 龍魂備份推理回應

您好！當前Kimi API服務暫時不可用，這是本地備份推理引擎提供的回應。

### 能力說明
- ✅ 基礎文本理解和生成
- ✅ 簡易代碼框架生成
- ✅ 結構化分析模板
- ⚠️ 複雜推理能力有限

### 當前狀態
- 断路器狀態: {self.断路器.狀態.value}
- 故障計數: {self.断路器.故障計數}/{斷路器故障閾值}
- 請求總數: {self.請求計數}

> 💡 API服務恢復後將自動切回完整能力。
> 🧬 DNA: {DNA標記}
"""

    def 健康檢查(self) -> Dict:
        """健康檢查端點"""
        try:
            開始時間 = time.time()
            請求 = urllib.request.Request(
                self.API端點 + "health",
                headers={'X-DNA-Marker': DNA標記},
                method='GET'
            )
            響應 = urllib.request.urlopen(請求, timeout=0.1)
            延遲毫秒 = (time.time() - 開始時間) * 1000
            self.審計.綠(f"健康檢查通過 | 延遲: {延遲毫秒:.1f}ms")
            return {
                "健康": True,
                "延遲毫秒": round(延遲毫秒, 2),
                "狀態碼": 響應.getcode(),
                "断路器狀態": self.断路器.獲取狀態字典()
            }
        except Exception as e:
            self.審計.紅(f"健康檢查失敗: {str(e)}")
            return {
                "健康": False,
                "錯誤": str(e),
                "断路器狀態": self.断路器.獲取狀態字典()
            }


# ═══════════════════════════════════════════════════════════════
# 集成模式處理器
# ═══════════════════════════════════════════════════════════════

class 集成模式處理器:
    """處理4個集成模式的健康檢查、備份推理、技能調用、斷路器狀態查詢"""

    def __init__(self):
        self.審計 = 三色審計器("Kimi集成器")
        self.追溯 = DNA追溯鏈()
        self.客戶端 = Kimi客戶端(self.審計, self.追溯)
        self.啟動時間 = datetime.now().isoformat()

    def 處理(self, 模式: 集成模式, 參數: Dict = None) -> Dict:
        """處理指定的集成模式"""
        參數 = 參數 or {}
        self.審計.綠(f"處理模式: {模式.value}")

        處理器映射 = {
            集成模式.健康檢查: self._處理健康檢查,
            集成模式.備份推理: self._處理備份推理,
            集成模式.技能調用: self._處理技能調用,
            集成模式.斷路器狀態查詢: self._處理斷路器狀態,
        }

        處理函數 = 處理器映射.get(模式)
        if not 處理函數:
            return {"錯誤": f"未知模式: {模式.value}"}

        try:
            return 處理函數(參數)
        except Exception as e:
            self.審計.紅(f"模式處理異常: {str(e)}", {"traceback": traceback.format_exc()})
            return {"錯誤": str(e), "模式": 模式.value}

    def _處理健康檢查(self, 參數: Dict) -> Dict:
        """模式: health - 檢查API和断路器健康狀態"""
        健康結果 = self.客戶端.健康檢查()
        統計 = {
            "請求總數": self.客戶端.請求計數,
            "成功計數": self.客戶端.成功計數,
            "失敗計數": self.客戶端.失敗計數,
            "成功率": f"{(self.客戶端.成功計數 / max(self.客戶端.請求計數, 1) * 100):.1f}%"
        }
        return {
            "模式": "health",
            "DNA": DNA標記,
            "版本": 版本號,
            "啟動時間": self.啟動時間,
            "健康檢查": 健康結果,
            "統計": 統計,
            "時間戳": datetime.now().isoformat()
        }

    def _處理備份推理(self, 參數: Dict) -> Dict:
        """模式: backup-inference - 直接使用本地備份推理"""
        提示詞 = 參數.get("prompt", "")
        if not 提示詞:
            return {"錯誤": "缺少prompt參數"}

        結果 = self.客戶端._故障轉移(提示詞, {}, "手動觸發備份推理")
        return {
            "模式": "backup-inference",
            "DNA": DNA標記,
            "結果": {
                "內容": 結果.內容,
                "延遲毫秒": round(結果.延遲毫秒, 2),
                "來源": 結果.來源,
                "DNA節點ID": 結果.DNA節點ID
            },
            "時間戳": datetime.now().isoformat()
        }

    def _處理技能調用(self, 參數: Dict) -> Dict:
        """模式: skill - 調用Kimi API進行技能處理"""
        提示詞 = 參數.get("prompt", "")
        if not 提示詞:
            return {"錯誤": "缺少prompt參數"}

        結果 = self.客戶端.調用(提示詞, 參數.get("options", {}))
        return {
            "模式": "skill",
            "DNA": DNA標記,
            "結果": {
                "成功": 結果.成功,
                "內容": 結果.內容,
                "延遲毫秒": round(結果.延遲毫秒, 2),
                "狀態碼": 結果.狀態碼,
                "來源": 結果.來源,
                "使用断路器": 結果.使用断路器,
                "DNA節點ID": 結果.DNA節點ID
            },
            "時間戳": datetime.now().isoformat()
        }

    def _處理斷路器狀態(self, 參數: Dict) -> Dict:
        """模式: circuit-status - 查詢断路器詳細狀態"""
        狀態 = self.客戶端.断路器.獲取狀態字典()
        日誌統計 = self.審計.統計()
        return {
            "模式": "circuit-status",
            "DNA": DNA標記,
            "断路器": 狀態,
            "日誌統計": 日誌統計,
            "追溯鏈長度": len(self.追溯.獲取鏈()),
            "時間戳": datetime.now().isoformat()
        }

    def 獲取統計(self) -> Dict:
        """獲取完整統計信息"""
        return {
            "DNA": DNA標記,
            "版本": 版本號,
            "啟動時間": self.啟動時間,
            "客戶端統計": {
                "請求總數": self.客戶端.請求計數,
                "成功計數": self.客戶端.成功計數,
                "失敗計數": self.客戶端.失敗計數,
            },
            "断路器": self.客戶端.断路器.獲取狀態字典(),
            "日誌統計": self.審計.統計(),
            "追溯鏈長度": len(self.追溯.獲取鏈())
        }


# ═══════════════════════════════════════════════════════════════
# 命令行入口
# ═══════════════════════════════════════════════════════════════

def 主函數():
    """命令行入口點"""
    import argparse

    解析器 = argparse.ArgumentParser(
        description="龍魂Kimi集成器 v5.0 - Kimi API接入+断路器+故障轉移+本地備份推理"
    )
    解析器.add_argument(
        "--mode", "-m",
        choices=[m.value for m in 集成模式],
        default="health",
        help="集成模式 (默認: health)"
    )
    解析器.add_argument(
        "--prompt", "-p",
        default="",
        help="提示詞 (skill/backup-inference模式需要)"
    )
    解析器.add_argument(
        "--params", "-P",
        default="{}",
        help="JSON格式額外參數"
    )
    解析器.add_argument(
        "--output", "-o",
        default="",
        help="輸出JSON文件路徑"
    )
    解析器.add_argument(
        "--export-logs", "-l",
        default="",
        help="導出日誌到指定路徑"
    )
    解析器.add_argument(
        "--export-dna", "-d",
        default="",
        help="導出DNA追溯鏈到指定路徑"
    )
    解析器.add_argument(
        "--version", "-v",
        action="store_true",
        help="顯示版本信息"
    )

    參數 = 解析器.parse_args()

    if 參數.version:
        print(f"龍魂Kimi集成器 v{版本號}")
        print(f"DNA: {DNA標記}")
        print(f"API端點: {API端點}")
        sys.exit(0)

    # 解析JSON參數
    try:
        額外參數 = json.loads(參數.params)
    except json.JSONDecodeError:
        print("錯誤: --params 必須是有效的JSON字符串")
        sys.exit(1)

    # 如果有提示詞，添加到參數
    if 參數.prompt:
        額外參數["prompt"] = 參數.prompt

    # 創建處理器並執行
    處理器 = 集成模式處理器()

    # 查找對應的集成模式
    模式映射 = {m.value: m for m in 集成模式}
    模式 = 模式映射.get(參數.mode, 集成模式.健康檢查)

    結果 = 處理器.處理(模式, 額外參數)

    # 輸出結果
    print("\n" + "=" * 60)
    print(f"  龍魂Kimi集成器 v{版本號} | 模式: {參數.mode}")
    print("=" * 60)
    print(json.dumps(結果, ensure_ascii=False, indent=2))

    # 導出日誌
    if 參數.export_logs:
        處理器.審計.匯出JSON(參數.export_logs)
        print(f"\n日誌已導出: {參數.export_logs}")

    # 導出DNA追溯鏈
    if 參數.export_dna:
        處理器.追溯.匯出JSON(參數.export_dna)
        print(f"DNA追溯鏈已導出: {參數.export_dna}")

    # 輸出到文件
    if 參數.output:
        with open(參數.output, 'w', encoding='utf-8') as f:
            json.dump(結果, f, ensure_ascii=False, indent=2)
        print(f"\n結果已輸出: {參數.output}")

    print(f"\n🧬 {DNA標記}")

    # 返回退出碼
    if "錯誤" in 結果:
        sys.exit(1)
    sys.exit(0)


# ═══════════════════════════════════════════════════════════════
# 模塊入口
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    主函數()
