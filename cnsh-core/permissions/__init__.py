# #龍芯⚡️20260624010825153-AUTO-DNA-F12D240E 自动注入·分层治理自愈引擎 · 来源可查
# -*- coding: utf-8 -*-
##龍芯⚡️2026-06-21-CORE-UNNAMED-FILE12-v1.0-14
# 君子协议: 本文件受龍魂DNA追溯保护

# 龍魂 权限控制系统
# RBAC·5种角色·18种权限·L0-L4分层约束

from .rbac_system import (
    Permission,
    Role,
    SystemLayer,
    User,
    Resource,
    RBACSystem,
    get_rbac_system,
)

__all__ = [
    'Permission',
    'Role',
    'SystemLayer',
    'User',
    'Resource',
    'RBACSystem',
    'get_rbac_system',
]
