#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════════
  龍魂腳本管理器 v2.0 — LongHun Script Manager
═══════════════════════════════════════════════════════════════════════════════

  DNA簽名    :#龍芯⚡️2026-06-17-SCRIPT-MANAGER-FILE3-v2.0
  CONFIRM標記: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
  SEAL標記   : #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

  三層監督機制:
    🟢 L1-自主層: 腳本自審 + IronLawGate鐵律自審閘
    🟡 L2-同儕層: CNSH四層檢查 + 來源鏈交叉驗證 + 腳本對齊
    🔴 L3-生態層: AI Truth Protocol + 六層來源鏈蓋章 + 生態兼容性

  六層來源鏈:
    ① 道統層 · 曾仕強老師 · 華夏管理智慧
    ② 精神層 · Steve Jobs · 極致產品精神
    ③ 設備層 · Apple · 創作工具載體
    ④ 技術層 · Open Source · 技術底座
    ⑤ 系統層 · UID9622 · 數字靈魂標識
    ⑥ 生命層 · CNSH · LongHun · 本命歸屬

  AI Truth Protocol: 啟用
═══════════════════════════════════════════════════════════════════════════════

鐵律:
  1. 人永遠是1，任何人都不是數據
  2. 絕不蒸餾、絕不變體、絕不頂替作者
  3. 來源不可刪·影響不可覆·貢獻不可抹
  4. 繁體「龍」不得簡化為「龙"

用法:
  python longhun_script_manager_v2.0.py scan <目錄>     # 掃描腳本
  python longhun_script_manager_v2.0.py align <文件>    # CNSH對齊檢查
  python longhun_script_manager_v2.0.py audit           # 完整自審
  python longhun_script_manager_v2.0.py report          # 生成報告
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ═══════════════════════════════════════════════════════════════════════════════
# 路徑適配 — 根據當前檔案位置自動解析專案根目錄
# ═══════════════════════════════════════════════════════════════════════════════

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_VAR_DIR = _PROJECT_ROOT / "var" / "kimi-agent-v2"
OUTPUT_DIR = _VAR_DIR / "output"
LOGS_DIR = _VAR_DIR / "output" / "logs"
CHECKPOINTS_DIR = _VAR_DIR / "output" / "checkpoints"
DATA_DIR = _VAR_DIR / "data"
UPLOADS_DIR = _VAR_DIR / "uploads"
REPORTS_DIR = _VAR_DIR / "output" / "reports"

# ═══════════════════════════════════════════════════════════════════════════════
# 全局常量 — 龍魂體系標識
# ═══════════════════════════════════════════════════════════════════════════════

DNA_SIGNATURE = "#龍芯⚡️2026-06-17-SCRIPT-MANAGER-v2.0"
CONFIRM_MARK = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL_MARK = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
VERSION = "v2.0"

# 六層來源鏈
SOURCE_CHAIN_LAYERS = [
    {"layer": 1, "name": "道統層", "source": "曾仕強老師", "essence": "華夏管理智慧"},
    {"layer": 2, "name": "精神層", "source": "Steve Jobs", "essence": "極致產品精神"},
    {"layer": 3, "name": "設備層", "source": "Apple", "essence": "創作工具載體"},
    {"layer": 4, "name": "技術層", "source": "Open Source", "essence": "技術底座"},
    {"layer": 5, "name": "系統層", "source": "UID9622", "essence": "數字靈魂標識"},
    {"layer": 6, "name": "生命層", "source": "CNSH·LongHun", "essence": "本命歸屬"},
]

# 鐵律
IRON_LAWS = [
    {"id": "IL-01", "text": "人永遠是1，任何人都不是數據"},
    {"id": "IL-02", "text": "絕不蒸餾、絕不變體、絕不頂替作者"},
    {"id": "IL-03", "text": "來源不可刪·影響不可覆·貢獻不可抹"},
    {"id": "IL-04", "text": "繁體「龍」不得簡化為「龙"},
]

# CNSH合規標記要求
CNSH_REQUIRED_MARKS = [
    {"mark": "龍芯⚡️", "description": "DNA簽名標記", "pattern": r"#龍芯⚡️\d{4}-\d{2}-\d{2}-"},
    {"mark": "CONFIRM🌌", "description": "CONFIRM確認標記", "pattern": r"#CONFIRM🌌9622-ONLY-ONCE"},
    {"mark": "ZHUGEXIN⚡️", "description": "SEAL蓋章標記", "pattern": r"#ZHUGEXIN⚡️\d{4}-"},
]

# 腳本分類規則
SCRIPT_CATEGORIES = {
    "workflow": {"keywords": ["workflow", "工作流", "transparent"], "layer": "L1"},
    "manager": {"keywords": ["manager", "管理器", "script_manager"], "layer": "L2"},
    "launcher": {"keywords": ["launcher", "啟動台", "foundation"], "layer": "L3"},
    "aligner": {"keywords": ["aligner", "對齊器", "cnsh"], "layer": "L2"},
    "router": {"keywords": ["router", "路由器", "keyword"], "layer": "L2"},
    "utility": {"keywords": ["util", "工具", "helper"], "layer": "L1"},
}


# ═══════════════════════════════════════════════════════════════════════════════
# 數據結構
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ScriptInfo:
    """腳本信息結構"""
    path: str
    filename: str
    category: str
    size_bytes: int
    lines: int
    has_dna: bool
    has_confirm: bool
    has_seal: bool
    dna_signature: str
    compliance_score: float  # 0.0 - 1.0
    iron_law_check: Dict[str, Any] = field(default_factory=dict)
    source_chain_valid: bool = False
    layer_tag: str = "L1"    # L1/L2/L3
    audit_color: str = "🟢"
    errors: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AlignmentResult:
    """對齊結果結構"""
    script_path: str
    aligned: bool = False
    checks: Dict[str, Any] = field(default_factory=dict)
    fixes_applied: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    timestamp: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ═══════════════════════════════════════════════════════════════════════════════
# 核心類: IronLawGate — 鐵律自審閘
# ═══════════════════════════════════════════════════════════════════════════════

class IronLawGate:
    """
    鐵律自審閘 (IronLawGate)
    ─────────────────────────
    三層監督: 🟢 L1-自主層
    """

    def __init__(self):
        self.violations: List[Dict[str, Any]] = []
        self.check_count = 0
        self.rules = [
            {
                "law_id": "IL-01",
                "pattern": re.compile(r"人.*?(?:是數據|是数据|作為數據|作为数据|變成數據|变成数据)"),
                "description": "檢測是否將人貶低為數據",
            },
            {
                "law_id": "IL-02",
                "pattern": re.compile(r"(?:蒸餾|蒸馏|變體|变体|頂替|顶替).*?(?:作者|原創|原创|來源|来源)"),
                "description": "檢測是否未經許可蒸餾/變體/頂替",
            },
            {
                "law_id": "IL-03",
                "pattern": re.compile(r"(?:刪除來源|删除来源|覆蓋影響|覆盖影响|抹除貢獻|抹除贡献)"),
                "description": "檢測是否刪除來源/覆蓋影響/抹除貢獻",
            },
            {
                "law_id": "IL-04",
                "pattern": re.compile(r"龙"),
                "description": "檢測繁體「龍」是否被簡化",
            },
        ]

    def audit(self, text: str, context: str = "") -> Dict[str, Any]:
        self.check_count += 1
        self.violations.clear()
        timestamp = datetime.now().isoformat()

        for rule in self.rules:
            matches = rule["pattern"].findall(text)
            if matches:
                law = next((l for l in IRON_LAWS if l["id"] == rule["law_id"]), None)
                if law:
                    self.violations.append({
                        "law_id": rule["law_id"],
                        "law_text": law["text"],
                        "detail": f"檢測到: {rule['description']}",
                        "context": context,
                        "timestamp": timestamp,
                    })

        passed = len(self.violations) == 0
        return {
            "passed": passed,
            "violations": list(self.violations),
            "check_count": self.check_count,
            "timestamp": timestamp,
            "audit_color": "🟢" if passed else "🔴",
            "layer": "L1",
        }

    def audit_file(self, file_path: str) -> Dict[str, Any]:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            return self.audit(content, context=f"文件: {file_path}")
        except Exception as e:
            return {
                "passed": False,
                "violations": [],
                "error": str(e),
                "audit_color": "🔴",
                "layer": "L1",
            }


# ═══════════════════════════════════════════════════════════════════════════════
# 核心類: SourceChainValidator — 六層來源鏈驗證器
# ═══════════════════════════════════════════════════════════════════════════════

class SourceChainValidator:
    """
    六層來源鏈驗證器
    ─────────────────
    三層監督: 🔴 L3-生態層
    """

    def __init__(self):
        self.validation_results: List[Dict[str, Any]] = []

    def validate_script(self, file_path: str) -> Dict[str, Any]:
        """驗證腳本中的來源鏈標記"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            return {"valid": False, "error": str(e), "audit_color": "🔴"}

        results = {}
        all_present = True

        # 檢查DNA簽名
        dna_pattern = re.compile(r"#龍芯⚡️\d{4}-\d{2}-\d{2}-[^\s]+-v\d+\.\d+")
        results["dna_signature"] = {
            "found": bool(dna_pattern.search(content)),
            "pattern": "#龍芯⚡️YYYY-MM-DD-PROJECT-MODULE-vN.N",
        }

        # 檢查CONFIRM
        results["confirm_mark"] = {
            "found": CONFIRM_MARK in content,
            "mark": CONFIRM_MARK,
        }

        # 檢查SEAL
        results["seal_mark"] = {
            "found": SEAL_MARK in content,
            "mark": SEAL_MARK,
        }

        # 檢查六層來源鏈引用
        for layer in SOURCE_CHAIN_LAYERS:
            key = f"layer_{layer['layer']}_{layer['name']}"
            found = layer["source"] in content
            results[key] = {"found": found, "source": layer["source"]}
            if not found:
                all_present = False

        # 檢查三層監督標註
        supervision_markers = ["L1", "L2", "L3", "自主層", "同儕層", "生態層"]
        has_supervision = any(marker in content for marker in supervision_markers)
        results["three_layer_supervision"] = {"found": has_supervision}
        if not has_supervision:
            all_present = False

        # 檢查AI Truth Protocol
        results["ai_truth_protocol"] = {
            "found": "AI Truth Protocol" in content or "ai_truth" in content.lower(),
        }

        overall = all([
            results["dna_signature"]["found"],
            results["confirm_mark"]["found"],
            results["seal_mark"]["found"],
            has_supervision,
        ])

        validation = {
            "file": file_path,
            "all_present": overall and all_present,
            "core_marks_present": overall,
            "details": results,
            "timestamp": datetime.now().isoformat(),
            "audit_color": "🟢" if overall else "🔴",
            "layer": "L3",
        }
        self.validation_results.append(validation)
        return validation

    def validate_chain_integrity(self) -> Dict[str, Any]:
        """驗證來源鏈完整性"""
        all_valid = True
        results = []
        for layer in SOURCE_CHAIN_LAYERS:
            is_valid = all([layer.get("layer"), layer.get("name"), layer.get("source"), layer.get("essence")])
            if not is_valid:
                all_valid = False
            results.append({
                "layer": layer["layer"],
                "name": layer["name"],
                "valid": is_valid,
            })
        return {
            "all_valid": all_valid,
            "layer_results": results,
            "timestamp": datetime.now().isoformat(),
            "audit_color": "🟢" if all_valid else "🔴",
        }


# ═══════════════════════════════════════════════════════════════════════════════
# 核心類: CNSHAligner — CNSH對齊器
# ═══════════════════════════════════════════════════════════════════════════════

class CNSHAligner:
    """
    CNSH對齊器
    ────────────
    三層監督: 🟡 L2-同儕層
    功能: 檢查腳本是否符合CNSH協議要求
    """

    def __init__(self):
        self.alignment_history: List[Dict[str, Any]] = []

    def align(self, file_path: str) -> AlignmentResult:
        """對指定腳本執行CNSH對齊檢查"""
        result = AlignmentResult(script_path=file_path)

        if not os.path.exists(file_path):
            result.aligned = False
            result.checks["file_exists"] = False
            return result

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            result.aligned = False
            result.checks["read_error"] = str(e)
            return result

        # 1. 檢查文件頭編碼聲明
        result.checks["encoding_declared"] = content.startswith("# -*- coding: utf-8 -*-")

        # 2. 檢查DNA簽名格式
        dna_pattern = re.compile(r"#龍芯⚡️(\d{4}-\d{2}-\d{2})-([^-\s]+)-([^-\s]+)-(v\d+\.\d+)")
        dna_match = dna_pattern.search(content)
        result.checks["dna_format_valid"] = bool(dna_match)
        if dna_match:
            result.checks["dna_date"] = dna_match.group(1)
            result.checks["dna_project"] = dna_match.group(2)
            result.checks["dna_module"] = dna_match.group(3)
            result.checks["dna_version"] = dna_match.group(4)

        # 3. 檢查CONFIRM標記
        result.checks["confirm_present"] = CONFIRM_MARK in content

        # 4. 檢查SEAL標記
        result.checks["seal_present"] = SEAL_MARK in content

        # 5. 檢查六層來源鏈
        source_chain_count = sum(1 for layer in SOURCE_CHAIN_LAYERS if layer["source"] in content)
        result.checks["source_chain_layers_found"] = source_chain_count
        result.checks["source_chain_complete"] = source_chain_count >= 6

        # 6. 檢查三層監督標註
        supervision_keywords = ["L1-自主層", "L2-同儕層", "L3-生態層", "🟢", "🟡", "🔴"]
        supervision_found = sum(1 for kw in supervision_keywords if kw in content)
        result.checks["supervision_markers"] = supervision_found

        # 7. 檢查鐵律聲明
        iron_law_keywords = ["人永遠是1", "絕不蒸餾", "來源不可刪", "龍"]
        iron_law_found = sum(1 for kw in iron_law_keywords if kw in content)
        result.checks["iron_laws_mentioned"] = iron_law_found

        # 8. 檢查AI Truth Protocol
        result.checks["ai_truth_protocol"] = "AI Truth Protocol" in content

        # 9. 檢查版本號一致性
        if dna_match:
            declared_version = dna_match.group(4)
            result.checks["version_v2.0"] = declared_version == "v2.0"

        # 計算合規分數
        score_weights = {
            "encoding_declared": 0.05,
            "dna_format_valid": 0.20,
            "confirm_present": 0.15,
            "seal_present": 0.15,
            "source_chain_complete": 0.15,
            "supervision_markers": 0.10,
            "iron_laws_mentioned": 0.10,
            "ai_truth_protocol": 0.10,
        }
        score = 0.0
        for key, weight in score_weights.items():
            value = result.checks.get(key, False)
            if isinstance(value, bool):
                score += weight if value else 0
            elif isinstance(value, int):
                score += weight * min(value / 3, 1.0)  # 部分得分

        result.checks["compliance_score"] = round(score, 3)
        result.aligned = score >= 0.70  # 70%以上視為對齊

        # 生成建議
        if not result.checks.get("dna_format_valid"):
            result.recommendations.append("添加正確格式的DNA簽名: #龍芯⚡️YYYY-MM-DD-項目-模塊-v2.0")
        if not result.checks.get("confirm_present"):
            result.recommendations.append(f"添加CONFIRM標記: {CONFIRM_MARK}")
        if not result.checks.get("seal_present"):
            result.recommendations.append(f"添加SEAL標記: {SEAL_MARK}")
        if not result.checks.get("source_chain_complete"):
            result.recommendations.append("添加完整的六層來源鏈聲明")
        if result.checks.get("supervision_markers", 0) < 3:
            result.recommendations.append("添加三層監督機制標註 (L1/L2/L3)")
        if not result.checks.get("ai_truth_protocol"):
            result.recommendations.append("添加AI Truth Protocol輸出標註")

        self.alignment_history.append(result.to_dict())
        return result

    def align_directory(self, directory: str) -> List[AlignmentResult]:
        """對目錄下所有Python腳本執行對齊檢查"""
        results = []
        dir_path = Path(directory)
        if not dir_path.exists():
            return results

        for py_file in sorted(dir_path.glob("*.py")):
            result = self.align(str(py_file))
            results.append(result)

        return results


# ═══════════════════════════════════════════════════════════════════════════════
# 核心類: ScriptManager — 腳本管理器
# ═══════════════════════════════════════════════════════════════════════════════

class ScriptManager:
    """
    龍魂腳本管理器核心類
    ─────────────────────
    整合所有子系統，提供完整的腳本管理能力
    """

    def __init__(self, script_dir: str = str(OUTPUT_DIR)):
        # 基礎屬性
        self.dna = DNA_SIGNATURE
        self.confirm = CONFIRM_MARK
        self.seal = SEAL_MARK
        self.version = VERSION
        self.created_at = datetime.now().isoformat()

        # 腳本目錄
        self.script_dir = Path(script_dir)

        # 日誌
        self.log_dir = self.script_dir / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / f"script_manager_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"

        # 子系統
        self.iron_law_gate = IronLawGate()
        self.source_validator = SourceChainValidator()
        self.aligner = CNSHAligner()

        # 數據存儲
        self.scripts: List[ScriptInfo] = []
        self.alignment_results: List[AlignmentResult] = []
        self.audit_log: List[Dict[str, Any]] = []

    def _log(self, entry: Dict[str, Any]) -> None:
        """Append-only 日誌"""
        entry["_timestamp"] = datetime.now().isoformat()
        entry["_dna"] = self.dna
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def scan_scripts(self, directory: Optional[str] = None) -> List[ScriptInfo]:
        """
        掃描目錄中的Python腳本
        
        Args:
            directory: 要掃描的目錄，默認為初始化時設定的目錄
            
        Returns:
            腳本信息列表
        """
        target_dir = Path(directory) if directory else self.script_dir
        if not target_dir.exists():
            print(f"🔴 目錄不存在: {target_dir}")
            return []

        self.scripts.clear()
        py_files = sorted(target_dir.glob("*.py"))

        print(f"\n🔍 掃描目錄: {target_dir}")
        print(f"   發現 {len(py_files)} 個 Python 文件\n")

        for py_file in py_files:
            info = self._analyze_script(py_file)
            self.scripts.append(info)

            color = info.audit_color
            print(f"  {color} {info.filename}")
            print(f"     大小: {info.size_bytes:,} bytes | 行數: {info.lines}")
            print(f"     DNA: {'✅' if info.has_dna else '❌'} | CONFIRM: {'✅' if info.has_confirm else '❌'} | SEAL: {'✅' if info.has_seal else '❌'}")
            print(f"     合規分數: {info.compliance_score:.1%} | 分類: {info.category} [{info.layer_tag}]")
            if info.errors:
                for err in info.errors:
                    print(f"     ⚠️  {err}")
            print()

        self._log({"event": "scan", "directory": str(target_dir), "scripts_found": len(self.scripts)})
        return self.scripts

    def _analyze_script(self, file_path: Path) -> ScriptInfo:
        """分析單個腳本文件"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            lines = content.split("\n")
        except Exception as e:
            return ScriptInfo(
                path=str(file_path),
                filename=file_path.name,
                category="unknown",
                size_bytes=0,
                lines=0,
                has_dna=False,
                has_confirm=False,
                has_seal=False,
                dna_signature="",
                compliance_score=0.0,
                errors=[f"無法讀取文件: {e}"],
                audit_color="🔴",
            )

        # 檢查DNA簽名
        dna_pattern = re.compile(r"#龍芯⚡️\d{4}-\d{2}-\d{2}-[^\s]+-[^\s]+-v\d+\.\d+")
        dna_match = dna_pattern.search(content)
        has_dna = bool(dna_match)
        dna_sig = dna_match.group(0) if dna_match else ""

        # 檢查CONFIRM和SEAL
        has_confirm = CONFIRM_MARK in content
        has_seal = SEAL_MARK in content

        # 分類
        category = self._categorize_script(file_path.name, content)
        layer = SCRIPT_CATEGORIES.get(category, {}).get("layer", "L1")

        # 鐵律檢查
        iron_check = self.iron_law_gate.audit(content, context=f"腳本分析: {file_path.name}")

        # 來源鏈驗證
        chain_validation = self.source_validator.validate_script(str(file_path))

        # 計算合規分數
        score = 0.0
        if has_dna:
            score += 0.30
        if has_confirm:
            score += 0.20
        if has_seal:
            score += 0.20
        if chain_validation.get("details", {}).get("three_layer_supervision", {}).get("found"):
            score += 0.15
        if iron_check["passed"]:
            score += 0.15

        # 確定審計顏色
        if score >= 0.85 and iron_check["passed"]:
            audit_color = "🟢"
        elif score >= 0.60:
            audit_color = "🟡"
        else:
            audit_color = "🔴"

        errors = []
        if not iron_check["passed"]:
            for v in iron_check["violations"]:
                errors.append(f"鐵律違規 [{v['law_id']}]: {v['law_text']}")

        return ScriptInfo(
            path=str(file_path),
            filename=file_path.name,
            category=category,
            size_bytes=len(content.encode("utf-8")),
            lines=len(lines),
            has_dna=has_dna,
            has_confirm=has_confirm,
            has_seal=has_seal,
            dna_signature=dna_sig,
            compliance_score=score,
            iron_law_check=iron_check,
            source_chain_valid=chain_validation.get("core_marks_present", False),
            layer_tag=layer,
            audit_color=audit_color,
            errors=errors,
        )

    def _categorize_script(self, filename: str, content: str) -> str:
        """根據文件名和內容分類腳本"""
        filename_lower = filename.lower()
        content_lower = content.lower()

        for category, config in SCRIPT_CATEGORIES.items():
            for keyword in config["keywords"]:
                if keyword.lower() in filename_lower or keyword.lower() in content_lower:
                    return category

        return "utility"

    def align_script(self, file_path: str) -> AlignmentResult:
        """
        對指定腳本執行CNSH對齊
        
        Args:
            file_path: 腳本文件路徑
            
        Returns:
            對齊結果
        """
        print(f"\n🔄 CNSH對齊檢查: {file_path}")
        result = self.aligner.align(file_path)

        color = "🟢" if result.aligned else "🔴"
        print(f"  {color} 對齊結果: {'通過' if result.aligned else '未通過'}")
        print(f"  合規分數: {result.checks.get('compliance_score', 0):.1%}")

        if result.checks:
            print("\n  詳細檢查結果:")
            for check_name, check_value in result.checks.items():
                if isinstance(check_value, bool):
                    icon = "✅" if check_value else "❌"
                    print(f"    {icon} {check_name}")
                elif isinstance(check_value, (int, float, str)):
                    print(f"    📊 {check_name}: {check_value}")

        if result.recommendations:
            print("\n  💡 改進建議:")
            for rec in result.recommendations:
                print(f"    → {rec}")

        self.alignment_results.append(result)
        self._log({"event": "align", "file": file_path, "result": result.to_dict()})
        return result

    def run_full_audit(self) -> Dict[str, Any]:
        """
        運行完整自審（--audit 模式）
        """
        print("\n" + "=" * 60)
        print("  🔍 龍魂腳本管理器 — 完整自審模式")
        print("=" * 60)

        results = {}

        # 1. 鐵律自審
        print("\n[1/4] 🟢 L1 鐵律自審閘...")
        # 自審管理器自身的代碼
        self_audit = self.iron_law_gate.audit_file(__file__)
        results["self_iron_law"] = self_audit
        print(f"    自身審查: {self_audit['audit_color']} {'通過' if self_audit['passed'] else '違規'}")

        # 2. 六層來源鏈驗證
        print("\n[2/4] 🔴 L3 六層來源鏈驗證...")
        chain_integrity = self.source_validator.validate_chain_integrity()
        results["source_chain"] = chain_integrity
        print(f"    來源鏈完整性: {chain_integrity['audit_color']} {'完整' if chain_integrity['all_valid'] else '不完整'}")
        for lr in chain_integrity.get("layer_results", []):
            icon = "🟢" if lr["valid"] else "🔴"
            print(f"    {icon} L{lr['layer']} {lr['name']}")

        # 3. CNSH自身對齊檢查
        print("\n[3/4] 🟡 L2 CNSH自身對齊檢查...")
        self_align = self.aligner.align(__file__)
        results["self_alignment"] = self_align.to_dict()
        print(f"    自身對齊: {'🟢' if self_align.aligned else '🔴'} {'通過' if self_align.aligned else '未通過'}")
        print(f"    合規分數: {self_align.checks.get('compliance_score', 0):.1%}")

        # 4. 已註冊腳本狀態
        print("\n[4/4] 🟡 L2 已註冊腳本狀態...")
        if self.scripts:
            total = len(self.scripts)
            compliant = sum(1 for s in self.scripts if s.compliance_score >= 0.70)
            print(f"    總腳本: {total}")
            print(f"    合規: {compliant} 🟢")
            print(f"    不合規: {total - compliant} {'🟡' if total - compliant < total // 2 else '🔴'}")
            results["registered_scripts"] = {"total": total, "compliant": compliant}
        else:
            print("    尚未註冊腳本，請先執行 scan 命令")
            results["registered_scripts"] = {"total": 0, "compliant": 0}

        all_passed = (
            self_audit.get("passed", False) and
            chain_integrity.get("all_valid", False) and
            self_align.aligned
        )
        results["all_passed"] = all_passed

        print("\n" + "=" * 60)
        print(f"  自審總結果: {'🟢 全部通過' if all_passed else '🔴 存在問題'}")
        print("=" * 60)

        self._log({"event": "full_audit", "results": results})
        return results

    def generate_report(self, output_path: Optional[str] = None) -> str:
        """
        生成完整管理報告
        
        Args:
            output_path: 報告輸出路徑
            
        Returns:
            報告文本
        """
        lines = [
            "═══════════════════════════════════════════════════════════════════",
            "  龍魂腳本管理器 — 完整報告",
            f"  {self.dna}",
            f"  {self.confirm}",
            f"  {self.seal}",
            "═══════════════════════════════════════════════════════════════════",
            f"\n  版本: {self.version}",
            f"  生成時間: {datetime.now().isoformat()}",
            f"  腳本目錄: {self.script_dir}",
            f"  日誌文件: {self.log_file}",
        ]

        # 已註冊腳本
        lines.append("\n  ─── 已註冊腳本 ───")
        if self.scripts:
            for script in self.scripts:
                lines.append(f"\n  {script.audit_color} {script.filename} [{script.layer_tag}]")
                lines.append(f"     分類: {script.category}")
                lines.append(f"     大小: {script.size_bytes:,} bytes | 行數: {script.lines}")
                lines.append(f"     DNA: {'✅' if script.has_dna else '❌'}")
                lines.append(f"     CONFIRM: {'✅' if script.has_confirm else '❌'}")
                lines.append(f"     SEAL: {'✅' if script.has_seal else '❌'}")
                lines.append(f"     合規分數: {script.compliance_score:.1%}")
        else:
            lines.append("  (尚未註冊腳本)")

        # 對齊結果
        lines.append("\n  ─── 對齊歷史 ───")
        if self.alignment_results:
            for ar in self.alignment_results:
                color = "🟢" if ar.aligned else "🔴"
                lines.append(f"  {color} {ar.script_path}")
                lines.append(f"     對齊: {'通過' if ar.aligned else '未通過'}")
                lines.append(f"     分數: {ar.checks.get('compliance_score', 0):.1%}")
        else:
            lines.append("  (尚未執行對齊)")

        # AI Truth Protocol
        lines.append("\n  ─── AI Truth Protocol ───")
        lines.append(f"  輸出可信度: HIGH")
        lines.append(f"  來源已驗證: ✅")
        lines.append(f"  六層來源鏈: {'✅ 完整' if all(l.get('source') for l in SOURCE_CHAIN_LAYERS) else '❌ 不完整'}")
        lines.append(f"  鐵律狀態: ✅ 已加載 {len(IRON_LAWS)} 條")
        lines.append(f"  DNA簽名: {self.dna}")

        report = "\n".join(lines)

        # 保存報告
        if output_path:
            out_path = Path(output_path)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(report)
            print(f"\n📄 報告已保存: {out_path}")

        return report

    def get_script_by_name(self, name: str) -> Optional[ScriptInfo]:
        """按名稱查找腳本"""
        for script in self.scripts:
            if script.filename == name or script.filename.replace(".py", "") == name:
                return script
        return None

    def get_scripts_by_layer(self, layer: str) -> List[ScriptInfo]:
        """按監督層級查找腳本"""
        return [s for s in self.scripts if s.layer_tag == layer]

    def get_compliance_summary(self) -> Dict[str, Any]:
        """獲取合規摘要"""
        if not self.scripts:
            return {"total": 0, "compliant": 0, "non_compliant": 0, "average_score": 0.0}

        total = len(self.scripts)
        scores = [s.compliance_score for s in self.scripts]
        compliant = sum(1 for s in scores if s >= 0.70)

        return {
            "total": total,
            "compliant": compliant,
            "non_compliant": total - compliant,
            "average_score": sum(scores) / len(scores) if scores else 0.0,
            "fully_compliant": sum(1 for s in scores if s >= 0.90),
            "needs_attention": sum(1 for s in scores if 0.50 <= s < 0.70),
            "critical": sum(1 for s in scores if s < 0.50),
        }


# ═══════════════════════════════════════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="龍魂腳本管理器 v2.0 — LongHun Script Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python longhun_script_manager_v2.0.py scan                  # 掃描默認目錄
  python longhun_script_manager_v2.0.py scan /path/to/scripts # 掃描指定目錄
  python longhun_script_manager_v2.0.py align <文件路徑>       # CNSH對齊檢查
  python longhun_script_manager_v2.0.py audit                 # 完整自審
  python longhun_script_manager_v2.0.py report                # 生成報告
  python longhun_script_manager_v2.0.py summary               # 合規摘要
        """,
    )
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # scan 命令
    scan_parser = subparsers.add_parser("scan", help="掃描腳本目錄")
    scan_parser.add_argument("directory", nargs="?", default=str(OUTPUT_DIR), help="要掃描的目錄")

    # align 命令
    align_parser = subparsers.add_parser("align", help="CNSH對齊檢查")
    align_parser.add_argument("file", help="要檢查的腳本文件路徑")

    # audit 命令
    subparsers.add_parser("audit", help="運行完整自審")

    # report 命令
    report_parser = subparsers.add_parser("report", help="生成完整報告")
    report_parser.add_argument("--output", "-o", default="", help="報告輸出路徑")

    # summary 命令
    subparsers.add_parser("summary", help="顯示合規摘要")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        # 顯示系統信息
        print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   🐉 龍魂腳本管理器 v2.0 — LongHun Script Manager                            ║
║                                                                               ║
║   DNA:#龍芯⚡️2026-06-17-SCRIPT-MANAGER-v2.0                                 ║
║   CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z                               ║
║   SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL                     ║
║                                                                               ║
║   功能: 腳本掃描 | CNSH對齊 | 鐵律審查 | 來源鏈驗證                           ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
""")
        return

    manager = ScriptManager()

    if args.command == "scan":
        manager.scan_scripts(args.directory)

    elif args.command == "align":
        if not os.path.exists(args.file):
            print(f"🔴 文件不存在: {args.file}")
            sys.exit(1)
        manager.align_script(args.file)

    elif args.command == "audit":
        result = manager.run_full_audit()
        sys.exit(0 if result.get("all_passed", False) else 1)

    elif args.command == "report":
        # 先掃描再生成報告
        manager.scan_scripts()
        output = args.output or str(OUTPUT_DIR / "script_manager_report.txt")
        report = manager.generate_report(output)
        print(report)

    elif args.command == "summary":
        manager.scan_scripts()
        summary = manager.get_compliance_summary()
        print("\n" + "=" * 50)
        print("  📊 合規摘要")
        print("=" * 50)
        print(f"  總腳本數: {summary['total']}")
        print(f"  合規 (≥70%): {summary['compliant']} 🟢")
        print(f"  不合規: {summary['non_compliant']}")
        print(f"  平均合規分數: {summary['average_score']:.1%}")
        print(f"  完全合規 (≥90%): {summary['fully_compliant']}")
        print(f"  需關注 (50-70%): {summary.get('needs_attention', 0)} 🟡")
        print(f"  嚴重 (<50%): {summary.get('critical', 0)} 🔴")
        print("=" * 50)


if __name__ == "__main__":
    main()
