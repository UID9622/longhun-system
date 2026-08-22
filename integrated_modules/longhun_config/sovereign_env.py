#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
🐉 龍魂/CNSH 主权环境变量加载器
DNA:#龍芯⚡️丙午·甲午·庚申·壬午·䷙大畜-LONGHUN-SOVEREIGN-ENV-v1.0

设计原则：
1. 真实密钥只驻留本地 ~/.longhun/secrets.env，不上传 Git
2. 统一使用 UID9622 主权变量名
3. 向后兼容旧变量名，迁移期间自动回退并告警
4. 中国优先 · 本地优先 · 数据不出本地
"""

import os
import re
import sys
import warnings
from pathlib import Path
from typing import Dict, List, Optional, Sequence


# UID9622 主权变量规范
SOVEREIGN_VARIABLES: Dict[str, List[str]] = {
    # Notion 生态
    "NOTION_TOKEN": ["NOTION_TOKEN"],
    "DB_LU": ["NOTION_BRAIN_DB", "DB_LU"],          # 主脑/核心记忆数据库
    "DB_JQ": ["NOTION_AUDIT_DB_ID", "NOTION_LOG_DB", "DB_JQ"],  # 审计/纪律/日志库
    "DB_AL": ["NOTION_MULTICURRENCY_DB", "DB_AL"],  # 多币种/经济数据库
    "DB_PUB": ["NOTION_MULTICURRENCY_PAGE", "NOTION_PARENT_PAGE_ID", "DB_PUB"],  # 公共页面
    "DB_CLOUD": ["NOTION_TEAM_PARENT_ID", "DB_CLOUD"],  # 团队/云端数据库

    # AI 服务
    "KIMI_API_KEY": ["KIMI_API_KEY"],

    # 身份与加密
    "GPG_FINGERPRINT": ["GPG_FINGERPRINT", "GPG_KEY_ID", "GPG_KEY_FINGERPRINT"],
    "LONGHUN_CONFIRM_CODE": ["LONGHUN_CONFIRM_CODE", "CONFIRM_CODE"],

    # 通讯
    "TELEGRAM_BOT_TOKEN": ["TELEGRAM_BOT_TOKEN", "TELEGRAM_TOKEN"],

    # 大本营/工厂
    "CAMP_IP": ["CAMP_IP", "LONGHUN_CAMP_IP"],
    "LONGHUN_FACTORY_ID": ["LONGHUN_FACTORY_ID"],
    "LONGHUN_FACTORY_SERIAL": ["LONGHUN_FACTORY_SERIAL"],
    "LONGHUN_SUBKEY": ["LONGHUN_SUBKEY"],

    # 数据库
    "DATABASE_URL": ["DATABASE_URL"],
    "LONGHUN_DB_PASSWORD": ["LONGHUN_DB_PASSWORD", "DB_PASSWORD"],
    "LONGHUN_REDIS_PASSWORD": ["LONGHUN_REDIS_PASSWORD", "REDIS_PASSWORD"],

    # 监控
    "DATADOG_API_KEY": ["DATADOG_API_KEY", "DD_API_KEY"],
    "DATADOG_APP_KEY": ["DATADOG_APP_KEY"],
}

# 反向索引：旧名 -> 标准名
_LEGACY_TO_SOV: Dict[str, str] = {}
for _std, _aliases in SOVEREIGN_VARIABLES.items():
    for _alias in _aliases:
        _LEGACY_TO_SOV[_alias] = _std


def _default_secrets_path() -> Path:
    """返回默认本地密钥文件路径"""
    return Path.home() / ".longhun" / "secrets.env"


def _parse_env_line(line: str) -> Optional[tuple]:
    """解析一行 KEY=VALUE，支持 export 前缀与基本引号"""
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    # 去掉 export 前缀
    if line.startswith("export "):
        line = line[len("export "):]
    if "=" not in line:
        return None
    key, value = line.split("=", 1)
    key = key.strip()
    value = value.strip()
    if not key:
        return None
    # 去掉引号
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
        value = value[1:-1]
    return key, value


def load_secrets_env(path: Optional[Path] = None) -> Dict[str, str]:
    """
    加载本地密钥文件到 os.environ。
    仅在变量尚未设置时写入，避免覆盖用户显式 export 的值。
    """
    env_path = path or _default_secrets_path()
    loaded: Dict[str, str] = {}
    if not env_path.exists():
        return loaded
    try:
        with env_path.open("r", encoding="utf-8") as f:
            for line in f:
                parsed = _parse_env_line(line)
                if not parsed:
                    continue
                key, value = parsed
                # 本地文件不覆盖已存在的环境变量，尊重运行时注入
                if os.environ.get(key) is None and value:
                    os.environ[key] = value
                    loaded[key] = value
    except Exception as exc:  # pragma: no cover
        warnings.warn(f"[龍魂] 加载密钥文件失败 {env_path}: {exc}")
    return loaded


# 模块导入时自动加载一次，保证旧代码无需改动即可获得密钥
_auto_loaded = load_secrets_env()


def _warn_once(msg: str):
    """避免重复告警"""
    if msg not in _warn_once._seen:  # type: ignore[attr-defined]
        _warn_once._seen.add(msg)  # type: ignore[attr-defined]
        warnings.warn(msg, stacklevel=3)


_warn_once._seen = set()  # type: ignore[attr-defined]


def getenv(name: str, default: Optional[str] = None, *, legacy_names: Optional[Sequence[str]] = None) -> Optional[str]:
    """
    读取主权变量。优先标准名，若未设置则按 legacy_names 回退。

    Args:
        name: 主权变量名
        default: 全部未找到时的默认值
        legacy_names: 额外的旧变量名（可选）
    """
    # 1. 直接读取标准名
    value = os.environ.get(name)
    if value:
        return value

    # 2. 内置旧名回退
    aliases = list(SOVEREIGN_VARIABLES.get(name, []))
    if legacy_names:
        aliases.extend(legacy_names)

    for alias in aliases:
        if alias == name:
            continue
        value = os.environ.get(alias)
        if value:
            _warn_once(
                f"[龍魂·迁移告警] 变量 '{name}' 未设置，已回退到旧名 '{alias}'。"
                f"请尽快在 ~/.longhun/secrets.env 中改为 {name}={value}"
            )
            return value

    return default


def require(name: str, *, legacy_names: Optional[Sequence[str]] = None) -> str:
    """读取主权变量，缺失时抛出清晰错误"""
    value = getenv(name, legacy_names=legacy_names)
    if not value:
        raise RuntimeError(
            f"[龍魂·配置缺失] 环境变量 '{name}' 未设置。"
            f"请在 ~/.longhun/secrets.env 中添加：\n    export {name}=<你的值>"
        )
    return value


def standardize_environ() -> Dict[str, str]:
    """
    将当前环境中的旧变量名同步到标准名。
    返回实际同步了哪些变量。
    """
    synced: Dict[str, str] = {}
    for std_name, aliases in SOVEREIGN_VARIABLES.items():
        if os.environ.get(std_name):
            continue
        for alias in aliases:
            if alias == std_name:
                continue
            value = os.environ.get(alias)
            if value:
                os.environ[std_name] = value
                synced[std_name] = alias
                break
    return synced


def list_unconfigured(required: Optional[Sequence[str]] = None) -> List[str]:
    """列出未配置的关键变量"""
    required = required or [
        "NOTION_TOKEN",
        "DB_LU",
        "KIMI_API_KEY",
        "GPG_FINGERPRINT",
    ]
    return [name for name in required if not getenv(name)]


if __name__ == "__main__":  # pragma: no cover
    # 自检：打印已加载的变量名（不打印值）
    print("[龍魂] 主权变量加载器自检")
    print(f"  密钥文件: {_default_secrets_path()}")
    print(f"  已自动加载键数: {len(_auto_loaded)}")
    print(f"  未配置关键项: {list_unconfigured()}")
