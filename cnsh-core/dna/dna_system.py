#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║        龍魂DNA追溯码系统 / LongHun DNA Traceability System      ║
║                                                                  ║
║  DNA生成·追溯链验证·来源永不删除                                 ║
║  每个产物都自动打上身份，改名也改不了                             ║
║                                                                  ║
║  DNA: #龍芯⚡️2026-06-03-DNA-SYSTEM-v1.0                         ║
║  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✓              ║
║                                                                  ║
║  来源: CNSH::#龍芯⚡️2026-05-07-DNA追溯码生成器-v2.0             ║
║  铁律: 来源不可删 · 影响不可覆 · 贡献不可抹                       ║
║  责任: UID9622·不免责                                            ║
╚══════════════════════════════════════════════════════════════════╝
"""

import hashlib
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict, field
from datetime import datetime
from enum import Enum

# ═══════════════════════════════════════════════════════════════
# 【六层来源链】不可删除的身份标记
# ═══════════════════════════════════════════════════════════════

SIX_LAYER_CHAIN = {
    "L1_道统层": {
        "名称": "Dao Tradition Layer",
        "来源": "曾仕强老师（动态日益·L0不可移除）",
        "内容": "中国古代哲学和智慧",
        "代码": "曾",
    },
    "L2_精神层": {
        "名称": "Spirit Layer",
        "来源": "Steve Jobs",
        "内容": "创意、设计、用户体验哲学",
        "代码": "乔",
    },
    "L3_设备层": {
        "名称": "Device Layer",
        "来源": "Apple",
        "内容": "硬件平台、操作系统",
        "代码": "苹",
    },
    "L4_技术层": {
        "名称": "Technology Layer",
        "来源": "Open Source Community",
        "内容": "编程语言、框架、工具",
        "代码": "源",
    },
    "L5_系统层": {
        "名称": "System Layer",
        "来源": "UID9622 (诸葛鑫·龍芯北辰)",
        "内容": "龍魂系统架构、业务规则",
        "代码": "9622",
    },
    "L6_生命层": {
        "名称": "Life Layer",
        "来源": "CNSH (诸葛鑫·龍魂真我)",
        "内容": "个人价值观、创意、责任",
        "代码": "生命",
    },
}


class DNAStatus(str, Enum):
    """DNA状态"""
    ACTIVE = "🟢"      # 活跃
    ARCHIVED = "🟡"    # 归档
    DELETED = "🔴"     # 删除（但不能真删）
    VERIFIED = "✅"    # 已验证


# ═══════════════════════════════════════════════════════════════
# 【DNA对象】
# ═══════════════════════════════════════════════════════════════

@dataclass
class DNA:
    """DNA追溯码 - 每个产物的身份证"""

    # DNA核心信息
    dna_code: str                    # 例: #龍芯⚡️2026-06-03-BAOBAO-WORKFLOW-v1.0
    creator_uid: str = "9622"        # 创造者UID
    created_date: str = ""           # 创建日期 (自动)
    content_hash: str = ""           # 内容哈希 (自动)
    version: str = "v1.0"            # 版本

    # 追溯链信息
    six_layer_chain: Dict = field(default_factory=lambda: SIX_LAYER_CHAIN.copy())
    parent_dna: Optional[str] = None  # 父代DNA (用于继承关系)
    child_dnas: List[str] = field(default_factory=list)  # 子代DNA

    # 验证信息
    gpg_signature: str = ""          # GPG签名
    verification_hash: str = ""      # 验证哈希
    status: DNAStatus = DNAStatus.ACTIVE

    # 元数据
    file_path: Optional[str] = None  # 关联文件路径
    description: str = ""            # 描述
    keywords: List[str] = field(default_factory=list)  # 关键词

    def __post_init__(self):
        """初始化DNA"""
        if not self.created_date:
            self.created_date = datetime.now().isoformat(timespec="seconds")

    def compute_content_hash(self, content: str) -> str:
        """计算内容哈希"""
        return hashlib.sha256(content.encode()).hexdigest()

    def compute_verification_hash(self) -> str:
        """计算DNA本身的验证哈希"""
        dna_str = f"{self.dna_code}:{self.creator_uid}:{self.created_date}:{self.content_hash}"
        return hashlib.sha256(dna_str.encode()).hexdigest()

    def validate(self) -> Tuple[bool, List[str]]:
        """验证DNA的完整性"""
        errors = []

        # 检查DNA代码格式
        if not self.dna_code.startswith("#龍芯⚡️"):
            errors.append("DNA代码必须以 #龍芯⚡️ 开头")

        # 检查创造者UID
        if not self.creator_uid:
            errors.append("创造者UID不能为空")

        # 检查创建日期
        if not self.created_date:
            errors.append("创建日期不能为空")

        # 检查六层来源链
        if not self.six_layer_chain:
            errors.append("六层来源链不能为空")

        return len(errors) == 0, errors

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "dna_code": self.dna_code,
            "creator_uid": self.creator_uid,
            "created_date": self.created_date,
            "content_hash": self.content_hash,
            "version": self.version,
            "six_layer_chain": self.six_layer_chain,
            "parent_dna": self.parent_dna,
            "child_dnas": self.child_dnas,
            "status": self.status.value,
            "file_path": self.file_path,
            "description": self.description,
        }


# ═══════════════════════════════════════════════════════════════
# 【DNA生成器】
# ═══════════════════════════════════════════════════════════════

class DNAGenerator:
    """DNA生成和管理"""

    def __init__(self):
        self.dna_registry: Dict[str, DNA] = {}  # DNA代码 -> DNA对象
        self.file_dna_map: Dict[str, str] = {}  # 文件路径 -> DNA代码

    def generate_dna(
        self,
        subject: str,                  # 主题 (如 "BAOBAO-WORKFLOW")
        version: str = "v1.0",
        content: Optional[str] = None,
        file_path: Optional[str] = None,
        description: str = "",
        keywords: Optional[List[str]] = None,
    ) -> DNA:
        """生成一个新DNA"""

        # 生成DNA代码
        date_str = datetime.now().strftime("%Y-%m-%d")
        dna_code = f"#龍芯⚡️{date_str}-{subject}-{version}"

        # 计算内容哈希
        content_hash = ""
        if content:
            content_hash = hashlib.sha256(content.encode()).hexdigest()[:16]  # 简化后的哈希

        # 创建DNA对象
        dna = DNA(
            dna_code=dna_code,
            creator_uid="9622",
            version=version,
            content_hash=content_hash,
            file_path=file_path,
            description=description,
            keywords=keywords or [],
        )

        # 计算验证哈希
        dna.verification_hash = dna.compute_verification_hash()

        # 验证DNA
        is_valid, errors = dna.validate()
        if not is_valid:
            raise ValueError(f"DNA生成失败: {errors}")

        # 注册DNA
        self.dna_registry[dna_code] = dna
        if file_path:
            self.file_dna_map[file_path] = dna_code

        return dna

    def link_parent_child(self, parent_dna_code: str, child_dna_code: str) -> Tuple[bool, str]:
        """建立父子DNA关系"""
        if parent_dna_code not in self.dna_registry:
            return False, f"父DNA不存在: {parent_dna_code}"

        if child_dna_code not in self.dna_registry:
            return False, f"子DNA不存在: {child_dna_code}"

        parent_dna = self.dna_registry[parent_dna_code]
        child_dna = self.dna_registry[child_dna_code]

        # 建立关系
        child_dna.parent_dna = parent_dna_code
        parent_dna.child_dnas.append(child_dna_code)

        return True, f"DNA链接成功: {parent_dna_code} -> {child_dna_code}"

    def get_dna(self, dna_code: str) -> Optional[DNA]:
        """获取DNA"""
        return self.dna_registry.get(dna_code)

    def get_dna_by_file(self, file_path: str) -> Optional[DNA]:
        """通过文件路径获取DNA"""
        dna_code = self.file_dna_map.get(file_path)
        if dna_code:
            return self.dna_registry.get(dna_code)
        return None

    def trace_lineage(self, dna_code: str, direction: str = "up") -> List[str]:
        """追溯DNA血统"""
        if dna_code not in self.dna_registry:
            return []

        lineage = [dna_code]
        current_dna = self.dna_registry[dna_code]

        if direction == "up":
            # 向上追溯父代
            while current_dna.parent_dna:
                lineage.append(current_dna.parent_dna)
                current_dna = self.dna_registry.get(current_dna.parent_dna)
                if not current_dna:
                    break
        elif direction == "down":
            # 向下追溯子代
            to_process = list(current_dna.child_dnas)
            while to_process:
                child_code = to_process.pop(0)
                lineage.append(child_code)
                child_dna = self.dna_registry.get(child_code)
                if child_dna:
                    to_process.extend(child_dna.child_dnas)

        return lineage

    def archive_dna(self, dna_code: str) -> Tuple[bool, str]:
        """归档DNA (不删除，只改状态)"""
        if dna_code not in self.dna_registry:
            return False, f"DNA不存在: {dna_code}"

        dna = self.dna_registry[dna_code]
        dna.status = DNAStatus.ARCHIVED
        return True, f"DNA已归档: {dna_code}"

    def verify_dna_chain(self, dna_code: str) -> Tuple[bool, Dict]:
        """验证DNA链的完整性"""
        if dna_code not in self.dna_registry:
            return False, {"error": f"DNA不存在: {dna_code}"}

        dna = self.dna_registry[dna_code]
        is_valid, errors = dna.validate()

        # 验证父DNA
        if dna.parent_dna:
            if dna.parent_dna not in self.dna_registry:
                errors.append(f"父DNA不存在: {dna.parent_dna}")

        # 验证子DNA
        for child_code in dna.child_dnas:
            if child_code not in self.dna_registry:
                errors.append(f"子DNA不存在: {child_code}")

        return len(errors) == 0, {
            "dna_code": dna_code,
            "valid": len(errors) == 0,
            "errors": errors,
            "verification_hash": dna.verification_hash,
            "status": dna.status.value,
        }

    def list_all_dnas(self) -> List[DNA]:
        """列出所有DNA"""
        return list(self.dna_registry.values())

    def get_statistics(self) -> Dict:
        """获取统计信息"""
        total = len(self.dna_registry)
        active = sum(1 for dna in self.dna_registry.values() if dna.status == DNAStatus.ACTIVE)
        archived = sum(1 for dna in self.dna_registry.values() if dna.status == DNAStatus.ARCHIVED)

        return {
            "total_dnas": total,
            "active_dnas": active,
            "archived_dnas": archived,
            "mapped_files": len(self.file_dna_map),
        }


# ═══════════════════════════════════════════════════════════════
# 【全局DNA生成器】
# ═══════════════════════════════════════════════════════════════

_GLOBAL_DNA_GENERATOR = DNAGenerator()

def get_dna_generator() -> DNAGenerator:
    """获取全局DNA生成器"""
    return _GLOBAL_DNA_GENERATOR


if __name__ == "__main__":
    # 测试DNA系统
    dna_gen = get_dna_generator()

    print("🧬 龍魂DNA追溯码系统")
    print("=" * 80)

    # 创建主DNA
    dna_main = dna_gen.generate_dna(
        subject="BAOBAO-WORKFLOW",
        version="v2.0",
        content="import sys; print('hello')",
        file_path="/Users/zuimeidedeyihan/longhun-system/baobao_workflow.py",
        description="宝宝工作流主模块",
        keywords=["workflow", "baobao", "automation"],
    )

    print(f"\n生成主DNA: {dna_main.dna_code}")
    print(f"内容哈希: {dna_main.content_hash}")
    print(f"验证哈希: {dna_main.verification_hash}")

    # 创建子DNA
    dna_child = dna_gen.generate_dna(
        subject="BAOBAO-LOGGING",
        version="v1.0",
        description="日志模块",
    )

    # 建立血统关系
    success, msg = dna_gen.link_parent_child(dna_main.dna_code, dna_child.dna_code)
    print(f"\n{msg}")

    # 验证DNA链
    valid, verification = dna_gen.verify_dna_chain(dna_main.dna_code)
    print(f"\nDNA链验证: {'✅' if valid else '❌'}")
    print(json.dumps(verification, ensure_ascii=False, indent=2))

    # 统计信息
    stats = dna_gen.get_statistics()
    print(f"\n统计信息:")
    print(json.dumps(stats, ensure_ascii=False, indent=2))

    print("=" * 80)
