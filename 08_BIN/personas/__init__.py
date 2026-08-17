#龍芯⚡️丙午·丙申·庚戌·亥时·䷙大畜-PERSONA-EXEC-MODULE-INIT-v4.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂人格执行器模块（24人格全注册版）
Persona Executors Module

DNA: #龍芯⚡️丙午·丙申·庚戌·亥时·䷙大畜-PERSONA-EXEC-MODULE-INIT-v4.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼♀️❤️♾️-DEVICE-BIND-SOUL

责任: UID9622·不免责
每個人格執行器 = 可調用的 Python 模塊，不是空殼文檔。

v4.0(2026-08-17): 24人格全注册(P00-P15/P18/P19/P20/P72/P77/S1-S3)
· 修复 P02/P03/P09 import 断链(执行器改名对齐: longxin→baobao / mozi→wenwen / daoyin→sunsi)
· 对齐唯一口径表: 20_CONFIG/persona-canonical-table.md
"""

from .p00_wenxin import P00Wenxin
from .p01_zhugeliang import P01Zhugeliang
from .p02_baobao import P02Longxin
from .p03_wenwen import P03Mozi
from .p04_luban import P04Luban
from .p05_godseye import P05Godseye
from .p06_mathmaster import P06Mathmaster
from .p07_guanzhong import P07Guanzhong
from .p08_cangjie import P08Cangjie
from .p09_sunsi import P09Sunsi
from .p10_sudongpo import P10Sudongpo
from .p11_libai import P11Libai
from .p12_quyuan import P12Quyuan
from .p13_jiangziya import P13Jiang
from .p14_lvmeng import P14Lvmeng
from .p15_qiao import P15Qiao
from .p18_registrar import P18Registrar
from .p19_auditor import P19Auditor
from .p20_trust import P20Trust
from .p72_longdun import P72Longdun
from .p77_security import P77Security
from .s1_legal import S1Legal
from .s2_luoshu import S2Luoshu
from .s3_civil import S3Civil

__all__ = [
    "P00Wenxin",
    "P01Zhugeliang",
    "P02Longxin",
    "P03Mozi",
    "P04Luban",
    "P05Godseye",
    "P06Mathmaster",
    "P07Guanzhong",
    "P08Cangjie",
    "P09Sunsi",
    "P10Sudongpo",
    "P11Libai",
    "P12Quyuan",
    "P13Jiang",
    "P14Lvmeng",
    "P15Qiao",
    "P18Registrar",
    "P19Auditor",
    "P20Trust",
    "P72Longdun",
    "P77Security",
    "S1Legal",
    "S2Luoshu",
    "S3Civil",
]

# 人格執行器註冊表（與 orchestrator 對接 · v4.0 24人格全注册）
PERSONA_EXECUTORS = {
    "P00": P00Wenxin,
    "P01": P01Zhugeliang,
    "P02": P02Longxin,
    "P03": P03Mozi,
    "P04": P04Luban,
    "P05": P05Godseye,
    "P06": P06Mathmaster,
    "P07": P07Guanzhong,
    "P08": P08Cangjie,
    "P09": P09Sunsi,
    "P10": P10Sudongpo,
    "P11": P11Libai,
    "P12": P12Quyuan,
    "P13": P13Jiang,
    "P14": P14Lvmeng,
    "P15": P15Qiao,
    "P18": P18Registrar,
    "P19": P19Auditor,
    "P20": P20Trust,
    "P72": P72Longdun,
    "P77": P77Security,
    "S1": S1Legal,
    "S2": S2Luoshu,
    "S3": S3Civil,
}


def get_executor(persona_code: str):
    """獲取人格執行器實例"""
    cls = PERSONA_EXECUTORS.get(persona_code.upper())
    if cls is None:
        return None
    return cls()
