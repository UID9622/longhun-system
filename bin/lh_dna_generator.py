#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂·DNA追溯码生成器 v2.0
DNA: #龍芯⚡️丙午·乙未·甲辰·离为火-DNA生成器-v2.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

双维度DNA体系：
  A）文档/模块DNA — 文件·代码·协议·引擎的追溯码（v∞干支卦格式）
  B）人物DNA — 一世一双人·身份绑定·族谱继承（v1.0格式）

DNA格式（v∞推荐）:
  #龍芯⚡️<年柱>·<月柱>·<日柱>·<时辰>·<卦象符号><卦名>-<模块>-<动作>-<版本>-<哈希8>

示例（文档/模块）:
  #龍芯⚡️丙午·乙未·甲辰·申时·䷜坎-安全检查-引擎-v1.0-A3B9C2D1
  #龍芯⚡️丙午·乙未·甲辰·午时·䷀乾-BENCHMARK-ALLOC-v2.1-1A2B3C4D

示例（人物）:
  #龍芯⚡️丙午·乙未·甲辰·离为火-龙芯1990-v1.0-ABCD1234

核心功能：
  1. 文档/模块DNA — 基于内容哈希+干支四柱+梅花易数起卦
  2. 人物DNA — 一世一双人·实名绑定·族谱继承
  3. 精确干支计算 — 年柱(公元4年基准)·月柱(五虎遁)·日柱(序数公式)·时辰(十二时辰)
  4. 六十四卦映射 — 模块→卦德·梅花易数起卦·384爻辞
  5. HMAC双签名 — 内容签名+GPG签名·防篡改验证链
  6. DNA注册表 — SQLite永久记录·审计日志·抗删除
  7. 族谱系统 — 继承链·深度限制·后代追溯
"""

import os
import sys
import json
import hashlib
import hmac
import time
import sqlite3
import argparse
import re
import uuid
import getpass
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, field, asdict
from enum import Enum

# ═══════════════════════════════════════════════════════════
# 一、配置
# ═══════════════════════════════════════════════════════════

BASE_DIR = Path.home() / ".longhun/dna"
BASE_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = BASE_DIR / "dna_registry.db"
CONFIG_PATH = BASE_DIR / "dna_config.json"

# DNA v∞ 格式正则
DNA_VINF_PATTERN = re.compile(
    r'^#龍芯⚡️[\u4e00-\u9fa5]+·[\u4e00-\u9fa5]+·[\u4e00-\u9fa5]+·[\u4e00-\u9fa5]+·[\u4e00-\u9fa5䷀-䷿]+-[A-Za-z0-9]+-[A-Z]+-v[\d.]+-[A-F0-9]{8}$'
)
# DNA v1.0 格式正则（人物DNA）
DNA_PERSON_PATTERN = re.compile(
    r'^#龍芯⚡️[\u4e00-\u9fa5]+·[\u4e00-\u9fa5]+·[\u4e00-\u9fa5]+·[\u4e00-\u9fa5]+-[A-Za-z0-9]+-v[\d.]+-[A-F0-9]{8}$'
)

GPG_KEY = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
HMAC_SECRET = "LONGHUN_DNA_SALT_V2_9622"

DEFAULT_CONFIG = {
    "version": "2.0",
    "dna_prefix": "#龍芯⚡️",
    "hash_length": 8,
    "hash_algorithm": "sha256",
    "max_inheritance_depth": 5,
    "require_real_name": True,
    "auto_gpg_sign": False,
}

# ============================================================
# 二、干支四柱精确计算（v∞引擎）
# ============================================================

十天干 = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
十二地支 = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
十二时辰名 = ["子时", "丑时", "寅时", "卯时", "辰时", "巳时",
              "午时", "未时", "申时", "酉时", "戌时", "亥时"]

# 八卦基础
八卦名 = ["乾", "兑", "离", "震", "巽", "坎", "艮", "坤"]
八卦象 = {"乾": "☰", "兑": "☱", "离": "☲", "震": "☳", "巽": "☴", "坎": "☵", "艮": "☶", "坤": "☷"}
八卦德 = {"乾": "天·健", "兑": "泽·悦", "离": "火·明", "震": "雷·动",
          "巽": "风·入", "坎": "水·流", "艮": "山·止", "坤": "地·藏"}
八卦五行 = {"乾": "金", "兑": "金", "离": "火", "震": "木", "巽": "木", "坎": "水", "艮": "土", "坤": "土"}

# 64卦表：上卦(0-7)×8 + 下卦(0-7)
六十四卦表 = {
    0:  "䷀乾为天", 1:  "䷫天风姤", 2:  "䷌天火同人", 3:  "䷉天泽履",
    4:  "䷈风天小畜", 5:  "䷍火天大有", 6:  "䷊地天泰", 7:  "䷋天地否",
    8:  "䷠天山遯", 9:  "䷞泽山咸", 10: "䷢火地晋", 11: "䷎地山谦",
    12: "䷽雷山小过", 13: "䷵雷泽归妹", 14: "䷼风泽中孚", 15: "䷻水泽节",
    16: "䷤风火家人", 17: "䷰泽火革", 18: "䷝离为火", 19: "䷶雷火丰",
    20: "䷣地火明夷", 21: "䷔火雷噬嗑", 22: "䷀乾为天", 23: "䷕山火贲",
    24: "䷩风雷益", 25: "䷐泽雷随", 26: "䷔火雷噬嗑", 27: "䷲震为雷",
    28: "䷟雷风恒", 29: "䷧雷水解", 30: "䷵雷泽归妹", 31: "䷽雷山小过",
    32: "䷓风地观", 33: "䷑山风蛊", 34: "䷱火风鼎", 35: "䷟雷风恒",
    36: "䷸巽为风", 37: "䷼风泽中孚", 38: "䷺风水涣", 39: "䷴风山渐",
    40: "䷅天水讼", 41: "䷮泽水困", 42: "䷿火水未济", 43: "䷧雷水解",
    44: "䷺风水涣", 45: "䷜坎为水", 46: "䷃山水蒙", 47: "䷦水山蹇",
    48: "䷠天山遯", 49: "䷞泽山咸", 50: "䷃山水蒙", 51: "䷽雷山小过",
    52: "䷴风山渐", 53: "䷦水山蹇", 54: "䷳艮为山", 55: "䷎地山谦",
    56: "䷇水地比", 57: "䷬泽地萃", 58: "䷢火地晋", 59: "䷏雷地豫",
    60: "䷓风地观", 61: "䷇水地比", 62: "䷖山地剥", 63: "䷁坤为地",
}

# 模块→卦德映射（按关键词长度降序匹配）
模块宫映射: Dict[str, str] = {
    "CODEBUDDY": "乾", "ALIGNMENT": "乾", "CONSTITUTION": "乾",
    "GOVERNANCE": "乾", "PROTOCOL": "乾", "WHITE": "乾", "RULES": "乾",
    "REGISTER-MAIL": "坎", "DUALVIEW": "离", "DASHBOARD": "离",
    "SOVEREIGNTY": "艮", "PRIVACY": "艮",
    "INTEGRATION": "离", "PERSONA": "巽", "PHEROMONE": "巽",
    "SCHEDULE": "巽", "SOLDIER": "震", "MELTDOWN": "震",
    "SECURITY": "震", "CRAWLER": "坎", "STREAM": "坎",
    "ARCHIVE": "坤", "BACKUP": "坤", "MEMORY": "坤",
    "SCOUT": "坎", "NOTIFY": "坎", "MAIL": "坎",
    "GUARD": "震", "MINOR": "震", "ALARM": "震", "DNA": "震",
    "QUEEN": "巽", "WORKER": "巽", "ROUTE": "巽",
    "TRUST": "兑", "ECOM": "兑", "ECO": "兑", "REGISTER": "兑",
    "NAMING": "乾", "MATH": "离", "AUDIT": "离", "TEST": "离",
    "MODEL": "巽", "DEPLOY": "巽", "TRAIN": "巽",
    "DATA": "坤", "SYNC": "坎", "TAIJI": "坎", "STATE": "离",
    "ENGINE": "坎", "RISK": "乾", "RULE": "乾", "GATE": "艮",
    "SKILL": "兑", "FEED": "坤", "SEARCH": "离", "API": "离",
    "WEB": "离", "PORTAL": "离", "AUTH": "乾", "SIGN": "乾",
}
_模块宫排序列表 = sorted(模块宫映射.keys(), key=len, reverse=True)


class 干支引擎:
    """精确干支四柱计算（v∞标准）"""

    @staticmethod
    def 年干支(year: int = None) -> str:
        """年柱：公元4年为甲子年基准"""
        if year is None:
            year = datetime.now().year
        base = year - 4
        gan = 十天干[base % 10]
        zhi = 十二地支[base % 12]
        return gan + zhi

    @staticmethod
    def 月干支(year: int = None, month: int = None) -> Tuple[str, str]:
        """
        月柱（五虎遁法）：
        甲己之年丙作首，乙庚之岁戊为头，
        丙辛必定寻庚起，丁壬壬位顺行流，
        若问戊癸何方发，甲寅之上好追求。
        """
        if year is None: year = datetime.now().year
        if month is None: month = datetime.now().month

        # 月支映射：寅月=2月... (立春后算寅月)
        月支映射 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0]
        月支_idx = 月支映射[month - 1]

        # 年干决定寅月天干
        年干 = 十天干.index(干支引擎.年干支(year)[0])
        寅月干映射 = [2, 4, 6, 8, 0, 2, 4, 6, 8, 0]
        寅月干 = 寅月干映射[年干]

        offset = (月支_idx - 2) % 12
        月干 = (寅月干 + offset) % 10

        return 十天干[月干] + 十二地支[月支_idx], 十二地支[月支_idx]

    @staticmethod
    def 日干支(year: int = None, month: int = None, day: int = None) -> str:
        """
        日柱（精确序数公式）：
        基数 = (年尾+7)*5 + 15 + (年尾+19)/4 取整
        日干支序 = (基数 + 第N天) % 60
        """
        if year is None: year = datetime.now().year
        if month is None: month = datetime.now().month
        if day is None: day = datetime.now().day

        yy = year % 100
        base = (yy + 7) * 5 + 15 + (yy + 19) // 4
        base %= 60

        is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
        月天数 = [31, 29 if is_leap else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        day_of_year = sum(月天数[:month - 1]) + day

        seq = (base + day_of_year) % 60
        gan = 十天干[(seq - 1) % 10]
        zhi = 十二地支[(seq - 1) % 12]
        return gan + zhi

    @staticmethod
    def 时辰(hour: int = None) -> str:
        """时柱：23-1子时, 1-3丑时, ..."""
        if hour is None:
            hour = datetime.now().hour
        idx = ((hour + 1) // 2) % 12
        return 十二时辰名[idx]

    @staticmethod
    def 当前四柱(ts: datetime = None) -> Tuple[str, str, str, str]:
        """返回 (年柱, 月柱, 日柱, 时辰)"""
        if ts is None:
            ts = datetime.now()
        nian = 干支引擎.年干支(ts.year)
        yue, _ = 干支引擎.月干支(ts.year, ts.month)
        ri = 干支引擎.日干支(ts.year, ts.month, ts.day)
        shi = 干支引擎.时辰(ts.hour)
        return nian, yue, ri, shi

    @staticmethod
    def 梅花起卦(content: str = "", ts: datetime = None) -> str:
        """
        梅花易数起卦：
        - 有内容 → SHA256首2字节确定上下卦
        - 无内容 → 时间戳起卦
        返回卦象符号+卦名，如 '䷜坎为水'
        """
        if ts is None:
            ts = datetime.now()
        if content:
            h = hashlib.sha256(content.encode()).digest()
            upper = h[0] % 8
            lower = h[1] % 8
        else:
            t = int(ts.timestamp())
            upper = t % 8
            lower = (t // 60) % 8
        return 六十四卦表[upper * 8 + lower]

    @staticmethod
    def 模块起卦(module: str) -> str:
        """模块名→卦德匹配，按关键词长度降序"""
        m = module.upper()
        for kw in _模块宫排序列表:
            if kw in m:
                gua_name = 模块宫映射[kw]
                gua_idx = 八卦名.index(gua_name)
                return 六十四卦表[gua_idx * 8 + gua_idx]  # 纯卦
        return 六十四卦表[5 * 8 + 5]  # 默认坎为水


# ═══════════════════════════════════════════════════════════
# 三、数据结构
# ═══════════════════════════════════════════════════════════

class DNA类型(Enum):
    文档 = "📄 文档DNA"
    模块 = "🧩 模块DNA"
    人物 = "👤 人物DNA"
    引擎 = "⚙️ 引擎DNA"
    协议 = "📜 协议DNA"


class DNA状态(Enum):
    活跃 = "🟢 活跃"
    已继承 = "🟡 已继承"
    已冻结 = "🔴 已冻结"
    已撤销 = "⚫ 已撤销"


@dataclass
class DNA元数据:
    """DNA附加元数据"""
    创建者: str = "UID9622"
    来源: str = "本地生成"
    优先级: str = "P0"
    描述: str = ""
    标签: List[str] = field(default_factory=list)
    关联文件: str = ""
    关联引擎: str = ""


@dataclass
class DNA记录:
    """文档/模块DNA记录"""
    dna: str
    类型: DNA类型
    模块名: str
    动作: str
    版本: str
    哈希值: str
    干支四柱: str          # 年·月·日·时
    卦象: str              # 卦象符号+卦名
    内容指纹: str           # SHA256 of content
    hmac签名: str           # HMAC-SHA256
    元数据: DNA元数据 = field(default_factory=DNA元数据)
    创建时间: str = ""
    状态: DNA状态 = DNA状态.活跃
    父DNA: Optional[str] = None


@dataclass
class DNAPerson:
    """人物DNA — 一世一双人"""
    dna: str
    real_name: str
    id_type: str
    id_number: str
    born_date: str
    gender: str
    birthplace: str
    current_location: str
    parent_dna: Optional[str] = None
    children_dna: List[str] = field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""
    status: str = "active"
    gpg_fingerprint: Optional[str] = None
    dna_signature: Optional[str] = None
    notes: str = ""

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class DNAInheritance:
    """人物DNA继承记录"""
    id: int = 0
    from_dna: str = ""
    to_dna: str = ""
    relation: str = ""
    inheritance_time: str = ""
    reason: str = "自然传承"
    witness_dna: Optional[str] = None
    notes: str = ""


# ═══════════════════════════════════════════════════════════
# 四、DNA生成器（文档/模块维度）
# ═══════════════════════════════════════════════════════════

class 文档DNA生成器:
    """文档/模块DNA生成器 — v∞干支卦格式"""

    def __init__(self):
        self.registry = DNA注册表()

    @staticmethod
    def _生成哈希(seed: str, length: int = 8) -> str:
        return hashlib.sha256(seed.encode()).hexdigest()[:length].upper()

    @staticmethod
    def _HMAC签名(dna: str, content: str = "") -> str:
        """HMAC-SHA256 双重签名"""
        secret = f"{HMAC_SECRET}{GPG_KEY[:16]}"
        payload = f"{dna}{content}" if content else dna
        return hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()[:16]

    @staticmethod
    def _内容指纹(content: str) -> str:
        """生成内容SHA256指纹"""
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def 生成文档DNA(
        self,
        模块名: str,
        动作: str = "DOC",
        版本: str = "1.0",
        内容: str = "",
        元数据: Optional[DNA元数据] = None,
        类型: DNA类型 = DNA类型.文档
    ) -> DNA记录:
        """生成文档/模块DNA（v∞格式）"""
        ts = datetime.now()
        nian, yue, ri, shi = 干支引擎.当前四柱(ts)
        卦象 = 干支引擎.梅花起卦(content, ts) if content else 干支引擎.模块起卦(模块名)

        # 组装DNA主体
        干支 = f"{nian}·{yue}·{ri}·{shi}"
        种子 = f"{模块名}{动作}{版本}{ts.isoformat()}{uuid.uuid4().hex}"
        哈希 = self._生成哈希(种子)

        dna = f"#龍芯⚡️{干支}·{卦象}-{模块名}-{动作}-v{版本}-{哈希}"

        # 内容指纹
        fingerprint = self._内容指纹(content) if content else ""

        # HMAC签名
        signature = self._HMAC签名(dna, content)

        if 元数据 is None:
            元数据 = DNA元数据(创建者="UID9622", 来源="自动生成")

        record = DNA记录(
            dna=dna,
            类型=类型,
            模块名=模块名,
            动作=动作,
            版本=版本,
            哈希值=哈希,
            干支四柱=干支,
            卦象=卦象,
            内容指纹=fingerprint,
            hmac签名=signature,
            元数据=元数据,
            创建时间=ts.isoformat(),
            状态=DNA状态.活跃,
        )

        self.registry.注册文档DNA(record)
        return record

    def 批量生成(self, 条目列表: List[Dict]) -> List[DNA记录]:
        """批量生成DNA"""
        results = []
        for item in 条目列表:
            模块名 = item.get("模块名", item.get("module", "UNKNOWN"))
            动作 = item.get("动作", item.get("action", "DOC"))
            版本 = item.get("版本", item.get("version", "1.0"))
            内容 = item.get("内容", item.get("content", ""))
            类型标识 = item.get("类型", "文档")
            类型映射 = {"文档": DNA类型.文档, "模块": DNA类型.模块,
                       "引擎": DNA类型.引擎, "协议": DNA类型.协议}
            类型 = 类型映射.get(类型标识, DNA类型.文档)
            results.append(self.生成文档DNA(模块名, 动作, 版本, 内容, 类型=类型))
        return results

    def 验证(self, dna: str, 内容: str = "") -> Tuple[bool, str]:
        """验证DNA：格式→注册→HMAC签名三重验证"""
        # 1. 格式验证
        if not DNA_VINF_PATTERN.match(dna) and not DNA_PERSON_PATTERN.match(dna):
            return False, "格式不匹配v∞或v1.0正则"

        # 2. 注册表验证
        record = self.registry.查文档DNA(dna)
        if not record:
            return False, "DNA未在注册表中找到"

        # 3. HMAC签名验证
        if 内容:
            expected_sig = self._HMAC签名(dna, 内容)
            if record.hmac签名 != expected_sig:
                return False, f"HMAC签名不匹配"

        return True, "验证通过"

    def 查询(self, dna: str) -> Optional[DNA记录]:
        return self.registry.查文档DNA(dna)

    def 按模块查询(self, 模块名: str) -> List[DNA记录]:
        return self.registry.查文档DNA按模块(模块名)

    def 按类型统计(self) -> Dict:
        return self.registry.文档DNA统计()


# ═══════════════════════════════════════════════════════════
# 五、DNA生成器（人物维度）— 保留v1.0兼容
# ═══════════════════════════════════════════════════════════

class 人物DNA生成器:
    """人物DNA生成器 — 一世一双人"""

    def __init__(self):
        self.registry = DNA注册表()

    @staticmethod
    def _生成人物DNA字符串(实名: str, 身份证号: str, 出生日期: str) -> str:
        ts = datetime.now()
        nian, yue, ri, shi = 干支引擎.当前四柱(ts)
        卦象 = 干支引擎.梅花起卦(f"{实名}{身份证号}", ts)
        人标识 = f"{实名[:2]}{出生日期[:4]}"
        哈希 = hashlib.sha256(f"{实名}{身份证号}{ts.isoformat()}{uuid.uuid4().hex}".encode()).hexdigest()[:8].upper()
        return f"#龍芯⚡️{nian}·{yue}·{ri}·{卦象}-{人标识}-v1.0-{哈希}"

    def 生成(self, real_name: str, id_type: str, id_number: str,
            born_date: str, gender: str, birthplace: str,
            current_location: str, parent_dna: str = None,
            gpg_fingerprint: str = None) -> DNAPerson:
        existing = self.registry.查人物DNA(real_name, id_number)
        if existing:
            raise ValueError(f"❌ {real_name} 已注册DNA: {existing.dna}")

        if parent_dna:
            parent = self.registry.查人物DNA_by_dna(parent_dna)
            if not parent: raise ValueError(f"❌ 父DNA不存在: {parent_dna}")
            if parent.status != "active": raise ValueError(f"❌ 父DNA状态异常")
            depth = self.registry.继承深度(parent_dna)
            if depth >= DEFAULT_CONFIG["max_inheritance_depth"]:
                raise ValueError(f"❌ 继承深度已达上限")

        dna = self._生成人物DNA字符串(real_name, id_number, born_date)

        signature = hmac.new(
            f"{real_name}{id_number}LONGHUN_DNA_SALT".encode(),
            dna.encode(), hashlib.sha256
        ).hexdigest()[:16]

        person = DNAPerson(
            dna=dna, real_name=real_name, id_type=id_type,
            id_number=id_number, born_date=born_date, gender=gender,
            birthplace=birthplace, current_location=current_location,
            parent_dna=parent_dna, gpg_fingerprint=gpg_fingerprint,
            dna_signature=signature,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            status="active", notes="一世一双人，DNA不可转让。"
        )

        self.registry.注册人物DNA(person)
        if parent_dna:
            self.registry.添加继承(parent_dna, dna, "父子/母女", "自然传承")
        return person

    def 验证(self, dna: str, real_name: str, id_number: str) -> bool:
        person = self.registry.查人物DNA_by_dna(dna)
        if not person: return False
        if person.real_name != real_name or person.id_number != id_number:
            return False
        expected = hmac.new(
            f"{real_name}{id_number}LONGHUN_DNA_SALT".encode(),
            dna.encode(), hashlib.sha256
        ).hexdigest()[:16]
        return person.dna_signature == expected

    def 查询(self, dna: str) -> Optional[DNAPerson]:
        return self.registry.查人物DNA_by_dna(dna)

    def 按身份证查询(self, id_number: str) -> Optional[DNAPerson]:
        return self.registry.查人物DNA_by_id(id_number)

    def 统计(self) -> Dict:
        return self.registry.人物DNA统计()


# ═══════════════════════════════════════════════════════════
# 六、DNA注册表（SQLite · 双维度）
# ═══════════════════════════════════════════════════════════

class DNA注册表:
    """DNA注册表 — SQLite持久化 · 审计日志 · 防篡改"""

    def __init__(self, db_path: Path = None):
        self.db_path = db_path or DB_PATH
        self._建表()

    def _建表(self):
        conn = sqlite3.connect(str(self.db_path))
        # 文档/模块DNA表
        conn.execute("""
            CREATE TABLE IF NOT EXISTS doc_dna (
                dna TEXT PRIMARY KEY,
                类型 TEXT NOT NULL,
                模块名 TEXT NOT NULL,
                动作 TEXT NOT NULL,
                版本 TEXT NOT NULL,
                哈希值 TEXT NOT NULL,
                干支四柱 TEXT NOT NULL,
                卦象 TEXT NOT NULL,
                内容指纹 TEXT,
                hmac签名 TEXT NOT NULL,
                元数据 JSON,
                创建时间 TEXT NOT NULL,
                状态 TEXT DEFAULT '活跃',
                父DNA TEXT
            )
        """)
        # 人物DNA表
        conn.execute("""
            CREATE TABLE IF NOT EXISTS person_dna (
                dna TEXT PRIMARY KEY,
                real_name TEXT NOT NULL,
                id_type TEXT NOT NULL,
                id_number TEXT NOT NULL UNIQUE,
                born_date TEXT NOT NULL,
                gender TEXT NOT NULL,
                birthplace TEXT,
                current_location TEXT,
                parent_dna TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                status TEXT DEFAULT 'active',
                gpg_fingerprint TEXT,
                dna_signature TEXT,
                notes TEXT
            )
        """)
        # 继承表
        conn.execute("""
            CREATE TABLE IF NOT EXISTS inheritance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_dna TEXT NOT NULL,
                to_dna TEXT NOT NULL,
                relation TEXT NOT NULL,
                inheritance_time TEXT NOT NULL,
                reason TEXT DEFAULT '自然传承',
                witness_dna TEXT,
                notes TEXT
            )
        """)
        # 统一审计日志
        conn.execute("""
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                操作 TEXT NOT NULL,
                维度 TEXT NOT NULL,
                dna TEXT,
                详情 TEXT,
                操作者 TEXT,
                时间 TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def _审计(self, 操作: str, 维度: str, dna: str, 详情: str = ""):
        conn = sqlite3.connect(str(self.db_path))
        conn.execute(
            "INSERT INTO audit_log (操作, 维度, dna, 详情, 操作者, 时间) VALUES (?,?,?,?,?,?)",
            (操作, 维度, dna, 详情, "system", datetime.now().isoformat())
        )
        conn.commit()
        conn.close()

    # --- 文档DNA CRUD ---
    def 注册文档DNA(self, record: DNA记录):
        conn = sqlite3.connect(str(self.db_path))
        try:
            conn.execute("""
                INSERT INTO doc_dna (dna, 类型, 模块名, 动作, 版本, 哈希值, 干支四柱, 卦象,
                                     内容指纹, hmac签名, 元数据, 创建时间, 状态, 父DNA)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                record.dna, record.类型.value, record.模块名, record.动作,
                record.版本, record.哈希值, record.干支四柱, record.卦象,
                record.内容指纹, record.hmac签名,
                json.dumps(asdict(record.元数据), ensure_ascii=False),
                record.创建时间, record.状态.value, record.父DNA
            ))
            conn.commit()
            self._审计("注册", "文档", record.dna, f"模块:{record.模块名} 动作:{record.动作}")
        except sqlite3.IntegrityError as e:
            raise ValueError(f"DNA注册失败（可能已存在）: {e}")
        finally:
            conn.close()

    def 查文档DNA(self, dna: str) -> Optional[DNA记录]:
        conn = sqlite3.connect(str(self.db_path))
        cur = conn.execute("SELECT * FROM doc_dna WHERE dna = ?", (dna,))
        row = cur.fetchone()
        conn.close()
        if row:
            return self._行转文档DNA(row)
        return None

    def 查文档DNA按模块(self, 模块名: str) -> List[DNA记录]:
        conn = sqlite3.connect(str(self.db_path))
        cur = conn.execute("SELECT * FROM doc_dna WHERE 模块名 = ? ORDER BY 创建时间 DESC", (模块名,))
        rows = cur.fetchall()
        conn.close()
        return [self._行转文档DNA(row) for row in rows]

    def 查文档DNA历史(self, limit: int = 20) -> List[DNA记录]:
        conn = sqlite3.connect(str(self.db_path))
        cur = conn.execute("SELECT * FROM doc_dna ORDER BY 创建时间 DESC LIMIT ?", (limit,))
        rows = cur.fetchall()
        conn.close()
        return [self._行转文档DNA(row) for row in rows]

    def 文档DNA统计(self) -> Dict:
        conn = sqlite3.connect(str(self.db_path))
        cur = conn.execute("SELECT COUNT(*) FROM doc_dna")
        total = cur.fetchone()[0]
        cur = conn.execute("SELECT 类型, COUNT(*) FROM doc_dna GROUP BY 类型")
        类型分布 = {row[0]: row[1] for row in cur.fetchall()}
        cur = conn.execute("SELECT COUNT(DISTINCT 模块名) FROM doc_dna")
        modules = cur.fetchone()[0]
        conn.close()
        return {"总数": total, "模块数": modules, "类型分布": 类型分布}

    def _行转文档DNA(self, row) -> DNA记录:
        元数据_dict = json.loads(row[9]) if row[9] else {}
        return DNA记录(
            dna=row[0],
            类型=next((t for t in DNA类型 if t.value == row[1]), DNA类型.文档),
            模块名=row[2],
            动作=row[3],
            版本=row[4],
            哈希值=row[5],
            干支四柱=row[6],
            卦象=row[7],
            内容指纹=row[8] or "",
            hmac签名=row[9],
            元数据=DNA元数据(**元数据_dict) if 元数据_dict else DNA元数据(),
            创建时间=row[10],
            状态=next((s for s in DNA状态 if s.value == row[11]), DNA状态.活跃),
            父DNA=row[12],
        )

    # --- 人物DNA CRUD (v1.0兼容) ---
    def 注册人物DNA(self, person: DNAPerson):
        conn = sqlite3.connect(str(self.db_path))
        try:
            conn.execute("""
                INSERT INTO person_dna (dna, real_name, id_type, id_number, born_date, gender,
                    birthplace, current_location, parent_dna, created_at, updated_at, status,
                    gpg_fingerprint, dna_signature, notes)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (person.dna, person.real_name, person.id_type, person.id_number,
                  person.born_date, person.gender, person.birthplace, person.current_location,
                  person.parent_dna, person.created_at, person.updated_at, person.status,
                  person.gpg_fingerprint, person.dna_signature, person.notes))
            conn.commit()
            self._审计("注册", "人物", person.dna, person.real_name)
        except sqlite3.IntegrityError as e:
            raise ValueError(f"人物DNA注册失败: {e}")
        finally:
            conn.close()

    def 查人物DNA_by_dna(self, dna: str) -> Optional[DNAPerson]:
        conn = sqlite3.connect(str(self.db_path))
        cur = conn.execute("SELECT * FROM person_dna WHERE dna = ?", (dna,))
        row = cur.fetchone()
        conn.close()
        return self._行转人物DNA(row) if row else None

    def 查人物DNA_by_id(self, id_number: str) -> Optional[DNAPerson]:
        conn = sqlite3.connect(str(self.db_path))
        cur = conn.execute("SELECT * FROM person_dna WHERE id_number = ?", (id_number,))
        row = cur.fetchone()
        conn.close()
        return self._行转人物DNA(row) if row else None

    def 查人物DNA(self, real_name: str, id_number: str) -> Optional[DNAPerson]:
        conn = sqlite3.connect(str(self.db_path))
        cur = conn.execute("SELECT * FROM person_dna WHERE real_name=? AND id_number=?",
                          (real_name, id_number))
        row = cur.fetchone()
        conn.close()
        return self._行转人物DNA(row) if row else None

    def _行转人物DNA(self, row) -> DNAPerson:
        return DNAPerson(
            dna=row[0], real_name=row[1], id_type=row[2], id_number=row[3],
            born_date=row[4], gender=row[5], birthplace=row[6] or "",
            current_location=row[7] or "", parent_dna=row[8], created_at=row[9],
            updated_at=row[10], status=row[11], gpg_fingerprint=row[12],
            dna_signature=row[13], notes=row[14] or ""
        )

    def 添加继承(self, from_dna: str, to_dna: str, relation: str, reason: str = "自然传承"):
        conn = sqlite3.connect(str(self.db_path))
        now = datetime.now().isoformat()
        try:
            conn.execute("""
                INSERT INTO inheritance (from_dna, to_dna, relation, inheritance_time, reason)
                VALUES (?,?,?,?,?)
            """, (from_dna, to_dna, relation, now, reason))
            conn.execute("UPDATE person_dna SET status='inherited', updated_at=? WHERE dna=?",
                        (now, from_dna))
            conn.execute("UPDATE person_dna SET parent_dna=?, updated_at=? WHERE dna=?",
                        (from_dna, now, to_dna))
            conn.commit()
            self._审计("继承", "人物", from_dna, f"{from_dna[:20]}→{to_dna[:20]}")
        except Exception as e:
            raise ValueError(f"继承失败: {e}")
        finally:
            conn.close()

    def 继承深度(self, dna: str) -> int:
        depth, cur = 0, dna
        conn = sqlite3.connect(str(self.db_path))
        while cur:
            row = conn.execute("SELECT parent_dna FROM person_dna WHERE dna=?", (cur,)).fetchone()
            if row and row[0]: depth += 1; cur = row[0]
            else: cur = None
        conn.close()
        return depth

    def 继承链(self, dna: str) -> List[str]:
        chain = []
        cur = dna
        conn = sqlite3.connect(str(self.db_path))
        while cur:
            chain.append(cur)
            row = conn.execute("SELECT parent_dna FROM person_dna WHERE dna=?", (cur,)).fetchone()
            cur = row[0] if row and row[0] else None
        conn.close()
        return chain[::-1]

    def 后代(self, dna: str) -> List[DNAPerson]:
        conn = sqlite3.connect(str(self.db_path))
        cur = conn.execute("SELECT * FROM person_dna WHERE parent_dna=?", (dna,))
        rows = cur.fetchall()
        conn.close()
        return [self._行转人物DNA(row) for row in rows]

    def 族谱(self, root_dna: str, max_depth: int = 5) -> Dict:
        root = self.查人物DNA_by_dna(root_dna)
        if not root: return {"error": "DNA不存在"}
        return {"root": {"dna": root.dna, "name": root.real_name, "status": root.status},
                "tree": self._建族谱树(root_dna, 0, max_depth)}

    def _建族谱树(self, dna: str, depth: int, max_depth: int) -> List[Dict]:
        if depth >= max_depth: return []
        result = []
        for child in self.后代(dna):
            result.append({"dna": child.dna, "name": child.real_name,
                          "born": child.born_date, "status": child.status,
                          "children": self._建族谱树(child.dna, depth + 1, max_depth)})
        return result

    def 人物DNA统计(self) -> Dict:
        conn = sqlite3.connect(str(self.db_path))
        total = conn.execute("SELECT COUNT(*) FROM person_dna").fetchone()[0]
        active = conn.execute("SELECT COUNT(*) FROM person_dna WHERE status='active'").fetchone()[0]
        inherits = conn.execute("SELECT COUNT(*) FROM inheritance").fetchone()[0]
        audit = conn.execute("SELECT COUNT(*) FROM audit_log").fetchone()[0]
        conn.close()
        return {"总人数": total, "活跃": active, "继承记录": inherits, "审计日志": audit}

    def 统一统计(self) -> Dict:
        doc = self.文档DNA统计()
        per = self.人物DNA统计()
        conn = sqlite3.connect(str(self.db_path))
        total_audit = conn.execute("SELECT COUNT(*) FROM audit_log").fetchone()[0]
        conn.close()
        return {"文档DNA": doc, "人物DNA": per, "审计日志总数": total_audit}


# ═══════════════════════════════════════════════════════════
# 七、DNA族谱（人物维度）
# ═══════════════════════════════════════════════════════════

class DNA族谱:
    """DNA族谱生成器"""

    def __init__(self):
        self.registry = DNA注册表()

    def 生成族谱树(self, root_dna: str, max_depth: int = 5) -> Dict:
        return self.registry.族谱(root_dna, max_depth)

    def 文本族谱(self, root_dna: str) -> str:
        root = self.registry.查人物DNA_by_dna(root_dna)
        if not root: return "❌ DNA不存在"
        lines = ["📜 龍魂族谱", f"├─ {root.real_name} ({root.dna[:25]}...)"]
        self._文本构建(root_dna, "", lines)
        return "\n".join(lines)

    def _文本构建(self, dna: str, prefix: str, lines: List[str]):
        for i, child in enumerate(self.registry.后代(dna)):
            is_last = (i == len(self.registry.后代(dna)) - 1)
            lp = prefix + ("└─ " if is_last else "├─ ")
            cp = prefix + ("   " if is_last else "│  ")
            lines.append(f"{lp}{child.real_name} ({child.dna[:25]}...)")
            self._文本构建(child.dna, cp, lines)


# ═══════════════════════════════════════════════════════════
# 八、DNA查询与验证工具
# ═══════════════════════════════════════════════════════════

class DNA查询器:
    """统一DNA查询入口"""

    def __init__(self):
        self.registry = DNA注册表()

    def 查(self, dna: str) -> Optional[Dict]:
        """自动判断文档/人物DNA并返回"""
        文档 = self.registry.查文档DNA(dna)
        if 文档:
            return {"维度": "文档", "记录": asdict(文档)}
        人物 = self.registry.查人物DNA_by_dna(dna)
        if 人物:
            d = asdict(人物)
            d["维度"] = "人物"
            return d
        return None

    def 搜索(self, 关键词: str) -> List[Dict]:
        """模糊搜索：模块名/姓名/描述"""
        conn = sqlite3.connect(str(self.registry.db_path))
        results = []
        cur = conn.execute("SELECT dna FROM doc_dna WHERE 模块名 LIKE ? OR 元数据 LIKE ?",
                          (f"%{关键词}%", f"%{关键词}%"))
        for (dna,) in cur.fetchall():
            r = self.registry.查文档DNA(dna)
            if r: results.append({"维度": "文档", "dna": dna, "模块": r.模块名, "时间": r.创建时间})
        cur = conn.execute("SELECT dna FROM person_dna WHERE real_name LIKE ? OR notes LIKE ?",
                          (f"%{关键词}%", f"%{关键词}%"))
        for (dna,) in cur.fetchall():
            p = self.registry.查人物DNA_by_dna(dna)
            if p: results.append({"维度": "人物", "dna": dna, "姓名": p.real_name, "时间": p.created_at})
        conn.close()
        return results


# ═══════════════════════════════════════════════════════════
# 九、向后兼容层 + CLI入口
  # ═══════════════════════════════════════════════════════════




# ═══════════════════════════════════════════════════════════
# 十、向后兼容层（v1.0 API → v2.0 内部）
# ═══════════════════════════════════════════════════════════

def generate_dna(action_tag: str, version: str = "1.0",
                 module: str = "", content: str = "") -> str:
    """
    v1.0兼容API — 被 lh_k3_distill_v39.py / lh_fix_missing_dna.py 等导入
    返回完整DNA字符串
    """
    mod = module or action_tag.upper().replace(" ", "-")
    gen = 文档DNA生成器()
    record = gen.生成文档DNA(模块名=mod, 动作=action_tag, 版本=version, 内容=content)
    return record.dna


def compute_full_dna(module: str, version: str = "1.0",
                     action: str = "DOC", content: str = "") -> str:
    """
    v2.0便利函数 — 返回完整DNA字符串（含干支卦象+哈希）
    被 lh_dna_api.py 导入
    """
    return generate_dna(action_tag=action, version=version,
                        module=module, content=content)


def main():
    # 兼容旧CLI: python3 lh_dna_generator.py <action_tag> <version>
    if len(sys.argv) >= 3 and sys.argv[1] not in (
        "doc", "person", "lookup", "verify", "inherit", "family",
        "stats", "history", "search", "interactive", "-h", "--help"
    ):
        action_tag = sys.argv[1]
        version = sys.argv[2]
        print(f"# DNA: {generate_dna(action_tag, version)}")
        return

    # v2.0 CLI: 正常子命令解析
    parser = argparse.ArgumentParser(
        description="🐉 龍魂·DNA追溯码生成器 v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
双维度DNA体系：A) 文档/模块DNA（v∞干支卦） B) 人物DNA（v1.0·一世一双人）

文档/模块DNA示例:
  # 生成模块DNA
  python3 bin/lh_dna_generator.py doc --module 安全检查 --action 引擎 --version 1.0

  # 带内容绑定
  python3 bin/lh_dna_generator.py doc --module 审计规则 --content "P0铁律：为人民服务"

  # 批量生成
  python3 bin/lh_dna_generator.py doc --batch batch.json

  # 查询文档DNA
  python3 bin/lh_dna_generator.py lookup --dna "#龍芯⚡️丙午·..."

  # 验证
  python3 bin/lh_dna_generator.py verify --dna "#龍芯⚡️..." --content "原始内容"

人物DNA示例:
  # 生成人物DNA
  python3 bin/lh_dna_generator.py person --name 张三 --id-number 110101199001011234 --born 1990-01-01 --gender 男

  # 继承
  python3 bin/lh_dna_generator.py inherit --from-dna "父DNA" --to-dna "子DNA" --relation 父子

  # 族谱
  python3 bin/lh_dna_generator.py family --dna "祖先DNA"

统一操作:
  # 统计
  python3 bin/lh_dna_generator.py stats

  # 搜索
  python3 bin/lh_dna_generator.py search "关键词"

  # 历史
  python3 bin/lh_dna_generator.py history --limit 20

  # 交互模式
  python3 bin/lh_dna_generator.py --interactive

旧版兼容:
  python3 bin/lh_dna_generator.py ACTION v1.0
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # === doc: 文档/模块DNA ===
    doc_parser = subparsers.add_parser("doc", help="生成文档/模块DNA")
    doc_parser.add_argument("--module", "-m", required=True, help="模块名")
    doc_parser.add_argument("--action", "-a", default="DOC", help="动作（DOC/ENGINE/PROTOCOL/CODE）")
    doc_parser.add_argument("--version", "-v", default="1.0", help="版本号")
    doc_parser.add_argument("--content", "-c", default="", help="绑定内容（生成内容指纹）")
    doc_parser.add_argument("--type", "-t", default="文档",
                           choices=["文档","模块","引擎","协议"], help="DNA类型")
    doc_parser.add_argument("--desc", "-d", default="", help="描述")
    doc_parser.add_argument("--batch", "-b", help="批量JSON文件路径")
    doc_parser.add_argument("--json", action="store_true", help="JSON输出")

    # === person: 人物DNA ===
    person_parser = subparsers.add_parser("person", help="生成人物DNA")
    person_parser.add_argument("--name", required=True, help="真实姓名")
    person_parser.add_argument("--id-type", default="身份证", help="证件类型")
    person_parser.add_argument("--id-number", required=True, help="证件号码")
    person_parser.add_argument("--born", required=True, help="出生日期 YYYY-MM-DD")
    person_parser.add_argument("--gender", required=True, choices=["男","女"], help="性别")
    person_parser.add_argument("--birthplace", default="中国", help="出生地")
    person_parser.add_argument("--location", default="中国", help="当前所在地")
    person_parser.add_argument("--parent", help="父DNA")
    person_parser.add_argument("--gpg", help="GPG指纹")

    # === lookup ===
    lookup_parser = subparsers.add_parser("lookup", help="查询DNA（自动判断类型）")
    lookup_parser.add_argument("--dna", required=True, help="DNA追溯码")

    # === verify ===
    verify_parser = subparsers.add_parser("verify", help="验证DNA")
    verify_parser.add_argument("--dna", required=True, help="DNA追溯码")
    verify_parser.add_argument("--content", default="", help="原始内容（文档DNA用）")
    verify_parser.add_argument("--name", help="真实姓名（人物DNA用）")
    verify_parser.add_argument("--id-number", help="证件号码（人物DNA用）")

    # === inherit ===
    inherit_parser = subparsers.add_parser("inherit", help="继承DNA")
    inherit_parser.add_argument("--from-dna", required=True)
    inherit_parser.add_argument("--to-dna", required=True)
    inherit_parser.add_argument("--relation", required=True, help="父子/母女")
    inherit_parser.add_argument("--reason", default="自然传承")

    # === family ===
    family_parser = subparsers.add_parser("family", help="查看族谱")
    family_parser.add_argument("--dna", required=True)
    family_parser.add_argument("--depth", type=int, default=5)
    family_parser.add_argument("--text", action="store_true", help="文本格式")

    # === stats ===
    subparsers.add_parser("stats", help="统一统计")

    # === history ===
    history_parser = subparsers.add_parser("history", help="文档DNA历史")
    history_parser.add_argument("--limit", type=int, default=20)

    # === search ===
    search_parser = subparsers.add_parser("search", help="模糊搜索")
    search_parser.add_argument("keyword", help="搜索关键词")

    # === interactive ===
    subparsers.add_parser("interactive", help="交互模式")

    args = parser.parse_args()
    doc_gen = 文档DNA生成器()
    person_gen = 人物DNA生成器()
    registry = DNA注册表()
    family_tree = DNA族谱()
    querier = DNA查询器()

    # --- 交互模式 ---
    if args.command == "interactive":
        print("\n" + "=" * 60)
        print("🐉 DNA追溯码生成器 v2.0 - 交互模式")
        print("=" * 60)
        print("文档DNA:  模块名 | 动作 | 版本 | [内容]")
        print("人物DNA:  person | 姓名 | 身份证 | 出生 | 性别")
        print("查询:     lookup DNA码")
        print("退出:     exit")
        print("=" * 60)
        while True:
            try:
                输入 = input("\n📥 > ").strip()
                if not 输入: continue
                if 输入.lower() in ['exit', 'quit']: break
                if 输入 == 'stats':
                    s = registry.统一统计()
                    print(json.dumps(s, ensure_ascii=False, indent=2)); continue

                parts = [p.strip() for p in 输入.split("|")]
                if parts[0].lower() == "lookup" and len(parts) > 1:
                    r = querier.查(parts[1])
                    if r: print(json.dumps(r, ensure_ascii=False, indent=2))
                    else: print(f"❌ 未找到: {parts[1]}")
                elif parts[0].lower() == "person" and len(parts) >= 5:
                    person = person_gen.生成(parts[1], "身份证", parts[2], parts[3], parts[4], "中国", "中国")
                    print(f"✅ 人物DNA: {person.dna}")
                elif len(parts) >= 3:
                    content = parts[3] if len(parts) > 3 else ""
                    r = doc_gen.生成文档DNA(parts[0], parts[1], parts[2], content)
                    print(f"✅ 文档DNA: {r.dna}")
                    print(f"   模块: {r.模块名} | 动作: {r.动作} | 版本: v{r.版本}")
                    print(f"   干支: {r.干支四柱} | 卦象: {r.卦象}")
                else:
                    print("❌ 格式: 模块|动作|版本|[内容] 或 person|姓名|身份证|出生|性别")
            except KeyboardInterrupt: break
            except Exception as e: print(f"❌ {e}")
        return

    # --- doc ---
    if args.command == "doc":
        if args.batch:
            with open(args.batch, 'r', encoding='utf-8') as f:
                items = json.load(f)
            results = doc_gen.批量生成(items)
            for r in results:
                print(f"✅ {r.dna}")
            print(f"\n📊 共生成 {len(results)} 条DNA")
            return

        类型映射 = {"文档": DNA类型.文档, "模块": DNA类型.模块, "引擎": DNA类型.引擎, "协议": DNA类型.协议}
        元数据 = DNA元数据(创建者="UID9622", 描述=args.desc, 来源="CLI生成")

        r = doc_gen.生成文档DNA(
            模块名=args.module, 动作=args.action, 版本=args.version,
            内容=args.content, 元数据=元数据, 类型=类型映射[args.type]
        )

        if args.json:
            print(json.dumps(asdict(r), ensure_ascii=False, indent=2))
        else:
            print(f"\n✅ DNA生成成功!")
            print(f"🧬 DNA:       {r.dna}")
            print(f"📦 模块:       {r.模块名}")
            print(f"⚡ 动作:       {r.动作}")
            print(f"📌 版本:       v{r.版本}")
            print(f"🗓️  干支四柱:   {r.干支四柱}")
            print(f"☯️  卦象:       {r.卦象}")
            print(f"🔑 哈希:       {r.哈希值}")
            if r.内容指纹:
                print(f"📎 内容指纹:   {r.内容指纹}")
            print(f"🔐 HMAC:       {r.hmac签名[:12]}...")
            print(f"📋 类型:       {r.类型.value}")
            print(f"🕐 创建时间:   {r.创建时间}")

    # --- person ---
    elif args.command == "person":
        try:
            person = person_gen.生成(
                real_name=args.name, id_type=args.id_type, id_number=args.id_number,
                born_date=args.born, gender=args.gender, birthplace=args.birthplace,
                current_location=args.location, parent_dna=args.parent,
                gpg_fingerprint=args.gpg
            )
            print(f"\n✅ 人物DNA生成成功!")
            print(f"🧬 DNA:  {person.dna}")
            print(f"📛 姓名: {person.real_name}")
            print(f"📌 状态: {person.status}")
            print(f"🔑 签名: {person.dna_signature[:16]}...")
            if person.parent_dna: print(f"📜 继承自: {person.parent_dna[:25]}...")
            print(f"\n⚡ 一世一双人，DNA不可转让，不可借用。")
            print(f"📖 所有记忆归此DNA，只能后人继承。")
        except Exception as e:
            print(f"❌ {e}")

    # --- lookup ---
    elif args.command == "lookup":
        r = querier.查(args.dna)
        if r:
            if r.get("维度") == "文档":
                rec = r["记录"]
                print(f"\n🧬 文档DNA")
                print(f"   DNA:     {rec['dna']}")
                print(f"   模块:    {rec['模块名']}")
                print(f"   动作:    {rec['动作']}")
                print(f"   版本:    v{rec['版本']}")
                print(f"   干支:    {rec['干支四柱']}")
                print(f"   卦象:    {rec['卦象']}")
                print(f"   时间:    {rec['创建时间']}")
                if rec.get('内容指纹'):
                    print(f"   指纹:    {rec['内容指纹']}")
            else:
                print(f"\n👤 人物DNA")
                for k, v in r.items():
                    if k != "dna_signature":
                        print(f"   {k}: {v}")
                if r.get("dna_signature"):
                    print(f"   签名:    {r['dna_signature'][:16]}...")
        else:
            print(f"❌ 未找到DNA: {args.dna}")

    # --- verify ---
    elif args.command == "verify":
        if args.name and args.id_number:
            valid = person_gen.验证(args.dna, args.name, args.id_number)
            print(f"{'✅' if valid else '❌'} 人物DNA验证{'通过' if valid else '失败'}")
        else:
            valid, msg = doc_gen.验证(args.dna, args.content)
            print(f"{'✅' if valid else '❌'} {msg}")

    # --- inherit ---
    elif args.command == "inherit":
        try:
            registry.添加继承(args.from_dna, args.to_dna, args.relation, args.reason)
            print(f"✅ 继承成功! {args.from_dna[:20]}... → {args.to_dna[:20]}...")
        except Exception as e:
            print(f"❌ {e}")

    # --- family ---
    elif args.command == "family":
        if args.text:
            print(family_tree.文本族谱(args.dna))
        else:
            tree = family_tree.生成族谱树(args.dna, args.depth)
            print(json.dumps(tree, ensure_ascii=False, indent=2))

    # --- stats ---
    elif args.command == "stats":
        s = registry.统一统计()
        print("\n📊 龍魂DNA统一统计")
        print("=" * 50)
        print(f"\n📄 文档/模块DNA:")
        print(f"   总数: {s['文档DNA']['总数']}")
        print(f"   模块: {s['文档DNA']['模块数']} 个")
        print(f"   类型: {s['文档DNA']['类型分布']}")
        print(f"\n👤 人物DNA:")
        print(f"   总数: {s['人物DNA']['总人数']}")
        print(f"   活跃: {s['人物DNA']['活跃']}")
        print(f"   继承: {s['人物DNA']['继承记录']} 条")
        print(f"\n📋 审计日志: {s['审计日志总数']} 条")

    # --- history ---
    elif args.command == "history":
        records = registry.查文档DNA历史(limit=args.limit)
        print(f"\n📋 文档DNA历史（最新{len(records)}条）")
        print("-" * 70)
        for r in records:
            print(f"  {r.dna}")
            print(f"    模块:{r.模块名} | 动作:{r.动作} | 版本:v{r.版本} | {r.创建时间[:16]}")
            print()

    # --- search ---
    elif args.command == "search":
        results = querier.搜索(args.keyword)
        print(f"\n🔍 搜索「{args.keyword}」: {len(results)} 条结果")
        print("-" * 60)
        for r in results:
            dim = "📄" if r["维度"] == "文档" else "👤"
            info = r.get("模块", r.get("姓名", "未知"))
            print(f"  {dim} {r['dna'][:40]}... → {info} ({r['时间'][:16]})")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
