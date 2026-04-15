"""
CNSH L3 Extension Registry — Entry Model
私域/公域边界定义 + 扩展注册条目

核心设计原则：
  私域无限 → 系统不干涉，不上链，不审计
  公域透明 → 必须DNA登记 + 伦理门 + 链式追溯

Author: 诸葛鑫 (UID9622)
DNA: #LONGHUN⚡️2026-03-23-L3-REGISTRY-v1.0
"""

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
import hashlib
import time


# ── 域类型 ────────────────────────────────────────────────────────

class Scope(str, Enum):
    PRIVATE = "PRIVATE"   # 私域：本地设备，系统不干涉，不上链
    PUBLIC  = "PUBLIC"    # 公域：必须DNA登记 + 伦理审计 + 链式追溯


class ExtType(str, Enum):
    ALGO   = "ALGO"    # 算法扩展（EXT[algo.xxx]）
    AI     = "AI"      # AI模型扩展（EXT[ai.xxx]）
    PLUGIN = "PLUGIN"  # 工具插件（EXT[plugin.xxx]）
    NODE   = "NODE"    # 计算节点（EXT[node.xxx]）
    EVENT  = "EVENT"   # 普通事件条目（非扩展）


# ── 注册表条目 ────────────────────────────────────────────────────

@dataclass
class RegistryEntry:
    """
    L3注册表条目 — DNA追溯的最小公共单元

    每个进入公域的事件、扩展、声明，都必须以此对象记录。
    私域条目可以存在，但 can_enter_public() == False，系统不管也不追。
    """

    # 核心字段
    dna_code:     str              # #龍芯⚡️... 全局唯一标识
    scope:        Scope            # PRIVATE / PUBLIC
    owner_gpg:    str              # GPG指纹（A2D0092C...）
    timestamp:    float            # Unix时间戳
    content_hash: str              # SHA256(原始内容)
    prev_entry:   str              # 前驱DNA码（公链链式追溯，私域为空）

    # 扩展注册专用字段（非扩展条目留空）
    ext_id:       str  = ""        # algo.fractal / ai.local / plugin.xxx
    ext_type:     str  = ""        # ExtType枚举值
    handler_path: str  = ""        # 处理器路径：模块路径 or HTTP端点
    version:      str  = "1.0.0"  # 版本号
    description:  str  = ""        # 可读描述

    # 完整性字段
    gpg_sig:      str  = ""        # 整体GPG签名（可选，无GPG环境时为空）
    active:       bool = True      # 是否激活（停用不删除，保留DNA）

    # 自动填充
    entry_hash:   str  = ""        # 条目自身防篡改哈希
    created_at:   float = field(default_factory=time.time)

    # ── 计算方法 ──────────────────────────────────────────────────

    def compute_entry_hash(self) -> str:
        """计算条目哈希（防篡改校验用）"""
        raw = "|".join([
            self.dna_code,
            str(self.scope),
            self.owner_gpg,
            str(self.timestamp),
            self.content_hash,
            self.prev_entry,
            self.ext_id,
            self.handler_path,
            str(int(self.active)),
        ])
        return hashlib.sha256(raw.encode()).hexdigest()

    def can_enter_public(self) -> bool:
        """
        私域条目不得进入公域。
        这是"私域无限，公域透明"的工程锁。
        """
        if self.scope == Scope.PRIVATE:
            return False
        return True

    def to_dict(self) -> dict:
        return {
            "dna_code":     self.dna_code,
            "scope":        self.scope.value,
            "owner_gpg":    self.owner_gpg,
            "timestamp":    self.timestamp,
            "content_hash": self.content_hash,
            "prev_entry":   self.prev_entry,
            "ext_id":       self.ext_id,
            "ext_type":     self.ext_type,
            "handler_path": self.handler_path,
            "version":      self.version,
            "description":  self.description,
            "active":       self.active,
            "entry_hash":   self.entry_hash,
            "created_at":   self.created_at,
        }

    @property
    def label(self) -> str:
        if self.ext_id:
            return f"EXT[{self.ext_id}] @ {self.handler_path}"
        return f"{self.scope} :: {self.dna_code[:32]}"
