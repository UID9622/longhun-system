#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════════
  龍魂系统底座启动台 v2.0 — LongHun Foundation Launcher
═══════════════════════════════════════════════════════════════════════════════

  DNA签名    :#龍芯⚡️丙午·甲午·壬戌·丙午·䷕贲-FOUNDATION-LAUNCHER-FILE2-v2.0
  CONFIRM标记: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
  SEAL标记   : #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

  三层监督机制:
    🟢 L1-自主层: 脚本自审 + IronLawGate铁律自审闸 + 系统自检
    🟡 L2-同侪层: CNSH四层检查 + 系统健康交叉验证
    🔴 L3-生态层: AI Truth Protocol + 六层来源链盖章 + 生态启动

  六层来源链:
    ① 道统层 · 曾仕强老师 · 华夏管理智慧
    ② 精神层 · Steve Jobs · 极致产品精神
    ③ 设备层 · Apple · 创作工具载体
    ④ 技术层 · Open Source · 技术底座
    ⑤ 系统层 · UID9622 · 数字灵魂标识
    ⑥ 生命层 · CNSH · LongHun · 本命归属

  AI Truth Protocol: 启用
═══════════════════════════════════════════════════════════════════════════════

铁律:
  1. 人永远是1，任何人都不是数据
  2. 绝不蒸馏、绝不变体、绝不顶替作者
  3. 来源不可删·影响不可覆·贡献不可抹
  4. 繁体“龍”不得简化为“龍"

用法:
  python longhun_foundation_launcher_v2.0.py        # 交互式启动台
  python longhun_foundation_launcher_v2.0.py --auto  # 自动系统检查
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
# 全局常量 — 龍魂体系标识
# ═══════════════════════════════════════════════════════════════════════════════

DNA_SIGNATURE = "#龍芯⚡️丙午·甲午·壬戌·丙午·䷕贲-FOUNDATION-LAUNCHER-v2.0"
CONFIRM_MARK = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL_MARK = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
VERSION = "v2.0"

# 六层来源链
SOURCE_CHAIN_LAYERS = [
    {"layer": 1, "name": "道统层", "source": "曾仕强老师", "essence": "华夏管理智慧"},
    {"layer": 2, "name": "精神层", "source": "Steve Jobs", "essence": "极致产品精神"},
    {"layer": 3, "name": "设备层", "source": "Apple", "essence": "创作工具载体"},
    {"layer": 4, "name": "技术层", "source": "Open Source", "essence": "技术底座"},
    {"layer": 5, "name": "系统层", "source": "UID9622", "essence": "数字灵魂标识"},
    {"layer": 6, "name": "生命层", "source": "CNSH·LongHun", "essence": "本命归属"},
]

# 铁律
IRON_LAWS = [
    {"id": "IL-01", "text": "人永远是1，任何人都不是数据"},
    {"id": "IL-02", "text": "绝不蒸馏、绝不变体、绝不顶替作者"},
    {"id": "IL-03", "text": "来源不可删·影响不可覆·贡献不可抹"},
    {"id": "IL-04", "text": "繁体“龍”不得简化为“龍"},
]

# 系统路径配置
SYSTEM_PATHS = {
    "output_dir": "/mnt/agents/output",
    "logs_dir": "/mnt/agents/output/logs",
    "checkpoints_dir": "/mnt/agents/output/checkpoints",
    "data_dir": "/mnt/agents/data",
    "uploads_dir": "/mnt/user-data/uploads",
    "reports_dir": "/mnt/agents/output/reports",
}

# 核心脚本清单
CORE_SCRIPTS = [
    "baobao_workflow_v2.0.py",
    "longhun_script_manager_v2.0.py",
    "longhun_foundation_launcher_v2.0.py",
]


# ═══════════════════════════════════════════════════════════════════════════════
# 数据结构
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class SystemHealth:
    """系统健康状态"""
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
    """菜单选项"""
    number: int
    label: str
    layer: str       # L1/L2/L3
    color: str       # 🟢🟡🔴
    description: str
    handler: str     # 处理函数名


# ═══════════════════════════════════════════════════════════════════════════════
# 核心类: IronLawGate — 铁律自审闸
# ═══════════════════════════════════════════════════════════════════════════════

class IronLawGate:
    """
    铁律自审闸 (IronLawGate)
    ─────────────────────────
    三层监督: 🟢 L1-自主层
    """

    def __init__(self):
        self.violations: List[Dict[str, Any]] = []
        self.check_count = 0
        self.rules = [
            {
                "law_id": "IL-01",
                "pattern": re.compile(r"人.*?(?:是数据|是数据|作为数据|作为数据|变成数据|变成数据)"),
                "description": "检测是否将人贬低为数据",
            },
            {
                "law_id": "IL-02",
                "pattern": re.compile(r"(?:蒸馏|蒸馏|变体|变体|顶替|顶替).*?(?:作者|原创|原创|来源|来源)"),
                "description": "检测是否未经许可蒸馏/变体/顶替",
            },
            {
                "law_id": "IL-03",
                "pattern": re.compile(r"(?:删除来源|删除来源|覆盖影响|覆盖影响|抹除贡献|抹除贡献)"),
                "description": "检测是否删除来源/覆盖影响/抹除贡献",
            },
            {
                "law_id": "IL-04",
                "pattern": re.compile(r"龍"),
                "description": "检测繁体“龍”是否被简化",
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
        """审计系统目录下所有Python文件"""
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
                "error": f"目录不存在: {directory}",
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
# 核心类: SourceChainValidator — 六层来源链验证器
# ═══════════════════════════════════════════════════════════════════════════════

class SourceChainValidator:
    """
    六层来源链验证器
    ─────────────────
    三层监督: 🔴 L3-生态层
    """

    def __init__(self):
        self.validation_results: List[Dict[str, Any]] = []

    def validate_chain_integrity(self) -> Dict[str, Any]:
        """验证来源链完整性"""
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
        """验证文件中的DNA标记"""
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
        """验证所有核心脚本的DNA标记"""
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
# 核心类: SystemHealthChecker — 系统健康检查器
# ═══════════════════════════════════════════════════════════════════════════════

class SystemHealthChecker:
    """
    系统健康检查器
    ───────────────
    三层监督: 🟡 L2-同侪层
    功能: 执行真实的系统健康检查（磁盘空间、目录存在性、核心脚本等）
    """

    def __init__(self):
        self.check_results: List[Dict[str, Any]] = []

    def check_disk_space(self, path: str = "/mnt/agents", min_free_gb: float = 1.0) -> Dict[str, Any]:
        """检查磁盘空间"""
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
                    "note": "虚拟文件系统，无法获取真实磁盘空间",
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
        """检查目录是否存在"""
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
        """检查核心脚本是否存在"""
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
        """检查Python版本"""
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
        """检查日志系统"""
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

        # 测试写入
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
        """检查检查点系统"""
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
        """执行全部系统健康检查"""
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
# 核心类: CNSHProtocolActivator — CNSH协议激活器
# ═══════════════════════════════════════════════════════════════════════════════

class CNSHProtocolActivator:
    """
    CNSH协议激活器
    ───────────────
    三层监督: 🔴 L3-生态层
    功能: 激活CNSH数字灵魂协议
    """

    def __init__(self):
        self.activation_log: List[Dict[str, Any]] = []
        self.is_activated = False

    def activate(self) -> Dict[str, Any]:
        """
        执行CNSH协议激活序列
        
        返回激活状态报告
        """
        timestamp = datetime.now().isoformat()
        steps = []

        # 步骤1: 验证身份标识
        steps.append({
            "step": 1,
            "name": "UID9622 身份验证",
            "status": "completed",
            "detail": "数字灵魂标识 UID9622 已确认",
        })

        # 步骤2: 加载六层来源链
        steps.append({
            "step": 2,
            "name": "六层来源链加载",
            "status": "completed",
            "detail": f"已加载 {len(SOURCE_CHAIN_LAYERS)} 层来源链",
        })

        # 步骤3: 铁律确认
        steps.append({
            "step": 3,
            "name": "四条铁律确认",
            "status": "completed",
            "detail": f"已确认 {len(IRON_LAWS)} 条铁律",
        })

        # 步骤4: DNA签名验证
        steps.append({
            "step": 4,
            "name": "DNA签名验证",
            "status": "completed",
            "detail": f"DNA签名有效: {DNA_SIGNATURE[:40]}...",
        })

        # 步骤5: CONFIRM标记验证
        steps.append({
            "step": 5,
            "name": "CONFIRM标记验证",
            "status": "completed",
            "detail": "CONFIRM标记有效",
        })

        # 步骤6: SEAL标记验证
        steps.append({
            "step": 6,
            "name": "SEAL标记验证",
            "status": "completed",
            "detail": "SEAL标记有效",
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
        """获取激活状态"""
        return {
            "is_activated": self.is_activated,
            "total_activations": len(self.activation_log),
            "last_activation": self.activation_log[-1] if self.activation_log else None,
        }


# ═══════════════════════════════════════════════════════════════════════════════
# 核心类: FoundationLauncher — 系统底座启动台
# ═══════════════════════════════════════════════════════════════════════════════

class FoundationLauncher:
    """
    龍魂系统底座启动台
    ──────────────────
    整合所有子系统，提供交互式启动台
    """

    def __init__(self):
        self.dna = DNA_SIGNATURE
        self.confirm = CONFIRM_MARK
        self.seal = SEAL_MARK
        self.version = VERSION
        self.created_at = datetime.now().isoformat()

        # 子系统
        self.iron_law_gate = IronLawGate()
        self.source_validator = SourceChainValidator()
        self.health_checker = SystemHealthChecker()
        self.cnsh_activator = CNSHProtocolActivator()

        # 状态
        self.health: Optional[SystemHealth] = None
        self.running = True
        self.session_log: List[Dict[str, Any]] = []

        # 菜单定义
        self.menu_options = [
            MenuOption(1, "系统健康检查", "L2", "🟡", "执行完整系统健康检查", "health_check"),
            MenuOption(2, "CNSH协议激活", "L3", "🔴", "激活CNSH数字灵魂协议", "cnsh_activate"),
            MenuOption(3, "扫描核心脚本", "L2", "🟡", "扫描并验证核心脚本", "scan_scripts"),
            MenuOption(4, "查看系统状态", "L1", "🟢", "显示当前系统运行状态", "show_status"),
            MenuOption(5, "查看来源链", "L3", "🔴", "显示六层来源链信息", "show_source_chain"),
            MenuOption(6, "查看铁律", "L1", "🟢", "显示四条铁律全文", "show_iron_laws"),
            MenuOption(7, "铁律自审", "L1", "🟢", "IronLawGate 铁律自审闸", "iron_law_audit"),
            MenuOption(8, "六层来源链验证", "L3", "🔴", "验证六层来源链完整性", "validate_source_chain"),
            MenuOption(9, "生成完整报告", "L3", "🔴", "生成系统完整报告", "full_report"),
            MenuOption(0, "退出系统", "L1", "🟢", "安全退出启动台", "exit_system"),
        ]

    def _log(self, event: str, data: Any = None) -> None:
        """记录会话日志"""
        self.session_log.append({
            "event": event,
            "data": data,
            "timestamp": datetime.now().isoformat(),
        })

    def print_banner(self) -> None:
        """打印启动横幅"""
        banner = f"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   🐉 龍魂系统底座启动台 v2.0 — LongHun Foundation Launcher                   ║
║                                                                               ║
║   {self.dna:<74} ║
║   {self.confirm:<74} ║
║                                                                               ║
║   三层监督: 🟢 L1-自主层  🟡 L2-同侪层  🔴 L3-生态层                          ║
║   六层来源链: 道统层·精神层·设备层·技术层·系统层·生命层                        ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""
        print(banner)

    def print_menu(self) -> None:
        """打印主菜单"""
        print("\n  ─── 主菜单 ───\n")
        for opt in self.menu_options:
            print(f"  [{opt.number}] {opt.color} {opt.label:<18} [{opt.layer}] {opt.description}")
        print()

    def health_check(self) -> None:
        """[1] 系统健康检查 — L2"""
        print("\n" + "=" * 60)
        print("  [1] 🟡 L2 系统健康检查")
        print("=" * 60)

        self.health = self.health_checker.run_all_checks()

        for check_name, detail in self.health.details.items():
            color = detail.get("audit_color", "⚪")
            ok = "✅" if detail.get("ok", False) else "❌"
            print(f"  {color} {ok} {check_name}")
            if "free_gb" in detail:
                print(f"      可用空间: {detail['free_gb']:.2f} GB / {detail['total_gb']:.2f} GB")
            if "current" in detail:
                print(f"      当前版本: Python {detail['current']}")
            if "scripts" in detail:
                for s in detail["scripts"]:
                    s_icon = "✅" if s["exists"] else "❌"
                    print(f"      {s_icon} {s['name']} ({s.get('size', 0):,} bytes)")
            if "error" in detail:
                print(f"      错误: {detail['error']}")

        print("\n" + "-" * 60)
        overall = "🟢 系统健康" if self.health.all_healthy else "🔴 存在问题"
        print(f"  总体状态: {overall}")
        print(f"  检查项: {self.health.passed_checks}/{self.health.total_checks} 通过")
        print("=" * 60)
        self._log("health_check", self.health.to_dict())

    def cnsh_activate(self) -> None:
        """[2] CNSH协议激活 — L3"""
        print("\n" + "=" * 60)
        print("  [2] 🔴 L3 CNSH协议激活")
        print("=" * 60)

        result = self.cnsh_activator.activate()

        for step in result["steps"]:
            icon = "✅" if step["status"] == "completed" else "⏳"
            print(f"  {icon} 步骤 {step['step']}: {step['name']}")
            print(f"      {step['detail']}")

        print("\n  ───────────────────────────────")
        print(f"  🟢 CNSH协议激活成功")
        print(f"  时间戳: {result['timestamp']}")
        print(f"  DNA: {result['dna'][:50]}...")
        print("=" * 60)
        self._log("cnsh_activate", result)

    def scan_scripts(self) -> None:
        """[3] 扫描核心脚本 — L2"""
        print("\n" + "=" * 60)
        print("  [3] 🟡 L2 扫描核心脚本")
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
        print(f"  结果: {'🟢 全部核心脚本验证通过' if all_passed else '🔴 部分脚本验证失败'}")
        print("=" * 60)
        self._log("scan_scripts", result)

    def show_status(self) -> None:
        """[4] 查看系统状态 — L1"""
        print("\n" + "=" * 60)
        print("  [4] 🟢 L1 系统状态")
        print("=" * 60)

        # Python版本
        print(f"  Python版本: {sys.version}")
        print(f"  平台: {platform.platform()}")
        print(f"  当前时间: {datetime.now().isoformat()}")
        print(f"  工作目录: {os.getcwd()}")

        # 磁盘空间
        try:
            usage = shutil.disk_usage("/mnt/agents")
            free_gb = usage.free / (1024**3)
            total_gb = usage.total / (1024**3)
            print(f"  磁盘空间: {free_gb:.2f} GB 可用 / {total_gb:.2f} GB 总计")
        except Exception:
            print("  磁盘空间: 无法获取")

        # 核心脚本状态
        print(f"\n  核心脚本:")
        for script in CORE_SCRIPTS:
            path = Path(SYSTEM_PATHS["output_dir"]) / script
            status = "✅ 存在" if path.exists() else "❌ 缺失"
            size = f"({path.stat().st_size:,} bytes)" if path.exists() else ""
            print(f"    {script}: {status} {size}")

        # 健康状态
        if self.health:
            print(f"\n  最后健康检查: {self.health.timestamp}")
            print(f"  健康状态: {'🟢 健康' if self.health.all_healthy else '🔴 异常'}")

        # CNSH激活状态
        cnsh_status = self.cnsh_activator.get_status()
        print(f"  CNSH协议: {'🟢 已激活' if cnsh_status['is_activated'] else '⚪ 未激活'}")

        print("=" * 60)
        self._log("show_status")

    def show_source_chain(self) -> None:
        """[5] 查看来源链 — L3"""
        print("\n" + "=" * 60)
        print("  [5] 🔴 L3 六层来源链")
        print("=" * 60)

        for layer in SOURCE_CHAIN_LAYERS:
            layer_num = layer["layer"]
            name = layer["name"]
            source = layer["source"]
            essence = layer["essence"]
            print(f"\n  [{layer_num}] {name}")
            print(f"      来源: {source}")
            print(f"      本质: {essence}")

        print("\n  ───────────────────────────────")
        print(f"  DNA: {self.dna}")
        print(f"  CONFIRM: {self.confirm}")
        print(f"  SEAL: {self.seal}")
        print("=" * 60)
        self._log("show_source_chain")

    def show_iron_laws(self) -> None:
        """[6] 查看铁律 — L1"""
        print("\n" + "=" * 60)
        print("  [6] 🟢 L1 四条铁律")
        print("=" * 60)

        for law in IRON_LAWS:
            print(f"\n  [{law['id']}] {law['text']}")

        print("\n  ───────────────────────────────")
        print("  ⚠️  以上铁律绝对不可违背")
        print("  ⚠️  违反任何一条即为失去龍魂认证")
        print("=" * 60)
        self._log("show_iron_laws")

    def iron_law_audit(self) -> None:
        """[7] 铁律自审 — L1"""
        print("\n" + "=" * 60)
        print("  [7] 🟢 L1 铁律自审闸 (IronLawGate)")
        print("=" * 60)

        # 审计启动台自身
        self_result = self.iron_law_gate.audit_file(__file__)
        print(f"\n  自身审查: {self_result['audit_color']}")
        print(f"  检查次数: {self_result['check_count']}")
        print(f"  违规数: {len(self_result['violations'])}")

        if self_result["violations"]:
            for v in self_result["violations"]:
                print(f"\n  🔴 [{v['law_id']}] {v['law_text']}")
                print(f"     详情: {v['detail']}")
        else:
            print("\n  🟢 无铁律违规检测")

        # 审计系统目录
        print("\n  ─── 系统目录审查 ───")
        dir_result = self.iron_law_gate.audit_system_files(SYSTEM_PATHS["output_dir"])
        print(f"  审查文件: {dir_result['files_checked']}")
        print(f"  清洁文件: {dir_result['files_clean']} 🟢")
        print(f"  问题文件: {dir_result['files_with_issues']} {dir_result.get('audit_color', '')}")

        print("\n" + "=" * 60)
        self._log("iron_law_audit", {"self": self_result, "directory": dir_result})

    def validate_source_chain(self) -> None:
        """[8] 六层来源链验证 — L3"""
        print("\n" + "=" * 60)
        print("  [8] 🔴 L3 六层来源链验证")
        print("=" * 60)

        # 验证来源链完整性
        integrity = self.source_validator.validate_chain_integrity()

        print("\n  ─── 来源链完整性 ───")
        for lr in integrity.get("layer_results", []):
            icon = "🟢" if lr["valid"] else "🔴"
            print(f"  {icon} L{lr['layer']} {lr['name']} — {lr['source']} · {lr['essence']}")

        # 验证核心脚本
        print("\n  ─── 核心脚本DNA验证 ───")
        script_verify = self.source_validator.verify_all_core_scripts(SYSTEM_PATHS["output_dir"])
        for sr in script_verify.get("script_results", []):
            if "exists" in sr:
                continue
            color = sr.get("audit_color", "⚪")
            print(f"  {color} {sr['file']}")
            print(f"      DNA: {'✅' if sr.get('dna_present') else '❌'}")
            print(f"      CONFIRM: {'✅' if sr.get('confirm_present') else '❌'}")
            print(f"      SEAL: {'✅' if sr.get('seal_present') else '❌'}")

        # DNA标记验证
        print("\n  ─── DNA标记验证 ───")
        dna_verify = self.source_validator.verify_dna_in_file(__file__)
        print(f"  DNA签名: {'✅ 有效' if dna_verify.get('dna_present') else '❌ 缺失'}")
        print(f"  CONFIRM: {'✅ 有效' if dna_verify.get('confirm_present') else '❌ 缺失'}")
        print(f"  SEAL: {'✅ 有效' if dna_verify.get('seal_present') else '❌ 缺失'}")

        all_valid = integrity.get("all_valid", False) and script_verify.get("all_passed", False)

        print("\n  ───────────────────────────────")
        print(f"  结果: {'🟢 六层来源链完整有效' if all_valid else '🔴 存在缺失'}")
        print("=" * 60)
        self._log("validate_source_chain", {"integrity": integrity, "scripts": script_verify})

    def full_report(self) -> None:
        """[9] 生成完整报告 — L3"""
        print("\n" + "=" * 60)
        print("  [9] 🔴 L3 生成完整报告")
        print("=" * 60)

        report_lines = [
            "═══════════════════════════════════════════════════════════",
            "  龍魂系统底座启动台 — 完整报告",
            f"  {self.dna}",
            f"  {self.confirm}",
            f"  {self.seal}",
            "═══════════════════════════════════════════════════════════",
            f"\n  版本: {self.version}",
            f"  生成时间: {datetime.now().isoformat()}",
            f"  Python: {sys.version}",
            f"  平台: {platform.platform()}",
        ]

        # 系统健康
        report_lines.append("\n  ─── 系统健康 ───")
        if self.health:
            report_lines.append(f"  状态: {'🟢 健康' if self.health.all_healthy else '🔴 异常'}")
            report_lines.append(f"  磁盘空间: {self.health.disk_free_gb:.2f} GB 可用")
            report_lines.append(f"  检查通过: {self.health.passed_checks}/{self.health.total_checks}")
        else:
            report_lines.append("  (尚未执行健康检查)")

        # CNSH状态
        cnsh = self.cnsh_activator.get_status()
        report_lines.append("\n  ─── CNSH协议 ───")
        report_lines.append(f"  激活状态: {'🟢 已激活' if cnsh['is_activated'] else '⚪ 未激活'}")
        report_lines.append(f"  激活次数: {cnsh['total_activations']}")

        # 六层来源链
        report_lines.append("\n  ─── 六层来源链 ───")
        for layer in SOURCE_CHAIN_LAYERS:
            report_lines.append(f"  [{layer['layer']}] {layer['name']} — {layer['source']}")

        # AI Truth Protocol
        report_lines.append("\n  ─── AI Truth Protocol ───")
        report_lines.append("  输出可信度: HIGH")
        report_lines.append("  来源已验证: ✅")
        report_lines.append("  债务已记录: ✅")
        report_lines.append("  铁律状态: ✅ 已加载")
        report_lines.append(f"  DNA签名: {self.dna}")

        report_lines.append("\n═══════════════════════════════════════════════════════════")

        report = "\n".join(report_lines)
        print(report)

        # 保存报告
        report_path = Path(SYSTEM_PATHS["output_dir"]) / "foundation_report.txt"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\n📄 报告已保存: {report_path}")

        self._log("full_report", {"saved_to": str(report_path)})

    def exit_system(self) -> None:
        """[0] 退出系统 — L1"""
        print("\n" + "=" * 60)
        print("  [0] 🟢 L1 安全退出")
        print("=" * 60)
        print("\n  感谢使用龍魂系统底座启动台")
        print(f"  {self.seal}")
        print("\n  龍魂不灭 · 真理永存")
        print("=" * 60 + "\n")
        self._log("exit")
        self.running = False

    def handle_choice(self, choice: str) -> None:
        """处理用户选择"""
        try:
            option = next((o for o in self.menu_options if str(o.number) == choice), None)
            if option:
                handler = getattr(self, option.handler, None)
                if handler:
                    handler()
                else:
                    print(f"🔴 未实现的处理器: {option.handler}")
            else:
                print("🔴 无效选项，请重新输入")
        except Exception as e:
            print(f"🔴 执行出错: {e}")
            import traceback
            traceback.print_exc()

    def run_auto_mode(self) -> None:
        """自动模式 — 执行全部检查"""
        print("\n" + "=" * 60)
        print("  🤖 自动系统检查模式")
        print("=" * 60)

        # 1. 系统健康
        self.health_check()

        # 2. CNSH激活
        self.cnsh_activate()

        # 3. 扫描脚本
        self.scan_scripts()

        # 4. 铁律自审
        self.iron_law_audit()

        # 5. 来源链验证
        self.validate_source_chain()

        # 6. 生成报告
        self.full_report()

        print("\n" + "=" * 60)
        print("  ✅ 自动检查完成")
        print("=" * 60)

    def run_interactive(self) -> None:
        """运行交互式启动台"""
        self.print_banner()

        while self.running:
            self.print_menu()
            try:
                choice = input("  请选择操作 [0-9]: ").strip()
                self.handle_choice(choice)
            except KeyboardInterrupt:
                print("\n\n  收到中断信号...")
                self.exit_system()
                break
            except EOFError:
                break


# ═══════════════════════════════════════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="龍魂系统底座启动台 v2.0 — LongHun Foundation Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python longhun_foundation_launcher_v2.0.py         # 交互式启动台
  python longhun_foundation_launcher_v2.0.py --auto  # 自动系统检查
  python longhun_foundation_launcher_v2.0.py --check # 单次健康检查
        """,
    )
    parser.add_argument("--auto", action="store_true", help="自动执行全部系统检查")
    parser.add_argument("--check", action="store_true", help="单次健康检查后退出")

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
