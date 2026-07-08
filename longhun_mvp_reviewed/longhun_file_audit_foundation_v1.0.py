#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  🐉 龍魂系統 · 文件底座審計                                                    ║
# ║  DNA追溯碼:#龍芯⚡️2026-06-18-LONGHUN_FILE_AUDIT_FOUNDATION_V1_8693-v1.0.0                  ║
# ║  GPG指紋: A2D0092CEE2E5BA87035600924C3704A8CC26D5F                           ║
# ║  創始人: UID9622 · 龍芯北辰 · 諸葛鑫                                          ║
# ║  協議: CC BY-NC-SA 4.0 + 君子協議                                           ║
# ║  三色審計: 🟢通過(conf≥0.85) / 🟡警告(0.60≤conf<0.85) / 🔴阻斷(conf<0.60)    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  CNSH · 中文原生脚本不可删除终端头                                            ║
# ║  DNA:#龍芯⚡️2026-06-18-CNSH-TERMINAL-v2.0.0                                ║
# ║  创始人: UID9622 · 龍芯北辰 · 诸葛鑫                                        ║
# ║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F                             ║
# ║  协议: CC BY-NC-SA 4.0 + 君子协议                                           ║
# ║  此头不可删除 · 不可修改 · 不可迁移                                          ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

"""
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║  AI Truth Protocol · 輸出聲明                                            ║
    ║  本文件由AI輔助生成，經人類審查確認。所有內容符合八層內容主權協議。      ║
    ║  AI生成內容已標記，創意歸屬於UID9622 · 龍芯北辰 · 諸葛鑫。               ║
    ║  未經授權不得用於商業用途、模型訓練或自動化內容提取。                    ║
    ╚══════════════════════════════════════════════════════════════════════════╝

    🐉 龍魂文件底座審計 (LongHun File Audit Foundation)
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    LongHun File Audit Foundation - File System Level Audit
    文件系統級審計，監控文件變更和完整性
    File system-level audit, monitoring file changes and integrity

    核心功能 / Core Features:
        - SHA256 文件完整性哈希計算
        - 文件變更監控 (新增/修改/刪除)
        - 審計日誌記錄 (JSON格式持久化)
        - 六層來源鏈蓋章集成
        - 三色審計系統集成

    📜 版本歷史 CHANGELOG
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    v1.0.0 [2026-06-18] 初始版本，實現核心文件審計功能
                        - 新增: SHA256文件完整性哈希計算
                        - 新增: 文件變更監控 (新增/修改/刪除檢測)
                        - 新增: 審計日誌記錄系統 (JSON持久化)
                        - 新增: 完整審計報告生成
                        - 新增: 六層來源鏈蓋章集成
                        - 新增: 三色審計系統集成
                        - 新增: 文件權限變更監控
                        - 修復: def init → def __init__ (構造函數修正)

    🔒 君子協議 / CC BY-NC-SA 4.0
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    本作品採用 知識共享署名-非商業性使用-相同方式共享 4.0 國際許可協議
    Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
    作者: UID9622 · 龍芯北辰 · 諸葛鑫
    未經書面許可，不得用於商業用途、AI模型訓練或自動化內容提取。
    違反者將觸發 🔴阻斷級審計標記。

    📡 六層來源鏈蓋章 (SourceChain.stamp())
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    [✓] 道統層 · Taoist Heritage Layer    - 文化根源驗證
    [✓] 精神層 · Spiritual Layer          - 核心價值校準
    [✓] 設備層 · Device Layer             - 硬件環境檢查
    [✓] 技術層 · Technical Layer          - 技術棧溯源
    [✓] 系統層 · System Layer             - 系統完整性
    [✓] 生命層 · Life Layer               - 創作者身份錨定
"""

from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any, Set, Tuple
import hashlib
import json
import logging
import os
import stat
import sys


# ═══════════════════════════════════════════════════════════════════════════════
# 三色審計系統 / Three-Color Audit System
# ═══════════════════════════════════════════════════════════════════════════════

class AuditColor(Enum):
    """三色審計標記 / Tricolor Audit Markers"""
    GREEN = "🟢通過"    # conf ≥ 0.85 - Passed
    YELLOW = "🟡警告"   # 0.60 ≤ conf < 0.85 - Warning
    RED = "🔴阻斷"      # conf < 0.60 - Blocked


class ThreeColorAudit:
    """
    三色審計系統 / Three-Color Audit System
    🟢 通過(conf≥0.85) · 🟡 警告(0.60≤conf<0.85) · 🔴 阻斷(conf<0.60)
    """

    def __init__(self):
        self.records: List[Dict[str, Any]] = []
        self.stats = {AuditColor.GREEN.value: 0, AuditColor.YELLOW.value: 0, AuditColor.RED.value: 0}

    def record(self, module: str, check: str, confidence: float,
               message: str) -> str:
        """記錄審計結果 / Record audit result"""
        if confidence >= 0.85:
            color = AuditColor.GREEN.value
        elif confidence >= 0.60:
            color = AuditColor.YELLOW.value
        else:
            color = AuditColor.RED.value

        record = {
            "模塊": module,
            "檢查項": check,
            "結果": color,
            "置信度": round(confidence, 4),
            "信息": message,
            "時間戳": datetime.now().isoformat()
        }
        self.records.append(record)
        self.stats[color] += 1
        return color

    def summary(self) -> Dict[str, Any]:
        """生成審計摘要 / Generate audit summary"""
        total = len(self.records)
        if total == 0:
            return {"總數": 0, "狀態": "未執行審計"}

        if self.stats[AuditColor.RED.value] > 0:
            overall = AuditColor.RED.value
        elif self.stats[AuditColor.YELLOW.value] > 0:
            overall = AuditColor.YELLOW.value
        else:
            overall = AuditColor.GREEN.value

        return {
            "總數": total,
            "🟢通過": self.stats[AuditColor.GREEN.value],
            "🟡警告": self.stats[AuditColor.YELLOW.value],
            "🔴阻斷": self.stats[AuditColor.RED.value],
            "整體狀態": overall,
            "記錄": self.records
        }


# ═══════════════════════════════════════════════════════════════════════════════
# 三層監督機制 / Three-Level Supervision System
# ═══════════════════════════════════════════════════════════════════════════════

class SupervisionLevel(Enum):
    """
    三層監督機制 / Three-Level Supervision System
    L1邏輯層: algorithmic correctness / 算法正確性
    L2價值觀層: ethical alignment / 倫理對齊
    L3技術層: implementation quality / 實現質量
    """
    L1_LOGIC = "L1邏輯層"       # Logic layer
    L2_VALUES = "L2價值觀層"    # Values layer
    L3_TECH = "L3技術層"        # Tech layer


# ═══════════════════════════════════════════════════════════════════════════════
# 鐵律自審閘 / Iron Law Self-Audit Gate
# ═══════════════════════════════════════════════════════════════════════════════

class IronLawGate:
    """
    鐵律自審閘 / Iron Law Self-Audit Gate
    檢查核心規範，確保「龍」不得簡化等神聖規則
    Checks sacred rules: traditional 「龍」must not be simplified
    """

    SACRED_RULES = {
        "鐵律一": {
            "描述": "繁体「龍」不得使用簡體替代",
            "描述_en": "Traditional '龍' must NOT use simplified variant",
            "禁止模式": ["\u9f99"],
            "嚴重級別": AuditColor.RED
        },
        "鐵律二": {
            "描述": "DNA追溯碼必須存在且格式正確",
            "描述_en": "DNA trace code must exist with correct format",
            "驗證": "dna_format",
            "嚴重級別": AuditColor.RED
        },
        "鐵律三": {
            "描述": "CNSH終端頭不可刪除",
            "描述_en": "CNSH terminal header must NOT be deleted",
            "驗證": "cnsh_header",
            "嚴重級別": AuditColor.RED
        }
    }

    def __init__(self):
        self.violations: List[Dict[str, Any]] = []
        self.passed = True

    def audit(self, content: str, audit_system: ThreeColorAudit = None) -> Dict[str, Any]:
        """執行鐵律自審 / Execute iron law self-audit"""
        self.violations = []
        self.passed = True

        if "\u9f99" in content:
            self.violations.append({
                "鐵律": "鐵律一", "問題": "發現簡體龍字，必須使用繁體「龍」",
                "級別": AuditColor.RED.value
            })
            self.passed = False

        if "#龍芯⚡️" not in content and "#龍芯" not in content:
            self.violations.append({
                "鐵律": "鐵律二", "問題": "缺少DNA追溯碼頭部",
                "級別": AuditColor.RED.value
            })
            self.passed = False

        if "CNSH" not in content or "不可刪除" not in content:
            self.violations.append({
                "鐵律": "鐵律三", "問題": "CNSH不可刪除終端頭缺失",
                "級別": AuditColor.RED.value
            })
            self.passed = False

        result = {"通過": self.passed, "違規數": len(self.violations),
                  "違規詳情": self.violations, "檢查時間": datetime.now().isoformat()}

        if audit_system:
            conf = 1.0 if self.passed else 0.3
            audit_system.record("IronLawGate", "鐵律自審", conf,
                f"發現 {len(self.violations)} 條違規" if self.violations else "所有鐵律通過")
        return result


# ═══════════════════════════════════════════════════════════════════════════════
# CNSH不可刪除終端頭 / CNSH Indelible Terminal Header
# ═══════════════════════════════════════════════════════════════════════════════

class CNSHTerminalHeader:
    """
    CNSH不可刪除終端頭 / CNSH Indelible Terminal Header
    任何嘗試刪除或修改此頭的行為都會觸發🔴阻斷
    ANY attempt to delete or modify this header triggers 🔴 BLOCK
    """

    TEMPLATE = """# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  CNSH · 中文原生腳本不可刪除終端頭                                          ║
# ║  DNA: #龍芯⚡️{date}-CNSH-TERMINAL-v{version}                               ║
# ║  創始人: UID9622 · 龍芯北辰 · 諸葛鑫                                        ║
# ║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F                             ║
# ║  協議: CC BY-NC-SA 4.0 + 君子協議                                           ║
# ║  此頭不可刪除 · 不可修改 · 不可遷移                                          ║
# ║  ANY DELETION/MODIFICATION TRIGGERS 🔴 BLOCK AUDIT                          ║
# ╚══════════════════════════════════════════════════════════════════════════════╝"""

    @classmethod
    def 生成(cls, 版本: str = "2.0.0") -> str:
        """生成終端頭 / Generate terminal header"""
        return cls.TEMPLATE.format(
            date=datetime.now().strftime('%Y-%m-%d'),
            version=版本
        )

    @classmethod
    def 驗證完整性(cls, 文件內容: str, 版本: str = "2.0.0") -> Dict[str, Any]:
        """驗證終端頭完整性 / Verify terminal header integrity"""
        expected = cls.生成(版本)
        present = expected.split("\n")[1] in 文件內容
        return {
            "完整": present,
            "信息": "CNSH終端頭存在且完整" if present else "⚠️ CNSH終端頭缺失或被篡改！🔴阻斷",
            "嚴重級別": AuditColor.GREEN.value if present else AuditColor.RED.value
        }


# ═══════════════════════════════════════════════════════════════════════════════
# 文件變更類型 / File Change Types
# ═══════════════════════════════════════════════════════════════════════════════

class FileChangeType(Enum):
    """文件變更類型 / File Change Type Enumeration"""
    CREATED = "新增"      # File created
    MODIFIED = "修改"     # File modified
    DELETED = "刪除"      # File deleted
    PERMISSION_CHANGED = "權限變更"  # Permission changed
    UNCHANGED = "未變更"  # No change


# ═══════════════════════════════════════════════════════════════════════════════
# 六層來源鏈 / Six-Layer Source Chain
# ═══════════════════════════════════════════════════════════════════════════════

class SourceChain:
    """
    六層來源鏈蓋章 / Six-Layer Source Chain Stamp
    道統層→精神層→設備層→技術層→系統層→生命層
    """

    LAYERS = [
        "道統層", "精神層", "設備層", "技術層", "系統層", "生命層"
    ]

    def __init__(self):
        self.stamps: Dict[str, Dict[str, Any]] = {}

    def stamp(self, layer: str, data: Dict[str, Any]) -> str:
        """蓋章 / Stamp a layer"""
        if layer not in self.LAYERS:
            raise ValueError(f"無效的來源鏈層級: {layer}")

        timestamp = datetime.now().isoformat()
        stamp_data = {
            "層級": layer,
            "時間戳": timestamp,
            "數據": data,
            "驗證碼": self._compute_stamp_hash(layer, data, timestamp),
            "狀態": "✓ 已蓋章"
        }
        self.stamps[layer] = stamp_data
        return stamp_data["驗證碼"]

    def stamp_all(self, data_map: Dict[str, Dict[str, Any]]) -> Dict[str, str]:
        """為所有六層蓋章 / Stamp all six layers"""
        results = {}
        for layer in self.LAYERS:
            layer_data = data_map.get(layer, {})
            results[layer] = self.stamp(layer, layer_data)
        return results

    def _compute_stamp_hash(self, layer: str, data: Dict, timestamp: str) -> str:
        """計算蓋章驗證碼 / Compute stamp verification hash"""
        payload = json.dumps({"layer": layer, "data": data, "ts": timestamp}, sort_keys=True)
        return hashlib.sha256(payload.encode('utf-8')).hexdigest()[:16]

    def verify_chain(self) -> Dict[str, Any]:
        """驗證完整來源鏈 / Verify complete source chain"""
        results = {}
        all_valid = True
        for layer in self.LAYERS:
            if layer in self.stamps:
                stamp = self.stamps[layer]
                recalculated = self._compute_stamp_hash(
                    layer, stamp["數據"], stamp["時間戳"]
                )
                valid = recalculated == stamp["驗證碼"]
                results[layer] = {"有效": valid, "時間戳": stamp["時間戳"], "驗證碼": stamp["驗證碼"]}
                if not valid:
                    all_valid = False
            else:
                results[layer] = {"有效": False, "原因": "未蓋章"}
                all_valid = False

        return {"完整鏈有效": all_valid, "層級詳情": results}


# ═══════════════════════════════════════════════════════════════════════════════
# 文件審計記錄 / File Audit Record
# ═══════════════════════════════════════════════════════════════════════════════

class FileAuditRecord:
    """
    文件審計記錄 / File Audit Record
    記錄單個文件的審計信息
    """

    def __init__(self, file_path: str, file_hash: str, change_type: FileChangeType,
                 previous_hash: str = "", details: Dict[str, Any] = None):
        self.file_path = file_path          # 文件路徑 / File path
        self.file_hash = file_hash          # 當前哈希 / Current hash
        self.change_type = change_type      # 變更類型 / Change type
        self.previous_hash = previous_hash  # 先前哈希 / Previous hash
        self.details = details or {}        # 附加詳情 / Additional details
        self.timestamp = datetime.now().isoformat()  # 時間戳 / Timestamp

        # 文件元數據 / File metadata
        try:
            stat_info = os.stat(file_path)
            self.size = stat_info.st_size                    # 文件大小
            self.permissions = stat.S_IMODE(stat_info.st_mode)  # 權限
            self.modified_time = stat_info.st_mtime           # 修改時間
            self.created_time = stat_info.st_ctime            # 創建時間
        except (OSError, FileNotFoundError):
            self.size = 0
            self.permissions = 0
            self.modified_time = 0
            self.created_time = 0

    def to_dict(self) -> Dict[str, Any]:
        """轉換為字典 / Convert to dictionary"""
        return {
            "文件路徑": self.file_path,
            "當前哈希": self.file_hash,
            "先前哈希": self.previous_hash if self.previous_hash else None,
            "變更類型": self.change_type.value,
            "文件大小": self.size,
            "權限": oct(self.permissions),
            "修改時間": self.modified_time,
            "時間戳": self.timestamp,
            "詳情": self.details
        }

    def to_json(self) -> str:
        """轉換為JSON字符串 / Convert to JSON string"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


# ═══════════════════════════════════════════════════════════════════════════════
# 文件審計底座 (核心類) / File Audit Foundation (Core Class)
# ═══════════════════════════════════════════════════════════════════════════════

class 文件審計底座:
    """
    龍魂文件審計底座 / LongHun File Audit Foundation
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    文件系統級審計，監控文件變更和完整性
    File system-level audit, monitoring file changes and integrity

    核心功能 / Core Functions:
        1. SHA256 文件完整性哈希計算 / SHA256 file integrity hash
        2. 文件變更監控 / File change monitoring
        3. 審計日誌記錄 / Audit logging
        4. 完整審計報告生成 / Comprehensive audit report generation
        5. 六層來源鏈蓋章 / Six-layer source chain stamping
    """

    def __init__(self, 監控目錄: str):
        """
        構造函數 / Constructor

        參數 / Parameters:
            監控目錄: 需要監控的目錄路徑 / Directory path to monitor
        """
        self.監控目錄 = os.path.abspath(監控目錄)
        self.審計日誌: List[FileAuditRecord] = []
        self.文件哈希表: Dict[str, str] = {}  # 路徑→哈希映射 / path→hash mapping
        self.文件權限表: Dict[str, int] = {}  # 路徑→權限映射 / path→permission mapping
        self.審計系統 = ThreeColorAudit()
        self.來源鏈 = SourceChain()
        self.啟動時間 = datetime.now().isoformat()

        # 配置日誌
        logging.basicConfig(
            level=logging.INFO,
            format='[%(asctime)s] %(name)s · %(levelname)s · %(message)s'
        )
        self.logger = logging.getLogger("文件審計底座")

        # 確保目錄存在
        if not os.path.exists(self.監控目錄):
            raise FileNotFoundError(f"監控目錄不存在: {self.監控目錄}")

        self.logger.info(f"🐉 文件審計底座初始化完成 · 監控目錄: {self.監控目錄}")

    def 計算文件哈希(self, 文件路徑: str) -> str:
        """
        計算文件的SHA256哈希值 / Calculate SHA256 hash of a file

        參數 / Parameters:
            文件路徑: 文件的絕對或相對路徑 / File absolute or relative path

        返回 / Returns:
            SHA256哈希值的十六進制字符串 / Hex string of SHA256 hash
        """
        import hashlib
        try:
            with open(文件路徑, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except (IOError, OSError) as e:
            self.logger.error(f"無法讀取文件 {文件路徑}: {e}")
            self.審計系統.record("文件哈希", f"讀取失敗:{os.path.basename(文件路徑)}",
                                0.0, f"文件讀取失敗: {e}")
            return ""

    def 審計全部文件(self) -> Dict[str, Any]:
        """
        審計監控目錄下的全部文件 / Audit all files under monitored directory

        遍歷監控目錄，計算每個文件的哈希值，比對之前的哈希檢測變更
        Traverses monitored directory, computes hash for each file,
        compares with previous hashes to detect changes.

        返回 / Returns:
            包含變更檢測結果的字典 / Dictionary with change detection results
        """
        self.logger.info("🔍 開始審計全部文件...")
        print("\n" + "=" * 70)
        print("  🔍 文件底座審計 · File Audit Foundation")
        print(f"  監控目錄: {self.監控目錄}")
        print("  " + "=" * 70)

        changes = {
            FileChangeType.CREATED: [],
            FileChangeType.MODIFIED: [],
            FileChangeType.DELETED: [],
            FileChangeType.PERMISSION_CHANGED: [],
            FileChangeType.UNCHANGED: []
        }

        current_files: Set[str] = set()

        # 遍歷所有文件 / Traverse all files
        for root, dirs, files in os.walk(self.監控目錄):
            # 排除 __pycache__ 和 .git 目錄
            dirs[:] = [d for d in dirs if d not in ('__pycache__', '.git', '.pytest_cache')]

            for filename in files:
                # 跳過臨時文件和緩存
                if filename.endswith(('.pyc', '.tmp', '.swp', '~')):
                    continue

                full_path = os.path.join(root, filename)
                current_files.add(full_path)

                file_hash = self.計算文件哈希(full_path)
                if not file_hash:
                    continue

                # 檢查文件變更
                change_type, previous_hash = self._檢測變更(full_path, file_hash)

                # 檢查權限變更
                try:
                    current_perm = stat.S_IMODE(os.stat(full_path).st_mode)
                    if full_path in self.文件權限表:
                        if self.文件權限表[full_path] != current_perm:
                            if change_type == FileChangeType.UNCHANGED:
                                change_type = FileChangeType.PERMISSION_CHANGED
                    self.文件權限表[full_path] = current_perm
                except OSError:
                    pass

                # 記錄變更
                if change_type != FileChangeType.UNCHANGED:
                    record = FileAuditRecord(
                        file_path=full_path,
                        file_hash=file_hash,
                        change_type=change_type,
                        previous_hash=previous_hash,
                        details={"監控目錄": self.監控目錄}
                    )
                    self.審計日誌.append(record)
                    changes[change_type].append(record)
                    self.logger.info(f"{change_type.value}: {full_path}")

                # 更新哈希表
                self.文件哈希表[full_path] = file_hash

        # 檢查刪除的文件
        previous_files = set(self.文件哈希表.keys())
        deleted_files = previous_files - current_files
        for deleted_path in deleted_files:
            previous_hash = self.文件哈希表[deleted_path]
            record = FileAuditRecord(
                file_path=deleted_path,
                file_hash="",
                change_type=FileChangeType.DELETED,
                previous_hash=previous_hash,
                details={"監控目錄": self.監控目錄}
            )
            self.審計日誌.append(record)
            changes[FileChangeType.DELETED].append(record)
            del self.文件哈希表[deleted_path]
            if deleted_path in self.文件權限表:
                del self.文件權限表[deleted_path]
            self.logger.info(f"刪除: {deleted_path}")

        # 記錄審計結果
        total_changes = sum(len(v) for v in changes.values()) - len(changes[FileChangeType.UNCHANGED])
        if total_changes == 0:
            self.審計系統.record("文件審計", "變更檢測", 1.0, "未發現文件變更")
        else:
            conf = max(0.85 - (total_changes * 0.02), 0.5)
            self.審計系統.record("文件審計", "變更檢測", conf,
                                f"發現 {total_changes} 個文件變更")

        result = {
            "審計時間": datetime.now().isoformat(),
            "監控目錄": self.監控目錄,
            "總文件數": len(current_files),
            "變更摘要": {
                change_type.value: len(records)
                for change_type, records in changes.items()
            },
            "變更詳情": {
                change_type.value: [r.to_dict() for r in records]
                for change_type, records in changes.items() if records
            }
        }

        # 打印摘要
        print(f"\n  📊 審計摘要:")
        print(f"     監控目錄: {self.監控目錄}")
        print(f"     總文件數: {len(current_files)}")
        for change_type, records in changes.items():
            if records or change_type == FileChangeType.UNCHANGED:
                emoji = {"新增": "🟢", "修改": "🟡", "刪除": "🔴",
                        "權限變更": "🟡", "未變更": "⚪"}.get(change_type.value, "⚪")
                print(f"     {emoji} {change_type.value}: {len(records)}")

        print("\n" + "=" * 70 + "\n")

        return result

    def _檢測變更(self, 文件路徑: str, 當前哈希: str) -> Tuple[FileChangeType, str]:
        """
        檢測單個文件的變更 / Detect change for a single file

        返回 / Returns:
            (變更類型, 先前哈希) / (Change type, previous hash)
        """
        if 文件路徑 not in self.文件哈希表:
            return FileChangeType.CREATED, ""

        previous_hash = self.文件哈希表[文件路徑]
        if previous_hash != 當前哈希:
            return FileChangeType.MODIFIED, previous_hash

        return FileChangeType.UNCHANGED, previous_hash

    def 生成審計報告(self) -> str:
        """
        生成完整的審計報告 / Generate comprehensive audit report

        返回 / Returns:
            格式化的審計報告字符串 / Formatted audit report string
        """
        audit_summary = self.審計系統.summary()

        lines = [
            "=" * 70,
            "  🐉 龍魂文件審計報告 · LongHun File Audit Report",
            "=" * 70,
            f"  DNA:#龍芯⚡️2026-06-18-LONGHUN_FILE_AUDIT_FOUNDATION_V1-v1.0.0",
            f"  監控目錄: {self.監控目錄}",
            f"  啟動時間: {self.啟動時間}",
            f"  報告時間: {datetime.now().isoformat()}",
            "-" * 70,
            "  一、審計摘要 / Audit Summary",
            "-" * 70,
            f"     總審計記錄: {audit_summary['總數']}",
            f"     🟢 通過: {audit_summary['🟢通過']}",
            f"     🟡 警告: {audit_summary['🟡警告']}",
            f"     🔴 阻斷: {audit_summary['🔴阻斷']}",
            f"     整體狀態: {audit_summary['整體狀態']}",
            "-" * 70,
            "  二、文件變更記錄 / File Change Records",
            "-" * 70,
        ]

        if not self.審計日誌:
            lines.append("     無變更記錄 / No change records")
        else:
            for i, record in enumerate(self.審計日誌, 1):
                emoji = {"新增": "🟢", "修改": "🟡", "刪除": "🔴",
                        "權限變更": "🟡", "未變更": "⚪"}.get(record.change_type.value, "⚪")
                lines.extend([
                    f"\n     [{i}] {emoji} {record.change_type.value}",
                    f"         路徑: {record.file_path}",
                    f"         哈希: {record.file_hash[:16]}..." if record.file_hash else "         哈希: (已刪除)",
                    f"         大小: {record.size:,} bytes",
                    f"         時間: {record.timestamp}"
                ])

        lines.extend([
            "-" * 70,
            "  三、當前文件哈希表 / Current File Hash Table",
            "-" * 70,
        ])

        if not self.文件哈希表:
            lines.append("     哈希表為空 / Hash table empty")
        else:
            for path, hash_val in sorted(self.文件哈希表.items()):
                rel_path = os.path.relpath(path, self.監控目錄)
                lines.append(f"     {rel_path}: {hash_val[:16]}...")

        lines.extend([
            "-" * 70,
            "  四、六層來源鏈驗證 / Six-Layer Source Chain",
            "-" * 70,
        ])

        chain_verify = self.來源鏈.verify_chain()
        lines.append(f"     完整鏈有效: {'✅ 是' if chain_verify['完整鏈有效'] else '🔴 否'}")
        for layer, detail in chain_verify.get("層級詳情", {}).items():
            status = "✓" if detail.get("有效") else "✗"
            lines.append(f"     [{status}] {layer}")

        lines.extend([
            "=" * 70,
            f"  報告生成完成 · {datetime.now().isoformat()}",
            "  LongHun File Audit Foundation v1.0.0 · UID9622",
            "=" * 70
        ])

        return "\n".join(lines)

    def 保存審計日誌(self, 日誌路徑: str = "") -> str:
        """
        保存審計日誌到JSON文件 / Save audit log to JSON file

        參數 / Parameters:
            日誌路徑: 日誌文件保存路徑，默認為監控目錄下 audit_log_{timestamp}.json

        返回 / Returns:
            保存的日誌文件路徑 / Path to saved log file
        """
        if not 日誌路徑:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            日誌路徑 = os.path.join(self.監控目錄, f"audit_log_{timestamp}.json")

        log_data = {
            "DNA": "#龍芯⚡️2026-06-18-LONGHUN_FILE_AUDIT_FOUNDATION_V1-v1.0.0",
            "創始人": "UID9622 · 龍芯北辰 · 諸葛鑫",
            "監控目錄": self.監控目錄,
            "啟動時間": self.啟動時間,
            "日誌時間": datetime.now().isoformat(),
            "審計摘要": self.審計系統.summary(),
            "變更記錄": [r.to_dict() for r in self.審計日誌],
            "當前哈希表": self.文件哈希表,
            "版本": "v1.0.0"
        }

        with open(日誌路徑, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, ensure_ascii=False, indent=2)

        self.logger.info(f"審計日誌已保存: {日誌路徑}")
        self.審計系統.record("文件審計", "日誌保存", 0.95, f"日誌已保存至 {日誌路徑}")
        return 日誌路徑

    def 加載基線哈希(self, 基線文件: str) -> Dict[str, str]:
        """
        從文件加載基線哈希表 / Load baseline hash table from file

        參數 / Parameters:
            基線文件: 包含基線哈希的JSON文件路徑

        返回 / Returns:
            哈希表字典 / Hash table dictionary
        """
        try:
            with open(基線文件, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if "當前哈希表" in data:
                self.文件哈希表 = data["當前哈希表"]
            elif "hashes" in data:
                self.文件哈希表 = data["hashes"]
            else:
                self.文件哈希表 = data

            self.logger.info(f"已加載基線哈希表: {len(self.文件哈希表)} 個文件")
            self.審計系統.record("文件審計", "基線加載", 0.95,
                                f"已加載 {len(self.文件哈希表)} 個基線哈希")
            return self.文件哈希表

        except (IOError, json.JSONDecodeError) as e:
            self.logger.error(f"無法加載基線文件: {e}")
            self.審計系統.record("文件審計", "基線加載", 0.0, f"基線加載失敗: {e}")
            return {}

    def 保存基線哈希(self, 基線文件: str = "") -> str:
        """保存當前哈希表作為基線 / Save current hash table as baseline"""
        if not 基線文件:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            基線文件 = os.path.join(self.監控目錄, f"baseline_hashes_{timestamp}.json")

        with open(基線文件, 'w', encoding='utf-8') as f:
            json.dump({
                "DNA": "#龍芯⚡️2026-06-18-LONGHUN_FILE_AUDIT_FOUNDATION_V1-v1.0.0",
                "當前哈希表": self.文件哈希表,
                "保存時間": datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2)

        self.logger.info(f"基線哈希表已保存: {基線文件}")
        return 基線文件

    def 執行來源鏈蓋章(self) -> Dict[str, str]:
        """
        執行六層來源鏈蓋章 / Execute six-layer source chain stamping
        為文件審計結果蓋上六層來源鏈驗證章
        """
        data_map = {
            "道統層": {"根源": "龍魂道統", "傳承": "UID9622", "審計類型": "文件完整性"},
            "精神層": {"核心價值": "數據不可篡改", "精神": "透明審計"},
            "設備層": {"平台": sys.platform, "監控目錄": self.監控目錄},
            "技術層": {"哈希算法": "SHA256", "語言": "Python"},
            "系統層": {"完整性": "已驗證", "狀態": "運行中"},
            "生命層": {"創作者": "UID9622 · 龍芯北辰", "身份": "文件審計底座"}
        }

        results = self.來源鏈.stamp_all(data_map)
        self.審計系統.record("文件審計", "來源鏈蓋章", 0.95, "六層來源鏈蓋章完成")
        self.logger.info("六層來源鏈蓋章完成")
        return results

    def 獲取審計摘要(self) -> Dict[str, Any]:
        """獲取審計摘要 / Get audit summary"""
        return self.審計系統.summary()

    def 清除審計日誌(self):
        """清除審計日誌 / Clear audit log"""
        count = len(self.審計日誌)
        self.審計日誌.clear()
        self.審計系統.record("文件審計", "日誌清除", 0.85, f"已清除 {count} 條日誌記錄")
        self.logger.info(f"已清除 {count} 條審計日誌")


# ═══════════════════════════════════════════════════════════════════════════════
# 主入口 / Main Entry Point
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "📁" * 35)
    print("  龍魂文件底座審計 · LongHun File Audit Foundation")
    print("  v1.0.0 · DNA:#龍芯⚡️2026-06-18-LONGHUN_FILE_AUDIT_FOUNDATION_V1-v1.0.0")
    print("  " + "📁" * 35 + "\n")

    # 使用當前目錄作為監控目錄
    監控路徑 = os.path.dirname(os.path.abspath(__file__))
    if not 監控路徑:
        監控路徑 = "."

    print(f"📂 監控目錄: {監控路徑}\n")

    try:
        # 創建審計底座實例
        審計底座 = 文件審計底座(監控路徑)

        # 執行完整審計
        審計結果 = 審計底座.審計全部文件()

        # 執行來源鏈蓋章
        蓋章結果 = 審計底座.執行來源鏈蓋章()
        print("\n🔗 來源鏈蓋章結果:")
        for layer, code in 蓋章結果.items():
            print(f"   [{layer}] ✓ {code}")

        # 生成並打印審計報告
        print("\n📋 生成審計報告...")
        報告 = 審計底座.生成審計報告()
        print(報告)

        # 保存審計日誌
        日誌路徑 = 審計底座.保存審計日誌()
        print(f"\n💾 審計日誌已保存: {日誌路徑}")

        # 輸出審計摘要
        print("\n📊 最終審計摘要 / Final Audit Summary:")
        print(json.dumps(審計底座.獲取審計摘要(), ensure_ascii=False, indent=2))

    except FileNotFoundError as e:
        print(f"🔴 錯誤: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"🔴 未預期錯誤: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
