# #龍芯⚡️20260624010825153-AUTO-DNA-FA4C9F5B 自动注入·分层治理自愈引擎 · 来源可查
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║        龍魂权限控制系统 / LongHun RBAC System                    ║
║                                                                  ║
║  角色权限管理·访问控制列表·L0-L4分层权重                          ║
║  不是第一条功能，不是第一条规则——是根。                           ║
║                                                                  ║
║  DNA:#龍芯⚡️2026-06-03-RBAC-SYSTEM-FILE1-v1.0                        ║
║  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✓              ║
║                                                                  ║
║  来源: 龍魂系统底座声明·人永远是1 v1.0                           ║
║  责任: UID9622·不免责                                            ║
╚══════════════════════════════════════════════════════════════════╝
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Tuple, Any
from datetime import datetime
import json

# ═══════════════════════════════════════════════════════════════
# 【权限定义】
# ═══════════════════════════════════════════════════════════════

class Permission(str, Enum):
    """系统权限定义"""
    # 读权限
    READ = "read"
    READ_SOURCE = "read:source"
    READ_CONFIG = "read:config"
    READ_LOG = "read:log"

    # 写权限
    WRITE = "write"
    WRITE_CODE = "write:code"
    WRITE_CONFIG = "write:config"
    WRITE_LOG = "write:log"

    # 执行权限
    EXECUTE = "execute"
    EXECUTE_WORKFLOW = "execute:workflow"
    EXECUTE_SYSTEM = "execute:system"

    # 管理权限
    ADMIN = "admin"
    ADMIN_USER = "admin:user"
    ADMIN_ROLE = "admin:role"
    ADMIN_SYSTEM = "admin:system"

    # 特殊权限
    SIGN_DNA = "sign:dna"
    VERIFY_SIGNATURE = "verify:signature"
    CREATE_CONFIRM_CODE = "create:confirm_code"


class Role(str, Enum):
    """系统角色定义"""
    CREATOR = "creator"           # UID9622 - 创始人（最高权限）
    MAINTAINER = "maintainer"     # 维护者（次级权限）
    CONTRIBUTOR = "contributor"   # 贡献者（普通权限）
    USER = "user"                 # 普通用户（只读）
    GUEST = "guest"               # 访客（最小权限）


class SystemLayer(str, Enum):
    """系统分层·权重衰减"""
    L0_ETERNAL = "L0"             # α=0      永恒不变
    L1_CENTURY = "L1"             # α≈0.01   百年家训
    L2_DECADE = "L2"              # α≈0.1    十年战略
    L3_DAILY = "L3"               # α≈1.0    日常迭代
    L4_INSTANT = "L4"             # α→∞      瞬时坍缩


# ═══════════════════════════════════════════════════════════════
# 【角色权限映射】
# ═══════════════════════════════════════════════════════════════

ROLE_PERMISSIONS: Dict[Role, Set[Permission]] = {
    Role.CREATOR: {
        # 创始人·最高权限
        Permission.READ,
        Permission.WRITE,
        Permission.EXECUTE,
        Permission.ADMIN,
        Permission.SIGN_DNA,
        Permission.VERIFY_SIGNATURE,
        Permission.CREATE_CONFIRM_CODE,
        Permission.READ_SOURCE,
        Permission.READ_CONFIG,
        Permission.READ_LOG,
        Permission.WRITE_CODE,
        Permission.WRITE_CONFIG,
        Permission.WRITE_LOG,
        Permission.EXECUTE_WORKFLOW,
        Permission.EXECUTE_SYSTEM,
        Permission.ADMIN_USER,
        Permission.ADMIN_ROLE,
        Permission.ADMIN_SYSTEM,
    },

    Role.MAINTAINER: {
        # 维护者·次级权限
        Permission.READ,
        Permission.WRITE,
        Permission.EXECUTE,
        Permission.SIGN_DNA,
        Permission.READ_SOURCE,
        Permission.READ_CONFIG,
        Permission.READ_LOG,
        Permission.WRITE_CODE,
        Permission.WRITE_LOG,
        Permission.EXECUTE_WORKFLOW,
    },

    Role.CONTRIBUTOR: {
        # 贡献者·普通权限
        Permission.READ,
        Permission.WRITE,
        Permission.EXECUTE,
        Permission.READ_SOURCE,
        Permission.WRITE_CODE,
        Permission.EXECUTE_WORKFLOW,
    },

    Role.USER: {
        # 普通用户·只读权限
        Permission.READ,
        Permission.READ_SOURCE,
        Permission.READ_LOG,
    },

    Role.GUEST: {
        # 访客·最小权限
        Permission.READ,
    },
}

# ═══════════════════════════════════════════════════════════════
# 【分层权重映射】L0-L4的修改权限
# ═══════════════════════════════════════════════════════════════

LAYER_MODIFICATION_RIGHTS: Dict[SystemLayer, List[str]] = {
    SystemLayer.L0_ETERNAL: {
        "who_can_modify": ["creator"],
        "modification_requirement": "系统重启 + 用户明确确认",
        "change_log": "必须记录所有修改",
        "rollback": "支持完全回滚到初始状态",
        "immutable_fields": [
            "身份认证",
            "DNA定义",
            "系统根本原则",
            "创始人信息",
        ],
    },

    SystemLayer.L1_CENTURY: {
        "who_can_modify": ["creator"],
        "modification_requirement": "git commit + 审计记录 + 标记为重大变更",
        "change_log": "必须记录所有修改",
        "rollback": "支持git回滚",
        "immutable_fields": [
            "系统宪法",
            "权限模型",
            "决策流程",
        ],
    },

    SystemLayer.L2_DECADE: {
        "who_can_modify": ["creator", "maintainer"],
        "modification_requirement": "Pull Request审查",
        "change_log": "自动记录所有修改",
        "rollback": "支持git回滚",
        "immutable_fields": [],
    },

    SystemLayer.L3_DAILY: {
        "who_can_modify": ["creator", "maintainer", "contributor"],
        "modification_requirement": "无特殊要求",
        "change_log": "自动追踪所有修改",
        "rollback": "支持git回滚",
        "immutable_fields": [],
    },

    SystemLayer.L4_INSTANT: {
        "who_can_modify": ["anyone"],
        "modification_requirement": "无",
        "change_log": "日志记录（24小时后删除）",
        "rollback": "不支持",
        "immutable_fields": [],
        "auto_cleanup": "24小时后自动坍缩",
    },
}

# ═══════════════════════════════════════════════════════════════
# 【访问控制对象】
# ═══════════════════════════════════════════════════════════════

@dataclass
class User:
    """系统用户"""
    uid: str
    name: str
    role: Role
    roles: Set[Role] = field(default_factory=set)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    is_active: bool = True

    def __post_init__(self):
        """初始化用户角色集合"""
        self.roles.add(self.role)

    def has_permission(self, permission: Permission) -> bool:
        """检查用户是否有特定权限"""
        for role in self.roles:
            if role in ROLE_PERMISSIONS:
                if permission in ROLE_PERMISSIONS[role]:
                    return True
        return False

    def get_all_permissions(self) -> Set[Permission]:
        """获取用户的所有权限"""
        all_perms = set()
        for role in self.roles:
            if role in ROLE_PERMISSIONS:
                all_perms.update(ROLE_PERMISSIONS[role])
        return all_perms


@dataclass
class Resource:
    """受保护的资源"""
    resource_id: str
    resource_type: str  # 'file', 'config', 'workflow', 'log' 等
    layer: SystemLayer  # L0-L4
    owner: str  # 所有者UID
    acl: Dict[str, Set[Permission]] = field(default_factory=dict)  # UID -> 权限集
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    modified_at: str = field(default_factory=lambda: datetime.now().isoformat())
    description: str = ""

    def grant_permission(self, uid: str, permission: Permission) -> bool:
        """授予用户权限"""
        if uid not in self.acl:
            self.acl[uid] = set()
        self.acl[uid].add(permission)
        self.modified_at = datetime.now().isoformat()
        return True

    def revoke_permission(self, uid: str, permission: Permission) -> bool:
        """撤销用户权限"""
        if uid in self.acl:
            self.acl[uid].discard(permission)
            if not self.acl[uid]:
                del self.acl[uid]
        self.modified_at = datetime.now().isoformat()
        return True

    def check_access(self, uid: str, permission: Permission) -> bool:
        """检查特定用户对资源的访问权限"""
        # 所有者有所有权限
        if uid == self.owner:
            return True
        # 检查ACL
        if uid in self.acl:
            return permission in self.acl[uid]
        return False


# ═══════════════════════════════════════════════════════════════
# 【RBAC管理系统】
# ═══════════════════════════════════════════════════════════════

class RBACSystem:
    """基于角色的访问控制系统"""

    def __init__(self):
        self.users: Dict[str, User] = {}
        self.resources: Dict[str, Resource] = {}
        self.audit_log: List[Dict] = []

        # 初始化创始人
        self._init_creator()

    def _init_creator(self):
        """初始化创始人（UID9622）"""
        creator = User(
            uid="9622",
            name="诸葛鑫(龍芯北辰)",
            role=Role.CREATOR,
        )
        self.users["9622"] = creator
        self._audit_log("user_created", f"创始人账户初始化: {creator.uid}")

    def create_user(self, uid: str, name: str, role: Role) -> Tuple[bool, str]:
        """创建新用户"""
        if uid in self.users:
            return False, f"用户 {uid} 已存在"

        user = User(uid=uid, name=name, role=role)
        self.users[uid] = user
        self._audit_log("user_created", f"创建用户: {uid} ({name}) 角色: {role}")
        return True, f"用户 {uid} 创建成功"

    def assign_role(self, uid: str, role: Role) -> Tuple[bool, str]:
        """为用户分配角色"""
        if uid not in self.users:
            return False, f"用户 {uid} 不存在"

        self.users[uid].roles.add(role)
        self._audit_log("role_assigned", f"为用户 {uid} 分配角色: {role}")
        return True, f"角色 {role} 分配成功"

    def check_access(self, uid: str, permission: Permission, resource_id: Optional[str] = None) -> bool:
        """检查用户访问权限"""
        if uid not in self.users:
            return False

        user = self.users[uid]

        # 检查用户权限
        if not user.has_permission(permission):
            return False

        # 如果指定了资源，检查资源ACL
        if resource_id:
            if resource_id not in self.resources:
                return False
            return self.resources[resource_id].check_access(uid, permission)

        return True

    def protect_resource(self, resource_id: str, resource_type: str, layer: SystemLayer,
                        owner: str, description: str = "") -> Tuple[bool, str]:
        """保护资源"""
        if resource_id in self.resources:
            return False, f"资源 {resource_id} 已存在"

        resource = Resource(
            resource_id=resource_id,
            resource_type=resource_type,
            layer=layer,
            owner=owner,
            description=description,
        )
        self.resources[resource_id] = resource
        self._audit_log("resource_protected", f"保护资源: {resource_id} (L层级: {layer})")
        return True, f"资源 {resource_id} 已受保护"

    def _audit_log(self, event_type: str, message: str):
        """记录审计日志"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "message": message,
        }
        self.audit_log.append(log_entry)

    def get_audit_log(self) -> List[Dict]:
        """获取审计日志"""
        return self.audit_log.copy()

    def get_system_status(self) -> Dict[str, Any]:
        """获取系统状态"""
        return {
            "users_count": len(self.users),
            "resources_count": len(self.resources),
            "audit_log_count": len(self.audit_log),
            "creator_verified": "9622" in self.users and self.users["9622"].role == Role.CREATOR,
        }


# ═══════════════════════════════════════════════════════════════
# 【初始化全局RBAC系统】
# ═══════════════════════════════════════════════════════════════

_GLOBAL_RBAC = RBACSystem()

def get_rbac_system() -> RBACSystem:
    """获取全局RBAC系统实例"""
    return _GLOBAL_RBAC


if __name__ == "__main__":
    # 测试RBAC系统
    rbac = get_rbac_system()

    print("🔐 龍魂权限控制系统 (RBAC)")
    print("=" * 80)

    # 创建测试用户
    rbac.create_user("0001", "张三", Role.CONTRIBUTOR)
    rbac.create_user("0002", "李四", Role.USER)

    # 保护一个资源
    rbac.protect_resource(
        resource_id="config_l0.yaml",
        resource_type="config",
        layer=SystemLayer.L0_ETERNAL,
        owner="9622",
        description="系统L0配置文件"
    )

    # 测试权限检查
    print("\n权限检查:")
    print(f"创始人 (9622) 可读取 L0配置: {rbac.check_access('9622', Permission.READ_CONFIG, 'config_l0.yaml')}")
    print(f"普通用户 (0002) 可读取 L0配置: {rbac.check_access('0002', Permission.READ_CONFIG, 'config_l0.yaml')}")

    # 打印系统状态
    print("\n系统状态:")
    print(json.dumps(rbac.get_system_status(), ensure_ascii=False, indent=2))

    print("\n审计日志 (前5条):")
    for log in rbac.get_audit_log()[:5]:
        print(f"  [{log['timestamp']}] {log['event_type']}: {log['message']}")

    print("=" * 80)
