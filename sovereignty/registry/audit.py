# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 UID9622 主权注册三色审计模块
Dragon Soul Sovereign Registration Tri-Color Audit

DNA: #龍芯⚡️20260628-SOVEREIGN-AUDIT-v1.0
"""

import re
import hashlib
from typing import Dict, Any

# 铁律守护关键词
RED_KEYWORDS = [
    "伪造", "假冒", "篡改", "攻击", "窃取", "泄露", "Root", "sudo",
    "root", "admin", "管理员", "测试用户", "fake", "test", "example",
    "匿名", "anonymous", "未知", "unknow",
]

YELLOW_KEYWORDS = [
    "代理", "代办", "临时", "未实名", "待审", "异常", "注意",
]

GREEN_KEYWORDS = [
    "真实", "实名", "合规", "通过", "可信", "龍魂", "UID9622",
]


def audit_registration(
    name: str,
    id_type: str,
    id_number: str,
    device_fingerprint: str = "",
) -> Dict[str, Any]:
    """
    对注册请求执行三色审计。

    Returns:
        {"level": "🟢/🟡/🔴", "reason": "...", "rules": [...]}
    """
    rules_triggered = []
    text = f"{name} {id_type} {id_number} {device_fingerprint}".lower()

    # §9.49 用之者王铁律：姓名不能为空且需含中文或合法字符
    if not name or len(name) < 2:
        rules_triggered.append("§9.49 姓名过短或为空")
        return {"level": "🔴", "reason": "姓名不符合用之者王铁律", "rules": rules_triggered}

    # §9.50 不读规则反胜规则铁律：检测明显测试/伪造信息
    for kw in RED_KEYWORDS:
        if kw.lower() in text:
            rules_triggered.append(f"§9.50 命中禁用词: {kw}")
            return {"level": "🔴", "reason": f"注册信息包含禁用内容: {kw}", "rules": rules_triggered}

    # 证件号基础校验
    if id_type == "身份证":
        if not re.match(r"^\d{15}$|^\d{17}[\dXx]$", id_number):
            rules_triggered.append("§9.50 身份证格式异常")
            return {"level": "🟡", "reason": "身份证格式不符合规范", "rules": rules_triggered}

    # §9.51 主权字繁体铁律：姓名中鼓励使用中文（至少包含中文字符）
    if not re.search(r"[\u4e00-\u9fa5]", name):
        rules_triggered.append("§9.51 姓名未含中文")
        return {"level": "🟡", "reason": "主权身份注册建议使用中文姓名", "rules": rules_triggered}

    # 黄色关键词检测
    for kw in YELLOW_KEYWORDS:
        if kw.lower() in text:
            rules_triggered.append(f"🟡 命中警示词: {kw}")
            return {"level": "🟡", "reason": f"注册信息含警示内容: {kw}", "rules": rules_triggered}

    # 绿色通行
    rules_triggered.append("§9.52 量子态一次塌缩铁律：注册信息通过")
    return {"level": "🟢", "reason": "注册信息通过三色审计", "rules": rules_triggered}
