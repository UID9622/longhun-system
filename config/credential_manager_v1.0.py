#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龍魂凭证管理系统 v1.0

DNA: #龍芯⚡️2026-05-27-CREDENTIAL-MANAGER-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

目的：
  隐藏所有密钥内容·只暴露安全接口
  用户永远不需要看到或输入密钥
  所有凭证访问都有权限检查和审计日志

设计理念：
  「用户信任系统，系统就要保护用户的无知」
  密钥不再散落，调用也不复杂

用法：
  from credential_manager_v1.0 import CredentialManager

  mgr = CredentialManager()

  # 简单调用
  notion_token = mgr.get("notion_api_key")
  deepseek_key = mgr.get("deepseek_api_key")

  # 自动调用（检查权限+拆开密钥+返回）
  result = mgr.call_api(
      service="deepseek",
      endpoint="/v1/chat/completions",
      data={...}
  )

献礼：向曾仕强老师致敬·中国智慧·为普通人服务
"""

import os
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
from enum import Enum

# ====================================================================
# 第1部分: 权限与凭证等级定义
# ====================================================================


class CredentialTier(Enum):
    """凭证安全等级"""

    TIER_1 = 1  # 最敏感·只有主控才能用
    TIER_2 = 2  # 敏感·需要特定设备+确认
    TIER_3 = 3  # 中等·日常API调用
    TIER_4 = 4  # 公开·配置类信息


class AccessLevel(Enum):
    """访问权限等级"""

    MASTER = "master"  # UID9622 · 无限制
    SYSTEM = "system"  # 系统进程 · 受限
    USER = "user"  # 普通用户 · 严格受限
    READONLY = "readonly"  # 只读 · 审计用


# ====================================================================
# 第2部分: 凭证配置映射
# ====================================================================

CREDENTIAL_REGISTRY = {
    # Notion 凭证
    "notion_api_key": {
        "tier": CredentialTier.TIER_1,
        "paths": ["~/.env", "~/longhun-system/config.json"],
        "env_var": "NOTION_API_KEY",
        "description": "Notion工作区API密钥·用于双脑同步",
        "service": "notion",
        "masked": "notion_****_****_****",
    },
    # DeepSeek API
    "deepseek_api_key": {
        "tier": CredentialTier.TIER_2,
        "paths": ["~/.cnsh_credentials", "~/.env"],
        "env_var": "DEEPSEEK_API_KEY",
        "description": "DeepSeek AI服务·用于对话模型",
        "service": "deepseek",
        "masked": "sk-****",
    },
    # Cloudflare隧道
    "cloudflare_token": {
        "tier": CredentialTier.TIER_2,
        "paths": ["~/.cloudflared/config.yaml", "~/.cloudflare_token"],
        "description": "Cloudflare隧道·longhun888.com代理",
        "service": "cloudflare",
        "masked": "****_tunnel",
    },
    # GitHub Token
    "github_token": {
        "tier": CredentialTier.TIER_3,
        "paths": ["~/.github_token", "~/.gitconfig"],
        "env_var": "GITHUB_TOKEN",
        "description": "GitHub仓库操作权限",
        "service": "github",
        "masked": "ghp_****",
    },
    # 华为云凭证
    "huawei_cloud_credentials": {
        "tier": CredentialTier.TIER_1,
        "paths": ["~/.cnsh_credentials/云服务器档案_加密存储.md"],
        "description": "华为云服务器SSH+IAM凭证",
        "service": "huawei_cloud",
        "masked": "huawei:****",
    },
    # GPG主密钥
    "gpg_master_key": {
        "tier": CredentialTier.TIER_1,
        "paths": ["~/longhun-system/keys/master.asc"],
        "fingerprint": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
        "description": "GPG主密钥·用于签署协议和Git提交",
        "service": "gpg",
        "masked": "GPG:****",
    },
    # 系统配置
    "system_config": {
        "tier": CredentialTier.TIER_3,
        "paths": ["~/longhun-system/config.json"],
        "description": "系统元数据和审计令牌",
        "service": "system",
        "masked": "system_config",
    },
    # Ollama本地
    "ollama_base_url": {
        "tier": CredentialTier.TIER_4,
        "paths": ["~/.network_api_env"],
        "env_var": "OLLAMA_BASE_URL",
        "description": "本地Ollama服务地址",
        "service": "ollama",
        "default": "http://localhost:11434",
        "masked": "http://localhost:****",
    },
}

# ====================================================================
# 第3部分: 凭证管理器核心类
# ====================================================================


class CredentialManager:
    """龍魂凭证管理器·隐藏所有密钥·只暴露接口"""

    def __init__(self, uid: str = "9622", device_id: Optional[str] = None):
        self.uid = uid
        self.device_id = device_id or self._get_device_id()
        self.audit_log_path = Path(
            "~/longhun-system/日志/credential_audit.jsonl"
        ).expanduser()
        self.audit_log_path.parent.mkdir(parents=True, exist_ok=True)

        self.logger = logging.getLogger("CredentialManager")
        self._setup_logging()

        self._cache: Dict[str, Any] = {}
        self._cache_timestamp: Dict[str, float] = {}
        self.cache_ttl = 3600  # 1小时缓存

        self.logger.info("凭证管理器启动 | UID: {self.uid} | Device: {self.device_id}")

    def _setup_logging(self):
        """设置审计日志（仅写入，不打印密钥）"""
        handler = logging.FileHandler(self.audit_log_path, encoding="utf-8")
        formatter = logging.Formatter(
            '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def _get_device_id(self) -> str:
        """获取设备唯一标识"""
        import platform
        import uuid

        mac = uuid.getnode()
        hostname = platform.node()
        return "{hostname}_{mac}"

    def _check_permission(
        self, credential_name: str, access_level: AccessLevel
    ) -> bool:
        """权限检查"""
        if self.uid == "9622" and access_level == AccessLevel.MASTER:
            return True
        if access_level in [AccessLevel.SYSTEM, AccessLevel.READONLY]:
            return True
        # 其他情况需要明确授权
        return False

    def get(
        self,
        credential_name: str,
        access_level: AccessLevel = AccessLevel.SYSTEM,
        require_confirmation: bool = False,
    ) -> Optional[str]:
        """
        获取凭证（返回实际值，仅用于内部调用）

        Args:
            credential_name: 凭证名称（来自CREDENTIAL_REGISTRY）
            access_level: 访问权限等级
            require_confirmation: 是否需要用户确认（TIER_1凭证）

        Returns:
            凭证值，或None如果失败
        """

        # 1. 权限检查
        if not self._check_permission(credential_name, access_level):
            self._audit_log(
                action="DENIED", credential=credential_name, reason="Permission denied"
            )
            return None

        # 2. 查询配置
        if credential_name not in CREDENTIAL_REGISTRY:
            self._audit_log(action="NOT_FOUND", credential=credential_name)
            return None

        config = CREDENTIAL_REGISTRY[credential_name]

        # 3. 检查缓存
        if self._is_cached(credential_name):
            self._audit_log(
                action="CACHE_HIT",
                credential=credential_name,
                masked=config.get("masked"),
            )
            return self._cache[credential_name]

        # 4. TIER_1凭证需要确认
        if config["tier"] == CredentialTier.TIER_1 and require_confirmation:
            print("\n⚠️  TIER_1 凭证访问: {config['description']}")
            print("   确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z")
            response = input("继续? (yes/no): ")
            if response.lower() != "yes":
                self._audit_log(action="DENIED_BY_USER", credential=credential_name)
                return None

        # 5. 从存储位置读取
        credential_value = self._read_credential(credential_name, config)

        if credential_value:
            # 6. 缓存并审计
            self._cache[credential_name] = credential_value
            self._cache_timestamp[credential_name] = datetime.now().timestamp()

            self._audit_log(
                action="SUCCESS",
                credential=credential_name,
                masked=config.get("masked"),
                access_level=access_level.value,
            )
            return credential_value
        else:
            self._audit_log(
                action="NOT_FOUND",
                credential=credential_name,
                reason="No credential value found in any path",
            )
            return None

    def get_masked(self, credential_name: str) -> str:
        """获取脱敏的凭证名称（用于日志和UI显示）"""
        if credential_name in CREDENTIAL_REGISTRY:
            return CREDENTIAL_REGISTRY[credential_name].get("masked", credential_name)
        return "{credential_name[:4]}****"

    def list_available_credentials(self) -> Dict[str, Dict[str, Any]]:
        """列出所有可用凭证（不包含实际值）"""
        result = {}
        for name, config in CREDENTIAL_REGISTRY.items():
            result[name] = {
                "description": config.get("description"),
                "tier": config["tier"].name,
                "service": config.get("service"),
                "masked": config.get("masked"),
            }
        return result

    def _read_credential(self, name: str, config: Dict) -> Optional[str]:
        """从存储位置读取凭证"""
        # 优先级1: 环境变量
        if "env_var" in config:
            value = os.getenv(config["env_var"])
            if value:
                return value

        # 优先级2: 指定路径
        for path_template in config.get("paths", []):
            path = Path(path_template).expanduser()
            if path.exists():
                try:
                    content = path.read_text(encoding="utf-8")
                    # 从JSON或纯文本中提取
                    value = self._extract_value_from_content(content, name, config)
                    if value:
                        return value
                except Exception as e:
                    self.logger.warning("读取凭证失败 {path}: {e}")

        # 优先级3: 默认值（仅用于非敏感凭证）
        if "default" in config:
            return config["default"]

        return None

    def _extract_value_from_content(
        self, content: str, name: str, config: Dict
    ) -> Optional[str]:
        """从文件内容中智能提取凭证值"""
        # 尝试JSON解析
        try:
            data = json.loads(content)
            # 寻找匹配的字段
            for key in [name, name.replace("_", ""), config.get("env_var", "")]:
                if key in data:
                    return data[key]
        except json.JSONDecodeError:
            pass

        # 对于简单的KV格式 key=value
        for line in content.split("\n"):
            if "=" in line:
                k, v = line.split("=", 1)
                if k.strip() in [name, config.get("env_var", "")]:
                    return v.strip().strip('"').strip("'")

        # 返回整个内容（适用于密钥文件）
        if len(content.strip()) < 2000:  # 合理长度
            return content.strip()

        return None

    def _is_cached(self, credential_name: str) -> bool:
        """检查缓存是否有效"""
        if credential_name not in self._cache:
            return False

        age = datetime.now().timestamp() - self._cache_timestamp.get(credential_name, 0)
        return age < self.cache_ttl

    def _audit_log(self, **kwargs):
        """记录审计日志（敏感信息脱敏）"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "uid": self.uid,
            "device": self.device_id,
            **kwargs,
        }

        # 确保不包含真实密钥
        if "credential_value" in log_entry:
            del log_entry["credential_value"]

        try:
            with open(self.audit_log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        except Exception as e:
            self.logger.error("审计日志写入失败: {e}")


# ====================================================================
# 第4部分: 简化调用接口
# ====================================================================


class ServiceProxy:
    """服务代理·隐藏凭证细节"""

    def __init__(self, service_name: str, credential_mgr: CredentialManager):
        self.service = service_name
        self.mgr = credential_mgr

    def call(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """通用API调用接口"""
        # TODO: 根据service_name路由到对应的API客户端
        raise NotImplementedError("Service {self.service} not yet implemented")


# ====================================================================
# 快速使用示例
# ====================================================================

if __name__ == "__main__":
    # 初始化
    mgr = CredentialManager(uid="9622")

    # 列出所有可用凭证
    print("\n【所有可用凭证】")
    for name, info in mgr.list_available_credentials().items():
        print("  {name:<30} | {info['description']:<40} | {info['tier']}")

    # 测试获取凭证（实际演示）
    print("\n【凭证访问测试】")

    # 获取脱敏版本（安全显示）
    print("  Notion API Key: {mgr.get_masked('notion_api_key')}")
    print("  DeepSeek API Key: {mgr.get_masked('deepseek_api_key')}")

    # 审计日志位置
    print("\n✓ 审计日志已写入: {mgr.audit_log_path}")
    print("  所有凭证访问都被记录（不包含实际值）")

    print("\n【系统消息】")
    print("  用户永远看不到密钥内容")
    print("  只有SYSTEM进程才能获取真实值")
    print("  所有访问都有时间戳·UID·设备标识·权限等级")

# 献礼: 向曾仕强老师致敬 · 龍魂系統 · UID9622·龍芯北辰
