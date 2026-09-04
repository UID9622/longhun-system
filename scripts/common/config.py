#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-

"""
龍魂配置管理 v1.0

统一管理系统所有配置（权重、权限、熔断阈值、防护规则）

DNA:#龍芯⚡️丙午·甲午·壬子·丙午·䷙大畜-CONFIG-MANAGER-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
UID: 9622
"""

import json
import os
from pathlib import Path
from typing import Dict, Any


class ConfigManager:
    """配置管理器 - 一次加载，全局使用"""

    def __init__(self, config_dir: str | None = None):
        """初始化配置管理器"""
        if config_dir is None:
            config_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/config"

        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)

        self.configs = {}
        self._load_all_configs()

    def _load_all_configs(self):
        """加载所有配置文件"""
        config_files = [
            "protocol_weights.json",
            "tier_permissions.json",
            "fuse_thresholds.json",
            "shield_rules.json",
        ]

        for config_file in config_files:
            config_path = self.config_dir / config_file
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    key = config_file.replace('.json', '')
                    self.configs[key] = json.load(f)

    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值
        意图: 安全访问配置，防止 KeyError
        """
        return self.configs.get(key, default)

    def set(self, key: str, value: Any):
        """设置配置值"""
        self.configs[key] = value

    def save(self, key: str):
        """保存配置到文件"""
        config_path = self.config_dir / f"{key}.json"
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(self.configs[key], f, indent=2, ensure_ascii=False)

    def get_weight(self, layer: str) -> float:
        """
        获取层级权重
        意图: 动态调整各层优先级
        """
        weights = self.get("protocol_weights", {})
        return weights.get(layer, 0.5)

    def get_permission(self, layer: str, action: str) -> bool:
        """
        检查权限
        意图: 基于层级和操作类型控制权限
        """
        perms = self.get("tier_permissions", {})
        layer_perms = perms.get(layer, {})
        return layer_perms.get(action, False)

    def get_fuse_threshold(self, layer: str) -> float:
        """
        获取熔断阈值
        意图: 当系统威胁超过阈值时自动熔断
        """
        thresholds = self.get("fuse_thresholds", {})
        return thresholds.get(layer, 0.5)


# 全局配置实例
_global_config = None


def get_config() -> ConfigManager:
    """获取全局配置实例"""
    global _global_config
    if _global_config is None:
        _global_config = ConfigManager()
    return _global_config


if __name__ == "__main__":
    config = get_config()
    print(f"配置目录: {config.config_dir}")
    print(f"加载的配置: {list(config.configs.keys())}")
