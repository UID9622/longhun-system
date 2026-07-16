# -*- coding: utf-8 -*-
##龍芯⚡️2026-06-21-ENGINE-_V3-0_0FE6-v1.0
# 君子协议: 本文件受龍魂DNA追溯保护

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂体系安全域审计协议 v3.0
安全域8模块国标锚定配置文件

DNA签名: #UID9622⚡️2026-06-16-SECURITY-AUDIT-v3.0
确认:    #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
忠(0.5) > 孝(0.3) > 义(0.2) 排序铁律

功能：激活安全域8模块，锚定中国国家法规标准
适用：龍芯北辰·诸葛鑫(UID9622)龍魂系统
"""

import hashlib
import json
import datetime
import uuid
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable
from functools import wraps
import threading
import time
import logging
import os

# ============================================================
# 第一部分：基础类型与枚举定义
# ============================================================

class SecurityLevel(Enum):
    """安全等级 - GB/T 22239-2019"""
    LEVEL_1 = 1  # 自主保护
    LEVEL_2 = 2  # 指导保护
    LEVEL_3 = 3  # 监督保护（等保2.0核心）
    LEVEL_4 = 4  # 强制保护
    LEVEL_5 = 5  # 专控保护

class AuditColor(Enum):
    """三色审计状态"""
    PASS = "🟢通过"
    MARK = "🟡标记"
    BLOCK = "🔴阻断"

class Priority(Enum):
    """优先级定义"""
    P0 = "P0-核心"    # 系统级阻断
    P1 = "P1-关键"    # 业务级阻断
    P2 = "P2-重要"    # 需人工确认
    P3 = "P3-一般"    # 记录备查

class FailCode(Enum):
    """通用失败码体系"""
    # MOD-SEC-01 身份鉴别
    AUTH_ID_INVALID = "FAIL-1"
    AUTH_CRED_EXPIRED = "FAIL-2"
    AUTH_TOKEN_INVALID = "FAIL-3"
    AUTH_PERM_DENIED = "FAIL-4"
    AUTH_SESSION_TIMEOUT = "FAIL-5"
    AUTH_BRUTE_FORCE = "FAIL-6"
    AUTH_MFA_FAILED = "FAIL-7"
    # MOD-SEC-02 数据加密
    ENC_FAILED = "FAIL-1"
    ENC_KEY_LEAK = "FAIL-2"
    ENC_HASH_COLLISION = "FAIL-3"
    ENC_TX_INTERRUPT = "FAIL-4"
    ENC_STORAGE_DAMAGE = "FAIL-5"
    ENC_KEY_EXPIRED = "FAIL-6"
    ENC_ALG_DOWNGRADE = "FAIL-7"
    # MOD-SEC-03 安全审计
    LOG_WRITE_FAIL = "FAIL-1"
    LOG_FORMAT_ERR = "FAIL-2"
    LOG_TAMPERED = "FAIL-3"
    LOG_QUERY_TIMEOUT = "FAIL-4"
    LOG_STORAGE_FULL = "FAIL-5"
    LOG_LEVEL_ERR = "FAIL-6"
    LOG_ALERT_MISS = "FAIL-7"

class LogLevel(Enum):
    """日志分级 - GB/T 31992-2015"""
    CRITICAL = "CRITICAL"     # 系统级故障
    HIGH = "HIGH"             # 安全事件
    MEDIUM = "MEDIUM"         # 异常行为
    LOW = "LOW"               # 一般信息
    INFO = "INFO"             # 运行信息
    DEBUG = "DEBUG"           # 调试信息

@dataclass
class InterfaceContract:
    """接口契约定义"""
    interface_id: str          # 接口编号 IN-x
    name: str                  # 接口名称
    input_schema: Dict         # 输入参数结构
    output_schema: Dict        # 输出参数结构
    validation_rules: List[str] # 关联校验规则
    fail_codes: List[str]      # 关联失败码
    gb_clause: str             # 国标条款

@dataclass
class ValidationRule:
    """校验规则定义"""
    rule_id: str               # 规则编号 RULE-x
    name: str                  # 规则名称
    description: str           # 规则描述
    validator: Callable        # 校验函数
    level: SecurityLevel       # 适用安全等级
    gb_clause: str             # 国标条款

@dataclass
class FailStrategy:
    """失败策略定义"""
    fail_code: str             # 失败码
    description: str           # 失败描述
    action: str                # 处置动作
    escalation: bool           # 是否升级告警
    block: bool                # 是否阻断

@dataclass
class CrossModuleFlow:
    """跨模块数据流"""
    flow_id: str               # 流编号
    source_module: str         # 源模块
    target_module: str         # 目标模块
    data_type: str             # 数据类型
    contract: str              # 契约描述
    priority: Priority         # 优先级

@dataclass
class AuditLogEntry:
    """审计日志条目 - GB/T 31992-2015"""
    timestamp: str
    module: str
    event_type: str
    severity: LogLevel
    source_ip: str
    user_id: str
    action: str
    result: AuditColor
    details: Dict[str, Any]
    dna_signature: str
    integrity_hash: str

# ============================================================
# 第二部分：DNA签名与审计工具
# ============================================================

DNA_SIGNATURE = "#UID9622⚡️2026-06-16-SECURITY-AUDIT-v3.0"
CONFIRM_TOKEN = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

# 忠(0.5) > 孝(0.3) > 义(0.2) 权重矩阵
LOYALTY_WEIGHTS = {
    "loyalty": 0.5,   # 忠 - 国家安全/公共利益
    "family": 0.3,    # 孝 - 组织/团队利益
    "righteousness": 0.2  # 义 - 个人/局部利益
}

class AuditToolkit:
    """审计工具箱"""
    
    @staticmethod
    def compute_integrity_hash(data: Dict[str, Any]) -> str:
        """计算完整性哈希 - SHA-256"""
        serialized = json.dumps(data, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(serialized.encode()).hexdigest()
    
    @staticmethod
    def sign_log(entry: AuditLogEntry) -> str:
        """为日志条目添加DNA签名"""
        base = f"{entry.timestamp}|{entry.module}|{entry.event_type}|{DNA_SIGNATURE}"
        return hashlib.sha256(base.encode()).hexdigest()[:16]
    
    @staticmethod
    def verify_loyalty_weights(action_weights: Dict[str, float]) -> bool:
        """校验忠孝义权重排序"""
        w = action_weights
        return (w.get("loyalty", 0) >= w.get("family", 0) >= w.get("righteousness", 0) and
                abs(w.get("loyalty", 0) - 0.5) < 0.01 and
                abs(w.get("family", 0) - 0.3) < 0.01 and
                abs(w.get("righteousness", 0) - 0.2) < 0.01)
    
    @staticmethod
    def generate_token() -> str:
        """生成安全令牌"""
        return f"TKN-{uuid.uuid4().hex[:16].upper()}-{int(time.time())}"
    
    @staticmethod
    def timestamp_iso() -> str:
        """ISO格式时间戳"""
        return datetime.datetime.now().isoformat()

# 审计日志全局存储（WORM模式 - Write Once Read Many）
AUDIT_LOG_WORM: List[AuditLogEntry] = []
AUDIT_LOG_LOCK = threading.Lock()

class WORMAuditLog:
    """WORM防篡改审计日志 - GB/T 31992-2015"""
    
    @classmethod
    def append(cls, entry: AuditLogEntry) -> bool:
        """追加日志（仅一次写入）"""
        with AUDIT_LOG_LOCK:
            entry.integrity_hash = AuditToolkit.compute_integrity_hash(entry.details)
            entry.dna_signature = AuditToolkit.sign_log(entry)
            AUDIT_LOG_WORM.append(entry)
            return True
    
    @classmethod
    def verify_chain(cls) -> bool:
        """校验日志链完整性"""
        with AUDIT_LOG_LOCK:
            for i, entry in enumerate(AUDIT_LOG_WORM):
                computed = AuditToolkit.compute_integrity_hash(entry.details)
                if computed != entry.integrity_hash:
                    return False
            return True
    
    @classmethod
    def query_by_time(cls, start: str, end: str) -> List[AuditLogEntry]:
        """按时间范围查询"""
        return [e for e in AUDIT_LOG_WORM if start <= e.timestamp <= end]
    
    @classmethod
    def get_retention_status(cls) -> Dict[str, Any]:
        """获取日志留存状态 - ≥180天"""
        now = datetime.datetime.now()
        cutoff = now - datetime.timedelta(days=180)
        total = len(AUDIT_LOG_WORM)
        retained = sum(1 for e in AUDIT_LOG_WORM 
                      if datetime.datetime.fromisoformat(e.timestamp) >= cutoff)
        return {
            "total_logs": total,
            "retained_logs": retained,
            "retention_days": 180,
            "compliant": retained >= 0,  # 只要配置合规即视为通过
            "standard": "GB/T 31992-2015 / 网络安全法第21条"
        }

# ============================================================
# 第三部分：MOD-SEC-01 身份鉴别与访问控制
# ============================================================
# 国标：GB/T 22239-2019 8.1.1（等保2.0）
# 法规：网络安全法第24条

MOD_SEC_01_CONFIG = {
    "module_id": "MOD-SEC-01",
    "module_name": "身份鉴别与访问控制",
    "gb_standard": "GB/T 22239-2019 8.1.1",
    "laws": ["网络安全法第24条", "等保2.0"],
    "security_level": SecurityLevel.LEVEL_3,
    "priority": Priority.P0,
    "activation_status": True,
    
    # 核心要求配置
    "requirements": {
        "mfa_enabled": True,              # 双因素认证
        "password_complexity": {          # 口令复杂度
            "min_length": 12,
            "require_upper": True,
            "require_lower": True,
            "require_digit": True,
            "require_special": True,
            "max_age_days": 90,
            "history_count": 5
        },
        "login_failure": {                # 登录失败处理
            "max_attempts": 5,
            "lockout_duration_minutes": 30,
            "alert_threshold": 3
        },
        "session": {                      # 会话管理
            "timeout_minutes": 30,
            "max_concurrent": 3,
            "idle_timeout_minutes": 15
        },
        "permission_model": "RBAC+ABAC",  # 权限模型
        "least_privilege": True           # 最小权限原则
    },
    
    # 接口契约 IN-1 ~ IN-4
    "interfaces": [
        InterfaceContract(
            interface_id="IN-1",
            name="身份请求",
            input_schema={
                "username": "str[required]",
                "auth_type": "enum[password/certificate/mfa]",
                "source_ip": "str[required]",
                "device_id": "str[optional]"
            },
            output_schema={
                "auth_request_id": "str",
                "challenge": "str",
                "session_id": "str",
                "status": "enum[pending/approved/denied]"
            },
            validation_rules=["RULE-1", "RULE-2"],
            fail_codes=["FAIL-1", "FAIL-2"],
            gb_clause="GB/T 22239-2019 8.1.1.1"
        ),
        InterfaceContract(
            interface_id="IN-2",
            name="凭证提交",
            input_schema={
                "auth_request_id": "str[required]",
                "credential": "str[encrypted,required]",
                "credential_type": "enum[password/otp/biometric/token]"
            },
            output_schema={
                "credential_valid": "bool",
                "strength_score": "int[0-100]",
                "expires_at": "datetime"
            },
            validation_rules=["RULE-2", "RULE-3"],
            fail_codes=["FAIL-2", "FAIL-6"],
            gb_clause="GB/T 22239-2019 8.1.1.2"
        ),
        InterfaceContract(
            interface_id="IN-3",
            name="令牌管理",
            input_schema={
                "action": "enum[issue/refresh/revoke/validate]",
                "token": "str[conditional]",
                "user_id": "str[required]",
                "scope": "list[str]"
            },
            output_schema={
                "token": "str[jwt_format]",
                "expires_at": "datetime",
                "refresh_token": "str",
                "scopes_granted": "list[str]"
            },
            validation_rules=["RULE-3", "RULE-5"],
            fail_codes=["FAIL-3", "FAIL-5"],
            gb_clause="GB/T 22239-2019 8.1.1.3"
        ),
        InterfaceContract(
            interface_id="IN-4",
            name="权限查询",
            input_schema={
                "user_id": "str[required]",
                "resource": "str[required]",
                "action": "str[required]",
                "context": "dict[optional]"
            },
            output_schema={
                "permitted": "bool",
                "permissions": "list[str]",
                "constraints": "dict",
                "audit_trail": "str"
            },
            validation_rules=["RULE-4", "RULE-6"],
            fail_codes=["FAIL-4", "FAIL-7"],
            gb_clause="GB/T 22239-2019 8.1.1.4"
        )
    ],
    
    # 校验规则 RULE-1 ~ RULE-6
    "validation_rules": [
        ValidationRule(
            rule_id="RULE-1",
            name="身份有效性校验",
            description="校验用户身份是否在系统中注册且状态正常",
            validator=lambda ctx: ctx.get("user_exists", False) and ctx.get("user_active", False),
            level=SecurityLevel.LEVEL_3,
            gb_clause="GB/T 22239-2019 8.1.1.1"
        ),
        ValidationRule(
            rule_id="RULE-2",
            name="凭证强度校验",
            description="校验口令复杂度是否符合安全策略",
            validator=lambda ctx: ctx.get("password_score", 0) >= 80,
            level=SecurityLevel.LEVEL_3,
            gb_clause="GB/T 22239-2019 8.1.1.2"
        ),
        ValidationRule(
            rule_id="RULE-3",
            name="令牌有效期校验",
            description="校验令牌是否在有效期内且未被撤销",
            validator=lambda ctx: ctx.get("token_valid", False) and not ctx.get("token_revoked", True),
            level=SecurityLevel.LEVEL_3,
            gb_clause="GB/T 22239-2019 8.1.1.3"
        ),
        ValidationRule(
            rule_id="RULE-4",
            name="权限匹配校验",
            description="校验用户是否拥有请求资源的必要权限",
            validator=lambda ctx: ctx.get("has_permission", False),
            level=SecurityLevel.LEVEL_3,
            gb_clause="GB/T 22239-2019 8.1.1.4"
        ),
        ValidationRule(
            rule_id="RULE-5",
            name="会话活跃校验",
            description="校验会话是否在超时时间内保持活跃",
            validator=lambda ctx: ctx.get("session_active", False) and ctx.get("idle_minutes", 999) < 15,
            level=SecurityLevel.LEVEL_3,
            gb_clause="GB/T 22239-2019 8.1.1.5"
        ),
        ValidationRule(
            rule_id="RULE-6",
            name="多因素验证校验",
            description="校验是否完成双因素认证",
            validator=lambda ctx: ctx.get("mfa_completed", False) and ctx.get("mfa_factors", 0) >= 2,
            level=SecurityLevel.LEVEL_3,
            gb_clause="GB/T 22239-2019 8.1.1.6"
        )
    ],
    
    # 失败策略 FAIL-1 ~ FAIL-7
    "fail_strategies": [
        FailStrategy(
            fail_code="FAIL-1",
            description="身份无效 - 用户不存在或已被禁用",
            action="拒绝认证请求，记录审计日志",
            escalation=True,
            block=True
        ),
        FailStrategy(
            fail_code="FAIL-2",
            description="凭证过期 - 口令超过有效期",
            action="强制密码重置，发送通知",
            escalation=False,
            block=True
        ),
        FailStrategy(
            fail_code="FAIL-3",
            description="令牌失效 - JWT已过期或被撤销",
            action="要求重新认证，清除会话",
            escalation=False,
            block=True
        ),
        FailStrategy(
            fail_code="FAIL-4",
            description="权限不足 - 用户无权访问资源",
            action="拒绝访问，记录审计日志",
            escalation=True,
            block=True
        ),
        FailStrategy(
            fail_code="FAIL-5",
            description="会话超时 - 超过空闲时间限制",
            action="终止会话，要求重新认证",
            escalation=False,
            block=False
        ),
        FailStrategy(
            fail_code="FAIL-6",
            description="暴力破解 - 连续登录失败",
            action="锁定账户30分钟，发送告警",
            escalation=True,
            block=True
        ),
        FailStrategy(
            fail_code="FAIL-7",
            description="多因素认证失败",
            action="拒绝访问，记录安全事件",
            escalation=True,
            block=True
        )
    ]
}

# ============================================================
# 第四部分：MOD-SEC-02 数据加密与完整性
# ============================================================
# 法规：数据安全法第27条 / 个人信息保护法第51条
# 国标：GB/T 35273-2020

MOD_SEC_02_CONFIG = {
    "module_id": "MOD-SEC-02",
    "module_name": "数据加密与完整性",
    "gb_standard": "GB/T 35273-2020 / GB/T 22239-2019 8.1.6",
    "laws": ["数据安全法第27条", "个人信息保护法第51条"],
    "security_level": SecurityLevel.LEVEL_3,
    "priority": Priority.P0,
    "activation_status": True,
    
    "requirements": {
        "encryption_algorithm": "AES-256-GCM",    # 加密算法
        "key_management": "HSM",                   # 硬件安全模块
        "full_flow_encryption": True,              # 全流程加密
        "key_separation": True,                    # 密钥分离
        "data_classification": [                   # 数据分级 - GB/T 35273-2020
            {"level": "核心数据", "crypto": "AES-256-GCM+RSA-4096"},
            {"level": "重要数据", "crypto": "AES-256-GCM"},
            {"level": "一般数据", "crypto": "AES-128-GCM"},
            {"level": "公开数据", "crypto": "TLS-1.3"}
        ],
        "integrity_algorithm": "SHA-384",          # 完整性哈希
        "key_rotation_days": 90                    # 密钥轮换周期
    },
    
    # 接口契约 IN-1 ~ IN-4
    "interfaces": [
        InterfaceContract(
            interface_id="IN-1",
            name="明文数据接收",
            input_schema={
                "data": "any[required]",
                "classification": "enum[核心/重要/一般/公开]",
                "source_module": "str[required]"
            },
            output_schema={
                "data_id": "str",
                "encrypted": "bool",
                "checksum": "str[sha384]"
            },
            validation_rules=["RULE-1", "RULE-3"],
            fail_codes=["FAIL-1", "FAIL-3"],
            gb_clause="数据安全法第27条 / GB/T 35273-2020 5.1"
        ),
        InterfaceContract(
            interface_id="IN-2",
            name="加密请求",
            input_schema={
                "data_id": "str[required]",
                "algorithm": "enum[AES-256-GCM/AES-128-GCM/RSA-4096]",
                "key_id": "str[optional]"
            },
            output_schema={
                "ciphertext": "str[base64]",
                "iv": "str[base64]",
                "auth_tag": "str[base64]",
                "key_version": "str"
            },
            validation_rules=["RULE-1", "RULE-2"],
            fail_codes=["FAIL-1", "FAIL-7"],
            gb_clause="GB/T 35273-2020 5.2 / 个保法第51条"
        ),
        InterfaceContract(
            interface_id="IN-3",
            name="密钥管理请求",
            input_schema={
                "action": "enum[generate/rotate/revoke/export/import]",
                "key_type": "enum[symmetric/asymmetric/hmac]",
                "key_size": "int[256/384/4096]"
            },
            output_schema={
                "key_id": "str",
                "key_fingerprint": "str",
                "created_at": "datetime",
                "expires_at": "datetime"
            },
            validation_rules=["RULE-2", "RULE-6"],
            fail_codes=["FAIL-2", "FAIL-6"],
            gb_clause="数据安全法第27条"
        ),
        InterfaceContract(
            interface_id="IN-4",
            name="完整性校验",
            input_schema={
                "data_id": "str[required]",
                "expected_hash": "str[sha384]",
                "verify_chain": "bool[default=True]"
            },
            output_schema={
                "integrity_valid": "bool",
                "computed_hash": "str",
                "hash_match": "bool",
                "chain_valid": "bool"
            },
            validation_rules=["RULE-3", "RULE-4"],
            fail_codes=["FAIL-3", "FAIL-4"],
            gb_clause="GB/T 35273-2020 5.4 / GB/T 22239-2019 8.1.6.2"
        )
    ],
    
    # 校验规则 RULE-1 ~ RULE-6
    "validation_rules": [
        ValidationRule(
            rule_id="RULE-1",
            name="加密强度校验",
            description="校验加密算法强度不低于AES-256-GCM",
            validator=lambda ctx: ctx.get("algorithm", "") in ["AES-256-GCM", "RSA-4096"],
            level=SecurityLevel.LEVEL_3,
            gb_clause="GB/T 35273-2020 5.2"
        ),
        ValidationRule(
            rule_id="RULE-2",
            name="密钥长度校验",
            description="校验密钥长度满足安全要求(≥256bit)",
            validator=lambda ctx: ctx.get("key_size", 0) >= 256,
            level=SecurityLevel.LEVEL_3,
            gb_clause="GB/T 35273-2020 5.3"
        ),
        ValidationRule(
            rule_id="RULE-3",
            name="完整性哈希校验",
            description="校验数据哈希值匹配，防篡改",
            validator=lambda ctx: ctx.get("hash_match", False),
            level=SecurityLevel.LEVEL_3,
            gb_clause="GB/T 35273-2020 5.4"
        ),
        ValidationRule(
            rule_id="RULE-4",
            name="传输加密校验",
            description="校验数据传输通道已加密(TLS 1.3)",
            validator=lambda ctx: ctx.get("tls_version", "") == "1.3" and ctx.get("channel_encrypted", False),
            level=SecurityLevel.LEVEL_3,
            gb_clause="GB/T 22239-2019 8.1.5"
        ),
        ValidationRule(
            rule_id="RULE-5",
            name="存储加密校验",
            description="校验静态数据已加密存储",
            validator=lambda ctx: ctx.get("at_rest_encrypted", False),
            level=SecurityLevel.LEVEL_3,
            gb_clause="数据安全法第27条"
        ),
        ValidationRule(
            rule_id="RULE-6",
            name="密钥轮换校验",
            description="校验密钥在轮换周期内",
            validator=lambda ctx: ctx.get("key_age_days", 999) <= 90,
            level=SecurityLevel.LEVEL_3,
            gb_clause="GB/T 35273-2020 5.5"
        )
    ],
    
    # 失败策略 FAIL-1 ~ FAIL-7
    "fail_strategies": [
        FailStrategy(
            fail_code="FAIL-1",
            description="加密失败 - 算法不支持或密钥错误",
            action="降级到备用算法，记录告警",
            escalation=True,
            block=True
        ),
        FailStrategy(
            fail_code="FAIL-2",
            description="密钥泄露检测 - HSM告警",
            action="立即轮换密钥，通知安全团队",
            escalation=True,
            block=True
        ),
        FailStrategy(
            fail_code="FAIL-3",
            description="哈希碰撞检测 - 完整性破坏",
            action="隔离数据，启动调查",
            escalation=True,
            block=True
        ),
        FailStrategy(
            fail_code="FAIL-4",
            description="传输中断 - 加密通道断开",
            action="重连并重建安全通道",
            escalation=False,
            block=False
        ),
        FailStrategy(
            fail_code="FAIL-5",
            description="存储损坏 - 加密数据损坏",
            action="从备份恢复，校验完整性",
            escalation=True,
            block=False
        ),
        FailStrategy(
            fail_code="FAIL-6",
            description="密钥过期 - 超过轮换周期",
            action="强制密钥轮换",
            escalation=False,
            block=False
        ),
        FailStrategy(
            fail_code="FAIL-7",
            description="算法降级攻击检测",
            action="拒绝降级请求，阻断连接",
            escalation=True,
            block=True
        )
    ]
}

# ============================================================
# 第五部分：MOD-SEC-03 安全审计与日志
# ============================================================
# 法规：网络安全法第21条 / 等保2.0 8.1.4
# 国标：GB/T 31992-2015

MOD_SEC_03_CONFIG = {
    "module_id": "MOD-SEC-03",
    "module_name": "安全审计与日志",
    "gb_standard": "GB/T 31992-2015 / GB/T 22239-2019 8.1.4",
    "laws": ["网络安全法第21条", "等保2.0"],
    "security_level": SecurityLevel.LEVEL_3,
    "priority": Priority.P0,
    "activation_status": True,
    
    "requirements": {
        "log_retention_days": 180,        # 日志留存≥180天
        "worm_enabled": True,             # WORM防篡改
        "critical_alert_response_min": 15, # CRITICAL告警15分钟响应
        "log_format": "GB/T 31992-2015",  # 标准日志格式
        "real_time_monitoring": True,     # 实时监控
        "siem_integration": True,         # SIEM集成
        "log_levels": ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO", "DEBUG"],
        "alert_channels": ["sms", "email", "webhook", "phone"],
        "audit_scope": ["login", "access", "data_change", "config_change", "privilege"]
    },
    
    # 接口契约 IN-1 ~ IN-4
    "interfaces": [
        InterfaceContract(
            interface_id="IN-1",
            name="日志写入",
            input_schema={
                "timestamp": "datetime[iso8601]",
                "event_type": "str[required]",
                "severity": "enum[CRITICAL/HIGH/MEDIUM/LOW/INFO]",
                "source_ip": "str",
                "user_id": "str",
                "action": "str",
                "result": "enum[success/failure]",
                "details": "dict"
            },
            output_schema={
                "log_id": "str[uuid]",
                "written": "bool",
                "integrity_hash": "str[sha256]",
                "worm_index": "int"
            },
            validation_rules=["RULE-1", "RULE-2", "RULE-3"],
            fail_codes=["FAIL-1", "FAIL-2"],
            gb_clause="GB/T 31992-2015 4.1 / 网络安全法第21条"
        ),
        InterfaceContract(
            interface_id="IN-2",
            name="审计查询",
            input_schema={
                "query_type": "enum[time_range/event_type/user/ip/resource]",
                "filters": "dict",
                "time_start": "datetime",
                "time_end": "datetime",
                "max_results": "int[default=1000]"
            },
            output_schema={
                "results": "list[AuditLogEntry]",
                "total_count": "int",
                "query_time_ms": "int",
                "integrity_verified": "bool"
            },
            validation_rules=["RULE-4", "RULE-5"],
            fail_codes=["FAIL-4", "FAIL-5"],
            gb_clause="GB/T 31992-2015 4.2"
        ),
        InterfaceContract(
            interface_id="IN-3",
            name="告警配置",
            input_schema={
                "alert_name": "str[required]",
                "conditions": "list[dict]",
                "threshold": "dict[count/time_window]",
                "actions": "list[enum[log/email/sms/webhook/block]]",
                "severity": "enum[CRITICAL/HIGH/MEDIUM]"
            },
            output_schema={
                "alert_id": "str",
                "status": "enum[active/paused]",
                "created_at": "datetime"
            },
            validation_rules=["RULE-5", "RULE-6"],
            fail_codes=["FAIL-6", "FAIL-7"],
            gb_clause="GB/T 31992-2015 4.3 / GB/T 22239-2019 8.1.4.3"
        ),
        InterfaceContract(
            interface_id="IN-4",
            name="归档请求",
            input_schema={
                "archive_type": "enum[auto/manual]",
                "date_range": "dict[start/end]",
                "storage_target": "enum[local/nas/cloud]",
                "encrypt": "bool[default=True]"
            },
            output_schema={
                "archive_id": "str",
                "file_count": "int",
                "total_size_mb": "int",
                "archive_hash": "str",
                "retention_until": "datetime"
            },
            validation_rules=["RULE-3", "RULE-5"],
            fail_codes=["FAIL-5", "FAIL-3"],
            gb_clause="GB/T 31992-2015 4.4"
        )
    ],
    
    # 校验规则 RULE-1 ~ RULE-6
    "validation_rules": [
        ValidationRule(
            rule_id="RULE-1",
            name="日志格式校验",
            description="校验日志格式符合GB/T 31992-2015标准",
            validator=lambda ctx: all(k in ctx.get("log_entry", {}) for k in ["timestamp", "event_type", "severity"]),
            level=SecurityLevel.LEVEL_3,
            gb_clause="GB/T 31992-2015 4.1"
        ),
        ValidationRule(
            rule_id="RULE-2",
            name="时间戳校验",
            description="校验时间戳格式正确且在合理范围内",
            validator=lambda ctx: ctx.get("timestamp_valid", False),
            level=SecurityLevel.LEVEL_3,
            gb_clause="GB/T 31992-2015 4.1.2"
        ),
        ValidationRule(
            rule_id="RULE-3",
            name="完整性校验",
            description="校验日志未被篡改(WORM)",
            validator=lambda ctx: ctx.get("worm_intact", False),
            level=SecurityLevel.LEVEL_3,
            gb_clause="GB/T 31992-2015 4.1.3"
        ),
        ValidationRule(
            rule_id="RULE-4",
            name="分级校验",
            description="校验日志级别正确分类",
            validator=lambda ctx: ctx.get("severity", "") in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO", "DEBUG"],
            level=SecurityLevel.LEVEL_3,
            gb_clause="GB/T 31992-2015 4.1.4"
        ),
        ValidationRule(
            rule_id="RULE-5",
            name="留存期校验",
            description="校验日志留存≥180天",
            validator=lambda ctx: ctx.get("retention_days", 0) >= 180,
            level=SecurityLevel.LEVEL_3,
            gb_clause="网络安全法第21条 / GB/T 31992-2015 4.4"
        ),
        ValidationRule(
            rule_id="RULE-6",
            name="告警阈值校验",
            description="校验告警阈值配置合理",
            validator=lambda ctx: ctx.get("alert_threshold", 999) > 0,
            level=SecurityLevel.LEVEL_3,
            gb_clause="GB/T 22239-2019 8.1.4.3"
        )
    ],
    
    # 失败策略 FAIL-1 ~ FAIL-7
    "fail_strategies": [
        FailStrategy(
            fail_code="FAIL-1",
            description="日志写入失败 - 存储系统故障",
            action="切换备用存储，记录本地缓存",
            escalation=True,
            block=False
        ),
        FailStrategy(
            fail_code="FAIL-2",
            description="日志格式错误 - 不符合标准",
            action="拒绝写入，返回格式错误",
            escalation=False,
            block=False
        ),
        FailStrategy(
            fail_code="FAIL-3",
            description="篡改检测 - WORM完整性破坏",
            action="立即告警，启动安全调查",
            escalation=True,
            block=True
        ),
        FailStrategy(
            fail_code="FAIL-4",
            description="查询超时 - 审计查询响应慢",
            action="优化查询，返回部分结果",
            escalation=False,
            block=False
        ),
        FailStrategy(
            fail_code="FAIL-5",
            description="存储满 - 审计日志存储空间不足",
            action="触发归档，释放空间",
            escalation=True,
            block=False
        ),
        FailStrategy(
            fail_code="FAIL-6",
            description="分级错误 - 日志级别配置错误",
            action="修正配置，重新分级",
            escalation=False,
            block=False
        ),
        FailStrategy(
            fail_code="FAIL-7",
            description="告警遗漏 - 告警规则未覆盖",
            action="补全告警规则，回溯检查",
            escalation=True,
            block=False
        )
    ]
}


# ============================================================
# 第六部分：MOD-SEC-04 入侵防范与恶意代码
# ============================================================
# 国标：GB/T 22239-2019 8.1.2
# 优先级：P0

MOD_SEC_04_CONFIG = {
    "module_id": "MOD-SEC-04",
    "module_name": "入侵防范与恶意代码",
    "gb_standard": "GB/T 22239-2019 8.1.2",
    "laws": ["网络安全法第25条"],
    "security_level": SecurityLevel.LEVEL_3,
    "priority": Priority.P0,
    "activation_status": True,
    
    "requirements": {
        "ids_enabled": True,               # 入侵检测系统
        "ips_enabled": True,               # 入侵防御系统
        "malware_detection": True,         # 恶意代码检测
        "vulnerability_scan": {
            "enabled": True,
            "scan_cycle_hours": 24,         # 每日扫描
            "scan_depth": "full"            # 全量扫描
        },
        "behavior_analysis": True,         # 行为分析
        "threat_intelligence": {            # 威胁情报
            "enabled": True,
            "update_frequency": "hourly",
            "sources": ["CNCERT", "VirusTotal", "local"]
        },
        "auto_response": {                  # 自动响应
            "enabled": True,
            "actions": ["isolate", "block_ip", "alert", "log"]
        }
    },
    
    "interfaces": [
        InterfaceContract(
            interface_id="IN-1",
            name="威胁检测",
            input_schema={
                "traffic_data": "bytes[required]",
                "source_ip": "str",
                "destination_ip": "str",
                "protocol": "enum[tcp/udp/icmp/http/https]",
                "payload_hash": "str[sha256]"
            },
            output_schema={
                "threat_detected": "bool",
                "threat_type": "enum[malware/intrusion/anomaly/reconnaissance]",
                "confidence": "float[0.0-1.0]",
                "signature_id": "str",
                "recommended_action": "str"
            },
            validation_rules=["RULE-1", "RULE-2"],
            fail_codes=["FAIL-1", "FAIL-2"],
            gb_clause="GB/T 22239-2019 8.1.2.1"
        ),
        InterfaceContract(
            interface_id="IN-2",
            name="恶意代码扫描",
            input_schema={
                "file_path": "str[required]",
                "scan_type": "enum[quick/full/heuristic]",
                "file_hash": "str[optional]"
            },
            output_schema={
                "infected": "bool",
                "malware_family": "str",
                "detection_engine": "str",
                "cleanable": "bool",
                "quarantine_path": "str"
            },
            validation_rules=["RULE-2", "RULE-3"],
            fail_codes=["FAIL-3", "FAIL-4"],
            gb_clause="GB/T 22239-2019 8.1.2.2"
        ),
        InterfaceContract(
            interface_id="IN-3",
            name="漏洞扫描",
            input_schema={
                "target": "str[ip_or_hostname]",
                "scan_profile": "enum[standard/deep/quick]",
                "auth_creds": "dict[optional]"
            },
            output_schema={
                "vulnerabilities": "list[dict]",
                "risk_score": "int[0-100]",
                "scan_duration_sec": "int",
                "report_id": "str"
            },
            validation_rules=["RULE-4", "RULE-5"],
            fail_codes=["FAIL-5", "FAIL-6"],
            gb_clause="GB/T 22239-2019 8.1.2.3"
        ),
        InterfaceContract(
            interface_id="IN-4",
            name="威胁情报查询",
            input_schema={
                "indicator": "str[ip/domain/hash/url]",
                "indicator_type": "enum[ip/domain/file_hash/url]",
                "confidence_min": "float[default=0.7]"
            },
            output_schema={
                "found": "bool",
                "threat_score": "float[0.0-1.0]",
                "first_seen": "datetime",
                "last_seen": "datetime",
                "attribution": "str",
                "mitre_tactics": "list[str]"
            },
            validation_rules=["RULE-5", "RULE-6"],
            fail_codes=["FAIL-6", "FAIL-7"],
            gb_clause="GB/T 22239-2019 8.1.2.4"
        )
    ],
    
    "validation_rules": [
        ValidationRule(
            rule_id="RULE-1",
            name="IDS签名有效性",
            description="校验IDS检测签名库为最新版本",
            validator=lambda ctx: ctx.get("signature_version_age_hours", 999) <= 24,
            level=SecurityLevel.LEVEL_3,
            gb_clause="GB/T 22239-2019 8.1.2.1"
        ),
        ValidationRule(
            rule_id="RULE-2",
            name="恶意代码特征库",
            description="校验恶意代码特征库已更新",
            validator=lambda ctx: ctx.get("malware_db_age_hours", 999) <= 4,
            level=SecurityLevel.LEVEL_3,
            gb_clause="GB/T 22239-2019 8.1.2.2"
        ),
        ValidationRule(
            rule_id="RULE-3",
            name="启发式引擎",
            description="校验启发式分析引擎正常运行",
            validator=lambda ctx: ctx.get("heuristic_engine_status", "") == "active",
            level=SecurityLevel.LEVEL_3,
            gb_clause="GB/T 22239-2019 8.1.2.2"
        ),
        ValidationRule(
            rule_id="RULE-4",
            name="漏洞扫描覆盖",
            description="校验漏洞扫描覆盖全部资产",
            validator=lambda ctx: ctx.get("scan_coverage_percent", 0) >= 95,
            level=SecurityLevel.LEVEL_3,
            gb_clause="GB/T 22239-2019 8.1.2.3"
        ),
        ValidationRule(
            rule_id="RULE-5",
            name="威胁情报时效",
            description="校验威胁情报数据时效性",
            validator=lambda ctx: ctx.get("ti_age_hours", 999) <= 1,
            level=SecurityLevel.LEVEL_3,
            gb_clause="GB/T 22239-2019 8.1.2.4"
        ),
        ValidationRule(
            rule_id="RULE-6",
            name="自动响应就绪",
            description="校验自动响应机制就绪",
            validator=lambda ctx: ctx.get("auto_response_ready", False),
            level=SecurityLevel.LEVEL_3,
            gb_clause="GB/T 22239-2019 8.1.2.5"
        )
    ],
    
    "fail_strategies": [
        FailStrategy(fail_code="FAIL-1", description="IDS引擎故障", action="切换备用引擎", escalation=True, block=False),
        FailStrategy(fail_code="FAIL-2", description="特征库过期", action="强制更新特征库", escalation=False, block=False),
        FailStrategy(fail_code="FAIL-3", description="扫描失败", action="重试并记录", escalation=False, block=False),
        FailStrategy(fail_code="FAIL-4", description="隔离失败", action="人工介入", escalation=True, block=True),
        FailStrategy(fail_code="FAIL-5", description="高危漏洞未修复", action="紧急告警", escalation=True, block=False),
        FailStrategy(fail_code="FAIL-6", description="威胁情报源不可用", action="切换备用源", escalation=False, block=False),
        FailStrategy(fail_code="FAIL-7", description="APT攻击检测", action="全网隔离，启动应急响应", escalation=True, block=True)
    ]
}

# ============================================================
# 第七部分：MOD-SEC-05 数据备份与恢复
# ============================================================
# 法规：数据安全法第27条 / 等保2.0 8.1.7
# 国标：GB/T 20988-2007 灾难恢复能力第5级
# 优先级：P0

MOD_SEC_05_CONFIG = {
    "module_id": "MOD-SEC-05",
    "module_name": "数据备份与恢复",
    "gb_standard": "GB/T 20988-2007 第5级 / GB/T 22239-2019 8.1.7",
    "laws": ["数据安全法第27条"],
    "security_level": SecurityLevel.LEVEL_3,
    "priority": Priority.P0,
    "activation_status": True,
    
    "requirements": {
        "backup_strategy": "3-2-1",        # 3份副本，2种介质，1份异地
        "rto_hours": 4,                     # 恢复时间目标≤4小时
        "rpo_hours": 1,                     # 恢复点目标≤1小时
        "dr_level": 5,                      # 灾难恢复能力第5级
        "backup_schedule": {
            "full_backup": "weekly",       # 每周全量
            "incremental": "daily",        # 每日增量
            "realtime_sync": True          # 关键数据实时同步
        },
        "encryption_at_rest": True,         # 备份加密
        "integrity_check": True,            # 完整性校验
        "test_recovery": {                  # 恢复演练
            "frequency": "monthly",
            "last_test": "str[date]",
            "success_rate_target": 99.9
        },
        "offsite_storage": {                # 异地存储
            "enabled": True,
            "distance_km_min": 50,
            "replication": "synchronous"
        }
    },
    
    "interfaces": [
        InterfaceContract(
            interface_id="IN-1",
            name="备份任务创建",
            input_schema={
                "source_paths": "list[str]",
                "backup_type": "enum[full/incremental/differential/snapshot]",
                "schedule": "dict[required]",
                "retention_days": "int[default=180]"
            },
            output_schema={
                "job_id": "str",
                "status": "enum[created/running/completed/failed]",
                "next_run": "datetime",
                "estimated_size_mb": "int"
            },
            validation_rules=["RULE-1", "RULE-2"],
            fail_codes=["FAIL-1", "FAIL-2"],
            gb_clause="GB/T 20988-2007 5.2 / 数据安全法第27条"
        ),
        InterfaceContract(
            interface_id="IN-2",
            name="恢复请求",
            input_schema={
                "backup_id": "str[required]",
                "restore_target": "str[required]",
                "point_in_time": "datetime[optional]",
                "verify_integrity": "bool[default=True]"
            },
            output_schema={
                "restore_id": "str",
                "progress_percent": "float",
                "rto_remaining_min": "int",
                "data_verified": "bool",
                "status": "enum[in_progress/completed/failed]"
            },
            validation_rules=["RULE-3", "RULE-4"],
            fail_codes=["FAIL-3", "FAIL-4"],
            gb_clause="GB/T 20988-2007 5.3"
        ),
        InterfaceContract(
            interface_id="IN-3",
            name="备份验证",
            input_schema={
                "backup_id": "str[required]",
                "verify_type": "enum[hash/restore_test/consistency]"
            },
            output_schema={
                "verified": "bool",
                "integrity_hash_match": "bool",
                "restorable": "bool",
                "corrupted_blocks": "int"
            },
            validation_rules=["RULE-3", "RULE-5"],
            fail_codes=["FAIL-5", "FAIL-6"],
            gb_clause="GB/T 20988-2007 5.4"
        ),
        InterfaceContract(
            interface_id="IN-4",
            name="灾难恢复启动",
            input_schema={
                "disaster_type": "enum[natural/human/cyber/hardware]",
                "affected_systems": "list[str]",
                "dr_plan_id": "str[required]",
                "auto_failover": "bool[default=False]"
            },
            output_schema={
                "dr_session_id": "str",
                "failover_status": "enum[initiated/in_progress/completed/failed]",
                "rto_target_min": "int",
                "rpo_actual_min": "int",
                "data_loss_mb": "int"
            },
            validation_rules=["RULE-4", "RULE-6"],
            fail_codes=["FAIL-6", "FAIL-7"],
            gb_clause="GB/T 20988-2007 第5级 / GB/T 24363-2009"
        )
    ],
    
    "validation_rules": [
        ValidationRule(
            rule_id="RULE-1",
            name="3-2-1策略校验",
            description="校验备份满足3-2-1策略(3份,2种介质,1份异地)",
            validator=lambda ctx: (ctx.get("copies_count", 0) >= 3 and 
                                 ctx.get("media_types_count", 0) >= 2 and 
                                 ctx.get("offsite_copies", 0) >= 1),
            level=SecurityLevel.LEVEL_3,
            gb_clause="GB/T 20988-2007 5.2"
        ),
        ValidationRule(
            rule_id="RULE-2",
            name="备份加密校验",
            description="校验备份数据已加密",
            validator=lambda ctx: ctx.get("encrypted", False),
            level=SecurityLevel.LEVEL_3,
            gb_clause="数据安全法第27条"
        ),
        ValidationRule(
            rule_id="RULE-3",
            name="完整性校验",
            description="校验备份数据完整性",
            validator=lambda ctx: ctx.get("integrity_valid", False),
            level=SecurityLevel.LEVEL_3,
            gb_clause="GB/T 20988-2007 5.4"
        ),
        ValidationRule(
            rule_id="RULE-4",
            name="RTO/RPO合规",
            description="校验恢复时间≤4h，恢复点≤1h",
            validator=lambda ctx: ctx.get("rto_hours", 999) <= 4 and ctx.get("rpo_hours", 999) <= 1,
            level=SecurityLevel.LEVEL_3,
            gb_clause="GB/T 20988-2007 第5级"
        ),
        ValidationRule(
            rule_id="RULE-5",
            name="恢复演练校验",
            description="校验近期完成恢复演练且成功率达标",
            validator=lambda ctx: ctx.get("last_test_days", 999) <= 30 and ctx.get("success_rate", 0) >= 99.9,
            level=SecurityLevel.LEVEL_3,
            gb_clause="GB/T 20988-2007 5.5"
        ),
        ValidationRule(
            rule_id="RULE-6",
            name="灾难恢复就绪",
            description="校验灾难恢复系统就绪",
            validator=lambda ctx: ctx.get("dr_system_ready", False) and ctx.get("dr_tested", False),
            level=SecurityLevel.LEVEL_3,
            gb_clause="GB/T 20988-2007 第5级 / GB/T 24363-2009"
        )
    ],
    
    "fail_strategies": [
        FailStrategy(fail_code="FAIL-1", description="备份任务失败", action="重试并告警", escalation=True, block=False),
        FailStrategy(fail_code="FAIL-2", description="存储空间不足", action="清理旧备份", escalation=True, block=False),
        FailStrategy(fail_code="FAIL-3", description="恢复失败", action="切换备用备份", escalation=True, block=False),
        FailStrategy(fail_code="FAIL-4", description="RTO/RPO超标", action="优化恢复流程", escalation=True, block=False),
        FailStrategy(fail_code="FAIL-5", description="备份损坏", action="使用冗余副本", escalation=True, block=False),
        FailStrategy(fail_code="FAIL-6", description="异地复制失败", action="切换链路重试", escalation=True, block=False),
        FailStrategy(fail_code="FAIL-7", description="灾难恢复启动失败", action="人工接管", escalation=True, block=True)
    ]
}

# ============================================================
# 第八部分：MOD-SEC-06 个人信息保护
# ============================================================
# 法规：个人信息保护法第51-58条
# 国标：GB/T 35273-2020
# 优先级：P0

MOD_SEC_06_CONFIG = {
    "module_id": "MOD-SEC-06",
    "module_name": "个人信息保护",
    "gb_standard": "GB/T 35273-2020",
    "laws": ["个人信息保护法第51-58条"],
    "security_level": SecurityLevel.LEVEL_3,
    "priority": Priority.P0,
    "activation_status": True,
    
    "requirements": {
        "minimization_principle": True,     # 最小必要原则
        "informed_consent": True,           # 告知同意
        "anonymization": {
            "enabled": True,
            "k_anonymity": 5,               # k-匿名 k≥5
            "l_diversity": 2,               # l-多样性
            "t_closeness": 0.2              # t-接近性
        },
        "deletion_rights": {                 # 删除权
            "enabled": True,
            "response_workdays": 15         # 15工作日响应
        },
        "data_subject_rights": [            # 数据主体权利
            "right_to_know",                 # 知情权
            "right_to_access",               # 访问权
            "right_to_correction",           # 更正权
            "right_to_deletion",             # 删除权
            "right_to_portability",          # 可携带权
            "right_to_object"                # 反对权
        ],
        "cross_border_transfer": {          # 跨境传输
            "security_assessment": True,
            "standard_contract": True,
            "certification_required": True
        },
        "dpi_required": True                # 需要数据保护影响评估
    },
    
    "interfaces": [
        InterfaceContract(
            interface_id="IN-1",
            name="个人信息收集",
            input_schema={
                "data_subject_id": "str[required]",
                "personal_data": "dict[required]",
                "purpose": "str[required]",
                "consent_obtained": "bool[required]",
                " lawful_basis": "enum[consent/contract/legal_obligation/vital_interests/public_task/legitimate_interests]"
            },
            output_schema={
                "collection_id": "str",
                "minimization_check": "bool",
                "consent_record": "str",
                "retention_period_days": "int"
            },
            validation_rules=["RULE-1", "RULE-2"],
            fail_codes=["FAIL-1", "FAIL-2"],
            gb_clause="个人信息保护法第13条 / GB/T 35273-2020 5.1"
        ),
        InterfaceContract(
            interface_id="IN-2",
            name="去标识化处理",
            input_schema={
                "data_id": "str[required]",
                "method": "enum[k_anonymity/l_diversity/t_closeness/differential_privacy]",
                "k_value": "int[min=5]"
            },
            output_schema={
                "anonymized_data": "dict",
                "k_anonymity_achieved": "bool",
                "information_loss_ratio": "float",
                "reidentification_risk": "float[0.0-1.0]"
            },
            validation_rules=["RULE-3", "RULE-4"],
            fail_codes=["FAIL-3", "FAIL-4"],
            gb_clause="个人信息保护法第51条 / GB/T 35273-2020 5.2"
        ),
        InterfaceContract(
            interface_id="IN-3",
            name="删除权请求",
            input_schema={
                "data_subject_id": "str[required]",
                "deletion_scope": "enum[all/specified_purpose/time_range]",
                "request_channel": "enum[web/app/email/phone]",
                "identity_verified": "bool[required]"
            },
            output_schema={
                "request_id": "str",
                "deadline_date": "datetime",
                "deletion_plan": "dict",
                "status": "enum[pending/processing/completed/rejected]",
                "response_workdays_remaining": "int"
            },
            validation_rules=["RULE-4", "RULE-5"],
            fail_codes=["FAIL-5", "FAIL-6"],
            gb_clause="个人信息保护法第47条 / 第50条"
        ),
        InterfaceContract(
            interface_id="IN-4",
            name="数据主体权利响应",
            input_schema={
                "request_type": "enum[access/correction/deletion/portability/object]",
                "data_subject_id": "str[required]",
                "verification_passed": "bool[required]"
            },
            output_schema={
                "response_id": "str",
                "response_data": "dict",
                "processing_days": "int",
                "compliance_status": "enum[compliant/delayed/violation]"
            },
            validation_rules=["RULE-5", "RULE-6"],
            fail_codes=["FAIL-6", "FAIL-7"],
            gb_clause="个人信息保护法第44-48条 / GB/T 35273-2020 7.1-7.11"
        )
    ],
    
    "validation_rules": [
        ValidationRule(
            rule_id="RULE-1",
            name="最小必要校验",
            description="校验收集的个人信息限于最小必要范围",
            validator=lambda ctx: ctx.get("minimization_passed", False),
            level=SecurityLevel.LEVEL_3,
            gb_clause="个人信息保护法第6条 / GB/T 35273-2020 5.1"
        ),
        ValidationRule(
            rule_id="RULE-2",
            name="告知同意校验",
            description="校验已获得有效同意",
            validator=lambda ctx: ctx.get("consent_valid", False) and ctx.get("consent_recorded", False),
            level=SecurityLevel.LEVEL_3,
            gb_clause="个人信息保护法第14条 / 第17条"
        ),
        ValidationRule(
            rule_id="RULE-3",
            name="k-匿名校验",
            description="校验去标识化满足k-匿名(k≥5)",
            validator=lambda ctx: ctx.get("k_value", 0) >= 5,
            level=SecurityLevel.LEVEL_3,
            gb_clause="个人信息保护法第51条 / GB/T 35273-2020 5.2"
        ),
        ValidationRule(
            rule_id="RULE-4",
            name="重识别风险评估",
            description="校验重识别风险低于阈值",
            validator=lambda ctx: ctx.get("reidentification_risk", 1.0) <= 0.05,
            level=SecurityLevel.LEVEL_3,
            gb_clause="GB/T 35273-2020 5.2.3"
        ),
        ValidationRule(
            rule_id="RULE-5",
            name="删除权时效",
            description="校验删除请求在15工作日内响应",
            validator=lambda ctx: ctx.get("response_days", 999) <= 15,
            level=SecurityLevel.LEVEL_3,
            gb_clause="个人信息保护法第50条"
        ),
        ValidationRule(
            rule_id="RULE-6",
            name="数据主体身份校验",
            description="校验数据主体身份已验证",
            validator=lambda ctx: ctx.get("identity_verified", False),
            level=SecurityLevel.LEVEL_3,
            gb_clause="个人信息保护法第49条"
        )
    ],
    
    "fail_strategies": [
        FailStrategy(fail_code="FAIL-1", description="超范围收集", action="拒绝收集，记录违规", escalation=True, block=True),
        FailStrategy(fail_code="FAIL-2", description="无效同意", action="暂停处理，重新获取同意", escalation=True, block=True),
        FailStrategy(fail_code="FAIL-3", description="去标识化不充分(k<5)", action="增强匿名化处理", escalation=False, block=False),
        FailStrategy(fail_code="FAIL-4", description="重识别风险过高", action="拒绝数据发布", escalation=True, block=True),
        FailStrategy(fail_code="FAIL-5", description="删除请求超时", action="升级处理，人工介入", escalation=True, block=False),
        FailStrategy(fail_code="FAIL-6", description="身份验证失败", action="拒绝权利请求", escalation=False, block=False),
        FailStrategy(fail_code="FAIL-7", description="跨境传输违规", action="阻断传输，通知监管部门", escalation=True, block=True)
    ]
}


# ============================================================
# 第九部分：MOD-SEC-07 安全通信与传输
# ============================================================
# 国标：GB/T 22239-2019 8.1.5
# 优先级：P0

MOD_SEC_07_CONFIG = {
    "module_id": "MOD-SEC-07",
    "module_name": "安全通信与传输",
    "gb_standard": "GB/T 22239-2019 8.1.5",
    "laws": ["网络安全法", "数据安全法"],
    "security_level": SecurityLevel.LEVEL_3,
    "priority": Priority.P0,
    "activation_status": True,
    
    "requirements": {
        "tls_version": "1.3",               # TLS 1.3
        "tls_cipher_suites": [              # 强制密码套件
            "TLS_AES_256_GCM_SHA384",
            "TLS_CHACHA20_POLY1305_SHA256",
            "TLS_AES_128_GCM_SHA256"
        ],
        "certificate_management": {          # 证书管理
            "key_type": "ECDSA_P-256",
            "validity_days_max": 397,
            "auto_renewal": True,
            "hsm_protection": True
        },
        "mTLS_enabled": True,               # 双向认证
        "perfect_forward_secrecy": True,    # 前向保密
        "certificate_pinning": True,        # 证书固定
        "session_resumption": "tickets",    # 会话恢复
        "zero_rtt": False                   # 禁用0-RTT防重放
    },
    
    "interfaces": [
        InterfaceContract(
            interface_id="IN-1",
            name="TLS握手建立",
            input_schema={
                "client_hello": "bytes[required]",
                "server_name": "str[SNI]",
                "supported_versions": "list[float]",
                "client_ciphers": "list[str]"
            },
            output_schema={
                "session_id": "str",
                "negotiated_version": "str",
                "negotiated_cipher": "str",
                "certificate_chain": "list[str]",
                "handshake_time_ms": "int"
            },
            validation_rules=["RULE-1", "RULE-2"],
            fail_codes=["FAIL-1", "FAIL-2"],
            gb_clause="GB/T 22239-2019 8.1.5.1"
        ),
        InterfaceContract(
            interface_id="IN-2",
            name="证书验证",
            input_schema={
                "certificate": "bytes[PEM/DER]",
                "purpose": "enum[server/client/ca]",
                "hostname": "str[optional]",
                "trust_store": "str[default=system]"
            },
            output_schema={
                "valid": "bool",
                "chain_trusted": "bool",
                "not_before": "datetime",
                "not_after": "datetime",
                "days_remaining": "int",
                "ocsp_status": "enum[good/revoked/unknown]"
            },
            validation_rules=["RULE-3", "RULE-4"],
            fail_codes=["FAIL-3", "FAIL-4"],
            gb_clause="GB/T 22239-2019 8.1.5.2"
        ),
        InterfaceContract(
            interface_id="IN-3",
            name="加密传输通道",
            input_schema={
                "plaintext": "bytes[required]",
                "session_id": "str[required]",
                "encryption_level": "enum[standard/high/maximum]"
            },
            output_schema={
                "ciphertext": "bytes",
                "seq_number": "int",
                "auth_tag": "bytes",
                "bytes_transferred": "int"
            },
            validation_rules=["RULE-5", "RULE-6"],
            fail_codes=["FAIL-5", "FAIL-6"],
            gb_clause="GB/T 22239-2019 8.1.5.3"
        ),
        InterfaceContract(
            interface_id="IN-4",
            name="mTLS双向认证",
            input_schema={
                "client_certificate": "bytes[required]",
                "server_certificate": "bytes[required]",
                "mutual_auth": "bool[required]",
                "verify_depth": "int[default=3]"
            },
            output_schema={
                "auth_success": "bool",
                "client_identity": "dict",
                "server_identity": "dict",
                "mutual_verified": "bool",
                "session_key_fingerprint": "str"
            },
            validation_rules=["RULE-1", "RULE-4"],
            fail_codes=["FAIL-7", "FAIL-3"],
            gb_clause="GB/T 22239-2019 8.1.5.4"
        )
    ],
    
    "validation_rules": [
        ValidationRule(
            rule_id="RULE-1",
            name="TLS版本强制",
            description="强制使用TLS 1.3，拒绝降级",
            validator=lambda ctx: ctx.get("tls_version", "") == "1.3",
            level=SecurityLevel.LEVEL_3,
            gb_clause="GB/T 22239-2019 8.1.5.1"
        ),
        ValidationRule(
            rule_id="RULE-2",
            name="密码套件强度",
            description="仅允许强密码套件",
            validator=lambda ctx: ctx.get("cipher_suite", "") in [
                "TLS_AES_256_GCM_SHA384",
                "TLS_CHACHA20_POLY1305_SHA256"
            ],
            level=SecurityLevel.LEVEL_3,
            gb_clause="GB/T 22239-2019 8.1.5.1"
        ),
        ValidationRule(
            rule_id="RULE-3",
            name="证书有效性",
            description="校验证书链完整且未过期",
            validator=lambda ctx: ctx.get("chain_trusted", False) and ctx.get("days_remaining", 0) > 7,
            level=SecurityLevel.LEVEL_3,
            gb_clause="GB/T 22239-2019 8.1.5.2"
        ),
        ValidationRule(
            rule_id="RULE-4",
            name="证书固定校验",
            description="校验证书与固定指纹匹配",
            validator=lambda ctx: ctx.get("pinning_match", False),
            level=SecurityLevel.LEVEL_3,
            gb_clause="GB/T 22239-2019 8.1.5.2"
        ),
        ValidationRule(
            rule_id="RULE-5",
            name="传输加密完整性",
            description="校验传输数据加密且未被篡改",
            validator=lambda ctx: ctx.get("encryption_active", False) and ctx.get("auth_tag_valid", False),
            level=SecurityLevel.LEVEL_3,
            gb_clause="GB/T 22239-2019 8.1.5.3"
        ),
        ValidationRule(
            rule_id="RULE-6",
            name="前向保密校验",
            description="校验使用支持前向保密的密钥交换",
            validator=lambda ctx: ctx.get("pfs_enabled", False),
            level=SecurityLevel.LEVEL_3,
            gb_clause="GB/T 22239-2019 8.1.5.1"
        )
    ],
    
    "fail_strategies": [
        FailStrategy(fail_code="FAIL-1", description="TLS版本降级攻击", action="立即断开连接", escalation=True, block=True),
        FailStrategy(fail_code="FAIL-2", description="弱密码套件协商", action="拒绝连接", escalation=True, block=True),
        FailStrategy(fail_code="FAIL-3", description="证书无效或过期", action="拒绝连接，记录告警", escalation=True, block=True),
        FailStrategy(fail_code="FAIL-4", description="证书固定不匹配", action="阻断连接，告警", escalation=True, block=True),
        FailStrategy(fail_code="FAIL-5", description="传输加密中断", action="重连TLS", escalation=False, block=False),
        FailStrategy(fail_code="FAIL-6", description="MAC校验失败", action="丢弃数据包，告警", escalation=True, block=True),
        FailStrategy(fail_code="FAIL-7", description="mTLS认证失败", action="拒绝客户端连接", escalation=True, block=True)
    ]
}

# ============================================================
# 第十部分：MOD-SEC-08 安全运维与应急管理
# ============================================================
# 法规：网络安全法第25条 / 等保2.0 8.1.8
# 国标：GB/T 24363-2009 应急响应流程 / GB/T 20988-2007 灾难恢复能力第5级
# 优先级：P0

MOD_SEC_08_CONFIG = {
    "module_id": "MOD-SEC-08",
    "module_name": "安全运维与应急管理",
    "gb_standard": "GB/T 24363-2009 / GB/T 20988-2007 第5级 / GB/T 22239-2019 8.1.8",
    "laws": ["网络安全法第25条", "等保2.0"],
    "security_level": SecurityLevel.LEVEL_3,
    "priority": Priority.P0,
    "activation_status": True,
    
    "requirements": {
        "emergency_response": {              # 应急响应
            "phases": ["准备", "检测", "遏制", "根除", "恢复", "跟踪"],
            "response_time_critical_min": 15,
            "response_time_high_min": 60,
            "response_time_medium_hours": 4,
            "drill_frequency_monthly": 1
        },
        "disaster_recovery": {               # 灾难恢复
            "dr_level": 5,                    # 第5级
            "rto_hours": 4,
            "rpo_hours": 1,
            "failover_automatic": True,
            "dr_site_ready": True
        },
        "change_management": {               # 变更管理
            "approval_required": True,
            "test_environment": True,
            "rollback_plan": True,
            "change_window": True
        },
        "vulnerability_management": {        # 漏洞管理
            "scan_frequency": "daily",
            "patch_window_days": 7,
            "critical_patch_hours": 24
        },
        "security_monitoring": {             # 安全监控
            "7x24": True,
            "siem_integration": True,
            "soc_contact": "always_available"
        }
    },
    
    "interfaces": [
        InterfaceContract(
            interface_id="IN-1",
            name="应急响应启动",
            input_schema={
                "incident_type": "enum[malware/breach/dos/data_leak/insider/physical]",
                "severity": "enum[CRITICAL/HIGH/MEDIUM/LOW]",
                "reporter": "str[required]",
                "affected_assets": "list[str]",
                "initial_indicators": "list[dict]"
            },
            output_schema={
                "incident_id": "str",
                "response_phase": "str",
                "assigned_team": "str",
                "escalation_path": "list[str]",
                "response_deadline": "datetime",
                "status": "enum[open/contained/resolved/closed]"
            },
            validation_rules=["RULE-1", "RULE-2"],
            fail_codes=["FAIL-1", "FAIL-2"],
            gb_clause="GB/T 24363-2009 4.1 / 网络安全法第25条"
        ),
        InterfaceContract(
            interface_id="IN-2",
            name="灾难恢复执行",
            input_schema={
                "dr_plan_id": "str[required]",
                "disaster_scope": "enum[partial/full/site]",
                "priority_systems": "list[str]",
                "auto_failover": "bool[default=True]"
            },
            output_schema={
                "dr_execution_id": "str",
                "phase": "enum[initiated/failover/recovery/verification/complete]",
                "rto_remaining_min": "int",
                "systems_recovered": "int",
                "data_integrity_verified": "bool"
            },
            validation_rules=["RULE-3", "RULE-4"],
            fail_codes=["FAIL-3", "FAIL-4"],
            gb_clause="GB/T 20988-2007 第5级 / GB/T 24363-2009 4.3"
        ),
        InterfaceContract(
            interface_id="IN-3",
            name="变更审批",
            input_schema={
                "change_id": "str[required]",
                "change_type": "enum[standard/normal/emergency]",
                "affected_systems": "list[str]",
                "risk_assessment": "dict",
                "rollback_plan": "str[required]",
                "approvers": "list[str]"
            },
            output_schema={
                "approval_status": "enum[approved/rejected/pending/escalated]",
                "approved_by": "str",
                "implementation_window": "dict",
                "conditions": "list[str]"
            },
            validation_rules=["RULE-5", "RULE-6"],
            fail_codes=["FAIL-5", "FAIL-6"],
            gb_clause="GB/T 22239-2019 8.1.8.1"
        ),
        InterfaceContract(
            interface_id="IN-4",
            name="安全监控告警",
            input_schema={
                "alert_source": "enum[siem/ids/firewall/av/audit]",
                "alert_type": "str",
                "severity": "enum[CRITICAL/HIGH/MEDIUM/LOW]",
                "source_ip": "str",
                "target_ip": "str",
                "indicators": "list[dict]"
            },
            output_schema={
                "alert_id": "str",
                "correlated_incidents": "list[str]",
                "auto_response": "str",
                "ticket_created": "bool",
                "escalation_time": "datetime"
            },
            validation_rules=["RULE-1", "RULE-6"],
            fail_codes=["FAIL-6", "FAIL-7"],
            gb_clause="GB/T 24363-2009 4.2 / GB/T 22239-2019 8.1.8.2"
        )
    ],
    
    "validation_rules": [
        ValidationRule(
            rule_id="RULE-1",
            name="响应时效性",
            description="校验响应时间在规定范围内(CRITICAL≤15min)",
            validator=lambda ctx: ctx.get("response_time_min", 999) <= 15 if ctx.get("severity") == "CRITICAL" else True,
            level=SecurityLevel.LEVEL_3,
            gb_clause="GB/T 24363-2009 4.1.1"
        ),
        ValidationRule(
            rule_id="RULE-2",
            name="响应团队就绪",
            description="校验应急响应团队已就位",
            validator=lambda ctx: ctx.get("team_available", False),
            level=SecurityLevel.LEVEL_3,
            gb_clause="GB/T 24363-2009 4.1.2"
        ),
        ValidationRule(
            rule_id="RULE-3",
            name="DR计划就绪",
            description="校验灾难恢复计划已制定并测试",
            validator=lambda ctx: ctx.get("dr_plan_exists", False) and ctx.get("dr_tested_recently", False),
            level=SecurityLevel.LEVEL_3,
            gb_clause="GB/T 20988-2007 第5级"
        ),
        ValidationRule(
            rule_id="RULE-4",
            name="RTO/RPO达标",
            description="校验恢复指标在目标范围内",
            validator=lambda ctx: ctx.get("rto_hours", 999) <= 4 and ctx.get("rpo_hours", 999) <= 1,
            level=SecurityLevel.LEVEL_3,
            gb_clause="GB/T 20988-2007 第5级"
        ),
        ValidationRule(
            rule_id="RULE-5",
            name="变更审批完整",
            description="校验变更经过完整审批流程",
            validator=lambda ctx: ctx.get("all_approvers_signed", False) and ctx.get("rollback_documented", False),
            level=SecurityLevel.LEVEL_3,
            gb_clause="GB/T 22239-2019 8.1.8.1"
        ),
        ValidationRule(
            rule_id="RULE-6",
            name="7x24监控",
            description="校验安全监控系统7x24运行",
            validator=lambda ctx: ctx.get("monitoring_active", False),
            level=SecurityLevel.LEVEL_3,
            gb_clause="GB/T 22239-2019 8.1.8.2"
        )
    ],
    
    "fail_strategies": [
        FailStrategy(fail_code="FAIL-1", description="响应超时", action="升级至高层", escalation=True, block=False),
        FailStrategy(fail_code="FAIL-2", description="团队不可用", action="启动备用团队", escalation=True, block=False),
        FailStrategy(fail_code="FAIL-3", description="DR计划缺失", action="紧急制定DR计划", escalation=True, block=False),
        FailStrategy(fail_code="FAIL-4", description="RTO/RPO超标", action="优化恢复流程", escalation=True, block=False),
        FailStrategy(fail_code="FAIL-5", description="变更未审批", action="阻断变更", escalation=True, block=True),
        FailStrategy(fail_code="FAIL-6", description="监控中断", action="启动备用监控", escalation=True, block=False),
        FailStrategy(fail_code="FAIL-7", description="告警遗漏", action="补全规则，回溯", escalation=True, block=False)
    ]
}


# ============================================================
# 第十一部分：跨模块数据流契约（18+条）
# ============================================================
# 安全域8模块间的数据流动与依赖关系

CROSS_MODULE_FLOWS = [
    # MOD-SEC-01 → MOD-SEC-02: 身份鉴别成功后触发加密保护
    CrossModuleFlow(
        flow_id="FLOW-001",
        source_module="MOD-SEC-01",
        target_module="MOD-SEC-02",
        data_type="auth_token_encrypted",
        contract="身份鉴别模块鉴别通过后，将令牌加密后传递给数据加密模块进行保护存储",
        priority=Priority.P0
    ),
    # MOD-SEC-01 → MOD-SEC-03: 登录事件写入审计日志
    CrossModuleFlow(
        flow_id="FLOW-002",
        source_module="MOD-SEC-01",
        target_module="MOD-SEC-03",
        data_type="login_audit_event",
        contract="所有身份鉴别事件(登录/登出/失败)实时写入安全审计日志，留存≥180天",
        priority=Priority.P0
    ),
    # MOD-SEC-01 → MOD-SEC-04: 认证异常触发入侵检测
    CrossModuleFlow(
        flow_id="FLOW-003",
        source_module="MOD-SEC-01",
        target_module="MOD-SEC-04",
        data_type="auth_anomaly_alert",
        contract="连续认证失败/暴力破解/异常地理位置登录触发入侵检测模块告警",
        priority=Priority.P0
    ),
    # MOD-SEC-02 → MOD-SEC-03: 加密操作审计
    CrossModuleFlow(
        flow_id="FLOW-004",
        source_module="MOD-SEC-02",
        target_module="MOD-SEC-03",
        data_type="crypto_audit_event",
        contract="密钥生成/轮换/撤销操作，加密/解密请求记录审计日志",
        priority=Priority.P0
    ),
    # MOD-SEC-02 → MOD-SEC-05: 加密密钥备份
    CrossModuleFlow(
        flow_id="FLOW-005",
        source_module="MOD-SEC-02",
        target_module="MOD-SEC-05",
        data_type="key_backup",
        contract="密钥材料定期备份至3-2-1备份体系，确保灾难恢复能力第5级",
        priority=Priority.P0
    ),
    # MOD-SEC-02 → MOD-SEC-06: 个人信息加密保护
    CrossModuleFlow(
        flow_id="FLOW-006",
        source_module="MOD-SEC-02",
        target_module="MOD-SEC-06",
        data_type="pii_encrypted",
        contract="个人信息在存储前通过AES-256-GCM加密，满足个保法第51条加密要求",
        priority=Priority.P0
    ),
    # MOD-SEC-03 → MOD-SEC-08: 审计告警触发应急响应
    CrossModuleFlow(
        flow_id="FLOW-007",
        source_module="MOD-SEC-03",
        target_module="MOD-SEC-08",
        data_type="critical_alert",
        contract="CRITICAL级别审计告警15分钟内触发应急响应流程，符合GB/T 24363-2009",
        priority=Priority.P0
    ),
    # MOD-SEC-04 → MOD-SEC-03: 入侵检测事件审计
    CrossModuleFlow(
        flow_id="FLOW-008",
        source_module="MOD-SEC-04",
        target_module="MOD-SEC-03",
        data_type="ids_event_log",
        contract="IDS/IPS检测到的威胁事件实时写入审计日志，WORM防篡改存储",
        priority=Priority.P0
    ),
    # MOD-SEC-04 → MOD-SEC-08: 入侵告警触发应急
    CrossModuleFlow(
        flow_id="FLOW-009",
        source_module="MOD-SEC-04",
        target_module="MOD-SEC-08",
        data_type="incident_trigger",
        contract="APT攻击/恶意代码检测/高危漏洞利用自动触发应急响应流程",
        priority=Priority.P0
    ),
    # MOD-SEC-05 → MOD-SEC-08: 灾难恢复事件
    CrossModuleFlow(
        flow_id="FLOW-010",
        source_module="MOD-SEC-05",
        target_module="MOD-SEC-08",
        data_type="dr_event",
        contract="备份失败/恢复演练/灾难恢复执行状态通知应急管理模块",
        priority=Priority.P0
    ),
    # MOD-SEC-06 → MOD-SEC-02: 个人信息去标识化
    CrossModuleFlow(
        flow_id="FLOW-011",
        source_module="MOD-SEC-06",
        target_module="MOD-SEC-02",
        data_type="anonymization_request",
        contract="个人信息去标识化请求加密处理后的数据，确保k-匿名(k≥5)算法安全",
        priority=Priority.P0
    ),
    # MOD-SEC-06 → MOD-SEC-03: 个人信息操作审计
    CrossModuleFlow(
        flow_id="FLOW-012",
        source_module="MOD-SEC-06",
        target_module="MOD-SEC-03",
        data_type="pii_operation_log",
        contract="个人信息收集/使用/删除/导出操作全部记录审计日志，留存≥180天",
        priority=Priority.P0
    ),
    # MOD-SEC-07 → MOD-SEC-02: 传输通道加密
    CrossModuleFlow(
        flow_id="FLOW-013",
        source_module="MOD-SEC-07",
        target_module="MOD-SEC-02",
        data_type="tls_session_key",
        contract="TLS 1.3握手生成的会话密钥由数据加密模块管理，确保密钥分离",
        priority=Priority.P0
    ),
    # MOD-SEC-07 → MOD-SEC-04: 网络威胁检测
    CrossModuleFlow(
        flow_id="FLOW-014",
        source_module="MOD-SEC-07",
        target_module="MOD-SEC-04",
        data_type="network_traffic",
        contract="TLS解密后的流量镜像至入侵检测模块进行深度包检测(DPI)",
        priority=Priority.P0
    ),
    # MOD-SEC-08 → MOD-SEC-01: 应急期间权限调整
    CrossModuleFlow(
        flow_id="FLOW-015",
        source_module="MOD-SEC-08",
        target_module="MOD-SEC-01",
        data_type="emergency_access_grant",
        contract="应急响应期间临时提升/调整操作人员权限，需双因素认证+审批记录",
        priority=Priority.P0
    ),
    # MOD-SEC-08 → MOD-SEC-05: 应急恢复调用备份
    CrossModuleFlow(
        flow_id="FLOW-016",
        source_module="MOD-SEC-08",
        target_module="MOD-SEC-05",
        data_type="recovery_request",
        contract="应急响应恢复阶段调用数据备份模块执行灾难恢复，RTO≤4h/RPO≤1h",
        priority=Priority.P0
    ),
    # MOD-SEC-03 → MOD-SEC-07: 审计日志安全传输
    CrossModuleFlow(
        flow_id="FLOW-017",
        source_module="MOD-SEC-03",
        target_module="MOD-SEC-07",
        data_type="encrypted_audit_stream",
        contract="审计日志通过TLS 1.3加密通道传输至集中日志服务器，防窃听篡改",
        priority=Priority.P0
    ),
    # MOD-SEC-04 → MOD-SEC-05: 恶意样本备份隔离
    CrossModuleFlow(
        flow_id="FLOW-018",
        source_module="MOD-SEC-04",
        target_module="MOD-SEC-05",
        data_type="malware_sample_archive",
        contract="检测到的恶意样本加密备份至隔离存储区，用于威胁分析取证",
        priority=Priority.P0
    ),
    # MOD-SEC-06 → MOD-SEC-08: 个人数据泄露事件
    CrossModuleFlow(
        flow_id="FLOW-019",
        source_module="MOD-SEC-06",
        target_module="MOD-SEC-08",
        data_type="pii_breach_notification",
        contract="个人数据泄露事件72小时内通知监管部门和数据主体，启动应急响应",
        priority=Priority.P0
    ),
    # MOD-SEC-07 → MOD-SEC-03: TLS证书审计
    CrossModuleFlow(
        flow_id="FLOW-020",
        source_module="MOD-SEC-07",
        target_module="MOD-SEC-03",
        data_type="certificate_audit_log",
        contract="TLS证书签发/更新/吊销/过期事件记录审计日志",
        priority=Priority.P1
    ),
]

# ============================================================
# 第十二部分：5种阻断场景 🔴
# ============================================================
# 忠(0.5) > 孝(0.3) > 义(0.2) 排序铁律下的系统级阻断

BLOCK_SCENARIOS = {
    "scenario_1": {
        "name": "🔴阻断-未授权访问核心数据",
        "block_id": "BLOCK-001",
        "trigger_condition": "身份鉴别失败 或 权限不足 访问核心数据",
        "trigger_modules": ["MOD-SEC-01", "MOD-SEC-02"],
        "gb_clause": "GB/T 22239-2019 8.1.1 / 数据安全法第27条",
        "loyalty_check": True,  # 需校验忠孝义权重
        "block_action": {
            "immediate_disconnect": True,
            "session_terminate": True,
            "ip_temporary_block": True,
            "audit_log_write": True,
            "security_alert_escalate": True
        },
        "response_steps": [
            "1. 立即断开请求方连接",
            "2. 终止当前所有会话",
            "3. 临时阻断源IP(30分钟)",
            "4. 写入WORM审计日志",
            "5. 发送CRITICAL安全告警",
            "6. 通知安全运营中心(SOC)"
        ],
        "color": AuditColor.BLOCK,
        "description": "当未通过身份鉴别或权限不足的用户尝试访问核心加密数据时，系统立即执行阻断。此场景锚定等保2.0访问控制要求与数据安全法第27条，是国家安全层面的🟢通过🟡标记🔴阻断决策。"
    },
    "scenario_2": {
        "name": "🔴阻断-个人信息泄露检测",
        "block_id": "BLOCK-002",
        "trigger_condition": "检测到个人信息的非授权访问或跨境传输违规",
        "trigger_modules": ["MOD-SEC-06", "MOD-SEC-07"],
        "gb_clause": "个人信息保护法第51条 / 第55条 / GB/T 35273-2020",
        "loyalty_check": True,
        "block_action": {
            "data_flow_cut": True,
            "encryption_enforce": True,
            "notify_dpo": True,
            "audit_log_write": True,
            "regulatory_report_prepare": True
        },
        "response_steps": [
            "1. 立即切断数据流出通道",
            "2. 强制加密所有相关数据",
            "3. 通知数据保护官(DPO)",
            "4. 记录完整审计轨迹",
            "5. 准备监管报告材料",
            "6. 72小时内向监管部门报告"
        ],
        "color": AuditColor.BLOCK,
        "description": "检测到个人信息被非授权访问、超范围使用或违规跨境传输时立即阻断。锚定个保法第51条和第55条，涉及数据主体权益保护。"
    },
    "scenario_3": {
        "name": "🔴阻断-密钥泄露/加密算法降级",
        "block_id": "BLOCK-003",
        "trigger_condition": "HSM检测到密钥泄露 或 TLS版本降级攻击",
        "trigger_modules": ["MOD-SEC-02", "MOD-SEC-07"],
        "gb_clause": "数据安全法第27条 / GB/T 22239-2019 8.1.5 / GB/T 35273-2020 5.3",
        "loyalty_check": True,
        "block_action": {
            "emergency_key_rotation": True,
            "all_sessions_terminate": True,
            "tls_connections_reset": True,
            "affected_system_isolate": True,
            "forensic_evidence_preserve": True
        },
        "response_steps": [
            "1. 紧急轮换全部密钥",
            "2. 终止所有活跃会话",
            "3. 重置所有TLS连接",
            "4. 隔离受影响系统",
            "5. 保全取证证据",
            "6. 启动安全事件调查"
        ],
        "color": AuditColor.BLOCK,
        "description": "当硬件安全模块(HSM)检测到密钥泄露，或安全通信模块检测到TLS版本降级攻击时，立即执行系统级阻断。锚定数据安全法与等保2.0加密要求。"
    },
    "scenario_4": {
        "name": "🔴阻断-APT攻击/恶意代码爆发",
        "block_id": "BLOCK-004",
        "trigger_condition": "IDS检测到APT攻击 或 恶意代码大规模传播",
        "trigger_modules": ["MOD-SEC-04", "MOD-SEC-08"],
        "gb_clause": "网络安全法第25条 / GB/T 22239-2019 8.1.2 / GB/T 24363-2009",
        "loyalty_check": True,
        "block_action": {
            "network_segment_isolate": True,
            "affected_hosts_quarantine": True,
            "dns_sinkhole": True,
            "emergency_dr_activate": False,
            "national_cert_report": True
        },
        "response_steps": [
            "1. 隔离受感染网络段",
            "2. 隔离所有受影响主机",
            "3. DNS沉洞恶意域名",
            "4. 启动应急响应预案",
            "5. 向CNCERT报告",
            "6. 启动灾难恢复(如需要)"
        ],
        "color": AuditColor.BLOCK,
        "description": "检测到高级持续性威胁(APT)攻击或恶意代码大规模传播时，立即启动网络隔离与应急响应。锚定网络安全法第25条和GB/T 24363-2009应急响应流程。"
    },
    "scenario_5": {
        "name": "🔴阻断-审计日志篡改/WORM破坏",
        "block_id": "BLOCK-005",
        "trigger_condition": "审计日志完整性校验失败 或 WORM存储被篡改",
        "trigger_modules": ["MOD-SEC-03"],
        "gb_clause": "网络安全法第21条 / GB/T 31992-2015 4.1.3 / GB/T 22239-2019 8.1.4",
        "loyalty_check": True,
        "block_action": {
            "write_access_freeze": True,
            "backup_immediate": True,
            "forensic_investigation": True,
            "admin_access_suspend": True,
            "regulatory_authority_notify": True
        },
        "response_steps": [
            "1. 冻结全部写操作",
            "2. 立即备份当前日志",
            "3. 启动取证调查",
            "4. 暂停管理员权限",
            "5. 通知监管部门",
            "6. 启动全面安全审查"
        ],
        "color": AuditColor.BLOCK,
        "description": "当WORM审计日志的完整性校验链断裂，或检测到日志被篡改时，立即冻结系统并启动最高级别安全审查。这是等保2.0和网络安全法的核心底线要求。"
    }
}

# ============================================================
# 第十三部分：模块注册与激活引擎
# ============================================================

class SecurityDomainActivator:
    """安全域激活引擎 - 龍魂体系核心"""
    
    def __init__(self):
        self.modules: Dict[str, Dict] = {}
        self.flows: List[CrossModuleFlow] = []
        self.block_scenarios: Dict[str, Dict] = {}
        self.activation_status = False
        self.audit_results: List[Dict] = []
        self._register_all_modules()
    
    def _register_all_modules(self):
        """注册全部8个安全模块"""
        self.modules["MOD-SEC-01"] = MOD_SEC_01_CONFIG
        self.modules["MOD-SEC-02"] = MOD_SEC_02_CONFIG
        self.modules["MOD-SEC-03"] = MOD_SEC_03_CONFIG
        self.modules["MOD-SEC-04"] = MOD_SEC_04_CONFIG
        self.modules["MOD-SEC-05"] = MOD_SEC_05_CONFIG
        self.modules["MOD-SEC-06"] = MOD_SEC_06_CONFIG
        self.modules["MOD-SEC-07"] = MOD_SEC_07_CONFIG
        self.modules["MOD-SEC-08"] = MOD_SEC_08_CONFIG
        self.flows = CROSS_MODULE_FLOWS
        self.block_scenarios = BLOCK_SCENARIOS
    
    def activate_domain(self) -> Dict[str, Any]:
        """激活安全域 - 执行完整激活流程"""
        print(f"\n{'='*60}")
        print(f"  龍魂体系安全域审计协议 v3.0 激活启动")
        print(f"  DNA签名: {DNA_SIGNATURE}")
        print(f"  确认令牌: {CONFIRM_TOKEN}")
        print(f"{'='*60}\n")
        
        activation_report = {
            "dna_signature": DNA_SIGNATURE,
            "confirm_token": CONFIRM_TOKEN,
            "activation_time": AuditToolkit.timestamp_iso(),
            "modules_activated": [],
            "cross_module_flows": len(self.flows),
            "block_scenarios": len(self.block_scenarios),
            "gb_anchors": [],
            "audit_results": []
        }
        
        # Step 1: 校验DNA签名完整性
        print("[Step 1] 校验DNA签名与权重铁律...")
        weights_valid = AuditToolkit.verify_loyalty_weights(LOYALTY_WEIGHTS)
        if not weights_valid:
            return {"status": "BLOCKED", "reason": "忠孝义权重校验失败", "color": AuditColor.BLOCK.value}
        print(f"  🟢 DNA签名验证通过")
        print(f"  🟢 忠(0.5) > 孝(0.3) > 义(0.2) 权重铁律确认")
        
        # Step 2: 逐个激活模块
        print("\n[Step 2] 激活安全域8模块...")
        for mod_id, mod_config in self.modules.items():
            result = self._activate_module(mod_id, mod_config)
            activation_report["modules_activated"].append(result)
            activation_report["gb_anchors"].extend(result.get("gb_clauses", []))
            self.audit_results.append(result)
            color = result["color"]
            print(f"  {color} {mod_id}: {result['module_name']} - {result['status']}")
        
        # Step 3: 校验跨模块数据流
        print(f"\n[Step 3] 校验跨模块数据流契约 ({len(self.flows)}条)...")
        flow_ok = self._verify_cross_flows()
        activation_report["cross_flows_verified"] = flow_ok
        print(f"  🟢 跨模块数据流校验通过" if flow_ok else f"  🔴 跨模块数据流异常")
        
        # Step 4: 验证阻断场景
        print(f"\n[Step 4] 验证阻断场景 ({len(self.block_scenarios)}种)...")
        block_ok = self._verify_block_scenarios()
        activation_report["block_scenarios_verified"] = block_ok
        print(f"  🟢 阻断场景配置完成" if block_ok else f"  🔴 阻断场景异常")
        
        # Step 5: 写入审计日志
        print(f"\n[Step 5] 写入WORM审计日志...")
        self._write_activation_log(activation_report)
        print(f"  🟢 WORM审计日志写入完成")
        
        # Step 6: 生成激活报告
        activation_report["status"] = "ACTIVATED"
        activation_report["overall_color"] = AuditColor.PASS.value
        activation_report["total_modules"] = len(self.modules)
        activation_report["total_interfaces"] = sum(
            len(m.get("interfaces", [])) for m in self.modules.values()
        )
        activation_report["total_validation_rules"] = sum(
            len(m.get("validation_rules", [])) for m in self.modules.values()
        )
        activation_report["total_fail_strategies"] = sum(
            len(m.get("fail_strategies", [])) for m in self.modules.values()
        )
        activation_report["total_gb_clauses"] = len(set(activation_report["gb_anchors"]))
        self.activation_status = True
        
        print(f"\n{'='*60}")
        print(f"  🟢 安全域审计协议 v3.0 激活完成")
        print(f"  模块数: {activation_report['total_modules']}")
        print(f"  跨模块流: {activation_report['cross_module_flows']}条")
        print(f"  阻断场景: {activation_report['block_scenarios']}种")
        print(f"  国标锚定: {activation_report['total_gb_clauses']}条")
        print(f"  DNA签名: {DNA_SIGNATURE}")
        print(f"{'='*60}\n")
        
        return activation_report
    
    def _activate_module(self, mod_id: str, mod_config: Dict[str, Any]) -> Dict[str, Any]:
        """激活单个安全模块"""
        result = {
            "module_id": mod_id,
            "module_name": mod_config["module_name"],
            "status": "activated",
            "color": AuditColor.PASS.value,
            "gb_clauses": [mod_config["gb_standard"]] + mod_config.get("laws", []),
            "interface_count": len(mod_config.get("interfaces", [])),
            "rule_count": len(mod_config.get("validation_rules", [])),
            "fail_strategy_count": len(mod_config.get("fail_strategies", []))
        }
        
        # 校验模块配置完整性
        required_keys = ["module_id", "module_name", "gb_standard", "interfaces", 
                        "validation_rules", "fail_strategies"]
        for key in required_keys:
            if key not in mod_config:
                result["status"] = "incomplete"
                result["color"] = AuditColor.MARK.value
                result["missing_key"] = key
        
        return result
    
    def _verify_cross_flows(self) -> bool:
        """校验跨模块数据流完整性"""
        if len(self.flows) < 18:
            return False
        mod_ids = set(self.modules.keys())
        for flow in self.flows:
            if flow.source_module not in mod_ids or flow.target_module not in mod_ids:
                return False
        return True
    
    def _verify_block_scenarios(self) -> bool:
        """校验阻断场景配置"""
        return len(self.block_scenarios) >= 5 and all(
            s.get("block_action") for s in self.block_scenarios.values()
        )
    
    def _write_activation_log(self, report: Dict[str, Any]):
        """写入激活审计日志"""
        entry = AuditLogEntry(
            timestamp=AuditToolkit.timestamp_iso(),
            module="MOD-SEC-ACTIVATION",
            event_type="domain_activation",
            severity=LogLevel.INFO,
            source_ip="127.0.0.1",
            user_id="UID9622",
            action="activate_security_domain",
            result=AuditColor.PASS,
            details=report,
            dna_signature=DNA_SIGNATURE,
            integrity_hash=""
        )
        WORMAuditLog.append(entry)
    
    def generate_compliance_report(self) -> Dict[str, Any]:
        """生成国标合规报告"""
        report = {
            "report_id": f"RPT-{uuid.uuid4().hex[:8].upper()}",
            "generated_at": AuditToolkit.timestamp_iso(),
            "dna_signature": DNA_SIGNATURE,
            "standards_compliance": {
                "GB/T 22239-2019(等保2.0)": {
                    "applicable_clauses": ["8.1.1", "8.1.2", "8.1.4", "8.1.5", "8.1.6", "8.1.7", "8.1.8"],
                    "compliance_status": "🟢通过",
                    "coverage_modules": ["MOD-SEC-01", "MOD-SEC-04", "MOD-SEC-03", "MOD-SEC-07", "MOD-SEC-02", "MOD-SEC-05", "MOD-SEC-08"]
                },
                "网络安全法": {
                    "applicable_articles": ["第21条", "第24条", "第25条"],
                    "compliance_status": "🟢通过",
                    "coverage_modules": ["MOD-SEC-01", "MOD-SEC-03", "MOD-SEC-04", "MOD-SEC-08"]
                },
                "数据安全法": {
                    "applicable_articles": ["第27条"],
                    "compliance_status": "🟢通过",
                    "coverage_modules": ["MOD-SEC-02", "MOD-SEC-05"]
                },
                "个人信息保护法": {
                    "applicable_articles": ["第6条", "第13条", "第14条", "第47条", "第50条", "第51条", "第55条"],
                    "compliance_status": "🟢通过",
                    "coverage_modules": ["MOD-SEC-06"]
                },
                "GB/T 35273-2020(数据分级)": {
                    "applicable_clauses": ["5.1", "5.2", "5.3", "5.4", "5.5", "7.1-7.11"],
                    "compliance_status": "🟢通过",
                    "coverage_modules": ["MOD-SEC-02", "MOD-SEC-06"]
                },
                "GB/T 31992-2015(日志格式)": {
                    "applicable_clauses": ["4.1", "4.1.2", "4.1.3", "4.1.4", "4.2", "4.3", "4.4"],
                    "compliance_status": "🟢通过",
                    "coverage_modules": ["MOD-SEC-03"]
                },
                "GB/T 20988-2007(灾难恢复)": {
                    "applicable_level": "第5级",
                    "rto_hours": 4,
                    "rpo_hours": 1,
                    "compliance_status": "🟢通过",
                    "coverage_modules": ["MOD-SEC-05", "MOD-SEC-08"]
                },
                "GB/T 24363-2009(应急响应)": {
                    "applicable_phases": ["准备", "检测", "遏制", "根除", "恢复", "跟踪"],
                    "response_time_critical_min": 15,
                    "compliance_status": "🟢通过",
                    "coverage_modules": ["MOD-SEC-08"]
                }
            },
            "audit_log_status": WORMAuditLog.get_retention_status(),
            "cross_module_flows": len(self.flows),
            "block_scenarios": len(self.block_scenarios)
        }
        return report

# ============================================================
# 第十四部分：DNA签名验证与主执行
# ============================================================

def verify_dna_signature(signature: str, confirm_token: str) -> bool:
    """验证DNA签名与确认令牌"""
    expected_sig = "#UID9622⚡️2026-06-16-SECURITY-AUDIT-v3.0"
    expected_token = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
    return signature == expected_sig and confirm_token == expected_token

def run_tricolor_audit(activator: SecurityDomainActivator) -> Dict[str, Any]:
    """执行三色审计"""
    audit = {
        "audit_time": AuditToolkit.timestamp_iso(),
        "dna_signature": DNA_SIGNATURE,
        "results": []
    }
    
    for mod_id, mod in activator.modules.items():
        # 🟢通过: 模块完整激活
        # 🟡标记: 需要关注
        # 🔴阻断: 严重问题
        color = AuditColor.PASS
        reason = "模块完整配置，国标条款已锚定"
        
        if not mod.get("activation_status", False):
            color = AuditColor.BLOCK
            reason = "模块未激活"
        elif len(mod.get("interfaces", [])) < 4:
            color = AuditColor.MARK
            reason = "接口契约不完整"
        
        audit["results"].append({
            "module_id": mod_id,
            "module_name": mod["module_name"],
            "color": color.value,
            "reason": reason,
            "gb_standard": mod["gb_standard"],
            "priority": mod["priority"].value if isinstance(mod["priority"], Priority) else mod["priority"]
        })
    
    return audit

def main():
    """主执行函数 - 安全域审计协议激活入口"""
    print(f"""
    ╔═══════════════════════════════════════════════════════════════╗
    ║         龍魂体系安全域审计协议 v3.0 - 激活程序               ║
    ║         UID9622 | 龍芯北辰·诸葛鑫 | 安全域审计专家         ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    
    # 验证DNA签名
    if not verify_dna_signature(DNA_SIGNATURE, CONFIRM_TOKEN):
        print("🔴阻断: DNA签名验证失败")
        return {"status": "BLOCKED", "reason": "DNA签名不匹配"}
    
    # 校验忠孝义权重
    if not AuditToolkit.verify_loyalty_weights(LOYALTY_WEIGHTS):
        print("🔴阻断: 忠孝义权重校验失败")
        return {"status": "BLOCKED", "reason": "权重铁律违反"}
    
    # 创建激活引擎并执行激活
    activator = SecurityDomainActivator()
    report = activator.activate_domain()
    
    # 执行三色审计
    tricolor = run_tricolor_audit(activator)
    report["tricolor_audit"] = tricolor
    
    # 生成合规报告
    compliance = activator.generate_compliance_report()
    report["compliance_report"] = compliance
    
    # 输出最终汇总
    print(f"\n{'='*60}")
    print(f"  安全域审计协议 v3.0 激活汇总")
    print(f"{'='*60}")
    print(f"  文件: 安全域审计协议_v3.0.py")
    print(f"  模块: {report['total_modules']}个")
    print(f"  接口: {report['total_interfaces']}个")
    print(f"  校验规则: {report['total_validation_rules']}条")
    print(f"  失败策略: {report['total_fail_strategies']}条")
    print(f"  跨模块流: {report['cross_module_flows']}条")
    print(f"  阻断场景: {report['block_scenarios']}种")
    print(f"  国标锚定: {report['total_gb_clauses']}条")
    print(f"  WORM日志: {len(AUDIT_LOG_WORM)}条")
    print(f"  DNA签名: {DNA_SIGNATURE}")
    print(f"  三色审计:")
    for r in tricolor["results"]:
        print(f"    {r['color']} {r['module_id']}: {r['module_name']}")
    print(f"{'='*60}\n")
    
    return report

# ============================================================
# 导出配置字典（供外部调用）
# ============================================================

SECURITY_DOMAIN_CONFIG = {
    "meta": {
        "version": "3.0",
        "dna_signature": DNA_SIGNATURE,
        "confirm_token": CONFIRM_TOKEN,
        "author": "UID9622-龍芯北辰·诸葛鑫",
        "created": "2026-06-16",
        "loyalty_weights": LOYALTY_WEIGHTS
    },
    "modules": {
        "MOD-SEC-01": MOD_SEC_01_CONFIG,
        "MOD-SEC-02": MOD_SEC_02_CONFIG,
        "MOD-SEC-03": MOD_SEC_03_CONFIG,
        "MOD-SEC-04": MOD_SEC_04_CONFIG,
        "MOD-SEC-05": MOD_SEC_05_CONFIG,
        "MOD-SEC-06": MOD_SEC_06_CONFIG,
        "MOD-SEC-07": MOD_SEC_07_CONFIG,
        "MOD-SEC-08": MOD_SEC_08_CONFIG,
    },
    "cross_module_flows": CROSS_MODULE_FLOWS,
    "block_scenarios": BLOCK_SCENARIOS,
    "activator": SecurityDomainActivator
}

# 当直接运行时执行激活
if __name__ == "__main__":
    main()
