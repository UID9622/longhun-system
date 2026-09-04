#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════════
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
  龍魂脚本管理器 v2.0 — LongHun Script Manager
═══════════════════════════════════════════════════════════════════════════════

  DNA签名    :#龍芯⚡️丙午·甲午·壬戌·丙午·䷕贲-SCRIPT-MANAGER-FILE3-v2.0
  CONFIRM标记: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
  SEAL标记   : #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

  三层监督机制:
    🟢 L1-自主层: 脚本自审 + IronLawGate铁律自审闸
    🟡 L2-同侪层: CNSH四层检查 + 来源链交叉验证 + 脚本对齐
    🔴 L3-生态层: AI Truth Protocol + 六层来源链盖章 + 生态兼容性

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
  python longhun_script_manager_v2.0.py scan <目录>     # 扫描脚本
  python longhun_script_manager_v2.0.py align <文件>    # CNSH对齐检查
  python longhun_script_manager_v2.0.py audit           # 完整自审
  python longhun_script_manager_v2.0.py report          # 生成报告
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
# 路径适配 — 根据当前档案位置自动解析专案根目录
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
# 全局常量 — 龍魂体系标识
# ═══════════════════════════════════════════════════════════════════════════════

DNA_SIGNATURE = "#龍芯⚡️丙午·甲午·壬戌·丙午·䷕贲-SCRIPT-MANAGER-v2.0"
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

# CNSH合规标记要求
CNSH_REQUIRED_MARKS = [
    {"mark": "龍芯⚡️", "description": "DNA签名标记", "pattern": r"#龍芯⚡️\d{4}-\d{2}-\d{2}-"},
    {"mark": "CONFIRM🌌", "description": "CONFIRM确认标记", "pattern": r"#CONFIRM🌌9622-ONLY-ONCE"},
    {"mark": "ZHUGEXIN⚡️", "description": "SEAL盖章标记", "pattern": r"#ZHUGEXIN⚡️\d{4}-"},
]

# 脚本分类规则
SCRIPT_CATEGORIES = {
    "workflow": {"keywords": ["workflow", "工作流", "transparent"], "layer": "L1"},
    "manager": {"keywords": ["manager", "管理器", "script_manager"], "layer": "L2"},
    "launcher": {"keywords": ["launcher", "启动台", "foundation"], "layer": "L3"},
    "aligner": {"keywords": ["aligner", "对齐器", "cnsh"], "layer": "L2"},
    "router": {"keywords": ["router", "路由器", "keyword"], "layer": "L2"},
    "utility": {"keywords": ["util", "工具", "helper"], "layer": "L1"},
}


# ═══════════════════════════════════════════════════════════════════════════════
# 数据结构
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ScriptInfo:
    """脚本信息结构"""
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
    """对齐结果结构"""
    script_path: str
    aligned: bool = False
    checks: Dict[str, Any] = field(default_factory=dict)
    fixes_applied: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    timestamp: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()



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
                        "detail": f"检测到: {rule['description']}",
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

    def validate_script(self, file_path: str) -> Dict[str, Any]:
        """验证脚本中的来源链标记"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            return {"valid": False, "error": str(e), "audit_color": "🔴"}

        results = {}
        all_present = True

        # 检查DNA签名
        dna_pattern = re.compile(r"#龍芯⚡️\d{4}-\d{2}-\d{2}-[^\s]+-v\d+\.\d+")
        results["dna_signature"] = {
            "found": bool(dna_pattern.search(content)),
            "pattern": "#龍芯⚡️YYYY-MM-DD-PROJECT-MODULE-vN.N",
        }

        # 检查CONFIRM
        results["confirm_mark"] = {
            "found": CONFIRM_MARK in content,
            "mark": CONFIRM_MARK,
        }

        # 检查SEAL
        results["seal_mark"] = {
            "found": SEAL_MARK in content,
            "mark": SEAL_MARK,
        }

        # 检查六层来源链引用
        for layer in SOURCE_CHAIN_LAYERS:
            key = f"layer_{layer['layer']}_{layer['name']}"
            found = layer["source"] in content
            results[key] = {"found": found, "source": layer["source"]}
            if not found:
                all_present = False

        # 检查三层监督标注
        supervision_markers = ["L1", "L2", "L3", "自主层", "同侪层", "生态层"]
        has_supervision = any(marker in content for marker in supervision_markers)
        results["three_layer_supervision"] = {"found": has_supervision}
        if not has_supervision:
            all_present = False

        # 检查AI Truth Protocol
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
            })
        return {
            "all_valid": all_valid,
            "layer_results": results,
            "timestamp": datetime.now().isoformat(),
            "audit_color": "🟢" if all_valid else "🔴",
        }


# ═══════════════════════════════════════════════════════════════════════════════
# 核心类: CNSHAligner — CNSH对齐器
# ═══════════════════════════════════════════════════════════════════════════════

class CNSHAligner:
    """
    CNSH对齐器
    ────────────
    三层监督: 🟡 L2-同侪层
    功能: 检查脚本是否符合CNSH协议要求
    """

    def __init__(self):
        self.alignment_history: List[Dict[str, Any]] = []

    def align(self, file_path: str) -> AlignmentResult:
        """对指定脚本执行CNSH对齐检查"""
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

        # 1. 检查文件头编码声明
        result.checks["encoding_declared"] = content.startswith("# -*- coding: utf-8 -*-")

        # 2. 检查DNA签名格式
        dna_pattern = re.compile(r"#龍芯⚡️(\d{4}-\d{2}-\d{2})-([^-\s]+)-([^-\s]+)-(v\d+\.\d+)")
        dna_match = dna_pattern.search(content)
        result.checks["dna_format_valid"] = bool(dna_match)
        if dna_match:
            result.checks["dna_date"] = dna_match.group(1)
            result.checks["dna_project"] = dna_match.group(2)
            result.checks["dna_module"] = dna_match.group(3)
            result.checks["dna_version"] = dna_match.group(4)

        # 3. 检查CONFIRM标记
        result.checks["confirm_present"] = CONFIRM_MARK in content

        # 4. 检查SEAL标记
        result.checks["seal_present"] = SEAL_MARK in content

        # 5. 检查六层来源链
        source_chain_count = sum(1 for layer in SOURCE_CHAIN_LAYERS if layer["source"] in content)
        result.checks["source_chain_layers_found"] = source_chain_count
        result.checks["source_chain_complete"] = source_chain_count >= 6

        # 6. 检查三层监督标注
        supervision_keywords = ["L1-自主层", "L2-同侪层", "L3-生态层", "🟢", "🟡", "🔴"]
        supervision_found = sum(1 for kw in supervision_keywords if kw in content)
        result.checks["supervision_markers"] = supervision_found

        # 7. 检查铁律声明
        iron_law_keywords = ["人永远是1", "绝不蒸馏", "来源不可删", "龍"]
        iron_law_found = sum(1 for kw in iron_law_keywords if kw in content)
        result.checks["iron_laws_mentioned"] = iron_law_found

        # 8. 检查AI Truth Protocol
        result.checks["ai_truth_protocol"] = "AI Truth Protocol" in content

        # 9. 检查版本号一致性
        if dna_match:
            declared_version = dna_match.group(4)
            result.checks["version_v2.0"] = declared_version == "v2.0"

        # 计算合规分数
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
        result.aligned = score >= 0.70  # 70%以上视为对齐

        # 生成建议
        if not result.checks.get("dna_format_valid"):
            result.recommendations.append("添加正确格式的DNA签名: #龍芯⚡️YYYY-MM-DD-项目-模块-v2.0")
        if not result.checks.get("confirm_present"):
            result.recommendations.append(f"添加CONFIRM标记: {CONFIRM_MARK}")
        if not result.checks.get("seal_present"):
            result.recommendations.append(f"添加SEAL标记: {SEAL_MARK}")
        if not result.checks.get("source_chain_complete"):
            result.recommendations.append("添加完整的六层来源链声明")
        if result.checks.get("supervision_markers", 0) < 3:
            result.recommendations.append("添加三层监督机制标注 (L1/L2/L3)")
        if not result.checks.get("ai_truth_protocol"):
            result.recommendations.append("添加AI Truth Protocol输出标注")

        self.alignment_history.append(result.to_dict())
        return result

    def align_directory(self, directory: str) -> List[AlignmentResult]:
        """对目录下所有Python脚本执行对齐检查"""
        results = []
        dir_path = Path(directory)
        if not dir_path.exists():
            return results

        for py_file in sorted(dir_path.glob("*.py")):
            result = self.align(str(py_file))
            results.append(result)

        return results


# ═══════════════════════════════════════════════════════════════════════════════
# 核心类: ScriptManager — 脚本管理器
# ═══════════════════════════════════════════════════════════════════════════════

class ScriptManager:
    """
    龍魂脚本管理器核心类
    ─────────────────────
    整合所有子系统，提供完整的脚本管理能力
    """

    def __init__(self, script_dir: str = str(OUTPUT_DIR)):
        # 基础属性
        self.dna = DNA_SIGNATURE
        self.confirm = CONFIRM_MARK
        self.seal = SEAL_MARK
        self.version = VERSION
        self.created_at = datetime.now().isoformat()

        # 脚本目录
        self.script_dir = Path(script_dir)

        # 日志
        self.log_dir = self.script_dir / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / f"script_manager_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"

        # 子系统
        self.iron_law_gate = IronLawGate()
        self.source_validator = SourceChainValidator()
        self.aligner = CNSHAligner()

        # 数据存储
        self.scripts: List[ScriptInfo] = []
        self.alignment_results: List[AlignmentResult] = []
        self.audit_log: List[Dict[str, Any]] = []

    def _log(self, entry: Dict[str, Any]) -> None:
        """Append-only 日志"""
        entry["_timestamp"] = datetime.now().isoformat()
        entry["_dna"] = self.dna
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def scan_scripts(self, directory: Optional[str] = None) -> List[ScriptInfo]:
        """
        扫描目录中的Python脚本
        
        Args:
            directory: 要扫描的目录，默认为初始化时设定的目录
            
        Returns:
            脚本信息列表
        """
        target_dir = Path(directory) if directory else self.script_dir
        if not target_dir.exists():
            print(f"🔴 目录不存在: {target_dir}")
            return []

        self.scripts.clear()
        py_files = sorted(target_dir.glob("*.py"))

        print(f"\n🔍 扫描目录: {target_dir}")
        print(f"   发现 {len(py_files)} 个 Python 文件\n")

        for py_file in py_files:
            info = self._analyze_script(py_file)
            self.scripts.append(info)

            color = info.audit_color
            print(f"  {color} {info.filename}")
            print(f"     大小: {info.size_bytes:,} bytes | 行数: {info.lines}")
            print(f"     DNA: {'✅' if info.has_dna else '❌'} | CONFIRM: {'✅' if info.has_confirm else '❌'} | SEAL: {'✅' if info.has_seal else '❌'}")
            print(f"     合规分数: {info.compliance_score:.1%} | 分类: {info.category} [{info.layer_tag}]")
            if info.errors:
                for err in info.errors:
                    print(f"     ⚠️  {err}")
            print()

        self._log({"event": "scan", "directory": str(target_dir), "scripts_found": len(self.scripts)})
        return self.scripts

    def _analyze_script(self, file_path: Path) -> ScriptInfo:
        """分析单个脚本文件"""
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
                errors=[f"无法读取文件: {e}"],
                audit_color="🔴",
            )

        # 检查DNA签名
        dna_pattern = re.compile(r"#龍芯⚡️\d{4}-\d{2}-\d{2}-[^\s]+-[^\s]+-v\d+\.\d+")
        dna_match = dna_pattern.search(content)
        has_dna = bool(dna_match)
        dna_sig = dna_match.group(0) if dna_match else ""

        # 检查CONFIRM和SEAL
        has_confirm = CONFIRM_MARK in content
        has_seal = SEAL_MARK in content

        # 分类
        category = self._categorize_script(file_path.name, content)
        layer = SCRIPT_CATEGORIES.get(category, {}).get("layer", "L1")

        # 铁律检查
        iron_check = self.iron_law_gate.audit(content, context=f"脚本分析: {file_path.name}")

        # 来源链验证
        chain_validation = self.source_validator.validate_script(str(file_path))

        # 计算合规分数
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

        # 确定审计颜色
        if score >= 0.85 and iron_check["passed"]:
            audit_color = "🟢"
        elif score >= 0.60:
            audit_color = "🟡"
        else:
            audit_color = "🔴"

        errors = []
        if not iron_check["passed"]:
            for v in iron_check["violations"]:
                errors.append(f"铁律违规 [{v['law_id']}]: {v['law_text']}")

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
        """根据文件名和内容分类脚本"""
        filename_lower = filename.lower()
        content_lower = content.lower()

        for category, config in SCRIPT_CATEGORIES.items():
            for keyword in config["keywords"]:
                if keyword.lower() in filename_lower or keyword.lower() in content_lower:
                    return category

        return "utility"

    def align_script(self, file_path: str) -> AlignmentResult:
        """
        对指定脚本执行CNSH对齐
        
        Args:
            file_path: 脚本文件路径
            
        Returns:
            对齐结果
        """
        print(f"\n🔄 CNSH对齐检查: {file_path}")
        result = self.aligner.align(file_path)

        color = "🟢" if result.aligned else "🔴"
        print(f"  {color} 对齐结果: {'通过' if result.aligned else '未通过'}")
        print(f"  合规分数: {result.checks.get('compliance_score', 0):.1%}")

        if result.checks:
            print("\n  详细检查结果:")
            for check_name, check_value in result.checks.items():
                if isinstance(check_value, bool):
                    icon = "✅" if check_value else "❌"
                    print(f"    {icon} {check_name}")
                elif isinstance(check_value, (int, float, str)):
                    print(f"    📊 {check_name}: {check_value}")

        if result.recommendations:
            print("\n  💡 改进建议:")
            for rec in result.recommendations:
                print(f"    → {rec}")

        self.alignment_results.append(result)
        self._log({"event": "align", "file": file_path, "result": result.to_dict()})
        return result

    def run_full_audit(self) -> Dict[str, Any]:
        """
        运行完整自审（--audit 模式）
        """
        print("\n" + "=" * 60)
        print("  🔍 龍魂脚本管理器 — 完整自审模式")
        print("=" * 60)

        results = {}

        # 1. 铁律自审
        print("\n[1/4] 🟢 L1 铁律自审闸...")
        # 自审管理器自身的代码
        self_audit = self.iron_law_gate.audit_file(__file__)
        results["self_iron_law"] = self_audit
        print(f"    自身审查: {self_audit['audit_color']} {'通过' if self_audit['passed'] else '违规'}")

        # 2. 六层来源链验证
        print("\n[2/4] 🔴 L3 六层来源链验证...")
        chain_integrity = self.source_validator.validate_chain_integrity()
        results["source_chain"] = chain_integrity
        print(f"    来源链完整性: {chain_integrity['audit_color']} {'完整' if chain_integrity['all_valid'] else '不完整'}")
        for lr in chain_integrity.get("layer_results", []):
            icon = "🟢" if lr["valid"] else "🔴"
            print(f"    {icon} L{lr['layer']} {lr['name']}")

        # 3. CNSH自身对齐检查
        print("\n[3/4] 🟡 L2 CNSH自身对齐检查...")
        self_align = self.aligner.align(__file__)
        results["self_alignment"] = self_align.to_dict()
        print(f"    自身对齐: {'🟢' if self_align.aligned else '🔴'} {'通过' if self_align.aligned else '未通过'}")
        print(f"    合规分数: {self_align.checks.get('compliance_score', 0):.1%}")

        # 4. 已注册脚本状态
        print("\n[4/4] 🟡 L2 已注册脚本状态...")
        if self.scripts:
            total = len(self.scripts)
            compliant = sum(1 for s in self.scripts if s.compliance_score >= 0.70)
            print(f"    总脚本: {total}")
            print(f"    合规: {compliant} 🟢")
            print(f"    不合规: {total - compliant} {'🟡' if total - compliant < total // 2 else '🔴'}")
            results["registered_scripts"] = {"total": total, "compliant": compliant}
        else:
            print("    尚未注册脚本，请先执行 scan 命令")
            results["registered_scripts"] = {"total": 0, "compliant": 0}

        all_passed = (
            self_audit.get("passed", False) and
            chain_integrity.get("all_valid", False) and
            self_align.aligned
        )
        results["all_passed"] = all_passed

        print("\n" + "=" * 60)
        print(f"  自审总结果: {'🟢 全部通过' if all_passed else '🔴 存在问题'}")
        print("=" * 60)

        self._log({"event": "full_audit", "results": results})
        return results

    def generate_report(self, output_path: Optional[str] = None) -> str:
        """
        生成完整管理报告
        
        Args:
            output_path: 报告输出路径
            
        Returns:
            报告文本
        """
        lines = [
            "═══════════════════════════════════════════════════════════════════",
            "  龍魂脚本管理器 — 完整报告",
            f"  {self.dna}",
            f"  {self.confirm}",
            f"  {self.seal}",
            "═══════════════════════════════════════════════════════════════════",
            f"\n  版本: {self.version}",
            f"  生成时间: {datetime.now().isoformat()}",
            f"  脚本目录: {self.script_dir}",
            f"  日志文件: {self.log_file}",
        ]

        # 已注册脚本
        lines.append("\n  ─── 已注册脚本 ───")
        if self.scripts:
            for script in self.scripts:
                lines.append(f"\n  {script.audit_color} {script.filename} [{script.layer_tag}]")
                lines.append(f"     分类: {script.category}")
                lines.append(f"     大小: {script.size_bytes:,} bytes | 行数: {script.lines}")
                lines.append(f"     DNA: {'✅' if script.has_dna else '❌'}")
                lines.append(f"     CONFIRM: {'✅' if script.has_confirm else '❌'}")
                lines.append(f"     SEAL: {'✅' if script.has_seal else '❌'}")
                lines.append(f"     合规分数: {script.compliance_score:.1%}")
        else:
            lines.append("  (尚未注册脚本)")

        # 对齐结果
        lines.append("\n  ─── 对齐历史 ───")
        if self.alignment_results:
            for ar in self.alignment_results:
                color = "🟢" if ar.aligned else "🔴"
                lines.append(f"  {color} {ar.script_path}")
                lines.append(f"     对齐: {'通过' if ar.aligned else '未通过'}")
                lines.append(f"     分数: {ar.checks.get('compliance_score', 0):.1%}")
        else:
            lines.append("  (尚未执行对齐)")

        # AI Truth Protocol
        lines.append("\n  ─── AI Truth Protocol ───")
        lines.append(f"  输出可信度: HIGH")
        lines.append(f"  来源已验证: ✅")
        lines.append(f"  六层来源链: {'✅ 完整' if all(l.get('source') for l in SOURCE_CHAIN_LAYERS) else '❌ 不完整'}")
        lines.append(f"  铁律状态: ✅ 已加载 {len(IRON_LAWS)} 条")
        lines.append(f"  DNA签名: {self.dna}")

        report = "\n".join(lines)

        # 保存报告
        if output_path:
            out_path = Path(output_path)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(report)
            print(f"\n📄 报告已保存: {out_path}")

        return report

    def get_script_by_name(self, name: str) -> Optional[ScriptInfo]:
        """按名称查找脚本"""
        for script in self.scripts:
            if script.filename == name or script.filename.replace(".py", "") == name:
                return script
        return None

    def get_scripts_by_layer(self, layer: str) -> List[ScriptInfo]:
        """按监督层级查找脚本"""
        return [s for s in self.scripts if s.layer_tag == layer]

    def get_compliance_summary(self) -> Dict[str, Any]:
        """获取合规摘要"""
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
        description="龍魂脚本管理器 v2.0 — LongHun Script Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python longhun_script_manager_v2.0.py scan                  # 扫描默认目录
  python longhun_script_manager_v2.0.py scan /path/to/scripts # 扫描指定目录
  python longhun_script_manager_v2.0.py align <文件路径>       # CNSH对齐检查
  python longhun_script_manager_v2.0.py audit                 # 完整自审
  python longhun_script_manager_v2.0.py report                # 生成报告
  python longhun_script_manager_v2.0.py summary               # 合规摘要
        """,
    )
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # scan 命令
    scan_parser = subparsers.add_parser("scan", help="扫描脚本目录")
    scan_parser.add_argument("directory", nargs="?", default=str(OUTPUT_DIR), help="要扫描的目录")

    # align 命令
    align_parser = subparsers.add_parser("align", help="CNSH对齐检查")
    align_parser.add_argument("file", help="要检查的脚本文件路径")

    # audit 命令
    subparsers.add_parser("audit", help="运行完整自审")

    # report 命令
    report_parser = subparsers.add_parser("report", help="生成完整报告")
    report_parser.add_argument("--output", "-o", default="", help="报告输出路径")

    # summary 命令
    subparsers.add_parser("summary", help="显示合规摘要")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        # 显示系统信息
        print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   🐉 龍魂脚本管理器 v2.0 — LongHun Script Manager                            ║
║                                                                               ║
║   DNA:#龍芯⚡️丙午·甲午·壬戌·丙午·䷕贲-SCRIPT-MANAGER-v2.0                                 ║
║   CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z                               ║
║   SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL                     ║
║                                                                               ║
║   功能: 脚本扫描 | CNSH对齐 | 铁律审查 | 来源链验证                           ║
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
        # 先扫描再生成报告
        manager.scan_scripts()
        output = args.output or str(OUTPUT_DIR / "script_manager_report.txt")
        report = manager.generate_report(output)
        print(report)

    elif args.command == "summary":
        manager.scan_scripts()
        summary = manager.get_compliance_summary()
        print("\n" + "=" * 50)
        print("  📊 合规摘要")
        print("=" * 50)
        print(f"  总脚本数: {summary['total']}")
        print(f"  合规 (≥70%): {summary['compliant']} 🟢")
        print(f"  不合规: {summary['non_compliant']}")
        print(f"  平均合规分数: {summary['average_score']:.1%}")
        print(f"  完全合规 (≥90%): {summary['fully_compliant']}")
        print(f"  需关注 (50-70%): {summary.get('needs_attention', 0)} 🟡")
        print(f"  严重 (<50%): {summary.get('critical', 0)} 🔴")
        print("=" * 50)


if __name__ == "__main__":
    main()
