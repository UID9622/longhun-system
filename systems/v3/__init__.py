#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂系統 · v3.0 核心模塊集成包
Longhun System · v3.0 Core Modules Integration Package

DNA:#龍芯⚡️2026-06-16-V3-SYSTEMS-INTEGRATION-v1.0
責任: UID9622·不免責

本包將下載包「Kimi_Agent_啟動全部技能」中的 5 個 v3.0 核心 Python 模塊
吸收進 longhun-system 主幹，並透過英文別名提供兼容導入，不干擾既有主干函數。

原始檔案保留於本目錄（中文檔名），作為存檔與直接執行入口。
"""

import os
import sys
import importlib.util
from pathlib import Path
from typing import Optional

__all__ = [
    "WuxingDecisionEngine",
    "PersonaMatrixEngine",
    "SecurityDomainActivator",
    "DNATraceabilityManager",
    "TricolorAuditEngine",
    "load_v3_modules",
]

# 原始中文檔名 → 英文別名
_V3_MODULE_MAP = {
    "wuxing_decision_engine": "五行融合决策引擎_v3.0.py",
    "persona_matrix_engine": "人格矩阵路由系统_v3.0.py",
    "security_domain_activator": "安全域审计协议_v3.0.py",
    "dna_traceability_manager": "DNA追溯链系统_v3.0.py",
    "tricolor_audit_engine": "三色审计与10道闸系统_v3.0.py",
}

# 延遲加載快取
_loaded_modules: dict = {}


def _load_module(alias: str, filename: str):
    """使用 importlib 從本包目錄載入指定中文名稱的模塊。"""
    if alias in _loaded_modules:
        return _loaded_modules[alias]

    package_dir = Path(__file__).parent.resolve()
    file_path = package_dir / filename
    if not file_path.exists():
        raise FileNotFoundError(f"v3 模塊檔案不存在: {file_path}")

    # 使用完整限定名稱作為 spec name，確保 dataclass 能正確解析 sys.modules
    full_name = f"{__name__}.{alias}"
    spec = importlib.util.spec_from_file_location(full_name, str(file_path))
    if spec is None or spec.loader is None:
        raise ImportError(f"無法建立模組規格: {file_path}")

    module = importlib.util.module_from_spec(spec)
    # 註冊到 sys.modules 避免重複載入與 dataclass 查找失敗
    sys.modules[full_name] = module
    spec.loader.exec_module(module)
    _loaded_modules[alias] = module
    return module


def load_v3_modules():
    """預載全部 v3.0 核心模塊，返回別名到模塊物件的對照表。"""
    for alias, filename in _V3_MODULE_MAP.items():
        _load_module(alias, filename)
    return _loaded_modules.copy()


# ---- 屬性式延遲導出 ----
def __getattr__(name: str):
    alias_map = {
        "WuxingDecisionEngine": ("wuxing_decision_engine", "WuxingDecisionEngine"),
        "PersonaMatrixEngine": ("persona_matrix_engine", "PersonaMatrixEngine"),
        "SecurityDomainActivator": ("security_domain_activator", "SecurityDomainActivator"),
        "DNATraceabilityManager": ("dna_traceability_manager", "DNA追溯系统管理器"),
        "TricolorAuditEngine": ("tricolor_audit_engine", "TricolorAuditEngine"),
    }
    if name not in alias_map:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    alias, cls_name = alias_map[name]
    filename = _V3_MODULE_MAP[alias]
    module = _load_module(alias, filename)
    try:
        return getattr(module, cls_name)
    except AttributeError as exc:
        raise AttributeError(
            f"v3 模塊 {filename!r} 中找不到類別 {cls_name!r}"
        ) from exc


# 包級元信息
__version__ = "1.0.0"
__dna__ = "#龍芯⚡️2026-06-16-V3-SYSTEMS-INTEGRATION-v1.0"
