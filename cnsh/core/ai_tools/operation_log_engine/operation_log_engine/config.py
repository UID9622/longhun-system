#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# 1 道统层 Dao           : 曾仕强老师
# 2 精神层 Spirit        : Steve Jobs
# 3 设备层 Device        : Apple
# 4 技术层 Technology    : Open Source
# 5 系统层 System        : UID9622
# 6 生命层 Life          : CNSH · LongHun (诸葛鑫 / 龍芯北辰)
# DNA追溯码:#龍芯⚡️2026-06-02-CNSH-SOVEREIGN-PUBLISH-METADATA-FILE1293-v2.0
# 铁律: 来源不可删 · 影响不可覆 · 贡献不可抹 (rule_01 来源必标)
# 文件: config.py | 标记时间: 2026-06-03T07:46:12+0800
# -*- coding: utf-8 -*-
"""
🧬 龍魂操作日记引擎 · config.py

DNA:#龍芯⚡️2026-05-30-CONFIG-MANAGER-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
责任: UID9622·不免责

统一配置管理系统。所有路径、设置通过此模组集中管理。
"""

import os
import sys
from pathlib import Path
from typing import Optional, Any


# 在模组加载前，先加载 .env 文件
def _load_env_file():
    """加载 .env 文件到环境变数"""
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        try:
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" in line:
                        key, value = line.split("=", 1)
                        key = key.strip()
                        value = value.strip()
                        # 强制设置环境变数
                        os.environ[key] = value
        except Exception as e:
            print(f"⚠️  警告: 无法加载 .env 文件: {e}")


_load_env_file()


class Config:
    """龍魂系统统一配置管理"""

    # ==================== 路径配置 ====================

    # 龍魂根目录
    LONGHUN_ROOT = Path(os.getenv(
        "LONGHUN_ROOT",
        str(Path.home() / "longhun-system")
    )).expanduser().resolve()

    # 引擎根目录
    ENGINE_ROOT = LONGHUN_ROOT / "cnsh-core/ai-tools/operation_log_engine"

    # 数据目录
    DATA_DIR = ENGINE_ROOT / ".data"
    BACKUP_DIR = ENGINE_ROOT / ".backup"
    LOG_DIR = ENGINE_ROOT / ".logs"

    # ==================== 核心数据文件 ====================

    # 操作日记
    LEDGER_FILE = DATA_DIR / "ledger.jsonl"

    # DNA 粒子
    DNA_DIR = DATA_DIR / "dna_particles"
    DNA_INDEX_FILE = DATA_DIR / "dna_index.json"

    # 习惯指纹
    BASELINE_FILE = DATA_DIR / "baseline_snapshot.json"
    HABITS_STATS_FILE = DATA_DIR / "habits_stats.json"

    # 设备信息
    DEVICE_SEALS_FILE = DATA_DIR / "device_seals.jsonl"

    # ==================== 同步配置 ====================

    # 同步日志
    SYNC_LOG_FILE = DATA_DIR / "sync_operations.jsonl"
    CONFLICT_LOG = DATA_DIR / "conflicts.jsonl"

    # USB 同步路径 (默认)
    USB_MOUNT_PATH = Path(os.getenv(
        "USB_MOUNT_PATH",
        "/Volumes/LONGHUN_USB"  # macOS
    )).expanduser()

    # ==================== 验证配置 ====================

    # 验证日志
    VERIFICATION_LOG = DATA_DIR / "verifications.jsonl"
    ALERTS_LOG = DATA_DIR / "alerts.jsonl"

    # ==================== 性能配置 ====================

    # 批量操作大小
    BATCH_SIZE = int(os.getenv("BATCH_SIZE", "1000"))

    # 缓存 TTL (秒)
    CACHE_TTL = int(os.getenv("CACHE_TTL", "3600"))

    # 操作超时 (秒)
    TIMEOUT = int(os.getenv("TIMEOUT", "30"))

    # 最大查询结果
    MAX_QUERY_LIMIT = int(os.getenv("MAX_QUERY_LIMIT", "10000"))

    # ==================== 日志配置 ====================

    # 日志等级: DEBUG, INFO, WARNING, ERROR, CRITICAL
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # 主日志文件
    LOG_FILE = LOG_DIR / "engine.log"

    # 分类日志
    OPERATION_LOG = LOG_DIR / "operations.log"
    SYNC_LOG = LOG_DIR / "sync.log"
    VERIFICATION_LOG_FILE = LOG_DIR / "verification.log"
    ERROR_LOG = LOG_DIR / "errors.log"

    # 日志轮转 (MB)
    LOG_MAX_SIZE = int(os.getenv("LOG_MAX_SIZE", "10"))

    # 保留日志数
    LOG_BACKUP_COUNT = int(os.getenv("LOG_BACKUP_COUNT", "5"))

    # ==================== 应用配置 ====================

    # 应用模式: development, production, testing
    APP_MODE = os.getenv("APP_MODE", "production")

    # 调试模式
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"

    # 版本
    VERSION = "1.0.0"

    # ==================== 敏感操作配置 ====================

    # 需要 3/3 验证的操作列表
    SENSITIVE_OPERATIONS = [
        "焊接",           # 工程操作
        "规则更新",       # 系统规则变更
        "策略变更",       # 安全策略变更
        "权限授予",       # 权限操作
        "设备绑定",       # 设备管理
        "同步启动",       # 同步操作
    ]

    # ==================== 验证配置 ====================

    # UID9622 的硬编码值 (用于验证)
    UID_EXPECTED = "UID9622"

    # GPG 公钥指纹 (用于验证)
    GPG_KEY_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

    # ==================== 类方法 ====================

    @classmethod
    def validate(cls) -> bool:
        """验证配置的合法性和完整性"""
        errors = []

        # 检查龍魂根目录
        if not cls.LONGHUN_ROOT.exists():
            errors.append(f"龍魂根目录不存在: {cls.LONGHUN_ROOT}")

        # 检查引擎根目录
        if not cls.ENGINE_ROOT.exists():
            errors.append(f"引擎目录不存在: {cls.ENGINE_ROOT}")

        # 如果有错误，返回 False
        if errors:
            for error in errors:
                print(f"❌ 配置错误: {error}")
            return False

        return True

    @classmethod
    def init_directories(cls) -> bool:
        """初始化所有必要的目录"""
        try:
            # 创建数据目录
            cls.DATA_DIR.mkdir(parents=True, exist_ok=True)

            # 创建备份目录
            cls.BACKUP_DIR.mkdir(parents=True, exist_ok=True)

            # 创建日志目录
            cls.LOG_DIR.mkdir(parents=True, exist_ok=True)

            # 创建 DNA 粒子目录
            cls.DNA_DIR.mkdir(parents=True, exist_ok=True)

            return True
        except Exception as e:
            print(f"❌ 无法创建目录: {e}")
            return False

    @classmethod
    def get_config_dict(cls) -> dict[str, Any]:
        """获取配置字典"""
        return {
            "paths": {
                "longhun_root": str(cls.LONGHUN_ROOT),
                "engine_root": str(cls.ENGINE_ROOT),
                "data_dir": str(cls.DATA_DIR),
                "backup_dir": str(cls.BACKUP_DIR),
                "log_dir": str(cls.LOG_DIR),
            },
            "performance": {
                "batch_size": cls.BATCH_SIZE,
                "cache_ttl": cls.CACHE_TTL,
                "timeout": cls.TIMEOUT,
                "max_query_limit": cls.MAX_QUERY_LIMIT,
            },
            "logging": {
                "level": cls.LOG_LEVEL,
                "max_size_mb": cls.LOG_MAX_SIZE,
                "backup_count": cls.LOG_BACKUP_COUNT,
            },
            "application": {
                "mode": cls.APP_MODE,
                "debug": cls.DEBUG,
                "version": cls.VERSION,
            },
        }

    @classmethod
    def print_config(cls) -> None:
        """打印配置信息"""
        import json
        config_dict = cls.get_config_dict()
        print("\n" + "=" * 60)
        print("龍魂系统配置")
        print("=" * 60)
        print(json.dumps(config_dict, indent=2, ensure_ascii=False))
        print("=" * 60 + "\n")


# 验证配置
if not Config.validate():
    print("⚠️  警告: 配置验证失败，某些功能可能无法正常工作")

# 初始化目录
if not Config.init_directories():
    print("⚠️  警告: 无法初始化目录，某些功能可能无法正常工作")
