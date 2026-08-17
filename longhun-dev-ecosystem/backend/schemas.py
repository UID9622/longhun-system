#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂生态 · Pydantic模型
DNA: #龍芯⚡️丙午·丙申·庚申·亥时-DEV-SCHEMAS-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（思想层）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""

from pydantic import BaseModel, EmailStr
from typing import Optional


class DeveloperRegisterRequest(BaseModel):
    name: str
    email: EmailStr
    nickname: str
    gpg_public_key: Optional[str] = None
    is_enterprise: Optional[bool] = False        # 企业/机构标记（可自愿上浮）
    amount: Optional[float] = 1.0                # 自愿上浮首月费（>=1）
    channel: Optional[str] = "sandbox"           # 支付通道 wechat/alipay/cbpay/sandbox


class SmsSendRequest(BaseModel):
    phone: str  # 11位中国大陆手机号


class PhoneLoginRequest(BaseModel):
    """手机号+验证码 登录/注册（Kimi式·首次需补昵称）"""
    phone: str
    code: str
    nickname: Optional[str] = None               # 新手机号首次注册必填
    gpg_public_key: Optional[str] = None
    is_enterprise: Optional[bool] = False


class PaymentConfirmRequest(BaseModel):
    developer_dna: str
    order_id: Optional[str] = None
    amount: Optional[float] = 1.0
    payment_method: Optional[str] = "wechat"
    channel: Optional[str] = "sandbox"


class BillRequest(BaseModel):
    developer_dna: str
    amount: Optional[float] = None               # 自愿上浮金额（>=1）
    channel: Optional[str] = "sandbox"


class PayNotifyRequest(BaseModel):
    """支付网关回调（正规验签）"""
    params: dict
    signature: str
    channel: Optional[str] = "sandbox"


class CodeInjectRequest(BaseModel):
    file_path: str
    content: str
    developer_dna: str
    language: Optional[str] = None


class CodeInjectResponse(BaseModel):
    success: bool
    dna: str
    message: str
    file_path: str
