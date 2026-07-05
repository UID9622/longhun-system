# #龍芯⚡️20260624010825152-AUTO-DNA-CDD17034 自动注入·分层治理自愈引擎 · 来源可查
# -*- coding: utf-8 -*-
##龍芯⚡️2026-06-21-CORE-UNNAMED-FILE13-v1.0-15
# 君子协议: 本文件受龍魂DNA追溯保护

# 龍魂 宪法和基础配置系统
# 系统根本原则·L0永恒层·不可改动

from .longhun_foundation_config import (
    CreatorIdentity,
    SystemMission,
    get_system_config,
    validate_config,
)
from .sancai_protocol import (
    SancaiProtocol,
    SancaiProtocolTamperedError,
    SANCAI,
    get_protocol,
    validate_alignment,
    verify_protocol_integrity,
)

__all__ = [
    'CreatorIdentity',
    'SystemMission',
    'get_system_config',
    'validate_config',
    'SancaiProtocol',
    'SancaiProtocolTamperedError',
    'SANCAI',
    'get_protocol',
    'validate_alignment',
    'verify_protocol_integrity',
]
