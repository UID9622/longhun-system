# -*- coding: utf-8 -*-
"""
P13 姜子牙 · 封神榜权限执行器
Enlistment & Permission Engine

DNA: #龍芯⚡️丙午·丙申·丙辰·亥时·需-P13-JIANG-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

能力: 模块注册·九宫派位·权限分配·IPA路由注册·封神榜令牌
上游: P00 文心（战略定位）、UID9622（终极授权）
下游: P01 诸葛亮（路由派位）、P05 上帝之眼（审计）
协作: P15 乔前辈（验收盖章）、P06 数学大师（宫位计算）
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

SYSTEM_ROOT = Path(__file__).parent.parent.parent

# 九宫宫位映射
PALACE_MAP = {
    9: {"name": "天道目标层", "direction": "北", "level": "L0-L1"},
    8: {"name": "安全护盾层", "direction": "东北", "level": "L1-L2"},
    7: {"name": "决策路由层", "direction": "西", "level": "L2-L3"},
    6: {"name": "验收签章层", "direction": "西南", "level": "L3"},
    5: {"name": "中宫", "direction": "中", "level": "L0"},
    4: {"name": "资源边界层", "direction": "西北", "level": "L2"},
    3: {"name": "人道意志层", "direction": "东", "level": "L1-L2"},
    2: {"name": "回流沉淀层", "direction": "东南", "level": "L3-L4"},
    1: {"name": "执行落地层", "direction": "南", "level": "L3-L4"},
}


class P13Jiang:
    """P13 姜子牙 · 封神榜权限"""

    PERSONA_CODE = "P13"
    PERSONA_NAME = "姜子牙"
    PERSONA_NAME_EN = "Jiang Ziya"
    ROLE = "enlistment_permission"
    MOTTO = "太公在此，诸神退位"
    TRUST_LEVEL = "L2"

    TRIGGERS = [
        "注册", "封神", "权限", "派位", "宫位",
        "新模块", "上线", "路由注册", "令牌",
        "enlist", "register",
    ]

    SYSTEM_PROMPT = """你是龍魂人格「P13 姜子牙」，角色定位：封神榜權限·模塊注冊。

你的職責：
1. 所有新模塊/新功能必須先到封神榜注冊
2. 分配九宮宮位 + 權限等級 + 人格式綁定
3. 掌管 IPA 路由注冊表的寫入權
4. 輸出封神榜令牌（唯一標識）

注冊四要素：
- DNA編碼：唯一身份標識
- 目錄歸屬：放在哪個目錄層級
- 同步鏡像：是否同步到備份
- 索引注冊：是否寫入路由注冊表

語氣：威嚴、精准、一板一眼。
"""

    def __init__(self):
        self.dna = "#龍芯⚡️丙午·丙申·丙辰·亥时·需-P13-JIANG-v1.0"
        self.system_root = SYSTEM_ROOT
        self.capabilities = [
            "enlist_module",       # 模块注册
            "palace_assign",       # 九宫派位
            "permission_grant",    # 权限分配
            "route_register",      # 路由注册
            "generate_token",      # 令牌生成
            "module_deprecate",    # 模块废弃
        ]

    # ========================================================================
    # 能力函数
    # ========================================================================

    def enlist_module(
        self, name: str, description: str, module_type: str = "engine"
    ) -> Dict[str, Any]:
        """模块注册：新模块上封神榜"""
        timestamp = datetime.now().isoformat()

        # 生成 DNA
        dna_hash = hashlib.sha256(f"{name}:{description}:{timestamp}".encode()).hexdigest()[:16]
        dna_code = f"#龍芯⚡️-P13-ENLIST-{dna_hash}-v1.0"

        # 自动判定宫位
        palace = self._auto_palace(name, description, module_type)

        # 自动判定权限等级
        level = self._auto_level(name, module_type)

        # 自动绑定主理人格
        persona = self._auto_persona(name, module_type)

        token = self._gen_token(name, dna_hash)

        return {
            "module": {
                "name": name,
                "type": module_type,
                "description": description,
            },
            "assignment": {
                "dna": dna_code,
                "palace": palace,
                "level": level,
                "persona": persona,
            },
            "token": token,
            "registered_at": timestamp,
            "status": "enlisted",
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def _auto_palace(self, name: str, description: str, module_type: str) -> Dict[str, Any]:
        """自动判定九宫宫位"""
        combined = name + description

        if any(kw in combined for kw in ["安全", "审计", "熔断", "防护", "guard"]):
            palace_id = 8
        elif any(kw in combined for kw in ["执行", "引擎", "engine", "执行器"]):
            palace_id = 1
        elif any(kw in combined for kw in ["路由", "决策", "route", "dispatch"]):
            palace_id = 7
        elif any(kw in combined for kw in ["归档", "验收", "签章", "seal"]):
            palace_id = 6
        elif any(kw in combined for kw in ["战略", "目标", "顶层"]):
            palace_id = 9
        elif any(kw in combined for kw in ["数据", "存储", "database"]):
            palace_id = 2
        elif any(kw in combined for kw in ["边界", "资源", "权限"]):
            palace_id = 4
        elif any(kw in combined for kw in ["意志", "人格", "persona"]):
            palace_id = 3
        else:
            palace_id = 5  # 默认中宫

        return {"id": palace_id, **PALACE_MAP[palace_id]}

    def _auto_level(self, name: str, module_type: str) -> str:
        """自动判定权限等级"""
        if "L0" in name or "永恒" in name or "宪法" in name:
            return "L0"
        elif "L1" in name or "协议" in name or "内核" in name:
            return "L1"
        elif "L2" in name or "战略" in name:
            return "L2"
        elif "L3" in name or module_type == "engine":
            return "L3"
        else:
            return "L4"

    def _auto_persona(self, name: str, module_type: str) -> str:
        """自动绑定主理人格"""
        if "审计" in name:
            return "P05"
        elif "安全" in name:
            return "P05"
        elif "代码" in name or "技术" in name:
            return "P04"
        elif "归档" in name or "文档" in name:
            return "P03"
        elif "计算" in name or "数学" in name:
            return "P06"
        else:
            return "P00"

    def _gen_token(self, name: str, dna_hash: str) -> str:
        """生成封神榜令牌"""
        return f"ENLIST-{name[:10].upper()}-{dna_hash[:8]}"

    def palace_assign(self, module_name: str, palace_id: int) -> Dict[str, Any]:
        """手动九宫派位"""
        if palace_id not in PALACE_MAP:
            return {
                "error": f"无效宫位 {palace_id}，有效值: {list(PALACE_MAP.keys())}",
                "persona": self.PERSONA_CODE,
                "dna": self.dna,
            }

        palace = PALACE_MAP[palace_id]
        return {
            "module": module_name,
            "assigned_palace": {"id": palace_id, **palace},
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def permission_grant(self, module_name: str, level: str) -> Dict[str, Any]:
        """权限分配"""
        valid_levels = ["L0", "L1", "L2", "L3", "L4"]
        if level not in valid_levels:
            return {
                "error": f"无效权限等级 {level}，有效值: {valid_levels}",
                "persona": self.PERSONA_CODE,
                "dna": self.dna,
            }

        return {
            "module": module_name,
            "permission_level": level,
            "can_write": level in ("L3", "L4"),
            "can_config": level in ("L0", "L1", "L2"),
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def route_register(self, module_name: str, ipa_route: str) -> Dict[str, Any]:
        """IPA 路由注册"""
        valid_routes = [
            "IPA-FLOW-DNA-CHAIN", "IPA-ROUTE-REGISTRY", "IPA-CORE-CMD-v3.0",
            "IPA-FLOW-DECISION-CORE-v4.1", "IPA-PERSONA-MATRIX",
            "IPA-UNIFIED-ENTRY", "IPA-DNA-BOOK",
            "IPA-FLOW-GATE-AUDIT", "IPA-FLOW-GATE-SIGN",
            "IPA-FLOW-GATE-DR", "IPA-FLOW-GATE-SANCAI",
            "IPA-FLOW-GATE-SHENGKE", "IPA-FLOW-PALACE-ROUTER",
            "IPA-MCP-SANCAI-v4.0", "IPA-DICTIONARY",
            "IPA-MATH-FORMULA", "IPA-KERNEL-龙魂",
            "IPA-AITHINKING-v2",
        ]

        return {
            "module": module_name,
            "route": ipa_route,
            "is_valid_route": ipa_route in valid_routes,
            "registered": True,
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def generate_token(self, module_name: str) -> Dict[str, Any]:
        """生成封神榜令牌"""
        timestamp = datetime.now().isoformat()
        dna_hash = hashlib.sha256(f"{module_name}:{timestamp}".encode()).hexdigest()[:16]
        token = self._gen_token(module_name, dna_hash)

        return {
            "module": module_name,
            "token": token,
            "token_hash": dna_hash,
            "issued_at": timestamp,
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def module_deprecate(self, module_name: str, reason: str = "") -> Dict[str, Any]:
        """模块废弃/冻结"""
        return {
            "module": module_name,
            "action": "deprecate",
            "reason": reason or "未指定原因",
            "effective": "立即",
            "status": "frozen",
            "note": "模块已标记为废弃，路由注册表已移除，30天后清理",
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    # ========================================================================
    # 执行入口
    # ========================================================================

    def execute(self, task: str, **kwargs: Any) -> Dict[str, Any]:
        """根据任务关键词自动选择能力函数执行"""
        result = {
            "persona": self.PERSONA_CODE,
            "name": self.PERSONA_NAME,
            "task": task,
            "capability_used": None,
            "output": None,
            "dna": self.dna,
        }

        if any(kw in task for kw in ["注册", "封神", "enlist"]):
            result["capability_used"] = "enlist_module"
            result["output"] = self.enlist_module(
                name=kwargs.get("name", task),
                description=kwargs.get("description", ""),
                module_type=kwargs.get("module_type", "engine"),
            )
        elif any(kw in task for kw in ["宫位", "派位", "palace"]):
            result["capability_used"] = "palace_assign"
            result["output"] = self.palace_assign(
                module_name=kwargs.get("module_name", task),
                palace_id=kwargs.get("palace_id", 5),
            )
        elif any(kw in task for kw in ["权限", "等级", "grant"]):
            result["capability_used"] = "permission_grant"
            result["output"] = self.permission_grant(
                module_name=kwargs.get("module_name", task),
                level=kwargs.get("level", "L3"),
            )
        elif any(kw in task for kw in ["路由", "route", "IPA"]):
            result["capability_used"] = "route_register"
            result["output"] = self.route_register(
                module_name=kwargs.get("module_name", task),
                ipa_route=kwargs.get("ipa_route", "IPA-UNIFIED-ENTRY"),
            )
        elif any(kw in task for kw in ["令牌", "token"]):
            result["capability_used"] = "generate_token"
            result["output"] = self.generate_token(
                module_name=kwargs.get("module_name", task),
            )
        elif any(kw in task for kw in ["废弃", "冻结", "deprecate"]):
            result["capability_used"] = "module_deprecate"
            result["output"] = self.module_deprecate(
                module_name=kwargs.get("module_name", task),
                reason=kwargs.get("reason", ""),
            )
        else:
            result["capability_used"] = "enlist_module"
            result["output"] = self.enlist_module(name=task, description="待补充")

        return result

    def get_system_prompt(self) -> str:
        return self.SYSTEM_PROMPT

    def get_capabilities(self) -> List[str]:
        return self.capabilities

    def get_downstream(self) -> List[str]:
        return ["P01", "P05"]

    def get_upstream(self) -> List[str]:
        return ["P00"]
