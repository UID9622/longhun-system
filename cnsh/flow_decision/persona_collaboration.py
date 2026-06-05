#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂流场·人格协作框架（6条铁律+硬闸实现）
CNSH Flow - Persona Collaboration Framework (6 Iron Laws)

DNA: #龍芯⚡️2026-05-03-CNSH-FLOW-PERSONA-COLLABORATION-v4.1
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

责任: UID9622·不免责
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum
from schemas import PersonaEnum, GateReceipt


# ============================================================================
# 人格铁律定义（6条）
# ============================================================================

class PersonaIronLaw(str, Enum):
    """人格协作铁律"""
    LAW_1 = "一闸一主：每道闸只有一个主驻人格"
    LAW_2 = "熔断独立：龍盾+上帝之眼拥有独立熔断权"
    LAW_3 = "L0必须文心：L0永恒必须文心盖章+老大最终确认"
    LAW_4 = "sealed必须三签：sealed→P03+P72+P05不可缺一"
    LAW_5 = "路由权姜子牙独占：九宫派位由P13独家执行"
    LAW_6 = "写档权乔前辈独占：父子链JSONL/SQLite/Notion由P15独家执行"


@dataclass
class GateCollaboration:
    """闸口协作配置"""
    gate_number: int
    gate_name: str
    main_persona: PersonaEnum
    assist_personas: List[PersonaEnum] = field(default_factory=list)
    hard_rule_ids: List[int] = field(default_factory=list)

    def validate_iron_law_1(self) -> Tuple[bool, str]:
        """验证铁律1：一闸一主"""
        if len([p for p in [self.main_persona] if p]) != 1:
            return False, "闸口未指定唯一主驻人格"
        return True, "通过"

    def validate_iron_law_sealed(self) -> Tuple[bool, str]:
        """验证sealed必须三签"""
        required = {PersonaEnum.P03_WANWAN, PersonaEnum.P05_GODSEYE, PersonaEnum.P72_LONGSHIELD}
        present = {self.main_persona} | set(self.assist_personas)
        if not required.issubset(present):
            return False, f"sealed闸缺少必需人格：{required - present}"
        return True, "三签完整"


@dataclass
class PersonaFuseRight:
    """人格熔断权"""
    persona: PersonaEnum
    has_independent_fuse: bool
    gates_fuse_authority: List[int] = field(default_factory=list)


class PersonaCollaborationFramework:
    """人格协作框架"""

    # 标准10道闸配置
    STANDARD_GATES = {
        1: GateCollaboration(
            gate_number=1,
            gate_name="签章闸",
            main_persona=PersonaEnum.P05_GODSEYE,
            assist_personas=[PersonaEnum.P72_LONGSHIELD],
            hard_rule_ids=[1, 2]
        ),
        2: GateCollaboration(
            gate_number=2,
            gate_name="隐私闸",
            main_persona=PersonaEnum.P03_WANWAN,
            assist_personas=[PersonaEnum.P05_GODSEYE, PersonaEnum.P72_LONGSHIELD],
            hard_rule_ids=[3, 10]
        ),
        3: GateCollaboration(
            gate_number=3,
            gate_name="数字根闸",
            main_persona=PersonaEnum.P06_MATHMASTER,
            assist_personas=[],
            hard_rule_ids=[]
        ),
        4: GateCollaboration(
            gate_number=4,
            gate_name="五行映射",
            main_persona=PersonaEnum.P06_MATHMASTER,
            assist_personas=[],
            hard_rule_ids=[]
        ),
        5: GateCollaboration(
            gate_number=5,
            gate_name="三色闸",
            main_persona=PersonaEnum.P05_GODSEYE,
            assist_personas=[],
            hard_rule_ids=[7, 8]
        ),
        6: GateCollaboration(
            gate_number=6,
            gate_name="三才闸",
            main_persona=PersonaEnum.P00_WENXIN,
            assist_personas=[PersonaEnum.P01_ZHUGELVLIANG],
            hard_rule_ids=[6, 9]
        ),
        7: GateCollaboration(
            gate_number=7,
            gate_name="生克闸",
            main_persona=PersonaEnum.P01_ZHUGELVLIANG,
            assist_personas=[],
            hard_rule_ids=[]
        ),
        8: GateCollaboration(
            gate_number=8,
            gate_name="九宫派位",
            main_persona=PersonaEnum.P13_JIANGZIYA,
            assist_personas=[PersonaEnum.P14_LVMENG],
            hard_rule_ids=[]
        ),
        9: GateCollaboration(
            gate_number=9,
            gate_name="沙盒分拣",
            main_persona=PersonaEnum.P03_WANWAN,
            assist_personas=[PersonaEnum.P15_QIAOQIANDAI],
            hard_rule_ids=[]
        ),
        10: GateCollaboration(
            gate_number=10,
            gate_name="父子链落档",
            main_persona=PersonaEnum.P15_QIAOQIANDAI,
            assist_personas=[PersonaEnum.P05_GODSEYE],
            hard_rule_ids=[4, 5]
        ),
    }

    # 熔断权配置
    FUSE_RIGHTS = {
        PersonaEnum.P05_GODSEYE: PersonaFuseRight(
            persona=PersonaEnum.P05_GODSEYE,
            has_independent_fuse=True,
            gates_fuse_authority=[1, 2, 5, 10]
        ),
        PersonaEnum.P72_LONGSHIELD: PersonaFuseRight(
            persona=PersonaEnum.P72_LONGSHIELD,
            has_independent_fuse=True,
            gates_fuse_authority=[1, 2, 5, 10]
        ),
    }

    @classmethod
    def get_gate_config(cls, gate_number: int) -> Optional[GateCollaboration]:
        """获取闸口协作配置"""
        return cls.STANDARD_GATES.get(gate_number)

    @classmethod
    def get_all_gates(cls) -> Dict[int, GateCollaboration]:
        """获取所有闸口配置"""
        return cls.STANDARD_GATES.copy()

    @classmethod
    def validate_iron_law_1_all(cls) -> Tuple[bool, List[str]]:
        """验证铁律1：所有闸的一闸一主"""
        errors = []
        for gate_num, gate in cls.STANDARD_GATES.items():
            valid, msg = gate.validate_iron_law_1()
            if not valid:
                errors.append(f"闸{gate_num}({gate.gate_name}): {msg}")
        return len(errors) == 0, errors

    @classmethod
    def validate_iron_law_2(cls) -> Tuple[bool, List[str]]:
        """验证铁律2：熔断独立权"""
        errors = []
        for persona, fuse_right in cls.FUSE_RIGHTS.items():
            if not fuse_right.has_independent_fuse:
                errors.append(f"{persona.value}无独立熔断权")
        return len(errors) == 0, errors

    @classmethod
    def validate_iron_law_5(cls) -> Tuple[bool, str]:
        """验证铁律5：路由权姜子牙独占"""
        gate_8 = cls.get_gate_config(8)
        if gate_8.main_persona != PersonaEnum.P13_JIANGZIYA:
            return False, "九宫派位主驻人格不是P13"
        return True, "验证通过"

    @classmethod
    def validate_iron_law_6(cls) -> Tuple[bool, str]:
        """验证铁律6：写档权乔前辈独占"""
        gate_10 = cls.get_gate_config(10)
        if gate_10.main_persona != PersonaEnum.P15_QIAOQIANDAI:
            return False, "父子链落档主驻人格不是P15"
        return True, "验证通过"

    @classmethod
    def create_gate_receipt(
        cls,
        gate_number: int,
        signal: str,
        hard_rule_triggered: str = ""
    ) -> Optional[GateReceipt]:
        """创建闸口回执"""
        gate_config = cls.get_gate_config(gate_number)
        if not gate_config:
            return None

        return GateReceipt(
            gate_name=gate_config.gate_name,
            gate_number=gate_number,
            main_persona=gate_config.main_persona,
            assist_personas=gate_config.assist_personas,
            hard_rule_triggered=hard_rule_triggered,
            signal=signal
        )

    @classmethod
    def can_fuse(cls, persona: PersonaEnum, gate_number: int) -> bool:
        """检查人格是否有该闸的熔断权"""
        fuse_right = cls.FUSE_RIGHTS.get(persona)
        if not fuse_right:
            return False
        if fuse_right.has_independent_fuse:
            return True
        return gate_number in fuse_right.gates_fuse_authority


# 硬闸与人格对应关系
HARDLAW_PERSONA_MAP = {
    1: [(PersonaEnum.P05_GODSEYE, "主"), (PersonaEnum.P72_LONGSHIELD, "辅")],
    2: [(PersonaEnum.P05_GODSEYE, "主"), (PersonaEnum.P72_LONGSHIELD, "辅")],
    3: [(PersonaEnum.P03_WANWAN, "主"), (PersonaEnum.P05_GODSEYE, "辅"), (PersonaEnum.P72_LONGSHIELD, "辅")],
    4: [(PersonaEnum.P03_WANWAN, "主"), (PersonaEnum.P05_GODSEYE, "辅")],
    5: [(PersonaEnum.P72_LONGSHIELD, "主")],
    6: [(PersonaEnum.P00_WENXIN, "主")],
    7: [(PersonaEnum.P01_ZHUGELVLIANG, "主")],
    8: [(PersonaEnum.P13_JIANGZIYA, "主"), (PersonaEnum.P14_LVMENG, "辅")],
    9: [(PersonaEnum.P00_WENXIN, "主"), (PersonaEnum.P01_ZHUGELVLIANG, "辅")],
    10: [(PersonaEnum.P15_QIAOQIANDAI, "主"), (PersonaEnum.P05_GODSEYE, "辅")],
}


def get_hardlaw_personas(hardlaw_id: int) -> List[Tuple[PersonaEnum, str]]:
    """获取硬闸对应的人格(id, 角色)"""
    return HARDLAW_PERSONA_MAP.get(hardlaw_id, [])
