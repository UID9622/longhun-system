#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DNA: #龍芯⚡️丙午·丁酉·乙酉·午时·䷾既济-CNSH-STD-DNA-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
CNSH 标准库 · dna —— DNA 追溯码生成/校验
格式: #龍芯⚡️<干支四柱或日期>·<模块>-<动作>-<哈希8>
"""
import hashlib
import re
import time as _t

_PAT = re.compile(r"#龍芯⚡️[\u4e00-\u9fa5·\.\-A-Za-z0-9]{1,24}(?:·[\u4e00-\u9fa5A-Za-z0-9]+-[A-Za-z0-9]+(?:-([0-9a-f]{8}))?)?")


def generate(module: str, action: str, seed: str = "", date: str = None) -> str:
    """生成 DNA 追溯码（哈希8=模块+动作+种子 的 sha256 前缀）"""
    date = date or _t.strftime("%Y-%m-%d")
    digest = hashlib.sha256(f"{module}:{action}:{seed}".encode("utf-8")).hexdigest()[:8]
    return f"#龍芯⚡️{date}·{module}-{action}-{digest}"


def validate(dna: str) -> bool:
    """校验 DNA 格式合法"""
    return bool(_PAT.match(dna or ""))


def trace_hash(module: str, action: str, seed: str = "") -> str:
    """追溯哈希（不含 DNA 头，用于比对）"""
    return hashlib.sha256(f"{module}:{action}:{seed}".encode("utf-8")).hexdigest()


def extract(text: str) -> list:
    """从文本提取所有 DNA 码"""
    return _PAT.findall(text) if isinstance(text, str) else []


def stamp_full() -> str:
    """带日期全格式（提交用）"""
    return generate("TRACE", "AUDIT")
