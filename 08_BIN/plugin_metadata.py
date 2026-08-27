# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂系统 · 插件元数据标准格式 v1.0
DNA: #龍芯⚡️2026-08-22-PLUGIN-METADATA-v1.0-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any
from datetime import datetime, UTC
import json
import hashlib

# ============================================================
# 标准元数据定义（所有插件必须遵循）
# ============================================================

REQUIRED_FIELDS = [
    "plugin_id", "name", "version", "author", "description",
    "category", "compatible_core", "compatible_with",
    "language", "target_audience", "license", "created_at",
]

OPTIONAL_FIELDS = [
    "dependencies", "conflicts", "tags", "homepage", "repository",
    "min_longhun_version", "allow_auto_optimize", "allow_secondary_dev",
    "require_author_credit", "require_author_approval",
    "notify_on_merge", "dna", "extra",
]

@dataclass
class PluginMetadata:
    """插件元数据标准结构"""

    # ---------- 必填字段 ----------
    plugin_id: str          # 唯一ID，推荐: 作者.名称.版本简写
    name: str               # 插件显示名称
    version: str            # 语义化版本，如 1.0.0
    author: str             # 作者（UID 或名称）
    description: str        # 简短描述
    category: str           # 分类: core/professional/personal/national/experimental
    compatible_core: bool   # 是否声明兼容核心锚点（必须为 True）
    compatible_with: List[str]  # 声明兼容的现有插件ID列表（可为空列表）
    language: List[str]     # 支持语言，如 ["zh", "en"]
    target_audience: List[str]  # 目标人群: junior/senior/university/phd/all
    license: str            # 许可证
    created_at: str         # ISO 时间

    # ---------- 可选字段 ----------
    dependencies: List[str] = field(default_factory=list)
    conflicts: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    homepage: Optional[str] = None
    repository: Optional[str] = None
    min_longhun_version: str = "1.0.0"
    allow_auto_optimize: bool = True
    allow_secondary_dev: bool = True
    require_author_credit: bool = True
    require_author_approval: bool = False
    notify_on_merge: bool = True
    dna: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)

    def generate_dna(self, title: Optional[str] = None) -> str:
        """生成简单 DNA 占位（实际项目中可调用 lh_dna_ref_impl）"""
        raw = f"{self.plugin_id}:{self.version}:{self.author}"
        h = hashlib.sha256(raw.encode()).hexdigest()[:8]
        self.dna = f"#龍芯⚡️PLUGIN-{self.category.upper()}-{self.name}-{h}"
        return self.dna

    def validate(self) -> List[str]:
        """返回错误列表，空列表表示通过"""
        errors = []
        for field_name in REQUIRED_FIELDS:
            val = getattr(self, field_name, None)
            if val is None or (isinstance(val, str) and not val):
                errors.append(f"缺少必填字段: {field_name}")
        if not self.compatible_core:
            errors.append("compatible_core 必须为 True（必须声明兼容核心锚点）")
        if not self.version or len(self.version.split(".")) < 2:
            errors.append("version 必须使用语义化版本（如 1.0.0）")
        if not self.language:
            errors.append("language 不能为空")
        if not self.target_audience:
            errors.append("target_audience 不能为空")
        return errors

def create_example_metadata() -> PluginMetadata:
    """生成标准示例"""
    meta = PluginMetadata(
        plugin_id="uid9622.example_audit_helper.v1",
        name="示例审计辅助插件",
        version="1.0.0",
        author="UID9622",
        description="用于演示金字塔协议的标准插件元数据格式",
        category="professional",
        compatible_core=True,
        compatible_with=[],
        language=["zh", "en"],
        target_audience=["university", "phd", "all"],
        license="MulanPSL-2.0",
        created_at=datetime.now(UTC).isoformat(),
        tags=["audit", "example", "pyramid"],
    )
    meta.generate_dna()
    return meta

if __name__ == "__main__":
    example = create_example_metadata()
    print("=== 标准插件元数据示例 ===")
    print(example.to_json())
    print("\n校验结果:", example.validate() or "通过")
