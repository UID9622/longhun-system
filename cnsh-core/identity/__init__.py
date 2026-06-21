# -*- coding: utf-8 -*-
##龍芯⚡️2026-06-21-CORE-UNNAMED-FILE9-v1.0-11
# 君子協議: 本文件受龍魂DNA追溯保護

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
