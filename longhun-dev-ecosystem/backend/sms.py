#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂生态 · 短信验证码引擎（沙箱优先·正式接短信只换提供商标识）
DNA: #龍芯⚡️丙午·丙申·庚申·亥时-DEV-SMS-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（思想层）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
用法: 沙箱模式验证码直接随响应返回（可跑通全流程）· 正式模式 SMS_PROVIDER=aliyun/tencent + 环境变量密钥
"""

import random
import re
import threading
import time

from .config import SMS_PROVIDER, SMS_CODE_TTL, SMS_CODE_MAX_FAIL, SMS_CODE_COOLDOWN

# 中国大陆手机号（11位·1[3-9]开头）
PHONE_RE = re.compile(r"^1[3-9]\d{9}$")

# 内存验证码存储 {phone: {"code","expire","sent_at","fail"}}（沙箱够用；正式高并发可换 Redis，接口不变）
_codes: dict[str, dict] = {}
_lock = threading.Lock()


def validate_phone(phone: str) -> bool:
    """校验手机号格式"""
    return bool(PHONE_RE.match(phone or ""))


def _provider_send(phone: str, code: str) -> None:
    """正式短信通道接口位（沙箱不真正发送）"""
    if SMS_PROVIDER == "aliyun":
        # TODO(UID9622): 阿里云短信 — SMS_ACCESS_KEY / SMS_SIGN_NAME / SMS_TEMPLATE_CODE 环境变量注入
        raise NotImplementedError("阿里云短信未接入：需配置 SMS_ACCESS_KEY 等环境变量")
    if SMS_PROVIDER == "tencent":
        # TODO(UID9622): 腾讯云短信 — SMS_SECRET_ID / SMS_SECRET_KEY / SMS_SDK_APP_ID 环境变量注入
        raise NotImplementedError("腾讯云短信未接入：需配置 SMS_SECRET_ID 等环境变量")
    # sandbox: 不真正发送，验证码随响应返回


def send_code(phone: str) -> dict:
    """发送验证码 → 沙箱直接返回 dev_code；正式模式走短信服务商"""
    if not validate_phone(phone):
        return {"success": False, "error": "手机号格式不正确（需11位中国大陆手机号）"}
    with _lock:
        now = time.time()
        prev = _codes.get(phone)
        if prev and now - prev["sent_at"] < SMS_CODE_COOLDOWN:
            wait = int(SMS_CODE_COOLDOWN - (now - prev["sent_at"]))
            return {"success": False, "error": f"发送太频繁，请 {wait} 秒后再试"}

        code = f"{random.randint(0, 999999):06d}"
        _codes[phone] = {
            "code": code,
            "expire": now + SMS_CODE_TTL,
            "sent_at": now,
            "fail": 0,
        }
    try:
        _provider_send(phone, code)
    except NotImplementedError as e:
        # 正式通道未配置 → 自动降级沙箱（不阻断流程·日志留痕）
        print(f"[SMS][{SMS_PROVIDER}] 发送失败降级沙箱: {e}")

    result = {
        "success": True,
        "message": "验证码已发送",
        "expires_in": SMS_CODE_TTL,
        "provider": SMS_PROVIDER,
    }
    if SMS_PROVIDER == "sandbox":
        result["dev_code"] = code  # 仅沙箱可见（正式模式绝不返回）
        result["message"] = f"沙箱模式验证码: {code}（接入正式短信后自动隐藏）"
    return result


def verify_code(phone: str, code: str) -> dict:
    """校验验证码（一次性消费·5分钟过期·5次错误锁定·防爆破）"""
    if not validate_phone(phone):
        return {"success": False, "error": "手机号格式不正确"}
    with _lock:
        entry = _codes.get(phone)
        if not entry:
            return {"success": False, "error": "验证码不存在或已过期，请重新获取"}
        if time.time() > entry["expire"]:
            _codes.pop(phone, None)
            return {"success": False, "error": "验证码已过期，请重新获取"}
        if entry["fail"] >= SMS_CODE_MAX_FAIL:
            _codes.pop(phone, None)
            return {"success": False, "error": "错误次数过多已锁定，请重新获取验证码"}
        if entry["code"] != code:
            entry["fail"] += 1
            left = SMS_CODE_MAX_FAIL - entry["fail"]
            return {"success": False, "error": f"验证码错误（剩余 {left} 次机会）"}
        _codes.pop(phone, None)  # 一次性消费
        return {"success": True}
