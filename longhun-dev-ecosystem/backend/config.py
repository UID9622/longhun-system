#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂生态 · 配置
DNA: #龍芯⚡️丙午·丙申·庚申·亥时-DEV-CONFIG-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（思想层）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# 数据库
DATABASE_URL = f"sqlite:///{DATA_DIR}/developers.db"

# DNA 配置
DNA_UID = "9622"
DNA_PREFIX = "#龍芯⚡️"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

# ---- 支付网关配置（正规支付·按网关规范）----
PAYMENT_ENABLED = True
PAYMENT_MIN_AMOUNT = 1.0  # 1元起步·上不封顶

# 当前激活通道: sandbox(本地沙箱·验签闭环) / wechat(微信Native) / alipay(支付宝当面付) / cbpay(数字人民币)
PAYMENT_GATEWAY = os.getenv("PAYMENT_GATEWAY", "sandbox")

# 商户参数（正式通道接入时从环境变量注入·严禁硬编码）
WECHAT_MCH_ID = os.getenv("WECHAT_MCH_ID", "")
WECHAT_APP_ID = os.getenv("WECHAT_APP_ID", "")
WECHAT_API_KEY = os.getenv("WECHAT_API_KEY", "")          # APIv3密钥
ALIPAY_APP_ID = os.getenv("ALIPAY_APP_ID", "")
ALIPAY_PRIVATE_KEY = os.getenv("ALIPAY_PRIVATE_KEY", "")
CBPay_MERCHANT_NO = os.getenv("CBPay_MERCHANT_NO", "")

# 沙箱验签密钥（仅本地闭环使用·生产切真实通道后废弃）
SANDBOX_SECRET = os.getenv("SANDBOX_SECRET", "longhun-sandbox-secret-9622")

# 导出管理员 Token（历史账单/名册导出鉴权·从环境变量注入）
ADMIN_TOKEN = os.getenv("LONGHUN_DEV_ADMIN_TOKEN", "longhun-dev-admin-9622")

# ---- 短信验证码配置（沙箱优先·正式接阿里云/腾讯云只改提供商标识）----
SMS_PROVIDER = os.getenv("SMS_PROVIDER", "sandbox")   # sandbox / aliyun / tencent
SMS_CODE_TTL = 300            # 验证码有效期（秒）
SMS_CODE_MAX_FAIL = 5         # 最大错误次数（防爆破·超出锁定需重发）
SMS_CODE_COOLDOWN = 60        # 重发冷却（秒）
# 正式短信通道密钥（严禁硬编码·环境变量注入）
SMS_ACCESS_KEY = os.getenv("SMS_ACCESS_KEY", "")
SMS_SECRET_ID = os.getenv("SMS_SECRET_ID", "")

# 生态配置
ECOSYSTEM_NAME = "龍魂主权开发者联盟"
ECOSYSTEM_DNA = "#龍芯⚡️丙午·丙申·庚申·亥时-ECOSYSTEM-UID9622"

# 月度主权确认金公约锚点
MONTHLY_FEE_ANCHOR = {
    "protocol": "01_protocols/LH-DEVELOPER-FEE-CONVENTION-v1.0.md",
    "min_fee": 1.0,
    "slogan": "1元/月不是钱，是立场。上不封顶，是觉悟。杜绝一毛不拔。",
}
