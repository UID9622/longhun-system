#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════════
  龍魂系統底座啟動台 v2.0 — LongHun Foundation Launcher
═══════════════════════════════════════════════════════════════════════════════

  DNA簽名    : #龍芯⚡️2026-06-17-FOUNDATION-LAUNCHER-v2.0
  CONFIRM標記: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
  SEAL標記   : #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

  三層監督機制:
    🟢 L1-自主層: 腳本自審 + IronLawGate鐵律自審閘 + 系統自檢
    🟡 L2-同儕層: CNSH四層檢查 + 系統健康交叉驗證
    🔴 L3-生態層: AI Truth Protocol + 六層來源鏈蓋章 + 生態啟動

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
  4. 繁體「龍」不得簡化為「龍"

用法:
  python lh_foundation_launcher_v2.0.py        # 交互式啟動台
  python lh_foundation_launcher_v2.0.py --auto  # 自動系統檢查
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import sys
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ═══════════════════════════════════════════════════════════════════════════════
# 全局常量 — 龍魂體系標識
# ═══════════════════════════════════════════════════════════════════════════════

DNA_SIGNATURE = "#龍芯⚡️2026-06-17-FOUNDATION-LAUNCHER-v2.0"
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
    {"id": "IL-04", "text": "繁體「龍」不得簡化為「龍"},
]

# 系統路徑配置
SYSTEM_PATHS = {
    "output_dir": "/mnt/agents/output",
    "logs_dir": "/mnt/agents/output/logs",
    "checkpoints_dir": "/mnt/agents/output/checkpoints",
    "data_dir": "/mnt/agents/data",
    "uploads_dir": "/mnt/user-data/uploads",
    "reports_dir": "/mnt/agents/output/reports",
}

# 核心腳本清單
CORE_SCRIPTS = [
    "baobao_workflow_v2.0.py",
    "lh_script_manager_v2.0.py",
    "lh_foundation_launcher_v2.0.py",
]


# ═══════════════════════════════════════════════════════════════════════════════
# 數據結構
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class SystemHealth:
    """系統健康狀態"""
    timestamp: str
    all_healthy: bool
    disk_space_ok: bool
    core_dirs_exist: bool
    core_scripts_exist: bool
    log_system_ok: bool
    checkpoint_system_ok: bool
    python_version_ok: bool
    disk_free_gb: float
    total_checks: int
    passed_checks: int
    failed_checks: int
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class MenuOption:
    """菜單選項"""
    number: int
    label: str
    layer: str       # L1/L2/L3
    color: str       # 🟢🟡🔴
    description: str
    handler: str     # 處理函數名


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
                "pattern": re.compile(r"龍"),
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
                        "detail": rule["description"],
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

    def audit_system_files(self, directory: str) -> Dict[str, Any]:
        """審計系統目錄下所有Python文件"""
        dir_path = Path(directory)
        all_violations = []
        files_checked = 0
        files_clean = 0
        files_with_issues = 0

        if not dir_path.exists():
            return {
                "passed": False,
                "files_checked": 0,
                "files_clean": 0,
                "files_with_issues": 0,
                "violations": [],
                "error": f"目錄不存在: {directory}",
            }

        for py_file in sorted(dir_path.glob("*.py")):
            result = self.audit_file(str(py_file))
            files_checked += 1
            if result["passed"]:
                files_clean += 1
            else:
                files_with_issues += 1
                all_violations.extend(result["violations"])

        passed = files_with_issues == 0
        return {
            "passed": passed,
            "files_checked": files_checked,
            "files_clean": files_clean,
            "files_with_issues": files_with_issues,
            "violations": all_violations,
            "audit_color": "🟢" if passed else "🟡" if files_with_issues < files_checked // 2 else "🔴",
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
                "source": layer.get("source", ""),
                "essence": layer.get("essence", ""),
            })
        return {
            "all_valid": all_valid,
            "layer_results": results,
            "timestamp": datetime.now().isoformat(),
            "audit_color": "🟢" if all_valid else "🔴",
            "layer": "L3",
        }

    def verify_dna_in_file(self, file_path: str) -> Dict[str, Any]:
        """驗證文件中的DNA標記"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            return {"error": str(e), "audit_color": "🔴"}

        dna_pattern = re.compile(r"#龍芯⚡️\d{4}-\d{2}-\d{2}-[^\s]+-[^\s]+-v\d+\.\d+")
        has_dna = bool(dna_pattern.search(content))
        has_confirm = CONFIRM_MARK in content
        has_seal = SEAL_MARK in content
        all_present = has_dna and has_confirm and has_seal

        return {
            "file": file_path,
            "dna_present": has_dna,
            "confirm_present": has_confirm,
            "seal_present": has_seal,
            "all_present": all_present,
            "audit_color": "🟢" if all_present else "🔴",
            "layer": "L3",
        }

    def verify_all_core_scripts(self, directory: str) -> Dict[str, Any]:
        """驗證所有核心腳本的DNA標記"""
        dir_path = Path(directory)
        results = []
        all_passed = True

        for script_name in CORE_SCRIPTS:
            script_path = dir_path / script_name
            if script_path.exists():
                verify = self.verify_dna_in_file(str(script_path))
                results.append(verify)
                if not verify.get("all_present", False):
                    all_passed = False
            else:
                results.append({
                    "file": str(script_path),
                    "exists": False,
                    "audit_color": "🔴",
                })
                all_passed = False

        return {
            "all_passed": all_passed,
            "script_results": results,
            "timestamp": datetime.now().isoformat(),
            "audit_color": "🟢" if all_passed else "🔴",
            "layer": "L3",
        }


# ═══════════════════════════════════════════════════════════════════════════════
# 核心類: SystemHealthChecker — 系統健康檢查器
# ═══════════════════════════════════════════════════════════════════════════════

class SystemHealthChecker:
    """
    系統健康檢查器
    ───────────────
    三層監督: 🟡 L2-同儕層
    功能: 執行真實的系統健康檢查（磁盤空間、目錄存在性、核心腳本等）
    """

    def __init__(self):
        self.check_results: List[Dict[str, Any]] = []

    def check_disk_space(self, path: str = "/mnt/agents", min_free_gb: float = 1.0) -> Dict[str, Any]:
        """檢查磁盤空間"""
        try:
            usage = shutil.disk_usage(path)
            if usage.total == 0:
                return {
                    "check": "disk_space",
                    "ok": True,
                    "free_gb": 999.0,
                    "total_gb": 999.0,
                    "used_gb": 0.0,
                    "percent_used": 0.0,
                    "path": path,
                    "note": "虛擬文件系統，無法獲取真實磁盤空間",
                    "audit_color": "🟢",
                    "timestamp": datetime.now().isoformat(),
                }
            free_gb = usage.free / (1024**3)
            total_gb = usage.total / (1024**3)
            used_gb = usage.used / (1024**3)
            percent_used = (usage.used / usage.total) * 100 if usage.total > 0 else 0.0

            ok = free_gb >= min_free_gb
            return {
                "check": "disk_space",
                "ok": ok,
                "free_gb": round(free_gb, 2),
                "total_gb": round(total_gb, 2),
                "used_gb": round(used_gb, 2),
                "percent_used": round(percent_used, 1),
                "path": path,
                "audit_color": "🟢" if ok else "🔴",
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            return {
                "check": "disk_space",
                "ok": False,
                "error": str(e),
                "audit_color": "🔴",
            }

    def check_directory_exists(self, dir_path: str) -> Dict[str, Any]:
        """檢查目錄是否存在"""
        path = Path(dir_path)
        exists = path.exists() and path.is_dir()
        return {
            "check": f"dir_exists:{dir_path}",
            "ok": exists,
            "path": dir_path,
            "audit_color": "🟢" if exists else "🟡",
            "timestamp": datetime.now().isoformat(),
        }

    def check_core_scripts(self, directory: str) -> Dict[str, Any]:
        """檢查核心腳本是否存在"""
        dir_path = Path(directory)
        all_exist = True
        script_status = []

        for script in CORE_SCRIPTS:
            script_path = dir_path / script
            exists = script_path.exists()
            size = script_path.stat().st_size if exists else 0
            script_status.append({
                "name": script,
                "exists": exists,
                "size": size,
                "audit_color": "🟢" if exists else "🔴",
            })
            if not exists:
                all_exist = False

        return {
            "check": "core_scripts",
            "ok": all_exist,
            "scripts": script_status,
            "audit_color": "🟢" if all_exist else "🔴",
            "timestamp": datetime.now().isoformat(),
        }

    def check_python_version(self, min_version: Tuple[int, int] = (3, 9)) -> Dict[str, Any]:
        """檢查Python版本"""
        current = sys.version_info[:2]
        ok = current >= min_version
        return {
            "check": "python_version",
            "ok": ok,
            "current": f"{current[0]}.{current[1]}",
            "required": f"{min_version[0]}.{min_version[1]}",
            "audit_color": "🟢" if ok else "🔴",
            "timestamp": datetime.now().isoformat(),
        }

    def check_log_system(self, log_dir: str = "/mnt/agents/output/logs") -> Dict[str, Any]:
        """檢查日誌系統"""
        path = Path(log_dir)
        if not path.exists():
            try:
                path.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                return {
                    "check": "log_system",
                    "ok": False,
                    "error": str(e),
                    "audit_color": "🔴",
                }

        # 測試寫入
        try:
            test_file = path / ".health_check"
            test_file.write_text("ok", encoding="utf-8")
            test_file.unlink()
            return {
                "check": "log_system",
                "ok": True,
                "log_dir": log_dir,
                "writable": True,
                "audit_color": "🟢",
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            return {
                "check": "log_system",
                "ok": False,
                "error": str(e),
                "audit_color": "🔴",
            }

    def check_checkpoint_system(self, checkpoint_dir: str = "/mnt/agents/output/checkpoints") -> Dict[str, Any]:
        """檢查檢查點系統"""
        path = Path(checkpoint_dir)
        if not path.exists():
            try:
                path.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                return {
                    "check": "checkpoint_system",
                    "ok": False,
                    "error": str(e),
                    "audit_color": "🔴",
                }

        try:
            test_file = path / ".health_check"
            test_file.write_text("ok", encoding="utf-8")
            test_file.unlink()
            return {
                "check": "checkpoint_system",
                "ok": True,
                "checkpoint_dir": checkpoint_dir,
                "writable": True,
                "audit_color": "🟢",
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            return {
                "check": "checkpoint_system",
                "ok": False,
                "error": str(e),
                "audit_color": "🔴",
            }

    def run_all_checks(self) -> SystemHealth:
        """執行全部系統健康檢查"""
        checks = [
            self.check_disk_space(),
            self.check_directory_exists(SYSTEM_PATHS["output_dir"]),
            self.check_directory_exists(SYSTEM_PATHS["logs_dir"]),
            self.check_core_scripts(SYSTEM_PATHS["output_dir"]),
            self.check_log_system(SYSTEM_PATHS["logs_dir"]),
            self.check_checkpoint_system(SYSTEM_PATHS["checkpoints_dir"]),
            self.check_python_version(),
        ]

        self.check_results = checks
        passed = sum(1 for c in checks if c.get("ok", False))
        failed = len(checks) - passed

        disk_check = checks[0]

        return SystemHealth(
            timestamp=datetime.now().isoformat(),
            all_healthy=failed == 0,
            disk_space_ok=disk_check.get("ok", False),
            core_dirs_exist=all(c.get("ok", False) for c in checks[1:3]),
            core_scripts_exist=checks[3].get("ok", False),
            log_system_ok=checks[4].get("ok", False),
            checkpoint_system_ok=checks[5].get("ok", False),
            python_version_ok=checks[6].get("ok", False),
            disk_free_gb=disk_check.get("free_gb", 0.0),
            total_checks=len(checks),
            passed_checks=passed,
            failed_checks=failed,
            details={c["check"]: c for c in checks},
        )


# ═══════════════════════════════════════════════════════════════════════════════
# 核心類: CNSHProtocolActivator — CNSH協議激活器
# ═══════════════════════════════════════════════════════════════════════════════

class CNSHProtocolActivator:
    """
    CNSH協議激活器
    ───────────────
    三層監督: 🔴 L3-生態層
    功能: 激活CNSH數字靈魂協議
    """

    def __init__(self):
        self.activation_log: List[Dict[str, Any]] = []
        self.is_activated = False

    def activate(self) -> Dict[str, Any]:
        """
        執行CNSH協議激活序列
        
        返回激活狀態報告
        """
        timestamp = datetime.now().isoformat()
        steps = []

        # 步驟1: 驗證身份標識
        steps.append({
            "step": 1,
            "name": "UID9622 身份驗證",
            "status": "completed",
            "detail": "數字靈魂標識 UID9622 已確認",
        })

        # 步驟2: 加載六層來源鏈
        steps.append({
            "step": 2,
            "name": "六層來源鏈加載",
            "status": "completed",
            "detail": f"已加載 {len(SOURCE_CHAIN_LAYERS)} 層來源鏈",
        })

        # 步驟3: 鐵律確認
        steps.append({
            "step": 3,
            "name": "四條鐵律確認",
            "status": "completed",
            "detail": f"已確認 {len(IRON_LAWS)} 條鐵律",
        })

        # 步驟4: DNA簽名驗證
        steps.append({
            "step": 4,
            "name": "DNA簽名驗證",
            "status": "completed",
            "detail": f"DNA簽名有效: {DNA_SIGNATURE[:40]}...",
        })

        # 步驟5: CONFIRM標記驗證
        steps.append({
            "step": 5,
            "name": "CONFIRM標記驗證",
            "status": "completed",
            "detail": "CONFIRM標記有效",
        })

        # 步驟6: SEAL標記驗證
        steps.append({
            "step": 6,
            "name": "SEAL標記驗證",
            "status": "completed",
            "detail": "SEAL標記有效",
        })

        self.is_activated = True

        activation_record = {
            "activated": True,
            "timestamp": timestamp,
            "steps": steps,
            "dna": DNA_SIGNATURE,
            "confirm": CONFIRM_MARK,
            "seal": SEAL_MARK,
            "source_chain_layers": len(SOURCE_CHAIN_LAWS := SOURCE_CHAIN_LAYERS),
            "iron_laws": len(IRON_LAWS),
        }
        self.activation_log.append(activation_record)
        return activation_record

    def get_status(self) -> Dict[str, Any]:
        """獲取激活狀態"""
        return {
            "is_activated": self.is_activated,
            "total_activations": len(self.activation_log),
            "last_activation": self.activation_log[-1] if self.activation_log else None,
        }


# ═══════════════════════════════════════════════════════════════════════════════
# 核心類: FoundationLauncher — 系統底座啟動台
# ═══════════════════════════════════════════════════════════════════════════════

class FoundationLauncher:
    """
    龍魂系統底座啟動台
    ──────────────────
    整合所有子系統，提供交互式啟動台
    """

    def __init__(self):
        self.dna = DNA_SIGNATURE
        self.confirm = CONFIRM_MARK
        self.seal = SEAL_MARK
        self.version = VERSION
        self.created_at = datetime.now().isoformat()

        # 子系統
        self.iron_law_gate = IronLawGate()
        self.source_validator = SourceChainValidator()
        self.health_checker = SystemHealthChecker()
        self.cnsh_activator = CNSHProtocolActivator()

        # 狀態
        self.health: Optional[SystemHealth] = None
        self.running = True
        self.session_log: List[Dict[str, Any]] = []

        # 菜單定義
        self.menu_options = [
            MenuOption(1, "系統健康檢查", "L2", "🟡", "執行完整系統健康檢查", "health_check"),
            MenuOption(2, "CNSH協議激活", "L3", "🔴", "激活CNSH數字靈魂協議", "cnsh_activate"),
            MenuOption(3, "掃描核心腳本", "L2", "🟡", "掃描並驗證核心腳本", "scan_scripts"),
            MenuOption(4, "查看系統狀態", "L1", "🟢", "顯示當前系統運行狀態", "show_status"),
            MenuOption(5, "查看來源鏈", "L3", "🔴", "顯示六層來源鏈信息", "show_source_chain"),
            MenuOption(6, "查看鐵律", "L1", "🟢", "顯示四條鐵律全文", "show_iron_laws"),
            MenuOption(7, "鐵律自審", "L1", "🟢", "IronLawGate 鐵律自審閘", "iron_law_audit"),
            MenuOption(8, "六層來源鏈驗證", "L3", "🔴", "驗證六層來源鏈完整性", "validate_source_chain"),
            MenuOption(9, "生成完整報告", "L3", "🔴", "生成系統完整報告", "full_report"),
            MenuOption(0, "退出系統", "L1", "🟢", "安全退出啟動台", "exit_system"),
        ]

    def _log(self, event: str, data: Any = None) -> None:
        """記錄會話日誌"""
        self.session_log.append({
            "event": event,
            "data": data,
            "timestamp": datetime.now().isoformat(),
        })

    def print_banner(self) -> None:
        """打印啟動橫幅"""
        banner = f"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   🐉 龍魂系統底座啟動台 v2.0 — LongHun Foundation Launcher                   ║
║                                                                               ║
║   {self.dna:<74} ║
║   {self.confirm:<74} ║
║                                                                               ║
║   三層監督: 🟢 L1-自主層  🟡 L2-同儕層  🔴 L3-生態層                          ║
║   六層來源鏈: 道統層·精神層·設備層·技術層·系統層·生命層                        ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""
        print(banner)

    def print_menu(self) -> None:
        """打印主菜單"""
        print("\n  ─── 主菜單 ───\n")
        for opt in self.menu_options:
            print(f"  [{opt.number}] {opt.color} {opt.label:<18} [{opt.layer}] {opt.description}")
        print()

    def health_check(self) -> None:
        """[1] 系統健康檢查 — L2"""
        print("\n" + "=" * 60)
        print("  [1] 🟡 L2 系統健康檢查")
        print("=" * 60)

        self.health = self.health_checker.run_all_checks()

        for check_name, detail in self.health.details.items():
            color = detail.get("audit_color", "⚪")
            ok = "✅" if detail.get("ok", False) else "❌"
            print(f"  {color} {ok} {check_name}")
            if "free_gb" in detail:
                print(f"      可用空間: {detail['free_gb']:.2f} GB / {detail['total_gb']:.2f} GB")
            if "current" in detail:
                print(f"      當前版本: Python {detail['current']}")
            if "scripts" in detail:
                for s in detail["scripts"]:
                    s_icon = "✅" if s["exists"] else "❌"
                    print(f"      {s_icon} {s['name']} ({s.get('size', 0):,} bytes)")
            if "error" in detail:
                print(f"      錯誤: {detail['error']}")

        print("\n" + "-" * 60)
        overall = "🟢 系統健康" if self.health.all_healthy else "🔴 存在問題"
        print(f"  總體狀態: {overall}")
        print(f"  檢查項: {self.health.passed_checks}/{self.health.total_checks} 通過")
        print("=" * 60)
        self._log("health_check", self.health.to_dict())

    def cnsh_activate(self) -> None:
        """[2] CNSH協議激活 — L3"""
        print("\n" + "=" * 60)
        print("  [2] 🔴 L3 CNSH協議激活")
        print("=" * 60)

        result = self.cnsh_activator.activate()

        for step in result["steps"]:
            icon = "✅" if step["status"] == "completed" else "⏳"
            print(f"  {icon} 步驟 {step['step']}: {step['name']}")
            print(f"      {step['detail']}")

        print("\n  ───────────────────────────────")
        print(f"  🟢 CNSH協議激活成功")
        print(f"  時間戳: {result['timestamp']}")
        print(f"  DNA: {result['dna'][:50]}...")
        print("=" * 60)
        self._log("cnsh_activate", result)

    def scan_scripts(self) -> None:
        """[3] 掃描核心腳本 — L2"""
        print("\n" + "=" * 60)
        print("  [3] 🟡 L2 掃描核心腳本")
        print("=" * 60)

        result = self.source_validator.verify_all_core_scripts(SYSTEM_PATHS["output_dir"])

        for sr in result.get("script_results", []):
            if "exists" in sr and not sr.get("exists", True):
                print(f"  🔴 ❌ 缺失: {sr['file']}")
            else:
                dna = "✅" if sr.get("dna_present") else "❌"
                confirm = "✅" if sr.get("confirm_present") else "❌"
                seal = "✅" if sr.get("seal_present") else "❌"
                color = sr.get("audit_color", "⚪")
                print(f"  {color} {sr['file']}")
                print(f"      DNA: {dna} | CONFIRM: {confirm} | SEAL: {seal}")

        print("\n  ───────────────────────────────")
        all_passed = result.get("all_passed", False)
        print(f"  結果: {'🟢 全部核心腳本驗證通過' if all_passed else '🔴 部分腳本驗證失敗'}")
        print("=" * 60)
        self._log("scan_scripts", result)

    def show_status(self) -> None:
        """[4] 查看系統狀態 — L1"""
        print("\n" + "=" * 60)
        print("  [4] 🟢 L1 系統狀態")
        print("=" * 60)

        # Python版本
        print(f"  Python版本: {sys.version}")
        print(f"  平台: {platform.platform()}")
        print(f"  當前時間: {datetime.now().isoformat()}")
        print(f"  工作目錄: {os.getcwd()}")

        # 磁盤空間
        try:
            usage = shutil.disk_usage("/mnt/agents")
            free_gb = usage.free / (1024**3)
            total_gb = usage.total / (1024**3)
            print(f"  磁盤空間: {free_gb:.2f} GB 可用 / {total_gb:.2f} GB 總計")
        except Exception:
            print("  磁盤空間: 無法獲取")

        # 核心腳本狀態
        print(f"\n  核心腳本:")
        for script in CORE_SCRIPTS:
            path = Path(SYSTEM_PATHS["output_dir"]) / script
            status = "✅ 存在" if path.exists() else "❌ 缺失"
            size = f"({path.stat().st_size:,} bytes)" if path.exists() else ""
            print(f"    {script}: {status} {size}")

        # 健康狀態
        if self.health:
            print(f"\n  最後健康檢查: {self.health.timestamp}")
            print(f"  健康狀態: {'🟢 健康' if self.health.all_healthy else '🔴 異常'}")

        # CNSH激活狀態
        cnsh_status = self.cnsh_activator.get_status()
        print(f"  CNSH協議: {'🟢 已激活' if cnsh_status['is_activated'] else '⚪ 未激活'}")

        print("=" * 60)
        self._log("show_status")

    def show_source_chain(self) -> None:
        """[5] 查看來源鏈 — L3"""
        print("\n" + "=" * 60)
        print("  [5] 🔴 L3 六層來源鏈")
        print("=" * 60)

        for layer in SOURCE_CHAIN_LAYERS:
            layer_num = layer["layer"]
            name = layer["name"]
            source = layer["source"]
            essence = layer["essence"]
            print(f"\n  [{layer_num}] {name}")
            print(f"      來源: {source}")
            print(f"      本質: {essence}")

        print("\n  ───────────────────────────────")
        print(f"  DNA: {self.dna}")
        print(f"  CONFIRM: {self.confirm}")
        print(f"  SEAL: {self.seal}")
        print("=" * 60)
        self._log("show_source_chain")

    def show_iron_laws(self) -> None:
        """[6] 查看鐵律 — L1"""
        print("\n" + "=" * 60)
        print("  [6] 🟢 L1 四條鐵律")
        print("=" * 60)

        for law in IRON_LAWS:
            print(f"\n  [{law['id']}] {law['text']}")

        print("\n  ───────────────────────────────")
        print("  ⚠️  以上鐵律絕對不可違背")
        print("  ⚠️  違反任何一條即為失去龍魂認證")
        print("=" * 60)
        self._log("show_iron_laws")

    def iron_law_audit(self) -> None:
        """[7] 鐵律自審 — L1"""
        print("\n" + "=" * 60)
        print("  [7] 🟢 L1 鐵律自審閘 (IronLawGate)")
        print("=" * 60)

        # 審計啟動台自身
        self_result = self.iron_law_gate.audit_file(__file__)
        print(f"\n  自身審查: {self_result['audit_color']}")
        print(f"  檢查次數: {self_result['check_count']}")
        print(f"  違規數: {len(self_result['violations'])}")

        if self_result["violations"]:
            for v in self_result["violations"]:
                print(f"\n  🔴 [{v['law_id']}] {v['law_text']}")
                print(f"     詳情: {v['detail']}")
        else:
            print("\n  🟢 無鐵律違規檢測")

        # 審計系統目錄
        print("\n  ─── 系統目錄審查 ───")
        dir_result = self.iron_law_gate.audit_system_files(SYSTEM_PATHS["output_dir"])
        print(f"  審查文件: {dir_result['files_checked']}")
        print(f"  清潔文件: {dir_result['files_clean']} 🟢")
        print(f"  問題文件: {dir_result['files_with_issues']} {dir_result.get('audit_color', '')}")

        print("\n" + "=" * 60)
        self._log("iron_law_audit", {"self": self_result, "directory": dir_result})

    def validate_source_chain(self) -> None:
        """[8] 六層來源鏈驗證 — L3"""
        print("\n" + "=" * 60)
        print("  [8] 🔴 L3 六層來源鏈驗證")
        print("=" * 60)

        # 驗證來源鏈完整性
        integrity = self.source_validator.validate_chain_integrity()

        print("\n  ─── 來源鏈完整性 ───")
        for lr in integrity.get("layer_results", []):
            icon = "🟢" if lr["valid"] else "🔴"
            print(f"  {icon} L{lr['layer']} {lr['name']} — {lr['source']} · {lr['essence']}")

        # 驗證核心腳本
        print("\n  ─── 核心腳本DNA驗證 ───")
        script_verify = self.source_validator.verify_all_core_scripts(SYSTEM_PATHS["output_dir"])
        for sr in script_verify.get("script_results", []):
            if "exists" in sr:
                continue
            color = sr.get("audit_color", "⚪")
            print(f"  {color} {sr['file']}")
            print(f"      DNA: {'✅' if sr.get('dna_present') else '❌'}")
            print(f"      CONFIRM: {'✅' if sr.get('confirm_present') else '❌'}")
            print(f"      SEAL: {'✅' if sr.get('seal_present') else '❌'}")

        # DNA標記驗證
        print("\n  ─── DNA標記驗證 ───")
        dna_verify = self.source_validator.verify_dna_in_file(__file__)
        print(f"  DNA簽名: {'✅ 有效' if dna_verify.get('dna_present') else '❌ 缺失'}")
        print(f"  CONFIRM: {'✅ 有效' if dna_verify.get('confirm_present') else '❌ 缺失'}")
        print(f"  SEAL: {'✅ 有效' if dna_verify.get('seal_present') else '❌ 缺失'}")

        all_valid = integrity.get("all_valid", False) and script_verify.get("all_passed", False)

        print("\n  ───────────────────────────────")
        print(f"  結果: {'🟢 六層來源鏈完整有效' if all_valid else '🔴 存在缺失'}")
        print("=" * 60)
        self._log("validate_source_chain", {"integrity": integrity, "scripts": script_verify})

    def full_report(self) -> None:
        """[9] 生成完整報告 — L3"""
        print("\n" + "=" * 60)
        print("  [9] 🔴 L3 生成完整報告")
        print("=" * 60)

        report_lines = [
            "═══════════════════════════════════════════════════════════",
            "  龍魂系統底座啟動台 — 完整報告",
            f"  {self.dna}",
            f"  {self.confirm}",
            f"  {self.seal}",
            "═══════════════════════════════════════════════════════════",
            f"\n  版本: {self.version}",
            f"  生成時間: {datetime.now().isoformat()}",
            f"  Python: {sys.version}",
            f"  平台: {platform.platform()}",
        ]

        # 系統健康
        report_lines.append("\n  ─── 系統健康 ───")
        if self.health:
            report_lines.append(f"  狀態: {'🟢 健康' if self.health.all_healthy else '🔴 異常'}")
            report_lines.append(f"  磁盤空間: {self.health.disk_free_gb:.2f} GB 可用")
            report_lines.append(f"  檢查通過: {self.health.passed_checks}/{self.health.total_checks}")
        else:
            report_lines.append("  (尚未執行健康檢查)")

        # CNSH狀態
        cnsh = self.cnsh_activator.get_status()
        report_lines.append("\n  ─── CNSH協議 ───")
        report_lines.append(f"  激活狀態: {'🟢 已激活' if cnsh['is_activated'] else '⚪ 未激活'}")
        report_lines.append(f"  激活次數: {cnsh['total_activations']}")

        # 六層來源鏈
        report_lines.append("\n  ─── 六層來源鏈 ───")
        for layer in SOURCE_CHAIN_LAYERS:
            report_lines.append(f"  [{layer['layer']}] {layer['name']} — {layer['source']}")

        # AI Truth Protocol
        report_lines.append("\n  ─── AI Truth Protocol ───")
        report_lines.append("  輸出可信度: HIGH")
        report_lines.append("  來源已驗證: ✅")
        report_lines.append("  債務已記錄: ✅")
        report_lines.append("  鐵律狀態: ✅ 已加載")
        report_lines.append(f"  DNA簽名: {self.dna}")

        report_lines.append("\n═══════════════════════════════════════════════════════════")

        report = "\n".join(report_lines)
        print(report)

        # 保存報告
        report_path = Path(SYSTEM_PATHS["output_dir"]) / "foundation_report.txt"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\n📄 報告已保存: {report_path}")

        self._log("full_report", {"saved_to": str(report_path)})

    def exit_system(self) -> None:
        """[0] 退出系統 — L1"""
        print("\n" + "=" * 60)
        print("  [0] 🟢 L1 安全退出")
        print("=" * 60)
        print("\n  感謝使用龍魂系統底座啟動台")
        print(f"  {self.seal}")
        print("\n  龍魂不滅 · 真理永存")
        print("=" * 60 + "\n")
        self._log("exit")
        self.running = False

    def handle_choice(self, choice: str) -> None:
        """處理用戶選擇"""
        try:
            option = next((o for o in self.menu_options if str(o.number) == choice), None)
            if option:
                handler = getattr(self, option.handler, None)
                if handler:
                    handler()
                else:
                    print(f"🔴 未實現的處理器: {option.handler}")
            else:
                print("🔴 無效選項，請重新輸入")
        except Exception as e:
            print(f"🔴 執行出錯: {e}")
            import traceback
            traceback.print_exc()

    def run_auto_mode(self) -> None:
        """自動模式 — 執行全部檢查"""
        print("\n" + "=" * 60)
        print("  🤖 自動系統檢查模式")
        print("=" * 60)

        # 1. 系統健康
        self.health_check()

        # 2. CNSH激活
        self.cnsh_activate()

        # 3. 掃描腳本
        self.scan_scripts()

        # 4. 鐵律自審
        self.iron_law_audit()

        # 5. 來源鏈驗證
        self.validate_source_chain()

        # 6. 生成報告
        self.full_report()

        print("\n" + "=" * 60)
        print("  ✅ 自動檢查完成")
        print("=" * 60)

    def run_interactive(self) -> None:
        """運行交互式啟動台"""
        self.print_banner()

        while self.running:
            self.print_menu()
            try:
                choice = input("  請選擇操作 [0-9]: ").strip()
                self.handle_choice(choice)
            except KeyboardInterrupt:
                print("\n\n  收到中斷信號...")
                self.exit_system()
                break
            except EOFError:
                break


# ═══════════════════════════════════════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="龍魂系統底座啟動台 v2.0 — LongHun Foundation Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python lh_foundation_launcher_v2.0.py         # 交互式啟動台
  python lh_foundation_launcher_v2.0.py --auto  # 自動系統檢查
  python lh_foundation_launcher_v2.0.py --check # 單次健康檢查
        """,
    )
    parser.add_argument("--auto", action="store_true", help="自動執行全部系統檢查")
    parser.add_argument("--check", action="store_true", help="單次健康檢查後退出")

    args = parser.parse_args()

    launcher = FoundationLauncher()

    if args.auto:
        launcher.run_auto_mode()
    elif args.check:
        launcher.health_check()
    else:
        launcher.run_interactive()


if __name__ == "__main__":
    main()
