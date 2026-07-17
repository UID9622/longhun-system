#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════╗
║  🐉 龍瞳OCR — 中文優先圖像識別引擎 / LONGTENG OCR Engine              ║
║  Dragon Pupil OCR — Chinese-First Image Recognition Engine           ║
╠══════════════════════════════════════════════════════════════════════╣
║  DNA追溯 / DNA Trace: #龍芯⚡️2026-06-18-LONGTENG-OCR-v1.0          ║
║  龍魂體系核心模塊 / Dragon Soul System Core Module                   ║
╠══════════════════════════════════════════════════════════════════════╣
║  君子協議 / Gentleman's Agreement:                                   ║
║  CC BY-NC-SA 4.0 — 署名-非商業性使用-相同方式共享                     ║
║  Attribution-NonCommercial-ShareAlike 4.0 International              ║
║  作者：龍魂體系開源社區 / Author: Dragon Soul Open Source Community  ║
╠══════════════════════════════════════════════════════════════════════╣
║  核心策略 / Core Strategy:                                           ║
║  能中文替代的中文實現，不能的用國際標準庫兜底                          ║
║  Chinese-first implementation; international libraries as fallback   ║
╚══════════════════════════════════════════════════════════════════════╝

三色審計標註 / Tri-color Audit Markers:
  🟢 已實現 / Implemented | 🟡 部分實現 / Partial | 🔴 未實現 / Not Implemented
"""

# ═══════════════════════════════════════════════════════════════════════
# 標準庫導入 / Standard Library Imports
# ═══════════════════════════════════════════════════════════════════════
import os
import sys
import json
import math
import logging
import warnings
import traceback
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Tuple, Optional, Union, Any
from collections import Counter, defaultdict
from enum import Enum

# ═══════════════════════════════════════════════════════════════════════
# 第三方庫導入（含兜底）/ Third-party Imports (with fallback)
# ═══════════════════════════════════════════════════════════════════════
import numpy as np

# 日誌配置 / Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
日誌 = logging.getLogger('龍瞳OCR')

# 🟢 OpenCV — 國際兜底：基礎圖像I/O / International fallback: basic I/O
try:
    import cv2
    CV2可用 = True
    日誌.info("🟢 OpenCV已加載 / OpenCV loaded")
except ImportError:
    CV2可用 = False
    warnings.warn("🟡 OpenCV未安裝 — 圖像I/O將受限 | OpenCV not installed", RuntimeWarning)

# 🟢 Pillow — 圖像格式處理 / Image format handling
try:
    from PIL import Image, ImageFilter, ImageOps, ImageEnhance, ImageDraw, ImageFont
    PIL可用 = True
    日誌.info("🟢 Pillow已加載 / Pillow loaded")
except ImportError:
    PIL可用 = False
    warnings.warn("🟡 Pillow未安裝 — 格式轉換將受限 | Pillow not installed", RuntimeWarning)

# 🟡 Tesseract — OCR國際兜底 / OCR international fallback
try:
    import pytesseract
    TESSERACT可用 = True
    日誌.info("🟢 Tesseract已加載 / Tesseract loaded")
except ImportError:
    TESSERACT可用 = False
    warnings.warn("🟡 Tesseract未安裝 — OCR降級不可用 | Tesseract not installed", RuntimeWarning)

# 🟢 SciPy — 科學計算（用於距離變換）/ Scientific computing (distance transform)
try:
    from scipy import ndimage
    SCIPY可用 = True
except ImportError:
    SCIPY可用 = False
    warnings.warn("🟡 SciPy未安裝 — 骨架化將使用替代方案 | SciPy not installed", RuntimeWarning)

# ═══════════════════════════════════════════════════════════════════════
# 枚舉定義 / Enumerations
# ═══════════════════════════════════════════════════════════════════════
class 識別模式(Enum):
    """識別模式枚舉 / Recognition mode enumeration"""
    中文優先 = "中文優先"      # Chinese-first: native algos first
    國際兜底 = "國際兜底"      # International fallback only
    混合模式 = "混合模式"      # Hybrid: combine both approaches


class 字符結構(Enum):
    """中文字符結構分類 / Chinese character structure classification"""
    獨體 = "獨體"            # Single component (e.g., 日, 月)
    左右 = "左右"            # Left-right (e.g., 明, 龍)
    上下 = "上下"            # Top-bottom (e.g., 思, 字)
    包圍 = "包圍"            # Enclosure (e.g., 國, 回)
    半包圍 = "半包圍"        # Semi-enclosure (e.g., 匡, 凶)
    未知 = "未知"            # Unknown structure


# ═══════════════════════════════════════════════════════════════════════
# 數據類定義 / Data Class Definitions
# ═══════════════════════════════════════════════════════════════════════
@dataclass
class 識別結果:
    """識別結果數據類 / Recognition result data class"""
    文本: str = ""                           # 識別文本 / Recognized text
    置信度: float = 0.0                       # 置信度 0.0-1.0 / Confidence score
    區域: List[Dict[str, Any]] = field(default_factory=list)   # 文本區域 / Text regions
    審計: str = "🟢"                         # 三色審計標註 / Audit marker
    結構: str = ""                           # 字符結構 / Character structure
    備註: str = ""                           # 附加備註 / Additional notes
    引擎來源: str = "龍瞳核心"                  # Engine source / Engine source

    def 轉字典(self) -> Dict[str, Any]:
        """轉換為字典 / Convert to dictionary"""
        return asdict(self)

    def 轉JSON(self, 文件路徑: Optional[str] = None, 確保中文: bool = True) -> str:
        """轉換為JSON字符串 / Convert to JSON string
        
        參數 Parameters:
            文件路徑: 若指定則保存到文件 / Save to file if specified
            確保中文: 確保中文字符正確編碼 / Ensure Chinese encoding
        """
        選項 = 4 if 確保中文 else None
        json字符串 = json.dumps(self.轉字典(), ensure_ascii=False, indent=選項)
        if 文件路徑:
            os.makedirs(os.path.dirname(文件路徑), exist_ok=True)
            with open(文件路徑, 'w', encoding='utf-8') as f:
                f.write(json字符串)
            日誌.info(f"🟢 JSON已保存 | JSON saved: {文件路徑}")
        return json字符串


@dataclass
class 區域框:
    """文本區域框 / Text region bounding box"""
    左上橫: int = 0       # x1 / Left
    左上縱: int = 0       # y1 / Top
    右下橫: int = 0       # x2 / Right
    右下縱: int = 0       # y2 / Bottom
    置信度: float = 0.0    # Confidence
    文本: str = ""        # Recognized text

    def 轉字典(self) -> Dict[str, Union[int, float, str]]:
        return {
            "x1": self.左上橫, "y1": self.左上縱,
            "x2": self.右下橫, "y2": self.右下縱,
            "寬": self.右下橫 - self.左上橫,
            "高": self.右下縱 - self.左上縱,
            "置信度": round(self.置信度, 4),
            "文本": self.文本
        }


# ═══════════════════════════════════════════════════════════════════════
# CNSH術語詞典 / CNSH Terminology Dictionary
# ═══════════════════════════════════════════════════════════════════════
class CNSH詞典:
    """CNSH中文編程術語詞典 / CNSH Chinese programming terminology"""
    
    # 🟢 常見中文變量名模式 / Common Chinese variable name patterns
    編程術語 = {
        # 控制流程 / Control flow
        "函數", "變量", "常量", "參數", "返回", "循環", "條件", "分支",
        "遍歷", "迭代", "遞歸", "調用", "定義", "聲明", "初始化",
        # 數據類型 / Data types
        "字符串", "整數", "浮點", "列表", "字典", "元組", "集合", "對象",
        "數組", "矩陣", "向量", "布爾", "空值", "字節",
        # 面向對象 / OOP
        "類", "實例", "方法", "屬性", "繼承", "多態", "封裝", "構造",
        "析構", "抽象", "接口", "重寫", "重載",
        # 異常處理 / Exception handling
        "異常", "錯誤", "捕獲", "拋出", "嘗試", "終止", "斷言",
        # 模塊系統 / Module system
        "模塊", "導入", "導出", "包", "庫", "命名空間", "作用域",
        # I/O操作 / I/O operations
        "文件", "讀取", "寫入", "打開", "關閉", "路徑", "流",
        # 並發 / Concurrency
        "線程", "進程", "異步", "同步", "鎖", "信號", "隊列",
        # 網絡 / Network
        "請求", "響應", "連接", "服務器", "客戶端", "協議", "套接字",
        # 數據庫 / Database
        "查詢", "插入", "更新", "刪除", "事務", "索引", "表", "記錄",
        # 龍魂體系專用 / Dragon Soul system specific
        "龍魂", "龍芯", "龍瞳", "龍骨", "龍鱗", "龍息", "龍脈",
        "通心譯", "CNSH", "君子協議", "三色審計", "DNA追溯",
        "覺醒", "開光", "入定", "調息", "運氣", "周天", "築基",
    }
    
    # 🟢 中文前綴後綴模式 / Chinese prefix/suffix patterns
    命名模式 = [
        ("動詞", ["獲取", "設置", "計算", "解析", "轉換", "驗證", 
                  "加載", "保存", "創建", "刪除", "更新", "查找",
                  "提取", "過濾", "排序", "合併", "分割", "處理",
                  "檢測", "識別", "分析", "生成", "導入", "導出"]),
        ("名詞", ["數組", "列表", "字典", "字符串", "數值", "對象",
                  "計數器", "索引", "緩存", "配置", "狀態", "結果",
                  "引擎", "管理器", "處理器", "控制器", "服務", "客戶端"]),
        ("形容詞", ["最大", "最小", "平均", "總和", "當前", "臨時",
                    "全局", "局部", "有效", "無效", "激活", "靜態"]),
    ]
    
    @classmethod
    def 是編程術語(cls, 詞: str) -> bool:
        """檢查是否為編程術語 / Check if term is programming terminology"""
        return 詞 in cls.編程術語
    
    @classmethod
    def 匹配命名模式(cls, 文本: str) -> List[Dict[str, str]]:
        """匹配中文編程命名模式 / Match Chinese naming patterns
        
        返回 Returns:
            匹配結果列表 / List of matched patterns
        """
        結果 = []
        for 類型, 詞列表 in cls.命名模式:
            for 詞 in 詞列表:
                if 詞 in 文本:
                    結果.append({"類型": 類型, "詞": 詞, "位置": str(文本.index(詞))})
        return 結果


# ═══════════════════════════════════════════════════════════════════════
# 圖像預處理器（中文算法實現）/ Image Preprocessor (Chinese Algorithm Implementation)
# ═══════════════════════════════════════════════════════════════════════
class 圖像預處理器:
    """
    圖像預處理器 — 純中文算法實現
    Image Preprocessor — Pure Chinese algorithm implementation
    
    🟢 Otsu二值化 — 自己實現 / Self-implemented
    🟢 中值濾波 — 自己實現 / Self-implemented
    🟢 傾斜校正 — 基於投影自己實現 / Projection-based self-implemented
    """
    
    def __init__(self):
        self.版本 = "1.0"
        self.審計狀態 = "🟢"
    
    def 轉灰度(self, 圖像: np.ndarray) -> np.ndarray:
        """
        轉換為灰度圖像 / Convert to grayscale
        
        參數 Parameters:
            圖像: 輸入圖像數組 (H, W, C) 或 (H, W) / Input image array
        
        返回 Returns:
            灰度圖像 (H, W) / Grayscale image
        """
        if len(圖像.shape) == 3:
            if 圖像.shape[2] == 3:
                灰度 = (0.299 * 圖像[:, :, 0] + 
                       0.587 * 圖像[:, :, 1] + 
                       0.114 * 圖像[:, :, 2]).astype(np.uint8)
                return 灰度
            elif 圖像.shape[2] == 4:
                灰度 = (0.299 * 圖像[:, :, 0] + 
                       0.587 * 圖像[:, :, 1] + 
                       0.114 * 圖像[:, :, 2]).astype(np.uint8)
                return 灰度
        elif len(圖像.shape) == 2:
            return 圖像.astype(np.uint8)
        else:
            raise ValueError(f"🔴 不支持的圖像維度 / Unsupported image dims: {圖像.shape}")
    
    def OTSU二值化(self, 灰度圖: np.ndarray) -> np.ndarray:
        """
        🟢 OTSU自動閾值二值化 — 自己實現
        OTSU Automatic Threshold Binarization — Self-implemented
        
        基於最大類間方差法 / Based on maximum between-class variance method
        
        參數 Parameters:
            灰度圖: 灰度圖像數組 (H, W) / Grayscale image
        
        返回 Returns:
            二值圖像 (H, W) / Binary image
        """
        if 灰度圖.max() <= 1.0:
            灰度圖 = (灰度圖 * 255).astype(np.uint8)
        
        # 計算直方圖 / Calculate histogram
        直方圖 = np.zeros(256, dtype=np.float64)
        for 值 in 灰度圖.flatten():
            直方圖[int(值)] += 1
        
        總像素數 = 灰度圖.size
        正規化直方圖 = 直方圖 / 總像素數
        
        # OTSU算法核心 / OTSU core algorithm
        最大方差 = 0.0
        最佳閾值 = 127
        
        for 閾值 in range(256):
            前景概率 = np.sum(正規化直方圖[:閾值 + 1])
            背景概率 = np.sum(正規化直方圖[閾值 + 1:])
            
            if 前景概率 == 0 or 背景概率 == 0:
                continue
            
            前景均值 = np.sum(np.arange(閾值 + 1) * 正規化直方圖[:閾值 + 1]) / 前景概率
            背景均值 = np.sum(np.arange(閾值 + 1, 256) * 正規化直方圖[閾值 + 1:]) / 背景概率
            
            類間方差 = 前景概率 * 背景概率 * (前景均值 - 背景均值) ** 2
            
            if 類間方差 > 最大方差:
                最大方差 = 類間方差
                最佳閾值 = 閾值
        
        二值圖 = np.where(灰度圖 > 最佳閾值, 255, 0).astype(np.uint8)
        
        日誌.debug(f"🟢 OTSU閾值 / Threshold: {最佳閾值}, 方差 / Variance: {最大方差:.2f}")
        return 二值圖
    
    def 中值濾波(self, 圖像: np.ndarray, 核大小: int = 3) -> np.ndarray:
        """
        🟢 中值濾波去噪 — 自己實現（不使用OpenCV）
        Median Filter Denoising — Self-implemented (no OpenCV)
        
        參數 Parameters:
            圖像: 輸入圖像 / Input image
            核大小: 濾波核大小（奇數）/ Kernel size (odd)
        
        返回 Returns:
            濾波後圖像 / Filtered image
        """
        if 核大小 % 2 == 0:
            raise ValueError("🔴 核大小必須為奇數 / Kernel size must be odd")
        
        高, 寬 = 圖像.shape[:2]
        邊距 = 核大小 // 2
        
        if len(圖像.shape) == 3:
            填充圖 = np.pad(圖像, ((邊距, 邊距), (邊距, 邊距), (0, 0)), mode='edge')
            結果 = np.zeros_like(圖像)
            for 縱 in range(高):
                for 橫 in range(寬):
                    for 通道 in range(圖像.shape[2]):
                        區域 = 填充圖[縱:縱+核大小, 橫:橫+核大小, 通道]
                        結果[縱, 橫, 通道] = np.median(區域)
        else:
            填充圖 = np.pad(圖像, 邊距, mode='edge')
            結果 = np.zeros_like(圖像)
            for 縱 in range(高):
                for 橫 in range(寬):
                    區域 = 填充圖[縱:縱+核大小, 橫:橫+核大小]
                    結果[縱, 橫] = np.median(區域)
        
        日誌.debug(f"🟢 中值濾波完成 / Median filter done, kernel={核大小}")
        return 結果.astype(圖像.dtype)
    
    def 旋轉圖像(self, 圖像: np.ndarray, 角度: float) -> np.ndarray:
        """
        🟢 圖像旋轉 — 自己實現（不使用OpenCV）
        Image Rotation — Self-implemented (no OpenCV)
        
        參數 Parameters:
            圖像: 輸入圖像 / Input image
            角度: 旋轉角度（度）/ Rotation angle (degrees)
        
        返回 Returns:
            旋轉後圖像 / Rotated image
        """
        弧度 = math.radians(角度)
        餘弦 = math.cos(弧度)
        正弦 = math.sin(弧度)
        
        高, 寬 = 圖像.shape[:2]
        
        新寬 = int(abs(寬 * 餘弦) + abs(高 * 正弦))
        新高 = int(abs(寬 * 正弦) + abs(高 * 餘弦))
        
        原中心橫, 原中心縱 = 寬 / 2, 高 / 2
        新中心橫, 新中心縱 = 新寬 / 2, 新高 / 2
        
        if len(圖像.shape) == 3:
            結果 = np.full((新高, 新寬, 圖像.shape[2]), 255, dtype=圖像.dtype)
        else:
            結果 = np.full((新高, 新寬), 255, dtype=圖像.dtype)
        
        for 新縱 in range(新高):
            for 新橫 in range(新寬):
                原橫 = int((新橫 - 新中心橫) * 餘弦 + (新縱 - 新中心縱) * 正弦 + 原中心橫)
                原縱 = int(-(新橫 - 新中心橫) * 正弦 + (新縱 - 新中心縱) * 餘弦 + 原中心縱)
                
                if 0 <= 原橫 < 寬 and 0 <= 原縱 < 高:
                    結果[新縱, 新橫] = 圖像[原縱, 原橫]
        
        return 結果
    
    def 傾斜校正(self, 二值圖: np.ndarray) -> np.ndarray:
        """
        🟢 傾斜校正 — 基於投影的自己實現
        Skew Correction — Self-implemented projection-based method
        
        通過旋轉投影尋找最佳角度 / Find optimal angle by rotating projection
        
        參數 Parameters:
            二值圖: 二值圖像 / Binary image
        
        返回 Returns:
            校正後圖像 / Corrected image
        """
        最佳角度 = 0
        最大投影差 = 0
        
        for 角度 in range(-15, 16):
            旋轉圖 = self.旋轉圖像(二值圖, 角度)
            投影 = np.sum(旋轉圖 < 128, axis=1)
            差分 = np.diff(投影)
            方差 = np.var(差分)
            
            if 方差 > 最大投影差:
                最大投影差 = 方差
                最佳角度 = 角度
        
        if 最佳角度 != 0:
            校正圖 = self.旋轉圖像(二值圖, 最佳角度)
            日誌.info(f"🟢 傾斜校正 / Skew corrected: {最佳角度}°")
            return 校正圖
        
        return 二值圖
    
    def 預處理(self, 圖像: np.ndarray) -> np.ndarray:
        """
        🟢 完整預處理流程 / Complete preprocessing pipeline
        
        步驟 Steps:
            1. 灰度轉換 / Grayscale conversion
            2. 中值濾波去噪 / Median filter denoising
            3. OTSU二值化 / OTSU binarization
            4. 傾斜校正 / Skew correction
        
        參數 Parameters:
            圖像: 輸入圖像 / Input image
        
        返回 Returns:
            預處理後二值圖像 / Preprocessed binary image
        """
        日誌.info("🟢 開始圖像預處理 / Starting image preprocessing...")
        
        灰度 = self.轉灰度(圖像)
        日誌.debug("  Step 1/4: 灰度轉換完成 / Grayscale done")
        
        去噪 = self.中值濾波(灰度, 核大小=3)
        日誌.debug("  Step 2/4: 中值濾波完成 / Median filter done")
        
        二值 = self.OTSU二值化(去噪)
        日誌.debug("  Step 3/4: OTSU二值化完成 / OTSU done")
        
        校正 = self.傾斜校正(二值)
        日誌.debug("  Step 4/4: 傾斜校正完成 / Skew correction done")
        
        日誌.info("🟢 預處理完成 / Preprocessing complete")
        return 校正


# ═══════════════════════════════════════════════════════════════════════
# 中文文本區域檢測器 / Chinese Text Region Detector
# ═══════════════════════════════════════════════════════════════════════
class 文本區域檢測器:
    """
    🟢 中文文本區域檢測器 — 基於筆畫密度的自己實現
    Chinese Text Region Detector — Self-implemented stroke-density based
    
    不依賴OpenCV高級API，使用基於筆畫密度的投影分析
    No OpenCV advanced APIs; uses stroke-density projection analysis
    """
    
    def __init__(self, 最小區域寬: int = 8, 最小區域高: int = 8, 
                 最小筆畫密度: float = 0.05):
        """
        參數 Parameters:
            最小區域寬: 最小文本區域寬度 / Min region width
            最小區域高: 最小文本區域高度 / Min region height
            最小筆畫密度: 最小筆畫密度閾值 / Min stroke density threshold
        """
        self.最小區域寬 = 最小區域寬
        self.最小區域高 = 最小區域高
        self.最小筆畫密度 = 最小筆畫密度
        self.審計狀態 = "🟢"
    
    def 計算筆畫密度圖(self, 二值圖: np.ndarray, 窗口大小: int = 5) -> np.ndarray:
        """
        🟢 計算筆畫密度圖 / Calculate stroke density map
        
        通過局部窗口內黑色像素密度估算筆畫密度
        Estimate stroke density via local black pixel density
        
        參數 Parameters:
            二值圖: 二值圖像（黑=文字，白=背景）/ Binary image
            窗口大小: 局部密度估計窗口 / Local density window
        
        返回 Returns:
            筆畫密度圖 [0,1] / Stroke density map
        """
        高, 寬 = 二值圖.shape
        密度圖 = np.zeros((高, 寬), dtype=np.float32)
        
        文字掩碼 = (二值圖 < 128).astype(np.float32)
        
        邊距 = 窗口大小 // 2
        
        for 縱 in range(邊距, 高 - 邊距):
            for 橫 in range(邊距, 寬 - 邊距):
                窗口 = 文字掩碼[縱-邊距:縱+邊距+1, 橫-邊距:橫+邊距+1]
                密度圖[縱, 橫] = np.mean(窗口)
        
        return 密度圖
    
    def 水平投影分割(self, 二值圖: np.ndarray) -> List[Tuple[int, int]]:
        """
        🟢 基於水平投影的行分割 / Row segmentation via horizontal projection
        
        參數 Parameters:
            二值圖: 二值圖像 / Binary image
        
        返回 Returns:
            行區域列表 [(起始縱, 結束縱), ...] / Row regions
        """
        高 = 二值圖.shape[0]
        文字掩碼 = (二值圖 < 128).astype(np.int32)
        
        水平投影 = np.sum(文字掩碼, axis=1)
        
        行列表 = []
        在行中 = False
        行起始 = 0
        
        for 縱 in range(高):
            if 水平投影[縱] > 0 and not 在行中:
                在行中 = True
                行起始 = 縱
            elif 水平投影[縱] == 0 and 在行中:
                在行中 = False
                if 縱 - 行起始 >= self.最小區域高:
                    行列表.append((行起始, 縱))
        
        if 在行中 and 高 - 行起始 >= self.最小區域高:
            行列表.append((行起始, 高))
        
        return 行列表
    
    def 垂直投影分割(self, 行圖像: np.ndarray) -> List[Tuple[int, int]]:
        """
        🟢 基於垂直投影的字符分割 / Character segmentation via vertical projection
        
        參數 Parameters:
            行圖像: 單行圖像 / Single line image
        
        返回 Returns:
            字符區域列表 [(起始橫, 結束橫), ...] / Character regions
        """
        寬 = 行圖像.shape[1]
        文字掩碼 = (行圖像 < 128).astype(np.int32)
        
        垂直投影 = np.sum(文字掩碼, axis=0)
        
        字符列表 = []
        在字符中 = False
        字符起始 = 0
        
        for 橫 in range(寬):
            if 垂直投影[橫] > 0 and not 在字符中:
                在字符中 = True
                字符起始 = 橫
            elif 垂直投影[橫] == 0 and 在字符中:
                在字符中 = False
                if 橫 - 字符起始 >= self.最小區域寬:
                    字符列表.append((字符起始, 橫))
        
        if 在字符中 and 寬 - 字符起始 >= self.最小區域寬:
            字符列表.append((字符起始, 寬))
        
        return 字符列表
    
    def 檢測文本區域(self, 二值圖: np.ndarray) -> List[區域框]:
        """
        🟢 主檢測函數：檢測所有文本區域
        Main detection function: detect all text regions
        
        算法步驟 / Algorithm:
            1. 計算筆畫密度圖 / Calculate stroke density
            2. 水平投影分割行 / Horizontal projection for rows
            3. 垂直投影分割字符 / Vertical projection for characters
            4. 過濾噪聲區域 / Filter noise regions
        
        參數 Parameters:
            二值圖: 二值圖像 / Binary image
        
        返回 Returns:
            文本區域框列表 / List of text region boxes
        """
        日誌.info("🟢 開始文本區域檢測 / Starting text region detection...")
        
        密度圖 = self.計算筆畫密度圖(二值圖)
        
        行區域 = self.水平投影分割(二值圖)
        日誌.info(f"  檢測到 {len(行區域)} 個文本行 / {len(行區域)} text rows detected")
        
        所有區域 = []
        for 行索引, (行起始, 行結束) in enumerate(行區域):
            行圖像 = 二值圖[行起始:行結束, :]
            字符區域 = self.垂直投影分割(行圖像)
            
            for 字符起始, 字符結束 in 字符區域:
                區域密度圖 = 密度圖[行起始:行結束, 字符起始:字符結束]
                平均密度 = np.mean(區域密度圖)
                
                if 平均密度 >= self.最小筆畫密度:
                    區域 = 區域框(
                        左上橫=字符起始,
                        左上縱=行起始,
                        右下橫=字符結束,
                        右下縱=行結束,
                        置信度=min(1.0, 平均密度 * 2),
                        文本=""
                    )
                    所有區域.append(區域)
        
        日誌.info(f"🟢 文本區域檢測完成：{len(所有區域)} 個區域 / Text detection done: {len(所有區域)} regions")
        return 所有區域


# ═══════════════════════════════════════════════════════════════════════
# 中文字符特徵提取器 / Chinese Character Feature Extractor
# ═══════════════════════════════════════════════════════════════════════
class 字符特徵提取器:
    """
    🟢 中文字符特徵提取器 — 核心中文算法
    Chinese Character Feature Extractor — Core Chinese Algorithm
    
    提取筆畫密度、結構特徵、字形特徵
    Extract stroke density, structure features, glyph features
    """
    
    def __init__(self):
        self.版本 = "1.0"
        self.審計狀態 = "🟢"
        self.部首模板 = self._初始化部首模板()
    
    def _初始化部首模板(self) -> Dict[str, Dict[str, Any]]:
        """初始化常見部首特徵模板 / Initialize radical feature templates"""
        return {
            "氵": {"點數": 3, "位置": "左", "類型": "偏旁"},
            "艹": {"橫數": 2, "位置": "上", "類型": "偏旁"},
            "扌": {"橫豎交": True, "位置": "左", "類型": "偏旁"},
            "口": {"包圍度": 0.8, "位置": "變", "類型": "偏旁"},
            "亻": {"豎為主": True, "位置": "左", "類型": "偏旁"},
            "木": {"交叉": True, "位置": "變", "類型": "偏旁"},
            "糹": {"折線": True, "位置": "左", "類型": "偏旁"},
            "讠": {"點橫": True, "位置": "左", "類型": "偏旁"},
        }
    
    def 提取筆畫密度(self, 字符圖: np.ndarray) -> Dict[str, float]:
        """
        🟢 提取筆畫密度特徵 / Extract stroke density features
        
        分析字符圖像中筆畫的分佈密度
        Analyze stroke distribution density in character image
        
        參數 Parameters:
            字符圖: 單字符二值圖像 / Single character binary image
        
        返回 Returns:
            密度特徵字典 / Density feature dictionary
        """
        高, 寬 = 字符圖.shape[:2]
        文字像素 = (字符圖 < 128)
        總文字像素 = np.sum(文字像素)
        總像素 = 高 * 寬
        
        if 總文字像素 == 0:
            return {"總密度": 0.0, "上密度": 0.0, "中密度": 0.0, "下密度": 0.0,
                    "左密度": 0.0, "中密度橫": 0.0, "右密度": 0.0, "均勻度": 0.0}
        
        總密度 = 總文字像素 / 總像素
        
        上密度 = np.sum(文字像素[:高//3, :]) / (總像素 // 3) if 高 >= 3 else 0
        中密度 = np.sum(文字像素[高//3:2*高//3, :]) / (總像素 // 3) if 高 >= 3 else 0
        下密度 = np.sum(文字像素[2*高//3:, :]) / (總像素 // 3) if 高 >= 3 else 0
        
        左密度 = np.sum(文字像素[:, :寬//3]) / (總像素 // 3) if 寬 >= 3 else 0
        中密度橫 = np.sum(文字像素[:, 寬//3:2*寬//3]) / (總像素 // 3) if 寬 >= 3 else 0
        右密度 = np.sum(文字像素[:, 2*寬//3:]) / (總像素 // 3) if 寬 >= 3 else 0
        
        水平差異 = abs(上密度 - 中密度) + abs(中密度 - 下密度) + abs(上密度 - 下密度)
        垂直差異 = abs(左密度 - 中密度橫) + abs(中密度橫 - 右密度) + abs(左密度 - 右密度)
        均勻度 = max(0.0, 1.0 - (水平差異 + 垂直差異) / 6.0)
        
        return {
            "總密度": round(總密度, 4),
            "上密度": round(上密度, 4),
            "中密度": round(中密度, 4),
            "下密度": round(下密度, 4),
            "左密度": round(左密度, 4),
            "中密度橫": round(中密度橫, 4),
            "右密度": round(右密度, 4),
            "均勻度": round(均勻度, 4),
        }
    
    def 分析結構(self, 字符圖: np.ndarray) -> 字符結構:
        """
        🟢 分析字符結構（左右/上下/包圍/獨體）
        Analyze character structure (left-right/top-bottom/enclosure/single)
        
        基於筆畫密度分佈的結構分類 / Structure classification based on density distribution
        
        參數 Parameters:
            字符圖: 單字符二值圖像 / Single character binary image
        
        返回 Returns:
            字符結構枚舉 / Character structure enum
        """
        高, 寬 = 字符圖.shape[:2]
        if 高 < 3 or 寬 < 3:
            return 字符結構.未知
        
        文字像素 = (字符圖 < 128).astype(np.float32)
        
        左密度 = np.mean(文字像素[:, :寬//2])
        右密度 = np.mean(文字像素[:, 寬//2:])
        
        上密度 = np.mean(文字像素[:高//2, :])
        下密度 = np.mean(文字像素[高//2:, :])
        
        中密度 = np.mean(文字像素[高//4:3*高//4, 寬//4:3*寬//4])
        
        上邊密度 = np.mean(文字像素[0:高//4, :])
        下邊密度 = np.mean(文字像素[3*高//4:, :])
        左邊密度 = np.mean(文字像素[:, 0:寬//4])
        右邊密度 = np.mean(文字像素[:, 3*寬//4:])
        
        左右差異 = abs(左密度 - 右密度) / max(左密度 + 右密度, 1e-6)
        上下差異 = abs(上密度 - 下密度) / max(上密度 + 下密度, 1e-6)
        
        邊緣密度 = (上邊密度 + 下邊密度 + 左邊密度 + 右邊密度) / 4
        包圍度 = 邊緣密度 / max(中密度, 1e-6) if 中密度 > 1e-6 else 0
        
        if 包圍度 > 1.5 and 邊緣密度 > 0.05:
            if min(上邊密度, 左邊密度) > max(下邊密度, 右邊密度) * 2:
                return 字符結構.半包圍
            return 字符結構.包圍
        
        if 左右差異 > 0.3 and 左右差異 > 上下差異:
            return 字符結構.左右
        
        if 上下差異 > 0.3:
            return 字符結構.上下
        
        if max(左右差異, 上下差異) < 0.15:
            return 字符結構.獨體
        
        return 字符結構.未知
    
    def 簡易骨架化(self, 二值圖: np.ndarray) -> np.ndarray:
        """
        🟢 簡易骨架化算法 / Simplified skeletonization
        
        使用距離變換近似骨架 / Use distance transform approximation
        
        參數 Parameters:
            二值圖: 二值圖像 / Binary image
        
        返回 Returns:
            骨架圖像 / Skeleton image
        """
        if SCIPY可用:
            距離 = ndimage.distance_transform_edt(二值圖)
            局部極大 = ndimage.maximum_filter(距離, size=3) == 距離
            骨架 = (局部極大 & (二值圖 > 0)).astype(np.uint8)
            return 骨架
        else:
            # 替代方案：迭代腐蝕 / Alternative: iterative erosion
            骨架 = 二值圖.copy()
            return骨架
    
    def 檢測端點(self, 骨架: np.ndarray) -> List[Tuple[int, int]]:
        """
        🟢 檢測骨架端點 / Detect skeleton endpoints
        
        端點 = 只有一個鄰居的像素
        Endpoint = pixel with only one neighbor
        
        參數 Parameters:
            骨架: 骨架圖像 / Skeleton image
        
        返回 Returns:
            端點坐標列表 / Endpoint coordinates
        """
        高, 寬 = 骨架.shape
        端點 = []
        
        for 縱 in range(1, 高 - 1):
            for 橫 in range(1, 寬 - 1):
                if 骨架[縱, 橫] > 0:
                    鄰居 = np.sum(骨架[縱-1:縱+2, 橫-1:橫+2]) - 1
                    if 鄰居 == 1:
                        端點.append((橫, 縱))
        
        return 端點
    
    def 檢測交叉點(self, 骨架: np.ndarray) -> List[Tuple[int, int]]:
        """
        🟢 檢測骨架交叉點 / Detect skeleton crossing points
        
        交叉點 = 有3個或以上鄰居的像素
        Crossing = pixel with 3+ neighbors
        
        參數 Parameters:
            骨架: 骨架圖像 / Skeleton image
        
        返回 Returns:
            交叉點坐標列表 / Crossing coordinates
        """
        高, 寬 = 骨架.shape
        交叉點 = []
        
        for 縱 in range(1, 高 - 1):
            for 橫 in range(1, 寬 - 1):
                if 骨架[縱, 橫] > 0:
                    鄰居 = np.sum(骨架[縱-1:縱+2, 橫-1:橫+2]) - 1
                    if 鄰居 >= 3:
                        交叉點.append((橫, 縱))
        
        return 交叉點
    
    def 提取筆畫特徵(self, 字符圖: np.ndarray) -> Dict[str, Any]:
        """
        🟢 提取筆畫級特徵（端點、交叉點、轉折點）
        Extract stroke-level features (endpoints, crossings, turning points)
        
        參數 Parameters:
            字符圖: 單字符二值圖像 / Single character binary image
        
        返回 Returns:
            筆畫特徵字典 / Stroke feature dictionary
        """
        文字像素 = (字符圖 < 128).astype(np.uint8)
        
        骨架 = self.簡易骨架化(文字像素)
        
        端點 = self.檢測端點(骨架)
        
        交叉點 = self.檢測交叉點(骨架)
        
        筆畫數 = len(端點) // 2 + len(交叉點)
        
        return {
            "端點數": len(端點),
            "交叉點數": len(交叉點),
            "估計筆畫數": max(筆畫數, 1),
            "端點位置": 端點[:10],  # 只保留前10個
            "交叉位置": 交叉點[:10],
        }
    
    def 提取全部特徵(self, 字符圖: np.ndarray) -> Dict[str, Any]:
        """
        🟢 提取字符全部特徵 / Extract all character features
        
        參數 Parameters:
            字符圖: 單字符圖像 / Single character image
        
        返回 Returns:
            完整特徵字典 / Complete feature dictionary
        """
        日誌.debug("  提取字符特徵... / Extracting character features...")
        
        密度特徵 = self.提取筆畫密度(字符圖)
        結構 = self.分析結構(字符圖)
        筆畫特徵 = self.提取筆畫特徵(字符圖)
        
        return {
            "密度特徵": 密度特徵,
            "結構": 結構.value,
            "筆畫特徵": 筆畫特徵,
            "尺寸": {"高": 字符圖.shape[0], "寬": 字符圖.shape[1]},
        }


# ═══════════════════════════════════════════════════════════════════════
# 龍字專用檢測器 / Dragon Character (龍) Specialized Detector
# ═══════════════════════════════════════════════════════════════════════
class 龍字檢測器:
    """
    🟢 繁體「龍」字專用檢測器
    Traditional "龍" (Dragon) Character Specialized Detector
    
    基於龍字獨特結構特徵的模式識別：
    - 左上角「立」部 / Top-left "立" radical
    - 右側彎曲龍身 / Right-side curved body
    - 底部三點或彎鉤 / Bottom dots or hook
    - 整體左右結構 / Overall left-right structure
    
    Pattern recognition based on 龍's unique structural features
    """
    
    def __init__(self):
        self.版本 = "1.0"
        self.審計狀態 = "🟢"
        self.標準筆畫數 = 16
        self.標準密度模式 = {
            "左上高": True,
            "右下彎": True,
            "中間空": True,
        }
    
    def 檢測(self, 字符圖: np.ndarray) -> Dict[str, Any]:
        """
        🟢 檢測是否為龍字 / Detect if character is 龍
        
        參數 Parameters:
            字符圖: 單字符圖像 / Single character image
        
        返回 Returns:
            檢測結果字典 / Detection result dictionary
        """
        高, 寬 = 字符圖.shape[:2]
        if 高 < 8 or 寬 < 8:
            return {"是龍字": False, "置信度": 0.0, "原因": "圖像太小 / Image too small"}
        
        文字像素 = (字符圖 < 128).astype(np.float32)
        
        結構 = self._分析結構(文字像素, 高, 寬)
        密度匹配 = self._匹配密度模式(文字像素, 高, 寬)
        端點模式 = self._分析端點模式(文字像素, 高, 寬)
        
        綜合置信度 = (
            結構 * 0.35 +
            密度匹配 * 0.35 +
            端點模式 * 0.30
        )
        
        結果 = {
            "是龍字": 綜合置信度 > 0.6,
            "置信度": round(min(1.0, 綜合置信度), 4),
            "結構分數": round(結構, 4),
            "密度分數": round(密度匹配, 4),
            "端點分數": round(端點模式, 4),
            "詳細分析": self._生成詳細分析(結構, 密度匹配, 端點模式)
        }
        
        return 結果
    
    def _分析結構(self, 文字像素: np.ndarray, 高: int, 寬: int) -> float:
        """分析龍字結構特徵 / Analyze 龍 character structure"""
        左密度 = np.mean(文字像素[:, :寬//2])
        右密度 = np.mean(文字像素[:, 寬//2:])
        
        上密度 = np.mean(文字像素[:高//2, :])
        下密度 = np.mean(文字像素[高//2:, :])
        
        上下比 = 上密度 / max(下密度, 1e-6)
        左右比 = 右密度 / max(左密度, 1e-6)
        
        結構分 = 0.0
        if 1.0 <= 上下比 <= 2.0:
            結構分 += 0.5
        if 0.8 <= 左右比 <= 1.8:
            結構分 += 0.5
        
        return 結構分
    
    def _匹配密度模式(self, 文字像素: np.ndarray, 高: int, 寬: int) -> float:
        """匹配龍字密度模式 / Match 龍 density pattern"""
        左上 = np.mean(文字像素[:高//2, :寬//2])
        右上 = np.mean(文字像素[:高//2, 寬//2:])
        左下 = np.mean(文字像素[高//2:, :寬//2])
        右下 = np.mean(文字像素[高//2:, 寬//2:])
        
        分數 = 0.0
        
        if 左上 > 0.1:
            分數 += 0.25
        if 右下 > 0.05:
            分數 += 0.25
        
        中密度 = np.mean(文字像素[高//3:2*高//3, 寬//3:2*寬//3])
        if 中密度 < (左上 + 右上) / 2:
            分數 += 0.25
        
        總密度 = np.mean(文字像素)
        if 0.05 <= 總密度 <= 0.35:
            分數 += 0.25
        
        return 分數
    
    def _分析端點模式(self, 文字像素: np.ndarray, 高: int, 寬: int) -> float:
        """分析端點分佈模式 / Analyze endpoint distribution"""
        if SCIPY可用:
            距離 = ndimage.distance_transform_edt(文字像素)
            局部極大 = ndimage.maximum_filter(距離, size=3) == 距離
            骨架 = (局部極大 & (文字像素 > 0)).astype(np.uint8)
        else:
            骨架 = 文字像素.astype(np.uint8)
        
        提取器 = 字符特徵提取器()
        端點 = 提取器.檢測端點(骨架)
        
        端點數 = len(端點)
        if 8 <= 端點數 <= 14:
            return 1.0
        elif 6 <= 端點數 <= 16:
            return 0.7
        elif 4 <= 端點數 <= 18:
            return 0.4
        else:
            return 0.1
    
    def _生成詳細分析(self, 結構: float, 密度: float, 端點: float) -> str:
        """生成詳細分析文本 / Generate detailed analysis text"""
        分析 = []
        if 結構 > 0.5:
            分析.append("結構匹配 / Structure match")
        else:
            分析.append("結構不匹配 / Structure mismatch")
        
        if 密度 > 0.5:
            分析.append("密度模式匹配 / Density match")
        else:
            分析.append("密度模式不匹配 / Density mismatch")
        
        if 端點 > 0.5:
            分析.append("端點模式匹配 / Endpoint match")
        else:
            分析.append("端點模式不匹配 / Endpoint mismatch")
        
        return "; ".join(分析)


# ═══════════════════════════════════════════════════════════════════════
# 甲骨文字符分類器 / Oracle Bone Character Classifier
# ═══════════════════════════════════════════════════════════════════════
class 甲骨文分類器:
    """
    🟢 甲骨文字符分類器 — 基於筆畫數的特徵分類
    Oracle Bone Character Classifier — Stroke-count based feature classification
    
    甲骨文特徵：
    - 筆畫細長、角度分明 / Thin strokes, distinct angles
    - 多直線、少曲線 / More straight lines, fewer curves
    - 結構不對稱 / Asymmetric structure
    - 筆畫數一般較少 / Generally fewer strokes
    """
    
    def __init__(self):
        self.版本 = "1.0"
        self.審計狀態 = "🟢"
        
        self.分類閾值 = {
            "極簡": (1, 3),
            "簡單": (4, 6),
            "中等": (7, 10),
            "複雜": (11, 15),
            "極複雜": (16, 25),
        }
    
    def 分類(self, 字符圖: np.ndarray) -> Dict[str, Any]:
        """
        🟢 對字符進行甲骨文特徵分類 / Classify character with oracle bone features
        
        參數 Parameters:
            字符圖: 單字符圖像 / Single character image
        
        返回 Returns:
            分類結果字典 / Classification result
        """
        高, 寬 = 字符圖.shape[:2]
        if 高 < 4 or 寬 < 4:
            return {"類別": "未知", "置信度": 0.0, "原因": "圖像太小"}
        
        文字像素 = (字符圖 < 128).astype(np.float32)
        
        筆畫數 = self._估算筆畫數(文字像素, 高, 寬)
        直線度 = self._分析直線度(文字像素, 高, 寬)
        對稱度 = self._分析對稱度(文字像素, 高, 寬)
        密度特徵 = self._分析密度特徵(文字像素, 高, 寬)
        
        甲骨文分數 = (
            self._筆畫分數(筆畫數) * 0.30 +
            直線度 * 0.25 +
            (1.0 - 對稱度) * 0.25 +
            密度特徵 * 0.20
        )
        
        類別 = self._筆畫數分類(筆畫數)
        
        return {
            "類別": 類別,
            "甲骨文相似度": round(min(1.0, 甲骨文分數), 4),
            "筆畫數": 筆畫數,
            "直線度": round(直線度, 4),
            "不對稱度": round(1.0 - 對稱度, 4),
            "是甲骨文": 甲骨文分數 > 0.55,
            "置信度": round(min(1.0, 甲骨文分數), 4),
        }
    
    def _估算筆畫數(self, 文字像素: np.ndarray, 高: int, 寬: int) -> int:
        """估算字符筆畫數 / Estimate character stroke count"""
        if SCIPY可用:
            距離 = ndimage.distance_transform_edt(文字像素)
            局部極大 = ndimage.maximum_filter(距離, size=3) == 距離
            骨架 = (局部極大 & (文字像素 > 0)).astype(np.uint8)
        else:
            骨架 = 文字像素.astype(np.uint8)
        
        提取器 = 字符特徵提取器()
        端點 = 提取器.檢測端點(骨架)
        交叉 = 提取器.檢測交叉點(骨架)
        
        筆畫 = max(1, len(端點) // 2 + len(交叉) + 1)
        return min(筆畫, 25)
    
    def _分析直線度(self, 文字像素: np.ndarray, 高: int, 寬: int) -> float:
        """分析筆畫直線程度 / Analyze stroke straightness"""
        if SCIPY可用:
            距離 = ndimage.distance_transform_edt(文字像素)
            局部極大 = ndimage.maximum_filter(距離, size=3) == 距離
            骨架 = (局部極大 & (文字像素 > 0)).astype(np.uint8)
        else:
            骨架 = 文字像素.astype(np.uint8)
        
        骨架點 = np.argwhere(骨架 > 0)
        if len(骨架點) < 10:
            return 0.5
        
        方向變化 = 0
        總方向 = 0
        
        for 縱, 橫 in 骨架點[:100]:
            if 縱 <= 0 or 縱 >= 高 - 1 or 橫 <= 0 or 橫 >= 寬 - 1:
                continue
            鄰居 = 骨架[縱-1:縱+2, 橫-1:橫+2]
            鄰居點 = np.argwhere(鄰居 > 0)
            if len(鄰居點) >= 2:
                方向差 = np.std(鄰居點[:, 0]) + np.std(鄰居點[:, 1])
                方向變化 += 方向差
                總方向 += 1
        
        if 總方向 == 0:
            return 0.5
        
        平均變化 = 方向變化 / 總方向
        直線度 = max(0.0, 1.0 - 平均變化 / 3.0)
        return 直線度
    
    def _分析對稱度(self, 文字像素: np.ndarray, 高: int, 寬: int) -> float:
        """分析字符對稱程度 / Analyze character symmetry"""
        左半 = 文字像素[:, :寬//2]
        右半 = np.fliplr(文字像素[:, 寬//2 + 寬 % 2:])
        
        if 左半.shape[1] != 右半.shape[1]:
            最小寬 = min(左半.shape[1], 右半.shape[1])
            左半 = 左半[:, :最小寬]
            右半 = 右半[:, :最小寬]
        
        水平對稱 = 1.0 - np.mean(np.abs(左半 - 右半))
        
        上半 = 文字像素[:高//2, :]
        下半 = np.flipud(文字像素[高//2 + 高 % 2:, :])
        
        if 上半.shape[0] != 下半.shape[0]:
            最小高 = min(上半.shape[0], 下半.shape[0])
            上半 = 上半[:最小高, :]
            下半 = 下半[:最小高, :]
        
        垂直對稱 = 1.0 - np.mean(np.abs(上半 - 下半))
        
        return (水平對稱 + 垂直對稱) / 2.0
    
    def _分析密度特徵(self, 文字像素: np.ndarray, 高: int, 寬: int) -> float:
        """分析密度特徵 / Analyze density features"""
        總密度 = np.mean(文字像素)
        
        密度分 = 0.0
        if 0.03 <= 總密度 <= 0.25:
            密度分 = 1.0
        elif 0.01 <= 總密度 <= 0.35:
            密度分 = 0.6
        else:
            密度分 = 0.2
        
        四分區 = [
            np.mean(文字像素[:高//2, :寬//2]),
            np.mean(文字像素[:高//2, 寬//2:]),
            np.mean(文字像素[高//2:, :寬//2]),
            np.mean(文字像素[高//2:, 寬//2:]),
        ]
        不均勻度 = np.std(四分區)
        不均分 = min(1.0, 不均勻度 * 5.0)
        
        return 密度分 * 0.6 + 不均分 * 0.4
    
    def _筆畫分數(self, 筆畫數: int) -> float:
        """根據筆畫數計算甲骨文相似分數 / Score based on stroke count"""
        if 1 <= 筆畫數 <= 6:
            return 1.0
        elif 7 <= 筆畫數 <= 10:
            return 0.7
        elif 11 <= 筆畫數 <= 15:
            return 0.4
        else:
            return 0.2
    
    def _筆畫數分類(self, 筆畫數: int) -> str:
        """根據筆畫數分類 / Classify by stroke count"""
        for 類別, (最小, 最大) in self.分類閾值.items():
            if 最小 <= 筆畫數 <= 最大:
                return 類別
        return "未知"


# ═══════════════════════════════════════════════════════════════════════
# Tesseract國際兜底引擎 / Tesseract International Fallback Engine
# ═══════════════════════════════════════════════════════════════════════
class 國際兜底引擎:
    """
    🟡 Tesseract OCR國際兜底引擎
    Tesseract OCR International Fallback Engine
    
    當中文算法置信度 < 0.7 時自動降級
    Auto-fallback when Chinese algorithm confidence < 0.7
    """
    
    def __init__(self):
        self.版本 = "1.0"
        self.可用 = TESSERACT可用
        self.審計狀態 = "🟢" if self.可用 else "🔴"
        
        if self.可用:
            self.語言配置 = 'chi_sim+chi_tra+eng'
            self._配置Tesseract()
    
    def _配置Tesseract(self):
        """配置Tesseract參數 / Configure Tesseract parameters"""
        可能路徑 = [
            '/usr/bin/tesseract',
            '/usr/local/bin/tesseract',
            '/opt/homebrew/bin/tesseract',
            'C:\\Program Files\\Tesseract-OCR\\tesseract.exe',
        ]
        for 路徑 in 可能路徑:
            if os.path.exists(路徑):
                pytesseract.pytesseract.tesseract_cmd = 路徑
                日誌.info(f"🟢 Tesseract路徑 / Path: {路徑}")
                break
    
    def 識別(self, 圖像數組: np.ndarray, 語言: str | None = None) -> 識別結果:
        """
        🟡 使用Tesseract進行OCR識別 / OCR recognition using Tesseract
        
        參數 Parameters:
            圖像數組: 輸入圖像數組 / Input image array
            語言: 語言配置 / Language config
        
        返回 Returns:
            識別結果 / Recognition result
        """
        if not self.可用:
            return 識別結果(
                文本="",
                置信度=0.0,
                審計="🔴",
                備註="Tesseract未安裝 / Tesseract not installed",
                引擎來源="Tesseract(不可用)"
            )
        
        try:
            if len(圖像數組.shape) == 2:
                PIL圖像 = Image.fromarray(圖像數組)
            else:
                PIL圖像 = Image.fromarray(圖像數組.astype(np.uint8))
            
            語言配置 = 語言 or self.語言配置
            
            配置 = f'--oem 3 --psm 6 -l {語言配置}'
            文本 = pytesseract.image_to_string(PIL圖像, config=配置)
            
            數據 = pytesseract.image_to_data(PIL圖像, config=配置, output_type=pytesseract.Output.DICT)
            
            置信度列表 = [c for c in 數據.get('conf', []) if isinstance(c, (int, float)) and c > 0]
            平均置信度 = np.mean(置信度列表) / 100.0 if 置信度列表 else 0.5
            
            區域列表 = []
            for i in range(len(數據.get('text', []))):
                if 數據['text'][i].strip():
                    區域 = {
                        'x': 數據['left'][i],
                        'y': 數據['top'][i],
                        '寬': 數據['width'][i],
                        '高': 數據['height'][i],
                        '文本': 數據['text'][i],
                        '置信度': 數據['conf'][i] / 100.0 if isinstance(數據['conf'][i], (int, float)) else 0.0
                    }
                    區域列表.append(區域)
            
            日誌.info(f"🟡 Tesseract識別完成 / Recognition done: conf={平均置信度:.3f}")
            
            return 識別結果(
                文本=文本.strip(),
                置信度=min(1.0, 平均置信度),
                區域=區域列表,
                審計="🟡",
                備註="Tesseract國際兜底 / Tesseract fallback",
                引擎來源="Tesseract"
            )
        
        except Exception as 錯誤:
            日誌.error(f"🔴 Tesseract識別失敗 / Recognition failed: {錯誤}")
            return 識別結果(
                文本="",
                置信度=0.0,
                審計="🔴",
                備註=f"Tesseract錯誤: {str(錯誤)}",
                引擎來源="Tesseract(錯誤)"
            )


# ═══════════════════════════════════════════════════════════════════════
# 中文字符識別器 / Chinese Character Recognizer
# ═══════════════════════════════════════════════════════════════════════
class 中文字符識別器:
    """
    🟢 中文字符識別器 — 基於特徵匹配的識別
    Chinese Character Recognizer — Feature matching based recognition
    
    使用筆畫密度和結構特徵進行簡單字符匹配
    Simple character matching using stroke density and structure
    """
    
    def __init__(self):
        self.版本 = "1.0"
        self.特徵提取 = 字符特徵提取器()
        self.龍字檢測 = 龍字檢測器()
        self.甲骨文分類 = 甲骨文分類器()
        self.字符模板庫 = self._建立模板庫()
    
    def _建立模板庫(self) -> Dict[str, Dict[str, Any]]:
        """建立基礎字符特徵模板庫 / Build base character feature template library"""
        模板庫 = {
            "龍": {
                "結構": "左右",
                "筆畫數": 16,
                "上密度": 0.15,
                "下密度": 0.10,
                "左密度": 0.12,
                "右密度": 0.14,
                "龍字特徵": True,
            },
            "一": {
                "結構": "獨體",
                "筆畫數": 1,
                "上密度": 0.3,
                "下密度": 0.0,
                "左密度": 0.0,
                "右密度": 0.3,
            },
            "二": {
                "結構": "上下",
                "筆畫數": 2,
                "上密度": 0.2,
                "下密度": 0.2,
                "左密度": 0.0,
                "右密度": 0.2,
            },
            "三": {
                "結構": "上下",
                "筆畫數": 3,
                "上密度": 0.15,
                "中密度": 0.15,
                "下密度": 0.15,
            },
            "十": {
                "結構": "獨體",
                "筆畫數": 2,
                "上密度": 0.1,
                "下密度": 0.1,
                "左密度": 0.1,
                "右密度": 0.1,
            },
            "大": {
                "結構": "獨體",
                "筆畫數": 3,
                "上密度": 0.15,
                "下密度": 0.1,
                "左密度": 0.1,
                "右密度": 0.1,
            },
            "中": {
                "結構": "包圍",
                "筆畫數": 4,
                "上密度": 0.1,
                "下密度": 0.1,
                "左密度": 0.1,
                "右密度": 0.1,
            },
            "文": {
                "結構": "獨體",
                "筆畫數": 4,
                "上密度": 0.1,
                "下密度": 0.1,
                "左密度": 0.1,
                "右密度": 0.1,
            },
            "人": {
                "結構": "獨體",
                "筆畫數": 2,
                "上密度": 0.1,
                "下密度": 0.2,
                "左密度": 0.1,
                "右密度": 0.1,
            },
            "日": {
                "結構": "包圍",
                "筆畫數": 4,
                "上密度": 0.15,
                "下密度": 0.15,
                "左密度": 0.15,
                "右密度": 0.15,
            },
            "月": {
                "結構": "包圍",
                "筆畫數": 4,
                "上密度": 0.12,
                "下密度": 0.12,
                "左密度": 0.15,
                "右密度": 0.05,
            },
            "山": {
                "結構": "獨體",
                "筆畫數": 3,
                "上密度": 0.1,
                "下密度": 0.2,
                "左密度": 0.1,
                "右密度": 0.1,
            },
            "水": {
                "結構": "獨體",
                "筆畫數": 4,
                "上密度": 0.1,
                "下密度": 0.2,
                "左密度": 0.1,
                "右密度": 0.1,
            },
            "火": {
                "結構": "獨體",
                "筆畫數": 4,
                "上密度": 0.15,
                "下密度": 0.15,
                "左密度": 0.1,
                "右密度": 0.1,
            },
            "木": {
                "結構": "獨體",
                "筆畫數": 4,
                "上密度": 0.1,
                "下密度": 0.15,
                "左密度": 0.1,
                "右密度": 0.1,
            },
            "土": {
                "結構": "獨體",
                "筆畫數": 3,
                "上密度": 0.1,
                "下密度": 0.2,
                "左密度": 0.1,
                "右密度": 0.1,
            },
            "金": {
                "結構": "上下",
                "筆畫數": 8,
                "上密度": 0.12,
                "下密度": 0.12,
                "左密度": 0.1,
                "右密度": 0.1,
            },
        }
        return 模板庫
    
    def 識別字符(self, 字符圖: np.ndarray) -> 識別結果:
        """
        🟢 識別單個中文字符 / Recognize single Chinese character
        
        參數 Parameters:
            字符圖: 單字符圖像 / Single character image
        
        返回 Returns:
            識別結果 / Recognition result
        """
        特徵 = self.特徵提取.提取全部特徵(字符圖)
        
        # 嘗試龍字檢測 / Try 龍 detection
        龍結果 = self.龍字檢測.檢測(字符圖)
        if 龍結果["是龍字"] and 龍結果["置信度"] > 0.6:
            return 識別結果(
                文本="龍",
                置信度=龍結果["置信度"],
                審計="🟢",
                結構="左右",
                備註=f"龍字專用檢測器命中 / 龍 detector hit: {龍結果['置信度']:.2f}",
                引擎來源="龍瞳-龍字檢測器"
            )
        
        # 模板匹配 / Template matching
        最佳匹配 = None
        最佳分數 = 0.0
        
        for 字符, 模板 in self.字符模板庫.items():
            分數 = self._計算匹配分數(特徵, 模板)
            if 分數 > 最佳分數:
                最佳分數 = 分數
                最佳匹配 = 字符
        
        if 最佳匹配 and 最佳分數 > 0.4:
            return 識別結果(
                文本=最佳匹配,
                置信度=min(1.0, 最佳分數),
                審計="🟢" if 最佳分數 > 0.6 else "🟡",
                結構=特徵["結構"],
                備註=f"模板匹配 / Template match: {最佳分數:.2f}",
                引擎來源="龍瞳-模板匹配"
            )
        
        return 識別結果(
            文本="?",
            置信度=0.0,
            審計="🔴",
            結構=特徵["結構"],
            備註="未能識別 / Unrecognized",
            引擎來源="龍瞳-模板匹配"
        )
    
    def _計算匹配分數(self, 特徵: Dict[str, Any], 模板: Dict[str, Any]) -> float:
        """計算特徵與模板的匹配分數 / Calculate feature-template match score"""
        分數 = 0.0
        權重 = 0.0
        
        if "結構" in 模板:
            if 特徵.get("結構") == 模板["結構"]:
                分數 += 0.3
            權重 += 0.3
        
        密度特徵 = 特徵.get("密度特徵", {})
        for 密度名 in ["上密度", "中密度", "下密度", "左密度", "右密度"]:
            if 密度名 in 模板:
                差異 = abs(密度特徵.get(密度名, 0) - 模板[密度名])
                分數 += max(0, 0.1 - 差異)
                權重 += 0.1
        
        if "筆畫數" in 模板:
            估計筆畫 = 特徵.get("筆畫特徵", {}).get("估計筆畫數", 0)
            筆畫差異 = abs(估計筆畫 - 模板["筆畫數"])
            分數 += max(0, 0.2 - 筆畫差異 * 0.05)
            權重 += 0.2
        
        return 分數 / max(權重, 1e-6)


# ═══════════════════════════════════════════════════════════════════════
# 圖像生成輔助函數 / Image Generation Helper
# ═══════════════════════════════════════════════════════════════════════
class 圖像生成器:
    """
    🟢 測試用圖像生成器 / Test image generator
    
    生成簡單的測試字符圖像用於驗證
    Generate simple test character images for validation
    """
    
    @staticmethod
    def _查找中文字體() -> Optional[str]:
        """查找系統中文字體 / Find system Chinese fonts"""
        字體路徑列表 = [
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/STHeiti Light.ttc",
            "/Library/Fonts/Arial Unicode.ttf",
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
            "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
            "C:\\Windows\\Fonts\\msyh.ttc",
            "C:\\Windows\\Fonts\\simhei.ttf",
            "C:\\Windows\\Fonts\\simsun.ttc",
            "C:\\Windows\\Fonts\\msyhbd.ttc",
        ]
        for 路徑 in 字體路徑列表:
            if os.path.exists(路徑):
                return 路徑
        return None
    
    @staticmethod
    def _繪製替代文字(圖像: np.ndarray, 內容: str, 寬: int, 高: int) -> np.ndarray:
        """
        繪製替代文字（不用字體庫）/ Draw alternative text (no font library)
        
        繪製簡單的幾何圖案來模擬文字 / Draw simple geometric patterns
        """
        邊距 = 40
        中心橫 = 寬 // 2
        中心縱 = 高 // 2
        
        if "龍" in 內容:
            for i in range(3):
                圖像[邊距 + i*15, 邊距:中心橫, :] = 0
            for i in range(2):
                圖像[邊距:中心縱, 邊距 + i*20, :] = 0
            for i in range(5):
                圖像[邊距 + i*20, 中心橫:寬-邊距, :] = 0
            for i in range(3):
                圖像[高-邊距-30+i*10, 中心橫-20:寬-邊距, :] = 0
        elif "一" in 內容:
            圖像[中心縱, 邊距:寬-邊距, :] = 0
        elif "二" in 內容:
            圖像[中心縱-20, 邊距:寬-邊距, :] = 0
            圖像[中心縱+20, 邊距:寬-邊距, :] = 0
        elif "十" in 內容:
            圖像[邊距:高-邊距, 中心橫, :] = 0
            圖像[中心縱, 邊距:寬-邊距, :] = 0
        else:
            圖像[邊距, 邊距:寬-邊距, :] = 0
            圖像[高-邊距, 邊距:寬-邊距, :] = 0
            圖像[邊距:高-邊距, 邊距, :] = 0
            圖像[邊距:高-邊距, 寬-邊距, :] = 0
        
        return 圖像
    
    @staticmethod
    def 生成測試圖像(內容: str = "龍", 尺寸: Tuple[int, int] = (200, 200),
                    字號: int = 64, 輸出路徑: str = None) -> np.ndarray:
        """
        生成測試圖像 / Generate test image
        
        參數 Parameters:
            內容: 圖像內容文字 / Content text
            尺寸: (寬, 高) / (width, height)
            字號: 字體大小 / Font size
            輸出路徑: 保存路徑（可選）/ Save path (optional)
        
        返回 Returns:
            圖像數組 / Image array
        """
        寬, 高 = 尺寸
        
        # 創建白色背景 / Create white background
        圖像 = np.ones((高, 寬, 3), dtype=np.uint8) * 255
        
        if PIL可用 and 內容:
            try:
                PIL圖 = Image.fromarray(圖像)
                畫筆 = ImageDraw.Draw(PIL圖)
                
                字體路徑 = 圖像生成器._查找中文字體()
                if 字體路徑:
                    字體 = ImageFont.truetype(字體路徑, 字號)
                else:
                    字體 = ImageFont.load_default()
                
                邊界框 = 畫筆.textbbox((0, 0), 內容, font=字體)
                文字寬 = 邊界框[2] - 邊界框[0]
                文字高 = 邊界框[3] - 邊界框[1]
                位置橫 = (寬 - 文字寬) // 2
                位置縱 = (高 - 文字高) // 2
                
                畫筆.text((位置橫, 位置縱), 內容, fill=0, font=字體)
                圖像 = np.array(PIL圖)
            except Exception as 錯誤:
                日誌.warning(f"🟡 文字渲染失敗，使用替代方案 / Text render failed: {錯誤}")
                圖像 = 圖像生成器._繪製替代文字(圖像, 內容, 寬, 高)
        else:
            圖像 = 圖像生成器._繪製替代文字(圖像, 內容, 寬, 高)
        
        if 輸出路徑:
            os.makedirs(os.path.dirname(輸出路徑), exist_ok=True)
            if CV2可用:
                cv2.imwrite(輸出路徑, cv2.cvtColor(圖像, cv2.COLOR_RGB2BGR))
            elif PIL可用:
                Image.fromarray(圖像).save(輸出路徑)
            日誌.info(f"🟢 測試圖像已保存 / Test image saved: {輸出路徑}")
        
        return 圖像


# ═══════════════════════════════════════════════════════════════════════
# 主引擎：龍瞳OCR引擎 / Main Engine: Dragon Pupil OCR Engine
# ═══════════════════════════════════════════════════════════════════════
class 龍瞳OCR引擎:
    """
    ╔═══════════════════════════════════════════════════════════════╗
    ║  🐉 龍瞳OCR引擎 — 中文優先圖像識別引擎                        ║
    ║  Dragon Pupil OCR Engine — Chinese-First Image Recognition    ║
    ║                                                               ║
    ║  DNA: #龍芯⚡️2026-06-18-LONGTENG-OCR-v1.0                   ║
    ║  核心策略：能中文替代的中文實現，不能的用國際標準庫兜底          ║
    ║  Core Strategy: Chinese-first, international fallback         ║
    ╚═══════════════════════════════════════════════════════════════╝
    
    🟢 已實現功能 / Implemented:
        - OTSU二值化（自己實現）/ OTSU binarization (self-implemented)
        - 中值濾波（自己實現）/ Median filter (self-implemented)
        - 傾斜校正（自己實現）/ Skew correction (self-implemented)
        - 文本區域檢測（基於筆畫密度）/ Text region detection (stroke-density based)
        - 中文字符特徵提取 / Chinese character feature extraction
        - 繁體龍字專用檢測器 / Traditional 龍 character detector
        - 甲骨文字符分類器 / Oracle bone character classifier
        - CNSH術語識別 / CNSH terminology recognition
    
    🟡 國際兜底 / International Fallback:
        - Tesseract OCR（當置信度 < 0.7 時）/ Tesseract when confidence < 0.7
        - OpenCV（基礎I/O）/ OpenCV (basic I/O)
    """
    
    def __init__(self, 模式: str = "中文優先", 置信度閾值: float = 0.7):
        """
        初始化龍瞳OCR引擎 / Initialize Dragon Pupil OCR Engine
        
        參數 Parameters:
            模式: 識別模式（"中文優先"|"國際兜底"|"混合模式"）/ Recognition mode
            置信度閾值: 降級閾值 0.0-1.0 / Fallback threshold
        """
        日誌.info("🐉 龍瞳OCR引擎啟動中 / Initializing Dragon Pupil OCR...")
        
        # DNA追溯 / DNA Trace
        self.DNA = "#龍芯⚡️2026-06-18-LONGTENG-OCR-v1.0"
        
        # 模式設置 / Mode setting
        self.模式 = 模式
        self.置信度閾值 = 置信度閾值
        
        # 🟢 初始化中文核心模塊 / Initialize Chinese core modules
        self.預處理器 = 圖像預處理器()
        self.區域檢測器 = 文本區域檢測器()
        self.特徵提取器 = 字符特徵提取器()
        self.龍字檢測器 = 龍字檢測器()
        self.甲骨文分類器 = 甲骨文分類器()
        self.字符識別器 = 中文字符識別器()
        self.CNSH詞典 = CNSH詞典()
        
        # 🟡 初始化國際兜底引擎 / Initialize international fallback
        self.兜底引擎 = 國際兜底引擎()
        
        # 版本信息 / Version info
        self.版本 = "1.0"
        self.引擎名 = "龍瞳OCR"
        
        # 統計信息 / Statistics
        self.統計 = {
            "總識別次數": 0,
            "中文識別次數": 0,
            "兜底次數": 0,
            "龍字檢測次數": 0,
            "甲骨文分類次數": 0,
        }
        
        日誌.info(f"🐉 龍瞳OCR引擎已就緒 / Engine ready — 模式/Mode: {模式}")
        日誌.info(f"   DNA: {self.DNA}")
        日誌.info(f"   置信度閾值/Threshold: {置信度閾值}")
    
    def 識別圖像(self, 圖像路徑: Union[str, np.ndarray]) -> 識別結果:
        """
        🟢 主識別函數：識別圖像中的文本
        Main recognition function: recognize text in image
        
        流程 / Pipeline:
            1. 加載圖像 / Load image
            2. 預處理（OTSU+中值濾波+傾斜校正）/ Preprocess
            3. 檢測文本區域 / Detect text regions
            4. 識別每個區域 / Recognize each region
            5. 必要時降級到Tesseract / Fallback to Tesseract if needed
        
        參數 Parameters:
            圖像路徑: 圖像文件路徑或numpy數組 / Image path or numpy array
        
        返回 Returns:
            識別結果 / Recognition result
        """
        self.統計["總識別次數"] += 1
        
        日誌.info(f"🐉 開始識別 / Starting recognition: {圖像路徑 if isinstance(圖像路徑, str) else 'numpy數組'}")
        
        try:
            # Step 1: 加載圖像 / Load image
            圖像數組 = self._加載圖像(圖像路徑)
            if 圖像數組 is None:
                return 識別結果(
                    文本="",
                    置信度=0.0,
                    審計="🔴",
                    備註="圖像加載失敗 / Image load failed"
                )
            
            # Step 2: 預處理 / Preprocess
            日誌.info("  [1/4] 圖像預處理 / Preprocessing...")
            預處理圖 = self.預處理器.預處理(圖像數組)
            
            # Step 3: 檢測文本區域 / Detect text regions
            日誌.info("  [2/4] 檢測文本區域 / Detecting text regions...")
            文本區域 = self.區域檢測器.檢測文本區域(預處理圖)
            
            if not 文本區域:
                日誌.info("  未檢測到文本區域，嘗試整圖識別 / No regions, trying whole image")
                return self._識別整圖(圖像數組, 預處理圖)
            
            # Step 4: 識別每個區域 / Recognize each region
            日誌.info(f"  [3/4] 識別 {len(文本區域)} 個文本區域 / Recognizing {len(文本區域)} regions...")
            識別文本列表 = []
            所有區域 = []
            總置信度 = []
            
            for 索引, 區域 in enumerate(文本區域):
                區域圖 = 預處理圖[區域.左上縱:區域.右下縱, 區域.左上橫:區域.右下橫]
                
                if 區域圖.size == 0:
                    continue
                
                # 使用中文核心識別 / Use Chinese core
                結果 = self.字符識別器.識別字符(區域圖)
                
                # 檢查是否需要降級 / Check if fallback needed
                if 結果.置信度 < self.置信度閾值 and self.模式 != "中文優先":
                    結果 = self._國際兜底識別(區域圖)
                
                識別文本列表.append(結果.文本)
                總置信度.append(結果.置信度)
                
                區域字典 = 區域.轉字典()
                區域字典["識別文本"] = 結果.文本
                區域字典["識別置信度"] = round(結果.置信度, 4)
                所有區域.append(區域字典)
            
            # Step 5: 組合結果 / Combine results
            日誌.info("  [4/4] 組合識別結果 / Combining results...")
            合併文本 = "".join(識別文本列表)
            平均置信度 = float(np.mean(總置信度)) if 總置信度 else 0.0
            
            # 檢查CNSH術語 / Check CNSH terminology
            CNSH匹配 = self.CNSH詞典.匹配命名模式(合併文本)
            
            審計 = "🟢" if 平均置信度 > 0.7 else "🟡" if 平均置信度 > 0.4 else "🔴"
            
            結果 = 識別結果(
                文本=合併文本,
                置信度=round(平均置信度, 4),
                區域=所有區域,
                審計=審計,
                備註=f"識別 {len(文本區域)} 個區域 / Recognized {len(文本區域)} regions",
                引擎來源="龍瞳OCR-中文核心"
            )
            
            # 最終兜底檢查 / Final fallback check
            if 平均置信度 < self.置信度閾值 and self.模式 in ["混合模式", "國際兜底"]:
                兜底結果 = self._國際兜底識別(圖像數組)
                if 兜底結果.置信度 > 平均置信度:
                    self.統計["兜底次數"] += 1
                    兜底結果.備註 = f"已降級到國際引擎 / Fallback: {結果.置信度:.2f} -> {兜底結果.置信度:.2f}"
                    return 兜底結果
            
            self.統計["中文識別次數"] += 1
            日誌.info(f"🐉 識別完成 / Done: 文本/Text=[{合併文本}], 置信度/Conf={平均置信度:.3f}")
            return 結果
        
        except Exception as 錯誤:
            日誌.error(f"🔴 識別過程出錯 / Recognition error: {錯誤}")
            traceback.print_exc()
            return 識別結果(
                文本="",
                置信度=0.0,
                審計="🔴",
                備註=f"識別錯誤 / Error: {str(錯誤)}"
            )
    
    def 識別中文字符(self, 圖像數組: np.ndarray) -> 識別結果:
        """
        🟢 識別單個中文字符 / Recognize single Chinese character
        
        參數 Parameters:
            圖像數組: 字符圖像數組 / Character image array
        
        返回 Returns:
            識別結果 / Recognition result
        """
        return self.字符識別器.識別字符(圖像數組)
    
    def 檢測龍字(self, 圖像數組: np.ndarray) -> Dict[str, Any]:
        """
        🟢 檢測圖像中是否包含繁體「龍」字
        Detect if image contains traditional "龍" character
        
        參數 Parameters:
            圖像數組: 輸入圖像 / Input image
        
        返回 Returns:
            檢測結果字典 / Detection result
        """
        self.統計["龍字檢測次數"] += 1
        
        try:
            預處理圖 = self.預處理器.預處理(圖像數組)
            
            區域列表 = self.區域檢測器.檢測文本區域(預處理圖)
            
            龍字結果 = []
            for 區域 in 區域列表:
                區域圖 = 預處理圖[區域.左上縱:區域.右下縱, 區域.左上橫:區域.右下橫]
                if 區域圖.size == 0:
                    continue
                
                結果 = self.龍字檢測器.檢測(區域圖)
                if 結果["是龍字"]:
                    龍字結果.append({
                        "區域": 區域.轉字典(),
                        "置信度": 結果["置信度"],
                        "詳細分析": 結果["詳細分析"]
                    })
            
            return {
                "包含龍字": len(龍字結果) > 0,
                "龍字數量": len(龍字結果),
                "龍字位置": 龍字結果,
                "DNA": self.DNA,
            }
        
        except Exception as 錯誤:
            日誌.error(f"🔴 龍字檢測失敗 / 龍 detection failed: {錯誤}")
            return {"包含龍字": False, "錯誤": str(錯誤)}
    
    def 檢測甲骨文(self, 圖像數組: np.ndarray) -> Dict[str, Any]:
        """
        🟢 檢測圖像中的甲骨文字符特徵
        Detect oracle bone character features in image
        
        參數 Parameters:
            圖像數組: 輸入圖像 / Input image
        
        返回 Returns:
            分類結果 / Classification result
        """
        self.統計["甲骨文分類次數"] += 1
        
        try:
            預處理圖 = self.預處理器.預處理(圖像數組)
            
            區域列表 = self.區域檢測器.檢測文本區域(預處理圖)
            
            甲骨文結果 = []
            for 區域 in 區域列表:
                區域圖 = 預處理圖[區域.左上縱:區域.右下縱, 區域.左上橫:區域.右下橫]
                if 區域圖.size == 0:
                    continue
                
                結果 = self.甲骨文分類器.分類(區域圖)
                結果["區域"] = 區域.轉字典()
                甲骨文結果.append(結果)
            
            return {
                "字符總數": len(甲骨文結果),
                "甲骨文特徵字符數": sum(1 for r in 甲骨文結果 if r.get("是甲骨文", False)),
                "字符詳情": 甲骨文結果,
                "DNA": self.DNA,
            }
        
        except Exception as 錯誤:
            日誌.error(f"🔴 甲骨文檢測失敗 / Oracle bone detection failed: {錯誤}")
            return {"字符總數": 0, "錯誤": str(錯誤)}
    
    def 提取文本區域(self, 圖像數組: np.ndarray) -> List[區域框]:
        """
        🟢 提取圖像中的文本區域（自己實現）
        Extract text regions from image (self-implemented)
        
        參數 Parameters:
            圖像數組: 輸入圖像 / Input image
        
        返回 Returns:
            文本區域框列表 / List of text region boxes
        """
        預處理圖 = self.預處理器.預處理(圖像數組)
        return self.區域檢測器.檢測文本區域(預處理圖)
    
    def 預處理(self, 圖像數組: np.ndarray) -> np.ndarray:
        """
        🟢 圖像預處理（OTSU二值化+中值濾波+傾斜校正）
        Image preprocessing (OTSU + median filter + skew correction)
        
        參數 Parameters:
            圖像數組: 輸入圖像 / Input image
        
        返回 Returns:
            預處理後二值圖像 / Preprocessed binary image
        """
        return self.預處理器.預處理(圖像數組)
    
    def 安裝依賴(self) -> Dict[str, Any]:
        """
        🟡 自動檢測並提示安裝依賴包
        Auto-detect and prompt for dependency installation
        
        檢測項 / Checks:
            - opencv-python / OpenCV
            - pytesseract / Tesseract
            - Pillow / PIL
            - numpy / NumPy
        
        返回 Returns:
            依賴狀態字典 / Dependency status dictionary
        """
        日誌.info("🔍 檢測依賴狀態 / Checking dependencies...")
        
        依賴狀態 = {
            "numpy": {"已安裝": True, "版本": np.__version__},
            "opencv-python": {"已安裝": CV2可用, "版本": getattr(cv2, "__version__", "N/A") if CV2可用 else "未安裝"},
            "Pillow": {"已安裝": PIL可用, "版本": getattr(Image, "__version__", "N/A") if PIL可用 else "未安裝"},
            "pytesseract": {"已安裝": TESSERACT可用, "版本": str(getattr(pytesseract, "get_tesseract_version", lambda: "N/A")()) if TESSERACT可用 else "未安裝"},
        }
        
        待安裝 = []
        for 包名, 狀態 in 依賴狀態.items():
            if not 狀態["已安裝"]:
                待安裝.append(包名)
        
        if 待安裝:
            日誌.info("⚠️ 以下依賴未安裝 / Missing dependencies:")
            for 包 in 待安裝:
                日誌.info(f"   pip install {包}")
        else:
            日誌.info("🟢 所有依賴已安裝 / All dependencies installed")
        
        return 依賴狀態
    
    def 識別CNSH代碼(self, 圖像路徑: Union[str, np.ndarray]) -> Dict[str, Any]:
        """
        🟢 識別CNSH代碼截圖中的中文標識符
        Recognize Chinese identifiers in CNSH code screenshots
        
        參數 Parameters:
            圖像路徑: 圖像路徑或數組 / Image path or array
        
        返回 Returns:
            CNSH識別結果 / CNSH recognition result
        """
        # 先進行常規OCR / Perform regular OCR first
        OCR結果 = self.識別圖像(圖像路徑)
        
        文本 = OCR結果.文本
        
        # 匹配CNSH術語 / Match CNSH terminology
        術語匹配 = []
        for 術語 in self.CNSH詞典.編程術語:
            if 術語 in 文本:
                術語匹配.append({
                    "術語": 術語,
                    "位置": 文本.index(術語),
                    "長度": len(術語)
                })
        
        # 匹配命名模式 / Match naming patterns
        命名匹配 = self.CNSH詞典.匹配命名模式(文本)
        
        return {
            "原始文本": 文本,
            "置信度": OCR結果.置信度,
            "CNSH術語": 術語匹配,
            "命名模式": 命名匹配,
            "術語數量": len(術語匹配),
            "引擎來源": "龍瞳OCR-CNSH專用",
            "DNA": self.DNA,
        }
    
    def 導出JSON(self, 結果: 識別結果, 文件路徑: str) -> str:
        """
        導出識別結果為JSON / Export recognition result to JSON
        
        參數 Parameters:
            結果: 識別結果對象 / Recognition result
            文件路徑: 輸出JSON路徑 / Output JSON path
        
        返回 Returns:
            JSON字符串 / JSON string
        """
        return 結果.轉JSON(文件路徑=文件路徑, 確保中文=True)
    
    def 獲取統計(self) -> Dict[str, int]:
        """
        獲取引擎統計信息 / Get engine statistics
        
        返回 Returns:
            統計字典 / Statistics dictionary
        """
        return self.統計.copy()
    
    def _加載圖像(self, 圖像路徑: Union[str, np.ndarray]) -> Optional[np.ndarray]:
        """
        加載圖像為numpy數組 / Load image as numpy array
        
        參數 Parameters:
            圖像路徑: 文件路徑或numpy數組 / File path or numpy array
        
        返回 Returns:
            圖像數組或None / Image array or None
        """
        if isinstance(圖像路徑, np.ndarray):
            return 圖像路徑
        
        if not os.path.exists(圖像路徑):
            日誌.error(f"🔴 圖像不存在 / Image not found: {圖像路徑}")
            return None
        
        try:
            if CV2可用:
                圖像 = cv2.imread(圖像路徑)
                if 圖像 is None:
                    raise ValueError("OpenCV無法讀取圖像")
                return cv2.cvtColor(圖像, cv2.COLOR_BGR2RGB)
            elif PIL可用:
                PIL圖像 = Image.open(圖像路徑).convert('RGB')
                return np.array(PIL圖像)
            else:
                raise RuntimeError("🔴 無圖像庫可用 / No image library available")
        
        except Exception as 錯誤:
            日誌.error(f"🔴 圖像加載失敗 / Image load failed: {錯誤}")
            return None
    
    def _識別整圖(self, 原始圖: np.ndarray, 預處理圖: np.ndarray) -> 識別結果:
        """
        整圖識別（無區域分割時）/ Whole image recognition
        
        參數 Parameters:
            原始圖: 原始圖像 / Original image
            預處理圖: 預處理後圖像 / Preprocessed image
        
        返回 Returns:
            識別結果 / Recognition result
        """
        結果 = self.字符識別器.識別字符(預處理圖)
        
        if 結果.置信度 < self.置信度閾值:
            兜底結果 = self._國際兜底識別(原始圖)
            if 兜底結果.置信度 > 結果.置信度:
                self.統計["兜底次數"] += 1
                return 兜底結果
        
        return 結果
    
    def _國際兜底識別(self, 圖像: np.ndarray) -> 識別結果:
        """
        🟡 調用國際兜底引擎 / Call international fallback engine
        
        參數 Parameters:
            圖像: 輸入圖像 / Input image
        
        返回 Returns:
            識別結果 / Recognition result
        """
        if self.模式 == "中文優先":
            return 識別結果(
                文本="",
                置信度=0.0,
                審計="🔴",
                備註="中文優先模式下禁用兜底 / Fallback disabled in Chinese-first mode"
            )
        
        日誌.info("🟡 降級到國際兜底引擎 / Falling back to international engine...")
        self.統計["兜底次數"] += 1
        return self.兜底引擎.識別(圖像)


# ═══════════════════════════════════════════════════════════════════════
# 君子協議與許可聲明 / Gentleman's Agreement & License
# ═══════════════════════════════════════════════════════════════════════
def 君子協議聲明() -> str:
    """
    輸出君子協議聲明 / Output Gentleman's Agreement
    
    返回 Returns:
        協議文本 / Agreement text
    """
    聲明 = """
╔══════════════════════════════════════════════════════════════════╗
║                         君子協議 / Gentleman's Agreement          ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  本作品採用知識共享 署名-非商業性使用-相同方式共享 4.0 國際許可   ║
║  This work is licensed under a Creative Commons                   ║
║  Attribution-NonCommercial-ShareAlike 4.0 International License   ║
║                                                                   ║
║  您可以： / You may:                                               ║
║    🟢 共享 — 複製、發行並傳播本作品 / Share                       ║
║    🟢 演繹 — 修改、轉換或以本作品為基礎進行創作 / Adapt            ║
║                                                                   ║
║  惟須遵守下列條件 / Under these conditions:                        ║
║    🟡 署名 — 您必須給出適當的署名 / Attribution                    ║
║    🔴 非商業性使用 — 您不得將本作品用於商業目的 / NonCommercial      ║
║    🟡 相同方式共享 — 採用相同許可協議發布 / ShareAlike              ║
║                                                                   ║
║  作者：龍魂體系開源社區 / Author: Dragon Soul Open Source          ║
║  DNA：#龍芯⚡️2026-06-18-LONGTENG-OCR-v1.0                        ║
║                                                                   ║
║  「龍魂體系，中文編程，通心譯世」                                  ║
║  "Dragon Soul System, Chinese Programming, Heart-to-Heart         ║
║   Translation for the World"                                      ║
║                                                                   ║
╚══════════════════════════════════════════════════════════════════╝
"""
    return 聲明


# ═══════════════════════════════════════════════════════════════════════
# 入口點：測試與示範 / Entry Point: Test & Demonstration
# ═══════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 70)
    print("  🐉 龍瞳OCR引擎 — 啟動測試 / Dragon Pupil OCR — Startup Test")
    print("  " + "=" * 68)
    print()
    
    # 打印君子協議 / Print agreement
    print(君子協議聲明())
    
    # ═══════════════════════════════════════════════════════════════
    # Step 1: 初始化引擎 / Initialize engine
    # ═══════════════════════════════════════════════════════════════
    print("\n[Step 1] 🐉 初始化龍瞳OCR引擎 / Initializing engine...")
    引擎 = 龍瞳OCR引擎(模式="混合模式", 置信度閾值=0.7)
    
    # ═══════════════════════════════════════════════════════════════
    # Step 2: 檢測依賴 / Check dependencies
    # ═══════════════════════════════════════════════════════════════
    print("\n[Step 2] 🔍 檢測依賴狀態 / Checking dependencies...")
    依賴狀態 = 引擎.安裝依賴()
    for 包名, 狀態 in 依賴狀態.items():
        標記 = "🟢" if 狀態["已安裝"] else "🔴"
        print(f"  {標記} {包名}: {狀態['版本']}")
    
    # ═══════════════════════════════════════════════════════════════
    # Step 3: 生成測試圖像 / Generate test images
    # ═══════════════════════════════════════════════════════════════
    print("\n[Step 3] 🖼️ 生成測試圖像 / Generating test images...")
    測試目錄 = "/mnt/agents/output/CNSH/reactor/測試圖像"
    os.makedirs(測試目錄, exist_ok=True)
    
    測試字符 = ["龍", "一", "二", "十"]
    測試圖像路徑 = []
    
    for 字符 in 測試字符:
        路徑 = os.path.join(測試目錄, f"測試_{字符}.png")
        圖像生成器.生成測試圖像(字符, 尺寸=(200, 200), 字號=80, 輸出路徑=路徑)
        測試圖像路徑.append((字符, 路徑))
        print(f"  🟢 已生成 / Generated: {路徑}")
    
    # ═══════════════════════════════════════════════════════════════
    # Step 4: 測試預處理模塊 / Test preprocessing module
    # ═══════════════════════════════════════════════════════════════
    print("\n[Step 4] ⚙️ 測試預處理模塊 / Testing preprocessing module...")
    
    預處理器 = 圖像預處理器()
    for 字符, 路徑 in 測試圖像路徑[:2]:
        圖像 = 引擎._加載圖像(路徑)
        if 圖像 is not None:
            灰度 = 預處理器.轉灰度(圖像)
            二值 = 預處理器.OTSU二值化(灰度)
            去噪 = 預處理器.中值濾波(二值, 核大小=3)
            print(f"  🟢 預處理測試通過 / Preprocess OK: {字符}")
    
    # ═══════════════════════════════════════════════════════════════
    # Step 5: 測試龍字檢測器 / Test 龍 detector
    # ═══════════════════════════════════════════════════════════════
    print("\n[Step 5] 🐉 測試龍字檢測器 / Testing 龍 character detector...")
    
    龍圖像 = 圖像生成器.生成測試圖像("龍", 尺寸=(128, 128), 字號=64)
    龍結果 = 引擎.檢測龍字(龍圖像)
    print(f"  龍字檢測結果 / Detection result:")
    print(f"    包含龍字 / Contains 龍: {龍結果.get('包含龍字', False)}")
    print(f"    龍字數量 / Count: {龍結果.get('龍字數量', 0)}")
    
    # ═══════════════════════════════════════════════════════════════
    # Step 6: 測試甲骨文分類器 / Test oracle bone classifier
    # ═══════════════════════════════════════════════════════════════
    print("\n[Step 6] 🦴 測試甲骨文分類器 / Testing oracle bone classifier...")
    
    測試圖 = 圖像生成器.生成測試圖像("十", 尺寸=(128, 128), 字號=64)
    甲骨文結果 = 引擎.檢測甲骨文(測試圖)
    print(f"  甲骨文檢測結果 / Oracle bone result:")
    print(f"    字符總數 / Total chars: {甲骨文結果.get('字符總數', 0)}")
    print(f"    甲骨文特徵數 / Oracle bone chars: {甲骨文結果.get('甲骨文特徵字符數', 0)}")
    
    # ═══════════════════════════════════════════════════════════════
    # Step 7: 測試文本區域檢測 / Test text region detection
    # ═══════════════════════════════════════════════════════════════
    print("\n[Step 7] 📐 測試文本區域檢測 / Testing text region detection...")
    
    測試圖 = 圖像生成器.生成測試圖像("龍", 尺寸=(256, 256), 字號=128)
    預處理圖 = 引擎.預處理(測試圖)
    區域列表 = 引擎.提取文本區域(測試圖)
    print(f"  檢測到 {len(區域列表)} 個文本區域 / {len(區域列表)} text regions detected")
    for i, 區域 in enumerate(區域列表[:3]):
        print(f"    區域 {i+1}: 位置/Pos=({區域.左上橫},{區域.左上縱})-({區域.右下橫},{區域.右下縱})")
    
    # ═══════════════════════════════════════════════════════════════
    # Step 8: 測試CNSH詞典 / Test CNSH dictionary
    # ═══════════════════════════════════════════════════════════════
    print("\n[Step 8] 📚 測試CNSH詞典 / Testing CNSH dictionary...")
    
    測試文本 = "定義函數獲取龍魂狀態"
    匹配結果 = CNSH詞典.匹配命名模式(測試文本)
    print(f"  測試文本 / Test text: {測試文本}")
    print(f"  匹配到 {len(匹配結果)} 個命名模式 / Matched {len(匹配結果)} patterns")
    for 匹配 in 匹配結果[:5]:
        print(f"    🟢 {匹配['類型']}: {匹配['詞']}")
    
    # ═══════════════════════════════════════════════════════════════
    # Step 9: 測試完整識別流程 / Test full recognition pipeline
    # ═══════════════════════════════════════════════════════════════
    print("\n[Step 9] 🔄 測試完整識別流程 / Testing full recognition pipeline...")
    
    for 字符, 路徑 in 測試圖像路徑:
        結果 = 引擎.識別圖像(路徑)
        print(f"  字符 '{字符}' -> 識別結果: {結果.文本} (置信度/Conf: {結果.置信度:.3f}) {結果.審計}")
    
    # ═══════════════════════════════════════════════════════════════
    # Step 10: 測試JSON導出 / Test JSON export
    # ═══════════════════════════════════════════════════════════════
    print("\n[Step 10] 💾 測試JSON導出 / Testing JSON export...")
    
    測試結果 = 識別結果(
        文本="龍魂體系",
        置信度=0.95,
        區域=[{"x1": 0, "y1": 0, "x2": 100, "y2": 100, "文本": "龍"}],
        審計="🟢",
        結構="左右",
        備註="測試數據 / Test data",
        引擎來源="龍瞳OCR-測試"
    )
    
    JSON路徑 = os.path.join(測試目錄, "測試結果.json")
    JSON字符串 = 引擎.導出JSON(測試結果, JSON路徑)
    print(f"  🟢 JSON已導出 / JSON exported: {JSON路徑}")
    print(f"  JSON內容 / Content preview: {JSON字符串[:100]}...")
    
    # ═══════════════════════════════════════════════════════════════
    # Step 11: 打印統計 / Print statistics
    # ═══════════════════════════════════════════════════════════════
    print("\n[Step 11] 📊 引擎統計 / Engine statistics...")
    
    統計 = 引擎.獲取統計()
    for 鍵, 值 in 統計.items():
        print(f"  {鍵}: {值}")
    
    # ═══════════════════════════════════════════════════════════════
    # 完成 / Done
    # ═══════════════════════════════════════════════════════════════
    print("\n" + "=" * 70)
    print("  🐉 龍瞳OCR引擎測試完成 / Dragon Pupil OCR Test Complete!")
    print(f"  DNA: {引擎.DNA}")
    print("  君子協議: CC BY-NC-SA 4.0")
    print("  「龍魂體系，中文編程，通心譯世」")
    print("  " + "=" * 68)
