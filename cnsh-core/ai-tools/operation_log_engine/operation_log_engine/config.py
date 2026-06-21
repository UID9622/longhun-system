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
🧬 龍魂操作日記引擎 · config.py

DNA:#龍芯⚡️2026-05-30-CONFIG-MANAGER-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
責任: UID9622·不免責

統一配置管理系統。所有路徑、設置通過此模組集中管理。
"""

import os
import sys
from pathlib import Path
from typing import Optional


# 在模組加載前，先加載 .env 文件
def _load_env_file():
    """加載 .env 文件到環境變數"""
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
                        # 強制設置環境變數
                        os.environ[key] = value
        except Exception as e:
            print(f"⚠️  警告: 無法加載 .env 文件: {e}")


_load_env_file()


class Config:
    """龍魂系統統一配置管理"""

    # ==================== 路徑配置 ====================

    # 龍魂根目錄
    LONGHUN_ROOT = Path(os.getenv(
        "LONGHUN_ROOT",
        str(Path.home() / "longhun-system")
    )).expanduser().resolve()

    # 引擎根目錄
    ENGINE_ROOT = LONGHUN_ROOT / "cnsh-core/ai-tools/operation_log_engine"

    # 數據目錄
    DATA_DIR = ENGINE_ROOT / ".data"
    BACKUP_DIR = ENGINE_ROOT / ".backup"
    LOG_DIR = ENGINE_ROOT / ".logs"

    # ==================== 核心數據文件 ====================

    # 操作日記
    LEDGER_FILE = DATA_DIR / "ledger.jsonl"

    # DNA 粒子
    DNA_DIR = DATA_DIR / "dna_particles"
    DNA_INDEX_FILE = DATA_DIR / "dna_index.json"

    # 習慣指紋
    BASELINE_FILE = DATA_DIR / "baseline_snapshot.json"
    HABITS_STATS_FILE = DATA_DIR / "habits_stats.json"

    # 設備信息
    DEVICE_SEALS_FILE = DATA_DIR / "device_seals.jsonl"

    # ==================== 同步配置 ====================

    # 同步日誌
    SYNC_LOG_FILE = DATA_DIR / "sync_operations.jsonl"
    CONFLICT_LOG = DATA_DIR / "conflicts.jsonl"

    # USB 同步路徑 (默認)
    USB_MOUNT_PATH = Path(os.getenv(
        "USB_MOUNT_PATH",
        "/Volumes/LONGHUN_USB"  # macOS
    )).expanduser()

    # ==================== 驗證配置 ====================

    # 驗證日誌
    VERIFICATION_LOG = DATA_DIR / "verifications.jsonl"
    ALERTS_LOG = DATA_DIR / "alerts.jsonl"

    # ==================== 性能配置 ====================

    # 批量操作大小
    BATCH_SIZE = int(os.getenv("BATCH_SIZE", "1000"))

    # 緩存 TTL (秒)
    CACHE_TTL = int(os.getenv("CACHE_TTL", "3600"))

    # 操作超時 (秒)
    TIMEOUT = int(os.getenv("TIMEOUT", "30"))

    # 最大查詢結果
    MAX_QUERY_LIMIT = int(os.getenv("MAX_QUERY_LIMIT", "10000"))

    # ==================== 日誌配置 ====================

    # 日誌等級: DEBUG, INFO, WARNING, ERROR, CRITICAL
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # 主日誌文件
    LOG_FILE = LOG_DIR / "engine.log"

    # 分類日誌
    OPERATION_LOG = LOG_DIR / "operations.log"
    SYNC_LOG = LOG_DIR / "sync.log"
    VERIFICATION_LOG_FILE = LOG_DIR / "verification.log"
    ERROR_LOG = LOG_DIR / "errors.log"

    # 日誌輪轉 (MB)
    LOG_MAX_SIZE = int(os.getenv("LOG_MAX_SIZE", "10"))

    # 保留日誌數
    LOG_BACKUP_COUNT = int(os.getenv("LOG_BACKUP_COUNT", "5"))

    # ==================== 應用配置 ====================

    # 應用模式: development, production, testing
    APP_MODE = os.getenv("APP_MODE", "production")

    # 調試模式
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"

    # 版本
    VERSION = "1.0.0"

    # ==================== 敏感操作配置 ====================

    # 需要 3/3 驗證的操作列表
    SENSITIVE_OPERATIONS = [
        "焊接",           # 工程操作
        "規則更新",       # 系統規則變更
        "策略變更",       # 安全策略變更
        "權限授予",       # 權限操作
        "設備綁定",       # 設備管理
        "同步啟動",       # 同步操作
    ]

    # ==================== 驗證配置 ====================

    # UID9622 的硬編碼值 (用於驗證)
    UID_EXPECTED = "UID9622"

    # GPG 公鑰指紋 (用於驗證)
    GPG_KEY_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

    # ==================== 類方法 ====================

    @classmethod
    def validate(cls) -> bool:
        """驗證配置的合法性和完整性"""
        errors = []

        # 檢查龍魂根目錄
        if not cls.LONGHUN_ROOT.exists():
            errors.append(f"龍魂根目錄不存在: {cls.LONGHUN_ROOT}")

        # 檢查引擎根目錄
        if not cls.ENGINE_ROOT.exists():
            errors.append(f"引擎目錄不存在: {cls.ENGINE_ROOT}")

        # 如果有錯誤，返回 False
        if errors:
            for error in errors:
                print(f"❌ 配置錯誤: {error}")
            return False

        return True

    @classmethod
    def init_directories(cls) -> bool:
        """初始化所有必要的目錄"""
        try:
            # 創建數據目錄
            cls.DATA_DIR.mkdir(parents=True, exist_ok=True)

            # 創建備份目錄
            cls.BACKUP_DIR.mkdir(parents=True, exist_ok=True)

            # 創建日誌目錄
            cls.LOG_DIR.mkdir(parents=True, exist_ok=True)

            # 創建 DNA 粒子目錄
            cls.DNA_DIR.mkdir(parents=True, exist_ok=True)

            return True
        except Exception as e:
            print(f"❌ 無法創建目錄: {e}")
            return False

    @classmethod
    def get_config_dict(cls) -> dict:
        """獲取配置字典"""
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
        print("龍魂系統配置")
        print("=" * 60)
        print(json.dumps(config_dict, indent=2, ensure_ascii=False))
        print("=" * 60 + "\n")


# 驗證配置
if not Config.validate():
    print("⚠️  警告: 配置驗證失敗，某些功能可能無法正常工作")

# 初始化目錄
if not Config.init_directories():
    print("⚠️  警告: 無法初始化目錄，某些功能可能無法正常工作")
