#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂插件沙箱 · 插件加载器 v1.0
DNA: #龍芯⚡️2026-08-22-PLUGIN-LOADER-v1.0
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""

import json
import importlib.util
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field

@dataclass
class PluginManifest:
    """插件元数据"""
    id: str
    name: str
    version: str
    description: str
    author: str
    capabilities: List[str] = field(default_factory=list)
    entry: str = "main.py"
    timeout: int = 30

class PluginLoader:
    """插件加载器 · 每个插件必须有 plugin.json · 严格限制上下文"""

    PLUGINS_ROOT = Path(__file__).resolve().parent.parent / "plugins"

    @classmethod
    def get_plugin_path(cls, plugin_id: str) -> Path:
        return cls.PLUGINS_ROOT / plugin_id

    @classmethod
    def load_manifest(cls, plugin_id: str) -> Optional[PluginManifest]:
        plugin_path = cls.get_plugin_path(plugin_id)
        manifest_path = plugin_path / "plugin.json"
        if not manifest_path.exists():
            return None
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return PluginManifest(
                id=data.get("id", plugin_id),
                name=data.get("name", plugin_id),
                version=data.get("version", "0.0.1"),
                description=data.get("description", ""),
                author=data.get("author", "unknown"),
                capabilities=data.get("capabilities", []),
                entry=data.get("entry", "main.py"),
                timeout=data.get("timeout", 30))
        except Exception:
            return None

    @classmethod
    def load_plugin_module(cls, plugin_id: str):
        """加载插件入口模块 (只能加载插件自己的文件)"""
        plugin_path = cls.get_plugin_path(plugin_id)
        manifest = cls.load_manifest(plugin_id)
        if manifest is None:
            raise ValueError(f"无法加载插件清单: {plugin_id}")
        entry_path = plugin_path / manifest.entry
        if not entry_path.exists():
            raise FileNotFoundError(f"插件入口文件不存在: {entry_path}")
        sys.path.insert(0, str(plugin_path))
        spec = importlib.util.spec_from_file_location(f"plugin_{plugin_id}", entry_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module, manifest
