# DNA: #龍芯⚡️丙午·壬辰·乙亥·壬午·䷚颐-SYNC-COMPLIANCE-20260827-7A2C9F3D
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
##龍芯⚡️丙午·甲午·丙寅·甲午·䷕贲-CORE-UNNAMED-FILE9-v1.0-11
# 君子协议: 本文件受龍魂DNA追溯保护

# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 龍魂 身份验证系统
# 三重验证·GPG + UID + Confirm Code·不可绕过

from .identity_verification import (
    GPGIdentity,
    UIDIdentity,
    ConfirmCode,
    IdentityVerificationL0,
    generate_identity_proof,
)

__all__ = [
    'GPGIdentity',
    'UIDIdentity',
    'ConfirmCode',
    'IdentityVerificationL0',
    'generate_identity_proof',
]
