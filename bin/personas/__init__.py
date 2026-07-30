#龍芯⚡️丙午·乙未·甲寅·酉时·需-PERSONA-EXEC-MODULE-INIT-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂人格执行器模块
Persona Executors Module

DNA: #龍芯⚡️丙午·乙未·甲寅·酉时·需-PERSONA-EXEC-MODULE-INIT-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

责任: UID9622·不免责
每個人格執行器 = 可調用的 Python 模塊，不是空殼文檔。
"""

from .p01_zhugeliang import P01Zhugeliang
from .p02_longxin import P02Longxin
from .p03_mozi import P03Mozi
from .p05_godseye import P05Godseye
from .p06_mathmaster import P06Mathmaster
from .p09_daoyin import P09Daoyin
from .p14_lvmeng import P14Lvmeng
from .p18_registrar import P18Registrar
from .p19_auditor import P19Auditor
from .p20_trust import P20Trust

__all__ = [
    "P01Zhugeliang",
    "P02Longxin",
    "P03Mozi",
    "P05Godseye",
    "P06Mathmaster",
    "P09Daoyin",
    "P14Lvmeng",
    "P18Registrar",
    "P19Auditor",
    "P20Trust",
]

# 人格執行器註冊表（與 orchestrator 對接）
PERSONA_EXECUTORS = {
    "P01": P01Zhugeliang,
    "P02": P02Longxin,
    "P03": P03Mozi,
    "P05": P05Godseye,
    "P06": P06Mathmaster,
    "P09": P09Daoyin,
    "P14": P14Lvmeng,
    "P18": P18Registrar,
    "P19": P19Auditor,
    "P20": P20Trust,
}

def get_executor(persona_code: str):
    """獲取人格執行器實例"""
    cls = PERSONA_EXECUTORS.get(persona_code.upper())
    if cls is None:
        return None
    return cls()
