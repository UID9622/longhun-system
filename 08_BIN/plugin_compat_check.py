# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂系统 · 自动兼容性检查脚本骨架 v1.0
DNA: #龍芯⚡️2026-08-22-COMPAT-CHECK-v1.0-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

用途：
  检查新插件是否满足金字塔协议的兼容性要求
  输出三色结果：🟢 通过 / 🟡 待审 / 🔴 拒绝
"""

from __future__ import annotations
import json
import sys
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass

sys.path.insert(0, str(Path(__file__).resolve().parent))
from plugin_metadata import PluginMetadata, REQUIRED_FIELDS

# ============================================================
# 配置区（可后续接入真实插件仓库）
# ============================================================

EXISTING_PLUGINS: List[Dict[str, Any]] = [
    {"plugin_id": "core.tri_color_audit.v1",  "name": "三色审计核心",  "version": "1.0.0", "category": "core", "compatible_core": True},
    {"plugin_id": "core.dna_trace.v1",        "name": "DNA追溯核心",   "version": "1.0.0", "category": "core", "compatible_core": True},
]

CORE_ANCHORS = ["tri_color", "三色", "dna", "龍芯", "data_sovereignty", "数据主权"]

@dataclass
class CheckResult:
    status: str          # 🟢 / 🟡 / 🔴
    score: int           # 0-100
    errors: List[str]
    warnings: List[str]
    suggestions: List[str]

    def to_dict(self) -> dict:
        return {"status": self.status, "score": self.score,
                "errors": self.errors, "warnings": self.warnings,
                "suggestions": self.suggestions}

def load_metadata_from_file(path: str) -> PluginMetadata:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    known = set(PluginMetadata.__dataclass_fields__.keys())
    filtered = {k: v for k, v in data.items() if k in known}
    return PluginMetadata(**filtered)

def check_core_compatibility(meta: PluginMetadata) -> List[str]:
    errors = []
    if not meta.compatible_core:
        errors.append("未声明兼容核心锚点（compatible_core 必须为 True）")
    desc = (meta.description or "").lower()
    name = (meta.name or "").lower()
    for anchor in CORE_ANCHORS:
        if f"override_{anchor}" in desc or f"replace_{anchor}" in name:
            errors.append(f"疑似试图覆盖核心锚点: {anchor}")
    return errors

def check_conflict_with_existing(meta: PluginMetadata) -> List[str]:
    errors = []
    existing_ids = {p["plugin_id"] for p in EXISTING_PLUGINS}
    if meta.plugin_id in existing_ids:
        errors.append(f"plugin_id 已存在: {meta.plugin_id}")
    for c in meta.conflicts:
        if c in existing_ids:
            errors.append(f"与现有插件冲突: {c}")
    return errors

def check_dependency_availability(meta: PluginMetadata) -> List[str]:
    warnings = []
    existing_ids = {p["plugin_id"] for p in EXISTING_PLUGINS}
    for dep in meta.dependencies:
        if dep not in existing_ids:
            warnings.append(f"依赖插件尚未在仓库中: {dep}")
    return warnings

def check_audience_and_language(meta: PluginMetadata) -> List[str]:
    warnings = []
    if "all" not in meta.target_audience and len(meta.target_audience) < 1:
        warnings.append("target_audience 建议至少包含一个明确人群或 all")
    if not meta.language:
        warnings.append("language 为空，建议至少声明 zh 或 en")
    return warnings

def run_compatibility_check(meta: PluginMetadata) -> CheckResult:
    errors: List[str] = []
    warnings: List[str] = []
    suggestions: List[str] = []

    errors.extend(meta.validate())
    errors.extend(check_core_compatibility(meta))
    errors.extend(check_conflict_with_existing(meta))
    warnings.extend(check_dependency_availability(meta))
    warnings.extend(check_audience_and_language(meta))

    score = max(0, min(100, 100 - len(errors) * 25 - len(warnings) * 5))

    if errors:
        status = "🔴"
        suggestions.append("请修复所有错误后重新提交")
    elif warnings:
        status = "🟡"
        suggestions.append("存在警告项，建议人工复核后再合并")
    else:
        status = "🟢"
        suggestions.append("可以进入自动合并流程")

    return CheckResult(status=status, score=score,
                       errors=errors, warnings=warnings, suggestions=suggestions)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂插件自动兼容性检查")
    parser.add_argument("--meta", required=True, help="插件元数据 JSON 文件路径")
    parser.add_argument("--json", action="store_true", help="以 JSON 格式输出结果")
    args = parser.parse_args()

    try:
        meta = load_metadata_from_file(args.meta)
    except Exception as e:
        print(f"🔴 无法加载元数据: {e}")
        sys.exit(2)

    result = run_compatibility_check(meta)

    if args.json:
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    else:
        print("=" * 50)
        print(f"插件: {meta.name} ({meta.plugin_id})")
        print(f"版本: {meta.version}")
        print(f"结果: {result.status}  得分: {result.score}")
        print("=" * 50)
        if result.errors:
            print("\n[错误]")
            for e in result.errors:
                print(f"  ❌ {e}")
        if result.warnings:
            print("\n[警告]")
            for w in result.warnings:
                print(f"  ⚠️  {w}")
        if result.suggestions:
            print("\n[建议]")
            for s in result.suggestions:
                print(f"  → {s}")

    if result.status == "🟢":
        sys.exit(0)
    elif result.status == "🟡":
        sys.exit(1)
    else:
        sys.exit(2)

if __name__ == "__main__":
    main()
