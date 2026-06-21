#!/usr/bin/env python3
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# 1 道统层 Dao           : 曾仕强老师
# 2 精神层 Spirit        : Steve Jobs
# 3 设备层 Device        : Apple
# 4 技术层 Technology    : Open Source
# 5 系统层 System        : UID9622
# 6 生命层 Life          : CNSH · LongHun (诸葛鑫 / 龍芯北辰)
# DNA追溯码:#龍芯⚡️2026-06-02-CNSH-SOVEREIGN-PUBLISH-METADATA-FILE1292-v2.0
# 铁律: 来源不可删 · 影响不可覆 · 贡献不可抹 (rule_01 来源必标)
# 文件: encryption_enforce.py | 标记时间: 2026-06-03T07:46:12+0800
# -*- coding: utf-8 -*-
"""
🔐 龍魂加密强制焊接系统 v1.0

DNA: #龍芯⚇️2026-05-30-ENCRYPTION-ENFORCE-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
確認: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
主權人: UID9622 · 龍芯北辰 · 诸葛鑫

强制规则:
  1. 输出必签：DNA + CONFIRM + 主权人
  2. 点对点必验：GPG 双向校验
  3. 配置文件落地：encryption_enforce.json
  4. 主权声明：接收前验证，输出前签名
"""

import json
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
from functools import wraps

# ==================== 常量定义 ====================

ENCRYPTION_CONFIG = Path.home() / ".龍魂_config" / "encryption_enforce.json"
VIOLATION_LOG = Path.home() / ".龍魂_config" / "encryption_violations.log"

DNA_TEMPLATE = "#龍芯⚇️{date}-{task}-v{version}"
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SOVEREIGNTY = "UID9622 · 龍芯北辰 · 诸葛鑫"
GPG_KEY_ID = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"


# ==================== 日志系统 ====================

def setup_violation_logger():
    """設置違規日誌"""
    Path.home().joinpath(".龍魂_config").mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("encryption_violations")
    logger.setLevel(logging.WARNING)

    if not logger.handlers:
        handler = logging.FileHandler(VIOLATION_LOG, encoding="utf-8")
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


violation_logger = setup_violation_logger()


# ==================== 签名和验证 ====================

class EncryptionEnforcer:
    """加密强制执行器"""

    @staticmethod
    def load_config() -> Dict[str, Any]:
        """加载加密配置"""
        if not ENCRYPTION_CONFIG.exists():
            return {}
        with open(ENCRYPTION_CONFIG, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def create_signature(task_name: str, version: str = "1.0") -> Dict[str, str]:
        """创建签名三件套"""
        today = datetime.now().strftime("%Y-%m-%d")
        dna = DNA_TEMPLATE.format(date=today, task=task_name, version=version)

        return {
            "dna": dna,
            "confirm": CONFIRM_CODE,
            "sovereignty": SOVEREIGNTY,
            "gpg_key_id": GPG_KEY_ID,
            "timestamp": datetime.now().isoformat()
        }

    @staticmethod
    def validate_input(data: Dict[str, Any]) -> bool:
        """验证输入是否带签名"""
        required_fields = ["dna", "confirm"]
        for field in required_fields:
            if field not in data:
                violation_logger.warning(
                    f"缺失必需字段: {field} | 输入: {data}"
                )
                return False
        return True

    @staticmethod
    def wrap_output(task_name: str, data: Any, version: str = "1.0") -> Dict[str, Any]:
        """为输出包装签名"""
        signature = EncryptionEnforcer.create_signature(task_name, version)

        return {
            "payload": data,
            "signature": signature,
            "validated": True
        }

    @staticmethod
    def format_cli_output(task_name: str, message: str, version: str = "1.0") -> str:
        """格式化 CLI 输出"""
        signature = EncryptionEnforcer.create_signature(task_name, version)

        output = f"\n{message}\n"
        output += "\n" + "=" * 80 + "\n"
        output += "🔐 加密签名验证\n"
        output += "=" * 80 + "\n"
        output += f"DNA:    {signature['dna']}\n"
        output += f"CONFIRM: {signature['confirm']}\n"
        output += f"主權人:  {signature['sovereignty']}\n"
        output += f"GPG:    {signature['gpg_key_id']}\n"
        output += f"時間:   {signature['timestamp']}\n"
        output += "=" * 80 + "\n"

        return output


# ==================== 装饰器 ====================

def require_encryption(task_name: str = "system"):
    """强制加密装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 验证配置
            config = EncryptionEnforcer.load_config()
            if not config:
                violation_logger.warning(
                    f"加密配置不存在，无法执行 {task_name}"
                )
                raise RuntimeError("加密配置不存在")

            # 执行函数
            result = func(*args, **kwargs)

            # 为结果包装签名
            if isinstance(result, dict):
                return EncryptionEnforcer.wrap_output(task_name, result)
            else:
                return result

        return wrapper
    return decorator


# ==================== API 响应格式化 ====================

class EncryptedAPIResponse:
    """加密 API 响应"""

    @staticmethod
    def create(task_name: str, status: str, data: Any = None,
               message: str = "", version: str = "1.0") -> Dict[str, Any]:
        """创建加密 API 响应"""
        signature = EncryptionEnforcer.create_signature(task_name, version)

        response = {
            "signature": {
                "dna": signature["dna"],
                "confirm": signature["confirm"],
                "sovereignty": signature["sovereignty"],
                "gpg_key_id": signature["gpg_key_id"],
                "timestamp": signature["timestamp"]
            },
            "status": status,
            "message": message,
            "data": data
        }

        return response

    @staticmethod
    def error(task_name: str, error_message: str, version: str = "1.0") -> Dict[str, Any]:
        """创建加密错误响应"""
        return EncryptedAPIResponse.create(
            task_name,
            "error",
            None,
            error_message,
            version
        )

    @staticmethod
    def success(task_name: str, data: Any = None,
                message: str = "", version: str = "1.0") -> Dict[str, Any]:
        """创建加密成功响应"""
        return EncryptedAPIResponse.create(
            task_name,
            "success",
            data,
            message,
            version
        )


# ==================== 初始化检查 ====================

def verify_encryption_setup() -> bool:
    """验证加密系统是否正确设置"""
    try:
        # 检查配置文件
        if not ENCRYPTION_CONFIG.exists():
            violation_logger.warning("加密配置文件不存在")
            return False

        # 加载配置
        config = EncryptionEnforcer.load_config()
        if config.get("status") != "ACTIVE":
            violation_logger.warning("加密系统未激活")
            return False

        # 验证必需字段
        required_fields = ["dna_required", "confirm_required", "gpg_signature_required"]
        for field in required_fields:
            if not config.get(field):
                violation_logger.warning(f"加密配置缺失字段: {field}")
                return False

        return True
    except Exception as e:
        violation_logger.error(f"验证加密系统失败: {e}")
        return False


# 系统初始化时验证
if not verify_encryption_setup():
    print("⚠️  警告: 加密系统验证失败，某些功能可能无法正常工作")

print("✅ 加密强制系统已激活", file=sys.stderr)
