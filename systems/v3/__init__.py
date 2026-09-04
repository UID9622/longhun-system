#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
from __future__ import annotations
"""
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
龍魂系统 · v3.0 核心模块集成包
LongHun System · v3.0 Core Modules Integration Package

DNA:#龍芯⚡️丙午·甲午·辛酉·甲午·䷨损-V3-SYSTEMS-INTEGRATION-v1.0
责任: UID9622·不免责

本包将下载包“Kimi_Agent_启动全部技能”中的 5 个 v3.0 核心 Python 模块
吸收进 longhun-system 主干，并透过英文别名提供兼容导入，不干扰既有主干函数。

原始档案保留于本目录（中文档名），作为存档与直接执行入口。
"""

import os
import sys
import importlib.util
from pathlib import Path
from typing import Optional, Any

__all__ = [
    "WuxingDecisionEngine",
    "PersonaMatrixEngine",
    "SecurityDomainActivator",
    "DNATraceabilityManager",
    "TricolorAuditEngine",
    "load_v3_modules",
]

# 原始中文档名 → 英文别名
_V3_MODULE_MAP = {
    "wuxing_decision_engine": "五行融合决策引擎_v3.0.py",
    "persona_matrix_engine": "人格矩阵路由系统_v3.0.py",
    "security_domain_activator": "安全域审计协议_v3.0.py",
    "dna_traceability_manager": "DNA追溯链系统_v3.0.py",
    "tricolor_audit_engine": "三色审计与10道闸系统_v3.0.py",
}

# 延迟加载快取
_loaded_modules: dict[str, Any] = {}


def _load_module(alias: str, filename: str):
    """使用 importlib 从本包目录载入指定中文名称的模块。"""
    if alias in _loaded_modules:
        return _loaded_modules[alias]

    package_dir = Path(__file__).parent.resolve()
    file_path = package_dir / filename
    if not file_path.exists():
        raise FileNotFoundError(f"v3 模块档案不存在: {file_path}")

    # 使用完整限定名称作为 spec name，确保 dataclass 能正确解析 sys.modules
    full_name = f"{__name__}.{alias}"
    spec = importlib.util.spec_from_file_location(full_name, str(file_path))
    if spec is None or spec.loader is None:
        raise ImportError(f"无法建立模组规格: {file_path}")

    module = importlib.util.module_from_spec(spec)
    # 注册到 sys.modules 避免重复载入与 dataclass 查找失败
    sys.modules[full_name] = module
    spec.loader.exec_module(module)
    _loaded_modules[alias] = module
    return module


def load_v3_modules():
    """预载全部 v3.0 核心模块，返回别名到模块物件的对照表。"""
    for alias, filename in _V3_MODULE_MAP.items():
        _load_module(alias, filename)
    return _loaded_modules.copy()


# ---- 属性式延迟导出 ----
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
            f"v3 模块 {filename!r} 中找不到类别 {cls_name!r}"
        ) from exc


# 包级元信息
__version__ = "1.0.0"
__dna__ = "#龍芯⚡️丙午·甲午·辛酉·甲午·䷨损-V3-SYSTEMS-INTEGRATION-v1.0"
