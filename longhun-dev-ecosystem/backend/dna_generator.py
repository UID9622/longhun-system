# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂生态 · DNA生成引擎
DNA: #龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-DNA-GEN-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（思想层）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""

import hashlib
import time
import uuid
from datetime import datetime
from .config import DNA_PREFIX, DNA_UID

TIAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
DI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]


def get_ganzhi():
    """获取当前年份天干地支（年柱简化版）"""
    year = datetime.now().year
    gan = TIAN[(year - 4) % 10]
    zhi = DI[(year - 4) % 12]
    return f"{gan}{zhi}"


def get_hexagram(seed_str: str = "") -> str:
    """由种子字符串取卦象（8卦轮转·梅花简易）"""
    GUAS = ["乾", "兑", "离", "震", "巽", "坎", "艮", "坤"]
    h = int(hashlib.sha256(seed_str.encode()).hexdigest(), 16) if seed_str else int(time.time() * 1000)
    return GUAS[h % 8]


def _rand8(seed: str) -> str:
    """8位随机大写十六进制"""
    return hashlib.sha256(seed.encode()).hexdigest()[:8].upper()


def generate_dna(prefix: str = "DEV", uid: str = DNA_UID, seed: str = "") -> str:
    """生成 DNA 追溯码：{#龍芯⚡️}{年干支}-{前缀}-{哈希8}-{UID}"""
    if not seed:
        seed = f"{prefix}{datetime.now().isoformat()}{time.time()}{uuid.uuid4().hex}"
    ganzhi = get_ganzhi()
    return f"{DNA_PREFIX}{ganzhi}-{prefix}-{_rand8(seed)}-{uid}"


def generate_developer_dna(name: str, email: str) -> str:
    """生成开发者 DNA（姓名+邮箱+时间 双哈希）"""
    seed = f"{name}{email}{time.time()}{uuid.uuid4().hex}"
    return generate_dna("DEV", seed=seed)


def generate_code_dna(file_path: str, content: str) -> str:
    """生成代码 DNA（文件路径+内容哈希）"""
    seed = f"{file_path}{hashlib.sha256(content.encode()).hexdigest()}{time.time()}"
    return generate_dna("CODE", seed=seed)
