# -*- coding: utf-8 -*-
##龍芯⚡️2026-06-21-CORE-UNNAMED-FILE12-v1.0-14
# 君子協議: 本文件受龍魂DNA追溯保護

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
