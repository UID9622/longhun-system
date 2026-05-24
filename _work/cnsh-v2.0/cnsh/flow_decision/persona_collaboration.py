# -*- coding: utf-8 -*-
"""人格协作闸口（§1 表 + §1.1 六条铁律校验）"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class GateDef:
    name: str
    main: str
    aux: Tuple[str, ...]
    receipt_prefix: str


GATES: Tuple[GateDef, ...] = (
    GateDef("签章闸", "P05", ("P72",), "gate:sign"),
    GateDef("隐私闸", "P03", ("P05", "P72"), "gate:privacy"),
    GateDef("数字根闸", "P06", (), "gate:dr"),
    GateDef("五行映射", "P06", (), "wuxing:map"),
    GateDef("三色闸", "P05", (), "gate:audit"),
    GateDef("三才闸", "P00", ("P01",), "gate:sancai"),
    GateDef("生克闸", "P01", (), "gate:shengke"),
    GateDef("九宫派位", "P13", ("P14",), "palace:route"),
    GateDef("沙盒分拣", "P03", ("P15",), "sandbox:bucket"),
    GateDef("父子链落档", "P15", ("P05",), "dna:chain"),
)


def assert_one_primary_per_gate() -> bool:
    return all(g.main for g in GATES)


def jiang_ziya_exclusive_palace() -> bool:
    """铁律5：九宫派位主驻唯一 P13"""
    g = [x for x in GATES if x.name == "九宫派位"][0]
    return g.main == "P13" and "P14" in g.aux


def qiao_exclusive_write() -> bool:
    """铁律6：写档主驻 P15"""
    g = [x for x in GATES if x.name == "父子链落档"][0]
    return g.main == "P15"
